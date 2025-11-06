#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test script to verify AI Character Toolkit functionality
"""

import asyncio
import sys
import os
sys.path.insert(0, './src')

from ai_toolkit.core.character import CharacterManager
from ai_toolkit.core.exploration import CreativeExplorer
from ai_toolkit.ai.zhipu_provider import ZhipuProvider
from ai_toolkit.models.schemas import CharacterType
from ai_toolkit.utils.config import config

async def test_basic_functionality():
    """Test basic functionality"""
    print("=== AI Character Toolkit Functionality Test ===")

    try:
        # 1. Test AI provider
        print("\n1. Testing AI provider...")
        ai_config = config.get_zhipu_config()
        provider = ZhipuProvider(ai_config)
        await provider.initialize()
        print("   AI Provider initialized successfully!")

        # 2. Test character manager
        print("\n2. Testing character manager...")
        character_manager = CharacterManager(provider)
        print("   Character manager initialized successfully!")

        # 3. Test creative explorer
        print("\n3. Testing creative explorer...")
        explorer = CreativeExplorer(provider)
        print("   Creative explorer initialized successfully!")

        # 4. Test exploration session
        print("\n4. Testing exploration session...")
        session = await explorer.start_exploration("开发一个AI辅助学习编程的移动应用")
        print(f"   Exploration session created: {session.id}")

        # 5. Test character generation
        print("\n5. Testing character generation...")
        summary = await explorer.get_exploration_summary(session.id)
        user_character = await character_manager.create_character(
            summary, CharacterType.USER, "学习者代表"
        )
        print(f"   User character created: {user_character.name}")

        print("\n=== All tests passed! ===")
        print("Your AI Character Toolkit is ready to use!")

        return True

    except Exception as e:
        print(f"\n=== Test failed: {e} ===")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Set UTF-8 encoding
    if sys.platform == "win32":
        os.system("chcp 65001 > nul")

    result = asyncio.run(test_basic_functionality())

    if result:
        print("\nNext steps:")
        print("1. Try running: python cli.py explore start 'your idea'")
        print("2. Create characters: python cli.py character create --type user")
        print("3. Start dialogue: python cli.py dialogue start <character-id>")
    else:
        print("\nPlease check the error messages above for troubleshooting.")