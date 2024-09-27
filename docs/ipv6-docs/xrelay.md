# 4G/5G网络的IPv6万能中继配置

## 1. 说明
为什么需要中继，因为大多数4G/5G网络分配到的IPv6都是64位掩码的，并且分配不到IPv6-PD地址，x-wrt特有的万能中继配置可以让客户端也能连上ipv6

## 2. 网络拓扑
```
clients--->(lan)Router(usbwan6)--->Internet
```

## 3. 基本配置
假设wan/usbwan6口的网口设备名字是`usb0`（有些5G模块是eth1或者wwan0），要实现IPv6万能中继，执行下面命令:
```
echo vline_clear >/dev/natflow_ctl
echo vline_add=br-lan,usb0,ipv6 >/dev/natflow_ctl
echo vline_apply >/dev/natflow_ctl
```
注: `br-lan` 是lan口的网口设备名字

这样就可以对ipv6进行万能中继了

你可以把这些命令写入到 /etc/rc.local 启动脚本里面，这样就可以开机启用x-wrt特有IPv6万能中继了

**注意了，本配置适用于20240928之后的[官网下载](https://downloads.x-wrt.com/rom/)版本，GitHub下载版本不支持此功能**
