setup-alertmanager
=========

This role will instantiate a alertmanager container on targeted hosts. The notifications are sent to SMTP port (25) on the host server.

Requirements
------------

Docker must be available and running on the targeted hosts.

Role Variables
--------------
Default values of variables:
```
alertmanager_image: 'prom/alertmanager'
alertmanager_image_version: 'latest'
alertmanager_port: '9093'

provision_state: "started"

```
`alertmanager_image` - The alertmanager image to deploy.
`alertmanager_image_version` - The image tag to deploy.
`alertmanager_port` - The port to expose on the target hosts.
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
- name: Setup alertmanager
  hosts: prometheus_master
  become: True
  vars:
    provision_state: "started"
  roles:
    - prometheus/generic/setup-alertmanager
```

License
-------

BSD
