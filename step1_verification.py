#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
步骤1验证学习：使用实际代码库完整演示创意探索
用于验证和理解步骤1的所有核心概念
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# 设置编码
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 添加 src 目录到路径
sys.path.insert(0, './src')

# 设置环境变量
os.environ['ZHIPU_API_KEY'] = "31b5715b41cd4e6e8dde08232ec63146.Jjs6gp46gAYsI5sl"
os.environ['ZAI_API_KEY'] = "31b5715b41cd4e6e8dde08232ec63146.Jjs6gp46gAYsI5sl"

async def step1_verification_learning():
    """步骤1验证学习：完整的创意探索流程"""
    print("=" * 70)
    print("AI Character Toolkit - 步骤1验证学习：创意探索功能")
    print("=" * 70)
    print("目标：理解创意探索的作用、流程和数据管理")
    print("想法：'创建一个智能家居控制系统'")

    try:
        # ========== 阶段1：系统初始化和组件理解 ==========
        print("\n" + "="*50)
        print("阶段1：系统初始化和组件理解")
        print("="*50)

        print("\n1.1 导入核心模块...")
        from ai_toolkit.utils.config import config
        from ai_toolkit.ai.zhipu_provider import ZhipuProvider
        from ai_toolkit.core.exploration import CreativeExplorer
        from ai_toolkit.storage.file_storage import FileStorage
        from ai_toolkit.models.schemas import ExplorationSession
        print("   [OK] 成功导入所有核心模块")
        print("   📚 模块说明：")
        print("      - config: 配置管理器")
        print("      - ZhipuProvider: AI对话接口")
        print("      - CreativeExplorer: 创意探索引擎")
        print("      - FileStorage: 数据持久化")
        print("      - ExplorationSession: 探索会话数据模型")

        print("\n1.2 加载系统配置...")
        config.load_config()
        zhipu_config = config.get_zhipu_config()
        print(f"   ✅ 配置加载成功")
        print(f"   🔧 AI模型配置：{zhipu_config['model']}")
        print(f"   🔧 最大Token：{zhipu_config['max_tokens']}")
        print(f"   🔧 API超时：{zhipu_config['timeout']}秒")

        print("\n1.3 初始化系统组件...")
        provider = ZhipuProvider(zhipu_config)
        await provider.initialize()
        explorer = CreativeExplorer(provider)
        storage = FileStorage()
        print("   ✅ 所有组件初始化成功")
        print("   🏗️ 系统架构：Provider → Explorer → Storage")

        # ========== 阶段2：创建探索会话 ==========
        print("\n" + "="*50)
        print("阶段2：创建探索会话")
        print("="*50)

        print("\n2.1 定义初始想法...")
        initial_idea = "创建一个智能家居控制系统"
        print(f"   💡 初始想法：{initial_idea}")

        print("\n2.2 启动创意探索会话...")
        session = await explorer.start_exploration(initial_idea)
        print(f"   ✅ 探索会话创建成功")
        print(f"   🆔 会话ID：{session.id}")
        print(f"   📅 创建时间：{session.created_at}")
        print(f"   📊 会话类型：{type(session).__name__}")
        print(f"   📝 初始想法：{session.initial_idea}")

        # 探索会话的数据结构分析
        print("\n2.3 探索会话数据结构分析...")
        print("   📋 ExplorationSession 包含：")
        print(f"      - id: 唯一标识符")
        print(f"      - initial_idea: 初始想法")
        print(f"      - exploration_data: 探索数据 (当前: {len(session.exploration_data)}项)")
        print(f"      - created_at: 创建时间")
        print(f"      - updated_at: 更新时间")
        print(f"      - stakeholder_analysis: 利益相关者分析")
        print(f"      - character_ids: 关联角色ID列表")

        # ========== 阶段3：AI引导的深度探索 ==========
        print("\n" + "="*50)
        print("阶段3：AI引导的深度探索")
        print("="*50)

        print("\n3.1 设计探索提示...")
        exploration_prompt = """
        作为创意探索专家，请从以下角度深入分析"创建一个智能家居控制系统"这个想法：

        1. 【市场分析】目标用户群体、市场潜力、竞争格局
        2. 【技术可行性】核心技术要求、实现难点、技术趋势
        3. 【用户价值】解决什么问题、用户使用场景、价值主张
        4. 【商业模式】盈利方式、成本结构、收入来源
        5. 【风险评估】主要风险、应对策略、成功要素

        请为每个角度提供详细的分析和建议。
        """
        print("   🎯 探索目标：多角度深度分析")
        print("   📋 分析维度：市场、技术、价值、商业、风险")

        print("\n3.2 执行AI深度探索...")
        print("   🤖 正在调用AI进行分析...")
        result = await explorer.explore_idea(session.id, exploration_prompt)

        print("\n   === AI深度分析结果 ===")
        ai_response = result.get('ai_response', '')
        print(ai_response)

        print(f"\n   📊 分析统计：")
        print(f"      - 响应长度：{len(ai_response)} 字符")
        print(f"      - 会话ID：{result.get('session_id', '')[:8]}...")

        # 分析AI响应的关键特征
        print(f"\n   🔍 AI分析特征分析：")
        lines = ai_response.split('\n')
        sections = [line for line in lines if line.strip().startswith('1.') or line.strip().startswith('2.') or line.strip().startswith('3.') or line.strip().startswith('4.') or line.strip().startswith('5.')]
        print(f"      - 分析维度数量：{len(sections)}")
        print(f"      - 主要分析方向：市场、技术、用户价值、商业模式、风险评估")

        # ========== 阶段4：利益相关者识别 ==========
        print("\n" + "="*50)
        print("阶段4：利益相关者识别")
        print("="*50)

        print("\n4.1 识别关键利益相关者...")
        stakeholders = await explorer.identify_stakeholders(session.id)

        print(f"   ✅ 识别到 {len(stakeholders)} 个利益相关者群体：")
        for i, stakeholder in enumerate(stakeholders, 1):
            print(f"      {i}. {stakeholder.get('description', 'Unknown')}")
            print(f"         类型：{stakeholder.get('type', 'Unknown')}")

        print(f"\n   🎯 利益相关者分析：")
        print(f"      - 识别方法：基于AI分析结果自动提取")
        print(f"      - 作用：为后续角色生成提供基础")
        print(f"      - 类型分布：用户群体、合作伙伴、竞争者等")

        # ========== 阶段5：探索摘要生成 ==========
        print("\n" + "="*50)
        print("阶段5：探索摘要生成")
        print("="*50)

        print("\n5.1 生成探索摘要...")
        summary = await explorer.get_exploration_summary(session.id)

        print("   📋 探索摘要信息：")
        print(f"      - 会话ID：{summary.get('session_id', '')[:8]}...")
        print(f"      - 初始想法：{summary.get('initial_idea', '')}")
        print(f"      - 探索时长：{summary.get('exploration_duration', '')}")
        print(f"      - 角色生成准备度：{summary.get('character_generation_readiness', '')}")
        print(f"      - 关键洞察数量：{len(summary.get('key_insights', []))}")

        print(f"\n   🎯 准备度分析：")
        readiness = summary.get('character_generation_readiness', '')
        print(f"      - 当前状态：{readiness}")
        if readiness == 'sufficient':
            print("      - ✅ 探索充分，可以进行角色生成")
        else:
            print("      - ⚠️ 探索可能不足，建议补充更多分析")

        # ========== 阶段6：数据持久化和验证 ==========
        print("\n" + "="*50)
        print("阶段6：数据持久化和验证")
        print("="*50)

        print("\n6.1 保存探索会话...")
        save_success = await storage.save_exploration(session)
        if save_success:
            print("   ✅ 探索会话保存成功")
        else:
            print("   ❌ 探索会话保存失败")

        print("\n6.2 验证数据保存...")
        loaded_session = await storage.load_exploration(session.id)
        if loaded_session:
            print("   ✅ 数据验证成功")
            print(f"      - 重新加载会话：{loaded_session.id[:8]}...")
            print(f"      - 想法一致性：{loaded_session.initial_idea == initial_idea}")
            print(f"      - 数据完整性：{len(loaded_session.exploration_data)} 项探索数据")
        else:
            print("   ❌ 数据验证失败")

        print("\n6.3 文件系统状态...")
        data_dir = "data"
        if os.path.exists(data_dir):
            print(f"   📁 数据目录：{os.path.abspath(data_dir)}")

            # 检查探索文件
            explorations_dir = os.path.join(data_dir, "explorations")
            if os.path.exists(explorations_dir):
                exploration_files = [f for f in os.listdir(explorations_dir) if f.endswith('.json')]
                print(f"   📄 探索文件数量：{len(exploration_files)}")

                # 找到当前的探索文件
                current_file = os.path.join(explorations_dir, f"{session.id}.json")
                if os.path.exists(current_file):
                    file_size = os.path.getsize(current_file)
                    print(f"   📊 当前会话文件：{session.id[:8]}...json ({file_size} bytes)")

        # ========== 阶段7：系统状态统计 ==========
        print("\n" + "="*50)
        print("阶段7：系统状态统计")
        print("="*50)

        print("\n7.1 存储系统统计...")
        stats = await storage.get_storage_stats()
        print("   📊 存储统计：")
        print(f"      - 总角色数：{stats.get('total_characters', 0)}")
        print(f"      - 存储格式：{stats.get('storage_format', 'unknown')}")
        print(f"      - 存储路径：{stats.get('storage_path', 'unknown')}")
        print(f"      - 总大小：{stats.get('total_size_mb', 0)} MB")

        # ========== 学习总结 ==========
        print("\n" + "="*70)
        print("🎯 步骤1学习总结")
        print("="*70)

        print("\n✅ 创意探索的核心作用：")
        print("   1. 【想法深化】将初步想法转化为多维度深度分析")
        print("   2. 【需求发现】识别用户需求、技术要求、商业机会")
        print("   3. 【风险识别】提前发现潜在风险和挑战")
        print("   4. 【角色基础】为后续角色生成提供丰富的背景信息")

        print("\n✅ 核心组件协作流程：")
        print("   1. ZhipuProvider：提供AI对话能力")
        print("   2. CreativeExplorer：管理探索流程和逻辑")
        print("   3. FileStorage：确保数据持久化和可追溯")

        print("\n✅ 探索会话的数据价值：")
        print("   - 结构化存储探索过程")
        print("   - 支持增量式探索")
        print("   - 为角色生成提供背景")
        print("   - 支持探索历史追溯")

        print(f"\n✅ 当前探索会话状态：")
        print(f"   - 会话ID：{session.id}")
        print(f"   - 初始想法：{initial_idea}")
        print(f"   - AI分析长度：{len(ai_response)} 字符")
        print(f"   - 利益相关者：{len(stakeholders)} 个群体")
        print(f"   - 准备度：{summary.get('character_generation_readiness', '')}")

        print(f"\n🚀 下一步：角色生成")
        print(f"   基于当前探索会话 {session.id[:8]}... 生成用户、专家、组织三个角色")

        return {
            'session': session,
            'ai_analysis': ai_response,
            'stakeholders': stakeholders,
            'summary': summary,
            'storage_stats': stats
        }

    except Exception as e:
        print(f"\n❌ 验证学习过程出错: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("开始步骤1验证学习...")

    result = asyncio.run(step1_verification_learning())

    if result:
        print(f"\n🎉 步骤1验证学习完成！")
        print(f"✅ 你已经理解了创意探索的完整流程")
        print(f"✅ 系统组件和数据流都已验证")
        print(f"✅ 准备进入步骤2：角色生成")
    else:
        print(f"\n❌ 步骤1验证学习失败，请检查错误信息")