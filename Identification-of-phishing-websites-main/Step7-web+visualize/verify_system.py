#!/usr/bin/env python3
"""
钓鱼网站检测系统 - 验证脚本
用于检查系统各组件是否正常工作
"""

import os
import sys

def check_files():
    """检查所有必需文件是否存在"""
    print("📁 检查文件...")
    required_files = [
        'index.html',
        'app.js',
        'server_fixed.py',
        'README.md',
        'QUICK_START.md',
        'OPTIMIZATION_NOTES.md',
        'COMPARISON.md'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - 缺失")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  缺少 {len(missing_files)} 个文件")
        return False
    else:
        print(f"\n✅ 所有 {len(required_files)} 个文件都存在")
        return True

def check_dependencies():
    """检查Python依赖"""
    print("\n📦 检查Python依赖...")
    required_modules = [
        'flask',
        'flask_cors',
        'joblib',
        'numpy'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module} - 未安装")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️  缺少 {len(missing_modules)} 个依赖包")
        print("💡 安装命令:")
        print("   pip install flask flask-cors joblib numpy scikit-learn")
        return False
    else:
        print(f"\n✅ 所有 {len(required_modules)} 个依赖都已安装")
        return True

def check_html_structure():
    """检查HTML文件结构"""
    print("\n🔍 检查HTML结构...")
    
    if not os.path.exists('index.html'):
        print("  ❌ index.html 不存在")
        return False
    
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        'Chart.js': 'chart.js' in content.lower(),
        '混淆矩阵Canvas': 'confusionMatrix' in content,
        '特征重要性Canvas': 'featureImportance' in content,
        'ROC曲线Canvas': 'rocCurve' in content,
        '训练历史Canvas': 'trainingHistory' in content,
        'app.js引用': 'app' in content and '.js' in content
    }
    
    all_passed = True
    for check_name, passed in checks.items():
        if passed:
            print(f"  ✅ {check_name}")
        else:
            print(f"  ❌ {check_name}")
            all_passed = False
    
    return all_passed

def check_js_structure():
    """检查JavaScript文件结构"""
    print("\n🔍 检查JavaScript结构...")
    
    if not os.path.exists('app.js'):
        print("  ❌ app.js 不存在")
        return False
    
    with open('app.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        '配色定义': 'const colors' in content,
        '混淆矩阵函数': 'createConfusionMatrix' in content,
        '特征重要性函数': 'createFeatureImportance' in content,
        'ROC曲线函数': 'createROCCurve' in content,
        '训练历史函数': 'createTrainingHistory' in content,
        'URL检测函数': 'detectURL' in content
    }
    
    all_passed = True
    for check_name, passed in checks.items():
        if passed:
            print(f"  ✅ {check_name}")
        else:
            print(f"  ❌ {check_name}")
            all_passed = False
    
    return all_passed

def get_file_sizes():
    """获取文件大小信息"""
    print("\n📊 文件大小统计...")
    
    files = {
        'index.html': 'HTML页面',
        'app.js': 'JavaScript',
        'server_fixed.py': 'Python后端',
        'README.md': '主文档',
        'QUICK_START.md': '快速启动',
        'OPTIMIZATION_NOTES.md': '优化说明',
        'COMPARISON.md': '对比文档'
    }
    
    total_size = 0
    for filename, description in files.items():
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            total_size += size
            print(f"  📄 {description:20} {size:>8,} bytes")
    
    print(f"\n  📦 总计: {total_size:>8,} bytes ({total_size/1024:.1f} KB)")

def print_summary():
    """打印总结信息"""
    print("\n" + "="*60)
    print("🎉 系统验证完成！")
    print("="*60)
    print("\n📚 下一步:")
    print("  1. 阅读 README.md 了解系统概览")
    print("  2. 查看 QUICK_START.md 快速开始")
    print("  3. 运行 'python server_fixed.py' 启动服务")
    print("  4. 访问 http://localhost:5000")
    print("\n💡 提示:")
    print("  - 所有文档都包含详细的使用说明")
    print("  - 遇到问题请先查看 QUICK_START.md 的故障排除部分")
    print("  - 图表优化细节请参考 OPTIMIZATION_NOTES.md")
    print("\n" + "="*60)

def main():
    """主函数"""
    print("\n" + "="*60)
    print("🛡️  钓鱼网站检测系统 v2.0 - 验证工具")
    print("="*60)
    
    results = []
    
    # 执行各项检查
    results.append(("文件完整性", check_files()))
    results.append(("Python依赖", check_dependencies()))
    results.append(("HTML结构", check_html_structure()))
    results.append(("JavaScript结构", check_js_structure()))
    
    # 显示文件大小
    get_file_sizes()
    
    # 统计结果
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n📋 检查结果: {passed}/{total} 通过")
    
    for check_name, result in results:
        status = "✅" if result else "❌"
        print(f"  {status} {check_name}")
    
    # 打印总结
    if passed == total:
        print_summary()
        return 0
    else:
        print("\n⚠️  部分检查未通过，请修复上述问题后重试")
        return 1

if __name__ == '__main__':
    sys.exit(main())
