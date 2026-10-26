# Linux 系统性能分析与调优方法论

性能优化是高级运维开发的试金石。我们通常关注四大资源：CPU、内存、磁盘 I/O、网络。

## 1. USE 方法 (Utilization, Saturation, Errors)
由性能专家 Brendan Gregg 提出：
- **Utilization (利用率)**: 资源被使用的时间百分比。
- **Saturation (饱和度)**: 排队等待资源的任务数量。
- **Errors (错误)**: 资源产生的错误数。

---

## 2. CPU 性能分析

### 关键指标
- **Load Average**: 平均负载 (1分钟, 5分钟, 15分钟)。如果 Load > CPU 核数，说明系统过载。
- **User/System/Idle/Iowait**:
    - `User` 高: 应用程序计算密集。
    - `System` 高: 内核调用频繁 (如大量小包网络处理)。
    - `Iowait` 高: 等待磁盘 I/O。

### 常用工具
- `top / htop`: 实时查看进程 CPU 占用。
- `vmstat 1`: 查看系统整体上下文切换 (cs) 和中断 (in)。
- `pidstat -u 1`: 查看具体进程的 CPU 使用。
- `perf`: 内核级性能分析工具 (生成火焰图)。

---

## 3. 内存性能分析

### 关键概念
- **Buffer vs Cache**:
    - Buffer: 原始磁盘块的临时存储 (写缓冲)。
    - Cache: 文件内容的缓存 (读缓存)。
- **Swap**: 内存不足时，数据交换到磁盘。Swap 频繁会导致性能急剧下降。
- **OOM (Out Of Memory)**: 内存耗尽时，内核会杀死进程。

### 常用工具
- `free -h`: 查看内存使用概况。
- `vmstat 1`: 关注 `si` (swap in) 和 `so` (swap out)。
- `slabtop`: 查看内核 Slab 缓存占用。

---

## 4. 磁盘 I/O 分析

### 关键指标
- **IOPS**: 每秒读写次数 (随机读写关键指标)。
- **Throughput**: 吞吐量 (顺序读写关键指标)。
- **Latency**: 响应延迟。

### 常用工具
- `iostat -xz 1`: 查看磁盘利用率 (%util) 和等待队列 (aqu-sz)。
    - 如果 `%util` 接近 100%，说明磁盘饱和。
- `iotop`: 查看哪个进程在进行 I/O 操作。

---

## 5. 网络性能分析

### 关键指标
- **Bandwidth**: 带宽。
- **PPS (Packets Per Second)**: 每秒包数 (小包处理能力)。
- **Latency**: 网络延迟 (RTT)。

### 常用工具
- `ping`: 测试连通性和延迟。
- `netstat -ant / ss -lnt`: 查看连接状态 (ESTABLISHED, TIME_WAIT)。
- `sar -n DEV 1`: 查看网卡流量。
- `tcpdump`: 抓包分析。
