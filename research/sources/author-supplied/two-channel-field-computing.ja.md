<!-- Translation of: research/sources/author-supplied/two-channel-field-computing.md; source commit: 304d75ed6ff646d311fd9df8b4e2db0d4dee277a -->
# 連続学習橋と場方程式反崩壊系つき二重チャネル（BYTE／TOKEN）「Any-to-Any」アーキテクチャを支える技術研究

## 要約
- 本報告は著者の宣言アーキテクチャの構築を支える技術材料——数学、アルゴリズム、工学——を集め、七正面（A–G）に整理する：BYTE取り込みチャネルの能動推論／自由エネルギー；バイト水準模型と動的パッチ化；any-to-any多様態アーキテクチャ；[0,1]の連続スカラーをオンラインで割り当て学習する方法；反崩壊場方程式（NLS／グロス–ピタエフスキー＋分数ラプラシアン＋非エルミート項＋記憶＋雑音）の完全数学；計算基盤としての連続動力学；微分可能工学。
- 主要素は具体的で新しい文献的根拠をもつ：バイト↔パッチ境界のBLT（Meta、2024年）とH-Net（Hwang、Wang＆Gu、2507.07955）；[0,1]連続スカラーのL0／hard-concrete（Louizosら、2017年）と確率ゲート；収束NLSの崩壊を乗法雑音が防ぎ遅らせうるというde Bouard＆Debusscheの結果；Boulengerらの分数爆発基準。すべて利用可能な技術材料として示され、著者企画の同名語の意味の定義としてではない。
- 全体として扱われる場方程式の数値・微分可能実装について、材料は対称（Strang）分割ステップ・フーリエ（フーリエ空間の|k|^σ乗数による分数ラプラシアン）、指数和近似による記憶項（O(1)履歴漸化式）、オイラー–丸山／ストラトノヴィッチ確率積分、チェックポイント法つきソルバ経由バックプロップによる微分（torch.fft／JAX、diffrax、torchsde、TorchGPE）を指す。

---

## 主要知見

1. **純粋取込モードの能動推論によるBYTEチャネルは文献で持続可能である。**変分自由エネルギー原理（Friston）は、知覚／信念更新のみが起こる定式化（変分自由エネルギーFの最小化）を認め、行為選択（期待自由エネルギーGの最小化）から分離される。Gの方策／行為分岐なしにFのみ最小化する系はまさに「外部出力なき取り込み」に対応する。

2. **型破りのバイト↔トークン／パッチ境界には複数の技術先例がある**——エントロピーパッチ化（BLT）、学習ルーターと微分可能境界つき動的チャンク化（H-Net）、境界予測器、局所符号器と大域変換器のクロスアテンション。そのいずれも固定トークン化ではなく、すべて境界を学ぶ。

3. **「学習」による[0,1]連続数のオンライン割り当て学習**はhard-concrete確率ゲート（Louizosら）、ガウス確率ゲート（Yamadaら）、Gumbel-Softmax／Concrete緩和、オンライン重要度得点（Fisher／EWC、Synaptic Intelligence経路積分、MAS出力勾配）に直接支えられる。「どれほど学んだか」の指標は存在する：情報利得、ベイズ・サプライズ（Itti＆Baldi）、圧縮進展（Schmidhuber）。

4. **全体として扱われる著者の場方程式は、研究された一般化NLS族と数学的に整合する。**各項は相互作用する：収束三次非線形性Λ|Ψ|²はZakharov–Glasseyビリアル恒等式に支配される崩壊（爆発）の原動力である；分数ラプラシアンα(−Δ)^(σ/2)は臨界性と分散を変える（Laskin；Boulengerら）；−iΓ項は散逸／吸収する；V_memは履歴を導入する；η（雑音）はde Bouard＆Debusscheによれば崩壊を防ぎ遅らせうる。否定的・矛盾する結果（保存的雑音は正確率で爆発を加速しうる）はここに保存される。

5. **微分可能工学は実行可能である**：PyTorch／JAXの自動微分FFTは分割ステップ・フーリエを完全微分可能にする；随伴法（Chenら、2018年）とチェックポイント法（Griewank＆Walther）は長いロールアウトの制御された記憶で勾配を許す；TorchGPEはすでにPyTorchで自動微分FFT層の上に分割ステップGPE／NLS伝播子を実装する。

---

## 詳細

### A）能動推論と自由エネルギー（BYTEチャネル、取り込み）

**数学的定式化。**生成模型p(o,s)と認識密度q(s)について、時点tの変分自由エネルギーは
F_t ＝ E_{q(s)}[ ln q(s) − ln p(s, o_t) ] ＝ D_KL[ q(s) ‖ p(s | o_t) ] − ln p(o_t)。
D_KL項≥0なので、F_tはサプライズ−ln p(o_t)（負対数証拠）の上界である。知覚推論はq_t ＝ argmin_q F_tである。これが純粋取込チャネルを支える目的である：系は行為を発することなくF最小化のために信念q(s)を更新する。

能動推論は**期待自由エネルギー**による行為選択を加える（方策π、τ＞t）：
G(π) ＝ Σ_{τ＞t} E_{q(s_τ,o_τ|π)}[ ln q(s_τ|π) − ln p(s_τ, o_τ) ]、
a_t* ＝ argmin_a G(π ∋ a)つき。Gはリスク（期待と選好結果の乖離）＋曖昧さに分解する；等価に認識利得（情報探索）＋実用価値に。**取り込み専用BYTEチャネルではG／行為分岐は省かれる；F（知覚／学習）のみ動く。**学習（母数最適化）と推論（状態最適化）はともにFの最小化である；変分ベイズでは自己無撞着方程式を収束まで反復するか、Fの勾配降下を用いる（座標上昇変分推論／不動点反復はpymdpで用いられる方法である）。

**階層生成模型と予測符号化。**予測符号化（Rao＆Ballard、1999年、『Nature Neuroscience』；Friston、2005年）は系を水準階層に組織し、各水準は下位水準活動の予測を生成する；**精度**（分散の逆、「精度重みづけ」）で重みづけられた予測誤差は階層を上り緩和と学習を駆動する。Buckley、Kim、McGregor＆Seth（2017年）、「The free energy principle for action and perception: A mathematical review」は連続時間・状態の予測符号化と能動推論を導く——バイトチャネルのような連続低水準流の鍵参照である。

