---
title: Aether Pro 代码库核验报告（代码级事实层）
tags: [代码核验, 事实层, Aether, LoopAxis, 技术尽调, 自研度, v6.1]
status: active
updated: 2026-10-28
version: 1.0
source: C:\ai_agent\6aabb37206e22b5aaf95316f\loopaxis-pro-common-algo（dev 分支，HEAD a4358c2，2026-10-12）
---

# Aether Pro 代码库核验报告（代码级事实层）

> ⭐⭐ **这份文档的定位**：v6 用 [[100-物理AI产品与领域/010-产品与战略/BP事实核验与口径修正表]] 把 BP 的 22 页逐句核了一遍，
> 但那仍然是**文档级核验**——材料自己说的话能查，材料背后**实际做没做**查不了。
>
> **这份文档是第一次"看代码"**。它回答一个材料永远回答不了的问题：
> **"你说的话，代码里到底有没有？"**
>
> **核验日期**：2026-10-28
> **核验范围**：`loopaxis-pro-common-algo` 全仓（1398 个非 .git 文件 / 216 个 .py / 71 个 .rs / 324 个 .md / 228 个 .cu）
> **核验方式**：6 个域并行深读 + 关键结论逐条 grep 复核（本文所有判定均可指到 `文件:行号`）
> **排除项**：`aether/solve/warp/third_party/amgx`（NVIDIA AMGX 第三方，不计入自研）
>
> ⭐⭐ **一句话结论**：
> **代码比材料更保守。** 代码里藏着一批**没写进任何材料的真本事**（自研 GPU 拓扑优化内核、GPU 有限体积 CHT 求解器、手写 FNO/POD），
> 也藏着**比材料更硬的三处证伪**（GPINO 这个名字不存在、"5000+ 规范"差 20 倍、"不依赖 Abaqus"其实依赖了更不透明的 FEMAI 闭源二进制）。
> **但同时——材料里的核心卖点，一个都没被代码支撑。**

---

## 零、⭐⭐ 先看结论：六个域的自研度评级

| 域 | 代码规模 | 自研度 | 一句话定性 |
|---|---|---|---|
| **design/topology/algorithm** | 3,829 行 | ⭐⭐⭐⭐⭐ **高** | **完全自研的 GPU SIMP 拓扑优化内核**，零 dolfinx 依赖，配 Tet10 重网格 + 外部求解器交叉验证 |
| **solve/warp + solve/cht** | ~15,000 行 | ⭐⭐⭐⭐ **中高** | **自研 GPU 有限体积（TPFA）CHT 求解器** + 手写 AMGX ctypes 绑定；代码自述"不是完整 Navier-Stokes 验证" |
| **design/metamat** | 3,650 行 | ⭐⭐⭐⭐ **中高** | **自研渐近均匀化**（H8/Q4 能量法 + 周期 BC + PCG），文献定位准确；但 2D 版是稠密求解原型 |
| **design/control + optimization** | 6,478 行 | ⭐⭐⭐ **中** | 进程隔离/幂等/崩溃恢复/完成证明做得像生产系统；DOE 只有 LHS/factorial/OAT，参数优化是自研单目标 GA |
| **operator/physics_ai** | 1,987 行 | ⭐⭐⭐ **中** | **真训练能力**（Adam + MSELoss + 200 epoch + CUDA）；但标量侧 5 个模型全是 sklearn/xgboost 封装，场侧是手写 FNO/CNN |
| **geometry** | 8,771 行 | ⭐⭐ **低（2.5/10）** | **零自研内核**（全 FreeCAD/OCCT 或 CadQuery/OCP）；真正的自研是 1474 行**工程配合自动推荐** |
| **solve/cae + fenics + gmsh + femai + ondsel** | ~7,000 行 | ⭐⭐ **低** | **全是适配层**；CAE 域 3,900 行**不含任何 PDE 求解**，是"CAD 选择→离散边界条件"的翻译层 |
| **agent/claw (Rust)** | 57,362 行 | ⭐⭐ **低（真业务仅 1,558 行）** | 38,700 行 `runtime` crate 是外部开源 CLI 血统的通用框架；**29 个 action kind 服务端 0 实现** |
| **agent/cad (Python)** | 9,604 行 | ⭐⭐⭐⭐ **中高** | LangGraph 闭环 + **可执行的几何语义校验器** + 双层确定性兜底 + 274 篇自动沉淀的成功案例 |
| **data + core + mechanics** | 201 行 | ⭐ **纯占位** | `core` 7 行、`mechanics` 3 行（`__all__ = ()`），公共契约全在仓库外 |

