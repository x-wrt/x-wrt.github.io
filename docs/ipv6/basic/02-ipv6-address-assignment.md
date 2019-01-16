# IPv6基础: IPv6 地址分配

## 1. 介绍
IPv6地址分配采用了自动配置和DHCP的方式, 使得IPv6地址配置容易了不少(相比与IPv4)
## 2. 地址分配

### 2.1 静态获取
类似IPv4的静态IP, 手动设置
### 2.2 无状态地址自动配置(SLAAC)
+ SLAAC: statless address auto configuration;
+ 原理: 前缀可以通过主机本身或者路由器分配, 接口ID通过EUI-64方式生成,通过邻居节点请求消息广播该地值是否为是否唯一.
+ 过程:
    1. 主机接入网络后发送路由请求消息(Router Solicitation);
    2. 路由器收到请求后,会发送路由通告消息(Router Advertisement)
    3. 主机获取到RA消息后, 可以获取到:
       + 默认网关(即系路由器的默认本地链路地址)
       + 地址前缀
    4. 根据EUI-64生成接口ID
+ 缺点:
    + 不能给节点配置更多信息(如DNS)
+ 应用场景: ...
### 2.3 有状态地址自动配置(DHCPv6)
依赖于DHCPv6服务, 分为: 有状态IPv6和无状态IPv6, 依赖路由通告消息(RA)数据包的`M`和`O`状态位
+ [无状态DHCP(stateless)](#)
标签O: `1`
仅分配基本配置参数(), 接口ID还是自己生成的, 可以理解为SLAAC + DHCPv6, 使用SLAAC方式配置地址, DHCPv6获取其他配置. 这样的DHCP方式无需要管理IP租约lease, 所以成为无状态<br>
+ [有状态DHCPv6(stateful)](#)
类似IPv4的DHCP, 由路由器来分配IPv6地址和配置参数
标签M: `1` 
过程:
  1. 主机接入网络后发送路由请求消息(Router Solicitation);
  2. 路由器收到请求后,会发送路由通告消息(Router Advertisement), 状态位M设置为`1`
  3. 主机获取到RA消息后, 由于M=1, 会使用DHCPv6协议获取IPv6地址和其他配置信息.
  4. 路由器收到DHCPv6请求后会分配一个地址个主机






