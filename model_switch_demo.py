#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示如何切换不同AI模型
"""

import asyncio
import sys
import os
sys.path.insert(0, './src')

from ai_toolkit.utils.config import config
from ai_toolkit.ai.zhipu_provider import ZhipuProvider
from ai_toolkit.ai.base import AIRequest

async def test_different_models():
    """测试不同模型的效果"""
    print("=== AI模型版本切换演示 ===")

    # 可用的智谱AI模型
    models = [
        "glm-4-flash",    # 快速响应，成本低
        "glm-4",          # 标准模型，平衡性能
        "glm-4-air",      # 轻量级，适合简单任务
        "glm-3-turbo"     # 旧版，速度快
    ]

    test_prompt = "请简单介绍你自己，并说明你的特点"

    for model in models:
        print(f"\n--- 测试模型: {model} ---")

        try:
            # 创建自定义配置
            zhipu_config = {
                'model': model,
                'api_key': config.get_zhipu_config().get('api_key'),
                'max_tokens': 150,
                'temperature': 0.7,
                'timeout': 30
            }

            # 初始化AI提供商
            provider = ZhipuProvider(zhipu_config)
            await provider.initialize()

            # 发送请求
            request = AIRequest(
                messages=[
                    {"role": "user", "content": test_prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )

            response = await provider.chat_completion(request)

            print(f"模型: {model}")
            print(f"响应: {response.content}")
            print(f"Token使用: {response.usage.get('total_tokens', 'N/A') if response.usage else 'N/A'}")
            print("-" * 50)

        except Exception as e:
            print(f"模型 {model} 测试失败: {e}")

async def compare_model_performance():
    """比较不同模型的性能"""
    print("\n=== 模型性能对比 ===")

    tasks = [
        "简单任务：1+1等于几？",
        "中等任务：解释什么是机器学习",
        "复杂任务：设计一个AI辅助学习的应用方案"
    ]

    # 使用两个主要模型进行对比
    models_to_compare = ["glm-4-flash", "glm-4"]

    for task in tasks:
        print(f"\n任务: {task}")
        print("=" * 60)

        for model in models_to_compare:
            print(f"\n{model} 的回答:")

            try:
                zhipu_config = {
                    'model': model,
                    'api_key': config.get_zhipu_config().get('api_key'),
                    'max_tokens': 200,
                    'temperature': 0.7
                }

                provider = ZhipuProvider(zhipu_config)
                await provider.initialize()

                request = AIRequest(
                    messages=[
                        {"role": "user", "content": task}
                    ],
                    max_tokens=200,
                    temperature=0.7
                )

                import time
                start_time = time.time()
                response = await provider.chat_completion(request)
                end_time = time.time()

                print(f"内容: {response.content}")
                print(f"响应时间: {end_time - start_time:.2f}秒")
                print(f"Token使用: {response.usage.get('total_tokens', 'N/A') if response.usage else 'N/A'}")

            except Exception as e:
                print(f"请求失败: {e}")

if __name__ == "__main__":
    if sys.platform == "win32":
        os.system("chcp 65001 > nul")

    os.environ['PYTHONIOENCODING'] = 'utf-8'

    # 运行模型测试
    asyncio.run(test_different_models())

    # 运行性能对比
    asyncio.run(compare_model_performance())

    print("\n=== 模型选择建议 ===")
    print("1. glm-4-flash: 适合日常对话、简单任务，响应快、成本低")
    print("2. glm-4: 适合复杂分析、创意任务，质量高、成本适中")
    print("3. glm-4-air: 适合轻量级任务，平衡速度和质量")
    print("4. glm-3-turbo: 适合快速响应场景，成本最低")
    print("\n根据你的需求选择合适的模型！")