> ⭐⭐ **这张表本身就是最重要的对外纪律**：
> **我们真正自研且有技术含量的，是"拓扑优化内核 + GPU 热流求解器 + 均匀化 + CAD Agent 编排"这四块；
> 而材料对外讲的是"物理 AI 平台 + 四物理场 + GPINO + 5000+ 规范 + C919 复材"。**
> **两者交集接近于零。**

---

## 一、代码库结构事实（可对外陈述的部分）

```
loopaxis-pro-common-algo   dev 分支 / HEAD a4358c2 / 2026-10-12
└── aether/
    ├── agent/      51 py + 57k 行 Rust   CAD Agent(3967, Python) + AICube Agent(3947, Rust)
    ├── core/       1 py / 7 行          占位
    ├── data/       5 py / 191 行        pickle 注册表 + DOE 投影
    ├── design/     52 py / 16,039 行    topology + metamat + optimization
    ├── geometry/   37 py / 12,476 行    selfcad(FreeCAD) + cadquery + snapshot
    ├── material/   3 py / 330 行        等效材料契约（version + provenance）
    ├── mechanics/  1 py / 3 行          占位
    ├── operator/   7 py / 2,092 行      physics_ai: POD / pernode / FNO / CNN
    └── solve/      59 py / 24,886 行    cae / cht / femai / fenics / gmsh / ondsel / warp(+AMGX)
```

| 事实 | 数值 | 证据 |
|---|---|---|
| 提交人数 | **6 人**（zhangyanshen 57 次、yanziming 4、femai 1、maojiawen 2、zhanghuajie 1） | `git shortlog -sne --all` |
| 最近 8 次提交主题 | **全部是 CAE 选点缺陷修复**，且每条标注"（与 backend 同步）" | `git log --oneline -25` |
| 唯一的决策记录载体 | **git 提交历史**（无 ADR / RFC / postmortem 文件） | `find -iname '*adr*' -o -iname '*postmortem*'` → 0 |
| 全仓文档中"对外材料/客户案例" | **0 份**（324 个 .md 里 279 个是 RAG 语料，44 个是工程文档） | 全仓检索 `sales\|case-study\|客户案例` → 误报 |
| 已知缺陷复盘记录 | 1 处具名：`cae_input.py:530-534` 注释 "prod334's defect lived in this step and was duplicated verbatim" | 代码注释 |

> ⭐ **这条信息本身是好消息也是坏消息**：
> **好消息**——近 8 次提交全在修"选区映射落错"这一类真问题，说明团队正在啃工程化最难啃的那块。
> **坏消息**——**仓库里没有任何一份客户案例材料**，所以 [[100-物理AI产品与领域/010-产品与战略/融资BP叙述手册]] 里那些"客户五档状态表 L0–L4"在代码侧完全找不到落点。

---

## 二、⭐⭐ 核心资产：15 条对外宣称的代码级核验

> **这是本文最重要的一节。** 每条判定都可以当场指着代码复核。

