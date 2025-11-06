#!/usr/bin/env python3
"""
AI Character Toolkit Example Usage
基本使用示例演示
"""

import asyncio
import os
import sys

# Add src to path
sys.path.insert(0, './src')

from ai_toolkit.utils.config import config
from ai_toolkit.utils.logger import get_logger
from ai_toolkit.ai.openai_provider import OpenAIProvider
from ai_toolkit.core.character import CharacterManager
from ai_toolkit.core.exploration import CreativeExplorer
from ai_toolkit.core.dialogue import DialogueManager
from ai_toolkit.core.concurrent import ConcurrentValidator
from ai_toolkit.storage.file_storage import FileStorage
from ai_toolkit.models.schemas import CharacterType


async def basic_example():
    """基本功能示例"""
    print("🚀 AI Character Toolkit - 基本功能演示")
    print("=" * 50)

    # 初始化日志
    logger = get_logger("example")
    logger.info("开始基本功能演示")

    try:
        # 1. 设置AI提供商（使用模拟模式）
        print("\n1. 初始化AI提供商...")
        ai_config = {
            'model': 'gpt-3.5-turbo',
            'api_key': os.getenv('OPENAI_API_KEY', 'demo-key'),
            'max_tokens': 1000,
            'temperature': 0.7
        }

        # 如果没有API密钥，使用模拟模式
        if ai_config['api_key'] == 'demo-key':
            print("   ⚠️  未检测到API密钥，使用演示模式")
            from ai_toolkit.ai.base import BaseAIProvider, AIRequest, AIResponse

            class MockAIProvider(BaseAIProvider):
                def __init__(self, config):
                    self.config = config
                    self.provider_name = "mock"

                @property
                def default_model(self):
                    return "mock-model"

                async def initialize(self):
                    pass

                async def chat_completion(self, request):
                    # 模拟AI响应
                    mock_responses = {
                        'exploration': "这是一个很有趣的想法，值得深入探索。我们可以从用户需求、技术可行性、商业价值等多个角度来分析。",
                        'character_user': "作为一名普通用户，我希望这个应用简单易用，能够真正解决我的学习问题。",
                        'character_expert': "从技术角度来看，这个方案是可行的，但需要考虑数据隐私和算法准确性问题。",
                        'character_org': "从商业角度，这个项目有潜力，但需要明确盈利模式和用户获取策略。"
                    }

                    content = "这是一个模拟的AI响应，用于演示系统功能。"
                    return AIResponse(content=content, role="assistant")

                async def chat_completion_stream(self, request):
                    yield "模拟流式响应"

            ai_provider = MockAIProvider(ai_config)
        else:
            ai_provider = OpenAIProvider(ai_config)
            await ai_provider.initialize()

        print(f"   ✅ AI提供商已初始化: {ai_provider.provider_name}")

        # 2. 初始化管理器
        print("\n2. 初始化系统组件...")
        storage = FileStorage()
        character_manager = CharacterManager(ai_provider)
        explorer = CreativeExplorer(ai_provider)
        dialogue_manager = DialogueManager(ai_provider, character_manager)
        validator = ConcurrentValidator(ai_provider, character_manager)
        print("   ✅ 所有组件初始化完成")

        # 3. 创意探索示例
        print("\n3. 创意探索示例...")
        initial_idea = "开发一个AI辅助学习编程的移动应用"
        exploration_session = await explorer.start_exploration(initial_idea)
        print(f"   🔍 探索会话已创建: {exploration_session.id}")
        print(f"   💡 初始想法: {initial_idea}")

        # 模拟探索对话
        exploration_result = await explorer.explore_idea(
            exploration_session.id,
            "请帮我分析这个想法的市场潜力和技术挑战"
        )
        print("   📊 探索分析完成")

        # 获取探索摘要
        summary = await explorer.get_exploration_summary(exploration_session.id)
        print(f"   📈 探索准备度: {summary['character_generation_readiness']}")

        # 4. 角色生成示例
        print("\n4. 角色生成示例...")
        user_character = await character_manager.create_character(
            summary, CharacterType.USER, "张三"
        )
        print(f"   👤 用户角色已生成: {user_character.name} ({user_character.id})")

        expert_character = await character_manager.create_character(
            summary, CharacterType.EXPERT, "李老师"
        )
        print(f"   👨‍💼 专家角色已生成: {expert_character.name} ({expert_character.id})")

        org_character = await character_manager.create_character(
            summary, CharacterType.ORGANIZATION, "教育科技公司"
        )
        print(f"   🏢 组织角色已生成: {org_character.name} ({org_character.id})")

        # 5. 对话管理示例
        print("\n5. 对话管理示例...")
        dialogue = await dialogue_manager.create_dialogue(
            user_character.id,
            "产品功能讨论"
        )
        print(f"   💬 对话已创建: {dialogue.id}")

        response = await dialogue_manager.send_message(
            dialogue.id,
            "你认为这个学习应用最重要的功能是什么？"
        )
        print(f"   🤖 角色响应: {response.content[:50]}...")

        # 6. 并发验证示例
        print("\n6. 并发验证示例...")
        question = "如何平衡学习效果和用户体验？"
        validation_session = await validator.create_validation_session(
            question,
            [user_character.id, expert_character.id, org_character.id]
        )
        print(f"   🔍 验证会话已创建: {validation_session.id}")

        # 运行并发验证
        validation_result = await validator.run_concurrent_validation(
            validation_session.id,
            [user_character.id, expert_character.id, org_character.id]
        )
        print("   📊 多角色验证完成")

        # 7. 存储示例
        print("\n7. 数据存储示例...")

        # 保存角色
        await storage.save_character(user_character)
        await storage.save_character(expert_character)
        await storage.save_character(org_character)

        # 保存探索会话
        await storage.save_exploration(exploration_session)

        # 保存对话
        await storage.save_dialogue(dialogue)

        # 保存验证会话
        await storage.save_validation(validation_session)

        print("   💾 所有数据已保存到文件")

        # 8. 存储统计
        stats = await storage.get_storage_stats()
        print(f"\n📊 存储统计:")
        print(f"   - 总角色数: {stats.get('total_characters', 0)}")
        print(f"   - 存储格式: {stats.get('storage_format', 'unknown')}")
        print(f"   - 存储路径: {stats.get('storage_path', 'unknown')}")
        print(f"   - 总大小: {stats.get('total_size_mb', 0)} MB")

        print("\n🎉 演示完成！所有核心功能运行正常。")

    except Exception as e:
        logger.error(f"演示过程中出现错误: {e}")
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


