# X-wrt IPv6: dhcp中继模式

## 1. 介绍
X-wrt可以通过中继的模式获取到原始的IPv6的IP

## 2. 网络拓扑
![](./img/ipv6-dhcp-relay.png)

## 3. 步骤

### 3.1 R1路由器配置
#### 3.1.1 修改dhcp配置
`$ /etc/config/dhcp`

[lan](#)配置如下添加:
+ `option ra 'relay'`
+ `option ndp 'relay'`

如
```
config dhcp 'lan'
	option interface 'lan'
	option start '100'
	option limit '150'
	option leasetime '12h'
	option dhcpv6 'server'
	option ra 'relay'
	option ndp 'relay'
```

[wan](#)配置如下添加:
+ `option ra 'relay'`
+ `option ndp 'relay'`
+ `option master '1'`

如
```
config dhcp 'wan'
	option interface 'wan'
	option ignore '1'
	option ra 'relay'
	option ndp 'relay'
	option master '1'	
```
#### 3.1.2 重启网络
`$ /etc/init.d/network restart`

### 3.2 R2路由器配置
[参考 DHCP服务(服务器模式)](./01-ipv6-lan-dhcp-server-mod.md)


### 3.3 PC
PC重新获取一下IP, 查看接口信息: IPv6地址是有[R2路由器](#)分配的
`$ ifconfig`

![](./img/PC-ipv6-dhcp-relay.jpg)