#!/usr/bin/python3

import subprocess
import json
from collections import namedtuple
from prometheus_client import start_http_server, Summary, Gauge
import argparse
import time

# Simple JSON mappers
def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)


#Generic to fetch administrative quota value
def getQuotaValue(quotaCode,serviceCode):
   psq = subprocess.run(['/usr/local/bin/aws','service-quotas','list-service-quotas','--service-code',serviceCode ],stdout=subprocess.PIPE, universal_newlines=True)
   if args.debug == True:
     print(str(psq.args)+str(psq.stdout))
   psq_j = json2obj(psq.stdout)
   for i in psq_j.Quotas:
     if i.QuotaCode == quotaCode:
         currentQ = str(i.Value)
   return currentQ

# Calculate number of Elastic IP currently in use
def getEipUsage():
    psu = subprocess.run(['/usr/local/bin/aws','ec2','describe-addresses'],stdout=subprocess.PIPE, universal_newlines=True)
    psu_j = json2obj(psu.stdout)
    if args.debug == True:
      print(str(psu.args)+str(psu.stdout))
    currentUsage = 0
    for i in psu_j.Addresses:
       currentUsage=currentUsage+1
    return currentUsage

# Extract usage for "VPCs per Region"
def getVPCNumUsage():
    psu = subprocess.run(['/usr/local/bin/aws','ec2','describe-vpcs'],stdout=subprocess.PIPE, universal_newlines=True)
    psu_j = json2obj(psu.stdout)
    if args.debug == True:
      print(str(psu.args)+str(psu.stdout))
    currentUsage = 0
    for i in psu_j.Vpcs:
      currentUsage=currentUsage+1
    return currentUsage


# Fetch&parse args
parser = argparse.ArgumentParser()

##To be addded later
#parser.add_argument("-r","--region", help="AWS region to be queried for metrics, if not defined exporter will fallback to what's on default profile")
#parser.add_argument("-ki","--aws-key-id", help="",)
#parser.add_argument("-sk","--aws-secret-key",help="")

parser.add_argument("-t","--time", type=int, default=1200 , help="Sleep time between fetching the AWS API input")
parser.add_argument("-d","--debug", help=" Should we be more verbose?",action="store_true")
parser.add_argument("-p","--port", default=8000, help=" TCP port to be used to expose metrics HTTP endpoint")
args = parser.parse_args()


# Create a metrics.
AwsEipQuota = Gauge('aws_eip_quota_value', 'Administrative Quota set on EIP')
AwsEipUsage = Gauge('aws_eip_quota_usage', 'Number of Elastic IPs in use')
AwsVPCNumQuota = Gauge('aws_vpc_per_region_quota_value', 'Administrative Quota set on "VPCs per Region"')
AwsVPCNumUsage = Gauge('aws_vpc_per_region_quota_usage', 'Number of VPCs  in use')


if __name__ == '__main__':
   if args.debug == True:
      print("Starting AWS Service Quota Exporter with the following parameters:")
      print("TCP port:"+str(args.port))
      print("Interval:"+str(args.time))
   # Start up the server to expose the metrics.
   start_http_server(args.port)
   print("Started AWS Service Quota Exporter listening on port:"+str(args.port))
   while True:
     #EIP Quota value
     AwsEipQuota.set(getQuotaValue("L-0263D0A3","ec2"))
     AwsEipUsage.set(getEipUsage())
     #VPC Quota value
     AwsVPCNumQuota.set(getQuotaValue("L-F678F1CE","vpc"))
     AwsVPCNumUsage.set(getVPCNumUsage())
     time.sleep(args.time)
exit()