| # | 对外宣称 | 判定 | 代码证据 | 备注 |
|---|---|---|---|---|
| **1** | **GPINO / GPINN v2.1** | ❌ **名字不存在** | 全仓 `gpino\|gino\|deeponet\|neuraloperator` → **0 命中**；最接近是 `aether/operator/physics_ai/field.py:196` `SpectralConv3d` / `:225` `FNO3d` | **没有几何编码、没有物理残差项、没有 PINN 损失**。真实算法名是 **FNO**，不是 GPINO。⚠️ 被追问"GPINO 比 FNO 多了什么"时**无答案** |
| **2** | **预测置信度 96.8%** | ❌ **完全无据** | 全仓 `96.8\|0.968` → **0 命中**；`operator/physics_ai/` 内 `confidence\|uncertainty\|conformal\|coverage` → **0 命中** | 代码只产出 **R² / RMSE / MAE / nRMSE**（`field.py:448-460`）。**唯一近似 UQ 的是二元越界告警**（`ml_service.py:390-403`），不是概率化置信度 |
| **3** | **412 MPa** | ❌ **无据（量级合理）** | 全仓无 412；代码能输出 von Mises（`topology/.../validation.py:555`），但**无任何材料强度库**（`yield`/`allowable` 全仓 0 命中） | 是求解结果的**输出量**，不是标定值。且**无基准算例**（NAFEMS 全仓 0 命中），无从谈"标定" |
| **4** | **k = 0.5 W/(m·K)** | ⚠️ **量级差 1–2 个数量级** | 固体默认 **45**（`cae/application/cae_input.py:774`）；CHT 示例铝 **205** / 空气 **0.026**（`cht/unstructured/examples/gmsh_cht_pipeline.example.json:23`） | 0.5 既不是默认值也不是示例值。**最接近的是空气 0.026（低 20 倍）**。与 v6 判断一致：这不是金属散热器量级 |
| **5** | **追觅 42%→52% / 效率百倍** | ❌ **完全无据** | 全仓 `追觅\|dreame` → **0 命中**；`42%`/`52%` → **0 命中**；代码**只记耗时不产出加速比**（`amgx_backend.py:590/634/670` 的 `setup_seconds`/`total_solve_seconds`） | **整个客户案例在代码侧零痕迹**，连 274 篇 RAG 案例里都没有（全是通用 CAD 件） |
| **6** | **5000+ 规范/规则** | ❌ **量级差 20 倍以上** | 全仓 `5000` 仅 4 处命中，**全部无关**（STL 采样数 5000 / 文本截断 5000 / 树数上限 5000 / 测试热流值 5000） | 最实的三个真实数字：① **提示词编号规则 42 条**（`agent/cad/prompt/prompt_builder.py`）② **RAG 成功案例 274 个** ③ **行业知识 3 篇**（`agent/cad/rag/industry_docs/`，各约 23–24 条）。**没有一个接近 5000** |
| **7** | **C919 复材机翼 / 层合板 / 变刚度** | ❌ **完全无据** | 全仓 `c919\|复材\|机翼\|laminate\|orthotropic` → **0 命中**；`material/equivalent/model.py:63-64` **强制** `model == "isotropic-linear-elastic"` | **只支持各向同性线弹性**。最接近的是 MetaMat 点阵的**各向异性等效刚度张量**（6×6 Voigt，`homog3d.py`）——**那是周期均化，不是层合板本构** |
| **8** | **医疗骨科** | ❌ **完全无据** | 全仓 `orthopedi\|implant\|应力屏蔽` → 唯一命中是 **1 个 RAG 案例文件名**（"创建一个骨科接骨板示意模型"） | 无骨密度、无多孔本构、无应力屏蔽分析。**骨科在代码里的全部存在 = 一个 CAD 语料文件名** |
| **9** | **接触力学 / 装配 mates 变运动学** | ⚠️ **仅 deck 级语法，运动学为零** | 接触只写进 INP 关键字（`cae_input.py:877-881` `*Contact Pair`），但 **`cae_input.py:1278` 明确把接触挡在 FEniCS 之外**；`aether/mechanics/` 是空壳 | 装配 mates 有真 Ondsel 路径（`solve/ondsel/freecad_ondsel_solver.py`，含 9 种 joint + DOF 削减表 + 结果码翻译），但**不存在"mates→运动学方程→位移求解"链路** |
| **10** | **神经算子 / ROM / 代理模型加速** | ✅ **真实实现（本仓最扎实的一条）** | **FNO**：`field.py:196-240` 真 PyTorch 谱卷积（`rfftn` + 4 组复权重 + 逆变换）；**POD/ROM**：`field.py:97` 经济 SVD；**CNN**：`field.py:242`；**持久化有测试**：`tests/test_torch_persistence.py` | 代理模型替代重复 CAE 求解**是真的**。但要说清边界：FNO 需 torch+CUDA，且输入需重采样到结构化网格；**网格一致是前提**（`field.py:10` 明写）。⚠️ 建议话术落在 **FNO/POD**，不要落在 GPINO |
| **11** | **多物理场耦合** | ⚠️ **2 场弱耦合** | CHT 双向耦合**真实**（`cht/unstructured/unstructured_gmsh_v1.py:1836-1945` 松弛迭代 + `:1796` 浮力 + `:961-967` 谐波界面导热，**有解析解单测** `tests/test_unstructured_gmsh.py:205`） | **热↔流（Boussinesq）弱耦合，固体应力不参与**；`:1998` 明写 "flow_model: Stokes/Boussinesq MVP; momentum advection is not implemented"。**热-力耦合全仓不存在** |
| **12** | **不依赖 Abaqus / 自主可控** | 🔴 **代码反证（结论要改口径）** | `aether/solve/abaqus/` **目录已删**（git 历史亦无）→ 确实不用 Abaqus。**但**：真正在跑的是 **FEMAI 闭源二进制**（`solve/femai/README.md:5` "separately supplied runtime dependency"，仓库内无源码）；**且 `solve/cae/package.json:7-8,11-12` 仍引用已删的 `../abaqus/server.mjs` 等 4 处悬空路径** | ⭐ **正确口径不是"不依赖 Abaqus"（那反而是真的），而是"依赖了另一个更不透明的闭源自研求解器 FEMAI"**。拿掉 Abaqus 当卖点，等于把提问引向"FEMAI 源码在哪、谁控制它"——**那是比 Abaqus 更难答的问题** |
| **13** | **网格无关性 / 网格收敛验证** | ❌ **完全无据** | 全仓 `mesh.?converg\|Richardson\|h.?refine\|网格收敛` → **0 命中** | 仓库有**优秀的求解收敛性纪律**（"Worker 完成 ≠ 物理收敛"，`solve/warp/README.md:56-58`；迭代上限不得被粉饰成收敛，`cht/application/executor.py:106-125`），但**求解收敛 ≠ 网格无关性**，两者不可混为一谈 |
| **14** | **并行 / 分布式求解** | 🔴 **代码反证** | **三处任务队列全部 `max_workers=1`**（`design/topology/control/topopt_control_service.py:199`、`design/topology/service/topopt_service.py:41`、`solve/warp/warp_solver/service.py:44`）；无 `torch.distributed`/`mpi4py`/`celery`/`ray`/`slurm` | GPU 加速**真实**（CUDA kernel + AMGX 设备端 CSR 求解），但**单机单卡**。FEMAI 可传 `-n` 进程数，**默认 1** |
| **15** | **精度标定 / 试验对标 / 与实测比对** | ❌ **完全无据** | 全仓 `nafems\|ostergard\|对标\|实测\|试验` → **0 命中** | 存在的只是**内部守恒/残差验证**（真残差 `_true_residual`、界面不渗透、开放边界能流、谐波导热解析解）。这是真工程亮点，但**它不是精度标定** |

