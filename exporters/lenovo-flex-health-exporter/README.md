# Lenovo Flex System Health Exporter

Exporter to expose health of Lenovo/IBM Flex CMM & IMM systems to Prometheus.
## Gauges

Gauge status codes:

```
0 - OK
1 - Not OK
2 - Problem retrieving data
```
## Output Examples

Healthy CMM:

```
# HELP cmm_health_blade Blade health as collected from the Flex System
# TYPE cmm_health_blade gauge
cmm_health_blade{blade="0"} 0
cmm_health_blade{blade="1"} 0
cmm_health_blade{blade="2"} 0

# HELP cmm_health_blower Blower (fan) health as collected from the Flex System
# TYPE cmm_health_blower gauge
cmm_health_blower{blower="0"} 0
cmm_health_blower{blower="1"} 0
cmm_health_blower{blower="2"} 0

# HELP cmm_health_power PSU health as collected from the Flex System
# TYPE cmm_health_power gauge
cmm_health_power{power="0"} 0
cmm_health_power{power="1"} 0

# HELP cmm_health_mm MM health as collected from the Flex System
# TYPE cmm_health_mm gauge
cmm_health_mm{mm="0"} 0
cmm_health_mm{mm="1"} 0

# HELP cmm_health_switch Switch health as collected from the Flex System
# TYPE cmm_health_switch gauge
cmm_health_switch{switch="0"} 0
cmm_health_switch{switch="1"} 0
cmm_health_switch{switch="2"} 0

# HELP cmm_health_mt MT health as collected from the Flex System
# TYPE cmm_health_mt gauge
cmm_health_mt{mt="0"} 0

# HELP cmm_health_fanmux Fan health as collected from the Flex System
# TYPE cmm_health_fanmux gauge
cmm_health_fanmux{fanmux="0"} 0
cmm_health_fanmux{fanmux="1"} 0
```

Healthy IMM:

```
# HELP imm_restarts Blade power status as collected from the Flex System (0 if on)
# TYPE imm_restarts counter
imm_restarts{} 0

# HELP imm_health_power Blade power status as collected from the Flex System (0 if on)
# TYPE imm_health_power gauge
imm_health_power{} 0

# HELP imm_health_state Blade state as collected from the Flex System (0 if booted to OS)
# TYPE imm_health_state gauge
imm_health_state{} 0

# HELP imm_health_storage Storage health as collected from the Flex System
# TYPE imm_health_storage gauge
imm_health_storage{} 0

# HELP imm_health_processors Processor health as collected from the Flex System
# TYPE imm_health_processors gauge
imm_health_processors{} 0

# HELP imm_health_memory Memory health as collected from the Flex System
# TYPE imm_health_memory gauge
imm_health_memory{} 0

# HELP imm_health_system Blade system health as collected from the Flex System
# TYPE imm_health_system gauge
imm_health_system{} 0
```

### Container Image

Prebuilt images are available from the docker repository

```
quay.io/redhat-cop/monitoring-lenovo-flex-exporter:latest
```

To build the image yourself

```
docker build --rm -t lenovo-flex-exporter .
```

To run the container

```
docker run -p 9417:9417 lenovo-flex-exporter:latest
```

You can then call the web server on the defined endpoint, `/cmmhealth` or `/immhealth`.

```
curl 'http://127.0.0.1:9417/immhealth?host=10.0.0.1&password=mypassword&username=myusername'
curl 'http://127.0.0.1:9417/cmmhealth?host=10.0.0.1,10.0.0.2&password=mypassword&username=myusername'
```

Note that `/cmmhealth` is able to parse a comma-separated list of hosts as a redundant set of CMMs, any of which may be the current primary/active CMM. That is, if at least one CMM in the list returns health data, the entire set is considered "up". This way, any non-primary CMMs are not reflected as "down" in Prometheus.

### Prometheus config

Assuming:

- the exporter is available on `http://lenovo-flex-exporter:9417`
- you use same the username and password for all your consoles

```yml
- job_name: 'lenovo-flex-cmm'
  metrics_path: /cmmhealth
  scrape_interval: 1m
  scrape_timeout: 30s
  params:
    username: ['my_user']
    password: ['my_password']
  static_configs:
    - targets:
      - 10.0.0.1,10.0.0.2
  relabel_configs:
    - source_labels: [__address__]
      target_label: __param_host
    - source_labels: [__param_host]
      target_label: host
    - target_label: __address__
      replacement: lenovo-flex-exporter:9417

- job_name: 'lenovo-flex-imm'
  metrics_path: /immhealth
  scrape_interval: 1m
  scrape_timeout: 30s
  params:
    username: ['my_user']
    password: ['my_password']
  static_configs:
    - targets:
      - 10.0.0.3
      - 10.0.0.4
  relabel_configs:
    - source_labels: [__address__]
      target_label: __param_host
    - source_labels: [__param_host]
      target_label: host
    - target_label: __address__
      replacement: lenovo-flex-exporter:9417
```
