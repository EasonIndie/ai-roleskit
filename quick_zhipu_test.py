#!/usr/bin/env python3
"""
快速智谱API测试
"""

import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def test_zhipu():
    """测试智谱API"""
    api_key = os.getenv('ZHIPU_API_KEY')

    if not api_key or api_key == 'your_zhipu_api_key_here':
        print("ERROR: Please configure ZHIPU_API_KEY in .env file")
        return False

    print(f"API Key: {api_key[:10]}...")

    try:
        # 直接HTTP测试
        import httpx

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "glm-4",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 50
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://open.bigmodel.cn/api/paas/v4/chat/completions",
                headers=headers,
                json=data
            )

            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                if "choices" in result:
                    content = result["choices"][0]["message"]["content"]
                    print(f"SUCCESS: {content}")
                    return True
                else:
                    print("ERROR: Invalid response format")
                    return False
            else:
                print(f"ERROR: {response.text}")
                return False

    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_zhipu())
    if success:
        print("Zhipu API is working!")
    else:
        print("Zhipu API test failed")