import json
import os
from settings import LAST_CONNECT, CONFIG_DIR, PLATFORM
from fill_config import config

config_path = CONFIG_DIR+'config.json'
log_path = CONFIG_DIR+'connect.log'


def print_node():
    cnt = 1
    sub_path = CONFIG_DIR+'groups.json'
    con_path = CONFIG_DIR+'connections.json'
    conn = {}
    sub = {}
    with open(sub_path, 'r', encoding='utf-8') as f:
        sub = json.load(f)
    with open(con_path, 'r', encoding='utf-8') as f:
        conn = json.load(f)
    # format  {"sub_name":[node_name_list]}
    info = {}
    for item in sub.keys():
        connections = sub[item]['connections']
        for i in range(len(connections)):
            connections[i] = str(cnt)+'. '+conn[connections[i]]['displayName']
            cnt += 1
        info[sub[item]['displayName']] = connections
    print(json.dumps(info, indent=4, ensure_ascii=False))


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
    con_path = CONFIG_DIR+'connections.json'
    if ((not os.path.exists(LAST_CONNECT)) or (not os.path.getsize(LAST_CONNECT))):
        print("No connection currently!")
        return
    with open(LAST_CONNECT, 'r', encoding='utf-8') as f:
        last_dict = json.load(f)
    if 'node' not in last_dict:
        print("No connection currently!")
    else:
        with open(con_path, mode='r') as f:
            node_dict = json.load(f)
        node = last_dict['node']
        if node == "":
            print('Error!')
            return
        print("Current connect: "+node_dict[node]['displayName'])


def convet_num_to_nodestr(choice):
    sub_path = CONFIG_DIR+'groups.json'
    con_path = CONFIG_DIR+'connections.json'
    if not os.path.exists(con_path):
        print('No node, please update the subscription and try again')
        return ""
    conn = {}
    sub = {}
    with open(sub_path, 'r', encoding='utf-8') as f:
        sub = json.load(f)
    with open(con_path, 'r', encoding='utf-8') as f:
        conn = json.load(f)
    # format  {"sub_name":[node_name_list]}
    info = {}
    values = []
    for item in sub.keys():
        connections = sub[item]['connections']
        for i in range(len(connections)):
            values.append(conn[connections[i]]['displayName'])
    if choice > len(values):
        print('Bad choice!')
        return ""
    node_name = values[choice-1]
    for item in conn.keys():
        if conn[item]['displayName'] == node_name:
            return item


def connect(choice, path="/usr/bin/v2ray", http_port=8889, socks_port=11223):
    path = path.replace("\\", '/')

    if (("/" in path) and (not os.path.exists(path))):
        print("No such file!")
        return
    if PLATFORM == 'linux':
        if os.system('pgrep -x v2ray >/dev/null 2>&1') == 0:
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
    node_str = convet_num_to_nodestr(choice)
    node_name = ''

    connect_info = {"node": node_str, "path": path,
                    "http_port": http_port, "socks_port": socks_port}
    with open(CONFIG_DIR+'lastconnect.json', 'w') as f:
        f.write(json.dumps(connect_info, indent=4))
    if node_str == "":
        print('Invalid choice')
        return
    with open(CONFIG_DIR+'connections.json') as f:
        node_name = json.load(f)[node_str]['displayName']
        pass
    config(node_str, http_port, socks_port)
    if PLATFORM == 'linux':
        os.system("exec %s -config %s > %s 2>&1 &" %
                  (path, config_path, log_path))
    elif PLATFORM == 'win32':
        filepath, fullflname = os.path.split(path)
        os.chdir(filepath)
        os.system("start /b %s -config %s > %s 2>&1 &" %
                  (fullflname, config_path, log_path))
    print("Connect  %s successfully" % (node_name))


def connect_default():
    with open(CONFIG_DIR+'lastconnect.json', 'r', encoding='utf-8') as f:
        info = json.load(f)
    path = info['path']
    path = path.replace("\\", '/')

    if (("/" in path) and (not os.path.exists(path))):
        print("No such file!")
        return
    if PLATFORM == 'linux':
        os.system("exec %s -config %s > %s 2>&1 &" %
                  (path, config_path, log_path))
    elif PLATFORM == 'win32':
        filepath, fullflname = os.path.split(path)
        os.chdir(filepath)
        os.system("start /b %s -config %s > %s 2>&1 &" %
                  (fullflname, config_path, log_path))
    print("Connect successfully")
