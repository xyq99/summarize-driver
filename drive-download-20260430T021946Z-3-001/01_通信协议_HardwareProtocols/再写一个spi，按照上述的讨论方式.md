在 RK3568 上，SPI（Serial Peripheral Interface）的实现逻辑与 I2C 类似，但由于 SPI 是全双工通信，且涉及 **Chip Select (CS)**、**CPOL/CPHA 极性配置**以及**时钟频率**等物理特性，其设备树描述和驱动实现会稍微复杂一些。

## 1. 设备树描述 (DTS)

RK3568 的 SPI 控制器通常有 spi0 到 spi3。假设你将外设挂在 spi0 上，使用 CS0。

&spi0 {  
status = "okay";  
pinctrl-names = "default", "high_speed";  
pinctrl-0 = \<&spi0m0_pins\>; // 对应引脚复用配置  
pinctrl-1 = \<&spi0m0_pins_hs\>; // 高速模式配置（可选）  
  
/\* 外设节点：名称@片选编号 \*/  
my_spi_device@0 {  
compatible = "vendor,spi_model";  
reg = \<0\>; // 使用 CS0  
spi-max-frequency = \<24000000\>; // 最大时钟频率 24MHz  
  
/\* SPI 模式配置（核心参数） \*/  
// spi-cpol; // 如果设置，则时钟极性为高，否则为低  
// spi-cpha; // 如果设置，则在第二个边沿采样  
// spi-cs-high; // 如果片选信号是高电平有效则添加  
  
/\* 其他硬件连接 \*/  
interrupt-parent = \<&gpio0\>;  
interrupts = \<RK_PC1 IRQ_TYPE_EDGE_FALLING\>;  
};  
};

## 2. 内核空间驱动代码 (C)

SPI 驱动基于 spi_driver 框架。与 I2C 不同，SPI 常用 spi_sync 或 spi_write_then_read 进行通信。

\#include \<linux/module.h\>  
\#include \<linux/spi/spi.h\>  
\#include \<linux/of.h\>  
  
struct my_spi_dev {  
struct spi_device \*spi;  
u8 tx_buf\[64\];  
u8 rx_buf\[64\];  
};  
  
/\* 1. SPI 读写复合操作函数 \*/  
static int my_spi_read_reg(struct spi_device \*spi, u8 reg, u8 \*val)  
{  
int ret;  
u8 cmd = reg \| 0x80; // 假设最高位为 1 表示读操作  
  
/\* 这是一个常用的简易接口：先写 cmd，紧接着读回数据 \*/  
ret = spi_write_then_read(spi, &cmd, 1, val, 1);  
if (ret \< 0)  
dev_err(&spi-\>dev, "SPI read failed: %d\n", ret);  
  
return ret;  
}  
  
/\* 2. Probe 函数 \*/  
static int my_spi_probe(struct spi_device \*spi)  
{  
struct my_spi_dev \*ms;  
u8 device_id = 0;  
  
dev_info(&spi-\>dev, "SPI Device Probed!\n");  
  
/\* 配置 SPI 运行参数（通常在驱动中再次确认） \*/  
spi-\>mode = SPI_MODE_0; // CPOL=0, CPHA=0  
spi-\>bits_per_word = 8;  
spi-\>max_speed_hz = 10000000; // 10MHz  
spi_setup(spi);  
  
ms = devm_kzalloc(&spi-\>dev, sizeof(\*ms), GFP_KERNEL);  
if (!ms) return -ENOMEM;  
  
ms-\>spi = spi;  
spi_set_drvdata(spi, ms);  
  
/\* 尝试读取 ID 寄存器 \*/  
if (my_spi_read_reg(spi, 0x00, &device_id) == 0) {  
dev_info(&spi-\>dev, "Detected Device ID: 0x%02x\n", device_id);  
}  
  
return 0;  
}  
  
/\* 3. 设备树匹配 \*/  
static const struct of_device_id my_spi_of_match\[\] = {  
{ .compatible = "vendor,spi_model", },  
{ /\* sentinel \*/ }  
};  
MODULE_DEVICE_TABLE(of, my_spi_of_match);  
  
/\* 4. 驱动结构体 \*/  
static struct spi_driver my_spi_driver = {  
.driver = {  
.name = "my_spi_driver",  
.of_match_table = my_spi_of_match,  
},  
.probe = my_spi_probe,  
};  
  
module_spi_driver(my_spi_driver);  
  
MODULE_LICENSE("GPL");  
MODULE_AUTHOR("Engineer");

## 3. 驱动层关键接口对比

| 接口函数                  | 适用场景      | 特点                                                               |
|---------------------------|---------------|--------------------------------------------------------------------|
| **spi_setup()**           | 初始化        | 根据 spi_device 的设置（模式、频率）更新控制器寄存器。             |
| **spi_write_then_read()** | 寄存器读写    | **最常用**。内部处理了两个 spi_transfer，适合“写命令+收数据”。     |
| **spi_sync()**            | 复杂数据传输  | 同步阻塞。可以发送一个 spi_message（包含多个 spi_transfer 队列）。 |
| **spi_async()**           | 高性能/非阻塞 | 异步传输，完成后回调。适合大流量、对实时性要求高的场景。           |

## 4. RK3568 特别说明

1.  **Pinctrl 引脚组**：RK3568 的 SPI 拥有 M0, M1 等多组引脚，如果在 DTS 里配错了 pinctrl，逻辑分析仪上将看不到任何波形。

2.  **CS 引脚控制**：

    - **硬件 CS**：由 SPI 控制器自动拉低。

    - **GPIO CS**：在 DTS 中使用 cs-gpios = \<&gpio1 RK_PA2 GPIO_ACTIVE_LOW\>; 描述，内核 SPI 子系统会自动将其作为片选信号处理。

3.  **Spidev 测试**：如果你只想在用户态测试，可以使用内核自带的通用驱动 compatible = "rohm,dh2228fv"（或其他匹配 spidev 的 ID），这样会在 /dev/ 下生成 spidev0.0，然后用 ioctl 进行读写。

你是在调试传感器、显示屏还是高带宽的 ADC 数据采集？SPI 的 spi_message 构造对于大批量采样（如你之前提到的 128 路信号处理）会非常有帮助。
