# CSAC刷机教程

## 进入原版固件后台
默认Wi-Fi名称为"CSAC_Home_XXXX"，默认后台地址[http://172.16.0.1/](http://172.16.0.1/)，默认密码"admin"。

## 刷入 X-Wrt 固件
可以下载本文作者测试过的[固件](https://dl.x-wrt.com:4443/rom/x-wrt-6.0-b201912290728-ath79-generic-xwrt_csac-squashfs-factory.bin)或者在 https://dl.x-wrt.net/rom/ 搜索 <code>xwrt_csac-squashfs-factory.bin</code> 下载最新固件。

进入固件后台，高级设置，升级，选择文件，选择刚才下载的文件，点击升级，出现弹窗：

<pre>
上传成功！下面是效验值和文件的大小，请与原文件进行比较，以确保数据的完整性。点击“确定”，
效验值：eb353d067d6eb082c732f0ac0b6ce9ef
文件大小：11.82MB
</pre>

点击确认，开始刷写固件。6分钟之后可以搜到 X-WRT 开头的热点。

