---
title: CAD与几何工程
tags: [CAD, 几何, 网格, 内核, STEP, 几何深度学习]
status: active
updated: 2026-10-26
---

# CAD 与几何工程

> **这是几何侧的基础课，也是物理 AI 落地的真正入口。**
> CAE 的失败有 80% 源于几何本身有缺陷，而不是求解器不行。
> 上一版知识库完全没有这一层——这是最大的空白。

---

## 一、⭐ 几何清理（Healing）：CAE 前处理 60%+ 工时所在

### 1.1 为什么缺陷的代价是数量级的

一个可复核的对照实验（**技术邻《有限元网格避坑③》**）：

> 仅引入 **3 个小面 + 1 条小缝** → 最小面面积比干净模型小 **5 个数量级**
> → 单元数约 **2×**、核时约 **4×**、非正交质量 **86 → 77**

> ⭐ **含义**：几何缺陷不是"小问题"，它会把后处理成本放大一个数量级。
> **在 AICube 的入口做 healing，比在求解器里做加速更有杠杆。**

### 1.2 专家的必做操作清单（按工具链归位）

| 环节 | 工具 | 具体操作 |
|---|---|---|
| **诊断** | Abaqus `Tools → Geometry Diagnostics` | 勾选 Invalid entities / Short edges / Small faces / Slivers / Coincident edges / Free edges |
| **缝合** | OCCT `BRepBuilderAPI_Sewing`；CATIA `Healing`（Merging Distance、Domain Distance）；Hexagon Apex `Geometry Cleanup → Clean Topology` | 按最大间隙设容差，**逐步增大而非一次到位** |
| **小特征移除** | Hexagon `Find and Fix Small Features`：Small Edges / Small Face / Sliver Surface / Spike Surface / Sheet Body Crack | 尺寸阈值需**小于全局网格尺寸的 1/5** |
| **去细节（defeature）** | Ansys Meshing `Defeature Size`；CADfix CAE；Cubit 的 `reduce` 命令（用 ML 对螺栓、弹簧做快速简化） | 只抑制对目标物理量无影响的倒角/螺纹/小孔 |
| **虚拟拓扑** | Abaqus `Tools → Virtual Topology → Assign` | 合并小面/短边**而不改实体** |
| **自相交检测** | OCCT `BRepAlgoAPI_Check`；`BRepCheck_Analyzer` | 报 `BRepCheck_SelfIntersectingWire` 等 |
| **尖角规整化** | 加倒角（把奇异转成应力集中）或 partition | **直接决定 meshing 是否失败** |

> ⭐ **对清航飞迈的直接启示**：
> AICube 的"宽入口建模层"如果要做 CAD 特征入口，**必须内置 healing + defeaturing 层**，
> 否则用户传来的 STEP 会在网格阶段直接炸掉。
> 官方宣称的"仿真速度提升 80%"里，**几何预处理这一段是绕不开的工程量**。

---

## 二、几何简化 vs 精度：如何量化

### 2.1 双向守恒检查

- **CAD → 仿真几何**（defeature）用**双向 Hausdorff 距离 + 体积/面积守恒**
- CADfix 的 `Protect Proprietary Shapes (PPS)` 是"生成简化外包络、保留功能意图、不泄露内部设计"的商业实现

### 2.2 几何简化误差度量标准组合

| 度量 | 含义 | 何时用 |
|---|---|---|
| **Chamfer Distance (CD)** | 生成任务主流指标 | CAD 生成模型评测 |
| **Hausdorff 距离** | 最坏情况，捕捉局部偏差 | 简化守恒检查 |
| **surface distance F1** | 同时惩罚偏差与覆盖不足 | ⭐ **CADGenBench 采用，最接近工业需求** |
| **volume IoU (256³ 体素)** | 体积重叠 | 配合 surface F1 使用 |

### 2.3 ⭐ 三维判据：几何拓扑不变量

| 不变量 | 含义 | 用途 |
|---|---|---|
| **Betti 数 (b₀, b₁, b₂)** | 连通分支数 / 环数 / 壳数 | ⭐ **CADGenBench 用它做 topology match 轴**；b₁ 变化 = 拓扑变了（打孔/挖槽）；b₂ 变化 = 壳变了 |
| **欧拉数 χ = b₀ − b₁ + b₂** | 亏格相关 | 快速判"这一刀是不是把环打开了" |
| **Manifold 性** | 每条边恰被 2 个面共享、方向相反 | **非流形 = 大多数 CAE 求解器直接拒绝** |
| **亏格 (genus)** | 洞数 | 拓扑不变性检测的基础 |
| **体积/面积/质心/惯性矩** | 质量属性 | **STEP AP242 的 Validation Properties 就是这组**；跨格式传递后必须守恒 |

---

## 三、CAD → CAE 链路：格式级缺陷签名表

> **这张表可以直接做成 AICube 的入口预检规则。**

