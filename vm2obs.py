import json
import base64
import os
import string
import random


vmscheme = "vmess://"
CONNECTIONS_DIR = "connections/"

ret = {"outbounds": [
    {},
    {
        "protocol": "freedom",
        "tag": "direct",
        "settings": {
            "domainStrategy": "UseIP"
        }
    }
]}
TPL = {}
TPL["outbounds"] = [
    {
        "mux": {
            "enabled": True
        },
        "protocol": "vmess",
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
            "network": "ws",
        },
        "tag": "outBound_PROXY"
    }
]

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


def load_TPL(stype):
    s = TPL[stype]
    return json.loads(s)


def fill_tcp_http(_c, _v):
    tcps = load_TPL("http")
    tcps["header"]["type"] = _v["type"]
    if _v["host"] != "":
        # multiple host
        tcps["header"]["request"]["headers"]["Host"] = _v["host"].split(",")

    if _v["path"] != "":
        tcps["header"]["request"]["path"] = [_v["path"]]

    _c["outbounds"][0]["streamSettings"]["tcpSettings"] = tcps
    return _c


def fill_kcp(_c, _v):
    kcps = load_TPL("kcp")
    kcps["header"]["type"] = _v["type"]
    _c["streamSettings"]["kcpSettings"] = kcps
    return _c


def fill_ws(_c, _v):
    wss = load_TPL("ws")
    wss["path"] = _v["path"]
    wss["headers"]["Host"] = _v["host"]
    _c["streamSettings"]["wsSettings"] = wss
    return _c


def fill_h2(_c, _v):
    h2s = load_TPL("h2")
    h2s["path"] = _v["path"]
    h2s["host"] = [_v["host"]]
    _c["streamSettings"]["httpSettings"] = h2s
    return _c


def fill_quic(_c, _v):
    quics = load_TPL("quic")
    quics["header"]["type"] = _v["type"]
    quics["security"] = _v["host"]
    quics["key"] = _v["path"]
    _c[0]["streamSettings"]["quicSettings"] = quics
    return _c


def fill_basic(_c, _v):
    _vnext = _c["settings"]["vnext"][0]

    _vnext["address"] = _v["add"]
    _vnext["port"] = int(_v["port"])
    _vnext["users"][0]["id"] = _v["id"]
    _vnext["users"][0]["alterId"] = int(_v["aid"])

    _c["streamSettings"]["network"] = _v["net"]

    if _v["tls"] == "tls":
        _c["streamSettings"]["security"] = "tls"
        _c["streamSettings"]["tlsSettings"] = {"allowInsecure": True}
        if _v["host"] != "":
            _c["streamSettings"]["tlsSettings"]["serverName"] = _v["host"]

    return _c


def vmess2outbounds(_t, _v):
    _net = _v["net"]
    _type = _v["type"]

    _c = fill_basic(_t, _v)

    if _net == "kcp":
        return fill_kcp(_c, _v)
    elif _net == "ws":
        return fill_ws(_c, _v)
    elif _net == "h2":
        return fill_h2(_c, _v)
    elif _net == "quic":
        return fill_quic(_c, _v)
    elif _net == "tcp":
        if _type == "http":
            return fill_tcp_http(_c, _v)
        return _c
    else:
        raise Exception(
            "this link seem invalid to the script.")


def parsevmess(vmesslink):
    if vmesslink.startswith(vmscheme):
        bs = vmesslink[len(vmscheme):]
        blen = len(bs)
        if blen % 4 > 0:
            bs += "=" * (4 - blen % 4)

        vms = base64.b64decode(bs).decode()
        return json.loads(vms)
    else:
        raise Exception("vmess link invalid")


# 设置节点过滤规则,可自定义
def check_link(vmess):
    if vmess['net'] == "tcp":
        return False
    return True


def convert(vmess_link):
    vc = parsevmess(vmess_link)
    if not check_link(vc):
        return "", ""
    ret['outbounds'][0] = vmess2outbounds(TPL["outbounds"][0], vc)
    if not os.path.exists(CONNECTIONS_DIR):
        os.makedirs(CONNECTIONS_DIR)
    ran_str = ''.join(random.sample(string.ascii_lowercase, 12))
    node_name = vc["ps"]
    out_path = CONNECTIONS_DIR+("{}.json".format(ran_str))
    with open(out_path, 'w') as f:
        f.write(json.dumps(ret, indent=4))
    return ran_str, node_name
