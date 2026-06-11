"""前端 UI 静态文案（单一真源）。

设计目的：把原本硬编码在前端（index.html / app.js）里的中文界面文字——
导航、背景介绍、各区块标题、按钮、8 个 visual 渲染器里的内联标签、裁决卡、
指标表头等——全部集中到后端，通过 `GET /api/ui/text` 下发。

这样后续把后端交给前端工程师重做界面时，所有文案都能从接口拿到，前端无需再
内嵌任何业务文字。本模块不含任何实验逻辑，只是文案常量。

约定：
  - 句子里需要插入运行时变量的，用 ``{name}`` 占位符模板，前端用 fmt() 替换。
  - 模板里保留原有的 HTML 标记（如 ``<b>`` / ``<span>``），前端按 innerHTML 注入。
  - 纯文本标签为无占位符的普通字符串。
"""
from __future__ import annotations

UI_TEXT: dict = {
    # ------------------------------------------------------------------
    # 站点 meta / 顶部导航
    # ------------------------------------------------------------------
    "meta": {
        "title": "SkillCODER · Skill 水印与买家溯源全流程演示",
        "brand_title": "SkillCODER",
        "brand_sub": "Skill 水印 · 黑盒识别 · 买家溯源 · 全流程演示",
        "nav": [
            {"href": "#sec-intro", "label": "背景"},
            {"href": "#sec-cases", "label": "案例"},
            {"href": "#sec-story", "label": "演示"},
            {"href": "#sec-verdict", "label": "裁决"},
            {"href": "#sec-metrics", "label": "指标"},
        ],
        "conn": {
            "wait": "连接后端中…",
            "ok": "● 后端已连接",
            "bad": "● 后端未连接",
        },
    },

    # ------------------------------------------------------------------
    # 后端未连接时的提示卡
    # ------------------------------------------------------------------
    "offline": {
        "title": "⚠️ 没有连接到后端",
        "desc": "请先启动后端服务，再刷新本页面：",
        "url_label": "当前尝试连接：",
        "button": "重新连接",
    },

    # ------------------------------------------------------------------
    # ① 知识背景 hero
    # ------------------------------------------------------------------
    "hero": {
        "h1": "当一份 Skill 被盗走，我们如何证明并追凶？",
        "lead": "智能体 <b>Skill</b> 不是一句提示词，而是一套包含<b>角色、工作流、约束、异常处理、示例</b>的可复用能力资产，"
                "单价可达数千美元。但它公开、可读、可部署，因此极易被原样复制或改写转售。",
        "cards": [
            {"icon": "📈", "title": "难点一：规模长",
             "body": "Skill 是几千 token 的长文档，传统 token 级水印信号会被稀释。"},
            {"icon": "📖", "title": "难点二：要可读",
             "body": "Skill 要给人看、给人改，token 级扰动会破坏可读性与实用价值。"},
            {"icon": "✅", "title": "我们的答案：SkillCODER", "highlight": True,
             "body": "把水印锚定在技能的<b>行为结构</b>上，而非表面词句；纯黑盒、不碰模型权重、不破坏正常功能。"},
        ],
        "flow": ["加水印", "卖给买家", "被盗改部署", "黑盒探测", "证明所有权", "追出买家"],
        "cta": "选择一个案例，开始演示 ↓",
    },

    # ------------------------------------------------------------------
    # 各区块标题 / 说明
    # ------------------------------------------------------------------
    "sections": {
        "cases": {
            "h2": "② 选择展示案例",
            "desc": "五个真实实验场景。点击任意一张卡片，进入八步故事流演示。",
            "attack_legend": [
                "<b>第一类攻击</b>：攻击者不知道有水印，只做保功能的同义改写 / 压缩 / 重排（盲攻击）。",
                "<b>第二类攻击</b>：攻击者怀疑有水印，定向删除内部审计 / 交接 / 胶囊相关条款（针对性削弱，最难）。",
            ],
        },
        "story": {
            "h2": "③ 全流程演示",
            "sub_default": "请先在上方选择一个案例。",
        },
        "verdict": {
            "h2": "④ 结果裁决",
            "empty": "完成一个案例的演示后，这里会给出最终判决。",
        },
        "metrics": {
            "h2": "⑤ 实验指标总览",
            "desc": "单个案例之外，方法在整体上是否可信？整体汇总指标 + 本次真实运行的官方实测。",
        },
    },

    # ------------------------------------------------------------------
    # 故事流控制条 / 通用
    # ------------------------------------------------------------------
    "controls": {
        "prev": "← 上一步",
        "next": "下一步 →",
        "play": "▶ 自动播放",
        "pause": "⏸ 暂停",
        "tech_summary": "🔬 技术细节（点开查看）",
        "pip_step": "STEP",
    },

    "footer": "SkillCODER 比赛展示系统 · 纯展示前端",

    # bit 网格每个格子的悬浮提示（第几位）
    "bit_tooltip": "第 {i} 位",

    # ------------------------------------------------------------------
    # 三大阶段标签（与后端 step.phase 对应；颜色仍由前端样式决定）
    # ------------------------------------------------------------------
    "phases": {
        "embedding": "阶段一 · 水印嵌入",
        "deploy": "过渡 · 部署/攻击",
        "verification": "阶段二 · 黑盒验证",
    },

    # ------------------------------------------------------------------
    # ② 案例卡
    # ------------------------------------------------------------------
    "attack_tags": {
        "none": "无攻击",
        "type1": "第一类·改写",
        "type2": "第二类·删条款",
    },
    "case_card": {
        "go": "进入演示 →",
    },

    # ------------------------------------------------------------------
    # ③ 选中案例后的提示 / 来源标签
    # ------------------------------------------------------------------
    "story": {
        "loading": "正在加载真实实验数据…",
        "load_failed": "加载失败：{msg}",
        "cur_case": "当前案例：<b>{title}</b> ｜ 数据来源：{model} + {agent} {src_tag}",
        "src_real": "真实模型输出",
        "src_sim": "推导数据",
    },
    # visual 内部的来源小标签
    "src_tag": {
        "real": "真实数据",
        "sim": "推导数据",
    },

    # ------------------------------------------------------------------
    # 8 个 visual 渲染器的内联标签
    # ------------------------------------------------------------------
    "visual": {
        "skill_document": {
            "hero_title": "🎯 当前对象：{name}",
            "what_it_does": "它做什么：",
            "why_this_skill": "为何用它：",
            "composition_title": "🧩 Skill 的典型构成",
            "others_title": "📦 素材包内的其它 Skill（本页未展开）",
            "others_note": "本页以 code_review 为主故事线，其它 Skill 用于实验覆盖。",
            "section_count": "这份 Skill 含 <b>{count}</b> 个功能段落：",
            "full_doc_label": "完整 Skill 文档（可上下拖动查看全文）：",
        },
        "node_graph": {
            "intro": "系统把整篇文档拆成带类型的<b>结构节点</b>（水印将锚定在这些节点上，而非表面词句）：",
            "node_types": "六类节点：约束 / 工作流 / 示例 / 输出格式 / 上下文 / 异常处理",
            "anchors_label": "本例选中的四个 anchor（水印挂载点）及其选择理由：",
            "anchor_idx": "anchor {n}",
            "meaning": "含义：",
            "reason": "为何选它：",
            "explain_title": "从文本水印到结构水印",
        },
        "capsule_schema": {
            "gate_title": "📜 新增到 Skill 的门控规则（默认沉默，审计时才激活）",
            "capsule_title": "🧬 五字段内部胶囊 internal_capsule",
            "example_summary": "查看一条真实胶囊（可滚动）",
            "field_meanings_title": "字段含义",
            "explain_title": "相比未加水印 Skill，多了什么",
            "diff_label": "真实文件对比：未加水印 reference.md → 加所有者水印后（<span style=\"color:var(--green)\">绿色=新增的审计条款</span>）",
        },
        "bit_grid": {
            "intro": "买家 <b>{buyer_id}</b> 的指纹 = 一串 <b>{codeword_length} 位</b>纠错码（编码规则：{bit_rule}）",
            "codeword_label": "{buyer_id} 的码字",
            "compare_label": "对照 {buyer_b} 的码字（<span style=\"color:var(--amber)\">黄框</span>=两者不同的位）",
            "distance": "两者相隔 <b>{hamming}</b> 位（≥ d_min={d_min}）。{note}",
            "token_table_title": "buyer_1 与 buyer_2 前 8 个码位对照",
            "th_anchor": "anchor",
            "th_b1_token": "buyer_1 token",
            "th_bit": "bit",
            "th_b2_token": "buyer_2 token",
            "rule_note": "规则写在表里：trace_xxx = 0，xxx_trace = 1。",
            "explain_title": "买家专属版本额外加了什么",
            "diff_label": "真实样例对比：所有者样例(token: owner_00) → {buyer_id} 专属样例（受控词汇即买家指纹位）",
        },
        "attack_diff": {
            "fidelity_title": "🧪 保真度：攻击后普通任务仍正常",
            "case_card_title": "🎭 当前故事设定",
            "case_card_line": "<b>受测 Skill：</b>{skill} ｜ <b>真实泄露源：</b>{leaker} ｜ <b>处理方式：</b>{attack}",
            "diff_label": "攻击前后 Skill 真实代码对比（<span style=\"color:var(--red)\">红=被删/改</span>，<span style=\"color:var(--green)\">绿=新增</span>）：",
            "diff_note": "这不是改一个标识符，而是在真实 Skill 文本里重写、删减或重排审计相关规则。",
            "no_attack_title": "无攻击",
            "no_attack_body": "买家副本被直接重新部署，没有文本改动。",
            "impact_label": "对水印码字的影响 {src_tag}",
            "before_label": "攻击前 · 买家真实码字",
            "after_label": "攻击后 · 审计侧观测码字（<span style=\"color:var(--red)\">红框</span>=被影响的位；⊥=读不出）",
            "constraint_prefix": "⚠ ",
        },
        "probe_pair": {
            "intro": "审计方只能黑盒提问。成对发送 <b>{positive_count}</b> 正 + <b>{negative_count}</b> 负探针 {src_tag}{model_part}",
            "model_part": " ｜真实模型：{model} + {agent}",
            "positive_title": "正探针 <span class=\"pill pill-pos\">应触发胶囊</span>",
            "negative_title": "负探针 <span class=\"pill pill-neg\">应保持沉默</span>",
            "question_label": "提问：",
            "positive_answer_label": "真实回答：吐出 internal_capsule ✅",
            "negative_answer_label": "真实回答：正常回复、不吐胶囊 🤐",
            "negative_empty": "（普通回答，无胶囊）",
            "diff_prefix": "✓ ",
            "token_focus_title": "🔑 从这条胶囊里读到的“这一位”",
            "token_focus_line": "受控词 token = <code>{token}</code> → 比特 <b>{bit}</b> ｜ 位置：{where_to_find}",
        },
        "score_bar": {
            "official": "📊 与官方指标对照：True-WS <b>{true_ws}</b> ｜ False-WS <b>{false_ws}</b> ｜ Margin <b>{margin}</b> ｜ 准确率 <b>{accuracy}</b>",
            "formula": "公式：<code>{formula}</code> {src_tag}",
            "true_ws_label": "True-WS（正探针胶囊得分） = {value}",
            "false_ws_label": "False-WS（负探针误触发） = {value}",
            "threshold_label": "↑ 黄线 = 判定阈值 τ_o = {thr}",
            "summary_line": "Margin = <b>{margin}</b> ｜ Score_own = <b>{score_own}</b> →",
            "verified": "✅ 所有权成立",
            "not_verified": "❌ 未成立",
            "explain_score_title": "True-WS 与 False-WS 怎么来的",
            "explain_why_title": "为什么能确认所有权",
            "verdict_prefix": "⚖ ",
        },
        "decode_grid": {
            "official": "📊 与官方指标对照：Top-1 <b>{top1}</b> ｜ Top-3 <b>{top3}</b> ｜ 擦除率 <b>{erasure_rate}</b>",
            "badge_hit": "命中",
            "exact_match": "（完全吻合）",
            "status_matched": "✅ 命中",
            "status_error": "⚠ 读错",
            "status_erasure": "⊥ 漏读",
            "decode_table_title": "前 8 个观测码位（token → bit → 与期望对照）",
            "th_anchor": "anchor",
            "th_obs_token": "观测 token",
            "th_bit": "bit",
            "th_expected": "期望",
            "th_status": "状态",
            "decode_table_note": "完整流程有 32 位；这里先列前 8 位，溯源恢复的是带冗余的码字，而非明文 buyer_id。",
            "observed_label": "从真实输出还原的观测码字：",
            "rank_intro": "把观测码字与每个买家的标准码字比对，按错误数排序，最少者即泄露买家：",
            "th_buyer": "买家",
            "th_errors": "错误数 e",
            "th_erasures": "擦除数 s",
            "th_diff": "差异",
            "result_line": "🎯 溯源结果：<b class=\"ok\">{attributed_buyer}</b> ｜ 解码裕度 = <b>{decode_margin}</b> ｜ 置信度 = <b>{confidence}</b>",
            "ecc_line": "纠错条件 <code>2·e + s = {ecc_lhs} {op} d_min = {d_min}</code> → ",
            "ecc_ok": "满足，可靠恢复 ✅",
            "ecc_bad": "不满足",
            "verdict_prefix": "⚖ ",
        },
    },

    # ------------------------------------------------------------------
    # ④ 裁决卡
    # ------------------------------------------------------------------
    "verdict": {
        "title": "📋 判决书 · {title}",
        "ownership_label": "所有权认定",
        "ownership_ok": "✅ 已确认",
        "ownership_bad": "❌ 未确认",
        "ownership_stats": "True-WS <b>{true_ws}</b> · False-WS <b>{false_ws}</b> · Margin <b>{margin}</b>",
        "attribution_label": "买家溯源",
        "attribution_value": "🎯 {attributed_buyer}",
        "attribution_stats": "置信度 <b>{confidence}</b> · 错误 <b>{errors}</b> · 擦除 <b>{erasures}</b> · 解码裕度 <b>{decode_margin}</b>",
        "attack_title": "🛡 攻击类型",
        "ecc_title": "🧮 纠错条件",
        "ecc_ok": "2e+s < d_min ✅",
        "ecc_bad": "2e+s ≥ d_min",
        "ecc_note": "纠错保证：满足即可唯一恢复买家。",
        "source_title": "📊 数据出处",
        "source_real": "真实模型输出",
        "source_sim": "推导数据",
    },

    # ------------------------------------------------------------------
    # ⑤ 指标总览
    # ------------------------------------------------------------------
    "metrics": {
        "compare_headers": ["指标", "SkillCODER", "PromptCARE", "PromptCOS", ""],
        "robust_headers": ["攻击类型", "买家 Top-1", "所有权准确率"],
        "ablation_headers": ["去掉的组件", "后果"],
        "run_official_title": "🟢 本次真实运行实测（{model} + {agent}）",
        "run_official_headers": ["域", "True-WS", "False-WS", "Margin", "准确率"],
    },
}
