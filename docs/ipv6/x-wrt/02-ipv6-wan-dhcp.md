# X-wrt IPv6: wan获取IPv6地址

## 1. 介绍
WAN接口配置dhcpv6的服务, 从上游获取IPv6地址

## 2. 步骤

### 2.1 newtork配置
```
$  vim  /etc/config/network
```

添加[interface](#)配置项如:`wan6`, 使用`dhcpv6`协议

```
config interface 'wan6'
        option ifname 'eth0.2'
        option proto 'dhcpv6'
```

###2.2 重启网络
```
$ /etc/init.d/network restart
```

### 2.3 查看网口IP
```
$ ifconfig
```
![](./img/wan-ipv6-ip.png)


