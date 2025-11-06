#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct Zhipu AI test without toolkit wrapper
"""

import asyncio
import sys
import os
sys.path.insert(0, './src')

from ai_toolkit.utils.config import config

async def test_direct_zhipu():
    """Test Zhipu AI directly"""
    print("=== Direct Zhipu AI Test ===")

    try:
        # Get config directly
        print("\n1. Checking configuration...")
        zhipu_config = config.get_zhipu_config()

        api_key = zhipu_config.get('api_key', '')
        model = zhipu_config.get('model', 'glm-4')

        print(f"   Model: {model}")
        print(f"   API Key: {api_key[:8]}...{api_key[-4:] if len(api_key) > 12 else 'INVALID'}")
        print(f"   API Key length: {len(api_key)}")

        # Try direct zai-sdk usage
        print("\n2. Testing direct zai-sdk...")
        try:
            import zai
            from zai import ZhipuAI

            client = ZhipuAI(api_key=api_key)

            # Simple test
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": "你好，请回复'测试成功'"}
                ],
                max_tokens=10
            )

            print(f"   Direct response: {response.choices[0].message.content}")
            print("   Direct zai-sdk test: SUCCESS")

            return True

        except Exception as e:
            print(f"   Direct zai-sdk test failed: {e}")

            # Fallback: try with requests
            print("\n3. Testing with HTTP requests...")
            import httpx

            url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": model,
                "messages": [
                    {"role": "user", "content": "你好，请回复'HTTP测试成功'"}
                ],
                "max_tokens": 10
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=data)

                if response.status_code == 200:
                    result = response.json()
                    message = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                    print(f"   HTTP response: {message}")
                    print("   HTTP test: SUCCESS")
                    return True
                else:
                    print(f"   HTTP test failed: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"   All tests failed: {e}")
        import traceback
        traceback.print_exc()

    return False

if __name__ == "__main__":
    result = asyncio.run(test_direct_zhipu())

    if result:
        print("\n=== Zhipu AI is working! ===")
        print("The issue might be in the toolkit wrapper.")
        print("You can use the toolkit with some modifications.")
    else:
        print("\n=== Zhipu AI connection failed ===")
        print("Please check:")
        print("1. API key is correct and active")
        print("2. Account has sufficient credits")
        print("3. Network connection is stable")
        print("4. API service is available")