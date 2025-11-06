#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试实际的 CreativeExplorer 功能
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

async def test_creative_explorer():
    """测试 CreativeExplorer"""
    print("=== 测试实际 CreativeExplorer ===")

    try:
        # 1. 导入模块
        print("\n1.1 导入 CreativeExplorer...")
        from ai_toolkit.core.exploration import CreativeExplorer
        from ai_toolkit.ai.zhipu_provider import ZhipuProvider
        from ai_toolkit.utils.config import config
        print("   导入成功！")

        # 2. 加载配置
        print("\n2.1 加载配置...")
        config.load_config()
        zhipu_config = config.get_zhipu_config()
        print(f"   配置加载成功")

        # 3. 初始化 Provider 和 Explorer
        print("\n3.1 初始化 Provider 和 Explorer...")
        provider = ZhipuProvider(zhipu_config)
        await provider.initialize()
        explorer = CreativeExplorer(provider)
        print("   Explorer 初始化成功！")

        # 4. 开始探索
        print("\n4.1 开始创意探索...")
        initial_idea = "开发一个AI辅助学习编程的移动应用"
        session = await explorer.start_exploration(initial_idea)
        print(f"   探索会话已创建: {session.id[:8]}...")
        print(f"   初始想法: {initial_idea}")

        # 5. 执行探索
        print("\n5.1 执行深度探索...")
        exploration_prompt = """
        请帮我从多个角度深入分析这个想法：
        1. 市场潜力和用户需求
        2. 技术实现的主要挑战
        3. 与现有解决方案的差异化
        4. 潜在的商业模式
        """

        result = await explorer.explore_idea(session.id, exploration_prompt)
        print("\n   === AI深度分析结果 ===")
        print(result.get('ai_response', 'No response'))
        print(f"\n   分析统计:")
        print(f"   - 会话ID: {result.get('session_id', 'N/A')[:8]}...")
        print(f"   - 响应长度: {len(result.get('ai_response', ''))}")

        # 6. 识别利益相关者
        print("\n6.1 识别利益相关者...")
        stakeholders = await explorer.identify_stakeholders(session.id)
        print("   识别到的利益相关者:")
        for i, stakeholder in enumerate(stakeholders, 1):
            print(f"   {i}. {stakeholder.get('description', 'Unknown')}")

        # 7. 获取探索摘要
        print("\n7.1 获取探索摘要...")
        summary = await explorer.get_exploration_summary(session.id)
        print("   探索摘要:")
        print(f"   - 会话ID: {summary.get('session_id', 'N/A')[:8]}...")
        print(f"   - 探索时长: {summary.get('exploration_duration', 'N/A')}")
        print(f"   - 角色生成准备度: {summary.get('character_generation_readiness', 'N/A')}")

        print("\n=== CreativeExplorer 测试成功 ===")
        return session, result, summary

    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None

if __name__ == "__main__":
    session, result, summary = asyncio.run(test_creative_explorer())
    if session and result and summary:
        print("\n[SUCCESS] 实际 CreativeExplorer 可用！")
    else:
        print("\n[ERROR] 实际 CreativeExplorer 有问题")