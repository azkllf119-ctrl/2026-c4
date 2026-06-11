#!/usr/bin/env bash
# 启动 SkillCODER 展示后端。
# 用法：bash backend/run.sh   （默认监听 http://127.0.0.1:8000）
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"
export SKILLCODER_DATA_DIR="${SKILLCODER_DATA_DIR:-$(cd "$HERE/.." && pwd)/data}"
echo "[SkillCODER demo] 数据目录: $SKILLCODER_DATA_DIR"
exec uvicorn app.main:app --host "${HOST:-127.0.0.1}" --port "${PORT:-8000}" --reload
