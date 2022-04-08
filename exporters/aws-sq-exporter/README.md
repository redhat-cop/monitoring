## AWS Service Quotas Exporter ##
*** ***
This is a simple Prometheus Exporter that querries AWS API for quota values of specific configuration items and calculates actual usage of those quotas.

### AWS SQs ###
*** ***
Currently there's support for only two SQs:
* L-0263D0A3 - number of Elastic IPs defined for the region
* L-F678F1CE - number of VCPs defined for the region

## Building the exporter Docker image ##
Docker image should be based on provided Dockerfile, to build the image run that command from repository root directory:

   `export VERSION="0.1.1"; docker build -t aws-sq-exporter:${VERSION} exporters/aws-sq-exporter/`

## Running the exporter and AWS credentials ##
Exporter uses AWS API directly, simplest way of injecting API keys is by mounting prepopulated .aws into the container:

    `docker run  -p 8000:8000 -v /${HOME}/.aws:/home/exporter/.aws aws-sq-exporter:0.1.1`

Other options are:

* -a APIKEY, --apikey APIKEY          : AWS Access Key ID
* -s SECRETKEY, --secretkey SECRETKEY : AWS Sercet Access Key
* -r REGION(S), --regions REGION      : AWS Region or list of comma separated regions to be used for queries
* -t TIME, --time TIME                : Sleep time between fetching the AWS API input
* -d, --debug                         : Should we be more verbose?
* -p PORT, --port PORT                : TCP port to be used to expose metrics HTTP endpoint

## Metric file  format ##
Metric definitions should follow the example format:

```yaml
---
- metricNameUsage: "aws_vpc_per_region_quota_usage"
   usageDesc: "Number of VPCs  in use"
   metricNameQuota: "aws_vpc_per_region_quota_value"
   quotaDesc: "Administrative Quota set on VPCs per Region"
   serviceCode: "vpc"
   quotaCode: "L-F678F1CE"
   usageRetrieval: "describe_vpcs"
   usageFilter: "Vpcs"
   paginate: True
```
* metricNameUsage    - a name for Prometheus metric showing actual usage
* usageDesc          - description that will be added to Prometheus usage metric  
* metricNameQuota    - a name for Prometheus metric showing the quota value
* quotaDesc          - description that will be added to Prometheus quota value metrics
* serviceCode        - serviceCode that's assigned to the metric (see AWS CLI manual)
* quotaCode          - unique quotaCode (see AWS CLI manual)
* usageRetrieval     - name of method which presents the information used to count the actual usage values
* usageFiter         - name of dictionary that AWS API returns for usageRetrieval query
* paginate           - reserved for future development
