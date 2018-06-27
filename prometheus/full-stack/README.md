## Prerequisites

The following prerequisites must be met prior to beginning to deploy GitLab CE

* 1 [Persistent Volume](https://docs.openshift.com/container-platform/latest/architecture/additional_concepts/storage.html) or a cluster that supports [dynamic provisioning with a default StorageClass](https://docs.openshift.com/container-platform/latest/install_config/storage_examples/storage_classes_dynamic_provisioning.html)
* OpenShift Command Line Tool
* [Openshift Applier](https://github.com/redhat-cop/openshift-applier/) to deploy GitLab CE. As a result you'll need to have [ansible installed](http://docs.ansible.com/ansible/latest/intro_installation.html)
* The following traffic must be enabled for the Cluster Nodes on the underlaying Firewall
    * 9100/TCP
    * 1936/TCP
    * 8443/TCP


### Environment Setup

1. Clone this repository: `git clone https://gitlab.consulting.redhat.com/mentenza/monitoring-initiative.git`
2. `cd monitoring-initiative/prometheus/full-stack`
3. Run `ansible-galaxy install -r requirements.yml --roles-path=galaxy`
4. Login to OpenShift: `oc login -u <username> https://master.example.com:8443`
5. Modify parameters in `files/params/prometheus-stack-params` according to your requirements

:heavy_exclamation_mark: This stack will create objects that require `cluster-admin` privileges. Ensure you are logged into the Cluster (step 4) with an user with those privileges

### Deploy Prometheus Stack (Prometheus, Node Exporter, Kube Metric, AlertManager and Grafana)

Run the openshift-applier to create the project and deploy required objects
```
ansible-playbook -i ./inventory galaxy/openshift-applier/playbooks/openshift-cluster-seed.yml
```

### Delete Prometheus Stack

```
$ oc delete ns ${NAMESPACE}         - Name of the namespace configured for the Stack
$ oc delete scc prometheus-anyuid prometheus-privileged
$ oc delete clusterrolebinding prometheus-role-bind
$ oc delete clusterrole prometheus-role