**逆伝播の代替としての予測符号化。**Whittington＆Bogacz（2017年、『Neural Computation』）は局所ヘブ可塑性つき予測符号化網が逆伝播を近似することを示した；Millidge、Tschantz＆Buckley（2022年、『Neural Computation』34(6):1329–1368）、「Predictive coding approximates backprop along arbitrary computation graphs」（arXiv:2006.04182）；Song、Lukasiewicz、Xu＆Bogacz（2020年、NeurIPS）、「Can the brain do backpropagation? — exact implementation of backpropagation in predictive coding networks」。保存される*批判的／否定的*結果：Zahid、Guo＆Fountas（2023年）、「Predictive Coding as a Neuromorphic Alternative to Backpropagation: A Critical Evaluation」（『Neural Computation』35(12):1881–1909）は主張される利点を批判的に評価する。Song、Millidge、Salvatoriら（2024年、『Nature Neuroscience』）、「Inferring neural activity before plasticity as a foundation for learning beyond backpropagation」（「prospective configuration」規則）。Millidge、Tang、Osanlouy、Harper＆Bogacz（2024年、『PLOS Computational Biology』20(4):e1011183）、「Predictive coding networks for temporal prediction」——時系列／生信号に関連する。

**深層能動推論、償却推論、VAE、世界模型。**Millidgeらの展望および「The Free Energy Principle for Perception and Action: A Deep Learning Perspective」（arXiv:2207.06415）参照。償却推論（VAEのように認識網q_φを訓練）は能動推論を変分自己符号器と世界模型に結ぶ。Tschantz、Millidge、Seth＆Buckley（2023年、『PLOS Comp. Biol.』）、「Hybrid predictive coding: inferring, fast and slow」（arXiv:2204.02169）——償却（速）と反復（遅）推論を結合する。オンライン信念更新のNeural Kalman Filtering（Millidgeら、arXiv:2102.10021）。

**ライブラリと具体的実装。**
- **pymdp**（Heins、Millidge、Demekas、Klein、Friston、Couzin＆Tschantz、2022年、『JOSS』7(73):4098；arXiv:2201.03904）——Python、離散POMDP、JAXバックエンド、CAVI／不動点反復。リポジトリ：github.com/infer-actively/pymdp；docs：pymdp-rtd.readthedocs.io。
- **RxInfer.jl**（Bagaev、Podusenko＆De Vries、2023年、『JOSS』8(84):5161）——Julia、因子グラフとメッセージ伝達による実時間反応ベイズ推論；GraphPPL.jlフロントエンド。
- **ForneyLab.jl**——メッセージ伝達のForney因子グラフ。
- **ActiveInference.jl**（2024／2025年、PMC11765463）——Juliaのpymdp再実装、標本化と変分法で経験データへのフィッティングを許す。
- **SPM/DEM**（MATLAB）——SPM内部の本来のDynamic Expectation Maximization道具箱。
- **cpp-AIF**（Gregoretti、Pezzulo＆Maisto、2024年、『Neurocomputing』568:127065）——多核C++。
- 最近のハードウェア加速作業：「A Hardware-oriented Approach for Efficient Active Inference」（arXiv:2508.13177、2025年）。

能動推論の連続バイト流を**離散化／実装**するには：一般化座標つき連続時間予測符号化（Buckleyら2017年）または神経カルマンフィルター（Millidgeら）を用いよ；離散時間では行列A（尤度）、B（遷移）、C（選好——取り込みモードで省略）、D（初期状態事前分布）つきpymdpのPOMDP図式を用いよ。

### B）バイト水準模型と代替トークン化

**Byte Latent Transformer（BLT）**——Pagnoni、Pasunuru、Rodriguez、Nguyen、Muller、Li、Zhou、Yu、Weston、Zettlemoyer、Ghosh、Lewis、Holtzman＆Iyer（Meta、2024年）、「Byte Latent Transformer: Patches Scale Better Than Tokens」（arXiv:2412.09871；連絡先：artidoro@cs.washington.edu、2024年12月16日）。直接バイト上で動く；バイトを小さな補助バイト水準言語模型（1億母数変換器、14層、512次元、512バイトスライディング窓）で推定される**次バイトエントロピー**により**可変長パッチ**にまとめる。次バイトの不確定性（エントロピー）が閾値を超えるとパッチ境界が開く——データが複雑な所により多くの計算を割り当てる。構成：軽量**局所符号器**（バイト→パッチ）、パッチ上の大**潜在／大域変換器**、**局所復号器**（パッチ→バイト）。「80億母数・4兆訓練バイトまでのバイト水準模型の最初のFLOP統制規模化研究」であり、BLTは規模でトークン化模型（Llama 3）に並ぶ。公開重み：facebook/blt-1b、facebook/blt-entropy（github.com/facebookresearch/blt）。2026年拡張：「Fast Byte Latent Transformer」（arXiv:2605.08044）——Nバイト→M≈N/4パッチ。

**H-Net（動的チャンク化）**——Hwang、Wang＆Gu（2025年）、「Dynamic Chunking for End-to-End Hierarchical Sequence Modeling」（arXiv:2507.07955）。完全端々微分可能な**動的チャンク化**機構：**ルーター部**が適応的位置別境界確率を予測し、圧縮表現に区分する；**平滑部**が再構成で補間し微分可能性を保つ；**残差接続**が符号器の初期出力を直接脱チャンク段階に投射し、局所バイト特徴を大域文脈に結ぶ。SSM符号器／復号器は変換器層に勝る。流れ：バイト→符号器→ルーター→チャンク化→主網→脱チャンク化→復号器。著者らによれば「計算とデータを合わせると、バイト水準で動く一段H-NetはBPEトークン上の強い変換器に勝る…自らの倍の大きさのトークン変換器に並ぶ」。DNAでは「各H-Net模型は対応する等方模型と同じ減衰前困惑度におよそ3.6倍少ないデータで達する」（≈3.6倍少ないデータ／等方基準に対する4倍近いデータ効率改善）。2025／2026年変種：**H-Net++**（Zakershahrak＆共著、arXiv:2508.05628）、形態豊かな言語（ペルシア語）用——190万母数文脈混合器、二層超事前分布、GPT-2-faに対する0.159 BPB低下（12%良い圧縮）；「Adaptive Targeted Dynamic Chunking」（arXiv:2605.30080）；「ByteGen」（arXiv:2508.02247、金融データ）；「Distilling Token-Trained Models into Byte-Level Models」（arXiv:2602.01007）。

