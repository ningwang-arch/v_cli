import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        description="A python-based v2ray command line client")

    parser.add_argument('--disconnect',
                        action="store_true",
                        help="Disconnect v2ray link and close v2ray task")

    parser.add_argument('-u', '--update',
                        nargs='?',
                        action="store",
                        help="Update subscription")

    parser.add_argument('-c', '--connect',
                        nargs='?',
                        action="store",
                        help="Start v2ray and link to the specified link. If there is no choice parameter, the last link will be used by default")

    parser.add_argument('--http_port',
                        action='store',
                        help="Proxy http traffic on the specified port, if the parameter is not added, the default proxy port 8889")

    parser.add_argument('--socks_port',
                        action='store',
                        help="Proxy socks traffic on the specified port, if the parameter is not added, the default proxy port 11223")

    parser.add_argument('--list_all',
                        action="store_true",
                        help="List all nodes")

    parser.add_argument('--current',
                        action="store_true",
                        help="Display the node currently in use")
    parser.add_argument('--path', '-p',
                        action="store",
                        help="v2ray executable file path, the system path is called by default")

    parser.add_argument('--delete_node',
                        action='store',
                        help='Delete node')

    parser.add_argument('--delete_sub',
                        action='store',
                        help='Delete a subscription')

    return parser


create_parser()
