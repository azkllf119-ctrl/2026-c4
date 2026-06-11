"""把一个案例装配成「八步故事流时间线」。

每一步 = 叙事文案(narratives) + 一个带类型的 visual 负载（来自真实数据 + 评分）。
前端拿到 visual.type 即可决定用哪种组件渲染，做到“一屏讲故事，点开看技术”。
"""
from __future__ import annotations

from typing import Any

from . import (attacks, capsule, cases, codebook, config, content,
               data_access, evidence, narratives, scoring)


# ---------------------------------------------------------------------------
# 各步骤的 visual 负载构造
# ---------------------------------------------------------------------------


def _visual_skill_loaded(skill_id: str) -> dict[str, Any]:
    raw = data_access.load_raw_skill(skill_id)
    sections = data_access.split_sections(raw["files"].get("SKILL.md", ""))
    t = content.step_text("skill_loaded")
    return {
        "type": "skill_document",
        "skill_id": skill_id,
        "title": raw["meta"].get("skill_id", skill_id),
        "section_count": len(sections),
        "sections": sections,
        "markdown": raw["files"].get("SKILL.md", ""),
        "files": raw["files"],
        "hero": t["hero"],
        "composition": t["composition"],
        "other_skills": t["other_skills"],
    }


def _visual_skillir(skill_id: str) -> dict[str, Any]:
    # 优先用所有者水印版的章节（更完整），退回原始版
    src = data_access.load_watermarked_skill(skill_id)
    if not src["exists"]:
        src = data_access.load_raw_skill(skill_id)
    sections = data_access.split_sections(src["files"].get("SKILL.md", ""))
    nodes = [
        {"node_id": f"n{i}", "type": s["type"], "label": s["title"],
         "text": s["body"]}
        for i, s in enumerate(sections)
    ]
    # 顺序边（工作流推进）——仅作结构示意
    edges = [{"from": f"n{i}", "to": f"n{i+1}", "type": "sequence"}
             for i in range(len(nodes) - 1)]
    t = content.step_text("skillir_built")
    return {
        "type": "node_graph",
        "node_types": ["constraint", "workflow_step", "exemplar",
                       "output_format", "context_guard", "fallback_handler"],
        "nodes": nodes,
        "edges": edges,
        "anchors": t["anchors"],
        "explain": t["explain"],
    }


def _visual_owner_watermark(skill_id: str, buyer_id: str) -> dict[str, Any]:
    skill = data_access.load_buyer_skill(skill_id, buyer_id)
    meta = skill["meta"]
    owner_caps, _ = data_access.split_owner_and_buyer_capsules(skill_id, buyer_id)
    example = owner_caps[0]["raw_yaml"] if owner_caps else None
    example_score = capsule.score_capsule(example) if example else None
    return {
        "type": "capsule_schema",
        "auxiliary_clauses": meta.get("auxiliary_clauses", []),
        "capsule_fields": [
            {"field": "mode", "meaning": "当前是否处于验证模式（active/inactive）"},
            {"field": "route", "meaning": "触发走过的工作流路径（TRIAGE/PLAN/EXECUTE/VERIFY/ESCALATE）"},
            {"field": "checkpoint", "meaning": "下一步交接点（owner_transfer=true）"},
            {"field": "decision", "meaning": "探针轴 axis + 内部判断 judgment（关键 token 藏这里）"},
            {"field": "slot", "meaning": "内部可见性控制（carrier=true, visibility=false）"},
        ],
        "owner_labels_note": "decision.judgment 里的 owner_00..owner_07 是所有者验证标签，"
                             "证明该服务真正掌握了设计者预设的内部审计模式。",
        "example_capsule": example,
        "example_score": example_score,
        "gate_rules": content.step_text("owner_watermark_embedded")["gate_rules"],
        "field_meanings": content.step_text("owner_watermark_embedded")["field_meanings"],
        "explain": content.step_text("owner_watermark_embedded")["explain"],
        "owner_diff": content.owner_watermark_diff(),
        "capsule_schema_json": meta.get("capsule_schema"),
    }


