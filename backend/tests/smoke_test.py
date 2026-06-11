"""冒烟测试：不依赖网络，验证 5 个案例的全链路与关键不变量。

运行：python3 -m tests.smoke_test   （在 backend/ 目录下）
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import cases, codebook, config, metrics, narratives, pipeline  # noqa: E402


def check(cond: bool, msg: str):
    print(("  ✓ " if cond else "  ✗ ") + msg)
    if not cond:
        raise AssertionError(msg)


def main():
    skill = cases.DEFAULT_SKILL
    print(f"[1] 码本完整性（skill={skill}）")
    book = codebook.build_codebook(skill)
    check(len(book) >= 2, f"至少 2 个买家，实际 {len(book)}")
    for bid, bits in book.items():
        check(len(bits) == config.CODEWORD_LENGTH,
              f"{bid} 码字长度={len(bits)}（应为 {config.CODEWORD_LENGTH}）")
    d = codebook.pairwise_distance(skill, "buyer_1", "buyer_2")
    check(d["hamming_distance"] >= config.D_MIN,
          f"buyer_1↔buyer_2 距离={d['hamming_distance']}（应≥d_min={config.D_MIN}）")

    print("[2] 五个案例全链路")
    for c in cases.list_cases():
        tl = pipeline.build_timeline(c["case_id"])
        s = tl["summary"]
        check(len(tl["timeline"]) == len(narratives.STAGES),
              f"{c['case_id']}: 时间线 {len(tl['timeline'])} 步")
        check(s["ownership"] == "verified",
              f"{c['case_id']}: 所有权={s['ownership']}")
        check(s["attribution_correct"] is True,
              f"{c['case_id']}: 溯源命中 {s['attributed_buyer']}（期望 {c['buyer_id']}）")
        check(s["ecc_satisfied"] is True,
              f"{c['case_id']}: ECC 2e+s<d_min 满足（e={s['errors']}, s={s['erasures']}）")
        check(s["score_own"] > config.TAU_OWNER,
              f"{c['case_id']}: Score_own={s['score_own']} > τ_o={config.TAU_OWNER}")
        print(f"    · {c['case_id']:<22} 归属={s['attributed_buyer']} "
              f"Margin={s['margin']} conf={s['confidence']} e/s={s['errors']}/{s['erasures']}")

    print("[3] 每步 visual 类型齐全")
    expected_types = {
        "skill_loaded": "skill_document",
        "skillir_built": "node_graph",
        "owner_watermark_embedded": "capsule_schema",
        "buyer_fingerprint_embedded": "bit_grid",
        "attack_applied": "attack_diff",
        "differential_probing": "probe_pair",
        "ownership_scored": "score_bar",
        "buyer_decoded": "decode_grid",
    }
    tl = pipeline.build_timeline("buyer1_attack_type2")
    for step in tl["timeline"]:
        vt = step["visual"]["type"]
        check(vt == expected_types[step["stage"]],
              f"{step['stage']} -> visual.type={vt}")

    print("[4] 指标总览可用")
    ov = metrics.overview()
    check("owner_verification" in ov["overall"], "整体汇总指标齐全")

    print("[5] 数据来源")
    from app import evidence
    tl = pipeline.build_timeline("buyer1_clean")
    src = tl["provenance"]["data_source"]
    check(src in ("real", "simulated"), f"数据来源={src}")
    if evidence.available():
        check(src == "real", "已接入真实实验输出（evidence）")
        check(ov["run_official"] is not None, "官方指标已加载")
        print(f"    · 真实运行：{tl['provenance']['model']} + {tl['provenance']['agent']}")

    print("\n全部冒烟测试通过 ✅")


if __name__ == "__main__":
    main()
