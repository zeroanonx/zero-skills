#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云南五一4天旅游攻略PDF生成器
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
                alignment=TA_CENTER),
            'highlight': ParagraphStyle('Highlight', parent=styles['Normal'],
                fontName=self.chinese_font, fontSize=9, textColor=colors.HexColor('#D32F2F'),
                backColor=colors.HexColor('#FFEBEE'),
                borderPadding=5)
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
            self.story.append(Paragraph("<b>⚠️ 需提前预约(五一期间务必提前3天以上预约)：</b>", self.styles['body']))
            for item in booking_list:
                self.story.append(Paragraph(f"• {item}", self.styles['body']))
        self.story.append(Spacer(1, 15))
    
    def add_weather_info(self, weather_data):
        self.story.append(Paragraph("🌤️ 五一期间天气预报", self.styles['section']))
        for day, info in weather_data.items():
            self.story.append(Paragraph(f"<b>{day}：</b>{info}", self.styles['body']))
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
        self.story.append(Paragraph("🏨 推荐住宿", self.styles['section']))
        for hotel in hotels:
            self.story.append(Paragraph(f"• {hotel}", self.styles['body']))
        self.story.append(Spacer(1, 15))
    
    def add_packing_list(self, items):
        self.story.append(Paragraph("🎒 携带清单", self.styles['section']))
        for item in items:
            self.story.append(Paragraph(f"☑️ {item}", self.styles['body']))
        self.story.append(Spacer(1, 15))
    
    def add_budget_info(self, budget_data):
        self.story.append(Paragraph("💰 费用预算参考", self.styles['section']))
        for category, amount in budget_data.items():
            self.story.append(Paragraph(f"• {category}：{amount}", self.styles['body']))
        self.story.append(Spacer(1, 15))
    
    def add_footer(self, text):
        self.story.append(Spacer(1, 20))
        self.story.append(Paragraph(text, self.styles['footer']))
    
    def add_page_break(self):
        self.story.append(PageBreak())
    
    def generate(self):
        self.doc.build(self.story)
        return self.doc.filename

