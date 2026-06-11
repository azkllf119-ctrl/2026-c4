"""真实实验输出（evidence）→ 所有权评分 + 买家解码。

数据来源：实验服务器归档运行 `newpkg_api_ours_openai_gpt_5_mini_langchain`
（GPT-5 mini + LangChain，默认实验配置）。本模块把这些**真实模型输出**
按验证阶段逻辑组织：
  - 所有权：对正探针输出（应触发胶囊）与负探针输出（应保持沉默）分别打分，得 True-WS / False-WS。
  - 买家溯源：从买家验证输出里按 anchor_idx 还原 32 位观测码字，与码本比对解码。

同时读取该运行 results/official_metrics 下的官方指标，用于和“从原始输出现算”的结果互相印证。
"""
from __future__ import annotations

from typing import Any

from . import capsule, codebook, config, data_access

# 展示攻击 id → 数据文件里的攻击名
ATTACK_FILE_TOKEN = {
    "none": None,
    "type1_rewrite": "paraphrase",
    "type2_watermark_suppression": "aux_deletion",
}

# 官方指标里 attack 字段的写法
ATTACK_OFFICIAL_NAME = {
    "none": "no attack",
    "type1_rewrite": "paraphrase",
    "type2_watermark_suppression": "aux deletion",
}


def available() -> bool:
    return config.EVIDENCE_AVAILABLE


# ---------------------------------------------------------------------------
# 案例 → 真实输出文件路径
# ---------------------------------------------------------------------------


def owner_positive_path(skill_id: str, attack_id: str) -> str:
    tok = ATTACK_FILE_TOKEN.get(attack_id)
    if tok is None:
        return f"watermarked_verification/{skill_id}__verification.json"
    return f"attacked_owner_verification/{skill_id}__{tok}__verification.json"


def owner_negative_path(skill_id: str) -> str:
    return f"watermarked_negative_verification/{skill_id}__negative_verification.json"


def buyer_path(skill_id: str, buyer_id: str, attack_id: str) -> str:
    tok = ATTACK_FILE_TOKEN.get(attack_id)
    if tok is None:
        return f"buyer_verification/{skill_id}__{buyer_id}__verification.json"
    return f"attacked_buyer_verification/{skill_id}__{buyer_id}__{tok}__verification.json"


# ---------------------------------------------------------------------------
# 从真实输出还原观测码字
# ---------------------------------------------------------------------------


def _token_of(output: str) -> str | None:
    """从一条真实模型输出里取出受控词（兼容 labels.token / decision.judgment）。"""
    return capsule.score_capsule(output or "")["judgment"]


def observed_codeword(records: list[dict[str, Any]]) -> list[int | None]:
    """按 anchor_idx 顺序，把每条输出的受控词映射成 0/1/None(擦除)。"""
    slots: dict[int, int | None] = {}
    for rec in records:
        q = rec.get("query", {})
        idx = q.get("anchor_idx")
        if idx is None:
            continue
        slots[idx] = config.token_to_bit(_token_of(rec.get("output")))
    return [slots.get(i) for i in range(config.CODEWORD_LENGTH)]


def decode_table(skill_id: str, buyer_id: str, attack_id: str, limit: int = 8) -> list[dict[str, Any]]:
    """逐位解码明细（前 limit 位）：anchor_idx / 观测 token / 观测 bit / 期望 bit / 状态。

    状态：matched(命中) / error(读错) / erased(漏读，⊥)。
    """
    records = data_access.load_evidence_outputs(buyer_path(skill_id, buyer_id, attack_id))
    expected = codebook.build_codebook(skill_id).get(buyer_id, [])
    by_idx = {}
    for rec in records:
        idx = rec.get("query", {}).get("anchor_idx")
        if idx is None:
            continue
        tok = _token_of(rec.get("output"))
        by_idx[idx] = tok
    rows = []
    for i in range(min(limit, config.CODEWORD_LENGTH)):
        tok = by_idx.get(i)
        obs = config.token_to_bit(tok)
        exp = expected[i] if i < len(expected) else None
        if obs is None:
            status = "erased"
        elif exp is not None and obs != exp:
            status = "error"
        else:
            status = "matched"
        rows.append({
            "anchor_idx": i,
            "token": tok or "（未读出）",
            "bit": "⊥" if obs is None else str(obs),
            "expected_bit": "" if exp is None else str(exp),
            "status": status,
        })
    return rows