### 2.1 判定汇总

| 判定 | 条数 | 编号 |
|---|---|---|
| ✅ 真实实现 | **1** | 10 |
| ⚠️ 部分对应 / 需改口径 | **4** | 4、9、11、12 |
| ❌ 完全无据 | **10** | 1、2、3、5、6、7、8、13、14、15 |

> ⭐⭐ **这张表要做的唯一一件事，就是让"哪些话不能说"从"感觉"变成"有据"**：
> 之前 [[100-物理AI产品与领域/010-产品与战略/BP事实核验与口径修正表]] 核出的是 7 处硬伤（材料层面），
> 现在补上了**材料背后的 10 处无据**（实现层面）。
> **两者叠加 = 12 处硬伤 + 4 处需改口径。**

---

## 三、⭐ 代码能支撑的最强叙事（3 条，全部可指着代码讲）

### C1｜"GPU 加速的共形网格热流耦合求解器，且不拿 CPU 回退冒充 GPU 结果"

- **真实 CUDA kernel**：`solve/warp/warp_solver/algorithms/unstructured_cht/vendor/unstructured_warp_kernels.py`（503 行）
  温度、动量、守恒面通量、压力投影、收敛归约**全在 device 上跑**
- **真实 AMGX 设备端求解**：`amgx_backend.py` 手写 `ctypes` 绑定（761 行），FGMRES + AGGREGATION AMG，`BLOCK_JACOBI` 平滑，松弛 0.8
- ⭐ **工程诚信的硬证据**：`solve/warp/README.md:35-36` 明文承诺
  > "It does **not silently substitute a CPU solver or an unvalidated GPU Jacobi iteration** after failure."
  `plugin.py:110` 真实区分 `accelerated` vs `cpu_fallback` 并写入报告
- **真残差验证**：不信递归残差，直接算真残差
- **谐波界面导热有解析解单测**：`expected = 0.5/(0.25/1.0 + 0.25/10.0)`

> ⭐ **这一条是全仓最经得起技术尽调的叙事**，而且**没有写进任何材料**。

### C2｜"自研 GPU 拓扑优化内核，含 Helmholtz PDE 滤波 + 混合 level-set 精修 + 外部求解器交叉验证"

- **依赖表只有 meshio / numpy / scipy / warp-lang**（`design/topology/algorithm/pyproject.toml:10-15`）→ **零 dolfinx / FEniCS**
- **matrix-free P1 Tet4 弹性组装**（`kernels.py:48-80`，`wp.atomic_add` 散射，无稀疏矩阵）
- **Helmholtz PDE 滤波 + CG 伴随**（`filter.py:43-82` + `optimizer.py:474-534`）——**这是 2020 年后才成熟的技术路线**，多数工业软件仍用密度滤波
- **tanh 投影 + 解析导数**（`kernels.py:163-182`）
- **OC 优化器 + 自适应 move limit + continuation**（`optimizer.py:702-815`）
- ⭐ **`validation.py`（646 行）是全仓工程含金量最高的一块**：Tet10 重网格 + 闭合 2-流形校验 + 可定向性 BFS + 写 Abaqus INP + 调 FEMAI 外部求解器**交叉对拍**——**多数同类产品不做这件事**
- ⚠️ **但**：制造约束（拔模/最小特征尺寸/悬垂）**全域 0 命中**，物理场只有静力

