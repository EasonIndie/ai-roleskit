#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
步骤1：使用实际代码库的创意探索演示
基于真实的 AI Character Toolkit 实现
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# 设置编码
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 添加 src 目录到路径
sys.path.insert(0, './src')

# 设置环境变量
os.environ['ZHIPU_API_KEY'] = "31b5715b41cd4e6e8dde08232ec63146.Jjs6gp46gAYsI5sl"
os.environ['ZAI_API_KEY'] = "31b5715b41cd4e6e8dde08232ec63146.Jjs6gp46gAYsI5sl"

async def step1_real_exploration():
    """使用实际代码库进行创意探索"""
    print("=== 步骤1：使用实际代码库的创意探索功能 ===")
    print("我们将使用真实的 AI Character Toolkit 探索想法：'开发一个AI辅助学习编程的移动应用'")

    try:
        # 1. 初始化实际系统组件
        print("\n1.1 初始化 AI Character Toolkit 系统...")

        # 导入实际的模块
        from ai_toolkit.utils.config import config
        from ai_toolkit.ai.zhipu_provider import ZhipuProvider
        from ai_toolkit.core.exploration import CreativeExplorer
        from ai_toolkit.storage.file_storage import FileStorage

        print("   所有模块导入成功！")

        # 加载配置
        config.load_config()
        zhipu_config = config.get_zhipu_config()
        print(f"   配置加载成功，模型: {zhipu_config['model']}")

        # 初始化组件
        provider = ZhipuProvider(zhipu_config)
        await provider.initialize()
        explorer = CreativeExplorer(provider)
        storage = FileStorage()
        print("   系统组件初始化成功！")

        # 2. 创建真实的探索会话
        print("\n2.1 创建创意探索会话...")
        initial_idea = "开发一个AI辅助学习编程的移动应用"
        session = await explorer.start_exploration(initial_idea)
        print(f"   探索会话已创建: {session.id[:8]}...")
        print(f"   初始想法: {initial_idea}")
        print(f"   会话类型: {type(session).__name__}")

        # 3. 使用真实的探索功能
        print("\n3.1 AI引导深度探索...")
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
        print(f"   - 响应长度: {len(result.get('ai_response', ''))} 字符")
        if 'usage' in result:
            print(f"   - Token使用: {result['usage']}")

        # 4. 使用真实的利益相关者识别
        print("\n4.1 识别利益相关者...")
        stakeholders = await explorer.identify_stakeholders(session.id)
        print("   识别到的利益相关者:")
        for i, stakeholder in enumerate(stakeholders, 1):
            print(f"   {i}. {stakeholder.get('description', 'Unknown')} (类型: {stakeholder.get('type', 'Unknown')})")

        # 5. 使用真实的探索摘要功能
        print("\n5.1 生成探索摘要...")
        summary = await explorer.get_exploration_summary(session.id)
        print("   探索摘要:")
        print(f"   - 会话ID: {summary.get('session_id', 'N/A')[:8]}...")
        print(f"   - 探索时长: {summary.get('exploration_duration', 'N/A')}")
        print(f"   - 角色生成准备度: {summary.get('character_generation_readiness', 'N/A')}")
        print(f"   - 关键洞察: {len(summary.get('key_insights', []))} 项")

        # 6. 使用真实的存储系统
        print("\n6.1 保存探索数据到文件系统...")
        save_success = await storage.save_exploration(session)
        if save_success:
            print("   探索会话保存成功！")
        else:
            print("   探索会话保存失败！")

        # 7. 验证保存的数据
        print("\n7.1 验证保存的数据...")
        loaded_session = await storage.load_exploration(session.id)
        if loaded_session:
            print(f"   数据验证成功：重新加载会话 {loaded_session.id[:8]}...")
            print(f"   初始想法匹配: {loaded_session.initial_idea == initial_idea}")
        else:
            print("   数据验证失败：无法重新加载会话")

        # 8. 显示文件系统状态
        print("\n8.1 显示文件系统状态...")
        data_dir = "data"
        if os.path.exists(data_dir):
            print(f"   数据目录: {os.path.abspath(data_dir)}")
            explorations_dir = os.path.join(data_dir, "explorations")
            if os.path.exists(explorations_dir):
                files = [f for f in os.listdir(explorations_dir) if f.endswith('.json')]
                print(f"   探索文件数量: {len(files)}")
                if files:
                    latest_file = os.path.join(explorations_dir, files[-1])
                    file_size = os.path.getsize(latest_file)
                    print(f"   最新文件: {files[-1]} ({file_size} bytes)")

        # 9. 系统状态统计
        print("\n9.1 系统状态统计...")
        stats = await storage.get_storage_stats()
        print("   存储统计:")
        print(f"   - 总角色数: {stats.get('total_characters', 0)}")
        print(f"   - 存储格式: {stats.get('storage_format', 'Unknown')}")
        print(f"   - 存储路径: {stats.get('storage_path', 'Unknown')}")
        print(f"   - 总大小: {stats.get('total_size_mb', 0)} MB")

        print("\n=== 步骤1：实际代码库探索演示完成 ===")
        print("成功完成的探索任务:")
        print("   - 使用真实的 ZhipuProvider 进行AI对话")
        print("   - 使用真实的 CreativeExplorer 进行创意探索")
        print("   - 使用真实的 FileStorage 进行数据持久化")
        print("   - 完整的探索会话生命周期管理")
        print("   - 数据验证和系统状态统计")

        return {
            'session': session,
            'result': result,
            'summary': summary,
            'storage_stats': stats
        }

    except Exception as e:
        print(f"\n探索过程出错: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("AI Character Toolkit - 步骤1：使用实际代码库的创意探索")
    print("=" * 60)

    result_data = asyncio.run(step1_real_exploration())

    if result_data:
        print(f"\n[SUCCESS] 步骤1探索成功！")
        print(f"你现在可以进入下一步：角色生成")
        print(f"会话ID: {result_data['session'].id}")
        print(f"系统已验证可以正常工作，所有核心组件都已就绪")
    else:
        print(f"\n[ERROR] 步骤1探索失败，请检查错误信息")