```
原生 CAD (CATIA/NX/Creo/SolidWorks)
   │  ← 失效点①：内核不同（Parasolid / ACIS / CGM）→ 拓扑重建、容差不一致
   ▼
中性几何 STEP AP242 (.step/.stp)  ← 失效点②：装配树扁平化、实例丢失、容差不一致
   │  ← 失效点③：PMI 语义与几何分离；Validation Properties 缺失
   ▼
导入前处理（CADfix CAE / Hexagon / SpaceClaim）
   │  ← 失效点④：defeature 阈值选择；中面(mid-surface)提取；虚拟拓扑
   ▼
网格生成器（Gmsh / Salome SMESH / Netgen / TetGen / Cubit / HyperMesh / ANSYS Meshing / Simcenter）
   │  ← 失效点⑤：小面/缝隙/尖角 → sliver/针状单元、单元数疯涨
   ▼
求解器 (Abaqus / ANSYS / LS-DYNA / CalculiX / Elmer / Code_Aster)
```

| 格式 | 典型缺陷签名 |
|---|---|
| **STEP** | 缝合缝隙、系统间容差不一致、导出时实例丢失、装配结构扁平化 |
| **IGES** | 未缝合曲面、sliver、高阶 NURBS、缺面、自相交频繁 |
| **JT** | B-rep 导入失精、模型退化为仅 tessellation、PMI 元数据不完整 |
| **Parasolid** | 非流形模型、重复 body、装配构建历史不一致 |
| **ACIS** | 边连接不良、实体不完整、sliver、随 SAT 版本变化的 NURBS 不稳定 |
| **IFC** | 几何碎片化、非水密 body、复杂 BIM 结构冗余实体、对象间容差不一 |

