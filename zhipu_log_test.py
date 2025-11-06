#!/usr/bin/env python3
"""
智谱AI日志测试脚本
展示完整的日志输出和调试信息
"""

import asyncio
import sys
import os
import logging
sys.path.insert(0, './src')

from dotenv import load_dotenv

load_dotenv()

# 设置日志级别以查看更多详细信息
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_with_detailed_logs():
    """测试带有详细日志输出的智谱功能"""
    print("=== 智谱AI详细日志测试 ===")

    api_key = os.getenv('ZHIPU_API_KEY')
    if not api_key:
        print("ERROR: ZHIPU_API_KEY not configured")
        return False

    print(f"API Key: {api_key[:10]}...")

    try:
        # 导入模块（会显示导入日志）
        print("\n1. 导入智谱模块...")
        from ai_toolkit.ai.zhipu_provider import ZhipuProvider
        from ai_toolkit.models.schemas import Character, CharacterInfo, CharacterType
        from ai_toolkit.ai.base import AIRequest
        print("SUCCESS: 模块导入完成")

        # 创建Provider（会显示初始化日志）
        print("\n2. 创建智谱Provider...")
        config = {
            'api_key': api_key,
            'model': 'glm-4',
            'max_tokens': 800,
            'temperature': 0.7,
            'timeout': 30
        }

        provider = ZhipuProvider(config)
        print("SUCCESS: Provider对象创建完成")

        # 初始化Provider（会显示连接日志）
        print("\n3. 初始化Provider...")
        await provider.initialize()
        print("SUCCESS: Provider初始化完成")

        # 显示可用模型（会显示模型加载日志）
        print("\n4. 检查可用模型...")
        models = provider._load_models()
        print(f"可用模型数量: {len(models)}")
        for model in models:
            print(f"  - {model.name}: max_tokens={model.max_tokens}")

        # 创建角色
        print("\n5. 创建AI角色...")
        character_info = CharacterInfo(
            name="智谱技术专家",
            position="AI研发工程师",
            experience="5年大模型开发和应用经验"
        )

        character = Character(
            name="智谱技术专家",
            type=CharacterType.EXPERT,
            description="专注于智谱大模型技术应用的专家",
            info=character_info
        )
        print(f"SUCCESS: 角色创建完成 - {character.name}")

        # 测试对话（会显示请求/响应日志）
        print("\n6. 测试对话功能...")
        questions = [
            "智谱大模型的核心优势是什么？",
            "如何优化大模型的推理性能？"
        ]

        for i, question in enumerate(questions, 1):
            print(f"\n  对话 {i}:")
            print(f"  问题: {question}")

            # 构建请求
            request = AIRequest(
                messages=[
                    {
                        "role": "system",
                        "content": f"你是{character.name}，{character.description}。{character.info.experience}。请用专业的技术语调回答问题。"
                    },
                    {"role": "user", "content": question}
                ],
                max_tokens=300,
                temperature=0.7
            )

            # 发送请求（会显示API调用日志）
            print(f"  发送请求...")
            response = await provider.chat_completion(request)

            # 显示响应信息
            print(f"  角色回复: {response.content[:100]}...")
            if response.usage:
                print(f"  Token使用: {response.usage}")
            if response.metadata:
                print(f"  元数据: {response.metadata}")

        print("\n=== 所有测试完成 ===")
        return True

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_streaming_with_logs():
    """测试流式对话的日志输出"""
    print("\n=== 流式对话日志测试 ===")

    try:
        from ai_toolkit.ai.zhipu_provider import ZhipuProvider
        from ai_toolkit.ai.base import AIRequest

        api_key = os.getenv('ZHIPU_API_KEY')
        config = {
            'api_key': api_key,
            'model': 'glm-4',
            'max_tokens': 400,
            'temperature': 0.8
        }

        provider = ZhipuProvider(config)
        await provider.initialize()

        print("开始流式对话测试...")

        request = AIRequest(
            messages=[
                {"role": "user", "content": "请简要介绍一下智谱AI的发展历程"}
            ],
            stream=True
        )

        print("流式回复: ", end="", flush=True)

        word_count = 0
        async for chunk in provider.chat_completion_stream(request):
            print(chunk, end="", flush=True)
            word_count += 1
            if word_count % 20 == 0:
                print(f"\n[已输出{word_count}个词] ", end="", flush=True)

        print(f"\n\n流式对话完成，总共约{word_count}个词")
        return True

    except Exception as e:
        print(f"流式对话测试失败: {e}")
        return False

def show_log_file_info():
    """显示日志文件信息"""
    print("\n=== 日志文件信息 ===")

    # 检查data目录
    if os.path.exists('./data'):
        print("✓ data目录存在")
        log_files = [f for f in os.listdir('./data') if f.endswith('.log')]
        if log_files:
            print(f"日志文件: {log_files}")
        else:
            print("暂无日志文件")
    else:
        print("✗ data目录不存在")

async def main():
    """主函数"""
    print("智谱AI完整日志测试")
    print("=" * 50)

    # 基本功能测试
    success1 = await test_with_detailed_logs()

    # 流式对话测试
    success2 = await test_streaming_with_logs()

    # 显示日志信息
    show_log_file_info()

    # 总结
    print("\n" + "=" * 50)
    print("测试总结:")
    print(f"基本功能: {'PASS' if success1 else 'FAIL'}")
    print(f"流式对话: {'PASS' if success2 else 'FAIL'}")

    if success1 and success2:
        print("\n🎉 所有测试通过！智谱AI集成成功！")
        print("\n日志功能说明:")
        print("- DEBUG级别日志显示详细的执行过程")
        print("- INFO级别日志显示关键操作结果")
        print("- ERROR级别日志显示错误信息")
        print("\n你可以:")
        print("1. 查看上面详细的日志输出")
        print("2. 使用智谱AI创建角色和对话")
        print("3. 运行: python cli.py --provider zhipu")
    else:
        print("\n❌ 部分测试失败，请检查配置")

if __name__ == "__main__":
    asyncio.run(main())