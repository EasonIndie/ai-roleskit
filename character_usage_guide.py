#!/usr/bin/env python3
"""
角色使用指南 - 展示如何创建和使用角色
"""

import asyncio
import sys
sys.path.insert(0, './src')

from ai_toolkit.models.schemas import Character, CharacterInfo, CharacterType
from demo import MockAIProvider
from ai_toolkit.ai.base import AIRequest


def create_character_examples():
    """创建不同类型角色的示例"""
    print("=== 角色创建示例 ===")

    # 1. 专家角色
    expert_info = CharacterInfo(
        name="李博士",
        position="可持续发展专家",
        experience="15年环保和新能源领域经验"
    )
    expert_character = Character(
        name="李博士",
        type=CharacterType.EXPERT,
        description="专注于可持续发展和绿色能源解决方案的专家",
        info=expert_info
    )

    # 2. 用户角色
    user_info = CharacterInfo(
        name="小明",
        position="产品经理",
        experience="5年互联网产品设计经验"
    )
    user_character = Character(
        name="小明",
        type=CharacterType.USER,
        description="正在寻找创新解决方案的产品经理",
        info=user_info
    )

    # 3. 组织角色
    org_info = CharacterInfo(
        name="创新科技",
        position="AI研发部门",
        experience="10年AI产品开发经验"
    )
    org_character = Character(
        name="创新科技",
        type=CharacterType.ORGANIZATION,
        description="专注于人工智能技术研发的创新团队",
        info=org_info
    )

    return [expert_character, user_character, org_character]


async def demonstrate_character_usage(character):
    """演示角色使用方法"""
    print(f"\n=== 使用角色: {character.name} ===")
    print(f"类型: {character.type.value}")
    print(f"描述: {character.description}")

    # 创建AI provider
    ai_provider = MockAIProvider({'api_key': 'mock'})
    await ai_provider.initialize()

    # 根据角色类型设置不同的系统提示
    if character.type == CharacterType.EXPERT:
        system_prompt = f"你是{character.name}，{character.description}。请以专业、深入的语调回答问题。"
    elif character.type == CharacterType.USER:
        system_prompt = f"你是{character.name}，{character.description}。请以好奇、探索的语调回应。"
    else:  # ORGANIZATION
        system_prompt = f"你代表{character.name}，{character.description}。请以专业、客观的语调提供组织观点。"

    print(f"\n系统提示: {system_prompt}")

    # 模拟对话
    questions = [
        "请介绍一下您的主要专长领域",
        "您如何看待当前的技术发展趋势？",
        "您有什么建议可以分享吗？"
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n{i}. 问题: {question}")

        # 构建AI请求
        ai_request = AIRequest(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=150,
            temperature=0.7
        )

        # 获取回复
        response = await ai_provider.chat_completion(ai_request)
        print(f"   {character.name}: {response.content}")


def show_usage_methods():
    """展示角色的不同使用方法"""
    print(f"\n=== 角色使用方法总结 ===")

    methods = {
        "1. CLI方式": [
            "python cli.py character create <type> --name <name>",
            "python cli.py dialogue start <character_id>",
            "python cli.py dialogue message <character_id> <message>"
        ],
        "2. 代码方式": [
            "# 创建角色",
            "character = Character(name='专家', type=CharacterType.EXPERT)",
            "# 使用角色进行AI对话",
            "ai_request = AIRequest(messages=[...])",
            "response = await ai_provider.chat_completion(ai_request)"
        ],
        "3. 存储方式": [
            "# 保存角色",
            "await storage.save_character(character)",
            "# 加载角色",
            "character = await storage.load_character(character_id)"
        ],
        "4. 对话管理": [
            "# 创建对话会话",
            "dialogue = await dialogue_manager.create_dialogue(character_id)",
            "# 添加消息",
            "await dialogue_manager.add_message(dialogue_id, role, content)",
            "# 获取回复",
            "response = await dialogue_manager.get_character_response(...)"
        ]
    }

    for method, steps in methods.items():
        print(f"\n{method}:")
        for step in steps:
            print(f"   {step}")


def show_character_types():
    """展示不同角色类型的用途"""
    print(f"\n=== 角色类型说明 ===")

    types_info = {
        "专家 (EXPERT)": {
            "用途": "提供专业知识和深度见解",
            "示例": "科学家、顾问、行业专家",
            "特点": "专业、深入、权威",
            "适用场景": "技术咨询、专业分析、深度探讨"
        },
        "用户 (USER)": {
            "用途": "代表用户视角和需求",
            "示例": "客户、用户、利益相关者",
            "特点": "实用、体验导向、需求驱动",
            "适用场景": "用户研究、需求分析、产品讨论"
        },
        "组织 (ORGANIZATION)": {
            "用途": "代表机构或群体观点",
            "示例": "公司、部门、团队",
            "特点": "客观、全面、战略思考",
            "适用场景": "战略分析、组织决策、团队协作"
        }
    }

    for char_type, info in types_info.items():
        print(f"\n{char_type}:")
        for key, value in info.items():
            print(f"   {key}: {value}")


async def main():
    """主函数"""
    print("AI Character Toolkit - 完整角色使用指南")
    print("=" * 50)

    # 1. 创建不同类型的角色示例
    characters = create_character_examples()

    print(f"\n创建了 {len(characters)} 个角色:")
    for char in characters:
        print(f"- {char.name} ({char.type.value})")

    # 2. 演示每个角色的使用
    for character in characters:
        await demonstrate_character_usage(character)

    # 3. 展示使用方法
    show_usage_methods()

    # 4. 展示角色类型
    show_character_types()

    print(f"\n=== 总结 ===")
    print("角色创建后，你可以通过以下方式调用:")
    print("1. 保存角色ID用于后续加载")
    print("2. 在AI对话中使用角色信息作为系统提示")
    print("3. 通过对话管理器进行连续对话")
    print("4. 在不同的AI模型和场景中复用角色")


if __name__ == "__main__":
    asyncio.run(main())