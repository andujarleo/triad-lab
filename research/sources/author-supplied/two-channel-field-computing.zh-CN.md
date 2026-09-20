<!-- Translation of: research/sources/author-supplied/two-channel-field-computing.md; source commit: 304d75ed6ff646d311fd9df8b4e2db0d4dee277a -->
# 支持双通道（BYTE/TOKEN）"Any-to-Any"架构的技术研究：连续学习桥与场方程抗坍缩系统

## TL;DR
- 本报告收集支持作者声明架构构建的技术材料——数学、算法与工程，按七条战线（A–G）组织：BYTE 摄入通道的主动推理/自由能；字节级模型与动态 patching；any-to-any 多模态架构；在线分配与学习 [0,1] 连续标量的方法；抗坍缩场方程的完整数学（NLS/Gross-Pitaevskii + 分数拉普拉斯 + 非厄米项 + 记忆 + 噪声）；作为计算基质的连续动力学；以及可微工程。
- 主要组件有具体、近期的文献基础：BLT（Meta，2024）与 H-Net（Hwang、Wang 与 Gu，2507.07955）对应 byte↔patch 前沿；L0/hard-concrete（Louizos 等，2017）与 stochastic gates 对应 [0,1] 连续标量；de Bouard 与 Debussche 关于乘性噪声可预防/延迟聚焦 NLS 坍缩的结果；以及 Boulenger 等的分数 blow-up 判据。所有这些都作为可用技术材料呈现，而非作者项目中同名术语含义的定义。
- 对作为整体处理的场方程的数值与可微实现，材料指向对称（Strang）split-step Fourier，分数拉普拉斯经傅里叶空间 |k|^σ 乘子，记忆项经指数和近似（O(1) 历史递推），Euler–Maruyama/Stratonovich 随机积分，以及带 checkpointing 的 backprop-through-the-solver 微分（torch.fft/JAX、diffrax、torchsde、TorchGPE）。

---

## Key Findings

1. **纯摄入模式下主动推理的 BYTE 通道在文献中是可持续的。**变分自由能原理（Friston）允许这样的表述：只发生感知/信念更新（变分自由能 F 最小化），与动作选择（期望自由能 G 最小化）分离。只最小化 F 而无 G 的策略/动作分支的系统，恰对应"摄入而无外部输出"。

2. **非常规 byte↔token/patch 边界有多项技术先例**——熵 patching（BLT）、带学习路由器与可微边界的动态 chunking（H-Net）、boundary predictors、局部 encoder 与全局 transformer 之间的 cross-attention。它们都不是固定 tokenization；都学习边界。

3. **通过"学习"在线分配与学习 [0,1] 连续数**得到直接支持：hard-concrete 随机门（Louizos 等）、高斯 stochastic gates（Yamada 等）、Gumbel-Softmax/Concrete 松弛，以及在线重要性分数（Fisher/EWC、Synaptic Intelligence 的 path-integral、MAS 的 output-gradient）。"学到了多少"的度量存在：信息增益、贝叶斯惊奇（Itti 与 Baldi）、压缩进展（Schmidhuber）。

4. **作者的场方程作为整体，与一个已研究的广义 NLS 家族数学一致。**每项都相互作用：聚焦三次非线性 Λ|Ψ|² 是坍缩（blow-up）的引擎，受 Zakharov–Glassey virial 恒等式支配；分数拉普拉斯 α(−Δ)^(σ/2) 改变临界性与色散（Laskin；Boulenger 等）；−iΓ 项耗散/吸收；V_mem 引入历史；η（噪声）按 de Bouard 与 Debussche 可预防或延迟坍缩。存在负面与矛盾结果（保守噪声可以正概率*加速* blow-up），此处予以保留。

5. **可微工程可行**：PyTorch/JAX 中带 autograd 的 FFT 使 split-step Fourier 完全可微；adjoint 方法（Chen 等，2018）与 checkpointing（Griewank 与 Walther）允许长 rollout 中内存可控的梯度；TorchGPE 已在 PyTorch 中于 autograd FFT 栈上实现了 split-step GPE/NLS 传播子。

---

## Details

### A) 主动推理与自由能（BYTE 通道，摄入）

**数学表述。**对生成模型 p(o,s) 与 recognition 密度 q(s)，时刻 t 的变分自由能为
F_t = E_{q(s)}[ ln q(s) − ln p(s, o_t) ] = D_KL[ q(s) ‖ p(s | o_t) ] − ln p(o_t).
因 D_KL 项 ≥ 0，F_t 是惊奇 −ln p(o_t)（负对数证据）的上界。感知推理为 q_t = argmin_q F_t。这是支撑纯摄入通道的目标：系统更新信念 q(s) 以最小化 F，而永不需发出动作。

主动推理经**期望自由能**增加动作选择（对策略 π，τ>t）：
G(π) = Σ_{τ>t} E_{q(s_τ,o_τ|π)}[ ln q(s_τ|π) − ln p(s_τ, o_τ) ],
其中 a_t* = argmin_a G(π ∋ a)。G 分解为风险（期望与偏好结果间散度）+ 歧义；等价为认知增益（信息寻求）+ 实用价值。**对纯摄入 BYTE 通道，G/动作分支省略；只有 F（感知/学习）运作。**学习（参数优化）与推理（状态优化）都是 F 的最小化；在 variational Bayes 中迭代自洽方程至收敛，或用 F 的梯度下降（Coordinate Ascent Variational Inference / fixed-point iteration 是 pymdp 使用的方法）。

**层级生成模型与预测编码。**预测编码（Rao 与 Ballard，1999，《Nature Neuroscience》；Friston，2005）将系统组织为层级：每层生成对下层活动的预测；预测误差经**精度**（方差倒数，"precision weighting"）加权，上行层级，驱动松弛与学习。Buckley、Kim、McGregor 与 Seth（2017），"The free energy principle for action and perception: A mathematical review"，在连续时间与连续状态下推导预测编码与主动推理——字节通道这类连续低层流的关键参考文献。

