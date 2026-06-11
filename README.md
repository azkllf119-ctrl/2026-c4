# SkillCODER · Skill 水印与买家溯源全流程演示平台

这是一个**纯展示**网站：用一条完整的故事线讲清楚——当一份高价值的智能体 **Skill** 被盗走后，
我们如何**证明所有权**并**追出泄露的买家**。后端读取已经跑完的真实实验数据（GPT-5 mini +
LangChain），按「两阶段 · 八步骤」组织成可渲染的故事流；前端按步渲染，配合上一步/下一步/
自动播放等交互，希望在几分钟内让大家能看懂方法。

> 后端**不含**任何水印嵌入 / 攻击 / 模型推理的实验源码，只做「读数据 + 组织讲解」。



---

## 一、目录结构

```
SkillCODER_Demo_Final/
├── README.md          # 本文件（总览）
├── backend/           # FastAPI 后端：读数据 + 组织八步故事流 + 下发界面文案
│   ├── app/           # 路由与装配逻辑（详见 backend/README.md）
│   ├── run.sh         # 启动脚本
│   ├── requirements.txt
│   ├── tests/smoke_test.py
│   └── 前端对接说明.md  # 给前端工程师的接口对接手册
├── frontend/          # 纯原生 HTML/CSS/JS（无框架、无构建）
│   ├── index.html     # 页面骨架（静态文字由后端下发后注入）
│   ├── app.js         # 全部逻辑：拉数据 + 按 visual.type 渲染 8 步 + 交互
│   ├── styles.css     # 样式（含三大阶段配色）
│   └── config.js      # 后端地址配置
└── data/              # 真实实验数据（evidence 归档运行）
```

> **文案的唯一真源在后端。** 前端不内嵌业务中文——所有界面文字（导航、背景介绍、各区块标题、8 个 visual 渲染器的内联标签、裁决卡、指标表头等）都由 `GET /api/ui/text` 下发。请前端工程师做界面时，对接接口拿到全部文字。详见下文「四、界面文案后端化」。

---

## 二、怎么启动

### 方式 A：后端一并托管前端（推荐，一条命令跑通整套）

后端已把 `frontend/` 挂在 `/ui`，启动后端后直接访问页面：

```bash
cd backend
pip install -r requirements.txt
bash run.sh                      # 默认监听 0.0.0.0:8000（带 --reload 热重载）
```

> `run.sh` 现默认绑定 `0.0.0.0`，即监听本机所有网卡——本机用 `127.0.0.1` 访问，
> 局域网内其它设备/手机用本机 IP（如 `http://192.168.1.10:8000/ui/`）也能直接打开。
> 只想本机可见时，加 `HOST=127.0.0.1 bash run.sh`。

- 本机演示页面： **http://127.0.0.1:8000/ui/**
- 交互式接口文档（Swagger）： **http://127.0.0.1:8000/docs**

环境变量（均可选）：

| 变量                      | 默认                 | 说明                                   |
| ------------------------- | -------------------- | -------------------------------------- |
| `HOST`                    | `0.0.0.0`            | 监听地址（默认全网卡；本机访问设为 `127.0.0.1`） |
| `PORT`                    | `8000`               | 端口                                   |
| `SKILLCODER_DATA_DIR`     | 仓库根 `data/`       | 实验数据目录                           |
| `SKILLCODER_EVIDENCE_RUN` | `gpt5mini_langchain` | 选用 `data/evidence/` 下哪一组归档运行 |

### 方式 B：前端单独起静态服务器

```bash
cd frontend
python3 -m http.server 8080      # 浏览器开 http://127.0.0.1:8080/
```

此方式下前端默认连 `http://127.0.0.1:8000` 的后端（已开 CORS）。后端在别处时用 URL 参数覆盖：
`http://127.0.0.1:8080/?api=http://192.168.1.10:8000`

### 冒烟测试（离线，不依赖浏览器）

```bash
cd backend
python3 -m tests.smoke_test      # 验证 5 个案例全链路、真实数据校验，全绿即 OK
```

---

## 三、接口设计

- **基地址**：`http://127.0.0.1:8000`
- **返回格式**：全部 JSON，已开启 CORS（前端任意端口可直接 fetch）
- **约定参数**：
  - `case_id` ∈ `buyer1_clean` / `buyer1_attack_type1` / `buyer1_attack_type2` / `buyer2_clean` / `buyer2_attack_type1`
  - `skill_id` 用 `code_review`
  - `stage` ∈ 见下八步标识

### 接口清单（15 个）

