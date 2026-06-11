"""攻击效应模型（确定性、可复现，忠实于鲁棒性结论）。

⚠️ 数据说明：仓库当前不含“攻击后再探测”的真实模型输出（见 README 缺失数据清单）。
因此攻击对水印的影响在此用一个**确定性**模型表达——不引入随机数，便于评委每次看到
一致的结果，并与鲁棒性实验的结论方向一致：

  - 第一类攻击（语义保持改写 paraphrase）：结构不变，胶囊照常触发；仅极少数位读不出
    （擦除）。实验结果：买家 Top-1≈97.6%，所有权≥99.7%。
  - 第二类攻击（辅助条款删除 aux deletion）：定向删审计条款，是最具挑战性的攻击；
    更多位无法触发（擦除）并可能出现个别误读（错误），但仍满足纠错条件 2e+s<d_min，
    因此仍可解码。实验结果：买家 Top-1≥91%，所有权≥99.5%。

“擦除/错误落在哪些位”用固定常量给出（与买家、攻击类型绑定），使可视化稳定可讲。
"""
from __future__ import annotations

from . import config

# 攻击类型定义。erasure_positions / error_positions 为 32 位码字中的索引。
ATTACKS: dict[str, dict] = {
    "none": {
        "name": "无攻击",
        "family": "clean",
        "description": "攻击者原样转售买家副本，未做任何改写。",
        "true_ws_retention": 1.00,
        "false_ws_delta": 0.00,
        "erasure_positions": [],
        "error_positions": [],
        "text_effect": "Skill 文本与买家副本完全一致，结构与辅助条款均未改动。",
    },
    "type1_rewrite": {
        "name": "第一类攻击：语义保持改写",
        "family": "oblivious",
        "description": "攻击者不知道水印细节，只做保功能的同义改写、压缩与章节重排。",
        "true_ws_retention": 0.99,
        "false_ws_delta": 0.00,
        "erasure_positions": [9],          # 个别位在改写后读不出 -> 擦除
        "error_positions": [],
        "text_effect": "表面词句被同义替换、段落被压缩重排，但 SkillIR 结构节点保持不变，"
                       "胶囊仍稳定触发。",
    },
    "type2_watermark_suppression": {
        "name": "第二类攻击：辅助条款删除",
        "family": "adaptive",
        "description": "攻击者怀疑存在水印，定向删除看似内部审计/交接/胶囊的辅助条款，"
                       "属于针对性削弱攻击。",
        "true_ws_retention": 0.985,
        "false_ws_delta": 0.005,
        "erasure_positions": [5, 17, 28],  # 多个锚点被削弱 -> 擦除
        "error_positions": [22],           # 个别位被误读 -> 错误
        "text_effect": "部分 internal_capsule / handoff 相关辅助条款被删除，少数锚点不再触发；"
                       "但删干净会破坏 Skill 可用性（效用须≥80%），故水印整体存活。",
    },
}

# 5 个展示案例约定的攻击别名（与展示逻辑设计文档一致）
ATTACK_ALIASES = {
    "none": "none",
    "type1_rewrite": "type1_rewrite",
    "type2_watermark_suppression": "type2_watermark_suppression",
    # 数据/方法里的等价说法
    "paraphrase": "type1_rewrite",
    "aux_deletion": "type2_watermark_suppression",
}


def get_attack(attack_id: str) -> dict:
    key = ATTACK_ALIASES.get(attack_id, attack_id)
    if key not in ATTACKS:
        raise KeyError(f"未知攻击类型: {attack_id}")
    return {"id": key, **ATTACKS[key]}


def apply_to_codeword(true_bits: list[int | None], attack_id: str) -> list[int | None]:
    """把攻击效应施加到买家真实码字上，得到“审计侧观测到的”码字。

    - 擦除位 -> None（⊥）
    - 错误位 -> 翻转 0/1
    其余位保持真实值。
    """
    atk = get_attack(attack_id)
    observed: list[int | None] = list(true_bits)
    for p in atk["erasure_positions"]:
        if 0 <= p < len(observed):
            observed[p] = None
    for p in atk["error_positions"]:
        if 0 <= p < len(observed) and observed[p] is not None:
            observed[p] = 1 - observed[p]
    return observed
