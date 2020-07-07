setup-node-exporter
=========

This role will instantiate a grafana container on targeted hosts. It also seeds the host with dashboards

Requirements
------------

Docker must be available and running on the targeted hosts.

Role Variables
--------------
Default values of variables:
```
---
grafana_image: 'grafana/grafana'
grafana_image_version: 'latest'
grafana_port: '3000'
grafana_password: 'super_secure_password'

prometheus_port: '9090'

provision_state: "started"

```
`grafana_image` - The node exporter image to deploy.
`grafana_image_version` - The image tag to deploy.
`grafana_port` - The port to expose on the target hosts.
`grafana_password` - The admin password to set for Grafana.
`prometheus_port` - The target port on the prometheus host to pull data.
`provision_state` - Options: [absent, killed, present, reloaded, restarted, **started** (default), stopped]


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
- name: Setup grafana
  hosts: grafana
  become: True
  vars:
    provision_state: "started"
    dashboard_dir: "/home/user/dashboards"
  roles:
    - grafana/generic/setup-grafana
```

License
-------

BSD