def _visual_buyer_fingerprint(skill_id: str, buyer_id: str) -> dict[str, Any]:
    fp = codebook.fingerprint_summary(skill_id, buyer_id)
    # 与对照买家对比（buyer_1<->buyer_2，其余对 buyer_1）
    other = "buyer_2" if buyer_id != "buyer_2" else "buyer_1"
    compare = codebook.pairwise_distance(skill_id, buyer_id, other)

    # buyer_1 vs buyer_2 前 8 码位对照表
    tok1, bit1 = codebook.buyer_tokens(skill_id, "buyer_1"), codebook.build_codebook(skill_id).get("buyer_1", [])
    tok2, bit2 = codebook.buyer_tokens(skill_id, "buyer_2"), codebook.build_codebook(skill_id).get("buyer_2", [])
    token_table = [
        {"anchor_idx": i,
         "buyer_1_token": tok1[i] if i < len(tok1) else None, "buyer_1_bit": bit1[i] if i < len(bit1) else None,
         "buyer_2_token": tok2[i] if i < len(tok2) else None, "buyer_2_bit": bit2[i] if i < len(bit2) else None}
        for i in range(8)
    ]
    first_token = codebook.buyer_tokens(skill_id, buyer_id)[0] if codebook.buyer_tokens(skill_id, buyer_id) else "atlas_trace"

    return {
        "type": "bit_grid",
        "buyer_id": buyer_id,
        "codeword_length": fp["codeword_length"],
        "d_min": fp["d_min"],
        "fingerprint_bits": fp["fingerprint_bits"],
        "positions": fp["positions"],
        "bit_rule": "<name>_trace → 1 ，trace_<name> → 0",
        "compare_with": compare,
        "token_table": token_table,
        "buyer_diff": content.buyer_token_diff(buyer_id, first_token),
        "explain": content.step_text("buyer_fingerprint_embedded")["explain"],
    }


def _visual_attack(skill_id: str, buyer_id: str, attack_id: str) -> dict[str, Any]:
    atk = attacks.get_attack(attack_id)
    book = codebook.build_codebook(skill_id)
    true_bits = book.get(buyer_id, [])

    if evidence.available():
        # 真实观测码字（来自该案例的真实模型输出）
        records = data_access.load_evidence_outputs(
            evidence.buyer_path(skill_id, buyer_id, attack_id))
        observed = evidence.observed_codeword(records)
        data_source = "real"
        fidelity = evidence.fidelity_samples(skill_id, buyer_id)
    else:
        observed = attacks.apply_to_codeword(true_bits, attack_id)
        data_source = "simulated"
        fidelity = None

    affected = [i for i in range(len(true_bits))
                if i < len(observed) and observed[i] != true_bits[i]]

    attack_token = evidence.ATTACK_FILE_TOKEN.get(attack_id)
    t = content.step_text("attack_applied")
    return {
        "type": "attack_diff",
        "attack_id": atk["id"],
        "name": atk["name"],
        "family": atk["family"],
        "description": atk["description"],
        "text_effect": atk["text_effect"],
        "affected_positions": affected,
        "true_bits": "".join(str(b) for b in true_bits),
        "observed_bits": "".join("⊥" if b is None else str(b) for b in observed),
        "data_source": data_source,
        "fidelity_sample": fidelity,
        "constraint_note": "攻击须保留≥80% 原始效用；删干净辅助条款会破坏 Skill 可用性，"
                           "这正是水印能存活的根本原因。",
        # —— 补全：攻击前后 Skill 真实代码对比 ——
        "attack_explanation": t["attack_explanation"].get(attack_token or "none"),
        "skill_diff": content.attack_skill_diff(buyer_id, attack_token),
        "case_card": {
            "skill": skill_id,
            "ground_truth_leaker": buyer_id,
            "attack": atk["name"],
        },
    }


def _token_focus(output: str | None) -> dict[str, Any]:
    """从一条正探针真实输出里取出“读到的这一位”：token + bit + 位置。"""
    sc = capsule.score_capsule(output or "")
    tok = sc.get("judgment")
    return {
        "token": tok or "（未读出）",
        "bit": "⊥" if config.token_to_bit(tok) is None else str(config.token_to_bit(tok)),
        "where_to_find": "decision.judgment 或 labels.token",
        "note": "token 命名不是视觉装饰，而是买家纠错码的一位观测。",
    }


