#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试实际 ZhipuProvider 的功能
"""

import asyncio
import sys
import os
import json

# 设置编码
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 添加 src 目录到路径
sys.path.insert(0, './src')

# 设置环境变量
os.environ['ZHIPU_API_KEY'] = "31b5715b41cd4e6e8dde08232ec63146.Jjs6gp46gAYsI5sl"
os.environ['ZAI_API_KEY'] = "31b5715b41cd4e6e8dde08232ec63146.Jjs6gp46gAYsI5sl"

async def test_zhipu_provider():
    """测试 ZhipuProvider"""
    print("=== 测试实际 ZhipuProvider ===")

    try:
        # 1. 导入模块
        print("\n1.1 导入 ZhipuProvider...")
        from ai_toolkit.ai.zhipu_provider import ZhipuProvider
        from ai_toolkit.utils.config import config
        print("   导入成功！")

        # 2. 加载配置
        print("\n2.1 加载配置...")
        config.load_config()
        zhipu_config = config.get_zhipu_config()
        print(f"   配置加载成功: {zhipu_config}")

        # 3. 初始化 Provider
        print("\n3.1 初始化 ZhipuProvider...")
        provider = ZhipuProvider(zhipu_config)
        print("   Provider 创建成功！")

        # 4. 初始化连接
        print("\n4.1 初始化连接...")
        await provider.initialize()
        print("   连接初始化成功！")

        # 5. 测试聊天
        print("\n5.1 测试聊天功能...")
        from ai_toolkit.ai.base import AIRequest

        request = AIRequest(
            messages=[
                {"role": "user", "content": "你好，请简单介绍一下你自己"}
            ],
            max_tokens=100,
            temperature=0.7
        )

        response = await provider.chat_completion(request)
        print(f"   AI响应: {response.content}")
        print(f"   使用量: {response.usage}")

        print("\n=== ZhipuProvider 测试成功 ===")
        return True

    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_zhipu_provider())
    if success:
        print("\n[SUCCESS] 实际 ZhipuProvider 可用！")
    else:
        print("\n[ERROR] 实际 ZhipuProvider 有问题")