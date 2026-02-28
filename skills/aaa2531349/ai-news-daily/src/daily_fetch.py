"""
AI News Aggregator - 国内 AI 媒体抓取（改进版）
优化点：
1. 更严格的AI相关性判断（标题必须含AI关键词）
2. 过滤综合早报/晨报类文章
3. 抓取正文获取真实摘要
4. 按AI相关度排序
"""
import requests
import feedparser
import json
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# 国内 AI 媒体源
SOURCES = {
    "qbitai": {
        "name": "量子位",
        "rss": "https://www.qbitai.com/feed",
        "type": "rss"
    },
    "jiqizhixin": {
        "name": "机器之心",
        "rss": "https://www.jiqizhixin.com/rss",
        "type": "rss"
    },
    "infoq": {
        "name": "InfoQ",
        "rss": "https://www.infoq.cn/feed",
        "type": "rss"
    },
    "36kr": {
        "name": "36氪",
        "rss": "https://36kr.com/feed",
        "type": "rss"
    },
    "leiphone": {
        "name": "雷锋网",
        "rss": "https://www.leiphone.com/feed",
        "type": "rss"
    },
    "tmtpost": {
        "name": "钛媒体",
        "rss": "https://www.tmtpost.com/feed",
        "type": "rss"
    },
    "aiera": {
        "name": "新智元",
        "url": "https://www.aiera.com.cn",
        "type": "web"
    }
}

# AI核心关键词 - 标题必须包含这些才算AI新闻
AI_CORE_KEYWORDS = [
    "AI", "人工智能", "机器学习", "深度学习", "大模型", "LLM", 
    "神经网络", "GPT", "ChatGPT", "Claude", "OpenAI", "文心一言", 
    "通义千问", "智谱", "GLM", "月之暗面", "Kimi", "DeepSeek", 
    "人形机器人", "具身智能", "自动驾驶", "无人驾驶", "算力", 
    "芯片", "英伟达", "NVIDIA", "GPU", "TPU", "AI芯片",
    "生成式AI", "AIGC", "多模态", "Agent", "智能体", "AGI"
]

# 次要关键词 - 用于辅助判断
AI_SECONDARY_KEYWORDS = [
    "百度", "阿里", "腾讯", "字节", "华为", "小米", "商汤", 
    "旷视", "依图", "云从", "寒武纪", "地平线", "融资", "IPO", "财报"
]

# 需要过滤的标题模式（综合早报、娱乐八卦等）
FILTER_PATTERNS = [
    r'早报|晨报|晚报|日报',  # 综合新闻
    r'要闻提示|今日头条',  # 杂烩新闻
    r'降价|被骂|骂惨',  # 情绪标题
    r'游戏|电竞|手游',  # 游戏新闻（除非明确AI相关）
    r'明星|娱乐|八卦',  # 娱乐新闻
]


def is_ai_related(title, summary=""):
    """
    严格检查是否与 AI 相关
    要求：标题必须包含核心AI关键词
    """
    title_lower = title.lower()
    
    # 先过滤掉明显不是AI新闻的标题模式
    for pattern in FILTER_PATTERNS:
        if re.search(pattern, title):
            # 但如果同时有强AI关键词，保留
            has_strong_ai = any(kw.lower() in title_lower for kw in AI_CORE_KEYWORDS)
            if not has_strong_ai:
                return False, 0
    
    # 标题必须包含核心AI关键词
    core_matches = sum(1 for kw in AI_CORE_KEYWORDS if kw.lower() in title_lower)
    
    if core_matches == 0:
        return False, 0
    
    # 计算相关度分数
    score = core_matches * 10
    
    # 次要关键词加分
    summary_lower = summary.lower()
    for kw in AI_SECONDARY_KEYWORDS:
        if kw.lower() in title_lower:
            score += 3
        if kw.lower() in summary_lower:
            score += 1
    
    return True, score


def is_yesterday(published_str):
    """检查是否是昨天的文章"""
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(published_str)
        yesterday = datetime.now() - timedelta(days=1)
        return dt.date() == yesterday.date()
    except:
        # 如果日期解析失败，默认包含（让内容筛选来决定）
        return True


