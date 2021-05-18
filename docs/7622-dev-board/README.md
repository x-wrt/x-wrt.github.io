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
