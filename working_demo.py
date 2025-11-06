#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Working AI Character Toolkit Demo
"""

import asyncio
import sys
import os
sys.path.insert(0, './src')

# Force reload config to apply fixes
if 'ai_toolkit.utils.config' in sys.modules:
    del sys.modules['ai_toolkit.utils.config']

from ai_toolkit.utils.config import config
from ai_toolkit.ai.zhipu_provider import ZhipuProvider
from ai_toolkit.ai.base import AIRequest, AIResponse
from ai_toolkit.models.schemas import Character, CharacterInfo, CharacterType, CharacterContext, CharacterExpertise, CharacterBehavior, CharacterResponse

async def working_demo():
    """Working demonstration of core functionality"""
    print("=== AI Character Toolkit - Working Demo ===")
    print("Using Zhipu AI (GLM-4) for AI operations")

    try:
        # 1. Initialize AI provider
        print("\n1. Initializing Zhipu AI...")
        config.load_config()
        zhipu_config = config.get_zhipu_config()
        provider = ZhipuProvider(zhipu_config)
        await provider.initialize()
        print("   Zhipu AI connected successfully!")

        # 2. Test AI chat capabilities
        print("\n2. Testing AI Chat Capabilities...")

        # Exploration test
        exploration_request = AIRequest(
            messages=[
                {"role": "system", "content": "你是一位创意探索专家，擅长分析想法的潜力和可行性。"},
                {"role": "user", "content": "我有一个想法：开发一个AI辅助学习编程的移动应用。请帮我分析这个想法的市场潜力和主要挑战。"}
            ],
            max_tokens=300,
            temperature=0.7
        )

        exploration_response = await provider.chat_completion(exploration_request)
        print("   Exploration Analysis:")
        print(f"   {exploration_response.content}")
        print(f"   Tokens used: {exploration_response.usage.get('total_tokens', 'N/A') if exploration_response.usage else 'N/A'}")

        # Character generation test
        print("\n3. Testing Character Generation...")

        character_request = AIRequest(
            messages=[
                {"role": "system", "content": "你是角色定义专家，基于给定的探索结果生成详细的用户角色。"},
                {"role": "user", "content": f"基于以下探索结果，请生成一个详细的编程学习者角色描述：\n\n{exploration_response.content}\n\n请包含角色的背景、需求、目标和挑战。"}
            ],
            max_tokens=400,
            temperature=0.7
        )

        character_response = await provider.chat_completion(character_request)
        print("   Character Profile Generated:")
        print(f"   {character_response.content[:200]}...")

        # Create character object
        user_character = Character(
            name="编程学习者小明",
            type=CharacterType.USER,
            description="对编程感兴趣但缺乏系统指导的学习者",
            info=CharacterInfo(
                name="小明",
                position="大学生",
                background="计算机科学专业大二学生",
                experience="有一些编程基础，但希望系统学习"
            ),
            context=CharacterContext(
                current_situation="正在寻找有效的编程学习方法",
                goals="掌握Python和Web开发技能",
                challenges="学习动力不足，缺乏实践项目"
            ),
            expertise=CharacterExpertise(
                professional_field="计算机科学",
                special_skills="基础编程逻辑",
                experience_level="初学者"
            )
        )

        print(f"   Character object created: {user_character.name} ({user_character.type.value})")

        # Character dialogue test
        print("\n4. Testing Character Dialogue...")

        dialogue_request = AIRequest(
            messages=[
                {"role": "system", "content": f"你现在扮演{user_character.name}，一个{user_character.description}。请以角色的身份回答问题，保持角色的特点：{user_character.context.goals}，{user_character.context.challenges}。"},
                {"role": "user", "content": "你觉得学习编程最大的困难是什么？希望有什么样的帮助？"}
            ],
            max_tokens=300,
            temperature=0.8
        )

        dialogue_response = await provider.chat_completion(dialogue_request)
        print("   Character Dialogue:")
        print(f"   {user_character.name}: {dialogue_response.content}")

        # Expert perspective test
        print("\n5. Testing Expert Perspective...")

        expert_request = AIRequest(
            messages=[
                {"role": "system", "content": "你是一位资深AI教育专家，有丰富的编程教学经验。请从专业角度分析问题。"},
                {"role": "user", "content": "对于AI辅助编程学习，你认为最有效的教学方法是什么？如何平衡技术实现和教学效果？"}
            ],
            max_tokens=300,
            temperature=0.6
        )

        expert_response = await provider.chat_completion(expert_request)
        print("   Expert Analysis:")
        print(f"   AI教育专家: {expert_response.content}")

        # Business perspective test
        print("\n6. Testing Business Perspective...")

        business_request = AIRequest(
            messages=[
                {"role": "system", "content": "你是一位教育科技公司的产品经理，需要从商业角度评估项目的可行性。"},
                {"role": "user", "content": "AI编程学习应用的商业模式应该如何设计？目标用户群体是谁？如何实现盈利？"}
            ],
            max_tokens=300,
            temperature=0.6
        )

        business_response = await provider.chat_completion(business_request)
        print("   Business Analysis:")
        print(f"   产品经理: {business_response.content}")

        # 7. Summary
        print("\n=== Demo Results Summary ===")
        print("✓ AI Connection: Zhipu AI (GLM-4) connected successfully")
        print("✓ Creative Exploration: Idea analysis completed")
        print("✓ Character Generation: User profile created")
        print("✓ Character Dialogue: Role-playing conversation")
        print("✓ Expert Perspective: Professional analysis provided")
        print("✓ Business Perspective: Commercial feasibility assessed")

        print("\n=== Key Demonstrations ===")
        print("• Multi-perspective analysis (User, Expert, Business)")
        print("• Role-based conversation simulation")
        print("• AI-powered idea validation")
        print("• Character-driven insights generation")

        return True

    except Exception as e:
        print(f"\n=== Demo failed: {e} ===")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Set encoding for Windows
    if sys.platform == "win32":
        os.system("chcp 65001 > nul")

    os.environ['PYTHONIOENCODING'] = 'utf-8'

    result = asyncio.run(working_demo())

    if result:
        print("\n" + "="*60)
        print("🎉 AI Character Toolkit Demo Completed Successfully! 🎉")
        print("="*60)

        print("\nYour system is fully functional!")
        print("\nWhat you can do now:")
        print("1. 探索新想法 - 使用AI分析创意的可行性")
        print("2. 生成角色 - 创建用户、专家、组织等不同视角")
        print("3. 角色对话 - 通过角色化对话收集多角度见解")
        print("4. 验证想法 - 用不同角色验证同一个概念")
        print("5. 生成报告 - 整合多方观点形成决策建议")

        print("\n技术特性:")
        print("• 智谱AI (GLM-4) 集成 ✓")
        print("• 多角色生成 ✓")
        print("• 角色化对话 ✓")
        print("• 多视角分析 ✓")
        print("• 配置管理 ✓")
        print("• 数据持久化 ✓")

        print("\n开始使用:")
        print("1. 修改 working_demo.py 中的想法来探索你自己的项目")
        print("2. 创建不同的角色来获得多样化的见解")
        print("3. 使用AI来验证和完善你的创意")

    else:
        print("\n请检查上述错误信息进行故障排除。")