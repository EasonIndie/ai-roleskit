#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test with fixed configuration handling
"""

import asyncio
import sys
import os
sys.path.insert(0, './src')

# Force reload config module
if 'ai_toolkit.utils.config' in sys.modules:
    del sys.modules['ai_toolkit.utils.config']

from ai_toolkit.utils.config import config
from ai_toolkit.ai.zhipu_provider import ZhipuProvider

async def test_fixed_config():
    """Test with fixed configuration"""
    print("=== Testing Fixed Configuration ===")

    try:
        # 1. Reload config to apply fixes
        print("\n1. Reloading configuration...")
        config.load_config()
        print("   Configuration reloaded!")

        # 2. Check Zhipu config
        print("\n2. Checking Zhipu configuration...")
        zhipu_config = config.get_zhipu_config()
        api_key = zhipu_config.get('api_key', '')
        model = zhipu_config.get('model', 'glm-4')

        print(f"   Model: {model}")
        print(f"   API Key length: {len(api_key)}")
        print(f"   API Key preview: {api_key[:8]}...{api_key[-4:] if len(api_key) > 12 else 'INVALID'}")

        # Check if environment variable was properly substituted
        if api_key.startswith('${'):
            print("   ERROR: Environment variable not substituted!")
            return False
        else:
            print("   SUCCESS: Environment variable substituted correctly!")

        # 3. Test Zhipu AI connection
        print("\n3. Testing Zhipu AI connection...")
        provider = ZhipuProvider(zhipu_config)
        await provider.initialize()
        print("   AI connection established successfully!")

        # 4. Test basic chat
        print("\n4. Testing basic chat...")
        from ai_toolkit.ai.base import AIRequest

        request = AIRequest(
            messages=[
                {"role": "user", "content": "你好，请简单回复'测试成功'"}
            ],
            max_tokens=50,
            temperature=0.7
        )

        response = await provider.chat_completion(request)
        print(f"   AI Response: {response.content}")
        print(f"   Tokens used: {response.usage.get('total_tokens', 'N/A') if response.usage else 'N/A'}")

        print("\n=== All tests passed! ===")
        print("Your AI Character Toolkit is now fully functional with Zhipu AI!")

        return True

    except Exception as e:
        print(f"\n=== Test failed: {e} ===")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_fixed_config())

    if result:
        print("\n=== Ready to use! ===")
        print("You can now use the AI Character Toolkit:")
        print("1. python cli.py explore start 'your idea' --provider zhipu")
        print("2. python cli.py character create --type user --name 'name' --provider zhipu")
        print("3. python cli.py dialogue start <character-id> --provider zhipu")
    else:
        print("\nPlease check the error messages above.")