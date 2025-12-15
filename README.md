# 韭菜公社每日新闻自动化系统

## 概述

本系统实现了每天早上8点自动抓取韭菜公社新闻、分析投资机会并发送邮件到指定邮箱的完整自动化流程。

## 系统架构

```
cron定时任务 (每天8:00)
    ↓
Python自动化脚本
    ↓
claude code命令 (/jiucai-s)
    ↓
新闻抓取与分析
    ↓
生成Markdown报告
    ↓
resend mcp发送邮件
    ↓
modeyangg@gmail.com
```

## 文件结构

```
/Users/yanggenxing/.claude/scripts/
├── README.md                           # 本文档
├── run-jiucai-automation.py            # Python自动化脚本（主入口）
├── run-jiucai-with-email.sh            # Bash脚本（备用方案）
├── test-jiucai-full.sh                 # 测试脚本
├── execute-jiucai-and-send-email.md    # 执行指南
├── logs/                               # 日志目录
│   ├── jiucai-automation-YYYYMMDD.log  # 每日执行日志
│   └── jiucai-cron.log                 # Cron任务日志
└── /tmp/
    ├── jiucai-email-info-*.txt         # 邮件信息临时文件
    └── jiucai-email-body-*.txt         # 邮件内容临时文件
```

## 安装配置

### 1. 脚本权限设置
```bash
chmod +x /Users/yanggenxing/.claude/scripts/run-jiucai-automation.py
chmod +x /Users/yanggenxing/.claude/scripts/run-jiucai-with-email.sh
chmod +x /Users/yanggenxing/.claude/scripts/test-jiucai-full.sh
```

### 2. Cron任务配置
```bash
# 查看当前cron任务
crontab -l

# 安装cron任务
crontab /tmp/jiucai-cron-v2

# 验证安装
crontab -l
```

### 3. 环境检查
确保以下组件可用：
- ✅ claude code: `/Users/yanggenxing/.claude/local/claude`
- ✅ Python3: `/usr/bin/python3`
- ✅ 工作目录: `/Users/yanggenxing/Documents/Obsidian Vault`
- ✅ 报告目录: `/Users/yanggenxing/Documents/Obsidian Vault/DiaryFinance/韭菜公社新闻`

## 使用方法

### 自动执行（推荐）
系统已配置为每天早上8:00自动执行，无需手动干预。

### 手动测试
```bash
# 方法1: 运行Python脚本
python3 /Users/yanggenxing/.claude/scripts/run-jiucai-automation.py

# 方法2: 运行Bash脚本
/Users/yanggenxing/.claude/scripts/test-jiucai-full.sh

# 方法3: 在claude code中直接执行
/jiucai-s
```

### 手动发送邮件
如果需要手动发送邮件，使用以下resend mcp命令：
```python
mcp__resend-mcp__send_email(
    to="modeyangg@gmail.com",
    subject="韭菜公社每日新闻汇总与投资机会 - 2025-12-13",
    content="邮件内容...",
    attachments=[{"filename": "报告文件名.md", "localPath": "/path/to/report.md"}]
)
```

## 日志查看

### 查看执行日志
```bash
# 查看今日日志
tail -f /Users/yanggenxing/.claude/scripts/logs/jiucai-automation-$(date +%Y%m%d).log

# 查看cron任务日志
tail -f /Users/yanggenxing/.claude/scripts/logs/jiucai-cron.log

# 查看所有日志文件
ls -lah /Users/yanggenxing/.claude/scripts/logs/
```

### 日志级别
- ✅ 成功执行
- ⚠️ 警告（不影响主流程）
- ✗ 错误（需要关注）
- 📊 统计信息

## 故障排除

### 问题1: Cron任务未执行
```bash
# 检查cron服务状态
sudo launchctl list | grep cron

# 手动触发cron任务
crontab -l
# 检查任务是否在列表中

# 查看cron日志
grep CRON /var/log/system.log
```

### 问题2: 报告文件未生成
```bash
# 检查工作目录权限
ls -la /Users/yanggenxing/Documents/Obsidian Vault/

# 检查报告目录
ls -la /Users/yanggenxing/Documents/Obsidian Vault/DiaryFinance/韭菜公社新闻/

# 手动执行测试
python3 /Users/yanggenxing/.claude/scripts/run-jiucai-automation.py
```

### 问题3: 邮件发送失败
```bash
# 检查resend mcp是否可用
# 在claude code中测试：
mcp__resend-mcp__send_email(to="test@example.com", subject="Test", content="Test")

# 检查临时文件
ls -la /tmp/jiucai-email-*.txt
```

### 问题4: 权限问题
```bash
# 修复脚本权限
chmod +x /Users/yanggenxing/.claude/scripts/*.sh
chmod +x /Users/yanggenxing/.claude/scripts/*.py

# 修复目录权限
chmod -R 755 /Users/yanggenxing/.claude/scripts/
chmod -R 755 /Users/yanggenxing/.claude/scripts/logs/
```

## 定制配置

### 修改执行时间
编辑cron任务配置：
```bash
crontab -e
# 修改行: 0 8 * * *
# 格式: 分 时 日 月 星期
# 示例: 每天7:30执行 -> 30 7 * * *
```

### 修改收件人
编辑 `run-jiucai-automation.py`：
```python
EMAIL_TO = "your-email@example.com"
```

### 修改报告保存目录
编辑 `run-jiucai-automation.py`：
```python
REPORT_DIR = "/your/custom/path"
```

## 监控和维护

### 每日检查清单
- [ ] 检查cron任务是否执行
- [ ] 查看执行日志
- [ ] 验证报告文件生成
- [ ] 确认邮件发送成功

### 每周维护
- [ ] 清理7天前的日志文件（自动）
- [ ] 检查磁盘空间使用
- [ ] 验证报告文件完整性

### 每月检查
- [ ] 检查所有脚本权限
- [ ] 更新依赖组件
- [ ] 清理临时文件

## 性能优化

### 执行时间
- 正常执行时间: 3-5分钟
- 网络较慢时: 5-10分钟
- 超时设置: 15分钟

### 资源使用
- CPU: < 50%
- 内存: < 500MB
- 磁盘: 每次执行约1-2MB

## 安全注意事项

1. **文件权限**: 确保脚本文件权限设置为600（仅所有者可读写）
2. **敏感信息**: 避免在脚本中硬编码敏感信息
3. **日志安全**: 日志文件可能包含敏感信息，定期清理
4. **网络访问**: 确保防火墙允许必要的网络访问

## 技术支持

如遇到问题，请检查：
1. 系统日志：`/var/log/system.log`
2. 执行日志：`/Users/yanggenxing/.claude/scripts/logs/`
3. 错误信息：根据日志中的错误提示进行排查

## 更新日志

### v1.0 (2025-12-13)
- 初始版本发布
- 实现基本的新闻抓取和邮件发送功能
- 配置每日8点自动执行
