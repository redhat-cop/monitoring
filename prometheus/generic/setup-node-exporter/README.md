setup-node-exporter
=========

This role will instantiate a node-exporter container on targeted hosts.

Requirements
------------

Docker must be available and running on the targeted hosts.

Role Variables
--------------
Default values of variables:
```
node_exporter_image: 'prom/node-exporter'
node_exporter_image_version: 'latest'
node_exporter_port: '9100'

provision_state: "started"
```
`node_exporter_image` - The node exporter image to deploy.
`node_exporter_image_version` - The image tag to deploy.
`node_exporter_port` - The port to expose on the target hosts.
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
- name: Setup node exporters
  hosts: prometheus_nodes
  become: True
  vars:
    provision_state: "started"
  roles:
    - prometheus/generic/setup-node-exporter
```

License
-------

BSD
