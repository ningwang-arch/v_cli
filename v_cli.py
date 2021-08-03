#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import sys
from settings import default_config, trim
import connect_node
import json2vmess
import del_func
import port_path
import update_sub
from prompt_toolkit import prompt
from completer_generator import generate_completer
from prompt_toolkit.styles import Style

if __name__ == '__main__':
    # completer = generate_completer()
    # print(completer)
    default_config()
    style = Style.from_dict({
        # User input (default text).
        '':          '#ffffff',
        # Prompt.
        'pound':    '#caa9fa',
    })
    message = [
        ('class:pound',    '>>> '),
    ]
    while True:
        user_input = prompt(message, style=style,
                            completer=generate_completer())
        # print(user_input)
        blocks = trim(user_input).split(' ')

        if blocks[0] == 'all':
            connect_node.print_node()
        elif blocks[0] == 'info':
            json2vmess.show_info(blocks[1:])
        elif blocks[0] == 'disconnect':
            connect_node.disconnect()
        elif blocks[0] == 'connect':
            connect_node.connect(blocks[1:])
        elif blocks[0] == 'delete':
            del_func.delete_func(blocks[1:])
        elif blocks[0] == 'port':
            port_path.port_about(blocks[1:])
        elif blocks[0] == 'path':
            port_path.path_about(blocks[1:])
        elif blocks[0] == 'current':
            connect_node.current()
        elif blocks[0] == 'update':
            update_sub.update(blocks[1:])
        elif blocks[0] == 'exit':
            print('Bye!')
            sys.exit(0)
