##  Install and configure Sysdig agent on OpenShift as a DaemonSet

In order to automate the agent deployment and configuration 2 templates are provided. Sysdig gives the possibility of deploying the Sysdig Cloud component on-premise, in case you want to avoid your monitoring agents traffic leave your Data Centre or to accomplish security teams restrictions:

  - [Cloud Template](templates/sysdig-agent-template.yaml)
  - [On Prem Template](templates/sysdig-agent-onprem-template.yaml)

Follow the steps below in order to deploy the desired agent.

### 1. Install kernel-devel package on all your OCP nodes

  ```bash
  $ yum -y install kernel-devel-$(uname -r)
  ```

### 2. Create a project in which to host Sysdig agent

  ```bash
  $ oc new-project <project>
  ```

### 3a. Deploy DaemonSet and all required objects from the template - **Cloud Agent**

  ```bash
  $ oc process -f templates/sysdig-agent-template.yaml \
    -p NAMESPACE="<project name from previous step>" \
    -p SYSDIG_KEY="<your Sysdig Cloud Access Key>" \
    -p CLUSTER_TAG="<name to tag your cluster with>" \
    | oc create -f-
  ```
### 3b. Deploy DaemonSet and all required objects from the template - **On Prem Agent**

  ```bash
  $ oc process -f templates/sysdig-agent-onprem-template.yaml \
    -p NAMESPACE="<project name from previous step>" \
    -p SYSDIG_KEY="<your Sysdig Cloud Access Key>" \
    -p CLUSTER_TAG="<name to tag your cluster with>" \
    -p COLLECTOR_ADDRESS="Collector Hostname or IP" \
    | oc create -f-
  ```

:bulb: **Check template for more available parameters**
