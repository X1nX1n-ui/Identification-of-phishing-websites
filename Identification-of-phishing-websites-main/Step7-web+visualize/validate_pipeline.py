"""
数据流转跟踪和验证脚本
帮助理解和验证整个数据处理流程
"""

import pandas as pd
import os
from datetime import datetime

class DataPipelineTracker:
    """数据处理流程跟踪器"""
    
    def __init__(self):
        self.steps = []
        
    def track_step(self, step_name, input_file, output_file, description):
        """记录处理步骤"""
        step_info = {
            'step': step_name,
            'input': input_file,
            'output': output_file,
            'description': description,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 检查文件是否存在并获取信息
        if os.path.exists(input_file):
            df_input = pd.read_csv(input_file)
            step_info['input_rows'] = len(df_input)
            step_info['input_cols'] = len(df_input.columns)
        else:
            step_info['input_rows'] = 'N/A'
            step_info['input_cols'] = 'N/A'
            
        if os.path.exists(output_file):
            df_output = pd.read_csv(output_file)
            step_info['output_rows'] = len(df_output)
            step_info['output_cols'] = len(df_output.columns)
        else:
            step_info['output_rows'] = 'N/A'
            step_info['output_cols'] = 'N/A'
        
        self.steps.append(step_info)
        
    def print_summary(self):
        """打印流程摘要"""
        print("\n" + "="*80)
        print("数据处理流程摘要")
        print("="*80)
        
        for i, step in enumerate(self.steps, 1):
            print(f"\n{i}. {step['step']}")
            print(f"   描述: {step['description']}")
            print(f"   输入: {step['input']}")
            print(f"          行数: {step['input_rows']}, 列数: {step['input_cols']}")
            print(f"   输出: {step['output']}")
            print(f"          行数: {step['output_rows']}, 列数: {step['output_cols']}")
            
            if isinstance(step['input_rows'], int) and isinstance(step['output_rows'], int):
                change = step['output_rows'] - step['input_rows']
                if change > 0:
                    print(f"   变化: +{change} 行 ⬆")
                elif change < 0:
                    print(f"   变化: {change} 行 ⬇")
                else:
                    print(f"   变化: 无变化 ━")
        
        print("\n" + "="*80)


def validate_data_pipeline():
    """验证完整的数据处理流程"""
    
    print("\n" + "="*80)
    print("钓鱼网站检测项目 - 数据流转验证")
    print("="*80)
    
    tracker = DataPipelineTracker()
    
    # Step 1: 数据收集与标注
    print("\n检查 Step 1: 数据收集与标注...")
    input_file_1 = "Step1-Label/phish_url.csv"
    output_file_1 = "Step1-Label/phishing_dataset1.csv"
    
    if os.path.exists(output_file_1):
        print(f"✓ 找到: {output_file_1}")
        df1 = pd.read_csv(output_file_1)
        print(f"  样本数: {len(df1)}")
        print(f"  列: {df1.columns.tolist()}")
        if 'label' in df1.columns:
            print(f"  标签分布:")
            print(f"    合法 (0): {sum(df1['label']==0)}")
            print(f"    钓鱼 (1): {sum(df1['label']==1)}")
        
        tracker.track_step(
            "Step 1: 数据收集与标注",
            input_file_1,
            output_file_1,
            "从PhishTank和CommonCrawl收集并标注URL"
        )
    else:
        print(f"✗ 未找到: {output_file_1}")
        print(f"  请先运行: cd Step1-Label && python pre-processing.py")
    
    # Step 2: 特征提取
    print("\n检查 Step 2: 特征提取...")
    input_file_2 = "Step2-Feature/phishing_dataset1.csv"
    output_file_2 = "Step2-Feature/url_features.csv"
    
    if os.path.exists(output_file_2):
        print(f"✓ 找到: {output_file_2}")
        df2 = pd.read_csv(output_file_2)
        print(f"  样本数: {len(df2)}")
        print(f"  特征数: {len(df2.columns) - 1}")  # 减去label列
        print(f"  列: {df2.columns.tolist()}")
        
        # 检查缺失值
        missing = df2.isnull().sum().sum()
        if missing > 0:
            print(f"  ⚠ 缺失值: {missing} 个")
        else:
            print(f"  ✓ 无缺失值")
        
        # 检查-1值（特征提取失败）
        neg_ones = (df2 == -1).sum().sum()
        if neg_ones > 0:
            print(f"  ⚠ 值为-1: {neg_ones} 个（特征提取失败）")
        
        tracker.track_step(
            "Step 2: 特征提取",
            input_file_2,
            output_file_2,
            "提取URL的10个特征"
        )
    else:
        print(f"✗ 未找到: {output_file_2}")
        print(f"  请先运行: cd Step2-Feature && python featureExtractor.py")
    
    # Step 2.5: 数据清洗
    print("\n检查 Step 2.5: 数据清洗...")
    input_file_3 = "Step2-Feature/url_features.csv"
    output_file_3 = "Step2-Feature/url_features_final.csv"
    
    if os.path.exists(output_file_3):
        print(f"✓ 找到: {output_file_3}")
        df3 = pd.read_csv(output_file_3)
        print(f"  样本数: {len(df3)}")
        print(f"  特征数: {len(df3.columns) - 1}")
        
        # 数据质量检查
        missing = df3.isnull().sum().sum()
        print(f"  缺失值: {missing} 个")
        
        neg_ones = (df3 == -1).sum().sum()
        print(f"  值为-1: {neg_ones} 个")
        
        if 'label' in df3.columns:
            label_counts = df3['label'].value_counts()
            ratio = label_counts.max() / label_counts.min()
            print(f"  标签平衡: {ratio:.2f}:1")
        
        tracker.track_step(
            "Step 2.5: 数据清洗",
            input_file_3,
            output_file_3,
            "清洗数据：处理缺失值、异常值、重复值"
        )
    else:
        print(f"✗ 未找到: {output_file_3}")
        print(f"  建议运行: cd Step2-Feature && python clean_data.py")
    
    # Step 3: 模型训练
    print("\n检查 Step 3: 模型训练...")
    input_file_4 = "Step3-Modeling/url_features_final.csv"
    output_file_4 = "Step3-Modeling/phishing_url_model.pkl"
    
    if os.path.exists(output_file_4):
        print(f"✓ 找到: {output_file_4}")
        file_size = os.path.getsize(output_file_4) / 1024  # KB
        print(f"  模型大小: {file_size:.2f} KB")
        
        # 检查是否有其他输出
        if os.path.exists("Step3-Modeling/selected_features.csv"):
            print(f"  ✓ 找到特征选择结果")
    else:
        print(f"✗ 未找到: {output_file_4}")
        print(f"  请先运行: cd Step3-Modeling && python model.py")
    
    # 打印流程摘要
    tracker.print_summary()
    
    # 数据流转图
    print("\n" + "="*80)
    print("数据流转示意图")
    print("="*80)
    print("""
    phish_url.csv (PhishTank原始数据)
           |
           | pre-processing.py
           ↓
    phishing_dataset1.csv (标注数据: url + label)
           |
           | featureExtractor.py
           ↓
    url_features.csv (特征数据: 10特征 + label)
           |
           | clean_data.py (可选但推荐)
           ↓
    url_features_final.csv (清洗后的数据)
           |
           | model.py
           ↓
    phishing_url_model.pkl (训练好的模型)
           |
           ↓
    应用 (GUI.py / Web版本)
    """)
    
    # 建议下一步操作
    print("\n" + "="*80)
    print("建议的下一步操作")
    print("="*80)
    
    if not os.path.exists(output_file_1):
        print("\n1. 运行 Step1:")
        print("   cd Step1-Label")
        print("   python pre-processing.py")
    elif not os.path.exists(output_file_2):
        print("\n1. 复制数据到 Step2:")
        print("   cp Step1-Label/phishing_dataset1.csv Step2-Feature/")
        print("\n2. 运行 Step2:")
        print("   cd Step2-Feature")
        print("   python featureExtractor.py")
    elif not os.path.exists(output_file_3):
        print("\n1. 运行数据清洗:")
        print("   cd Step2-Feature")
        print("   python clean_data.py")
    elif not os.path.exists(output_file_4):
        print("\n1. 复制数据到 Step3:")
        print("   cp Step2-Feature/url_features_final.csv Step3-Modeling/")
        print("\n2. 运行 Step3:")
        print("   cd Step3-Modeling")
        print("   python model.py")
    else:
        print("\n✓ 所有步骤已完成！")
        print("\n你可以:")
        print("1. 运行GUI应用: cd Step4-GUI && python GUI.py")
        print("2. 运行Web应用: python server.py")
        print("3. 生成可视化: python visualize.py")
    
    print("\n" + "="*80)


def create_sample_data():
    """创建示例数据用于测试流程"""
    
    print("\n创建示例数据用于测试...")
    
    # 创建Step1输出示例
    sample_data_1 = pd.DataFrame({
        'url': [
            'http://fake-paypal.com/login.php',
            'https://www.google.com',
            'http://phishing-bank.tk/verify.html',
            'https://www.microsoft.com',
            'http://192.168.1.1/admin.php'
        ],
        'label': [1, 0, 1, 0, 1]
    })
    
    os.makedirs('Step1-Label', exist_ok=True)
    sample_data_1.to_csv('Step1-Label/phishing_dataset1_sample.csv', index=False)
    print(f"✓ 创建示例数据: Step1-Label/phishing_dataset1_sample.csv")
    
    # 创建Step2输出示例
    sample_data_2 = pd.DataFrame({
        'url_length': [32, 23, 38, 27, 28],
        'uses_ip': [0, 0, 0, 0, 1],
        'num_dots': [2, 2, 3, 2, 3],
        'protocol': [0, 1, 0, 1, 0],
        'num_subdomains': [1, 1, 2, 1, 0],
        'domain_age_days': [30, 7300, 15, 5475, -1],
        'dns_valid': [1, 1, 1, 1, 0],
        'whois_info_exists': [1, 1, 0, 1, 0],
        'has_iframe': [1, 0, 1, 0, 0],
        'has_obfuscated_js': [1, 0, 1, 0, 0],
        'label': [1, 0, 1, 0, 1]
    })
    
    os.makedirs('Step2-Feature', exist_ok=True)
    sample_data_2.to_csv('Step2-Feature/url_features_sample.csv', index=False)
    print(f"✓ 创建示例数据: Step2-Feature/url_features_sample.csv")
    
    print("\n示例数据创建完成！可以用于理解数据格式。")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--create-sample':
        create_sample_data()
    else:
        validate_data_pipeline()
