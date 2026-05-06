明白了，你是想为 AI Agent 编写一份“引导指令”或“上下文说明书”（`skills.md`），让它能够像专家一样理解这个特定 BSP 目录的结构和逻辑。

这份文档需要定义**目录结构映射**、**关键文件索引**以及**分析逻辑**。你可以将以下内容保存为 `skills.md` 放入项目根目录。

------

# BSP Analysis Skills for Zynq-7100

本指南旨在赋予 Agent 理解并分析 Zynq-7100 平台项目（基于 Vitis/Vivado SDK 架构）的能力。

## 1. 目录架构映射 (Directory Mapping)

Agent 在扫描目录时应遵循以下语义关联：

- **`/hw`**: 硬件定义目录。包含 `.xsa` 或 `.hdf` 文件，定义了 PL 逻辑、比特流和 PS 外设基地址。
- **`/ps7_cortexa9_0`**: 核心处理器子系统目录。
  - **`.../freertos10_ps7_0...`**: 目标操作系统代码库。
  - **`.../bsp/ps7_cortexa9_0/libsrc`**: 核心驱动源代码（如 GPIO, SPI, UART）。
  - **`.../bsp/ps7_cortexa9_0/include`**: 编译所需的头文件。
- **`/zynq_fsbl`**: 第一阶段启动加载程序源代码，负责初始化 DDR 和加载 Bitstream。
- **`platform.spr`**: 平台配置主文件，记录了硬件与软件栈的关联关系。

## 2. 关键文件分析逻辑 (Critical File Inspection)

当询问具体功能时，Agent 必须检查以下“事实来源”：

### A. 硬件参数字典：`xparameters.h`

- **路径**: `ps7_cortexa9_0/bsp/ps7_cortexa9_0/include/xparameters.h`
- **任务**: 检索外设基地址（`BASEADDR`）、中断 ID（`IRQ_ID`）和时钟频率。
- **内存约束**: 重点确认 `XPAR_PS7_DDR_0_S_AXI_BASEADDR` 到 `HIGHADDR` 的范围。针对 256MB DDR 配置，验证地址空间是否溢出。

### B. 软件配置描述：`system.mss`

- **路径**: `ps7_cortexa9_0/bsp/system.mss`
- **任务**: 确认驱动版本、标准输入输出设置（`stdin`/`stdout`）以及是否启用了扩展库（如 `xilffs`）。

### C. 链接脚本：`lscript.ld`

- **路径**: 应用工程根目录或 BSP 目录。
- **任务**: 分析 `Section` 分配。确认 Stack 和 Heap 的大小是否在 256MB 物理内存的安全范围内，防止内存重叠。

## 3. 驱动与协议识别技能

当 Agent 接收到涉及特定外设的指令时，应自动定位到以下驱动模型：

- **GPIO**: 区分 `XGpio` (PL 端 IP) 和 `XGpioPs` (PS 端原生)。
- **中断**: 检索 `XScuGic` 相关初始化代码，确认中断向量表配置。
- **内存管理**: 在 FreeRTOS 环境下，检查 `FreeRTOSConfig.h` 中的 `configTOTAL_HEAP_SIZE`。

## 4. Agent 执行准则 (Instruction for Agent)

1. **优先检索**: 任何涉及引脚、地址或中断的问题，首选检索 `xparameters.h`。
2. **版本校验**: 针对 `freertos10`，注意任务优先级映射与原生 FreeRTOS 的差异。
3. **资源预警**: 若发现代码尝试分配超过 200MB 以上的大块连续内存，必须提示物理 DDR 只有 256MB 的限制。

------

### 如何使用此文档？

你可以直接将上述 Markdown 内容发给 Agent，并对它说：

> “请学习这份 `skills.md`，它定义了我的 Zynq-7100 项目目录结构和分析逻辑。以后当我询问关于驱动、地址空间或系统配置的问题时，请根据这份文档定义的路径和规则进行检索和回答。”

**你需要我针对具体的驱动（比如你之前研究的 ADC 采集或 DMA）在这份 `skills.md` 中加入更细化的代码路径索引吗？**