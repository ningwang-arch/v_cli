import os
import json
from prompt_toolkit.completion import NestedCompleter
from settings import CONFIG_DIR, nested_dict_base


def get_sub_node_set():
    if not os.path.exists(CONFIG_DIR+'groups.json') or not os.path.exists(CONFIG_DIR+'connections.json'):
        return None
    with open(CONFIG_DIR+'groups.json') as f:
        groups_info = json.load(f)
    with open(CONFIG_DIR+'connections.json', encoding='utf-8') as f:
        conn = json.load(f)
    res = {}
    for item in groups_info:
        sub_name = groups_info[item]['displayName'].replace(' ', '%20')
        connections = [conn[i]['displayName'].replace(' ', '%20')
                       for i in groups_info[item]['connections']]

        res[sub_name] = set(connections)
    return res


def generate_completer():
    res = get_sub_node_set()
    nested_dict_base['update'] = set(res.keys())
    nested_dict_base['connect'] = res
    nested_dict_base['info'] = res
    nested_dict_base['delete'] = res

    completer = NestedCompleter.from_nested_dict(nested_dict_base)

    return completer
