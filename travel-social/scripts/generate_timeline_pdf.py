#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时间轴旅游攻略PDF生成器
生成包含详细时间节点、交通、美食的PDF
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from extract_route_info import TimelineItem

def register_chinese_fonts():
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

class TimelineGuidePDF:
    def __init__(self, output_path):
        self.chinese_font = register_chinese_fonts()
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        self.styles = self._create_styles()
        self.story = []
    
    def _create_styles(self):
        styles = getSampleStyleSheet()
        return {
            'title': ParagraphStyle('CustomTitle', parent=styles['Heading1'],
                fontName=self.chinese_font, fontSize=24, textColor=colors.HexColor('#1B5E20'),
                spaceAfter=20, alignment=TA_CENTER, leading=30),
            'subtitle': ParagraphStyle('CustomSubtitle', parent=styles['Normal'],
                fontName=self.chinese_font, fontSize=12, textColor=colors.HexColor('#555555'),
                alignment=TA_CENTER, spaceAfter=30),
            'day_title': ParagraphStyle('DayTitle', parent=styles['Heading2'],
                fontName=self.chinese_font, fontSize=16, textColor=colors.white,
                spaceBefore=15, spaceAfter=10, backColor=colors.HexColor('#1976D2'),
                borderPadding=8),
            'section': ParagraphStyle('SectionTitle', parent=styles['Heading2'],
                fontName=self.chinese_font, fontSize=14, textColor=colors.HexColor('#1B5E20'),
                spaceBefore=20, spaceAfter=12),
            'body': ParagraphStyle('CustomBody', parent=styles['Normal'],
                fontName=self.chinese_font, fontSize=10, leading=16,
                alignment=TA_LEFT, spaceAfter=6),
            'time_cell': ParagraphStyle('TimeCell', parent=styles['Normal'],
                fontName=self.chinese_font, fontSize=9, textColor=colors.HexColor('#1565C0'),
                alignment=TA_CENTER),
            'activity_cell': ParagraphStyle('ActivityCell', parent=styles['Normal'],
                fontName=self.chinese_font, fontSize=10, textColor=colors.HexColor('#333333'),
                alignment=TA_LEFT),
            'transport_cell': ParagraphStyle('TransportCell', parent=styles['Normal'],
                fontName=self.chinese_font, fontSize=8, textColor=colors.HexColor('#666666'),
                alignment=TA_LEFT),
            'tips_cell': ParagraphStyle('TipsCell', parent=styles['Normal'],
                fontName=self.chinese_font, fontSize=8, textColor=colors.HexColor('#E65100'),
                alignment=TA_LEFT),
            'food_cell': ParagraphStyle('FoodCell', parent=styles['Normal'],
                fontName=self.chinese_font, fontSize=8, textColor=colors.HexColor('#2E7D32'),
                alignment=TA_LEFT),
            'header': ParagraphStyle('TableHeader', parent=styles['Normal'],
                fontName=self.chinese_font, fontSize=9, textColor=colors.white,
                alignment=TA_CENTER),
            'footer': ParagraphStyle('Footer', parent=styles['Normal'],
                fontName=self.chinese_font, fontSize=8, textColor=colors.grey,
                alignment=TA_CENTER)
        }
    
    def add_cover(self, title, subtitle, info):
        self.story.append(Spacer(1, 60))
        self.story.append(Paragraph(title, self.styles['title']))
        self.story.append(Paragraph(subtitle, self.styles['subtitle']))
        self.story.append(Spacer(1, 20))
        info_text = "<br/>".join([f"<b>{k}：</b>{v}" for k, v in info.items()])
        self.story.append(Paragraph(info_text, self.styles['body']))
        self.story.append(Spacer(1, 30))
    
    def add_overview(self, date, route_summary, booking_list):
        self.story.append(Paragraph("📋 行程总览", self.styles['section']))
        self.story.append(Paragraph(f"<b>日期：</b>{date}", self.styles['body']))
        self.story.append(Paragraph(f"<b>路线：</b>{route_summary}", self.styles['body']))
        self.story.append(Spacer(1, 10))
        if booking_list:
            self.story.append(Paragraph("<b>⚠️ 需提前预约：</b>", self.styles['body']))
            for item in booking_list:
                self.story.append(Paragraph(f"• {item}", self.styles['body']))
        self.story.append(Spacer(1, 15))
    
    def add_timeline_table(self, day_title, items):
        self.story.append(Paragraph(day_title, self.styles['day_title']))
        headers = ['时间', '游玩安排', '交通细节', '小提示', '美食']
        data = [[Paragraph(h, self.styles['header']) for h in headers]]
        
        for item in items:
            time_str = f"{item.time_start}<br/>～<br/>{item.time_end}"
            activity_str = f"<b>{item.activity}</b><br/>{item.duration}分钟"
            data.append([
                Paragraph(time_str, self.styles['time_cell']),
                Paragraph(activity_str, self.styles['activity_cell']),
                Paragraph(item.transport, self.styles['transport_cell']),
                Paragraph(item.tips, self.styles['tips_cell']),
                Paragraph(item.food, self.styles['food_cell'])
            ])
        
        table = Table(data, colWidths=[2.5*cm, 3.5*cm, 4*cm, 4*cm, 2.5*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976D2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), self.chinese_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDBDBD')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#1976D2')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#E3F2FD'), colors.white]),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        self.story.append(table)
        self.story.append(Spacer(1, 20))
    
    def add_hotel_info(self, hotels):
        self.story.append(Paragraph("🏨 推荐酒店", self.styles['section']))
        for hotel in hotels:
            self.story.append(Paragraph(f"• {hotel}", self.styles['body']))
        self.story.append(Spacer(1, 15))
    
    def add_packing_list(self, items):
        self.story.append(Paragraph("🎒 携带清单", self.styles['section']))
        for item in items:
            self.story.append(Paragraph(f"☑️ {item}", self.styles['body']))
        self.story.append(Spacer(1, 15))
    
    def add_footer(self, text):
        self.story.append(Spacer(1, 20))
        self.story.append(Paragraph(text, self.styles['footer']))
    
    def add_page_break(self):
        self.story.append(PageBreak())
    
    def generate(self):
        self.doc.build(self.story)
        return self.doc.filename

