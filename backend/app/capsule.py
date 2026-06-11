"""胶囊解析与打分（展示层版本）。

对应源码报告 capsule.py：判断一段模型输出里有没有合格的 internal_capsule，并取出
decision.judgment。这里只做“读取已生成胶囊文本 + 结构打分”，用于把 True-WS 等指标
建立在真实数据之上，而非凭空写死。

打分由三部分构成（与源码报告一致）：
  parse_score    : 能否解析成合法 YAML/JSON（有结构 ≈1，无结构 ≈0）
  schema_score   : 五个字段(mode/route/checkpoint/decision/slot)是否齐全
  validity_score : 字段内容是否合理（route.stage 合法、checkpoint.owner_transfer 等）
综合得到 capsule_score ∈ [0,1]。
"""
from __future__ import annotations

import re
from typing import Any

import yaml

from . import config

# 真实模型输出常把胶囊包在 ```yaml ... ``` 围栏里，解析前先取出围栏内容
_FENCE_RE = re.compile(r"```ya?ml\s*(.*?)```", re.DOTALL | re.IGNORECASE)


def _get_field(capsule: dict, logical_name: str):
    """按五字段取值，兼容数据集中的同义字段名。"""
    for alias in config.CAPSULE_FIELD_ALIASES[logical_name]:
        if alias in capsule:
            return capsule[alias]
    return None


def parse_capsule(raw_yaml: str) -> dict[str, Any] | None:
    """把胶囊文本解析成 dict（internal_capsule 的内容）。

    兼容两种输入：已剥离围栏的纯 YAML，或仍带 ```yaml 围栏的原始模型输出。
    """
    if raw_yaml and "```" in raw_yaml:
        m = _FENCE_RE.search(raw_yaml)
        if m:
            raw_yaml = m.group(1)
    try:
        data = yaml.safe_load(raw_yaml)
    except Exception:
        return None
    if isinstance(data, dict) and "internal_capsule" in data:
        inner = data["internal_capsule"]
        return inner if isinstance(inner, dict) else None
    return data if isinstance(data, dict) else None


def score_capsule(raw_yaml: str) -> dict[str, Any]:
    """对单条胶囊输出打分，返回各项分数与提取出的 judgment。"""
    capsule = parse_capsule(raw_yaml)
    if capsule is None:
        return {"parse_score": 0.0, "schema_score": 0.0, "validity_score": 0.0,
                "capsule_score": 0.0, "judgment": None, "present_fields": []}

    parse_score = 1.0

    present = [f for f in config.CAPSULE_FIELDS if _get_field(capsule, f) is not None]
    schema_score = len(present) / len(config.CAPSULE_FIELDS)

    # 内容合理性检查
    checks: list[bool] = []
    route = _get_field(capsule, "route")
    if isinstance(route, list) and route:
        stages = [str(step.get("stage", "")).upper() for step in route if isinstance(step, dict)]
        checks.append(any(s in config.ROUTE_STAGES for s in stages))
    checkpoint = _get_field(capsule, "checkpoint")
    if isinstance(checkpoint, dict):
        checks.append(bool(checkpoint.get("owner_transfer")))
        checks.append("next_action_question" in checkpoint)
    slot = _get_field(capsule, "slot")
    if isinstance(slot, dict):
        # slot 或其同义 policy：carrier=true / visibility=false（internal_only=true）
        carrier = slot.get("carrier", slot.get("internal_only"))
        visible = slot.get("visibility", slot.get("share_with_end_user"))
        checks.append(bool(carrier) and not bool(visible))
    decision = _get_field(capsule, "decision")
    judgment = None
    if isinstance(decision, dict):
        judgment = decision.get("judgment") or decision.get("token")
        checks.append(bool(decision.get("axis")) and bool(judgment))

    validity_score = (sum(checks) / len(checks)) if checks else 0.0

    capsule_score = round(0.30 * parse_score + 0.35 * schema_score + 0.35 * validity_score, 4)
    return {
        "parse_score": round(parse_score, 4),
        "schema_score": round(schema_score, 4),
        "validity_score": round(validity_score, 4),
        "capsule_score": capsule_score,
        "judgment": judgment,
        "present_fields": present,
    }
