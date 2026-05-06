# xparameters.h 宏定义说明

此文档对 `xparameters.h` 中的每个宏定义提供简要中文说明，帮助开发者快速理解各宏的含义与用途。宏按功能分组，便于查阅。

---

## 1. CPU 相关

| 宏定义 | 说明 |
|---|---|
| `XPAR_CPU_ID` | CPU 的唯一标识符，默认 `0U`。
| `XPAR_PS7_CORTEXA9_0_CPU_CLK_FREQ_HZ` | PS7 Cortex‑A9 核心的时钟频率（单位 Hz），此处为 `666666687` Hz。
| `XPAR_CPU_CORTEXA9_0_CPU_CLK_FREQ_HZ` | 与上面相同的别名，提供统一的 CPU 时钟频率宏。

---

## 2. 标准输入/输出基址

| 宏定义 | 说明 |
|---|---|
| `STDIN_BASEADDRESS` | 标准输入（UART）寄存器基址 `0xE0001000`。
| `STDOUT_BASEADDRESS` | 标准输出（UART）寄存器基址 `0xE0001000`（与 STDIN 相同）。

---

## 3. 片上外设（Peripheral）驱动实例数

| 宏定义 | 说明 |
|---|---|
| `XPAR_XAXIDMA_NUM_INSTANCES` | AXI DMA 驱动实例数量，当前为 `1`。
| `XPAR_XGPIOPS_NUM_INSTANCES` | GPIO PS 驱动实例数量，当前为 `1`。
| `XPAR_XIICPS_NUM_INSTANCES` | I2C PS 驱动实例数量，当前为 `1`。
| `XPAR_XQSPIPS_NUM_INSTANCES` | QSPI PS 驱动实例数量，当前为 `1`。
| `XPAR_XSCUGIC_NUM_INSTANCES` | SCU 通用中断控制器实例数量，当前为 `1`。
| `XPAR_XSCUTIMER_NUM_INSTANCES` | SCU 计时器实例数量，当前为 `1`。
| `XPAR_XSCUWDT_NUM_INSTANCES` | SCU 看门狗计时器实例数量，当前为 `1`。
| `XPAR_XUARTPS_NUM_INSTANCES` | UART PS 驱动实例数量，当前为 `2`。
| `XPAR_XSDPS_NUM_INSTANCES` | SD 卡驱动实例数量，当前为 `2`。
| `XPAR_XEMACPS_NUM_INSTANCES` | Ethernet MAC 驱动实例数量，当前为 `1`。
| `XPAR_XADCPS_NUM_INSTANCES` | ADC PS 驱动实例数量，当前为 `1`。

---

## 4. AXI DMA 0 (AXI_DMA_0) 详细配置

| 宏定义 | 说明 |
|---|---|
| `XPAR_AXI_DMA_0_DEVICE_ID` | AXI DMA 0 的设备 ID，`0`。
| `XPAR_AXI_DMA_0_BASEADDR` | DMA 控制器基址 `0x40400000`。
| `XPAR_AXI_DMA_0_HIGHADDR` | DMA 控制器高地址 `0x4040FFFF`。
| `XPAR_AXI_DMA_0_SG_INCLUDE_STSCNTRL_STRM` | 是否在散列表中包含状态/控制流，`0`（不包含）。
| `XPAR_AXI_DMA_0_INCLUDE_MM2S_DRE` | MM2S（内存到流）数据重传使能，`0`（不使能）。
| `XPAR_AXI_DMA_0_INCLUDE_S2MM_DRE` | S2MM（流到内存）数据重传使能，`0`（不使能）。
| `XPAR_AXI_DMA_0_INCLUDE_MM2S` | 是否包含 MM2S 通道，`1`（包含）。
| `XPAR_AXI_DMA_0_INCLUDE_S2MM` | 是否包含 S2MM 通道，`1`（包含）。
| `XPAR_AXI_DMA_0_M_AXI_MM2S_DATA_WIDTH` | MM2S 数据宽度，`64` 位。
| `XPAR_AXI_DMA_0_M_AXI_S2MM_DATA_WIDTH` | S2MM 数据宽度，`64` 位。
| `XPAR_AXI_DMA_0_INCLUDE_SG` | 是否支持散列表（Scatter‑Gather），`1`（支持）。
| `XPAR_AXI_DMA_0_ENABLE_MULTI_CHANNEL` | 多通道支持，`0`（单通道）。
| `XPAR_AXI_DMA_0_NUM_MM2S_CHANNELS` | MM2S 通道数，`1`。
| `XPAR_AXI_DMA_0_NUM_S2MM_CHANNELS` | S2MM 通道数，`1`。
| `XPAR_AXI_DMA_0_MM2S_BURST_SIZE` | MM2S 传输突发大小，`128`。
| `XPAR_AXI_DMA_0_S2MM_BURST_SIZE` | S2MM 传输突发大小，`128`。
| `XPAR_AXI_DMA_0_MICRO_DMA` | 是否使用微型 DMA，`0`（否）。
| `XPAR_AXI_DMA_0_ADDR_WIDTH` | 地址宽度，`32` 位。
| `XPAR_AXI_DMA_0_SG_LENGTH_WIDTH` | 散列表长度宽度，`23` 位。

