在 Linux 内核开发中，devm_kzalloc 是一个非常经典且被强烈推荐的用法。简单来说，它是 **“内存分配 + 自动垃圾回收”** 的组合。

为了理解它的必要性，我们可以从以下三个维度来拆解：

### 1. 核心作用：生命周期管理 (Resource Management)

在传统的内核编程中，你在 probe 中申请了内存（使用 kzalloc），就必须在驱动卸载的 remove 函数中手动调用 kfree。

- **传统方式 (危、繁)**：如果你的 probe 函数中有 5 个步骤（申请内存、映射 IO、请求中断等），只要第 4 步失败了，你必须写一堆 goto 语句来手动释放前 3 步申请的资源。一旦漏掉一个，就会导致**内核内存泄漏**。

- **devm 方式 (安、简)**：devm 前缀代表 **Device Managed**。当你调用 devm_kzalloc 时，这块内存就绑定到了这个 device 结构体上。

  - **自动释放**：如果 probe 失败返回了，或者驱动被 rmmod 卸载了，内核会自动帮你调用 kfree。

### 2. 避免“Goto Hell”（代码简洁性）

对比一下两种写法，你就能明白为什么大家更喜欢在 probe 里用它：

#### 传统 kzalloc 写法：

static int my_probe(struct i2c_client \*client) {\
struct my_data \*priv = kzalloc(sizeof(\*priv), GFP_KERNEL);\
if (!priv) return -ENOMEM;\
\
ret = request_irq(client-\>irq, ...);\
if (ret) {\
kfree(priv); // 必须手动释放\
return ret;\
}\
// ... 更多的错误处理逻辑\
}

#### 使用 devm_kzalloc 写法：

static int my_probe(struct i2c_client \*client) {\
// 内存申请后直接不管了，内核会负责到底\
struct my_data \*priv = devm_kzalloc(&client-\>dev, sizeof(\*priv), GFP_KERNEL);\
if (!priv) return -ENOMEM;\
\
return request_irq(client-\>irq, ...); // 即使失败，priv 也会被自动回收\
}

### 3. 在 Probe 中的典型用途

在 probe 函数中，我们通常需要创建一个驱动的“私有上下文结构体”（如 struct my_i2c_dev），用来保存该设备的寄存器映射地址、中断号、锁、当前状态等信息。

- **数据隔离**：RK3568 可能会挂载多个相同的 I2C 外设。如果不使用 devm_kzalloc 动态分配空间，而使用全局变量，会导致多个设备共用同一块内存，产生数据冲突。

- **数据传递**：分配好这块内存后，我们会通过 i2c_set_clientdata() 或 dev_set_drvdata() 将其存入设备对象中。这样在 read、write 或 interrupt 处理函数里，我们可以随时取回这个结构体，知道当前是在操作哪一个物理设备。

### 总结

在 probe 中加入 devm_kzalloc 的主要原因有：

1.  **防止泄漏**：确保驱动卸载或初始化失败时，内存百分之百被回收。

2.  **简化代码**：消除冗长的错误处理逻辑（不需要写那么多 kfree）。

3.  **多实例支持**：为每一个匹配到的硬件实例创建独立的内存空间，互不干扰。

除了 devm_kzalloc，内核还提供了 devm_ioremap、devm_request_irq、devm_gpio_request 等，都是遵循同样的\*\*“申请即托管”\*\*原则。
