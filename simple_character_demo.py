#!/usr/bin/env python3
"""
简单的角色创建和基本使用演示
"""

import asyncio
import sys
sys.path.insert(0, './src')

from ai_toolkit.models.schemas import Character, CharacterInfo, CharacterType
from ai_toolkit.storage.file_storage import FileStorage
from demo import MockAIProvider
from ai_toolkit.ai.base import AIRequest


async def simple_character_demo():
    """简单的角色演示"""
    print("AI Character Toolkit - 简单角色演示")
    print("=" * 40)

    # 1. 创建角色
    print("\n1. 创建角色...")
    character_info = CharacterInfo(
        name="张教授",
        position="人工智能研究员",
        experience="10年机器学习和深度学习研究经验"
    )

    character = Character(
        name="张教授",
        type=CharacterType.EXPERT,
        description="专门研究人工智能和机器学习的专家",
        info=character_info
    )

    print(f"   角色名称: {character.name}")
    print(f"   角色类型: {character.type.value}")
    print(f"   角色描述: {character.description}")
    print(f"   职位: {character.info.position}")

    # 2. 保存角色
    print("\n2. 保存角色...")
    storage = FileStorage()
    await storage.save_character(character)
    print(f"   角色已保存，ID: {character.id}")

    # 3. 加载角色
    print("\n3. 加载角色...")
    loaded_character = await storage.load_character(character.id)
    print(f"   成功加载角色: {loaded_character.name}")
    print(f"   ID: {loaded_character.id}")

    # 4. 使用角色进行AI对话模拟
    print("\n4. 与角色对话模拟...")
    ai_provider = MockAIProvider({'api_key': 'mock'})
    await ai_provider.initialize()

    # 模拟用户问题
    user_questions = [
        "请介绍一下人工智能的最新发展趋势",
        "机器学习在医疗领域有什么应用前景？",
        "您对AI伦理问题有什么看法？"
    ]

    for i, question in enumerate(user_questions, 1):
        print(f"\n   用户问题 {i}: {question}")

        # 创建AI请求
        ai_request = AIRequest(
            messages=[
                {"role": "system", "content": f"你是{character.name}，{character.description}"},
                {"role": "user", "content": question}
            ],
            max_tokens=200,
            temperature=0.7
        )

        # 获取AI回复
        response = await ai_provider.chat_completion(ai_request)
        print(f"   {character.name}的回答: {response.content}")

    # 5. 展示角色信息的用途
    print(f"\n5. 角色信息用途...")
    print(f"   - 角色类型 ({character.type.value}): 决定对话风格和知识领域")
    print(f"   - 角色描述: 用于AI生成符合角色的回复")
    print(f"   - 职位信息: 提供专业的背景知识")
    print(f"   - 经验背景: 影响回答的深度和专业性")

    print(f"\n=== 角色使用完成 ===")
    print(f"角色ID: {character.id}")
    print(f"你可以在其他会话中使用此角色ID来继续与该角色对话")


async def list_characters_demo():
    """列出所有角色的演示"""
    print(f"\n=== 查看所有已保存的角色 ===")

    storage = FileStorage()

    try:
        # 尝试列出角色 (注意：这个方法可能不存在于FileStorage中)
        characters = []  # 这里需要根据实际的FileStorage API调整

        if not characters:
            print("   当前没有保存的角色，或者FileStorage不支持列表功能")
            print("   你可以通过角色ID直接加载特定角色")
        else:
            for char in characters:
                print(f"   - {char.name} (ID: {char.id})")

    except Exception as e:
        print(f"   列出角色时出错: {e}")
        print("   这是正常的，某些存储系统可能不支持列表功能")


if __name__ == "__main__":
    asyncio.run(simple_character_demo())
    asyncio.run(list_characters_demo())

    print(f"\n=== 如何在其他地方使用角色 ===")
    print(f"1. 保存角色ID以便后续使用")
    print(f"2. 使用相同代码在不同程序中加载角色")
    print(f"3. 通过API或CLI工具与角色交互")
    print(f"4. 将角色集成到更大的AI应用中")