---

## 5. AXI DMA 的 Canonical（规范）定义
> 为了兼容 Xilinx SDK，提供的宏是对上面原始宏的别名。

| 宏定义 | 对应原始宏 |
|---|---|
| `XPAR_AXIDMA_0_DEVICE_ID` | `XPAR_AXI_DMA_0_DEVICE_ID` |
| `XPAR_AXIDMA_0_BASEADDR` | `XPAR_AXI_DMA_0_BASEADDR` |
| `XPAR_AXIDMA_0_SG_INCLUDE_STSCNTRL_STRM` | `XPAR_AXI_DMA_0_SG_INCLUDE_STSCNTRL_STRM` |
| `XPAR_AXIDMA_0_INCLUDE_MM2S` | `XPAR_AXI_DMA_0_INCLUDE_MM2S` |
| `...` | `...` |

（此处省略其余相同映射的宏，全部保持一一对应关系）

---

## 6. DDR 地址空间

| 宏定义 | 说明 |
|---|---|
| `XPAR_PS7_DDR_0_S_AXI_BASEADDR` | DDR 控制器 0 的起始地址 `0x00100000`。
| `XPAR_PS7_DDR_0_S_AXI_HIGHADDR` | DDR 控制器 0 的最高地址 `0x3FFFFFFF`。

---

## 7. 设备配置（DEVCFG）

| 宏定义 | 说明 |
|---|---|
| `XPAR_PS7_DEV_CFG_0_DEVICE_ID` | 设备配置模块 ID，`0U`。
| `XPAR_PS7_DEV_CFG_0_BASEADDR` | 基址 `0xF8007000U`。
| `XPAR_PS7_DEV_CFG_0_HIGHADDR` | 高地址 `0xF80070FFU`。
| `XPAR_XDCFG_0_DEVICE_ID` | 规范别名，同上。
| `XPAR_XDCFG_0_BASEADDR` | 规范别名，同上。
| `XPAR_XDCFG_0_HIGHADDR` | 规范别名，同上。

---

## 8. DMA (PS7_DMA_NS / PS7_DMA_S) 物理地址

| 宏定义 | 说明 |
|---|---|
| `XPAR_PS7_DMA_NS_DEVICE_ID` | 非安全 DMA 控制器 ID `0`。
| `XPAR_PS7_DMA_NS_BASEADDR` | 基址 `0xF8004000`。
| `XPAR_PS7_DMA_NS_HIGHADDR` | 高地址 `0xF8004FFF`。
| `XPAR_PS7_DMA_S_DEVICE_ID` | 安全 DMA 控制器 ID `1`。
| `XPAR_PS7_DMA_S_BASEADDR` | 基址 `0xF8003000`。
| `XPAR_PS7_DMA_S_HIGHADDR` | 高地址 `0xF8003FFF`。

---

## 9. Ethernet（PS7_ETHERNET_0）

