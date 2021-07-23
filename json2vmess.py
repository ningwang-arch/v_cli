from settings import CONFIG_DIR, CONNECTIONS_DIR
import json
import base64
from connect_node import convet_num_to_nodestr


class UnknowProtocolException(Exception):
    pass


def show_info(choice):
    node_str = convet_num_to_nodestr(choice)
    info_list = convert(node_str)
    for info in info_list:
        print('Group    %s\nName     %s\nProtocol %s\nAddress  %s\nPort     %s\nLink     %s' % (
            info['Group'], info['Name'], info['Protocol'], info['Address'], info['Port'], info['Link']))


def convert(node_str):
    outbounds_path = CONNECTIONS_DIR+('{}.json'.format(node_str))
    f = open(outbounds_path, 'r', encoding='utf-8')
    jsonobj = json.load(f)
    conn_json = json.load(
        open(CONFIG_DIR+'connections.json', 'r', encoding='utf-8'))
    node_name = conn_json[node_str]['displayName']
    groups_name = get_group(node_str)
    vmesses = parse_outbounds(jsonobj)
    info_list = []
    for v in vmesses:
        v['ps'] = node_name
        link = "vmess://" + \
            base64.b64encode(json.dumps(
                v, sort_keys=True).encode('utf-8')).decode()
        protocol = 'vmess+'+v['net']
        info = {'Name': v['ps'], 'Group': groups_name, 'Protocol': protocol,
                'Address': v['add'], 'Port': v['port'], 'Link': link}
        info_list.append(info)
    return info_list


def get_group(node_str):
    groups_json = json.load(
        open(CONFIG_DIR+'groups.json', 'r', encoding='utf-8'))
    for item in groups_json.keys():
        if node_str in groups_json[item]['connections']:
            return groups_json[item]['displayName']


def parse_outbounds(jsonobj):
    vmesses = []
    if "outbounds" in jsonobj:
        for ib in jsonobj['outbounds']:
            if ib['protocol'] == 'vmess':
                try:
                    # outbounds2vmess(ib)
                    vmesses += outbounds2vmess(ib)
                except UnknowProtocolException:
                    pass
    return vmesses


def outbounds2vmess(outbound):
    _net = ""
    sset = {}
    _type = "none"
    _host = ""
    _path = ""
    _tls = ""
    _add = ""
    _port = ""
    _settings = outbound['settings']

    if "streamSettings" in outbound:
        sset = outbound["streamSettings"]

    if "network" in sset:
        _net = sset["network"]
    else:
        _net = "tcp"

    if _net == "tcp":
        if "tcpSettings" in sset and \
            "header" in sset["tcpSettings"] and \
                "type" in sset["tcpSettings"]["header"]:
            _type = sset["tcpSettings"]["header"]["type"]

        if "security" in sset:
            _tls = sset["security"]

    elif _net == "kcp":
        if "kcpSettings" in sset and \
            "header" in sset["kcpSettings"] and \
                "type" in sset["kcpSettings"]["header"]:
            _type = sset["kcpSettings"]["header"]["type"]

    elif _net == "ws":
        if "wsSettings" in sset and \
            "headers" in sset["wsSettings"] and \
                "Host" in sset["wsSettings"]["headers"]:
            _host = sset["wsSettings"]["headers"]["Host"]

        if "wsSettings" in sset and "path" in sset["wsSettings"]:
            _path = sset["wsSettings"]["path"]

        if "security" in sset:
            _tls = sset["security"]

    elif _net == "h2" or _net == "http":
        if "httpSettings" in sset and \
                "host" in sset["httpSettings"]:
            _host = ",".join(sset["httpSettings"]["host"])
        if "httpSettings" in sset and \
                "path" in sset["httpSettings"]:
            _path = sset["httpSettings"]["path"]
        _tls = "tls"

    elif _net == "quic":
        if "quicSettings" in sset:
            _host = sset["quicSettings"]["security"]
            _path = sset["quicSettings"]["key"]
            _type = sset["quicSettings"]["header"]["type"]

    else:
        raise UnknowProtocolException()

    vobj = []
    if 'vnext' in _settings:
        for c in _settings['vnext']:
            _add = c['address']
            _port = str(c['port'])
            if 'users' in c:
                _users = c['users']
                for u in _users:
                    _aid = u['alterId']
                    _id = u['id']
                    # {"v": "", "ps": "", "add": "", "port": "", "id": "", "aid": "",
                    #     "net": "", "type": "", "host": "", "path": "", "tls": ""}
                    vobj_tmp = dict(v='2', ps="", add=_add,
                                    port=_port, id=_id, aid=_aid, net=_net, type=_type, host=_host, path=_path, tls=_tls)
                    # print(json.dumps(vobj))
                    vobj.append(vobj_tmp)
    return vobj


if __name__ == '__main__':
    # get_group('zuwltsbpadjy')
    show_info(98)
