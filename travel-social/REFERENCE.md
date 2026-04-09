# Travel-Social Skill 参考文档

## 详细API使用说明

### 社交媒体搜索

#### 小红书搜索

**API调用:**
```python
# 使用websearch搜索小红书内容
search_query = "site:xiaohongshu.com 杭州徒步路线"
```

**搜索关键词模板:**
- `{城市名}徒步路线`
- `{城市名}周末去哪`
- `{景点名}攻略`
- `{城市名}美食推荐`
- `{城市名}避坑指南`

**信息提取字段:**
```python
{
    "title": "笔记标题",
    "author": "作者",
    "likes": "点赞数",
    "saves": "收藏数",
    "content": "正文内容",
    "tags": ["标签1", "标签2"],
    "publish_date": "发布日期",
    "url": "链接"
}
```

#### 抖音搜索

**API调用:**
```python
# 使用websearch搜索抖音内容
search_query = "site:douyin.com 杭州徒步"
```

**搜索关键词模板:**
- `{城市名}徒步`
- `{城市名}旅游攻略`
- `{景点名}打卡`
- `{城市名}美食`

**信息提取字段:**
```python
{
    "title": "视频标题",
    "author": "作者",
    "views": "播放量",
    "likes": "点赞数",
    "description": "视频描述",
    "tags": ["标签1", "标签2"],
    "publish_date": "发布日期",
    "url": "链接"
}
```

### 信息提取模板

#### 路线信息提取

**正则表达式模板:**
```python
import re

# 提取距离
 Distance: r'(\d+(?:\.\d+)?)\s*(?:km|公里)'

# 提取时间
Time: r'(\d+(?:\.\d+)?)\s*(?:小时|h|分钟|min)'

# 提取难度
Difficulty: r'难度[:：]\s*([★☆]+)'

# 提取起点终点
Route: r'(?:从|起点)[:：]\s*(.+?)(?:→|到|终点)[:：]\s*(.+)'
```

#### 实用信息提取

**交通信息:**
```python
transport_keywords = {
    "地铁": ["号线", "站", "出口"],
    "公交": ["路", "站", "下车"],
    "自驾": ["停车", "停车场", "自驾"],
    "打车": ["打车", "网约车", "出租车"]
}
```

**餐饮信息:**
```python
food_keywords = {
    "餐厅": ["人均", "推荐", "好吃"],
    "小吃": ["特色", "必吃", "排队"],
    "饮品": ["奶茶", "咖啡", "茶"]
}
```

**装备信息:**
```python
equipment_keywords = {
    "必备": ["必须", "一定要", "必备"],
    "选带": ["可以带", "建议带", "可选"],
    "季节": ["春夏", "秋冬", "防晒", "保暖"]
}
```

### PDF生成配置

#### 页面设置

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

PAGE_CONFIG = {
    "pagesize": A4,
    "rightMargin": 2*cm,
    "leftMargin": 2*cm,
    "topMargin": 2*cm,
    "bottomMargin": 2*cm
}
```

#### 样式配置

```python
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

STYLES = {
    "title": {
        "fontSize": 28,
        "textColor": colors.HexColor('#2E7D32'),
        "alignment": "CENTER",
        "spaceAfter": 30
    },
    "section": {
        "fontSize": 18,
        "textColor": colors.HexColor('#1B5E20'),
        "spaceBefore": 20,
        "spaceAfter": 15
    },
    "subsection": {
        "fontSize": 14,
        "textColor": colors.HexColor('#2E7D32'),
        "spaceBefore": 15,
        "spaceAfter": 10
    },
    "body": {
        "fontSize": 11,
        "leading": 18,
        "alignment": "JUSTIFY"
    }
}
```

#### 表格样式

```python
from reportlab.platypus import TableStyle
from reportlab.lib import colors

TABLE_STYLE = TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'ChineseFont'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
])
```

### 中文支持

#### 字体注册

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def register_chinese_fonts():
    font_paths = [
        '/System/Library/Fonts/PingFang.ttc',  # macOS
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',  # Linux
        'C:/Windows/Fonts/simhei.ttf',  # Windows
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                return 'ChineseFont'
            except:
                continue
    
    return 'Helvetica'
```

## 常见问题

### Q1: 如何处理小红书/抖音的反爬机制？

A: 使用websearch工具，避免直接爬取页面。

### Q2: 信息来源如何标注？

A: 在PDF中注明"信息来源于社交媒体用户分享，仅供参考"。

### Q3: 如何处理过时信息？

A: 优先使用3个月内的内容，并在PDF中注明信息收集日期。

### Q4: 是否可以插入图片？

A: 可以使用reportlab的Image功能插入本地图片，但需注意版权。

## 扩展开发

### 添加新数据源

1. 在`scripts/`创建新的搜索脚本
2. 实现统一的信息提取接口
3. 更新`SKILL.md`文档

### 自定义模板

1. 修改`templates/`目录下的模板文件
2. 调整样式、颜色、布局
3. 测试PDF生成效果

### 多语言支持

1. 准备多语言字体
2. 实现语言切换逻辑
3. 翻译模板内容

## 最佳实践

1. **搜索策略**
   - 使用多个关键词组合搜索
   - 交叉验证不同来源的信息
   - 优先使用高赞、高收藏内容

2. **信息提取**
   - 使用正则表达式提取结构化数据
   - 保留原文中的emoji和特殊符号
   - 记录信息来源和时间

3. **PDF生成**
   - 保持样式一致性
   - 合理使用分页符
   - 添加目录或导航

4. **质量控制**
   - 人工审核关键信息
   - 测试PDF在不同设备上的显示效果
   - 收集用户反馈持续改进
