# setup-netapp-exporter

This role will instantiate a NetApp health exporter container on targeted hosts.

## Requirements

Docker must be available and running on the targeted hosts.

The EPEL repository must be available on the targeted hosts.

## Role Variables

Default values of variables:

```
netapp_exporter_image: 'quay.io/redhat-cop/monitoring-netapp-exporter'
netapp_exporter_image_version: 'latest'
netapp_exporter_port: '9418'

provision_state: "started"
```

`netapp_exporter_image` - The NetApp exporter image to deploy.

`netapp_exporter_image_version` - The image tag to deploy.

`netapp_exporter_port` - The port to expose on the target hosts.

`provision_state` - Options: [absent, killed, present, reloaded, restarted, **started** (default), stopped]

## Example Inventory

Snippet below configures targets for the NetApp exporter. Note that `monitoring_username` and `monitoring_password` must be valid SSH credentials for the NetApp hosts.

```
monitoring_username: "Administrator"
monitoring_password: "password123"

netapp_hosts:
- 10.0.0.1
- 10.0.0.2
- 10.0.0.3
```

## Dependencies

```
The docker server >= 0.10.0
```

## Example Playbook

```
- name: Setup NetApp exporters
  hosts: prometheus_scraper
  become: True
  vars:
    provision_state: "started"
  roles:
    - prometheus/generic/setup-netapp-exporter
```

## License

Apache License 2.0

## Author Information

Red Hat Community of Practice & staff of the Red Hat Open Innovation Labs.
