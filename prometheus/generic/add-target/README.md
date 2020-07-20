add-target
=========

This role creates target definitions on prometheus instance

Requirements
------------

Prometheus deployed with ../setup-prometheus role on the targeted hosts.

Role Variables
--------------
Default values of variables:
```
haproxy_exporter_port: '9101'
bind_exporter_port: '9119'
ssl_exporter_port: '9219'
```
`haproxy_exporter_port` - port on which the haproxy exporter is listening
`bind_exporter_port` - port on which the bind exporter is listening
`ssl_exporter_port` - port on which the ssl exporter is listening

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
---
- name: Setup targets
  hosts: prometheus_scraper
  become: True
  roles:
    - ../../prometheus/generic/add-target
```

Example Inventory
-----------------

Example inventory can be found in /playbooks/infra-prometheus/inventory/

License
-------

BSD
