---
This directory contains playbooks for managing the prometheus, alertmanager, grafana and exporters. Example inventory is also included

The requirements.yaml contains roles required for running these playbooks. The required roles have to be installed first by running:

```
$ ansible-galaxy install -r requirements.yml
```

Playbooks
=========

setup-grafana-datasource.yml - Configures grafana datasource, iterates over "{{ datasources }}".

setup-ssl-exporter.yml - Deploys ssl exporter. This exporter runs locally on prometheus host.  

setup-bind-exporter.yml - Deploys bind exporter. This exporter runs on name server (bind). 

setup-haproxy-exporter.yml - Deploys haproxy exporter. This exporter runs on haproxy node.

setup-prometheus-grafana.yml - Deploys and configures prometheus, alertmanager, grafana and also node-exporters. 

add-targets.yml - This playbook iterates over inventory groups and creates target definitions. 



Inventory Description
=====================

## example group_vars/all.yml 

`docker_install: True` <br />
`docker_username: centos` <br />
`ansible_user: centos` <br />  

## example group_vars/prometheus-scraper.yml
`smtp_host: my_smtp_host` - hostname of smtp server <br />
`smtp_port: my_smtp_port` - port on which smtp server listens <br />
`from: my_smtp_from` - smtp sender e-mail address <br />
`smtp_username: 'smtp_user'` - username to authenticate on smtp server <br />
`smtp_password: 'smtp_password'` - password to authenticate on smtp server <br />
`smtp_tls: 'false'` - switch for enabling/disabling tls verification <br />
`notification_recipients: somebody@example.com` - recipient address for alertmanager <br />
`dashboard_dir: /home/user/dashbooards` - directory from which the grafana dashboards are copied (optional) <br />
`custom_rule_file: /path/to/custom/rules_file.yml` - file with custom alerting rules1 (optional) <br />




## example hosts.yml
```
[prometheus_scraper]

[prometheus_target]

[prometheus_target_haproxy]

[prometheus_target_bind]

[ocp-clusters]
openshift-1

[grafana_datasources:children]
ocp-clusters

[prometheus_target_ssl:children]
ocp-clusters

[prometheus_target_prometheus:children]
ocp-clusters

[osp_instances:children]
prometheus_scraper
prometheus_target
prometheus_target_haproxy
prometheus_target_bind


[prometheus:children]
prometheus_scraper
prometheus_target
prometheus_target_haproxy
prometheus_target_bind

[osp-provisioner]
localhost
```

##example host file from ocp-ocp cluster group
```
datasource_url: "https://prometheus-k8s-openshift-monitoring.apps.openshift-1.example.com"
bearer_token: "my-secret-bearer-token"

ssl_certs:
  - console-openshift-console.apps.openshift-1.example.com:443
  - api.openshift-1.example.com:6443
```
