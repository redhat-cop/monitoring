# setup-ilo-exporter

This role will instantiate a ilo-exporter container on targeted hosts.

## Requirements

Docker must be available and running on the targeted hosts.

## Role Variables

Default values of variables:

```
ilo_exporter_image: 'quay.io/jacobsee/hpilo-exporter'
ilo_exporter_image_version: 'latest'
ilo_exporter_port: '9416'

provision_state: "started"
```

`ilo_exporter_image` - The ilo exporter image to deploy.

`ilo_exporter_image_version` - The image tag to deploy.

`ilo_exporter_port` - The port to expose on the target hosts.

`provision_state` - Options: [absent, killed, present, reloaded, restarted, **started** (default), stopped]

## Example Inventory

Snippet below configures targets for the iLO exporter.

```
ilo_user: "Administrator"
ilo_password: "password123"
ilo_port: 443

ilo_hosts:
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
- name: Setup ilo exporters
  hosts: prometheus_scraper
  become: True
  vars:
    provision_state: "started"
  roles:
    - prometheus/generic/setup-ilo-exporter
```

## License

MIT
