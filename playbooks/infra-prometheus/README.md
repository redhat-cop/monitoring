---
This directory contains playbooks for managing the prometheus, alertmanager, grafana and exporters. Example inventory is also included

The requirements.yaml contains roles required for running these playbooks. The required roles have to be installed first by running:

```
$ ansible-galaxy install -r requirements.yml
```

Playbooks
=========

setup-grafana-datasource.yml - Configures grafana datasource, iterates over "{{ datasources }}"

setup-ssl-exporter.yml - Deploys ssl exporter. This exporter runs locally on prometheus host.

setup-bind-exporter.yml - Deploys bind exporter. This exporter runs on name server (bind).

setup-haproxy-exporter.yml - Deploys haproxy exporter. This exporter runs on haproxy node.

setup-prometheus-grafana.yml - Deploys and configures prometheus, alertmanager, grafana and also node-exporters.



Inventory Description
=====================

## example group_vars/all.yml 

`docker_install: True` <br />
`docker_username: centos` <br />
`ansible_user: centos` <br />  
`dashboard_dir: /home/user/dashbooards` - directory from which the grafana dashboards are copied <br />
`notification_recipients: somebody@example.com` - recipient address for alertmanager <br />

## example group_vars/prometheus-scraper.yml
`smtp_host: my_smtp_host` - hostname of smtp server <br />
`smtp_port: my_smtp_port` - port on which smtp server listens <br />
`from: my_smtp_from` - smtp sender e-mail address <br />
`smtp_username: 'smtp_user'` - username to authenticate on smtp server <br />
`smtp_password: 'smtp_password'` - password to authenticate on smtp server <br />
`smtp_tls: 'false'` - switch for enabling/disabling tls verification <br />


`datasources:` -  inventory used for configuration of grafana datasources and prometheus-targets <br />
`- name: "openshift-1"` - name of the prometheus datasource to be created <br />
`&nbsp;&nbsp;datasource_url: "https://prometheus-k8s-openshift-monitoring.apps.openshift-1.example.com"` - url of the prometheus <br />
`&nbsp;&nbsp;bearer_token: "prometheus-k8s-secret-token"` - authentication token for the prometheus <br />

`ssl_certs:` - inventory used for configuration of ssl-exporter prometheus targets <br />
`&nbsp;&nbsp;- prometheus-k8s-openshift-monitoring.apps.openshift-1.example.com:443` <br />
`&nbsp;&nbsp;- api.openshift-1.example.com:443` <br />

## example hosts.yml
`[prometheus_scraper]` - target host for prometheus, alertmanager, grafana <br />

`[prometheus_target]` - hosts on which node-exporter is deployed <br />

`[prometheus_target_haproxy]` - hosts on which haproxy exporter is deployed <br />

`[prometheus_target_bind]` - hosts on which target bind exporter is deployed <br />

`[osp_instances:children]` <br />
`prometheus_scraper` <br />
`prometheus_target` <br />

`[prometheus:children]` <br />
`prometheus_scraper` <br />
`prometheus_target` <br />
`prometheus_target_bind` <br />
`prometheus_target_haproxy` <br />
