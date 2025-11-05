"""
Creative exploration module for AI Character Toolkit.
"""

import asyncio
from typing import Dict, List, Optional, Any, Tuple
import uuid
from datetime import datetime

from ..models.schemas import ExplorationSession, CharacterType
from ..ai.base import BaseAIProvider, AIRequest
from ..templates.prompts import template_manager
from ..utils.logger import get_logger, LogTimer
from ..utils.config import config


class CreativeExplorer:
    """Creative exploration manager."""

    def __init__(self, ai_provider: BaseAIProvider):
        """
        Initialize creative explorer.

        Args:
            ai_provider: AI provider for exploration
        """
        self.ai_provider = ai_provider
        self.logger = get_logger(__name__)
        self.current_session: Optional[ExplorationSession] = None

    async def start_exploration(self, initial_idea: str) -> ExplorationSession:
        """
        Start a new creative exploration session.

        Args:
            initial_idea: Initial idea to explore

        Returns:
            Exploration session
        """
        self.logger.info(f"Starting exploration for idea: {initial_idea[:100]}...")

        with LogTimer(self.logger, "Create exploration session"):
            session = ExplorationSession(
                id=str(uuid.uuid4()),
                initial_idea=initial_idea,
                exploration_data={
                    'start_time': datetime.now().isoformat(),
                    'questions_asked': [],
                    'insights_discovered': [],
                    'stakeholders_identified': [],
                    'knowledge_areas': [],
                    'implementation_context': {}
                }
            )

        self.current_session = session
        self.logger.info(f"Exploration session created: {session.id}")
        return session

    async def explore_idea(self, session_id: str, user_input: str) -> Dict[str, Any]:
        """
        Explore idea with AI assistance.

        Args:
            session_id: Exploration session ID
            user_input: User input or response

        Returns:
            Exploration results
        """
        if not self.current_session or self.current_session.id != session_id:
            raise ValueError("Invalid or expired exploration session")

        self.logger.info(f"Exploring idea for session {session_id}")

        with LogTimer(self.logger, "AI exploration response"):
            # Generate exploration prompt
            prompt = template_manager.render_template(
                'creative_exploration',
                initial_idea=self.current_session.initial_idea
            )

            # Prepare AI request
            request = AIRequest(
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=config.get('dialogue.max_tokens', 1500),
                temperature=config.get('dialogue.temperature', 0.7)
            )

            try:
                response = await self.ai_provider.chat_completion(request)
                exploration_result = await self._parse_exploration_response(response.content)

                # Update session with new data
                await self._update_exploration_data(exploration_result)

                return {
                    'session_id': session_id,
                    'ai_response': response.content,
                    'analysis': exploration_result,
                    'session_data': self.current_session.exploration_data
                }

            except Exception as e:
                self.logger.error(f"Error during exploration: {e}")
                raise

    async def ask_exploration_question(self, session_id: str, question_type: str = "general") -> str:
        """
        Ask a specific type of exploration question.

        Args:
            session_id: Exploration session ID
            question_type: Type of question to ask

        Returns:
            AI-generated question
        """
        if not self.current_session or self.current_session.id != session_id:
            raise ValueError("Invalid or expired exploration session")

        question_templates = {
            "stakeholders": "基于当前的想法，请帮助我们识别：谁是主要用户？谁会受到影响？谁可能提供帮助？请提出具体的问题来澄清这些利益相关者的特征。",
            "scenarios": "请帮助我们探索这个想法的不同应用场景：在什么情况下这个想法最有价值？哪些场景下可能不适用？请提出具体问题来探索各种可能性。",
            "feasibility": "请帮助我们评估实施可行性：需要什么技术？需要什么资源？有什么潜在的障碍？请提出相关问题来深入了解实施要求。",
            "value": "请帮助我们探索价值主张：这个想法解决了什么问题？为谁创造了价值？独特之处在哪里？请提出相关问题来明确价值点。",
            "risks": "请帮助我们识别风险：可能遇到什么挑战？有什么潜在的风险因素？如何规避这些风险？请提出相关问题来全面评估风险。",
            "general": "请基于我们讨论的想法，提出一个深入的、开放性的问题，帮助我们进一步探索和完善这个概念。"
        }

        question_prompt = question_templates.get(question_type, question_templates["general"])

        with LogTimer(self.logger, f"Generate {question_type} question"):
            request = AIRequest(
                messages=[
                    {"role": "system", "content": "你是一个专业的创意探索助手，擅长提出有洞察力的问题。请只提出一个简洁、具体、有深度的问题。"},
                    {"role": "user", "content": f"当前想法：{self.current_session.initial_idea}\n\n{question_prompt}"}
                ],
                max_tokens=200,
                temperature=0.8
            )

            response = await self.ai_provider.chat_completion(request)
            question = response.content.strip()

            # Record question in session
            self.current_session.exploration_data['questions_asked'].append({
                'type': question_type,
                'question': question,
                'timestamp': datetime.now().isoformat()
            })

            return question

    async def identify_stakeholders(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Identify stakeholders for the idea.

        Args:
            session_id: Exploration session ID

        Returns:
            List of identified stakeholders
        """
        if not self.current_session or self.current_session.id != session_id:
            raise ValueError("Invalid or expired exploration session")

        prompt = f"""
        基于以下想法，请识别和分析关键利益相关者：

        想法：{self.current_session.initial_idea}

        请提供：
        1. 主要用户群体（3-5个）
        2. 间接受影响的群体（2-3个）
        3. 可能提供帮助的群体（2-3个）

        对每个群体，请描述：
        - 群体特征
        - 与想法的关系
        - 核心需求和关切
        - 可能的贡献或影响

        请以结构化的方式回应。
        """

        with LogTimer(self.logger, "Identify stakeholders"):
            request = AIRequest(
                messages=[
                    {"role": "system", "content": "你是利益相关者分析专家。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.6
            )

            response = await self.ai_provider.chat_completion(request)
            stakeholders = await self._parse_stakeholders(response.content)

            # Update session data
            self.current_session.exploration_data['stakeholders_identified'] = stakeholders
            self.current_session.update_timestamp()

            return stakeholders

    async def identify_knowledge_areas(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Identify required knowledge areas.

        Args:
            session_id: Exploration session ID

        Returns:
            List of knowledge areas
        """
        if not self.current_session or self.current_session.id != session_id:
            raise ValueError("Invalid or expired exploration session")

        prompt = f"""
        基于以下想法，请分析所需的知识领域：

        想法：{self.current_session.initial_idea}

        请识别：
        1. 核心技术领域
        2. 商业知识领域
        3. 法律法规要求
        4. 行业专业知识

        对每个领域，请说明：
        - 重要程度（高/中/低）
        - 具体内容要求
        - 获取难度
        - 推荐学习资源（如有）

        请以结构化的方式回应。
        """

        with LogTimer(self.logger, "Identify knowledge areas"):
            request = AIRequest(
                messages=[
                    {"role": "system", "content": "你是知识领域分析专家。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.5
            )

            response = await self.ai_provider.chat_completion(request)
            knowledge_areas = await self._parse_knowledge_areas(response.content)

            # Update session data
            self.current_session.exploration_data['knowledge_areas'] = knowledge_areas
            self.current_session.update_timestamp()

            return knowledge_areas

    async def analyze_implementation_context(self, session_id: str) -> Dict[str, Any]:
        """
        Analyze implementation context.

        Args:
            session_id: Exploration session ID

        Returns:
            Implementation context analysis
        """
        if not self.current_session or self.current_session.id != session_id:
            raise ValueError("Invalid or expired exploration session")

        prompt = f"""
        基于以下想法，请分析实施环境和要求：

        想法：{self.current_session.initial_idea}

        请分析：
        1. 适合的组织类型
        2. 资源需求（人力、财力、技术）
        3. 时间周期预估
        4. 关键成功因素
        5. 潜在商业模式

        请提供具体的分析和建议。
        """

        with LogTimer(self.logger, "Analyze implementation context"):
            request = AIRequest(
                messages=[
                    {"role": "system", "content": "你是实施环境分析专家。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.6
            )

            response = await self.ai_provider.chat_completion(request)
            context = await self._parse_implementation_context(response.content)

            # Update session data
            self.current_session.exploration_data['implementation_context'] = context
            self.current_session.update_timestamp()

            return context

    async def get_exploration_summary(self, session_id: str) -> Dict[str, Any]:
        """
        Get comprehensive exploration summary.

        Args:
            session_id: Exploration session ID

        Returns:
            Exploration summary
        """
        if not self.current_session or self.current_session.id != session_id:
            raise ValueError("Invalid or expired exploration session")

        session_data = self.current_session.exploration_data

        summary = {
            'session_id': session_id,
            'initial_idea': self.current_session.initial_idea,
            'exploration_duration': self._calculate_exploration_duration(),
            'key_insights': session_data.get('insights_discovered', []),
            'stakeholders': session_data.get('stakeholders_identified', []),
            'knowledge_areas': session_data.get('knowledge_areas', []),
            'implementation_context': session_data.get('implementation_context', {}),
            'questions_explored': session_data.get('questions_asked', []),
            'character_generation_readiness': self._assess_character_generation_readiness()
        }

        return summary

    async def _parse_exploration_response(self, response: str) -> Dict[str, Any]:
        """Parse AI exploration response."""
        # Simple parsing - in production, you'd use more sophisticated NLP
        insights = []
        if "洞察" in response or "发现" in response:
            insights.append("发现新的可能性或机会")

        questions = []
        if "？" in response or "问题" in response:
            questions.append("需要进一步澄清的问题")

        return {
            'insights': insights,
            'questions': questions,
            'new_directions': 1 if "新方向" in response else 0,
            'complexity_level': "medium"  # Simplified
        }

    async def _parse_stakeholders(self, response: str) -> List[Dict[str, Any]]:
        """Parse stakeholders from AI response."""
        # Simplified parsing - in production, use structured extraction
        return [
            {'type': 'primary_users', 'description': '主要用户群体'},
            {'type': 'secondary_users', 'description': '次要用户群体'},
            {'type': 'partners', 'description': '合作伙伴'}
        ]

    async def _parse_knowledge_areas(self, response: str) -> List[Dict[str, Any]]:
        """Parse knowledge areas from AI response."""
        # Simplified parsing
        return [
            {'area': '技术领域', 'importance': 'high'},
            {'area': '商业知识', 'importance': 'medium'},
            {'area': '法律要求', 'importance': 'medium'}
        ]

    async def _parse_implementation_context(self, response: str) -> Dict[str, Any]:
        """Parse implementation context from AI response."""
        # Simplified parsing
        return {
            'organization_type': 'startup',
            'resource_requirements': 'medium',
            'time_estimate': '6-12 months',
            'key_factors': ['技术', '市场', '团队']
        }

    async def _update_exploration_data(self, exploration_result: Dict[str, Any]):
        """Update exploration session data."""
        if exploration_result.get('insights'):
            self.current_session.exploration_data['insights_discovered'].extend(
                exploration_result['insights']
            )

        self.current_session.update_timestamp()

    def _calculate_exploration_duration(self) -> str:
        """Calculate exploration session duration."""
        start_time = self.current_session.exploration_data.get('start_time')
        if start_time:
            start = datetime.fromisoformat(start_time)
            duration = datetime.now() - start
            return str(duration).split('.')[0]  # Remove microseconds
        return "Unknown"

    def _assess_character_generation_readiness(self) -> str:
        """Assess readiness for character generation."""
        data = self.current_session.exploration_data
        score = 0

        if data.get('stakeholders_identified'):
            score += 1
        if data.get('knowledge_areas'):
            score += 1
        if data.get('implementation_context'):
            score += 1
        if len(data.get('questions_asked', [])) >= 3:
            score += 1

        if score >= 3:
            return "ready"
        elif score >= 2:
            return "partial"
        else:
            return "insufficient"