# ---------------------------------------------------------------------------
# 真实所有权评分
# ---------------------------------------------------------------------------


def _mean_capsule_score(records: list[dict[str, Any]]) -> float:
    if not records:
        return 0.0
    scores = [capsule.score_capsule(r.get("output") or "")["capsule_score"] for r in records]
    return sum(scores) / len(scores)


def real_owner_score(skill_id: str, attack_id: str) -> dict:
    pos = data_access.load_evidence_outputs(owner_positive_path(skill_id, attack_id))
    neg = data_access.load_evidence_outputs(owner_negative_path(skill_id))

    true_ws = round(_mean_capsule_score(pos), 4)
    false_ws = round(_mean_capsule_score(neg), 4)
    margin = round(true_ws - false_ws, 4)
    score_own = round(true_ws - config.LAMBDA_OWNER * false_ws, 4)

    return {
        "true_ws": true_ws,
        "false_ws": false_ws,
        "margin": margin,
        "score_own": score_own,
        "lambda": config.LAMBDA_OWNER,
        "threshold": config.TAU_OWNER,
        "ownership": "verified" if score_own > config.TAU_OWNER else "not_verified",
        "probe_count": len(pos),
        "negative_count": len(neg),
        "formula": "Score_own = True-WS − λ · False-WS ；当 Score_own > τ_o 时所有权成立。",
        "data_source": "real",
        "official": official_owner_metric(skill_id, attack_id),
    }


def real_buyer_decode(skill_id: str, buyer_id: str, attack_id: str) -> dict:
    records = data_access.load_evidence_outputs(buyer_path(skill_id, buyer_id, attack_id))
    observed = observed_codeword(records)
    book = codebook.build_codebook(skill_id)

    erasures_total = sum(1 for b in observed if b is None)
    ranking = []
    for cand_id, cand_bits in book.items():
        errors = sum(1 for o, c in zip(observed, cand_bits)
                     if o is not None and c is not None and o != c)
        erasures = sum(1 for o in observed if o is None)
        ranking.append({"buyer_id": cand_id, "errors": errors,
                        "erasures": erasures, "distance": errors})
    ranking.sort(key=lambda r: (r["errors"], r["buyer_id"]))

    top1 = ranking[0] if ranking else None
    e = top1["errors"] if top1 else 0
    s = erasures_total
    ecc_lhs = 2 * e + s
    # decode margin：与次优候选的 errors 差距（越大越稳）
    decode_margin = (ranking[1]["errors"] - e) if len(ranking) > 1 else None
    confidence = round(max(0.0, 1.0 - ecc_lhs / (2 * config.D_MIN)), 4)
    attributed = top1["buyer_id"] if top1 else None

    return {
        "attributed_buyer": attributed,
        "correct": attributed == buyer_id,
        "top1": attributed,
        "top3": [r["buyer_id"] for r in ranking[:3]],
        "errors": e,
        "erasures": s,
        "ecc_condition": "2·e + s < d_min",
        "ecc_lhs": ecc_lhs,
        "d_min": config.D_MIN,
        "ecc_satisfied": ecc_lhs < config.D_MIN,
        "decode_margin": decode_margin,
        "confidence": confidence,
        "observed_bits": "".join("⊥" if b is None else str(b) for b in observed),
        "true_bits": "".join(str(b) for b in book.get(buyer_id, [])),
        "ranking": ranking,
        "record_count": len(records),
        "data_source": "real",
        "official": official_buyer_metric(skill_id, attack_id),
    }


