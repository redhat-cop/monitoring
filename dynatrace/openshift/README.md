## Prerequisites

The following prerequisites must be met prior to deployment of the Dynatrace Stack

* OpenShift Command Line Tool (`oc`)
  * Can be downloaded from [here](https://mirror.openshift.com/pub/openshift-v3/clients)
* [Openshift Applier](https://github.com/redhat-cop/openshift-applier/) to deploy the content to the OpenShift Container Platform.
* [ansible installed](http://docs.ansible.com/ansible/latest/intro_installation.html)
 * Alternatively follow the instructions to use the [openshift-applier container image](https://github.com/redhat-cop/openshift-applier#openshift-applier-container-image) which includes all the required tools and versions.

### Environment Setup

1. Clone this repository: `git clone https://github.com/redhat-cop/monitoring.git`
2. `cd monitoring/dynatrace/openshift`
3. Run `ansible-galaxy install -r requirements.yml --roles-path=galaxy`
4. Login to OpenShift: `oc login -u <username> <openshift_fqdn>[:port(optional)]`
5. Modify parameters in `params/dynatrace-custom-resource.params` to set the following config option:
 * Dynatrace SaaS URL
5. Modify parameters in `params/dynatrace-secret.params` to set the following config options:
 * Dynatrace API Token (in base64 encoding - see below)
 * Dynatrace PaaS Token (in base64 encoding - see below)


:heavy_exclamation_mark: This stack will create objects that require `cluster-admin` privileges. Ensure you are logged into the Cluster (step 4) with an user with those privileges.

#### Tokens in base64 encoding

Using templates to create OpenShift secrets means that the values needs to be in `base64` encoding. See the Environment Setup section above which values needs to be base64 encoded. To create a base64 value, the following command can be used (where 'token' is the actual token value to be encoded):

```
> echo -n 'token' | base64
```

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
