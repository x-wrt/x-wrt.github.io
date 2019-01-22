# 搭建PPPoe服务器

## 1. 介绍

## 2. 搭建PPPoe服务器
### 2.1 下载源码
```
$ wget https://dianne.skoll.ca/projects/rp-pppoe/download/rp-pppoe-3.13.tar.gz
```

### 2.2 编译&安装
```
> tar -zxf rp-pppoe-3.13.tar.gz
> cd rp-pppoe-3.13/src
> ./configure
> make
> sudo make install
```

### 2.3 配置
+ 打开`/etc/ppp/chap-secrets`添加用户名/密码<br>
```
# Secrets for authentication using CHAP
# client	server	secret			IP addresses
"test"      *       "123456"        *
```

+ 打开`/etc/ppp/pppoe-server-options`<br>
```
logfile /var/log/pppd.log

auth
lcp-echo-failure 3
lcp-echo-interval 60
mtu 1482
mru 1482
require-chap
ms-dns 8.8.8.8
ms-dns 8.8.4.4
netmask 255.255.255.0
defaultroute
noipdefault
usepeerdns
```


### 2.4 启动
```
$ sudo pppoe-server -I enp3s0 -l -L 172.16.0.1 -R 172.16.0.10 -N 10
```

配置radvd:
```
interface ppp0 {         
	AdvSendAdvert on;
	MinRtrAdvInterval 3;
	MaxRtrAdvInterval 10;
	AdvDefaultPreference high;
	AdvHomeAgentFlag off;
	IgnoreIfMissing on;   #这个很关键
	AdvManagedFlag off;   #这个很关键
	AdvOtherConfigFlag off; #这个很关键        
	prefix 2001:1111:2222:1::/64 {
		AdvOnLink on;
		AdvAutonomous on; #让PPP接口根据PREFIX生成地址
		AdvRouterAddr on;
	};
	RDNSS 2001::1 2001::2 {
		AdvRDNSSPreference 8;
		AdvRDNSSLifetime 30;
	};
};
```