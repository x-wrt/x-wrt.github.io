## 配置chroot的ubuntu环境

1. 修改/创建配置文件 /etc/schroot/chroot.d/focal.conf
```
[focal]
type=directory
description=Ubuntu Focal
directory=/mnt/sda1/schroot/ubuntu
root-users=root
users=root
root-groups=root
personality=linux
```

2. 修改配置文件 `/etc/schroot/default/fstab`
```
# fstab: static file system information for chroots.
# Note that the mount point will be prefixed by the chroot path
# (CHROOT_PATH)
#
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
/proc           /proc           none    rw,bind         0       0
/sys            /sys            none    rw,bind         0       0
/dev            /dev            none    rw,bind         0       0
/dev/pts        /dev/pts        none    rw,bind         0       0
#/home           /home           none    rw,bind         0       0
/tmp            /tmp            none    rw,bind         0       0

# It may be desirable to have access to /run, especially if you wish
# to run additional services in the chroot.  However, note that this
# may potentially cause undesirable behaviour on upgrades, such as
# killing services on the host.
#/run           /run            none    rw,bind         0       0
#/run/lock      /run/lock       none    rw,bind         0       0
/tmp/shm       /dev/shm        none    rw,bind         0       0
/tmp/shm       /run/shm        none    rw,bind         0       0
```
这里把 `/home` `/run` 这两行注释掉了

3. 下载ubuntu环境的软件包
```
https://downloads.x-wrt.com/rom/Downloads/chroot/schroot-ubuntu-focal.tgz
```
保存到 `/mnt/sda1/schroot-ubuntu-focal.tgz`
```
cd /mnt/sda1/
wget https://downloads.x-wrt.com/rom/Downloads/chroot/schroot-ubuntu-focal.tgz --no-check-certificate -O schroot-ubuntu-focal.tgz

tar xvzf schroot-ubuntu-focal.tgz
```

解压后得到 `/mnt/sda1/schroot/ubuntu`

4. schroot 环境运行
```
schroot -l # 列出可以用的schroot环境
schroot -c focal # 切换到 ubuntu focal 的chroot环境
```

后面适用过程，就是 `schroot -c focal` 命令，切换到Ubuntu的chroot环境了，用起来跟Ubuntu基本无差异


## 创建 swapfile 交换内存
因为目前这个设备内存太小，不适合后面的编译工作，需要swap内存辅助
swapfile文件放到 U盘里面

```
dd if=/dev/zero of=/mnt/sda1/swapfile bs=1M count=1024

mkswap /mnt/sda1/swapfile
```

挂载swapfile
```
swapon /mnt/sda1/swapfile
```