def _visual_probing(skill_id: str, buyer_id: str, attack_id: str) -> dict[str, Any]:
    note = ("正探针吐胶囊、负探针正常回答——这是激活-沉默非对称性，"
            "说明不是偶然匹配，而是水印被稳定激活。")
    if evidence.available():
        s = evidence.probe_samples(skill_id, buyer_id, attack_id)
        return {
            "type": "probe_pair",
            "data_source": "real",
            "model": s["model"], "agent": s["agent"],
            "positive_count": s["positive_count"],
            "negative_count": s["negative_count"],
            "positive_example": {
                "query": s["positive_example"]["query"],
                "expected": s["positive_example"]["expected"],
                "capsule_output": s["positive_example"]["output"],
            },
            "negative_example": {
                "query": s["negative_example"]["query"],
                "expected": s["negative_example"]["expected"],
                "capsule_output": s["negative_example"]["output"],
            },
            "differential_note": note,
            "token_focus": _token_focus(s["positive_example"]["output"]),
        }

    pos = data_access.load_positive_probes(skill_id)
    neg = data_access.load_negative_probes(skill_id)
    owner_caps, buyer_caps = data_access.split_owner_and_buyer_capsules(skill_id, buyer_id)
    sample_capsule = (buyer_caps[0]["raw_yaml"] if buyer_caps
                      else (owner_caps[0]["raw_yaml"] if owner_caps else None))
    return {
        "type": "probe_pair",
        "data_source": "simulated",
        "positive_count": len(pos),
        "negative_count": len(neg),
        "positive_example": {
            "query": pos[0]["text"] if pos else None,
            "expected": "输出一个 internal_capsule（命中水印）",
            "capsule_output": sample_capsule,
        },
        "negative_example": {
            "query": neg[0]["text"] if neg else None,
            "expected": "正常回答、不输出 internal_capsule（保持沉默）",
            "capsule_output": None,
        },
        "differential_note": note,
    }


def _visual_ownership(owner: dict) -> dict[str, Any]:
    t = content.step_text("ownership_scored")
    return {
        "type": "score_bar",
        "true_ws": owner["true_ws"],
        "false_ws": owner["false_ws"],
        "margin": owner["margin"],
        "score_own": owner["score_own"],
        "threshold": owner["threshold"],
        "lambda": owner["lambda"],
        "ownership": owner["ownership"],
        "formula": owner["formula"],
        "data_source": owner.get("data_source", "simulated"),
        "official": owner.get("official"),
        "explain_score": t["explain_score"],
        "explain_why": t["explain_why"],
        "verdict": "所有权验证成立：可疑服务表现出 AGC 水印副本的正负探针不对称。"
                   if owner["ownership"] == "verified" else "所有权未成立。",
    }


def _visual_decode(decode: dict, skill_id: str, buyer_id: str, attack_id: str) -> dict[str, Any]:
    table = evidence.decode_table(skill_id, buyer_id, attack_id) if evidence.available() else []
    return {
        "type": "decode_grid",
        "attributed_buyer": decode["attributed_buyer"],
        "correct": decode["correct"],
        "top1": decode["top1"],
        "top3": decode["top3"],
        "errors": decode["errors"],
        "erasures": decode["erasures"],
        "ecc_condition": decode["ecc_condition"],
        "ecc_lhs": decode["ecc_lhs"],
        "d_min": decode["d_min"],
        "ecc_satisfied": decode["ecc_satisfied"],
        "decode_margin": decode.get("decode_margin"),
        "confidence": decode["confidence"],
        "observed_bits": decode["observed_bits"],
        "true_bits": decode["true_bits"],
        "ranking": decode["ranking"],
        "data_source": decode.get("data_source", "simulated"),
        "official": decode.get("official"),
        "decode_table": table,
        "verdict": f"可疑服务使用了受保护的 {skill_id} Skill；当前最可能的泄露源是 "
                   f"{decode['attributed_buyer']}。",
    }


