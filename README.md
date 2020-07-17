Monitoring Initiative
======================

Infrastructure and Application monitoring to support an OpenShift and containerized ecosystem

## Implementations

* [Prometheus](prometheus)
* [Sysdig](sysdig)
* [Dynatrace](dynatrace)

Getting Started
===============

This repository contains roles and playbooks for deployment and configuration of Prometheus, Alertmanager, Grafana and multiple exporters for exporting metrics. 

The easiest way to deploy your monitoring stack is to run the playbooks in the playbooks/infra-prometheus/ directory using the example inventory in the same directory. 

Repository Content
==================
## Playbooks
* setup-bind-exporter
* setup-grafana-datasource
* setup-ssl-exporter
* setup-prometheus-grafana
* setup-haproxy-exporter

## Roles Prometheus
* setup-alertmanager - deploys alertmanager in docker container
* setup-prometheus - deploys and configures prometheus in a docker container. The scraping targets are configured based on inventory

* setup-ssl-exporter - deploys ssl exporter in docker container. This exporter should be running locally on prometheus instance
* setup-bind-exporter - deploys bind exporter in docker container. This exporter should be running on target host 
* setup-haproxy-exporter - deploys haproxy exporter in docker container. This exporter should be running on target host
* setup-node-exporter - deploys node exporter in docker container. This exporter should be running on target host


## Roles Grafana
* setup-grafana - deploys containerized Grafana with Prometheus as a datasource
* configure-grafana-datasource - configures grafana datasource based on "{{ datasources }}"

More to come! 
