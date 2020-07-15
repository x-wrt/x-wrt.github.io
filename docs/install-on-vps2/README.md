# X-Wrt安装部署到VPS上(新)

### 1. 介绍:

把OpenWrt系统部署到云服务器（VPS），因为OpenWrt是网络系统，对转发做了不少优化，而且有良好的配置界面，很多服务比如OpenVPN等可以一键部署。注意本教程只适用于x-wrt固件，其它OpenWrt固件不适用。

本教程对于绝大多数VPS适用，比如vultr digitalocean Amazon的AWS Linode 阿里云 腾讯云 等等。但是不同的云，实际情况不太相同，要随机应变，根据实际情况做正确的处理。

这是新版本的教程，可以保证几乎100%成功部署到所有的VPS上面。

### 2. 教程:

#### 2.1 固件下载
我们选择选择x86 64bits(MBR dos)或者x86 64bits(UEFI gpt)的固件，下载地址:
[https://downloads.x-wrt.com/rom/](https://downloads.x-wrt.com/rom/)
刷机需要到的文件
```
x-wrt-x86-64-generic-initramfs-kernel.bin
x-wrt-x86-64-generic-ext4-combined.img.gz
```
如果是EFI系统，需要EFI固件
```
x-wrt-x86-64-generic-ext4-combined-efi.img.gz
```

#### 2.2 VPS系统部署
VPS系统的要求，可以是Ubuntu，可以是CentOS，可以是Debian，或者其他

#### 2.3 VPS系统的网络配置识别
在部署之前，我们要清楚VPS的IP地址是如何分配的，有些VPS是自动获取(DHCP)分配的IP，有些是静态配置的，有些是双网卡和多网卡的。

登录VPS后，查看VPS的网卡IP地址，`ifconfig` 或者 `ip list` 命令查看，然后执行 `grep /etc -nre <IP>` 命令，如果抓到了包含这个`<IP>`的文件，打开看看是否是静态配置的脚本，找到这样的脚本，我们就鉴定这个VPS是静态配置，否则是动态配置。

另外，观察是否有多个网口，如果有多个网口，安装的时候需要注意，下面有说明。

#### 2.4 确定磁盘的路径和分区类型
用 `df` 和 `mount` 命令查看磁盘，确定磁盘第一个分区挂载的路径，比如磁盘第一个分区，通常是`/dev/sda1 /dev/vda1 /dev/xvda1`等等，类似这些。要注意的是这个分区的挂载路径和剩余空间大小，通常这个分区挂载在 `/` 或者 `/boot` 我们在刷机过程需要把固件等文件放到这个路径下面保存好。

用`fdisk -l`查看分区类型，看是不是gpt，如果是gpt就需要刷EFI固件，通常不是。

#### 2.5 开始刷机
刷机需要的文件，用wget下载下来
```
x-wrt-x86-64-generic-initramfs-kernel.bin
x-wrt-x86-64-generic-ext4-combined.img.gz 或者 x-wrt-x86-64-generic-ext4-combined-efi.img.gz
```

确定当前系统运行的内核路径，通常是 `/boot/vmlinuz*` 用 `uname -r` 查看内核版本。比如，路径是`/boot/vmlinuz-4.15.0-111-generic` 我们需要把 `x-wrt-x86-64-generic-initramfs-kernel.bin` 替换这个内核
```
cp x-wrt-x86-64-generic-initramfs-kernel.bin /boot/vmlinuz-4.15.0-111-generic
```

然后我们需要确定第一个分区的路径，假如第一个分区是 `/` 我们把固件拷贝到 `/` 保存好 主意保存的名字是 `x-wrt.img.gz`
```
cp x-wrt-x86-64-generic-ext4-combined.img.gz /x-wrt.img.gz
```
同时我们还需要一个安装脚本，脚本路径和固件保存的目录相同，这个例子是`/` 脚本名字是 `x-wrt-install-vps.sh` 脚本的代码参考如下:
```
#!/bin/sh

BDEV=sda
# static ip
#network=172.21.170.245,255.255.240.0,172.21.175.253,8.8.8.8
# static ip swap eth0 eth1
#network="117.18.13.159,255.255.255.0,117.18.13.1,8.8.8.8,initscript=dWNpIHNldCBuZXR3b3JrLmxhbi5pZm5hbWU9ZXRoMQp1Y2kgc2V0IG5ldHdvcmsud2FuLmlmbmFtZT1ldGgwCnVjaSBjb21taXQgbmV0d29yawo="
# dhcp ip
network=dhcp

vmroot=/tmp/block
mkdir -p $vmroot
mount /dev/${BDEV}1 $vmroot || exit 0
cp $vmroot/x-wrt.img.gz /tmp/x-wrt.img.gz && {
	cd /
	umount $vmroot
	sync
	(zcat /tmp/x-wrt.img.gz;
	 echo open=443,network=$network;
	) >/dev/$BDEV && reboot
}
```
这个脚本准备刷机的磁盘是sda，第一个分区是sda1，它是DHCP动态获取IP的。你需要根据情况修改刷机脚本，脚本会在重启后启动initramfs内核并且执行。
如果磁盘是vda，就修改BDEV的值，注意，如果是静态IP，就注释掉`network=dhcp`，启用静态IP那一行的`network=<ip>,<mask>,<gateway>,<dns>`，如果VPS有多个网卡，比如有2个`eth0 eth1`，我们需要附加一个`initscript=<script base64 codes>`来做交换网口，这个`<script base64 codes>`其实是如下脚本的base64编码，你要根据情况修改
```
uci set network.lan.ifname=eth1
uci set network.wan.ifname=eth0
uci commit network
```

好了，如果上述处理妥当，就`reboot`重启，由于咱们用initramfs-kernel替换了内核，重启后将会进入initramfs-kernel的系统，然后这个系统会寻找 x-wrt-install-vps.sh 这个脚本执行刷机，这个脚本干的事情很简单，挂载第一个分区，拷贝固件到`/tmp`目录，然后执行刷机重启。

这个过程大概需要5分钟，看情况了。


系统重启后，我们将可以访问到OpenWrt管理界面，比如本文的例子，管理界面地址 `https://[VPS_IP]/` 进入管理界面后，要立刻修改默认的管理密码，默认的账号密码是 root/admin，其次，如果有需要，进入系统管理权页面，开启ssh账号密码登录，并且要设置防火墙开放wan区22端口的访问。

最后，自由的进行各种配置吧！一个漂亮又熟悉的OpenWrt Luci界面就在你面前了。

