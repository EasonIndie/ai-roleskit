#!/usr/bin/env python3
"""
AI Character Toolkit - 实用示例集合
包含各种常见使用场景的完整代码示例
"""

import asyncio
import sys
sys.path.insert(0, './src')

from ai_toolkit.models.schemas import Character, CharacterInfo, CharacterType
from ai_toolkit.storage.file_storage import FileStorage
from demo import MockAIProvider
from ai_toolkit.ai.base import AIRequest


# 示例1: 创建专家角色并进行咨询
async def example_1_expert_consultation():
    """示例1: 专家咨询"""
    print("=== 示例1: 专家咨询 ===")

    # 创建AI专家
    expert_info = CharacterInfo(
        name="张博士",
        position="AI研究科学家",
        experience="15年机器学习和深度学习研究经验"
    )

    expert = Character(
        name="张博士",
        type=CharacterType.EXPERT,
        description="专门研究人工智能和机器学习的资深专家",
        info=expert_info
    )

    # 保存角色
    storage = FileStorage()
    await storage.save_character(expert)

    # 模拟咨询对话
    ai_provider = MockAIProvider({'api_key': 'mock'})
    await ai_provider.initialize()

    consultations = [
        "请解释一下transformer模型的工作原理",
        "您认为AGI（通用人工智能）什么时候能实现？",
        "对于想进入AI领域的新人，您有什么建议？"
    ]

    print(f"咨询专家: {expert.name}")
    for i, question in enumerate(consultations, 1):
        print(f"\n{i}. 用户: {question}")

        request = AIRequest(
            messages=[
                {"role": "system", "content": f"你是{expert.name}，{expert.description}。请用专业、准确的语调回答。"},
                {"role": "user", "content": question}
            ]
        )

        response = await ai_provider.chat_completion(request)
        print(f"   {expert.name}: {response.content}")

    return expert


# 示例2: 用户角色进行需求分析
async def example_2_user_analysis():
    """示例2: 用户需求分析"""
    print("\n=== 示例2: 用户需求分析 ===")

    # 创建用户角色
    user_info = CharacterInfo(
        name="李经理",
        position="产品经理",
        experience="5年互联网产品设计经验"
    )

    user = Character(
        name="李经理",
        type=CharacterType.USER,
        description="正在为新项目寻找AI解决方案的产品经理",
        info=user_info
    )

    # 模拟需求分析对话
    ai_provider = MockAIProvider({'api_key': 'mock'})
    await ai_provider.initialize()

    scenarios = [
        "我们公司想要开发一个智能客服系统，您觉得应该从哪些方面考虑？",
        "用户对我们的产品反应说界面太复杂，您有什么建议？",
        "如何平衡功能性和用户体验？"
    ]

    print(f"用户访谈: {user.name}")
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. 产品需求: {scenario}")

        request = AIRequest(
            messages=[
                {"role": "system", "content": f"你是{user.name}，{user.description}。请从用户角度出发，关注实用性和体验。"},
                {"role": "user", "content": scenario}
            ]
        )

        response = await ai_provider.chat_completion(request)
        print(f"   {user.name}: {response.content}")

    return user


# 示例3: 组织角色进行战略分析
async def example_3_organization_strategy():
    """示例3: 组织战略分析"""
    print("\n=== 示例3: 组织战略分析 ===")

    # 创建组织角色
    org_info = CharacterInfo(
        name="科技创新部",
        position="企业战略部门",
        experience="10年技术战略规划经验"
    )

    organization = Character(
        name="科技创新部",
        type=CharacterType.ORGANIZATION,
        description="负责公司技术创新战略制定的专业团队",
        info=org_info
    )

    # 模拟战略讨论
    ai_provider = MockAIProvider({'api_key': 'mock'})
    await ai_provider.initialize()

    strategies = [
        "公司应该如何布局AI技术发展？",
        "在数字化转型中，我们应该优先投资哪些领域？",
        "如何平衡短期收益和长期技术发展？"
    ]

    print(f"战略讨论: {organization.name}")
    for i, strategy in enumerate(strategies, 1):
        print(f"\n{i}. 战略问题: {strategy}")

        request = AIRequest(
            messages=[
                {"role": "system", "content": f"你代表{organization.name}，{organization.description}。请从组织角度，提供客观、全面的战略建议。"},
                {"role": "user", "content": strategy}
            ]
        )

        response = await ai_provider.chat_completion(request)
        print(f"   {organization.name}: {response.content}")

    return organization


# 示例4: 多角色协作讨论
async def example_4_multi_role_collaboration():
    """示例4: 多角色协作讨论"""
    print("\n=== 示例4: 多角色协作讨论 ===")

    # 创建三个不同角色
    ai_provider = MockAIProvider({'api_key': 'mock'})
    await ai_provider.initialize()

    expert = Character(
        name="技术专家",
        type=CharacterType.EXPERT,
        description="AI技术专家"
    )

    user = Character(
        name="用户代表",
        type=CharacterType.USER,
        description="产品用户代表"
    )

    org = Character(
        name="项目经理",
        type=CharacterType.ORGANIZATION,
        description="项目管理负责人"
    )

    # 讨论主题：开发AI聊天机器人
    topic = "我们应该如何设计一个AI客服聊天机器人？"

    print(f"讨论主题: {topic}")
    print("=" * 40)

    roles = [
        (expert, "技术专家角度"),
        (user, "用户体验角度"),
        (org, "项目管理角度")
    ]

    for character, perspective in roles:
        print(f"\n{perspective} - {character.name}:")

        request = AIRequest(
            messages=[
                {"role": "system", "content": f"你是{character.name}，{character.description}。请从{perspective}发表意见。"},
                {"role": "user", "content": topic}
            ]
        )

        response = await ai_provider.chat_completion(request)
        print(f"   {response.content}")


