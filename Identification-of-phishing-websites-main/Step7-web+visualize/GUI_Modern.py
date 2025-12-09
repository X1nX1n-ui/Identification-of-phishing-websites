"""
钓鱼网站检测系统 - 现代化GUI
莫兰迪配色方案，与Web系统风格统一
"""

import tkinter as tk
from tkinter import ttk, messagebox
import joblib
import pandas as pd
import urllib.parse
import requests
from bs4 import BeautifulSoup
import whois
import datetime
import socket
import tldextract
import threading

# ==================== 莫兰迪配色方案 ====================
COLORS = {
    'background': '#F5F1E8',      # 米白色背景
    'card': '#FFFFFF',            # 卡片白色
    'primary': '#3A3632',         # 深棕色文字
    'secondary': '#6B6460',       # 次要文字
    'border': '#C9BFB0',          # 边框色
    'accent_orange': '#D4886E',   # 莫兰迪橙红色（钓鱼警告）
    'accent_yellow': '#D4A574',   # 姜黄色（强调）
    'safe_green': '#828B78',      # 莫兰迪绿（安全）
    'button_hover': '#E5DBC7',    # 按钮悬停
    'input_bg': '#FDFCF9',        # 输入框背景
}

# ==================== 特征提取（与GUI.py完全一致） ====================
def extract_features(url):
    """提取URL特征 - 与原始GUI.py完全一致"""
    features = {}

    # 提取地址栏特征
    features['url_length'] = len(url)

    try:
        domain = urllib.parse.urlparse(url).netloc
        socket.inet_aton(domain.split(':')[0])
        features['uses_ip'] = 1
    except OSError:
        features['uses_ip'] = 0

    features['num_dots'] = url.count('.')
    features['protocol'] = 1 if urllib.parse.urlparse(url).scheme == 'https' else 0

    extracted = tldextract.extract(url)
    subdomains = extracted.subdomain.split('.')
    features['num_subdomains'] = len(subdomains) if extracted.subdomain else 0

    # 提取域名特征
    whois_info = None
    try:
        domain = f"{extracted.domain}.{extracted.suffix}"
        whois_info = whois.whois(domain)
        if whois_info.creation_date:
            if isinstance(whois_info.creation_date, list):
                creation_date = whois_info.creation_date[0]
            else:
                creation_date = whois_info.creation_date
            domain_age = (datetime.datetime.now() - creation_date).days
            features['domain_age_days'] = domain_age
        else:
            features['domain_age_days'] = -1
    except Exception as e:
        features['domain_age_days'] = -1

    try:
        socket.gethostbyname(domain)
        features['dns_valid'] = 1
    except OSError:
        features['dns_valid'] = 0

    features['whois_info_exists'] = 1 if whois_info else 0

    # 提取HTML和JavaScript特征
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')

        features['has_iframe'] = 1 if soup.find('iframe') else 0

        scripts = soup.find_all('script')
        obfuscated = 0
        for script in scripts:
            if script.string:
                if 'eval(' in script.string or '\\x' in script.string or 'unescape(' in script.string:
                    obfuscated = 1
                    break
        features['has_obfuscated_js'] = obfuscated

    except Exception as e:
        features['has_iframe'] = -1
        features['has_obfuscated_js'] = -1

    return features


