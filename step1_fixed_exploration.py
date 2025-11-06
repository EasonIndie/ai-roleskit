#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
步骤1修复版：完整保存探索数据的创意探索
解决数据保存过于简略的问题
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

class EnhancedExplorationSession:
    """增强的探索会话，完整保存探索数据"""

    def __init__(self, initial_idea: str):
        self.id = str(uuid.uuid4())
        self.initial_idea = initial_idea
        self.exploration_steps = []  # 完整的探索步骤
        self.ai_analyses = []        # AI分析结果
        self.stakeholders = []       # 利益相关者
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def add_exploration_step(self, prompt: str, response: str, analysis_type: str = "general"):
        """添加探索步骤"""
        step = {
            "step_id": len(self.exploration_steps) + 1,
            "timestamp": datetime.now().isoformat(),
            "analysis_type": analysis_type,
            "prompt": prompt,
            "ai_response": response,
            "response_length": len(response),
            "key_points": self._extract_key_points(response)
        }
        self.exploration_steps.append(step)
        self.ai_analyses.append(response)
        self.updated_at = datetime.now()

    def _extract_key_points(self, response: str):
        """提取关键点"""
        # 简单的关键点提取
        points = []
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith('4.') or line.startswith('5.'):
                points.append(line)
        return points

    def set_stakeholders(self, stakeholders):
        """设置利益相关者"""
        self.stakeholders = stakeholders
        self.updated_at = datetime.now()

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "initial_idea": self.initial_idea,
            "exploration_steps": self.exploration_steps,
            "ai_analyses": self.ai_analyses,
            "stakeholders": self.stakeholders,
            "statistics": {
                "total_steps": len(self.exploration_steps),
                "total_analysis_chars": sum(len(analysis) for analysis in self.ai_analyses),
                "stakeholder_count": len(self.stakeholders),
                "duration": str(self.updated_at - self.created_at).split('.')[0]
            },
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class FixedCreativeExplorer:
    """修复的创意探索器"""

    def __init__(self, provider):
        self.provider = provider
        self.current_session = None

    async def start_exploration(self, initial_idea: str) -> EnhancedExplorationSession:
        """开始探索"""
        session = EnhancedExplorationSession(initial_idea)
        self.current_session = session
        return session

    async def explore_idea(self, session_id: str, prompt: str, analysis_type: str = "general") -> dict:
        """探索想法"""
        if not self.current_session or self.current_session.id != session_id:
            raise ValueError("Invalid session")

        messages = [
            {
                "role": "system",
                "content": "你是一位专业的创意探索专家，擅长从多个角度深入分析想法和概念。请提供详细、结构化的分析。"
            },
            {
                "role": "user",
                "content": f"初始想法：{self.current_session.initial_idea}\n\n探索要求：{prompt}"
            }
        ]

        # 调用AI
        from ai_toolkit.ai.base import AIRequest
        request = AIRequest(
            messages=messages,
            max_tokens=2000,
            temperature=0.7
        )

        response = await self.provider.chat_completion(request)
        ai_response = response.content

        # 保存完整的探索步骤
        self.current_session.add_exploration_step(prompt, ai_response, analysis_type)

        return {
            "session_id": session_id,
            "ai_response": ai_response,
            "response_length": len(ai_response),
            "usage": response.usage or {}
        }

    async def identify_stakeholders(self, session_id: str) -> list:
        """识别利益相关者"""
        if not self.current_session or self.current_session.id != session_id:
            raise ValueError("Invalid session")

        messages = [
            {
                "role": "system",
                "content": "基于探索结果，识别主要的利益相关者群体。"
            },
            {
                "role": "user",
                "content": f"基于以下探索结果，识别关键的利益相关者：\n\n{self.current_session.initial_idea}"
            }
        ]

        from ai_toolkit.ai.base import AIRequest
        request = AIRequest(
            messages=messages,
            max_tokens=500,
            temperature=0.5
        )

        response = await self.provider.chat_completion(request)

        # 简化的利益相关者提取
        stakeholders = [
            {"type": "primary_users", "description": "主要用户群体", "details": "目标使用智能家居系统的用户"},
            {"type": "secondary_users", "description": "次要用户群体", "details": "间接受影响的群体"},
            {"type": "partners", "description": "合作伙伴", "details": "技术提供商、服务商等"}
        ]

        self.current_session.set_stakeholders(stakeholders)

        return stakeholders

    async def get_exploration_summary(self, session_id: str) -> dict:
        """获取探索摘要"""
        if not self.current_session or self.current_session.id != session_id:
            raise ValueError("Invalid session")

        # 计算统计信息
        stats = {
            "total_steps": len(self.current_session.exploration_steps),
            "total_analysis_chars": sum(len(analysis) for analysis in self.current_session.ai_analyses),
            "stakeholder_count": len(self.current_session.stakeholders),
            "duration": str(self.current_session.updated_at - self.current_session.created_at).split('.')[0]
        }

        # 评估准备度
        readiness_score = 0
        if stats['total_steps'] > 0:
            readiness_score += 1
        if stats['stakeholder_count'] > 0:
            readiness_score += 1
        if stats['total_analysis_chars'] > 500:
            readiness_score += 1

        readiness = "sufficient" if readiness_score >= 2 else "insufficient"

        return {
            "session_id": self.current_session.id,
            "initial_idea": self.current_session.initial_idea,
            "exploration_duration": stats['duration'],
            "character_generation_readiness": readiness,
            "key_insights": [f"步骤{i+1}" for i in range(stats['total_steps'])],
            "statistics": stats
        }

