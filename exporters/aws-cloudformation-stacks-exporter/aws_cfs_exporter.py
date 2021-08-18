#!/opt/app-root/bin/python

import subprocess, os
from prometheus_client import start_http_server, Summary, Gauge, Counter
import argparse
import time
import boto3
import botocore
from benedict import benedict


# calculate number of stacks with state breakdown
def getAwsStacks(cSessions,awsStackAvailableSt):
    paginator = cSessions["cloudformation"].get_paginator("list_stacks")
    paginatorCursor = paginator.paginate(PaginationConfig={"MaxItems": 10000})
    nrStacksPerState = {}
    #Initialize temporary structure holding the data
    for stacks in awsStackAvailableSt:
        nrStacksPerState[stacks] = 0
    for page in paginatorCursor:
        for stacks in page["StackSummaries"]:
            for stackState in awsStackAvailableSt:
                if stacks["StackStatus"] == stackState:
                        nrStacksPerState[stackState] = nrStacksPerState[stackState] +1
    return nrStacksPerState

def getAccountID():
    awsSession = boto3.client("sts", aws_access_key_id=args.apikey, aws_secret_access_key=args.secretkey)
    awsReturns = awsSession.get_caller_identity()
    return awsReturns["Account"]

def getAccountAliasBasedonID(accountID):
    return 0

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
    args = parser.parse_args()

    promMetrics = {}
    awsStackAvailableStates= []
    with open('./aws-stack-states.cnf') as confFile:
        for line in confFile:
          if line != None and "#" not in line:
              state = line.strip()
              awsStackAvailableStates.append(state)
              promMetrics[state] = {}
              print("Creating metric for " + state + " CF stack state")
              apiCFMetricName = "aws_cloudformation_stack_in_" + state
              apiCFMetricDesc = "Gauge set on number of CloudFormation Stacks in "+ state +" state"
              promMetrics[state] = Gauge(
                   apiCFMetricName, apiCFMetricDesc, ["region", "accountid"]
              )

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

    # Getting AccountId
    awsAccountID = getAccountID()
    print("Exporter configured to calculate metrics on : " + str(awsAccountID))

    ## Setting initial sessions, per region
    for region in awsRegionsList:
        awsRegions[region]["clientSession"] = {}
        awsRegions[region]["clientSession"]["cloudformation"] = boto3.client(
            "cloudformation",
            aws_access_key_id=args.apikey,
            aws_secret_access_key=args.secretkey,
            region_name=region,
        )
        awsRegions[region]["clientSession"]["ec2"] = boto3.client(
            "ec2",
            aws_access_key_id=args.apikey,
            aws_secret_access_key=args.secretkey,
            region_name=region,
        )

    ## Setting up Counter metrics to track AWS API call failures
    # Setting variables
    apiCallFailureMetricName = "aws_api_failed_requests_cloudformation"
    apiCallFailureMetricDesc = "Counter set on failed AWS API calls"
    apiCallSuccessMetricName = "aws_api_success_requests_cloudformation"
    apiCallSuccessMetricDesc = "Counter set on succesfull AWS API calls"
    # Initializing metrics
    apiCallFails = Counter(apiCallFailureMetricName, apiCallFailureMetricDesc)
    apiCallSuccess = Counter(apiCallSuccessMetricName, apiCallSuccessMetricDesc)

    # Resetting counters
    apiCallFails.inc(0)
    apiCallSuccess.inc(0)

    ## Initializing HTTP /metrics endpoint for Prometheus metrics
    start_http_server(args.port)
    print("Started AWS CloudFormation Stack State Exporter listening on port: " + str(args.port))

    # Variables controlling the flow on main loop
    initialRequestsCounter = 0
    warmUpPeriod = 1
    requestDelay = 0.5
    requestCounterHardStop = 8196

    #if args.debug == True:
    #    print("Total of CloudFormation Stacks Metric/Label set to be calculated: "
    #         +str(len(awsRegionsList) * len(promMetrics["PrometheusMetrics"])))

    ## Main loop, going through the regions and setting current metrics values for both value and usage
    while True:
      for region in awsRegionsList:
         metricsValue = getAwsStacks(awsRegions[region]["clientSession"],awsStackAvailableStates)
               # Looping through metrics definitions:
         for state in awsStackAvailableStates:
                try:
                    apiCallSuccess.inc()
                    apiCFMetricName = "aws_cloudformation_stack_in_" + state
                    for state in awsStackAvailableStates:
                        promMetrics[state].labels(region=region, accountid=awsAccountID).set(metricsValue[state])
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
                    initialRequestsCounter >= (len(awsRegionsList) * len(promMetrics.keys()))
                    and initialRequestsCounter != requestCounterHardStop):

                    if args.debug == True:
                        print("Warmup completed after " + str(initialRequestsCounter) + ", throttling down")
                    requestDelay = args.time
                    warmUpPeriod = 0
                    initialRequestsCounter = requestCounterHardStop

                if warmUpPeriod == 1:
                    initialRequestsCounter = initialRequestsCounter + 1


                ## Hardcoded sleep to ensure we don't choke on AWS API
                time.sleep(0.5)
         time.sleep(requestDelay)
exit()
