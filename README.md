### Todo
    修改README;
    修改代码结构;
    添加tui,便于操作(可能耗时较长 概率鸽)



---



##### requirements: python3 python3-pip




---



It is recommended to build or run in a virtual environment.

#### Run

```
1. pip3 install pipenv
2. pipenv install
3. pipenv shell
4. python3 v_cli.py
```

 

#### Build

```
1. pip3 install pipenv
2. pipenv install
3. pipenv shell
4. pipenv run pip3 install pyinstaller
5. pipenv run pyinstaller -Fw v_cli.py
```

The target file is located in the dist folder



#### Usage

​	If you need node filtering

```
1. mkdir ~/.config/v_cli  (if v_cli folder does not exist)
2. cp rules.yaml.example ~/.config/v_cli/rules.yaml
```

​	Modify rules.yaml according to the comments (group name needs to be the same as the corresponding subscription name)

1. run `port set` to set v2ray executable file path
2. run `update sub_url` to add a subscription
3.  run `connect group_name node_name ` to start v2ray
4.  run `disconnect` to stop v2ray





### 预计产生文件

        1. groups.json               订阅保存文件
        2. config.json               v2ray启动的配置文件
        3. connections (dir)         各节点信息保存位置(每次更新后清空文件夹并重新填充信息)
        4. lastconnect.json          上次启动使用的参数
        5. connect.log               产生的连接日志
        6. connections.json          各节点名称与对应文件名
        7. .history                  保存历史记录




​									
