import re

class NodeConnectivityDisksHealth:
    def __init__(self):
        self.disks = []

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

def get_disks_health(ssh):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("system health node-connectivity disk show")
    exit_status = ssh_stdout.channel.recv_exit_status()
    ssh_output = ssh_stdout.read().decode('ascii').replace("\r", "")

    health = NodeConnectivityDisksHealth()

    # Capture the five columns from the output example shown below
    pattern = re.compile(r'^(\S+)\s+(\S+)\s+([0-9]+)\s+([0-9]+)\s+([a-zA-Z]+)$', re.M)
    for (node, disk, bay, path, status) in re.findall(pattern, ssh_output):
        health.disks.append((node, disk, bay, path, 0 if status == "ok" else 1))
    
    return health

# Output looks like:

#                                                         Num
# Node         Disk Name                             Bay   Paths  Status 
# ------------ ------------------------------------- ----  -----  ----------
# cluster1-01  0a.00.5                                  5    2    ok
# cluster1-01  0a.01.2                                  2    2    ok
# cluster1-01  0b.02.22                                22    2    ok
# cluster1-01  0b.01.3                                  3    2    ok
# cluster1-01  0b.01.5                                  5    2    ok
# cluster1-01  0b.02.17                                17    2    ok
# cluster1-01  0a.01.16                                16    2    ok
# cluster1-01  0a.01.20                                20    2    ok
# cluster1-01  0b.02.23                                23    2    ok
# cluster1-01  0b.02.16                                16    2    ok
# cluster1-01  0b.02.15                                15    2    ok
# cluster1-01  0b.02.3                                  3    2    ok
# cluster1-01  0b.02.6                                  6    2    ok
# cluster1-01  0b.02.12                                12    2    ok
# ...