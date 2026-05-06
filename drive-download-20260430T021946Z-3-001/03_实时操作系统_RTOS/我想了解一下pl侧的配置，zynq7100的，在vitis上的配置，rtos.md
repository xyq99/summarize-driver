在 Zynq-7000 系列（如 Zynq-7100）的开发中，PL（可编程逻辑）侧的配置与 PS（处理器系统）的 RTOS 应用程序紧密相连。在 Vitis 环境下，这种协作通常通过 **Hardware Platform (XSA)** 来实现。

以下是将 PL 配置集成到 Vitis RTOS 开发中的核心流程和关键点：

## 1. 硬件描述文件 (XSA) 的角色

在 Vitis 中，一切 PL 的信息都源自 Vivado 生成的 .xsa 文件。对于 Zynq-7100 这种高性能器件，PL 侧通常包含复杂的 IP 核（如 FFT、Video Pipeline 或自定义加速器）。

- **地址映射 (Address Map)：** RTOS 需要知道 PL 寄存器在 CPU 存储空间中的基地址。

- **中断信号 (Interrupts)：** PL 的中断必须连接到 PS 的 **GIC (Generic Interrupt Controller)**，并在 RTOS 中注册。

- **驱动程序：** Vitis 会根据 XSA 自动生成外设的 **Layer 0 (Standalone)** 驱动，RTOS 通常会包装这些驱动。

## 2. Vitis 中的 RTOS 配置流程

### A. 创建 Platform Project

1.  **导入 XSA：** 在 Vitis 中新建 Platform Project，指向你的 Vivado 导出文件。

2.  **选择 OS：** 在 Domain 设置中，选择你的 RTOS（如 **FreeRTOS**）。如果是第三方 RTOS（如 RT-Thread 或 VxWorks），需要预先安装对应的 Repo。

3.  **BSP 生成：** Vitis 会自动根据 PL 侧的 IP 生成对应的 BSP (Board Support Package)。

### B. 配置 PL 寄存器访问

在 RTOS 中访问 PL，通常采用 **Memory Mapped I/O (MMIO)**。

- 使用 xil_io.h 中的函数（如 Xil_In32 和 Xil_Out32）。

- **注意：** 如果 RTOS 启用了 **MMU (Memory Management Unit)**，你需要确保 PL 的地址段在页表中被映射为 "Device Memory" 或 "Non-cacheable"。

## 3. 关键配置：中断处理

在 RTOS 环境下，处理 PL 传来的中断是核心任务。

- **ID 确认：** 查阅 xparameters.h 找到 PL 中断在 GIC 上的 ID 号。

- **ISR 注册：** \* 在 FreeRTOS 中，使用 XScuGic_Connect 绑定中断服务例程 (ISR)。

  - 使用 XScuGic_Enable 开启通道。

- **上下文切换：** 确保 ISR 符合 RTOS 规范（例如在 FreeRTOS 中使用 FromISR 结尾的 API）。

## 4. PL 侧的比特流加载 (Bitstream)

对于 Zynq-7100，PL 的加载通常有几种方式：

| **方式**        | **场景** | **说明**                                                   |
|-----------------|----------|------------------------------------------------------------|
| **FSBL 加载**   | 生产环境 | 在启动阶段由 First Stage Bootloader 直接将 PL 比特流刷入。 |
| **Vitis Debug** | 开发调试 | 在运行 RTOS 调试前，Vitis 自动通过 JTAG 下载 .bit 文件。   |
| **运行时重构**  | 动态需求 | 通过 RTOS 调用 DevCfg 驱动，在系统运行时更新 PL 功能。     |

## 5. 开发建议

- **缓存一致性 (Coherency)：** 如果你的 PL 侧有 DMA 往 DDR 写数据，而 RTOS 在读数据，务必处理 **Cache Flush/Invalidate**，或者使用 ACP 接口。

- **资源分布：** Zynq-7100 拥有极大的 PL 资源（约 444K Logic Cells），如果 RTOS 负载较重，建议将耗时算法完全硬化在 PL 侧，仅通过中断通知 RTOS 结果。

你目前使用的是哪款具体的 RTOS（例如 FreeRTOS 还是 RT-Thread）？我可以针对该系统的中断注册代码给你提供更详细的模板。
