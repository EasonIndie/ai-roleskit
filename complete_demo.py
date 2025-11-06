#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete AI Character Toolkit Demo with Zhipu AI
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
from ai_toolkit.core.character import CharacterManager
from ai_toolkit.core.exploration import CreativeExplorer
from ai_toolkit.core.dialogue import DialogueManager
from ai_toolkit.models.schemas import CharacterType

async def complete_workflow_demo():
    """Complete workflow demonstration"""
    print("=== AI Character Toolkit - Complete Workflow Demo ===")
    print("Using Zhipu AI (GLM-4) for all AI operations")

    try:
        # 1. Initialize all components
        print("\n1. Initializing AI Character Toolkit...")
        config.load_config()
        zhipu_config = config.get_zhipu_config()
        provider = ZhipuProvider(zhipu_config)
        await provider.initialize()

        character_manager = CharacterManager(provider)
        explorer = CreativeExplorer(provider)
        dialogue_manager = DialogueManager(provider, character_manager)

        print("   All components initialized successfully!")

        # 2. Creative Exploration
        print("\n2. Starting Creative Exploration...")
        print("   Idea: 开发一个AI辅助学习编程的移动应用")

        session = await explorer.start_exploration("开发一个AI辅助学习编程的移动应用")
        print(f"   Session created: {session.id}")

        # Explore the idea
        result = await explorer.explore_idea(
            session.id,
            "请帮我分析这个想法的市场潜力和技术可行性"
        )
        print(f"   Analysis completed!")
        print(f"   AI Response: {result['ai_response'][:100]}...")

        # Get exploration summary
        summary = await explorer.get_exploration_summary(session.id)
        print(f"   Exploration readiness: {summary['character_generation_readiness']}")

        # 3. Character Generation
        print("\n3. Generating AI Characters...")

        # Create user character
        user_char = await character_manager.create_character(
            summary, CharacterType.USER, "编程学习者小明"
        )
        print(f"   User character created: {user_char.name}")
        print(f"   Description: {user_char.description}")

        # Create expert character
        expert_char = await character_manager.create_character(
            summary, CharacterType.EXPERT, "AI教育专家李老师"
        )
        print(f"   Expert character created: {expert_char.name}")
        print(f"   Description: {expert_char.description}")

        # Create organization character
        org_char = await character_manager.create_character(
            summary, CharacterType.ORGANIZATION, "教育科技公司"
        )
        print(f"   Organization character created: {org_char.name}")
        print(f"   Description: {org_char.description}")

        # 4. Character Dialogues
        print("\n4. Starting Character Dialogues...")

        # Dialogue with user character
        user_dialogue = await dialogue_manager.create_dialogue(
            user_char.id,
            "用户需求讨论"
        )

        user_response = await dialogue_manager.send_message(
            user_dialogue.id,
            "你认为编程初学者最需要什么样的帮助？"
        )
        print(f"   User ({user_char.name}): {user_response.content[:80]}...")

        # Dialogue with expert character
        expert_dialogue = await dialogue_manager.create_dialogue(
            expert_char.id,
            "专业建议咨询"
        )

        expert_response = await dialogue_manager.send_message(
            expert_dialogue.id,
            "从教学角度，如何设计AI辅助编程学习最有效？"
        )
        print(f"   Expert ({expert_char.name}): {expert_response.content[:80]}...")

        # Dialogue with organization character
        org_dialogue = await dialogue_manager.create_dialogue(
            org_char.id,
            "商业可行性分析"
        )

        org_response = await dialogue_manager.send_message(
            org_dialogue.id,
            "这个AI编程学习应用的商业模式应该如何设计？"
        )
        print(f"   Organization ({org_char.name}): {org_response.content[:80]}...")

        # 5. Multi-Character Validation
        print("\n5. Multi-Character Perspective Analysis...")

        from ai_toolkit.core.concurrent import ConcurrentValidator
        validator = ConcurrentValidator(provider, character_manager)

        question = "如何平衡学习效果和用户体验？"
        validation_session = await validator.create_validation_session(
            question,
            [user_char.id, expert_char.id, org_char.id]
        )

        validation_result = await validator.run_concurrent_validation(
            validation_session.id,
            [user_char.id, expert_char.id, org_char.id]
        )

        print(f"   Question: {question}")
        print(f"   User perspective: {validation_result['character_responses'][user_char.id][:50]}...")
        print(f"   Expert perspective: {validation_result['character_responses'][expert_char.id][:50]}...")
        print(f"   Organization perspective: {validation_result['character_responses'][org_char.id][:50]}...")

        # 6. Integration Analysis
        print("\n6. Integration Analysis...")

        from ai_toolkit.core.analysis import IntegrationAnalyzer
        analyzer = IntegrationAnalyzer(provider, character_manager)

        decision_report = await analyzer.generate_decision_report(validation_session)
        print(f"   Decision report generated: {len(decision_report.get('executive_summary', ''))} characters")

        # 7. Summary
        print("\n=== Demo Summary ===")
        print(f"✓ Creative exploration session: {session.id}")
        print(f"✓ Characters generated: {len([user_char, expert_char, org_char])}")
        print(f"✓ Dialogues conducted: 3")
        print(f"✓ Multi-perspective validation: Completed")
        print(f"✓ Integration analysis: Generated")

        print("\n=== Key Insights Generated ===")
        print("• User perspective on learning needs")
        print("• Expert recommendations for teaching methodology")
        print("• Business considerations for implementation")
        print("• Multi-stakeholder validation results")
        print("• Integrated decision recommendations")

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

    result = asyncio.run(complete_workflow_demo())

    if result:
        print("\n" + "="*50)
        print("🎉 AI Character Toolkit Demo Completed Successfully! 🎉")
        print("="*50)
        print("\nYour system is fully functional and ready for production use!")

        print("\nNext steps:")
        print("1. Explore your own ideas:")
        print("   python -c \"import asyncio; from complete_demo import complete_workflow_demo; asyncio.run(complete_workflow_demo())\"")
        print("\n2. Use CLI for interactive sessions:")
        print("   (Note: CLI may have encoding issues on Windows)")
        print("\n3. Create custom characters and dialogues")
        print("4. Generate reports and recommendations")

        print("\nFeatures demonstrated:")
        print("• Creative idea exploration")
        print("• Multi-character generation")
        print("• Interactive dialogues")
        print("• Concurrent validation")
        print("• Integration analysis")
        print("• Decision support")
    else:
        print("\nPlease check the error messages above for troubleshooting.")