在 FreeRTOS 中，查看任务堆栈信息是调试内核、防止\*\*堆栈溢出（Stack Overflow）\*\*的关键手段。FreeRTOS 提供了一系列 API 来获取这些数据。

以下是几种常用的实现方式：

## 1. 使用 uxTaskGetStackHighWaterMark()

这是最常用且简单的方法。它返回自任务启动以来，任务堆栈中曾经剩余的**最小空闲字节数**（以字/Word 为单位，取决于你的架构）。

- **返回值越小，说明堆栈越接近耗尽。** 如果返回 0，说明堆栈很可能已经溢出了。

- **用法示例**：

> C

UBaseType_t uxHighWaterMark;  
// 查看当前任务  
uxHighWaterMark = uxTaskGetStackHighWaterMark(NULL);  
// 查看特定句柄的任务  
uxHighWaterMark = uxTaskGetStackHighWaterMark(xTaskHandle);

## 2. 使用 vTaskList() 打印列表

如果你想一次性查看系统中**所有任务**的状态（包括堆栈剩余量），可以使用 vTaskList()。

- **前提条件**：需要在 FreeRTOSConfig.h 中配置：

  - configUSE_TRACE_FACILITY 设置为 1

  - configUSE_STATS_FORMATTING_FUNCTIONS 设置为 1

- **效果**：它会生成一个字符串，包含任务名、状态、优先级、**堆栈历史最小剩余量**和任务编号。

> C

char pcWriteBuffer\[2048\];  
vTaskList(pcWriteBuffer);  
printf("Task State Priority Stack \#\n");  
printf("%s\n", pcWriteBuffer);

## 3. 使用 vTaskGetInfo() 获取详细结构体

如果你需要更细致的编程控制，可以使用 vTaskGetInfo() 获取 TaskStatus_t 结构体。

- **配置**：需要 configUSE_TRACE_FACILITY 为 1。

- **结构体成员**：usStackHighWaterMark 会告诉你该任务的堆栈安全边际。

> C

TaskStatus_t xTaskDetails;  
vTaskGetInfo(xTaskHandle, &xTaskDetails, pdTRUE, eInvalid);  
// 访问 xTaskDetails.usStackHighWaterMark;

## 4. 堆栈溢出钩子函数 (Runtime Detection)

如果你不是为了查看剩余量，而是为了**捕捉崩溃**，你应该开启堆栈溢出检测。

- **配置**：configCHECK_FOR_STACK_OVERFLOW 设置为 1 或 2。

- **实现**：你需要定义以下回调函数，当系统检测到任务越界时会自动跳转到这里：

> C

void vApplicationStackOverflowHook(TaskHandle_t xTask, char \*pcTaskName) {  
// 在这里打断点或重启系统  
printf("任务 \[%s\] 堆栈溢出了！\n", pcTaskName);  
}

### 关键概念：什么是 "High Water Mark"？

在 FreeRTOS 中，堆栈通常在初始化时被填充为一个特定数值（例如 0xa5）。随着任务运行，堆栈指针 \$SP\$ 会上下移动。uxTaskGetStackHighWaterMark 通过检查堆栈末端还有多少字节依然是 0xa5，来确定堆栈曾经“淹没”到的最高水位线。

### 注意事项

1.  **开销**：vTaskList() 和 uxTaskGetStackHighWaterMark() 涉及到遍历堆栈内存，会有一定的 CPU 开销，通常建议仅在 **Debug 模式** 下使用。

2.  **单位**：请注意，某些版本的 FreeRTOS 返回的是 **Words**（字），而不是 Bytes（字节）。在 32 位架构（如 STM32）上，1 Word = 4 Bytes。

你目前是在调试突发的系统死机问题，还是在进行项目后期的资源优化？
