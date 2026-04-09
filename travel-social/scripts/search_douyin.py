#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音内容搜索脚本
用于从websearch结果中提取抖音旅游视频信息
"""

import re
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class DouyinVideo:
    """抖音视频数据结构"""
    title: str
    author: str
    description: str
    views: int
    likes: int
    comments: int
    tags: List[str]
    publish_date: str
    url: str
    duration: str = ""  # 视频时长
    source: str = "douyin"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "author": self.author,
            "description": self.description,
            "views": self.views,
            "likes": self.likes,
            "comments": self.comments,
            "tags": self.tags,
            "publish_date": self.publish_date,
            "url": self.url,
            "duration": self.duration,
            "source": self.source
        }

def parse_search_results(search_results: List[Dict]) -> List[DouyinVideo]:
    """
    解析websearch返回的抖音搜索结果
    
    Args:
        search_results: websearch工具的返回结果
        
    Returns:
        List[DouyinVideo]: 解析后的视频列表
    """
    videos = []
    
    for result in search_results:
        video = parse_single_result(result)
        if video:
            videos.append(video)
    
    # 按播放量排序
    videos.sort(key=lambda x: x.views, reverse=True)
    return videos

def parse_single_result(result: Dict) -> DouyinVideo:
    """解析单条搜索结果"""
    try:
        title = result.get('title', '')
        description = result.get('text', '')
        url = result.get('url', '')
        
        # 提取作者
        author = extract_author(url, description)
        
        # 提取播放量、点赞数、评论数
        views = extract_number(description, ['播放', 'views', 'view_count'])
        likes = extract_number(description, ['赞', 'likes', '点赞'])
        comments = extract_number(description, ['评论', 'comments', '留言'])
        
        # 提取标签
        tags = extract_tags(description)
        
        # 提取发布日期
        publish_date = extract_date(description)
        
        # 提取视频时长
        duration = extract_duration(description)
        
        return DouyinVideo(
            title=title,
            author=author,
            description=description,
            views=views,
            likes=likes,
            comments=comments,
            tags=tags,
            publish_date=publish_date,
            url=url,
            duration=duration
        )
    except Exception as e:
        print(f"解析结果失败: {e}")
        return None

def extract_author(url: str, content: str) -> str:
    """从URL或内容中提取作者名"""
    # 从URL中提取
    patterns = [
        r'douyin\.com/user/([\w-]+)',
        r'@([\w-]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # 从内容中提取
    match = re.search(r'@(\w+)', content)
    if match:
        return match.group(1)
    
    return "未知作者"

def extract_number(text: str, keywords: List[str]) -> int:
    """提取数字（播放量、点赞数等）"""
    for keyword in keywords:
        # 匹配不同格式
        patterns = [
            rf'(\d+(?:\.\d+)?)\s*(?:万|w)?\s*{keyword}',
            rf'{keyword}[:：]\s*(\d+(?:\.\d+)?)\s*(?:万|w)?',
            rf'{keyword}\s*[:：]?\s*(\d+(?:\.\d+)?)\s*(?:万|w)?\s*(?:次|个)?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                num = float(match.group(1))
                # 检查是否有"万"
                text_segment = text[match.start():match.end()+10]
                if '万' in text_segment or 'w' in text_segment.lower():
                    num *= 10000
                return int(num)
    
    return 0

def extract_tags(text: str) -> List[str]:
    """提取标签（#标签）"""
    tags = re.findall(r'#(\w+)', text)
    return list(set(tags))

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

def extract_duration(text: str) -> str:
    """提取视频时长"""
    # 匹配"16分钟10秒"或"16:10"或"10s"
    patterns = [
        r'(\d+)\s*分钟\s*(\d+)\s*秒',
        r'(\d+):(\d+)(?::(\d+))?',
        r'(\d+)\s*min',
        r'(\d+)\s*s',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    
    return ""

def filter_by_relevance(videos: List[DouyinVideo],
                        min_views: int = 1000,
                        min_duration: str = "30s") -> List[DouyinVideo]:
    """
    按相关性过滤视频
    
    Args:
        videos: 视频列表
        min_views: 最小播放量
        min_duration: 最小时长
        
    Returns:
        过滤后的视频列表
    """
    filtered = []
    
    for video in videos:
        # 检查播放量
        if video.views < min_views:
            continue
        
        filtered.append(video)
    
    return filtered

def generate_search_keywords(city: str, theme: str = None) -> List[str]:
    """
    生成搜索关键词组合
    
    Args:
        city: 城市名
        theme: 主题
        
    Returns:
        关键词列表
    """
    base_keywords = [
        f"{city}旅游",
        f"{city}打卡",
        f"{city}vlog",
    ]
    
    if theme:
        theme_keywords = [
            f"{city}{theme}",
            f"{theme}{city}",
            f"{city}周末",
        ]
        base_keywords.extend(theme_keywords)
    
    return base_keywords

# 使用示例
if __name__ == '__main__':
    # 示例：处理websearch结果
    example_results = [
        {
            'title': '杭州徒步vlog',
            'text': '这条徒步路线太美了！九溪十八涧全程攻略。1.2万播放 3456赞 123评论 #杭州 #徒步',
            'url': 'https://douyin.com/video/123456'
        }
    ]
    
    videos = parse_search_results(example_results)
    for video in videos:
        print(f"标题: {video.title}")
        print(f"播放: {video.views}, 点赞: {video.likes}")
        print(f"标签: {video.tags}")
        print("---")