### C3｜"AI 代理模型真的能替代重复 CAE 求解"

- 真 FNO（`field.py:196-240`）+ 真 POD（`field.py:97`）+ 真 CNN（`field.py:242`）
- **真训练能力**：Adam + MSELoss + 200 epoch + CUDA 自动选卡 + CPU `state_dict` 持久化（`field.py:277-297`）
- **真代理加速闭环**：`design/optimization/.../parametric_optimization.py:182-184` 声明依赖 `physics-ai.ml.scalar-predict`，**整个 GA 种群走 ML 代理，不跑 CAE**（`:473-484`），且**强制校验代理与 DOE 数据集共享同一 `datasetSignature`**（`:378-385`）
- **精度指标真实计算**：`field.py:448-460` 返回 `{r2, rmse, nrmse, maxError, peakMae}`
- ⚠️ **必须承认的边界**：样本 < 8 时**训练集即评估集**（`ml_service.py:307-310`）→ 前端显示的 R²=0.99 可能是自评分

> ⭐ **这三条合起来，是"我们真的做过硬工程"的证明——但都不是材料在讲的那几条。**

---

## 四、⭐ 代码证伪的最强叙事（3 条）

### R1｜"自主可控的工业 CAE 求解内核" —— 真正的问题不是 Abaqus

- Abaqus 求解器**确已移除**（目录已删，git 历史亦无）
- **但 INP 就是 Abaqus 关键字格式**（`*Node`/`*Element`/`*Material`/`*Elastic`/`*Contact Pair`）
- **真正在跑的是 FEMAI 闭源二进制**：`solve/femai/README.md:5` + `femai/Dockerfile:1-4`（须挂载或经 `FEMAI_COMMAND` 注入），**仓库内零源码**
- **`solve/cae/package.json:7-8,11-12` 仍有 4 处指向已删目录的悬空引用** → `npm run check` / `npm test` 直接失败
- **FEniCS 侧主动保留 Abaqus 契约**：`fenics_service.py:3-7` "intentionally preserves the old Abaqus HTTP contract"

> ⭐ **口径改法**：从"不依赖 Abaqus"改成
> **"求解器内核完全自研（FEMAI），Abaqus 只是已停用的历史后端与交换格式"**——但**这句话只有在能出示 FEMAI 源码归属时才敢说**。

### R2｜"多物理场 + 分布式并行" —— 双重证伪

- **耦合实际只有热↔流**，弱耦合松弛迭代，**固体应力不参与**
- **并行度 = 1**：三处队列全 `max_workers=1`
- ⚠️ **而 `solve/warp/README.md:52-55` 已主动列出不支持清单**（瞬态 / 辐射 / 湍流 / 非共形接触 / 非正交修正）
  → **代码比材料更保守，一旦被要求对照 README，逐条都暴露**

### R3｜"物理 AI Agent 的工具编排" —— 29 个 action，服务端 0 实现

- **29 个 action kind 白名单**在 `agent/claw/crates/claw-solid-agent/src/lib.rs:1119-1150`
- **逐个全仓检索，服务端实现数 = 0**；命中只在系统提示词与单元测试里
- **不是原生 function-calling**：`lib.rs:644-654` 请求体 `tools` 字段为 `None`；靠 `rest.find("```solid_action")` 抠代码块（`:1092`），兜底还会把文本里任意 `{...}` 当 action 解析（`:1100-1106`）
- **`action_result` 记了但从不回灌上下文**（`:571-594` 存 vs `:621-639` 只读 transcript）→ **不是多轮 agent，是单轮建议器**
- **审计规范（`report_schema.rs` 552 行）零生产调用方**；`ReportConfidence` High/Medium **无任何判定逻辑**
- ⚠️ **`agent/cad/rag/` 顶层目录（3 篇行业知识 + BOSL2 工具文档）是死资产**，检索实际走 `agent/cad/context/rag/`

---

## 五、逐域自研度详评（要点摘录）

### 5.1 solve 域 —— 唯一自研数值内核在 Warp，但它是有限体积不是有限元

