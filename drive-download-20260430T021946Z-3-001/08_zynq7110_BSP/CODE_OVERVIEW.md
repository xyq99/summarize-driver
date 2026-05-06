# 代码阐述文档

## 项目概述
本项目是 **HighSpeed** 系列嵌入式系统的固件实现，主要用于高速数据采集、处理以及网络通信。代码基于 FreeRTOS 框架，结合 Xilinx FPGA 与多种外设（如 GPS、传感器、文件系统等）实现完整的系统功能。

## 目录结构
```
app/
├─ .cproject                # Eclipse 项目配置文件
├─ .gitignore               # Git 忽略规则
├─ .project                 # Eclipse 项目元数据
├─ .settings/               # IDE 设置目录
├─ README.md                # 项目说明（当前仅占位）
├─ _ide/                    # IDE 相关辅助文件（未展开）
├─ app.prj                  # 项目入口描述文件
├─ src/                     # 源代码目录
│   ├─ Xilinx.spec          # Xilinx 相关规格说明
│   ├─ app_cmds/            # 命令集合（目录结构自行补充）
│   ├─ app_regs/            # 寄存器映射文件（目录结构自行补充）
│   ├─ comm.c               # 通信层实现，提供日志输出、数据写入等接口
│   ├─ fileshare/           # 文件共享/FTP 相关实现
│   ├─ function/            # 各功能模块实现（传感器、调制解调等）
│   ├─ gps_position/        # GPS 定位相关代码（目录结构自行补充）
│   ├─ init.c               # 系统初始化入口，完成硬件、协议、任务等初始化
│   ├─ lscript.ld           # 链接脚本，定义内存布局
│   ├─ main.c               # 程序入口，创建初始化任务并启动调度器
│   ├─ modem/               # 调制解调器驱动（目录结构自行补充）
│   ├─ network/             # 网络协议栈实现（目录结构自行补充）
│   └─ protocol/            # 自定义协议实现（目录结构自行补充）
```

## 关键文件说明
| 文件 | 作用 | 主要实现 |
|------|------|----------|
| **main.c** | 程序入口 | 调用 `sot_createInitTask` 创建初始化任务并启动 FreeRTOS 调度器 |
| **init.c** | 系统初始化 | 包含硬件初始化、日志系统、各模块（如 GPS、FS、Watchdog）初始化以及任务创建逻辑 |
| **comm.c** | 通信/日志输出 | 实现 `Cmd_outprint`、`Dbg_output`、`Show_output` 等函数，用于向不同日志通道写入数据 |
| **lscript.ld** | 链接脚本 | 定义 Flash、RAM、堆栈等内存区域的映射关系 |
| **Xilinx.spec** | FPGA 规格说明 | 记录 FPGA 资源、时钟等信息（供编译脚本使用） |
| **app_cmds/**、**app_regs/** | 命令/寄存器映射 | 通过宏定义和结构体暴露给上层业务代码，便于统一管理 |
| **function/** | 功能模块集合 | 包含传感器、调制解调、重传等子模块的实现文件 |
| **fileshare/** | 文件共享/FTP | 提供 `Ftp_upload`、`Ftp_notify` 等接口，实现数据上传功能 |

## 主要功能模块
1. **任务调度**：基于 FreeRTOS，实现多任务并发运行。`init.c` 中的 `initTask` 为系统初始化任务，完成硬件、协议、日志等初始化后自行删除。
2. **日志系统**：`log_info`、`log_dbg`、`log_show` 等宏封装了不同级别的日志输出，`comm.c` 提供统一的日志写入实现。
3. **文件系统**：在 `CONFIG_FS_FAT32` 编译宏下，使用 `Afs_*` 系列接口操作 FAT32 文件系统，实现数据文件的创建、写入和关闭。
4. **网络/FTP**：`fileshare/` 目录下的 FTP 实现支持将采集的原始数据通过网络上传至服务器。
5. **传感器/外设**：通过 `Ms5837`、`HDSC`、`Ranging`、`Syncgps` 等模块读取深度、温度、定位等传感器数据。
6. **功耗管理**：`Watchdog`、`Sleep`、`Power`（若存在）等模块提供低功耗和看门狗复位功能。

## 编译与运行说明
1. **编译环境**：需要 Xilinx SDK（或 Vitis）以及支持 FreeRTOS 的交叉编译工具链。链接脚本 `lscript.ld` 必须与目标硬件的内存布局保持一致。
2. **宏配置**：通过 `#define CONFIG_XXX` 控制功能的编译，常用宏包括 `CONFIG_FS_FAT32`、`CONFIG_SHAREMEMORY`、`CONFIG_ETHERNET`、`CONFIG_MS5837` 等。
3. **启动流程**：
   - `main.c` 调用 `sot_createInitTask` 创建初始化任务。
   - 调度器启动后，`initTask` 执行硬件初始化并启动各子模块。
   - 初始化完成后调用 `StartMsgPrint` 打印系统信息并删除自身任务。
4. **调试**：可通过 UART、日志文件或网络抓包查看 `log_info` 输出的系统状态。

## 代码风格与约定
- 采用 **CamelCase** 与 **snake_case** 混合的命名方式，宏使用全大写下划线分隔。
- 所有公共 API 前缀统一为 `sot_` 或模块名（如 `Cmd_`、`Dbg_`）。
- 通过 `#ifdef CONFIG_XXX` 控制可选功能，保持代码的可裁剪性。
- 注释使用中文，保持简洁明了，变量、函数名保持英文以便跨语言阅读。

## 备注
- 目前 `README.md` 仅包含占位文字，建议后续补充项目背景、硬件平台、依赖库版本等信息。
- 如需进一步了解各子模块的实现细节，可打开对应目录下的 `.c/.h` 文件进行阅读。

---
*本文档自动生成于 2026-04-17，使用 Antigravity AI 编写。*
