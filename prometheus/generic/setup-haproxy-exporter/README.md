setup-node-exporter
=========

This role will instantiate a haproxy-exporter container on targeted hosts.

Requirements
------------

Docker must be available and running on the targeted hosts. The stats page has to be available on target host.

Role Variables
--------------
Default values of variables:
```
haproxy_exporter_image: 'prom/haproxy-exporter'
haproxy_exporter_image_version: 'latest'
haproxy_exporter_port: '9101'

provision_state: "started"

stats_port: '8080'
stats_user: admin
stats_password: admin
```
`haproxy_exporter_image` - The haproxy exporter image to deploy.
`haproxy_exporter_image_version` - The image tag to deploy.
`haproxy_exporter_port` - The port to expose on the target hosts.
`provision_state` - Options: [absent, killed, present, reloaded, restarted, **started** (default), stopped]

`stats_port` - port on which is the stats page available
`stats_user` - stats page user
`stats_password` - stats page password

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
- name: Setup haproxy exporters
  hosts: haproxy_nodes
  become: True
  vars:
    provision_state: "started"
  roles:
    - prometheus/generic/setup-haproxy-exporter
```

License
-------

BSD
