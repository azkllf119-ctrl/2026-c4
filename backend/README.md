# SkillCODER 比赛展示网站 · 后端

本目录是「展示逻辑设计文档」对应的后端实现。它**只做展示**：读取仓库里**已经跑完的实验数据**，
按论文逻辑组织成「八步故事流 + 五个案例 + 指标总览」，供前端一一渲染。

> 设计原则
> 1. **完全遵循论文逻辑**：两阶段（嵌入 / 验证）、八步骤、五字段胶囊、CV-ECC 买家溯源、`2e+s<d_min` 纠错条件，全部对齐论文。
> 2. **展示优先、亲和评委**：接口直接返回可渲染的「主线文案 + 带类型 visual + 可折叠技术细节」，前端无需自己拼论文细节；并提供 SSE 逐步播放、买家指纹对比等交互接口。
>
> 本后端**不含任何水印嵌入 / 攻击 / 模型推理的实验源码**，与 `src/` 完全解耦。

---

## 一、快速启动

```bash
cd backend
pip install -r requirements.txt
bash run.sh                      # 默认绑定 0.0.0.0:8000（本机开 http://127.0.0.1:8000 ，交互文档 /docs）
python3 -m tests.smoke_test      # 离线冒烟测试（验证 5 个案例全链路）
```

默认从仓库根的 `data/` 读数据，可用环境变量覆盖：`export SKILLCODER_DATA_DIR=/abs/path/to/data`。

---

## 二、接口总览

| 区块 | 方法 / 路径 | 说明 |
|---|---|---|
| 健康 | `GET /api/health` | 服务状态、数据目录是否就绪 |
| 总配置 | `GET /api/demo/meta` | 默认 skill、买家列表、攻击族、论文常量、八步元信息 |
| **案例列表** | `GET /api/demo/cases` | 5 个预置案例 |
| **核心故事流** | `GET /api/demo/cases/{case_id}` | 一个案例的完整八步时间线 + 结论摘要 |
| 单步 | `GET /api/demo/cases/{case_id}/steps/{stage}` | 单独取某一步（点开细节用） |
| **逐步播放** | `GET /api/demo/cases/{case_id}/stream?delay=0.9` | SSE 流式推送八步事件 + `report_ready` |
| 原始 Skill | `GET /api/skills/{skill_id}/raw` | 原始未加水印 Skill 文本与章节 |
| 水印 Skill | `GET /api/skills/{skill_id}/watermarked` | 所有者水印 Skill |
| SkillIR | `GET /api/skills/{skill_id}/ir` | 结构化节点图（第 2 步） |
| 买家列表 | `GET /api/skills/{skill_id}/buyers` | 该 skill 的全部买家 |
| **买家指纹** | `GET /api/watermarks/{skill_id}/buyers/{buyer_id}` | 32 位指纹、受控词、逐位映射 |
| **指纹对比** | `GET /api/watermarks/{skill_id}/compare?a=buyer_1&b=buyer_2` | 两买家码字逐位 diff + 汉明距离 |
| 探针 | `GET /api/queries/{skill_id}?kind=all\|positive\|negative\|normal` | 正/负/普通查询 |
| 指标总览 | `GET /api/metrics/overview` | 论文 Table 1/2、图 3、保真、消融 |

`case_id` ∈ `buyer1_clean` / `buyer1_attack_type1` / `buyer1_attack_type2` / `buyer2_clean` / `buyer2_attack_type1`
`stage` ∈ 见下八步标识。

### 故事流八步（stage 标识）

| # | stage | 标题 | visual.type |
|---|---|---|---|
| 1 | `skill_loaded` | 原始 Skill 出场 | `skill_document` |
| 2 | `skillir_built` | 结构化解析 SkillIR | `node_graph` |
| 3 | `owner_watermark_embedded` | 嵌入所有者水印（AGC） | `capsule_schema` |
| 4 | `buyer_fingerprint_embedded` | 嵌入买家指纹（CV-ECC） | `bit_grid` |
| 5 | `attack_applied` | 攻击者复制 / 改写 | `attack_diff` |
| 6 | `differential_probing` | 黑盒差分探测（正/负探针） | `probe_pair` |
| 7 | `ownership_scored` | 胶囊提取与所有权评分 | `score_bar` |
| 8 | `buyer_decoded` | 买家解码与溯源 | `decode_grid` |

每个步骤统一返回：`story`（主线文案）、`technical_hint`（技术细节）、`paper_ref`（论文出处）、`visual`（带类型的可渲染数据）。

---

## 三、真实实验数据来源（已接入）

后端**已接入真实模型输出**，不再依赖任何模拟。数据取自实验服务器的归档运行：

| 项 | 值 |
|---|---|
| run_tag | `newpkg_api_ours_openai_gpt_5_mini_langchain` |
| 模型 | `openai/gpt-5-mini`（论文 closed-source API 之一） |
| Agent 框架 | `LangChain` |
| 配置 | 论文 manifest 默认配置（generalization_3domain） |
| 域 | code_review（展示用）、data_science、travel_planning |
| 买家 | buyer_1 ~ buyer_4 |
| 本地落地路径 | `data/evidence/gpt5mini_langchain/` |
| 原始归档 | `backend/real_assets/skillcoder_demo_real.tar.gz`（md5 `26e512cadef500f2a78278a9c79aaaea`） |

**可信度校验**（下载后逐案例验证，见 `tests/smoke_test.py`）：
5 个案例的真实输出全部正确溯源、`decode_margin = 16`（与次优买家恰好相隔 `d_min`）、
负探针 0 误触发；与该运行 `results/paper/` 官方指标一致（code_review 无攻击 True-WS=0.9956、
各攻击 buyer Top-1=1.0、erasure_rate=0.0）。

