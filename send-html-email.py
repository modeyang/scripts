#!/usr/bin/env python3
"""
HTML邮件发送脚本
"""

import resend
import datetime
import sys
import os
import base64
import markdown

def send_html_email(report_file):
    """发送HTML格式的韭菜公社新闻邮件"""
    # 设置 API 密钥
    resend.api_key = "re_WcRR9QLz_DQcAvpzy6HhXL7K2r64iG7NS"

    try:
        # 读取报告文件内容
        with open(report_file, 'r', encoding='utf-8') as f:
            report_content = f.read()
        print(f"✅ 报告文件读取成功，大小: {len(report_content):,} 字节")

        # 准备邮件
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        subject = f"韭菜公社每日新闻汇总与投资机会 - {today}"

        # 取报告前2500字符作为邮件预览
        preview_content = report_content[:2500]

        # 转换markdown为HTML
        try:
            md = markdown.Markdown(extensions=['tables', 'fenced_code'])
            preview_html = md.convert(preview_content)

            # 构建HTML邮件内容（带样式）
            html_parts = []
            html_parts.append('<!DOCTYPE html>')
            html_parts.append('<html>')
            html_parts.append('<head>')
            html_parts.append('    <meta charset="utf-8">')
            html_parts.append('    <style>')
            html_parts.append('        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }')
            html_parts.append('        h1, h2, h3 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }')
            html_parts.append('        h1 { font-size: 24px; }')
            html_parts.append('        h2 { font-size: 20px; margin-top: 30px; }')
            html_parts.append('        h3 { font-size: 18px; margin-top: 25px; }')
            html_parts.append('        a { color: #3498db; text-decoration: none; }')
            html_parts.append('        a:hover { text-decoration: underline; }')
            html_parts.append('        ul, ol { padding-left: 20px; }')
            html_parts.append('        li { margin-bottom: 8px; }')
            html_parts.append('        strong { color: #e74c3c; font-weight: 600; }')
            html_parts.append('        hr { border: none; height: 2px; background: linear-gradient(to right, #3498db, #2ecc71); margin: 30px 0; }')
            html_parts.append('        .footer { background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 30px; font-size: 14px; color: #666; }')
            html_parts.append('    </style>')
            html_parts.append('</head>')
            html_parts.append('<body>')
            html_parts.append('    <div style="background-color: #3498db; color: white; padding: 20px; text-align: center; margin: -20px -20px 30px -20px;">')
            html_parts.append('        <h1 style="color: white; border: none; margin: 0; padding: 0;">📊 韭菜公社每日新闻汇总与投资机会</h1>')
            html_parts.append(f'        <p style="margin: 10px 0 0 0; font-size: 16px;">{today}</p>')
            html_parts.append('    </div>')
            html_parts.append('    <div>')
            html_parts.append(f'        {preview_html}')
            html_parts.append('    </div>')
            html_parts.append('    <div class="footer">')
            html_parts.append('        <h3>📋 报告详情</h3>')
            html_parts.append('        <ul style="list-style: none; padding: 0;">')
            html_parts.append(f'            <li>• 生成时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</li>')
            html_parts.append(f'            <li>• 报告文件: {os.path.basename(report_file)}</li>')
            html_parts.append(f'            <li>• 文件大小: {len(report_content):,} 字节</li>')
            html_parts.append('            <li>• 数据来源: 韭菜公社 (jiuyangongshe.com)</li>')
            html_parts.append('        </ul>')
            html_parts.append('        <p style="margin-top: 15px; font-style: italic;">此邮件由Claude Code自动发送</p>')
            html_parts.append('    </div>')
            html_parts.append('</body>')
            html_parts.append('</html>')

            html_content = '\n'.join(html_parts)
            print("✅ Markdown转换为HTML成功")
        except Exception as e:
            print(f"⚠️ HTML转换失败: {e}")
            html_content = f"<p>{preview_content}</p>"

        # 文本版本作为备用
        text_body = f"""您好！

以下是今日韭菜公社新闻汇总与投资机会分析：

{preview_content}

...(完整报告请查看附件)

---
📊 报告详情:
• 生成时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
• 报告文件: {os.path.basename(report_file)}
• 文件大小: {len(report_content):,} 字节
• 数据来源: 韭菜公社 (jiuyangongshe.com)

此邮件由Claude Code自动发送
"""

        # 准备附件（Base64编码）
        try:
            with open(report_file, 'rb') as f:
                file_content = f.read()
            file_base64 = base64.b64encode(file_content).decode('utf-8')
            attachment = {
                "filename": os.path.basename(report_file),
                "content": file_base64,
                "type": "text/markdown"
            }
            print(f"✅ 附件准备完成: {attachment['filename']} ({len(file_content):,} 字节)")
        except Exception as e:
            print(f"⚠️ 附件准备失败: {e}")
            attachment = None

        # 发送HTML邮件
        email_params = {
            "from": "韭菜公社新闻 <onboarding@resend.dev>",
            "to": ["modeyangg@gmail.com"],
            "subject": subject,
            "html": html_content,
            "text": text_body
        }

        # 添加附件
        if attachment:
            email_params["attachments"] = [attachment]

        print("📧 正在发送HTML格式邮件...")

        response = resend.Emails.send(email_params)

        if response and "id" in response:
            print(f"✅ HTML邮件发送成功！邮件ID: {response['id']}")
            return True
        else:
            print(f"❌ HTML邮件发送失败，响应: {response}")
            return False

    except Exception as e:
        print(f"❌ 发送HTML邮件时发生错误: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python send-html-email.py <report_file>")
        sys.exit(1)

    report_file = sys.argv[1]
    success = send_html_email(report_file)
    sys.exit(0 if success else 1)
