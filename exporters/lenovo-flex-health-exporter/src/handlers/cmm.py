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

    for host in hosts:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(host, username=username, password=password)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("health -l 2")
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

    pattern = re.compile(r'([a-z]+)\[(\d+)\]\s*:\s*(\S+)')
    for (system, instance, status) in re.findall(pattern, ssh_output):
        getattr(health, system).append((instance, 0 if status == "OK" else 1))

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    template = env.get_template('cmm.j2')

    return template.render(health=health)