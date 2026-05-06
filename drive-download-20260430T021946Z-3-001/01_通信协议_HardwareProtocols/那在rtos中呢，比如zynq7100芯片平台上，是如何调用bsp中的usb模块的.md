在 Zynq-7100 这种基于 SoC 的平台上，USB 模块通常是通过 **PS (Processing System)** 侧的 USB 控制器实现的（Zynq-7000 系列通常集成了两个 USB 2.0 OTG 控制器）。

在 RTOS 环境（如 FreeRTOS、RT-Thread 或 vxWorks）中，调用 BSP 中的 USB 模块通常遵循一套从硬件初始化到协议栈挂载的层次化流程。

## 1. 硬件抽象层与驱动层 (Low-Level Driver)

在 Zynq-7100 上，Xilinx 官方通常提供 **Standalone (Baremetal)** 驱动，这是 RTOS 中 BSP 的核心。

- **驱动库:** 通常使用 xusbps 库。

- **初始化:** 调用 XUsbPs_CfgInitialize()。你需要向其传递控制器的基地址（如 XPAR_PS7_USB_0_BASEADDR）和设备 ID。

- **端点配置:** 通过 XUsbPs_DeviceConfig 结构体配置端点（Endpoints），包括端点号、传输类型（Bulk, Interrupt, Control）和缓冲区大小。

## 2. RTOS 协议栈的适配 (Stack Integration)

由于 USB 协议极其复杂，你很少直接操作寄存器，而是通过 RTOS 提供的 **USB Stack**。

### 常见的调用逻辑：

1.  **BSP 注册:** RTOS 的 USB 框架会定义一个标准的接口结构体（Ops）。你需要将 Xilinx 的 xusbps 函数封装进去。

2.  **中断绑定:** 必须在 RTOS 中挂接 USB 中断。  
    // 伪代码示例：在 Zynq 中断控制器注册 USB 中断  
    XScuGic_Connect(&IntcInstance, USB_INT_ID, (Xilinx_InterruptHandler)XUsbPs_IntrHandler, &UsbInstance);

3.  **模式声明:** 在 xparameters.h 或配置文件中，指明该 USB 控制器是作为 **Host** (主机) 还是 **Device** (外设) 运行。

## 3. Zynq-7100 的特殊考虑：DMA 与内存

Zynq 的 USB 控制器自带 **DMA 引擎**，在 RTOS 中调用时，必须处理好 **Cache 一致性**：

- **非缓存内存:** 通常为 USB 的传输描述符（DQH, DTD）分配一段 uncached 的内存区域。

- **Cache Flush/Invalidate:** 在发送数据前，需要 Xil_DCacheFlushRange()；在接收数据后，需要 Xil_DCacheInvalidateRange()。如果忽视这一点，在 Zynq 这种带二级缓存的 ARM Cortex-A9 架构上会出现严重的数据损坏。

## 4. 具体的调用链路 (以 Device 模式为例)

如果你在 Zynq-7100 上实现一个 USB 虚拟串口 (CDC) 或 U 盘 (MSC)：

| 层次           | 关键动作                       | 涉及文件/模块                  |
|----------------|--------------------------------|--------------------------------|
| **应用层**     | write() 或 read() 数据         | app.c                          |
| **类驱动层**   | 封装成 CDC 或 MSC 协议包       | usb_cdc.c                      |
| **协议栈层**   | 管理枚举、标准请求、端点分配   | usb_stack.c                    |
| **BSP/HCD 层** | **操作 Zynq 寄存器、启动 DMA** | xusbps_hw.c, xusbps_endpoint.c |
| **硬件层**     | ULPI 接口与外部 PHY 通信       | Zynq PS USB Controller         |

## 5. 常见痛点：ULPI 与 PHY

Zynq-7100 内部没有内置高速 PHY，通常需要外部通过 **ULPI 接口** 接一颗 PHY 芯片（如 USB3320）。

- **Reset 信号:** 在 BSP 初始化时，务必检查是否通过 GPIO 正确复位了外部 PHY 芯片。

- **时钟:** 确保 PS 端的 I/O 时钟配置正确（通常是 60MHz 由 PHY 提供给 Zynq）。

你在 Zynq-7100 上是打算将其配置为主机接 U 盘，还是作为从机模拟一个设备？
