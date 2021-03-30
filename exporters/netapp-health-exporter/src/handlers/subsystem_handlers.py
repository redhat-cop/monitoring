import re

class SubsystemHandlersHealth:
    def __init__(self):
        self.sas_connect = 2
        self.environment = 2
        self.memory = 2
        self.service_processor = 2
        self.switch_health = 2
        self.cifs_ndo = 2
        self.motherboard = 2
        self.io = 2
        self.metrocluster = 2
        self.metrocluster_node = 2
        self.fhm_switch = 2
        self.fhm_bridge = 2

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

def get_subsystem_handlers_health(ssh):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("system health subsystem show")
    exit_status = ssh_stdout.channel.recv_exit_status()
    ssh_output = ssh_stdout.read().decode('ascii').replace("\r", "")

    health = SubsystemHandlersHealth()

    pattern = re.compile(r'^([\S\-_]+)\s+(\S+)$', re.M)
    for (system, status) in re.findall(pattern, ssh_output):
        # print(f"found {system} with status {status}")
        if hasattr(health, system.lower().replace("-", "_")):
            setattr(health, system.lower().replace("-", "_"), 0 if status == "ok" else 1)
    
    return health

'''
Output looks like:

Subsystem         Health
----------------- ------------------
SAS-connect       ok
Environment       ok
Memory            ok
Service-Processor ok
Switch-Health     ok
CIFS-NDO          ok
Motherboard       ok
IO                ok
MetroCluster      ok
MetroCluster_Node ok
FHM-Switch        ok
FHM-Bridge        ok
12 entries were displayed.
'''