> 关于数据 schema：该批次胶囊使用 `snapshot/labels/policy` 字段名（买家受控词在 `labels.token`），
> 攻击批次部分使用 `mode/route/decision/slot`。两者是论文同一套五字段胶囊的等价写法，
> 后端 `capsule.py` 已统一兼容。

### 真实数据 → 展示步骤 映射

| 步骤 | 真实数据文件（相对 `data/evidence/gpt5mini_langchain/`） |
|---|---|
| 第1步 原始 Skill | `skills/skills_raw/code_review/` |
| 第2步 SkillIR | 由 `skills/skills_watermarked/code_review/SKILL.md` 章节拆解 |
| 第3步 所有者水印 | `skills/skills_buyer/code_review__buyer_N/skillcoder.json` + examples.md（`owner_00..07` 胶囊） |
| 第4步 买家指纹 | 各买家 examples.md 的 32 个受控词 → 码字（真实 Hadamard：buyer_1=`1010…`、buyer_2=`1100…`、buyer_4=`11110000…`） |
| 第5步 攻击 | `outputs/attacked_buyer_verification/...`（真实攻击后观测码字）+ `outputs/buyer_normal`、`raw_normal`（保真样例） |
| 第6步 正负探针 | 正：`outputs/buyer_verification/code_review__buyer_N__verification.json`；负：`outputs/watermarked_negative_verification/code_review__negative_verification.json`（均为**真实模型回答**） |
| 第7步 所有权评分 | 正：`outputs/watermarked_verification/` 或 `outputs/attacked_owner_verification/`；负：同上。`capsule.py` 打分得 True-WS/False-WS，并与 `results/paper/effectiveness_distinctiveness.json`、`robustness.json` 交叉印证 |
| 第8步 买家解码 | 从第6步真实输出按 anchor_idx 还原观测码字 → 与码本比对 → top1/top3/errors/erasures/ECC；并与 `results/paper/buyer_attribution.json` 交叉印证 |
| ⑤ 指标总览 | `paper_aggregate`=论文 Table 1/2/图 3；`run_official`=本次运行 `results/paper/*.json` 实测逐域指标 |

每个步骤的 `visual.data_source` 字段标明 `real`（真实输出）或 `simulated`（回退推导）；
`ownership`/`decode` 还带 `official` 字段，给出官方指标用于同屏对照。

---

## 四、数据完整性与回退机制

- **已齐全**：5 个展示案例所需的真实正/负探针输出、攻击后输出、官方指标、买家 skill 全部就位，
  无缺失。后端启动时若检测到 `data/evidence/<run>/outputs/`，即自动进入真实数据模式（`provenance.data_source = "real"`）。
- **回退**：若该目录缺失（例如换部署环境未带数据），后端自动回退到基于买家 examples.md 标准胶囊 +
  `app/attacks.py` 确定性攻击模型的推导值（`data_source = "simulated"`），接口契约不变、前端无需改动。
- **切换数据源**：设环境变量 `SKILLCODER_EVIDENCE_RUN=<run目录名>` 可指向 `data/evidence/` 下的其它运行
  （如换成 Claude Haiku 或 Qwen 系列的归档）。

> 备注：服务器上另有 GPT-5 mini × {CAMEL, OpenClaw}、Claude Haiku 4.5、GLM-Z1-9B、Qwen3-{1.7B,4B,8B} 等
> 多组运行可供替换；本次选用 **GPT-5 mini + LangChain** 因其为 manifest 默认、指标干净、最具代表性。
> 部分 `*_smoke_*` / 早期 probe 运行水印触发不稳定（True-WS 极低、erasure≈1），不可作为展示数据，已排除。

---

## 五、目录结构

```
backend/
├── README.md            # 本文件
├── requirements.txt
├── run.sh               # 启动脚本
├── app/
│   ├── config.py        # 路径 + 论文常量（L=32, d_min=16, λ, τ_o ...）+ evidence 路径
│   ├── data_access.py   # 只读加载 skills / queries / examples 胶囊 / 真实输出
│   ├── codebook.py      # 受控词↔bit，买家 32 位码本（CV-ECC）
│   ├── capsule.py       # 胶囊解析与五字段打分（兼容双 schema + 围栏）
│   ├── evidence.py      # 真实实验输出→所有权评分/买家解码 + 官方指标（首选数据源）
│   ├── attacks.py       # 攻击元信息 + 确定性攻击模型（仅回退模式使用）
│   ├── scoring.py       # 所有权评分 + 买家纠错解码（优先 evidence，否则回退）
│   ├── narratives.py    # 八步中文解说文案
│   ├── cases.py         # 5 个预置案例
│   ├── pipeline.py      # 八步时间线装配（核心，含 provenance/data_source 标注）
│   ├── metrics.py       # 论文聚合指标 + 本次运行官方实测指标
│   └── main.py          # FastAPI 路由 + SSE + CORS
├── real_assets/
│   └── skillcoder_demo_real.tar.gz   # 服务器归档原始包（不解压也可，已落地到 data/evidence/）
└── tests/
    └── smoke_test.py    # 离线全链路冒烟测试（含真实数据校验）
```

数据目录（仓库根）：
```
data/evidence/gpt5mini_langchain/
├── outputs/             # 真实模型输出（buyer/attacked/negative/owner/normal）
├── results/paper/       # 该运行官方指标（effectiveness/robustness/buyer_attribution/fidelity）
├── skills/              # 产生这些输出的 skill 副本（raw/watermarked/buyer_1..4）
└── queries/             # 探针查询
```