**预测编码作为 backprop 的替代。**Whittington 与 Bogacz（2017，《Neural Computation》）显示带局部 Hebb 可塑性的预测编码网络近似 backprop；Millidge、Tschantz 与 Buckley（2022，《Neural Computation》34(6):1329–1368），"Predictive coding approximates backprop along arbitrary computation graphs"（arXiv:2006.04182）；Song、Lukasiewicz、Xu 与 Bogacz（2020，NeurIPS），"Can the brain do backpropagation? — exact implementation of backpropagation in predictive coding networks"。保留的*批判/负面*结果：Zahid、Guo 与 Fountas（2023），"Predictive Coding as a Neuromorphic Alternative to Backpropagation: A Critical Evaluation"（《Neural Computation》35(12):1881–1909），批判评价了所称优势。Song、Millidge、Salvatori 等（2024，《Nature Neuroscience》），"Inferring neural activity before plasticity as a foundation for learning beyond backpropagation"（"prospective configuration"规则）。Millidge、Tang、Osanlouy、Harper 与 Bogacz（2024，《PLOS Computational Biology》20(4):e1011183），"Predictive coding networks for temporal prediction"——与时间序列/原始信号相关。

**深度主动推理、摊销推理、VAE、世界模型。**见 Millidge 等的 survey 与"The Free Energy Principle for Perception and Action: A Deep Learning Perspective"（arXiv:2207.06415）。摊销推理（训练 recognition 网络 q_φ，如 VAE）将主动推理与变分自编码器及世界模型连接。Tschantz、Millidge、Seth 与 Buckley（2023，《PLOS Comp. Biol.》），"Hybrid predictive coding: inferring, fast and slow"（arXiv:2204.02169）——结合摊销（快）与迭代（慢）推理。Neural Kalman Filtering（Millidge 等，arXiv:2102.10021）用于在线信念更新。

**库与具体实现。**
- **pymdp**（Heins、Millidge、Demekas、Klein、Friston、Couzin 与 Tschantz，2022，《JOSS》7(73):4098；arXiv:2201.03904）——Python、离散 POMDP、JAX 后端、CAVI/fixed-point iteration。仓库：github.com/infer-actively/pymdp；文档：pymdp-rtd.readthedocs.io。
- **RxInfer.jl**（Bagaev、Podusenko 与 De Vries，2023，《JOSS》8(84):5161）——Julia，经 factor graphs 与 message passing 的实时反应式贝叶斯推理；GraphPPL.jl 前端。
- **ForneyLab.jl**——用于 message passing 的 Forney factor graphs。
- **ActiveInference.jl**（2024/2025，PMC11765463）——Julia 重实现 pymdp，允许经采样与变分方法拟合经验数据。
- **SPM/DEM**（MATLAB）——SPM 内原始 Dynamic Expectation Maximization 工具箱。
- **cpp-AIF**（Gregoretti、Pezzulo 与 Maisto，2024，《Neurocomputing》568:127065）——多核 C++。
- 近期硬件加速工作："A Hardware-oriented Approach for Efficient Active Inference"（arXiv:2508.13177，2025）。

在主动推理中**离散化/实现**连续字节流：用带广义坐标的连续时间预测编码（Buckley 等，2017），或神经卡尔曼滤波（Millidge 等）；离散时间用 pymdp 的 POMDP 方案，矩阵 A（似然）、B（转移）、C（偏好——摄入模式省略）、D（初始状态先验）。

### B) 字节级模型与替代 TOKENIZATION

**Byte Latent Transformer（BLT）**——Pagnoni、Pasunuru、Rodriguez、Nguyen、Muller、Li、Zhou、Yu、Weston、Zettlemoyer、Ghosh、Lewis、Holtzman 与 Iyer（Meta，2024），"Byte Latent Transformer: Patches Scale Better Than Tokens"（arXiv:2412.09871；通讯：artidoro@cs.washington.edu，2024 年 12 月 16 日）。直接在字节上运作；按**下字节熵**将字节分组为**可变大小 patches**，熵由小型辅助字节级语言模型估计（100M 参数 transformer，14 层，512 维，512 字节滑动窗口）。当下字节不确定性（熵）超过阈值，打开 patch 边界——在数据复杂处分配更多计算。架构：轻量 **Local Encoder**（bytes→patches）、patches 上大型 **Latent/Global Transformer**、**Local Decoder**（patches→bytes）。它是"首个 FLOP 受控的字节级模型规模研究，至 8B 参数与 4T 训练字节"（"the first FLOP controlled scaling study of byte-level models up to 8B parameters and 4T training bytes"），BLT 在规模上匹敌基于 tokenization 的模型（Llama 3）。开放权重：facebook/blt-1b、facebook/blt-entropy（github.com/facebookresearch/blt）。2026 扩展："Fast Byte Latent Transformer"（arXiv:2605.08044）——N bytes → M ≈ N/4 patches。

**H-Net（Dynamic Chunking）**——Hwang、Wang 与 Gu（2025），"Dynamic Chunking for End-to-End Hierarchical Sequence Modeling"（arXiv:2507.07955）。完全端到端可微的**动态 chunking**机制：**路由器模块**预测自适应逐位置边界概率，切分为压缩表示；**平滑（smoothing）模块**在重构时插值以保持可微性；**残差连接**将 encoder 初始输出直接投影到 dechunking 阶段，连接局部字节级 features 与全局语境。基于 SSM 的 encoders/decoders 超过 Transformer 层。流程：Bytes → Encoder → Router → Chunking → Main Network → Dechunking → Decoder。按作者，"计算与数据匹配时，字节级单层级 H-Net 超过 BPE tokens 上的强 Transformer……匹敌两倍大小的基于 token 的 Transformer"。在 DNA 上，"每个 H-Net 模型以约 3.6× 更少数据达到相应各向同性模型相同的 pre-decay 困惑度"（≈3.6× 更少数据 / 对各向同性基线近 4× 数据效率提升）。2025/2026 变体：**H-Net++**（Zakershahrak 与合作者，arXiv:2508.05628）面向形态丰富语言（波斯语）——1.9M 参数 context-mixer、两级 hyper-prior、0.159 BPB 降低（12% 更好压缩）vs GPT-2-fa；"Adaptive Targeted Dynamic Chunking"（arXiv:2605.30080）；"ByteGen"（arXiv:2508.02247，金融数据）；"Distilling Token-Trained Models into Byte-Level Models"（arXiv:2602.01007）。

