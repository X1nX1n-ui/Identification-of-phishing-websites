#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
环境测试脚本 - 检查所有依赖是否正确安装
"""

import sys


def test_imports():
    """测试所有必需的库"""

    print("=" * 60)
    print("钓鱼网站检测项目 - 环境测试")
    print("=" * 60)
    print(f"\nPython版本: {sys.version}\n")
    print("-" * 60)

    # 定义要测试的库
    tests = [
        ("numpy", "NumPy"),
        ("pandas", "Pandas"),
        ("sklearn", "Scikit-learn"),
        ("torch", "PyTorch"),
        ("requests", "Requests"),
        ("bs4", "BeautifulSoup4"),
        ("whois", "python-whois"),
        ("tldextract", "TLD Extract"),
        ("joblib", "Joblib"),
        ("tkinter", "Tkinter (GUI)"),
    ]

    success_count = 0
    fail_count = 0

    for module_name, display_name in tests:
        try:
            module = __import__(module_name)
            version = getattr(module, "__version__", "已安装")
            print(f"✓ {display_name:20s} {version}")
            success_count += 1
        except ImportError as e:
            print(f"✗ {display_name:20s} 未安装 - {str(e)}")
            fail_count += 1

    print("-" * 60)

    # PyTorch特殊测试
    try:
        import torch
        print(f"\nPyTorch详细信息:")
        print(f"  - 版本: {torch.__version__}")
        print(f"  - CUDA可用: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"  - CUDA版本: {torch.version.cuda}")
            print(f"  - GPU设备数量: {torch.cuda.device_count()}")
    except:
        pass

    print("\n" + "=" * 60)
    print(f"测试完成: {success_count} 成功, {fail_count} 失败")
    print("=" * 60)

    if fail_count == 0:
        print("\n✓ 所有依赖已正确安装，可以开始项目开发！")
    else:
        print(f"\n✗ 有 {fail_count} 个库未安装，请检查安装步骤")

    return fail_count == 0


if __name__ == "__main__":
    test_imports()