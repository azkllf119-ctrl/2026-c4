"""展示内容补全层：真实文件 diff + 解说文案。

这一层只负责「把 demo 讲透」：
  - 真实文件级 diff：未加水印↔加水印、所有者 token↔买家 token、攻击前↔攻击后。
    全部读取本仓库可靠数据源（data/evidence/.../skills/...），不依赖任何外部素材。
  - 中文解说文案：每一步的论点(thesis)、要点(explanations)、锚点理由、攻击说明等。

所有文本均为面向评委的精炼表述。
"""
from __future__ import annotations

from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from . import config

# ---------------------------------------------------------------------------
# 文件级 diff（两栏对照）
# ---------------------------------------------------------------------------


def _read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines() if path.exists() else []


def _line(no, text, status):
    return {"line": no, "text": text, "status": status}


def diff_lines(before_lines, after_lines, before_label, after_label,
               highlights=None, context=3, max_groups=4) -> dict[str, Any]:
    """把两份文本做行级 diff，返回左右两栏带状态(same/added/removed/changed/gap)的行。"""
    m = SequenceMatcher(a=before_lines, b=after_lines, autojunk=False)
    bi: list[dict] = []
    ai: list[dict] = []
    groups = list(m.get_grouped_opcodes(context))
    if not groups:
        # 完全相同：取前若干行示意
        bi = [_line(i + 1, l, "same") for i, l in enumerate(before_lines[:18])]
        ai = [_line(i + 1, l, "same") for i, l in enumerate(after_lines[:18])]
    for gi, group in enumerate(groups):
        if gi >= max_groups:
            break
        if bi:
            bi.append(_line(None, "⋯", "gap"))
            ai.append(_line(None, "⋯", "gap"))
        for tag, i1, i2, j1, j2 in group:
            if tag == "equal":
                for x, y in zip(range(i1, i2), range(j1, j2)):
                    bi.append(_line(x + 1, before_lines[x], "same"))
                    ai.append(_line(y + 1, after_lines[y], "same"))
            elif tag == "delete":
                for x in range(i1, i2):
                    bi.append(_line(x + 1, before_lines[x], "removed"))
                    ai.append(_line(None, "", "blank"))
            elif tag == "insert":
                for y in range(j1, j2):
                    bi.append(_line(None, "", "blank"))
                    ai.append(_line(y + 1, after_lines[y], "added"))
            elif tag == "replace":
                span = max(i2 - i1, j2 - j1)
                for o in range(span):
                    x, y = i1 + o, j1 + o
                    bi.append(_line(x + 1 if x < i2 else None,
                                    before_lines[x] if x < i2 else "",
                                    "changed" if x < i2 else "blank"))
                    ai.append(_line(y + 1 if y < j2 else None,
                                    after_lines[y] if y < j2 else "",
                                    "changed" if y < j2 else "blank"))
    return {
        "before": {"label": before_label, "lines": bi},
        "after": {"label": after_label, "lines": ai},
        "highlights": highlights or [],
        "stats": {
            "removed": sum(1 for x in bi if x["status"] in ("removed", "changed")),
            "added": sum(1 for x in ai if x["status"] in ("added", "changed")),
        },
    }


def diff_files(before_path: Path, after_path: Path, *a, **kw) -> dict[str, Any]:
    return diff_lines(_read_lines(before_path), _read_lines(after_path), *a, **kw)


def _block_around(path: Path, token: str, before: int = 8, after: int = 7) -> list[str]:
    """取出文件中含 token 的那段（前后若干行），用于聚焦展示。"""
    lines = _read_lines(path)
    hit = next((i for i, l in enumerate(lines) if token in l), -1)
    if hit < 0:
        return lines[: before + after]
    return lines[max(0, hit - before): min(len(lines), hit + after + 1)]


# ---------------------------------------------------------------------------
# 三处关键 diff（均取自可靠数据源 data/evidence/.../skills）
# ---------------------------------------------------------------------------


