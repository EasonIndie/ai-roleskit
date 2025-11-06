#!/usr/bin/env python3
"""
如何使用已创建角色的示例代码
"""

import asyncio
import sys
sys.path.insert(0, './src')

from ai_toolkit.storage.file_storage import FileStorage
from ai_toolkit.core.dialogue import DialogueManager
from ai_toolkit.ai.openai_provider import OpenAIProvider
from ai_toolkit.models.schemas import Character, CharacterInfo, CharacterType, Message, DialogueRole


async def load_and_use_character(character_id: str):
    """加载并使用已创建的角色"""
    print(f"Loading character with ID: {character_id}")

    # 1. 初始化存储和管理器
    storage = FileStorage()

    # 2. 从存储中加载角色
    try:
        character = await storage.load_character(character_id)
        print(f"✓ Loaded character: {character.name}")
        print(f"  Type: {character.type.value}")
        print(f"  Description: {character.description}")

        # 显示角色详细信息
        if hasattr(character, 'info') and character.info:
            print(f"  Position: {character.info.position}")
            print(f"  Experience: {character.info.experience}")

    except Exception as e:
        print(f"✗ Failed to load character: {e}")
        return

    # 3. 初始化对话管理器（需要AI provider）
    # 这里使用模拟模式，实际使用时请配置真实的API密钥
    try:
        # 实际使用时，请先配置API密钥
        ai_provider = OpenAIProvider({
            'api_key': 'your_api_key_here',  # 替换为真实API密钥
            'model': 'gpt-3.5-turbo'
        })
        await ai_provider.initialize()
    except:
        print("⚠️ No valid API key configured. Using mock mode for demonstration.")
        # 使用模拟模式的AI provider
        from demo import MockAIProvider
        ai_provider = MockAIProvider({'api_key': 'mock'})

    dialogue_manager = DialogueManager(ai_provider, storage)

    # 4. 创建对话会话
    print(f"\nStarting dialogue with {character.name}...")
    dialogue = await dialogue_manager.create_dialogue(
        title=f"Dialogue with {character.name}",
        participants=[character]
    )

    print(f"✓ Created dialogue session: {dialogue.title}")

    # 5. 发送消息给角色
    user_message = "我想了解您在AI领域的见解，特别是关于机器学习的未来发展。"
    print(f"\nUser: {user_message}")

    # 添加用户消息
    await dialogue_manager.add_message(
        dialogue_id=dialogue.id,
        role=DialogueRole.USER,
        content=user_message
    )

    # 获取角色回复
    response = await dialogue_manager.get_character_response(
        dialogue_id=dialogue.id,
        character_id=character.id,
        context=user_message
    )

    print(f"{character.name}: {response}")

    # 6. 继续对话
    follow_up = "您认为AI在哪些行业有最大的应用潜力？"
    print(f"\nUser: {follow_up}")

    await dialogue_manager.add_message(
        dialogue_id=dialogue.id,
        role=DialogueRole.USER,
        content=follow_up
    )

    response2 = await dialogue_manager.get_character_response(
        dialogue_id=dialogue.id,
        character_id=character.id,
        context=follow_up
    )

    print(f"{character.name}: {response2}")

    # 7. 显示对话历史
    print(f"\n--- Dialogue History ---")
    messages = await dialogue_manager.get_dialogue_messages(dialogue.id)
    for i, msg in enumerate(messages, 1):
        role_prefix = "User" if msg.role == DialogueRole.USER else character.name
        print(f"{i}. {role_prefix}: {msg.content}")

    print(f"\n✓ Dialogue completed successfully!")


async def list_all_characters():
    """列出所有可用的角色"""
    print("=== Available Characters ===")

    storage = FileStorage()

    try:
        # 获取所有角色
        characters = await storage.list_characters()

        if not characters:
            print("No characters found. Please create some characters first.")
            return

        print(f"Found {len(characters)} characters:\n")

        for character in characters:
            print(f"ID: {character.id}")
            print(f"Name: {character.name}")
            print(f"Type: {character.type.value}")
            print(f"Description: {character.description}")
            if hasattr(character, 'info') and character.info:
                print(f"Position: {character.info.position}")
            print("-" * 40)

        return characters

    except Exception as e:
        print(f"Error listing characters: {e}")
        return []


async def main():
    """主函数"""
    print("AI Character Toolkit - Using Created Characters")
    print("=" * 50)

    # 1. 显示所有可用角色
    characters = await list_all_characters()

    if not characters:
        print("\nTo create characters, you can use:")
        print("1. CLI: python cli.py character create <type> --name <name>")
        print("2. Demo: python demo.py (creates a sample character)")
        return

    # 2. 选择要使用的角色
    print("\nSelect a character to interact with:")
    for i, char in enumerate(characters, 1):
        print(f"{i}. {char.name} ({char.type.value})")

    try:
        choice = int(input("\nEnter character number (or 0 to exit): ")) - 1

        if choice < 0 or choice >= len(characters):
            print("Invalid selection.")
            return

        selected_character = characters[choice]
        print(f"\nUsing character: {selected_character.name}")

        # 3. 使用选定的角色
        await load_and_use_character(selected_character.id)

    except (ValueError, KeyboardInterrupt):
        print("\nExiting...")


if __name__ == "__main__":
    asyncio.run(main())