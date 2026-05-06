针对 **16 MB NorFlash** 极度受限的存储环境，U-Boot 的裁剪目标只有一个：**极致的小体积与飞快的引导速度**。在这种场景下，U-Boot 不再是一个全功能的“嵌入式操作系统”，而是一个精密的“内核装载器”。

以下是实现这一方案的核心路径：

## 1. 物理尺寸“大瘦身”：Kconfig 深度精简

要让 U-Boot 运行在 16 MB 的 Flash 上（甚至可能需要腾出 12 MB 给内核和根文件系统），必须关掉一切非必要功能。

- **关闭所有交互式命令：** 生产环境不需要 CONFIG_CMDLINE。关闭后，U-Boot 将不再进入控制台，直接执行 CONFIG_BOOTCOMMAND，这能节省约 **100 KB+** 的体积。

- **精简驱动支持：**

  - 关闭 USB、网络协议栈（CONFIG_NET）、文件系统（CONFIG_FS_EXT4, CONFIG_FS_FAT）。

  - 对于 NorFlash，仅保留 CONFIG_MTD 和 CONFIG_SPI_FLASH。

- **禁用不必要的输出：** 关闭 CONFIG_CONSOLE_RECORD 和 CONFIG_LOG。甚至可以开启 CONFIG_SILENT_CONSOLE，这不仅减小体积，还能减少串口 I/O 带来的毫秒级延迟。

## 2. 启动流程优化：实现“秒开”引导

在 NorFlash 环境中，读取速度是瓶颈。

- **执行位置优化：** 尽可能使用 **XIP (Execute In Place)**。NorFlash 支持芯片内执行，如果硬件允许，直接在 Flash 上运行 U-Boot 代码，无需将其搬移到 RAM，这样可以省去搬移的时间。

- **加速 SPI 读取：**

  - 开启 **Quad SPI (QSPI)** 模式（如果硬件支持），从 1-bit 模式切换到 4-bit 模式。

  - 调高 CONFIG_SF_DEFAULT_SPEED（例如提升至 50MHz 或 100MHz）。

- **跳过不必要的初始化：** 在 board_init_f 中屏蔽掉对当前场景无用的硬件检测（如内存测试、不使用的外设时钟配置）。

## 3. 核心初始化方案：只保留“救命”代码

针对核心初始化与内核引导，代码逻辑应精简为以下链路：

1.  **CPU/时钟初始化：** 设置最基本的 CPU 频率和 DDR 控制器。

2.  **DDR 训练 (DDR Training)：** 确保内存可用（如果 bootrom 没做的话）。

3.  **Flash 控制器初始化：** 仅为了读取内核镜像。

4.  **内核引导：** 直接跳转到 bootm 或 bootz 逻辑。

> **高级技巧：Falcon Mode (猎鹰模式)**
>
> 如果 16 MB 依然局促，或者启动速度仍达不到要求，可以开启 **Falcon Mode**。这允许 U-Boot SPL 直接加载 Linux 内核，完全跳过体积巨大的 U-Boot 全功能镜像（u-boot.bin）。此时，SPL 负责初始化 DDR 并直接把内核搬到 RAM 执行，启动时间通常能压缩在 **500ms** 以内。

## 4. 存储布局规划 (Layout)

在 16 MB 空间内，建议的典型布局如下：

| **偏移地址** | **内容**          | **建议大小** | **备注**           |
|--------------|-------------------|--------------|--------------------|
| 0x000000     | SPL / U-Boot      | 256 KB       | 越小越好           |
| 0x040000     | DTB (Device Tree) | 64 KB        | 内核使用的设备树   |
| 0x050000     | U-Boot Env        | 64 KB        | 环境变量，可压缩   |
| 0x060000     | Kernel (zImage)   | 4 - 8 MB     | 取决于内核裁剪程度 |
| 0x860000     | Rootfs (SquashFS) | 剩余空间     | 只读压缩文件系统   |

## 5. 调试与量化

- **体积监控：** 使用 arm-linux-gnueabi-nm --size-sort u-boot 查找占用空间最大的符号，针对性优化代码。

- **时间统计：** 在代码中插入 get_timer(0) 打印关键节点的时间戳（Bootstage），精确定位耗时严重的初始化函数。

### 专家经验分享

在 NorFlash 环境下，**压缩比** 往往比 **解压速度** 更关键。对于内核镜像，虽然 LZ4 解压快，但在 16 MB 的狭窄空间里，使用压缩率更高的 XZ 或 GZIP 可能因为减少了从 Flash 读取的数据量，反而让总启动时间更短。

你目前在这个 16 MB 的环境中，U-Boot 镜像最终控制到了多大？是否有开启 **Falcon Mode** 的计划来追求极限速度？
