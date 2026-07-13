好的，那我们深入到 Linux 内核的源码层级，看看驱动开发者是如何定义这两者的。

在 pinctrl 子系统中，最核心的结构体通常是 struct pinctrl_desc，它包含了指向 pinctrl_ops 和 pinmux_ops 的指针。而 functions 和 groups 就隐藏在这些操作接口的实现中。

### 1. 结构化定义：底层是怎么“存”的？

驱动工程师通常会定义两个静态数组，一个存物理引脚组，一个存逻辑功能。

#### 引脚组 (Groups) 的定义

每个 Group 本质上是 **“名字 + 引脚索引数组”**。

> C

/\* 定义具体的引脚编号 \*/\
static const unsigned int uart1_pins\[\] = { 10, 11 };\
static const unsigned int i2c1_pins\[\] = { 20, 21 };\
\
/\* 将这些引脚封装成 Groups \*/\
static const struct pingroup my_groups\[\] = {\
{ .name = "uart1_grp", .pins = uart1_pins, .npins = 2 },\
{ .name = "i2c1_grp", .pins = i2c1_pins, .npins = 2 },\
};

#### 功能 (Functions) 的定义

每个 Function 本质上是 **“名字 + 它支持哪些 Groups”**。

> C

/\* 定义一个功能支持哪些引脚组（一个功能可能有多种走线方案） \*/\
static const char \* const uart1_grps\[\] = { "uart1_grp", "uart1_alt_grp" };\
\
static const struct pinfunction my_functions\[\] = {\
{ .name = "uart1", .groups = uart1_grps, .ngroups = 2 },\
{ .name = "i2c1", .groups = { "i2c1_grp" }, .ngroups = 1 },\
};

### 2. 关键回调函数：内核是怎么“用”的？

当设备树（DTS）要求切换模式时，内核会调用 pinmux_ops 里的 set_mux 回调函数。这是最底层、最硬核的部分。

> C

static int my_pinctrl_set_mux(struct pinctrl_dev \*pctldev,\
unsigned int selector, // Function 的索引\
unsigned int group) // Group 的索引\
{\
/\* 1. 根据 selector 找到具体的功能（如 UART） \*/\
/\* 2. 根据 group 找到具体的物理引脚（如 Pin 10, 11） \*/\
\
/\* 3. 硬件操作：写入寄存器 \*/\
// 遍历该 Group 里的所有 pins，通过写 IOMUX 寄存器，\
// 将这些物理引脚的 MUX 模式切换到对应的 Function。\
\
for (i = 0; i \< grp-\>npins; i++) {\
unsigned int pin = grp-\>pins\[i\];\
write_register(MUX_REG(pin), MUX_MODE_UART);\
}\
\
return 0;\
}

### 3. 设计上的深度思考：为什么要分两层？

如果只用 pins（引脚）和 functions（功能），逻辑会变得非常混乱。引入 groups 后，实现了以下解耦：

- **原子性操作：** UART 必须同时拥有 TX 和 RX 才能工作。通过 groups，内核保证了你配置的是一个**完整的通信链路**，而不是零散的孤立引脚。

- **状态冲突检测：** pinctrl 核心层维护了一张巨大的表。当驱动 A 申请了 uart1_grp 时，核心层会自动锁定该组内所有的引脚。如果驱动 B 尝试申请包含其中任何一个引脚的 spi_grp，内核会直接返回 -EBUSY。

- **配置复用：** 即使两个不同的 Function（比如 GPIO 和 UART）都可以用到同一个物理引脚，通过 groups 的划分，我们可以清晰地定义出“这根线在 A 方案里当串口，在 B 方案里当普通输入”。

### 总结

- **Groups：** 是对硬件引脚的**空间管理**（哪几根线是一伙的）。

- **Functions：** 是对硬件能力的**逻辑抽象**（这伙线能干什么）。

这就好比 **Functions 是“插线板上的插孔功能”**（电源、USB、网口），而 **Groups 是“你具体插在哪个位置的物理座子”**。

如果你有兴趣，我们可以挑一个具体的芯片（比如 **i.MX6** 或 **STM32**）的 pinctrl 源码来看看它是如何通过宏定义来简化这些繁琐的数组声明的？
