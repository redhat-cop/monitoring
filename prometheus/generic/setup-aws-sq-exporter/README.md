setup-aws-sq-exporter
=========

This role will instantiate a AWS SQ Exporter container on targeted hosts. Role accepts a list of AWS accounts to monitor, and will spin up one Docker container per account.

Requirements
------------

Docker must be available and running on the targeted hosts.

Role Variables
--------------
## Default values of variables:
```
---
ansible_connection: "local"
aws_sq_exporter_image: 'prom/aws-sq-exporter'
aws_sq_exporter_image_version: 'latest'
aws_sq_exporter_port: '8080'

provision_state: "started"

ansible_sq_exporter:
   - awsAccount: "Dummy-Account"
     port: 9420
     apikey: 22222
     secretkey: 3333
     regions: "us-east-1,us-east-2"
     debug: false
```
```
aws_sq_exporter_image - The AWS SQ Exporter image to deploy.
aws_sq_exporter_image_version - The image tag to deploy.
aws_sq_exporter_port - The port to be exposed on container.
provision_state - Options: [absent, killed, present, reloaded, restarted, **started** (default), stopped]

ansible_sq_exporter: - variable holding individual account configuration
   - awsAccount: "Dummy-Account"  - AWS Account alias
     port: 9420                  - Port on which this specific container will be exposed for metrics scraping
     apikey: 22222               - AWS Account API Key
     secretkey: 3333             - AWS Account SecretKey
     regions: "ex1,ex2"         - Commaseparated list of regions to query for SQs and usage
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
- name: Setup AWS SQ Exporter
  hosts: prometheus_master
  become: True
  vars:
    provision_state: "started"
  roles:
    - prometheus/generic/setup-aws-sq-exporter
```

License
-------

BSD
