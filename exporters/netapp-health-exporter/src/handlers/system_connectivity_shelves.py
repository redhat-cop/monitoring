import re

class SystemConnectivityShelvesHealth:
    def __init__(self):
        self.shelves = []

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

def get_shelves_health(ssh):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("system health system-connectivity shelf show")
    exit_status = ssh_stdout.channel.recv_exit_status()
    ssh_output = ssh_stdout.read().decode('ascii').replace("\r", "")

    health = SystemConnectivityShelvesHealth()

    pattern = re.compile(r'^([a-zA-Z0-9:]+)\s+(\d+)\s+\S+\s+\d+\s+([a-zA-Z]+)$', re.M)
    for (mac, id, status) in re.findall(pattern, ssh_output):
        # print(f"found {mac} {id} {status}")
        health.shelves.append((mac, id, 0 if status == "ok" else 1))
    
    return health

'''
Output looks like:

                                   Shelf     Connected       Num   Status      
Shelf UUID                         ID        Nodes           Paths
---------------------------------- ------    --------------- ----- ------------
BD:74:86:0F:76:41:74:86                 2    cluster1-02,   4   ok
                                             cluster1-01
BD:74:86:0F:76:41:74:87                 0    cluster1-02,   4   ok
                                             cluster1-01
BD:74:86:0F:76:41:74:88                 1    cluster1-02,   4   ok
                                             cluster1-01
3 entries were displayed.
'''