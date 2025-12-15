#!/bin/bash

# 韭菜公社每日新闻抓取并发送邮件的完整脚本
# 执行时间: 每天早上8:00

set -e

# 配置变量
WORK_DIR="/Users/yanggenxing/Documents/Obsidian Vault"
REPORT_DIR="$WORK_DIR/DiaryFinance/韭菜公社新闻"
CLAUDE_PATH="/Users/yanggenxing/.claude/local/claude"
LOG_FILE="/Users/yanggenxing/.claude/scripts/logs/jiucai-daily-$(date +%Y%m%d).log"
EMAIL_TO="modeyangg@gmail.com"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

# 日志函数
log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

log "========================================="
log "开始执行韭菜公社每日新闻抓取任务"
log "时间: $(date)"
log "========================================="

# 检查claude命令
if [ ! -f "$CLAUDE_PATH" ]; then
    log "错误: claude命令未找到"
    exit 1
fi

# 切换到工作目录
cd "$WORK_DIR" || {
    log "错误: 无法切换到工作目录"
    exit 1
}

log "当前工作目录: $(pwd)"

# 记录执行前的报告文件
BEFORE_REPORTS=$(find "$REPORT_DIR" -name "*韭菜公社新闻汇总与投资机会.md" -type f 2>/dev/null | wc -l)
log "执行前报告文件数量: $BEFORE_REPORTS"

# 执行jiucai-s命令
log "开始执行jiucai-s命令..."
if "$CLAUDE_PATH" --print "jiucai-s" >> "$LOG_FILE" 2>&1; then
    log "✓ jiucai-s命令执行成功"
else
    log "✗ 错误: jiucai-s命令执行失败"
    exit 1
fi

# 查找最新生成的报告文件
sleep 2  # 等待文件写入完成
LATEST_REPORT=$(find "$REPORT_DIR" -name "*韭菜公社新闻汇总与投资机会.md" -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)

if [ -z "$LATEST_REPORT" ]; then
    log "✗ 错误: 未找到生成的报告文件"
    exit 1
fi

log "✓ 找到最新报告: $LATEST_REPORT"

# 读取报告内容（前2000字符用于邮件预览）
REPORT_CONTENT=$(head -c 2000 "$LATEST_REPORT")

# 构建邮件内容
EMAIL_SUBJECT="韭菜公社每日新闻汇总与投资机会 - $(date +"%Y-%m-%d")"

# 创建临时文件存储邮件内容
TEMP_EMAIL_FILE="/tmp/jiucai-email-$(date +%Y%m%d-%H%M%S).txt"

cat > "$TEMP_EMAIL_FILE" << EOF
您好！

以下是今日韭菜公社新闻汇总与投资机会分析：

$REPORT_CONTENT

...(完整报告请查看附件)

---
📊 报告详情:
• 生成时间: $(date +"%Y-%m-%d %H:%M:%S")
• 报告文件: $(basename "$LATEST_REPORT")
• 数据来源: 韭菜公社 (jiuyangongshe.com)

此邮件由Claude Code自动发送
EOF

log "✓ 邮件内容已准备"
log "准备发送邮件到: $EMAIL_TO"

# 输出邮件发送命令（将在下一步执行）
echo "EMAIL_CONTENT_FILE=$TEMP_EMAIL_FILE" >> "$LOG_FILE"
echo "EMAIL_SUBJECT=$EMAIL_SUBJECT" >> "$LOG_FILE"
echo "REPORT_FILE=$LATEST_REPORT" >> "$LOG_FILE"

log "✓ 任务执行完成，准备发送邮件"
log "========================================="

# 导出变量供父进程使用
export EMAIL_CONTENT_FILE="$TEMP_EMAIL_FILE"
export EMAIL_SUBJECT="$EMAIL_SUBJECT"
export REPORT_FILE="$LATEST_REPORT"

exit 0