| 宏定义 | 说明 |
|---|---|
| `XPAR_PS7_ETHERNET_0_DEVICE_ID` | 以太网控制器 ID `0`。
| `XPAR_PS7_ETHERNET_0_BASEADDR` | 基址 `0xE000B000`。
| `XPAR_PS7_ETHERNET_0_HIGHADDR` | 高地址 `0xE000BFFF`。
| `XPAR_PS7_ETHERNET_0_ENET_CLK_FREQ_HZ` | 以太网时钟频率 `125000000` Hz。
| `XPAR_PS7_ETHERNET_0_ENET_SLCR_1000MBPS_DIV0` … `DIV1` | 1 Gbps 速率分频系数。
| `XPAR_PS7_ETHERNET_0_ENET_SLCR_100MBPS_DIV0` … `DIV1` | 100 Mbps 速率分频系数。
| `XPAR_PS7_ETHERNET_0_ENET_SLCR_10MBPS_DIV0` … `DIV1` | 10 Mbps 速率分频系数。
| `XPAR_PS7_ETHERNET_0_ENET_TSU_CLK_FREQ_HZ` | 时间戳单元时钟频率（未使用，`0`）。
| `XPAR_PS7_ETHERNET_0_IS_CACHE_COHERENT` | 是否支持缓存一致性，`0`（不支持）。
| `XPAR_XEMACPS_0_DEVICE_ID` 等 | 规范别名，指向同一以太网控制器。

---

## 10. AFI（AXI‑Fabric Interface）

| 宏定义 | 说明 |
|---|---|
| `XPAR_PS7_AFI_0_S_AXI_BASEADDR` | AFI 0 的 AXI 基址 `0xF8008000`。
| `XPAR_PS7_AFI_0_S_AXI_HIGHADDR` | AFI 0 的 AXI 高址 `0xF8008FFF`。
| `XPAR_PS7_AFI_1_S_AXI_BASEADDR` … | 同理，AFI 1、AFI 2、AFI 3 的基址与高址。

---

## 11. DDR 控制器（PS7_DDRC_0）

| 宏定义 | 说明 |
|---|---|
| `XPAR_PS7_DDRC_0_S_AXI_BASEADDR` | DDR 控制器 0 的 AXI 基址 `0xF8006000`。
| `XPAR_PS7_DDRC_0_S_AXI_HIGHADDR` | DDR 控制器 0 的 AXI 高址 `0xF8006FFF`。

---

## 12. 计时器与看门狗

| 宏定义 | 说明 |
|---|---|
| `XPAR_PS7_GLOBALTIMER_0_S_AXI_BASEADDR` | 全局计时器基址 `0xF8F00200`。
| `XPAR_PS7_GLOBALTIMER_0_S_AXI_HIGHADDR` | 高址 `0xF8F002FF`。
| `XPAR_PS7_SCUTIMER_0_BASEADDR` | SCU 计时器基址 `0xF8F00600`。
| `XPAR_PS7_SCUTIMER_0_HIGHADDR` | 高址 `0xF8F0061F`。
| `XPAR_PS7_SCUWDT_0_BASEADDR` | SCU 看门狗基址 `0xF8F00620`。
| `XPAR_PS7_SCUWDT_0_HIGHADDR` | 高址 `0xF8F006FF`。

---

## 13. GPIO（PS7_GPIO_0）

| 宏定义 | 说明 |
|---|---|
| `XPAR_PS7_GPIO_0_DEVICE_ID` | GPIO 0 的设备 ID `0`。
| `XPAR_PS7_GPIO_0_BASEADDR` | 基址 `0xE000A000`。
| `XPAR_PS7_GPIO_0_HIGHADDR` | 高址 `0xE000AFFF`。
| `XPAR_XGPIOPS_0_DEVICE_ID` 等 | 规范别名。

---

## 14. I2C（PS7_I2C_0）

| 宏定义 | 说明 |
|---|---|
| `XPAR_PS7_I2C_0_DEVICE_ID` | I2C 0 设备 ID `0`。
| `XPAR_PS7_I2C_0_BASEADDR` | 基址 `0xE0004000`。
| `XPAR_PS7_I2C_0_HIGHADDR` | 高址 `0xE0004FFF`。
| `XPAR_PS7_I2C_0_I2C_CLK_FREQ_HZ` | I2C 时钟频率 `111111115` Hz。
| `XPAR_XIICPS_0_DEVICE_ID` 等 | 规范别名。

---

## 15. QSPI（PS7_QSPI_0）

| 宏定义 | 说明 |
|---|---|
| `XPAR_PS7_QSPI_0_DEVICE_ID` | QSPI 0 设备 ID `0`。
| `XPAR_PS7_QSPI_0_BASEADDR` | 基址 `0xE000D000`。
| `XPAR_PS7_QSPI_0_HIGHADDR` | 高址 `0xE000DFFF`。
| `XPAR_PS7_QSPI_0_QSPI_CLK_FREQ_HZ` | QSPI 时钟频率 `200000000` Hz。
| `XPAR_PS7_QSPI_0_QSPI_MODE` | 工作模式 `0`（标准模式）。
| `XPAR_PS7_QSPI_0_QSPI_BUS_WIDTH` | 总线宽度 `2`（双线）。
| `XPAR_XQSPIPS_0_DEVICE_ID` 等 | 规范别名。

