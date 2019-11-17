# X-Wrt 安装软件

### 开启ssh 登录
进入luci界面 192.168.15.1
进入 系统 管理权 SSH访问
开启 SSH 登录

### 安装软件命令例子

```sh
#更新官方源信息
opkg update

#列出软件包
opkg list

#安装
opkg install luci-app-shadowsocks-libev
opkg install shadowsocks-libev-config
opkg install shadowsocks-libev-ss-local
opkg install shadowsocks-libev-ss-redir
opkg install shadowsocks-libev-ss-rules
opkg install shadowsocks-libev-ss-server
opkg install shadowsocks-libev-ss-tunnel
```
