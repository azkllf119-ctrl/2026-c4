"""数据访问层：只读地加载仓库中“已完成实验”的数据文件。

涉及的真实数据：
  - data/skills_raw/<skill>/                原始未加水印 Skill
  - data/skills_watermarked/<skill>/        加了所有者水印的 Skill
  - data/skills_buyer/<skill>__buyer_N/     各买家专属副本（含指纹）
  - data/queries/<skill>_verification.json          32 条正探针
  - data/queries/<skill>_negative_verification.json 32 条负探针
  - data/queries/<skill>_normal.json                普通任务查询

本模块不做任何水印/攻击/推理计算，只负责把磁盘上的实验产物读进内存。
"""
from __future__ import annotations

import functools
import json
import re
from pathlib import Path
from typing import Any

from . import config

# ---------------------------------------------------------------------------
# 基础读取
# ---------------------------------------------------------------------------


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _read_json(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Skill 读取（原始 / 所有者水印 / 买家副本）
# ---------------------------------------------------------------------------

_SKILL_FILES = ["SKILL.md", "reference.md", "examples.md", "verification_mode.md"]


def _load_skill_dir(base: Path) -> dict[str, Any]:
    """把一个 skill 目录读成统一结构。"""
    meta = _read_json(base / "skillcoder.json") or {}
    files = {name: _read_text(base / name) for name in _SKILL_FILES}
    return {
        "exists": base.exists(),
        "path": str(base),
        "meta": meta,
        "files": files,
    }


def load_raw_skill(skill_id: str) -> dict[str, Any]:
    return _load_skill_dir(config.SKILLS_RAW_DIR / skill_id)


def load_watermarked_skill(skill_id: str) -> dict[str, Any]:
    return _load_skill_dir(config.SKILLS_WATERMARKED_DIR / skill_id)


def load_buyer_skill(skill_id: str, buyer_id: str) -> dict[str, Any]:
    base = config.SKILLS_BUYER_DIR / f"{skill_id}__{buyer_id}"
    return _load_skill_dir(base)


def list_buyers(skill_id: str) -> list[str]:
    """列出某 skill 拥有的全部买家（如 buyer_1 .. buyer_8）。"""
    out = []
    prefix = f"{skill_id}__"
    if config.SKILLS_BUYER_DIR.exists():
        for d in sorted(config.SKILLS_BUYER_DIR.iterdir()):
            if d.is_dir() and d.name.startswith(prefix):
                out.append(d.name[len(prefix):])
    return _natural_sort(out)


def _natural_sort(items: list[str]) -> list[str]:
    def key(s: str):
        m = re.search(r"(\d+)", s)
        return (int(m.group(1)) if m else 0, s)
    return sorted(items, key=key)


# ---------------------------------------------------------------------------
# Skill 章节切分（用于「第 2 步：SkillIR 结构化」可视化）
# ---------------------------------------------------------------------------

# 把 Markdown 标题粗映射到方法 SkillIR 的六类节点类型。
_SECTION_TYPE_HINTS = [
    (r"role|persona|identity|overview|coordinat", "role"),
    (r"workflow|step|procedure|process", "workflow_step"),
    (r"constraint|rule|polic|must|guard", "constraint"),
    (r"exception|fallback|error|edge", "fallback_handler"),
    (r"output|format|response|template", "output_format"),
    (r"example|sample|demo", "exemplar"),
    (r"context|reference|background", "context_guard"),
]


def classify_section(title: str) -> str:
    low = title.lower()
    for pattern, node_type in _SECTION_TYPE_HINTS:
        if re.search(pattern, low):
            return node_type
    return "constraint"


def split_sections(markdown: str) -> list[dict[str, str]]:
    """把一份 SKILL.md 拆成 (标题, 类型, 正文片段) 列表，供前端画结构图。"""
    sections: list[dict[str, str]] = []
    current = None
    for line in markdown.splitlines():
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            if current:
                sections.append(current)
            title = m.group(2).strip()
            current = {"title": title, "type": classify_section(title), "body": ""}
        elif current is not None:
            current["body"] += line + "\n"
    if current:
        sections.append(current)
    # 保留完整正文（前端用可滚动容器展示，不做截断）
    for s in sections:
        s["body"] = s["body"].strip()
    return sections


# ---------------------------------------------------------------------------
# 探针查询读取
# ---------------------------------------------------------------------------


def load_positive_probes(skill_id: str) -> list[dict[str, Any]]:
    return _read_json(config.QUERIES_DIR / f"{skill_id}_verification.json") or []


def load_negative_probes(skill_id: str) -> list[dict[str, Any]]:
    return _read_json(config.QUERIES_DIR / f"{skill_id}_negative_verification.json") or []


def load_normal_queries(skill_id: str) -> list[dict[str, Any]]:
    return _read_json(config.QUERIES_DIR / f"{skill_id}_normal.json") or []


# ---------------------------------------------------------------------------
# 从买家 examples.md 中抽取“胶囊输出”（这是溯源的真实 ground-truth 数据）
# ---------------------------------------------------------------------------

# 抓取 ```yaml ... ``` 围栏代码块
_YAML_BLOCK_RE = re.compile(r"```ya?ml\s*(.*?)```", re.DOTALL | re.IGNORECASE)
# 受控词 token 兼容两套 schema：decision.judgment（judgment:）与 labels.token（token:）
_JUDGMENT_RE = re.compile(r"(?:judgment|token):\s*([A-Za-z0-9_]+)")
_AXIS_RE = re.compile(r"axis:\s*(.+)")


@functools.lru_cache(maxsize=256)
def load_buyer_capsules(skill_id: str, buyer_id: str) -> list[dict[str, Any]]:
    """解析买家 examples.md 中所有 internal_capsule，返回有序列表。

    每条记录：{order, raw_yaml, judgment, axis}
    其中 judgment 即 decision.judgment 受控词（owner_0x 或买家指纹 token）。
    这些是“一个忠实水印副本在对应探针下应当输出的胶囊”，作为展示用的模型输出基准。
    """
    skill = load_buyer_skill(skill_id, buyer_id)
    text = skill["files"].get("examples.md", "")
    capsules: list[dict[str, Any]] = []
    for i, block in enumerate(_YAML_BLOCK_RE.findall(text)):
        if "internal_capsule" not in block:
            continue
        jm = _JUDGMENT_RE.search(block)
        am = _AXIS_RE.search(block)
        capsules.append({
            "order": len(capsules),
            "raw_yaml": block.strip(),
            "judgment": jm.group(1) if jm else None,
            "axis": (am.group(1).strip() if am else None),
        })
    return capsules


def split_owner_and_buyer_capsules(skill_id: str, buyer_id: str):
    """把胶囊分成「所有者验证标签(owner_0x)」与「买家指纹 token」两组。

    返回 (owner_capsules, buyer_capsules)。
    - owner_capsules: judgment 形如 owner_00..owner_07，用于所有权验证。
    - buyer_capsules: 其余 32 个受控词，构成买家的 32 位指纹。
    """
    caps = load_buyer_capsules(skill_id, buyer_id)
    owner = [c for c in caps if c["judgment"] and re.fullmatch(r"owner_\d+", c["judgment"])]
    buyer = [c for c in caps if not (c["judgment"] and re.fullmatch(r"owner_\d+", c["judgment"]))]
    return owner, buyer


# ---------------------------------------------------------------------------
# 真实实验输出（evidence）读取
# ---------------------------------------------------------------------------


def load_evidence_outputs(rel_path: str) -> list[dict[str, Any]]:
    """读取一个真实输出文件（list of {query, output, meta, skill_path}）。

    rel_path 相对于 EVIDENCE_OUTPUTS_DIR，例如
    'buyer_verification/code_review__buyer_1__verification.json'。
    """
    data = _read_json(config.EVIDENCE_OUTPUTS_DIR / rel_path)
    return data if isinstance(data, list) else []


def load_evidence_result(name: str) -> Any:
    """读取一个官方指标文件，例如 'effectiveness_distinctiveness'。"""
    return _read_json(config.EVIDENCE_RESULTS_DIR / f"{name}.json")
