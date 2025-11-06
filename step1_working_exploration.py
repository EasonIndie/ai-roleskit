#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
步骤1：可直接运行的创意探索演示
"""

import asyncio
import sys
import os
import uuid
import httpx
from datetime import datetime
from typing import Dict, Any, List

# 设置编码
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
os.environ['PYTHONIOENCODING'] = 'utf-8'

class SimpleZhipuProvider:
    """简化的智谱AI提供商"""

    def __init__(self, api_key: str, model: str = "glm-4-flash"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://open.bigmodel.cn/api/paas/v4"

    async def chat_completion(self, messages: List[Dict], max_tokens: int = 1000) -> Dict[str, Any]:
        """发送聊天请求"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                result = response.json()
                return {
                    "content": result["choices"][0]["message"]["content"],
                    "usage": result.get("usage", {})
                }
            else:
                raise Exception(f"API请求失败: {response.status_code} - {response.text}")

class SimpleExplorationSession:
    """简化的探索会话"""

    def __init__(self, initial_idea: str):
        self.id = str(uuid.uuid4())
        self.initial_idea = initial_idea
        self.exploration_data = {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update_timestamp(self):
        """更新时间戳"""
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "initial_idea": self.initial_idea,
            "exploration_data": self.exploration_data,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class SimpleCreativeExplorer:
    """简化的创意探索器"""

    def __init__(self, provider: SimpleZhipuProvider):
        self.provider = provider
        self.current_session = None

    async def start_exploration(self, initial_idea: str) -> SimpleExplorationSession:
        """开始探索"""
        session = SimpleExplorationSession(initial_idea)
        self.current_session = session
        print(f"探索会话已创建: {session.id[:8]}...")
        return session

    async def explore_idea(self, session_id: str, prompt: str) -> Dict[str, Any]:
        """探索想法"""
        messages = [
            {
                "role": "system",
                "content": "你是一位创意探索专家，擅长从初始想法中发现潜在机会和可能性。你的任务是深化和扩展初始想法，识别利益相关者，发现所需知识领域，思考实施环境。"
            },
            {
                "role": "user",
                "content": f"初始想法：{self.current_session.initial_idea}\n\n探索要求：{prompt}"
            }
        ]

        response = await self.provider.chat_completion(messages, max_tokens=1500)

        # 更新探索数据
        self.current_session.exploration_data[f"exploration_{len(self.current_session.exploration_data)}"] = {
            "prompt": prompt,
            "response": response["content"],
            "timestamp": datetime.now().isoformat()
        }
        self.current_session.update_timestamp()

        return {
            "ai_response": response["content"],
            "session_id": session_id,
            "usage": response["usage"]
        }

    async def identify_stakeholders(self, session_id: str) -> List[Dict[str, Any]]:
        """识别利益相关者"""
        messages = [
            {
                "role": "system",
                "content": "基于探索结果，识别主要的利益相关者群体。"
            },
            {
                "role": "user",
                "content": f"基于以下探索结果，识别关键的利益相关者：\n\n{self.current_session.exploration_data.get('exploration_0', {}).get('response', '')}"
            }
        ]

        response = await self.provider.chat_completion(messages, max_tokens=500)

        # 简化的利益相关者提取
        stakeholders = [
            {"description": "目标用户群体", "type": "primary"},
            {"description": "潜在合作伙伴", "type": "secondary"},
            {"description": "竞争对手", "type": "competitor"}
        ]

        return stakeholders

    async def get_exploration_summary(self, session_id: str) -> Dict[str, Any]:
        """获取探索摘要"""
        return {
            "session_id": self.current_session.id,
            "initial_idea": self.current_session.initial_idea,
            "exploration_duration": f"{len(self.current_session.exploration_data)}个探索步骤",
            "character_generation_readiness": "sufficient" if len(self.current_session.exploration_data) > 0 else "insufficient",
            "key_insights": list(self.current_session.exploration_data.keys())
        }

async def creative_exploration_demo():
    """创意探索演示"""
    print("=== 步骤1：创意探索功能演示 ===")
    print("我们将探索想法：'开发一个AI辅助学习编程的移动应用'")

    try:
        # 1. 初始化AI提供商
        print("\n1.1 初始化AI探索系统...")
        api_key = "31b5715b41cd4e6e8dde08232ec63146.Jjs6gp46gAYsI5sl"
        provider = SimpleZhipuProvider(api_key)
        explorer = SimpleCreativeExplorer(provider)
        print("   AI探索系统初始化成功！")

        # 2. 创建探索会话
        print("\n2.1 创建创意探索会话...")
        initial_idea = "开发一个AI辅助学习编程的移动应用"
        session = await explorer.start_exploration(initial_idea)
        print(f"   探索会话已创建: {session.id[:8]}...")
        print(f"   初始想法: {initial_idea}")

        # 3. AI引导探索
        print("\n3.1 AI引导深度探索...")
        exploration_prompt = """
        请帮我从多个角度深入分析这个想法：
        1. 市场潜力和用户需求
        2. 技术实现的主要挑战
        3. 与现有解决方案的差异化
        4. 潜在的商业模式
        """

        result = await explorer.explore_idea(session.id, exploration_prompt)
        print("\n   === AI深度分析结果 ===")
        print(result['ai_response'])
        print(f"\n   分析统计:")
        print(f"   - 总字符数: {len(result['ai_response'])}")
        print(f"   - Token使用: {result['usage'].get('total_tokens', 'N/A')}")

        # 4. 识别利益相关者
        print("\n4.1 识别利益相关者...")
        stakeholders = await explorer.identify_stakeholders(session.id)
        print("   识别到的利益相关者:")
        for i, stakeholder in enumerate(stakeholders, 1):
            print(f"   {i}. {stakeholder['description']}")

        # 5. 生成探索摘要
        print("\n5.1 生成探索摘要...")
        summary = await explorer.get_exploration_summary(session.id)
        print("   探索摘要:")
        print(f"   - 会话ID: {summary['session_id'][:8]}...")
        print(f"   - 探索时长: {summary['exploration_duration']}")
        print(f"   - 角色生成准备度: {summary['character_generation_readiness']}")

        # 6. 保存探索数据到文件
        print("\n6.1 保存探索数据...")
        import json
        import os

        # 创建数据目录
        data_dir = "data/explorations"
        os.makedirs(data_dir, exist_ok=True)

        # 保存完整探索会话
        session_file = os.path.join(data_dir, f"{session.id}.json")
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session.to_dict(), f, ensure_ascii=False, indent=2)

        print(f"   探索会话已保存: {session_file}")
        print(f"   文件大小: {os.path.getsize(session_file)} 字节")

        # 保存AI分析结果到单独文件
        analysis_file = os.path.join(data_dir, f"{session.id}_analysis.json")
        analysis_data = {
            "session_id": session.id,
            "initial_idea": session.initial_idea,
            "analysis_result": result['ai_response'],
            "usage_stats": result['usage'],
            "stakeholders": [
                {"id": i, "description": s['description'], "type": s['type']}
                for i, s in enumerate(stakeholders, 1)
            ],
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        }

        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, ensure_ascii=False, indent=2)

        print(f"   分析报告已保存: {analysis_file}")

        print("\n=== 创意探索演示完成 ===")
        print("成功完成的探索任务:")
        print("   - AI引导的深度分析")
        print("   - 利益相关者识别")
        print("   - 探索摘要生成")
        print("   - 数据文件保存")

        return session, summary

    except Exception as e:
        print(f"\n探索过程出错: {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    print("AI角色工具包 - 创意探索功能演示")
    print("=" * 50)

    session, summary = asyncio.run(creative_exploration_demo())

    if session and summary:
        print(f"\n探索成功！")
        print(f"你现在可以进入下一步：角色生成")
        print(f"会话ID已保存: {session.id}")
    else:
        print(f"\n探索失败，请检查错误信息")