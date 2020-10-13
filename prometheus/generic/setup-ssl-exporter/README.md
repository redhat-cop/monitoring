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

Example Inventory
-----------------

Snippet below configures targets for the SSL exporter. It was taken from group_vars/monitoring_hosts.yml. {{ ssl_certs }} has to be defined for hostgroup prometheus_scraper or all, because the values are used in prometheus.yml.j2 template on the scraper nodes.

ssl_certs:
  - console-openshift-console.apps.openshift-1.example.com:443
  - api.openshift-1.example.com:6443



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
