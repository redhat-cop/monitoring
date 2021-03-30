# setup-lenovo-flex-exporter

This role will instantiate a Lenovo Flex exporter container on targeted hosts.

## Requirements

Docker must be available and running on the targeted hosts.

## Role Variables

Default values of variables:

```
lenovo_flex_exporter_image: 'quay.io/redhat-cop/monitoring-lenovo-flex-exporter'
lenovo_flex_exporter_image_version: 'latest'
lenovo_flex_exporter_port: '9417'

provision_state: "started"
```

`lenovo_flex_exporter_image` - The lenovo flex exporter image to deploy.

`lenovo_flex_exporter_image_version` - The image tag to deploy.

`lenovo_flex_exporter_port` - The port to expose on the target hosts.

`provision_state` - Options: [absent, killed, present, reloaded, restarted, **started** (default), stopped]

## Example Inventory

Snippet below configures targets for the Lenovo Flex exporter.

```
monitoring_username: "Administrator"
monitoring_password: "password123"

lenovo_flex_hosts:
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
- name: Setup Lenovo Flex exporters
  hosts: prometheus_scraper
  become: True
  vars:
    provision_state: "started"
  roles:
    - prometheus/generic/setup-lenovo-flex-exporter
```

## License

MIT
