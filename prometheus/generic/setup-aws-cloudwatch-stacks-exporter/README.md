setup-aws-cloudformation-stacks-exporter
=========

This role will instantiate a AWS Cloudformation Stacks Exporter container on targeted hosts. Role accepts a list of AWS accounts to monitor, and will spin up one Docker container per account.

Requirements
------------

Docker must be available and running on the targeted hosts.

Role Variables
--------------
## Default values of variables:
```
---
aws_cfs_exporter_image: 'prom/aws-cloudformation-stacks-exporter'
aws_cfs_exporter_image_version: 'latest'
aws_cfs_exporter_port: '8080'

provision_state: "started"

ansible_cfs_exporter:
   - awsAccount: "Dummy-Account"
     port: 9420
     apikey: 22222
     secretkey: 3333
     regions: "us-east-1,us-east-2"
     debug: false
```
```
aws_cfs_exporter_image - The AWS CFS Exporter image to deploy.
aws_cfs_exporter_image_version - The image tag to deploy.
aws_cfs_exporter_port - The port to be exposed on container.
provision_state - Options: [absent, killed, present, reloaded, restarted, **started** (default), stopped]

ansible_cfs_exporter: - variable holding individual account configuration
   - awsAccount: "Dummy-Account"  - AWS Account alias
     port: 9420                  - Port on which this specific container will be exposed for metrics scraping
     apikey: 22222               - AWS Account API Key
     secretkey: 3333             - AWS Account SecretKey
     regions: "ex1,ex2"          - Commaseparated list of regions to query for Cloudformations Stack statuses 
     debug: false                - Increase logging verbosity
```


Dependencies
------------
```
python >= 2.6
docker-py >= 0.3.0
The docker server >= 0.10.0
```

Example Playbook
----------------
```
- name: Setup AWS CFS Exporter
  hosts: prometheus_master
  become: True
  vars:
    provision_state: "started"
  roles:
    - prometheus/generic/setup-aws-cloudformation-stacks-exporter
```

License
-------

BSD
