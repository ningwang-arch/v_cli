import json
import os
import sys
import subprocess
from settings import CONNECTIONS_DIR, LAST_CONNECT, CONFIG_DIR, PLATFORM
from fill_config import config

config_path = CONFIG_DIR+'config.json'
log_path = CONFIG_DIR+'connect.log'

# 从connections.json中加载节点名称并赋予序号


def print_node():
    path = CONFIG_DIR+'connections.json'
    if not os.path.exists(path):
        print('No node, please update the subscription and try again')
        return
    with open(path, 'r', encoding='utf-8') as f:
        connections = json.load(f)
    values = list(connections.values())
    for i in range(len(values)):
        print(str(i+1)+"."+values[i])


def disconnect():
    if PLATFORM == 'linux':
        result = os.system("pkill v2ray")
        if os.path.exists(CONFIG_DIR+'connect.log'):
            os.remove(CONFIG_DIR+'connect.log')
        if result == 0:
            print("Disconnect successfully")
        else:
            print("Failed to disconnect, please kill the process manually")
    elif PLATFORM == 'win32':
        result = os.system('taskkill /f /im v2ray.exe >nul 2>nul')
        if result != 0:
            print('No such task or failed to disconnect!')
        else:
            print("Disconnect successfully")


def current():
    if ((not os.path.exists(LAST_CONNECT)) or (not os.path.getsize(LAST_CONNECT))):
        print("No connection currently!")
        return
    with open(LAST_CONNECT, 'r', encoding='utf-8') as f:
        last_dict = json.load(f)
    if 'node' not in last_dict:
        print("No connection currently!")
    else:
        with open(LAST_CONNECT, mode='r') as f:
            node_dict = json.load(f)
        node = last_dict['node']
        print("Current connect: "+node_dict[node])


def convet_num_to_nodestr(choice):
    path = CONFIG_DIR+'connections.json'
    if not os.path.exists(path):
        print('No node, please update the subscription and try again')
        return
    with open(path, 'r', encoding='utf-8') as f:
        connections = json.load(f)
    values = list(connections.values())
    node_name = values[choice-1]
    keys = list(connections.keys())
    if choice > len(values):
        return ""
    for i in range(len(keys)):
        if connections[keys[i]] == node_name:
            return keys[i]


def connect(choice, path="/usr/bin/v2ray", http_port=8889, socks_port=11223):
    path = path.replace("\\", '/')

    if (("/" in path) and (not os.path.exists(path))):
        print("No such file!")
        return
    if PLATFORM == 'linux':
        result = os.system("pkill v2ray")
        if result != 0:
            print("Port occupied or no executable program")
            return
    elif PLATFORM == 'win32':
        if os.system('tasklist -v | findstr v2ray > NUL') != 1:
            result = os.system('taskkill /f /im v2ray.exe >nul 2>nul')
            if result != 0:
                print('Port occupied or no executable program')
                return
    node_name = convet_num_to_nodestr(choice)
    connect_info = {"node": node_name, "path": path,
                    "http_port": http_port, "socks_port": socks_port}
    with open(CONFIG_DIR+'lastconnect.json', 'w') as f:
        f.write(json.dumps(connect_info, indent=4))
    if node_name == "":
        print('Invalid choice')
        return
    config(node_name, http_port, socks_port)
    if PLATFORM == 'linux':
        os.system("exec %s -config %s > %s 2>&1 &" %
                  (path, config_path, log_path))
    elif PLATFORM == 'win32':
        filepath, fullflname = os.path.split(path)
        os.chdir(filepath)
        os.system("start /b %s -config %s > %s 2>&1 &" %
                  (fullflname, config_path, log_path))
    print("Connect successfully")


def connect_default():
    with open(CONFIG_DIR+'lastconnect.json', 'r', encoding='utf-8') as f:
        info = json.load(f)
    path = info['path']
    if PLATFORM == 'linux':
        os.system("exec %s -config %s > %s 2>&1 &" %
                  (path, config_path, log_path))
    elif PLATFORM == 'win32':
        filepath, fullflname = os.path.split(path)
        os.chdir(filepath)
        os.system("start /b %s -config %s > %s 2>&1 &" %
                  (fullflname, config_path, log_path))
    print("Connect successfully")
