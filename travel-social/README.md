# Travel-Social Skill

从社交媒体和其他多源信息生成旅游攻略PDF的Skill。

## 🎯 项目目标

建立一个能够从真实用户分享中提取旅游信息，并生成详细攻略PDF的工具。

## 📁 文件结构

```
travel-social/
├── SKILL.md                    # 主文档 - 使用说明和工作流程
├── REFERENCE.md                # 参考文档 - API详细说明和最佳实践
├── README.md                   # 本文件 - 项目概述
├── scripts/
│   ├── search_xiaohongshu.py   # 小红书搜索脚本（框架）
│   ├── search_douyin.py        # 抖音搜索脚本（框架）
│   ├── extract_route_info.py   # 路线信息提取（可用）
│   └── generate_pdf.py         # PDF生成脚本（可用）
├── templates/                  # 模板目录（可扩展）
└── examples/
    └── hangzhou_hiking_example.md  # 杭州徒步示例
```

## 🚀 已完成的功能

### ✅ 核心框架
- [x] Skill文档结构
- [x] Python脚本框架
- [x] PDF生成工具（reportlab）
- [x] 路线信息提取器（正则表达式）

### ✅ 示例项目
- [x] 杭州春夏徒步攻略PDF（已生成）
- [x] 4条精选路线
- [x] 详细的实用信息
- [x] 精美排版（20页）

## ⚠️ 已知限制

### 数据源访问
- **小红书/抖音**：无法直接通过websearch获取详细内容（反爬机制）
- **解决方案**：使用混合数据源（携程、Trip.com、本地媒体等）

## 🛠️ 如何使用

### 快速开始

1. **收集信息**
   ```bash
   # 使用websearch搜索多个平台
   websearch "杭州徒步路线 site:you.ctrip.com"
   websearch "杭州徒步攻略 site:trip.com"
   ```

2. **提取结构化数据**
   ```python
   from extract_route_info import extract_route_info
   
   route = extract_route_info(text_content)
   print(f"距离: {route.total_distance}km")
   print(f"时长: {route.total_duration}分钟")
   ```

3. **生成PDF**
   ```python
   from generate_pdf import generate_travel_guide
   
   output = generate_travel_guide(
       city="杭州",
       routes=[route1, route2, route3, route4],
       output_path="~/Desktop/aiCreateFiles/杭州春夏徒步攻略.pdf",
       theme="徒步",
       season="春夏"
   )
   ```

### 完整示例

见 `examples/hangzhou_hiking_example.md`

## 📊 项目成果

### 已生成的PDF
**文件**: `~/Desktop/aiCreateFiles/杭州春夏徒步攻略.pdf`
**大小**: 332 KB
**页数**: ~20页

**包含内容：**
- 4条精选徒步路线
- 详细的路线分段说明
- 交通、装备、餐饮信息
- 安全注意事项
- 单人和结伴出行建议

### 使用的数据源
- Trip.com用户游记
- 杭州网官方攻略
- 每日商报
- 杭州市政府官网
- 网易旅游
- YouTube视频

## 🔮 未来计划

### 短期（1-2个月）
- [ ] 完善路线信息提取器（更多模式匹配）
- [ ] 添加图片插入功能
- [ ] 创建更多示例（成都、西安、厦门等）

### 中期（3-6个月）
- [ ] 接入官方API（如果可用）
- [ ] 开发Web界面
- [ ] 支持更多主题（美食、文化、亲子）

### 长期（6-12个月）
- [ ] 自动信息验证（交叉对比多个来源）
- [ ] 用户反馈机制
- [ ] 众包数据收集

## 🤝 贡献

欢迎提交Issue和PR！

## 📄 许可

MIT License

## 🙏 致谢

- ReportLab - PDF生成库
- 杭州旅游局 - 官方信息
- 所有分享旅游攻略的用户

---

**制作时间**: 2025年2月12日  
**作者**: Zero（LinHan）
