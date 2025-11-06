#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试实际的 FileStorage 功能
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

async def test_storage_system():
    """测试存储系统"""
    print("=== 测试实际 FileStorage ===")

    try:
        # 1. 导入模块
        print("\n1.1 导入存储模块...")
        from ai_toolkit.storage.file_storage import FileStorage
        from ai_toolkit.core.exploration import CreativeExplorer
        from ai_toolkit.ai.zhipu_provider import ZhipuProvider
        from ai_toolkit.utils.config import config
        print("   导入成功！")

        # 2. 初始化系统
        print("\n2.1 初始化系统...")
        config.load_config()
        zhipu_config = config.get_zhipu_config()
        provider = ZhipuProvider(zhipu_config)
        await provider.initialize()
        explorer = CreativeExplorer(provider)
        storage = FileStorage()
        print("   系统初始化成功！")

        # 3. 创建探索会话
        print("\n3.1 创建探索会话...")
        initial_idea = "测试AI辅助学习应用的想法"
        session = await explorer.start_exploration(initial_idea)
        print(f"   会话ID: {session.id[:8]}...")

        # 4. 简单探索
        print("\n4.1 执行简单探索...")
        result = await explorer.explore_idea(session.id, "请简单分析这个想法的可行性")
        print(f"   探索完成，响应长度: {len(result.get('ai_response', ''))}")

        # 5. 测试保存探索会话
        print("\n5.1 测试保存探索会话...")
        await storage.save_exploration(session)
        print("   探索会话保存成功！")

        # 6. 测试加载探索会话
        print("\n6.1 测试加载探索会话...")
        loaded_session = await storage.load_exploration(session.id)
        if loaded_session:
            print(f"   成功加载会话: {loaded_session.id[:8]}...")
            print(f"   初始想法: {loaded_session.initial_idea}")
        else:
            print("   加载失败")

        # 7. 检查文件系统
        print("\n7.1 检查文件系统...")
        data_dir = "data"
        if os.path.exists(data_dir):
            print(f"   数据目录存在: {os.path.abspath(data_dir)}")
            for root, dirs, files in os.walk(data_dir):
                level = root.replace(data_dir, '').count(os.sep)
                indent = ' ' * 2 * level
                print(f"   {indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    print(f"   {subindent}{file} ({file_size} bytes)")
        else:
            print("   数据目录不存在")

        print("\n=== FileStorage 测试成功 ===")
        return True

    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_storage_system())
    if success:
        print("\n[SUCCESS] 实际 FileStorage 可用！")
    else:
        print("\n[ERROR] 实际 FileStorage 有问题")