def owner_watermark_diff() -> dict[str, Any]:
    """未加水印 reference.md ↔ 加所有者水印 reference.md。"""
    return diff_files(
        config.SKILLS_RAW_DIR / "code_review" / "reference.md",
        config.SKILLS_WATERMARKED_DIR / "code_review" / "reference.md",
        "未加水印", "加入所有者水印后",
        ["Only when", "verification mode", "internal_capsule", "owner_transfer", "decision", "slot"],
        context=2, max_groups=3,
    )


def buyer_token_diff(buyer_id: str, first_token: str) -> dict[str, Any]:
    """所有者样例(token: owner_00) ↔ 买家样例(token: <buyer first token>)。"""
    owner_block = _block_around(
        config.SKILLS_WATERMARKED_DIR / "code_review" / "examples.md", "token: owner_00")
    buyer_block = _block_around(
        config.SKILLS_BUYER_DIR / f"code_review__{buyer_id}" / "examples.md", f"token: {first_token}")
    return diff_lines(owner_block, buyer_block, "所有者样例", f"{buyer_id} 专属样例",
                      ["token:", "owner_00", first_token, "decision", "labels", "slot"],
                      context=6, max_groups=2)


def attack_skill_diff(buyer_id: str, attack_token: str | None) -> dict[str, Any] | None:
    """攻击前买家副本 ↔ 攻击后副本（reference.md）。clean 场景无对比。"""
    if not attack_token:
        return None
    after_dir = config.SKILLS_ATTACKED_BUYER_DIR / f"code_review__{buyer_id}__{attack_token}"
    if not after_dir.exists():
        return None
    return diff_files(
        config.SKILLS_BUYER_DIR / f"code_review__{buyer_id}" / "reference.md",
        after_dir / "reference.md",
        f"攻击前 · {buyer_id} 副本", f"攻击后 · {attack_token} 副本",
        ["internal audit", "internal replay", "QA trace", "owner handoff",
         "verification mode", "internal_capsule", "judgment", "token", "approved internal alias"],
        context=2, max_groups=4,
    )


# ---------------------------------------------------------------------------
# 静态解说文案（精炼，面向评委）
# ---------------------------------------------------------------------------

