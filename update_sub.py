import re
import base64
import urllib3
import os
import json
import shutil

from vm2obs import convert
from settings import CONFIG_DIR, CONNECTIONS_DIR

sub_path = CONFIG_DIR + 'subscribe.txt'


def force_input():
    subscribe = ''
    while subscribe == '':
        print('Please input subscribe: ', end="")
        subscribe = input()
    return subscribe


# 从subscribe.txt中读取链接
def update_from_txt():
    if not os.path.exists(sub_path):
        url = force_input()
        update_from_url(url)
        return
    with open(sub_path, 'r') as f:
        subscribe = f.readline()
        if subscribe == "":
            url = force_input()
            update_from_url(url)
            return
        if re.match(r'^https?:/{2}\w.+$', subscribe):
            http = urllib3.PoolManager()
            response = http.request('GET', subscribe)
            if response.status == 200:
                str_b64 = response.data.decode()
            else:
                print('Invalid subscription link or network error. Update failed')
                return
        else:
            str_b64 = subscribe
    convert_subcribe(str_b64)


def update_from_url(url):
    with open(sub_path, 'w', encoding='utf-8') as f:
        f.write(url)
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    if response.status == 200:
        str_b64 = response.data.decode()
    else:
        print('Invalid subscription link or network error. Update failed')
        return
    node_list = convert_subcribe(str_b64)
    print("Update successfully")


def convert_subcribe(str_b64):
    blen = len(str_b64)
    connections = {}
    if blen % 4 > 0:
        str_b64 += "=" * (4 - blen % 4)
    str_links = base64.b64decode(str_b64).decode()
    v_list = str_links.split('\r\n')
    if len(v_list) == 1:
        v_list = str_links.split('\n')
    if not os.path.exists(CONNECTIONS_DIR):
        os.makedirs(CONNECTIONS_DIR)
    if os.listdir(CONNECTIONS_DIR):
        shutil.rmtree(CONNECTIONS_DIR)
    node_list = []
    for item in v_list:
        if item == "":
            continue
        else:
            ran_str, node_name = convert(item)
            if ran_str == '' or node_name == '':
                continue
            connections[ran_str] = node_name
            node_list.append(node_name)
    with open(CONFIG_DIR+'connections.json', mode='w', encoding='utf-8') as f:
        f.write(json.dumps(connections, indent=4, ensure_ascii=False))
    return node_list
