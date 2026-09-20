[Lab](../../README.md) · [English](../en/triad-identity-audit.md) · [Português](../pt-BR/triad-identity-audit.md) · [Español](../es/triad-identity-audit.md) · [Deutsch](../de/triad-identity-audit.md) · [Svenska](../sv/triad-identity-audit.md) · [Norsk](../no/triad-identity-audit.md) · [Dansk](../da/triad-identity-audit.md) · **中文（简体）**

# TRIAD 一致性审计

**逐项说明：什么是完整的 TRIAD**

英语是本审计的主要语言。其他版本是对相同结论的维护性翻译。

本登记册逐项检查 65 个已编目研究，明确说明其保存记录是否为完整 TRIAD 方程的一次执行：P1 振荡、P2 自指（瞬时自相互作用与记忆）、P3 耦合（耗散与热浴）共同作用。

每一行给出四种一致性结论之一、维护的范围说明，以及指向执行审计记录和已核查源码或文件索引的证据链接。本审计未重跑任何模拟，未改动任何保存文件。

无译文处，研究页面链接到英文版。

## 每项研究如何核查

核查遵循从源码到结论的保存链条：

```text
保存的源码 → 实现的算子 → 声明的运行条件 → 保存的测量 → 一致性结论
```

full 或 pure 等名称不能确立完整性；只有核查过的更新步骤、配置和运行绑定才能确立。关闭或改动了方程项的系统被标识为非完整 TRIAD，并记录其条件。

## 逐项核查点

每项研究都按相同的八个核查点阅读：

- **P1 · 振荡保留.** 更新步骤保留动力学的振荡部分。
- **P2 · 瞬时自相互作用保留.** 更新步骤保留瞬时非线性自相互作用。
- **P2 · 记忆保留，三个尺度.** 三个演化的记忆场承载密度历史并反馈于状态。
- **P3 · 热浴保留，FDT 锁定.** 耗散与随机热浴以 FDT 锁定的幅度共同作用。
- **未关闭任何方程项.** 演化过程中未移除、置零或冻结记忆、热浴、分数阶或相互作用项。
- **无未声明的轨迹重缩放.** 没有逐步重归一化或状态守卫改写演化后的场；声明的输入保持可见。
- **源码与运行已绑定.** 所提供的源码、配置、种子、网格和时间范围可标识所执行的运行；无未绑定的外部运行时。
- **观测量已定义.** 探测器、阈值和标签均已定义；新标签不是新轨迹。

## 逐项登记册

各行在每个一致性类别内按编目顺序排列。范围说明为维护的结论；“证据”链接执行审计记录和已核查的源码或文件索引。

### 完整 TRIAD — 联合作用项已记录 · 14

所提供的独立源码记录了 P1、P2、P3 的联合作用，含三个记忆模式、耗散和 FDT 噪声。这记录的是有文档的联合操作；不证明完全符合、数值收敛或所执行的运行时。

