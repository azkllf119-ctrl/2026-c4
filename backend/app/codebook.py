"""买家指纹码本（CV-ECC）。

对应方法与源码报告 buyer_coder.py：
  - 每个买家 = 一串长度 L=32 的 0/1 码字（Hadamard 码）。
  - 每一位由一对“受控词”实现：<name>_trace 表示 1，trace_<name> 表示 0。
  - 不同买家的码字在汉明距离上相隔较远（d_min=16），因此即使模型输出错几位也不易混淆。

本模块从买家 examples.md 中真实抽取的胶囊序列，还原出每个买家的码字。
"""
from __future__ import annotations

import functools

from . import config, data_access


def _bits_from_buyer_capsules(skill_id: str, buyer_id: str) -> list[int | None]:
    """取某买家的 32 个指纹 token，逐个映射为 0/1（无法识别记为 None=擦除）。"""
    _, buyer_caps = data_access.split_owner_and_buyer_capsules(skill_id, buyer_id)
    bits = [config.token_to_bit(c["judgment"]) for c in buyer_caps]
    return bits[: config.CODEWORD_LENGTH]


def buyer_tokens(skill_id: str, buyer_id: str) -> list[str | None]:
    _, buyer_caps = data_access.split_owner_and_buyer_capsules(skill_id, buyer_id)
    return [c["judgment"] for c in buyer_caps][: config.CODEWORD_LENGTH]


@functools.lru_cache(maxsize=32)
def build_codebook(skill_id: str) -> dict[str, list[int | None]]:
    """构建 {buyer_id: 32位码字} 的码本，覆盖该 skill 的全部买家。"""
    book: dict[str, list[int | None]] = {}
    for buyer_id in data_access.list_buyers(skill_id):
        bits = _bits_from_buyer_capsules(skill_id, buyer_id)
        if bits:
            book[buyer_id] = bits
    return book


def fingerprint_summary(skill_id: str, buyer_id: str) -> dict:
    """单个买家的指纹摘要，供「第 4 步：买家指纹」与拆分接口使用。"""
    bits = _bits_from_buyer_capsules(skill_id, buyer_id)
    tokens = buyer_tokens(skill_id, buyer_id)
    bitstr = "".join("⊥" if b is None else str(b) for b in bits)
    return {
        "buyer_id": buyer_id,
        "codeword_length": config.CODEWORD_LENGTH,
        "d_min": config.D_MIN,
        "fingerprint_bits": bitstr,
        "tokens": tokens,
        "positions": [
            {"index": i, "token": tokens[i] if i < len(tokens) else None,
             "bit": bits[i] if i < len(bits) else None}
            for i in range(config.CODEWORD_LENGTH)
        ],
    }


def hamming_distance(a: list[int | None], b: list[int | None]) -> int:
    """两码字在“双方都确定”的位上的汉明距离。"""
    return sum(1 for x, y in zip(a, b) if x is not None and y is not None and x != y)


def pairwise_distance(skill_id: str, buyer_a: str, buyer_b: str) -> dict:
    """两个买家码字的逐位对比，用于「buyer_1 vs buyer_2」可视化。"""
    book = build_codebook(skill_id)
    a, b = book.get(buyer_a, []), book.get(buyer_b, [])
    diff_positions = [i for i in range(min(len(a), len(b))) if a[i] != b[i]]
    return {
        "buyer_a": buyer_a,
        "buyer_b": buyer_b,
        "bits_a": "".join("⊥" if x is None else str(x) for x in a),
        "bits_b": "".join("⊥" if x is None else str(x) for x in b),
        "diff_positions": diff_positions,
        "hamming_distance": hamming_distance(a, b),
        "d_min": config.D_MIN,
        "note": "两份副本码字相隔的位数越多，越不会被混淆；这就是溯源能区分不同买家的根本原因。",
    }
