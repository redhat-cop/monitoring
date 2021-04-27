## AWS Service Quotas Exporter ##
*** ***
This is a simple Prometheus Exporter that querries AWS API for quota values of specific configuration items and calculates actual usage of those quotas.

### AWS SQs ###
*** ***
Currently there's support for only two SQs:
* L-0263D0A3 - number of Elastic IPs defined for the region
* L-F678F1CE - number of VCPs defined for the region

## Building the exporter Docker image ##
Docker image should be based on provided Dockerfile, build it by using standard command:

    export VERSION="0.1.1"; docker build -t sq-exporter:${VERSION} ./

## Running the exporter and AWS credentials ##
Exporter uses AWS API directly, simplest way of injecting API keys is by mounting prepopulated .aws into the container:

    docker run  -p 8000:8000 -v /${HOME}/.aws:/home/exporter/.aws sq-exporter:0.1.1

Other options are:

-c AWSCONFIG, --awsconfig AWSCONFIG : Location of optional configuration file, if not
                                      provided uses AWS CLI default
-a APIKEY, --apikey APIKEY          : AWS Access Key ID
-s SECRETKEY, --secretkey SECRETKEY : AWS Sercet Access Key
-r REGION, --region REGION          : AWS Region to be used for queries
-t TIME, --time TIME                : Sleep time between fetching the AWS API input
-d, --debug                         : Should we be more verbose?
-p PORT, --port PORT                : TCP port to be used to expose metrics HTTP endpoint
