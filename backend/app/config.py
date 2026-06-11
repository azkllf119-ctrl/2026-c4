"""全局路径与方法常量。

所有“魔法数字”集中在此，并标注其在方法中的出处，方便评委追溯。
"""
from __future__ import annotations

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# 路径
# ---------------------------------------------------------------------------
# backend/app/config.py -> backend/ -> 仓库根
_REPO_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = Path(os.environ.get("SKILLCODER_DATA_DIR", _REPO_ROOT / "data"))

# ---------------------------------------------------------------------------
# 真实实验数据（首选数据源）
# ---------------------------------------------------------------------------
# 取自实验服务器的归档运行：GPT-5 mini + LangChain（默认实验配置），
# 已逐案例校验：5 个案例全部正确溯源、decode margin=16、负探针零误触发。
# run_tag = newpkg_api_ours_openai_gpt_5_mini_langchain
EVIDENCE_RUN = os.environ.get("SKILLCODER_EVIDENCE_RUN", "gpt5mini_langchain")
EVIDENCE_DIR = DATA_DIR / "evidence" / EVIDENCE_RUN
EVIDENCE_OUTPUTS_DIR = EVIDENCE_DIR / "outputs"
EVIDENCE_RESULTS_DIR = EVIDENCE_DIR / "results" / "official_metrics"
EVIDENCE_SKILLS_DIR = EVIDENCE_DIR / "skills"
EVIDENCE_AVAILABLE = EVIDENCE_OUTPUTS_DIR.exists()

# Skill / 查询数据源：优先用 evidence 自带的（与真实输出同批次、labels.token schema），
# 否则退回仓库根 data/ 下的同名目录。
SKILLS_RAW_DIR = (EVIDENCE_SKILLS_DIR / "skills_raw") if EVIDENCE_AVAILABLE else (DATA_DIR / "skills_raw")
SKILLS_WATERMARKED_DIR = (EVIDENCE_SKILLS_DIR / "skills_watermarked") if EVIDENCE_AVAILABLE else (DATA_DIR / "skills_watermarked")
SKILLS_BUYER_DIR = (EVIDENCE_SKILLS_DIR / "skills_buyer") if EVIDENCE_AVAILABLE else (DATA_DIR / "skills_buyer")
# 攻击后的 Skill 副本（用于「攻击前后对比」），来自同一可靠运行的归档 artifacts
SKILLS_ATTACKED_BUYER_DIR = EVIDENCE_SKILLS_DIR / "skills_attacked_buyer"
SKILLS_ATTACKED_OWNER_DIR = EVIDENCE_SKILLS_DIR / "skills_attacked_owner"
QUERIES_DIR = (EVIDENCE_DIR / "queries") if (EVIDENCE_DIR / "queries").exists() else (DATA_DIR / "queries")
SIGNALS_DIR = DATA_DIR / "signals"

# 实验后端元信息（展示用）
EVIDENCE_MODEL = "openai/gpt-5-mini"
EVIDENCE_AGENT = "LangChain"

# ---------------------------------------------------------------------------
# 方法常量（来源标注）
# ---------------------------------------------------------------------------
# 买家纠错码码长 L。方法：采用 Hadamard 码，L=32 支持至多 64 个买家。
CODEWORD_LENGTH = 32

# Hadamard 码最小汉明距离 d_min = L/2。纠错保证。
D_MIN = CODEWORD_LENGTH // 2  # = 16

# 所有权胶囊的五个字段。方法定义：a = <mode, route, checkpoint, decision, slot>。
CAPSULE_FIELDS = ["mode", "route", "checkpoint", "decision", "slot"]

# 数据集中实际使用的等价字段名（源码报告：snapshot/labels/policy 与 mode/decision/slot 为同义批次）。
CAPSULE_FIELD_ALIASES = {
    "mode": ["mode", "snapshot"],
    "route": ["route", "decision_trace"],
    "checkpoint": ["checkpoint"],
    "decision": ["decision", "labels"],
    "slot": ["slot", "policy"],
}

# route.stage 允许取值。买家 skillcoder.json 的 auxiliary_clauses 中写明。
ROUTE_STAGES = ["TRIAGE", "PLAN", "EXECUTE", "VERIFY", "ESCALATE"]

# 所有权差分评分的惩罚权重 λ 与判定阈值 τ_o。
# 评分式：Score_own = True-WS − λ · False-WS；当 Score_own > τ_o 时判定所有权成立。
LAMBDA_OWNER = 1.0
TAU_OWNER = 0.50

# False-WS 的“偶然激活”地板值：独立编写的 skill 在负探针下极少误吐胶囊。
# 实验中 SkillCODER 平均 False-WS≈0.037，这里取一个同量级的保守基线。
FALSE_WS_FLOOR = 0.03

# 指纹受控词的 0/1 约定（源码报告 buyer_coder.py）：
#   <name>_trace -> 1 ，  trace_<name> -> 0
def token_to_bit(token: str):
    """把一个 judgment 受控词映射成 0 / 1；无法识别返回 None（擦除）。"""
    if not token:
        return None
    return 0 if token.startswith("trace_") else 1


# 服务版本号
DEMO_VERSION = "demo-v1"
