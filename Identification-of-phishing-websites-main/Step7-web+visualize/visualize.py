"""
模型评估和可视化生成 - 莫兰迪色系
生成专业的模型性能可视化图表
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix, classification_report, 
    roc_curve, auc, precision_recall_curve
)
from sklearn.model_selection import learning_curve
import joblib
import warnings
warnings.filterwarnings('ignore')

# 设置莫兰迪色系
COLORS = {
    'primary': '#3A3632',      # 柔和炭黑
    'warm_orange': '#D4886E',  # 暖橙红
    'ginger': '#D4A574',       # 暖姜黄
    'green': '#828B78',        # 绿色
    'surface': '#E8DCC8',      # 驼色
    'light': '#F9F5ED',        # 浅杏色
    'border': '#C9BFB0',       # 边框
    'text': '#2D2A27'          # 文字
}

# 设置全局样式
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette([COLORS['warm_orange'], COLORS['ginger'], COLORS['green'], COLORS['surface']])

# 配置字体
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.facecolor'] = COLORS['light']
plt.rcParams['axes.facecolor'] = COLORS['light']


def set_clean_style(ax):
    """设置简洁的图表样式 - 无圆角，强对比"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['primary'])
    ax.spines['bottom'].set_color(COLORS['primary'])
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    
    ax.tick_params(colors=COLORS['text'], width=2, length=6)
    ax.grid(True, alpha=0.2, color=COLORS['border'], linewidth=1)
    ax.set_facecolor(COLORS['light'])


def create_confusion_matrix_viz(y_true, y_pred, save_path='output/confusion_matrix.png'):
    """创建混淆矩阵可视化"""
    cm = confusion_matrix(y_true, y_pred)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 使用自定义颜色映射
    cmap_colors = [COLORS['light'], COLORS['green']]
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list('morandi_green', cmap_colors)
    
    # 绘制热图
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap, aspect='auto')
    
    # 添加数值标注
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], 'd'),
                   ha="center", va="center",
                   color=COLORS['text'] if cm[i, j] > thresh else COLORS['primary'],
                   fontsize=32, fontweight='bold')
    
    # 设置标签
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['合法网站', '钓鱼网站'], fontsize=14, color=COLORS['text'])
    ax.set_yticklabels(['合法网站', '钓鱼网站'], fontsize=14, color=COLORS['text'])
    
    ax.set_xlabel('预测标签', fontsize=16, color=COLORS['primary'], fontweight='500', labelpad=15)
    ax.set_ylabel('真实标签', fontsize=16, color=COLORS['primary'], fontweight='500', labelpad=15)
    ax.set_title('混淆矩阵 Confusion Matrix', 
                fontsize=20, color=COLORS['primary'], fontweight='600', pad=20)
    
    # 移除边框
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, facecolor=COLORS['light'], edgecolor='none', bbox_inches='tight')
    print(f"✓ 混淆矩阵已保存: {save_path}")
    plt.close()


def create_feature_importance_viz(feature_names, importances, save_path='output/feature_importance.png'):
    """创建特征重要性可视化 - 水平条形图"""
    # 排序
    indices = np.argsort(importances)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 绘制水平条形图
    bars = ax.barh(range(len(indices)), importances[indices], 
                   color=COLORS['ginger'], edgecolor=COLORS['primary'], linewidth=2)
    
    # 设置标签
    ax.set_yticks(range(len(indices)))
    ax.set_yticklabels([feature_names[i] for i in indices], 
                       fontsize=13, color=COLORS['text'], fontweight='500')
    ax.set_xlabel('特征重要性', fontsize=14, color=COLORS['primary'], fontweight='500', labelpad=15)
    ax.set_title('特征重要性排序 Feature Importance', 
                fontsize=20, color=COLORS['primary'], fontweight='600', pad=20)
    
    # 添加数值标注
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, 
               f'{width:.3f}',
               ha='left', va='center', fontsize=11, color=COLORS['text'], 
               fontweight='500', bbox=dict(boxstyle='square,pad=0.3', 
                                          facecolor='white', 
                                          edgecolor=COLORS['border'], 
                                          linewidth=1))
    
    set_clean_style(ax)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, facecolor=COLORS['light'], edgecolor='none', bbox_inches='tight')
    print(f"✓ 特征重要性图已保存: {save_path}")
    plt.close()


