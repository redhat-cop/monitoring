## Prerequisites

The following prerequisites must be met prior to deployment of the Dynatrace Stack

* OpenShift Command Line Tool (`oc`)
  * Can be downloaded from [here](https://mirror.openshift.com/pub/openshift-v3/clients)
* [Openshift Applier](https://github.com/redhat-cop/openshift-applier/) to deploy the content to the OpenShift Container Platform.
* [ansible installed](http://docs.ansible.com/ansible/latest/intro_installation.html)
 * Alternatively follow the instructions to use the [openshift-applier container image](https://github.com/redhat-cop/openshift-applier#openshift-applier-container-image) which includes all the required tools and versions.
* Access to Dynatrace Monitoring solution and API + PaaS tokens created. Please see [this link](https://www.dynatrace.com/support/help/get-started/introduction/why-do-i-need-an-access-token-and-an-environment-id/#access-tokens) for more information about the tokens, and how to generate these. 

### Environment Setup

1. Clone this repository: `git clone https://github.com/redhat-cop/monitoring.git`
2. `cd monitoring/dynatrace/openshift`
3. Run `ansible-galaxy install -r requirements.yml --roles-path=galaxy`
4. Login to OpenShift: `oc login -u <username> <openshift_fqdn>[:port(optional)]`
5. Modify parameters in `params/dynatrace-custom-resource.params` to set the following config option:
 * Dynatrace SaaS URL
5. Modify parameters in `params/dynatrace-secret.params` to set the following config options:
 * Dynatrace API Token
 * Dynatrace PaaS Token


:heavy_exclamation_mark: This stack will create objects that require `cluster-admin` privileges. Ensure you are logged into the Cluster (step 4) with an user with those privileges.


### Deploy the Dynatrace Stack

Run the [openshift-applier](https://github.com/redhat-cop/openshift-applier) to create the project and deploy required objects
```
> ansible-playbook -i ./inventory galaxy/openshift-applier/playbooks/openshift-cluster-seed.yml
```

### Delete the Dynatrace Stack

Run the [openshift-applier](https://github.com/redhat-cop/openshift-applier) to deprovision the Dynatrace Stack and delete all the objects created during the deploying phase
```
> ansible-playbook -i ./inventory galaxy/openshift-applier/playbooks/openshift-cluster-seed.yml -e 'provision=false'
```
