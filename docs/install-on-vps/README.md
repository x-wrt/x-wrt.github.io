# X-Wrt安装部署到VPS上

### 1. 介绍:

把OpenWrt系统部署到云服务器（VPS），因为OpenWrt是网络系统，对转发做了不少优化，而且有良好的配置界面，很多服务比如OpenVPN等可以一键部署。注意本教程只适用于x-wrt固件，其它OpenWrt固件不适用。

本教程对于绝大多数VPS适用，比如vultr digitalocean Amazon的AWS Linode 阿里云 腾讯云 等等。但是不同的云，实际情况不太相同，要随机应变，根据实际情况做正确的处理。

### 2. 教程:

#### 2.1 固件下载
我们选择选择x86 64bits(MBR dos)或者x86 64bits(UEFI gpt)的固件，下载地址:
[https://x-wrt.com/rom/](https://x-wrt.com/rom/)

#### 2.2 VPS系统部署
我们首先安装其它系统比如Ubuntu，然后从Ubuntu系统刷机变成OpenWrt系统。为什么不直接安装OpenWrt固件呢？因为云平台不支持。不过有些云平台是支持的，比如Linode可以启动一个小的拯救系统做系统安装的事情，再比如有些平台可以启动自定义ISO镜像，那安装方法自然是制作一个Live CD或者安装光盘之类了。

废话不多说，安装VPS初始系统: 选择Ubuntu系统，按照云平台指导的流程完全初始的部署

#### 2.3 上传固件
把固件（比如x-wrt-4.0-b2018xxxxxxxx-x86-64-combined-ext4.img.gz）上传到VPS的 `/root/` 目录下，保存为 `/root/x-wrt.img.gz` 其它目录也是可以的，当然也可以通过网络直接下载回来:
```sh
wget -O /root/x-wrt.img.gz --no-check-certificate https://x-wrt.com/rom/x-wrt-<XXXXXX>-x86-64-combined-ext4.img.gz
```

#### 2.4 确定磁盘的路径
用 `df -h` 命令查看 `/` 挂载的设备是什么，比如是 `/dev/vda1` （有些平台是 `/dev/sda1` 或者其它），这里很容易可以确定磁盘路径是 `/dev/vda` （去掉了尾数1）。
```
# df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            916M     0  916M   0% /dev
tmpfs           188M   22M  166M  12% /run
/dev/vda1        50G  3.9G   44G   9% /
tmpfs           937M   24K  937M   1% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
tmpfs           937M     0  937M   0% /sys/fs/cgroup
tmpfs           188M     0  188M   0% /run/user/500
```

#### 2.5 确定网络配置
有些平台给VPS自动DHCP分配IP，有些平台不是自动而是静态配置IP，我们需要根据实际情况确定好是哪一种方式。

假如是静态配置的方式，一般查看 `/etc/network/interfaces` 文件可以看到实际的配置参数，比如:
```
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address 172.21.170.245
    netmask 255.255.240.0
    post-up route add default gw 172.21.175.253 || true
    pre-down route del default gw 172.21.175.253 || true
```
这里我们就知道是 `ip=172.21.170.245 netmask=255.255.240.0 gateway=172.21.175.253`

如果是DHCP自动的方式，就更简单了，后面刷机的时候，就知道啦。

#### 2.6 刷机准备
由于刷机是在原有系统运行的情况下直接刷写磁盘，所以为了安全我们要让 `/` 文件系统挂成只读，防止相互写入导致数据错乱最后刷成砖。修改配置文件 `/etc/fstab` 把 `/` 挂载的那一行的选项改成 `ro` 意思是ReadOnly，然后 `reboot` 重启系统。
```
# /etc/fstab: static file system information.
#
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
UUID=061939c8-339d-488f-9538-83b9cbf559ea /     ext4    errors=remount-ro 0       1
```
比如这个例子文件，把 `errors=remount-ro` 改成 `ro`

另外我们还需要选择一个内存路径用来刷机过程存放临时文件，执行 `df -h` 命令查看
```
# df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            916M     0  916M   0% /dev
tmpfs           188M   22M  166M  12% /run
/dev/vda1        50G  3.9G   44G   9% /
tmpfs           937M   24K  937M   1% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
tmpfs           937M     0  937M   0% /sys/fs/cgroup
tmpfs           188M     0  188M   0% /run/user/500
```
不难发现 `/dev/shm/` 这个路径是tmpfs类型，有900M之多的可用空间，非常适合作为刷机的临时内存路径。注意了，x-wrt固件解压后的大小是256M，所以要选择大于300M的临时内存路径，否则空间不够。

#### 2.7 开始刷机
刷机阶段一: 把固件连同配置参数组合一起写入 `/dev/shm/` 这个临时路径。
```sh
(zcat /root/x-wrt.img.gz; echo open=443,network=dhcp) >/dev/shm/x-wrt.img
```
解释一下，这里是把固件解压，连同后面的配置参数 `open=443,network=dhcp` 一起合并写入到 `/dev/shm/x-wrt.img` 配置参数的意思是: wan口防火墙开放443端口（管理界面的端口），网络配置是DHCP自动获取IP地址。

如果网络配置是静态配置IP，使用下面的命令:
```sh
(zcat /root/x-wrt.img.gz; echo open=443,network=172.21.170.245,255.255.240.0,172.21.175.253,8.8.8.8) >/dev/shm/x-wrt.img
```
不难理解，我们要设置`ip=172.21.170.245 netmask=255.255.240.0 gateway=172.21.175.253 dns=8.8.8.8` 这些参数来源是原来这个VPS系统的参数。注意一下，这里`ip netmask gateway dns` 4个参数不要缺少任何一个，否则会失败。

再进一步解释一下，为什么可以这样给新刷的OpenWrt系统设置参数，因为这个x-wrt固件做了这方面的支持，它会在首次启动的时候读取这些配置参数并实际设置到OpenWrt的配置里面。

刷机阶段二: 把固件刷入磁盘并且重启
```sh
cat /dev/shm/x-wrt.img >/dev/vda && reboot
```
或者
```sh
dd if=/dev/shm/x-wrt.img of=/dev/vda && reboot
```
系统重启后，我们将可以访问到OpenWrt管理界面，比如本文的例子，管理界面地址 `https://[VPS_IP]/` 进入管理界面后，要立刻修改默认的管理密码，默认的账号密码是 root/admin，其次，如果有需要，进入系统管理权页面，开启ssh账号密码登录，并且要设置防火墙开放wan区22端口的访问。

最后，自由的进行各种配置吧！一个漂亮又熟悉的OpenWrt Luci界面就在你面前了。

