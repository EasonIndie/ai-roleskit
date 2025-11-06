#!/usr/bin/env python3
"""
快速创建并使用角色的示例
"""

import asyncio
import sys
sys.path.insert(0, './src')

from ai_toolkit.core.character import CharacterManager
from ai_toolkit.core.dialogue import DialogueManager
from ai_toolkit.storage.file_storage import FileStorage
from ai_toolkit.models.schemas import Character, CharacterInfo, CharacterType, Message, DialogueRole
from demo import MockAIProvider


async def create_and_use_character():
    """创建角色并立即使用"""
    print("创建并使用角色演示")
    print("=" * 30)

    # 1. 创建AI Provider (模拟模式)
    ai_provider = MockAIProvider({'api_key': 'mock'})
    await ai_provider.initialize()

    # 2. 初始化管理器
    storage = FileStorage()
    character_manager = CharacterManager(ai_provider)
    dialogue_manager = DialogueManager(ai_provider, storage)

    # 3. 创建角色
    character_info = CharacterInfo(
        name="李博士",
        position="可持续发展专家",
        experience="15年环保和新能源领域经验",
        background="清华大学环境工程博士"
    )

    character = Character(
        name="李博士",
        type=CharacterType.EXPERT,
        description="专注于可持续发展和绿色能源解决方案的专家",
        info=character_info
    )

    print(f"✓ 创建角色: {character.name}")
    print(f"  职位: {character.info.position}")
    print(f"  专长: {character.description}")

    # 4. 保存角色
    await storage.save_character(character)
    print(f"✓ 角色已保存，ID: {character.id}")

    # 5. 创建对话会话
    dialogue = await dialogue_manager.create_dialogue(
        title=f"与{character.name}的对话",
        participants=[character]
    )

    print(f"\n开始与 {character.name} 对话:")

    # 6. 模拟对话
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

    # 7. 显示对话总结
    print(f"\n=== 对话总结 ===")
    messages = await dialogue_manager.get_dialogue_messages(dialogue.id)
    print(f"总共进行了 {len([m for m in messages if m.role == DialogueRole.USER])} 轮对话")

    print(f"\n✓ 对话已保存，可以随时继续与 {character.name} 交流")
    print(f"✓ 角色 ID: {character.id} - 可用于后续调用")


async def use_existing_character(character_id: str):
    """使用已存在的角色进行快速对话"""
    print(f"使用角色 ID: {character_id}")

    try:
        # 初始化组件
        ai_provider = MockAIProvider({'api_key': 'mock'})
        await ai_provider.initialize()

        storage = FileStorage()
        dialogue_manager = DialogueManager(ai_provider, storage)

        # 加载角色
        character = await storage.load_character(character_id)
        print(f"✓ 加载角色: {character.name}")

        # 创建对话
        dialogue = await dialogue_manager.create_dialogue(
            title=f"与{character.name}的对话",
            participants=[character]
        )

        # 交互式对话
        print(f"\n开始与 {character.name} 对话 (输入 'quit' 退出):")

        while True:
            user_input = input("\n您: ").strip()

            if user_input.lower() == 'quit':
                break

            if not user_input:
                continue

            # 添加用户消息
            await dialogue_manager.add_message(
                dialogue_id=dialogue.id,
                role=DialogueRole.USER,
                content=user_input
            )

            # 获取角色回复
            response = await dialogue_manager.get_character_response(
                dialogue_id=dialogue.id,
                character_id=character.id,
                context=user_input
            )

            print(f"{character.name}: {response}")

        print("对话结束。")

    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    print("AI Character Toolkit - 角色使用示例")
    print("1. 创建并使用新角色")
    print("2. 使用现有角色")

    choice = input("请选择 (1 或 2): ").strip()

    if choice == "1":
        asyncio.run(create_and_use_character())
    elif choice == "2":
        character_id = input("请输入角色 ID: ").strip()
        if character_id:
            asyncio.run(use_existing_character(character_id))
        else:
            print("请提供有效的角色 ID")
    else:
        print("无效选择")