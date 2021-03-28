import json

CONNECTIONS_DIR = "connections/"
LAST_CONNECT = "lastconnect.json"

TPL = {}
TPL["outbounds"] = """
[
    {
        "mux": {
            "enabled": true
        },
        "protocol": "vmess",
        "sendThrough": "0.0.0.0",
        "settings": {
            "vnext": [
                {
                    "address": "host.host",
                    "port": 1234,
                    "users": [
                        {
                            "alterId": 1,
                            "id": "",
                            "level": 0,
                            "security": "auto",
                            "testsEnabled": "none"
                        }
                    ]
                }
            ]
        },
        "streamSettings": {
            "network": "ws"
        },
        "tag": "outBound_PROXY"
    },
    {
        "protocol": "freedom",
        "tag": "direct",
        "settings": {
            "domainStrategy": "UseIP"
        }
    }
]
"""

# tcpSettings
TPL["http"] = """
{
    "header": {
        "type": "http",
        "request": {
            "version": "1.1",
            "method": "GET",
            "path": [
                "/"
            ],
            "headers": {
                "Host": [
                    "www.cloudflare.com",
                    "www.amazon.com"
                ],
                "User-Agent": [
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"
                ],
                "Accept": [
                    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
                ],
                "Accept-language": [
                    "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4"
                ],
                "Accept-Encoding": [
                    "gzip, deflate, br"
                ],
                "Cache-Control": [
                    "no-cache"
                ],
                "Pragma": "no-cache"
            }
        }
    }
}
"""

# kcpSettings
TPL["kcp"] = """
{
    "mtu": 1350,
    "tti": 50,
    "uplinkCapacity": 12,
    "downlinkCapacity": 100,
    "congestion": false,
    "readBufferSize": 2,
    "writeBufferSize": 2,
    "header": {
        "type": "wechat-video"
    }
}
"""

# wsSettings
TPL["ws"] = """
{
    "connectionReuse": true,
    "path": "/path",
    "headers": {
        "Host": "host.host.host"
    }
}
"""


# httpSettings
TPL["h2"] = """
{
    "host": [
        "host.com"
    ],
    "path": "/host"
}
"""

TPL["quic"] = """
{
    "security": "none",
    "key": "",
    "header": {
        "type": "none"
    }
}
"""


TPL['config'] = """
{
    "dns": {
        "servers": [
            "1.1.1.1",
            "8.8.8.8",
            "8.8.4.4"
        ]
    },
    "inbounds": [],
    "outbounds": [],
    "log": {
        "loglevel": "warning"
    },
    "routing": {
        "domainStrategy": "AsIs",
        "rules": [{
                "ip": [
                    "geoip:private"
                ],
                "outboundTag": "outBound_DIRECT",
                "type": "field"
            },
            {
                "ip": [
                    "geoip:cn"
                ],
                "outboundTag": "outBound_DIRECT",
                "type": "field"
            },
            {
                "domain": [
                    "geosite:cn"
                ],
                "outboundTag": "outBound_DIRECT",
                "type": "field"
            }
        ]
    }
}
"""

TPL['http_in'] = """
{
    "listen": "127.0.0.1",
    "port": 0,
    "protocol": "http",
    "settings": {},
    "sniffing": {
        "enabled": false
    },
    "tag": "http_IN"
}
"""

TPL['socks_in'] = """
{
    "listen": "127.0.0.1",
    "port": 1089,
    "protocol": "socks",
    "settings": {
        "auth": "noauth",
        "ip": "127.0.0.1",
        "udp": true,
        "userLevel": 0
    },
    "sniffing": {
        "enabled": false
    },
    "tag": "socks_IN"
}

"""


def load_TPL(stype):
    s = TPL[stype]
    return json.loads(s)


# 设置节点过滤规则,可自定义
def check_link(vmess: json):
    if vmess['net'] == "tcp":
        return False
    return True
