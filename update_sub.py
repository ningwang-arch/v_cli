import re
import base64
import urllib3


# 从subscribe.txt中读取链接
def update_from_txt():
    with open("subscribe.txt", 'r') as f:
        subscribe = f.readline()
        if subscribe == "":
            # 转移到强制输入订阅链接
            return
        if re.match(r'^https?:/{2}\w.+$', subscribe):
            http = urllib3.PoolManager()
            str_b64 = http.request('GET', subscribe).data.decode()

        else:
            str_b64 = subscribe
    blen = len(str_b64)
    if blen % 4 > 0:
        str_b64 += "=" * (4 - blen % 4)
    str_links = base64.b64decode(str_b64).decode()
    v_list = str_links.split('\r\n')[:-2]
    print(v_list)


if __name__ == '__main__':
    update_from_txt()
