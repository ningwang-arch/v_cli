import re
import base64
import urllib3
import os
import json
import shutil

from vm2obs import convert


sub_path = 'subscribe.txt'


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
    with open(sub_path, 'r') as f:
        f.write(url)
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    if response.status == 200:
        str_b64 = response.data.decode()
    else:
        print('Invalid subscription link or network error. Update failed')
        return
    convert_subcribe(str_b64)


def convert_subcribe(str_b64):
    blen = len(str_b64)
    connections = {}
    if blen % 4 > 0:
        str_b64 += "=" * (4 - blen % 4)
    str_links = base64.b64decode(str_b64).decode()
    v_list = str_links.split('\r\n')
    if len(v_list) == 1:
        v_list = str_links.split('\n')
    if not os.path.exists('connections'):
        os.makedirs('connections')
    if os.listdir('connections'):
        shutil.rmtree('connections')
    for item in v_list:
        if item == "":
            continue
        else:
            ran_str, node_name = convert(item)
            if ran_str == '' or node_name == '':
                continue
            connections[ran_str] = node_name
    with open('connections.json', mode='w', encoding='utf-8') as f:
        f.write(json.dumps(connections, indent=4, ensure_ascii=False))
    print("Update successfully")
