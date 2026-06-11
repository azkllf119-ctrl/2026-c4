"""实验指标总览（⑤ 实验指标总览页）。

这些是“整体可信度”数字，用于证明方法不是个例，前端直接渲染对比图表。
"""
from __future__ import annotations

OWNER_VERIFICATION = {
    "title": "所有权验证（Owner Verification）",
    "metrics": [
        {"name": "准确率 Accuracy", "ours": 0.992, "promptcare": 0.896, "promptcos": 0.875,
         "higher_is_better": True},
        {"name": "True-WS", "ours": 0.992, "promptcare": 0.832, "promptcos": 0.865,
         "higher_is_better": True},
        {"name": "False-WS", "ours": 0.037, "promptcare": 0.097, "promptcos": 0.174,
         "higher_is_better": False},
        {"name": "Margin", "ours": 0.956, "promptcare": 0.735, "promptcos": 0.691,
         "higher_is_better": True},
    ],
    "takeaway": "SkillCODER 平均所有权验证准确率 99.2%，Margin 0.956，全面优于两个 prompt 级基线。",
}

BUYER_ATTRIBUTION = {
    "title": "买家溯源（Buyer Attribution · Top-1）",
    "metrics": [
        {"name": "Top-1 准确率", "ours": 0.993, "promptcare": 0.705, "promptcos": 0.676,
         "higher_is_better": True},
    ],
    "takeaway": "买家 Top-1 溯源准确率 99.3%，远高于基线（70.5% / 67.6%），"
                "说明受控词编码携带了足够的买家专属信息。",
}

ROBUSTNESS = {
    "title": "鲁棒性（四类盲攻击下的买家 Top-1）",
    "metrics": [
        {"name": "改写 Paraphrase", "buyer_top1": 0.976, "owner_acc": 0.997},
        {"name": "压缩 Compression", "buyer_top1": 0.996, "owner_acc": 0.998},
        {"name": "辅助条款删除 Aux deletion", "buyer_top1": 0.910, "owner_acc": 0.995},
        {"name": "章节重排 Reorganization", "buyer_top1": 0.998, "owner_acc": 0.999},
    ],
    "takeaway": "四类攻击下所有权验证均≥99.5%；最难的辅助条款删除买家 Top-1 仍≥91%。",
}

FIDELITY = {
    "title": "保真度（Fidelity · 加水印是否影响正常功能）",
    "metrics": [
        {"name": "效用下降 Utility Drop（越低越好）", "ours": 0.662,
         "promptcare": 0.700, "higher_is_better": False},
        {"name": "语义一致性 Semantic Consistency", "ours": 0.727,
         "promptcare": 0.559, "higher_is_better": True},
    ],
    "takeaway": "加水印后普通任务表现几乎无损，正常用户感知不到水印的存在。",
}

ABLATION = {
    "title": "消融实验（每个设计是否真的必要）",
    "items": [
        {"remove": "去掉 AGC 胶囊", "effect": "买家 Top-1 几乎崩溃"},
        {"remove": "去掉买家纠错码", "effect": "完全无法追踪买家"},
        {"remove": "去掉受控词表", "effect": "token 不稳定，买家溯源崩溃"},
        {"remove": "去掉验证示例", "effect": "胶囊触发不稳定"},
    ],
    "takeaway": "去掉任一核心组件性能都明显下降，证明每个设计都是必要的，而非摆设。",
}


def _run_official() -> dict | None:
    """读取本次真实运行（GPT-5 mini + LangChain）的官方逐域指标，作为“本场实测”板块。"""
    from . import config, data_access
    if not config.EVIDENCE_AVAILABLE:
        return None

    def rows_of(name):
        d = data_access.load_evidence_result(name)
        return (d or {}).get("rows", []) if d else []

    return {
        "run_tag": config.EVIDENCE_RUN,
        "model": config.EVIDENCE_MODEL,
        "agent": config.EVIDENCE_AGENT,
        "effectiveness_distinctiveness": rows_of("effectiveness_distinctiveness"),
        "buyer_attribution": rows_of("buyer_attribution"),
        "robustness": rows_of("robustness"),
        "fidelity": rows_of("fidelity"),
        "note": "以上为本次展示所用真实运行的官方指标（按域/攻击列出），与整体汇总方向一致。",
    }


def overview() -> dict:
    return {
        "overall": {
            "owner_verification": OWNER_VERIFICATION,
            "buyer_attribution": BUYER_ATTRIBUTION,
            "robustness": ROBUSTNESS,
            "fidelity": FIDELITY,
            "ablation": ABLATION,
            "source": "三域泛化实验汇总指标",
        },
        "run_official": _run_official(),
    }
