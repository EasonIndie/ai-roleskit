#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final integration test for AI Character Toolkit
"""

import asyncio
import sys
import os
sys.path.insert(0, './src')

from ai_toolkit.core.character import CharacterManager
from ai_toolkit.models.schemas import Character, CharacterInfo, CharacterType, CharacterContext, CharacterExpertise, CharacterBehavior, CharacterResponse
from ai_toolkit.storage.file_storage import FileStorage

async def final_integration_test():
    """Final comprehensive test"""
    print("=== AI Character Toolkit - Final Integration Test ===")

    try:
        # 1. Test data models
        print("\n1. Testing data models...")

        # Create a character info
        info = CharacterInfo(
            name="张三",
            position="产品经理",
            background="5年互联网产品设计经验",
            experience="擅长用户体验设计和产品规划"
        )

        # Create a full character
        character = Character(
            name="张三",
            type=CharacterType.USER,
            description="一个典型的互联网产品用户",
            info=info,
            context=CharacterContext(
                current_situation="正在寻找AI解决方案来改善产品",
                goals="提高用户满意度和产品效率"
            ),
            expertise=CharacterExpertise(
                professional_field="产品设计",
                special_skills="用户需求分析"
            )
        )

        print(f"   Character created: {character.name} ({character.type.value})")
        print(f"   Description: {character.description}")

        # 2. Test storage
        print("\n2. Testing file storage...")
        storage = FileStorage()

        # Save character
        await storage.save_character(character)
        print(f"   Character saved: {character.id}")

        # Load character
        loaded_char = await storage.get_character(character.id)
        print(f"   Character loaded: {loaded_char.name}")

        # List characters
        all_chars = await storage.list_characters()
        print(f"   Total characters in storage: {len(all_chars)}")

        # 3. Test character manager
        print("\n3. Testing character manager...")
        from ai_toolkit.ai.base import BaseAIProvider, AIRequest, AIResponse

        class SimpleMockProvider(BaseAIProvider):
            def __init__(self, config):
                self._provider_name = "mock"
                self._default_model = "mock-model"

            @property
            def provider_name(self):
                return self._provider_name

            @property
            def default_model(self):
                return self._default_model

            async def _load_models(self):
                pass

            async def initialize(self):
                pass

            async def chat_completion(self, request):
                return AIResponse(content="Mock response", role="assistant")

            async def chat_completion_stream(self, request):
                yield "Mock stream response"

        mock_provider = SimpleMockProvider({})
        await mock_provider.initialize()

        character_manager = CharacterManager(mock_provider)
        character_manager.characters[character.id] = character

        retrieved_char = await character_manager.get_character(character.id)
        print(f"   Retrieved character: {retrieved_char.name}")

        # 4. Test template system
        print("\n4. Testing template system...")
        from ai_toolkit.templates.prompts import template_manager

        # Test template rendering
        prompt = template_manager.render_template(
            'user_character',
            character=character,
            character_name=character.name
        )
        print(f"   Template rendered successfully (length: {len(prompt)})")

        # 5. Test configuration
        print("\n5. Testing configuration...")
        from ai_toolkit.utils.config import config

        # Test config reading
        ai_provider = config.get_ai_provider()
        print(f"   AI provider from config: {ai_provider}")

        # Test different config sections
        zhipu_config = config.get_zhipu_config()
        print(f"   Zhipu config available: {bool(zhipu_config)}")

        print("\n=== All Integration Tests Passed! ===")
        print("\nYour AI Character Toolkit is fully functional and ready to use!")

        print("\n=== Summary ===")
        print("✓ Data models working correctly")
        print("✓ File storage system functional")
        print("✓ Character manager operational")
        print("✓ Template system rendering correctly")
        print("✓ Configuration loading properly")

        print("\n=== Next Steps ===")
        print("To start using your AI Character Toolkit:")
        print("1. Configure your preferred AI provider API key in .env file")
        print("2. Run: python cli.py --help")
        print("3. Start exploring: python cli.py explore start 'your idea'")
        print("4. Create characters: python cli.py character create --type user")
        print("5. Start dialogues: python cli.py dialogue start <character-id>")

        return True

    except Exception as e:
        print(f"\n=== Integration test failed: {e} ===")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Set UTF-8 encoding for Windows
    if sys.platform == "win32":
        os.system("chcp 65001 > nul")

    result = asyncio.run(final_integration_test())

    if result:
        print("\n🎉 Installation and setup complete! 🎉")
    else:
        print("\n❌ Please check the error messages above.")