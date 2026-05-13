#   FreeRTOS 概要文档

## 1. 目录结构概览
```
 d:\xyq\HighSpeed_20260330.ide\bsp\ps7_cortexa9_0\freertos10_ps7_0\bsp\ps7_cortexa9_0
 ├─ include                 # 头文件目录
 │   ├─ FreeRTOS.h          # 核心 API 声明
 │   ├─ FreeRTOSConfig.h   # 项目级配置宏
 │   ├─ task.h、queue.h …   # 任务、队列等模块的头文件
 │   └─ … (大量辅助头文件)
 ├─ libsrc
 │   └─ freertos10_xilinx_v1_12
 │       └─ src
 │           ├─ tasks.c      # 任务管理、调度器实现
 │           ├─ queue.c      # 队列、信号量、互斥实现
 │           ├─ timers.c     # 软件定时器实现
 │           ├─ port.c、portASM.S  # 移植层 (Zynq‑7000/ Cortex‑A9)
 │           └─ … (其它源文件)
```

## 2. 核心配置 – `FreeRTOSConfig.h`
> **作用**：定义编译时宏，决定内核特性（抢占式/协作式调度、堆栈检查、勾选哪些 API、tick 频率等）。

```c
#define configUSE_PREEMPTION            1   // 1=抢占式调度, 0=协作式
#define configCPU_CLOCK_HZ              (800000000UL)   // Zynq‑7000 主频
#define configTICK_RATE_HZ              (1000)          // 1 ms tick
#define configMAX_PRIORITIES            (5)
#define configMINIMAL_STACK_SIZE        ((uint16_t)256)
#define configTOTAL_HEAP_SIZE           ((size_t)(32*1024))
#define configUSE_MUTEXES               1
#define configUSE_COUNTING_SEMAPHORES   1
#define configUSE_RECURSIVE_MUTEXES     1
```
> **使用方式**：在创建任务、队列等 API 前，编译器会根据这些宏启用/禁用对应代码路径。例如 `configUSE_MUTEXES` 为 1 时，`queue.c` 会编译互斥相关函数（`xQueueCreateMutex`、`xQueueGiveMutexRecursive` 等）。

## 3. 任务管理 – `tasks.c`
### 3.1 TCB（Task Control Block）结构
位置：`src/tasks.c` 第 255‑332 行
```c
typedef struct tskTaskControlBlock {
    volatile StackType_t *pxTopOfStack;   // 栈顶指针 (TCB 首成员)
    #if ( portUSING_MPU_WRAPPERS == 1 )
        xMPU_SETTINGS xMPUSettings;      // MPU 配置 (可选)
    #endif
    ListItem_t xStateListItem;            // 任务所在的状态链表节点
    ListItem_t xEventListItem;            // 任务在事件链表中的节点
    UBaseType_t uxPriority;               // 任务优先级 (0 为最低)
    StackType_t *pxStack;                 // 栈底指针
    char pcTaskName[ configMAX_TASK_NAME_LEN ]; // 可选任务名称
    … // 其余成员：栈高位指针、锁计数、统计信息等
} tskTCB;
typedef tskTCB TCB_t;
```
> **意义**：每个任务在创建时分配一个 TCB，保存运行时上下文（栈指针、优先级、状态链表等），调度器通过 `pxCurrentTCB` 指向当前执行的任务。

### 3.2 调度核心 – `vTaskStartScheduler`
入口函数约在 `tasks.c` 第 2100 行左右。主要流程：
1. 初始化就绪列表 `pxReadyTasksLists[]`（基于 `configMAX_PRIORITIES`）。
2. 创建并加入最低优先级的 **Idle Task**。
3. 启动 tick 中断 (`vPortStartFirstTask`) 进入首次上下文切换。
4. 进入无限循环，tick 中断触发 `xPortPendSVHandler`，调度器依据 `uxTopReadyPriority` 选择最高优先级的就绪任务。
> **关键宏**：`configUSE_PORT_OPTIMISED_TASK_SELECTION` 决定是否使用移植层的快速任务选择实现（`tasks.c` 第 118‑186 行）。

### 3.3 任务创建 – `xTaskCreate` / `xTaskCreateStatic`
- **动态分配**（`tasks.c` 第 726‑734 行）
```c
pxNewTCB = pvPortMalloc( sizeof( TCB_t ) );
pxNewTCB->pxStack = pvPortMallocStack( usStackDepth * sizeof( StackType_t ) );
prvInitialiseNewTask( … );               // 填充 TCB 各成员
prvAddNewTaskToReadyList( pxNewTCB );    // 加入就绪列表
```
- **静态分配**（`tasks.c` 第 574‑581 行）适用于 `configSUPPORT_STATIC_ALLOCATION` 为 1 的场景，避免堆占用。

