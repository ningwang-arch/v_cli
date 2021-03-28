import json
from settings import load_TPL, CONNECTIONS_DIR


def fill_inbounds(http_port, socks_port):
    http_in = load_TPL("http_in")
    socks_in = load_TPL("socks_in")
    http_in['port'] = http_port
    socks_in['port'] = socks_port
    config = load_TPL('config')
    config['inbounds'].append(http_in)
    config['inbounds'].append(socks_in)
    return config


def fill_outbounds(config, node_name):
    path = CONNECTIONS_DIR+("{}.json".format(node_name))
    with open(path, 'r') as f:
        conn = json.load(f)
    config['outbounds'] = conn['outbounds']
    return config


def config(node_name, http_port=8889, socks_port=1089):
    config = fill_outbounds(fill_inbounds(http_port, socks_port), node_name)
    with open('config.json', 'w') as f:
        f.write(json.dumps(config, indent=4, ensure_ascii=False))
