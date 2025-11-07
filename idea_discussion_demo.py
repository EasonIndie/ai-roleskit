#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
想法深度探讨演示
输入一个想法，生成三个角色，进行深度讨论，收集有用内容
完全基于src代码库功能，只需修改idea变量即可使用
"""

import asyncio
import sys
import os
from datetime import datetime

# 设置编码
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 添加 src 目录到路径
sys.path.insert(0, './src')

# 设置环境变量
os.environ['ZHIPU_API_KEY'] = "31b5715b41cd4e6e8dde08232ec63146.Jjs6gp46gAYsI5sl"

def print_header(title):
    """打印标题"""
    print("=" * 80)
    print(f" {title}")
    print("=" * 80)

def print_section(title):
    """打印章节"""
    print(f"\n{title}")
    print("-" * 50)

async def main():
    """主函数 - 使用完整的src代码库工作流"""
    print_header("想法深度探讨演示")
    print("输入想法 → AI探索 → 生成角色 → 深度讨论 → 保存结果")
    print(f"演示时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 1. 输入想法 - 只需修改这里即可
    idea = "我想开发一个自动生成软件著作权的工具，解决中小公司或者个人开发者申请软著的麻烦"

    try:
        # 2. 初始化src代码库组件
        print_section("1. 初始化AI工具包")
        from ai_toolkit.utils.config import config
        from ai_toolkit.ai.zhipu_provider import ZhipuProvider
        from ai_toolkit.core.exploration import CreativeExplorer
        from ai_toolkit.core.character import CharacterManager
        from ai_toolkit.core.dialogue import DialogueManager
        from ai_toolkit.storage.file_storage import FileStorage

        config.load_config()
        provider = ZhipuProvider(config.get_zhipu_config())
        await provider.initialize()

        # 初始化各个管理器
        explorer = CreativeExplorer(provider)
        character_manager = CharacterManager(provider)
        dialogue_manager = DialogueManager(provider, character_manager)
        storage = FileStorage()

        print("   [OK] AI工具包初始化完成")

        # 3. AI探索想法
        print_section("2. AI深度探索想法")
        print(f"想法: {idea}")

        # 启动探索会话
        exploration_session = await explorer.start_exploration(idea)
        print(f"   [OK] 探索会话已启动: {exploration_session.id}")

        # 进行探索
        exploration_result = await explorer.explore_idea(exploration_session.id, "请深入探索这个想法的各个方面，包括机会、挑战、利益相关者、知识需求等。")
        print(f"   [OK] 探索完成，发现 {len(exploration_result.get('key_insights', []))} 个关键洞察")

        # 4. 生成三个角色
        print_section("3. 基于探索结果生成角色")
        characters = await character_manager.generator.generate_character_set(
            exploration_result
        )

        print(f"   [OK] 生成了 {len(characters)} 个角色:")
        for char in characters:
            print(f"   - {char.name} ({char.type.value}): {char.info.position}")
            # 添加到管理器以便后续对话使用
            await character_manager.add_character(char)

        # 5. 进行多角色对话
        print_section("4. 多角色深度对话")

        # 基于探索结果生成讨论问题
        discussion_questions = [
            "对于这个想法，你认为最大的机遇和挑战是什么？",
            "从你的角度，如何确保这个产品的成功？",
            "这个想法需要哪些关键资源和技术支持？"
        ]

        dialogues = []
        for i, question in enumerate(discussion_questions, 1):
            print(f"\n   问题 {i}: {question}")

            for char in characters:
                # 创建对话
                dialogue = await dialogue_manager.create_dialogue(
                    char.id,
                    f"关于想法的讨论 - {char.name}"
                )

                # 发送问题并获取回复
                response = await dialogue_manager.send_message(dialogue.id, question)
                print(f"   {char.name}: {response.content[:100]}...")

                dialogues.append({
                    'character': char.name,
                    'type': char.type.value,
                    'question': question,
                    'answer': response.content,
                    'dialogue_id': dialogue.id
                })

        print(f"\n   [OK] 完成了 {len(discussion_questions)} × {len(characters)} = {len(dialogues)} 次对话")

        # 6. 保存所有数据
        print_section("5. 保存讨论结果")

        # 保存探索结果
        exploration_id = storage.save_exploration(exploration_result)
        print(f"   [OK] 探索结果已保存: {exploration_id}")

        # 保存角色
        character_ids = []
        for char in characters:
            char_id = storage.save_character(char)
            character_ids.append(char_id)
            print(f"   [OK] 角色已保存: {char.name}")

        # 保存对话
        dialogue_ids = []
        for dialogue_data in dialogues:
            dialogue_id = storage.save_dialogue(
                dialogue_data['dialogue_id'],
                await dialogue_manager.get_dialogue(dialogue_data['dialogue_id'])
            )
            dialogue_ids.append(dialogue_id)

        print(f"   [OK] 对话已保存: {len(dialogue_ids)} 个")

        # 7. 总结
        print_header("演示完成总结")
        print(f"想法: {idea}")
        print(f"探索洞察: {len(exploration_result.key_insights)} 个")
        print(f"生成角色: {len(characters)} 个")
        print(f"对话数量: {len(dialogues)} 次")
        print(f"数据保存: data/ 目录")

        print(f"\n[SUCCESS] 想法深度探讨完成！")
        print(f"   - AI智能探索了想法的多个维度")
        print(f"   - 生成了三个不同视角的专业角色")
        print(f"   - 进行了深度的多角色对话")
        print(f"   - 所有数据已保存，可进一步分析")
        print(f"   - 只需修改idea变量即可探索其他想法")

    except Exception as e:
        print(f"\n[ERROR] 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("启动想法深度探讨演示...")
    asyncio.run(main())