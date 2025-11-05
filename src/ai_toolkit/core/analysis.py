"""
Integration analysis module for AI Character Toolkit.
"""

import asyncio
from typing import Dict, List, Optional, Any, Tuple
import uuid
from datetime import datetime

from ..models.schemas import ValidationSession, Character, CharacterType
from ..ai.base import BaseAIProvider, AIRequest
from ..templates.prompts import template_manager
from ..utils.logger import get_logger, LogTimer
from ..utils.config import config
from .character import CharacterManager


class IntegrationAnalyzer:
    """Integration analysis manager for multi-perspective insights."""

    def __init__(self, ai_provider: BaseAIProvider, character_manager: CharacterManager):
        """
        Initialize integration analyzer.

        Args:
            ai_provider: AI provider for analysis
            character_manager: Character manager for character data
        """
        self.ai_provider = ai_provider
        self.character_manager = character_manager
        self.logger = get_logger(__name__)

    async def analyze_validation_session(
        self,
        validation_session: ValidationSession
    ) -> Dict[str, Any]:
        """
        Analyze validation session results.

        Args:
            validation_session: Validation session to analyze

        Returns:
            Comprehensive analysis results
        """
        self.logger.info(f"Analyzing validation session: {validation_session.id}")

        with LogTimer(self.logger, f"Analyze validation {validation_session.id}"):
            # Get character details
            character_details = {}
            for char_id in validation_session.character_responses.keys():
                character = await self.character_manager.get_character(char_id)
                if character:
                    character_details[char_id] = character

            # Prepare analysis data
            analysis_data = {
                'question': validation_session.question,
                'responses': validation_session.character_responses,
                'characters': character_details
            }

            # Perform comprehensive analysis
            integration_analysis = await self._perform_integration_analysis(analysis_data)

            return {
                'session_id': validation_session.id,
                'question': validation_session.question,
                'integration_analysis': integration_analysis,
                'timestamp': datetime.now().isoformat()
            }

    async def generate_decision_report(
        self,
        validation_session: ValidationSession,
        analysis_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive decision report.

        Args:
            validation_session: Validation session results
            analysis_context: Additional context for analysis

        Returns:
            Decision report
        """
        self.logger.info(f"Generating decision report for session: {validation_session.id}")

        # Get character information
        character_info = {}
        for char_id, response in validation_session.character_responses.items():
            character = await self.character_manager.get_character(char_id)
            if character:
                character_info[char_id] = {
                    'name': character.name,
                    'type': character.type.value,
                    'response': response
                }

        # Generate integration analysis
        integration_prompt = template_manager.render_template(
            'analysis_integration',
            user_name=character_info.get('user', {}).get('name', '用户代表'),
            user_concerns=self._extract_user_concerns(validation_session),
            user_acceptance=self._extract_acceptance_level(validation_session, CharacterType.USER),
            user_suggestions=self._extract_suggestions(validation_session, CharacterType.USER),
            user_insights=self._extract_insights(validation_session, CharacterType.USER),
            expert_name=character_info.get('expert', {}).get('name', '专家代表'),
            expert_feasibility=self._extract_feasibility_assessment(validation_session),
            expert_risks=self._extract_risk_assessment(validation_session),
            expert_recommendations=self._extract_recommendations(validation_session, CharacterType.EXPERT),
            expert_requirements=self._extract_requirements(validation_session),
            org_name=character_info.get('organization', {}).get('name', '组织代表'),
            org_value=self._extract_business_value(validation_session),
            org_resources=self._extract_resource_requirements(validation_session),
            org_implementation=self._extract_implementation_considerations(validation_session),
            org_strategic_fit=self._extract_strategic_fit(validation_session)
        )

        request = AIRequest(
            messages=[
                {"role": "system", "content": "你是专业的决策分析师，擅长整合多方观点并提供结构化的分析报告。"},
                {"role": "user", "content": integration_prompt}
            ],
            max_tokens=2000,
            temperature=0.5
        )

        response = await self.ai_provider.chat_completion(request)

        # Parse and structure the report
        report = await self._parse_decision_report(response.content, validation_session)

        # Add metadata
        report['metadata'] = {
            'session_id': validation_session.id,
            'question': validation_session.question,
            'analysis_timestamp': datetime.now().isoformat(),
            'character_count': len(validation_session.character_responses)
        }

        return report

    async def identify_action_items(
        self,
        validation_session: ValidationSession,
        priority_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Identify actionable items from validation results.

        Args:
            validation_session: Validation session results
            priority_filter: Optional priority filter (high, medium, low)

        Returns:
            List of action items
        """
        self.logger.info(f"Identifying action items for session: {validation_session.id}")

        action_items = []

        # Analyze each response for action items
        for char_id, response in validation_session.character_responses.items():
            character = await self.character_manager.get_character(char_id)
            if character:
                items = self._extract_action_items(response, character)
                action_items.extend(items)

        # Prioritize action items
        prioritized_items = await self._prioritize_action_items(action_items, priority_filter)

        return prioritized_items

    async def assess_risk_matrix(
        self,
        validation_session: ValidationSession
    ) -> Dict[str, Any]:
        """
        Create risk assessment matrix.

        Args:
            validation_session: Validation session results

        Returns:
            Risk assessment matrix
        """
        self.logger.info(f"Creating risk matrix for session: {validation_session.id}")

        # Extract risks from all responses
        all_risks = []
        for char_id, response in validation_session.character_responses.items():
            character = await self.character_manager.get_character(char_id)
            if character:
                risks = self._extract_risks(response, character)
                all_risks.extend(risks)

        # Categorize and assess risks
        risk_matrix = {
            'high_probability_high_impact': [],
            'high_probability_low_impact': [],
            'low_probability_high_impact': [],
            'low_probability_low_impact': [],
            'mitigation_strategies': {}
        }

        for risk in all_risks:
            category = self._categorize_risk(risk)
            risk_matrix[category].append(risk)

        # Generate mitigation strategies
        risk_matrix['mitigation_strategies'] = await self._generate_mitigation_strategies(risk_matrix)

        return risk_matrix

    async def generate_roadmap(
        self,
        validation_session: ValidationSession,
        timeframe_months: int = 12
    ) -> Dict[str, Any]:
        """
        Generate implementation roadmap.

        Args:
            validation_session: Validation session results
            timeframe_months: Roadmap timeframe in months

        Returns:
            Implementation roadmap
        """
        self.logger.info(f"Generating roadmap for session: {validation_session.id}")

        # Extract implementation insights
        implementation_insights = self._extract_implementation_insights(validation_session)

        # Generate roadmap phases
        roadmap = {
            'timeframe_months': timeframe_months,
            'phases': [],
            'milestones': [],
            'dependencies': [],
            'resource_allocation': {}
        }

        # Create phases based on complexity and dependencies
        phases = [
            {
                'name': '准备阶段',
                'duration_months': 1,
                'objectives': ['需求确认', '团队组建', '资源准备'],
                'deliverables': ['项目计划', '团队结构', '资源清单']
            },
            {
                'name': '设计阶段',
                'duration_months': 2,
                'objectives': ['概念设计', '技术方案', '原型开发'],
                'deliverables': ['设计文档', '技术架构', '原型']
            },
            {
                'name': '开发阶段',
                'duration_months': 6,
                'objectives': ['核心功能开发', '集成测试', '用户测试'],
                'deliverables': ['产品功能', '测试报告', '用户反馈']
            },
            {
                'name': '部署阶段',
                'duration_months': 3,
                'objectives': ['系统部署', '用户培训', '运营优化'],
                'deliverables': ['生产系统', '培训材料', '运营手册']
            }
        ]

        roadmap['phases'] = phases

        # Generate milestones
        current_month = 0
        for phase in phases:
            milestone = {
                'month': current_month + phase['duration_months'],
                'phase': phase['name'],
                'description': f"{phase['name']}完成"
            }
            roadmap['milestones'].append(milestone)
            current_month += phase['duration_months']

        return roadmap

    async def _perform_integration_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive integration analysis."""
        # Analyze consensus and conflicts
        consensus_analysis = await self._analyze_consensus(analysis_data['responses'])

        # Identify opportunities and risks
        opportunities = await self._identify_opportunities(analysis_data)
        risks = await self._identify_risks(analysis_data)

        # Generate recommendations
        recommendations = await self._generate_integrated_recommendations(analysis_data)

        return {
            'consensus_analysis': consensus_analysis,
            'opportunities': opportunities,
            'risks': risks,
            'recommendations': recommendations,
            'confidence_level': self._calculate_confidence_level(analysis_data)
        }

    async def _parse_decision_report(self, report_text: str, validation_session: ValidationSession) -> Dict[str, Any]:
        """Parse decision report from AI response."""
        # Simple parsing - in production, use structured extraction
        return {
            'executive_summary': report_text[:300] + "..." if len(report_text) > 300 else report_text,
            'key_findings': self._extract_key_findings(report_text),
            'recommendations': self._extract_recommendations_from_text(report_text),
            'next_steps': self._extract_next_steps(report_text),
            'success_factors': self._extract_success_factors(report_text)
        }

    def _extract_user_concerns(self, validation_session: ValidationSession) -> str:
        """Extract user concerns from validation session."""
        for char_id, response in validation_session.character_responses.items():
            character = asyncio.create_task(self.character_manager.get_character(char_id))
            # Simplified extraction
            if "用户" in response or "体验" in response:
                return "用户关注易用性和价值实现"
        return "用户需求需要进一步明确"

    def _extract_acceptance_level(self, validation_session: ValidationSession, char_type: CharacterType) -> str:
        """Extract acceptance level for character type."""
        # Simplified analysis
        return "较高" if char_type == CharacterType.USER else "中等"

    def _extract_suggestions(self, validation_session: ValidationSession, char_type: CharacterType) -> str:
        """Extract suggestions for character type."""
        return "需要更多用户反馈" if char_type == CharacterType.USER else "技术可行性需要验证"

    def _extract_insights(self, validation_session: ValidationSession, char_type: CharacterType) -> str:
        """Extract insights for character type."""
        return "用户痛点明确" if char_type == CharacterType.USER else "技术方案可行"

    def _extract_feasibility_assessment(self, validation_session: ValidationSession) -> str:
        """Extract feasibility assessment."""
        return "技术可行性较高，但需要充分考虑资源约束"

    def _extract_risk_assessment(self, validation_session: ValidationSession) -> str:
        """Extract risk assessment."""
        return "主要风险在技术复杂度和市场接受度"

    def _extract_recommendations(self, validation_session: ValidationSession, char_type: CharacterType) -> str:
        """Extract recommendations for character type."""
        return "建议采用渐进式开发" if char_type == CharacterType.EXPERT else "建议深入用户调研"

    def _extract_requirements(self, validation_session: ValidationSession) -> str:
        """Extract key requirements."""
        return "需要技术团队和市场团队的紧密合作"

    def _extract_business_value(self, validation_session: ValidationSession) -> str:
        """Extract business value assessment."""
        return "潜在商业价值较大，但需要明确盈利模式"

    def _extract_resource_requirements(self, validation_session: ValidationSession) -> str:
        """Extract resource requirements."""
        return "需要中等规模的技术团队和初期投资"

    def _extract_implementation_considerations(self, validation_session: ValidationSession) -> str:
        """Extract implementation considerations."""
        return "建议分阶段实施，先验证核心概念"

    def _extract_strategic_fit(self, validation_session: ValidationSession) -> str:
        """Extract strategic fit assessment."""
        return "与当前市场趋势相符，具有战略意义"

    def _extract_action_items(self, response: str, character: Character) -> List[Dict[str, Any]]:
        """Extract action items from response."""
        action_items = []

        # Look for action-oriented phrases
        action_indicators = ["应该", "需要", "建议", "必须", "可以"]

        for indicator in action_indicators:
            if indicator in response:
                # Extract the sentence containing the action
                sentences = response.split('。')
                for sentence in sentences:
                    if indicator in sentence:
                        action_items.append({
                            'description': sentence.strip(),
                            'character': character.name,
                            'character_type': character.type.value,
                            'priority': 'medium'  # Default priority
                        })

        return action_items

    async def _prioritize_action_items(self, action_items: List[Dict[str, Any]], priority_filter: Optional[str]) -> List[Dict[str, Any]]:
        """Prioritize action items."""
        # Simple prioritization based on keywords
        high_priority_keywords = ["必须", "紧急", "关键", "重要"]
        low_priority_keywords = ["可以", "考虑", "可选"]

        for item in action_items:
            description = item['description'].lower()
            if any(keyword in description for keyword in high_priority_keywords):
                item['priority'] = 'high'
            elif any(keyword in description for keyword in low_priority_keywords):
                item['priority'] = 'low'

        # Filter by priority if specified
        if priority_filter:
            action_items = [item for item in action_items if item['priority'] == priority_filter]

        return sorted(action_items, key=lambda x: {'high': 0, 'medium': 1, 'low': 2}[x['priority']])

    def _extract_risks(self, response: str, character: Character) -> List[Dict[str, Any]]:
        """Extract risks from response."""
        risks = []
        risk_indicators = ["风险", "挑战", "问题", "困难", "威胁"]

        for indicator in risk_indicators:
            if indicator in response:
                # Extract surrounding context
                sentences = response.split('。')
                for sentence in sentences:
                    if indicator in sentence:
                        risks.append({
                            'description': sentence.strip(),
                            'character': character.name,
                            'character_type': character.type.value
                        })

        return risks

    def _categorize_risk(self, risk: Dict[str, Any]) -> str:
        """Categorize risk based on content."""
        description = risk['description'].lower()

        # Simple categorization based on keywords
        if "严重" in description or "重大" in description:
            return 'high_probability_high_impact' if "经常" in description else 'low_probability_high_impact'
        else:
            return 'high_probability_low_impact' if "经常" in description else 'low_probability_low_impact'

    async def _generate_mitigation_strategies(self, risk_matrix: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate mitigation strategies for risks."""
        strategies = {
            'high_probability_high_impact': [
                "制定详细的应对计划",
                "建立监控机制",
                "准备应急方案"
            ],
            'high_probability_low_impact': [
                "加强日常管理",
                "建立预防措施",
                "定期检查"
            ],
            'low_probability_high_impact': [
                "建立应急预案",
                "购买保险",
                "分散风险"
            ],
            'low_probability_low_impact': [
                "定期监控",
                "建立预警机制",
                "记录经验"
            ]
        }

        return strategies

    def _extract_implementation_insights(self, validation_session: ValidationSession) -> Dict[str, Any]:
        """Extract implementation insights from validation session."""
        return {
            'complexity': 'medium',
            'duration_estimate': '6-12 months',
            'team_size': '5-10 people',
            'key_challenges': ['技术集成', '用户接受度', '资源协调']
        }

    async def _analyze_consensus(self, responses: Dict[str, str]) -> Dict[str, Any]:
        """Analyze consensus among responses."""
        if len(responses) < 2:
            return {'consensus_level': 1.0, 'common_themes': [], 'differences': []}

        # Simple consensus analysis
        all_words = set()
        for response in responses.values():
            words = set(response.lower().split())
            all_words.update(words)

        common_words = []
        for word in all_words:
            if all(word in response.lower() for response in responses.values()):
                common_words.append(word)

        consensus_level = len(common_words) / len(all_words) if all_words else 0

        return {
            'consensus_level': min(consensus_level * 2, 1.0),  # Scale to 0-1
            'common_themes': common_words[:10],
            'differences': []
        }

    async def _identify_opportunities(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Identify opportunities from analysis data."""
        opportunities = []
        opportunity_keywords = ["机会", "优势", "潜力", "空间", "可能"]

        for response in analysis_data['responses'].values():
            for keyword in opportunity_keywords:
                if keyword in response:
                    # Extract context around the keyword
                    start = response.find(keyword)
                    if start != -1:
                        end = response.find('。', start)
                        if end != -1:
                            opportunity = response[start:end].strip()
                            opportunities.append(opportunity)

        return list(set(opportunities))[:5]  # Unique opportunities, max 5

    async def _identify_risks(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Identify risks from analysis data."""
        risks = []
        risk_keywords = ["风险", "挑战", "问题", "困难", "威胁"]

        for response in analysis_data['responses'].values():
            for keyword in risk_keywords:
                if keyword in response:
                    start = response.find(keyword)
                    if start != -1:
                        end = response.find('。', start)
                        if end != -1:
                            risk = response[start:end].strip()
                            risks.append(risk)

        return list(set(risks))[:5]  # Unique risks, max 5

    async def _generate_integrated_recommendations(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Generate integrated recommendations."""
        return [
            "进行更详细的市场调研",
            "制定分阶段实施计划",
            "建立跨职能团队",
            "设置明确的成功指标",
            "建立用户反馈机制"
        ]

    def _calculate_confidence_level(self, analysis_data: Dict[str, Any]) -> float:
        """Calculate confidence level in analysis."""
        # Simple calculation based on number and diversity of responses
        response_count = len(analysis_data['responses'])

        if response_count >= 3:
            return 0.8
        elif response_count >= 2:
            return 0.6
        else:
            return 0.4

    def _extract_key_findings(self, report_text: str) -> List[str]:
        """Extract key findings from report text."""
        # Simple extraction
        findings = []
        sentences = report_text.split('。')

        for sentence in sentences:
            if any(indicator in sentence for indicator in ["发现", "表明", "显示", "结论"]):
                findings.append(sentence.strip())

        return findings[:5]

    def _extract_recommendations_from_text(self, report_text: str) -> List[str]:
        """Extract recommendations from report text."""
        recommendations = []
        sentences = report_text.split('。')

        for sentence in sentences:
            if any(indicator in sentence for indicator in ["建议", "应该", "需要", "推荐"]):
                recommendations.append(sentence.strip())

        return recommendations[:5]

    def _extract_next_steps(self, report_text: str) -> List[str]:
        """Extract next steps from report text."""
        next_steps = []
        sentences = report_text.split('。')

        for sentence in sentences:
            if any(indicator in sentence for indicator in ["下一步", "随后", "然后", "之后"]):
                next_steps.append(sentence.strip())

        return next_steps[:5]

    def _extract_success_factors(self, report_text: str) -> List[str]:
        """Extract success factors from report text."""
        success_factors = []
        sentences = report_text.split('。')

        for sentence in sentences:
            if any(indicator in sentence for indicator in ["成功", "关键", "重要", "核心"]):
                success_factors.append(sentence.strip())

        return success_factors[:5]