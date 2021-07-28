#!/usr/bin/python3
# -*- encoding: utf-8 -*-
from parser_create import create_parser
import connect_node
import sys
import json
import os
import update_sub
from settings import CONNECTIONS_DIR,CONFIG_DIR
import del_func
import json2vmess


def get_default_config():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    last_dict={}
    if os.path.exists(CONFIG_DIR+'lastconnect.json'):
        with open(CONFIG_DIR+'lastconnect.json', 'r',encoding=“utf-8”) as f:
            last_dict = json.load(f)
    else:
        last_dict = {'path': '/usr/bin/v2ray',
                     'http_port': 8889, 'socks_port': 11223}
    return last_dict


if __name__ == '__main__':
    default_config = get_default_config()
    parser = create_parser()
    option = parser.parse_args()
    argv_list = sys.argv
    if len(argv_list) <= 1:
        connect_node.connect_default()
    elif option.disconnect:
        connect_node.disconnect()
    elif option.list_all:
        connect_node.print_node()
    elif option.current:
        connect_node.current()
    elif option.delete_node:
        del_func.delete_node(int(option.delete_node))
    elif option.delete_sub:
        del_func.delete_sub(option.delete_sub)
    elif option.show_info:
        json2vmess.show_info(int(option.show_info))
    elif (('--update' in argv_list) or ('-u' in argv_list)):
        if option.update is not None:
            print('Please input subscription name: ', end='')
            sub_name = input()
            update_sub.update_from_url(option.update, sub_name)
        elif option.update is None:
            update_sub.update_from_sub()
    elif (('--connect' in argv_list) or ('-c' in argv_list)):
        if option.connect is not None:
            http_port = int(
                option.http_port) if option.http_port is not None else default_config['http_port']
            socks_port = int(
                option.socks_port) if option.socks_port is not None else default_config['socks_port']
            path = option.path if option.path is not None else default_config['path']
            connect_node.connect(int(option.connect),
                                 path, http_port, socks_port)
        elif option.connect is None:
            connect_node.connect_default()
