# 对所有字符串用引号包裹!!!!!

For Linux Only
### 模式

##### 		1.无参数 ：

​					默认启动上次链接

##### 		2. --help 参数： 打印帮助列表

​					--update url / -u url  更新订阅

​					--list_all       列出所有节点

​					--connect choice / -c choice	启动v2ray并链接至指定链接，若无choice参数，默认使用上次链接

​					--list_current  显示当前使用的节点信息

​					--disconnect    断开v2ray链接并关闭v2ray任务

​					--http_port  port  在指定端口代理http流量，若参数未添加，则默认代理8889端口

​					--socks_port port  在指定端口代理socks5流量，如参数未添加，则默认代理1089端口

​					--path [path of v2ray]  v2ray可执行文件路径，无参数则默认调用系统路径

##### 		3.--update  url  / -u url

​				更新订阅,若url参数不存在，则先从当前路径下的subscribe.txt读取链接,若subscribe.txt不存在，则提醒用户输入订阅链接，并将链接保存至subscribe.txt;若存在url参数，则从提供的url中读取订阅，并将url保存至subscribe.txt;  同时解析链接并获取节点信息保存至对应的config文件

##### 		4.--list_all

​				从已有文件中读取节点名称排序并打印

##### 		5.--connect choice / -c choice

​				由序号将对应节点的有关信息加载至config.json,并重启v2ray。

##### 		6.--list_current

​				打印当前节点的有关信息(如端口，address，host，alterId等)。

##### 		7.--disconnect

​				关闭v2ray进程

##### 		8.--http_port port

​				在制定端口代理http流量，默认8889端口

##### 		9.--socks_port port

​				在制定端口代理socks流量，默认1089端口

### 预计产生文件

##### 		1.subscribe.txt

​				保存订阅链接

##### 		2.config.json

​				v2ray启动的配置文件

##### 		3.connections (dir)

​				各节点信息保存位置(每次更新后清空文件夹并重新填充信息)

##### 		4.lastconnect.json

​				上次启动使用的参数

##### 5.connect.log

​				产生的连接信息

##### 6. connections.json

​				各节点名称与对应文件名





​									
