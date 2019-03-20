# 编译X-wrt支持IPv6

## 1. 需要模块支持

|模块|作用|
|---|---|
|[odhcpd](#)|支持DHCPv6和ICMPv6协议, 可以作为server,或者relay-agent|
|[odhcp6c](#)|dhcpv6的客户端|
|[dnsmasq](#)|可以做为IPv4和IPv6的dns服务器代理|

具体依赖包:
```
web管理界面:
PACKAGE_luci-theme-bootstrap
PACKAGE_luci-base
PACKAGE_luci-mod-admin-full
PACKAGE_luci-proto-ipv6
LUCI_LANG_zh-cn
PACKAGE_uhttpd
```
```
IPv6:
PACKAGE_kmod-ipt-nat6
PACKAGE_kmod-ip6tables-extra
PACKAGE_iputils-traceroute6
PACKAGE_ndppd
PACKAGE_odhcp6c=y
PACKAGE_odhcpd=y
PACKAGE_dnsmasq-full
```
