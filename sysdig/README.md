## Notes around the initial resources to be created for Sysdig monitoring

### Agent Documentation

  - Install and configure agent on RHEL
  - Install and configure agent on OpenShift as a DaemonSet

### Agent deployment

  - Ansible role to deploy and configure agent on RHEL
  - YAML template to deploy and configure agent as a daemonset on OpenShift (Check how to fit applier on this as we need to install kernel-devel package on every host as pre-deploy step)

### On-prem Appliance Documentation

  - Install and configure appliance on RHEL
  - Install and configure appliance on OpenShift

### On-prem Appliance deployment

  - Ansible role to deploy and configure the appliance on RHEL
  - YAML template to deploy and configure the appliance on OpenShift (Check how to fit applier on this as we need to modify iptables rules as pre-deploy step)

### Existing documentation and code resources from sysdig to review, include or point to

  - https://www.sysdig.org/wiki/how-to-install-sysdig-for-linux/
  - https://support.sysdig.com/hc/en-us/articles/115003032526-On-Premises-Software-Sizing-Guide
  - https://github.com/draios/
  - https://support.sysdig.com/hc/en-us/articles/211421063-Sysdig-Install-OpenShift
  - https://sysdig.com/resources/