def generate_yunnan_guide(output_path):
    pdf = TimelineGuidePDF(output_path)
    
    # 封面
    pdf.add_cover(
        title="云南大理·丽江 五一4天深度游",
        subtitle="风花雪月之旅 | 详细时间轴攻略 | 2025版",
        info={
            "核心目的地": "大理 + 丽江",
            "行程天数": "4天3晚",
            "最佳季节": "春季(3-5月)",
            "人均预算": "2000-3500元",
            "交通方式": "高铁+打车+拼车",
            "制作日期": datetime.now().strftime("%Y年%m月%d日")
        }
    )
    
    # 行程总览
    pdf.add_overview(
        date="五一假期(5月1日-4日)",
        route_summary="大理古城 ➡️ 洱海环湖 ➡️ 喜洲古镇 ➡️ 丽江古城 ➡️ 玉龙雪山 ➡️ 蓝月谷",
        booking_list=[
            "玉龙雪山冰川公园大索道(提前3天在'丽江旅游集团'小程序抢票，20:00放票)",
            "云杉坪索道(提前3天预约，21:00放票)",
            "《印象丽江》演出(提前1-2天预订)",
            "大理/丽江特色民宿(五一期间需提前1-2周预订)"
        ]
    )
    
    # 五一天气预报
    weather_data = {
        "5月1日": "大理多云11-21℃，丽江多云12-20℃，西部有小到中雨",
        "5月2日": "大理晴间多云12-25℃，丽江晴间多云13-24℃，适宜出行",
        "5月3日": "大理晴间多云13-26℃，丽江晴13-25℃，紫外线强",
        "5月4日": "大理晴13-27℃，丽江晴间多云13-26℃，注意防晒"
    }
    pdf.add_weather_info(weather_data)
    
    # Day 1: 抵达大理 + 大理古城
    day1_items = [
        TimelineItem("08:00", "10:00", "各地飞抵昆明/大理", "交通", 120,
            "飞机/高铁抵达<br/>昆明长水机场→大理高铁2小时(145元)", "", 
            "五一期间机票紧张，建议提前预订<br/>如飞昆明需预留充足转机时间", "", ""),
        TimelineItem("10:00", "10:30", "前往大理古城", "交通", 30,
            "大理站→古城打车约40元/40分钟<br/>或乘8路公交2元/50分钟", "", 
            "建议打车，节省时间<br/>古城周边易堵车", "", ""),
        TimelineItem("11:00", "12:00", "入住古城民宿", "住宿", 60,
            "推荐住古城南门/人民路附近", "", 
            "五一房价涨幅大，提前预订<br/>古城石板路拖行李不便，选靠近城门", "", ""),
        TimelineItem("12:00", "13:30", "午餐时间", "餐饮", 90,
            "古城内步行", "", "", 
            "再回首鸡肉米线 15元<br/>乳扇5元/个", ""),
        TimelineItem("14:00", "18:00", "大理古城深度游", "景点", 240,
            "步行游览", "", 
            "推荐路线：南门→五华楼→洋人街→人民路→崇圣寺三塔(门票75元)<br/>古城免费，三塔需购票<br/>人民路手作银饰、特色小店", 
            "凉鸡米线12元<br/>烤乳扇8元<br/>喜洲粑粑15元", ""),
        TimelineItem("18:30", "20:00", "古城晚餐+夜游", "餐饮", 90,
            "古城内", "", 
            "夜游古城别有一番风味<br/>洋人街酒吧街热闹，人民路文艺", 
            "尽善百年古院餐厅 人均77元<br/>桃红小馆 人均81元", ""),
        TimelineItem("20:30", "21:30", "返回民宿休息", "交通", 60,
            "步行", "", "", "", "")
    ]
    
    pdf.add_timeline_table("Day 1(5月1日)：抵达大理·古城漫步", day1_items)
    pdf.add_page_break()
    
    # Day 2: 洱海环湖
    day2_items = [
        TimelineItem("08:00", "08:30", "早餐", "餐饮", 30,
            "古城内", "", "", 
            "饵丝米线 12-18元", ""),
        TimelineItem("09:00", "09:30", "前往龙龛码头", "交通", 30,
            "古城→龙龛码头打车约25元/20分钟", "", 
            "环洱海骑行起点<br/>五一期间人多，早到可避开高峰", "", ""),
        TimelineItem("09:30", "12:00", "洱海生态廊道骑行", "景点", 150,
            "租自行车/电动车", "", 
            "骑行路线：龙龛码头→磻溪S弯(约7公里)<br/>租自行车40元/天，电动车50元/天<br/>网红S弯拍照绝佳，五一可能人多", 
            "沿途有咖啡车、小吃摊", ""),
        TimelineItem("12:00", "13:30", "前往喜洲古镇+午餐", "交通+餐饮", 90,
            "磻溪→喜洲打车约30元/25分钟", "", 
            "喜洲是白族文化重镇<br/>比大理古城更古朴", 
            "喜洲粑粑 8-15元<br/>白族酸辣鱼 人均40元", ""),
        TimelineItem("14:00", "16:00", "喜洲古镇游览", "景点", 120,
            "步行", "", 
            "必看：严家大院(门票25元)、转角楼、喜林苑黄墙<br/>可体验白族扎染(100元/次)<br/>五一期间有民俗表演", 
            "老冰棍3元<br/>手工酸奶10元", ""),
        TimelineItem("16:30", "17:30", "前往双廊", "交通", 60,
            "喜洲→双廊打车约50元/40分钟<br/>或乘中巴15元", "", 
            "沿海公路风景绝美<br/>五一易堵车，预留充足时间", "", ""),
        TimelineItem("18:00", "19:30", "双廊日落+晚餐", "景点+餐饮", 90,
            "双廊古镇", "", 
            "双廊是洱海最佳观日落点<br/>推荐去玉几岛、南诏风情岛(门票50元)", 
            "双廊白族私房菜 人均60元<br/>洱海鱼必吃", ""),
        TimelineItem("20:00", "21:00", "返回大理古城", "交通", 60,
            "双廊→古城打车约80元/1小时", "", 
            "晚上回古城住宿更便利<br/>也可选择住双廊海景房(价格高)", "", "")
    ]
    
    pdf.add_timeline_table("Day 2(5月2日)：洱海环游·喜洲双廊", day2_items)
    pdf.add_page_break()
    
    # Day 3: 大理到丽江 + 丽江古城
    day3_items = [
        TimelineItem("08:00", "09:00", "早餐+退房", "餐饮", 60,
            "古城内", "", "", 
            "耙肉饵丝 15元", ""),
        TimelineItem("09:30", "10:00", "前往大理站", "交通", 30,
            "古城→大理站打车约40元", "", 
            "五一期间提前1小时到车站<br/>古城到车站约40分钟", "", ""),
        TimelineItem("10:15", "12:15", "高铁前往丽江", "交通", 120,
            "大理→丽江高铁约2小时(80元)", "", 
            "沿途风景优美<br/>建议选靠窗座位", "", ""),
        TimelineItem("12:30", "13:00", "前往丽江古城", "交通", 30,
            "丽江站→古城打车约30元/25分钟<br/>或乘18路公交", "", 
            "建议住古城北门/南门附近<br/>拖行李更方便", "", ""),
        TimelineItem("13:00", "14:00", "入住+午餐", "住宿+餐饮", 60,
            "古城周边", "", "", 
            "阿婆腊排骨火锅 人均60元", ""),
        TimelineItem("14:30", "18:00", "丽江古城深度游", "景点", 210,
            "步行游览", "", 
            "推荐路线：大水车→四方街→木府(门票40元)→狮子山(门票35元)→万古楼<br/>古城免费，木府和狮子山需购票<br/>五一期间人流量大，注意安全", 
            "鸡豆凉粉 10元<br/>丽江粑粑 8元<br/>米灌肠 12元", ""),
        TimelineItem("18:30", "19:30", "晚餐", "餐饮", 60,
            "古城内", "", "", 
            "有一锅腊排骨火锅 人均81元<br/>滇厨小锅巴餐厅 人均83元", ""),
        TimelineItem("20:00", "21:30", "丽江古城夜游", "景点", 90,
            "步行", "", 
            "夜游古城最美<br/>四方街有篝火晚会<br/>五一期间可能有特别活动", 
            "鲜花饼 5元/个<br/>手工酸奶 12元", ""),
        TimelineItem("22:00", "22:30", "返回民宿", "交通", 30,
            "步行", "", 
            "丽江古城晚上很热闹<br/>建议住在不临街的房间", "", "")
    ]
    
    pdf.add_timeline_table("Day 3(5月3日)：大理→丽江·古城夜游", day3_items)
    pdf.add_page_break()
    
    # Day 4: 玉龙雪山
    day4_items = [
        TimelineItem("06:30", "07:00", "早餐", "餐饮", 30,
            "古城内或打包", "", 
            "玉龙雪山需早起<br/>五一期间排队人多", 
            "包子豆浆 15元", ""),
        TimelineItem("07:00", "08:00", "前往玉龙雪山", "交通", 60,
            "古城→玉龙雪山打车约100元/40分钟<br/>或乘雪山专线大巴15元", "", 
            "建议拼车或包车(约80-100元往返)<br/>五一期间7:30前到景区避开高峰", 
            "", ""),
        TimelineItem("08:00", "08:30", "购买门票+进山", "景点", 30,
            "景区大门", "", 
            "进山费100元(必买)<br/>大索道140元(含环保车)<br/>五一期间务必提前3天抢票", 
            "", ""),
        TimelineItem("08:30", "12:00", "冰川公园大索道", "景点", 210,
            "索道+环保车", "", 
            "大索道直达4506米<br/>可徒步至4680米观景台<br/>⚠️注意高反：带氧气瓶(景区39元/瓶，古城买15-20元)<br/>带巧克力、热水补充能量<br/>五一期间人多，排队可能1-2小时", 
            "", ""),
        TimelineItem("12:00", "13:00", "午餐", "餐饮", 60,
            "景区内", "", 
            "景区餐厅价格较高<br/>建议自带干粮", 
            "自带面包巧克力<br/>或雪厨餐厅简餐 50元", ""),
        TimelineItem("13:30", "15:30", "蓝月谷游览", "景点", 120,
            "环保车", "", 
            "蓝月谷在雪山脚下<br/>湖水呈梦幻蓝色，超级出片<br/>游览约1.5-2小时<br/>环保车包含在索道票内，无需额外购买电瓶车", 
            "", ""),
        TimelineItem("16:00", "17:00", "《印象丽江》演出(可选)", "景点", 60,
            "步行至剧场", "", 
            "张艺谋导演实景演出<br/>票价220元起<br/>每天14:00、16:30两场<br/>五一期间可能加场", 
            "", ""),
        TimelineItem("17:30", "18:30", "返回丽江古城/机场", "交通", 60,
            "拼车/打车", "", 
            "如需当天返程，建议订20:00后航班<br/>丽江三义机场离市区28公里", 
            "", ""),
        TimelineItem("19:00", "20:00", "晚餐+返程", "餐饮", 60,
            "古城或机场", "", 
            "", 
            "浮娴小锅饭(束河古镇) 人均81元<br/>汽锅鸡必吃", "")
    ]
    
    pdf.add_timeline_table("Day 4(5月4日)：玉龙雪山·蓝月谷·返程", day4_items)
    
    # 推荐住宿
    pdf.add_hotel_info([
        "【大理】大理古城南门附近民宿 - 交通便利，性价比高(五一约300-500元/晚)",
        "【大理】洱海双廊海景房 - 风景绝佳但价格高(五一约600-1000元/晚)",
        "【丽江】丽江古城北门/南门客栈 - 拖行李方便(五一约350-600元/晚)",
        "【丽江】束河古镇 - 比大研古城安静(五一约300-500元/晚)",
        "💡 提示：五一期间民宿价格翻倍，建议提前2周预订"
    ])
    
    # 费用预算
    budget_data = {
        "交通费用": "机票/高铁往返 800-1500元 + 当地交通 300-500元 = 约1100-2000元",
        "住宿费用": "3晚住宿(五一价格) 约900-1800元",
        "门票费用": "崇圣寺三塔75 + 木府40 + 狮子山35 + 玉龙雪山100+140 = 约390元",
        "餐饮费用": "4天约400-600元(人均每天100-150元)",
        "其他费用": "骑行租车40 + 扎染100 + 购物纪念品 = 约200-500元",
        "总计": "人均约3000-4300元(五一期间)"
    }
    pdf.add_budget_info(budget_data)
    
    # 携带清单
    pdf.add_packing_list([
        "身份证(必带，景区门票、酒店入住需要)",
        "学生证/老年证(景区门票半价优惠)",
        "防晒用品：SPF50+防晒霜、墨镜、遮阳帽、防晒衣(云南紫外线极强)",
        "保暖衣物：羽绒服/冲锋衣(玉龙雪山山顶0-10℃)、长裤、保暖内衣",
        "舒适鞋子：运动鞋/徒步鞋(古城石板路+爬山)",
        "雨具：雨伞/雨衣(五一可能下雨)",
        "高原反应预防：氧气瓶(古城买15-20元，景区39元)、红景天(提前一周服用)",
        "常用药品：感冒药、肠胃药、创可贴、晕车药",
        "充电宝(拍照耗电快)",
        "现金少量(部分小店不支持手机支付)",
        "保湿护肤品(云南干燥)",
        "保温杯(喝热水防高反)"
    ])
    
    # 重要提示
    pdf.story.append(Paragraph("⚠️ 五一期间重要提示", pdf.styles['section']))
    tips = [
        "玉龙雪山大索道票需提前3天在'丽江旅游集团'小程序抢购(每天20:00放票)",
        "五一期间游客量巨大，所有景点都需提前预约或抢票",
        "大理、丽江民宿价格翻倍且紧张，务必提前2周预订",
        "云南紫外线极强，即使阴天也要做好防晒，否则容易晒伤",
        "玉龙雪山海拔4680米，注意高原反应：不要剧烈运动、多喝水、带氧气瓶",
        "洱海骑行注意防晒和补水，带足饮用水",
        "五一期间交通易拥堵，预留充足时间，不要安排太紧凑",
        "尊重当地少数民族风俗，古城内勿大声喧哗",
        "警惕古城内的拉客和低价团，选择正规渠道",
        "12345政务服务热线 - 旅途中遇到问题可拨打"
    ]
    for tip in tips:
        pdf.story.append(Paragraph(f"• {tip}", pdf.styles['body']))
    
    pdf.add_footer(f"""
    <b>云南大理·丽江 五一4天深度游攻略</b><br/>
    制作时间：{datetime.now().strftime("%Y年%m月%d日")}<br/>
    本攻略根据2025年最新信息整理，实际价格以现场为准<br/>
    祝您五一假期旅途愉快！🌸
    """)
    
    return pdf.generate()

if __name__ == '__main__':
    output_path = "/Users/linhan/Desktop/aiCreateFiles/云南五一4天旅游攻略.pdf"
    result = generate_yunnan_guide(output_path)
    print(f"✅ PDF生成成功！")
    print(f"📄 保存路径：{result}")
