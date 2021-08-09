import json
import os
import sys
import yaml


PLATFORM = sys.platform


def get_home_path() -> str:
    env_dict = os.environ
    if PLATFORM == "win32":
        return env_dict['HOMEDRIVE']+(env_dict['HOMEPATH'].replace('\\', '/'))
    else:
        return env_dict['HOME']


CONFIG_DIR = get_home_path()+'/.config/v_cli/'
CONNECTIONS_DIR = CONFIG_DIR+"connections/"
LAST_CONNECT = CONFIG_DIR+"lastconnect.json"
RULES_YAML = CONFIG_DIR+'rules.yaml'
HISTORY_PATH = CONFIG_DIR+'.history'

TPL = {}
TPL["outbounds"] = """
[
    {
        "mux": {
            "enabled": true
        },
        "protocol": "",
        "sendThrough": "0.0.0.0",
        "settings": {
            "vnext": [
                {
                    "address": "host.host",
                    "port": 1234,
                    "users": [
                        {
                            "alterId": 1,
                            "id": "",
                            "level": 0,
                            "security": "auto",
                            "testsEnabled": "none"
                        }
                    ]
                }
            ]
        },
        "streamSettings": {
            "network": "ws"
        },
        "tag": "outBound_PROXY"
    },
    {
        "protocol": "freedom",
        "tag": "direct",
        "settings": {
            "domainStrategy": "UseIP"
        }
    }
]
"""

# tcpSettings
TPL["http"] = """
{
    "header": {
        "type": "http",
        "request": {
            "version": "1.1",
            "method": "GET",
            "path": [
                "/"
            ],
            "headers": {
                "Host": [
                    "www.cloudflare.com",
                    "www.amazon.com"
                ],
                "User-Agent": [
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"
                ],
                "Accept": [
                    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
                ],
                "Accept-language": [
                    "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4"
                ],
                "Accept-Encoding": [
                    "gzip, deflate, br"
                ],
                "Cache-Control": [
                    "no-cache"
                ],
                "Pragma": "no-cache"
            }
        }
    }
}
"""

# kcpSettings
TPL["kcp"] = """
{
    "mtu": 1350,
    "tti": 50,
    "uplinkCapacity": 12,
    "downlinkCapacity": 100,
    "congestion": false,
    "readBufferSize": 2,
    "writeBufferSize": 2,
    "header": {
        "type": "wechat-video"
    }
}
"""

# wsSettings
TPL["ws"] = """
{
    "connectionReuse": true,
    "path": "/path",
    "headers": {
        "Host": "host.host.host"
    }
}
"""


# httpSettings
TPL["h2"] = """
{
    "host": [
        "host.com"
    ],
    "path": "/host"
}
"""

TPL["quic"] = """
{
    "security": "none",
    "key": "",
    "header": {
        "type": "none"
    }
}
"""


TPL['config'] = """
{
    "dns": {
        "servers": [
            "1.1.1.1",
            "8.8.8.8",
            "8.8.4.4"
        ]
    },
    "inbounds": [],
    "outbounds": [],
    "log": {
        "loglevel": "warning"
    },
    "routing": {
        "domainStrategy": "AsIs",
        "rules": [{
                "ip": [
                    "geoip:private"
                ],
                "outboundTag": "outBound_DIRECT",
                "type": "field"
            },
            {
                "ip": [
                    "geoip:cn"
                ],
                "outboundTag": "outBound_DIRECT",
                "type": "field"
            },
            {
                "domain": [
                    "geosite:cn"
                ],
                "outboundTag": "outBound_DIRECT",
                "type": "field"
            }
        ]
    }
}
"""

TPL['http_in'] = """
{
    "listen": "127.0.0.1",
    "port": 0,
    "protocol": "http",
    "settings": {},
    "sniffing": {
        "enabled": false
    },
    "tag": "http_IN"
}
"""

TPL['socks_in'] = """
{
    "listen": "127.0.0.1",
    "port": 1089,
    "protocol": "socks",
    "settings": {
        "auth": "noauth",
        "ip": "127.0.0.1",
        "udp": true,
        "userLevel": 0
    },
    "sniffing": {
        "enabled": false
    },
    "tag": "socks_IN"
}

"""

nested_dict_base = {
    'all': None,
    'connect': {},
    'current': None,
    'delete': {},
    'disconnect': None,
    'exit': None,
    'info': {},
    'path': {
        'set': None,
        'show': None
    },
    'port': {
        'set': None,
        'show': None
    },
    'update': {},
}


def load_TPL(stype):
    s = TPL[stype]
    return json.loads(s)


def default_config():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    if os.path.exists(LAST_CONNECT):
        return
    with open(LAST_CONNECT, 'w', encoding='utf-8') as f:
        f.write(json.dumps({'node': '', 'http_port': '8889', 'socks_port': '11223',
                'path': '/usr/bin/v2ray'}, ensure_ascii=False, indent=4))


def get_node_str(node_name):
    with open(CONFIG_DIR+'connections.json', 'r', encoding='utf-8') as f:
        conn = json.load(f)
    for item in conn:
        if conn[item]['displayName'] == node_name.replace('%20', ' '):
            return item


def load_default_config():
    if not os.path.exists(LAST_CONNECT):
        return
    with open(LAST_CONNECT, 'r', encoding='utf-8') as f:
        return json.load(f)


def clean_blocks(blocks: list):
    for item in blocks.copy():
        if item == '':
            blocks.remove(item)
    return blocks


def trim(s):
    import re
    if s.startswith(' ') or s.endswith(' '):
        return re.sub(r"^(\s+)|(\s+)$", "", s)
    return s


def dict_copy(dict_input: dict, dict_output: dict):
    for i in dict_input:
        dict_output[i] = dict_input[i]


def load_rules():
    if not os.path.exists(RULES_YAML):
        return
    else:
        with open(RULES_YAML, 'r', encoding='utf-8') as f:
            from update_sub import group_current
            rules = yaml.unsafe_load(f)
            rules = rules[group_current] if group_current in rules else None
            return rules


def check_include(rules_include: dict, vmess: json):
    if not rules_include:
        return True
    relation = rules_include['relation']
    name = rules_include['name'] if 'name' in rules_include else []
    protocol = rules_include['protocol'] if 'protocol' in rules_include else []
    name_flag = True
    protocol_flag = True

    if protocol != vmess['net']:
        protocol_flag = False

    # or
    if relation == 'or':
        name_flag = any([i in vmess['ps'] for i in name])

    # and
    else:
        name_flag = all([i in vmess['ps'] for i in name])
    return (name_flag or protocol_flag)


def check_exclude(rules_exclude, vmess):
    if not rules_exclude:
        return True
    relation = rules_exclude['relation']
    name = rules_exclude['name'] if 'name' in rules_exclude else []
    protocol = rules_exclude['protocol'] if 'protocol' in rules_exclude else []
    name_flag = True
    protocol_flag = True

    if protocol == vmess['net']:
        protocol_flag = False

    if relation == 'or':
        name_flag = not any([i in vmess['ps'] for i in name])
    else:
        name_flag = not all([i in vmess['ps'] for i in name])

    return (name_flag and protocol_flag)


def check_link(vmess: json):
    rules = load_rules()
    if rules is None:
        return True
    if rules['mode'] == 'include':
        return check_include(rules, vmess)
    else:
        return check_exclude(rules, vmess)
