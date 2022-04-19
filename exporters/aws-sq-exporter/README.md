# AWS Service Quotas Exporter

Exporter used for querying specified AWS account for quotas and quatas usage, and transforming that data into Prometheus metrics.


### Parameters

```
-a, --apikey :  AWS Access Key ID
-s, --secretkey :  AWS Sercet Access Key
-r, --regions : List of AWS Regions to be used for queries (if no provided all regions will be queried)
-t, --time : Sleep time between fetching the AWS API input (default is 900s) 
-d, --debug : Set the exporter debug mode on
-p, --port : TCP port to be used to expose metrics HTTP endpoint (default is 8000)
-m, --metricsfile : a path to metrics definition file, should the default set would not be enough 
```


### Metrics definition file
By default, we're exporting metrics for number of ElasticIP and VPCs per region, but if user want to introduce other items, there's a support for custom definition file

Default file: 
```
---
-  metricNameUsage: "aws_eip_quota_usage"
   usageDesc: "Administrative Quota set on EIP"
   metricNameQuota: "aws_eip_quota_value"
   quotaDesc: "Number of Elastic IPs in use"
   serviceCode: "ec2"
   quotaCode: "L-0263D0A3"
   usageRetrieval: "describe_addresses"
   usageFilter: "Addresses"
   paginate: False

-  metricNameUsage: "aws_vpc_per_region_quota_usage"
   usageDesc: "Number of VPCs  in use"
   metricNameQuota: "aws_vpc_per_region_quota_value"
   quotaDesc: "Administrative Quota set on VPCs per Region"
   serviceCode: "vpc"
   quotaCode: "L-F678F1CE"
   usageRetrieval: "describe_vpcs"
   usageFilter: "Vpcs"
   paginate: True
```

Parameters explained:
```
metricNameUsage  : name for the usage  metric
usageDesc        : Description for the usage metric that will be presented on export
metricNameQuota  : name for quota metric
quotaDesc        : Description for the quota metric that will be presented on export
serviceCode      : Service code that will be used on AWS API call
quotaCode        : Quota Code that will be used to fetch quota value
usageRetrieval   : A part of AWS API call that checks for specific item you want to fetch
usageFilter      : a filter that's used to actually count specific items for usage
paginate         : Should AWS API call support pagination
```


### Running the exporter

You can run the exporter directly in your console by running the script with parameters specified in the section above


### Docker

To build the image: 
```
docker build --rm -t aws-sq-exporter .
```

To run the container
```
docker run -p 8000:8000 aws-sq-exporter:latest
```

You can then call the web server on the defined endpoint, `/metrics` by default.
```
curl 'http://127.0.0.1:8000/metrics'
```

Passing argument to the docker run command
```
docker run -p 8000:8000 aws-sq-exporter:latest --port 8000 --apikey ABC --secretkey XYZ
```


