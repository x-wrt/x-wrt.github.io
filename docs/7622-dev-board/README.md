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