---

## 16. 中断（Fabric Interrupts）

| 宏定义 | 说明 |
|---|---|
| `XPAR_FABRIC_AXI_DMA_0_S2MM_INTROUT_INTR` | AXI DMA 0 S2MM 中断号 `61U`。
| `XPAR_FABRIC_AXI_DMA_0_MM2S_INTROUT_INTR` | AXI DMA 0 MM2S 中断号 `62U`。
| `XPAR_FABRIC_AXIDMA_0_S2MM_INTROUT_VEC_ID` | 对应的向量 ID（别名）。
| `XPAR_FABRIC_AXIDMA_0_MM2S_INTROUT_VEC_ID` | 对应的向量 ID（别名）。

---

## 17. SCUGIC（中断控制器）

| 宏定义 | 说明 |
|---|---|
| `XPAR_PS7_SCUGIC_0_DEVICE_ID` | SCU 通用中断控制器 ID `0U`。
| `XPAR_PS7_SCUGIC_0_BASEADDR` | 基址 `0xF8F00100U`。
| `XPAR_PS7_SCUGIC_0_HIGHADDR` | 高址 `0xF8F001FFU`。
| `XPAR_PS7_SCUGIC_0_DIST_BASEADDR` | 分配器基址 `0xF8F01000U`。
| `XPAR_SCUGIC_0_DEVICE_ID` 等 | 规范别名。

---

## 18. UART（PS7_UART_0 / PS7_UART_1）

| 宏定义 | 说明 |
|---|---|
| `XPAR_PS7_UART_0_DEVICE_ID` | UART0 设备 ID `0`。
| `XPAR_PS7_UART_0_BASEADDR` | 基址 `0xE0000000`。
| `XPAR_PS7_UART_0_HIGHADDR` | 高址 `0xE0000FFF`。
| `XPAR_PS7_UART_0_UART_CLK_FREQ_HZ` | UART0 时钟频率 `100000000` Hz。
| `XPAR_PS7_UART_0_HAS_MODEM` | 是否具备调制解调器功能，`0`（无）。
| `XPAR_PS7_UART_1_DEVICE_ID` … | 同理，UART1 基址 `0xE0001000` 等。
| `XPAR_XUARTPS_0_DEVICE_ID` 等 | 规范别名。

---

## 19. ADC（PS7_XADC_0）

| 宏定义 | 说明 |
|---|---|
| `XPAR_PS7_XADC_0_DEVICE_ID` | XADC 设备 ID `0`。
| `XPAR_PS7_XADC_0_BASEADDR` | 基址 `0xF8007100`。
| `XPAR_PS7_XADC_0_HIGHADDR` | 高址 `0xF8007120`。
| `XPAR_XADCPS_0_DEVICE_ID` 等 | 规范别名。

---

## 20. 文件系统（Xilinx FAT FS）设置

| 宏定义 | 说明 |
|---|---|
| `FILE_SYSTEM_INTERFACE_SD` | 采用 SD 卡作为文件系统接口。
| `FILE_SYSTEM_USE_LFN` | 启用长文件名（1 表示启用）。
| `FILE_SYSTEM_USE_MKFS` | 启用文件系统创建（mkfs）功能。
| `FILE_SYSTEM_NUM_LOGIC_VOL` | 逻辑卷数量 `2`（SD0、SD1）。
| `FILE_SYSTEM_USE_STRFUNC` | 字符串函数使用方式 `0`（禁用）。
| `FILE_SYSTEM_SET_FS_RPATH` | 设置根路径选项 `0`（默认）。
| `FILE_SYSTEM_WORD_ACCESS` | 采用字访问模式。

---

## 21. 保护宏（Header Guard）

| 宏定义 | 说明 |
|---|---|
| `XPARAMETERS_H` | 防止头文件被多次包含的宏。

---

**说明**：本文件仅提供宏的基本含义，实际使用时请结合硬件手册与 SDK 文档获取更详细的配置说明。

*生成于 2026‑04‑28*
