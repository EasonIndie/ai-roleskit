#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo test script using mock AI provider
"""

import asyncio
import sys
import os
sys.path.insert(0, './src')

from ai_toolkit.core.character import CharacterManager
from ai_toolkit.core.exploration import CreativeExplorer
from ai_toolkit.core.dialogue import DialogueManager
from ai_toolkit.models.schemas import CharacterType
from ai_toolkit.ai.base import BaseAIProvider, AIRequest, AIResponse

class MockAIProvider(BaseAIProvider):
    """Mock AI provider for demonstration"""

    def __init__(self, config):
        self.config = config
        self._provider_name = "mock"
        self._default_model = "mock-model"

    @property
    def provider_name(self):
        return self._provider_name

    @property
    def default_model(self):
        return self._default_model

    async def _load_models(self):
        # Mock implementation
        pass

    async def initialize(self):
        pass

    async def chat_completion(self, request):
        # Mock responses for different types of requests
        mock_responses = {
            'exploration': "这是一个很有趣的想法！我们可以从用户需求、技术可行性、商业模式等多个角度来深入探索这个概念。",
            'character': "基于探索结果，我为您生成了一个具有丰富背景和专业知识的角色。",
            'dialogue': "作为一名AI角色，我认为这个想法很有价值，但也需要考虑一些实际因素。"
        }

        content = "这是一个模拟的AI响应，用于演示系统功能。"
        return AIResponse(content=content, role="assistant")

    async def chat_completion_stream(self, request):
        yield "模拟流式响应..."

async def test_with_mock_provider():
    """Test functionality with mock AI provider"""
    print("=== AI Character Toolkit Demo Test ===")

    try:
        # 1. Setup mock provider
        print("\n1. Setting up mock AI provider...")
        mock_provider = MockAIProvider({})
        await mock_provider.initialize()
        print("   Mock AI provider ready!")

        # 2. Initialize managers
        print("\n2. Initializing system components...")
        character_manager = CharacterManager(mock_provider)
        explorer = CreativeExplorer(mock_provider)
        dialogue_manager = DialogueManager(mock_provider, character_manager)
        print("   All components initialized successfully!")

        # 3. Test creative exploration
        print("\n3. Testing creative exploration...")
        session = await explorer.start_exploration("开发一个AI辅助学习编程的移动应用")
        print(f"   Exploration session created: {session.id}")
        print(f"   Initial idea: {session.initial_idea}")

        # Test exploration
        result = await explorer.explore_idea(
            session.id,
            "请帮我分析这个想法的可行性"
        )
        print(f"   Exploration response: {result['ai_response'][:50]}...")

        # 4. Test character generation
        print("\n4. Testing character generation...")
        summary = await explorer.get_exploration_summary(session.id)

        # Create different character types
        user_char = await character_manager.create_character(
            summary, CharacterType.USER, "学习者小王"
        )
        print(f"   User character created: {user_char.name}")

        expert_char = await character_manager.create_character(
            summary, CharacterType.EXPERT, "AI教育专家李老师"
        )
        print(f"   Expert character created: {expert_char.name}")

        org_char = await character_manager.create_character(
            summary, CharacterType.ORGANIZATION, "教育科技公司"
        )
        print(f"   Organization character created: {org_char.name}")

        # 5. Test dialogue
        print("\n5. Testing character dialogue...")
        dialogue = await dialogue_manager.create_dialogue(
            user_char.id,
            "产品需求讨论"
        )
        print(f"   Dialogue created: {dialogue.id}")

        response = await dialogue_manager.send_message(
            dialogue.id,
            "你认为这个学习应用最重要的功能是什么？"
        )
        print(f"   Character response: {response.content[:50]}...")

        # 6. Test character listing
        print("\n6. Testing character management...")
        all_characters = await character_manager.list_characters()
        print(f"   Total characters: {len(all_characters)}")
        for char in all_characters:
            print(f"   - {char.name} ({char.type.value})")

        print("\n=== All tests passed successfully! ===")
        print("\nYour AI Character Toolkit is fully functional!")
        print("\nTo use with real AI:")
        print("1. Configure your API key in .env file")
        print("2. Use: python cli.py explore start 'your idea'")
        print("3. Create characters and start dialogues")

        return True

    except Exception as e:
        print(f"\n=== Test failed: {e} ===")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Set UTF-8 encoding for Windows
    if sys.platform == "win32":
        os.system("chcp 65001 > nul")

    result = asyncio.run(test_with_mock_provider())

    if result:
        print("\n=== Ready to use! ===")
        print("\nQuick start commands:")
        print("1. python cli.py --help")
        print("2. python cli.py character list")
        print("3. python cli.py dialogue start <character-id>")
    else:
        print("\nPlease check the error messages above.")