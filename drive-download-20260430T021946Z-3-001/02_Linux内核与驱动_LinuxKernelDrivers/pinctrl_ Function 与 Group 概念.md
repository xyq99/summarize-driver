在 Linux 内核的 **pinctrl (Pin Control)** 子系统中，functions（功能）和 groups（组）是实现引脚复用（Muxing）的核心概念。

简单来说：**Function 是“你想让引脚干什么”，而 Group 是“哪些具体的物理引脚在干这件事”。**

## 1. 为什么需要 Groups？

在现代 SoC（片上系统）中，一个功能（比如 UART1）通常需要一组引脚才能工作（TX、RX、或者还有 RTS、CTS）。

- **硬件物理限制：** 芯片设计时，UART1 的 TX 可能只能在 Pin A 或 Pin E 上选；RX 可能只能在 Pin B 或 Pin F 上选。

- **组合的固定性：** 厂家通常会定义好几套“方案”。比如：

  - **方案 A (Group 1):** 使用 Pin A 和 Pin B 组成 UART1。

  - **方案 B (Group 2):** 使用 Pin E 和 Pin F 组成 UART1。

**Group 的本质就是：一组物理引脚的集合，它们作为一个整体被映射到某个 Function 上。**

## 2. Functions 与 Groups 的映射关系

它们之间通常是 **“多对多”** 的映射逻辑，但具体到某一次配置，是**一对一**的。

### 逻辑模型

- **Function (功能):** UART、I2C、SPI、SDIO 等。

- **Group (引脚组):** \* uart1_grp_a: {GPIO1, GPIO2}

  - uart1_grp_b: {GPIO10, GPIO11}

  - i2c1_grp: {GPIO3, GPIO4}

### 实际配置示例

如果你想启用 UART1，pinctrl 驱动会问你：“你要用哪组引脚？”

你选择 Function: UART1 + Group: uart1_grp_a。此时，GPIO1 和 GPIO2 就会被切换到 UART 模式。

## 3. 设计理念：抽象与解耦

区分这两个概念的设计理念主要是为了**灵活性**和**复用性**：

### A. 解决“引脚冲突”

由于 Function 和 Group 是分开的，内核可以很容易检测冲突。例如：

- 如果 UART1 使用了 Group A（含 GPIO1）。

- 此时你又想启动 SPI1，而 SPI1 的引脚组也包含了 GPIO1。

- pinctrl 系统会在底层直接报错，防止两个功能争抢同一个物理引脚。

### B. 适应不同的封装

同一个 SoC 可能会有不同的封装（如 BGA 或 QFP）。在 BGA 封装里，UART1 可能连接在 Pin A/B；而在引脚较少的 QFP 封装里，它可能被移到了 Pin E/F。

通过定义不同的 Groups，驱动程序代码可以保持不变，只需要在设备树（DTS）里切换 Group 即可。

## 4. 在设备树 (DTS) 中的体现

在实际开发中，你经常会看到类似这样的结构：

> 代码段

uart1_pins: uart1-pins {\
pinmux {\
/\* 这里就是将 function 和 group 绑定在一起 \*/\
function = "uart1";\
groups = "uart1_grp_a";\
};\
/\* 顺便配置电气属性，如上拉、驱动能力等 \*/\
conf {\
pins = "gpio1", "gpio2";\
bias-pull-up;\
};\
};

## 5. 总结

|              |                               |                          |
|--------------|-------------------------------|--------------------------|
| **概念**     | **关注点**                    | **例子**                 |
| **Function** | **逻辑功能** (做什么？)       | UART, I2C, PWM           |
| **Group**    | **物理路径** (用哪几根线做？) | pin_group_0, pin_group_1 |

**一句话总结：** Function 决定了芯片内部的信号源，Group 决定了这些信号最终通过芯片表面的哪些“脚”走出去。

你想看看在具体的 Linux 驱动代码（比如 pinctrl-mtk.c 或 pinctrl-imx.c）中，这些结构体是如何初始化的吗？
