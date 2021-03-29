from parser_create import create_parser
import connect_node
import sys
import update_sub

if __name__ == '__main__':
    parser = create_parser()
    option = parser.parse_args()
    argv_list = sys.argv
    if len(argv_list) <= 1:
        connect_node.connect_default()
    elif option.disconnect:
        connect_node.disconnect()
    elif option.list_all:
        connect_node.print_node()
    elif option.list_current:
        connect_node.current()
    elif (('--update' in argv_list) or ('-u' in argv_list)):
        if option.update is not None:
            update_sub.update_from_url(option.update)
        elif option.update is None:
            update_sub.update_from_txt()
    elif (('--connect' in argv_list) or ('-c' in argv_list)):
        if option.connect is not None:
            http_port = int(
                option.http_port) if option.http_port is not None else 8889
            socks_port = int(
                option.socks_port) if option.socks_port is not None else 1089
            path = option.path if option.path is not None else "v2ray"
            connect_node.connect(int(option.connect),
                                 path, http_port, socks_port)
        elif option.connect is None:
            connect_node.connect_default()
