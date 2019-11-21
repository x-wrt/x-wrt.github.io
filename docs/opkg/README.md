# 安装软件

### 开启ssh 登录
进入luci界面 `192.168.15.1`
进入 `系统` `管理权` `SSH访问`
开启SSH登录

### 安装软件命令例子

```sh
#我们使用https下载软件源
sed -i 's/http:/https:/g' /etc/opkg/distfeeds.conf

#更新官方源信息
opkg --no-check-certificate update

#列出软件包
opkg --no-check-certificate list

#安装
opkg --no-check-certificate install luci-app-shadowsocks-libev
opkg --no-check-certificate install shadowsocks-libev-config
opkg --no-check-certificate install shadowsocks-libev-ss-local
opkg --no-check-certificate install shadowsocks-libev-ss-redir
opkg --no-check-certificate install shadowsocks-libev-ss-rules
opkg --no-check-certificate install shadowsocks-libev-ss-server
opkg --no-check-certificate install shadowsocks-libev-ss-tunnel
```