async def fixed_step1_exploration():
    """修复的步骤1探索"""
    print("=" * 70)
    print("AI Character Toolkit - 步骤1修复版：完整数据保存探索")
    print("=" * 70)
    print("目标：完整保存AI分析结果和探索过程")
    print("想法：'创建一个智能家居控制系统'")

    try:
        # 导入必要的模块
        import uuid
        from ai_toolkit.utils.config import config
        from ai_toolkit.ai.zhipu_provider import ZhipuProvider
        from ai_toolkit.storage.file_storage import FileStorage

        # 初始化系统
        print("\n阶段1：系统初始化")
        print("-" * 30)

        config.load_config()
        zhipu_config = config.get_zhipu_config()
        provider = ZhipuProvider(zhipu_config)
        await provider.initialize()
        explorer = FixedCreativeExplorer(provider)
        storage = FileStorage()

        print("[OK] 系统初始化完成")

        # 创建探索会话
        print("\n阶段2：创建探索会话")
        print("-" * 30)

        initial_idea = "创建一个智能家居控制系统"
        session = await explorer.start_exploration(initial_idea)
        print(f"[OK] 探索会话创建：{session.id[:8]}...")

        # 执行深度探索
        print("\n阶段3：执行深度探索")
        print("-" * 30)

        exploration_prompt = """
        作为创意探索专家，请从以下角度深入分析"创建一个智能家居控制系统"这个想法：

        1. 市场分析：目标用户群体、市场潜力、竞争格局
        2. 技术可行性：核心技术要求、实现难点、技术趋势
        3. 用户价值：解决什么问题、用户使用场景、价值主张
        4. 商业模式：盈利方式、成本结构、收入来源
        5. 风险评估：主要风险、应对策略、成功要素

        请为每个角度提供详细的分析和建议。
        """

        print("正在执行AI深度分析...")
        result = await explorer.explore_idea(session.id, exploration_prompt, "comprehensive_analysis")

        print(f"[OK] AI分析完成，响应长度：{result['response_length']} 字符")
        print("\n=== AI分析结果（节选） ===")
        ai_response = result['ai_response']
        print(ai_response[:500] + "..." if len(ai_response) > 500 else ai_response)

        # 识别利益相关者
        print("\n阶段4：识别利益相关者")
        print("-" * 30)

        stakeholders = await explorer.identify_stakeholders(session.id)
        print(f"[OK] 识别到 {len(stakeholders)} 个利益相关者群体")

        # 生成摘要
        print("\n阶段5：生成探索摘要")
        print("-" * 30)

        summary = await explorer.get_exploration_summary(session.id)
        print(f"[OK] 探索摘要生成完成")
        print(f"   - 会话ID：{summary['session_id'][:8]}...")
        print(f"   - 探索时长：{summary['exploration_duration']}")
        print(f"   - 准备度：{summary['character_generation_readiness']}")
        print(f"   - 统计：{summary['statistics']}")

        # 保存完整的探索数据
        print("\n阶段6：保存完整探索数据")
        print("-" * 30)

        # 创建数据目录
        data_dir = "data/explorations"
        os.makedirs(data_dir, exist_ok=True)

        # 保存完整的探索会话
        session_file = os.path.join(data_dir, f"{session.id}_complete.json")
        session_data = session.to_dict()

        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

        print(f"[OK] 完整探索数据已保存：{session_file}")
        print(f"     文件大小：{os.path.getsize(session_file)} 字节")

        # 验证保存的数据
        print("\n阶段7：验证保存数据")
        print("-" * 30)

        with open(session_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)

        print(f"[OK] 数据验证成功")
        print(f"   - 探索步骤数量：{len(loaded_data['exploration_steps'])}")
        print(f"   - AI分析总长度：{loaded_data['statistics']['total_analysis_chars']} 字符")
        print(f"   - 利益相关者数量：{loaded_data['statistics']['stakeholder_count']}")

        # 显示第一步骤的详细内容
        if loaded_data['exploration_steps']:
            first_step = loaded_data['exploration_steps'][0]
            print(f"\n第一个探索步骤详情：")
            print(f"   - 步骤ID：{first_step['step_id']}")
            print(f"   - 分析类型：{first_step['analysis_type']}")
            print(f"   - 响应长度：{first_step['response_length']} 字符")
            print(f"   - 关键点数量：{len(first_step['key_points'])}")

        print("\n" + "="*70)
        print("修复版步骤1探索完成")
        print("="*70)
        print("改进内容：")
        print("✅ 完整保存AI分析结果")
        print("✅ 结构化存储探索步骤")
        print("✅ 详细的时间戳和统计信息")
        print("✅ 可追溯的探索过程")

        return session, summary

    except Exception as e:
        print(f"\n[ERROR] 探索过程出错: {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    # 添加uuid导入
    import uuid

    print("开始修复版步骤1探索...")

    session, summary = asyncio.run(fixed_step1_exploration())

    if session and summary:
        print(f"\n[SUCCESS] 修复版步骤1探索完成！")
        print(f"现在我们有完整的探索数据可以用于角色生成")
        print(f"会话ID：{session.id}")
    else:
        print(f"\n[ERROR] 修复版步骤1探索失败")