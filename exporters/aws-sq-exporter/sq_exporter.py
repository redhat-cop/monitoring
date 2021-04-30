#!/usr/bin/python3

import subprocess, os
import json
from collections import namedtuple
from prometheus_client import start_http_server, Summary, Gauge
import argparse
import time
import boto3
import bios
from benedict import benedict

#Generic function to fetch administrative quota value
def getQuotaValue(quotaCode,serviceCode,cSessions):
   paginator = cSessions["service-quotas"].get_paginator('list_service_quotas')
   pCursor = paginator.paginate(ServiceCode=serviceCode, PaginationConfig={'MaxItems': 1000 , 'PageSize': 10})
   i=0
   currentQ = 0
   for page in pCursor:
      for page2 in page['Quotas']:
         if page2['QuotaCode'] == quotaCode:
          currentQ = str(page2['Value'])
         i= i+1
   return currentQ


# Calculate number of Elastic IP currently in use
def getUsage(cSessions,usageRetrieval,usageFilter):
   awsCall = getattr(cSessions["ec2"],usageRetrieval)
   awsReturn = awsCall()
   return len(awsReturn[usageFilter])


if __name__ == '__main__':
   # Fetch&parse args
   parser = argparse.ArgumentParser()
   parser.add_argument("-c","--awsconfig",default="$HOME/.aws/config",help=" Location of optional configuration file, if not provided uses AWS CLI default")
   parser.add_argument("-a","--apikey",help=" AWS Access Key ID ")
   parser.add_argument("-s","--secretkey", help=" AWS Sercet Access Key")
   parser.add_argument("-r","--region", help=" AWS Region to be used fo queries")
   parser.add_argument("-t","--time", type=int, default=1200 , help="Sleep time between fetching the AWS API input")
   parser.add_argument("-d","--debug", help=" Should we be more verbose?",action="store_true")
   parser.add_argument("-p","--port", default=8000, help=" TCP port to be used to expose metrics HTTP endpoint")
   parser.add_argument("-m","--metrics", default="./metrics.yaml", help=" Metrics definition file")
   args = parser.parse_args()

   ##Adding metrics.yaml parsing( we need to load up clients for all unique services)

   metrics = benedict(args.metrics, format='yaml')

   if args.debug == True:
       print("Loading metrics definition file located at "+str(args.metrics))

   ## Get the services we'll need to connect to

   ##ec2 and VPC session set up
   clientSessions= {}
   clientSessions["ec2"] = boto3.client("ec2", aws_access_key_id=args.apikey, aws_secret_access_key= args.secretkey, region_name= args.region)
   clientSessions["service-quotas"] = boto3.client("service-quotas", aws_access_key_id=args.apikey, aws_secret_access_key= args.secretkey, region_name= args.region)

   # Create the actual metrics.
   for i in metrics["values"]:
    if args.debug == True:
      print("Creating metric for "+i['quotaCode']+" quota code")
    i['mObjectUsage']= Gauge(i['metricNameUsage'], i['usageDesc'])
    i['mObjectQuota']= Gauge(i['metricNameQuota'], i['quotaDesc'])

   if args.debug == True:
      print("Starting AWS Service Quota Exporter with the following parameters:")
      print("TCP port:"+str(args.port))
      print("Interval:"+str(args.time))
      print("AWS CONFIG:"+str(args.awsconfig))

   # Start HTTP Server
   start_http_server(args.port)
   print("Started AWS Service Quota Exporter listening on port:"+str(args.port))
   while True:
     for i in metrics["values"]:
         i['mObjectQuota'].set(getQuotaValue(i['quotaCode'],i['serviceCode'],clientSessions))
         i['mObjectUsage'].set(getUsage(clientSessions,i['usageRetrieval'],i['usageFilter']))
     time.sleep(args.time)
exit()
