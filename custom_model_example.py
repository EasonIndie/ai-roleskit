#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义模型使用示例
"""

import asyncio
import sys
import os
sys.path.insert(0, './src')

from ai_toolkit.utils.config import config
from ai_toolkit.ai.zhipu_provider import ZhipuProvider
from ai_toolkit.ai.base import AIRequest

async def custom_model_example():
    """演示如何在代码中指定不同模型"""
    print("=== 自定义模型使用示例 ===")

    # 获取API密钥
    api_key = config.get_zhipu_config().get('api_key')

    # 示例1：使用快速模型处理简单任务
    print("\n1. 使用 glm-4-flash 处理简单任务")
    quick_config = {
        'model': 'glm-4-flash',      # 指定快速模型
        'api_key': api_key,
        'max_tokens': 100,           # 较小的token限制
        'temperature': 0.5           # 较低的随机性
    }

    quick_provider = ZhipuProvider(quick_config)
    await quick_provider.initialize()

    quick_request = AIRequest(
        messages=[
            {"role": "user", "content": "你好，请简单介绍一下你的功能"}
        ],
        max_tokens=100
    )

    quick_response = await quick_provider.chat_completion(quick_request)
    print(f"快速模型响应: {quick_response.content}")

    # 示例2：使用标准模型处理复杂任务
    print("\n2. 使用 glm-4 处理复杂任务")
    standard_config = {
        'model': 'glm-4',           # 指定标准模型
        'api_key': api_key,
        'max_tokens': 500,          # 较大的token限制
        'temperature': 0.7          # 标准随机性
    }

    standard_provider = ZhipuProvider(standard_config)
    await standard_provider.initialize()

    complex_request = AIRequest(
        messages=[
            {"role": "system", "content": "你是一位AI教育专家"},
            {"role": "user", "content": "请详细分析AI在教育领域的应用前景，包括机遇和挑战"}
        ],
        max_tokens=500
    )

    complex_response = await standard_provider.chat_completion(complex_request)
    print(f"标准模型响应: {complex_response.content[:100]}...")

    # 示例3：使用不同模型进行角色对话
    print("\n3. 不同模型的角色对话对比")

    # 用户角色 - 使用快速模型
    user_config = {
        'model': 'glm-4-flash',
        'api_key': api_key,
        'max_tokens': 200
    }

    user_provider = ZhipuProvider(user_config)
    await user_provider.initialize()

    user_request = AIRequest(
        messages=[
            {"role": "system", "content": "你是一个正在学习编程的大学生"},
            {"role": "user", "content": "你觉得学习编程最难的地方是什么？"}
        ],
        max_tokens=200
    )

    user_response = await user_provider.chat_completion(user_request)
    print(f"用户角色 (glm-4-flash): {user_response.content}")

    # 专家角色 - 使用标准模型
    expert_config = {
        'model': 'glm-4',
        'api_key': api_key,
        'max_tokens': 300
    }

    expert_provider = ZhipuProvider(expert_config)
    await expert_provider.initialize()

    expert_request = AIRequest(
        messages=[
            {"role": "system", "content": "你是一位资深编程教育专家"},
            {"role": "user", "content": "针对初学者学习编程的困难，你有什么建议？"}
        ],
        max_tokens=300
    )

    expert_response = await expert_provider.chat_completion(expert_request)
    print(f"专家角色 (glm-4): {expert_response.content}")

    print("\n=== 模型选择总结 ===")
    print("• glm-4-flash: 适合简单对话、快速响应")
    print("• glm-4: 适合复杂分析、深度思考")
    print("• 可以根据任务复杂度和成本要求选择不同模型")

if __name__ == "__main__":
    if sys.platform == "win32":
        os.system("chcp 65001 > nul")

    os.environ['PYTHONIOENCODING'] = 'utf-8'

    asyncio.run(custom_model_example())