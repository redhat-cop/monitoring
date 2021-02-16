---
This directory contains playbooks for managing the prometheus, alertmanager, grafana and exporters. Example inventory is also included

The requirements.yaml contains roles required for running these playbooks. The required roles have to be installed first by running:

```
$ ansible-galaxy install -r requirements.yml
```

How to deploy prometheus alertmanager and grafana stack
=======================================================

The monitoring stack is deployed by running the setup-prometheus-grafana playbook. <br /> 
The playbook targets group monitoring-hosts. <br />
First run of the playbook should be done with --tags="install", which installs docker on target hosts. Due to a bug in infra-ansible install-docker role it has to be run twice (this should be fixed in https://github.com/redhat-cop/infra-ansible/pull/420/). Any consecutive runs can be done without the "install" tag. <br />

How to configure targets
========================

1. Add target hosts to respective group in the inventory hosts file. <br />
prometheus_target - node exporter is installed on this host group <br />
prometheus_target_haproxy - haproxy exporter is installed on this host group <br />
prometheus_target_bind - bind exporter is installed on this host group <br />
2. Run the monitoring-targets/setup-exporters.yml playbook. This playbook deploys exporters based on group membership described above. To install docker use --tags="install" (this has to be run twice). <br />
3. Add targets to the prometheus. Run the monitoring-hosts/add-targets.yml using the same inventory. This playbook templates target definitions on monitoring-hosts hostgroup. <br />


How to add Openshift to the monitoring
======================================

1. Add target host to ocp-cluster hostgroup in the inventory hosts file, there are multiple required variables. Example host_vars definition is available below or in inventory/host_vars/openshift-1.yml <br />
2. Run the monitoring-hosts/add-openshift.yml playbook, which configures OCP operated prometheus as a target. Optionally you can also configure ssl exporter targets with this playbook (when ssl_certs: are defined) <br />



Playbooks
=========

## monitoring hosts

setup-grafana-datasource.yml - Configures grafana datasource, iterates over "{{ datasources }}".

setup-ssl-exporter.yml - Deploys ssl exporter. This exporter runs locally on prometheus host.  

setup-openstack-exporter.yml - Deploys openstack exporter. This exporter runs locally on prometheus host.

setup-prometheus-grafana.yml - Deploys and configures prometheus, alertmanager, grafana and also node-exporters. 

add-targets.yml - This playbook iterates over inventory groups and creates target definitions. 

add-openshift.yml - This playbook combines the add-targets and configure-grafana-datasources to add Openshift environment to monitoring. The alertmanager.yaml is templated and created in files/ directory. The has to be applied on alertmanager-main secret in Openshift in order to configure the notification receivers.

## monitoring targets

setup-bind-exporter.yml - Deploys bind exporter. This exporter runs on name server (bind).

setup-haproxy-exporter.yml - Deploys haproxy exporter. This exporter runs on haproxy node.

setup-node-exporter.yml - Deploys node exporter. This exporter runs on target node.

setup-exporters.yml - Sets up all of above mentioned exporters based on group membership


Inventory Description
=====================

## example group_vars/all.yml 

`docker_install: True` <br />
`docker_username: centos` <br />
`ansible_user: centos` <br />  
`ansible_become: true` <br />

## example group_vars/monitoring-hosts.yml
`smtp_host: my_smtp_host` - hostname of smtp server <br />
`smtp_port: my_smtp_port` - port on which smtp server listens <br />
`from: my_smtp_from` - smtp sender e-mail address <br />
`smtp_username: 'smtp_user'` - username to authenticate on smtp server <br />
`smtp_password: 'smtp_password'` - password to authenticate on smtp server <br />
`smtp_tls: 'false'` - switch for enabling/disabling tls verification <br />
`notification_recipients: somebody@example.com` - recipient address for alertmanager <br />
`dashboard_dir: /home/user/dashbooards` - directory from which the grafana dashboards are copied (optional) <br />
`custom_rule_file: /path/to/custom/rules_file.yml` - file with custom alerting rules1 (optional) <br />
`ssl_expiration_warning_threshold: 7` - ssl cert warning threshold (days)
`ssl_expiration_critical_threshold: 3` - ssl cert critical threshold (days)
`memory_usage_warning_threshold: 60` - memory warning threshold (%)
`memory_usage_critical_threshold: 90` - memory critical threshold (%)
`disk_usage_warning_threshold: 60` - filesystem usage warning threshold (%)
`disk_usage_critical_threshold: 90` - filesystem usage critical threshold (%)





## example hosts.yml
```
[monitoring-hosts]

[prometheus_target]

[prometheus_target_haproxy]

[prometheus_target_bind]

[openstack_env]
openstack-1

[ocp-clusters]
openshift-1

[grafana_datasources:children]
ocp-clusters

[prometheus_target_ssl:children]
ocp-clusters

[prometheus_target_prometheus:children]
ocp-clusters

[osp_instances:children]
monitoring-hosts
prometheus_target
prometheus_target_haproxy
prometheus_target_bind

[osp-provisioner]
localhost
```

## example host file from ocp-cluster group
```
datasource_url: "https://prometheus-k8s-openshift-monitoring.apps.openshift-1.example.com"
bearer_token: "my-secret-bearer-token"

ssl_certs:
  - console-openshift-console.apps.openshift-1.example.com:443
  - api.openshift-1.example.com:6443
```

## example host_vars file from openstack_env group
```
osp_auth_url: https://openstack-1.example.com:13000/v3
osp_auth_username: myuser
osp_auth_password: mypassword
osp_project_id: my_project_id
osp_project_name: my_project_name
osp_user_domain: my_user_domain
openstack_exporter_port: 9180
```
