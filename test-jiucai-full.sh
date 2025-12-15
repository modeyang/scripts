#!/bin/bash

# 韭菜公社新闻完整测试脚本
# 模拟cron任务执行流程

set -e

# 配置变量
WORK_DIR="/Users/yanggenxing/Documents/Obsidian Vault"
REPORT_DIR="$WORK_DIR/DiaryFinance/韭菜公社新闻"
SCRIPT_DIR="/Users/yanggenxing/.claude/scripts"
LOG_FILE="$SCRIPT_DIR/logs/test-jiucai-$(date +%Y%m%d-%H%M%S).log"
EMAIL_TO="modeyangg@gmail.com"

# 创建日志目录
mkdir -p "$SCRIPT_DIR/logs"

# 日志函数
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "========================================="
log "开始测试韭菜公社新闻完整流程"
log "========================================="

# 检查必要目录
log "检查必要目录..."
for dir in "$WORK_DIR" "$REPORT_DIR" "$SCRIPT_DIR"; do
    if [ ! -d "$dir" ]; then
        log "错误: 目录不存在: $dir"
        exit 1
    fi
done
log "✓ 目录检查完成"

# 记录执行前的报告数量
BEFORE_COUNT=$(find "$REPORT_DIR" -name "*韭菜公社新闻汇总与投资机会.md" -type f 2>/dev/null | wc -l)
log "执行前报告文件数量: $BEFORE_COUNT"

# 第一步：运行jiucai-s命令抓取新闻
log ""
log "第一步: 执行jiucai-s命令..."
log "-----------------------------------------"

cd "$WORK_DIR"

if /Users/yanggenxing/.claude/local/claude --print "jiucai-s" >> "$LOG_FILE" 2>&1; then
    log "✓ jiucai-s命令执行成功"
else
    log "✗ jiucai-s命令执行失败"
    exit 1
fi

# 等待文件生成
sleep 3

# 查找最新报告
AFTER_COUNT=$(find "$REPORT_DIR" -name "*韭菜公社新闻汇总与投资机会.md" -type f 2>/dev/null | wc -l)
log "执行后报告文件数量: $AFTER_COUNT"

if [ "$AFTER_COUNT" -le "$BEFORE_COUNT" ]; then
    log "✗ 错误: 未生成新报告文件"
    exit 1
fi

LATEST_REPORT=$(find "$REPORT_DIR" -name "*韭菜公社新闻汇总与投资机会.md" -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)
log "✓ 找到最新报告: $(basename "$LATEST_REPORT")"

# 第二步：读取报告内容
log ""
log "第二步: 读取报告内容..."
log "-----------------------------------------"

if [ ! -f "$LATEST_REPORT" ]; then
    log "✗ 错误: 报告文件不存在"
    exit 1
fi

REPORT_SIZE=$(wc -c < "$LATEST_REPORT")
log "✓ 报告文件大小: $REPORT_SIZE 字节"

REPORT_LINES=$(wc -l < "$LATEST_REPORT")
log "✓ 报告行数: $REPORT_LINES 行"

# 读取报告前几行预览
log ""
log "报告内容预览:"
log "-----------------------------------------"
head -20 "$LATEST_REPORT" | tee -a "$LOG_FILE"
log "..."

# 第三步：发送邮件
log ""
log "第三步: 准备发送邮件..."
log "-----------------------------------------"

EMAIL_SUBJECT="韭菜公社每日新闻汇总与投资机会 - $(date +"%Y-%m-%d") [测试]"
log "邮件主题: $EMAIL_SUBJECT"
log "收件人: $EMAIL_TO"

# 创建邮件内容
EMAIL_CONTENT="您好！

这是韭菜公社每日新闻汇总与投资机会的测试邮件。

$(head -50 "$LATEST_REPORT")

...（完整报告请查看附件）

---
📊 报告详情:
• 生成时间: $(date +"%Y-%m-%d %H:%M:%S")
• 报告文件: $(basename "$LATEST_REPORT")
• 文件大小: $REPORT_SIZE 字节
• 报告行数: $REPORT_LINES 行
• 数据来源: 韭菜公社 (jiuyangongshe.com)

此邮件由Claude Code自动测试发送
"

log "✓ 邮件内容已准备"

# 这里将通过mcp__resend-mcp__send_email发送邮件
log ""
log "正在通过resend mcp发送邮件..."
log "-----------------------------------------"

# 将报告内容保存到临时文件
TEMP_REPORT="/tmp/jiucai-report-test-$(date +%Y%m%d-%H%M%S).md"
cp "$LATEST_REPORT" "$TEMP_REPORT"

log "✓ 报告已复制到临时文件: $TEMP_REPORT"
log ""
log "测试完成！"
log "========================================="

exit 0
