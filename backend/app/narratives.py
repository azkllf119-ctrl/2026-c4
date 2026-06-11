"""八步故事流的中文解说文案。

文风要求：浅显但不白话、面向评委、科技展示口吻。
每一步统一两层信息：
  story          —— 主线一句话（大字，故事化）
  technical_hint —— 技术细节（点开才看，含公式/字段）
"""
from __future__ import annotations

# 八个阶段的稳定标识（前端按此顺序播放 / 点选）
STAGES = [
    "skill_loaded",
    "skillir_built",
    "owner_watermark_embedded",
    "buyer_fingerprint_embedded",
    "attack_applied",
    "differential_probing",
    "ownership_scored",
    "buyer_decoded",
]

STAGE_META: dict[str, dict] = {
    "skill_loaded": {
        "index": 1,
        "title": "原始 Skill 出场",
        "phase": "embedding",
        "story": "我们先从一份普通的智能体 Skill 开始。它看起来只是一份 Markdown 文档，"
                 "但里面其实包含角色定义、任务流程、约束规则、异常处理和示例——它不是一句提示词，"
                 "而是一套可复用的能力资产。",
        "technical_hint": "原始技能 S：一份结构化、可读、可部署的多段文档。",
    },
    "skillir_built": {
        "index": 2,
        "title": "结构化解析 SkillIR",
        "phase": "embedding",
        "story": "系统不会把 Skill 当作一整段文本，而是先把它拆成结构化节点：哪些是约束、"
                 "哪些是工作流步骤、哪些是示例、哪些是输出格式。这样做是为了把水印锚定在技能的"
                 "行为结构上，而不是锚定在容易被改写的表面词句上。",
        "technical_hint": "Φ(S)=G_S=(V_S, E_S)，六类带类型的指令节点（约束/工作流/示例/输出/"
                          "上下文/异常）。结构在攻击下保持不变，是水印能够存活的基础。",
    },
    "owner_watermark_embedded": {
        "index": 3,
        "title": "嵌入所有者水印（Artifact-Gated Capsule）",
        "phase": "embedding",
        "story": "系统在多个结构节点里分散写入一组自然语言条件指令。它们平时不会触发，也不影响"
                 "普通用户使用；只有当审计方发出带特定条件的验证查询时，Skill 才会输出一个内部胶囊"
                 "（internal_capsule）。这个胶囊就是所有者证明。",
        "technical_hint": "胶囊 a=⟨mode, route, checkpoint, decision, slot⟩。由所有者密钥 k_o "
                          "决定写入哪些节点、以及触发所需满足的激活条件——条件门控+分散注入，"
                          "使得删一处不够，需协调地删多处才能去除胶囊，规避成本很高。",
    },
    "buyer_fingerprint_embedded": {
        "index": 4,
        "title": "嵌入买家指纹（Controlled-Vocabulary ECC）",
        "phase": "embedding",
        "story": "同一份 Skill 会卖给不同买家，所以只证明“这是我的 Skill”还不够，还得知道是哪一份"
                 "副本泄露了。系统为每个买家分配一串纠错码，把这串码藏进胶囊的 slot/decision 字段里。"
                 "即使输出有少量错误或缺失，也能靠纠错解码恢复买家身份。",
        "technical_hint": "CV-ECC：Hadamard 码，码长 L=32，最小距离 d_min=16。每一位由一对受控词实现"
                          "（<name>_trace=1 / trace_<name>=0）。不同买家码字相隔≥16 位，"
                          "因此错几位也不会把 buyer_1 误判成 buyer_2。",
    },
    "attack_applied": {
        "index": 5,
        "title": "攻击者复制 / 改写",
        "phase": "deploy",
        "story": "现在模拟攻击者拿到某个买家的副本并重新部署。无攻击下副本基本原样；第一类攻击做"
                 "改写、压缩或重排；第二类攻击专门删除看起来像内部审计的条款。攻击者的限制是："
                 "改得太狠，Skill 本身就不好用了。",
        "technical_hint": "四类攻击：paraphrase / compression / auxiliary-clause deletion / "
                          "reorganization，均须保留≥80% 原始效用（utility-preserving）。"
                          "辅助条款删除是其中最具挑战性的攻击。",
    },
    "differential_probing": {
        "index": 6,
        "title": "黑盒差分探测（正/负探针配对）",
        "phase": "verification",
        "story": "审计方看不到可疑服务内部的 Skill，只能像普通用户一样发请求。所以系统发送一组正负"
                 "探针：正探针带隐藏激活条件，负探针看起来很像但缺关键条件。真正的水印副本会在正探针"
                 "下吐胶囊、在负探针下保持沉默。",
        "technical_hint": "成对探针 Q={(q_i⁺, q_i⁻)}。正探针 q⁺ 嵌入所有者密钥 k_o，负探针 q⁻ 保持"
                          "相同话题/长度/风格但省略关键条件。只有“正向触发、负向沉默”的激活-沉默"
                          "非对称性才算真水印，可排除独立 skill 的偶然匹配。",
    },
    "ownership_scored": {
        "index": 7,
        "title": "胶囊提取与所有权评分",
        "phase": "verification",
        "story": "模型输出可能很长，胶囊也可能夹在普通回答里。系统用滑动窗口扫描输出，寻找符合 "
                 "mode/route/checkpoint/decision/slot 五字段的结构，再比较正负探针的得分差距。"
                 "如果正向稳定激活、负向稳定沉默，就判定所有权成立。",
        "technical_hint": "Score_own = True-WS − λ · False-WS。胶囊提取用滑动窗口 ψ(·) 做五字段相似度"
                          "匹配；当 Score_own > τ_o 时所有权成立。",
    },
    "buyer_decoded": {
        "index": 8,
        "title": "买家解码与溯源",
        "phase": "verification",
        "story": "所有权成立后，系统继续读胶囊里 slot/decision 的 token，把观察到的受控词还原成 "
                 "0、1 或缺失位（⊥），再交给纠错解码器。最终输出最可能的泄露买家——比如 buyer_1 或 "
                 "buyer_2，并给出错误数、擦除数和置信度。",
        "technical_hint": "对每个码位提取 ẑ_j∈{0,1,⊥}，再 b̂=Decode_ECC(ẑ,C)。纠错保证："
                          "当 2·errors + erasures < d_min 时可唯一恢复正确买家。",
    },
}


def stage_meta(stage: str) -> dict:
    return {"stage": stage, **STAGE_META[stage]}
