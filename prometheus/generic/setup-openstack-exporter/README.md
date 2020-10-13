setup-openstack-exporter
=========

This role will template clouds.yaml and instantiate a openstack-exporter container on targeted hosts. The role iterates over "openstack_env" host group

Requirements
------------

Docker must be available and running on the targeted hosts.

Role Variables
--------------
Default values of variables:
```
openstack_exporter_image: 'quay.io/niedbalski/openstack-exporter-linux-amd64'
openstack_exporter_image_version: 'master'
openstack_exporter_port: '9180'
openstack_cloud_name: 'openstack'

provision_state: "started"
```
`openstack_exporter_image` - The openstack exporter image to deploy.
`openstack_exporter_image_version` - The image tag to deploy.
`openstack_exporter_port` - The port to expose on the target hosts.
`openstack_cloud_name` - the cloud name used in clouds.yaml
`provision_state` - Options: [absent, killed, present, reloaded, restarted, **started** (default), stopped]

Example Inventory
-----------------

Snippet below configures targets for the openstack exporter. It was taken from host_vars definition of host in openstack_env hostgroup. The values are used in clouds.yaml.j2 template on the monitoring-hosts nodes.

osp_auth_url: https://openstack-1.example.com:13000/v3
osp_auth_username: myuser
osp_auth_password: mypassword
osp_project_id: my_project_id
osp_project_name: my_project_name
osp_user_domain: my_user_domain
openstack_exporter_port: 9180


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
- name: Setup openstack exporters
  hosts: monitoring-hosts
  become: True
  vars:
    provision_state: "started"
  roles:
    - prometheus/generic/setup-openstack-exporter
```

License
-------

BSD
