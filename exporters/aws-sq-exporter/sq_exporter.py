#!/usr/bin/python3

import subprocess, os
import json
from collections import namedtuple
from prometheus_client import start_http_server, Summary, Gauge
import argparse
import time
import yaml

# Simple JSON mappers
def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)


#Generic to fetch administrative quota value
def getQuotaValue(quotaCode,serviceCode,envVars):
   psq = subprocess.run(['/usr/local/bin/aws','service-quotas','list-service-quotas','--service-code',serviceCode ],stdout=subprocess.PIPE, universal_newlines=True, env=envVars)
   if args.debug == True:
     print(str(psq.args)+str(psq.stdout))
   psq_j = json2obj(psq.stdout)
   for i in psq_j.Quotas:
     if i.QuotaCode == quotaCode:
         currentQ = str(i.Value)
   return currentQ

# Calculate number of Elastic IP currently in use
def getEipUsage(envVars):
    
    psu = subprocess.run(['/usr/local/bin/aws','ec2','describe-addresses'],stdout=subprocess.PIPE, universal_newlines=True, env=envVars)
    psu_j = json2obj(psu.stdout)
    if args.debug == True:
      print(str(psu.args)+str(psu.stdout))
    currentUsage = 0
    for i in psu_j.Addresses:
       currentUsage=currentUsage+1
    return currentUsage

# Extract usage for "VPCs per Region"
def getVPCNumUsage(envVars):
    psu = subprocess.run(['/usr/local/bin/aws','ec2','describe-vpcs'],stdout=subprocess.PIPE, universal_newlines=True, env=envVars)
    psu_j = json2obj(psu.stdout)
    if args.debug == True:
      print(str(psu.args)+str(psu.stdout))
    currentUsage = 0
    for i in psu_j.Vpcs:
      currentUsage=currentUsage+1
    return currentUsage





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
   args = parser.parse_args()

   # Create a metrics.
  
   AwsEipQuota = Gauge('aws_eip_quota_value', 'Administrative Quota set on EIP')
   AwsEipUsage = Gauge('aws_eip_quota_usage', 'Number of Elastic IPs in use')
   AwsVPCNumQuota = Gauge('aws_vpc_per_region_quota_value', 'Administrative Quota set on "VPCs per Region"')
   AwsVPCNumUsage = Gauge('aws_vpc_per_region_quota_usage', 'Number of VPCs  in use')
   if args.debug == True:
      print("Starting AWS Service Quota Exporter with the following parameters:")
      print("TCP port:"+str(args.port))
      print("Interval:"+str(args.time))
      print("AWS CONFIG:"+str(args.awsconfig))
   # set the AWS CLI env variables
   mEnv = {}
   if args.apikey and args.secretkey:
      mEnv["AWS_ACCESS_KEY_ID"]=args.apikey
      mEnv["AWS_SECRET_ACCESS_KEY"]=args.secretkey
   if args.region: 
      mEnv["AWS_DEFAULT_REGION"]=args.region
   mEnv["AWS_CONFIG_FILE"]=args.awsconfig

   # Start HTTP Server
   start_http_server(args.port)
   print("Started AWS Service Quota Exporter listening on port:"+str(args.port))
   while True:
     #EIP Quota value
     AwsEipQuota.set(getQuotaValue("L-0263D0A3","ec2",mEnv))
     AwsEipUsage.set(getEipUsage(mEnv))
     #VPC Quota value
     AwsVPCNumQuota.set(getQuotaValue("L-F678F1CE","vpc",mEnv))
     AwsVPCNumUsage.set(getVPCNumUsage(mEnv))
     time.sleep(args.time)
exit()