import re
import base64
import urllib3
import os
from vm2obs import convert


sub_path = 'subscribe.txt'


def force_input():
    subscribe = ''
    while subscribe == '':
        subscribe = input()
    return subscribe


# 从subscribe.txt中读取链接
def update_from_txt():
    if not os.path.exists(sub_path):
        url = force_input()
        update_from_url(url)
        return
    with open(sub_path, 'r') as f:
        subscribe = f.readline()
        if subscribe == "":
            url = force_input()
            update_from_url(url)
            return
        if re.match(r'^https?:/{2}\w.+$', subscribe):
            http = urllib3.PoolManager()
            response = http.request('GET', subscribe)
            if response.status == 200:
                str_b64 = response.data.decode()
            else:
                print('Invalid subscription link')
                return
        else:
            str_b64 = subscribe
    blen = len(str_b64)
    if blen % 4 > 0:
        str_b64 += "=" * (4 - blen % 4)
    str_links = base64.b64decode(str_b64).decode()
    v_list = str_links.split('\r\n')
    for item in v_list:
        if item == "":
            continue
        else:
            convert(item)


def update_from_url(url):
    with open(sub_path, 'r') as f:
        f.write(url)
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    if response.status == 200:
        str_b64 = response.data.decode()
    else:
        print('Invalid subscription link')
        return
    blen = len(str_b64)
    if blen % 4 > 0:
        str_b64 += "=" * (4 - blen % 4)
    str_links = base64.b64decode(str_b64).decode()
    v_list = str_links.split('\r\n')
    for item in v_list:
        if item == "":
            continue
        else:
            convert(item)


if __name__ == '__main__':
    print(force_input())
