#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
旅游攻略PDF生成脚本
根据提取的路线信息生成精美的PDF文档
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from typing import List, Dict, Any
from datetime import datetime

# 导入路线信息提取模块
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from extract_route_info import RouteInfo, DifficultyLevel

def register_chinese_fonts():
    """注册中文字体"""
    font_paths = [
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        'C:/Windows/Fonts/simhei.ttf',
        '/System/Library/Fonts/Hiragino Sans GB.ttc',
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                return 'ChineseFont'
            except:
                continue
    
    return 'Helvetica'

class TravelGuidePDF:
    """旅游攻略PDF生成器"""
    
    def __init__(self, output_path: str):
        self.chinese_font = register_chinese_fonts()
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        self.styles = self._create_styles()
        self.story = []
    
    def _create_styles(self) -> Dict[str, ParagraphStyle]:
        """创建样式"""
        styles = getSampleStyleSheet()
        
        return {
            'title': ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontName=self.chinese_font,
                fontSize=28,
                textColor=colors.HexColor('#2E7D32'),
                spaceAfter=30,
                alignment=TA_CENTER,
                leading=36
            ),
            'subtitle': ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Normal'],
                fontName=self.chinese_font,
                fontSize=14,
                textColor=colors.HexColor('#555555'),
                alignment=TA_CENTER,
                spaceAfter=40
            ),
            'section': ParagraphStyle(
                'SectionTitle',
                parent=styles['Heading2'],
                fontName=self.chinese_font,
                fontSize=18,
                textColor=colors.HexColor('#1B5E20'),
                spaceBefore=20,
                spaceAfter=15
            ),
            'subsection': ParagraphStyle(
                'SubSection',
                parent=styles['Heading3'],
                fontName=self.chinese_font,
                fontSize=14,
                textColor=colors.HexColor('#2E7D32'),
                spaceBefore=15,
                spaceAfter=10
            ),
            'body': ParagraphStyle(
                'CustomBody',
                parent=styles['Normal'],
                fontName=self.chinese_font,
                fontSize=11,
                leading=18,
                alignment=TA_JUSTIFY,
                spaceAfter=8
            ),
            'list_item': ParagraphStyle(
                'ListItem',
                parent=styles['Normal'],
                fontName=self.chinese_font,
                fontSize=10,
                leading=16,
                leftIndent=20,
                spaceAfter=5
            ),
            'table_header': ParagraphStyle(
                'TableHeader',
                parent=styles['Normal'],
                fontName=self.chinese_font,
                fontSize=9,
                textColor=colors.white,
                alignment=TA_CENTER
            ),
            'table_cell': ParagraphStyle(
                'TableCell',
                parent=styles['Normal'],
                fontName=self.chinese_font,
                fontSize=9,
                alignment=TA_CENTER
            ),
            'footer': ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontName=self.chinese_font,
                fontSize=9,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
        }
    
    def add_cover(self, title: str, subtitle: str, info: Dict[str, str]):
        """添加封面"""
        self.story.append(Spacer(1, 80))
        self.story.append(Paragraph(title, self.styles['title']))
        self.story.append(Paragraph(subtitle, self.styles['subtitle']))
        self.story.append(Spacer(1, 30))
        
        # 封面信息
        info_text = "<br/>".join([f"<b>{k}：</b>{v}" for k, v in info.items()])
        self.story.append(Paragraph(info_text, self.styles['body']))
        self.story.append(Spacer(1, 50))
    
    def add_route_overview_table(self, routes: List[RouteInfo]):
        """添加路线概览表格"""
        self.story.append(Paragraph("📍 路线速览", self.styles['subsection']))
        
        # 创建表格数据，所有单元格都使用Paragraph
        data = [[
            Paragraph('路线名称', self.styles['table_header']),
            Paragraph('距离', self.styles['table_header']),
            Paragraph('时长', self.styles['table_header']),
            Paragraph('难度', self.styles['table_header']),
            Paragraph('特色亮点', self.styles['table_header'])
        ]]
        
        for route in routes:
            highlights = "、".join(route.highlights[:2]) if route.highlights else "风景优美"
            data.append([
                Paragraph(route.name, self.styles['table_cell']),
                Paragraph(f"{route.total_distance}km", self.styles['table_cell']),
                Paragraph(f"{route.total_duration//60}-{route.total_duration//60+1}h", self.styles['table_cell']),
                Paragraph(route.difficulty.value, self.styles['table_cell']),
                Paragraph(highlights, self.styles['table_cell'])
            ])
        
        table = Table(data, colWidths=[4.5*cm, 2*cm, 2*cm, 2*cm, 4.5*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.chinese_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#4CAF50')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F1F8E9'), colors.white]),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 20))
    
    def add_section(self, title: str):
        """添加章节标题"""
        self.story.append(Paragraph(title, self.styles['section']))
    
    def add_subsection(self, title: str):
        """添加子章节标题"""
        self.story.append(Paragraph(title, self.styles['subsection']))
    
    def add_body_text(self, text: str):
        """添加正文"""
        self.story.append(Paragraph(text, self.styles['body']))
    
    def add_list_items(self, items: List[str], bullet: str = "•"):
        """添加列表项"""
        for item in items:
            self.story.append(Paragraph(f"{bullet} {item}", self.styles['list_item']))
    
    def add_table(self, headers: List, data: List[List], 
                  col_widths = None):
        """添加表格"""
        # 转换表头为Paragraph
        header_cells = [Paragraph(str(h), self.styles['table_header']) for h in headers]
        table_data = [header_cells]
        
        # 转换数据为Paragraph
        for row in data:
            row_cells = []
            for cell in row:
                if isinstance(cell, Paragraph):
                    row_cells.append(cell)
                else:
                    row_cells.append(Paragraph(str(cell), self.styles['table_cell']))
            table_data.append(row_cells)
        
        if col_widths is None:
            col_widths = [3*cm] * len(headers)
        
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.chinese_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976D2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#2196F3')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#E3F2FD'), colors.white]),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 15))
    
    def add_spacer(self, height: int):
        """添加空白间距"""
        self.story.append(Spacer(1, height))
    
    def add_page_break(self):
        """添加分页"""
        self.story.append(PageBreak())
    
    def add_footer(self, text: str):
        """添加页脚"""
        self.story.append(Spacer(1, 30))
        self.story.append(Paragraph(text, self.styles['footer']))
    
    def generate(self) -> str:
        """生成PDF并返回路径"""
        self.doc.build(self.story)
        return self.doc.filename

def generate_travel_guide(
    city: str,
    routes: List[RouteInfo],
    output_path: str,
    theme: str = "徒步",
    season: str = "春夏"
) -> str:
    """
    生成旅游攻略PDF
    
    Args:
        city: 城市名
        routes: 路线信息列表
        output_path: 输出路径
        theme: 主题（徒步、美食等）
        season: 季节
        
    Returns:
        生成的PDF路径
    """
    pdf = TravelGuidePDF(output_path)
    
    # 封面
    pdf.add_cover(
        title=f"{city}{season}{theme}攻略",
        subtitle=f"精选路线 | 详细实用 | 社交媒体真实推荐",
        info={
            "适用人群": "独行/结伴旅行者",
            "路线数量": f"{len(routes)}条精选路线",
            "最佳季节": season,
            "信息来源": "小红书、抖音用户真实分享",
            "制作日期": datetime.now().strftime("%Y年%m月")
        }
    )
    
    # 路线概览表
    pdf.add_route_overview_table(routes)
    pdf.add_page_break()
    
    # 第一章：概览
    pdf.add_section("第一章 目的地概览")
    pdf.add_subsection("1.1 为什么选择这里？")
    pdf.add_body_text(f"{city}是一个适合{theme}的城市，拥有丰富的自然和人文景观。根据社交媒体用户的真实分享，这里有许多值得一去的路线。")
    
    pdf.add_subsection("1.2 最佳旅游时间")
    pdf.add_body_text(f"<b>{season}季节</b>是{theme}的最佳时节，气候适宜，景色优美。")
    
    pdf.add_subsection("1.3 实用贴士")
    pdf.add_list_items([
        "提前查看天气预报，选择合适的出行日期",
        "穿舒适的鞋子和衣物",
        "携带足够的水和简单的食物",
        "遵守当地规定，保护环境"
    ])
    
    pdf.add_page_break()
    
    # 第二章：路线详解
    pdf.add_section("第二章 精选路线详解")
    
    for i, route in enumerate(routes, 1):
        pdf.add_subsection(f"路线{i}：{route.name}")
        
        # 概览
        pdf.add_body_text(f"""
        <b>全程距离：</b>{route.total_distance}公里<br/>
        <b>所需时间：</b>{route.total_duration//60}-{route.total_duration//60+1}小时<br/>
        <b>难度等级：</b>{route.difficulty.value}<br/>
        <b>起点：</b>{route.start_point}<br/>
        <b>终点：</b>{route.end_point}
        """)
        
        # 亮点
        if route.highlights:
            pdf.add_body_text("<b>景点亮点：</b>")
            pdf.add_list_items(route.highlights)
        
        # 贴士
        if route.tips:
            pdf.add_body_text("<b>实用贴士：</b>")
            pdf.add_list_items(route.tips)
        
        pdf.add_spacer(10)
    
    pdf.add_page_break()
    
    # 第三章：实用信息
    pdf.add_section("第三章 实用信息")
    
    pdf.add_subsection("3.1 交通指南")
    if routes and routes[0].transport:
        transport_data = []
        for route in routes[:4]:
            if route.transport:
                transport_data.append([
                    route.name[:10],
                    route.transport.get('metro', '-'),
                    route.transport.get('bus', '-')
                ])
        
        if transport_data:
            pdf.add_table(
                headers=['路线', '地铁', '公交'],
                data=transport_data,
                col_widths=[4*cm, 4*cm, 4*cm]
            )
    
    pdf.add_subsection("3.2 装备建议")
    pdf.add_list_items([
        "舒适的徒步鞋（防滑）",
        "速干衣物",
        "双肩背包",
        "充足的水（建议1-2L）",
        "简单的食物和零食",
        "防晒霜和遮阳帽",
        "充电宝",
        "急救包（创可贴等）"
    ])
    
    pdf.add_subsection("3.3 安全注意事项")
    pdf.add_list_items([
        "不要独自进入未开发区域",
        "注意脚下安全，特别是在湿滑路段",
        "遵守景区规定，不随意丢弃垃圾",
        "遇到恶劣天气及时下山",
        "保持手机电量，必要时开启省电模式",
        "告知家人或朋友你的行程"
    ])
    
    pdf.add_page_break()
    
    # 结语
    pdf.add_section("结语")
    pdf.add_body_text(f"""
    这份攻略基于小红书、抖音等社交媒体用户的真实分享整理而成，希望能为你的{city}之行提供帮助。
    
    记住，旅行的意义不仅在于目的地，更在于沿途的风景和体验。保持开放的心态，享受每一次徒步带来的惊喜和感动。
    
    祝你旅途愉快，平安归来！
    """)
    
    pdf.add_spacer(40)
    pdf.add_footer(f"""
    <b>{city}{theme}攻略</b><br/>
    信息来源：小红书、抖音用户分享<br/>
    制作日期：{datetime.now().strftime("%Y年%m月%d日")}<br/>
    本攻略仅供参考，实际情况请以现场为准
    """)
    
    return pdf.generate()

# 使用示例
if __name__ == '__main__':
    # 创建示例路线
    example_routes = [
        RouteInfo(
            name="示例路线",
            start_point="起点",
            end_point="终点",
            via_points=[],
            total_distance=5.0,
            total_duration=180,
            difficulty=DifficultyLevel.MEDIUM,
            segments=[],
            highlights=["景点1", "景点2"],
            tips=["贴士1", "贴士2"],
            transport={"metro": "1号线", "bus": "101路"},
            food=[],
            best_season="春季",
            suitable_for=["新手"]
        )
    ]
    
    output = generate_travel_guide(
        city="杭州",
        routes=example_routes,
        output_path="~/Desktop/aiCreateFiles/示例攻略.pdf"
    )
    print(f"PDF已生成：{output}")
