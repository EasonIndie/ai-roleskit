#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
想法深度探讨演示
输入一个想法，生成三个角色，进行深度讨论，收集有用内容
使用现有代码库的角色生成和对话功能
"""

import asyncio
import sys
import os
from datetime import datetime

# 设置编码
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 添加 src 目录到路径
sys.path.insert(0, './src')

# 设置环境变量
os.environ['ZHIPU_API_KEY'] = "31b5715b41cd4e6e8dde08232ec63146.Jjs6gp46gAYsI5sl"

def print_header(title):
    """打印标题"""
    print("=" * 80)
    print(f" {title}")
    print("=" * 80)

def print_section(title):
    """打印章节"""
    print(f"\n{title}")
    print("-" * 50)

async def create_simple_character(provider, exploration_summary, char_type_name, position, description):
    """创建简单角色，避免复杂的模板依赖"""
    from ai_toolkit.models.schemas import Character, CharacterType, CharacterInfo, CharacterContext, CharacterExpertise, CharacterBehavior, CharacterResponse
    import uuid

    # 映射字符类型
    type_map = {
        "用户": CharacterType.USER,
        "专家": CharacterType.EXPERT,
        "组织": CharacterType.ORGANIZATION
    }
    char_type = type_map.get(char_type_name, CharacterType.USER)

    # 创建角色
    character = Character(
        name=f"{char_type_name}角色",
        type=char_type,
        description=description,
        info=CharacterInfo(
            name=f"{char_type_name}角色",
            age="30-40岁",
            position=position,
            background=description,
            experience="5年以上相关经验"
        ),
        context=CharacterContext(
            current_situation="正在评估软著申请工具的可行性",
            goals="找到高效、可靠的软著申请解决方案",
            challenges="软著申请流程复杂，时间成本高",
            resource_constraints="时间和预算有限"
        ),
        expertise=CharacterExpertise(
            professional_field="软件著作权" if char_type_name != "用户" else "软件开发",
            special_skills="专业知识分析" if char_type_name == "专家" else "实际需求理解",
            experience_level="资深专家" if char_type_name == "专家" else "经验丰富",
            industry_insights="深入了解行业痛点和发展趋势"
        ),
        behavior=CharacterBehavior(
            decision_style="分析型" if char_type_name == "专家" else "实用型",
            risk_preference="谨慎" if char_type_name == "组织" else "开放",
            communication_style="专业" if char_type_name == "专家" else "直接",
            values="专业、高效、创新"
        ),
        response=CharacterResponse(
            focus_areas="实用性、可行性、合规性",
            avoidance_areas="不切实际的承诺",
            expression_style="专业、清晰、建设性",
            expected_outcomes="有价值的见解和建议"
        ),
        tags=[char_type_name.lower(), "generated"],
        metadata={
            'generation_method': 'simple_direct',
            'exploration_summary': exploration_summary,
            'generation_time': datetime.now().isoformat()
        }
    )

    return character

async def generate_three_characters(idea):
    """基于想法生成三个角色"""
    print_section("1. 基于想法生成三个角色")
    print(f"输入想法: {idea}")

    from ai_toolkit.utils.config import config
    from ai_toolkit.ai.zhipu_provider import ZhipuProvider
    from ai_toolkit.core.character import CharacterManager
    from ai_toolkit.models.schemas import CharacterType

    config.load_config()
    provider = ZhipuProvider(config.get_zhipu_config())
    await provider.initialize()

    character_manager = CharacterManager(provider)

    # 创建探索摘要（用于角色生成）
    exploration_summary = {
        'initial_idea': idea,
        'key_insights': [
            "解决软著申请的复杂流程",
            "服务中小公司和个人开发者",
            "自动化文档生成",
            "提高申请效率"
        ],
        'stakeholders': [
            {'type': 'user', 'description': '需要申请软著的开发者'},
            {'type': 'expert', 'description': '知识产权专家'},
            {'type': 'organization', 'description': '技术服务提供商'}
        ],
        'knowledge_areas': [
            {'area': '软件著作权', 'importance': 'high'},
            {'area': '文档生成', 'importance': 'medium'},
            {'area': '法律合规', 'importance': 'high'}
        ],
        'implementation_context': {
            'organization_type': '科技公司',
            'resource_level': '中等',
            'complexity': '中等偏上'
        }
    }

    print("   正在生成角色...")

    try:
        # 直接生成角色而不依赖复杂模板系统
        print("   生成用户角色...")
        user_character = await create_simple_character(provider, exploration_summary, "用户", "软件开发者", "需要申请软著的个人开发者")
        await character_manager.add_character(user_character)
        print(f"   [OK] 用户角色生成完成: {user_character.name}")

        await asyncio.sleep(3)

        print("   生成专家角色...")
        expert_character = await create_simple_character(provider, exploration_summary, "专家", "知识产权专家", "专业的软件著作权申请顾问")
        await character_manager.add_character(expert_character)
        print(f"   [OK] 专家角色生成完成: {expert_character.name}")

        await asyncio.sleep(3)

        print("   生成组织角色...")
        org_character = await create_simple_character(provider, exploration_summary, "组织", "技术公司经理", "提供软著申请服务的技术公司管理者")
        await character_manager.add_character(org_character)
        print(f"   [OK] 组织角色生成完成: {org_character.name}")

        print(f"\n   [OK] 三个角色生成完成:")
        print(f"   - 用户: {user_character.name} ({user_character.info.position})")
        print(f"   - 专家: {expert_character.name} ({expert_character.info.position})")
        print(f"   - 组织: {org_character.name} ({org_character.info.position})")

        return user_character, expert_character, org_character, character_manager

    except Exception as e:
        print(f"   [ERROR] 角色生成失败: {e}")
        raise

async def conduct_discussion(characters, discussion_questions, character_manager):
    """进行角色深度讨论"""
    print_section("2. 角色深度讨论")

    from ai_toolkit.core.dialogue import DialogueManager

    dialogue_manager = DialogueManager(character_manager.ai_provider, character_manager)
    discussion_results = []

    # 为每个角色创建对话并讨论问题
    for i, question in enumerate(discussion_questions, 1):
        print(f"\n   讨论问题 {i}: {question}")
        print("-" * 50)

        question_results = {}

        for character in characters:
            char_name = character.name
            char_type = character.type.value

            # 创建对话
            dialogue = await dialogue_manager.create_dialogue(
                character.id,
                f"关于软著工具的讨论 - {char_name}"
            )

            print(f"   {char_name} 正在回答...")

            try:
                # 发送消息并获取回复
                response = await dialogue_manager.send_message(dialogue.id, question)

                question_results[char_name] = {
                    "answer": response.content,
                    "character_type": char_type,
                    "character": character,
                    "question": question,
                    "dialogue_id": dialogue.id
                }

                print(f"   [OK] {char_name} 回答完成 (长度: {len(response.content)} 字符)")

            except Exception as e:
                print(f"   [ERROR] {char_name} 回答失败: {e}")
                question_results[char_name] = {
                    "answer": f"抱歉，{char_name}暂时无法回答这个问题。",
                    "character_type": char_type,
                    "character": character,
                    "question": question,
                    "error": str(e)
                }

            # 避免API频率限制
            if character != characters[-1]:
                await asyncio.sleep(3)

        discussion_results.append(question_results)

    print(f"\n   [OK] 所有讨论完成，共 {len(discussion_questions)} 个问题")
    return discussion_results, dialogue_manager

def extract_useful_insights(discussion_results):
    """提取有用见解"""
    print_section("3. 提取有用见解")

    insights = {
        "common_themes": [],
        "unique_perspectives": {},
        "actionable_items": [],
        "key_findings": []
    }

    # 提取共同主题
    all_text = []
    for question_result in discussion_results:
        for char_name, result in question_result.items():
            all_text.append(result['answer'])

    # 简单的关键词分析
    keywords = ['自动化', '效率', '成本', '时间', '质量', '法律', '合规', '用户体验', '技术创新', '市场需求']
    keyword_counts = {}

    for keyword in keywords:
        count = sum(1 for text in all_text if keyword in text)
        if count >= 2:  # 至少两个角色提到
            keyword_counts[keyword] = count

    insights['common_themes'] = keyword_counts

    # 提取每个角色的独特观点
    for question_result in discussion_results:
        for char_name, result in question_result.items():
            char_type = result['character_type']
            if char_type not in insights['unique_perspectives']:
                insights['unique_perspectives'][char_type] = []

            insights['unique_perspectives'][char_type].append({
                'question': result['question'],
                'answer': result['answer'][:200] + "..." if len(result['answer']) > 200 else result['answer'],
                'character_name': char_name
            })

    # 提取关键发现
    insights['key_findings'] = [
        f"共同主题: {', '.join(insights['common_themes'].keys())}",
        f"参与角色: {len(set(result['character_type'] for qr in discussion_results for result in qr.values()))} 个类型",
        f"总讨论长度: {sum(len(result['answer']) for qr in discussion_results for result in qr.values())} 字符"
    ]

    print(f"   [OK] 提取完成:")
    print(f"   - 共同主题: {len(insights['common_themes'])} 个")
    print(f"   - 独特观点: {len(insights['unique_perspectives'])} 个角色")

    return insights

def save_discussion_results(idea, characters, discussion_results, insights):
    """保存讨论结果"""
    print_section("4. 保存讨论结果")

    # 确保数据目录存在
    import os
    import json
    data_dir = "data"
    discussions_dir = os.path.join(data_dir, "discussions")
    os.makedirs(discussions_dir, exist_ok=True)
    print(f"   [DEBUG] 确保目录存在: {discussions_dir}")

    # 保存角色数据到 characters 子目录
    characters_dir = os.path.join(data_dir, "characters")
    os.makedirs(characters_dir, exist_ok=True)

    try:
        # 保存角色数据
        for character in characters:
            char_filename = f"{character.type.value}_{character.id}.json"
            char_filepath = os.path.join(characters_dir, char_filename)

            char_data = {
                "id": character.id,
                "name": character.name,
                "type": character.type.value,
                "description": character.description,
                "info": character.info.__dict__,
                "context": character.context.__dict__,
                "expertise": character.expertise.__dict__,
                "behavior": character.behavior.__dict__,
                "response": character.response.__dict__,
                "tags": character.tags,
                "metadata": character.metadata,
                "created_at": character.created_at.isoformat() if character.created_at else None,
                "updated_at": character.updated_at.isoformat() if character.updated_at else None
            }

            with open(char_filepath, 'w', encoding='utf-8') as f:
                json.dump(char_data, f, ensure_ascii=False, indent=2)
            print(f"   [OK] 角色数据已保存: {char_filepath}")

        # 保存讨论数据
        filename = f"discussion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(discussions_dir, filename)

        discussion_data = {
            "timestamp": datetime.now().isoformat(),
            "idea": idea,
            "characters": [
                {
                    "id": char.id,
                    "name": char.name,
                    "type": char.type.value,
                    "position": char.info.position,
                    "description": char.description
                } for char in characters
            ],
            "discussion_questions": [next(iter(result.values()))['question'] for result in discussion_results if result],
            "discussion_results": discussion_results,
            "insights": insights,
            "summary": {
                "total_characters": len(characters),
                "total_questions": len(discussion_results),
                "common_themes_count": len(insights['common_themes']),
                "unique_perspectives_count": len(insights['unique_perspectives'])
            }
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(discussion_data, f, ensure_ascii=False, indent=2)

        print(f"   [OK] 讨论结果已保存到: {filepath}")
        return filename

    except Exception as e:
        print(f"   [ERROR] 保存失败: {e}")
        return None

async def main():
    """主函数"""
    print_header("想法深度探讨演示")
    print("输入想法 → 生成三个角色 → 深度讨论 → 收集有用内容")
    print(f"演示时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        # 1. 输入想法
        idea = "我想开发一个自动生成软件著作权的工具，解决中小公司或者个人开发者申请软著的麻烦"

        # 2. 生成三个角色
        characters = await generate_three_characters(idea)

        # 3. 定义讨论问题
        discussion_questions = [
            "对于这个想法，你认为最大的机遇和挑战是什么？",
            "从你的角度，如何确保这个产品的成功？",
            "这个想法需要哪些关键资源和技术支持？"
        ]

        # 4. 进行深度讨论
        user_character, expert_character, org_character, character_manager = characters
        all_characters = [user_character, expert_character, org_character]

        discussion_results, dialogue_manager = await conduct_discussion(
            all_characters, discussion_questions, character_manager
        )

        # 5. 提取有用见解
        insights = extract_useful_insights(discussion_results)

        # 6. 保存结果
        filename = save_discussion_results(idea, all_characters, discussion_results, insights)

        # 7. 总结
        print_header("演示完成总结")
        print(f"想法: {idea}")
        print(f"生成角色: {len(all_characters)} 个")
        print(f"讨论问题: {len(discussion_questions)} 个")
        print(f"讨论记录: {len(discussion_results)} 组")
        print(f"共同主题: {len(insights['common_themes'])} 个")
        print(f"保存文件: {filename}")

        print(f"\n[SUCCESS] 想法深度探讨完成！")
        print(f"   - 成功生成三个不同视角的角色")
        print(f"   - 完成深度讨论，收集了不同观点")
        print(f"   - 提取了共同主题和独特见解")
        print(f"   - 所有结果已保存，可进一步分析")
        print(f"   - 角色数据保存在 data/characters/ 目录")
        print(f"   - 讨论数据保存在 data/discussions/ 目录")

    except Exception as e:
        print(f"\n[ERROR] 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("启动想法深度探讨演示...")
    asyncio.run(main())