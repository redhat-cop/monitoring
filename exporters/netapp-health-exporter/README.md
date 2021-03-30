# NetApp Health Exporter

Exporter to expose health of NetApp systems to Prometheus.
## Gauges

Gauge status codes:

```
0 - OK
1 - Not OK
2 - Problem retrieving data
```

### Container Image

Prebuilt images are available from the docker repository

```
quay.io/redhat-cop/monitoring-netapp-exporter:latest
```

To build the image yourself

```
docker build --rm -t netapp-exporter .
```

To run the container

```
docker run -p 9418:9418 netapp-exporter:latest
```

You can then call the web server on the defined endpoint, `/health`.

```
curl 'http://127.0.0.1:9418/health?host=10.0.0.1&password=mypassword&username=myusername'
```

### Prometheus config

Assuming:

- the exporter is available on `http://netapp-exporter:9418`
- you use same the username and password for all your consoles

```yml
- job_name: 'netapp'
  metrics_path: /health
  scrape_interval: 1m
  scrape_timeout: 30s
  params:
    username: ['my_user']
    password: ['my_password']
  static_configs:
    - targets:
      - 10.0.0.1
  relabel_configs:
    - source_labels: [__address__]
      target_label: __param_host
    - source_labels: [__param_host]
      target_label: host
    - target_label: __address__
      replacement: netapp-exporter:9418
```
