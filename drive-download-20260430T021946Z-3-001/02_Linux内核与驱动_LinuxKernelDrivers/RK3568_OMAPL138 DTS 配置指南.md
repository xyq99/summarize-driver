在 RK3568（瑞芯微）和 OMAPL138（TI）这两个平台上进行 DTS 开发，本质上是处理两种完全不同的 SoC 架构逻辑：一个是现代的 64 位多核 ARM 架构，拥有成熟的 Pinctrl 子系统；另一个是较老但经典的 ARM9 + DSP 异构架构，其引脚多路复用（Muxing）逻辑更为底层。

要精通这两个平台的配置，建议从以下四个维度深度掌握：

## 1. 引脚复用 (Pinctrl) 与 GPIO 配置

这是硬件调通的第一步，两者在逻辑上有显著区别。

- **RK3568 (Pinctrl 子系统)：**  
  瑞芯微使用功能强大的 Pinctrl 驱动。配置时需遵循 bank、pin、func 的逻辑。

  - **复用定义：** 在 pinctrl 节点下定义 rockchip,pins。

  - **示例：** 将 GPIO3_A5 配置为 PWM 功能。

> DTS  
> &pinctrl {  
> pwm1 {  
> pwm1m0_pins: pwm1m0-pins {  
> rockchip,pins = \<3 RK_PA5 4 &pcfg_pull_none\>; // 4 代表复用函数号  
> };  
> };  
> };

- **OMAPL138 (Pinmux 寄存器)：**  
  TI 平台通常使用 pinctrl-single 驱动，直接操作寄存器偏移量和掩码。你需要查阅 DataSheet 中的 PINMUX 寄存器映射表，计算物理偏移地址。

## 2. 中断触发与控制 (Interrupts)

中断配置决定了外设能否实时响应。

- **中断属性：** 必须明确 interrupt-parent（指向中断控制器，如 GIC 或 GPIO Bank）和 interrupts 单元。

- **触发方式：**

  - IRQ_TYPE_EDGE_RISING (1): 上升沿触发。

  - IRQ_TYPE_LEVEL_LOW (8): 低电平触发。

- **RK3568 技巧：** 注意 RK3568 的 GPIO 中断通常挂载在 gic 下，级联结构在 DTSI 中已定义好，开发者只需引用对应的 GPIO 节点并设置 interrupts = \<5 IRQ_TYPE_EDGE_FALLING\>。

## 3. DMA 通道分配

DMA（直接存储器访问）对于高速协议（如 SPI、UART、McASP）至关重要。

- **OMAPL138 (EDMA)：** TI 平台使用 EDMA3 控制器。在 DTS 中需要指定传输控制器（TC）和队列。

- **RK3568 (DMAC)：** 采用 ARM 标准的 PL330 DMA 控制器。

- **配置关键：**  
  DTS  
  uart1: serial@fe650000 {  
  dmas = \<&dmac0 2\>, \<&dmac0 3\>; // 指定 DMA 控制器及其请求线  
  dma-names = "tx", "rx";  
  };

## 4. 底层协议总线 (I2C/SPI/UART)

这是连接传感器和外设的“高速公路”。

- **时钟配置：** 确保 assigned-clocks 和 assigned-clock-rates 设置正确，尤其是在 RK3568 上，总线频率直接影响传输稳定性。

- **状态切换：** 谨记在 &i2c0 或 &spi1 中将 status = "okay";，否则驱动不会加载。

- **OMAPL138 特性：** 对于 McASP（多通道音频序列端口），需额外注意总线同步时钟和时隙（Slots）的配置。

## 5. 实战调试思路：从 DTS 到硬件

配置完 DTS 后，如何证明你的配置生效了？

1.  **验证引脚状态：**  
    使用 cat /sys/kernel/debug/pinctrl/pinctrl-devices 查看控制器，或 cat /sys/kernel/debug/gpio 查看 GPIO 被谁占用。

2.  **查看中断统计：**  
    cat /proc/interrupts。如果你的外设动作了但中断计数没增加，说明触发方式或引脚复用配置错误。

3.  **时钟树检查：**  
    cat /sys/kernel/debug/clk/clk_summary。检查外设时钟是否被正确使能，频率是否符合预期。

### 避坑指南

> **注意：** 在 RK3568 上，很多引脚是多功能的（例如同一个引脚可以是 GPIO、I2C 或 PWM）。**千万不要在 DTS 中同时使能两个使用相同引脚的外设**，否则会导致驱动加载失败或系统崩溃。

你在针对这两个平台做开发时，目前遇到最棘手的问题是 DMA 数据传输不稳，还是硬件初始化时的引脚电平冲突？
