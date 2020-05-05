setup-node-exporter
=========

This role will instantiate a prometheus container on targeted hosts.

Requirements
------------

Docker must be available and running on the targeted hosts.

Role Variables
--------------
Default values of variables:
```
prometheus_image: 'prom/prometheus'
prometheus_image_version: 'latest'
prometheus_port: '9090'

provision_state: "started"
```
`prometheus_image` - The node exporter image to deploy.
`prometheus_image_version` - The image tag to deploy.
`prometheus_port` - The port to expose on the target hosts.
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
- name: Setup prometheus
  hosts: prometheus_master
  become: True
  vars:
    provision_state: "started"
  roles:
    - prometheus/generic/setup-prometheus
```

License
-------

BSD