**其他 byte/tokenizer-free。**
- **MegaByte**（Yu 等，2023）——双 decoder Transformer 层级（*固定*大小 patches 上全局 + 字节上局部自回归）；语境至 1.2M bytes。
- **MambaByte**（Wang、Gangavarapu、Yan 与 Rush，2024，COLM），"Token-free Selective State Space Model"（arXiv:2401.13660）——字节级 Mamba（SSM），线性时间；受控 FLOPs 下超过 MegaByte。按作者，"tokenized drafting 与 byte-level 验证的 speculative decoding 改编……相对标准 MambaByte 实现产生 2.6× 推理加速"（"This results in a 2.6× inference speedup to the standard MambaByte implementation"）。
- **SpaceByte**（Slagle，2024，NeurIPS；arXiv:2404.14408）——将字节划分为对齐词边界的 patches；按作者，"在 PG-19 上，SpaceByte 达到 bits-per-byte 1.009……显著好于 MegaByte 的 1.083 与 byte-level Transformer 的 1.138"（byte-level 与 MegaByte 需 ~10× 更多训练 FLOPs 才达 subword 相当性能）。代码：github.com/kjslag/spacebyte。
- **MBLM**（arXiv:2502.14553，2025）——Multiscale Byte Language Models，无限阶段层级、每阶段不同 decoders，单 GPU 选择性 checkpointing 下至 5M bytes。
- **ByT5**（Xue 等，2022，《TACL》10:291–306）、**CANINE**（Clark 等，2022）——带 downsampling 的 byte/char encoders。
- **bGPT / "Byte Models are Digital World Simulators"**（Wu 等，2024）——字节建模即数字世界模拟。
- **Perceiver / Perceiver IO / Perceiver AR**——从 latent array 到超高维输入的 cross-attention，经学习 latent bottleneck 桥接粒度。
- 精选列表：github.com/zjysteven/Awesome-Byte-LLM。

**粒度间桥接（byte↔patch）。**使用的具体机制：局部 encoder（byte）与全局 transformer（patch）间 cross-attention；学习 pooling；**boundary predictors**（BLT 经熵；H-Net 经带边界概率的路由器）；可微插值/平滑以恢复分辨率（H-Net）。关于 soft tokens/连续 embeddings 作为层间接口的工作包括 BLT 的 patch 隐表示（任意字节组经轻量学习 encoder/decoder 映射到隐表示，无固定词表）。

### C) 多模态 ANY-TO-ANY 架构

概览（参考 survey："Unified Multimodal Understanding and Generation Models: Advances, Challenges, and Opportunities"，arXiv:2505.02567，带 2023–2025 timeline；列表：github.com/aidc-ai/awesome-unified-multimodal-models 与 github.com/any2any-mllm/awesome-any2any）。

**策略家族：**
- **自回归 + modality-specific tokenizers → 离散 tokens：****4M** 与 **4M-21**（Mizrahi/Kar 等，EPFL/Apple；arXiv:2406.09406）——经 modality-specific tokenizers 将数十模态映射到离散 tokens（image-like 模态用基于 ViT 的 VQ-VAE；3D 姿态/embeddings 用基于 MLP 的离散 VAE），多模态掩码目标，至 3B 参数与 21 模态（RGB、edges、SAM、4DHumans 姿态、调色板、元数据、DINOv2/ImageBind features、T5-XXL embeddings）；4m.epfl.ch 开源代码。**Chameleon**（Meta，2024，arXiv:2405.09818）——带 VQ-IMG 的 early-fusion mixed-modal，因果。**Emu3**（BAAI，2024，arXiv:2409.18869）——"Next-Token Prediction is All You Need"，SBER-MoVQGAN。**AnyGPT**（2024）——音频用 EnCodec、语音用 SpeechTokenizer、modality-specific 前缀。**Unified-IO 2**（Lu 等，2024）——带视觉/音频/语言的结构化 encoder-decoder。
- **AR + 扩散头 / 扩散与自回归混合：****Transfusion**（Zhou、Yu、Babu 等，Meta，2024，arXiv:2408.11039）——在同一多模态 transformer 中预测下个 token 并扩散图像。**Show-o**（Xie 等，2024，arXiv:2408.12528）——集成离散扩散 schedule。**Bagel/BAGEL** 与 **Hyper-Bagel**（arXiv:2509.18824，2025）——统一加速 framework。
- **视觉编码解耦：****Janus / Janus-Pro**（DeepSeek，Wu 等，2025，CVPR）——为理解 vs 生成解耦视觉编码。
- **共享隐空间 / 跨模态对齐：****CoDi** 与 **CoDi-2**（Tang 等，2023）——可组合扩散，从任意输入组合并行生成任意模态组合。**NExT-GPT**（Wu 等，2023，arXiv:2309.05519；ICML 2024）——LLM（Vicuna-7B）+ ImageBind（6 模态统一 encoder）+ adapters + 扩散 decoders；只调 ~1% 参数——"NExT-GPT is tuned with only a small amount of parameter (1%) of certain projection layers"（~12.3B 中 ≈164M，即 ≈1.3%）——加 MosIT instruction tuning（≈5,000 精选对话）。保留的*负面/局限*结果：CoDi 作者指出它"未达到深度人类式推理"；NExT-GPT 仍依赖冻结预训练 encoders/decoders。
- **近期 2025/2026：**M2-omni（arXiv，多 tokenizers/decoders）、Emu3.5（"Native Multimodal Models are World Learners"，2025-10）、Uni-X（ICLR 2025，模态冲突用 "two-end-separated"）、OneCAT、MMaDA、Show-o2（arXiv:2506.15564）、FUDOKI（discrete flow，arXiv:2505.20147）。

与作者项目相关的**关键策略**：(i) 通用 tokenizers vs 共享 backbone 上的 modality-specific 投影；(ii) 模态间路由与多模态 mixture-of-experts；(iii) 扩散混合（连续输出）与自回归（离散输出）。尊重的风格注记：VQ-VAE 中"坍缩"（"dimensional collapse in VQVAEs"，NeurIPS）是同名现象，仅作参考呈现。

### D) 在线学习的 [0,1] 连续学习值

本节收集作者学习计算的材料——为每次学习分配 [0,1] 连续数（明确非二元）并在线学习该数。以下方法为文献材料；此处"学习"一名不预设与作者概念等价。