| 用途              | 方法 路径                                                    | 前端何时用                                         |
| ----------------- | ------------------------------------------------------------ | -------------------------------------------------- |
| 健康检查          | `GET /api/health`                                            | 启动时探活                                         |
| **界面文案**      | `GET /api/ui/text`                                           | 启动时拉取，填充所有界面静态文字                   |
| 全局配置          | `GET /api/demo/meta`                                         | 默认 skill、买家列表、攻击族、方法常量、八步元信息 |
| **案例列表**      | `GET /api/demo/cases`                                        | 渲染「② 案例选择台」5 张卡片                       |
| **★ 案例全流程**  | `GET /api/demo/cases/{case_id}`                              | 渲染「③ 故事流」整页（最重要）                     |
| 单个步骤          | `GET /api/demo/cases/{case_id}/steps/{stage}`                | 单独点开某一步细节（可选）                         |
| **逐步播放(SSE)** | `GET /api/demo/cases/{case_id}/stream?delay=0.9`             | 「运行中」动画                                     |
| 原始 Skill        | `GET /api/skills/{skill_id}/raw`                             | 第 1 步看原文                                      |
| 水印 Skill        | `GET /api/skills/{skill_id}/watermarked`                     | 文件对比时                                         |
| SkillIR 结构      | `GET /api/skills/{skill_id}/ir`                              | 第 2 步节点图（也已内嵌在全流程里）                |
| 买家列表          | `GET /api/skills/{skill_id}/buyers`                          | 下拉选买家                                         |
| **买家指纹**      | `GET /api/watermarks/{skill_id}/buyers/{buyer_id}`           | 第 4 步 32 位指纹格子                              |
| **指纹对比**      | `GET /api/watermarks/{skill_id}/compare?a=buyer_1&b=buyer_2` | buyer_1 vs buyer_2 逐位 diff                       |
| 探针查询          | `GET /api/queries/{skill_id}?kind=all\|positive\|negative\|normal` | 单独看探针文本                                     |
| **指标总览**      | `GET /api/metrics/overview`                                  | 渲染「⑤ 指标总览页」                               |

> **前端 90% 的工作只用三个接口**：`/api/ui/text`（界面文字）+ `/api/demo/cases`（案例列表）+
> `/api/demo/cases/{case_id}`（全流程）。其余都是锦上添花。完整字段说明见 `backend/前端对接说明.md`。

### 核心数据结构：`GET /api/demo/cases/{case_id}`

整个网站的主数据源。返回结构（节选）：

```jsonc
{
  "case_id": "buyer1_attack_type2",
  "title": "Buyer 1 · 第二类攻击",
  "skill_id": "code_review",
  "buyer_id": "buyer_1",
  "attack": { "id": "...", "name": "...", "description": "...", "text_effect": "..." },
  "goal": "这个案例想证明什么（一句话）",

  "provenance": {                  // 数据出处，体现“真实数据”
    "data_source": "real",         // real=真实模型输出 / simulated=回退推导
    "model": "openai/gpt-5-mini",
    "agent": "LangChain",
    "note": "步骤 6–8 均来自真实模型输出，并与官方指标交叉印证。"
  },

  "summary": {                     // ④ 裁决卡直接用这个
    "ownership": "verified",
    "attributed_buyer": "buyer_1",
    "attribution_correct": true,
    "true_ws": 1.0, "false_ws": 0.0187, "margin": 0.9813,
    "confidence": 1.0, "errors": 0, "erasures": 0,
    "decode_margin": 16, "ecc_satisfied": true
  },

  "timeline": [ /* 8 个步骤 */ ]
}
```

每个 `timeline[i]` 步骤统一是这个形状——**前端循环它，按 `visual.type` 选组件渲染即可**：

```jsonc
{
  "stage": "ownership_scored",    // 步骤稳定标识
  "index": 7,                     // 第几步
  "title": "胶囊提取与所有权评分",  // 大标题
  "phase": "verification",        // embedding/deploy/verification 三大阶段 → 配色
  "story": "主线一句话（大字）",
  "technical_hint": "技术细节（折叠区，含公式）",
  "thesis": "本步论点（一句话）",
  "explanations": ["要点1", "要点2"],
  "visual": { "type": "score_bar", /* 该步专属可视化数据 */ }
}
```

### 故事流八步 → `visual.type`

| #    | stage                        | 标题                       | visual.type      |
| ---- | ---------------------------- | -------------------------- | ---------------- |
| 1    | `skill_loaded`               | 原始 Skill 出场            | `skill_document` |
| 2    | `skillir_built`              | 结构化解析 SkillIR         | `node_graph`     |
| 3    | `owner_watermark_embedded`   | 嵌入所有者水印（AGC 胶囊） | `capsule_schema` |
| 4    | `buyer_fingerprint_embedded` | 嵌入买家指纹（CV-ECC）     | `bit_grid`       |
| 5    | `attack_applied`             | 攻击者复制 / 改写          | `attack_diff`    |
| 6    | `differential_probing`       | 黑盒差分探测（正/负探针）  | `probe_pair`     |
| 7    | `ownership_scored`           | 胶囊提取与所有权评分       | `score_bar`      |
| 8    | `buyer_decoded`              | 买家解码与溯源             | `decode_grid`    |

> 步骤 6–8 的 `visual` 里都有 `data_source`；步骤 7/8 还带 `official` 字段（官方指标），
> 可与实测数字同屏并排，强调「真实数据 + 论文一致」。

