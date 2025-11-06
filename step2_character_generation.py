#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
步骤2：角色生成功能演示
基于探索结果生成用户、专家、组织三个角色
"""

import asyncio
import sys
import os
sys.path.insert(0, './src')

# 确保配置重新加载
if 'ai_toolkit.utils.config' in sys.modules:
    del sys.modules['ai_toolkit.utils.config']

from ai_toolkit.utils.config import config
from ai_toolkit.ai.zhipu_provider import ZhipuProvider
from ai_toolkit.core.character import CharacterManager
from ai_toolkit.core.exploration import CreativeExplorer
from ai_toolkit.models.schemas import CharacterType
from ai_toolkit.storage.file_storage import FileStorage

async def character_generation_demo():
    """演示角色生成功能"""
    print("=== 步骤2：角色生成功能演示 ===")
    print("基于刚才的探索结果生成三个角色")

    try:
        # 1. 初始化系统
        print("\n1.1 初始化角色生成系统...")
        config.load_config()
        zhipu_config = config.get_zhipu_config()
        provider = ZhipuProvider(zhipu_config)
        await provider.initialize()

        character_manager = CharacterManager(provider)
        explorer = CreativeExplorer(provider)
        storage = FileStorage()

        print("   角色生成系统初始化成功！")

        # 2. 获取之前的探索结果
        print("\n2.1 获取探索会话...")
        # 使用之前的会话ID，如果不可用则创建新的
        session_id = "132b9321-a12c-44c1-929d-317fd5620e5f"

        try:
            # 尝试加载之前的会话
            session = await storage.get_exploration(session_id)
            if session:
                print(f"   成功加载探索会话: {session_id[:8]}...")
            else:
                # 如果加载失败，创建新会话
                print("   之前的会话不可用，创建新的探索会话...")
                session = await explorer.start_exploration("开发一个AI辅助学习编程的移动应用")
                session_id = session.id
                print(f"   新会话ID: {session_id[:8]}...")
        except:
            # 完全创建新会话
            print("   创建新的探索会话...")
            session = await explorer.start_exploration("开发一个AI辅助学习编程的移动应用")
            session_id = session.id
            print(f"   新会话ID: {session_id[:8]}...")

        # 3. 获取探索摘要
        print("\n3.1 生成探索摘要...")
        summary = await explorer.get_exploration_summary(session_id)
        print(f"   探索准备度: {summary['character_generation_readiness']}")

        # 4. 生成用户角色
        print("\n4.1 生成用户角色...")
        user_character = await character_manager.create_character(
            summary, CharacterType.USER, "编程学习者小李"
        )
        print(f"   用户角色创建成功!")
        print(f"   - 姓名: {user_character.name}")
        print(f"   - 类型: {user_character.type.value}")
        print(f"   - 描述: {user_character.description}")
        print(f"   - ID: {user_character.id}")

        # 5. 生成专家角色
        print("\n5.1 生成专家角色...")
        expert_character = await character_manager.create_character(
            summary, CharacterType.EXPERT, "AI教育专家王老师"
        )
        print(f"   专家角色创建成功!")
        print(f"   - 姓名: {expert_character.name}")
        print(f"   - 类型: {expert_character.type.value}")
        print(f"   - 描述: {expert_character.description}")
        print(f"   - ID: {expert_character.id}")

        # 6. 生成组织角色
        print("\n6.1 生成组织角色...")
        org_character = await character_manager.create_character(
            summary, CharacterType.ORGANIZATION, "教育科技公司产品经理"
        )
        print(f"   组织角色创建成功!")
        print(f"   - 姓名: {org_character.name}")
        print(f"   - 类型: {org_character.type.value}")
        print(f"   - 描述: {org_character.description}")
        print(f"   - ID: {org_character.id}")

        # 7. 保存角色到存储
        print("\n7.1 保存角色数据...")
        await storage.save_character(user_character)
        await storage.save_character(expert_character)
        await storage.save_character(org_character)
        print("   所有角色已保存到存储系统")

        # 8. 显示角色详细信息
        print("\n8.1 角色详细信息展示...")

        print("\n--- 用户角色详情 ---")
        print(f"姓名: {user_character.name}")
        print(f"背景: {user_character.info.background if user_character.info else '未设置'}")
        print(f"目标: {user_character.context.goals if user_character.context else '未设置'}")
        print(f"技能: {user_character.expertise.special_skills if user_character.expertise else '未设置'}")

        print("\n--- 专家角色详情 ---")
        print(f"姓名: {expert_character.name}")
        print(f"专业领域: {expert_character.info.position if expert_character.info else '未设置'}")
        print(f"经验: {expert_character.info.experience if expert_character.info else '未设置'}")
        print(f"专业能力: {expert_character.expertise.professional_field if expert_character.expertise else '未设置'}")

        print("\n--- 组织角色详情 ---")
        print(f"姓名: {org_character.name}")
        print(f"组织类型: {org_character.info.position if org_character.info else '未设置'}")
        print(f"商业模式: {org_character.info.experience if org_character.info else '未设置'}")
        print(f"关注重点: {org_character.response.focus_areas if org_character.response else '未设置'}")

        # 9. 更新探索会话
        print("\n9.1 更新探索会话...")
        session.add_character(user_character.id)
        session.add_character(expert_character.id)
        session.add_character(org_character.id)
        await storage.save_exploration(session)
        print("   探索会话已更新，包含生成的角色ID")

        print("\n=== 角色生成演示完成 ===")
        print("成功生成的角色:")
        print(f"   - 用户角色: {user_character.name} ({user_character.id[:8]}...)")
        print(f"   - 专家角色: {expert_character.name} ({expert_character.id[:8]}...)")
        print(f"   - 组织角色: {org_character.name} ({org_character.id[:8]}...)")

        return {
            'user': user_character,
            'expert': expert_character,
            'organization': org_character,
            'session_id': session_id
        }

    except Exception as e:
        print(f"\n角色生成过程出错: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if sys.platform == "win32":
        os.system("chcp 65001 > nul")
    os.environ['PYTHONIOENCODING'] = 'utf-8'

    print("AI角色工具包 - 角色生成功能演示")
    print("=" * 50)

    result = asyncio.run(character_generation_demo())

    if result:
        print(f"\n角色生成成功！")
        print(f"你现在可以进入下一步：基础对话测试")
        print(f"已生成3个角色，可以开始与它们对话")
        print(f"角色ID已保存，可用于后续步骤")
    else:
        print(f"\n角色生成失败，请检查错误信息")