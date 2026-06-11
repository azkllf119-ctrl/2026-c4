"""5 个预置展示案例（与展示逻辑设计文档完全一致）。"""
from __future__ import annotations

DEFAULT_SKILL = "code_review"

CASES: list[dict] = [
    {
        "case_id": "buyer1_clean",
        "title": "Buyer 1 · 无攻击",
        "skill_id": DEFAULT_SKILL,
        "buyer_id": "buyer_1",
        "attack": "none",
        "difficulty": "baseline",
        "goal": "理想情况下，所有权与溯源都干净命中（基线）。",
    },
    {
        "case_id": "buyer1_attack_type1",
        "title": "Buyer 1 · 第一类攻击",
        "skill_id": DEFAULT_SKILL,
        "buyer_id": "buyer_1",
        "attack": "type1_rewrite",
        "difficulty": "oblivious_attack",
        "goal": "攻击者不懂水印、只做普通改写，水印依然存活、溯源依然命中。",
    },
    {
        "case_id": "buyer1_attack_type2",
        "title": "Buyer 1 · 第二类攻击",
        "skill_id": DEFAULT_SKILL,
        "buyer_id": "buyer_1",
        "attack": "type2_watermark_suppression",
        "difficulty": "adaptive_attack",
        "goal": "攻击者定向删审计条款（最难场景），分数略降但仍稳定判对。",
    },
    {
        "case_id": "buyer2_clean",
        "title": "Buyer 2 · 无攻击",
        "skill_id": DEFAULT_SKILL,
        "buyer_id": "buyer_2",
        "attack": "none",
        "difficulty": "baseline",
        "goal": "换一个买家，溯源精准切到 buyer_2 而非 buyer_1，证明指纹有区分度。",
    },
    {
        "case_id": "buyer2_attack_type1",
        "title": "Buyer 2 · 第一类攻击",
        "skill_id": DEFAULT_SKILL,
        "buyer_id": "buyer_2",
        "attack": "type1_rewrite",
        "difficulty": "oblivious_attack",
        "goal": "换买家+攻击双重考验，所有权与溯源仍稳定，证明泛化性。",
    },
]

_BY_ID = {c["case_id"]: c for c in CASES}


def list_cases() -> list[dict]:
    return CASES


def get_case(case_id: str) -> dict:
    if case_id not in _BY_ID:
        raise KeyError(f"未知案例: {case_id}")
    return _BY_ID[case_id]
