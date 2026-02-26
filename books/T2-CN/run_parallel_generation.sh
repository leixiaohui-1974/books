#!/bin/bash
# ============================================================
# T2-CN 多智能体并行图片生成
# 将42张正文图 + 14张扉页图 = 56张 分6批并行生成
# 预计时间：串行约70分钟 → 并行约15分钟
# ============================================================

set -e

# ─── 检查环境变量 ──────────────────────────────────────────
if [ -z "$NB_API_KEY" ]; then
    echo "❌ 未设置 NB_API_KEY"
    echo "   export NB_API_KEY='你的key'"
    echo "   export NB_API_BASE='https://api.nanobananaapi.ai/v1'"
    echo "   export NB_MODEL='nano-banana-pro'"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$SCRIPT_DIR/H/logs"
mkdir -p "$LOG_DIR"

echo "=================================================="
echo "  T2-CN 并行图片生成（6批同时进行）"
echo "  API: $NB_API_BASE"
echo "  模型: $NB_MODEL"
echo "=================================================="
echo ""

# ─── 6批并行任务 ──────────────────────────────────────────
# 批次1：引子 + 第1章（共5张）
echo "[批次1] 引子+第1章 → 后台启动..."
python3 "$SCRIPT_DIR/generate_images_api.py" \
    --chapter 00 --update-md > "$LOG_DIR/batch1_ch00.log" 2>&1 &
PID1=$!

python3 "$SCRIPT_DIR/generate_images_api.py" \
    --chapter 01 --update-md > "$LOG_DIR/batch1_ch01.log" 2>&1 &
PID1B=$!

# 批次2：第2-3章（共8张）
echo "[批次2] 第2-3章 → 后台启动..."
python3 "$SCRIPT_DIR/generate_images_api.py" \
    --chapter 02 --update-md > "$LOG_DIR/batch2_ch02.log" 2>&1 &
PID2=$!

python3 "$SCRIPT_DIR/generate_images_api.py" \
    --chapter 03 --update-md > "$LOG_DIR/batch2_ch03.log" 2>&1 &
PID2B=$!

# 批次3：第4-5章（共9张）
echo "[批次3] 第4-5章 → 后台启动..."
python3 "$SCRIPT_DIR/generate_images_api.py" \
    --chapter 04 --update-md > "$LOG_DIR/batch3_ch04.log" 2>&1 &
PID3=$!

python3 "$SCRIPT_DIR/generate_images_api.py" \
    --chapter 05 --update-md > "$LOG_DIR/batch3_ch05.log" 2>&1 &
PID3B=$!

# 批次4：第6-7章（共7张）
echo "[批次4] 第6-7章 → 后台启动..."
python3 "$SCRIPT_DIR/generate_images_api.py" \
    --chapter 06 --update-md > "$LOG_DIR/batch4_ch06.log" 2>&1 &
PID4=$!

python3 "$SCRIPT_DIR/generate_images_api.py" \
    --chapter 07 --update-md > "$LOG_DIR/batch4_ch07.log" 2>&1 &
PID4B=$!

# 批次5：第8-9章（共7张）
echo "[批次5] 第8-9章 → 后台启动..."
python3 "$SCRIPT_DIR/generate_images_api.py" \
    --chapter 08 --update-md > "$LOG_DIR/batch5_ch08.log" 2>&1 &
PID5=$!

python3 "$SCRIPT_DIR/generate_images_api.py" \
    --chapter 09 --update-md > "$LOG_DIR/batch5_ch09.log" 2>&1 &
PID5B=$!

# 批次6：第10-12章（共8张）
echo "[批次6] 第10-12章 → 后台启动..."
python3 "$SCRIPT_DIR/generate_images_api.py" \
    --chapter 10 --update-md > "$LOG_DIR/batch6_ch10.log" 2>&1 &
PID6=$!

python3 "$SCRIPT_DIR/generate_images_api.py" \
    --chapter 11 --update-md > "$LOG_DIR/batch6_ch11.log" 2>&1 &
PID6B=$!

python3 "$SCRIPT_DIR/generate_images_api.py" \
    --chapter 12 --update-md > "$LOG_DIR/batch6_ch12.log" 2>&1 &
PID6C=$!

echo ""
echo "全部12个后台任务已启动，等待完成..."
echo "实时日志：tail -f H/logs/batch*.log"
echo ""

# ─── 等待全部完成 ─────────────────────────────────────────
for pid in $PID1 $PID1B $PID2 $PID2B $PID3 $PID3B $PID4 $PID4B $PID5 $PID5B $PID6 $PID6B $PID6C; do
    wait $pid || true
done

echo ""
echo "=================================================="
echo "全部任务完成！"
echo ""

# ─── 统计结果 ─────────────────────────────────────────────
echo "📊 生成结果统计："
python3 "$SCRIPT_DIR/generate_images_api.py" --list

echo ""
echo "日志目录：H/logs/"
echo "=================================================="