**他のバイト／トークナイザなし。**
- **MegaByte**（Yuら、2023年）——二復号器変換器階層（*固定*長パッチ上の大域＋バイト上の局所自己回帰）；文脈最大120万バイト。
- **MambaByte**（Wang、Gangavarapu、Yan＆Rush、2024年、COLM）、「Token-free Selective State Space Model」（arXiv:2401.13660）——バイト水準のMamba（SSM）、線形時間；統制FLOPでMegaByteに勝る。著者らによれば「トークン化起草とバイト水準検証つき投機的復号適応…標準MambaByte実装に対する2.6倍の推論高速化をもたらす」（「標準MambaByte実装に対する2.6倍の推論高速化をもたらす」）。
- **SpaceByte**（Slagle、2024年、NeurIPS；arXiv:2404.14408）——バイトを語境界に整列したパッチに分ける；著者によれば「PG-19でSpaceByteはbits-per-byte 1.009に達する…MegaByteの1.083とバイト水準変換器の1.138より著しく良い」（バイト水準とMegaByteは同等性能にサブワードの〜10倍の訓練FLOPを要する）。コード：github.com/kjslag/spacebyte。
- **MBLM**（arXiv:2502.14553、2025年）——Multiscale Byte Language Models、無限段階と段階別復号器の階層、選択的チェックポイント法で単一GPUに最大500万バイト。
- **ByT5**（Xueら、2022年、『TACL』10:291–306）、**CANINE**（Clarkら、2022年）—— ダウンサンプリングつきバイト／文字符号器。
- **bGPT／「Byte Models are Digital World Simulators」**（Wuら、2024年）—— デジタル世界模擬としてのバイト模型化。
- **Perceiver／Perceiver IO／Perceiver AR**——潜在配列から超高次元入力へのクロスアテンション、学習潜在ボトルネックで粒度を橋渡し。
- 厳選目録：github.com/zjysteven/Awesome-Byte-LLM。

**粒度架橋（バイト↔パッチ）。**用いられる具体機構：局所符号器（バイト）と大域変換器（パッチ）のクロスアテンション；学習プーリング；**境界予測器**（BLTはエントロピー経由；H-Netは境界確率つきルーター経由）；解像度回復の微分可能補間／平滑（H-Net）。水準間界面としてのソフトトークン／連続埋め込みの作業はBLTのパッチ潜在表現を含む（軽量学習符号器／復号器で潜在表現に対応づけられた任意バイト群、固定語彙なし）。

### C）多様態ANY-TO-ANYアーキテクチャ

概観（参照展望：「Unified Multimodal Understanding and Generation Models: Advances, Challenges, and Opportunities」、arXiv:2505.02567、2023–2025年表つき；目録：github.com/aidc-ai/awesome-unified-multimodal-modelsおよびgithub.com/any2any-mllm/awesome-any2any）。

**戦略族：**
- **様態別トークナイザつき自己回帰→離散トークン：****4M**と**4M-21**（Mizrahi／Karら、EPFL／Apple；arXiv:2406.09406）——様態別トークナイザ経由で数十様態を離散トークンに対応づける（画像様態のViT-based VQ-VAE；3D姿勢／埋め込みのMLP-based離散VAE）、多様態マスク目的、最大30億母数・21様態（RGB、輪郭、SAM、4DHumans姿勢、色パレット、メタデータ、DINOv2／ImageBind特徴、T5-XXL埋め込み）；公開コードは4m.epfl.ch。**Chameleon**（Meta、2024年、arXiv:2405.09818）——VQ-IMGつき初期融合混合様態、因果的。**Emu3**（BAAI、2024年、arXiv:2409.18869）——「Next-Token Prediction is All You Need」、SBER-MoVQGAN。**AnyGPT**（2024年）——音声のEnCodec、発話のSpeechTokenizer、様態別接頭辞。**Unified-IO 2**（Luら、2024年）——視覚／音声／言語つき構造化符号器–復号器。
- **AR＋拡散ヘッド／拡散–自己回帰混合：****Transfusion**（Zhou、Yu、Babuら、Meta、2024年、arXiv:2408.11039）——同じ多様態変換器で次トークンを予測し**かつ**画像を拡散する。**Show-o**（Xieら、2024年、arXiv:2408.12528）——離散拡散スケジュールを統合する。**Bagel／BAGEL**と**Hyper-Bagel**（arXiv:2509.18824、2025年）——統一加速枠組み。
- **視覚符号化解きほぐし：****Janus／Janus-Pro**（DeepSeek、Wuら、2025年、CVPR）——理解対生成の視覚符号化を分ける。
- **共有潜在空間／様態間整列：****CoDi**と**CoDi-2**（Tangら、2023年）——入力の任意組合せから様態の任意組合せを並列生成する合成可能拡散。**NExT-GPT**（Wuら、2023年、arXiv:2309.05519；ICML 2024年）——LLM（Vicuna-7B）＋ImageBind（6様態統一符号器）＋アダプター＋拡散復号器；母数の〜1%のみ調整——「NExT-GPTは特定投射層の少量の母数（1%）のみ調整される」（〜123億の〜1億6400万、≈1.3%）——MosIT指示調整（〜5000の厳選対話）つき。保存される*否定的／限界*結果：CoDi著者らは「深い人様の推論に達しない」と記す；NExT-GPTは依然凍結済み訓練符号器／復号器に依存する。
- **最近2025／2026年：**M2-omni（arXiv、複数トークナイザ／復号器）、Emu3.5（「Native Multimodal Models are World Learners」、2025-10）、Uni-X（ICLR 2025年、様態衝突の「two-end-separated」）、OneCAT、MMaDA、Show-o2（arXiv:2506.15564）、FUDOKI（離散フロー、arXiv:2505.20147）。

**鍵戦略**は著者企画に関連する：(i)共有バックボーン上の普遍トークナイザ対様態別投射；(ii)様態間ルーティングと多様態混合専門家；(iii)拡散混合（連続出力用）と自己回帰（離散出力用）。尊重される文体注：「VQ-VAEの崩壊」（「dimensional collapse in VQVAEs」、NeurIPS）は同名現象であり、参照としてのみ示される。

### D）オンライン学習される連続[0,1]学習値

この節は著者のLEARNING COMPUTATIONの材料を集める——各学習に連続（明示的に非二値）の[0,1]数を割り当て、その数をオンラインで学習すること。以下の方法は文献材料である；ここの「学習」という名は著者の概念との等価を前提しない。

