#!/opt/app-root/bin/python

import subprocess, os
from prometheus_client import start_http_server, Summary, Gauge, Counter
import argparse
import time
import boto3
import botocore
from benedict import benedict

# Generic function to fetch administrative quota values
def getQuotaValue(quotaCode, serviceCode, cSessions):
    paginator = cSessions["service-quotas"].get_paginator("list_service_quotas")
    pCursor = paginator.paginate(ServiceCode=serviceCode, PaginationConfig={"MaxItems": 1000, "PageSize": 10})
    currentValue = 0
    currentQ = 0
    for page in pCursor:
        for quotas in page["Quotas"]:
            if quotas["QuotaCode"] == quotaCode:
                currentQ = str(quotas["Value"])
            currentValue = currentValue + 1
    return currentQ


# fetch actual usage of specific service, works for EIP and Vpcs
def getUsage(cSessions, usageRetrieval, usageFilter):
    awsCall = getattr(cSessions["ec2"], usageRetrieval)
    awsReturns = awsCall()
    return len(awsReturns[usageFilter])


def getAccountID():
    awsSession = boto3.client("sts", aws_access_key_id=args.apikey, aws_secret_access_key=args.secretkey)
    awsReturns = awsSession.get_caller_identity()
    return awsReturns["Account"]


## If we want to fetch the usage for all of the regions on given account
## we'll need to fetch a list of regions available on this particular AWS account
def getRegions():
    awsSession = boto3.client("ec2", aws_access_key_id=args.apikey, aws_secret_access_key=args.secretkey, region_name="us-east-1")
    awsReturns = awsSession.describe_regions()
    if args.debug == True:
        print("Regions fetched from active account: " + str(awsReturns))
    regions = []
    for page in awsReturns["Regions"]:
        regions.append(page["RegionName"])
        if args.debug == True:
            print("Adding " + str(page["RegionName"]) + " to the region list")
    return regions


