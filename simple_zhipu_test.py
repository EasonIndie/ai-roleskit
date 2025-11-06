#!/usr/bin/env python3
"""
简单的智谱API测试
直接测试API连接，避免复杂的代理问题
"""

import os
import asyncio
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

async def test_zhipu_direct():
    """直接测试智谱API"""
    print("=== 智谱API直接测试 ===")

    # 获取API密钥
    api_key = os.getenv('ZHIPU_API_KEY')
    if not api_key or api_key == 'your_zhipu_api_key_here':
        print("请先在.env文件中配置ZHIPU_API_KEY")
        return False

    try:
        # 方法1: 尝试使用zai-sdk
        try:
            print("尝试使用zai-sdk...")
            from zai import ZhipuAiClient

            # 创建客户端，使用基本配置
            client = ZhipuAiClient(api_key=api_key)

            # 发送测试请求
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: client.chat.completions.create(
                    model="glm-4",
                    messages=[{"role": "user", "content": "你好，请用一句话介绍你自己"}],
                    max_tokens=50
                )
            )

            if response and response.choices:
                content = response.choices[0].message.content
                print(f"✓ 智谱API响应成功: {content}")
                return True
            else:
                print("✗ 智谱API响应为空")
                return False

        except ImportError as e:
            print(f"✗ zai-sdk导入失败: {e}")
            return False
        except Exception as e:
            print(f"✗ zai-sdk测试失败: {e}")

            # 方法2: 尝试直接HTTP请求
            try:
                print("尝试直接HTTP请求...")
                import httpx

                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }

                data = {
                    "model": "glm-4",
                    "messages": [{"role": "user", "content": "你好"}],
                    "max_tokens": 50
                }

                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        "https://open.bigmodel.cn/api/paas/v4/chat/completions",
                        headers=headers,
                        json=data
                    )

                    if response.status_code == 200:
                        result = response.json()
                        if "choices" in result and result["choices"]:
                            content = result["choices"][0]["message"]["content"]
                            print(f"✓ 直接HTTP请求成功: {content}")
                            return True
                        else:
                            print("✗ 响应格式异常")
                            return False
                    else:
                        print(f"✗ HTTP请求失败: {response.status_code} - {response.text}")
                        return False

            except Exception as http_error:
                print(f"✗ 直接HTTP请求失败: {http_error}")
                return False

    except Exception as e:
        print(f"✗ 所有测试方法都失败: {e}")
        return False


def check_environment():
    """检查环境配置"""
    print("=== 环境检查 ===")

    # 检查API密钥
    api_key = os.getenv('ZHIPU_API_KEY')
    if api_key:
        if api_key == 'your_zhipu_api_key_here':
            print("FAIL: API密钥未配置，请设置真实的智谱API密钥")
            return False
        else:
            print(f"PASS: API密钥已配置: {api_key[:10]}...")
            return True
    else:
        print("FAIL: 未找到ZHIPU_API_KEY环境变量")
        return False


def test_network():
    """测试网络连接"""
    print("\n=== 网络连接测试 ===")

    try:
        import httpx

        # 测试基础连接
        response = httpx.get("https://www.baidu.com", timeout=10)
        if response.status_code == 200:
            print("PASS: 基础网络连接正常")

            # 测试智谱API连接
            try:
                response = httpx.get("https://open.bigmodel.cn", timeout=10)
                print("✓ 智谱API域名可访问")
                return True
            except Exception as e:
                print(f"✗ 智谱API域名无法访问: {e}")
                return False
        else:
            print("✗ 基础网络连接失败")
            return False

    except Exception as e:
        print(f"✗ 网络测试失败: {e}")
        return False


def suggest_solutions():
    """提供解决方案建议"""
    print("\n=== 解决方案建议 ===")
    print("如果测试失败，请尝试以下解决方案：")
    print("1. 检查API密钥是否正确")
    print("2. 检查网络连接和防火墙设置")
    print("3. 关闭系统代理或VPN")
    print("4. 重新安装zai-sdk: pip uninstall zai-sdk && pip install zai-sdk")
    print("5. 检查智谱API余额和配额")


async def main():
    """主函数"""
    print("智谱API简单测试")
    print("=" * 40)

    # 环境检查
    if not check_environment():
        suggest_solutions()
        return

    # 网络检查
    if not test_network():
        suggest_solutions()
        return

    # API测试
    success = await test_zhipu_direct()

    if success:
        print("\n🎉 智谱API配置成功！")
        print("你可以开始使用智谱大模型了。")
        print("\n下一步:")
        print("1. 运行: python demo.py")
        print("2. 或运行: python cli.py --provider zhipu")
    else:
        print("\n❌ 智谱API配置失败")
        suggest_solutions()


if __name__ == "__main__":
    asyncio.run(main())