# ==================== 现代化GUI应用 ====================
class PhishingDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("钓鱼网站检测系统")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS['background'])
        
        # 加载模型
        self.model = None
        self.load_model()
        
        # 检测状态
        self.is_detecting = False
        
        # 创建UI
        self.create_ui()
    
    def load_model(self):
        """加载模型"""
        try:
            self.model = joblib.load("phishing_url_model.pkl")
            print("✓ 模型加载成功")
        except Exception as e:
            messagebox.showerror("错误", f"模型加载失败: {str(e)}\n\n请确保 phishing_url_model.pkl 在当前目录")
            self.root.destroy()
    
    def create_ui(self):
        """创建用户界面"""
        # 主容器
        main_frame = tk.Frame(self.root, bg=COLORS['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # 标题区域
        self.create_header(main_frame)
        
        # 输入区域
        self.create_input_section(main_frame)
        
        # 结果区域
        self.create_result_section(main_frame)
        
        # 特征详情区域
        self.create_features_section(main_frame)
    
    def create_header(self, parent):
        """创建标题"""
        header_frame = tk.Frame(parent, bg=COLORS['background'])
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # 主标题
        title = tk.Label(
            header_frame,
            text="钓鱼网站检测系统",
            font=("Microsoft YaHei UI", 28, "bold"),
            fg=COLORS['primary'],
            bg=COLORS['background']
        )
        title.pack()
        
        # 副标题
        subtitle = tk.Label(
            header_frame,
            text="基于机器学习的智能检测",
            font=("Microsoft YaHei UI", 12),
            fg=COLORS['secondary'],
            bg=COLORS['background']
        )
        subtitle.pack(pady=(5, 0))
    
    def create_input_section(self, parent):
        """创建输入区域"""
        input_frame = tk.Frame(parent, bg=COLORS['card'], relief=tk.FLAT)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 添加圆角效果（通过内边距）
        inner_frame = tk.Frame(input_frame, bg=COLORS['card'])
        inner_frame.pack(fill=tk.BOTH, padx=2, pady=2)
        
        # 标签
        label = tk.Label(
            inner_frame,
            text="请输入要检测的URL：",
            font=("Microsoft YaHei UI", 13, "bold"),
            fg=COLORS['primary'],
            bg=COLORS['card']
        )
        label.pack(anchor=tk.W, padx=25, pady=(20, 10))
        
        # 输入框容器
        entry_container = tk.Frame(inner_frame, bg=COLORS['input_bg'], 
                                  highlightbackground=COLORS['border'],
                                  highlightthickness=2)
        entry_container.pack(fill=tk.X, padx=25, pady=(0, 20))
        
        # 输入框
        self.url_entry = tk.Entry(
            entry_container,
            font=("Consolas", 12),
            fg=COLORS['primary'],
            bg=COLORS['input_bg'],
            relief=tk.FLAT,
            insertbackground=COLORS['primary']
        )
        self.url_entry.pack(fill=tk.X, padx=15, pady=12)
        self.url_entry.bind('<Return>', lambda e: self.start_detection())
        
        # 按钮容器
        button_frame = tk.Frame(inner_frame, bg=COLORS['card'])
        button_frame.pack(fill=tk.X, padx=25, pady=(0, 20))
        
        # 检测按钮
        self.detect_btn = tk.Button(
            button_frame,
            text="开始检测",
            font=("Microsoft YaHei UI", 12, "bold"),
            fg='white',
            bg=COLORS['accent_yellow'],
            activebackground=COLORS['button_hover'],
            activeforeground=COLORS['primary'],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.start_detection,
            padx=40,
            pady=12
        )
        self.detect_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 清空按钮
        clear_btn = tk.Button(
            button_frame,
            text="清空",
            font=("Microsoft YaHei UI", 11),
            fg=COLORS['secondary'],
            bg=COLORS['background'],
            activebackground=COLORS['border'],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.clear_input,
            padx=20,
            pady=12
        )
        clear_btn.pack(side=tk.LEFT)
    
    def create_result_section(self, parent):
        """创建结果显示区域"""
        self.result_frame = tk.Frame(parent, bg=COLORS['card'], relief=tk.FLAT)
        self.result_frame.pack(fill=tk.BOTH, pady=(0, 20))
        self.result_frame.pack_forget()  # 初始隐藏
        
        inner_frame = tk.Frame(self.result_frame, bg=COLORS['card'])
        inner_frame.pack(fill=tk.BOTH, padx=2, pady=2)
        
        # 结果图标和文字
        self.result_icon = tk.Label(
            inner_frame,
            text="",
            font=("Arial", 48),
            bg=COLORS['card']
        )
        self.result_icon.pack(pady=(30, 10))
        
        self.result_text = tk.Label(
            inner_frame,
            text="",
            font=("Microsoft YaHei UI", 22, "bold"),
            bg=COLORS['card']
        )
        self.result_text.pack(pady=(0, 10))
        
        self.result_confidence = tk.Label(
            inner_frame,
            text="",
            font=("Microsoft YaHei UI", 14),
            fg=COLORS['secondary'],
            bg=COLORS['card']
        )
        self.result_confidence.pack(pady=(0, 30))
    
    def create_features_section(self, parent):
        """创建特征详情区域"""
        self.features_frame = tk.Frame(parent, bg=COLORS['card'], relief=tk.FLAT)
        self.features_frame.pack(fill=tk.BOTH, expand=True)
        self.features_frame.pack_forget()  # 初始隐藏
        
        inner_frame = tk.Frame(self.features_frame, bg=COLORS['card'])
        inner_frame.pack(fill=tk.BOTH, padx=2, pady=2)
        
        # 标题
        title = tk.Label(
            inner_frame,
            text="特征分析",
            font=("Microsoft YaHei UI", 15, "bold"),
            fg=COLORS['primary'],
            bg=COLORS['card']
        )
        title.pack(anchor=tk.W, padx=25, pady=(20, 15))
        
        # 特征网格容器
        self.features_container = tk.Frame(inner_frame, bg=COLORS['card'])
        self.features_container.pack(fill=tk.BOTH, padx=25, pady=(0, 20))
    
    def clear_input(self):
        """清空输入"""
        self.url_entry.delete(0, tk.END)
        self.result_frame.pack_forget()
        self.features_frame.pack_forget()
    
    def start_detection(self):
        """开始检测"""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showwarning("警告", "请输入URL！")
            return
        
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)
        
        if self.is_detecting:
            return
        
        # 显示加载状态
        self.show_loading()
        
        # 在新线程中执行检测
        thread = threading.Thread(target=self.detect_url, args=(url,))
        thread.daemon = True
        thread.start()
    
    def show_loading(self):
        """显示加载状态"""
        self.is_detecting = True
        self.detect_btn.config(
            text="检测中...",
            state=tk.DISABLED,
            bg=COLORS['border']
        )
        self.result_frame.pack_forget()
        self.features_frame.pack_forget()
    
    def hide_loading(self):
        """隐藏加载状态"""
        self.is_detecting = False
        self.detect_btn.config(
            text="开始检测",
            state=tk.NORMAL,
            bg=COLORS['accent_yellow']
        )
    
    def detect_url(self, url):
        """检测URL（在后台线程运行）"""
        try:
            # 提取特征
            print(f"\n检测URL: {url}")
            features = extract_features(url)
            print(f"特征: {features}")
            
            # 创建DataFrame
            df = pd.DataFrame([features])
            
            # 预测
            prediction = self.model.predict(df)[0]
            probabilities = self.model.predict_proba(df)[0]
            
            is_phishing = (prediction == 1)
            confidence = probabilities[1] if is_phishing else probabilities[0]
            
            print(f"预测: {'钓鱼' if is_phishing else '合法'} (置信度: {confidence:.2%})")
            
            # 在主线程中更新UI
            self.root.after(0, self.show_result, is_phishing, confidence, features)
            
        except Exception as e:
            error_msg = f"检测失败: {str(e)}"
            print(f"错误: {error_msg}")
            self.root.after(0, lambda: messagebox.showerror("错误", error_msg))
            self.root.after(0, self.hide_loading)
    
    def show_result(self, is_phishing, confidence, features):
        """显示检测结果"""
        self.hide_loading()
        
        # 显示结果卡片
        self.result_frame.pack(fill=tk.BOTH, pady=(0, 20))
        
        # 设置图标和颜色
        if is_phishing:
            self.result_icon.config(text="⚠", fg=COLORS['accent_orange'])
            self.result_text.config(text="检测到钓鱼网站！", fg=COLORS['accent_orange'])
            self.result_frame.config(highlightbackground=COLORS['accent_orange'], highlightthickness=3)
        else:
            self.result_icon.config(text="✓", fg=COLORS['safe_green'])
            self.result_text.config(text="网站安全", fg=COLORS['safe_green'])
            self.result_frame.config(highlightbackground=COLORS['safe_green'], highlightthickness=3)
        
        # 置信度
        self.result_confidence.config(
            text=f"置信度: {confidence*100:.2f}%"
        )
        
        # 显示特征详情
        self.show_features(features)
    
    def show_features(self, features):
        """显示特征详情"""
        # 清空旧特征
        for widget in self.features_container.winfo_children():
            widget.destroy()
        
        # 特征名称映射
        feature_names = {
            'url_length': 'URL长度',
            'uses_ip': '使用IP地址',
            'num_dots': '点号数量',
            'protocol': 'HTTPS协议',
            'num_subdomains': '子域名数量',
            'domain_age_days': '域名年龄',
            'dns_valid': 'DNS有效性',
            'whois_info_exists': 'WHOIS信息',
            'has_iframe': '包含iframe',
            'has_obfuscated_js': '混淆JavaScript'
        }
        
        # 创建特征卡片（2列布局）
        row = 0
        col = 0
        for key, value in features.items():
            if key in feature_names:
                feature_card = self.create_feature_card(
                    self.features_container,
                    feature_names[key],
                    value
                )
                feature_card.grid(row=row, column=col, padx=10, pady=8, sticky='ew')
                
                col += 1
                if col >= 2:
                    col = 0
                    row += 1
        
        # 配置列权重
        self.features_container.columnconfigure(0, weight=1)
        self.features_container.columnconfigure(1, weight=1)
        
        # 显示特征区域
        self.features_frame.pack(fill=tk.BOTH, expand=True)
    
    def create_feature_card(self, parent, name, value):
        """创建特征卡片"""
        card = tk.Frame(parent, bg=COLORS['input_bg'], 
                       highlightbackground=COLORS['border'],
                       highlightthickness=1)
        
        # 特征名称
        name_label = tk.Label(
            card,
            text=name,
            font=("Microsoft YaHei UI", 11),
            fg=COLORS['secondary'],
            bg=COLORS['input_bg'],
            anchor=tk.W
        )
        name_label.pack(fill=tk.X, padx=15, pady=(10, 5))
        
        # 特征值
        value_text, value_color = self.format_feature_value(name, value)
        value_label = tk.Label(
            card,
            text=value_text,
            font=("Microsoft YaHei UI", 13, "bold"),
            fg=value_color,
            bg=COLORS['input_bg'],
            anchor=tk.W
        )
        value_label.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        return card
    
    def format_feature_value(self, name, value):
        """格式化特征值"""
        # 二值特征
        if name in ['使用IP地址', 'HTTPS协议', 'DNS有效性', 'WHOIS信息']:
            if value == 1:
                return "是 ✓", COLORS['safe_green']
            elif value == 0:
                return "否 ⚠", COLORS['accent_orange']
            else:
                return "未知", COLORS['secondary']
        
        # iframe和混淆JS
        elif name in ['包含iframe', '混淆JavaScript']:
            if value == 1:
                return "检测到 ⚠", COLORS['accent_orange']
            elif value == 0:
                return "未检测到 ✓", COLORS['safe_green']
            else:
                return "未检测", COLORS['secondary']
        
        # 域名年龄
        elif name == '域名年龄':
            if value == -1:
                return "未知", COLORS['secondary']
            elif value < 365:
                return f"{value} 天 ⚠", COLORS['accent_orange']
            else:
                return f"{value} 天 ✓", COLORS['safe_green']
        
        # 数值特征
        else:
            return str(value), COLORS['primary']


# ==================== 主程序 ====================
def main():
    root = tk.Tk()
    app = PhishingDetectorGUI(root)
    
    # 设置窗口图标（如果有的话）
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    # 居中显示
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    print("="*60)
    print("钓鱼网站检测系统 - GUI版本")
    print("="*60)
    main()
