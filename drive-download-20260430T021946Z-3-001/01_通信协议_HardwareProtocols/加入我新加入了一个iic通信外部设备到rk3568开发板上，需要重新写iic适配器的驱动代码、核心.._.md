在 Linux 系统中添加一个新的 I2C 外设（如传感器、EEPROM 或触摸芯片），**完全不需要**重新编写 I2C 适配器驱动或核心层代码。

Linux 的 I2C 子系统采用了分层架构，适配器驱动（负责硬件波形）和核心层（负责中转）是高度通用的“基础设施”。作为开发者，你的核心任务是**编写/配置设备驱动层**，并将设备挂载到对应的总线上。

## 1. 添加 I2C 外设的标准流程

对于像 RK3568 这样成熟的平台，流程通常分为以下三步：

#### 第一阶段：硬件连接

- 确认外设的 **SDA/SCL** 引脚连接到了 RK3568 的哪一组 I2C 控制器上（例如 I2C1）。

- 确认外设的 **Slave Address**（从机地址），并连接好 **INT**（中断）和 **RST**（复位）引脚。

#### 第二阶段：设备树（DTS）配置

这是最关键的一步，目的是告诉内核：**“在某条总线的某个地址上，有一个什么样的设备”**。

在 arch/arm64/boot/dts/rockchip/rk3568-xxx.dts 中添加：

> 代码段

&i2c1 {  
status = "okay";  
pinctrl-names = "default";  
pinctrl-0 = \<&i2c1m0_xfer\>; // 确认引脚复用配置  
  
my_sensor: my_sensor@48 {  
compatible = "myvendor,mysensor"; // 必须与驱动中的 id_table 匹配  
reg = \<0x48\>; // 外设的 I2C 7位地址  
interrupt-parent = \<&gpio0\>; // 中断挂在哪个 GPIO 组  
interrupts = \<RK_PA1 IRQ_TYPE_LEVEL_LOW\>; // 中断引脚和触发方式  
status = "okay";  
};  
};

> **为什么要这么做？**
>
> 内核启动时会解析这个节点，并自动为你创建一个 **i2c_client** 结构体。它会包含地址（0x48）、中断号以及指向 I2C1 适配器 (i2c_adapter) 的指针。

#### 第三阶段：编写或配置设备驱动（I2C Driver）

如果你使用的是标准设备（如 FT5x 触摸屏），内核通常已有驱动。你只需要在 .config 中开启即可。如果是全新设备，你需要编写 **i2c_driver**。

## 2. 编写 i2c_driver 的核心模板

你只需要关注如何与 i2c_client 交互。

> C

\#**include** \<linux/i2c.h\>  
  
// 1. Probe 函数：当 DTS 里的 compatible 匹配成功时执行  
static int my_sensor_probe(struct i2c_client \*client, const struct i2c_device_id \*id)  
{  
// 此时 client 已经包含了总线号、地址和中断号  
printk("My sensor probed at address 0x%x\n", client-\>addr);  
  
// 可以通过 i2c_master_send/recv 进行初始化通信  
// 注册字符设备或 Input 设备...  
return 0;  
}  
  
// 2. 匹配表：必须与 DTS 中的 compatible 字符串一致  
static const struct of_device_id my_sensor_of_match\[\] = {  
{ .compatible = "myvendor,mysensor", },  
{ },  
};  
  
// 3. 驱动结构体  
static struct i2c_driver my_sensor_driver = {  
.driver = {  
.name = "my_sensor_driver",  
.of_match_table = my_sensor_of_match,  
},  
.probe = my_sensor_probe,  
.remove = my_sensor_remove,  
};  
  
module_i2c_driver(my_sensor_driver); // 宏定义：自动完成注册

## 3. 为什么不需要改适配器和核心层？

- **适配器驱动 (i2c_adapter)**：由芯片厂商（Rockchip）写好。它只负责把 i2c_msg 转换成电平信号。无论你挂载的是温度计还是触摸屏，对它来说都只是 0 和 1。

- **核心层 (i2c-core)**：由 Linux 社区维护。它像是一个邮局，只负责把你的“信件”（i2c_msg）投递到正确的“地址”（i2c_client-\>addr）。

## 调试建议

在 RK3568 的 Shell 中，你可以使用 **i2c-tools** 来验证硬件是否连接成功：

- i2cdetect -y 1：扫描 I2C1 总线上的所有设备。如果你看到 0x48 位置显示了数值（或 UU 表示已被驱动占用），说明硬件连接和设备树基本没问题。

**你现在已经拿到了外设的 datasheet 吗？如果需要，我可以帮你写一个具体的 i2c_transfer 数据读写函数示例。**