| 后端 | 自研行数 | 性质 |
|---|---|---|
| **warp + cht** | **~15,000** | ⭐ **自研 GPU 有限体积 TPFA + 一阶迎风 CHT**，配 AMGX |
| cae | ~3,900 | **0 行 PDE 求解**——是"CAD 选择→网格边界条件"翻译层 + 质量闸门 |
| gmsh | ~2,300 | 薄适配（内核是 OpenCASCADE/Gmsh） |
| fenics | ~1,570 | UFL 封装 DOLFINx；自研仅 `recover_mises` 等约 300 行 |
| femai | ~1,120 | **纯外部可执行封装** |
| ondsel | ~510 | FreeCAD subprocess 壳 |

**关键判据**：
- `warp_cht_solver.py:722` 自述 `discretization: seven_point_upwind_finite_volume` —— **不是有限元**
- **物理范围**：稳态层流 Boussinesq / 低马赫理想气体；**无湍流、无瞬态（仅结构化路径）、无辐射（非结构化路径）**
- ⭐ **但代码诚实**：`unstructured_warp.py:909` 自己写 `"this is not a complete Navier-Stokes validation"`
- ⭐ **伪收敛防护是亮点**：`unstructured_warp.py:748-751` 明确用**未松弛的 fixed-point 更新量**判收敛，并配回归测试 `test_warp_native_numerics.py:368-383`

**CAE 域的真实贡献（可对外讲的工程细节）**：
- 受载面积闸门：匹配面积必须落在几何标注面积的 **90%–110%**（`cae_input.py:31-32` `_AREA_GATE_LOW/HIGH`），否则阻断
- 面选点三级回退：`override` → `selectionMappings` → 几何包围盒共面判据；歧义显式告警
- 平面容差 = **模型对角线 × 1e-6**（`:205-206`），且注释记录了事故复盘（prod334）

### 5.2 design 域 —— 内核硬、边界软、契约断线

- ⭐ **control 层做得像生产系统**：进程组 SIGTERM→SIGKILL 升级、fsync 持久化、幂等 hash 绑定（SHA256 canonical JSON）、崩溃恢复、取消墓碑、**completion attestation**（公共产物先 fsync 再提升为 done）、**32 个针对性测试**
- ⭐ **但**：GPU 调度只是 **单卡单并发**（`ThreadPoolExecutor(max_workers=1)`），无多卡池化、无作业级超时看门狗
- ⚠️ **静默降级**：`design/topology/application/.../object_reference.py:639-655` 把**热边界丢弃**、把**对称/部分位移约束降级为全固定**——只发 warning，用户会拿到"物理上错误但看起来算完了"的结果
- 🔴 **架构断线**：`material/equivalent` 契约设计专业（版本 + provenance + 手写 Cholesky 正定性），但 **mechanics 域是空目录、solve 域不消费它** → MetaMat 算出的 C^H 无处可去
- 🔴 **`design/topology/algorithm/` 3,829 行数值内核，零自动化测试**

### 5.3 geometry 域 —— 零内核，但有 1474 行真本事

- **两个第三方内核并存**：SelfCAD 走 FreeCAD/OCCT（子进程调 `freecadcmd`），CAD-Agent 走 CadQuery/OCP
- ⭐ **最有价值的自研**：`freecad_mate_candidates.py`（1,474 行）——解析曲面提取（圆柱/圆锥/球/平面 + 49 点最小二乘拟合螺旋）+ **6 类配合候选打分** + **M8 螺纹语义匹配** + 多孔孔距谱匹配
- ⚠️ **Healing 只有一种形态**：`freecad_cae_publisher.py` 里面向 CAE 的 BOP 修复（`removeSplitter` + fuzzy fuse + 无效面重建），**无缝合/补洞/小面合并**；修复报告**只写盘从不读取**；失败 `except: pass` 静默
- ❌ **无 Persistent ID**：`persistent_id\|v5_uuid\|EntityExternalIds\|CAx-IF` 全仓 0 命中。`stable_key` 只写不读且 **STEP 导入路径没有**
- ⭐ **但 solve 域有等价的"几何签名匹配"**（`cht/unstructured/gmsh_cht_pipeline.py:400-406` 注释直说：
  > "Entity ids are not stable across OCC imports or fragments, while a face signature (bbox, centroid, measure and normal) is stable"
  ）含容差、评分（0.30/0.30/0.20/0.15）、消歧（<0.75 拒绝、top1-top2 差 <0.05 判歧义）
  → ⭐ **这是"几何语义→物理场"护城河最接近的现有实现**，只是还没提到几何域

### 5.4 operator + data 域 —— 真训练、零 UQ、壳级数据层