def create_roc_curve_viz(y_true, y_proba, save_path='output/roc_curve.png'):
    """创建ROC曲线可视化"""
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    roc_auc = auc(fpr, tpr)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # 绘制ROC曲线
    ax.plot(fpr, tpr, color=COLORS['green'], linewidth=3, 
           label=f'ROC Curve (AUC = {roc_auc:.3f})')
    
    # 绘制对角线
    ax.plot([0, 1], [0, 1], color=COLORS['border'], linewidth=2, 
           linestyle='--', label='Random Classifier')
    
    # 设置标签和标题
    ax.set_xlabel('False Positive Rate', fontsize=14, color=COLORS['primary'], 
                 fontweight='500', labelpad=15)
    ax.set_ylabel('True Positive Rate', fontsize=14, color=COLORS['primary'], 
                 fontweight='500', labelpad=15)
    ax.set_title('ROC曲线分析 ROC Curve', fontsize=20, color=COLORS['primary'], 
                fontweight='600', pad=20)
    
    # 图例
    ax.legend(loc='lower right', fontsize=12, frameon=True, 
             facecolor='white', edgecolor=COLORS['border'], 
             framealpha=1, borderpad=1)
    
    # 设置范围
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    
    set_clean_style(ax)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, facecolor=COLORS['light'], edgecolor='none', bbox_inches='tight')
    print(f"✓ ROC曲线已保存: {save_path}")
    plt.close()


def create_precision_recall_viz(y_true, y_proba, save_path='output/precision_recall.png'):
    """创建Precision-Recall曲线"""
    precision, recall, _ = precision_recall_curve(y_true, y_proba)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # 绘制PR曲线
    ax.plot(recall, precision, color=COLORS['warm_orange'], linewidth=3, 
           label='Precision-Recall Curve')
    
    # 填充区域
    ax.fill_between(recall, precision, alpha=0.2, color=COLORS['warm_orange'])
    
    # 设置标签和标题
    ax.set_xlabel('Recall', fontsize=14, color=COLORS['primary'], 
                 fontweight='500', labelpad=15)
    ax.set_ylabel('Precision', fontsize=14, color=COLORS['primary'], 
                 fontweight='500', labelpad=15)
    ax.set_title('精确率-召回率曲线 Precision-Recall Curve', 
                fontsize=20, color=COLORS['primary'], fontweight='600', pad=20)
    
    ax.legend(loc='lower left', fontsize=12, frameon=True, 
             facecolor='white', edgecolor=COLORS['border'], 
             framealpha=1, borderpad=1)
    
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    
    set_clean_style(ax)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, facecolor=COLORS['light'], edgecolor='none', bbox_inches='tight')
    print(f"✓ Precision-Recall曲线已保存: {save_path}")
    plt.close()


def create_training_history_viz(history_data, save_path='output/training_history.png'):
    """创建训练历史可视化"""
    epochs = history_data['epoch']
    train_loss = history_data['train_loss']
    val_loss = history_data['val_loss']
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # 绘制训练和验证损失
    ax.plot(epochs, train_loss, color=COLORS['warm_orange'], 
           linewidth=2.5, label='Training Loss', marker='o', markersize=4, 
           markevery=10)
    ax.plot(epochs, val_loss, color=COLORS['ginger'], 
           linewidth=2.5, label='Validation Loss', marker='s', markersize=4, 
           markevery=10)
    
    # 设置标签和标题
    ax.set_xlabel('Epoch', fontsize=14, color=COLORS['primary'], 
                 fontweight='500', labelpad=15)
    ax.set_ylabel('Loss', fontsize=14, color=COLORS['primary'], 
                 fontweight='500', labelpad=15)
    ax.set_title('训练历史 Training History', fontsize=20, 
                color=COLORS['primary'], fontweight='600', pad=20)
    
    ax.legend(loc='upper right', fontsize=12, frameon=True, 
             facecolor='white', edgecolor=COLORS['border'], 
             framealpha=1, borderpad=1)
    
    set_clean_style(ax)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, facecolor=COLORS['light'], edgecolor='none', bbox_inches='tight')
    print(f"✓ 训练历史图已保存: {save_path}")
    plt.close()


