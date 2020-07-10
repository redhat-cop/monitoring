setup-grafana-datasource
========================

This role will configures Openshift operated prometheus datasources. It iterates over "{{ datasources }}" list described in Example Inventory section.

Requirements
------------

grafana has to be running on target host

Role Variables
--------------
Default values of variables:
```
---
grafana_port: '3000'
grafana_password: 'super_secure_password'
grafana_user: 'admin' 

```
`grafana_port:` - port on which grafana is listening
`grafana_password:` - password for grafana
`grafana_user:` - user in grafana who can create datasource

Example Inventory
-----------------
```
---
datasources:
- name: "test_datasource"
  datasource_url: "https://prometheus-k8s-openshift-monitoring.apps.openshift.test.com"
  bearer_token:

```
datasources:
- name: - name of new datasource
  datasource_url: - url on which the prometheus is listening
  bearer_token: - authentication token for the Prometheus Oauth proxy


Dependencies
------------
```
python >= 2.6
```

Example Playbook
----------------
```
- name: Setup grafana datasourdce
  hosts: prometheus_scraper
  become: True
  vars:
    grafana_port: '3000'
    grafana_password: 'custom_password'
    grafana_user: 'custom_user'
  roles:
    - grafana/generic/configure-grafana-datasource
```

License
-------

BSD
