# 7622 扩展U盘存储

1. 插上U盘，格式化
```
mkfs.ext4 /dev/sda1
```

2. 重新拔插U盘
```
df 命令可以看见
/dev/sda1             58148080   1528616  53635980   3% /mnt/sda1

block info 命令获得 UUID
/dev/sda1: UUID="c17aeec1-6733-4f2f-adcb-b094b7dd8c79" VERSION="1.0" MOUNT="/mnt/sda1" TYPE="ext4"

修改文件
vim /etc/config/fstab

config global
        option anon_swap '0'
        option auto_swap '1'
        option auto_mount '1'
        option delay_root '5'
        option check_fs '0'
        option anon_mount '1'

config 'mount'
        option  target  '/overlay'
        option  uuid    'c17aeec1-6733-4f2f-adcb-b094b7dd8c79'
        option  fstype  'ext4'
        option  options 'rw,noatime'
        option  enabled '1'

UUID 改成对应

cp -f -a /overlay/. /mnt/sda1/

然后 reboot 重启
```

重启后，可以看见，空间被扩展了
```
df -h
Filesystem                Size      Used Available Use% Mounted on
/dev/root                16.8M     16.8M         0 100% /rom
devtmpfs                113.8M         0    113.8M   0% /rom/dev
tmpfs                   114.0M    144.0K    113.9M   0% /tmp
/dev/sda1                55.5G      1.5G     51.2G   3% /overlay
overlayfs:/overlay       55.5G      1.5G     51.2G   3% /
tmpfs                     1.0M         0      1.0M   0% /mnt
tmpfs                   512.0K         0    512.0K   0% /dev
/dev/mtdblock8           10.5M    516.0K     10.0M   5% /mnt/mtdblock8

dmesg 可以看见如下信息:
root@X-WRT:~# dmesg | grep extroot
[    7.802622] mount_root: switched to extroot
```
# 7622 开发版安装aws greengrass

1. 下载java 11 (JDK 11)
```
OpenJDK11U-jdk_aarch64_linux_hotspot_11.0.11_9.tar.gz
```
https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.11%2B9/OpenJDK11U-jdk_aarch64_linux_hotspot_11.0.11_9.tar.gz

或者
```
amazon-corretto-11-aarch64-linux-jdk.tar.gz
```
https://corretto.aws/downloads/latest/amazon-corretto-11-aarch64-linux-jdk.tar.gz

2. 安装java 11 (JDK 11)
```
tar xvzf OpenJDK11U-jdk_aarch64_linux_hotspot_11.0.11_9.tar.gz
mkdir /usr/local
cp -a jdk-11.0.11\+9/. /usr/local/
```

修改环境变量 PATH
```
修改文件 /etc/preinit 和文件 /etc/profile
把
export PATH="/usr/sbin:/usr/bin:/sbin:/bin"
改成
export PATH="/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin"
```

3. 安装greengrass

```
wget --no-check-certificate https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-nucleus-latest.zip -O greengrass-nucleus-latest.zip

unzip greengrass-nucleus-latest.zip -d MyGreengrassCore

export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

java -Droot="/greengrass/v2" -Dlog.store=FILE \
  -jar ./MyGreengrassCore/lib/Greengrass.jar \
  --aws-region region \
  --thing-name MyGreengrassCore \
  --thing-group-name MyGreengrassCoreGroup \
  --tes-role-name GreengrassV2TokenExchangeRole \
  --tes-role-alias-name GreengrassCoreTokenExchangeRoleAlias \
  --component-default-user root:root \
  --provision true \
  --setup-system-service true \
  --deploy-dev-tools true
```

4. 运行greengrass核心服务
```
/greengrass/v2/alts/current/distro/bin/loader
```
如果需要开机启动，按照Openwrt规范写启动脚本，开机运行 (待定)
