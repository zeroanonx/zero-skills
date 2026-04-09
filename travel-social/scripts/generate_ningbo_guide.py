#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宁波两天旅游攻略PDF生成器
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

def generate_ningbo_guide(output_path):
    pdf = TimelineGuidePDF(output_path)
    
    # 封面
    pdf.add_cover(
        title="宁波两天一夜深度游",
        subtitle="甬城古韵·湖光山色 | 详细时间轴攻略 | 2025版",
        info={
            "核心目的地": "宁波市区 + 东钱湖",
            "行程天数": "2天1夜",
            "最佳季节": "春秋两季(3-5月、9-11月)",
            "人均预算": "800-1500元",
            "交通方式": "地铁+打车+共享单车",
            "制作日期": datetime.now().strftime("%Y年%m月%d日")
        }
    )
    
    # 行程总览
    pdf.add_overview(
        date="周末/假期",
        route_summary="天一阁 ➡️ 月湖公园 ➡️ 鼓楼 ➡️ 宁波博物馆 ➡️ 老外滩 ➡️ 东钱湖 ➡️ 韩岭老街",
        booking_list=[
            "宁波博物馆(免费，需提前在官方公众号预约)",
            "东钱湖骑行(建议提前查看天气，雨天不推荐)"
        ]
    )
    
    # Day 1: 市区文化游
    day1_items = [
        TimelineItem("08:00", "09:00", "抵达宁波", "交通", 60,
            "高铁至宁波站<br/>或飞机至栎社机场", "", 
            "宁波站是高铁主要站点<br/>地铁2号线直达市区", "", ""),
        TimelineItem("09:00", "09:30", "前往天一阁", "交通", 30,
            "宁波站→天一阁<br/>地铁1号线西门口站", "", 
            "地铁1号线直达，B出口步行5分钟<br/>也可打车约15元", "", ""),
        TimelineItem("09:30", "12:00", "天一阁博物馆", "景点", 150,
            "步行游览", "", 
            "中国现存最古老的私家藏书楼<br/>门票30元，建议游玩2-2.5小时<br/>7:30前入场可避开人流高峰<br/>园林建筑精美，拍照出片", 
            "", ""),
        TimelineItem("12:00", "13:30", "月湖公园+午餐", "景点+餐饮", 90,
            "天一阁后门直达月湖", "", 
            "月湖免费开放，'江南小西湖'<br/>沿宋代水系漫步，环境清幽", 
            "仓桥面结店(镇明路108号)<br/>面结+面 20元<br/>缸鸭狗汤圆 30元", ""),
        TimelineItem("14:00", "15:30", "鼓楼", "景点", 90,
            "月湖→鼓楼步行15分钟<br/>或地铁1号线鼓楼站", "", 
            "宁波地标建筑<br/>登楼俯瞰市区<br/>鼓楼外街品尝地道宁波菜<br/>周边小吃众多", 
            "南塘油赞子 15元/袋<br/>葱烤鲞、咸蛋黄焗蛏子", ""),
        TimelineItem("16:00", "18:00", "宁波博物馆", "景点", 120,
            "鼓楼→博物馆<br/>地铁1号线转3号线", "", 
            "免费开放，需提前预约<br/>王澍设计，建筑本身就是艺术品<br/>融合传统与现代<br/>了解宁波历史文化", 
            "", ""),
        TimelineItem("18:30", "20:00", "老外滩晚餐+夜游", "景点+餐饮", 90,
            "博物馆→老外滩打车约20元", "", 
            "欧式建筑群，三江口夜景<br/>灯光秀璀璨<br/>酒吧街热闹<br/>感受宁波夜生活", 
            "宁波状元楼 人均136元<br/>甬上名灶 人均110元<br/>红膏炝蟹必尝", ""),
        TimelineItem("20:30", "21:00", "返回酒店", "交通", 30,
            "老外滩附近住宿", "", 
            "建议住老外滩或天一广场附近<br/>交通便利", "", "")
    ]
    
    pdf.add_timeline_table("Day 1：宁波市区·文化古韵游", day1_items)
    pdf.add_page_break()
    
    # Day 2: 东钱湖
    day2_items = [
        TimelineItem("08:00", "08:30", "早餐", "餐饮", 30,
            "酒店附近", "", "", 
            "宁波年糕汤 15元<br/>海鲜面 25元", ""),
        TimelineItem("09:00", "10:00", "前往东钱湖", "交通", 60,
            "市区→东钱湖<br/>地铁4号线东钱湖站<br/>或打车约40元", "", 
            "地铁4号线直达，A出口<br/>打车约30-40元/30分钟<br/>建议早出发避开人流", "", ""),
        TimelineItem("10:00", "12:30", "东钱湖环湖骑行", "景点", 150,
            "租自行车/电动车", "", 
            "租车40-50元/天<br/>骑行路线：小普陀→福泉山→下水村<br/>约15公里，风景绝美<br/>五一/周末人多，早到", 
            "沿途农家乐<br/>东钱湖鱼头 60元", ""),
        TimelineItem("13:00", "14:30", "韩岭老街午餐", "餐饮", 90,
            "骑行至韩岭老街", "", 
            "千年古村落改造<br/>比南塘老街更古朴<br/>艺术氛围浓厚", 
            "农家土鸡煲 80元<br/>木木鲜海鲜面 40元<br/>奉化牛肉干面 25元", ""),
        TimelineItem("15:00", "16:30", "南宋石刻群", "景点", 90,
            "韩岭→石刻群打车15元", "", 
            "东钱湖石刻公园<br/>南宋时期墓葬石刻<br/>历史厚重感<br/>门票25元", "", ""),
        TimelineItem("17:00", "18:00", "返回市区", "交通", 60,
            "东钱湖→市区<br/>地铁4号线或打车", "", 
            "预留充足返程时间<br/>傍晚易堵车", "", ""),
        TimelineItem("18:30", "19:30", "南塘老街晚餐", "餐饮", 60,
            "地铁2号线宁波火车站旁", "", 
            "宁波传统小吃聚集地<br/>购买伴手礼", 
            "溪口千层饼 25元/袋<br/>南塘豆酥糖 15元<br/>矮子馅饼 20元", ""),
        TimelineItem("20:00", "21:00", "返程", "交通", 60,
            "宁波站/栎社机场", "", 
            "高铁返程或次日离开", "", "")
    ]
    
    pdf.add_timeline_table("Day 2：东钱湖·湖光山色游", day2_items)
    
    # 推荐住宿
    pdf.add_hotel_info([
        "【老外滩】宁波老外滩Ruby Bella瑰宝酒店 - 位置绝佳，步行可达老外滩、地铁站(约400-600元/晚)",
        "【天一广场】全季/如家精选 - 交通便利，靠近商圈(约300-500元/晚)",
        "【东钱湖】东钱湖华茂希尔顿/柏悦酒店 - 湖景房，度假首选(约800-1500元/晚)",
        "💡 提示：建议第一天住市区(老外滩/天一广场)，方便夜游和次日去东钱湖"
    ])
    
    # 费用预算
    budget_data = {
        "交通费用": "高铁往返 200-400元 + 当地地铁/打车 100-150元 = 约300-550元",
        "住宿费用": "1晚住宿(市区) 约300-600元",
        "门票费用": "天一阁30 + 南宋石刻25 = 约55元(博物馆、月湖免费)",
        "餐饮费用": "2天约200-400元(人均每天100-200元)",
        "其他费用": "东钱湖租车50 + 购物伴手礼100 = 约150元",
        "总计": "人均约1000-1200元(不含往返大交通)"
    }
    pdf.add_budget_info(budget_data)
    
    # 携带清单
    pdf.add_packing_list([
        "身份证(必带，景区门票、酒店入住需要)",
        "学生证/老年证(景区门票优惠)",
        "舒适鞋子：运动鞋(东钱湖骑行+步行较多)",
        "雨具：雨伞/雨衣(江南地区多雨)",
        "充电宝(手机拍照耗电快)",
        "防晒用品：防晒霜、遮阳帽(夏季必备)",
        "常用药品：肠胃药(海鲜多，预防不适)、晕车药",
        "现金少量(部分小吃店不支持手机支付)",
        "保温杯(喝热水)",
        "骑行装备：如自驾可带骑行眼镜、手套(东钱湖骑行用)"
    ])
    
    # 宁波美食推荐
    pdf.story.append(Paragraph("🍜 宁波必吃美食推荐", pdf.styles['section']))
    foods = [
        "<b>缸鸭狗猪油汤圆</b> - 始于1926年老字号，猪油芝麻馅香糯可口(天一广场店，人均30元)",
        "<b>慈城水磨年糕</b> - 浙江省非遗，可炒可汤可烤(慈城年糕主题餐厅，人均40元)",
        "<b>红膏炝蟹</b> - 宁波海鲜门面担当，咸鲜回甘(宁海食府，人均140元)",
        "<b>南塘油赞子</b> - 百年传统小吃，酥脆可口(南塘老街，15元/袋)",
        "<b>溪口千层饼</b> - 蒋介石最爱，27层薄如蝉翼(溪口武岭路，25元)",
        "<b>仓桥面结</b> - 百年老店，面结软糯入口即烂(镇明路108号，20元)",
        "<b>海鲜面</b> - 鱼骨熬汤，配花蟹、黄鱼、虾等(木木鲜，人均40元)",
        "<b>奉化牛肉干面</b> - 番薯粉丝+牛骨汤底，暖胃神器(奉化，25元)",
        "<b>宁波㸆菜</b> - 红烧肉做法烧蔬菜，软糯入味(甬上名灶)",
        "<b>宁波烤菜</b> - 老底子家常菜，咸鲜下饭(老宁波弄堂菜馆)"
    ]
    for food in foods:
        pdf.story.append(Paragraph(f"• {food}", pdf.styles['body']))
    pdf.story.append(Spacer(1, 15))
    
    # 交通指南
    pdf.story.append(Paragraph("🚇 宁波交通指南", pdf.styles['section']))
    transports = [
        "<b>地铁</b>：宁波地铁1-8号线覆盖主要景点，支付宝/微信可领乘车码，票价2-10元",
        "<b>公交</b>：90分钟内地铁公交换乘优惠，建议办交通卡或使用移动支付",
        "<b>打车</b>：滴滴/出租车起步价11元，市区景点间打车15-30元",
        "<b>共享单车</b>：市区景点集中，可骑共享单车，1-2元/次",
        "<b>东钱湖交通</b>：地铁4号线直达，或打车约40元，环湖建议租车骑行",
        "<b>机场</b>：栎社机场地铁2号线直达市区，约40分钟",
        "<b>高铁站</b>：宁波站是主要站点，地铁2号线、4号线可达"
    ]
    for t in transports:
        pdf.story.append(Paragraph(f"• {t}", pdf.styles['body']))
    pdf.story.append(Spacer(1, 15))
    
    # 避坑提示
    pdf.story.append(Paragraph("⚠️ 旅游避坑指南", pdf.styles['section']))
    tips = [
        "天一阁7:30开门，建议早到避开人流，体验更佳",
        "宁波博物馆免费但需提前预约，周一闭馆",
        "东钱湖骑行注意防晒，带足饮用水，沿途补给点较少",
        "红膏炝蟹是生腌食品，肠胃敏感者慎食",
        "南塘老街商业化较重，鼓楼小吃更地道",
        "东钱湖周末/节假日人多，建议工作日或早到",
        "宁波菜偏咸鲜，如口味清淡可提前告知店家少盐",
        "海鲜价格随季节波动，点餐前确认价格",
        "12345政务服务热线 - 旅途中遇到问题可拨打"
    ]
    for tip in tips:
        pdf.story.append(Paragraph(f"• {tip}", pdf.styles['body']))
    
    pdf.add_footer(f"""
    <b>宁波两天一夜深度游攻略</b><br/>
    制作时间：{datetime.now().strftime("%Y年%m月%d日")}<br/>
    本攻略根据2025年最新信息整理，实际价格以现场为准<br/>
    祝您宁波之旅愉快！🌊
    """)
    
    return pdf.generate()

if __name__ == '__main__':
    output_path = "/Users/linhan/Desktop/aiCreateFiles/宁波两天旅游攻略.pdf"
    result = generate_ningbo_guide(output_path)
    print(f"✅ PDF生成成功！")
    print(f"📄 保存路径：{result}")
