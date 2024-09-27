# IPv6 万能中继配置指南

## 1. 背景说明
为什么需要 IPv6 中继？适用于哪些场景？

1. 在大多数 4G/5G 网络环境中，运营商分配的 IPv6 地址通常是 64 位前缀，且无法获取 IPv6-PD（前缀委派）地址，这意味着下游设备无法获得公网 IPv6 地址。
2. 当路由器通过光猫连接网络，且由光猫负责拨号时，路由器通常只会获得 64 位掩码的 IPv6 地址，同样无法为下游设备分配 IPv6 地址。
3. 当路由器作为二级路由器使用时，即便拿到了 IPv6 地址，也无法将其分配给下游设备。

这些场景的共性是：WAN 口可以获取 IPv6 地址，但无法获取 IPv6-PD 地址，而 LAN 口只有内网 IPv6 地址。

通过以下配置，可以实现 IPv6 万能中继，突破这些限制，使下游设备也能获取公网 IPv6 地址访问互联网。

**注意：启用万能中继后，路由器的防火墙将不再管理下游设备的 IPv6 流量。**

## 2. 网络拓扑示例
```
clients--->(lan)Router(usbwan6)--->Internet
```

## 3. 配置步骤
假设 WAN 或 `usbwan6` 口对应的网卡设备名称为 `usb0`（某些 5G 模块的设备名称可能为 `eth1` 或 `wwan0`），可以通过以下命令实现 IPv6 万能中继：
```
echo vline_clear >/dev/natflow_ctl
echo vline_add=br-lan,usb0,ipv6 >/dev/natflow_ctl
echo vline_apply >/dev/natflow_ctl
```
注：`br-lan` 是 LAN 口的网卡设备名称。

执行上述命令后，即可完成 IPv6 万能中继的配置。

为确保每次开机自动启用 IPv6 万能中继功能，可以将这些命令添加到 `/etc/rc.local` 启动脚本中。这样在路由器启动时，X-WRT 独有的 IPv6 万能中继功能将自动启用。

**重要提示：本配置适用于20240928之后的[官网下载](https://downloads.x-wrt.com/rom/)版本，GitHub下载版本不支持此功能**