import json
from settings import LAST_CONNECT, clean_blocks, load_default_config


# port
def port_about(blocks: list):
    conf = load_default_config()
    blocks = clean_blocks(blocks)
    if (not len(blocks)) or len(blocks) > 3 or len(blocks) < 1:
        print(
            'Error Format,shoould be `port show port` or `port set port [port]`')
        return
    if blocks[0] == 'show':
        print('Http port  : %s\nSocks port : %s' %
              (conf['http_port'], conf['socks_port']))
    elif blocks[0] == 'set':
        http_port = int(input('Please input http port : '))
        socks_port = int(input('Please input socks port : '))
        conf['http_port'] = http_port
        conf['socks_port'] = socks_port
        with open(LAST_CONNECT, 'w', encoding='utf-8') as f:
            f.write(json.dumps(conf, ensure_ascii=False, indent=4))


# path
def path_about(blocks: list):
    conf = load_default_config()
    blocks = clean_blocks(blocks)
    if (not len(blocks)) or len(blocks) > 2 or len(blocks) < 1:
        print(
            'Error Format,shoould be `path show` or `path set [path]`')
        return
    if blocks[0] == 'show':
        print('Path : %s' % conf['path'])
    elif blocks[0] == 'set':
        path = input('Please input v2ray path : ')
        conf['path'] = path
        with open(LAST_CONNECT, 'w', encoding='utf-8') as f:
            f.write(json.dumps(conf, ensure_ascii=False, indent=4))
