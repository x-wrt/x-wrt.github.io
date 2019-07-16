## 激活 Telnet

固件 22.23.1.158 及以后出的版本, 将不支持激活。非官方原版固件因为删减的原因, 可能不支持。

使用方法：
1. 电脑有线或者无线连上K2T路由器，下载[激活工具](RoutAckK2TV1B1.zip)并解压缩，启动<code>RoutAckK2TV1B1.exe</code>，点击允许本程序访问网络（或者关闭防火墙）
2. 填写正确的 K2T 路由器 IP 地址
3. 点击【唤醒设备】（左侧按钮），程序会收到 设备识别码，收到后相应功能按钮可用。K2T的识别码为<code>343F6ECC3936CB73350B27A405FA6C4C</code>，如不是则可能是接错设备。如果收不到识别码，请检查IP和连线
4. 点击【打开Telnet】（右上按钮）
5. 功能按钮是一次性的，重复3、4步，再次执行功能

参考: http://www.right.com.cn/forum/thread-321483-16-1.html

## Windows 10 上开启 Telnet 功能
* 点击开始按钮，搜索“启用或关闭 Windows 功能”，点击第一个结果。
* 下拉找到“Telnet Client”，勾选并点击确定。
* 等一会儿就可以安装好了，点“关闭”即可。

English version: Enable Telnet Client on Windows 10

* Press Start button, type "Turn Windows Features on or off" and open the first setting.
* When Windows Features opens, scroll down and check Telnet Client. Click OK to install Telnet.
* Wait until Windows installs the necessary components.
* Once the installation is completed click the Close button.

## 可选：刷入breed
参考：http://www.right.com.cn/forum/thread-322551-1-1.html

## 刷机
连接路由器：
* 如果是第一次刷固件，则是 cmd ：<code>telnet 192.168.2.1</code>
* 如果是更新固件，需要先开启 SSH，然后 bash：<code>ssh  root@192.168.2.1</code>

执行以下命令：

```sh
cd /tmp
wget http://dl.x-wrt.net/rom/x-wrt-5.0-b201907141234-ar71xx-generic-k2t-squashfs-sysupgrade.bin
HASH=`md5sum x-wrt-5.0-b201907141234-ar71xx-generic-k2t-squashfs-sysupgrade.bin | awk '{print $1}'`
if [ "603216fbad62a7f81d9b529a12288567" == $HASH ]; then
  mtd -r write /tmp/x-wrt-5.0-b201907141234-ar71xx-generic-k2t-squashfs-sysupgrade.bin firmware
fi
```