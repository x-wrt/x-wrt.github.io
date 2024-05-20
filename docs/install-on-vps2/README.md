# X-WRT 安装部署到VPS上(新)

### 1. 介绍:

本教程旨在介绍如何将 X-WRT 系统部署到云服务器（VPS）上。X-WRT 是一个专为路由器设计的开源系统，具有出色的网络转发优化和友好的配置界面。同时，该系统还提供了许多方便的服务，如 OpenVPN 等，可以轻松地一键部署。

需要注意的是，本教程适用于大多数 VPS，如 vultr、digitalocean、Amazon 的 AWS、Linode、阿里云、腾讯云等。然而，由于不同云服务商的实际情况不同，您需要灵活应对，根据实际情况做出正确的处理。

本教程只适用于 X-WRT 固件，可以保证几乎 100% 成功地将 X-WRT 系统部署到所有的 VPS 上。

### 2. 教程:

#### 2.1 固件下载
我们选择 x86 64 位 (MBR dos) 或 x86 64 位 (UEFI gpt) 的固件进行部署。您可以从以下链接下载所需的文件：

[https://downloads.x-wrt.com/rom/](https://downloads.x-wrt.com/rom/)

刷机所需的文件如下：
```
x-wrt-x86-64-generic-initramfs-kernel.bin
x-wrt-x86-64-generic-ext4-combined.img.gz
```

如果您的系统是 EFI 系统，则还需要下载以下文件：
```
x-wrt-x86-64-generic-ext4-combined-efi.img.gz
```

#### 2.2 VPS系统部署
本教程所涉及的 VPS 系统要求比较宽松，可以是 Ubuntu、CentOS、Debian 或其他类 Unix 系统。

#### 2.3 VPS系统的网络配置识别
在开始部署之前，我们需要了解 VPS 的 IP 地址是如何分配的。有些 VPS 是通过 DHCP 自动获取 IP 地址，有些是静态配置的，还有一些是双网卡或多网卡的。

登录 VPS 后，可以使用 `ifconfig` 或者 `ip list` 命令查看 VPS 的网卡 IP 地址。然后，使用命令 `grep /etc -nre <IP>` 查找包含此 `<IP>` 的文件。如果找到了相关文件，并且文件内容包含静态配置的脚本，那么我们可以确定该 VPS 是静态配置的。否则，它是动态配置的。

此外，我们还需要观察 VPS 是否具有多个网口。如果是，那么在安装过程中需要特别注意。下面将有进一步的说明。

#### 2.4 确定磁盘的路径和分区类型
使用 `df` 和 `mount` 命令可以查看 VPS 的磁盘信息，确定磁盘的第一个分区挂载路径，例如 `/dev/sda1`、`/dev/vda1`、`/dev/xvda1` 等等。需要注意的是，此分区的挂载路径以及可用空间大小，通常情况下此分区挂载在 `/` 或者 `/boot` 下，而我们在刷机过程中需要将固件等文件保存在此路径下。

使用 `fdisk -l` 命令可以查看分区类型，以确定分区是否为 GPT。如果分区为 GPT，则需要刷写 EFI 固件。但通常情况下分区不是 GPT 类型。

#### 2.5 开始刷机
以下是刷机所需的文件，您可以使用 wget 命令进行下载：
```
x-wrt-x86-64-generic-initramfs-kernel.bin
x-wrt-x86-64-generic-ext4-combined.img.gz 或者 x-wrt-x86-64-generic-ext4-combined-efi.img.gz
```

在刷机之前，需要确定当前系统运行的内核路径。一般来说，这个路径是 `/boot/vmlinuz*`。您可以使用 `uname -r` 命令查看内核版本。比如，如果路径是 `/boot/vmlinuz-4.15.0-111-generic`，那么我们需要把 `x-wrt-x86-64-generic-initramfs-kernel.bin` 替换为这个内核：
```
cp x-wrt-x86-64-generic-initramfs-kernel.bin /boot/vmlinuz-4.15.0-111-generic
```

然后我们需要确定第一个分区的路径，假如第一个分区是 `/` 我们把固件拷贝到 `/` 保存好，注意保存的名字是 `x-wrt.img.gz`
```
cp x-wrt-x86-64-generic-ext4-combined.img.gz /x-wrt.img.gz
```

同时我们还需要一个安装脚本，脚本路径和固件保存的目录相同，这个例子是`/` ，脚本名字是 `x-wrt-install-vps.sh` 脚本的代码参考如下：（根据情况修改）
```
#!/bin/sh

# install to sda
BDEV=sda

# x-wrt.img.gz in disk part sda1
DDEV=sda1

# static ip
#network=172.21.170.245,255.255.240.0,172.21.175.253,8.8.8.8

# static ip swap eth0 eth1
#network="117.18.13.159,255.255.255.0,117.18.13.1,8.8.8.8,initscript=dWNpIHNldCBuZXR3b3JrLmxhbi5pZm5hbWU9ZXRoMQp1Y2kgc2V0IG5ldHdvcmsud2FuLmlmbmFtZT1ldGgwCnVjaSBjb21taXQgbmV0d29yawo="

# dhcp ip
network=dhcp

vmroot=/tmp/block
mkdir -p $vmroot
mount /dev/${DDEV} $vmroot || exit 0
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

如果磁盘是vda，就修改BDEV的值，注意，如果是静态IP，就注释掉`network=dhcp`，启用静态IP那一行的`network=<ip>,<mask>,<gateway>,<dns>`，如果VPS有多个网卡，比如有2个`eth0 eth1`，我们需要附加一个`initscript=<script base64 codes>`来做交换网口，这个`<script base64 codes>`其实是如下脚本的base64编码，你要根据情况修改。
```
uci set network.lan.ifname=eth1
uci set network.wan.ifname=eth0
uci commit network
```

如果以上操作正确无误，就执行`reboot`重启系统。由于我们使用initramfs-kernel替换了原有内核，重启后系统会进入initramfs-kernel环境。然后，该环境会查找 x-wrt-install-vps.sh 脚本并执行刷机操作。这个脚本执行的内容很简单：挂载第一个分区、将固件拷贝到 /tmp 目录中，然后执行刷机并重启。这个过程大概需要5分钟，看情况了。

### 3. 总结:

整个刷机过程，大概就三个步骤:
1. 下载好两个固件文件，保存到特定的路径
2. 拷贝并且根据情况修改好一个脚本(`x-wrt-install-vps.sh`)，保存到特定路径
3. 重启(reboot)并等待自动安装完成

系统重启后，你将能够通过访问 X-WRT 的管理界面来配置路由器。以本文的例子为例，管理界面的地址(HTTPS)是 `https://[VPS_IP]/`。进入管理界面后，你需要立即修改默认的管理密码。默认的账号/密码是 admin/admin。此外，如果需要，你可以进入系统管理页面，启用 SSH 账户密码登录，并设置防火墙以允许来自 WAN 区域的22端口访问。这样可以使你能够远程登录到路由器并进行更多的配置。