def fetch_article_content(url, source_name):
    """
    抓取文章正文，提取真实摘要
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=15)
        resp.encoding = resp.apparent_encoding or 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # 移除脚本和样式
        for script in soup(["script", "style", "nav", "header", "footer"]):
            script.decompose()
        
        # 尝试找文章正文
        content = ""
        
        # 常见文章容器选择器
        selectors = [
            'article', '.article-content', '.post-content', '.entry-content',
            '#article-content', '.content-detail', '.article-detail',
            '[class*="content"]', '[class*="article"]'
        ]
        
        for selector in selectors:
            container = soup.select_one(selector)
            if container:
                # 获取段落文本
                paragraphs = container.find_all(['p', 'div'])
                texts = []
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    # 过滤短文本和导航类内容
                    if len(text) > 30 and not any(x in text for x in ['Copyright', '版权', '免责声明', '相关阅读', '推荐阅读']):
                        texts.append(text)
                
                if texts:
                    content = ' '.join(texts[:5])  # 取前5段
                    break
        
        # 如果没找到，取整个body的文本
        if not content:
            body = soup.find('body')
            if body:
                content = body.get_text(separator=' ', strip=True)
        
        # 清理并截取
        content = re.sub(r'\s+', ' ', content)
        content = content[:800]  # 先多取一点，后面再精修
        
        return content
        
    except Exception as e:
        print(f"    抓取正文失败: {e}")
        return ""


def extract_summary(content, max_length=250):
    """
    从正文提取简洁摘要
    """
    if not content:
        return ""
    
    # 清理内容
    content = content.strip()
    
    # 如果内容较短，直接返回
    if len(content) <= max_length:
        return content
    
    # 尝试在句子边界截断
    sentences = re.split(r'([。！？\.\n])', content)
    summary = ""
    for i in range(0, len(sentences), 2):
        sentence = sentences[i]
        punct = sentences[i+1] if i+1 < len(sentences) else ""
        candidate = summary + sentence + punct
        if len(candidate) > max_length:
            break
        summary = candidate
    
    # 如果没找到句子边界，直接截断
    if not summary:
        summary = content[:max_length-3] + "..."
    
    return summary.strip()


def fetch_rss(source_key, source_config):
    """抓取 RSS 源"""
    items = []
    try:
        print(f"正在抓取 {source_config['name']}...")
        feed = feedparser.parse(source_config['rss'])
        
        for entry in feed.entries:
            title = entry.get('title', '').strip()
            published = entry.get('published', '')
            url = entry.get('link', '')
            
            if not title or not url:
                continue
            
            # 获取RSS摘要（备用）
            rss_summary = entry.get('summary', entry.get('description', ''))
            rss_summary = re.sub(r'<[^>]+>', '', rss_summary)
            
            # 检查AI相关性和计算分数
            is_ai, score = is_ai_related(title, rss_summary)
            
            if not is_ai:
                continue
            
            print(f"  ✓ AI相关: {title[:40]}...")
            
            # 抓取正文获取真实摘要
            print(f"    抓取正文...", end=" ")
            content = fetch_article_content(url, source_config['name'])
            
            if content:
                summary = extract_summary(content)
                print(f"成功 ({len(summary)}字)")
            else:
                #  fallback到RSS摘要
                summary = rss_summary[:300] + '...' if len(rss_summary) > 300 else rss_summary
                print(f"失败，使用RSS摘要")
            
            items.append({
                'title': title,
                'url': url,
                'source': source_config['name'],
                'published': published,
                'summary': summary,
                'score': score
            })
            
    except Exception as e:
        print(f"  ✗ 错误: {e}")
    
    return items


def fetch_web(source_key, source_config):
    """网页抓取（用于没有 RSS 的站点）"""
    items = []
    try:
        print(f"正在抓取 {source_config['name']} (网页)...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(source_config['url'], headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # 新智元网站的文章列表
        articles = soup.find_all('article', limit=15)
        if not articles:
            articles = soup.find_all(['div', 'a'], class_=re.compile('article|post|news|item'), limit=15)
        
        for article in articles:
            try:
                title_tag = article.find(['h1', 'h2', 'h3', 'h4']) or article.find('a')
                title = title_tag.get_text(strip=True) if title_tag else ''
                
                link_tag = article.find('a', href=True)
                url = link_tag['href'] if link_tag else ''
                if url and not url.startswith('http'):
                    url = source_config['url'] + url
                
                if not title or not url:
                    continue
                
                # 检查AI相关性
                is_ai, score = is_ai_related(title, "")
                
                if not is_ai:
                    continue
                
                print(f"  ✓ AI相关: {title[:40]}...")
                
                # 抓取正文
                print(f"    抓取正文...", end=" ")
                content = fetch_article_content(url, source_config['name'])
                
                if content:
                    summary = extract_summary(content)
                    print(f"成功 ({len(summary)}字)")
                else:
                    summary = ""
                    print(f"失败")
                
                items.append({
                    'title': title,
                    'url': url,
                    'source': source_config['name'],
                    'published': '',
                    'summary': summary,
                    'score': score
                })
                
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"  ✗ 错误: {e}")
    
    return items


def generate_markdown(news_items):
    """生成 Markdown 格式报告"""
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y年%m月%d日')
    
    md = f"""# 🤖 AI 每日新闻 - {yesterday}

共 {len(news_items)} 条精选

"""
    
    for i, item in enumerate(news_items, 1):
        md += f"""---

## {i}. [{item['source']}] {item['title']}

{item['summary']}

🔗 [阅读原文]({item['url']})

"""
    
    md += """---

*AI News Aggregator | 每日更新*
"""
    
    return md


def main():
    print("="*60)
    print("AI 国内媒体新闻抓取（改进版）")
    print("="*60)
    
    all_news = []
    
    for key, config in SOURCES.items():
        if config.get('type') == 'web':
            news = fetch_web(key, config)
        else:
            news = fetch_rss(key, config)
        all_news.extend(news)
        print(f"  从 {config['name']} 获取 {len(news)} 条AI新闻")
        print()
    
    # 按分数排序，取前10条
    all_news.sort(key=lambda x: x['score'], reverse=True)
    top_news = all_news[:10]
    
    print(f"{'='*60}")
    print(f"共 {len(all_news)} 条AI新闻，筛选出 Top {len(top_news)}")
    print(f"{'='*60}\n")
    
    # 生成 Markdown
    markdown = generate_markdown(top_news)
    
    # 保存文件
    import os
    os.makedirs('data', exist_ok=True)
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    filename = f'data/ai_news_{yesterday}.md'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print(f"报告已保存: {filename}")
    
    # 同时保存为最新版本
    with open('data/ai_news_latest.md', 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    # 返回 Markdown 内容（用于直接显示）
    return markdown


if __name__ == "__main__":
    markdown_content = main()
    print("\n" + "="*60)
    print("MARKDOWN 报告")
    print("="*60 + "\n")
    print(markdown_content)
