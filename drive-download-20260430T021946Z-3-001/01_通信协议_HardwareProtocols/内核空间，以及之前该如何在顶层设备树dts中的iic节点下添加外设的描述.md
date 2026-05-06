在 RK3568 的内核开发中，在设备树（DTS）中添加 I2C 外设描述是让内核识别设备的关键。RK3568 通常使用 i2c0 到 i2c5 等多个控制器，你需要将外设节点挂载在对应的控制器节点下。

以下是标准的添加步骤和模板：

## 1. 基础 DTS 节点模板

假设你有一个 I2C 设备（例如一个温湿度传感器或 EEPROM），挂载在 RK3568 的 i2c1 总线上，从机地址为 0x50。

&i2c1 {  
status = "okay";  
pinctrl-names = "default";  
pinctrl-0 = \<&i2c1m0_xfer\>; // 确保引脚复用配置正确  
clock-frequency = \<400000\>; // 设置频率为 400kHz (Fast Mode)  
  
/\* 外设节点名称@从机地址 \*/  
my_i2c_device@50 {  
compatible = "vendor,model_name"; // 必须与驱动中的 of_match_table 一致  
reg = \<0x50\>; // 外设的 7 位 I2C 地址  
  
/\* 中断配置（如果设备支持中断） \*/  
interrupt-parent = \<&gpio0\>;  
interrupts = \<RK_PA1 IRQ_TYPE_LEVEL_LOW\>;  
  
/\* 供电与复位（根据实际电路添加） \*/  
vcc-supply = \<&vcc3v3_sys\>;  
reset-gpios = \<&gpio1 RK_PB2 GPIO_ACTIVE_LOW\>;  
};  
};

## 2. 关键属性解析

### compatible (核心)

这是驱动匹配的“灵魂”。内核在加载驱动时，会扫描设备树中的 compatible 字符串，并与驱动程序中 struct i2c_driver 里的 id_table 或 of_match_table 进行比对。

- **格式**："厂家,型号"。

- **示例**："rockchip,rk3568-i2c" 或 "atmel,24c02"。

### reg

设备的 I2C 从机地址。

- 注意：这里填写的是 **7 位地址**。

- 地址必须与硬件原理图上的物理地址（包括硬件拉高/拉低的 A0/A1 位）保持一致。

### pinctrl-0

RK3568 的 I2C 引脚通常有多个复用组合（如 M0, M1）。

- 在 rk3568.dtsi 中已经预定义了这些配置。

- 你需要根据硬件 PCB 走线选择对应的引脚组，例如 &i2c1m0_xfer。

### status

必须设置为 "okay" 才能使能该 I2C 控制器。如果该控制器在主设备树文件中被设置为 "disabled"，你的插件 DTS 必须将其覆盖。

## 3. 进阶：如何处理中断与电源

如果你的 I2C 外设需要通过中断告知 CPU 数据已就绪（例如触摸屏或加速度计），则需要配置中断属性：

- **interrupt-parent**：指定中断挂在哪个 GPIO 控制器下。

- **interrupts**：

  - 参数 1：引脚编号（如 RK_PA1）。

  - 参数 2：触发类型（如 IRQ_TYPE_EDGE_FALLING 下降沿触发）。

## 4. 验证设备是否添加成功

编译并烧录新的 DTB 文件后，可以通过以下方式验证：

1.  **检查内核日志**：  
    dmesg \| grep i2c  
    如果驱动成功加载并匹配，通常会看到类似 i2c 1-0050: chip found 的提示。

2.  **查看系统目录**： 进入 /sys/bus/i2c/devices/，你会发现类似 1-0050 的目录。

    - 1 代表 i2c1 总线。

    - 0050 代表地址为 0x50 的设备。

3.  **用户态扫描**： 使用 i2cdetect 工具查看地址是否被占用（显示为 UU 表示该地址已被驱动程序占用并绑定）：  
    i2cdetect -y 1

你在配置具体的某种传感器（如 IMU 或音频 Codec）时，遇到了具体的匹配问题吗？
