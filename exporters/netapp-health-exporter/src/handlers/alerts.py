import re

class AlertHealth:
    def __init__(self):
        self.has_alert = 2

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

def get_alerts_health(ssh):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("system health alert show")
    exit_status = ssh_stdout.channel.recv_exit_status()
    ssh_output = ssh_stdout.read().decode('ascii').strip("\n")

    health = AlertHealth()

    health.has_alert = 0 if "This table is currently empty" in ssh_output else 1
    
    return health