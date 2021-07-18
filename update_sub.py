import base64
import urllib3
import os
import json
import random
import string

from vm2obs import convert
from settings import CONFIG_DIR, CONNECTIONS_DIR

sub_path = CONFIG_DIR + 'groups.json'


def convert_subcribe(str_b64, node_list=[]):
    blen = len(str_b64)
    con = {}
    with open(CONFIG_DIR+'connections.json', mode='r', encoding='utf-8') as f:
        con = json.load(f)
    str_b64 += "=" * (4 - blen % 4)
    str_links = base64.b64decode(str_b64).decode()
    v_list = str_links.split('\r\n')
    if len(v_list) == 1:
        v_list = str_links.split('\n')
    if not os.path.exists(CONNECTIONS_DIR):
        os.makedirs(CONNECTIONS_DIR)
    if node_list:
        for item in node_list:
            if os.path.exists(CONNECTIONS_DIR+('{}.json'.format(item))):
                os.remove(CONNECTIONS_DIR+('{}.json'.format(item)))
            if item in con.keys():
                con.pop(item)
    node_list.clear()
    for item in v_list:
        if item == "":
            continue
        else:
            ran_str, node_name = convert(item)
            if ran_str == '' or node_name == '':
                continue
            con[ran_str] = {'displayName': node_name}
            node_list.append(ran_str)
    with open(CONFIG_DIR+'connections.json', mode='w', encoding='utf-8') as f:
        f.write(json.dumps(con, indent=4, ensure_ascii=False))
    return node_list


def update_from_url(url, sub_name=''):
    info = {}
    node_list = []
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    if response.status == 200:
        str_b64 = response.data.decode()
    else:
        print('Invalid subscription link or network error. Update failed')
        return

    if (not os.path.exists(sub_path)) or (not os.path.getsize(sub_path)):
        with open(sub_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(info, indent=4, ensure_ascii=False))

    with open(sub_path, 'r', encoding='utf-8') as f:
        info = json.load(f)
    for item in info.keys():
        if url == info[item]['subscriptionOption']['address']:
            node_list = info[item]['connections']
            sub_name = info[item]['displayName']
            info[item]['connections'] = convert_subcribe(str_b64, node_list)
            with open(sub_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(info, indent=4, ensure_ascii=False))
            print("Update subscription %s successfully" % (sub_name))
            return
    info[''.join(random.sample(string.ascii_lowercase, 12))] = {
        'connections': convert_subcribe(str_b64, node_list),
        'displayName': sub_name,
        'subscriptionOption': {
            'address': url
        }}
    with open(sub_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(info, indent=4, ensure_ascii=False))
    print("Update subscription %s successfully" % (sub_name))


def update_from_sub():
    con = {}
    with open(sub_path, 'r', encoding='utf-8') as f:
        con = json.load(f)
    if not con.keys():
        print('No subscription found')
        return
    for item in con.keys():
        url = con[item]['subscriptionOption']['address']
        update_from_url(url)
