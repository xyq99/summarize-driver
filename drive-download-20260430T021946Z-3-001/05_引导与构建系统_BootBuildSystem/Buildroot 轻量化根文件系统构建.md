构建轻量化根文件系统（Rootfs）是嵌入式开发的终极“剪裁艺术”。相比于臃肿的 Ubuntu 或 Debian，Buildroot 能够让你在几分钟内生成一个从几 MB 到几十 MB 不等的精简系统。

要在 **SD 卡**、**eMMC** 以及 **海量存储设备**上实现完美适配，你需要掌握从构建逻辑到分区布局的全套流程。

## 1. Buildroot 核心配置逻辑

构建轻量化系统的第一步是在 make menuconfig 中进行“断舍离”：

- **Target Options:** 选对 CPU 架构（如 Cortex-A55）和浮点运算单元（VFPv4），确保二进制文件执行效率最高。

- **Toolchain:** 建议使用 External toolchain（如 Linaro 或 Arm 官方提供的），可以节省大量编译时间。

- **System configuration:** \* **Init system:** 追求极致速度选 BusyBox；需要现代化管理选 systemd。

  - **/dev management:** 建议选 Dynamic using devtmpfs + mdev，足以应对大多数嵌入式场景。

- **Target packages:** 核心准则——**不用的不选**。仅保留必要的工具（如 dropbear 代替 openssh 以减小体积）。

## 2. 存储介质适配：分区与映像生成

适配不同存储介质的关键在于 genimage.cfg 的编写，它决定了最终生成的 .img 文件结构。

### A. SD 卡与 eMMC 的适配

两者在逻辑上相似（均走 MMC 协议），但 eMMC 通常有专用的 boot 分区。

- **分区策略：** 建立 boot (FAT32, 存放 Kernel/DTS) 和 rootfs (EXT4) 双分区。

- **genimage 配置示例：**

> Plaintext

image sdcard.img {  
hdimage {}  
partition u-boot {  
in-partition-table = "no"  
image = "u-boot-sunxi-with-spl.bin"  
offset = 8K  
}  
partition boot {  
partition-type = 0xC  
bootable = "true"  
image = "boot.vfat"  
}  
partition rootfs {  
partition-type = 0x83  
image = "rootfs.ext4"  
}  
}

### B. 海量存储设备（USB/SATA/NVMe）

针对 SSD 或大容量存储，重点在于内核驱动的支持：

- **Kernel Config:** 必须内建 CONFIG_BLK_DEV_SD 和对应的控制器驱动（如 CONFIG_SATA_AHCI）。

- **挂载优化：** 在 /etc/fstab 中使用 UUID 或 PARTUUID 挂载，防止插拔多个设备时设备号（sda/sdb）漂移导致无法启动。

## 3. 根文件系统“瘦身”进阶

如果你的 Flash 空间极其有限（例如只有 16MB 或 32MB），可以尝试以下操作：

- **使用 SquashFS：** 这是一个只读的压缩文件系统，压缩比极高，非常适合固件发布。

- **去除符号表：** 在 Build options 中开启 strip 功能，丢弃二进制文件中的调试信息。

- **清理 Rootfs Overlays：** 通过 post-build.sh 脚本在打包前自动删除 /usr/share/man、/usr/share/doc 等无用目录。

## 4. 自动化构建与部署

为了提高生产效率，通常会利用 Buildroot 的 **External Tree (BR2_EXTERNAL)** 功能：

1.  **解耦配置：** 将项目特有的配置、补丁和脚本放在主源码目录之外，方便版本控制。

2.  **一键烧录：** 配合 dd 命令或瑞芯微、TI 的专用烧录工具（如 upgrade_tool），将生成的 output/images/ 下的镜像同步到目标板。

### 实战思考

在适配 **eMMC** 时，为了延长 Flash 寿命，你是否考虑过将 /var/log 和 /tmp 挂载为 tmpfs（内存文件系统）？此外，针对 **A/B 分区升级**（双系统备份）的需求，你在 Buildroot 中是如何规划分区表冗余的？
