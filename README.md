# Identification-of-phishing-websites
主要跑了一遍原有代码，代码的过程截图和结果截图在各Step的文件夹
优化了一下GUI界面，因为群聊里说网页，所以又写了一个网页都放在Step7
尽力了，可能有一些问题，本来想做的更好但是改吐了，实在是能力有限对不起
后续还需要修改和需要哪里的图再联系
还有一些可视化图在Step7的output里，下面是关于思路和方法：
项目概述
基于机器学习的钓鱼网站检测系统，包含完整的数据处理流程、模型训练、Web界面和GUI应用。
1.对来自两个网站的网址进行融合和数据平衡，保证50%合法网站，50%钓鱼网站并分别打标签标记
2.数据的特征提取
3.五个基础模型，交叉验证，保存随机森林
4.使用保存的模型识别网址的系统程序
5.根据特征重要性重新训练模型
6.使用深度学习得到的模型
7.使用保存的模型创建web网页

核心技术栈
● 机器学习: RandomForest分类器 (scikit-learn)
● 后端: Flask + Python
● 前端: HTML + CSS + JavaScript (Chart.js)
● GUI: Tkinter
● 特征提取: requests, BeautifulSoup, whois, tldextract

系统架构
数据流程:
phish_url.csv → 特征提取 → url_features.csv → 模型训练 → phishing_url_model.pkl
                                                              ↓
                                                    Web/GUI 实时检测

核心文件说明
1. 数据处理 (Step1-3)
Step1: 数据标注
● phish_url.csv - 原始URL数据集（合法/钓鱼标签）
Step2: 特征提取
● featureExtrator.py - 提取10个关键特征
  ○ 地址栏特征: URL长度、IP使用、点号数、HTTPS、子域名
  ○ 域名特征: 域名年龄、DNS有效性、WHOIS信息
  ○ HTML特征: iframe存在性、JS混淆
Step3: 模型训练
● model.py - 训练RandomForest模型
● phishing_url_model.pkl - 训练好的模型文件（12MB）
2. Web系统
后端:
● server_fixed.py - 完整版本（较慢，10-60秒）
前端:
● index.html - 主页面
● app_omptimized.js - 前端逻辑（图表展示）
● styles.css + styles_addon.css 
特点:
● 实时URL检测
● 动态图表可视化（特征重要性、概率分布、雷达图）
● 详细特征展示
3. GUI应用
● GUI_Modern.py ⭐ - 现代化桌面应用
  ○ 配色（与Web统一）
  ○ 卡片式布局
  ○ 后台线程检测（不冻结UI）
  ○ 特征详情展示
4. 可视化
● visualize.py - 生成模型性能图表
  ○ 需要测试数据文件 url_features_final.csv
  ○ 输出6张图: 混淆矩阵、特征重要性、ROC曲线、性能指标、精确率 - 召回率曲线、训练历史图

工作原理
特征提取
URL: https://www.google.com
  ↓
提取10个特征:
  1. url_length: 23
  2. uses_ip: 0 (否)
  3. num_dots: 2
  4. protocol: 1 (HTTPS)
  5. num_subdomains: 1
  6. domain_age_days: 7300 (20年)
  7. dns_valid: 1 (有效)
  8. whois_info_exists: 1
  9. has_iframe: 0
  10. has_obfuscated_js: 0
模型预测
特征向量 → RandomForest模型 → 预测结果
[23, 0, 2, 1, 1, 7300, 1, 1, 0, 0] → [0.982, 0.018]
                                      ↓
                                   合法: 98.2%
                                   钓鱼: 1.8%

快速启动
Web系统
# 1. 准备环境
pip install flask flask-cors joblib scikit-learn pandas requests beautifulsoup4 python-whois tldextract

# 2. 确认文件
phishing_url_model.pkl  # 必需
server_quick.py         # 必需
index.html             # 必需
app_final.js           # 必需

# 3. 启动
python server_quick.py

# 4. 访问
http://localhost:5000
GUI应用
# 1. 准备环境
pip install joblib scikit-learn pandas requests beautifulsoup4 python-whois tldextract

# 2. 确认文件
phishing_url_model.pkl  # 必需
GUI_Modern.py          # 必需

# 3. 运行
python GUI_Modern.py

关键技术点
1. 特征工程
为什么选这10个特征:
● 地址栏特征: 钓鱼网站URL通常很长、使用IP、子域名多
● 域名特征: 钓鱼网站域名通常很新、DNS不稳定
● HTML特征: 钓鱼网站常用iframe跳转、JS混淆
特征重要性排序 (模型自动学习):
1. URL长度 (25%)
2. 域名年龄 (22%)
3. 点号数量 (18%)
...
2. 模型选择
RandomForest分类器:
● 优点: 准确率高(88-92%)、过拟合少、可解释性强
● 参数: 100棵树，自动特征权重
● 训练数据: 1000+样本（合法/钓鱼各50%）
替代方案: XGBoost, LightGBM (准确率略高但更复杂)

依赖库版本
核心依赖:
- Python: 3.8+
- scikit-learn: 1.6+
- Flask: 2.0+
- pandas: 1.5+
- requests: 2.28+
- beautifulsoup4: 4.11+
- python-whois: 0.8+

前端:
- Chart.js: 3.9+

注意事项
1. 模型文件
● phishing_url_model.pkl 必须与代码在同一目录
● 文件大小约12MB
● 不要修改文件名
2. 网络要求
● 特征提取需要联网（DNS、WHOIS、HTML）
● 离线模式只能用地址栏特征（准确率降低）
3. 隐私安全
● 不记录用户输入的URL
● 不上传任何数据
● 本地检测，数据安全