---

## 四、界面文案后端化

为方便把后端单独交付给前端工程师重做界面，**所有界面静态中文都集中在后端**，经
`GET /api/ui/text` 下发，前端启动时拉一次并注入页面。

- 返回是一个按区域分组的字典：`meta` / `offline` / `hero` / `sections` / `controls` /
  `footer` / `phases` / `attack_tags` / `case_card` / `story` / `src_tag` / `visual` /
  `verdict` / `metrics` / `bit_tooltip`。其中 `visual` 下再按 8 种 `visual.type` 分组。
- **占位符约定**：需要插入运行时变量的句子用 `{name}` 占位符并保留 HTML 标记，例如
  `"买家 <b>{buyer_id}</b> 的指纹 = 一串 <b>{codeword_length} 位</b>纠错码"`。前端把占位符替换为对应数据
  即可（参考 `frontend/app.js` 里的 `fmt()` 与 `applyStaticText()`）。
- 唯一仍留在前端的文字是「后端未连接」时的兜底提示——那一刻后端正好不可达、无法由接口下发；
  其相同文案在本接口的 `meta.conn` / `offline` 里也有一份。

---

## 五、我们要的交互效果

整站是一条**单页滚动叙事**，从上到下 5 个区块。核心体验是：选一个案例 → 走完八步故事流 →
看到判决 → 再看整体指标。

### ① 知识背景（hero）

几分钟讲清「这是个真问题」：Skill 是什么、为何易被盗、两个技术难点（规模长 / 要可读）、
我们的答案（把水印锚定在行为结构上，纯黑盒、不破坏功能）。底部一条流程胶囊：
`加水印 → 卖给买家 → 被盗改部署 → 黑盒探测 → 证明所有权 → 追出买家`。

### ② 案例选择台

渲染 5 张案例卡（`title` / `goal` / 攻击标签 / 买家标签）。两类攻击要讲清区别：
**第一类**＝攻击者不知道有水印、只做保功能的改写/压缩/重排（盲攻击）；
**第二类**＝攻击者怀疑有水印、定向删除内部审计/交接条款（针对性削弱，最难）。点击卡片进入③。

### ③ 故事流时间线（核心页）

一次拉全 8 步（`GET /api/demo/cases/{case_id}`）。布局：顶部一条 8 节点进度条（按 `phase`
三色：嵌入·蓝 / 部署·灰 / 验证·绿）；主区域按当前步渲染「**story 大字 + thesis 论点 +
explanations 要点 + 按 `visual.type` 的可视化组件 + 可折叠的技术细节**」。交互：

- **上一步 / 下一步**：手动切换，首/末步自动禁用对应按钮。
- **进度条节点 / 圆点**：点击直接跳到任意一步。
- **自动播放**：每 2.6s 推进一步，到末步停止；可暂停。
- **逐步播放动画（可选）**：`GET /api/demo/cases/{case_id}/stream?delay=0.9` 是 SSE，
  用 `EventSource` 监听，事件名就是 `stage`，最后一个事件 `report_ready` 带 summary，
  每收到一个事件点亮一步——做「运行中」的逐步揭示效果。

8 种可视化组件各有侧重：完整 Skill 文档与章节高亮、结构节点图与 anchor 选点理由、
五字段胶囊 schema 与真实文件 diff、32 位指纹网格与买家间逐位差异、攻击前后代码 diff 与
受影响码位高亮、正/负探针左右对照、所有权双分数条与阈值线、买家解码排名表与纠错条件。

### ④ 结果裁决

复用③返回的 `summary` + `provenance`，渲染一张「判决书」：
✅ 所有权（`true_ws`/`false_ws`/`margin`）、🎯 溯源买家（`attributed_buyer` + 置信度 +
错误/擦除 + `ecc_satisfied`）、🛡 攻击类型、📊 数据出处（真实模型 + 官方指标一致）。

### ⑤ 实验指标总览

`GET /api/metrics/overview`，渲染两块：

- **整体汇总**：所有权 99.2%、买家 Top-1 99.3%、四类攻击鲁棒性、保真、消融——我们 vs 两个基线的对比条形图。
- **本次真实运行实测**：逐域官方指标表格，证明「不仅论文说有效，这次也实测有效」。

> 贯穿全站的一个体验点：每处真实数字旁标明 `real`（真实模型输出）或 `simulated`（回退推导），
> 步骤 7/8 还把 `official` 官方指标并排显示，强调数据可信、与论文一致。

---

## 六、数据与回退

后端**已接入真实模型输出**（`data/evidence/gpt5mini_langchain/`）：5 个案例全部正确溯源、
`decode_margin = 16`、负探针 0 误触发，并与该运行官方指标交叉印证。若该数据目录缺失，后端
自动回退到基于标准胶囊 + 确定性攻击模型的推导值（`data_source = "simulated"`），**接口契约不变、
前端无需改动**。更多细节见 `backend/README.md`。
