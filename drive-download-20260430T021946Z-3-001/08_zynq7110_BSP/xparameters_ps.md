# xparameters_ps.h 宏定义说明

此文档对 `xparameters_ps.h` 中的宏定义提供中文解释，帮助开发者快速了解各硬件资源的地址、时钟以及中断映射等信息。宏保持原始英文名称，说明全部使用中文。

---

## 1. 保护宏 (Header Guard)
| 宏 | 说明 |
|---|---|
| `_XPARAMETERS_PS_H_` | 防止头文件被多次包含的宏。

---

## 2. CPU 相关
| 宏 | 说明 |
|---|---|
| `XPAR_CPU_CORTEXA9_CORE_CLOCK_FREQ_HZ` | Cortex‑A9 主频，取决于对应的 `XPAR_CPU_CORTEXA9_0_CPU_CLK_FREQ_HZ` 或 `XPAR_CPU_CORTEXA9_1_CPU_CLK_FREQ_HZ`（条件编译）。
| `XPAR_CPU_CORTEXA9_0_CPU_CLK_FREQ_HZ` | 在 `xparameters.h` 中定义的 CPU 0 时钟频率 (例: 666 666 687 Hz)。
| `XPAR_CPU_CORTEXA9_1_CPU_CLK_FREQ_HZ` | 若系统有第二颗 Cortex‑A9 CPU，则对应其时钟频率。

---

## 3. DDR 内存空间
| 宏 | 说明 |
|---|---|
| `XPAR_DDR_MEM_BASEADDR` | DDR 起始基址 `0x00000000U`。
| `XPAR_DDR_MEM_HIGHADDR` | DDR 结束地址 `0x3FFFFFFFU`。

---

## 4. 硬件外设基址 (Peripheral Base Addresses)
> 这些宏提供硬件外设在地址空间的基址，主要用于裸机或驱动代码的寄存器映射。

| 宏 | 基址 | 说明 |
|---|---|---|
| `XPS_PERIPHERAL_BASEADDR` | `0xE0000000U` | 外设总基址（所有外设的公共前缀）。
| `XPS_UART0_BASEADDR` | `0xE0000000U` | UART0 寄存器基址。
| `XPS_UART1_BASEADDR` | `0xE0001000U` | UART1 寄存器基址。
| `XPS_USB0_BASEADDR` | `0xE0002000U` | USB0 基址。
| `XPS_USB1_BASEADDR` | `0xE0003000U` | USB1 基址。
| `XPS_I2C0_BASEADDR` | `0xE0004000U` | I2C0 基址。
| `XPS_I2C1_BASEADDR` | `0xE0005000U` | I2C1 基址。
| `XPS_SPI0_BASEADDR` | `0xE0006000U` | SPI0 基址。
| `XPS_SPI1_BASEADDR` | `0xE0007000U` | SPI1 基址。
| `XPS_CAN0_BASEADDR` | `0xE0008000U` | CAN0 基址。
| `XPS_CAN1_BASEADDR` | `0xE0009000U` | CAN1 基址。
| `XPS_GPIO_BASEADDR` | `0xE000A000U` | GPIO 基址。
| `XPS_GEM0_BASEADDR` | `0xE000B000U` | 第 0 个千兆以太网 MAC 基址。
| `XPS_GEM1_BASEADDR` | `0xE000C000U` | 第 1 个千兆以太网 MAC 基址。
| `XPS_QSPI_BASEADDR` | `0xE000D000U` | QSPI 基址。
| `XPS_PARPORT_CRTL_BASEADDR` | `0xE000E000U` | 并口（Parallel Port）控制寄存器基址。
| `XPS_SDIO0_BASEADDR` | `0xE0100000U` | SDIO0 基址。
| `XPS_SDIO1_BASEADDR` | `0xE0101000U` | SDIO1 基址。
| `XPS_IOU_BUS_CFG_BASEADDR` | `0xE0200000U` | IOU 总线配置基址。
| `XPS_NAND_BASEADDR` | `0xE1000000U` | NAND 控制器基址。
| `XPS_PARPORT0_BASEADDR` | `0xE2000000U` | 并口 0 基址。
| `XPS_PARPORT1_BASEADDR` | `0xE4000000U` | 并口 1 基址。
| `XPS_QSPI_LINEAR_BASEADDR` | `0xFC000000U` | QSPI 线性映射基址（用于文件系统）。
| `XPS_SYS_CTRL_BASEADDR` | `0xF8000000U` | 系统控制寄存器基址（SLCR）。
| `XPS_TTC0_BASEADDR` | `0xF8001000U` | TTC0（时钟计数器）基址。
| `XPS_TTC1_BASEADDR` | `0xF8002000U` | TTC1 基址。
| `XPS_DMAC0_SEC_BASEADDR` | `0xF8003000U` | 安全 DMA 控制器基址。
| `XPS_DMAC0_NON_SEC_BASEADDR` | `0xF8004000U` | 非安全 DMA 控制器基址。
| `XPS_WDT_BASEADDR` | `0xF8005000U` | 看门狗基址。
| `XPS_DDR_CTRL_BASEADDR` | `0xF8006000U` | DDR 控制器基址。
| `XPS_DEV_CFG_APB_BASEADDR` | `0xF8007000U` | 设备配置（APB）基址。
| `XPS_AFI0_BASEADDR` | `0xF8008000U` | AFI0 基址。
| `XPS_AFI1_BASEADDR` | `0xF8009000U` | AFI1 基址。
| `XPS_AFI2_BASEADDR` | `0xF800A000U` | AFI2 基址。
| `XPS_AFI3_BASEADDR` | `0xF800B000U` | AFI3 基址。
| `XPS_OCM_BASEADDR` | `0xF800C000U` | OCM（片上存储）基址。
| `XPS_EFUSE_BASEADDR` | `0xF800D000U` | eFuse 基址。
| `XPS_CORESIGHT_BASEADDR` | `0xF8800000U` | CoreSight 调试基址。
| `XPS_TOP_BUS_CFG_BASEADDR` | `0xF8900000U` | 顶层总线配置基址。
| `XPS_SCU_PERIPH_BASE` | `0xF8F00000U` | SCU 外设基址（包括 GIC、计时器、WDT 等）。
| `XPS_L2CC_BASEADDR` | `0xF8F02000U` | L2 缓存控制基址。
| `XPS_SAM_RAM_BASEADDR` | `0xFFFC0000U` | SAM（Secure Access Memory）基址。
| `XPS_FPGA_AXI_S0_BASEADDR` | `0x40000000U` | 第 0 条 FPGA AXI 主总线基址。
| `XPS_FPGA_AXI_S1_BASEADDR` | `0x80000000U` | 第 1 条 FPGA AXI 主总线基址。
| `XPS_IOU_S_SWITCH_BASEADDR` | `0xE0000000U` | IOU 交换基址。
| `XPS_PERIPH_APB_BASEADDR` | `0xF8000000U` | 外设 APB 总线基址。

