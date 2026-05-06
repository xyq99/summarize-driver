# lwIP 2.1.1 API 接口分析文档

本文档对 `lwip-2.1.1\src\api` 目录下的核心源码接口进行了分析和汇总。

## 目录结构
- [api_lib.c](#api_libc) - Sequential API 外部接口 (Netconn)
- [api_msg.c](#api_msgc) - Sequential API 内部消息处理
- [err.c](#errc) - 错误管理模块
- [if_api.c](#if_apic) - 接口标识 API (RFC 3493)
- [netbuf.c](#netbufc) - 网络缓冲区管理
- [netdb.c](#netdbc) - 域名解析 API
- [netifapi.c](#netifapic) - 网络接口顺序 API (线程安全)
- [sockets.c](#socketsc) - BSD 套接字 (Sockets) 兼容层
- [tcpip.c](#tcpipc) - TCPIP 主线程模块

---

<a name="api_libc"></a>
## 1. api_lib.c (Netconn API 外部模块)
该文件实现了 Netconn API 的客户端侧接口，供应用层线程调用。它是线程安全的，内部通过消息传递与 TCPIP 核心线程通信。

### 核心 API 列表
- `netconn_new_with_proto_and_callback`: 创建一个指定类型的新连接。
- `netconn_delete`: 释放连接及其占用的所有资源。
- `netconn_getaddr`: 获取连接的本地或远程 IP 地址及端口。
- `netconn_bind`: 将连接绑定到本地 IP 地址和端口。
- `netconn_bind_if`: 将连接绑定到指定的网络接口索引。
- `netconn_connect`: 连接到远程主机。
- `netconn_disconnect`: 断开 UDP 连接。
- `netconn_listen_with_backlog`: 进入监听模式（仅限 TCP）。
- `netconn_accept`: 接受新的 TCP 连接。
- `netconn_recv`: 接收数据（返回 `netbuf`）。
- `netconn_send`: 发送 UDP/RAW 数据。
- `netconn_write_partly`: 发送 TCP 数据（支持部分写入）。
- `netconn_close`: 关闭 TCP 连接（不释放 netconn 结构）。
- `netconn_shutdown`: 关闭连接的读、写或双端。
- `netconn_gethostbyname`: 执行 DNS 域名解析。

---

<a name="api_msgc"></a>
## 2. api_msg.c (Sequential API 内部模块)
该文件负责在 TCPIP 线程上下文中处理来自 `api_lib.c` 的请求。它直接与 lwIP 协议栈核心（如 `tcp.c`, `udp.c`）交互。

### 关键内部接口
- `lwip_netconn_do_newconn`: 实际执行 PCB（协议控制块）的分配。
- `lwip_netconn_do_bind`: 实际执行协议栈的绑定操作。
- `lwip_netconn_do_connect`: 实际启动 TCP 三次握手或 UDP 连接。
- `lwip_netconn_do_write`: 将数据排入 TCP 发送队列。
- `lwip_netconn_do_close`: 执行 TCP 关闭流程。
- `netconn_alloc`: 分配 `struct netconn` 内存。
- `netconn_free`: 释放 `struct netconn` 内存。

---

<a name="errc"></a>
## 3. err.c (错误管理)
提供 lwIP 内部错误码 (`err_t`) 与标准错误码或字符串之间的转换。

### API 列表
- `err_to_errno`: 将 `err_t` 映射为 POSIX 标准的 `errno` (如 `ENOMEM`, `EWOULDBLOCK`)。
- `lwip_strerr`: 返回错误码对应的可读字符串说明。

---

<a name="if_apic"></a>
## 4. if_api.c (接口标识 API)
实现 RFC 3493 定义的标准接口，用于网卡索引与名称之间的转换。

### API 列表
- `lwip_if_indextoname`: 将接口索引转换为接口名称（如 "en1"）。
- `lwip_if_nametoindex`: 将接口名称转换为接口索引。

---

<a name="netbufc"></a>
## 5. netbuf.c (网络缓冲区管理)
`netbuf` 是对 lwIP 内部 `pbuf` 的封装，主要用于 Netconn API 中的非拷贝数据传输。

### API 列表
- `netbuf_new`: 分配新的 netbuf 结构。
- `netbuf_delete`: 释放 netbuf 及其包含的 pbuf。
- `netbuf_alloc`: 为 netbuf 分配指定大小的内存。
- `netbuf_ref`: 让 netbuf 引用外部静态数据（不拷贝）。
- `netbuf_chain`: 将两个 netbuf 链连接在一起。
- `netbuf_data`: 获取当前 netbuf 片段的数据指针和长度。
- `netbuf_next`: 移动到 pbuf 链中的下一个片段。
- `netbuf_first`: 回到 pbuf 链的起始位置。

---

<a name="netdbc"></a>
## 6. netdb.c (域名解析 API)
实现标准的 POSIX DNS 查询接口。

### API 列表
- `lwip_gethostbyname`: 根据域名获取主机信息（非线程安全）。
- `lwip_gethostbyname_r`: 线程安全的域名解析接口。
- `lwip_getaddrinfo`: 通用的地址解析接口（支持 IPv4/IPv6）。
- `lwip_freeaddrinfo`: 释放由 `getaddrinfo` 分配的内存。

---

<a name="netifapic"></a>
## 7. netifapi.c (网络接口顺序 API)
提供线程安全的方法来配置和管理网络接口（`netif`），避免在非 TCPIP 线程中直接操作核心数据结构。

### API 列表
- `netifapi_netif_add`: 线程安全地添加一个网卡。
- `netifapi_netif_set_addr`: 线程安全地设置网卡 IP 地址。
- `netifapi_netif_common`: 调用通用的网卡操作函数（如 `netif_set_up`, `netif_set_link_up`）。
- `netifapi_arp_add`: 静态添加 ARP 条目。

---

<a name="socketsc"></a>
## 8. sockets.c (BSD 套接字兼容层)
这是应用层最常用的接口层，将标准的 BSD Socket 调用映射到 Netconn API。

### 核心 API 列表
- `lwip_socket`: 创建套接字。
- `lwip_bind`: 绑定地址。
- `lwip_listen`: 开启监听。
- `lwip_accept`: 接收连接。
- `lwip_connect`: 发起连接。
- `lwip_send / lwip_sendto`: 发送数据。
- `lwip_recv / lwip_recvfrom`: 接收数据。
- `lwip_setsockopt / lwip_getsockopt`: 设置/获取套接字选项（如超时、缓冲区大小、组播等）。
- `lwip_select / lwip_poll`: I/O 多路复用。
- `lwip_close`: 关闭套接字。

---

<a name="tcpipc"></a>
## 9. tcpip.c (TCPIP 主线程)
该文件管理 lwIP 的核心线程，负责任务调度、消息分发和定时器处理。

### API 列表
- `tcpip_init`: 初始化协议栈并启动 TCPIP 线程。
- `tcpip_input`: 将底层收到的数据包递交给 TCPIP 线程处理。
- `tcpip_callback`: 在 TCPIP 线程上下文中异步执行一个函数。
- `tcpip_api_call`: 同步调用一个函数并等待结果。
- `tcpip_timeout`: 在 TCPIP 线程中注册一个一次性定时器。
