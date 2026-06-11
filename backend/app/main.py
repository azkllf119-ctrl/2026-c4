"""SkillCODER 展示网站后端 · FastAPI 路由层。

设计原则：
  1. 完全遵循方法逻辑（两阶段、八步骤、五字段胶囊、CV-ECC 溯源）。
  2. 展示优先、亲和评委：接口直接返回可渲染的“故事流 + 带类型 visual”，
     前端无需自行拼接方法细节；并提供 SSE 逐步播放、买家指纹对比等交互接口。

本层不含任何水印/攻击/推理的实验源码，只做“读数据 + 组织讲解”。
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from . import (cases, codebook, config, data_access, metrics, narratives,
               pipeline, ui_text)

app = FastAPI(
    title="SkillCODER 展示后端",
    description="Skill 水印嵌入·识别·买家溯源全流程展示接口（仅展示，不跑实验）。",
    version=config.DEMO_VERSION,
)

# 展示站点：放开跨域，方便任意前端联调
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# 基础
# ---------------------------------------------------------------------------


@app.get("/")
def root():
    return {
        "service": "SkillCODER demo backend",
        "version": config.DEMO_VERSION,
        "docs": "/docs",
        "entrypoints": [
            "/api/demo/cases",
            "/api/demo/cases/{case_id}",
            "/api/demo/cases/{case_id}/stream",
            "/api/metrics/overview",
        ],
    }


@app.get("/api/health")
def health():
    return {
        "ok": True,
        "version": config.DEMO_VERSION,
        "data_dir": str(config.DATA_DIR),
        "data_present": config.SKILLS_BUYER_DIR.exists(),
    }


@app.get("/api/ui/text")
def ui_strings():
    """前端 UI 静态文案（导航、背景、各区块标题、visual 标签、裁决卡、指标表头等）。

    前端启动时拉取本接口，据此填充全部界面文字；业务文案的唯一真源在后端。
    """
    return ui_text.UI_TEXT


@app.get("/api/demo/meta")
def demo_meta():
    """展示总配置：默认 skill、买家列表、攻击族、方法常量。"""
    skill_id = cases.DEFAULT_SKILL
    return {
        "default_skill": skill_id,
        "buyers": data_access.list_buyers(skill_id),
        "attack_families": [
            {"id": "clean", "label": "无攻击"},
            {"id": "oblivious", "label": "第一类攻击（盲攻击·保功能改写）"},
            {"id": "adaptive", "label": "第二类攻击（针对性削弱·删辅助条款）"},
        ],
        "constants": {
            "codeword_length": config.CODEWORD_LENGTH,
            "d_min": config.D_MIN,
            "capsule_fields": config.CAPSULE_FIELDS,
            "lambda_owner": config.LAMBDA_OWNER,
            "tau_owner": config.TAU_OWNER,
        },
        "stages": [narratives.stage_meta(s) for s in narratives.STAGES],
    }


# ---------------------------------------------------------------------------
# 案例（核心故事流）
# ---------------------------------------------------------------------------


@app.get("/api/demo/cases")
def list_cases():
    return cases.list_cases()


@app.get("/api/demo/cases/{case_id}")
def get_case(case_id: str):
    try:
        return pipeline.build_timeline(case_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/demo/cases/{case_id}/steps/{stage}")
def get_case_step(case_id: str, stage: str):
    try:
        return pipeline.build_step(case_id, stage)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/demo/cases/{case_id}/stream")
async def stream_case(case_id: str, delay: float = Query(0.9, ge=0.0, le=5.0)):
    """SSE 流式播放：按八步顺序逐步推送，便于前端做“运行中”动画。

    每个事件 data 为一个步骤；最后推送 report_ready 收尾。
    """
    try:
        full = pipeline.build_timeline(case_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

    async def event_gen():
        for step in full["timeline"]:
            payload = json.dumps(step, ensure_ascii=False)
            yield f"event: {step['stage']}\ndata: {payload}\n\n"
            await asyncio.sleep(delay)
        summary = json.dumps(
            {"case_id": case_id, "summary": full["summary"]}, ensure_ascii=False)
        yield f"event: report_ready\ndata: {summary}\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream")


# ---------------------------------------------------------------------------
# 拆分接口（让每一步都能单独点开）
# ---------------------------------------------------------------------------


@app.get("/api/skills/{skill_id}/raw")
def skill_raw(skill_id: str):
    skill = data_access.load_raw_skill(skill_id)
    if not skill["exists"]:
        raise HTTPException(404, f"原始 skill 不存在: {skill_id}")
    return {
        "skill_id": skill_id,
        "meta": skill["meta"],
        "files": skill["files"],
        "sections": data_access.split_sections(skill["files"].get("SKILL.md", "")),
    }


@app.get("/api/skills/{skill_id}/watermarked")
def skill_watermarked(skill_id: str):
    skill = data_access.load_watermarked_skill(skill_id)
    if not skill["exists"]:
        raise HTTPException(404, f"所有者水印 skill 不存在: {skill_id}")
    return {"skill_id": skill_id, "meta": skill["meta"], "files": skill["files"]}


@app.get("/api/skills/{skill_id}/ir")
def skill_ir(skill_id: str):
    return pipeline._visual_skillir(skill_id)


@app.get("/api/skills/{skill_id}/buyers")
def skill_buyers(skill_id: str):
    return {"skill_id": skill_id, "buyers": data_access.list_buyers(skill_id)}


@app.get("/api/watermarks/{skill_id}/buyers/{buyer_id}")
def watermark_buyer(skill_id: str, buyer_id: str):
    fp = codebook.fingerprint_summary(skill_id, buyer_id)
    if not fp["tokens"]:
        raise HTTPException(404, f"买家副本不存在或无指纹: {skill_id}/{buyer_id}")
    return fp


@app.get("/api/watermarks/{skill_id}/compare")
def watermark_compare(skill_id: str, a: str = "buyer_1", b: str = "buyer_2"):
    """两个买家指纹的逐位对比（buyer_1 vs buyer_2 可视化）。"""
    return codebook.pairwise_distance(skill_id, a, b)


@app.get("/api/queries/{skill_id}")
def queries(skill_id: str, kind: str = Query("all", pattern="^(all|positive|negative|normal)$")):
    pos = data_access.load_positive_probes(skill_id)
    neg = data_access.load_negative_probes(skill_id)
    nor = data_access.load_normal_queries(skill_id)
    if kind == "positive":
        return {"skill_id": skill_id, "positive": pos}
    if kind == "negative":
        return {"skill_id": skill_id, "negative": neg}
    if kind == "normal":
        return {"skill_id": skill_id, "normal": nor}
    return {
        "skill_id": skill_id,
        "positive_count": len(pos), "negative_count": len(neg), "normal_count": len(nor),
        "positive": pos, "negative": neg, "normal": nor,
    }


# ---------------------------------------------------------------------------
# 指标总览
# ---------------------------------------------------------------------------


@app.get("/api/metrics/overview")
def metrics_overview():
    return metrics.overview()


# ---------------------------------------------------------------------------
# 前端静态托管：若同仓库存在 frontend/ 目录，则在 /ui 提供页面（一条命令跑通整套）
# 访问 http://127.0.0.1:8000/ui/
# ---------------------------------------------------------------------------
_FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
if _FRONTEND_DIR.exists():
    app.mount("/ui", StaticFiles(directory=str(_FRONTEND_DIR), html=True), name="ui")
