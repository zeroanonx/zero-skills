#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书内容搜索脚本
用于从websearch结果中提取小红书旅游攻略信息
"""

import re
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class XiaohongshuNote:
    """小红书笔记数据结构"""
    title: str
    author: str
    content: str
    likes: int
    saves: int
    tags: List[str]
    publish_date: str
    url: str
    source: str = "xiaohongshu"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "author": self.author,
            "content": self.content,
            "likes": self.likes,
            "saves": self.saves,
            "tags": self.tags,
            "publish_date": self.publish_date,
            "url": self.url,
            "source": self.source
        }

def parse_search_results(search_results: List[Dict]) -> List[XiaohongshuNote]:
    """
    解析websearch返回的小红书搜索结果
    
    Args:
        search_results: websearch工具的返回结果
        
    Returns:
        List[XiaohongshuNote]: 解析后的笔记列表
    """
    notes = []
    
    for result in search_results:
        note = parse_single_result(result)
        if note:
            notes.append(note)
    
    # 按点赞数排序
    notes.sort(key=lambda x: x.likes, reverse=True)
    return notes

def parse_single_result(result: Dict) -> XiaohongshuNote:
    """
    解析单条搜索结果
    
    由于websearch返回的是摘要信息，我们需要尽可能提取有用字段
    """
    try:
        title = result.get('title', '')
        content = result.get('text', '')
        url = result.get('url', '')
        
        # 尝试提取作者（通常在URL或内容中）
        author = extract_author(url, content)
        
        # 尝试提取点赞/收藏数
        likes = extract_number(content, ['赞', 'likes', '喜欢'])
        saves = extract_number(content, ['收藏', 'saves', '收藏数'])
        
        # 提取标签
        tags = extract_tags(content)
        
        # 提取发布日期
        publish_date = extract_date(content)
        
        return XiaohongshuNote(
            title=title,
            author=author,
            content=content,
            likes=likes,
            saves=saves,
            tags=tags,
            publish_date=publish_date,
            url=url
        )
    except Exception as e:
        print(f"解析结果失败: {e}")
        return None

def extract_author(url: str, content: str) -> str:
    """从URL或内容中提取作者名"""
    # 尝试从URL中提取
    patterns = [
        r'xiaohongshu\.com/user/profile/(\w+)',
        r'xhslink\.com/\w+',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # 从内容中提取
    author_patterns = [
        r'作者[:：]\s*(\w+)',
        r'@(\w+)',
        r'博主[:：]\s*(\w+)',
    ]
    
    for pattern in author_patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    
    return "未知作者"

def extract_number(text: str, keywords: List[str]) -> int:
    """提取数字（点赞数、收藏数等）"""
    for keyword in keywords:
        # 匹配"1234赞"或"赞：1234"或"1.2万赞"
        patterns = [
            rf'(\d+(?:\.\d+)?)\s*(?:万)?\s*{keyword}',
            rf'{keyword}[:：]\s*(\d+(?:\.\d+)?)\s*(?:万)?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                num = float(match.group(1))
                if '万' in text[match.start():match.end()+5]:
                    num *= 10000
                return int(num)
    
    return 0

def extract_tags(text: str) -> List[str]:
    """提取标签（#标签 或 [标签]）"""
    tags = []
    
    # 匹配 #标签
    hash_tags = re.findall(r'#(\w+)', text)
    tags.extend(hash_tags)
    
    # 匹配 [标签]
    bracket_tags = re.findall(r'\[(\w+)\]', text)
    tags.extend(bracket_tags)
    
    return list(set(tags))  # 去重

def extract_date(text: str) -> str:
    """提取发布日期"""
    patterns = [
        r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})',
        r'(\d{1,2}[-/]\d{1,2})',
        r'(\d{4})年(\d{1,2})月(\d{1,2})日',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    
    return "未知日期"

def filter_by_relevance(notes: List[XiaohongshuNote], 
                        min_likes: int = 100,
                        keywords: List[str] = None) -> List[XiaohongshuNote]:
    """
    按相关性过滤笔记
    
    Args:
        notes: 笔记列表
        min_likes: 最小点赞数
        keywords: 必须包含的关键词
        
    Returns:
        过滤后的笔记列表
    """
    filtered = []
    
    for note in notes:
        # 检查点赞数
        if note.likes < min_likes:
            continue
        
        # 检查关键词
        if keywords:
            content_lower = (note.title + note.content).lower()
            if not any(kw.lower() in content_lower for kw in keywords):
                continue
        
        filtered.append(note)
    
    return filtered

def generate_search_keywords(city: str, theme: str = None) -> List[str]:
    """
    生成搜索关键词组合
    
    Args:
        city: 城市名
        theme: 主题（徒步、美食等）
        
    Returns:
        关键词列表
    """
    base_keywords = [
        f"{city}旅游攻略",
        f"{city}周末去哪",
        f"{city}小众景点",
        f"{city}避坑指南",
    ]
    
    if theme:
        theme_keywords = [
            f"{city}{theme}",
            f"{city}{theme}路线",
            f"{city}{theme}攻略",
            f"{theme}{city}",
        ]
        base_keywords.extend(theme_keywords)
    
    return base_keywords

# 使用示例
if __name__ == '__main__':
    # 示例：处理websearch结果
    example_results = [
        {
            'title': '杭州徒步路线推荐',
            'text': '这条路线太美了！九溪十八涧到龙井村，全程6公里，走了3小时。1234赞 567收藏 #杭州徒步 #九溪十八涧',
            'url': 'https://xiaohongshu.com/note/123456'
        }
    ]
    
    notes = parse_search_results(example_results)
    for note in notes:
        print(f"标题: {note.title}")
        print(f"点赞: {note.likes}, 收藏: {note.saves}")
        print(f"标签: {note.tags}")
        print("---")
