# Docker 底层原理剖析

Docker 并非一项全新的技术，而是对 Linux 内核特性的封装。理解这些底层原理，是掌握 K8s 和容器排错的基础。

## 1. Namespace: 资源隔离

Namespace 是 Linux 内核提供的资源隔离机制，让进程“误以为”自己独占了系统。

Docker 主要使用了 6 种 Namespace：
1.  **PID Namespace**: 进程编号隔离。容器内 PID=1，宿主机上是其他 PID。
2.  **NET Namespace**: 网络设备、IP、端口隔离。每个容器有独立的 eth0 和 loopback。
3.  **MNT Namespace**: 文件系统挂载点隔离。
4.  **UTS Namespace**: 主机名和域名隔离。
5.  **IPC Namespace**: 进程间通信隔离 (信号量、消息队列)。
6.  **USER Namespace**: 用户和用户组隔离 (容器内 root 可能是宿主机的普通用户)。

## 2. Cgroups: 资源限制

Cgroups (Control Groups) 用于限制、记录和隔离进程组的资源使用 (CPU、内存、I/O)。

### 核心功能
- **资源限制**: 限制内存使用上限 (如 512MB)，超过则 OOM。
- **优先级分配**: 分配 CPU 时间片权重。
- **资源统计**: 统计 CPU 时长、内存用量 (用于计费)。

### 目录结构
通常位于 `/sys/fs/cgroup/`。

## 3. UnionFS: 联合文件系统

Docker 镜像的分层存储机制基于 UnionFS (如 Overlay2)。

### 镜像分层 (Image Layers)
- 镜像是**只读**的 (Read-Only)。
- 每一行 Dockerfile 指令 (RUN, COPY) 生成一层。
- 层与层之间通过联合挂载叠加。

### 容器层 (Container Layer)
- 容器启动时，在镜像层之上挂载一个**可读写层**。
- **Copy-on-Write (写时复制)**: 修改文件时，先从只读层复制到读写层，再进行修改。

## 4. 容器网络模型 (CNM)

### Bridge 模式 (默认)
- Docker 创建一个虚拟网桥 `docker0`。
- 容器通过 veth pair 连接到 `docker0`。
- 通过 NAT (iptables SNAT) 访问外网。

### Host 模式
- 容器与宿主机共享 Network Namespace。
- 性能最好，但端口易冲突。

### None 模式
- 只有 lo 网卡，无外网连接。用于高安全场景。
