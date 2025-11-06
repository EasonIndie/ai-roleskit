#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
步骤1简化验证学习：使用实际代码库完整演示创意探索
"""

import asyncio
import sys
import os
import json

# 设置编码
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 添加 src 目录到路径
sys.path.insert(0, './src')

# 设置环境变量
os.environ['ZHIPU_API_KEY'] = "31b5715b41cd4e6e8dde08232ec63146.Jjs6gp46gAYsI5sl"
os.environ['ZAI_API_KEY'] = "31b5715b41cd4e6e8dde08232ec63146.Jjs6gp46gAYsI5sl"

async def step1_simple_verification():
    """步骤1简化验证学习"""
    print("=" * 70)
    print("AI Character Toolkit - 步骤1验证学习：创意探索功能")
    print("=" * 70)
    print("目标：理解创意探索的作用、流程和数据管理")
    print("想法：'创建一个智能家居控制系统'")

    try:
        # 阶段1：系统初始化
        print("\n阶段1：系统初始化")
        print("-" * 30)

        print("\n1.1 导入核心模块...")
        from ai_toolkit.utils.config import config
        from ai_toolkit.ai.zhipu_provider import ZhipuProvider
        from ai_toolkit.core.exploration import CreativeExplorer
        from ai_toolkit.storage.file_storage import FileStorage
        print("   [OK] 成功导入所有核心模块")

        print("\n1.2 加载系统配置...")
        config.load_config()
        zhipu_config = config.get_zhipu_config()
        print(f"   [OK] 配置加载成功，模型：{zhipu_config['model']}")

        print("\n1.3 初始化系统组件...")
        provider = ZhipuProvider(zhipu_config)
        await provider.initialize()
        explorer = CreativeExplorer(provider)
        storage = FileStorage()
        print("   [OK] 所有组件初始化成功")

        # 阶段2：创建探索会话
        print("\n阶段2：创建探索会话")
        print("-" * 30)

        print("\n2.1 定义初始想法...")
        initial_idea = "创建一个智能家居控制系统"
        print(f"   初始想法：{initial_idea}")

        print("\n2.2 启动创意探索会话...")
        session = await explorer.start_exploration(initial_idea)
        print(f"   [OK] 探索会话创建成功")
        print(f"   会话ID：{session.id[:8]}...")
        print(f"   会话类型：{type(session).__name__}")

        print("\n2.3 探索会话数据结构分析...")
        print(f"   ExplorationSession 包含：")
        print(f"      - id: {session.id}")
        print(f"      - initial_idea: {session.initial_idea}")
        print(f"      - exploration_data: {len(session.exploration_data)} 项")
        print(f"      - created_at: {session.created_at}")

        # 阶段3：AI引导的深度探索
        print("\n阶段3：AI引导的深度探索")
        print("-" * 30)

        print("\n3.1 设计探索提示...")
        exploration_prompt = """
        作为创意探索专家，请从以下角度深入分析"创建一个智能家居控制系统"这个想法：

        1. 市场分析：目标用户群体、市场潜力、竞争格局
        2. 技术可行性：核心技术要求、实现难点、技术趋势
        3. 用户价值：解决什么问题、用户使用场景、价值主张
        4. 商业模式：盈利方式、成本结构、收入来源
        5. 风险评估：主要风险、应对策略、成功要素

        请为每个角度提供详细的分析和建议。
        """
        print("   探索目标：多角度深度分析")
        print("   分析维度：市场、技术、价值、商业、风险")

        print("\n3.2 执行AI深度探索...")
        print("   正在调用AI进行分析...")
        result = await explorer.explore_idea(session.id, exploration_prompt)

        print("\n   === AI深度分析结果 ===")
        ai_response = result.get('ai_response', '')
        print(ai_response)

        print(f"\n   分析统计：")
        print(f"      - 响应长度：{len(ai_response)} 字符")
        print(f"      - 会话ID：{result.get('session_id', '')[:8]}...")

        # 阶段4：利益相关者识别
        print("\n阶段4：利益相关者识别")
        print("-" * 30)

        print("\n4.1 识别关键利益相关者...")
        stakeholders = await explorer.identify_stakeholders(session.id)

        print(f"   识别到 {len(stakeholders)} 个利益相关者群体：")
        for i, stakeholder in enumerate(stakeholders, 1):
            print(f"      {i}. {stakeholder.get('description', 'Unknown')}")
            print(f"         类型：{stakeholder.get('type', 'Unknown')}")

        # 阶段5：探索摘要生成
        print("\n阶段5：探索摘要生成")
        print("-" * 30)

        print("\n5.1 生成探索摘要...")
        summary = await explorer.get_exploration_summary(session.id)

        print("   探索摘要信息：")
        print(f"      - 会话ID：{summary.get('session_id', '')[:8]}...")
        print(f"      - 初始想法：{summary.get('initial_idea', '')}")
        print(f"      - 探索时长：{summary.get('exploration_duration', '')}")
        print(f"      - 角色生成准备度：{summary.get('character_generation_readiness', '')}")

        readiness = summary.get('character_generation_readiness', '')
        print(f"      - 准备度状态：{readiness}")
        if readiness == 'sufficient':
            print("      - 状态：探索充分，可以进行角色生成")
        else:
            print("      - 状态：探索可能不足，建议补充更多分析")

        # 阶段6：数据持久化和验证
        print("\n阶段6：数据持久化和验证")
        print("-" * 30)

        print("\n6.1 保存探索会话...")
        save_success = await storage.save_exploration(session)
        if save_success:
            print("   [OK] 探索会话保存成功")
        else:
            print("   [ERROR] 探索会话保存失败")

        print("\n6.2 验证数据保存...")
        loaded_session = await storage.load_exploration(session.id)
        if loaded_session:
            print("   [OK] 数据验证成功")
            print(f"      - 重新加载会话：{loaded_session.id[:8]}...")
            print(f"      - 想法一致性：{loaded_session.initial_idea == initial_idea}")
            print(f"      - 数据完整性：{len(loaded_session.exploration_data)} 项探索数据")
        else:
            print("   [ERROR] 数据验证失败")

        print("\n6.3 文件系统状态...")
        data_dir = "data"
        if os.path.exists(data_dir):
            print(f"   数据目录：{os.path.abspath(data_dir)}")

            explorations_dir = os.path.join(data_dir, "explorations")
            if os.path.exists(explorations_dir):
                exploration_files = [f for f in os.listdir(explorations_dir) if f.endswith('.json')]
                print(f"   探索文件数量：{len(exploration_files)}")

        # 学习总结
        print("\n" + "="*70)
        print("步骤1学习总结")
        print("="*70)

        print("\n创意探索的核心作用：")
        print("   1. 想法深化：将初步想法转化为多维度深度分析")
        print("   2. 需求发现：识别用户需求、技术要求、商业机会")
        print("   3. 风险识别：提前发现潜在风险和挑战")
        print("   4. 角色基础：为后续角色生成提供丰富的背景信息")

        print("\n核心组件协作流程：")
        print("   1. ZhipuProvider：提供AI对话能力")
        print("   2. CreativeExplorer：管理探索流程和逻辑")
        print("   3. FileStorage：确保数据持久化和可追溯")

        print("\n探索会话的数据价值：")
        print("   - 结构化存储探索过程")
        print("   - 支持增量式探索")
        print("   - 为角色生成提供背景")
        print("   - 支持探索历史追溯")

        print(f"\n当前探索会话状态：")
        print(f"   - 会话ID：{session.id[:8]}...")
        print(f"   - 初始想法：{initial_idea}")
        print(f"   - AI分析长度：{len(ai_response)} 字符")
        print(f"   - 利益相关者：{len(stakeholders)} 个群体")
        print(f"   - 准备度：{readiness}")

        print(f"\n下一步：角色生成")
        print(f"   基于当前探索会话生成用户、专家、组织三个角色")

        return {
            'session': session,
            'ai_analysis': ai_response,
            'stakeholders': stakeholders,
            'summary': summary
        }

    except Exception as e:
        print(f"\n[ERROR] 验证学习过程出错: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("开始步骤1验证学习...")

    result = asyncio.run(step1_simple_verification())

    if result:
        print(f"\n[SUCCESS] 步骤1验证学习完成！")
        print(f"你已经理解了创意探索的完整流程")
        print(f"系统组件和数据流都已验证")
        print(f"准备进入步骤2：角色生成")
    else:
        print(f"\n[ERROR] 步骤1验证学习失败，请检查错误信息")