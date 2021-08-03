import base64
import urllib3
import os
import json
import random
import string

from vm2obs import convert
from settings import CONFIG_DIR, CONNECTIONS_DIR, clean_blocks, load_default_config

sub_path = CONFIG_DIR + 'groups.json'
conn_path = CONFIG_DIR+'connections.json'
last_path = CONFIG_DIR+'lastconnect.json'


def load_last_conn_node(**kwargs):
    last_dict = {}
    with open(CONFIG_DIR+'lastconnect.json', 'r', encoding='utf-8') as f:
        last_dict = json.load(f)
    if not kwargs:
        return last_dict['node']
    elif 'node' in kwargs.keys():
        f.close()
        last_dict['node'] = kwargs['node']
        with open(CONFIG_DIR+'lastconnect.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(last_dict, indent=4, ensure_ascii=False))


def update_lastconnection(**kwargs):
    conn = {}
    with open(CONFIG_DIR+'connections.json', 'r', encoding='utf-8') as f:
        conn = json.load(f)
    if 'ran_str' == list(kwargs.keys())[0]:
        return conn[kwargs['ran_str']]['displayName']
    if 'node_name' == list(kwargs.keys())[0]:
        for item in conn.keys():
            if conn[item]['displayName'] == kwargs['node_name']:
                return item


def convert_subcribe(str_b64, node_list=[]):
    blen = len(str_b64)
    con = {}
    if os.path.exists(CONFIG_DIR+'connections.json'):
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
    conf = load_default_config()
    node_name = ''
    if conf['node'] != '':
        node_name = update_lastconnection(ran_str=load_last_conn_node())
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
            if conf['node'] != '':
                load_last_conn_node(
                    node=update_lastconnection(node_name=node_name))
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
    if conf['node'] != '':
        load_last_conn_node(node=update_lastconnection(node_name=node_name))


def get_sub_url(sub_name):
    with open(sub_path, 'r', encoding='utf-8') as f:
        info = json.load(f)
    for item in info:
        if info[item]['displayName'] == sub_name.replace('%20', ' '):
            return info[item]['subscriptionOption']['address']


def update_from_sub():
    con = {}
    if not os.path.exists(sub_path):
        print('No subscription found')
        return
    with open(sub_path, 'r', encoding='utf-8') as f:
        con = json.load(f)
    if not con.keys():
        print('No subscription found')
        return
    for item in con.keys():
        url = con[item]['subscriptionOption']['address']
        update_from_url(url)


def update(blocks: list):
    blocks = clean_blocks(blocks)
    if len(blocks) > 1:
        print('Error format,should be `update sub_name` or `update [url]`')
    if len(blocks) == 0:
        update_from_sub()
    elif blocks[0].startswith('https://') or blocks[0].startswith('http://'):
        sub_name = input('Please input sub_name : ')
        update_from_url(blocks[0], sub_name)
    else:
        update_from_url(get_sub_url(blocks[0]))
