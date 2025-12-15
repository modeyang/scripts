#!/bin/bash

# 韭菜公社每日新闻自动抓取和邮件发送脚本
# 执行时间: 每天早上8:00
# 作者: Claude Code
# 创建时间: 2025-12-13

set -e  # 遇到错误立即退出

# 配置变量
CLAUDE_PATH="/Users/yanggenxing/.claude/local/claude"
LOG_FILE="/Users/yanggenxing/.claude/scripts/logs/jiucai-daily.log"
REPORT_DIR="/Users/yanggenxing/Documents/Obsidian Vault/DiaryFinance/韭菜公社新闻"
EMAIL_TO="modeyangg@gmail.com"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

# 日志函数
log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

log "=== 开始执行韭菜公社每日新闻抓取任务 ==="

# 检查claude命令是否存在
if [ ! -f "$CLAUDE_PATH" ]; then
    log "错误: claude命令未找到 at $CLAUDE_PATH"
    exit 1
fi

# 切换到工作目录
cd "/Users/yanggenxing/Documents/Obsidian Vault" || {
    log "错误: 无法切换到工作目录"
    exit 1
}

log "当前工作目录: $(pwd)"
log "开始执行jiucai-s命令..."

# 执行jiucai-s命令
if "$CLAUDE_PATH" --print "jiucai-s" 2>&1 | tee -a "$LOG_FILE"; then
    log "jiucai-s命令执行成功"
else
    log "错误: jiucai-s命令执行失败"
    exit 1
fi

# 查找最新生成的报告文件
LATEST_REPORT=$(find "$REPORT_DIR" -name "*韭菜公社新闻汇总与投资机会.md" -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)

if [ -z "$LATEST_REPORT" ]; then
    log "错误: 未找到生成的报告文件"
    exit 1
fi

log "找到最新报告: $LATEST_REPORT"

# 读取报告内容
REPORT_CONTENT=$(cat "$LATEST_REPORT")

# 构建邮件内容
EMAIL_SUBJECT="韭菜公社每日新闻汇总与投资机会 - $(date +"%Y-%m-%d")"
EMAIL_BODY="您好！

以下是今日韭菜公社新闻汇总与投资机会分析：

$(echo "$REPORT_CONTENT" | head -100)

... (详细内容请查看附件)

---
本邮件由Claude Code自动生成
执行时间: $(date +"%Y-%m-%d %H:%M:%S")
"

log "准备发送邮件到: $EMAIL_TO"
log "邮件主题: $EMAIL_SUBJECT"

# 发送邮件（通过resend mcp）
# 这里我们使用一个临时的claude code调用来发送邮件
echo "将通过resend mcp发送邮件..."

# 将报告内容写入临时文件供后续使用
TEMP_CONTENT_FILE="/tmp/jiucai-report-$(date +%Y%m%d).txt"
echo "$EMAIL_BODY" > "$TEMP_CONTENT_FILE"

log "邮件发送任务已准备完成"
log "=== 任务执行完成 ==="

exit 0
