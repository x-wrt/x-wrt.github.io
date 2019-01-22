# X-wrt: IPv6 LAN服务配置

## 1.介绍
LAN接口可以采用SLAAC, DHCPv6(无状态), DHCPv6(无状态)三种方式给客户端分配地址, 以及指定dns服务器

## 2 配置项
```
> cat /etc/config/dhcp

ra_management:
   M标记: 通知客户端 DHCPv6服务可用
   A标记: 告诉客户端使用自动配置(如SLAAC)
    取值:
      0: M标记 = 0 且 A标记 = 1
      1: M标记 = 1 且 A标记 = 1
      2: M标记 = 1 且 A标记 = 0
```

```
> cat /etc/config/dhcp

ra_default:
    IPv6默认路由配置
    取值:
      0: default 
      1: ignore no public address 
      2: ignore all
```
## 3. SLAAC(无状态地址自动配置)
配置文件`/etc/config/dhcp`<br>
```
config dhcp lan
    option dhcpv6        disabled  # dhcpv6服务
    option ra            server    # RA服务(发送路由通告)
    option ra_management 0         # M=0 & A=1
```
## 4. DHCPv6(无状态)
配置文件`/etc/config/dhcp`<br>
```
config dhcp lan
    option dhcpv6 server
    option ra     server
    option ra_management 1   # M=1 & A=1
```
## 5. DHCPv6(有状态)
配置文件`/etc/config/dhcp`<br>
```
config dhcp lan
    option dhcpv6 server     # 开启dhcpv6服务
    option ra     server     # 关闭RA服务器
    option ra_management 2   # M=1 & A=0
```
## 6. IPv6中继模式(不会影响IPv4地址获取)
配置文件`/etc/config/dhcp`<br>
```
config dhcp wan
    option dhcpv6 relay
    option ra relay
    option ndp relay
    option master 1

config dhcp lan
    option dhcpv6 relay
    option ra relay
    option ndp relay
```

## 7. 指定DNS服务器
配置文件`/etc/config/dhcp`<br>
```
config dhcp lan
    ...
    list dns 2001::1
    list dns 2001::2
    ...
```

