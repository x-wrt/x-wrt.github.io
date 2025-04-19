# 使用虚拟机运行 X-WRT：打造轻便旅行路由器（适用于 macOS M 系列）
在外出差、旅游时，很多人会携带一个旅行路由器，以便更方便地连网、翻墙、组网等。但随身带个设备终归麻烦。现在，有一个更轻巧的方案：直接在你的 M 系列 Mac（如 MacBook Air/Pro）上运行一个 X-WRT 虚拟机，模拟旅行路由器的功能，完全免设备，随插随用！

## ✅ 方案概览
我们将使用 QEMU 虚拟机在 macOS 上运行一个定制好的 X-WRT 系统镜像，X-WRT 是基于 OpenWRT 的路由系统，轻量灵活，适合网络穿透、科学上网、旁路由等场景。

## 🧰 准备工作
1. 安装 Homebrew：  
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. 安装 QEMU
   ```bash
   brew install qemu
   ```
3. 下载 X-WRT 虚拟机镜像包
   从官方提供的地址下载：

   [👉 x-wrt-macos.tgz 下载地址](https://downloads.x-wrt.com/rom/Downloads/x-wrt-macos.tgz)

4. 解压到主目录下
   ```bash
   tar -xzvf x-wrt-macos.tgz -C ~/
   ```
   默认目录为：`~/x-wrt-macos`

## 🚀 启动 X-WRT 虚拟路由器
打开终端，进入目录并运行启动脚本：
```bash
cd ~/x-wrt-macos
sudo sh qemu.root.sh
```
系统会要求输入当前用户的密码（用于修改网络配置），输入后回车。

等待大约 10~20 秒，X-WRT 启动完成后，你的 macOS 就像连接了一个虚拟路由器

## 🌐 访问路由器 Web 管理界面
打开浏览器访问：
```
http://192.168.15.1
```
默认账号密码：

- 用户名：`admin`

- 密码：`admin`

你可以在这里配置 VPN、旁路由、端口转发等所有 OpenWRT 支持的功能。

## 📴 如何关闭虚拟路由器
回到运行`QEMU`的终端界面：

按下`Enter`，出现登录提示。

输入用户名`root`，密码`admin`。

输入命令：
```
poweroff
```
虚拟机将优雅关机，并自动恢复 macOS 网络设置（DHCP）。

## 📜 启动脚本 qemu.root.sh 详解
脚本 qemu.root.sh：
```bash
#!/bin/sh

SRV=Wi-Fi
ifname=en0

# 步骤 1：获取默认路由出口设备名（如 en0）
DEVICE=$(route get default 2>/dev/null | awk '/interface: / {print $2}')
if [ -z "$DEVICE" ]; then
    echo "❌ 无法识别默认网络设备"
    exit 1
fi

echo "🔍 当前默认上网设备为: $DEVICE"
ifname="$DEVICE"

# 步骤 2：找到该设备对应的 networkservice 名称
SERVICE=$(networksetup -listallhardwareports | \
    awk -v dev="$DEVICE" '
    $1 == "Hardware" && $2 == "Port:" {port=$3}
    $1 == "Device:" && $2 == dev {print port}' \
)

if [ -z "$SERVICE" ]; then
    echo "❌ 无法匹配到 network service 名称"
    exit 1
fi

echo "✅ 对应的网络服务名称是: $SERVICE"
SRV="$SERVICE"

# 配置参数
STATIC_IP="192.168.15.123"
SUBNET="255.255.255.0"
ROUTER="192.168.15.1"
DNS1="223.5.5.5"
DNS2="8.8.8.8"

echo "⚙️ 设置静态 IP 为 $STATIC_IP"
networksetup -setmanual "$SRV" $STATIC_IP $SUBNET $ROUTER
echo "⚙️ 设置 DNS 为 $DNS1 和 $DNS2"
networksetup -setdnsservers "$SRV" $DNS1 $DNS2

echo "⚙️ 设置 网卡关闭tso"
ifconfig $ifname -tso

_DIR=$(dirname $0)
mac=$(ifconfig $ifname | awk '/ether/{print $2}')
md5=$(echo -n $mac | md5)

echo "🕐"
echo "🕐"
echo "🕐 qemu 启动x-wrt虚拟机..."
echo "." && sleep 1
echo ".." && sleep 1
echo "..." && sleep 5

ARCH=x86_64
DEVTYPE=pci
case $(uname -m) in
	arm64)
		ARCH=aarch64
		DEVTYPE=device
	;;
esac

qemu-system-$ARCH -m 256 -smp 2 -cpu host -M virt,highmem=off \
-nographic \
-accel hvf \
-kernel ${_DIR}/$ARCH-kernel.bin \
-drive file=${_DIR}/$ARCH-rootfs.img,format=raw,if=virtio \
-append root=/dev/vda \
-netdev vmnet-bridged,id=net0,ifname=$ifname \
-device virtio-net-$DEVTYPE,netdev=net0,mac=${mac:0:9}${md5:0:2}:${md5:2:2}:${md5:4:2}
#-nic vmnet-bridged,ifname=$ifname,mac=${mac:0:9}${md5:0:2}:${md5:2:2}:${md5:4:2}

echo "♻️ 正在恢复为 DHCP 模式..."
networksetup -setdnsservers "$SRV" "Empty"
networksetup -setdhcp $SRV

echo "✅ 已恢复为自动获取 IP 和 DNS！"

exit 0
```
这个脚本的作用不仅仅是启动虚拟机，还包括**网络接口选择**、**静态 IP 设置**、**DNS 配置**、**虚拟机桥接运行**、**网络恢复**等自动化步骤。下面是脚本主要功能分解：

### ✅ 功能要点：
1. **自动识别当前使用的默认上网接口（如 en0）**
2. **自动获取该接口对应的 macOS 网络服务名**
3. **设置该接口为静态 IP（192.168.15.123），用于桥接到 X-WRT**
4. **配置 DNS 为公共 DNS（223.5.5.5 / 8.8.8.8）**
5. **禁用 TSO，提升虚拟机网络兼容性**
6. **根据当前平台选择 ARM 或 x86 架构运行 QEMU**
7. **使用 macOS 原生虚拟化加速（hvf）启动 X-WRT 虚拟机**
8. **桥接物理网卡到虚拟机，实现与外部网络直通**
9. **自动恢复原始 DHCP 配置，确保退出后网络无异常**

### 🚦 关键技术细节：
- `qemu-system-$ARCH`: 根据平台（arm64/x86_64）自动切换 QEMU 架构
- `vmnet-bridged`: 使用 macOS 原生桥接技术，无需额外 TUN/TAP 驱动
- `virtio-net`: 虚拟高性能网卡驱动
- `-nographic`: 不使用图形窗口，纯命令行运行
- `mac=$(ifconfig $ifname | awk '/ether/{print $2}')`: 自动生成唯一 MAC 地址，避免冲突

## 🧳 总结
通过这个方案，你可以在任何地方使用 MacBook 轻松模拟出一台全功能路由器，不再需要携带额外设备，满足上网、组网、科学访问等各种需求。