**連続ゲーティングと連続緩和。**
- **L0正則化／hard-concreteゲート**——Louizos、Welling＆Kingma（2017年）、「Learning Sparse Neural Networks through L0 Regularization」（arXiv:1712.01312）。非負確率ゲートがどの重みをゼロにするか定める；**hard-concrete**分布は二値concreteを「伸ばし」hard-sigmoidを通して得られ、ちょうど{0,1}に質量を割り当て、残りを(0,1)に割り当てる。具体公式：
  s_i ＝ σ( (log u − log(1−u) ＋ α_i)/τ )、 u ～ Uniform(0,1)
  s̄_i ＝ s_i(ζ − γ) ＋ γ、 典型γ ＝ −0.1、ζ ＝ 1.1、[0,1]のhard-sigmoid clamp つき。
  α母数（と温度β／τ）は網とともに勾配で訓練される——まさに「連続値のオンライン学習」である。ゲートの期待値はσ(log α − β' log(−γ/ζ))である。
- **Concrete／Gumbel-Softmax**——Maddison、Mnih＆Teh（2016年、arXiv:1611.00712）とJang、Gu＆Poole（2016年）——離散変数の連続緩和、上記ゲートの基礎。
- **ガウス確率ゲート（STG）**——Yamada、Lindenbaum、Negahban＆Kluger（2020年）、「Feature Selection using Stochastic Gates」（arXiv:1810.04247）：z_d ＝ max(0, min(1, μ_d ＋ ε_d))、ε_d ～ N(0, σ²)、学習μ_dつき——hard-concreteより低分散の[0,1]ガウス clamp 。文脈／条件拡張：arXiv:2312.14254。
- **GRU／LSTMゲートと注意重み**はsigmoid／softmax経由の(0,1)連続重みとして学習連続ゲーティングの古典先例である。

**重要度／確信度のオンライン推定。**
- **Elastic Weight Consolidation（EWC）**——Kirkpatrickら（2017年、『PNAS』；arXiv:1612.00796）。重要度Ω_i ＝ **Fisher情報行列**の対角（局所損失曲率／KLのヘッシアン）。二次罰則Σ_i (F_i/2)(θ_i − θ_i*)²。保存される*否定的／批判的*結果：EWCは「一貫して準最適性能を示す」；FIM依存は特定状況で勾配消失と不正確推定を起こす（arXiv:2603.18596、「Elastic Weight Consolidation Done Right」）。
- **Synaptic Intelligence（SI）**——Zenke、Poole＆Ganguli（2017年、ICML）。最適化軌道に沿って蓄積される一次**経路積分**測度（損失低下への各シナプスの寄与）——作りとしてオンライン推定子。
- **Memory Aware Synapses（MAS）**——Aljundiら（2018年）。重要度＝重みに関する網出力勾配の大きさ（出力二乗L2ノルム）、教師なしオンライン計算可能。
- **重みのベイズオンライン学習／カルマンフィルタリング**——重み上の事後の漸進ベイズ更新；重み／状態の「Neural Kalman Filtering」（Millidgeら、arXiv:2102.10021）。

**率のメタ学習とクレジット割当。**
- **Hypergradient descent**（Baydinら、2018年）——率自体に関する損失勾配で学習率を学ぶ。
- **学習最適化子**と**適応母数別段階幅**——母数別段階のメタ学習。
- **Learning to reweight examples**（Renら、2018年）と**Meta-Weight-Net**（Shuら、2019年）——例／標本ごとに連続重みを学ぶ；**focal weighting**（Linら、2017年）——難しさごとの連続重み。これらはまさに学習される「カリキュラム／標本重みづけ」であり、項目ごとに連続スカラーを割り当てる。

**「どれほど学んだか」の指標。**
- **Prediction gain／information gain**——項目に帰する損失／不確定性の低下。
- **ベイズ・サプライズ**——Itti＆Baldi（2009年、『Vision Research』49(10):1295–1306、DOI:10.1016/j.visres.2008.09.007、PMCID PMC2782645）：「サプライズは世界についての事後と事前信念の差の点でデータが観察者にどう影響するか測る」——形式的にデータ観測後のD_KL[事後‖事前]である。「人注意の既知最強の誘引」であり、視線移動の72%が平均より驚くべき場所に向けられる（動画では84%）。[0,1]連続値を駆動する信号として直接使える。
- **圧縮進展／学習進展**——Schmidhuber（2009年）、「Driven by Compression Progress…」（arXiv:0812.4360）と「Formal Theory of Creativity, Fun, and Intrinsic Motivation (1990–2010)」（『IEEE TAMD』2010年）：内発的強化学習は主観圧縮可能性の時間*一次導関数*である——圧縮度自体ではなく（雑音の報酬を避ける）。好奇心の潜在ベイズ・サプライズ：Mazzagliaら（2021年、AAAI）。保存される*否定的*注：「Interestingness as an Inductive Heuristic for Future Compression Progress」（arXiv:2605.14831）は一般MDPでは文脈内予測誤差由来の報酬で学習進展を不偏推定することは不可能と証明する；肯定結果は非時間部分類（能動学習／ベイズ実験計画）のみである。

### E）著者場方程式の数学（全項一体）

宣言方程式：
i·ℏ·∂_t Ψ ＝ [ −ℏ²/(2m)∇² ＋ V_ext ＋ Λ|Ψ|² ＋ V_mem ＋ α(−Δ)^(σ/2) − iΓ ]Ψ ＋ η

項はここでは相互作用を示す結合系として示され——孤立片としてではない。

**NLS／グロス–ピタエフスキー核心（運動＋Λ|Ψ|²）。**他項なしでは収束NLS（収束／引力規約でΛ＜0）、i∂_tΨ ＝ −½∇²Ψ ＋ Λ|Ψ|²Ψであり、その場合はV_extトラップあるときのグロス–ピタエフスキーである。保存不変量（−iΓ、η、V_memの欠如で）：質量／ノルムM ＝ ∫|Ψ|²、エネルギー／ハミルトニアンE ＝ ∫[½|∇Ψ|² ＋ (Λ/2)|Ψ|⁴]、運動量。**崩壊／爆発：****ビリアル恒等式**（分散）V(t) ＝ ∫|x|²|Ψ|²dxに支配され、その二階時間導関数はd²V/dt² ＝ 8E（臨界非線形性）を満たし、E＜0は有限時間のV(t)→0を強いる→爆発（Vlasov–Petrishchev–Talanovと**Zakharov–Glassey**基準）。三次非線形性の**臨界次元**はd＝2（L²臨界：指数1＋4/d）；d＜2劣臨界（大域存在）、d＞2超臨界。L²臨界の場合に爆発率のMerle–Raphaël対数–対数則がある。参照：Colliander／Merle–Raphaëlノート（math.utoronto.ca）；「Enhancement of the Zakharov-Glassey's method for Blow-Up in NLS」（arXiv:2203.08522）；Merle、「Blow-up Results of Virial Type for Zakharov Equations」（『CMP』175(2)）。

**分数ラプラシアンα(−Δ)^(σ/2)（分数シュレーディンガー／レヴィ動力学）。**フーリエ乗数による定義：(−Δ)^s u ＝ F^{-1}[ |ξ|^{2s} F(u) ]——コードではフーリエ空間で|k|^σを掛ける（著者規約でσ ＝ 2s）。**Laskin**（2000年、『Phys. Lett. A』268:298–305；2002年、『Phys. Rev. E』66:056108）がファインマン経路積分をブラウンからレヴィ軌道へ拡張して導入した。崩壊効果：収束分数NLS i∂_t u ＝ (−Δ)^s u − |u|^{2p}uには**Boulenger、Himmelsbach＆Lenzmann**の一般爆発基準がp ≥ 2s/N（動径、N≥2）で成り立つ；L²臨界場合はp ＝ 2s/Nである。小さいs（より「分数的」）は分散を下げ崩壊閾値を変える。冪組合せつき分数↔三次相互作用：Feng（2018年、arXiv:1804.00973および『CPAA』）、「On the blow-up solutions for the fractional NLS with combined power-type nonlinearities」、0＜p₁＜p₂＜2s/(N−2s)、鋭い質量閾値つき。保存される*未解決*結果：局所FNLSの一般爆発存在定理は未解決問題のままであり、数値証拠に支えられる（arXiv:1804.00973に引用）。s＝1/2のときのボソン星／半相対論模型としてのFNLS。

**散逸／吸収項−iΓ（非エルミート）。**ハミルトニアンを非エルミートにする；複素ポテンシャルは利得／損失を模型化する。**PT対称性**：PT対称ハミルトニアンは非エルミートにもかかわらず実スペクトルをもちうる；光子学では複素ポテンシャル＝局在増幅／吸収つき媒体である。**リンドブラッドマスター方程式**との関係：開放系リンドブラッド動力学から有効非エルミート・ハミルトニアンが現れる（単粒子損失としての−iΓ項、ρ_{11}(t)＝ρ_{11}(0)e^{−2γt}）。**複素吸収ポテンシャル（CAP）**は境界で波動関数を吸収するのに用いられる。爆発防止との関係：散逸／吸収（Γ＞0）はノルムとエネルギーを流し、爆発を防ぎうる。参照：El-Ganainyら（2018年）、「Non-Hermitian physics and PT symmetry」（『Nat. Phys.』14:11）；「Density Matrix Formalism for PT-Symmetric Non-Hermitian Hamiltonians with the Lindblad Equation」（arXiv:2006.02445）；「Dissipative Dynamics and Active Stabilization of Linear and Nonlinear Waves in Non-PT-Symmetric Harmonic Traps」（arXiv:2605.12638、2026年）、虚数ポテンシャルによる非線形波の能動安定化を明示的に扱う。減衰分数NLSには：「Global existence for the nonlinear fractional Schrödinger equation with fractional dissipation」（arXiv:1704.05307）——任意の減衰項a＞0の大域存在。

**確率強制η（確率NLS）。****de Bouard＆Debussche**文献は中心的であり、ここに保存される肯定と矛盾の両結果を含む：
- 乗法雑音（時間に白色、空間に相関）は爆発を*遅らせる*効果をもつ；白色雑音は爆発を*防ぎ*さえしうる（de Bouard、Debussche＆Di Menza、2001年、『Journées EDP』の観察）。
- しかしde Bouard＆Debussche（2005年、『Ann. Probab.』33(3):1078–1110）、「Blow-up for the stochastic NLS with multiplicative noise」：超臨界の場合、空間に滑らかな雑音は任意の滑らかな初期データに正確率で即時爆発を*起こし*うる。
- L²超臨界の場合の*保存的*（ストラトノヴィッチ）雑音は正確率で爆発を*加速する*；大きな*非保存的*（ガウス乗法）雑音は高確率で任意有界区間の爆発を*防ぎ*うる（Barbu、Röckner＆Zhang；arXiv:2210.17010および『Nonlinear Analysis』136:102–116、2016年参照）。加法的効果：de Bouard＆Debussche（2002年、『Probab. Theory Relat. Fields』123:76–96）。
- 基礎：de Bouard＆Debussche（1999年、『CMP』205:161；2003年、『Stoch. Anal. Appl.』21:97）——確率ストリッカーツ評価によるL²とH¹の適切性。確率分数場合：「Stochastic Perturbations in the Fractional NLS: Well-posedness and Blow-up」（arXiv:2308.10270）——古典分散–ビリアル則は分数状況で*破れる*ことに注意し、伊藤公式による確率一般化を要する。エネルギー臨界場合：arXiv:2604.14852（2026年）。「確率シュレーディンガー方程式」／量子状態拡散（Fagnola＆Mora、2013年）はηを量子状態拡散に結ぶ。

**記憶項V_mem（履歴依存ポテンシャル）。**履歴依存実装の文献形：
- **非瞬時応答（光学のラマン型）：**R(t) ＝ (1−f_R)δ(t) ＋ f_R h_R(t)つきGNLSE、δ項は瞬時カー、h_R畳み込みは記憶である。Blow–Wood核：h_R(t) ＝ Θ(t)·(τ₁²＋τ₂²)/(τ₁τ₂²)·e^{−t/τ₂}·sin(t/τ₁)、石英のf_R＝0.18、τ₁＝12.2 fs、τ₂＝32 fsつき（Blow＆Wood、1989年、『IEEE JQE』25(12):2665；Lin＆Agrawal、2006年、『Opt. Lett.』31(21):3086；Agrawal、『Nonlinear Fiber Optics』第6版）。
- **畳み込み核つき積分微分方程式：**i∂_tΨ ＝ H₀Ψ ＋ ∫₀^t K(t−t′)Ψ(t′)dt′。非定常核：「Exact treatment of the memory kernel under time-dependent system-environment coupling」（arXiv:2505.00386）。ラプラス／グリーン経由のシュレーディンガー時間非局所ポテンシャル（arXiv:2502.18700）。
- **時間分数導関数（時間分数シュレーディンガー）：**Naber（2004年、『J. Math. Phys.』45(8):3339；arXiv:math-ph/0410028）——∂_tをα階カプト導関数に置き換える；ハミルトニアンは非エルミート・時間非局所になる；ミッターク–レフラー関数の解；*確率は保存されない*（保存される結果）。カプト導関数：₀^C D_t^α f ＝ 1/Γ(1−α) ∫₀^t f′(τ)(t−τ)^{−α} dτ（α∈(0,1)）。
- **データ駆動核発見**（V_memが学習される場合）：「Neural Discovery of Memory and Nonlocal Kernels in Integro-Differential Equations with Constrained KANs」（arXiv:2607.11110）；MINPO（arXiv:2512.17273）。

**全項の相互作用（一体の反崩壊）。**材料は、崩壊対大域存在の振る舞いが*共同競争*から現れることを示唆する：収束Λ|Ψ|²は爆発へ押す；運動と分数α(−Δ)^(σ/2)は分散する（指数σが臨界閾値を調整）；V_ext（トラップ）は閉じ込めうる；−iΓはノルム／エネルギーを流す（爆発を防ぐ散逸）；ηは非保存対保存乗法かに応じて爆発を防ぎ遅らせうるし加速もしうる；V_memは遅延応答が瞬時動態を変える履歴項を加える。文献の*既知*反崩壊機構は並行材料として示される（著者機構の置換としてではなく）：非線形性飽和（例：三次–五次CQNLS——Nature『Sci. Rep.』7285、非ゼロ背景が崩壊を中断し分散衝撃波を生成）、散逸／吸収、非エルミート項、安定化雑音、トラップ、非局所相互作用（arXiv:1008.1891、「Collapse in the nonlocal NLS」）。

**完全方程式の実用数値法。**
- **分割ステップ・フーリエ／擬スペクトル（Strang、対称）。**∂_tΨ ＝ (L＋N)Ψと書け、L ＝ 線形部（運動＋分数＋散逸、フーリエ対角）、N ＝ 非線形部（Λ|Ψ|² ＋ V_ext ＋ V_mem、物理空間対角）。対称O(Δt²)段階：(i)フーリエの線形半段階Ψ̂ ← e^{iL̂Δt/2}Ψ̂；(ii)物理空間の全非線形段階Ψ ← e^{iN(|Ψ|²)Δt}Ψ；(iii)線形半段階。**分数ラプラシアンはフーリエ線形作用素の|k|^σ乗数として入る**：L̂ ＝ −(ℏ/2m)|k|² − α|k|^σ − iΓ。分数NLSには：Kleinら、時間分割スペクトル（arXiv:1908.05719、調和ポテンシャル）；「A split-step Fourier pseudo-spectral method for space-fractional coupled NLS」（『Commun. Nonlinear Sci. Numer. Simul.』、ScienceDirect S1007570423000680）；「A split-step finite element method for the space-fractional Schrödinger equation in 2D」（PMC11484848）。
- **安定性と時間段階：**ソリトン背景上の分割ステップ数値不安定性（Weideman–Herbst）は段階への注意を要する；arXiv:1008.4974と平面波安定性分析（arXiv:1306.0656）参照。対称方式は誤差をO(Δt²)に改善する。
- **数値の記憶項：**畳み込み積分の**L1方式**離散化（カプト、2−α階）：∂̄_n^α φ ＝ Σ_{j=1}^n b_{n−j}∂̄_jφ、b_j ＝ Δt^{1−α}/Γ(2−α)·[(j+1)^{1−α}−j^{1−α}]つき——時間費用O(N²)、記憶O(N)。Jiang、Zhang、Zhang＆Zhang（2017年、『Commun. Comput. Phys.』21(3):650–678；arXiv:1511.03453）の**指数和（SOE）近似**：t^{−1−α}核をΣ_ℓ w_ℓ e^{−s_ℓ t}で近似し、畳み込みを*漸化式*にする（各モードy_ℓ^n ＝ e^{−s_ℓΔt}y_ℓ^{n−1} ＋ 局所求積）、O(N·N_exp)作業とO(N_exp)記憶に減らす——完全微分可能（exp／乗／和のみ）。高次方式：L1-2、AlikhanovのL2-1σ（3−α階）；空間4次コンパクト（DOI 10.1186/s13662-020-02946-w）。
- **確率積分子（η用）：**オイラー–丸山（一般雑音の強1/2階）、SPDEの高次方式のMilstein；伊藤対ストラトノヴィッチ解釈が重要である（保存的雑音はストラトノヴィッチ）。de Bouard、Debussche＆Di Menzaは確率NLSの収束証明つき数値方式を与える。
- **クランク–ニコルソンと緩和方式：**Besseの緩和方式はNLSの不変量を保存する；リース分数NLSの保存的CN-FDM。
- **指数積分子**は硬い線形部用。
- **共同扱い：**分割ですべての項を単一積分子に：{運動、分数、−iΓ}をフーリエ作用素にまとめ（正確な指数）、{Λ|Ψ|²、V_ext}を物理段階に、V_memを毎段階更新のSOE漸化式で、ηを物理段階のオイラー–丸山で注入する。
- **ライブラリ／コード：****GPELab**（Antoine＆Duboscq、2014／2015年、『Comput. Phys. Commun.』185:2969および193:95；gpelab.math.cnrs.fr）——MATLAB、擬スペクトル／緩和／クランク–ニコルソン、局所・非局所非線形性つき1D／2D／3D GPE、多成分、確率動力学。**XMDS2**（Dennis、Hope＆Johnsson、2013年、『Comput. Phys. Commun.』184:201；arXiv:1204.4255；xmds.org）——確率SPDEのXML→C++コード生成器、スペクトル法、適応RK、MPI。**TorchGPE**（Fioroniら、2024年、『SciPost Phys. Codebases』38；arXiv:2404.14401；github.com/qo-eth/TorchGPE）——PyTorchの対称分割ステップGPE／NLSソルバ、GPU、任意時間依存／自己無撞着ポテンシャル；PyTorchの自動微分FFT層の上に構築。**GPUE**（Schloss＆O'Riordan、2018年、『JOSS』3(32):1037）、**spinor-GPE**（PyTorch）、**BEC2HPC**。

### F）AI模型基盤としての場方程式と連続動力学

**神経ODE／SDE／連続時間RNN。**
- **神経ODE**——Chen、Rubanova、Bettencourt＆Duvenaud（2018年、NeurIPS；arXiv:1806.07366）：dz/dt ＝ f(z,t,θ)、O(1)記憶の随伴法による逆伝播。
- **神経SDE**——Li、Wong、Chen＆Duvenaud（2020年、AISTATS；arXiv:2001.01328）、「Scalable Gradients for SDEs」——torchsdeの基礎。
- **連続時間RNN（CTRNN）**——Funahashi＆Nakamura（1993年）。
- **液体時定数網（LTC）**——Hasaniら（2021年）：dx/dt ＝ −[1/τ ＋ f(x,u,t)]x ＋ f(x,u,t)A、入力依存時定数；**CfC**（閉形連続時間、Hasaniら2022年）は解析解を与える（〜20倍高速化）；**Liquid-S4**はLTCをSSMと統合する。LFM2（arXiv:2511.23404）は最近の応用である。

**状態空間模型（SSM）と連続時間定式化。**S4（Gu、Goel＆Ré、2021年）、S5、**Mamba／Mamba-2**（Gu＆Dao、2023／2024年）：構造化線形漸化式；連続時間はゼロ次ホールド（ZOH）で離散化され、一次でオイラーと等価である（arXiv、「Mamba neural operator」；「Demystifying the Token Dynamics of Deep Selective State Space Models」、arXiv:2410.03292）。基盤として関連するのは、連続動力学↔系列を結び、H-Netの符号器／復号器がSSMを使うからである。

**PINNと作用素学習。**物理ベース網（PINN）と作用素学習：**フーリエ神経作用素（FNO）**（Liら、2020年）と**DeepONet**（Luら、2021年）は関数空間間の作用素を学ぶ——場／PDE作用素を学ぶ道である。「Mamba neural operator」（ScienceDirect S0021999125008496）はSSMをPDE族の神経作用素に一般化する。

**網核心としてのハミルトン／量子動力学。****ハミルトン神経網**——Greydanus、Dzamba＆Yosinski（2019年、NeurIPS；arXiv:1906.01563）：損失L ＝ ½[(∂H/∂p − dq/dt)² ＋ (∂H/∂q ＋ dp/dt)²]でH(q,p)を学び、エネルギーを保存し時間可逆である（コード：github.com/greydanus/hamiltonian-nn）。関連：ラグランジュ神経網（Cranmerら、2020年、arXiv:2003.04630）、シンプレクティックRNN（Chenら、2020年、arXiv:1909.13334）、ハミルトン生成網（Tothら、2020年、arXiv:1909.13789）。HNNは神経ODEの部分類である（学習Hがシンプレクティックソルバで積分されるベクトル場を定める）。ユニタリ発展RNN（Arjovsky、Shah＆Bengio、2016年、ICML；arXiv:1511.06464）——位相を保存し消失／爆発勾配を避けるユニタリ動力学。

**複素・波ベース表現。**
- **深層複素網**——Trabelsi、Bilaniuk、Zhang、Serdyuk、Subramanian、Santos、Mehri、Rostamzadeh、Bengio＆Pal（2018年、ICLR；arXiv:1705.09792）：複素畳み込み、複素バッチ正規化（2×2実／虚共分散行列による白色化）、レイリー初期化、複素活性化（modReLU、CReLU）。コード：github.com/ChihebTrabelsi/deep_complex_networks。
- **複素逆伝播／ウィルティンガー解析**——作用素∂/∂z ＝ ½(∂/∂x − i∂/∂y)、∂/∂z* ＝ ½(∂/∂x ＋ i∂/∂y)。実損失Lには降下方向は*共役*導関数∂L/∂z*を用いる（PyTorchの複素自動微分の採用規約）。非正則連鎖律：∂L/∂z* ＝ (∂L/∂w)(∂w/∂z*) ＋ (∂L/∂w*)(∂w*/∂z*)。参照：Brandwood（1983年、『IEE Proc. F』130(1):11）、Kreutz-Delgado（arXiv:0906.4835）、展望arXiv:2101.12249、Hirose（2012年、Springer）。
- **情報担体としての位相：**Reichert＆Serre（2014年、ICLR；arXiv:1312.6115）、「Neuronal Synchrony in Complex-Valued Deep Networks」。
- **ホログラフィック縮約表現（HRR）**——Plate（1995年）——循環畳み込みによる結合。**ベクトル記号アーキテクチャ／超次元計算**（Kanerva）——高次元ベクトルの結合／束化；分散表現と位相への連結。

**表現崩壊（並行技術参照——著者機構を置換しない）。**MLの同名「崩壊」現象：**表現崩壊**（特徴が単一値に崩壊、分散→0）、**次元崩壊**（表現が全空間を使わない；共分散特異値で測定）、**情報崩壊**（相関特徴）、変換器の**ランク崩壊**。既知の反崩壊機構：**VICReg**（Bardes、Ponce＆LeCun、2022年）——分散項（標準偏差≥γのヒンジ）、不変性と共分散（非対角最小化）；**Barlow Twins**（Zbontarら、2021年）——相互相関行列を単位行列に強いる（「軟白色化」）；**白色化**（Ermolovら、2021年）；**スペクトル／直交**重み正則化（WERank、arXiv:2402.09586）。文体注：並行材料として示される；ここの「崩壊」という名は著者方程式が戦う「崩壊」との等価を前提しない。

### G）工学と実装

**微分可能パイプライン内部のPDE／場ソルバ結合。**
- **随伴法（連続／先最適化後離散化）：**随伴ODE a(t)＝∂L/∂z(t)、da/dt ＝ −a(t)ᵀ∂f/∂z（逆積分）、dL/dθ ＝ −∫ a(t)ᵀ∂f/∂θ dtを導く；O(1)記憶だが*近似*勾配（逆再構成は誤差を蓄積する）。Diffraxの`BacksolveAdjoint`であり、不正確さで「非推奨」と名づけられる。理論的根：Pontryaginら（1961年）。
- **ソルバ経由バックプロップ（先離散化後最適化）：**ソルバの実際の離散操作を微分する→*正確*勾配、大きな記憶、**チェックポイント法**で緩和される（Griewank＆Walther、「Algorithm 799: revolve」、『ACM TOMS』2000年；ANODE、Gholami、Keutzer＆Biros、IJCAI 2019年、arXiv:1902.10298；Adaptive Checkpoint Adjoint、Zhuangら、ICML 2020年；Symplectic Adjoint、Matsubara、Miyatake＆Yaguchi、NeurIPS 2021年、arXiv:2102.09750）。`RecursiveCheckpointAdjoint`（Diffraxの既定）である。分割ステップ・フーリエには先離散化後最適化が推奨される（正確勾配）とチェックポイント法——FFTはVJPが別の（共役）FFTであるユニタリ線形作用素であり、勾配は`fft`／`ifft`＋点別乗算をすっきり流れる。McCallumら（arXiv:2410.11648、「Efficient, Accurate and Stable Gradients for Neural ODEs」）とKidger（DPhil学位論文、Oxford、2021年、「On Neural Differential Equations」）も参照。

**枠組み。**
- **PyTorch `torch.fft`**（1.8以来）：自動微分＋GPU（cuFFT）。*但し書き*：複素自動微分はウィルティンガー共役規約を用いる（格納 grad は∂L/∂z*）；`.backward()`前に実スカラーに縮約せよ（さもなくばRuntimeError）。
- **JAX**（`jax.numpy.fft`、`jax.lax`）：微分可能、XLA GPU／TPU；`grad`／`vjp`と合成する。
- **diffrax**（Kidger、JAX；github.com/patrick-kidger/diffrax、docs.kidger.site/diffrax）——ODE／SDE／CDE、複数随伴（`RecursiveCheckpointAdjoint`、`BacksolveAdjoint`、`ImplicitAdjoint`）；Equinox上に構築、Python 3.10+。
- **torchdiffeq**（github.com/rtqichen/torchdiffeq）——`odeint`／`odeint_adjoint`（随伴は`func`を`nn.Module`として要する）；dopri5／dopri8／bosh3／適応／陰的Adamsソルバ。
- **torchsde**（google-research/torchsde）——GPU SDE、可逆Heun。
- **torchcde**（Kidger）——神経CDE；**torchode**（Lienen＆Günnemann、arXiv:2210.12375）——バッチ／JIT ODE問題；**TorchDyn**（Poliら）。
- 超高率バイトチャネルの**カスタムCUDAカーネル／GPU FFT**。

**超高率バイトチャネルの規模、記憶、並列性。**BLT／H-Net／MBLM図式——*圧縮*系列（L_S ≪ L_0）上で動く**主網**に容量のほとんどを集中し、軽量バイト水準符号器／復号器を保つ——は超高率の直接戦略である：データが複雑な所に計算を割り当て（エントロピーパッチ化）、バイト水準にSSM（線形費用）を用いる。選択的チェックポイント法（MBLM：単一GPUに最大500万バイト）とパッチバッチパッキング（BLT）は記憶頂を制御する。場ソルバには分割ステップ・フーリエはGPU並列化可能なO(N log N) FFTに支配される；V_mem SOE漸化式は履歴記憶をO(N)でなくO(N_exp)に保つ。

---

## 推奨

技術材料を集め運用する具体的段階的手順（著者の宣言要素が変えられないことの尊重つき）：

1. **BYTEチャネル（能動推論による取り込み）。**Buckleyら（2017年）の連続時間予測符号化定式化および／またはF専用モードのpymdp（G／行為分岐なし）から始めよ。準備ベンチマーク：系は行為を発することなく合成バイト流の上でFを下げて信念q(s)を更新する。バイト率が反復推論能力を超えるなら、償却推論（認識網q_φ）および／または神経カルマンフィルタリングに移れ。

2. **バイト↔トークン橋（[0,1]の学習計算）。**hard-concreteゲート（Louizosら）またはガウス確率ゲート（Yamadaら）ごとに連続値を例示し、勾配でオンライン学習されるα／μ母数つき——これは「行きながら数を学ぶ」を満たす。その値を駆動する「どれほど学んだか」信号にはベイズ・サプライズ（Itti＆Baldi——D_KL[事後‖事前]）または圧縮進展（Schmidhuber）を用い、arXiv:2605.14831の否定的結果（一般MDPの偏り）を承知せよ。決定変更閾値：学習値が全項目で0または1に飽和するなら（ゲート崩壊）、温度／伸ばし（ζ、γ）を再導入するか低分散ガウスSTGに替えよ。

3. **場方程式（一体のソルバ）。**対称分割ステップ・フーリエを実装せよ：フーリエ作用素L̂ ＝ −(ℏ/2m)|k|² − α|k|^σ − iΓ（|k|^σによる分数、−iΓによる散逸）；Λ|Ψ|² ＋ V_extつき物理段階；指数和漸化式によるV_mem（Jiang–Zhangら）；オイラー–丸山によるη（雑音の性質による伊藤またはストラトノヴィッチ）。コードベース：TorchGPE（PyTorch、自動微分可能）から始め分数項、−iΓ、V_mem、ηで拡張せよ。 ベンチマーク：既知体制を数値再現せよ（安定化項なしのL²臨界爆発；−iΓおよび／または非保存乗法ηの投入時の爆発防止／遅延、de Bouard–Debusscheによる）。 閾値：段階Δtがソリトン背景上のWeideman–Herbst不安定性を起こすなら、Δtを下げよ硬い部に指数積分子を用いよ。

4. **微分可能性。**正確勾配のソルバ経由に再帰チェックポイント法つき先離散化後最適化（FFT経由バックプロップ）を用いよ；連続随伴（backsolve）は記憶が支配的隘路の場合のみ留保し、不正確さを承知せよ。小場合の数値検査（有限差分）で勾配を検証し、PyTorchのウィルティンガー共役規約に注意せよ。

5. **Any-to-any多様態。**TOKENチャネル（I／O）には様態別トークナイザ→離散トークン（4M-21）と拡散＋自己回帰混合（Transfusion）の材料が投射と出力図式を与える；様態を向ける多様態ルーティング／MoE。軽量バイト水準符号器／復号器と圧縮表現上のバックボーン（BLT／H-Net図式）を保て。

一般ベンチマーク／選択を変える閾値：(i)エントロピーパッチ化が退化パッチ（すべて長さ1またはすべて巨大）を生むなら、エントロピー模型を再較正するかH-Netの微分可能ルーターに移れ；(ii)BYTEチャネルがFに収束しないなら、精度重みづけを改めよ；(iii)場ソルバが散逸項つきでも数値発散するなら、確率解釈（伊藤対ストラトノヴィッチ）と記憶方式を改めよ。

## 但し書き

- **同名性は等価を含意しない。**ここの全文献語——「崩壊」（NLSの爆発；MLの表現／次元／ランク崩壊；QMの波動関数崩壊）、「記憶」（V_mem、ラマン応答、カプト、EWC／SI／MAS、SSM記憶）、「場」、「原子」、「トークン」、「学習」——は利用可能な技術材料として示され、著者の意味の定義としてではない。それらは名を共有する異なる概念である。
- **否定的／矛盾する結果は保存される。**爆発へのη雑音効果は文献で真に曖昧である：防ぎ遅らせうる（非保存乗法）し加速し起こしうる（保存的、または超臨界の空間に滑らか）——両方報告される。EWCは「一貫して準最適性能を示す」。古典分散–ビリアル則は分数場合に*破れる*。局所FNLSの一般爆発存在定理は未解決のままである。逆伝播代替としての予測符号化の批判的評価（Zahidら2023年）は主張される利点を問う。
- **質可変の史料。**中心数学定式化は査読済み論文に来る（Ann. Probab.、CMP、J. Math. Phys.、Comput. Phys. Commun.、NeurIPS、ICLR、『Neural Computation』、『Vision Research』）。一部の二次支持点は展望／ブログ頁（Medium、emergentmind）に来て、中心定量事実ではなく文脈化にのみ用いられた。
- **2026年日付とプレプリント。**数項目は必ずしも査読済みでない2025–2026年プレプリント（arXiv）である（例：arXiv:2605.*、2606.*、2607.*）；最近の利用可能材料として報告され、プレプリント状態の但し書きつきである。
- **非較正の尊重。**いかなる推奨も方程式の「飼いならし」や線形化を示唆しない；Λ|Ψ|²非線形性は尊重すべき要素として扱われる。数値法は宣言通り（全項一体）の方程式を*解く*ためであり、単純化のためではない。
- **TorchGPE。**ソルバベースとしてのTorchGPE再利用は拡張である：著者論文は端々勾配訓練ではなくGPU加速を強調する；微分可能使用は実装の検証を要するだろう。
