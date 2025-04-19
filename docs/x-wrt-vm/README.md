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
   默认目录为：~/x-wrt-macos

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

- 用户名：root

- 密码：admin

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

📜 启动脚本 qemu.root.sh 详解
这个脚本的作用不仅仅是启动虚拟机，还包括**网络接口选择**、**静态 IP 设置**、**DNS 配置**、**虚拟机桥接运行**、**网络恢复**等自动化步骤。下面是脚本主要功能分解：

### ✅ 功能要点：
1. 自动识别当前使用的默认上网接口（如 en0）
2. 自动获取该接口对应的 macOS 网络服务名
3. 设置该接口为静态 IP（192.168.15.123），用于桥接到 X-WRT
4. 配置 DNS 为公共 DNS（223.5.5.5 / 8.8.8.8）
5. 禁用 TSO，提升虚拟机网络兼容性
6. 根据当前平台选择 ARM 或 x86 架构运行 QEMU
7. 使用 macOS 原生虚拟化加速（hvf）启动 X-WRT 虚拟机
8. 桥接物理网卡到虚拟机，实现与外部网络直通
9. 自动恢复原始 DHCP 配置，确保退出后网络无异常

### 🚦 关键技术细节：
- `qemu-system-$ARCH`: 根据平台（arm64/x86_64）自动切换 QEMU 架构
- `vmnet-bridged`: 使用 macOS 原生桥接技术，无需额外 TUN/TAP 驱动
- `virtio-net`: 虚拟高性能网卡驱动
- `-nographic`: 不使用图形窗口，纯命令行运行
- `mac=$(ifconfig $ifname | awk '/ether/{print $2}')`: 自动生成唯一 MAC 地址，避免冲突

## 🧳 总结
通过这个方案，你可以在任何地方使用 MacBook 轻松模拟出一台全功能路由器，不再需要携带额外设备，满足上网、组网、科学访问等各种需求。

如需更多定制功能（例如自动挂载共享目录、开启无线接入点、VPN 自动连接等），欢迎继续提问，我可以帮你进一步优化方案！
