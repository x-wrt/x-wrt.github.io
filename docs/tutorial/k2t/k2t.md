##激活 Telnet

固件 22.23.1.158 及以后出的版本, 将不支持激活。非官方原版固件因为删减的原因, 可能不支持。

使用方法：
1. 连接连好电脑与K2T路由器，启动<code>RoutAckK2TV1B1.exe</code>，点击允许本程序访问网络（或者关闭防火墙）
2. 填写正确的 K2T 路由器 IP 地址
3. 点击【唤醒设备】（左侧按钮），程序会收到 设备识别码，收到后相应功能按钮可用。K2T的识别码为<code>343F6ECC3936CB73350B27A405FA6C4C</code>，如不是则可能是接错设备。如果收不到识别码，请检查IP和连线
4. 点击【打开Telnet】（右上按钮）
5. 功能按钮是一次性的，重复3、4步，再次执行功能

参考: http://www.right.com.cn/forum/thread-321483-16-1.html

##Windows 10 上开启 Telnet 功能
* Press Windows Key + S on your keyboard and enter features. Select Turn Windows Features on or off.
* When Windows Features opens, scroll down and check Telnet Client. Click OK to install Telnet.
* Wait until Windows installs the necessary components.
* Once the installation is completed click the Close button.

##可选：刷入breed
参考：http://www.right.com.cn/forum/thread-322551-1-1.html

##刷机
打开 cmd：

  telnet 192.168.2.1

  cd /tmp
  wget http://hk5.beijingxi.net/dl/natcap-4.0-b201807220408-ar71xx-generic-k2t-squashfs-sysupgrade.bin
  HASH=`md5sum natcap-4.0-b201807220408-ar71xx-generic-k2t-squashfs-sysupgrade.bin | awk '{print $1}'`
  if [ "c8618abb2641e36e9abedb24e5492ae1" == $HASH ]; then
    mtd -r write /tmp/natcap-4.0-b201807220408-ar71xx-generic-k2t-squashfs-sysupgrade.bin firmware
  fi