def generate_nanjing_timeline_guide(output_path):
    pdf = TimelineGuidePDF(output_path)
    
    pdf.add_cover(
        title="杭州 ➡️ 南京 两天一夜深度游",
        subtitle="详细时间轴 | 交通美食全攻略 | 2025版",
        info={
            "出发地": "杭州",
            "目的地": "南京",
            "行程天数": "2天1夜",
            "出发时间": "早上10:00",
            "交通方式": "高铁+打车(优先)",
            "制作日期": datetime.now().strftime("%Y年%m月%d日")
        }
    )
    
    pdf.add_overview(
        date="12.07(周日) - 12.08(周一)",
        route_summary="南京南 ➡️ 总统府 ➡️ 南京博物院 ➡️ 梧桐大道 ➡️ 美龄宫 ➡️ 中山陵 ➡️ 音乐台 ➡️ 秦淮河夜游 ➡️ 鸡鸣寺 ➡️ 城墙 ➡️ 先锋书店 ➡️ 大屠杀纪念馆",
        booking_list=[
            "南京总统府(公众号预约，免费)",
            "南京博物院(公众号预约，免费)",
            "南京钟山风景区(中山陵+美龄宫+音乐台)",
            "夫子庙画舫夜场票(小程序预约，80元)",
            "大屠杀遇难同胞纪念馆(公众号预约，免费)"
        ]
    )
    
    day1_items = [
        TimelineItem("10:00", "10:30", "从酒店出发", "交通", 30,
            "打车18分钟/12元<br/>地铁：夫子庙➡️大行宫(21分钟)", "", "建议打车，节省时间", "", ""),
        TimelineItem("10:30", "11:50", "总统府", "景点", 80, "", "",
            "提前在'南京总统府'公众号预约<br/>08:30-17:00开放<br/>推荐游玩1.5小时", "", "需预约"),
        TimelineItem("11:50", "12:30", "午餐时间", "餐饮", 40,
            "步行至大行宫商圈", "", "", "南京大牌档<br/>鸭血粉丝汤 15-25元", ""),
        TimelineItem("12:30", "12:46", "前往南京博物院", "交通", 16,
            "打车16分钟/10元<br/>地铁：大行宫➡️明故宫(21分钟)", "", "", "", ""),
        TimelineItem("12:50", "15:30", "南京博物院", "景点", 160, "", "",
            "中国三大博物馆之一<br/>重点：民国馆、历史馆<br/>可租讲解器20元", "", "需预约"),
        TimelineItem("15:30", "15:48", "前往梧桐大道", "交通", 18,
            "打车18分钟/10元<br/>地铁：明故宫➡️苜蓿园(36分钟)", "", "", "", ""),
        TimelineItem("15:50", "16:30", "梧桐大道+美龄宫", "景点", 40,
            "梧桐大道步行8分钟到美龄宫", "",
            "一楼有'蒋宋爱情'主题展<br/>二楼阳台俯瞰梧桐大道", "", ""),
        TimelineItem("16:30", "17:30", "中山陵", "景点", 60,
            "美龄宫步行11分钟", "",
            "392级台阶<br/>第8层平台拍'博爱'坊最出片<br/>需预约", "", "需预约"),
        TimelineItem("17:30", "17:50", "音乐台", "景点", 20,
            "中山陵停车场➡️观光车➡️中山陵南站(10元)", "",
            "鸽子群飞拍照：整点放飞", "", ""),
        TimelineItem("17:50", "18:50", "前往夫子庙", "交通", 60,
            "中山陵➡️地铁➡️夫子庙<br/>约50分钟-1小时", "", "", "", ""),
        TimelineItem("19:00", "20:30", "秦淮河画舫夜游", "景点", 90, "", "",
            "夜游80元/人<br/>线上'夫子庙预定'小程序选'夜场票'<br/>建议18:00场次，提前30min取票<br/>座位随机",
            "夫子庙小吃街<br/>盐水鸭、汤包", "需预约")
    ]
    
    pdf.add_timeline_table("Day 1(周日)：钟山风景区 + 秦淮河夜游", day1_items)
    pdf.add_page_break()
    
    day2_items = [
        TimelineItem("10:00", "10:30", "从酒店出发", "交通", 30,
            "打车28分钟/18元<br/>地铁：夫子庙➡️鸡鸣寺(30分钟)", "", "", "", ""),
        TimelineItem("10:30", "11:30", "鸡鸣寺", "景点", 60, "", "",
            "求姻缘最灵<br/>寺内'古胭脂井'可顺路看<br/>门票10元", "", ""),
        TimelineItem("11:30", "12:00", "午餐时间", "餐饮", 30, "", "",
            "", "鸡鸣寺素斋<br/>或周边小吃", ""),
        TimelineItem("12:00", "13:00", "明城墙(台城段)", "景点", 60,
            "鸡鸣寺后门出，步行3分钟登台城城墙", "",
            "门票15元<br/>拍照点：第3个垛口'佛塔+湖景'同框", "", ""),
        TimelineItem("13:00", "13:30", "玄武湖", "景点", 30,
            "台城解放门下来即玄武湖'情侣园入口'", "",
            "沿湖步行1km出玄武门", "", ""),
        TimelineItem("13:30", "13:45", "前往先锋书店", "交通", 15,
            "地铁1号线玄武门站➡️珠江路站①号口出，步行5分钟", "", "", "", ""),
        TimelineItem("13:45", "14:45", "先锋书店(五台山总店)", "景点", 60, "", "",
            "09:00开门<br/>地下车库改造<br/>十字架打卡点在一楼最深处", "书店咖啡", ""),
        TimelineItem("14:45", "15:10", "前往纪念馆", "交通", 25,
            "打车16分钟/11元<br/>地铁：五台山➡️云锦路(25分钟)", "", "", "", ""),
        TimelineItem("15:10", "16:00", "大屠杀遇难同胞纪念馆", "景点", 50, "", "",
            "务必提前在'纪念馆'公众号预约<br/>安检严格<br/>禁止大声喧哗", "", "需预约"),
        TimelineItem("16:00", "16:30", "前往南京南站", "交通", 30,
            "打车22分钟到达南站<br/>或地铁2号线转1号线", "",
            "建议预留充足时间", "", ""),
        TimelineItem("16:30", "18:00", "返程回杭", "交通", 90,
            "高铁：南京南➡️杭州东<br/>约1-1.5小时", "", "", "", "")
    ]
    
    pdf.add_timeline_table("Day 2(周一)：鸡鸣寺 + 城墙 + 先锋书店 + 纪念馆", day2_items)
    
    pdf.add_hotel_info([
        "如家酒店neo(南京夫子庙店) - 位置便利，性价比高",
        "如家睿柏·云酒店(南京夫子庙步行街店) - 近景区",
        "全季酒店(南京新街口朝天宫店) - 品质较好",
        "建议住在夫子庙附近，夜游方便"
    ])
    
    pdf.add_packing_list([
        "身份证(必带，预约景点需要)",
        "充电宝(手机拍照耗电快)",
        "舒适的步行鞋(每天2万步+)",
        "外套(早晚温差大)",
        "雨伞/雨衣(春季多雨)",
        "相机/运动相机",
        "现金少量(部分小店不支持手机支付)",
        "纸巾、湿巾"
    ])
    
    pdf.add_footer(f"""
    <b>杭州 ➡️ 南京 两天一夜深度游</b><br/>
    制作时间：{datetime.now().strftime("%Y年%m月%d日")}<br/>
    本攻略仅供参考，实际路况和开放情况请以现场为准<br/>
    祝您旅途愉快！
    """)
    
    return pdf.generate()

if __name__ == '__main__':
    output_path = "/Users/linhan/Desktop/aiCreateFiles/杭州到南京两天游_详细时间轴版.pdf"
    result = generate_nanjing_timeline_guide(output_path)
    print(f"✅ PDF生成成功！")
    print(f"📄 保存路径：{result}")