if __name__ == "__main__":
    # Fetch&parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--apikey", help=" AWS Access Key ID ")
    parser.add_argument("-s", "--secretkey", help=" AWS Sercet Access Key")
    parser.add_argument("-r", "--regions", default="All", help="List of AWS Regions to be used for queries")
    parser.add_argument(
        "-t", "--time", type=int, default=900, help=" Sleep time between fetching the AWS API input"
    )
    parser.add_argument("-d", "--debug", help=" Should we be more verbose?", action="store_true")
    parser.add_argument(
        "-p", "--port", default=8000, help=" TCP port to be used to expose metrics HTTP endpoint"
    )
    parser.add_argument("-m", "--metricsfile", default="./metrics.yaml", help=" Metrics definition file")
    args = parser.parse_args()

    ## Strip regions string from leading and trailing spaces
    aRegions = str(args.regions).strip()

    ## Setting up basic variables
    awsRegions = {}
    awsRegionsList = []

    ## slice the string if we find comma or space between regions names
    if aRegions.find(" ") > 0:
        awsRegionsList = aRegions.split("\s")
        for region in awsRegionsList:
            awsRegions[region] = {}
    elif aRegions.find(",") > 0:
        awsRegionsList = aRegions.split(",")
        for region in awsRegionsList:
            awsRegions[region] = {}
    ## If no region was specified, we're defaulting to "All"
    elif aRegions == "All":
        print("Region parameter was not passed, fetching all available AWS Regions")
        awsRegionsList = getRegions()
        for region in awsRegionsList:
            awsRegions[region] = {}
    ## Falling back to a single specified region
    else:
        if args.debug == True:
            print("Following AWS region will be scraped for data: ")
            awsRegionsList.append(aRegions)
            print(str(awsRegionsList))
        for region in awsRegionsList:
            awsRegions[region] = {}

    print("Loading metrics definition file located at " + str(args.metricsfile))

    # Getting AccountId
    awsAccountID = getAccountID()
    print("Exporter configured to calculate metrics on : " + str(awsAccountID))

    ## Setting initial sessions, per region
    for region in awsRegionsList:
        awsRegions[region]["clientSession"] = {}
        awsRegions[region]["clientSession"]["ec2"] = boto3.client(
            "ec2",
            aws_access_key_id=args.apikey,
            aws_secret_access_key=args.secretkey,
            region_name=region,
        )
        awsRegions[region]["clientSession"]["service-quotas"] = boto3.client(
            "service-quotas",
            aws_access_key_id=args.apikey,
            aws_secret_access_key=args.secretkey,
            region_name=region,
        )

    # Loading up metrics configuration
    promMetrics = benedict(args.metricsfile, format="yaml")
    if args.debug == True:
        print("Metric configuration: ")
        print(str(promMetrics))

    # Initializing Prometheus Gauge metrics
    for metric in promMetrics["values"]:
        if args.debug == True:
            print("Creating metric for " + metric["quotaCode"] + " quota code")
        metric["mObjectUsage"] = Gauge(
            metric["metricNameUsage"], metric["usageDesc"], ["region", "accountid"]
        )
        metric["mObjectQuota"] = Gauge(
            metric["metricNameQuota"], metric["quotaDesc"], ["region", "accountid"]
        )

    ## Setting up Counter metrics to track AWS API call failures
    # Setting variables
    apiCallFailureMetricObjectID = "apiCallFailure"
    apiCallFailureMetricName = "aws_api_failed_requests"
    apiCallFailureMetricDesc = "Counter set on failed AWS API calls"
    apiCallSuccessMetricObjectID = "apiCallSuccess"
    apiCallSuccessMetricName = "aws_api_success_requests"
    apiCallSuccessMetricDesc = "Counter set on succesfull AWS API calls"
    # Initializing metrics
    apiCallFails = Counter(apiCallFailureMetricName, apiCallFailureMetricDesc)
    apiCallSuccess = Counter(apiCallSuccessMetricName, apiCallSuccessMetricDesc)

    # Resetting counters
    apiCallFails.inc(0)
    apiCallSuccess.inc(0)

    ## Initializing HTTP /metrics endpoint for Prometheus metrics
    start_http_server(args.port)
    print("Started AWS Service Quota Exporter listening on port: " + str(args.port))

    # Variables controlling the flow on main loop
    initialRequestsCounter = 0
    warmUpPeriod = 1
    requestDelay = 0.5
    requestCounterHardStop = 8196

    if args.debug == True:
        print("Total of ServiceQuotas Metric/Label set to be calculated: "
             +str(len(awsRegionsList) * len(promMetrics["values"])))

    ## Main loop, going through the regions and setting current metrics values for both value and usage
    while True:
        for region in awsRegionsList:
            # Looping through metrics definitions:
            for metric in promMetrics["values"]:
                try:
                    quotaValue = getQuotaValue(
                        metric["quotaCode"],
                        metric["serviceCode"],
                        awsRegions[region]["clientSession"],
                    )
                    apiCallSuccess.inc()
                    metric["mObjectQuota"].labels(region=region, accountid=awsAccountID).set(quotaValue)
                except botocore.exceptions.EndpointConnectionError as error:
                    apiCallFails.inc()
                    print(str(error))
                except botocore.exceptions.ClientError as error:
                    apiCallFails.inc()
                    print(str(error))
                try:
                    usage = getUsage(
                        awsRegions[region]["clientSession"],
                        metric["usageRetrieval"],
                        metric["usageFilter"],
                    )
                    apiCallSuccess.inc()
                    metric["mObjectUsage"].labels(region=region, accountid=awsAccountID).set(usage)
                except botocore.exceptions.EndpointConnectionError as error:
                    apiCallFails.inc()
                    print(str(error))
                except botocore.exceptions.ClientError as error:
                    apiCallFails.inc()
                    print(str(error))

                ## Initial Requests are executed quicker to ensure we got all values in metrics
                #initialRequestsCounter = initialRequestsCounter + 1
                # Check if we completed initial run
                # If so throttle down to delay value specified in command line

                if (
                    initialRequestsCounter >= (len(awsRegionsList) * len(promMetrics["values"]))
                    and initialRequestsCounter != requestCounterHardStop):

                    if args.debug == True:
                        print("Warmup completed after " + str(initialRequestsCounter) + ", throttling down")
                    requestDelay = args.time
                    warmUpPeriod = 0
                    initialRequestsCounter = requestCounterHardStop

                if warmUpPeriod == 1:
                    initialRequestsCounter = initialRequestsCounter + 1

                if args.debug == True:
                    print(
                        "Last obtained AWS Quota Value for "
                        + str(metric["mObjectQuota"])
                        + " on "
                        + str(region)
                        + " is:"
                    )
                    print(str(quotaValue))
                    print(
                        "Last obtained AWS resource usage for "
                        + str(metric["mObjectUsage"])
                        + " on "
                        + str(region)
                        + " is:"
                    )
                    print(str(usage))
                ## Hardcoded sleep to ensure we don't choke on AWS API
                time.sleep(0.5)
        time.sleep(requestDelay)
exit()