async def demo_workflow():
    """完整工作流程演示"""
    print("\n" + "=" * 60)
    print("🔄 AI Character Toolkit - 完整工作流程演示")
    print("=" * 60)

    # 这里可以添加更复杂的工作流程演示
    # 比如完整的探索->角色生成->对话->验证->分析流程

    print("📝 演示完整工作流程:")
    print("   1. 创意探索 → 深化想法")
    print("   2. 角色生成 → 创建多角色")
    print("   3. 角色对话 → 收集观点")
    print("   4. 并发验证 → 对比分析")
    print("   5. 整合分析 → 生成报告")
    print("   6. 决策建议 → 行动计划")

    print("\n✨ 这个工具包可以帮助您:")
    print("   • 从初始想法进行创意探索")
    print("   • 生成多维度的AI角色")
    print("   • 通过角色化对话收集观点")
    print("   • 并发验证不同角色视角")
    print("   • 整合分析生成决策报告")
    print("   • 制定实施路线图")


if __name__ == "__main__":
    print("🌟 AI Character Toolkit - Python实现")
    print("基于《动态AI角色生成工具包.md》的完整Python实现")
    print()

    # 运行基本示例
    asyncio.run(basic_example())

    # 运行工作流程演示
    asyncio.run(demo_workflow())

    print("\n" + "=" * 60)
    print("🚀 使用命令行界面:")
    print("   python cli.py --help")
    print("   python cli.py explore start '你的想法' --interactive")
    print("   python cli.py character list")
    print("   python cli.py dialogue start <角色ID>")
    print("   python cli.py validate concurrent '问题' --characters <角色ID列表>")
    print("   python cli.py analysis report <验证ID>")
    print("=" * 60)