---

## 5. 中断 ID 定义 (Interrupt IDs)
> 下面的宏将硬件中断号映射为友好的宏名称，供驱动和 BSP 使用。

### 共享外设中断 (SPI)
| 宏 | 中断号 |
|---|---|
| `XPS_CORE_PARITY0_INT_ID` | 32U |
| `XPS_CORE_PARITY1_INT_ID` | 33U |
| `XPS_L2CC_INT_ID` | 34U |
| `XPS_OCMINTR_INT_ID` | 35U |
| `XPS_ECC_INT_ID` | 36U |
| `XPS_PMU0_INT_ID` | 37U |
| `XPS_PMU1_INT_ID` | 38U |
| `XPS_SYSMON_INT_ID` | 39U |
| `XPS_DVC_INT_ID` | 40U |
| `XPS_WDT_INT_ID` | 41U |
| `XPS_TTC0_0_INT_ID` | 42U |
| `XPS_TTC0_1_INT_ID` | 43U |
| `XPS_TTC0_2_INT_ID` | 44U |
| `XPS_DMA0_ABORT_INT_ID` | 45U |
| `XPS_DMA0_INT_ID` | 46U |
| `XPS_DMA1_INT_ID` | 47U |
| `XPS_DMA2_INT_ID` | 48U |
| `XPS_DMA3_INT_ID` | 49U |
| `XPS_SMC_INT_ID` | 50U |
| `XPS_QSPI_INT_ID` | 51U |
| `XPS_GPIO_INT_ID` | 52U |
| `XPS_USB0_INT_ID` | 53U |
| `XPS_GEM0_INT_ID` | 54U |
| `XPS_GEM0_WAKE_INT_ID` | 55U |
| `XPS_SDIO0_INT_ID` | 56U |
| `XPS_I2C0_INT_ID` | 57U |
| `XPS_SPI0_INT_ID` | 58U |
| `XPS_UART0_INT_ID` | 59U |
| `XPS_CAN0_INT_ID` | 60U |
| `XPS_FPGA0_INT_ID` | 61U |
| `...` | `...` （后续 FPGA、USB、GEM、SDIO、I2C、SPI、UART、CAN 等中断同理） |