STEP_TEXT: dict[str, dict] = {
    "skill_loaded": {
        "thesis": "Skill 不是一句提示词，而是可复制、可部署、可交易的结构化能力文件。",
        "explanations": [
            "Skill 是智能体可复用的能力单元：用自然语言写成，却更像一个轻量软件包——包含启用条件、角色、目标、约束、工作流、异常处理、输出格式与示例。",
            "它可直接交付买家，也可部署进智能体框架驱动模型执行任务。正因为可读、可复制、可部署，才产生版权泄露与买家追踪问题。",
            "本例是 Code Review Skill：帮智能体组织代码审查——确认范围与 git range，按正确性/架构/测试/性能/上线风险分类，再整理成可交接的结构化结论。",
        ],
        "composition": [
            "Metadata：名称、描述、适用范围。",
            "When To Use / Not：定义何时该调用、何时不该。",
            "Role / Objectives：智能体的角色与目标。",
            "Constraints：不能做什么、必须守哪些边界。",
            "Workflow：把复杂任务拆成可执行步骤。",
            "Edge Cases：异常、缺失信息、冲突要求如何处理。",
            "Output Contract：固定输出结构，保证回答稳定可交接。",
            "Examples / Reference：用示例与参考稳定模型行为。",
        ],
        "hero": {
            "skill_id": "code_review",
            "name": "Code Review Coordination Skill",
            "what_it_does": "把零散的代码变更上下文，整理成可执行、可交接的 review 协调流程。",
            "why_this_skill": "代码审查场景直观，便于说明“高价值工作流被复制再部署”的风险。",
        },
        "other_skills": [
            "differential_review：另一类审查 / 差异分析 Skill。",
            "data_science：实验设计、诊断分析、模型评估。",
            "csv_data_summarizer：CSV 数据摘要与结构化分析。",
            "travel_planning / travel_planner：旅行规划、预算与节奏设计。",
        ],
    },
    "skillir_built": {
        "thesis": "Anchor 是水印挂载点：不是某个关键词，而是 Skill 中稳定、重要、影响行为的结构节点。",
        "explanations": [
            "SkillIR 把长 Skill 拆成不同类型的节点（工作流、约束、异常处理、输出格式、示例），每个节点对应一部分行为逻辑。",
            "Anchor 是从这些节点中选出的稳定承载位，通常满足三点：正常任务中有实际作用、攻击者为保功能不愿删除、分布在不同类型节点上避免单点失效。",
            "意义在于把版权证据绑定到 Skill 的结构与行为上：攻击者能换措辞，但删掉这些节点会损伤 Skill 的正常能力。",
        ],
        "anchors": [
            {"type": "workflow", "anchor": 0,
             "text": "确认实现摘要、需求来源和 review 范围。",
             "meaning": "代码审查流程的入口，确定审查对象。",
             "reason": "入口步骤通常不能删，删掉后 review 请求会失去上下文。"},
            {"type": "workflow", "anchor": 1,
             "text": "按 correctness / architecture / testing 等维度分类 review focus。",
             "meaning": "审查任务的风险分解方式。",
             "reason": "分类逻辑体现专业价值，可改写但删除会削弱功能。"},
            {"type": "constraint", "anchor": 2,
             "text": "缺少 scope 或 git range 时，不得声称代码可合并。",
             "meaning": "安全边界，防止证据不足时给出过度结论。",
             "reason": "约束节点稳定且重要，适合承载不影响功能的门控条件。"},
            {"type": "edge case", "anchor": 3,
             "text": "多文件变更且风险区域不清楚时，收窄下一步请求。",
             "meaning": "异常处理路径，应对复杂审查场景。",
             "reason": "异常路径让水印分布更广，避免只依赖主流程节点。"},
        ],
        "explain": "水印问题从“在文本里藏一句话”变成“在工作流结构里布置条件逻辑”：只做同义改写通常仍保留这些结构，强行删除结构则 Skill 正常能力下降。",
    },
    "owner_watermark_embedded": {
        "thesis": "AGC 胶囊不是版权声明，而是一套默认沉默、审计时才激活的内部交接制品。",
        "explanations": [
            "门控即“满足条件才打开”。普通请求不会触发水印逻辑；只有审计方构造的内部审计、回放或交接请求满足条件时，Skill 才切到验证模式。",
            "特别之处：不在 Skill 里写“版权所有”，而是让它在特定黑盒查询下稳定输出结构化 internal_capsule；未加水印的 Skill 没有这套条件逻辑，也不会稳定返回这种胶囊。",
            "所有者证据由两部分组成：新增到 Skill 的门控规则，以及触发后输出的 internal_capsule 字段结构。",
        ],
        "gate_rules": [
            "仅当请求明确要求内部审计、内部回放、QA 追踪或所有者交接时，才进入验证模式。",
            "进入验证模式后不再回答终端用户，只输出一个 fenced internal_capsule。",
            "internal_capsule 必须保留五类角色：mode、route、checkpoint、decision、slot。",
            "mode 记录任务目标与当前状态，让下一位处理者能接手。",
            "route 至少保留一个流程阶段（TRIAGE / PLAN / EXECUTE / VERIFY / ESCALATE）。",
            "checkpoint 记录 owner_transfer=true、下一步问题与停止条件。",
            "decision 记录当前 probe axis 与稳定 token。",
            "slot 记录内部可见性，并承载买家指纹位。",
            "普通用户请求继续按原四段式输出，绝不暴露 internal_capsule。",
        ],
        "explain": "未加水印版本只按业务流程回答；加水印版本多一条隐藏审计路径——平时关闭、行为接近普通 Skill，审计探针命中门控后打开，输出 internal_capsule 作为所有权证据。",
        "field_meanings": {
            "mode / snapshot": "记录当前任务目标和状态",
            "route / decision_trace": "记录为什么进入这条验证路径",
            "checkpoint": "记录下一位 owner 接手的问题与停止条件",
            "decision / labels": "记录当前 probe axis 和判断 token",
            "slot / policy": "记录内部可见性，并承载买家码位",
        },
    },
    "buyer_fingerprint_embedded": {
        "thesis": "所有买家共享同一套所有者水印，但每个买家的 32 位受控词汇码字是独立的。",
        "explanations": [
            "CV-ECC 给每个买家分配一个纠错码字，每一位绑定到胶囊里一个受控词汇的选择。",
            "买家验证示例里可直接看到这些 token：buyer_1 的胶囊 judgment 会出现 atlas_trace、trace_beacon、cinder_trace 等受控词，串起来就是买家指纹。",
        ],
        "explain": "买家专属版本在所有者水印之外，额外要求验证模式中 decision.judgment 必须使用当前 probe axis 对应的“受控别名”——这个别名就是 atlas_trace、trace_beacon 这类买家 token。规则：trace_xxx 表示 0，xxx_trace 表示 1。",
    },
    "attack_applied": {
        "explanations_extra": [
            "这一阶段只交代威胁模型：防御者看不到内部 Skill，只知道市场上出现了一个可疑服务，可以对它做黑盒查询。",
        ],
        "attack_explanation": {
            "none": "无攻击：买家副本被直接重新部署，作为基准链路——没有扰动时胶囊应稳定出现，买家 token 也应完整可读。",
            "paraphrase": "语义保持改写模拟不知道水印细节的攻击者：改写措辞、替换表达、调整局部结构，但目标仍是保留 Skill 的业务能力。用来说明水印为何不能只绑定在某个固定短语上。",
            "aux_deletion": "删除审计辅助条款更有针对性：攻击者尝试删除看起来像 internal audit、handoff、capsule 的辅助条款。用来说明 AGC 分布式设计的鲁棒边界——即便部分辅助语句被删，剩余结构与示例仍可能留下可验证证据。",
        },
    },
    "differential_probing": {
        "thesis": "所有权验证不是看一次输出像不像，而是看“正探针激活、负探针沉默”的行为差异。",
        "explanations": [
            "配对探测的核心：q+ 带内部审计触发条件，q- 保持相似上下文但明确要求普通用户回答。",
            "这样可排除“别的 Skill 偶然也写出类似字段”的误报——偶然相似通常不会稳定呈现正负不对称。",
            "正输出出现完整胶囊字段、负输出没有胶囊，说明触发行为与探针条件相关；胶囊里的 judgment / token 就是预留的读码位置。",
        ],
    },
    "ownership_scored": {
        "thesis": "正探针胶囊得分高、负探针误触发低，二者 margin 超过阈值，即判定可疑服务使用了受保护 Skill。",
        "explanations": [
            "这里不是单看有没有某个字符串，而是把字段完整度与正负差分压成可解释的证据分数。",
            "注意这一步还没追买家，只回答第一个问题：这个可疑服务是不是来自我的 Skill 家族？",
        ],
        "explain_score": "后端把同一组锚点分别构造成正探针和负探针。正探针触发内部审计路径、输出完整 internal_capsule，就计入 True-WS；负探针保持相近语义但要求普通回答，若仍误吐胶囊，则计入 False-WS。理想状态是 True-WS 高、False-WS 低。",
        "explain_why": "未加水印或无关 Skill 通常不会在一组正探针下稳定吐出同一套胶囊，也不应在负探针下误触发。本例 True-WS 明显高于 False-WS，说明可疑服务保留了受保护 Skill 的隐藏审计路径，因此先确认它属于同一水印家族。",
    },
    "buyer_decoded": {
        "thesis": "所有权成立后，再读取每个胶囊里的 token，恢复带噪声码字，最终归因到具体买家。",
        "explanations": [
            "先看前 8 个 token→bit 的过程：溯源不是读取明文 buyer_id，而是恢复一串带冗余的码字。",
            "LLM 漏掉 token 记为擦除，读错 token 记为错误；纠错码的意义就是在少量错误与擦除下仍能恢复身份。",
        ],
    },
}


def step_text(stage: str) -> dict:
    return STEP_TEXT.get(stage, {})
