"""
Flask后端服务器 - 真实模型版本
使用训练好的模型进行钓鱼网站检测
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import os
import sys

# 特征提取相关
import urllib.parse
import socket
import tldextract
import requests
from bs4 import BeautifulSoup
import datetime
import warnings

warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

# 全局变量
MODEL = None
FEATURE_NAMES = ['url_length', 'uses_ip', 'num_dots', 'protocol', 'num_subdomains',
                 'domain_age_days', 'dns_valid', 'whois_info_exists', 'has_iframe',
                 'has_obfuscated_js']

def load_model():
    """加载训练好的模型"""
    global MODEL
    
    model_path = 'phishing_url_model.pkl'
    
    # 尝试多个路径
    search_paths = [
        model_path,
        f'models/{model_path}',
        f'../Step3-Modeling/{model_path}',
        f'../../Step3-Modeling/{model_path}'
    ]
    
    for path in search_paths:
        if os.path.exists(path):
            try:
                MODEL = joblib.load(path)
                print(f'✓ 模型加载成功: {path}')
                print(f'  模型类型: {type(MODEL)}')
                print(f'  特征数量: {MODEL.n_features_in_}')
                return True
            except Exception as e:
                print(f'✗ 加载失败 {path}: {e}')
    
    print('⚠ 警告: 未找到模型文件，将使用规则引擎')
    return False


def extract_features(url):
    """
    提取URL的特征
    返回10个特征的列表
    """
    features = {}
    
    try:
        # 1. URL长度
        features['url_length'] = len(url)
        
        # 2. 是否使用IP地址
        try:
            domain = urllib.parse.urlparse(url).netloc
            domain_without_port = domain.split(':')[0]
            socket.inet_aton(domain_without_port)
            features['uses_ip'] = 1
        except:
            features['uses_ip'] = 0
        
        # 3. 点号数量
        features['num_dots'] = url.count('.')
        
        # 4. 协议 (https=1, http=0)
        features['protocol'] = 1 if urllib.parse.urlparse(url).scheme == 'https' else 0
        
        # 5. 子域名数量
        extracted = tldextract.extract(url)
        subdomains = extracted.subdomain.split('.')
        features['num_subdomains'] = len(subdomains) if extracted.subdomain else 0
        
        # 6. 域名年龄（简化处理，超时则为-1）
        features['domain_age_days'] = -1  # 默认值
        try:
            domain = f"{extracted.domain}.{extracted.suffix}"
            import whois
            whois_info = whois.whois(domain)
            if whois_info and hasattr(whois_info, 'creation_date'):
                creation_date = whois_info.creation_date
                if isinstance(creation_date, list):
                    creation_date = creation_date[0]
                if creation_date:
                    domain_age = (datetime.datetime.now() - creation_date).days
                    features['domain_age_days'] = domain_age
        except:
            pass
        
        # 7. DNS有效性
        try:
            domain = f"{extracted.domain}.{extracted.suffix}"
            socket.gethostbyname(domain)
            features['dns_valid'] = 1
        except:
            features['dns_valid'] = 0
        
        # 8. WHOIS信息存在
        features['whois_info_exists'] = 1 if features['domain_age_days'] > 0 else 0
        
        # 9-10. HTML特征（简化处理，超时则为0）
        features['has_iframe'] = 0
        features['has_obfuscated_js'] = 0
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=3, verify=False)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 检查iframe
                features['has_iframe'] = 1 if soup.find('iframe') else 0
                
                # 检查混淆JS
                scripts = soup.find_all('script')
                for script in scripts:
                    if script.string and ('eval(' in script.string or '\\x' in script.string):
                        features['has_obfuscated_js'] = 1
                        break
        except:
            pass
        
    except Exception as e:
        print(f'特征提取错误: {e}')
        # 返回默认特征
        features = {
            'url_length': len(url),
            'uses_ip': 0,
            'num_dots': 0,
            'protocol': 0,
            'num_subdomains': 0,
            'domain_age_days': -1,
            'dns_valid': 0,
            'whois_info_exists': 0,
            'has_iframe': 0,
            'has_obfuscated_js': 0
        }
    
    return features


def rule_based_prediction(features):
    """
    基于规则的预测（当模型不可用时使用）
    """
    risk_score = 0
    
    # 规则1: 使用IP地址 (+30分)
    if features['uses_ip'] == 1:
        risk_score += 30
    
    # 规则2: URL过长 (+20分)
    if features['url_length'] > 75:
        risk_score += 20
    
    # 规则3: 域名太新 (+25分)
    if 0 <= features['domain_age_days'] < 365:
        risk_score += 25
    
    # 规则4: 没有HTTPS (+15分)
    if features['protocol'] == 0:
        risk_score += 15
    
    # 规则5: 包含iframe (+20分)
    if features['has_iframe'] == 1:
        risk_score += 20
    
    # 规则6: 包含混淆JS (+25分)
    if features['has_obfuscated_js'] == 1:
        risk_score += 25
    
    # 规则7: DNS无效 (+30分)
    if features['dns_valid'] == 0:
        risk_score += 30
    
    # 规则8: 子域名过多 (+15分)
    if features['num_subdomains'] >= 3:
        risk_score += 15
    
    # 判断
    is_phishing = risk_score >= 50
    confidence = min(risk_score / 100, 0.99)
    
    return is_phishing, confidence, risk_score


@app.route('/')
def index():
    """返回主页"""
    return send_from_directory('.', 'index.html')


@app.route('/<path:path>')
def static_files(path):
    """返回静态文件"""
    return send_from_directory('.', path)


@app.route('/api/detect', methods=['POST'])
def detect():
    """
    检测URL是否为钓鱼网站
    
    请求格式:
    {
        "url": "http://example.com"
    }
    
    响应格式:
    {
        "is_phishing": true/false,
        "confidence": 0.95,
        "risk_score": 85,
        "features": {...},
        "method": "model/rule"
    }
    """
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': '请输入URL'}), 400
        
        # 添加协议前缀（如果没有）
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        print(f'\n检测URL: {url}')
        
        # 提取特征
        features = extract_features(url)
        print(f'特征: {features}')
        
        # 转换为特征向量
        feature_vector = [features[name] for name in FEATURE_NAMES]
        
        # 使用模型或规则引擎预测
        if MODEL is not None:
            # 使用模型
            try:
                prediction = MODEL.predict([feature_vector])[0]
                probabilities = MODEL.predict_proba([feature_vector])[0]
                
                is_phishing = bool(prediction == 1)
                confidence = float(probabilities[1] if is_phishing else probabilities[0])
                risk_score = int(probabilities[1] * 100)
                method = 'model'
                
                print(f'模型预测: {"钓鱼" if is_phishing else "合法"} (置信度: {confidence:.2%})')
                
            except Exception as e:
                print(f'模型预测失败: {e}，使用规则引擎')
                is_phishing, confidence, risk_score = rule_based_prediction(features)
                method = 'rule'
        else:
            # 使用规则引擎
            is_phishing, confidence, risk_score = rule_based_prediction(features)
            method = 'rule'
            print(f'规则预测: {"钓鱼" if is_phishing else "合法"} (风险分数: {risk_score})')
        
        # 返回结果
        response = {
            'is_phishing': is_phishing,
            'confidence': round(confidence, 4),
            'risk_score': risk_score,
            'features': features,
            'method': method
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f'检测错误: {e}')
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics', methods=['GET'])
def statistics():
    """
    返回系统统计信息
    """
    stats = {
        'model_loaded': MODEL is not None,
        'model_type': str(type(MODEL).__name__) if MODEL else 'RuleEngine',
        'feature_count': len(FEATURE_NAMES),
        'features': FEATURE_NAMES
    }
    
    if MODEL and hasattr(MODEL, 'n_estimators'):
        stats['n_estimators'] = MODEL.n_estimators
    
    return jsonify(stats)


@app.route('/api/model-info', methods=['GET'])
def model_info():
    """
    返回模型详细信息
    """
    if MODEL is None:
        return jsonify({'error': '模型未加载'}), 404
    
    info = {
        'type': str(type(MODEL).__name__),
        'n_features': MODEL.n_features_in_,
        'feature_names': FEATURE_NAMES,
        'classes': MODEL.classes_.tolist() if hasattr(MODEL, 'classes_') else None
    }
    
    # 如果是RandomForest，添加特征重要性
    if hasattr(MODEL, 'feature_importances_'):
        importances = MODEL.feature_importances_.tolist()
        info['feature_importances'] = dict(zip(FEATURE_NAMES, importances))
        
        # 排序
        sorted_features = sorted(
            zip(FEATURE_NAMES, importances),
            key=lambda x: x[1],
            reverse=True
        )
        info['top_features'] = [
            {'name': name, 'importance': float(imp)}
            for name, imp in sorted_features
        ]
    
    return jsonify(info)


if __name__ == '__main__':
    print('\n' + '='*60)
    print('钓鱼网站检测系统 - Web服务')
    print('='*60)
    
    # 加载模型
    model_loaded = load_model()
    
    if model_loaded:
        print('\n✓ 使用训练好的模型进行检测')
    else:
        print('\n⚠ 使用规则引擎进行检测（模型未找到）')
        print('  请将 phishing_url_model.pkl 放在以下位置之一:')
        print('  - 当前目录')
        print('  - models/ 目录')
        print('  - ../Step3-Modeling/ 目录')
    
    print('\n访问地址: http://localhost:5000')
    print('API接口: http://localhost:5000/api/detect')
    print('\n按 Ctrl+C 停止服务')
    print('='*60 + '\n')
    
    # 启动服务器
    app.run(host='0.0.0.0', port=5000, debug=True)
