#!/bin/bash

# 韭菜公社新闻邮件发送脚本
# 使用resend mcp发送邮件

set -e

REPORT_FILE="$1"
EMAIL_TO="modeyangg@gmail.com"
EMAIL_SUBJECT="韭菜公社每日新闻汇总与投资机会 - $(date +"%Y-%m-%d")"

if [ -z "$REPORT_FILE" ] || [ ! -f "$REPORT_FILE" ]; then
    echo "错误: 报告文件不存在"
    exit 1
fi

echo "准备发送邮件..."
echo "收件人: $EMAIL_TO"
echo "主题: $EMAIL_SUBJECT"
echo "附件: $REPORT_FILE"

# 这里需要通过claude code调用resend mcp
# 我们将创建一个临时的claude code命令来发送邮件

exit 0