- 标量侧 5 个模型**全是 sklearn/xgboost/lightgbm 封装**（`ml_service.py:199-241`）
- 场侧 FNO/CNN 是**手写 PyTorch**（未用 neuraloperator 库），结构与 Li et al. 2021 的分支算子 FNO **不同**
- ⭐ **命名夸大**：`operator/physics_ai/__init__.py:1` 写 "Physics-informed scalar and field learning operators."，但**全仓无任何 PINN 实现**
- data 层仅 118 行：DOE dict 投影 + pickle 注册表；**真正的 Dataset/ModelVersion/Provenance 权威在仓库外的 `aether_runtime`**
- **无 ONNX/PT 持久化**，只有 pickle

### 5.5 agent 域 —— Python 侧是真闭环，Rust 侧是提示词编排

- ⭐ **Python CAD Agent（3967）**：LangGraph 11 节点闭环（intent→domain→RAG→plan→generate→render→静态检查→几何/视觉校验→judge→repair→export）
  - **可执行的语义校验器**（`agent_v2/validator.py`）：包围盒 / 单一实体 / 孔必须减材 / 孔数 / 孔径 / 四角孔位，容差 `max(0.5, edge_margin×0.05)`
  - **评分权重** 0.35/0.25/0.25/0.10/0.05，**语义失败强制封顶 0.49**（阈值 0.75）→ 语义检查是硬门槛
  - **双层确定性兜底**：LLM 全挂仍能出"带 4 孔的箱体"或"L 型支架"
  - **274 篇自动沉淀的成功案例**（`context/rag/enterprise_memory/`，每次成功运行自动写入，含需求+可跑源码+run_id）
- ⚠️ **但 `agent_v2/` 不是生产路径**：生产走 `flow/`，`main.py:13-15` 注释明写 "never make it the production meaning of 'v2'"；**且 flow 路径没有 deterministic rescue，校验器不可用时默认放行**
- ❌ **Rust 侧 29 个 action 服务端 0 实现**；38,700 行 runtime 是外部开源 CLI 血统（`~/.local/share/opencode`、`DEFAULT_APP_NAME = "claude-code"`）

---

## 六、⭐ 五个"当场答不上来"的追问（附补救）

| 追问 | 现状 | 补救 |
|---|---|---|
| **① "GPINO 架构讲一下？"** | 名字不存在 | **先改材料**：GPINO → FNO/POD。然后讲 `field.py:196-240` 的谱卷积细节（这是真本事） |
| **② "412 MPa 怎么标定的？和实测对过吗？"** | 无强度库、无基准、无实测 | 讲 **`maximum_von_mises` 是求解输出量**，并**立刻补 NAFEMS 静力基准**（本库 P0 已列） |
| **③ "追觅那个案例，数据在哪个文件？"** | 全仓零痕迹 | **材料里不要写这个客户名**，或补一份脱敏案例说明 |
| **④ "百倍效率，哪个基准测出来的？"** | 只记耗时、无对照数据 | 按 `solve/warp/README.md:67-73` 的测量纪律（要含完整外迭代、全场上传、区分 JIT 预热与暖态）**真测一次并把数据放进仓** |
| **⑤ "三处耦合 + 分布式并行，画个架构图？"** | 耦合只有热↔流；并行度=1 | **直接引用 `solve/warp/README.md:52-55` 的不支持清单**——把"我们不做什么"讲成专业性 |

---

## 七、⭐ 立即可修的工程瑕疵（低成本、高回报）

> **这三条与叙事无关，但影响"专业度"的第一印象**，且都是分钟级修复。

| # | 问题 | 位置 | 修复动作 |
|---|---|---|---|
| **1** | 🔴 **`package.json` 4 处悬空引用已删除的 `../abaqus/`** → `npm run check` / `npm test` 直接失败 | `aether/solve/cae/package.json:7-8,11-12` | 删掉 4 处引用并重跑 check |
| **2** | 🔴 **MinIO 明文 access/secret 进仓库** | `aether/geometry/selfcad/README.md:35-36`（`admin` / `Femai@2025GF2re31~`）+ `minio_storage.py:66` 硬编码 endpoint | 立即轮换密钥；README 脱敏 |
| **3** | 🟡 **`DOMAIN_CONFIG_PATH` 默认路径错误** → 不设环境变量则整个 CAD Agent 起不来 | `agent/cad/core/config.py:119-121`（默认 `runs/domain_config.json`，真实在 `configs/`） | 改默认路径 |

**另有一处需澄清（非缺陷，但是命名陷阱）**：
`operator/physics_ai/__init__.py:1` 自称 "Physics-informed" 但无 PINN 实现 → 建议改为 "Physics-domain scalar and field learning operators."