## 4. 队列、信号量、互斥 – `queue.c`
### 4.1 `Queue_t`（原 `xQUEUE`）结构
位置：`src/queue.c` 第 100‑138 行
```c
typedef struct QueueDefinition {
    int8_t *pcHead;                // 队列存储区起始
    int8_t *pcWriteTo;             // 写指针 (下一个写入位置)
    union {
        QueuePointers_t xQueue;    // 普通队列使用的指针集合
        SemaphoreData_t xSemaphore;// 信号量/互斥使用的结构
    } u;
    List_t xTasksWaitingToSend;    // 发送阻塞任务链表 (优先级顺序)
    List_t xTasksWaitingToReceive; // 接收阻塞任务链表
    volatile UBaseType_t uxMessagesWaiting; // 当前已存条目数
    UBaseType_t uxLength;          // 队列长度 (条目数)
    UBaseType_t uxItemSize;        // 每条目字节数
    volatile int8_t cRxLock;       // 接收锁计数
    volatile int8_t cTxLock;       // 发送锁计数
    … // 其余成员：静态/动态标记、跟踪 ID、队列集合指针等
} xQUEUE;
typedef xQUEUE Queue_t;
```
> **解释**：
> - `pcHead` 与 `pcWriteTo` 共同维护循环缓冲区。 
> - `xQueue`（`pcTail`、`pcReadFrom`）仅在普通队列时使用。 
> - `xSemaphore` 用于信号量/互斥，`xMutexHolder` 记录拥有互斥的任务句柄。

### 4.2 队列创建 – `xQueueGenericCreate` / `xQueueGenericCreateStatic`
- **动态创建**（`queue.c` 第 398‑421 行）
```c
xQueueSizeInBytes = uxQueueLength * uxItemSize;
pxNewQueue = pvPortMalloc( sizeof( Queue_t ) + xQueueSizeInBytes );
// 队列结构在前，存储区紧随其后
pucQueueStorage = (uint8_t *)pxNewQueue + sizeof( Queue_t );
prvInitialiseNewQueue( uxQueueLength, uxItemSize, pucQueueStorage,
                       ucQueueType, pxNewQueue );
```
- **静态创建**（`queue.c` 第 335‑342 行）使用用户提供的 `StaticQueue_t` 与预先分配的存储区。
> `ucQueueType` 用于区分普通队列、信号量、互斥、计数信号量等。

### 4.3 发送 / 接收 – `xQueueGenericSend` / `xQueueGenericReceive`
实现位于 `queue.c`（约 1200‑1500 行）
```c
static BaseType_t prvCopyDataToQueue( Queue_t * const pxQueue,
                                      const void * pvItemToQueue,
                                      const BaseType_t xPosition );
BaseType_t xQueueGenericSend( QueueHandle_t xQueue,
                              const void * pvItemToQueue,
                              TickType_t xTicksToWait,
                              const BaseType_t xCopyPosition );
```
- **发送**：若队列未满则拷贝数据到 `pcWriteTo`，更新写指针；若已满则把调用任务挂到 `xTasksWaitingToSend` 链表并阻塞（可选超时）。
- **接收**：类似，若队列为空则阻塞在 `xTasksWaitingToReceive`。
> **锁机制**：`cRxLock / cTxLock` 用于在 ISR 环境安全地记录“在锁定期间有多少数据被发送/接收”，在恢复时触发对应任务的解阻。

### 4.4 互斥实现 – `prvInitialiseMutex`
位置：`queue.c` 第 512‑531 行
```c
pxNewQueue->u.xSemaphore.xMutexHolder = NULL;
pxNewQueue->uxQueueType = queueQUEUE_IS_MUTEX;   // 标记为互斥
pxNewQueue->u.xSemaphore.uxRecursiveCallCount = 0;
```
- **获取互斥**：`xQueueSemaphoreTake`（内部会检查 `uxMutexHolder`，若已被占用则阻塞）。
- **递归互斥**：`xQueueTakeMutexRecursive` / `xQueueGiveMutexRecursive` 通过 `uxRecursiveCallCount` 记录递归层数。

### 4.5 计数信号量 – `xQueueCreateCountingSemaphore`
实现位于 `queue.c` 第 736‑754 行（静态）与 770‑790 行（动态）
```c
QueueHandle_t xQueueCreateCountingSemaphore( const UBaseType_t uxMaxCount,
                                             const UBaseType_t uxInitialCount )
{
    // 创建普通信号量 (item size = 0) 并把初始计数写入 uxMessagesWaiting
}
```

