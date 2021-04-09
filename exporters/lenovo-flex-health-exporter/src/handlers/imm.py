import paramiko
import re
import jinja2
from urllib.parse import urlparse
from urllib.parse import parse_qs
from jinja2 import Environment, FileSystemLoader

class IMMHealth:
    # 2 = unable to fetch
    # 1 = reported problem / off
    # 0 = healthy / on
    # except for restarts, which is a counter
    def __init__(self):
        self.restarts = 0
        self.power = 2
        self.state = 2
        self.storage = 2
        self.processors = 2
        self.memory = 2
        self.system = 2

def get_health(request):
    host = ''
    username = ''
    password = ''
    query_components = parse_qs(urlparse(request.path).query)
    if 'host' in query_components:
        host = query_components["host"][0]
    if 'username' in query_components:
        username = query_components["username"][0]
    if 'password' in query_components:
        password = query_components["password"][0]

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("syshealth summary")
    exit_status = ssh_stdout.channel.recv_exit_status()
    if exit_status == 0:
        request.send_response(200)
        request.send_header("Content-type", "text/plain")
        request.end_headers()
    else:
        request.send_response(500)
        request.send_header("Content-type", "text/plain")
        request.end_headers()
    ssh.close()
    stdout_str = ssh_stdout.read().decode('ascii')

    health = IMMHealth()

    # see below for what's going on here [0]
    pattern = re.compile(r"([a-zA-Z]+\s?[a-zA-Z]+)\s+([a-zA-Z0-9]+\s?[a-zA-Z0-9]+)\s*$", re.M)
    for (system, status) in re.findall(pattern, stdout_str):
        if system == "Restarts":
            health.restarts = status
        elif system == "Local Storage":
            health.storage =  0 if status == "Normal" else 1
        elif system == "Processors":
            health.processors = 0 if status == "Normal" else 1
        elif system == "Memory":
            health.memory = 0 if status == "Normal" else 1
        elif system == "System":
            health.system = 0 if status == "Normal" else 1
        elif system == "Power":
            health.power = 0 if status == "On" else 1
        elif system == "State":
            health.state = 0 if status == "OS booted" else 1

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    template = env.get_template('imm.j2')

    return template.render(health=health)

# [0]
# We capture following output of `syshealth summary`.
#
# Power     On
# State     OS booted
# Restarts  460
# Component Type     Status
# ==================================
# Local Storage      Normal
# Processors         Normal
# Memory             Normal
# System             Normal