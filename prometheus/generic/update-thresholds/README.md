update-thresholds
=========

This role creates alertmanager rule file on reloads prometheus config

Role Variables
--------------
## Default values of variables:
```
ssl_expiration_warning_threshold: '7'
ssl_expiration_critical_threshold: '3'

memory_usage_warning_threshold: '70'
memory_usage_critical_threshold: '90'

disk_usage_warning_threshold: '70'
disk_usage_critical_threshold: '90'
```

Dependencies
------------
```
python >= 2.6
```

Example Playbook
----------------
```
- name: Setup prometheus
  hosts: prometheus_master
  become: True
  vars:
    ssl_expiration_warning_threshold: '10'
    ssl_expiration_critical_threshold: '2'
    memory_usage_warning_threshold: '65'
    memory_usage_critical_threshold: '90'
    disk_usage_warning_threshold: '65'
    disk_usage_critical_threshold: '90'
  roles:
    - prometheus/generic/update-thresholds
```

License
-------

BSD
