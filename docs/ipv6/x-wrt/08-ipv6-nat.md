# X-wrt IPv6: NAT模式

## 1. 介绍
IPv6本身不支持NAT, 但是可以用ip6tables规则实现

## 2. 网络拓扑
![](../img/ipv6-NAT.png)

## 3. 配置
### 3.1 R1与R2的配置
```
config dhcp 'lan'
    option interface 'lan'
    option dhcpv6 server
    option ra server
    option ra_default '1'
```
### 3.3 规则
在[R1](#)执行一下规则
```sh
$ ip6tables -t nat -A POSTROUTING -o eth0.2 -j MASQUERADE
$ ip6tables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
$ ip6tables -A FORWARD -i br-lan -j ACCEPT
```

## 4. 测试
可以在[R2](#)的LAN接口抓包,可以看到来自PC的数据流的源地址变成了R1的WAN地址