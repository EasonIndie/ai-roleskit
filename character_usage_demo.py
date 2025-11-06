#!/usr/bin/env python3
"""
角色使用演示 - 自动化版本
"""

import asyncio
import sys
sys.path.insert(0, './src')

from ai_toolkit.core.character import CharacterManager
from ai_toolkit.core.dialogue import DialogueManager
from ai_toolkit.storage.file_storage import FileStorage
from ai_toolkit.models.schemas import Character, CharacterInfo, CharacterType, Message, DialogueRole
from demo import MockAIProvider


async def create_character_demo():
    """创建角色演示"""
    print("=== 创建角色演示 ===")

    # 创建AI Provider
    ai_provider = MockAIProvider({'api_key': 'mock'})
    await ai_provider.initialize()

    # 初始化管理器
    storage = FileStorage()
    character_manager = CharacterManager(ai_provider)

    # 创建角色信息
    character_info = CharacterInfo(
        name="李博士",
        position="可持续发展专家",
        experience="15年环保和新能源领域经验"
    )

    # 创建角色
    character = Character(
        name="李博士",
        type=CharacterType.EXPERT,
        description="专注于可持续发展和绿色能源解决方案的专家",
        info=character_info
    )

    # 保存角色
    await storage.save_character(character)

    print(f"PASS: 创建角色: {character.name}")
    print(f"  ID: {character.id}")
    print(f"  类型: {character.type.value}")
    print(f"  职位: {character.info.position}")
    print(f"  描述: {character.description}")

    return character


async def dialogue_demo(character):
    """对话演示"""
    print(f"\n=== 与 {character.name} 对话演示 ===")

    # 创建AI Provider和对话管理器
    ai_provider = MockAIProvider({'api_key': 'mock'})
    await ai_provider.initialize()

    storage = FileStorage()
    character_manager = CharacterManager(ai_provider)
    dialogue_manager = DialogueManager(ai_provider, character_manager)

    # 创建对话会话
    dialogue = await dialogue_manager.create_dialogue(
        character_id=character.id,
        title=f"与{character.name}的对话"
    )

    print(f"PASS: 创建对话会话: {dialogue.title}")

    # 预定义的问题
    questions = [
        "您认为未来10年可再生能源的发展前景如何？",
        "企业应该如何制定可持续发展战略？",
        "个人在日常生活中可以为环保做些什么？"
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n{i}. 用户: {question}")

        # 添加用户消息
        await dialogue_manager.add_message(
            dialogue_id=dialogue.id,
            role=DialogueRole.USER,
            content=question
        )

        # 获取角色回复
        response = await dialogue_manager.get_character_response(
            dialogue_id=dialogue.id,
            character_id=character.id,
            context=question
        )

        print(f"   {character.name}: {response}")

    # 显示对话历史
    print(f"\n=== 对话历史 ===")
    messages = await dialogue_manager.get_dialogue_messages(dialogue.id)

    for i, msg in enumerate(messages, 1):
        role_name = "用户" if msg.role == DialogueRole.USER else character.name
        print(f"{i}. {role_name}: {msg.content}")

    return dialogue


async def load_character_demo(character_id):
    """加载角色演示"""
    print(f"\n=== 加载角色演示 ===")

    storage = FileStorage()

    try:
        # 加载角色
        character = await storage.load_character(character_id)
        print(f"PASS: 成功加载角色: {character.name}")
        print(f"  ID: {character.id}")
        print(f"  类型: {character.type.value}")
        print(f"  描述: {character.description}")

        return character

    except Exception as e:
        print(f"FAIL: 加载角色失败: {e}")
        return None


async def main():
    """主演示函数"""
    print("AI Character Toolkit - 角色使用完整演示")
    print("=" * 50)

    # 1. 创建角色
    character = await create_character_demo()

    # 2. 进行对话
    dialogue = await dialogue_demo(character)

    # 3. 重新加载角色
    print(f"\n=== 重新加载角色演示 ===")
    loaded_character = await load_character_demo(character.id)

    if loaded_character:
        print(f"PASS: 角色重载成功，可以继续使用 {loaded_character.name}")

    print(f"\n=== 使用总结 ===")
    print(f"1. 角色创建: 成功创建角色 {character.name}")
    print(f"2. 对话功能: 进行了 3 轮对话")
    print(f"3. 数据持久化: 角色和对话都已保存")
    print(f"4. 角色重载: 可以随时重新加载使用")

    print(f"\n=== 后续使用方法 ===")
    print(f"角色ID: {character.id}")
    print(f"你可以通过以下方式继续使用:")
    print(f"1. CLI: python cli.py dialogue start {character.id}")
    print(f"2. 代码: await storage.load_character('{character.id}')")
    print(f"3. 自定义: 在其他项目中导入并使用该角色")


if __name__ == "__main__":
    asyncio.run(main())