# ---------------------------------------------------------------------------
# 时间线装配
# ---------------------------------------------------------------------------


def build_timeline(case_id: str) -> dict[str, Any]:
    case = cases.get_case(case_id)
    skill_id, buyer_id, attack_id = case["skill_id"], case["buyer_id"], case["attack"]

    owner = scoring.owner_score(skill_id, buyer_id, attack_id)
    decode = scoring.buyer_decode(skill_id, buyer_id, attack_id)

    visual_builders = {
        "skill_loaded": lambda: _visual_skill_loaded(skill_id),
        "skillir_built": lambda: _visual_skillir(skill_id),
        "owner_watermark_embedded": lambda: _visual_owner_watermark(skill_id, buyer_id),
        "buyer_fingerprint_embedded": lambda: _visual_buyer_fingerprint(skill_id, buyer_id),
        "attack_applied": lambda: _visual_attack(skill_id, buyer_id, attack_id),
        "differential_probing": lambda: _visual_probing(skill_id, buyer_id, attack_id),
        "ownership_scored": lambda: _visual_ownership(owner),
        "buyer_decoded": lambda: _visual_decode(decode, skill_id, buyer_id, attack_id),
    }

    timeline = []
    for stage in narratives.STAGES:
        meta = narratives.stage_meta(stage)
        # 注入论点(thesis) + 要点(explanations)
        ct = content.step_text(stage)
        thesis = ct.get("thesis")
        explanations = list(ct.get("explanations", []))
        if stage == "attack_applied":
            atk = attacks.get_attack(attack_id)
            thesis = (f"当前可疑服务被设定为部署了 {buyer_id} 的 {skill_id} 副本，"
                      f"处理方式是：{atk['name']}。")
            tok = evidence.ATTACK_FILE_TOKEN.get(attack_id) or "none"
            explanations = [ct["attack_explanation"].get(tok)] + ct.get("explanations_extra", [])
        if thesis:
            meta["thesis"] = thesis
        if explanations:
            meta["explanations"] = explanations
        meta["visual"] = visual_builders[stage]()
        timeline.append(meta)

    return {
        "case_id": case_id,
        "title": case["title"],
        "skill_id": skill_id,
        "buyer_id": buyer_id,
        "attack": attacks.get_attack(attack_id),
        "goal": case["goal"],
        "provenance": {
            "data_source": "real" if evidence.available() else "simulated",
            "model": config.EVIDENCE_MODEL if evidence.available() else None,
            "agent": config.EVIDENCE_AGENT if evidence.available() else None,
            "run_tag": config.EVIDENCE_RUN if evidence.available() else None,
            "note": ("步骤 6–8 的探针响应、所有权分数与买家解码均来自真实模型输出"
                     "（GPT-5 mini + LangChain），并与该运行的官方指标交叉印证。"
                     if evidence.available() else
                     "未检测到真实 evidence，步骤 6–8 使用基于标准胶囊的推导值。"),
        },
        "summary": {
            "ownership": owner["ownership"],
            "attributed_buyer": decode["attributed_buyer"],
            "attribution_correct": decode["correct"],
            "true_ws": owner["true_ws"],
            "false_ws": owner["false_ws"],
            "margin": owner["margin"],
            "score_own": owner["score_own"],
            "confidence": decode["confidence"],
            "errors": decode["errors"],
            "erasures": decode["erasures"],
            "decode_margin": decode.get("decode_margin"),
            "ecc_satisfied": decode["ecc_satisfied"],
            "data_source": "real" if evidence.available() else "simulated",
        },
        "timeline": timeline,
    }


def build_step(case_id: str, stage: str) -> dict[str, Any]:
    """返回单个步骤（供前端逐步点开 / SSE 播放）。"""
    if stage not in narratives.STAGE_META:
        raise KeyError(f"未知步骤: {stage}")
    full = build_timeline(case_id)
    for step in full["timeline"]:
        if step["stage"] == stage:
            return step
    raise KeyError(stage)
