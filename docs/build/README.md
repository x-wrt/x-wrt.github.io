# 编译教程

很多人不知道怎样编译一个自己的固件，这里主要简单介绍大概的编译打包流程，具体的情况还需要大家自己发挥，情况千变万化，大家随机应变。

## 1 编译准备
我们建议使用[Ubuntu](https://www.ubuntu.com/)系统作为编译环境，这里以Ubuntu 18.04作为例子，其他版本也是可以的。特别注意的是，整个编译过程，都是用普通用户操作，不要用`root`用户操作。

首先要安装编译所需要的软件包:
```sh
sudo apt-get install build-essential flex gawk gettext git-core libncurses5-dev libssl-dev subversion unzip zlib1g-dev
```

下载源码:
```sh
git clone https://github.com/x-wrt/x-wrt.git
cd x-wrt
./scripts/feeds update -a
./scripts/feeds install -a
```

配置固件的命令`make menuconfig` 但是我们可以从配置模版开始会更轻松一些。

比如ar71xx-generic的设备可以用拷贝这个模版`feeds/ptpt52/rom/lede/config.ar71xx-generic`
```sh
cp feeds/ptpt52/rom/lede/config.ar71xx-generic .config
```

还有更多配置模版，请参考目录下的`config.*`文件:
```
feeds/ptpt52/rom/lede/config.ar71xx-generic
feeds/ptpt52/rom/lede/config.ar71xx-generic-nosymbol
feeds/ptpt52/rom/lede/config.ar71xx-nand
feeds/ptpt52/rom/lede/config.ar71xx-nand-nosymbol
feeds/ptpt52/rom/lede/config.ar71xx-tiny
feeds/ptpt52/rom/lede/config.ath79-generic
feeds/ptpt52/rom/lede/config.ath79-generic-nosymbol
feeds/ptpt52/rom/lede/config.bcm53xx-generic
feeds/ptpt52/rom/lede/config.ipq40xx-generic
feeds/ptpt52/rom/lede/config.ipq806x-generic
feeds/ptpt52/rom/lede/config.kirkwood-generic
feeds/ptpt52/rom/lede/config.mvebu-cortexa9
feeds/ptpt52/rom/lede/config.ramips-mt7620
feeds/ptpt52/rom/lede/config.ramips-mt7620-nosymbol
feeds/ptpt52/rom/lede/config.ramips-mt7621
feeds/ptpt52/rom/lede/config.ramips-mt76x8
feeds/ptpt52/rom/lede/config.ramips-mt76x8-nosymbol
feeds/ptpt52/rom/lede/config.ramips-rt3883-nosymbol
feeds/ptpt52/rom/lede/config.sunxi-cortexa7
feeds/ptpt52/rom/lede/config.x86_64
feeds/ptpt52/rom/lede/config.x86_generic
```

## 2. 配置目标
在模版配置文件的基础上，执行`make menuconfig`命令进行个性化定制，增删应用。

首先，在`Target Profile`菜单里面选择自己的目标设备，比如`Phicomm K2T`
![](./build-target.png)

然后，在定位到各个子菜单，选择对应的软件包
![](./build-m.png)

## 3. 执行编译
命令:
```sh
make
```
或者
```sh
make -j1 V=s
```

生成的包在`bin/targets/`下面