| 研究 | 一致性 | 记录的范围 | 证据 |
|---|---|---|---|
| <a id="study-t-30"></a>[Two atoms](../../simulations/structures/two-atoms/README.md) | **完整 TRIAD — 联合作用项已记录** | 所提供的独立更新记录了联合作用项与三个记忆模式，FDT 处于活跃状态。两个高斯种子；t=0.01 之后失去对该对的跟踪。 | [审计记录](../en/execution-audit.md#study-t-30) · [lines 33–40](../../simulations/structures/two-atoms/code/simulate_two_atoms.py) |
| <a id="study-t-31"></a>[Nested positive Gaussians](../../simulations/structures/nested-positive-gaussians/README.md) | **完整 TRIAD — 联合作用项已记录** | 所提供的独立更新记录了联合作用项与三个记忆模式，FDT 处于活跃状态。同心正种子；记录的双尺度标志持续至 t=0.02。 | [审计记录](../en/execution-audit.md#study-t-31) · [lines 33–40](../../simulations/structures/nested-positive-gaussians/code/simulate_nested_gaussians.py) |
| <a id="study-t-32"></a>[Atom inside a larger Gaussian](../../simulations/structures/atom-inside-a-larger-gaussian/README.md) | **完整 TRIAD — 联合作用项已记录** | 所提供的独立更新记录了联合作用项与三个记忆模式，FDT 处于活跃状态。宽包络与两个带符号的内部种子；仅初始帧保留该对。 | [审计记录](../en/execution-audit.md#study-t-32) · [lines 39–46](../../simulations/structures/atom-inside-a-larger-gaussian/code/simulate_atom_inside_gaussian.py) |
| <a id="study-t-33"></a>[Concentric positive/negative nest](../../simulations/structures/concentric-positive-negative-nest/README.md) | **完整 TRIAD — 联合作用项已记录** | 所提供的独立更新记录了联合作用项与三个记忆模式，FDT 处于活跃状态。带符号的同心嵌套；壳层与符号标志的记录寿命不同。 | [审计记录](../en/execution-audit.md#study-t-33) · [lines 33–40](../../simulations/structures/concentric-positive-negative-nest/code/simulate_signed_gaussian_nest.py) |
| <a id="study-t-34"></a>[Long nest trajectory](../../simulations/structures/long-nest-trajectory/README.md) | **完整 TRIAD — 联合作用项已记录** | 所提供的独立更新记录了联合作用项与三个记忆模式，FDT 处于活跃状态。同一嵌套延续至 T=60；t=8 的共同结果与短时运行一致。 | [审计记录](../en/execution-audit.md#study-t-34) · [发现 UNI-015](../en/execution-audit.md#finding-uni-015) · [lines 36–43](../../simulations/structures/long-nest-trajectory/code/simulate_long_gaussian_nest.py) |
| <a id="study-t-35"></a>[Finite peak, early window](../../simulations/structures/finite-peak-early-window/README.md) | **完整 TRIAD — 联合作用项已记录** | 所提供的独立更新记录了联合作用项与三个记忆模式，FDT 处于活跃状态。单种子与双种子的早期窗口；有限峰值仍可能占据一个网格单元。 | [审计记录](../en/execution-audit.md#study-t-35) · [lines 51–58](../../simulations/structures/finite-peak-early-window/code/simulate_early_peak.py) |
| <a id="study-t-37"></a>[A pocket in the field](../../simulations/structures/a-pocket-in-the-field/README.md) | **完整 TRIAD — 联合作用项已记录** | 所提供的独立更新记录了联合作用项与三个记忆模式，FDT 处于活跃状态。在 t=0.5 处加入声明的高斯输入；它是耦合场的输入。 | [审计记录](../en/execution-audit.md#study-t-37) · [发现 UNI-016](../en/execution-audit.md#finding-uni-016) · [lines 32–39](../../simulations/structures/a-pocket-in-the-field/code/simulate_field_pocket.py) |
| <a id="study-t-38"></a>[Two pockets](../../simulations/structures/two-pockets/README.md) | **完整 TRIAD — 联合作用项已记录** | 所提供的独立更新记录了联合作用项与三个记忆模式，FDT 处于活跃状态。在 t=0.5 处加入两个声明的带符号高斯输入。 | [审计记录](../en/execution-audit.md#study-t-38) · [发现 UNI-016](../en/execution-audit.md#finding-uni-016) · [lines 11–17](../../simulations/structures/two-pockets/code/simulate_two_field_pockets.py) |
| <a id="study-t-39"></a>[Density–memory maps](../../simulations/structures/density-memory-maps/README.md) | **完整 TRIAD — 联合作用项已记录** | 所提供的独立更新记录了联合作用项与三个记忆模式，FDT 处于活跃状态。运行器重新演化植入口袋情形并记录密度/记忆图；它不仅是图像读取器。 | [审计记录](../en/execution-audit.md#study-t-39) · [发现 UNI-016](../en/execution-audit.md#finding-uni-016) · [lines 11–17](../../simulations/structures/density-memory-maps/code/simulate_density_memory_maps.py) |
| <a id="study-q01"></a>[Spatial convergence](../../simulations/field-diagnostics/spatial-convergence/README.md) | **完整 TRIAD — 联合作用项已记录** | 所提供的独立更新记录了联合作用项与三个记忆模式，FDT 处于活跃状态。网格收敛尚未解决；记录的谱跟随网格截断。 | [审计记录](../en/execution-audit.md#study-q01) · [发现 UNI-013](../en/execution-audit.md#finding-uni-013) · [lines 36–43](../../simulations/field-diagnostics/spatial-convergence/code/measure_spatial_convergence.py) |
| <a id="study-q01b"></a>[Resolution and timestep](../../simulations/field-diagnostics/resolution-and-time-step/README.md) | **完整 TRIAD — 联合作用项已记录** | 所提供的独立更新记录了联合作用项与三个记忆模式，FDT 处于活跃状态。空间与时间步长加密保留联合作用项；数值收敛尚未解决。 | [审计记录](../en/execution-audit.md#study-q01b) · [发现 UNI-013](../en/execution-audit.md#finding-uni-013) · [lines 38–45](../../simulations/field-diagnostics/resolution-and-time-step/code/compare_grid_and_time_step.py) |
| <a id="study-q02"></a>[An ensemble of initial conditions](../../simulations/field-diagnostics/seed-ensemble/README.md) | **完整 TRIAD — 联合作用项已记录** | 所提供的独立更新记录了联合作用项与三个记忆模式，FDT 处于活跃状态。记录的 32 个种子均为有限值；该批次使用 complex64/float32 并声明了精度变化。 | [审计记录](../en/execution-audit.md#study-q02) · [发现 UNI-013](../en/execution-audit.md#finding-uni-013) · [lines 45–52](../../simulations/field-diagnostics/seed-ensemble/code/simulate_seed_ensemble.py) |
| <a id="study-q03"></a>[Field modes and subspaces](../../simulations/field-diagnostics/field-modes/README.md) | **完整 TRIAD — 联合作用项已记录** | 所提供的独立更新记录了联合作用项与三个记忆模式，FDT 处于活跃状态。源码包含演化与被动 POD/DMD；其后处理修正已声明。 | [审计记录](../en/execution-audit.md#study-q03) · [lines 52–59](../../simulations/field-diagnostics/field-modes/code/analyze_field_modes.py) |
| <a id="study-q04"></a>[Testing linearity](../../simulations/field-diagnostics/linearity-tests/README.md) | **完整 TRIAD — 联合作用项已记录** | 所提供的独立更新记录了联合作用项与三个记忆模式，FDT 处于活跃状态。叠加残差包含公共的加性热浴；它不是非线性响应的纯粹度量。 | [审计记录](../en/execution-audit.md#study-q04) · [发现 UNI-014](../en/execution-audit.md#finding-uni-014) · [文件](../../simulations/field-diagnostics/linearity-tests/FILES.md) |

### 非完整 TRIAD — 已记录的偏离 · 14

所提供的源码或配置被证明偏离完整参考：移除或冻结的方程项、不同的更新步骤或状态守卫。保存的输出仍是该实现系统的记录，而非完整 TRIAD 方程的记录。

| 研究 | 一致性 | 记录的范围 | 证据 |
|---|---|---|---|
| <a id="study-bravais-01-field"></a>[Emergent 3D field](../../simulations/geometry/field-3d/README.md) | **非完整 TRIAD — 已记录的偏离** | 演化源码使用了与参考不同的动能符号/噪声更新和条件状态守卫；其保存结果仍是该实现的记录。 | [审计记录](../en/execution-audit.md#study-bravais-01-field) · [发现 UNI-001](../en/execution-audit.md#finding-uni-001) · [lines 241–253](../../simulations/geometry/field-3d/code/pt-BR/bravais_puro_3d.py) |
| <a id="study-bravais-03-scale"></a>[Intrinsic scale](../../simulations/geometry/scale-sweep/README.md) | **非完整 TRIAD — 已记录的偏离** | 演化源码使用了与参考不同的动能符号/噪声更新和条件状态守卫；其保存结果仍是该实现的记录。 | [审计记录](../en/execution-audit.md#study-bravais-03-scale) · [发现 UNI-001](../en/execution-audit.md#finding-uni-001) · [lines 175–185](../../simulations/geometry/scale-sweep/code/pt-BR/bravais_sweep_L.py) |
| <a id="study-t-16"></a>[Memory at resolution 40](../../simulations/memory/memory-grid-40/README.md) | **非完整 TRIAD — 已记录的偏离** | 保存的比较明确包含一个无记忆分支。名为 full 的分支的生成源码缺失。 | [审计记录](../en/execution-audit.md#study-t-16) · [发现 UNI-002](../en/execution-audit.md#finding-uni-002) · [lines 12–24](../../simulations/memory/memory-grid-40/notes/original-record.md) |
| <a id="study-t-29"></a>[Memory at small amplitude](../../simulations/memory/memory-small-amplitude/README.md) | **非完整 TRIAD — 已记录的偏离** | 该运行设 alpha=0 并使用两个记忆模式；其热浴处于活跃状态。 | [审计记录](../en/execution-audit.md#study-t-29) · [lines 2–6](../../simulations/memory/memory-small-amplitude/code/simulate_memory_small_amplitude.py) |
| <a id="study-t-36"></a>[Ten-part rerun dossier](../../simulations/numerical-checks/reproduction-dossier/README.md) | **非完整 TRIAD — 已记录的偏离** | 该卷宗将数值/解析核查与记录的关闭项比较混合，包括关闭记忆、关闭热浴与冻结记忆情形。 | [审计记录](../en/execution-audit.md#study-t-36) · [发现 UNI-003](../en/execution-audit.md#finding-uni-003) · [发现 UNI-004](../en/execution-audit.md#finding-uni-004) · [发现 UNI-005](../en/execution-audit.md#finding-uni-005) · [发现 UNI-006](../en/execution-audit.md#finding-uni-006) · [发现 UNI-007](../en/execution-audit.md#finding-uni-007) · [lines 10–18](../../simulations/numerical-checks/reproduction-dossier/notes/memory-collapse-grid-64/predictions-memory-collapse-grid-64.md) |
| <a id="study-field-2d"></a>[2D field explorations](../../simulations/geometry/field-2d/README.md) | **非完整 TRIAD — 已记录的偏离** | 所提供的一维/二维实现包含轨迹归一化或守卫，与参考演化不同；纯二维耗散表达式呈相位型。 | [审计记录](../en/execution-audit.md#study-field-2d) · [发现 UNI-001](../en/execution-audit.md#finding-uni-001) · [lines 208–221](../../simulations/geometry/field-2d/code/bravais_pure_emerge.py) |
| <a id="study-dimension-comparison"></a>[Comparing 2D and 3D](../../simulations/geometry/dimension-comparison/README.md) | **非完整 TRIAD — 已记录的偏离** | 两个维度分支每步都归一化场（目标范数 3.0 与 2.2），且使用与参考不同的更新。 | [审计记录](../en/execution-audit.md#study-dimension-comparison) · [发现 UNI-001](../en/execution-audit.md#finding-uni-001) · [lines 84–94](../../simulations/geometry/dimension-comparison/code/bravais_long_2d3d.py) |
| <a id="study-vibrations"></a>[Strings and vibration](../../simulations/geometry/vibrations/README.md) | **非完整 TRIAD — 已记录的偏离** | 演化源码使用了与参考不同的动能符号/噪声更新和条件状态守卫；其保存结果仍是该实现的记录。独立的 bravais_vibracoes 读取器是运动学重建。 | [审计记录](../en/execution-audit.md#study-vibrations) · [发现 UNI-001](../en/execution-audit.md#finding-uni-001) · [lines 173–183](../../simulations/geometry/vibrations/code/bravais_cordas_vibracoes.py) |
| <a id="study-field-visualizations"></a>[Field movies and visual readouts](../../simulations/geometry/field-visualizations/README.md) | **非完整 TRIAD — 已记录的偏离** | 演化源码使用了与参考不同的动能符号/噪声更新和条件状态守卫；其保存结果仍是该实现的记录。这适用于 simula_filmes；其余五个文件是读取器/渲染器。 | [审计记录](../en/execution-audit.md#study-field-visualizations) · [发现 UNI-001](../en/execution-audit.md#finding-uni-001) · [lines 234–246](../../simulations/geometry/field-visualizations/code/simula_filmes.py) |
| <a id="study-perturbation-tests"></a>[Responses to perturbations](../../simulations/signals/perturbation-tests/README.md) | **非完整 TRIAD — 已记录的偏离** | 演化源码使用了与参考不同的动能符号/噪声更新和条件状态守卫；其保存结果仍是该实现的记录。 | [审计记录](../en/execution-audit.md#study-perturbation-tests) · [发现 UNI-001](../en/execution-audit.md#finding-uni-001) · [lines 247–259](../../simulations/signals/perturbation-tests/code/teste_borboleta.py) |
| <a id="study-wifi-input"></a>[Fields initialized from WiFi scans](../../simulations/signals/wifi-input/README.md) | **非完整 TRIAD — 已记录的偏离** | 所提供的源码使用了与参考不同的动能符号/噪声更新和条件状态守卫。所需的 WiFi 测量未提供；本条目未记录使用这些测量的已演示运行。 | [审计记录](../en/execution-audit.md#study-wifi-input) · [发现 UNI-001](../en/execution-audit.md#finding-uni-001) · [lines 226–235](../../simulations/signals/wifi-input/code/bravais_wifi.py) |
| <a id="study-string-structure-tests"></a>[Strings, atoms and scale](../../simulations/structures/string-structure-tests/README.md) | **非完整 TRIAD — 已记录的偏离** | 演化源码使用了与参考不同的动能符号/噪声更新和条件状态守卫；其保存结果仍是该实现的记录。 | [审计记录](../en/execution-audit.md#study-string-structure-tests) · [发现 UNI-001](../en/execution-audit.md#finding-uni-001) · [文件](../../simulations/structures/string-structure-tests/FILES.md) |
| <a id="study-passive-r5"></a>[Passive memory dynamics](../../simulations/memory/passive-memory-dynamics/README.md) | **非完整 TRIAD — 已记录的偏离** | 运行器将 alpha、Gamma 与 FDT 置零，保留两个记忆模式。 | [审计记录](../en/execution-audit.md#study-passive-r5) · [lines 23–25](../../simulations/memory/passive-memory-dynamics/code/simulate_passive_memory.py) |
| <a id="study-causal-traces"></a>[Following causal traces](../../simulations/continuity/causal-traces/README.md) | **非完整 TRIAD — 已记录的偏离** | 四个因果运行器使用确定性的双记忆更新，无分数阶/热浴项。 | [审计记录](../en/execution-audit.md#study-causal-traces) · [文件](../../simulations/continuity/causal-traces/FILES.md) |

### 未确立为完整 TRIAD — 可追溯性不完整 · 25

缺失源码、配置、绑定的运行时或运行关联，无法确立完整性。图像与表格在其声明的限制下仍可使用。

| 研究 | 一致性 | 记录的范围 | 证据 |
|---|---|---|---|
| <a id="study-t-01"></a>[Early field relations](../../simulations/relations/early-field-relations/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 仅存场关系图像与孤立/耦合描述；无生成器与数值表。 | [审计记录](../en/execution-audit.md#study-t-01) · [lines 10–27](../../simulations/relations/early-field-relations/notes/original-record.md) |
| <a id="study-t-02"></a>[Memory and thermal noise](../../simulations/memory/memory-and-thermal-noise/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | NLS/记忆/热浴探索仅存为图像；无源码或数值表可固定所执行的算子。 | [审计记录](../en/execution-audit.md#study-t-02) · [lines 10–27](../../simulations/memory/memory-and-thermal-noise/notes/original-record.md) |
| <a id="study-t-03"></a>[Tracking density peaks](../../simulations/memory/tracking-density-peaks/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 峰值跟踪图像得以保存，但修订后的生成器与数值样本缺失。 | [审计记录](../en/execution-audit.md#study-t-03) · [lines 10–27](../../simulations/memory/tracking-density-peaks/notes/original-record.md) |
| <a id="study-t-04"></a>[Gaussian atoms in one field](../../simulations/structures/gaussian-atoms-in-one-field/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 多高斯探索有图像，但无保存的源码或 CSV。 | [审计记录](../en/execution-audit.md#study-t-04) · [lines 10–27](../../simulations/structures/gaussian-atoms-in-one-field/notes/original-record.md) |
| <a id="study-t-05"></a>[Individual fields](../../simulations/structures/individual-fields/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 分离标识的场以可视方式描述；实现与 CSV 缺失。 | [审计记录](../en/execution-audit.md#study-t-05) · [lines 10–27](../../simulations/structures/individual-fields/notes/original-record.md) |
| <a id="study-t-06"></a>[Limit-test attempt](../../simulations/signals/limit-test-attempt/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 仅有准备说明；无持久化的执行产物。 | [审计记录](../en/execution-audit.md#study-t-06) · [lines 10–20](../../simulations/signals/limit-test-attempt/notes/original-record.md) |
| <a id="study-t-07"></a>[Fast limit sweep](../../simulations/signals/fast-limit-sweep/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | N/半径扫描有 CSV 数值，但所提供的生成器不能确立完整动力学。 | [审计记录](../en/execution-audit.md#study-t-07) · [lines 10–27](../../simulations/signals/fast-limit-sweep/notes/original-record.md) |
| <a id="study-t-08"></a>[Observer relations in a field](../../simulations/relations/observer-and-observed/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 存在基线/观察者 CSV；场求解器与参数映射缺失。 | [审计记录](../en/execution-audit.md#study-t-08) · [lines 10–27](../../simulations/relations/observer-and-observed/notes/original-record.md) |
| <a id="study-t-09"></a>[Continuous relational field](../../simulations/relations/continuous-relational-field/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 存在基线/连续关系数据，但无生成求解器与完整配置。 | [审计记录](../en/execution-audit.md#study-t-09) · [lines 10–27](../../simulations/relations/continuous-relational-field/notes/original-record.md) |
| <a id="study-t-10"></a>[3D anti-collapse exploration](../../simulations/memory/3d-anti-collapse-exploration/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 早期三维探索仅存为图像与说明。 | [审计记录](../en/execution-audit.md#study-t-10) · [lines 10–27](../../simulations/memory/3d-anti-collapse-exploration/notes/original-record.md) |
| <a id="study-t-11"></a>[Long-run attempt](../../simulations/structures/long-run-attempt/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 仅有准备说明；有效的长时输出属于其他条目。 | [审计记录](../en/execution-audit.md#study-t-11) · [lines 10–18](../../simulations/structures/long-run-attempt/notes/original-record.md) |
| <a id="study-t-12"></a>[Fast 3D long run](../../simulations/structures/fast-3d-long-run/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 五项长时诊断保存为图像，无 CSV 或生成器。 | [审计记录](../en/execution-audit.md#study-t-12) · [lines 10–27](../../simulations/structures/fast-3d-long-run/notes/original-record.md) |
| <a id="study-t-13"></a>[Compact 3D long run](../../simulations/structures/compact-3d-long-run/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 紧凑长时拼图与诊断无保存的生成器与数值表。 | [审计记录](../en/execution-audit.md#study-t-13) · [lines 10–24](../../simulations/structures/compact-3d-long-run/notes/original-record.md) |
| <a id="study-t-14"></a>[Memory reference attempt](../../simulations/memory/memory-reference-attempt/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 仅有参考运行的准备；无产物可确立一次执行。 | [审计记录](../en/execution-audit.md#study-t-14) · [lines 10–18](../../simulations/memory/memory-reference-attempt/notes/original-record.md) |
| <a id="study-t-15"></a>[Accelerated memory reference](../../simulations/memory/accelerated-memory-reference/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 仅有加速准备说明；输出始于独立的 N=40 记录。 | [审计记录](../en/execution-audit.md#study-t-15) · [lines 10–18](../../simulations/memory/accelerated-memory-reference/notes/original-record.md) |
| <a id="study-t-17"></a>[Memory at resolution 48](../../simulations/memory/memory-grid-48/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 有 N=48 数值指标与 Bravais 评分；生成器与确切的方程项配置缺失。 | [审计记录](../en/execution-audit.md#study-t-17) · [lines 10–27](../../simulations/memory/memory-grid-48/notes/original-record.md) |
| <a id="study-t-19"></a>[Hot-bath diagnostic failure](../../simulations/signals/hot-bath-diagnostic-failure/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 热浴记录有 CSV，但未绑定求解器/配置以核查完整性。 | [审计记录](../en/execution-audit.md#study-t-19) · [发现 UNI-010](../en/execution-audit.md#finding-uni-010) · [lines 10–27](../../simulations/signals/hot-bath-diagnostic-failure/notes/original-record.md) |
| <a id="study-t-20"></a>[3D cold-bath box](../../simulations/signals/3d-cold-bath-box/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 冷浴 CSV 同时改变了网格、时长、初始样本和热浴条件。生成器缺失。 | [审计记录](../en/execution-audit.md#study-t-20) · [发现 UNI-010](../en/execution-audit.md#finding-uni-010) · [lines 10–27](../../simulations/signals/3d-cold-bath-box/notes/original-record.md) |
| <a id="study-t-21"></a>[First phase-to-density diagnostic](../../simulations/signals/first-phase-to-density-diagnostic/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 首个相位/密度探测器记录了近零估计；其生成器缺失。 | [审计记录](../en/execution-audit.md#study-t-21) · [发现 UNI-012](../en/execution-audit.md#finding-uni-012) · [lines 10–27](../../simulations/signals/first-phase-to-density-diagnostic/notes/original-record.md) |
| <a id="study-t-22"></a>[Refined phase-to-density diagnostic](../../simulations/signals/refined-phase-to-density-diagnostic/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 精细化探测器改变了刺激与观测窗口；其生成器缺失。 | [审计记录](../en/execution-audit.md#study-t-22) · [发现 UNI-012](../en/execution-audit.md#finding-uni-012) · [lines 10–27](../../simulations/signals/refined-phase-to-density-diagnostic/notes/original-record.md) |
| <a id="study-t-23"></a>[Memory and bounce](../../simulations/memory/memory-and-bounce/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 存在反弹指标与记忆记录，但所执行的热浴幅度/源码未完全绑定。 | [审计记录](../en/execution-audit.md#study-t-23) · [发现 UNI-008](../en/execution-audit.md#finding-uni-008) · [lines 10–27](../../simulations/memory/memory-and-bounce/notes/original-record.md) |
| <a id="study-t-27"></a>[Twelve initial atoms](../../simulations/structures/twelve-atoms-full-field/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 运行器调用历史绝对路径下的外部 triad-lang 运行时；该已执行的依赖未以哈希绑定。 | [审计记录](../en/execution-audit.md#study-t-27) · [发现 UNI-011](../en/execution-audit.md#finding-uni-011) · [lines 22–31](../../simulations/structures/twelve-atoms-full-field/code/simulate_twelve_atoms.py) |
| <a id="study-t-28"></a>[3D atom trajectories](../../simulations/structures/3d-atom-trajectories/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 三维轨迹运行器保留三个记忆模式与热浴，但导入了未绑定的历史运行时。 | [审计记录](../en/execution-audit.md#study-t-28) · [发现 UNI-011](../en/execution-audit.md#finding-uni-011) · [lines 24–33](../../simulations/structures/3d-atom-trajectories/code/simulate_atom_trajectories.py) |
| <a id="study-string-catalogue"></a>[A catalogue of strings](../../simulations/geometry/string-catalogue/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 采集器导入求解器默认值/环境覆盖；记录的行未绑定每个生成配置。 | [审计记录](../en/execution-audit.md#study-string-catalogue) · [lines 29–55](../../simulations/geometry/string-catalogue/code/colhe_cordas.py) |
| <a id="study-persistent-universe"></a>[A persistent field prototype](../../simulations/continuity/persistent-universe/README.md) | **未确立为完整 TRIAD — 可追溯性不完整** | 存在模态检查点/读出与连续性测试；演化委托给所提供源码中缺失的外部原生库。 | [审计记录](../en/execution-audit.md#study-persistent-universe) · [lines 30–40](../../simulations/continuity/persistent-universe/code/genesis_modal.py) |

### 非 TRIAD 执行 — 背景或后处理 · 12

规范说明、概念节点模型、重建或读出。它不包含新的全场演化，按其记录的内容阅读。

| 研究 | 一致性 | 记录的范围 | 证据 |
|---|---|---|---|
| <a id="study-entre-01-observer"></a>[Observer and observed](../../simulations/relations/observer/README.md) | **非 TRIAD 执行 — 背景或后处理** | 有限节点相位/边记忆概念关系模型，非完整场方程的执行。 | [审计记录](../en/execution-audit.md#study-entre-01-observer) · [lines 116–138](../../simulations/relations/observer/code/en/simulate_observer_observed_relations.py) |
| <a id="study-entre-02-between"></a>[The between](../../simulations/relations/between/README.md) | **非 TRIAD 执行 — 背景或后处理** | 有限节点相位/边记忆概念关系模型，非完整场方程的执行。 | [审计记录](../en/execution-audit.md#study-entre-02-between) · [lines 88–101](../../simulations/relations/between/code/en/simulate_consciousness_between.py) |
| <a id="study-entre-03-chemistry"></a>[Eight coupled channels](../../simulations/relations/chemical-channels/README.md) | **非 TRIAD 执行 — 背景或后处理** | 有限节点相位/边记忆概念关系模型，非完整场方程的执行。可选的化学/生命层是模型开关，而非直接的 P1/P2/P3 消融。 | [审计记录](../en/execution-audit.md#study-entre-03-chemistry) · [lines 113–152](../../simulations/relations/chemical-channels/code/en/simulate_neurotransmitters_between.py) |
| <a id="study-entre-04-life-filter"></a>[Memory and life filter](../../simulations/relations/life-filter/README.md) | **非 TRIAD 执行 — 背景或后处理** | 有限节点相位/边记忆概念关系模型，非完整场方程的执行。可选的化学/生命层是模型开关，而非直接的 P1/P2/P3 消融。 | [审计记录](../en/execution-audit.md#study-entre-04-life-filter) · [lines 139–184](../../simulations/relations/life-filter/code/en/simulate_life_filter_between.py) |
| <a id="study-bravais-02-strings"></a>[Strings from a saved state](../../simulations/geometry/string-analysis/README.md) | **非 TRIAD 执行 — 背景或后处理** | 对已保存场状态的后处理；本条目不演化完整方程。 | [审计记录](../en/execution-audit.md#study-bravais-02-strings) · [lines 1–12](../../simulations/geometry/string-analysis/code/cordas_arte.py) |
| <a id="study-visual-comparisons"></a>[Additional visual comparisons](../../simulations/geometry/visual-comparisons/README.md) | **非 TRIAD 执行 — 背景或后处理** | 保存的可视比较，未确立与生成运行的关联。 | [审计记录](../en/execution-audit.md#study-visual-comparisons) · [lines 5–9](../../simulations/geometry/visual-comparisons/README.md) |
| <a id="study-t-18"></a>[Visual atlas](../../simulations/geometry/visual-atlas/README.md) | **非 TRIAD 执行 — 背景或后处理** | 对已记录场的读出或几何重建，非新的场演化。 | [审计记录](../en/execution-audit.md#study-t-18) · [lines 10–22](../../simulations/geometry/visual-atlas/notes/original-record.md) |
| <a id="study-t-24"></a>[Bravais template map](../../simulations/geometry/bravais-template-map/README.md) | **非 TRIAD 执行 — 背景或后处理** | 对已记录场的读出或几何重建，非新的场演化。 | [审计记录](../en/execution-audit.md#study-t-24) · [发现 UNI-009](../en/execution-audit.md#finding-uni-009) · [lines 10–22](../../simulations/geometry/bravais-template-map/notes/original-record.md) |
| <a id="study-t-25"></a>[First geometric network](../../simulations/geometry/first-geometric-network/README.md) | **非 TRIAD 执行 — 背景或后处理** | 对已记录场的读出或几何重建，非新的场演化。 | [审计记录](../en/execution-audit.md#study-t-25) · [发现 UNI-009](../en/execution-audit.md#finding-uni-009) · [lines 10–22](../../simulations/geometry/first-geometric-network/notes/original-record.md) |
| <a id="study-t-26"></a>[Refined geometric network](../../simulations/geometry/refined-geometric-network/README.md) | **非 TRIAD 执行 — 背景或后处理** | 对已记录场的读出或几何重建，非新的场演化。 | [审计记录](../en/execution-audit.md#study-t-26) · [发现 UNI-009](../en/execution-audit.md#finding-uni-009) · [lines 10–22](../../simulations/geometry/refined-geometric-network/notes/original-record.md) |
| <a id="study-q00"></a>[Reference specification](../../simulations/field-diagnostics/reference-specification/README.md) | **非 TRIAD 执行 — 背景或后处理** | 规范说明与冻结的声明参数；本条目无执行结果。 | [审计记录](../en/execution-audit.md#study-q00) · [lines 6–14](../../simulations/field-diagnostics/reference-specification/notes/specification-record.md) |
| <a id="study-dimension-analysis"></a>[Measuring spatial structure](../../simulations/geometry/dimension-analysis/README.md) | **非 TRIAD 执行 — 背景或后处理** | 对已保存场状态的后处理；本条目不演化完整方程。 | [审计记录](../en/execution-audit.md#study-dimension-analysis) · [lines 1–12](../../simulations/geometry/dimension-analysis/code/bravais_dimensoes.py) |

## 覆盖范围与限制

65 个编目条目；静态与文档式核查；零模拟重跑；零保存字节改动。对大型记录进行了检索，并结合源码链接核查了每项结论背后的段落。

解释的更新位于本维护登记册和各研究页面。原始代码、数值、失败的诊断、INCONCLUSIVE 分类和历史结论在溯源记录中保持不变。

[项目规则](../en/project-rules.md) · [执行审计](../en/execution-audit.md) · [方程参考](../reference/equation/README.md) · [模拟目录](../../simulations/README.md)