**连续 gating 与连续松弛。**
- **L0 regularization / hard-concrete gates**——Louizos、Welling 与 Kingma（2017），"Learning Sparse Neural Networks through L0 Regularization"（arXiv:1712.01312）。非负随机门决定哪些权重置零；**hard-concrete** 分布通过"拉伸" binary concrete 并过 hard-sigmoid 得到，在恰 {0,1} 上赋质量，其余在 (0,1)。具体公式：
  s_i = σ( (log u − log(1−u) + α_i)/τ ),  u ~ Uniform(0,1)
  s̄_i = s_i(ζ − γ) + γ,  典型 γ = −0.1, ζ = 1.1，随后 [0,1] 上 hard-sigmoid clamp。
  参数 α（与温度 β/τ）与网络一起梯度训练——这正是"在线学习连续值"。门的期望值为 σ(log α − β' log(−γ/ζ))。
- **Concrete / Gumbel-Softmax**——Maddison、Mnih 与 Teh（2016，arXiv:1611.00712）及 Jang、Gu 与 Poole（2016）——离散变量的连续松弛，上述门的基础。
- **高斯 Stochastic Gates（STG）**——Yamada、Lindenbaum、Negahban 与 Kluger（2020），"Feature Selection using Stochastic Gates"（arXiv:1810.04247）：z_d = max(0, min(1, μ_d + ε_d))，ε_d ~ N(0, σ²)，μ_d 学习——[0,1] 上高斯 clamp，方差小于 hard-concrete。语境/条件扩展：arXiv:2312.14254。
- **GRU/LSTM 门与 attention weights**作为经 sigmoid/softmax 的 (0,1) 连续权重，是学习连续 gating 的经典先例。

**重要性/置信度的在线估计。**
- **Elastic Weight Consolidation（EWC）**——Kirkpatrick 等（2017，《PNAS》；arXiv:1612.00796）。重要性 Ω_i = **Fisher 信息矩阵**对角（损失局部曲率 / KL 的 Hessian）。二次惩罚 Σ_i (F_i/2)(θ_i − θ_i*)²。保留的*负面/批判*结果：EWC"持续显示次优性能"；FIM 依赖在某些场景导致梯度消失与不精确估计（arXiv:2603.18596，"Elastic Weight Consolidation Done Right"）。
- **Synaptic Intelligence（SI）**——Zenke、Poole 与 Ganguli（2017，ICML）。一阶 **path-integral** 度量，沿优化轨迹累积（每突触对损失下降的贡献）——构造上是在线估计子。
- **Memory Aware Synapses（MAS）**——Aljundi 等（2018）。重要性 = 网络输出对权重的梯度幅度（输出的平方 L2 范数），可无监督在线计算。
- **权重的贝叶斯在线学习 / 卡尔曼滤波**——权重后验的增量贝叶斯更新；"Neural Kalman Filtering"（Millidge 等，arXiv:2102.10021）用于权重/状态。

**速率的元学习与 credit assignment。**
- **Hypergradient descent**（Baydin 等，2018）——经损失对速率本身的梯度学习学习率。
- **Learned optimizers** 与 **adaptive per-parameter step sizes**——逐参数步长的元学习。
- **Learning to reweight examples**（Ren 等，2018）与 **Meta-Weight-Net**（Shu 等，2019）——学习每样本连续权重；**focal weighting**（Lin 等，2017）——按难度的连续权重。这些正是学习的"curriculum/sample weighting"，为每项分配连续标量。

**"学到了多少"的度量。**
- **Prediction gain / information gain**——可归因于某项的损失/不确定性降低。
- **贝叶斯惊奇（Bayesian surprise）**——Itti 与 Baldi（2009，《Vision Research》49(10):1295–1306，DOI:10.1016/j.visres.2008.09.007，PMCID PMC2782645）："惊奇以后验与先验信念差异度量数据如何影响观察者"——形式上为观测数据后的 D_KL[posterior ‖ prior]。它是"已知最强的人类注意力吸引子"，72% 视线偏离指向高于平均惊奇处（视频中 84%）。可直接用作驱动 [0,1] 连续值的信号。
- **Compression progress / learning progress**——Schmidhuber（2009），"Driven by Compression Progress…"（arXiv:0812.4360）与"Formal Theory of Creativity, Fun, and Intrinsic Motivation (1990–2010)"（《IEEE TAMD》2010）：内在强化是主观可压缩性随时间的*一阶导数*——非压缩程度本身（避免奖励噪声）。好奇心的 Latent Bayesian Surprise：Mazzaglia 等（2021，AAAI）。保留的*负面*注记："Interestingness as an Inductive Heuristic for Future Compression Progress"（arXiv:2605.14831）证明，在一般 MDP 中，经 in-context 预测误差导出的 rewards 无偏估计 learning progress 不可能；正面结果仅对非时间子类（active learning / Bayesian Experimental Design）。

### E) 作者场方程的数学（所有项一起）

声明的方程：
i·ℏ·∂_t Ψ = [ −ℏ²/(2m)∇² + V_ext + Λ|Ψ|² + V_mem + α(−Δ)^(σ/2) − iΓ ]Ψ + η

此处将各项作为耦合系统呈现，显示它们如何相互作用——而非孤立部件。

**NLS/Gross-Pitaevskii 核心（动能 + Λ|Ψ|²）。**无其他项时，为聚焦 NLS（聚焦/吸引约定下 Λ<0），i∂_tΨ = −½∇²Ψ + Λ|Ψ|²Ψ，有 V_ext trap 时即 Gross-Pitaevskii 情形。守恒不变量（无 −iΓ、η、V_mem 时）：质量/范数 M = ∫|Ψ|²、能量/哈密顿 E = ∫ [½|∇Ψ|² + (Λ/2)|Ψ|⁴] 与动量。**坍缩/blow-up：**受 **virial 恒等式**（方差）V(t) = ∫ |x|²|Ψ|² dx 支配，其二阶时间导数满足 d²V/dt² = 8E（临界非线性），故 E<0 迫使 V(t)→0 有限时间 → blow-up（Vlasov–Petrishchev–Talanov 与 **Zakharov–Glassey** 判据）。三次非线性的**临界维度**为 d=2（L² 临界：指数 1+4/d）；d<2 次临界（全局存在），d>2 超临界。L² 临界情形有 Merle–Raphaël 的 blow-up 速率 log-log 律。参考文献：Colliander/Merle–Raphaël 笔记（math.utoronto.ca）；"Enhancement of the Zakharov-Glassey's method for Blow-Up in NLS"（arXiv:2203.08522）；Merle，"Blow-up Results of Virial Type for Zakharov Equations"（《CMP》175(2)）。

**分数拉普拉斯 α(−Δ)^(σ/2)（分数薛定谔 / Lévy 动力学）。**经傅里叶乘子定义：(−Δ)^s u = F^{-1}[ |ξ|^{2s} F(u) ]——代码中在傅里叶空间乘 |k|^σ（作者约定 σ = 2s）。由 **Laskin** 引入（2000，《Phys. Lett. A》268:298–305；2002，《Phys. Rev. E》66:056108），将 Feynman path integral 从布朗轨迹扩展到 Lévy 轨迹。对坍缩的影响：对聚焦分数 NLS i∂_t u = (−Δ)^s u − |u|^{2p}u，**Boulenger、Himmelsbach 与 Lenzmann** 的一般 blow-up 判据对 p ≥ 2s/N 成立（径向，N≥2）；L² 临界情形为 p = 2s/N。较小 s（更"分数"）降低色散从而改变坍缩阈值。分数↔三次幂组合相互作用：Feng（2018，arXiv:1804.00973 及《CPAA》），"On the blow-up solutions for the fractional NLS with combined power-type nonlinearities"，0<p₁<p₂<2s/(N−2s)，带 sharp 质量阈值。保留的*开放*结果：局域 FNLS 的一般 blow-up 存在定理仍是开放问题，有数值证据支持（引于 arXiv:1804.00973）。s=1/2 时 FNLS 作为玻色子星/半相对论模型。

**耗散/吸收项 −iΓ（非厄米）。**使哈密顿非厄米；复势模拟增益/损失。**PT-symmetry**：PT 对称哈密顿虽非厄米可有实谱；在光子学中，复势 = 带局域放大/吸收的介质。与 **Lindblad master 方程**的关系：有效非厄米哈密顿从开放系统 Lindblad 动力学涌现（−iΓ 项即单粒子损失，ρ_{11}(t)=ρ_{11}(0)e^{−2γt}）。**Complex absorbing potentials（CAP）**用于在边界吸收波函数。与 blow-up 预防的关系：耗散/吸收（Γ>0） 消耗范数与能量，可能预防爆炸。参考文献：El-Ganainy 等（2018），"Non-Hermitian physics and PT symmetry"（《Nat. Phys.》14:11）；"Density Matrix Formalism for PT-Symmetric Non-Hermitian Hamiltonians with the Lindblad Equation"（arXiv:2006.02445）；"Dissipative Dynamics and Active Stabilization of Linear and Nonlinear Waves in Non-PT-Symmetric Harmonic Traps"（arXiv:2605.12638，2026），明确处理经虚势主动稳定非线性波。对阻尼分数 NLS："Global existence for the nonlinear fractional Schrödinger equation with fractional dissipation"（arXiv:1704.05307）——任意阻尼项 a>0 全局存在。

**随机 forcing η（随机 NLS）。****de Bouard 与 Debussche** 文献是核心，包含此处保留的正面与矛盾结果：
- 乘性噪声（时间白、空间相关）效应为*延迟* blow-up；白噪声甚至可*预防* blow-up（de Bouard、Debussche 与 Di Menza，2001，《Journées EDP》观察）。
- 然而，de Bouard 与 Debussche（2005，《Ann. Probab.》33(3):1078–1110），"Blow-up for the stochastic NLS with multiplicative noise"：超临界情形，空间光滑噪声可对任意光滑初值以正概率*导致*即时 blow-up。
- L² 超临界情形*保守*（Stratonovich）噪声以正概率*加速* blow-up；大*非保守*（高斯乘性）噪声可以高概率在任意有界区间*预防* blow-up（Barbu、Röckner 与 Zhang；见 arXiv:2210.17010 及《Nonlinear Analysis》136:102–116，2016）。加性效应：de Bouard 与 Debussche（2002，《Probab. Theory Relat. Fields》123:76–96）。
- 基础：de Bouard 与 Debussche（1999，《CMP》205:161；2003，《Stoch. Anal. Appl.》21:97）——经随机 Strichartz 估计的 L² 与 H¹ well-posedness。随机分数情形："Stochastic Perturbations in the Fractional NLS: Well-posedness and Blow-up"（arXiv:2308.10270）——指出经典方差-virial 律在分数场景*失效*，需经 Itô 公式随机推广。能量临界情形：arXiv:2604.14852（2026）。"Stochastic Schrödinger equations"/quantum state diffusion（Fagnola 与 Mora，2013）将 η 与量子态扩散连接。

**记忆项 V_mem（历史依赖势）。**文献中实现历史依赖的形式：
- **非瞬时响应（光学中 Raman 型）：**GNLSE，R(t) = (1−f_R)δ(t) + f_R h_R(t)，其中 δ 项为瞬时 Kerr，h_R 卷积为记忆。Blow–Wood kernel：h_R(t) = Θ(t)·(τ₁²+τ₂²)/(τ₁τ₂²)·e^{−t/τ₂}·sin(t/τ₁)，石英 f_R=0.18，τ₁=12.2 fs，τ₂=32 fs（Blow 与 Wood，1989，《IEEE JQE》25(12):2665；Lin 与 Agrawal，2006，《Opt. Lett.》31(21):3086；Agrawal，《Nonlinear Fiber Optics》，第 6 版）。
- **带卷积 kernel 的 integro-differential 方程：**i∂_tΨ = H₀Ψ + ∫₀^t K(t−t′)Ψ(t′)dt′。非平稳 kernels："Exact treatment of the memory kernel under time-dependent system-environment coupling"（arXiv:2505.00386）。经 Laplace/Green 的薛定谔时间非局域势（arXiv:2502.18700）。
- **时间分数导数（时间分数薛定谔）：**Naber（2004，《J. Math. Phys.》45(8):3339；arXiv:math-ph/0410028）——以 α 阶 Caputo 导数替代 ∂_t；哈密顿变非厄米且时间非局域；Mittag-Leffler 函数解；*概率不守恒*（保留结果）。Caputo 导数：₀^C D_t^α f = 1/Γ(1−α) ∫₀^t f′(τ)(t−τ)^{−α} dτ，α∈(0,1)。
- **数据驱动 kernel 发现**（若 V_mem 被学习）："Neural Discovery of Memory and Nonlocal Kernels in Integro-Differential Equations with Constrained KANs"（arXiv:2607.11110）；MINPO（arXiv:2512.17273）。

**所有项如何相互作用（作为整体的抗坍缩）。**材料表明坍缩 vs 全局存在行为从*联合竞争*涌现：聚焦 Λ|Ψ|² 推向 blow-up；动能与分数 α(−Δ)^(σ/2) 色散（指数 σ 调整临界阈值）；V_ext（trap）可约束；−iΓ 消耗范数/能量（预防爆炸的耗散）；η 按非保守 vs 保守乘性可预防/延迟或加速 blow-up；V_mem 增加历史项，其延迟响应改变瞬时动力学。文献中*已知*的抗坍缩机制，作为平行材料呈现（非替代作者机制）：非线性饱和（如 cubic-quintic CQNLS——Nature《Sci. Rep.》7285，非零 background 中断坍缩并生成色散激波）、耗散/吸收、非厄米项、稳定噪声、traps 与非局域相互作用（arXiv:1008.1891，"Collapse in the nonlocal NLS"）。

**完整方程的实用数值方法。**
- **Split-step Fourier / pseudo-spectral（Strang，对称）。**写 ∂_tΨ = (L+N)Ψ，L = 线性部分（动能 + 分数 + 耗散，傅里叶对角），N = 非线性部分（Λ|Ψ|² + V_ext + V_mem，物理空间对角）。对称 O(Δt²) 步：(i) 傅里叶线性半步 Ψ̂ ← e^{iL̂Δt/2}Ψ̂；(ii) 物理空间全非线性步 Ψ ← e^{iN(|Ψ|²)Δt}Ψ；(iii) 线性半步。**分数拉普拉斯作为 |k|^σ 乘子**进入傅里叶线性算子：L̂ = −(ℏ/2m)|k|² − α|k|^σ − iΓ。对分数 NLS：Klein 等，time-splitting spectral（arXiv:1908.05719，谐振子势）；"A split-step Fourier pseudo-spectral method for space-fractional coupled NLS"（《Commun. Nonlinear Sci. Numer. Simul.》，ScienceDirect S1007570423000680）；"A split-step finite element method for the space-fractional Schrödinger equation in 2D"（PMC11484848）。
- **稳定性与时间步：**soliton 背景上 split-step 数值不稳定性（Weideman–Herbst）需注意步长；见 arXiv:1008.4974 与平面波稳定性分析（arXiv:1306.0656）。对称格式将误差改进至 O(Δt²)。
- **数值记忆项：****L1 scheme**（Caputo，2−α 阶）离散化卷积积分：∂̄_n^α φ = Σ_{j=1}^n b_{n−j}∂̄_jφ，b_j = Δt^{1−α}/Γ(2−α)·[(j+1)^{1−α}−j^{1−α}]——O(N²) 时间代价，O(N) 内存。Jiang、Zhang、Zhang 与 Zhang（2017，《Commun. Comput. Phys.》21(3):650–678；arXiv:1511.03453）的**指数和（SOE）近似**：以 Σ_ℓ w_ℓ e^{−s_ℓ t} 近似 t^{−1−α} kernel，使卷积*递推*（每模 y_ℓ^n = e^{−s_ℓΔt}y_ℓ^{n−1} + 局部求积），降至 O(N·N_exp) 工作量与 O(N_exp) 内存——完全可微（仅 exp/mult/sum）。高阶格式：L1-2、Alikhanov 的 L2-1σ（3−α 阶）；空间 4 阶 compact（DOI 10.1186/s13662-020-02946-w）。
- **随机积分器（对 η）：**Euler–Maruyama（一般噪声强 1/2 阶）、SPDE 的 Milstein 与高阶格式；Itô vs Stratonovich 解释重要（保守噪声是 Stratonovich）。de Bouard、Debussche 与 Di Menza 给出带收敛证明的随机 NLS 数值格式。
- **Crank-Nicolson 与 relaxation 格式：**Besse 的 relaxation 格式在 NLS 中保持不变量；Riesz 分数 NLS 的保守 CN-FDM。
- **指数积分器**用于刚性线性部分。
- **联合处理：**经 splitting 在单一积分器中处理所有项：{动能、分数、−iΓ} 归入傅里叶算子（精确指数），{Λ|Ψ|², V_ext} 归入物理步，V_mem 经每步更新的 SOE 递推，η 经 Euler–Maruyama 在物理步注入。
- **库/代码：****GPELab**（Antoine 与 Duboscq，2014/2015，《Comput. Phys. Commun.》185:2969 与 193:95；gpelab.math.cnrs.fr）——MATLAB，pseudo-spectral/relaxation/Crank-Nicolson，带局域与非局域非线性的 1D/2D/3D GPE，多组分，随机动力学。**XMDS2**（Dennis、Hope 与 Johnsson，2013，《Comput. Phys. Commun.》184:201；arXiv:1204.4255；xmds.org）——随机 SPDE 的 XML→C++ 代码生成器，谱方法，自适应 RK，MPI。**TorchGPE**（Fioroni 等，2024，《SciPost Phys. Codebases》38；arXiv:2404.14401；github.com/qo-eth/TorchGPE）——PyTorch 中对称 split-step GPE/NLS solver，GPU，任意含时/自洽势；构建于 PyTorch autograd FFT 栈上。**GPUE**（Schloss 与 O'Riordan，2018，《JOSS》3(32):1037）、**spinor-GPE**（PyTorch）、**BEC2HPC**。

### F) 作为 AI 模型基质的场方程与连续动力学

**Neural ODEs / SDEs / 连续时间 RNNs。**
- **Neural ODEs**——Chen、Rubanova、Bettencourt 与 Duvenaud（2018，NeurIPS；arXiv:1806.07366）：dz/dt = f(z,t,θ)，adjoint 方法 backprop，O(1) 内存。
- **Neural SDEs**——Li、Wong、Chen 与 Duvenaud（2020，AISTATS；arXiv:2001.01328），"Scalable Gradients for SDEs"——torchsde 的基础。
- **Continuous-time RNNs（CTRNN）**——Funahashi 与 Nakamura（1993）。
- **Liquid Time-Constant networks（LTC）**——Hasani 等（2021）：dx/dt = −[1/τ + f(x,u,t)]x + f(x,u,t)A，输入依赖 time-constants；**CfC**（Closed-form Continuous-time，Hasani 等，2022）给解析解（~20× speedup）；**Liquid-S4** 集成 LTC 与 SSMs。LFM2（arXiv:2511.23404）是近期应用。

**状态空间模型（SSMs）与连续时间表述。**S4（Gu、Goel 与 Ré，2021）、S5、**Mamba/Mamba-2**（Gu 与 Dao，2023/2024）：结构化线性递推；连续时间经 zero-order hold（ZOH）离散化，一阶等价 Euler（arXiv，"Mamba neural operator"；"Demystifying the Token Dynamics of Deep Selective State Space Models"，arXiv:2410.03292）。作为基质相关，因其连接连续动力学 ↔ 序列，且 H-Net 的 encoders/decoders 用 SSMs。

**PINNs 与 operator learning。**物理网络（PINNs）与算子学习：**Fourier Neural Operator（FNO）**（Li 等，2020）与 **DeepONet**（Lu 等，2021）学习函数空间间算子——学习场/PDE 算子的方式。"Mamba neural operator"（ScienceDirect S0021999125008496）将 SSM 推广到 PDE 家族的神经算子。

**哈密顿/量子动力学作网络核心。****Hamiltonian Neural Networks**——Greydanus、Dzamba 与 Yosinski（2019，NeurIPS；arXiv:1906.01563）：学 H(q,p)，损失 L = ½[(∂H/∂p − dq/dt)² + (∂H/∂q + dp/dt)²]，守恒能量且时间可逆（代码：github.com/greydanus/hamiltonian-nn）。相关：Lagrangian Neural Networks（Cranmer 等，2020，arXiv:2003.04630）、Symplectic RNN（Chen 等，2020，arXiv:1909.13334）、Hamiltonian Generative Networks（Toth 等，2020，arXiv:1909.13789）。HNNs 是 Neural ODEs 子类（学习的 H 定义经辛 solver 积分的向量场）。Unitary Evolution RNN（Arjovsky、Shah 与 Bengio，2016，ICML；arXiv:1511.06464）——保持相位的酉动力学，避免 vanishing/exploding gradients。

**复与波基表示。**
- **Deep Complex Networks**——Trabelsi、Bilaniuk、Zhang、Serdyuk、Subramanian、Santos、Mehri、Rostamzadeh、Bengio 与 Pal（2018，ICLR；arXiv:1705.09792）：复卷积、复 batch-norm（经 2×2 real/imag 协方差矩阵 whitening）、Rayleigh 初始化、复激活（modReLU、CReLU）。代码：github.com/ChihebTrabelsi/deep_complex_networks。
- **复 backprop / Wirtinger calculus**——算子 ∂/∂z = ½(∂/∂x − i∂/∂y)，∂/∂z* = ½(∂/∂x + i∂/∂y)。对实损失 L，下降方向用*共轭*导数 ∂L/∂z*（PyTorch 复 autograd 采用的约定）。非全纯链式法则：∂L/∂z* = (∂L/∂w)(∂w/∂z*) + (∂L/∂w*)(∂w*/∂z*)。参考文献：Brandwood（1983，《IEE Proc. F》130(1):11）、Kreutz-Delgado（arXiv:0906.4835）、survey arXiv:2101.12249、Hirose（2012，Springer）。
- **相位作信息载体：**Reichert 与 Serre（2014，ICLR；arXiv:1312.6115），"Neuronal Synchrony in Complex-Valued Deep Networks"。
- **Holographic Reduced Representations（HRR）**——Plate（1995）——经循环卷积 binding。**Vector Symbolic Architectures / Hyperdimensional Computing**（Kanerva）——高维向量中 binding/bundling；与分布式表示及相位的连接。

**表示坍缩（平行技术参考——不替代作者机制）。**ML 中同名"坍缩"现象：**representation collapse**（features 坍缩到单值，方差→0）、**dimensional collapse**（表示不用满空间；经协方差 singular values 度量）、**informational collapse**（相关 features）、transformers 中 **rank collapse**。已知抗坍缩机制：**VICReg**（Bardes、Ponce 与 LeCun，2022）——方差项（标准差 ≥ γ 上 hinge）、不变性与协方差（最小化 off-diagonals）；**Barlow Twins**（Zbontar 等，2021）——迫 cross-correlation 矩阵为单位阵（"soft whitening"）；**whitening**（Ermolov 等，2021）；权重**谱 / 正交**正则（WERank，arXiv:2402.09586）。风格注记：作为平行材料呈现；此处"坍缩"一名不预设与作者方程对抗的"坍缩"等价。

### G) 工程与实现

**在可微 pipeline 内耦合 PDE/场 solver。**
- **Adjoint 方法（continuous / optimize-then-discretize）：**推导 adjoint ODE a(t)=∂L/∂z(t)，da/dt = −a(t)ᵀ∂f/∂z（后向积分），dL/dθ = −∫ a(t)ᵀ∂f/∂θ dt；O(1) 内存但梯度*近似*（逆向重构累积误差）。即 Diffrax 的 `BacksolveAdjoint`，因不精确被标"不推荐"。理论根源：Pontryagin 等（1961）。
- **Backprop-through-the-solver（discretize-then-optimize）：**微分 solver 实际离散操作 → *精确*梯度，较大内存，经 **checkpointing** 缓解（Griewank 与 Walther，"Algorithm 799: revolve"，《ACM TOMS》2000；ANODE，Gholami、Keutzer 与 Biros，IJCAI 2019，arXiv:1902.10298；Adaptive Checkpoint Adjoint，Zhuang 等，ICML 2020；Symplectic Adjoint，Matsubara、Miyatake 与 Yaguchi，NeurIPS 2021，arXiv:2102.09750）。即 `RecursiveCheckpointAdjoint`（Diffrax 默认）。对 split-step Fourier，推荐 discretize-then-optimize（精确梯度）加 checkpointing——FFT 是酉线性算子，其 VJP 为另一（共轭）FFT，故梯度干净流过 `fft`/`ifft` + 逐点乘法。另见 McCallum 等（arXiv:2410.11648，"Efficient, Accurate and Stable Gradients for Neural ODEs"）与 Kidger（DPhil 论文，Oxford，2021，"On Neural Differential Equations"）。

**Frameworks。**
- **PyTorch `torch.fft`**（1.8 起）：autograd + GPU（cuFFT）。*注意*：复 autograd 用 Wirtinger-共轭约定（存的 grad 是 ∂L/∂z*）；`.backward()` 前约化到实标量（否则 RuntimeError）。
- **JAX**（`jax.numpy.fft`、`jax.lax`）：可微，XLA GPU/TPU；与 `grad`/`vjp` 组合。
- **diffrax**（Kidger，JAX；github.com/patrick-kidger/diffrax，docs.kidger.site/diffrax）——ODE/SDE/CDE，多 adjoints（`RecursiveCheckpointAdjoint`、`BacksolveAdjoint`、`ImplicitAdjoint`）；构建于 Equinox 上，Python 3.10+。
- **torchdiffeq**（github.com/rtqichen/torchdiffeq）——`odeint`/`odeint_adjoint`（adjoint 要求 `func` 为 `nn.Module`）；dopri5/dopri8/bosh3/adaptive/implicit Adams solvers。
- **torchsde**（google-research/torchsde）——GPU SDE，reversible Heun。
- **torchcde**（Kidger）——Neural CDEs；**torchode**（Lienen 与 Günnemann，arXiv:2210.12375）——batched/JIT ODE 问题；**TorchDyn**（Poli 等）。
- **Custom CUDA kernels / GPU FFT**用于超高速率字节通道。

**超高速率字节通道的规模、内存与并行。**BLT/H-Net/MBLM 模式——将大部分容量集中于*压缩*序列（L_S ≪ L_0）上运作的 **main network**，保持轻量字节级 encoders/decoders——是超高速率的直接策略：在数据复杂处分配计算（熵 patching），在字节层用 SSMs（线性代价）。选择性 checkpointing（MBLM：单 GPU 至 5M bytes）与 patch-batch packing（BLT）控制内存峰值。对场 solver，split-step Fourier 由 GPU 可并行 O(N log N) FFTs 主导；V_mem SOE 递推保持历史内存 O(N_exp) 而非 O(N)。

---

## Recommendations

收集/操作化技术材料的具体分阶段步骤（尊重作者声明元素不可更改）：

1. **BYTE 通道（主动推理摄入）。**从 Buckley 等（2017）连续时间预测编码表述和/或 pymdp 的纯 F 模式起（无 G/动作分支）。就绪 benchmark：系统在合成字节流上更新信念 q(s) 降低 F，永不发出动作。若字节速率超过迭代推理容量，迁移到摊销推理（recognition 网络 q_φ）和/或 Neural Kalman Filtering。

2. **Byte↔token 桥（[0,1] 学习计算）。**用 hard-concrete 门（Louizos 等）或高斯 stochastic gate（Yamada 等）实例化连续值，α/μ 参数在线梯度学习——这满足"边走边学数字"。对驱动该值的"学到了多少"信号，用贝叶斯惊奇（Itti 与 Baldi——D_KL[posterior‖prior]）或压缩进展（Schmidhuber），知晓 arXiv:2605.14831 的负面结果（一般 MDP 中偏差）。改变决策的阈值：若学习值对所有项饱和于 0 或 1（门坍缩），重新引入温度/拉伸（ζ,γ）或换到低方差高斯 STG。

3. **场方程（作为整体的 solver）。**实现对称 split-step Fourier：傅里叶算子 L̂ = −(ℏ/2m)|k|² − α|k|^σ − iΓ（经 |k|^σ 分数，经 −iΓ 耗散）；Λ|Ψ|² + V_ext 物理步；V_mem 经指数和递推（Jiang–Zhang 等）；η 经 Euler–Maruyama（按噪声性质 Itô 或 Stratonovich）。代码库：从 TorchGPE 起（PyTorch，autograd-capable），扩展分数项、−iΓ、V_mem 与 η。Benchmark：数值复现已知状态（无稳定项的 L² 临界 blow-up；打开 −iΓ 和/或非保守乘性 η 时 blow-up 预防/延迟，按 de Bouard–Debussche）。阈值：若步长 Δt 在 soliton 背景上触发 Weideman–Herbst 不稳定性，减小 Δt 或在刚性部分用指数积分器。

4. **可微性。**用 discretize-then-optimize（经 FFT backprop）加递归 checkpointing，得经 solver 的精确梯度；仅内存为主要瓶颈时保留连续 adjoint（backsolve），知晓其不精确。在小例子上经数值验证（有限差分）验证梯度，注意 PyTorch 的 Wirtinger-共轭约定。

5. **Any-to-any 多模态。**对 TOKEN 通道（I/O），modality-specific tokenizers → 离散 tokens（4M-21）与扩散+自回归混合（Transfusion）材料提供投影与输出模式；多模态路由/MoE 引导模态。保持轻量字节级 encoders/decoders 与压缩表示上的 backbone（BLT/H-Net 模式）。

改变选择的一般 benchmarks/阈值：(i) 熵 patching 若产生退化 patches（全大小 1 或全巨大），重校熵模型或迁移到 H-Net 可微路由器；(ii) BYTE 通道若 F 不收敛，修订精度加权；(iii) 场 solver 即使有耗散项仍数值发散，修订随机解释（Itô vs Stratonovich）与记忆格式。

## Caveats

- **同名不意味等价。**此处所有文献术语——"坍缩"（NLS 中 blow-up；ML 中 representation/dimensional/rank collapse；QM 中波函数坍缩）、"记忆"（V_mem、Raman 响应、Caputo、EWC/SI/MAS、SSM 记忆）、"场"、"原子"、"token"、"学习"——作为可用技术材料呈现，而非作者本意的定义。它们是共享名称的不同概念。
- **保留负面/矛盾结果。**η 噪声对 blow-up 的效应在文献中真正含混：可预防/延迟（非保守乘性）或加速/导致（保守，或超临界中空间光滑）——两者都报告。EWC"持续显示次优性能"。经典方差-virial 律在分数情形*失效*。局域 FNLS 的一般 blow-up 存在定理仍开放。预测编码作 backprop 替代的批判评价（Zahid 等，2023）质疑所称优势。
- **来源质量不一。**核心数学表述来自同行评审论文（Ann. Probab.、CMP、J. Math. Phys.、Comput. Phys. Commun.、NeurIPS、ICLR、《Neural Computation》、《Vision Research》）。一些次要支撑点来自 survey/博客页面（Medium、emergentmind），仅用于语境化，非核心定量事实。
- **2026 日期与预印本。**多项是 2025–2026 预印本（arXiv），尚不一定同行评审（如 arXiv:2605.*、2606.*、2607.*）；作为近期可用材料报告，附预印本状态 caveat。
- **尊重非校准。**无建议"驯化"或线性化方程；Λ|Ψ|² 非线性作为应尊重的元素处理。数值方法用于*求解*声明的方程（所有项一起），而非简化它。
- **TorchGPE。**重用 TorchGPE 作 solver 基础是扩展：作者论文强调 GPU 加速，非端到端梯度训练；可微用法需在实现中验证。
