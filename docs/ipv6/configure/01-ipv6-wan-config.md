# X-wrt: IPv6 WAN配置

## 1.介绍
IPv6 wan接口的地址配置可以通过手动配置, dhcp获取, pppoe拨号方式获得.
## 2. 静态配置(static)
### 2.1 修改`/etc/config/network`配置文件
```
config interface 'wan'
    option ifname    'eth0.2'
    option proto     'static'
    option ip6addr   2001:1234:5678:1::2/64 #给自己配置的地址
    option ip6gw     2001:1234:5678:1::1    #默认网关
    option ip6prefix 2001:db80:1::/48       #前缀, 可以用于给下游接口分配
    option dns       2001:db80::1           #dns服务器
```

### 2.2 重启网络
`$ /etc/init.d/network restart`

## 3. DHCP
### 3.1 修改`/etc/config/network`配置文件
```
config interface 'wan6'
        option ifname 'eth0.2'
        option proto 'dhcpv6'
```
### 3.2 重启网络
`$ /etc/init.d/network restart`

## 4. PPPoe拨号
### 4.1 修改`/etc/config/network`配置文件
```
config interface 'wan'
        option ifname   'eth0.2'
        option proto    'pppoe'
        option username 'test'   #拨号帐号
        option password '123456' #拨号密码

config interface 'wan6'
        option ifname '@wan'
        option ipv6   '1'
```
### 4.2 重启网络
`$ /etc/init.d/network restart`
