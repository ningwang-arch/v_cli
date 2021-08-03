### Update

2021.07.23

    完善节点显示信息

### Update

2021.07.21

    增加节点删除和订阅删除功能

### Bug fix
2021.07.19

    修复更新节点后lastconnect.json连接节点不变导致显示当前连接时可能崩溃

### Update  
2021.07.18

    增加多订阅支持
### Update
2021.07.16

    增加了对win的适配(可能不完善)

### Update
2021.07.15

    修改了配置文件以及中间生成文件路径

### Update

2021.06.22
    完善了lastconnect.json中的连接信息



### Todo

    修改代码结构;
    添加tui,便于操作(可能耗时较长 概率鸽)



# 对所有字符串用引号包裹!!!!!



requirements: python3 python3-pip

### 模式
#### 1.无参数 ：
            默认启动上次链接

#### 		2. --help 参数： 打印帮助列表
            --update [url] / -u [url]               更新订阅,无参数则更新所有订阅
            --list_all                              列出所有节点
            --connect [choice] / -c [choice]        启动v2ray并链接至指定链接，若无choice参数，默认使用上次链接
            --current                               显示当前使用的节点名称
            --disconnect                            断开v2ray连接并关闭v2ray任务
            --http_port  [port]                     在指定端口代理http流量，若参数未添加，则默认代理8889端口
            --socks_port [port]                     在指定端口代理socks5流量，如参数未添加，则默认代理11223端口
            --path [path of v2ray] / -p [path]      v2ray可执行文件路径，无参数则默认调用系统路径
            --delete_node [choice]                  删除给定序号的节点
            --delete_sub  [sub_name]                删除给定订阅的有关信息和相关文件
            --show_info   [choice]                  显示给定序号节点的有关信息



### 预计产生文件
        1 groups.json               订阅保存文件
        2.config.json               v2ray启动的配置文件
        3.connections (dir)         各节点信息保存位置(每次更新后清空文件夹并重新填充信息)
        4.lastconnect.json          上次启动使用的参数
        5.connect.log               产生的连接日志
        6.connections.json          各节点名称与对应文件名





​									
