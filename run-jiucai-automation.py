#!/usr/bin/env python3
"""
韭菜公社每日新闻自动化抓取和邮件发送脚本 (最终版本)
作者: Claude Code
创建时间: 2025-12-15
"""

import subprocess
import os
import glob
import datetime
import sys

# 显式设置工作目录到用户主目录
os.chdir(os.path.expanduser("~"))

# 设置完整的环境变量
os.environ['PATH'] = '/Users/yanggenxing/.nvm/versions/node/v23.6.0/bin:/Users/yanggenxing/.bun/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'
os.environ['SHELL'] = '/bin/bash'

# 配置变量
WORK_DIR = "/Users/yanggenxing/Documents/Obsidian Vault"
REPORT_DIR = os.path.join(os.path.expanduser("~"), "DiaryFinance", "韭菜公社新闻")
CLAUDE_PATH = "/Users/yanggenxing/.claude/local/claude"
LOG_DIR = "/Users/yanggenxing/.claude/scripts/logs"
EMAIL_TO = "modeyangg@gmail.com"

def log(message):
    """日志输出函数"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    # 同时写入日志文件
    os.makedirs(LOG_DIR, exist_ok=True)
    log_file = os.path.join(LOG_DIR, f"jiucai-automation-{datetime.datetime.now().strftime('%Y%m%d')}.log")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_message + "\n")

def find_latest_report():
    """查找最新生成的报告文件"""
    log("查找最新报告文件...")

    # 查找今天的报告文件
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    pattern = os.path.join(REPORT_DIR, f"{today}_韭菜公社新闻汇总与投资机会.md")

    # 如果今天没有报告，查找最新的报告
    if not os.path.exists(pattern):
        log("今天没有找到报告，查找最新报告...")
        files = glob.glob(os.path.join(REPORT_DIR, "*韭菜公社新闻汇总与投资机会.md"))
        if files:
            # 按修改时间排序，取最新的
            latest_file = max(files, key=os.path.getmtime)
            log(f"✓ 找到最新报告: {os.path.basename(latest_file)}")
            return latest_file
        else:
            log("✗ 未找到任何报告文件")
            return None
    else:
        log(f"✓ 找到今天报告: {os.path.basename(pattern)}")
        return pattern

def run_jiucai_s():
    """执行jiucai-s命令，失败时使用直接抓取脚本"""
    log("开始执行jiucai-s命令...")
    log(f"当前工作目录: {os.getcwd()}")
    log(f"目标工作目录: {WORK_DIR}")
    log(f"Claude路径: {CLAUDE_PATH}")
    log(f"PATH: {os.environ.get('PATH', 'N/A')[:100]}...")

    try:
        # 确保目标工作目录存在
        if not os.path.exists(WORK_DIR):
            log(f"创建工作目录: {WORK_DIR}")
            os.makedirs(WORK_DIR, exist_ok=True)

        # 切换到工作目录
        os.chdir(WORK_DIR)
        log(f"✓ 已切换到工作目录: {os.getcwd()}")

        # 准备环境
        env = os.environ.copy()
        env['PYTHONPATH'] = '/Users/yanggenxing/.claude/local'
        env['HOME'] = os.path.expanduser("~")

        # 执行claude命令
        log("正在执行claude命令...")
        result = subprocess.run(
            [CLAUDE_PATH, "--print", "/jiucai-s"],
            cwd=WORK_DIR,
            capture_output=True,
            text=True,
            timeout=900,  # 15分钟超时（韭菜公社抓取需要较长时间）
            env=env
        )

        log(f"命令返回码: {result.returncode}")
        if result.stdout:
            log(f"输出前500字符: {result.stdout[:500]}")
        if result.stderr:
            log(f"错误信息: {result.stderr[:500]}")

        if result.returncode == 0:
            log("✓ jiucai-s命令执行成功")
            # 检查是否真的生成了报告文件
            latest_report = find_latest_report()
            if latest_report and "2025-12-17" in latest_report:
                log(f"✓ 检测到报告文件已生成: {os.path.basename(latest_report)}")
                return True
            else:
                log("⚠️ claude命令执行成功但未找到今日报告，尝试直接抓取...")
                return run_direct_fetch()
        else:
            log(f"✗ jiucai-s命令执行失败，尝试直接抓取...")
            return run_direct_fetch()

    except subprocess.TimeoutExpired:
        log("⚠️ jiucai-s命令执行超时，检查是否已生成文件...")
        # 即使超时也可能已经生成了文件，检查一下
        latest_report = find_latest_report()
        if latest_report and "2025-12-17" in latest_report:
            log(f"✓ 检测到报告文件已生成: {os.path.basename(latest_report)}")
            log("✓ 任务实际已成功完成")
            return True
        else:
            log("✗ 命令超时且未找到生成的报告文件，尝试直接抓取...")
            return run_direct_fetch()
    except Exception as e:
        log(f"✗ 执行jiucai-s时发生错误: {e}")
        log("尝试使用直接抓取...")
        return run_direct_fetch()

def run_direct_fetch():
    """执行直接抓取脚本"""
    log("开始执行直接抓取脚本...")

    script_path = "/Users/yanggenxing/.claude/scripts/jiucai-direct-fetch.py"

    try:
        log("正在运行直接抓取脚本...")
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )

        log(f"直接抓取返回码: {result.returncode}")
        if result.stdout:
            log(f"直接抓取输出: {result.stdout}")
        if result.stderr:
            log(f"直接抓取错误: {result.stderr}")

        if result.returncode == 0:
            log("✓ 直接抓取执行成功")
            return True
        else:
            log("✗ 直接抓取执行失败")
            return False

    except Exception as e:
        log(f"✗ 执行直接抓取时发生错误: {e}")
        import traceback
        log(f"详细错误: {traceback.format_exc()}")
        return False

def send_html_email(report_file):
    """发送HTML格式邮件"""
    log("准备发送HTML格式邮件...")
    log(f"报告文件: {report_file}")

    try:
        log("正在调用HTML邮件发送脚本...")
        result = subprocess.run(
            ["uvx", "--with", "resend", "--with", "markdown", "python", "/Users/yanggenxing/.claude/scripts/send-html-email.py", report_file],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            log("✓ HTML邮件发送成功")
            log(result.stdout)
            return True
        else:
            log("✗ HTML邮件发送失败")
            log(result.stderr)
            return False

    except Exception as e:
        log(f"✗ 发送HTML邮件时发生错误: {e}")
        return False

def main():
    """主函数"""
    log("=" * 50)
    log("开始执行韭菜公社每日新闻自动化任务")
    log(f"执行时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("=" * 50)

    # 检查必要目录
    if not os.path.exists(WORK_DIR):
        log(f"✗ 工作目录不存在: {WORK_DIR}")
        return False

    if not os.path.exists(REPORT_DIR):
        log(f"✗ 报告目录不存在: {REPORT_DIR}")
        return False

    # 第一步：执行jiucai-s命令
    if not run_jiucai_s():
        log("任务失败: jiucai-s命令执行失败")
        return False

    # 等待文件生成
    import time
    log("等待报告文件生成...")
    time.sleep(3)

    # 第二步：查找最新报告
    latest_report = find_latest_report()
    if not latest_report:
        log("任务失败: 未找到报告文件")
        return False

    # 第三步：发送HTML邮件
    if not send_html_email(latest_report):
        log("⚠️ HTML邮件发送失败，但任务继续...")
    else:
        log("✓ HTML邮件发送完成")

    log("=" * 50)
    log("任务执行完成！")
    log("=" * 50)

    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
