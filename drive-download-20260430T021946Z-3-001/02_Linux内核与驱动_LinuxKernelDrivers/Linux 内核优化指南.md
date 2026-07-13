优化 Linux 5.10 内核是一项精细活，核心逻辑在于\*\*“按需分配”\*\*。要实现体积瘦身和启动优化，你需要从配置（Kconfig）、编译策略以及初始化流程三个维度入手。

以下是实现这一目标的实操指南：

## 1. 硬件资源审计：明确“删减清单”

在动手改 Kconfig 之前，必须摸清硬件底细，避免误删关键驱动导致无法开机。

- **查看当前驱动使用情况：** lsmod（查看已加载模块）和 lspci / lsusb（查看物理设备）。

- **自动缩减配置：** 在目标机器上运行 make localmodconfig。它会根据当前系统加载的驱动自动精简 .config，这是最稳健的起点。

## 2. Kconfig 深度定制：实现内核“瘦身”

进入 make menuconfig 界面，针对性关闭不必要的功能。

### A. 基础功能剥离

- **General setup:** \* 关闭 CONFIG_SWAP（如果内存充足或使用嵌入式存储）。

  - 关闭 CONFIG_SYSVIPC 和 CONFIG_POSIX_MQUEUE（若应用层不需要）。

  - 精简 CONFIG_EXPERT 模式下的选项。

- **Kernel hacking:** 生产环境关闭所有 DEBUG\_\* 选项，这能显著减小内核镜像体积并提升速度。

### B. 驱动与协议栈优化

- **Networking support:** 仅保留必要的协议。关闭 IP_MULTICAST、INET_DIAG 以及各种不常用的协议（如 Appletalk, IPX）。

- **Device Drivers:** 这是“大头”。

  - 删除所有不匹配的显卡、声卡、网卡驱动。

  - 关闭 CONFIG_DRM（如果是无头服务器或串口输出嵌入式设备）。

- **File systems:** 只保留 EXT4 或 SquashFS（针对固件），关闭不常用的 NTFS, CIFS, NFS 等。

## 3. 启动速度优化：毫秒必争

内核启动慢通常卡在驱动初始化和 I/O 等待上。

### A. 编译策略优化

- **内建 vs 模块：** 核心启动路径上的驱动（如磁盘控制器、文件系统、串口）建议**内建（Y）**，非核心驱动（如 WiFi）设为\*\*模块（M）\*\*以延迟加载。

- **压缩算法：** 权衡解压时间和加载时间。

  - CONFIG_KERNEL_LZO 或 CONFIG_KERNEL_LZ4：解压速度最快，启动延迟低。

  - CONFIG_KERNEL_XZ：压缩率最高，体积最小，但解压耗时。

### B. 内核参数微调

通过 GRUB 或 U-Boot 传递启动参数：

- quiet：禁用大部分打印，减少串口 I/O 耗时。

- lpj=\<value\>：预设 loops_per_jiffy，省去内核启动时的延迟校准（需先从 dmesg 获取该值）。

## 4. 编译与体积验证

使用以下命令进行编译并监控体积：

> Bash

\# 使用多核编译\
make -j\$(nproc) bzImage modules\
\
\# 检查内核镜像体积\
ls -lh arch/x86/boot/bzImage \# 或 arch/arm/boot/zImage

### 进一步瘦身工具：Scripts/bloat-o-meter

内核源码自带了 scripts/bloat-o-meter，可以对比两个不同配置编译出的二进制文件大小差异，帮助你精准定位是哪个函数或模块占据了空间。

## 5. 核心指标监控

优化后的验证指标主要看两点：

1.  **Storage Footprint:** vmlinuz 的字节数。

2.  **Boot Time:** 使用 systemd-analyze 或通过串口抓取 dmesg 中的时间戳：\[ 0.000000\] Linux version 5.10.x ...\
    \[ 1.234567\] Freeing unused kernel image memory...（此行代表内核初始化完成）

### 进阶提示

如果你在做嵌入式定制，建议关注 **Initial Ramdisk (initrd)** 的瘦身，甚至直接去掉 initrd，让内核直接挂载 rootfs。另外，使用 LTO (Link Time Optimization) 编译选项（5.10 内核已较好支持）可以进一步通过跨模块优化减少冗余代码。

你目前的优化目标是针对特定的嵌入式硬件，还是通用的服务器环境？