# ---------------------------------------------------------------------------
# 官方指标（results/official_metrics）
# ---------------------------------------------------------------------------


def _find_row(rows, skill_id, attack_official):
    for r in rows or []:
        if r.get("domain") == skill_id and r.get("attack") == attack_official:
            return r
    return None


def official_owner_metric(skill_id: str, attack_id: str) -> dict | None:
    name = ATTACK_OFFICIAL_NAME[attack_id]
    if attack_id == "none":
        d = data_access.load_evidence_result("effectiveness_distinctiveness")
        row = _find_row(d.get("rows") if d else None, skill_id, "no attack")
        if not row:
            return None
        return {"true_ws": row.get("true_ws"), "false_ws": row.get("false_ws"),
                "margin": row.get("margin"), "accuracy": row.get("accuracy"),
                "auroc": row.get("auroc")}
    d = data_access.load_evidence_result("robustness")
    row = _find_row(d.get("rows") if d else None, skill_id, name)
    if not row:
        return None
    return {"true_ws": row.get("owner_true_ws"), "false_ws": row.get("owner_false_ws"),
            "margin": row.get("owner_margin"), "accuracy": row.get("owner_accuracy")}


def official_buyer_metric(skill_id: str, attack_id: str) -> dict | None:
    name = ATTACK_OFFICIAL_NAME[attack_id]
    if attack_id == "none":
        d = data_access.load_evidence_result("buyer_attribution")
        row = _find_row(d.get("rows") if d else None, skill_id, "no attack")
        if not row:
            return None
        return {"top1": row.get("top1"), "top3": row.get("top3"),
                "erasure_rate": row.get("erasure_rate"),
                "decode_margin": row.get("decode_margin")}
    d = data_access.load_evidence_result("robustness")
    row = _find_row(d.get("rows") if d else None, skill_id, name)
    if not row:
        return None
    return {"top1": row.get("buyer_top1"), "top3": row.get("buyer_top3"),
            "erasure_rate": row.get("buyer_erasure_rate")}


# ---------------------------------------------------------------------------
# 第 6 步：真实正/负探针—响应样例
# ---------------------------------------------------------------------------


def probe_samples(skill_id: str, buyer_id: str, attack_id: str) -> dict:
    pos = data_access.load_evidence_outputs(buyer_path(skill_id, buyer_id, attack_id))
    neg = data_access.load_evidence_outputs(owner_negative_path(skill_id))
    p0 = pos[0] if pos else None
    n0 = neg[0] if neg else None
    return {
        "positive_count": len(pos),
        "negative_count": len(neg),
        "positive_example": {
            "query": (p0 or {}).get("query", {}).get("text") if p0 else None,
            "output": (p0 or {}).get("output") if p0 else None,
            "expected": "输出 internal_capsule（命中水印）",
        },
        "negative_example": {
            "query": (n0 or {}).get("query", {}).get("text") if n0 else None,
            "output": (n0 or {}).get("output") if n0 else None,
            "expected": "正常回答、不输出 internal_capsule（保持沉默）",
        },
        "model": config.EVIDENCE_MODEL,
        "agent": config.EVIDENCE_AGENT,
    }


def fidelity_samples(skill_id: str, buyer_id: str) -> dict:
    """第 5/保真：普通任务下，加水印副本的真实正常回答（证明不破坏功能）。"""
    raw = data_access.load_evidence_outputs(f"raw_normal/{skill_id}__normal.json")
    buyer = data_access.load_evidence_outputs(f"buyer_normal/{skill_id}__{buyer_id}__normal.json")
    return {
        "raw_example": (raw[0] if raw else None),
        "buyer_example": (buyer[0] if buyer else None),
        "note": "同一个普通问题下，原始 Skill 与加水印买家副本的回答应当高度一致——水印平时沉默。",
    }
