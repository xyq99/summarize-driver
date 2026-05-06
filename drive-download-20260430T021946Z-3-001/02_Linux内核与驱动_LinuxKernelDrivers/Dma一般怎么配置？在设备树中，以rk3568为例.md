在 RK3568（以及大多数基于现代 Linux 内核的 ARM SoC）中，DMA 的配置主要分为两个部分：**DMA 控制器节点的定义**（通常由芯片厂商在 rk3568.dsi 中定义）和**外设对 DMA 通道的引用**（由开发者在自己的 .dts 中配置）。

配置核心逻辑遵循 Linux 的 dma-common 绑定规范。

### 1. DMA 控制器节点 (Controller)

在 rk3568.dtsi 中，你会看到类似 DMAC 的定义。RK3568 通常有多个 DMA 控制器（如 dmac0, dmac1），它们是硬件资源池。

dmac0: dma-controller@fe270000 {  
compatible = "arm,pl330", "arm,primecell";  
reg = \<0x0 0xfe270000 0x0 0x4000\>;  
interrupts = \<GIC_SPI 143 IRQ_TYPE_LEVEL_HIGH\>,  
\<GIC_SPI 144 IRQ_TYPE_LEVEL_HIGH\>;  
\#dma-cells = \<1\>; // 关键：决定了引用时需要多少个参数  
arm,pl330-broken-no-flushp;  
clocks = \<&cru ACLK_DMAC0\>;  
clock-names = "apb_pclk";  
};

### 2. 外设如何引用 DMA (Consumer)

当你需要在某个外设（如 UART, SPI, I2C, I2S）中开启 DMA 时，你需要在该外设节点下添加 dmas 和 dma-names 属性。

#### 示例：配置 UART1 使用 DMA

以 UART 为例，通常需要两个通道：一个用于发送 (tx)，一个用于接收 (rx)。

&uart1 {  
status = "okay";  
pinctrl-names = "default";  
pinctrl-0 = \<&uart1m0_xfer\>;  
  
/\* 配置 DMA \*/  
dmas = \<&dmac0 0\>, // 引用 dmac0，通道 ID 为 0 (TX)  
\<&dmac0 1\>; // 引用 dmac0，通道 ID 为 1 (RX)  
dma-names = "tx", "rx"; // 必须与驱动程序中申请的名称对应  
};

**参数解析：**

- **dmas**:

  - 第一个参数是 DMA 控制器的句柄（如 &dmac0）。

  - 第二个参数是 **DMA 请求信号线 (Request ID)**。这个 ID 必须查阅 RK3568 的 *Technical Reference Manual (TRM)* 中的 "DMA Request Map" 表。每个外设对应的 ID 是固定的。

- **dma-names**: 这是一个字符串列表，内核驱动会通过 dma_request_chan() 查找这些名称。对于标准 UART 驱动，通常就是 "tx" 和 "rx"。

### 3. 特殊配置：Reserved Memory (预留内存)

对于某些高性能外设（如摄像头 VIP/CSI 或特定显示模块），你可能需要为其分配一段**连续的物理内存 (CMA)**。

reserved-memory {  
\#address-cells = \<2\>;  
\#size-cells = \<2\>;  
ranges;  
  
dma_reserved: dma_mem_region {  
compatible = "shared-dma-pool";  
reusable;  
size = \<0x0 0x2000000\>; // 预留 32MB  
alloc-ranges = \<0x0 0x10000000 0x0 0x20000000\>; // 指定物理地址范围  
linux,cma-default; // 设为默认 CMA 区域  
};  
};  
  
&some_device {  
memory-region = \<&dma_reserved\>; // 将此前预留的内存分配给该设备  
};

### 4. 常见配置检查清单

1.  **驱动支持**：确保内核配置中开启了 CONFIG_DW_DMAC_ROCKCHIP 或 CONFIG_ARM_PL330（RK3568 主要使用 PL330 IP）。

2.  **ID 对应**：检查 dmas 属性里的 ID 是否和 TRM 手册中的物理连接一致。如果 ID 填错，DMA 无法触发中断。

3.  **对齐要求**：RK3568 的某些 DMA 传输对内存地址有对齐要求（如 4 字节对齐），这通常在驱动层处理，但调试时需注意。

### 总结

在 RK3568 设备树中配置 DMA，核心就是：**在控制器节点定义 \#dma-cells，在外设节点通过 dmas 引用控制器并指定硬件 Request ID。**

你目前是在为哪个具体的硬件接口（如 SPI 还是自定义 IP）配置 DMA？不同接口在驱动层的表现会有细微差别。
