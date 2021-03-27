import json
import os


# 从connections.json中加载节点名称并赋予序号
def print_node():
    path = 'connections.json'
    if not os.path.exists(path):
        print('No node, please update the subscription and try again')
        return
    with open(path, 'r') as f:
        connections = json.load(f)
    values = list(connections.values())
    for i in range(len(values)):
        print(str(i+1)+"."+values[i])


if __name__ == '__main__':
    print_node()
