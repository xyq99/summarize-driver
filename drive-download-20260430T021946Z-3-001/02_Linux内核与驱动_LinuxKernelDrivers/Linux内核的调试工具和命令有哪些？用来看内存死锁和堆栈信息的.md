调试 Linux 内核就像是在行驶的赛车上换轮胎，既硬核又充满挑战。针对你提到的**内存、死锁和堆栈信息**，Linux 内核其实提供了一套非常成熟的“工具箱”。

以下是按功能分类的核心工具和命令：

## 1. 核心调试工具与机制

### **Kdump & Crash (离线分析之王)**

当内核崩溃（Panic）时，Kdump 会捕获当前内存的快照（vmcore）。

- **用途**：事后分析死锁、内存损坏和堆栈流向。

- **Crash 工具**：这是分析 vmcore 的标准工具。你可以像用 GDB 一样查看堆栈 (bt)、内存 (rd) 和进程状态 (ps)。

### **KDB & KGDB (在线调试)**

- **KDB**：内置在内核中的交互式调试器，不需要第二台机器。可以查内存、查堆栈，但不能源码级单步调试。

- **KGDB**：需要通过串口或网络连接两台机器，允许你像调试普通程序一样单步执行内核代码。

## 2. 死锁检测 (Deadlock Detection)

内核中有专门的子系统来盯着锁的状态，最常用的是 **Lockdep**。

### **Lockdep (锁定依赖证明器)**

- **原理**：它会跟踪内核中所有锁的获取顺序。如果它发现 A 锁住了 B，而 B 又试图去锁 A，它会立即在 dmesg 中抛出大段的警告。

- **如何查看**：

  - 检查日志：dmesg \| grep "DEBUG_LOCKS_WARN_ON"

  - 查看锁统计：cat /proc/lockstat

### **Hung Task Detector**

- **用途**：专门对付“处于 D 状态（不可中断睡眠）”超过 120 秒的任务。

- **输出**：它会自动打印死掉的任务堆栈，非常适合排查因等待 I/O 或锁导致的伪死锁。

## 3. 内存调试 (Memory Debugging)

### **Slab Debug & Slub_debug**

- **用途**：检查内存越界（Buffer Overflow）和写后释放（Use-after-free）。

- **操作**：在启动参数中加入 slub_debug=PU。它会在内存块前后加入“红区（Redzone）”，一旦被踩到，内核就会报错。

### **KASAN (Kernel Address Sanitizer)**

- **地位**：目前内核最强的动态内存检测工具。

- **能力**：能极高概率检测出释放后使用、越界访问等问题。

### **Meminfo & Slabinfo**

- cat /proc/meminfo：查看系统级内存水位。

- slabtop：实时查看内核各种缓存对象（如 inode, dentry）的占用情况，寻找内存泄漏。

## 4. 堆栈与调用链查看 (Stack Tracing)

当你怀疑某个进程卡死，或者想看内核在干什么时，使用以下命令：

### **常用命令组合**

- **dmesg**：查看内核环形缓冲区的日志，所有的崩溃堆栈（Oops/Panic）都在这里。

- **cat /proc/\<PID\>/stack**：这是**最简单直接**的方法。可以直接看到某个特定进程当前的内核态调用栈。

- **sysrq (魔术键)**：

  - echo t \> /proc/sysrq-trigger：导出所有任务的堆栈信息。

  - echo w \> /proc/sysrq-trigger：导出所有处于阻塞（Blocked）状态的任务堆栈。

### **ftrace (函数跟踪器)**

如果你想看堆栈是怎么一步步跑出来的，ftrace 的 function_graph 插件可以画出完整的调用树。

## 总结：该选哪个？

| 场景                       | 推荐工具                                    |
|----------------------------|---------------------------------------------|
| **内核已经挂了**           | Kdump + Crash                               |
| **怀疑有潜在死锁风险**     | 开启内核配置 CONFIG_PROVE_LOCKING (Lockdep) |
| **查看某个进程卡在哪了**   | cat /proc/PID/stack 或 SysRq-w              |
| **内存越界或不明原因崩溃** | KASAN 或 Slub_debug                         |
| **动态跟踪函数调用流**     | ftrace 或 eBPF (bpftrace)                   |

**提示**：在现代 Linux 调试中，**eBPF (bpftrace)** 正在成为新宠。它可以在不重启内核的情况下，通过简单的脚本监控锁的竞争时间和内存分配轨迹。
