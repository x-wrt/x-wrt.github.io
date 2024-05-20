# 新路由3刷机教程

## 一键刷Breed
推荐使用[一键刷Breed程序](https://www.right.com.cn/forum/forum.php?mod=viewthread&tid=343058&page=1#pid3139054)。
### macOS
打开终端，执行：
```sh
git clone https://github.com/x-wrt/x-wrt.github.io
cd x-wrt.github.io/docs/tutorial/newifi3
pip3 install -r requirements.txt
python3 zy_y.py
```
### Windows
如果会装 Python，建议使用类似 macOS 步骤。否则，下载[压缩包](NEWIFI3.exe.zip)，解压缩双击。

成功后路由器会自动重启。断电后按<code>复位健</code>或者<code>USB键</code>开机均可进入 Breed。

## 刷入 X-WRT 固件
可以下载本文作者测试过的[固件](x-wrt-5.0-b201907230028-ramips-mt7621-d-team_newifi-d2-squashfs-sysupgrade.bin)或者在 [https://downloads.x-wrt.com/rom/](https://downloads.x-wrt.com/rom/) 搜索 <code>newifi-d2-squashfs-sysupgrade.bin</code> 下载最新固件。

用网线连接路由器，浏览器打开 http://192.168.1.1 进 Breed 控制台。点固件更新，上传固件。闪存布局不用改，点击上传，然后确认。3分钟之后可以搜到 X-WRT 开头的热点。

对于当前版本固件，确认页面信息如下：

|||
| --- | --- |
| 文件名 | x-wrt-5.0-b201907230028-ramips-mt7621-d-team_newifi-d2-squashfs-sysupgrade.bin |
| 大小 | 12.25MB (12845842B) |
| MD5 校验 | 4d5055fc7a32b7f4c0084154299e07df |
