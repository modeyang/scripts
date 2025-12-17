#!/usr/bin/env python3
"""
韭菜公社直接抓取脚本
使用 jina.ai 服务直接抓取韭菜公社网站内容
"""

import urllib.request
import urllib.error
import re
import datetime
import os
import json
from typing import List, Dict, Any

def fetch_jiucai_content():
    """使用jina.ai获取韭菜公社网站内容"""
    url = "https://r.jina.ai/https://www.jiuyangongshe.com/"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"获取网站内容失败: {e}")
        return None

def parse_news_content(content: str) -> List[Dict[str, Any]]:
    """解析新闻内容"""
    news_items = []

    # 使用正则表达式查找新闻条目
    # 格式: 2025-12-17 HH:MM:SS 看好/中性/看空 新闻内容...
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(看好|中性|看空)\s+(.*?)(?=\d{4}-\d{2}-\d{2}|\Z)'

    matches = re.findall(pattern, content, re.DOTALL)

    for match in matches:
        timestamp_str, sentiment, content_text = match

        # 清理内容文本
        content_text = content_text.strip()

        # 移除多余的数字和符号
        content_text = re.sub(r'\s+\d+\s+\d+\s+\d+\s+\*?\s*\d*\s*$', '', content_text)
        content_text = re.sub(r'\s+', ' ', content_text)

        if len(content_text) > 10:  # 过滤太短的内容
            news_items.append({
                'timestamp': timestamp_str,
                'sentiment': sentiment,
                'content': content_text,
                'date': timestamp_str.split(' ')[0]
            })

    return news_items

def analyze_news_by_sector(news_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """按板块分析新闻"""
    sectors = {
        '航天军工': ['航天', '军工', '火箭', '卫星', '导弹', '航空'],
        'AI算力': ['AI', '算力', '加速卡', '智算', 'GPU', '芯片'],
        '新能源': ['新能源', '电池', '光伏', '风电', '储能'],
        '生物医药': ['医药', '生物', '疫苗', '制药'],
        '消费电子': ['手机', '电脑', '芯片', '半导体'],
        '并购重组': ['并购', '重组', '控股', '收购', '股权转让'],
        '高股息': ['分红', '股息', '派息', '权益分派'],
        '数字经济': ['数字', '钱包', '支付', '区块链']
    }

    sector_analysis = {}

    for sector, keywords in sectors.items():
        sector_news = []
        for news in news_items:
            content_lower = news['content'].lower()
            if any(keyword.lower() in content_lower for keyword in keywords):
                sector_news.append(news)

        if sector_news:
            sector_analysis[sector] = {
                'count': len(sector_news),
                'news': sector_news[:5],  # 最多显示5条
                'sentiment_score': sum(1 for n in sector_news if n['sentiment'] == '看好') - sum(1 for n in sector_news if n['sentiment'] == '看空')
            }

    return sector_analysis

def generate_investment_report(news_items: List[Dict[str, Any]], sector_analysis: Dict[str, Any]) -> str:
    """生成投资报告"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    report = f"""# [{today}] 韭菜公社新闻汇总与投资机会

**抓取时间**: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
**时间范围**: 最近24小时
**新闻总数**: {len(news_items)}条
**涉及板块**: {len(sector_analysis)}个

## 🔥 热点板块排行

"""

    # 按新闻数量排序板块
    sorted_sectors = sorted(sector_analysis.items(), key=lambda x: x[1]['count'], reverse=True)

    for i, (sector, data) in enumerate(sorted_sectors[:5], 1):
        sentiment_icon = "🚀" if data['sentiment_score'] > 0 else "⚠️" if data['sentiment_score'] < 0 else "📊"
        report += f"### {i}. {sector} {sentiment_icon}\n"
        report += f"- **新闻数量**: {data['count']}条\n"
        report += f"- **情绪指数**: {'积极' if data['sentiment_score'] > 0 else '消极' if data['sentiment_score'] < 0 else '中性'}\n"

        # 添加重要新闻
        if data['news']:
            report += "- **核心新闻**:\n"
            for news in data['news'][:2]:
                report += f"  - {news['sentiment']} {news['content'][:100]}{'...' if len(news['content']) > 100 else ''}\n"
        report += "\n"

    report += f"""## 📈 投资策略建议

### 短期机会 (1-3天)
1. **重点关注**: {sorted_sectors[0][0] if sorted_sectors else '无'} - 板块热度最高
2. **逢低布局**: {sorted_sectors[1][0] if len(sorted_sectors) > 1 else '无'} - 情绪积极但可能有回调

### 中期趋势 (1-2周)
"""

    for sector, data in sorted_sectors[:3]:
        if data['sentiment_score'] > 0:
            report += f"- **{sector}**: 持续看好，建议关注龙头标的\n"
        elif data['sentiment_score'] < 0:
            report += f"- **{sector}**: 短期承压，建议谨慎操作\n"

    report += f"""
### 风险提示
- 市场情绪变化较快，注意及时止盈止损
- 关注宏观数据和政策变化
- 控制仓位，分散投资风险

---
*报告生成时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
*数据来源: 韭菜公社 (jiuyangongshe.com)*
"""

    return report

def main():
    """主函数"""
    print("开始抓取韭菜公社新闻...")

    # 获取网站内容
    content = fetch_jiucai_content()
    if not content:
        print("❌ 无法获取网站内容")
        return False

    print("✅ 网站内容获取成功")

    # 解析新闻
    news_items = parse_news_content(content)
    print(f"✅ 解析到 {len(news_items)} 条新闻")

    if not news_items:
        print("❌ 未找到有效新闻内容")
        return False

    # 按板块分析
    sector_analysis = analyze_news_by_sector(news_items)
    print(f"✅ 分析了 {len(sector_analysis)} 个板块")

    # 生成报告
    report = generate_investment_report(news_items, sector_analysis)

    # 保存报告
    output_dir = os.path.expanduser("~/DiaryFinance/韭菜公社新闻")
    os.makedirs(output_dir, exist_ok=True)

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}_韭菜公社新闻汇总与投资机会.md"
    filepath = os.path.join(output_dir, filename)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ 报告已保存至: {filepath}")
        return True
    except Exception as e:
        print(f"❌ 保存报告失败: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)