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
## Playbooks (monitoring-hosts)
* setup-grafana-datasource
* setup-ssl-exporter
* setup-ilo-exporter
* setup-lenovo-flex-exporter
* setup-openstack-exporter
* setup-netapp-exporter
* setup-prometheus-grafana
* add-targets
* setup-openstack-exporter
* add-openshift

## Playbooks (monitoring-targets)
* setup-bind-exporter
* setup-haproxy-exporter
* setup-node-exporter
* setup-exporters

## Playbooks (one-stop)
* [setup-all](playbooks/infra-prometheus/setup-all.yml)
    * A one-stop-shop for spinning up an entire simple monitoring stack with some targets built-in
    * Host setup:
        * Install Docker (only if tag `install` is set)
        * setup-prometheus
        * setup-alertmanager
        * update-thresholds
    * Exporter roles included (on monitoring-hosts):
        * [setup-ssl-exporter](prometheus/generic/setup-alertmanager)
        * [setup-ilo-exporter](prometheus/generic/setup-ilo-exporter)
        * [setup-lenovo-flex-exporter](prometheus/generic/setup-lenovo-flex-exporter)
        * [setup-netapp-exporter](prometheus/generic/setup-netapp-exporter)
        * [setup-openstack-exporter](prometheus/generic/setup-openstack-exporter)
    * Exporter roles included (on remote targets):
        * cloudalchemy.node_exporter
    * Target configuration roles
        * add-target

## Roles Prometheus
* setup-alertmanager - deploys alertmanager in docker container
* setup-prometheus - deploys and configures prometheus in a docker container. The scraping targets are configured based on inventory
* add-target - configures prometheus targets
* update-thresholds - updates the alertmanager thresholds

* setup-ssl-exporter - deploys ssl exporter in docker container. This exporter should be running locally on prometheus instance
* setup-openstack-exporter - deploys openstack exporter in docker container. This exporter should be running locally on prometheus instance
* setup-bind-exporter - deploys bind exporter in docker container. This exporter should be running on target host
* setup-haproxy-exporter - deploys haproxy exporter in docker container. This exporter should be running on target host
* setup-node-exporter - deploys node exporter in docker container. This exporter should be running on target host

## Roles Grafana
* setup-grafana - deploys containerized Grafana with Prometheus as a datasource
* configure-grafana-datasource - configures grafana datasource based on "{{ datasources }}"

## Files
* alertmanager_rules - contains example rule file
* dashboards - contains collection of grafana dashboards
* ocp_alertmanager_templates - contains example alertmanager template to be applied on alertmanager-main secret in OCP

More to come! 
