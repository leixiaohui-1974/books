#!/bin/bash
# OpenClaw → HydroScribe Skill 入口脚本
# 通过 HTTP API 调用 HydroScribe 写作系统
#
# 用法: ./run_hydroscribe_skill.sh <book_id> [skill_type] [chapter_id] [gate_mode]
# 示例: ./run_hydroscribe_skill.sh T2a BK ch07 auto

set -e

# HydroScribe API 地址（Docker 容器内通过服务名访问）
HYDROSCRIBE_API="${HYDROSCRIBE_API_URL:-http://hydroscribe_api:8000}"

# 参数解析
BOOK_ID="${1:?错误: 请提供 book_id 参数}"
SKILL_TYPE="${2:-BK}"
CHAPTER_ID="${3:-}"
GATE_MODE="${4:-auto}"

# 输出目录
OUTPUT_DIR="${OUTPUT_DIR:-/app/output}"
mkdir -p "${OUTPUT_DIR}"
OUTPUT_FILE="${OUTPUT_DIR}/hydroscribe_${BOOK_ID}_$(date +%Y%m%d%H%M%S).json"

echo "[HydroScribe Skill] 启动写作任务"
echo "  书目: ${BOOK_ID}"
echo "  技能: ${SKILL_TYPE}"
echo "  章节: ${CHAPTER_ID:-自动选择}"
echo "  门控: ${GATE_MODE}"
echo "  API:  ${HYDROSCRIBE_API}"

# ① 启动写作任务
RESPONSE=$(curl -s -X POST "${HYDROSCRIBE_API}/api/tasks/start" \
    -H "Content-Type: application/json" \
    -d "{
        \"book_id\": \"${BOOK_ID}\",
        \"skill_type\": \"${SKILL_TYPE}\",
        \"gate_mode\": \"${GATE_MODE}\"
    }")

echo "[HydroScribe Skill] 启动响应: ${RESPONSE}"

TASK_STATUS=$(echo "${RESPONSE}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status','error'))" 2>/dev/null || echo "error")

if [ "${TASK_STATUS}" != "started" ]; then
    echo "[HydroScribe Skill] 错误: 任务启动失败"
    echo "ERROR: ${RESPONSE}" > "${OUTPUT_FILE}"
    echo "RESULT_FILE:${OUTPUT_FILE}"
    exit 1
fi

# ② 轮询等待任务完成（最多 60 分钟）
MAX_WAIT=3600
ELAPSED=0
POLL_INTERVAL=30

echo "[HydroScribe Skill] 等待任务完成..."

while [ ${ELAPSED} -lt ${MAX_WAIT} ]; do
    sleep ${POLL_INTERVAL}
    ELAPSED=$((ELAPSED + POLL_INTERVAL))

    STATUS_RESPONSE=$(curl -s "${HYDROSCRIBE_API}/api/status" 2>/dev/null || echo '{}')
    ACTIVE_COUNT=$(echo "${STATUS_RESPONSE}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
tasks = data.get('orchestrator', {}).get('active_tasks', {})
print(len(tasks))
" 2>/dev/null || echo "0")

    if [ "${ACTIVE_COUNT}" = "0" ]; then
        echo "[HydroScribe Skill] 任务已完成 (耗时 ${ELAPSED}s)"
        break
    fi

    echo "[HydroScribe Skill] 进行中... (${ELAPSED}s / ${MAX_WAIT}s)"
done

# ③ 获取最终结果
BOOK_RESPONSE=$(curl -s "${HYDROSCRIBE_API}/api/books/${BOOK_ID}" 2>/dev/null || echo '{}')
echo "${BOOK_RESPONSE}" > "${OUTPUT_FILE}"

echo "[HydroScribe Skill] 结果已保存到: ${OUTPUT_FILE}"
echo "RESULT_FILE:${OUTPUT_FILE}"
