import json
import base64
import os
import string
import random
from settings import load_TPL, CONNECTIONS_DIR, check_link


vmscheme = "vmess://"

ret = {"outbounds": [
]}


def fill_tcp_http(_c, _v):
    tcps = load_TPL("http")
    tcps["header"]["type"] = _v["type"]
    if _v["host"] != "":
        # multiple host
        tcps["header"]["request"]["headers"]["Host"] = _v["host"].split(",")

    if _v["path"] != "":
        tcps["header"]["request"]["path"] = [_v["path"]]

    _c[0]["streamSettings"]["tcpSettings"] = tcps
    return _c


def fill_kcp(_c, _v):
    kcps = load_TPL("kcp")
    kcps["header"]["type"] = _v["type"]
    _c[0]["streamSettings"]["kcpSettings"] = kcps
    return _c


def fill_ws(_c, _v):
    wss = load_TPL("ws")
    wss["path"] = _v["path"]
    wss["headers"]["Host"] = _v["host"]
    _c[0]["streamSettings"]["wsSettings"] = wss
    return _c


def fill_h2(_c, _v):
    h2s = load_TPL("h2")
    h2s["path"] = _v["path"]
    h2s["host"] = [_v["host"]]
    _c[0]["streamSettings"]["httpSettings"] = h2s
    return _c


def fill_quic(_c, _v):
    quics = load_TPL("quic")
    quics["header"]["type"] = _v["type"]
    quics["security"] = _v["host"]
    quics["key"] = _v["path"]
    _c[0]["streamSettings"]["quicSettings"] = quics
    return _c


def fill_basic(_c, _v):
    _outbound = _c[0]
    _vnext = _outbound["settings"]["vnext"][0]

    _vnext["address"] = _v["add"]
    _vnext["port"] = int(_v["port"])
    _vnext["users"][0]["id"] = _v["id"]
    _vnext["users"][0]["alterId"] = int(_v["aid"])

    _outbound["streamSettings"]["network"] = _v["net"]

    if _v["tls"] == "tls":
        _outbound["streamSettings"]["security"] = "tls"
        _outbound["streamSettings"]["tlsSettings"] = {"allowInsecure": True}
        if _v["host"] != "":
            _outbound["streamSettings"]["tlsSettings"]["serverName"] = _v["host"]

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


def convert(vmess_link: str):
    vc = parsevmess(vmess_link)
    if not check_link(vc):
        return "", ""
    ret['outbounds'] = vmess2outbounds(load_TPL("outbounds"), vc)
    if not os.path.exists(CONNECTIONS_DIR):
        os.makedirs(CONNECTIONS_DIR)
    ran_str = ''.join(random.sample(string.ascii_lowercase, 12))
    node_name = vc["ps"]
    out_path = CONNECTIONS_DIR+("{}.json".format(ran_str))
    with open(out_path, 'w') as f:
        f.write(json.dumps(ret, indent=4))
    return ran_str, node_name
