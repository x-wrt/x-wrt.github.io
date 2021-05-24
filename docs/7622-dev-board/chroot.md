### 这个教程主要是在x-wrt平台上，创建一个Ubuntu的chroot环境运行环境，方便开发/编译/运行相关程序，用起来和Ubuntu环境基本无差异


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

后面使用过程，就是 `schroot -c focal` 命令，切换到Ubuntu的chroot环境了，用起来跟Ubuntu基本无差异


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

### 最终效果
```
(focal)root@X-WRT:~#
(focal)root@X-WRT:~# lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 20.04.2 LTS
Release:        20.04
Codename:       focal
(focal)root@X-WRT:~# java --version
openjdk 11.0.11 2021-04-20
OpenJDK Runtime Environment (build 11.0.11+9-Ubuntu-0ubuntu2.20.04)
OpenJDK 64-Bit Server VM (build 11.0.11+9-Ubuntu-0ubuntu2.20.04, mixed mode)
(focal)root@X-WRT:~# python3 --version
Python 3.8.5
(focal)root@X-WRT:~#
```


## 关于 amazon-kinesis-video-streams-producer-sdk-cpp 的编译

无需编译它的依赖库，因为Ubuntu运行环境已经有了，所以我们编译的时候:

```
mkdir -p amazon-kinesis-video-streams-producer-sdk-cpp/build
cd amazon-kinesis-video-streams-producer-sdk-cpp/build

cmake .. -DBUILD_GSTREAMER_PLUGIN=ON -DBUILD_DEPENDENCIES=OFF

make
```
更多细节请参考: https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-cpp