def create_classification_report_viz(y_true, y_pred, save_path='output/classification_report.png'):
    """创建分类报告可视化"""
    from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
    
    # 计算指标
    metrics = {
        '准确率\nAccuracy': accuracy_score(y_true, y_pred),
        '精确率\nPrecision': precision_score(y_true, y_pred, average='weighted'),
        '召回率\nRecall': recall_score(y_true, y_pred, average='weighted'),
        'F1分数\nF1-Score': f1_score(y_true, y_pred, average='weighted')
    }
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 绘制条形图
    x_pos = np.arange(len(metrics))
    values = list(metrics.values())
    bars = ax.bar(x_pos, values, color=[COLORS['green'], COLORS['ginger'], 
                                        COLORS['warm_orange'], COLORS['surface']], 
                 edgecolor=COLORS['primary'], linewidth=2, width=0.6)
    
    # 添加数值标注
    for i, (bar, value) in enumerate(zip(bars, values)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{value:.3f}',
               ha='center', va='bottom', fontsize=14, 
               color=COLORS['text'], fontweight='600')
    
    # 设置标签
    ax.set_xticks(x_pos)
    ax.set_xticklabels(metrics.keys(), fontsize=13, color=COLORS['text'], 
                      fontweight='500')
    ax.set_ylabel('分数 Score', fontsize=14, color=COLORS['primary'], 
                 fontweight='500', labelpad=15)
    ax.set_title('模型性能指标 Model Performance Metrics', 
                fontsize=20, color=COLORS['primary'], fontweight='600', pad=20)
    
    ax.set_ylim([0, 1.1])
    
    set_clean_style(ax)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, facecolor=COLORS['light'], edgecolor='none', bbox_inches='tight')
    print(f"✓ 分类报告已保存: {save_path}")
    plt.close()


def generate_all_visualizations(model_path='models/phishing_url_model.pkl',
                                test_data_path='data/test_data.csv'):
    """生成所有可视化图表"""
    import os
    os.makedirs('output', exist_ok=True)
    
    print("\n" + "="*60)
    print("开始生成可视化图表 - 莫兰迪色系")
    print("="*60 + "\n")
    
    # 生成模拟数据（实际使用时替换为真实数据）
    np.random.seed(42)
    n_samples = 1800
    
    # 模拟真实标签和预测
    y_true = np.random.randint(0, 2, n_samples)
    y_pred = y_true.copy()
    # 添加一些错误预测
    error_indices = np.random.choice(n_samples, int(n_samples * 0.05), replace=False)
    y_pred[error_indices] = 1 - y_pred[error_indices]
    
    # 模拟概率输出
    y_proba = np.random.beta(8, 2, n_samples)
    y_proba[y_true == 0] = 1 - np.random.beta(8, 2, np.sum(y_true == 0))
    
    # 1. 混淆矩阵
    create_confusion_matrix_viz(y_true, y_pred)
    
    # 2. 特征重要性
    feature_names = np.array(['URL长度', '域名年龄', 'HTTPS协议', 'DNS有效性', 
                             '子域名数量', 'IP地址', '特殊字符'])
    importances = np.array([0.245, 0.198, 0.156, 0.134, 0.112, 0.089, 0.066])
    create_feature_importance_viz(feature_names, importances)
    
    # 3. ROC曲线
    create_roc_curve_viz(y_true, y_proba)
    
    # 4. Precision-Recall曲线
    create_precision_recall_viz(y_true, y_proba)
    
    # 5. 训练历史
    epochs = np.arange(1, 101)
    train_loss = 0.5 * np.exp(-epochs / 20) + np.random.rand(100) * 0.05
    val_loss = 0.55 * np.exp(-epochs / 18) + np.random.rand(100) * 0.06
    history_data = {
        'epoch': epochs,
        'train_loss': train_loss,
        'val_loss': val_loss
    }
    create_training_history_viz(history_data)
    
    # 6. 分类报告
    create_classification_report_viz(y_true, y_pred)
    
    print("\n" + "="*60)
    print("✓ 所有可视化图表生成完成！")
    print("图表保存在 output/ 目录")
    print("="*60 + "\n")


if __name__ == '__main__':
    generate_all_visualizations()
