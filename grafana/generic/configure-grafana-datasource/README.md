setup-grafana-datasource
========================

This role will configure grafana datasources. It iterates over hostgroups grafana_prometheus_datasoources and grafana_cloudwatch_datasources

Requirements
------------

Grafana has to be running on target host

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

cloudwatch datasource host
```
---
region: "my-aws-region"
access_key: "my-cloudwatch-key"
secret_access_key: "my-cloudwatch-secret"
```

prometheus datasource host
```
datasource_url: "https://prometheus-k8s-openshift-monitoring.apps.openshift-1.example.com"
bearer_token: "my-secret-bearer-token"
```


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