---

## 八、与既有文档的冲突与修正

| 既有结论 | 位置 | ⭐ 代码级修正 |
|---|---|---|
| "GPINO 是自研算子，存在命名混淆风险" | [[100-物理AI产品与领域/020-领域知识/领域知识索引]]（§v6 结论修正表） 修正 #7 | ⭐ **风险不是"混淆 GINO"，是"这个名字代码里根本没有"**。真实算法是 FNO/POD |
| "自研 vs 现成的 6 种架构决策表" | [[100-物理AI产品与领域/010-产品与战略/CTO技术战略与架构决策]] | ⭐ **决策表需要一个新维度：代码已经证明了什么**。自研的实际是：拓扑优化内核 / GPU 有限体积 CHT / 渐近均匀化 / CAD Agent 编排 / 几何签名匹配 |
| "护城河 = 几何语义→物理场联合训练闭环" | 同上 | ⭐ **代码里已有闭环的"前半段"**：几何签名匹配（含消歧+置信度）已实现并被 CAE 域消费。缺的是"后半段"——它还没进几何域、还没进 CAx-IF |
| "客户五档状态表 L0–L4" | [[100-物理AI产品与领域/010-产品与战略/融资BP叙述手册]] | ⭐ **仓库里 0 份客户案例材料**。这张表的证据在 CRM/销售侧，不在代码仓 |
| "CA 是我方 P0 缺口（精通主流 CAE 软件）" | [[700-职业档案/20-能力与证据/能力证据矩阵]] | ⭐ **代码仓是一个可核验的补强载体**——见 [[700-职业档案/20-能力与证据/能力证据矩阵#22-代码资产作为可核验技术证据]] |

---

## 九、⭐ 从代码里能提炼的三条"产品级"判断

1. ⭐ **"我们最强的自研不在求解器，在拓扑优化内核与 CAD Agent 编排"**
   → 这两块是**国内同类公司少见的扎实**（Helmholtz 滤波 + 外部求解器对拍 + 可执行语义校验器 + 274 篇自动沉淀案例）。
   → 但**它们目前没有出现在任何一份对外材料里**。这是最大的表达层浪费。

2. ⭐ **"代码的诚实度高于材料"——而这恰好是最有说服力的资产**
   → `solve/warp/README.md` 主动列不支持清单；`mechanics/README.md` 主动声明"不宣称独立力学引擎"；
   → `data/physics_ai/README.md` 主动声明 pickle 注册表"绝不可当权威模型目录"；`solve/femai/README.md` 主动披露外部二进制依赖；
   → `cht/unstructured/README_zh.md` 主动标注"本包未注册平台 capability"。
   → ⭐ **在投资人尽调里，"明确说自己不做什么"比多说十个能力更有说服力。**
   → **建议：把这句话写进 BP 的技术章节，并让技术负责人背书。**

3. ⭐ **"最该补的三件事，投入产出比最高"**
   ① **NAFEMS 基准集 + 网格无关性回归流水线**（本库已列 P0）——它是把"能算"变成"敢签字"的唯一路径，且**代码已有守恒/残差验证的骨架，缺的是外部锚点**；
   ② **拓扑优化制造约束层**（最小特征尺寸 + 拔模 + 悬垂）——这是"能演示"与"能用于实际生产"的分界线；
   ③ **FEMAI 内核的对外可解释性**——它是"自主可控"叙事唯一的软肋，必须先想清楚怎么回答"源码在谁手里"。

---

## 🔗 相关

- [[README|库首页]]
- [[100-物理AI产品与领域/010-产品与战略/BP事实核验与口径修正表]] ⭐ **材料级核验（7 处硬伤）** ← 本文是**实现级核验（10 处无据）**
- [[100-物理AI产品与领域/010-产品与战略/CTO技术战略与架构决策]] ⭐ **组织层：本文提供的代码事实应回填该文的架构决策表**
- [[100-物理AI产品与领域/020-领域知识/领域知识索引]] ⭐ **索引**
- [[100-物理AI产品与领域/020-领域知识/物理AI技术路线全景]]（6 主线 24 子路线，本文提供路线落地度的代码证据）
- [[100-物理AI产品与领域/020-领域知识/仿真可信度V-V与标准体系]]（NAFEMS / 网格无关性——本文第 15 条判定直接指向该缺口）
- [[100-物理AI产品与领域/020-领域知识/CAD与几何工程]]（几何签名匹配是 Persistent ID 的现有等价物）
- [[700-职业档案/20-能力与证据/能力证据矩阵]] ⭐ **代码仓作为可核验技术证据**
