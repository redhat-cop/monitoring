## AWS CloudFormation Stack Exporter ##
*** ***
This is a simple Prometheus Exporter that querries AWS API for number of CloudFormation Stacks in any state.

## Building the exporter Docker image ##
Docker image should be based on provided Dockerfile, to build the image run that command from repository root directory:

   `export VERSION="0.1.1"; docker build -t aws-cloudformation-stacks-exporter:${VERSION} exporters/aws-cloudformation-stacks-exporter/`

## Running the exporter and AWS credentials ##
Exporter uses AWS API directly, simplest way of injecting API keys is by mounting prepopulated .aws into the container:

    `docker run  -p 8000:8000 -v /${HOME}/.aws:/home/exporter/.aws aws-cloudformation-stacks-exporter:0.1.1`

Other options are:

* -a APIKEY, --apikey APIKEY          : AWS Access Key ID
* -s SECRETKEY, --secretkey SECRETKEY : AWS Sercet Access Key
* -r REGION(S), --regions REGION      : AWS Region or list of comma separated regions to be used for queries
* -t TIME, --time TIME                : Sleep time between fetching the AWS API input
* -d, --debug                         : Should we be more verbose?
* -p PORT, --port PORT                : TCP port to be used to expose metrics HTTP endpoint
