# 使用 x-wrt 虚拟机替代旅行路由器教程

在旅行时，有些朋友可能需要携带一个旅行路由器来上网，方便通过 VPN 或其他方式组网。然而，携带额外的设备可能会显得麻烦。本文将介绍如何使用虚拟机运行 x-wrt 系统，作为旅行路由器的替代方案。

## 环境要求

- 一台搭载 **M 芯片**的 Mac 电脑（例如 MacBook 系列）
- 已安装 Homebrew 包管理器

## 快速开始

### 1. 安装 QEMU

在终端中运行以下命令以安装 QEMU：

```bash
brew install qemu
```

### 2. 下载 x-wrt 虚拟机和运行脚本

下载打包好的 [x-wrt 虚拟机和运行脚本](https://downloads.x-wrt.com/rom/Downloads/x-wrt-macos.tgz)。

### 3. 解压文件

将下载的文件解压到目录，例如 `~/x-wrt-macos`：

```bash
tar -xzvf x-wrt-macos.tgz -C ~/
```

### 4. 启动 x-wrt 虚拟机

打开终端，依次运行以下命令：

```bash
cd ~/x-wrt-macos
sudo sh qemu.root.sh
```

输入管理员密码并按下回车后，系统会启动 x-wrt 虚拟机。启动完成后，您可以通过浏览器访问管理界面。

### 5. 管理 x-wrt 路由器

在浏览器中访问 [http://192.168.15.1](http://192.168.15.1) 即可进入 x-wrt 的管理界面，默认的用户名为 `admin`，密码为 `admin`。

### 6. 关闭 x-wrt 虚拟机

如果需要关闭虚拟机，在终端界面中按下回车键，输入以下命令：

```bash
# 登录虚拟机
root
admin
# 执行关机命令
poweroff
```

虚拟机关闭后，网络将恢复到原始状态。

---

## 网络拓扑变化

运行虚拟机前后，网络拓扑会发生如下变化：

### 运行前

```plaintext
MacBook电脑 ---> Wi-Fi网卡上网（DHCP） ---> 出口路由器
```

**图示：**

```plaintext
+-------------+    DHCP    +------------------+    Internet
| MacBook电脑 | ---------> | Wi-Fi网卡 (en0) |  -----------> 出口路由器
+-------------+            +------------------+
```

### 运行后

```plaintext
MacBook电脑（静态IP） ---> x-wrt虚拟路由器 ---> Wi-Fi网卡上网（DHCP） ---> 出口路由器
```

**图示：**

```plaintext
+-------------+    静态IP    +-----------------+    DHCP    +------------------+    Internet
| MacBook电脑 | -----------> | x-wrt虚拟路由器 | ---------> | Wi-Fi网卡 (en0) |  -----------> 出口路由器
+-------------+              +-----------------+            +------------------+
```

---

## qemu.root.sh 脚本详解

`qemu.root.sh` 脚本的主要功能是：

1. **检测默认网络设备**：自动识别当前的默认网络设备。
2. **配置静态 IP 和 DNS**：为虚拟机设置静态 IP 和 DNS。
3. **启动 QEMU 虚拟机**：加载 x-wrt 系统并运行。
4. **恢复网络设置**：在虚拟机关闭后，将网络恢复为 DHCP 模式。

以下是脚本的详细解析：

### 1. 检测默认网络设备

脚本通过以下命令获取当前默认网络设备名称（如 `en0`）：

```bash
DEVICE=$(route get default 2>/dev/null | awk '/interface: / {print $2}')
```

并根据设备名称找到对应的网络服务名称：

```bash
SERVICE=$(networksetup -listallhardwareports | awk -v dev="$DEVICE" '...')
```

### 2. 配置静态 IP 和 DNS

配置静态 IP 地址、子网掩码、默认网关和 DNS：

```bash
STATIC_IP="192.168.15.123"
SUBNET="255.255.255.0"
ROUTER="192.168.15.1"
DNS1="223.5.5.5"
DNS2="8.8.8.8"

networksetup -setmanual "$SRV" $STATIC_IP $SUBNET $ROUTER
networksetup -setdnsservers "$SRV" $DNS1 $DNS2
```

### 3. 启动 QEMU 虚拟机

脚本根据系统架构（如 `arm64` 或 `x86_64`）加载适配的内核和 rootfs 文件，并启动虚拟机：

```bash
qemu-system-$ARCH -m 256 -smp 2 -cpu host -M virt,highmem=off \
-nographic \
-accel hvf \
-kernel ${_DIR}/$ARCH-kernel.bin \
-drive file=${_DIR}/$ARCH-rootfs.img,format=raw,if=virtio \
-append root=/dev/vda \
-netdev vmnet-bridged,id=net0,ifname=$ifname \
-device virtio-net-$DEVTYPE,netdev=net0,mac=${mac:0:9}${md5:0:2}:${md5:2:2}:${md5:4:2}
```

### 4. 恢复网络设置

在虚拟机关闭后，脚本会恢复网络为 DHCP 模式：

```bash
networksetup -setdnsservers "$SRV" "Empty"
networksetup -setdhcp $SRV
```

---

## 注意事项

1. **管理员权限**：运行脚本需要管理员权限，请确保您有权限执行 `sudo` 命令。
2. **网络冲突**：虚拟机使用的 IP 地址段为 `192.168.15.x`，请确保该地址段不会与现有网络冲突。
3. **性能限制**：虚拟机性能可能受限于设备资源，请合理分配内存和 CPU。

---

通过本文提供的方案，您可以轻松地在 macOS 上使用 x-wrt 虚拟机代替旅行路由器，实现便捷的网络连接与管理。