## 5. 软硬件交互 – 移植层 (`port.c` / `portASM.S`)
虽然在当前目录下未直接列出，但 **FreeRTOS 移植层** 位于 `libsrc/freertos10_xilinx_v1_12/src/port.c` 与 `portASM.S`。它负责：
| 功能 | 关键实现 |
|------|----------|
| **tick 中断** | `vPortSetupTimerInterrupt` 配置 Zynq‑7000 定时器，使其每 1 ms 触发 `xPortSysTickHandler` |
| **上下文切换** | `portSAVE_CONTEXT` / `portRESTORE_CONTEXT` 在 `portASM.S` 中保存/恢复寄存器、SPSR、LR 等 |
| **临界区** | `taskENTER_CRITICAL` / `taskEXIT_CRITICAL` 使用 `cpsie/cpsid i`（中断屏蔽），并在多核系统中使用 `portDISABLE_INTERRUPTS` / `portENABLE_INTERRUPTS` 实现全局互斥 |
| **堆栈检查** | `configCHECK_FOR_STACK_OVERFLOW` 开启后，`vPortValidateInterruptStack` 在每次 tick 检查 `pxTopOfStack` 是否越界 |
> **查看源码**：
> - `src/port.c` (路径: `.../src/port.c`) 
> - `src/portASM.S` (路径: `.../src/portASM.S`)

## 6. 常用 API 示例（含代码片段）
### 6.1 创建任务
```c
void vTaskFunction( void *pvParameters )
{
    for( ;; )
    {
        /* 任务主体 */
        vTaskDelay( pdMS_TO_TICKS( 100 ) );
    }
}

/* 在系统初始化阶段调用 */
xTaskCreate( vTaskFunction,
             "DemoTask",
             configMINIMAL_STACK_SIZE,
             NULL,
             tskIDLE_PRIORITY + 1,
             NULL );
```
对应实现：`xTaskCreate` 位于 `tasks.c` 第 726‑734 行。

### 6.2 创建队列并发送/接收
```c
/* 创建一个长度为 10、每条目 4 字节的整数队列 */
QueueHandle_t xQueue = xQueueCreate( 10, sizeof( int ) );

int value = 42;
xQueueSend( xQueue, &value, pdMS_TO_TICKS( 10 ) );

int received;
xQueueReceive( xQueue, &received, portMAX_DELAY );
```
- `xQueueCreate` → `xQueueGenericCreate`（`queue.c` 第 398‑421 行）。
- `xQueueSend` / `xQueueReceive` → `xQueueGenericSend` / `xQueueGenericReceive`（对应实现位于 `queue.c` 中）。

### 6.3 使用互斥保护共享资源
```c
QueueHandle_t xMutex = xQueueCreateMutex();

void vProtectedFunc( void )
{
    if( xSemaphoreTake( xMutex, pdMS_TO_TICKS( 5 ) ) == pdPASS )
    {
        /* 临界区代码 */
        xSemaphoreGive( xMutex );
    }
}
```
- 互斥创建在 `xQueueCreateMutex`（`queue.c` 第 542‑550 行），拿/释放使用通用信号量 API `xSemaphoreTake` / `xSemaphoreGive`。

## 7. 推荐阅读的源码位置
| 功能 | 关键文件 | 行号范围（参考） |
|------|----------|-------------------|
| **TCB 定义** | `src/tasks.c` | 255‑332 |
| **任务调度入口** | `src/tasks.c` | 118‑186（调度选择） |
| **任务创建** | `src/tasks.c` | 726‑734（动态） |
| **队列结构** | `src/queue.c` | 100‑138 |
| **队列创建** | `src/queue.c` | 398‑421（动态） |
| **互斥初始化** | `src/queue.c` | 512‑531 |
| **计数信号量** | `src/queue.c` | 736‑754（静态） |
| **移植层 tick** | `src/port.c` | (搜索 `vPortSetupTimerInterrupt`) |
| **上下文切换** | `src/portASM.S` | (搜索 `portSAVE_CONTEXT`) |

> 你可以在编辑器中打开这些文件，直接定位上述行号进行深入阅读。

---

**结束语**
以上章节涵盖了 **FreeRTOS** 在该 BSP 中的核心实现：从配置、任务、调度，到同步原语（队列、信号量、互斥）以及底层移植层。只要熟悉 `FreeRTOSConfig.h` 中的宏配置，配合对应的 API（`xTaskCreate`、`xQueueCreate`、`xSemaphoreTake` 等），即可在 Zynq‑7000（Cortex‑A9）平台上构建可靠的实时任务系统。若还有更具体的疑问（比如某个 API 的细节实现、堆栈检查等），欢迎继续提问！
