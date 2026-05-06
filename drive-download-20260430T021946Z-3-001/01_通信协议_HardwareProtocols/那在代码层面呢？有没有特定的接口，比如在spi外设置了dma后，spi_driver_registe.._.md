在代码层面，Linux 内核的 DMA 子系统设计目标是**透明化**。当你通过设备树（DTS）配置了 DMA 后，绝大多数工作是由 **SPI 控制器驱动（Controller Driver）** 和 **SPI 核心层（Core）** 自动完成的，而不是由你写的特定外设驱动（Protocol Driver）去直接操作 DMA。

不过，理解这个过程对于调试和高性能开发至关重要。以下是代码层面的核心逻辑：

### 1. 注册阶段的“魔力”

当你调用 spi_register_controller（或旧版的 spi_register_master）时，RK3568 的 SPI 控制器驱动会执行以下操作：

- **解析 DTS**：控制器驱动会检查 DTS 中是否有 dmas 属性。

- **请求通道**：它会调用 dma_request_chan() 来获取 TX 和 RX 的虚拟通道。

- **能力上报**：如果成功获取 DMA 通道，控制器驱动会设置 ctlr-\>can_dma 回调函数。

对于你作为外设驱动开发者（即调用 spi_message 的人）来说，**并没有额外的 API**，你依然使用标准接口。

### 2. 核心接口：数据传输

在传输时，SPI 核心层会判断是否满足 DMA 传输条件（例如数据长度是否超过 ctlr-\>dma_min_bytes）。如果满足，底层会自动完成以下映射流程：

#### 映射缓冲区 (DMA Mapping)

在发起传输前，驱动需要将虚拟地址转换为 DMA 能够识别的物理地址（总线地址）。

- **Streaming DMA Mapping**：最常用，使用 dma_map_single() 或 spi_map_buf()。

- **Cache 一致性**：映射操作会处理 Cache 的 Flush（发送时）或 Invalidate（接收时），防止 CPU 看到旧数据。

// 在 SPI 控制器驱动内部（如 spi-rockchip.c），你会看到类似逻辑：  
xfer-\>tx_dma = dma_map_single(dev, xfer-\>tx_buf, xfer-\>len, DMA_TO_DEVICE);

### 3. 如何在代码中强制/优化 DMA？

虽然没有“额外”接口，但你可以通过以下方式在代码中干预 DMA 行为：

#### A. 设置传输阈值

如果你的数据很小（比如只有 4 字节），开启 DMA 的开销（Cache 操作、寄存器配置）反而比 CPU 拷贝慢。你可以在驱动中通过修改 spi_transfer 的参数来配合。

#### B. 预先映射 (Pre-mapping)

如果你在频繁发送同一块固定内存，为了性能，你可以提前手动映射 DMA 地址，并将其赋值给 xfer-\>tx_dma。

struct spi_transfer t = {  
.tx_buf = my_buf,  
.len = 1024,  
.tx_dma = my_pre_mapped_phys_addr, // 明确告知内核物理地址  
};  
t.conf_flags \|= SPI_TRANS_USE_DMA; // 某些架构支持强制标志

### 4. 关键数据结构变化

注册后，你可以通过 spi_controller 结构体查看 DMA 状态。这通常用于调试：

- **ctlr-\>dma_tx / ctlr-\>dma_rx**：存储了指向 dma_chan 的指针。

- **ctlr-\>max_dma_len**：该控制器支持的最大 DMA 传输长度。

### 5. 调试技巧：如何确认 DMA 真的生效了？

因为接口是透明的，你可能不知道 DMA 是否在工作。你可以查看内核节点：

1.  **中断统计**： cat /proc/interrupts \| grep dma 看 DMAC（PL330）的中断计数是否随着 SPI 传输而增加。

2.  **内核日志**： 在 drivers/spi/spi-rockchip.c 中开启 dev_dbg，或者查看加载时的 Log。如果 DMA 请求失败，通常会有一条： rockchip-spi fe610000.spi: Failed to request TX DMA channel

### 总结

对于 RK3568 的驱动开发，spi_driver_register 之后你不需要调用任何 spi_dma_start() 之类的接口。**只要 DTS 配置正确，且 spi_transfer 的数据长度超过了控制器定义的门槛值，DMA 就会自动介入。**

你现在遇到的问题是传输速度达不到预期，还是怀疑 DMA 压根没跑起来？
