setup-junos-exporter
=========

This role will instantiate a [junos-exporter](https://github.com/czerwonk/junos_exporter) container on targeted hosts.

Requirements
------------

Docker must be available and running on the targeted hosts.

Role Variables
--------------
Default values of variables:
```
junos_exporter_image: 'czerwonk/junos_exporter'
junos_exporter_image_version: 'latest'
junos_exporter_port: '9326'

provision_state: "started"
```
`junos_exporter_image` - The junos exporter image to deploy.
`junos_exporter_image_version` - The image tag to deploy.
`junos_exporter_port` - The port to expose on the target hosts.
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
  hosts: monitoring_host
  become: True
  vars:
    provision_state: "started"
  roles:
    - prometheus/generic/setup-junos-exporter
```

License
-------

BSD
