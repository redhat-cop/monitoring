import paramiko
import re
import jinja2
from urllib.parse import urlparse
from urllib.parse import parse_qs
from jinja2 import Environment, FileSystemLoader

class CMMHealth:
    def __init__(self):
        self.blade = []
        self.blower = []
        self.power = []
        self.mm = []
        self.switch = []
        self.mt = []
        self.fanmux = []

def get_health(request):
    host_str = ''
    username = ''
    password = ''
    query_components = parse_qs(urlparse(request.path).query)
    if 'host' in query_components:
        host_str = query_components["host"][0]
    if 'username' in query_components:
        username = query_components["username"][0]
    if 'password' in query_components:
        password = query_components["password"][0]

    hosts = host_str.split(",")

    ssh_output = None

    # Loop though the hosts that were passed in here.
    # We do this because a Flex server has multiple CMMs.
    # Only one is "active" at a time - and the others won't respond at all.
    # As long as one of the hosts responds - we consider it a pass.
    for host in hosts:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(host, username=username, password=password)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("health -l 2") # two levels of health detail gives a nice summary
            exit_status = ssh_stdout.channel.recv_exit_status()
            ssh.close()
            if ssh_stderr.read().decode('ascii') == "":
                ssh_output = ssh_stdout.read().decode('ascii').strip("\n")
                break
        except:
            pass

    if ssh_output is None:
        request.send_response(500)
        request.send_header("Content-type", "text/plain")
        request.end_headers()
        return ""
    else:
        request.send_response(200)
        request.send_header("Content-type", "text/plain")
        request.end_headers()

    health = CMMHealth()

    # see below for what's going on here [0]
    pattern = re.compile(r'([a-z]+)\[(\d+)\]\s*:\s*(\S+)')
    for (system, instance, status) in re.findall(pattern, ssh_output):
        getattr(health, system).append((instance, 0 if status == "OK" else 1))

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    template = env.get_template('cmm.j2')

    return template.render(health=health)


# [0]
# We capture the system name, the instance number, and the health
# status from the output of `health -l 2`.
# The command's output looks something like this:
#
#          power[1]  :          OK
#          power[2]  :          OK
#          power[3]  :          OK
#          power[4]  :          OK
#          power[5]  :          OK
#          power[6]  :          OK
#          mm[1]     :          OK
#          mm[2]     :          OK
#          switch[1] :          OK
#          switch[2] :          OK
#          switch[3] :          OK
#          switch[4] :          OK