# 示例5: 角色模板和快速创建
async def example_5_character_templates():
    """示例5: 角色模板创建"""
    print("\n=== 示例5: 角色模板创建 ===")

    # 定义角色模板
    character_templates = {
        "医生": {
            "type": CharacterType.EXPERT,
            "description": "资深医疗专家",
            "position": "主任医师",
            "experience": "15年临床经验"
        },
        "教师": {
            "type": CharacterType.EXPERT,
            "description": "教育领域专家",
            "position": "高级教师",
            "experience": "10年教学经验"
        },
        "律师": {
            "type": CharacterType.EXPERT,
            "description": "法律专业人士",
            "position": "执业律师",
            "experience": "8年法律实务经验"
        },
        "客户": {
            "type": CharacterType.USER,
            "description": "普通消费者",
            "position": "终端用户",
            "experience": "日常产品使用者"
        },
        "创业公司": {
            "type": CharacterType.ORGANIZATION,
            "description": "创新型创业团队",
            "position": "技术团队",
            "experience": "专注于新技术研发"
        }
    }

    print("可用角色模板:")
    for name, template in character_templates.items():
        print(f"- {name}: {template['description']}")

    # 使用模板创建角色
    selected_role = "医生"
    template = character_templates[selected_role]

    character_info = CharacterInfo(
        name="王医生",
        position=template["position"],
        experience=template["experience"]
    )

    doctor = Character(
        name="王医生",
        type=template["type"],
        description=template["description"],
        info=character_info
    )

    print(f"\n使用模板创建角色: {doctor.name}")
    print(f"类型: {doctor.type.value}")
    print(f"描述: {doctor.description}")
    print(f"职位: {doctor.info.position}")

    return doctor


# 示例6: 角色信息导出和导入
async def example_6_character_export_import():
    """示例6: 角色导出和导入"""
    print("\n=== 示例6: 角色导出和导入 ===")

    # 创建一个示例角色
    character_info = CharacterInfo(
        name="数据科学家",
        position="AI研究员",
        experience="8年数据分析和机器学习经验"
    )

    character = Character(
        name="数据科学家",
        type=CharacterType.EXPERT,
        description="专注于数据科学和机器学习的研究人员",
        info=character_info
    )

    # 导出角色信息为字典
    character_dict = character.to_dict()

    print("角色信息导出:")
    print(f"名称: {character_dict['name']}")
    print(f"类型: {character_dict['type']}")
    print(f"描述: {character_dict['description']}")
    print(f"职位: {character_dict['info']['position']}")

    # 保存到文件（模拟）
    import json
    with open('character_export.json', 'w', encoding='utf-8') as f:
        json.dump(character_dict, f, ensure_ascii=False, indent=2)

    print("\n角色已导出到 character_export.json")

    # 从文件导入（模拟）
    with open('character_export.json', 'r', encoding='utf-8') as f:
        loaded_dict = json.load(f)

    print("从文件导入的角色信息:")
    print(f"名称: {loaded_dict['name']}")
    print(f"类型: {loaded_dict['type']}")
    print(f"描述: {loaded_dict['description']}")


# 示例7: 批量创建和管理角色
async def example_7_batch_character_management():
    """示例7: 批量角色管理"""
    print("\n=== 示例7: 批量角色管理 ===")

    # 定义要批量创建的角色
    characters_to_create = [
        {
            "name": "市场分析师",
            "type": CharacterType.EXPERT,
            "description": "专业的市场趋势分析专家",
            "position": "高级市场分析师",
            "experience": "12年市场研究经验"
        },
        {
            "name": "用户体验设计师",
            "type": CharacterType.EXPERT,
            "description": "专注用户体验和界面设计的专家",
            "position": "UX设计主管",
            "experience": "8年设计经验"
        },
        {
            "name": "潜在客户",
            "type": CharacterType.USER,
            "description": "目标产品的潜在用户",
            "position": "消费者",
            "experience": "日常使用同类产品"
        }
    ]

    created_characters = []

    # 批量创建角色
    storage = FileStorage()

    for char_data in characters_to_create:
        character_info = CharacterInfo(
            name=char_data["name"],
            position=char_data["position"],
            experience=char_data["experience"]
        )

        character = Character(
            name=char_data["name"],
            type=char_data["type"],
            description=char_data["description"],
            info=character_info
        )

        # 保存角色
        await storage.save_character(character)
        created_characters.append(character)
        print(f"✓ 创建角色: {character.name} (ID: {character.id})")

    # 批量管理
    print(f"\n批量创建了 {len(created_characters)} 个角色:")
    for char in created_characters:
        print(f"- {char.name} ({char.type.value}): {char.description}")

    return created_characters


# 主函数：运行所有示例
async def main():
    """运行所有示例"""
    print("AI Character Toolkit - 实用示例集合")
    print("=" * 50)

    examples = [
        ("专家咨询", example_1_expert_consultation),
        ("用户需求分析", example_2_user_analysis),
        ("组织战略分析", example_3_organization_strategy),
        ("多角色协作", example_4_multi_role_collaboration),
        ("角色模板创建", example_5_character_templates),
        ("角色导出导入", example_6_character_export_import),
        ("批量角色管理", example_7_batch_character_management)
    ]

    for name, example_func in examples:
        try:
            print(f"\n{'='*20} {name} {'='*20}")
            await example_func()
            print(f"✓ {name} 示例完成")
        except Exception as e:
            print(f"✗ {name} 示例失败: {e}")

    print(f"\n{'='*50}")
    print("所有示例演示完成！")
    print("你可以根据这些示例来开发自己的AI角色应用。")


if __name__ == "__main__":
    asyncio.run(main())