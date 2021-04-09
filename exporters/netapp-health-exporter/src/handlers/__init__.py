import paramiko
import re
import jinja2
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs
from jinja2 import Environment, FileSystemLoader

from handlers import subsystem_handlers, alerts, node_connectivity_disks, system_connectivity_shelves

class Health:
    def __init__(self):
        self.SubsystemHandlers = None
        self.AlertHealth = None
        self.NodeConnectivityDisksHealth = None
        self.SystemConnectivityShelvesHealth = None

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
    health = Health()
    # Fetch health in the four ways that we know how:
    health.SubsystemHandlers = subsystem_handlers.get_subsystem_handlers_health(ssh)
    health.AlertHealth = alerts.get_alerts_health(ssh)
    health.NodeConnectivityDisksHealth = node_connectivity_disks.get_disks_health(ssh)
    health.SystemConnectivityShelvesHealth = system_connectivity_shelves.get_shelves_health(ssh)
    ssh.close()

    request.send_response(200)
    request.send_header("Content-type", "text/plain")
    request.end_headers()

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    template = env.get_template('health.j2')

    return template.render(health=health)