> 来源：[CADfix DX 格式×缺陷矩阵](http://www.cadinterop.com/en/your-needs-cad/cad-repair-and-healing.html)

---

## 四、⭐ 网格质量阈值表（专家会建立的三档基线）

> 专家不会只看求解器 PASS/FAIL，而是建立**理想 / 可接受 / 拒收**三档阈值，
> 并把"几何缺陷"与"网格质量"关联起来。

| 指标 | 理想 | 可接受（通过） | 拒收（失败） |
|---|---|---|---|
| 长宽比 AR | 1 | ≤3~5 | >20（关键区 >10 警觉） |
| 偏斜度 Skewness | 0 | ≥0.9 | >0.85 |
| 雅可比比 Jacobian | 1.0 | 常规 ≥0.3~0.5 | ≤0（负雅可比 = 翻折） |
| 翘曲 Warpage | 0° | >15°（壳 >10°） | — |
| 锥度 Taper | 0 | ≤0.4~0.5 | >0.4（静强度） |
| 内角 Min/Max | Tri 60° / Quad 90° | Tri 30°~120°；Quad 45°~135° | 超出范围 |
| 正交质量 | 1.0 | 0.5~1.0 | — |
| 形状因子 | 1 | ≥0.3 | — |
| 相对尺寸偏差 | 1 | ≤1.5~2 | >2（局部突变） |

### HyperMesh 侧对应阈值
长宽比通用 ≤5:1 / 关键区 ≤3:1 / 非关键 ≤10:1；
雅可比（高斯积分点）≥0.7、关键区 ≥0.8；
内角三角面 30°~150°、四边面 45°~135°；
弦偏差一般 5%~10%、高精度曲面 ≤3%；
四面体坍塌 ≥0.15、高质量 ≥0.3。

### ⚠️ 不同求解器口径不一致（踩坑高发区）

| 坑 | 说明 |
|---|---|
| **ANSYS "Orthogonal Quality" vs Abaqus "Jacobian"** | 同一网格两套报告可能给出不同"合格"结论 → 跨软件协作必须明确各自标准 |
| 二阶单元更敏感 | 同几何下二阶通常更差，但不代表不可用 |
| **显式动力学极敏感** | 时间步长受最小单元尺寸控制，1:50 长宽比可把全局时间步长拉低几个数量级 |
| 完全积分实体 | 显式计算中应避免：积分点之一可能负雅可比而整体仍正体积 |

### ⭐ 专家的三步工作流（可固化为 CI）

1. **预检几何**：修复微小边、窄面、非流形 —— "**80% 的网格失败源于几何本身有缺陷**"
2. **渐进式划分与评估**：先粗网格跑通 → 检查质量报告 → **只针对不合格区域局部加密/重画**（不要全局加密）
3. **结果反查**：应力/变形云图**叠加网格质量云图**；若关键位置网格质量差，该处结果必须标注"不确定"

### 网格收敛
同一模型 3 档（粗/中/细）求解，关键输出量（应力/变形/固有频率）收敛到 **<1–2%** 才认为可信；
并做**网格质量-结果敏感性分析**（在不良单元附近加密，看结果是否漂移）。

---

## 五、几何深度学习：完整谱系（编号已逐条核实 ✅）

### 5.1 网格 / 点云类

| 论文 | arXiv | 状态 |
|---|---|---|
| MeshCNN: A Network with an Edge | `1809.05910` | 已发布 |
| PD-MeshNet | `2010.12455` | NeurIPS 2020 |
| MeshGraphNets | `2010.03409` | ICLR 2021（DeepMind） |
| **Deep Marching Tetrahedra** | ✅ **`2111.04276`** | ⚠️ 常见误引为 2202.03372（那是粒子物理） |

### 5.2 CAD 序列生成类

| 论文 | arXiv | 状态 / 关键结论 |
|---|---|---|
| DeepCAD | `2105.09492` | ICCV 2021；自定义 token 词表；数据集 179,133 模型 |
| SketchGraphs | `2007.08506` | ICML 2020 Workshop；**1500 万**草图 |
| Text2CAD（文本→序列） | `2409.17106` | **NeurIPS 2024 Spotlight** |
| Text2CAD（工程图→3D） | `2411.06206` | ⚠️ **同名两篇，须区分** |
| **CAD-Recode** | `2412.14042` | ICCV 2025；用 **CadQuery Python 代码**；mean CD **0.30** / IoU **92.0%** / IR **0.4%** |
| **cadrille** | `2505.22914` | **ICLR 2026 Oral**；多模态 + 在线 RL |
| CAD-Llama | `2505.04481` | LLM 直出参数化 CAD |
| CAD-Coder | `2505.19713` / `2505.14646` | CoT + 几何奖励（⚠️ 同名两篇） |
| CADReview | `2505.22304` | ACL 2025 Main；自动审查 + 纠错 |
| **Computer-Aided Design as Language** | `2105.02769` | NeurIPS 2021；⭐ **"CAD 本质是程序合成"这条论断的原始出处** |
| STEP-LLM | `2601.12641` | DATE 2026；自然语言 → CAD **STEP 模型** |
| Clarify Before You Draw | `2602.03045` | ICML 2026；主动澄清歧义 |
| CADIR | `2608.00891` | 跨后端可编辑中间表示 |
| ReliCAD | `2609.22325` | 不确定性 LLM → 可靠参数化 CAD |
| Zero-to-CAD | `2604.24479` | ⭐ 配套 **Zero-To-CAD-1m** 数据集（~100 万几何验证过的 CadQuery 程序） |

> ⭐ **2026 年这批工作的共同特征：都退回"生成可执行代码 + 内核校验"。**

### 5.3 B-rep 类

| 论文 | arXiv | 状态 / 关键结论 |
|---|---|---|
| UV-Net | `2006.10211` | CVPR 2021 |
| **BRepNet** | `2104.00706` | CVPR 2021 Oral；Fusion 360 分割集 **35,858** B-rep 模型；per-face 准确率 **92.52%** / IoU **77.10%** |
| SolidGen | `2203.13944` | TMLR 2023 |
| BrepGen | `2401.15563` | ACM SIGGRAPH 2024 |
| **HoLa** | `2504.14257` | SIGGRAPH 2025；**无约束生成有效率 82–84% vs SOTA ≈50%** |
| AutoBrep | `2512.03018` | SIGGRAPH Asia 2025 |
| **HiFi-BRep** | `2608.16485` | CVPR 2026；DeepCAD 有效率 **72.20%**（vs DTGBrepGen 43.20%、BRepGen 20.76%）；3.83 s/件 |
| DualBrep | `2606.31579` | SIGGRAPH 2026；SDF+UDF 双场 → Flow Matching |
| BRepFormer | `2504.07378` | ACM ICMR 2025 |
| b-repLer | `2508.10201` | SIGGRAPH 2026；语言引导编辑 |
| BRepCLIP | `2606.05515` | 首个在 B-rep 原生格式上做多模态对比预训练 |
| **Learn the Solid, Not the File** | `2609.11573` | ⭐ 指出**文件格式噪声会污染学习**（"规范输入"问题） |

> ⚠️ **MFBRepNet / CurveNet（B-rep 语境）**：arXiv 精确标题检索 0 命中。
> 它们确实出现在 B-rep 论文的 baseline 表中，但**原始出处待查，不要写编号**。

### 5.4 几何基础模型的产业现状

> **结论：CAD 领域尚无被学界公认的独立"几何基础模型"单点产品；
> 产业界唯一大规模产品化的是 Autodesk 的 Neural CAD。**

- **Autodesk Neural CAD**（2025 AU 首次 keynote，源自 2024 Project Bernini）
  - 变体：neural CAD for geometry（Fusion，生成可编辑 B-rep）+ for buildings（Forma）
  - 面/边表示为 **point grids 并均匀采样**；支持文本/草图/点云/图像多条件
  - ⭐ 关键差异：Project Bernini 输出"不适合后续 CAD 开发的简单 mesh"，
    Neural CAD 输出**一等公民的可编辑 B-rep**，且**同时生成 Fusion 命令历史**
  - ⚠️ 截至 2026-10 仍处**预 beta / 逐步开放**阶段
  - Autodesk 同时在做 **anti-parroting**（防止模型复现客户设计）与训练数据透明度文档

---

## 六、⭐ 真实工业交付中的失败模式（最重要的一节）

| # | 失效模式 | 证据 |
|---|---|---|
| **A** | **泛化性**：在"见过的族"上好，换族就崩 | BenchCAD："微调与 RL 提升 in-distribution 性能，但对未见零件族的泛化仍然受限"；Vision2Code 最强模型总分仅 **0.318** |
| **B** | ⭐ **"可执行 ≠ 正确"** | Text2CAD-Bench：领域专用模型 **IR 低至 2%，但 CD ≈ 220、IoU ≈ 0** —— 语法完全合法、代码能跑、几何完全不对 |
| **C** | **能力悬崖**（不是平缓下降） | Text2CAD-Bench L1→L3：通用 LLM 的 IR 从 11–20% 飙到 **68–93%**；Qwen3-max 在 L3-Geo 上 IoU 仅 **0.07** |
| **D** | **操作替换失败** | BenchCAD 三类失败：缺失精细 3D 结构、误读工业设计参数、**把 sweeps/lofts/twist-extrudes 替换成更简单的 sketch-and-extrude** |
| **E** | **B-rep 多米诺骨牌式崩塌** | B-rep 硬约束意味**一条边归属错，整个模型在 CAD 里直接打不开**；BRepGen 在 DeepCAD 上有效率仅 **20.76%** |
| **F** | **提示词风格反转** | L1–L2 几何描述提示更优（CD 44.31 vs 48.73），**L3 反转**（82.94 vs 93.46）—— 复杂操作是路径型构造，文字传达不了 |
| **G** | **不确定性被低估** | HiFi-BRep 自陈：主要针对**封闭水密单一实体**，开放边界零件、多零件装配体、非流形结构仍无法处理 |
| **H** | **对称性/拓扑不变性/参数化精度/特征语义缺失** | DeepCAD 数据集只含 sketch-extrude，**排除了 sweeps/lofts/revolves/sheet metal/surfacing** |
| **I** | **无法处理真实工程图** | BenchCAD 47 个标准锚定族中 52 个族有真实规范表约束 —— 真实工程图与玩具 CAD 分布差异巨大 |
| **J** | **数据集天花板** | ABC 100 万模型但**无文本、无制造元数据、无设计历史**；公开 CAD 数据集存在"**几何深度 vs 过程语义**"的根本分裂 |

> ⭐ **对 FEMAI 的直接含义**：
> 如果 AICube 接受 LLM 生成的 CAD 代码，**不能以"执行成功"作为验收标准**。
> 必须有几何真值校验（见 §八）。

---

## 七、⭐ 几何内核作为"真值裁判"—— CAD 领域独有的验证优势

> **逻辑链**：CAD/CAE 的输出**不是像素**，而是**有精确数学定义的实体**。
> 因此它自带一个**确定性判官**：几何内核。
> 判定"对不对"不需要人眼、不需要标注者、不需要相似度阈值 —— **内核接受 / 不接受**。

### 六层验证（从弱到强）

| 层 | 检查 | 工具 | 失败即 |
|---|---|---|---|
| **L1** | 程序可执行、无异常 | Python 子进程 + 超时 | IR 计入 |
| **L2** | **B-rep 拓扑有效** | `BRepCheck_Analyzer.IsValid()` + `Failure()` | 直接判 0 |
| **L3** | **水密 / 无自由边** | 遍历 shell，检查裸边 | 直接判 0 |
| **L4** | **流形可网格化** | 三角化后检查每边恰被 2 三角共享、方向相反 | 直接判 0 |
| **L5** | **量守恒** | `BRepGProp` 体积/面积/质心 vs 期望；AP242 Validation Properties 跨格式比对 | 容差判定 |
| **L6** | **拓扑不变量** | Betti 数 (b₀,b₁,b₂)、欧拉数、亏格 | 与目标一致 |

### 三个已工程化验证的范例（可直接抄）

**① CADGenBench 的 "CAD Validity Gate"（零级联门）**
- 三支柱：`BRepCheck_Analyzer` 无错 + **Watertightness（无裸边）** + **Manifold Meshability**
- **零级联**：任一失败 → `is_valid=False`，`cad_score` **强制为 0**，其余指标不计算
- **安全上限**：文件 ≤50MB、三角形 ≤100 万、超时 30s
  （⚠️ 因为 OCCT 三角化是原生 C++ 调用，**不可靠响应 Python signal**，故用 `multiprocessing.Process` 隔离并 kill）
- **失败记忆化**：去重收集人类可读串（`BRepCheck_SelfIntersectingWire`、`BREP not watertight: open shells / naked edges`、`mesh non-manifold: edge shared by 4 triangles`）
- **附加诊断**（不影响分数但标记"脆弱"几何）：最小面面积 <0.001 mm²、最大面长宽比 >1000、最大 B-rep 容差 >0.1 mm

**② FllumaOne 的内核级验证链（生成即入库）**
- 建模操作解析为 **OpenCASCADE B-rep**
- 布尔 join/cut/intersect 用 **`BRepAlgoAPI` 家族**
- 结果用 **`BRepCheck_Analyzer`** 检查到面/边/顶点级有效性
- 体积与表面积用 **`BRepGProp`** 计算
- **STEP 导出/回读检查**用 `STEPControl` writer/reader
- ⭐ **"验证目标是内核接受的 B-rep 实体，而不仅仅是语法合法的 Python 脚本"**
- 另有**设计签名去重**（canonical construction signatures）先行过滤

**③ claude-cad（社区实践，方法论值得抄）**
四段式断言，且**明确排序**（先弱后强）：
1. `BRepCheck_Analyzer(solid.wrapped).IsValid()` 且 `len(solid.Solids()) == 1`
2. …（水密/流形）
3. …（量守恒）
4. …（拓扑不变量）

> ⭐ **这三套验证链，就是 AICube 入口层最该立刻建立的能力。**

---

## 八、⭐ LLM-for-CAD 的真实边界（2026）

### 8.1 "CAD 生成 = 代码生成"这条论断的证据链

> ⚠️ **精确表述**：这是"**更有效的表示**"，不是"本质已解决"。

| 证据 | 内容 |
|---|---|
| **CAD-Recode（ICCV 2025）** | 指出 DeepCAD 等用"封闭有限 token 词表"有两大局限——**表示能力受限**、**不可解释**；改用 CadQuery Python 代码后：① 复用 LLM 的 Python 预训练知识 ② 可直接执行 ③ 可被交互编辑。DeepCAD 测试集 **CD 0.89→0.30，IoU 86.2%→92.0%** |
| **Text2CAD-Bench 对照实验** | "基于代码的库（如 CadQuery）比专门的命令序列效率显著更高。LLM 从通用编程预训练中获益" |
| **FllumaOne** | 明确以此为方法论前提："训练目标从语法可执行的 Python 脚本，升级为**内核接受的 B-rep 实体**" |
| **CAD-Assistant / CADReview / CIT-CAD / ReliCAD / MIRAGE-CAD / StepCAD** | 全部是"代码 + 执行校验 + 修复"闭环，**无一例外** |

### 8.2 ⚠️ 必须同时给出的反证

- **"代码生成"不自动解决几何问题**：Text2CAD-Bench 显示领域专用模型 **IR 低至 2% 却 CD ≈ 220、IoU ≈ 0**
- **几何语义必须由内核兜底**：见 §七 FllumaOne 验证链
- **纯代码路线仍在探索跨后端 IR**：CADIR（`2608.00891`）做"跨后端可编辑中间表示"——
  说明"直接生成某家 CAD 的代码"不够，需要中间层

### 8.3 ⭐ 最重要的边界结论

> **LLM-for-CAD 的瓶颈已经从"能不能生成合法代码"转移到
> "能不能生成几何正确、约束自洽、且在真实工程复杂度下泛化的模型"。**
>
> 证据：IR 已被解决（低至 2%），但 CD/IoU 仍差
> （Text2CAD-Bench L3 IR 68–93%、CD 翻倍；BenchCAD Vision2Code 最强模型 0.318）。

---

## 九、⭐ CAD-CAE 一体化：谁真正做通了

| 层级 | 公司/产品 | 一体化程度 | 关键证据 |
|---|---|---|---|
| **L4：同一数据模型、无需导出转换** | **达索 3DEXPERIENCE MODSIM（CATIA + SIMULIA）** | ⭐⭐⭐⭐⭐ | 官方明确："**CAD model 与 simulation model 完全同步，无需导出、转换或清理**"；改几何→仿真自动更新；从"以周计"变"以小时/分钟计"；**基于物理的生成式设计、DOE**；LEO 虚拟伙伴可**运行仿真研究、诊断模型问题** |
| **L4：同一数据模型** | **西门子 Simcenter Simsolid + Designcenter** | ⭐⭐⭐⭐ | 官方："**无需几何简化、无需网格划分**"，可处理含**粗糙接触面、间隙、重叠几何**的复杂零件/大装配；标准 PC 上**秒到分钟**出结果；支持 CATIA/NX/Creo/Fusion/SOLIDWORKS/JT/STEP/VDA/Parasolid/ACIS/PLMXML/CGR/STL **无需导入导出**；与 Onshape、Teamcenter 直接集成 |
| **L3：装配级 FEA 内嵌 CAD** | **Onshape Simulation** | ⭐⭐⭐ | 浏览器内线性静力 + 模态；**装配 mates（fastened/revolute/slider）自动转成仿真运动学**；**无需 defeaturing、无需 meshing**；Inertial Relief 自动处理自由体；云端异步排队最多 50 并发；**结果随装配版本控制** |
| **L3：AI 代理仿真（几何→物理量，非几何生成）** | **Ansys SimAI / Discovery** | ⭐⭐⭐ | Sumitomo Riko 案例：**仿真加速 >10×**，橡胶 bush 预测 5 分钟内完成（原 >1 小时），偏差通常 **<5%**，散热片案例最大相对误差 **<0.6%** |
| **L2：同一 PLM 平台 + 关联模型** | 达索 3DEXPERIENCE / SIMULIA | ⭐⭐⭐⭐（平台层） | ENOVIA + CATIA + SIMULIA 单数据源；Neura Robotics 2026-04 战略合作（Physical AI 生态融合） |
| **L2'：AI 生成可编辑 B-rep** | Autodesk Neural CAD（Fusion） | ⭐⭐⭐ | 见 §5.4 |
| **L2''：CAD 平台内仿真代理** | Siemens PhysicsAI | ⭐⭐⭐ | 扩展至 Inspire/HyperMesh/STAR-CCM+，评估最快 **1000×** |
| **L1：CAD 内点开求解器** | SOLIDWORKS / Fusion Simulation | ⭐⭐ | SOLIDWORKS 2026 引入 AI 虚拟伙伴 |

> ⭐ **结论：真正做到"CAD 内直接仿真"到"无需导出、无需网格、装配 mates 直接变运动学、结果随模型版本走"的，只有 Onshape Simulation、Simcenter Simsolid、3DEXPERIENCE MODSIM 三家。**
> 其余都是"CAD 与仿真同平台但需导出/网格/清理"。

### ⭐ 对清航飞迈的战略含义（诚实评估）

SimSolid 已经证明"**无网格 + 直接吃 CAD 装配**"是可交付的。
**所以 FEMAI 的护城河不能是"我们也能在 CAD 里跑仿真"。** 真正的差异化在：

| # | 差异化方向 | 为什么对手没做 |
|---|---|---|
| 1 | ⭐ **AI 代理模型替代多少求解器次数** | SimSolid 是**确定性无网格 FEM**，不是 AI。替代物理场（而非几何）是另一件事 |
| 2 | ⭐ **C919 级复材结构的层合板本构 + 变刚度设计** | CAE2 年会报告提到"基于图神经网络的连续板体代理模型、非均质各向异体本构模型、跨尺度协同进化算法"—— SimSolid/Onshape 都不覆盖 |
| 3 | ⭐ **医疗骨科完整物理链路** | 从 CT 分割 → 3D 骨缺损重建 → 术前规划 → 术后受力仿真，这是完整链路而非单点工具 |

---

## 十、开源几何工具链（许可证已核实）

| 项目 | GitHub | 许可证 | 用途 | 成熟度（2026-10-26 实测） |
|---|---|---|---|---|
| **OpenCASCADE (OCCT)** | Open-Cascade-SAS/OCCT | **LGPL-2.1 + Exception** | 几何内核：建模/布尔/缝合/修复/B-rep | ⭐⭐⭐⭐⭐ 3,064★，2026-10-20 仍在推 |
| **OCP / cadquery-ocp** | CadQuery/OCP | wrapper **Apache-2.0** | OCCT 的 Python 绑定 | ⭐⭐⭐⭐ PyPI 月下载 **~106 万**；8.0.1.1.0 (2026-10-05) |
| **pythonocc-core** | tpaviot/pythonocc-core | **LGPL-3.0** | OCCT 的 SWIG 绑定 | ⭐⭐⭐⭐ 1,989★ |
| **manifold3d** | elalish/manifold | **Apache-2.0** | ⭐ **保证流形输出的三角网格布尔** | ⭐⭐⭐⭐ 2,372★，PyPI 月下载 **~310 万** |
| **CGAL** | CGAL/cgal | **GPL v3+ 或 GeometryFactory 商业许可** | 计算几何算法全谱 | ⭐⭐⭐⭐⭐ 6,088★；**CGAL 6.2.1**（2026-06）；2026-04 满 30 岁 |
| **trimesh** | mikedh/trimesh | **MIT** | Python 网格 I/O / 布尔 / watertight 检查 | ⭐⭐⭐⭐ 3,713★ |
| **Open3D** | isl-org/Open3D | **MIT** | 点云/网格处理与深度学习 | ⭐⭐⭐⭐⭐ 14,123★ |
| **pyvista / VTK** | pyvista/pyvista / Kitware/VTK | MIT / BSD | 可视化与网格分析 | ⭐⭐⭐⭐ |
| **gmsh** | ⚠️ **官方 GitLab** gitlab.onelab.info/gmsh/gmsh | **GPL v2+（带例外）** | FEM 网格生成 + 内置 CAD 引擎 + 后处理 | ⭐⭐⭐⭐⭐ **v4.15.2 (2026-03-24)** |
| **Salome / SMESH** | SalomePlatform | **LGPL 2.1** | CAE 平台 + 多算法网格 + PARAVIS | ⭐⭐⭐⭐ **v9.16.0 (2026-06)** |
| **Netgen / NGSolve** | NGSolve/netgen | **LGPL-2.1** | 四面体网格 + 多物理场求解 | ⭐⭐⭐ 589★ |
| **TetGen** | ⚠️ 主仓库在 **codeberg.org** | **AGPLv3**；可付费商业授权 | 精确约束 Delaunay 四面体 | ⭐⭐⭐ v1.6.1 |
| **meshio** | nschloe/meshio | MIT | 多种网格格式读写 | ⚠️ **最后推送 2024-07-23（近 2 年未更，注意维护风险）** |
| **OpenSCAD** | openscad/openscad | GPL 系 | 脚本化 CSG 建模 | ⭐⭐⭐⭐⭐ 10,512★；**已集成 manifold3d** |
| **SolveSpace** | solvespace/solvespace | **GPL-3.0** | 轻量参数化 2D/3D + 约束草图 | ⭐⭐⭐ 4,219★ |
| **libigl** | libigl/libigl | ⚠️ GitHub 元数据标 GPL-3.0，自述 MPL-2.0 —— **需读 LICENSE 确认** | 几何处理算法库 | ⭐⭐⭐⭐ 5,114★ |
| **geometry-central** | nmwsharp/geometry-central | **MIT** | 三角网格几何处理 | ⭐⭐⭐ 1,343★ |
| **cadquery** | CadQuery/cadquery | Apache-2.0 | 参数化 CAD 脚本 | ⭐⭐⭐⭐ 5,998★ |
| **build123d** | gumyr/build123d | **Apache-2.0** | Python 参数化 CAD（比 CadQuery 更现代） | ⭐⭐⭐⭐ 3,526★；配套 `bd_warehouse` |
| **FreeCAD** | FreeCAD/FreeCAD | **LGPL-2.1** | 开源参数化 CAD + FEM/CFD/BIM/CAM | ⭐⭐⭐⭐⭐ 34,782★ |

> ⚠️ **许可证陷阱**：
> - **TetGen 是 AGPLv3** —— 传染性强，商用必须购买许可
> - **Gmsh GPL v2+ 带例外** —— **商业闭源软件不可静态链接**（需商业许可）
> - **CGAL 双许可** —— 高层包 GPL，商业闭源需 GeometryFactory 商业许可

---

## 十一、几何学习数据集（规模已核实）

| 数据集 | 规模 | 许可 / 备注 |
|---|---|---|
| **ABC Dataset** | **~100 万** CAD 模型 | MIT；⚠️ **无文本、无制造元数据、无设计历史** |
| **Fusion 360 Gallery** | 8,625 人类设计序列；分割集 **35,858** B-rep 模型；装配集 **8,251 装配体 / 154,468 零件 / 32,148 接头** | Onshape ToU |
| **SketchGraphs** | **1,500 万**草图 | 原始 JSON 43GB |
| **DeepCAD 数据集** | **179,133** 参数化模型 | MIT；源自 ABC 过滤 sketch-extrude |
| **Zero-To-CAD-1m** | **~100 万**几何验证过的 CadQuery 可执行程序（65 类） | HF: ADSKAILab/Zero-To-CAD-1m |
| **Omni-CAD** | **~45 万**多模态实例 | 文本+多视图+点+命令序列 |
| **FllumaOne** | 代码原生多模态，**内核验证过特征历史** | `2606.17696` |
| **Thingi10K** | 10,000 模型 / 4,892 tags / 72 类 | ⭐ **真实缺陷统计是几何缺陷检测的黄金参考**：50% 非实体、45% 自相交、31% 共面自相交、26% 多组件、**22% 非流形**、16% 退化面、14% 非 PWN、11% 拓扑开放、10% 非定向 |

---

## 十二、CAD 领域的公开基准（2025-2026 爆发式增长）⭐

| 基准 | 规模与任务 | 入口 |
|---|---|---|
| **BenchCAD** | **17,900** 执行验证 CadQuery 程序 / **106** 工业零件族 / **47** 个 ISO-DIN-EN-ASME-IEC 标准码；4 任务 + BenchCAD-QA 2,400 对 + BenchCAD-Edit 748 对 | `2605.10865`、benchcad.com；⭐ **已被 Anthropic 与 OpenAI 收入官方模型卡**（Claude Fable 5 & Mythos 5 System Card §8.16.4、Claude Sonnet 5 §8.10.3、Claude Opus 5、OpenAI GPT-5.6 发布表 2026-07-09） |
| **CADGenBench** | Generation + Editing；⭐ **四轴打分**：Validity（gate，失败直接 0）、Shape similarity（surface distance F1 + volume IoU）、Interface match（keep-in/keep-out 子体积）、Topology match（Betti 数）；**工具无关** | HuggingFace Space `HuggingAI4Engineering/CADGenBench`；⭐ **有真实排行榜**（2026-10-23 快照：build123d-mcp + Claude Opus 5.5 = 86.9%） |
| **Text2CAD-Bench** | 600 例人工精选，L1–L4 四级复杂度，**双提示词风格**；L4 用 GLM4.6V 裁判 8 视图 | `2605.18430` |
| **neuralCAD-Edit** | 多模态指令驱动的 3D CAD 编辑基准 | `2604.16170` |
| **STEP AP242 Benchmarks** | CAD + PDM 两类测试用例 | afnet.fr |
| **CAx-IF 测试轮** | R55（2026-03）、**R57J（STEP 数据交换成功率 97%）** | mbx-if.org |

> ⚠️ **纠错**：所谓"DesignNet / Fusion 360 Gallery 排行"并不存在 ——
> DesignNet 是 C&C 2023 的设计空间知识图谱系统，Fusion 360 Gallery 也无公开下载量榜。
> **能替代的是 CADGenBench / BenchCAD 的模型榜单。**

---

## 十三、意图传递：标准各自能携带什么

| 标准 | 几何 | 装配/结构 | 材料 | 载荷/工况 | PMI/GD&T | 运动副 | 验证属性 | 网格/结果 | 定位 |
|---|---|---|---|---|---|---|---|---|---|
| **STEP AP242**（ISO 10303-242:2025 Ed.4，2025-08） | 精确 B-rep + tessellated | ✅ 产品/装配 | ✅ | ⚠️ 弱 | ✅ **语义 + 图形 PMI** | ✅ Kinematics | ✅ **Validation Properties** | AP209 有限元模型 | **唯一全能**；正做 AP242e4 |
| **JT**（ISO **14306**-1/2/3/4） | B-rep + 压缩 facet | ✅ 层次装配 | ⚠️ | ❌ | ✅ PMI + Saved Views | ⚠️ | ⚠️ | ❌ | **轻量可视化/DMU**，文件仅为 CAD 的 1–10% |
| **CGNS**（AIAA S-108，v4.5.0 2025-01-10） | ❌ | 多区接口（abutting + overset） | ✅ 物性/湍流模型 | ✅ 边界条件 | ❌ | ❌ | ✅ 收敛历史 | ✅ 完整 CFD 网格+解 | **CFD 专用**；正转向 HDF5 |
| **VMAP**（v1.2 2024-08-29） | ✅ 几何+离散化 | ⚠️ | ✅ **材料模型参数** | ✅ 状态变量 | ❌ | ⚠️ | ❌ | ✅ | 基于 **HDF5**；四大组 GEOMETRY/VARIABLES/SYSTEM/MATERIAL；已支持 Abaqus、ANSYS Mechanical、ANSYS Digimat、MpCCI、OpenFOAM、BETA CAE ANSA |
| **3DXML**（达索私有） | ✅ 精确曲面+拓扑网格 | ✅ BOM | ⚠️ | ❌ | ✅ 图形 PMI | ❌ | ❌ | ❌ | CATIA V6 原生；**锁定在达索生态** |
| **QIF**（ISO 23952） | ✅ | ✅ | ⚠️ | ✅ 测量计划/结果 | ✅ QIF MBD | ❌ | ❌ | 测量结果+统计 | **质量/检测侧**，通过 Persistent ID 与 STEP 打通 |
| **3D PDF / PRC**（ISO 14739-1） | ✅ PRC 精确 B-rep + U3D 网格 | ✅ | ⚠️ | ❌ | ✅ | ❌ | ❌ | ❌ | 给**无 CAD 许可证**的供应商看 |
| **glTF**（ISO/IEC 12113:2022） | ❌ 纯三角网格 | ✅ 节点层级 | ✅ 材质 | ❌ | ❌ | ❌ | ❌ | ❌ | 运行时 3D 资产；**不是工程数据格式** |
| **3MF**（ISO/IEC 25422:2025） | 网格（watertight by spec） | ✅ 组件 | ✅ | ❌ | ⚠️ Slice ext. | ❌ | ❌ | ❌ | 增材制造；Volumetric 扩展支持体素与 SDF |

### ⭐ Persistent ID：意图传递的硬机制

- CAx-IF 与 DMSC 联合发布的 *"Recommended Practices for Cross-Domain Exchange for Downstream Uses"*，
  **Version 1.0，2026-01-29**
- STEP 用 `V5_UUID_ATTRIBUTE` 标记几何实体与 PMI 元素；QIF 用 `EntityExternalIds` 保留同一身份
- CAx-IF 测试已验证 **STEP↔QIF 双向可追溯首次被演示**，正确实施可达 **100% 可追溯**
- **CAx-IF 主席 Jochen Boy：R57J 测试轮 STEP 数据交换成功率 97%**

### CAx-IF 推荐实践清单（最新，全部一手 PDF 可下载）

| 文档 | 版本 | 日期 |
|---|---|---|
| **Persistent IDs** | **v1.8** | **2026-03-13** |
| Cross-Domain Exchange for Downstream Uses（与 DMSC） | v1.0 | 2026-01-29 |
| **Composite Material Validation Properties** | v1.0 | **2026-06-23** |
| Model Styling and Organization | v1.10 | 2025-08-01 |
| Geometric and Assembly Validation Properties | v4.6 | 2023-04-21 |
| PMI Representation and Presentation (AP242) | v4.1 | 2024-06-20 |
| Product & Assembly Structure (Domain Model XML) | v4.0 | 2025-10-20 |
| Kinematics (Domain Model XML) | v1.3 | 2025-10-20 |
| **Composite Materials** | v4.4 | 2025-12-03 |
| Alternative Shapes | v1.0 | 2025-12-03 |
| Geometric and Assembly Validation Properties | v4.6 | 2023-04-21 |
| Supplemental Geometry | v1.3 | 2025-08-01 |
| Tessellated 3D Geometry | v1.1 | 2019-08-22 |

### ⭐ 专家会做的"意图丢失量化"实验

不是问"格式支持吗"，而是**做往返实验**：
1. 原生 CAD → 中性格式 → 回到另一 CAD/CAE
2. 比对：**装配层数与实例数、零件名、材料指派、基准体系、PMI 语义（不是图形）、Validation Properties（体积/面积/质心）、运动副、运动学求解结果**
3. 报告"丢失率"，并把它当作**供应商验收指标**

**已核实的往返测试基础设施**：NIST **STEP File Analyzer and Viewer**（免费，可生成实体/属性电子表格；
按 CAx-IF 推荐实践生成语义 PMI / 图形 PMI / Validation Properties 三类报告；语法检查器；
可查看 AP209 有限元模型、装配 BOM、剖切面、点云验证属性）

---

## 🔗 相关

- [[领域知识索引]]
- [[仿真可信度V-V与标准体系]]
- [[代理模型与神经算子工程化]]
- [[100-物理AI产品与领域/000-专家作业标准-四问]]
