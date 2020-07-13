setup-ssl-exporter
==================

This role will instantiate a ssl-exporter container on targeted hosts.

Requirements
------------

Docker must be available and running on the targeted hosts.

Role Variables
--------------
Default values of variables:
```
ssl_exporter_image: 'ribbybibby/ssl-exporter'
ssl_exporter_image_version: 'latest'
ssl_exporter_port: '9219'

provision_state: "started"
```
`ssl_exporter_image` - The ssl exporter image to deploy.
`ssl_exporter_image_version` - The image tag to deploy.
`ssl_exporter_port` - The port to expose on the target hosts.
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
- name: Setup ssl exporters
  hosts: prometheus_scraper
  become: True
  vars:
    provision_state: "started"
  roles:
    - prometheus/generic/setup-ssl-exporter
```

License
-------

BSD
