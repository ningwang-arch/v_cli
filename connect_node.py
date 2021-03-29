import json
import os
import subprocess
from settings import CONNECTIONS_DIR, LAST_CONNECT
from fill_config import config


# 从connections.json中加载节点名称并赋予序号
def print_node():
    path = 'connections.json'
    if not os.path.exists(path):
        print('No node, please update the subscription and try again')
        return
    with open(path, 'r',encoding='utf-8') as f:
        connections = json.load(f)
    values = list(connections.values())
    for i in range(len(values)):
        print(str(i+1)+"."+values[i])


def disconnect():
    child = subprocess.Popen(["pgrep", "-x", "v2ray"],
                             stdout=subprocess.PIPE, shell=False)
    pid = child.communicate()[0]
    if not pid:
        print("No target pid to kill,please check")
        return
    result = os.system("kill -9 "+pid.decode())
    if os.path.exists('connect.log'):
        os.remove('connect.log')
    if result == 0:
        print("Disconnect successfully")
    else:
        print("Failed to disconnect, please kill the process manually")


def current():
    if ((not os.path.exists(LAST_CONNECT)) or (not os.path.getsize(LAST_CONNECT))):
        print("No connection currently!")
        return
    with open(LAST_CONNECT, 'r',encoding='utf-8') as f:
        last_dict = json.load(f)
    if 'node' not in last_dict:
        print("No connection currently!")
    else:
        with open("connections.json", mode='r') as f:
            node_dict = json.load(f)
        node = last_dict['node']
        print("Current connect: "+node_dict[node])


def convet_num_to_nodestr(choice):
    path = 'connections.json'
    if not os.path.exists(path):
        print('No node, please update the subscription and try again')
        return
    with open(path, 'r') as f:
        connections = json.load(f)
    values = list(connections.values())
    node_name = values[choice-1]
    keys = list(connections.keys())
    if choice > len(values):
        return ""
    for i in range(len(keys)):
        if connections[keys[i]] == node_name:
            return keys[i]


def connect(choice, path="/usr/bin/v2ray", http_port=8889, socks_port=1089):
    path = path.replace("\\", '/')
    if (("/" in path) and (not os.path.exists(path))):
        print("No such file!")
        return
    child = subprocess.Popen(["pgrep", "-x", "v2ray"],
                             stdout=subprocess.PIPE, shell=False)
    pid = child.communicate()[0]
    if pid:
        result = os.system("kill -9 "+pid.decode())
        if result != 0:
            print("Port occupied or no executable program")
            return
    node_name = convet_num_to_nodestr(choice)
    connect_info = {"node": node_name, "path": path}
    with open('lastconnect.json', 'w') as f:
        f.write(json.dumps(connect_info, indent=4))
    if node_name == "":
        print('Invalid choice')
        return
    config(node_name, http_port, socks_port)
    os.system("nohup %s -config config.json > connect.log 2>&1 &" % path)
    print("Connect successfully")


def connect_default():
    with open('lastconnect.json', 'r',encoding='utf-8') as f:
        info = json.load(f)
    path = info['path']
    os.system("nohup %s -config config.json > connect.log 2>&1 &" % path)
    print("Connect successfully")
