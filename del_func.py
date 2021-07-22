import json
import os
from settings import CONFIG_DIR, CONNECTIONS_DIR
from connect_node import convet_num_to_nodestr


def delete_outbounds(node_str: str):
    conn_path = CONFIG_DIR+'connections.json'
    conn = {}
    target_path = CONNECTIONS_DIR+('{}.json'.format(node_str))
    if not os.path.exists(target_path):
        print('No such file: %s' % (target_path))
        return ""
    os.remove(target_path)
    with open(conn_path, 'r', encoding='utf-8') as f:
        conn = json.load(f)
    f.close()
    if node_str in conn.keys():
        node_name = conn[node_str]['displayName']
        conn.pop(node_str)
        with open(conn_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(conn, indent=4, ensure_ascii=False))
        f.close()
        return node_name
    else:
        return ""


def delete_node(choice: int):
    sub_path = CONFIG_DIR+'groups.json'
    sub_info = {}
    node_str = convet_num_to_nodestr(choice)
    if node_str == '':
        print('Delete failed')
        return
    node_name = delete_outbounds(node_str)
    if node_name == '':
        print('Delete failed')
        return
    with open(sub_path, 'r', encoding='utf-8') as f:
        sub_info = json.load(f)
        f.close()
    for item in sub_info.keys():
        info = sub_info[item]['connections']
        if node_str in info:
            info.remove(node_str)
    with open(sub_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(sub_info, indent=4, ensure_ascii=False))
    f.close()
    print('Delete node %s successful' % (node_name))


def delete_sub(sub_name: str):
    sub_path = CONFIG_DIR+'groups.json'
    sub_info = {}
    with open(sub_path, 'r', encoding='utf-8') as f:
        sub_info = json.load(f)
    f.close()
    for item in sub_info.keys():
        if sub_name == sub_info[item]['displayName']:
            connections = sub_info[item]['connections']
            for conn in connections:
                delete_outbounds(conn)
            sub_info.pop(item)
            print('Delete subscription %s successfully' % (sub_name))
            with open(sub_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(sub_info, indent=4, ensure_ascii=False))
            f.close()
            return
    print('No such subscription')
    return
