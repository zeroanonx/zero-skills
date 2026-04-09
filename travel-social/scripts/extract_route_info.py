#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
路线信息提取脚本
从社交媒体内容中提取结构化的路线信息
"""

import re
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum

class DifficultyLevel(Enum):
    """难度等级"""
    EASY = "★☆☆☆☆"
    EASY_MEDIUM = "★★☆☆☆"
    MEDIUM = "★★★☆☆"
    MEDIUM_HARD = "★★★★☆"
    HARD = "★★★★★"
    UNKNOWN = "未知"

@dataclass
class RouteSegment:
    """路线分段信息"""
    name: str
    distance: float  # 公里
    duration: int    # 分钟
    description: str
    highlights: List[str]

@dataclass
class TimelineItem:
    """时间轴行程项"""
    time_start: str      # 开始时间，如 "10:30"
    time_end: str        # 结束时间，如 "11:50"
    activity: str        # 活动内容，如 "总统府"
    activity_type: str   # 活动类型：景点/交通/餐饮/休息
    duration: int        # 活动时长（分钟）
    transport: str       # 交通方式，如 "打车18分钟/12元"
    transport_detail: str # 详细交通信息
    tips: str            # 小提示
    food: str            # 美食推荐
    booking_info: str    # 预约信息

@dataclass
class RouteInfo:
    """完整路线信息"""
    name: str
    start_point: str
    end_point: str
    via_points: List[str]
    total_distance: float  # 公里
    total_duration: int    # 分钟
    difficulty: DifficultyLevel
    segments: List[RouteSegment]
    highlights: List[str]
    tips: List[str]
    transport: Dict[str, str]
    food: List[Dict]
    best_season: str
    suitable_for: List[str]

def extract_route_info(text: str) -> RouteInfo:
    """
    从文本中提取路线信息
    
    Args:
        text: 社交媒体内容文本
        
    Returns:
        RouteInfo: 结构化的路线信息
    """
    # 提取基本路线信息
    name = extract_route_name(text)
    start, end, via = extract_start_end_via(text)
    distance = extract_distance(text)
    duration = extract_duration(text)
    difficulty = extract_difficulty(text)
    
    # 提取分段信息
    segments = extract_segments(text)
    
    # 提取其他信息
    highlights = extract_highlights(text)
    tips = extract_tips(text)
    transport = extract_transport(text)
    food = extract_food(text)
    season = extract_best_season(text)
    suitable = extract_suitable_for(text)
    
    return RouteInfo(
        name=name,
        start_point=start,
        end_point=end,
        via_points=via,
        total_distance=distance,
        total_duration=duration,
        difficulty=difficulty,
        segments=segments,
        highlights=highlights,
        tips=tips,
        transport=transport,
        food=food,
        best_season=season,
        suitable_for=suitable
    )

def extract_route_name(text: str) -> str:
    """提取路线名称"""
    patterns = [
        r'路线[一二三四五\d]+[:：]\s*(.+?)(?:\n|$)',
        r'(.+?)(?:路线|徒步|攻略)',
        r'【(.+?)】',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    
    return "未命名路线"

def extract_start_end_via(text: str) -> Tuple[str, str, List[str]]:
    """提取起点、终点和途经点"""
    start = ""
    end = ""
    via = []
    
    # 匹配"从A到B"或"起点：A 终点：B"
    patterns = [
        r'从\s*(.+?)\s*(?:→|到|出发|开始)\s*(.+?)(?:\n|$)',
        r'起点[:：]\s*(.+?)\s*终点[:：]\s*(.+?)(?:\n|$)',
        r'出发[:：]\s*(.+?)\s*到达[:：]\s*(.+?)(?:\n|$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            start = match.group(1).strip()
            end = match.group(2).strip()
            break
    
    # 提取途经点
    via_pattern = r'途经[:：]\s*(.+?)(?:\n|$)'
    via_match = re.search(via_pattern, text)
    if via_match:
        via_text = via_match.group(1)
        via = [v.strip() for v in re.split(r'[、，,→]', via_text)]
    
    return start, end, via

def extract_distance(text: str) -> float:
    """提取总距离"""
    patterns = [
        r'(\d+(?:\.\d+)?)\s*(?:km|公里|千米)',
        r'全程\s*(\d+(?:\.\d+)?)\s*(?:km|公里|千米)',
        r'距离\s*(\d+(?:\.\d+)?)\s*(?:km|公里|千米)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return float(match.group(1))
    
    return 0.0

def extract_duration(text: str) -> int:
    """提取总时长（分钟）"""
    patterns = [
        r'(\d+(?:\.\d+)?)\s*(?:小时|h)(?:\s*(\d+)\s*(?:分钟|min|分))?',
        r'(\d+)\s*(?:分钟|min|分)',
        r'耗时\s*(\d+(?:\.\d+)?)\s*(?:小时|h)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            if '小时' in text[match.start():match.end()] or 'h' in text[match.start():match.end()].lower():
                hours = float(match.group(1))
                minutes = int(match.group(2)) if match.group(2) else 0
                return int(hours * 60 + minutes)
            else:
                return int(match.group(1))
    
    return 0

def extract_difficulty(text: str) -> DifficultyLevel:
    """提取难度等级"""
    # 匹配星级
    star_match = re.search(r'难度[:：]?\s*([★☆]+)', text)
    if star_match:
        stars = star_match.group(1)
        count = stars.count('★')
        if count == 1:
            return DifficultyLevel.EASY
        elif count == 2:
            return DifficultyLevel.EASY_MEDIUM
        elif count == 3:
            return DifficultyLevel.MEDIUM
        elif count == 4:
            return DifficultyLevel.MEDIUM_HARD
        elif count == 5:
            return DifficultyLevel.HARD
    
    # 匹配文字描述
    if re.search(r'轻松|简单|休闲|初级', text):
        return DifficultyLevel.EASY
    elif re.search(r'中等|适中|有点挑战', text):
        return DifficultyLevel.MEDIUM
    elif re.search(r'困难|难|高强度|挑战', text):
        return DifficultyLevel.HARD
    
    return DifficultyLevel.UNKNOWN

def extract_segments(text: str) -> List[RouteSegment]:
    """提取分段信息"""
    segments = []
    
    # 匹配分段描述
    segment_patterns = [
        r'(\d+)[:：、.]\s*([^\n]+?)\s*[(（]([^)）]+)[)）]',
        r'第(\d+)段[:：]\s*([^\n]+)',
    ]
    
    for pattern in segment_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            seg_name = match.group(2).strip()
            seg_details = match.group(3) if len(match.groups()) > 2 else ""
            
            # 从细节中提取距离和时长
            seg_dist = 0.0
            seg_dur = 0
            
            dist_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:km|公里)', seg_details)
            if dist_match:
                seg_dist = float(dist_match.group(1))
            
            dur_match = re.search(r'(\d+)\s*(?:分钟|min)', seg_details)
            if dur_match:
                seg_dur = int(dur_match.group(1))
            
            segments.append(RouteSegment(
                name=seg_name,
                distance=seg_dist,
                duration=seg_dur,
                description="",
                highlights=[]
            ))
    
    return segments

def extract_highlights(text: str) -> List[str]:
    """提取景点亮点"""
    highlights = []
    
    # 查找"亮点"、"特色"、"打卡"等关键词后的内容
    patterns = [
        r'亮点[:：](.+?)(?:\n\n|\Z)',
        r'特色[:：](.+?)(?:\n\n|\Z)',
        r'打卡[:：](.+?)(?:\n\n|\Z)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            content = match.group(1)
            # 分割列表项
            items = re.split(r'[\n•●\-\*]', content)
            highlights.extend([item.strip() for item in items if item.strip()])
    
    return highlights[:10]  # 限制数量

def extract_tips(text: str) -> List[str]:
    """提取实用贴士/避坑指南"""
    tips = []
    
    # 查找"贴士"、"注意"、"避坑"等关键词
    patterns = [
        r'贴士[:：](.+?)(?:\n\n|\Z)',
        r'注意[:：](.+?)(?:\n\n|\Z)',
        r'避坑[:：](.+?)(?:\n\n|\Z)',
        r'建议[:：](.+?)(?:\n\n|\Z)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            content = match.group(1)
            items = re.split(r'[\n•●\-\*]', content)
            tips.extend([item.strip() for item in items if item.strip()])
    
    return tips[:10]

def extract_transport(text: str) -> Dict[str, str]:
    """提取交通信息"""
    transport = {}
    
    # 地铁
    metro_match = re.search(r'地铁[:：]\s*(.+?)(?:\n|$)', text)
    if metro_match:
        transport['metro'] = metro_match.group(1).strip()
    
    # 公交
    bus_match = re.search(r'公交[:：]\s*(.+?)(?:\n|$)', text)
    if bus_match:
        transport['bus'] = bus_match.group(1).strip()
    
    # 自驾
    car_match = re.search(r'自驾[:：]\s*(.+?)(?:\n|$)', text)
    if car_match:
        transport['car'] = car_match.group(1).strip()
    
    return transport

def extract_food(text: str) -> List[Dict]:
    """提取餐饮信息"""
    food_list = []
    
    # 查找餐饮推荐
    patterns = [
        r'推荐[:：](.+?)(?:\n\n|\Z)',
        r'美食[:：](.+?)(?:\n\n|\Z)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            content = match.group(1)
            items = re.split(r'[\n•●\-\*]', content)
            for item in items:
                if item.strip():
                    food_list.append({
                        'name': item.strip(),
                        'type': '未知',
                        'price': ''
                    })
    
    return food_list[:5]

def extract_best_season(text: str) -> str:
    """提取最佳季节"""
    patterns = [
        r'最佳季节[:：]\s*(.+?)(?:\n|$)',
        r'适合季节[:：]\s*(.+?)(?:\n|$)',
        r'(?:适合|推荐)\s*(春|夏|秋|冬|全年)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    
    return "全年皆宜"

def extract_suitable_for(text: str) -> List[str]:
    """提取适合人群"""
    suitable = []
    
    keywords = {
        '亲子': ['亲子', '家庭', '小孩', '儿童'],
        '情侣': ['情侣', '约会', '浪漫'],
        '朋友': ['朋友', '结伴', '三五好友'],
        '独行': ['独自', '一个人', '独行'],
        '新手': ['新手', '初级', '入门'],
        '进阶': ['进阶', '中级', '有一定基础'],
    }
    
    for category, words in keywords.items():
        if any(word in text for word in words):
            suitable.append(category)
    
    return suitable if suitable else ['大众']

def merge_route_info(route_infos: List[RouteInfo]) -> RouteInfo:
    """
    合并多个来源的路线信息，取最可靠的数据
    
    Args:
        route_infos: 多个RouteInfo对象
        
    Returns:
        合并后的RouteInfo
    """
    if not route_infos:
        return None
    
    # 使用第一个作为基础
    base = route_infos[0]
    
    # 合并亮点和贴士（去重）
    all_highlights = []
    all_tips = []
    
    for info in route_infos:
        all_highlights.extend(info.highlights)
        all_tips.extend(info.tips)
    
    base.highlights = list(set(all_highlights))[:15]
    base.tips = list(set(all_tips))[:15]
    
    return base

# 使用示例
if __name__ == '__main__':
    example_text = """
    路线一：九溪十八涧 → 龙井村
    
    全程约6公里，耗时3-4小时，难度：★★☆☆☆
    
    起点：九溪公交站
    终点：龙井村
    途经：九溪烟树 → 十八涧戏水区
    
    亮点：
    • 九溪烟树：小瀑布、碧池，绝佳拍照点
    • 十八涧：溪流穿路，趣味横生
    • 龙井村：古朴茶村，品茶体验
    
    贴士：
    • 夏季玩水建议穿溯溪鞋
    • 带上备用袜子
    
    交通：
    地铁：4号线水澄桥站
    公交：39路、308路九溪站
    """
    
    route = extract_route_info(example_text)
    print(f"路线名称: {route.name}")
    print(f"距离: {route.total_distance}km")
    print(f"时长: {route.total_duration}分钟")
    print(f"难度: {route.difficulty.value}")
    print(f"亮点: {route.highlights}")
