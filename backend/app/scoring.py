"""所有权评分 + 买家纠错解码。

对应方法与源码报告 verification_eval.py / ecc.py：
  - 所有权：比较正探针与负探针的胶囊得分差，得到 True-WS / False-WS / Margin / Score_own。
  - 买家溯源：把观测码字与每个买家的标准码字比对，按 errors 升序排出 top1/top3，
    并检查纠错条件 2·errors + erasures < d_min。
"""
from __future__ import annotations

from . import attacks, capsule, codebook, config, data_access, evidence


# ---------------------------------------------------------------------------
# 所有权评分
# ---------------------------------------------------------------------------


def owner_score(skill_id: str, buyer_id: str, attack_id: str) -> dict:
    """计算所有权验证分数。

    优先使用真实实验输出（evidence）：对真实正探针/负探针输出逐条打分得 True-WS/False-WS。
    若 evidence 不可用，退回基于 examples.md 标准胶囊 + 确定性攻击模型的推导值。
    """
    if evidence.available():
        return evidence.real_owner_score(skill_id, attack_id)

    atk = attacks.get_attack(attack_id)

    # 用真实胶囊文本算 True-WS 的“干净基线”
    owner_caps, buyer_caps = data_access.split_owner_and_buyer_capsules(skill_id, buyer_id)
    sample = owner_caps + buyer_caps
    scores = [capsule.score_capsule(c["raw_yaml"])["capsule_score"] for c in sample]
    clean_true_ws = (sum(scores) / len(scores)) if scores else 0.0

    true_ws = round(clean_true_ws * atk["true_ws_retention"], 4)
    false_ws = round(config.FALSE_WS_FLOOR + atk["false_ws_delta"], 4)
    margin = round(true_ws - false_ws, 4)                       # 标准定义
    score_own = round(true_ws - config.LAMBDA_OWNER * false_ws, 4)  # 评分式
    verified = score_own > config.TAU_OWNER

    return {
        "true_ws": true_ws,
        "false_ws": false_ws,
        "margin": margin,
        "score_own": score_own,
        "lambda": config.LAMBDA_OWNER,
        "threshold": config.TAU_OWNER,
        "ownership": "verified" if verified else "not_verified",
        "probe_count": len(data_access.load_positive_probes(skill_id)) or len(sample),
        "formula": "Score_own = True-WS − λ · False-WS ；当 Score_own > τ_o 时所有权成立。",
    }


# ---------------------------------------------------------------------------
# 买家纠错解码
# ---------------------------------------------------------------------------


def _compare(observed: list[int | None], candidate: list[int | None]) -> tuple[int, int]:
    """返回 (errors, erasures) 相对某候选买家码字。"""
    errors = 0
    erasures = 0
    n = min(len(observed), len(candidate))
    for i in range(n):
        if observed[i] is None:
            erasures += 1
        elif candidate[i] is not None and observed[i] != candidate[i]:
            errors += 1
    return errors, erasures


def buyer_decode(skill_id: str, buyer_id: str, attack_id: str) -> dict:
    """对某案例做买家溯源解码，返回 top1/top3、错误/擦除、ECC 条件与置信度。

    优先使用真实实验输出（evidence）；不可用时退回确定性攻击模型。
    """
    if evidence.available():
        return evidence.real_buyer_decode(skill_id, buyer_id, attack_id)

    book = codebook.build_codebook(skill_id)
    true_bits = book.get(buyer_id, [])
    observed = attacks.apply_to_codeword(true_bits, attack_id)

    erasures_total = sum(1 for b in observed if b is None)

    ranking = []
    for cand_id, cand_bits in book.items():
        errors, erasures = _compare(observed, cand_bits)
        ranking.append({
            "buyer_id": cand_id,
            "errors": errors,
            "erasures": erasures,
            "distance": errors,  # 解码按 errors 升序
        })
    ranking.sort(key=lambda r: (r["errors"], r["buyer_id"]))

    top1 = ranking[0] if ranking else None
    top3 = [r["buyer_id"] for r in ranking[:3]]

    # 纠错条件：2e + s < d_min（纠错保证）
    e = top1["errors"] if top1 else 0
    s = erasures_total
    ecc_lhs = 2 * e + s
    ecc_satisfied = ecc_lhs < config.D_MIN

    # 解码置信度（ECC 安全裕度）：噪声越小越接近 1
    confidence = round(max(0.0, 1.0 - ecc_lhs / (2 * config.D_MIN)), 4)

    decode_margin = (ranking[1]["errors"] - e) if len(ranking) > 1 else None
    attributed = top1["buyer_id"] if top1 else None
    return {
        "attributed_buyer": attributed,
        "correct": attributed == buyer_id,
        "top1": attributed,
        "top3": top3,
        "errors": e,
        "erasures": s,
        "ecc_condition": "2·e + s < d_min",
        "ecc_lhs": ecc_lhs,
        "d_min": config.D_MIN,
        "ecc_satisfied": ecc_satisfied,
        "decode_margin": decode_margin,
        "confidence": confidence,
        "observed_bits": "".join("⊥" if b is None else str(b) for b in observed),
        "true_bits": "".join("⊥" if b is None else str(b) for b in true_bits),
        "ranking": ranking,
        "data_source": "simulated",
        "official": None,
    }