### 私有外设中断 (PPI)
| 宏 | 中断号 |
|---|---|
| `XPS_GLOBAL_TMR_INT_ID` | 27U |
| `XPS_FIQ_INT_ID` | 28U |
| `XPS_SCU_TMR_INT_ID` | 29U |
| `XPS_SCU_WDT_INT_ID` | 30U |
| `XPS_IRQ_INT_ID` | 31U |

---

## 6. 驱动层面使用的 Canonical（规范）宏
> 为了兼容 Xilinx SDK，提供了以 `XPAR_` 前缀的别名。

| 原始宏 | Canonical 宏 |
|---|---|
| `XPAR_AXI_DMA_0_DEVICE_ID` | `XPAR_AXIDMA_0_DEVICE_ID` |
| `XPAR_AXI_DMA_0_BASEADDR` | `XPAR_AXIDMA_0_BASEADDR` |
| `XPAR_XUARTPS_0_INTR` | `XPAR_XUARTPS_0_INTR`（已是规范形式） |
| `XPAR_XGPIOPS_0_DEVICE_ID` | `XPAR_XGPIOPS_0_DEVICE_ID` |
| `XPAR_XQSPIPS_0_LINEAR_BASEADDR` | `XPAR_XQSPIPS_0_LINEAR_BASEADDR` |
| `XPAR_XPARPORTPS_CTRL_BASEADDR` | `XPAR_XPARPORTPS_CTRL_BASEADDR` |
| `...` | `...` （其余外设同理） |

---

## 7. 其他重要宏
| 宏 | 说明 |
|---|---|
| `XPAR_XSLCR_NUM_INSTANCES` | SLCR（系统级控制寄存器）实例数量，固定为 1。
| `XPAR_SCUGIC_NUM_INSTANCES` | SCU 通用中断控制器实例数量，固定为 1。
| `XPAR_GLOBAL_TMR_NUM_INSTANCES` | 全局计时器实例数量，固定为 1。
| `XPAR_XSCUTIMER_NUM_INSTANCES` | SCU 计时器实例数量，固定为 1。
| `XPAR_XSCUWDT_NUM_INSTANCES` | SCU 看门狗实例数量，固定为 1。
| `XPAR_XADCPS_NUM_INSTANCES` | XADC（模拟‑数字转换器）实例数量，固定为 1。
| `XPAR_XUARTPS_NUM_INSTANCES` | UART 实例数量，固定为 2（UART0、UART1）。
| `XPAR_XSDPS_NUM_INSTANCES` | SD 卡驱动实例数量，固定为 2（SD0、SD1）。
| `XPAR_XEMACPS_NUM_INSTANCES` | Ethernet MAC 实例数量，固定为 1。

---

## 8. 兼容性宏 (Backward Compatibility)
| 宏 | 说明 |
|---|---|
| `XPAR_XUARTPS_0_CLOCK_HZ` / `XPAR_XUARTPS_1_CLOCK_HZ` | 兼容旧代码的 UART 时钟宏，映射到 `XPAR_XUARTPS_0_UART_CLK_FREQ_HZ`、`XPAR_XUARTPS_1_UART_CLK_FREQ_HZ`。
| `XPAR_XTTCPS_0_CLOCK_HZ` … `XPAR_XTTCPS_5_CLOCK_HZ` | TTC 时钟频率兼容宏。
| `XPAR_XIICPS_0_CLOCK_HZ` / `XPAR_XIICPS_1_CLOCK_HZ` | I2C 时钟频率兼容宏。
| `XPAR_XQSPIPS_0_CLOCK_HZ` | QSPI 时钟频率兼容宏。

---

## 9. 文件系统（Xilinx FAT FS）相关宏（在 `xparameters.h` 中定义）
> 为了完整性，这里列出在本文件中出现的文件系统宏（实际实现位于 `xparameters.h`）：
| 宏 | 说明 |
|---|---|
| `FILE_SYSTEM_INTERFACE_SD` | 使用 SD 卡作为文件系统接口。
| `FILE_SYSTEM_USE_LFN` | 启用长文件名（1 表示启用）。
| `FILE_SYSTEM_USE_MKFS` | 启用格式化功能（mkfs）。
| `FILE_SYSTEM_NUM_LOGIC_VOL` | 逻辑卷数量（2 表示 SD0、SD1）。
| `FILE_SYSTEM_USE_STRFUNC` | 字符串函数使用方式（0 表示禁用）。
| `FILE_SYSTEM_SET_FS_RPATH` | 根路径设置选项（0 为默认）。
| `FILE_SYSTEM_WORD_ACCESS` | 使用字访问模式。

---

**备注**：本文件仅提供宏的概要说明，实际使用时请参考 Xilinx Zynq‑7000 技术参考手册及对应驱动库文档，以获取更详细的寄存器位定义和使用示例。

*生成于 2026‑04‑28*
