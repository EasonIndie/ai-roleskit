"""
Concurrent validation module for AI Character Toolkit.
"""

import asyncio
from typing import Dict, List, Optional, Any, Tuple
import uuid
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from ..models.schemas import ValidationSession, Character, CharacterType
from ..ai.base import BaseAIProvider, AIRequest
from ..templates.prompts import template_manager
from ..utils.logger import get_logger, LogTimer
from ..utils.config import config
from .character import CharacterManager


class ConcurrentValidator:
    """Concurrent validation manager for multi-character perspectives."""

    def __init__(self, ai_provider: BaseAIProvider, character_manager: CharacterManager):
        """
        Initialize concurrent validator.

        Args:
            ai_provider: AI provider for validation
            character_manager: Character manager for character data
        """
        self.ai_provider = ai_provider
        self.character_manager = character_manager
        self.logger = get_logger(__name__)
        self.max_workers = config.get('concurrent.max_workers', 3)
        self.timeout = config.get('concurrent.timeout', 60)
        self.validation_sessions: Dict[str, ValidationSession] = {}

    async def create_validation_session(
        self,
        question: str,
        character_ids: List[str]
    ) -> ValidationSession:
        """
        Create a new validation session.

        Args:
            question: Question to validate
            character_ids: List of character IDs to include

        Returns:
            Created validation session
        """
        # Validate characters exist
        characters = []
        for char_id in character_ids:
            character = await self.character_manager.get_character(char_id)
            if not character:
                raise ValueError(f"Character not found: {char_id}")
            characters.append(character)

        # Ensure we have different character types
        char_types = {char.type for char in characters}
        if len(char_types) < 2:
            self.logger.warning("Validation with limited character type diversity")

        session = ValidationSession(
            id=str(uuid.uuid4()),
            question=question,
            created_at=datetime.now()
        )

        self.validation_sessions[session.id] = session
        self.logger.info(f"Validation session created: {session.id}")

        return session

    async def run_concurrent_validation(
        self,
        session_id: str,
        character_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Run concurrent validation with multiple characters.

        Args:
            session_id: Validation session ID
            character_ids: Characters to include in validation

        Returns:
            Validation results
        """
        if session_id not in self.validation_sessions:
            raise ValueError(f"Validation session not found: {session_id}")

        session = self.validation_sessions[session_id]
        self.logger.info(f"Starting concurrent validation for session {session_id}")

        with LogTimer(self.logger, f"Concurrent validation {session_id}"):
            # Prepare characters
            characters = []
            for char_id in character_ids:
                character = await self.character_manager.get_character(char_id)
                if character:
                    characters.append(character)

            # Create validation tasks
            tasks = []
            for character in characters:
                task = self._get_character_perspective(session.question, character)
                tasks.append(task)

            # Run tasks concurrently
            try:
                responses = await asyncio.gather(*tasks, timeout=self.timeout)

                # Process responses
                for character, response in zip(characters, responses):
                    session.character_responses[character.id] = response

                # Analyze results
                analysis = await self._analyze_validation_results(session, characters)
                session.analysis_result = analysis

                self.logger.info(f"Concurrent validation completed for session {session_id}")

                return {
                    'session_id': session_id,
                    'question': session.question,
                    'character_responses': {
                        char.id: response for char, response in zip(characters, responses)
                    },
                    'analysis': analysis,
                    'timestamp': datetime.now().isoformat()
                }

            except asyncio.TimeoutError:
                self.logger.error(f"Validation timeout for session {session_id}")
                raise
            except Exception as e:
                self.logger.error(f"Error in concurrent validation: {e}")
                raise

    async def run_sequential_validation(
        self,
        session_id: str,
        character_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Run sequential validation (for comparison or when concurrency is limited).

        Args:
            session_id: Validation session ID
            character_ids: Characters to include in validation

        Returns:
            Validation results
        """
        if session_id not in self.validation_sessions:
            raise ValueError(f"Validation session not found: {session_id}")

        session = self.validation_sessions[session_id]
        self.logger.info(f"Starting sequential validation for session {session_id}")

        responses = {}
        characters = []

        for char_id in character_ids:
            character = await self.character_manager.get_character(char_id)
            if character:
                characters.append(character)
                response = await self._get_character_perspective(session.question, character)
                responses[char.id] = response

        # Store responses
        session.character_responses = responses

        # Analyze results
        analysis = await self._analyze_validation_results(session, characters)
        session.analysis_result = analysis

        return {
            'session_id': session_id,
            'question': session.question,
            'character_responses': responses,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }

    async def get_character_perspective(
        self,
        session_id: str,
        character_id: str
    ) -> str:
        """
        Get perspective from a specific character.

        Args:
            session_id: Validation session ID
            character_id: Character ID

        Returns:
            Character perspective
        """
        if session_id not in self.validation_sessions:
            raise ValueError(f"Validation session not found: {session_id}")

        session = self.validation_sessions[session_id]
        character = await self.character_manager.get_character(character_id)

        if not character:
            raise ValueError(f"Character not found: {character_id}")

        return await self._get_character_perspective(session.question, character)

    async def compare_perspectives(
        self,
        session_id: str
    ) -> Dict[str, Any]:
        """
        Compare different character perspectives.

        Args:
            session_id: Validation session ID

        Returns:
            Perspective comparison
        """
        if session_id not in self.validation_sessions:
            raise ValueError(f"Validation session not found: {session_id}")

        session = self.validation_sessions[session_id]

        comparison = {
            'session_id': session_id,
            'question': session.question,
            'perspectives': [],
            'common_points': [],
            'differences': [],
            'insights': []
        }

        # Analyze each perspective
        for char_id, response in session.character_responses.items():
            character = await self.character_manager.get_character(char_id)
            if character:
                perspective_analysis = await self._analyze_perspective(response, character)
                comparison['perspectives'].append({
                    'character_id': char_id,
                    'character_name': character.name,
                    'character_type': character.type.value,
                    'analysis': perspective_analysis
                })

        # Find common points and differences
        if len(session.character_responses) > 1:
            common_diff = await self._compare_responses(list(session.character_responses.values()))
            comparison['common_points'] = common_diff['common']
            comparison['differences'] = common_diff['differences']

        return comparison

    async def _get_character_perspective(self, question: str, character: Character) -> str:
        """Get perspective from a single character."""
        character_prompt = self.character_manager.generator.get_character_prompt(character)

        # Render validation template
        prompt = template_manager.render_template(
            'concurrent_validation',
            character_name=character.name,
            character_type=character.type.value,
            question=question,
            character_background=self._format_character_background(character)
        )

        request = AIRequest(
            messages=[
                {"role": "system", "content": character_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )

        response = await self.ai_provider.chat_completion(request)
        return response.content

    async def _analyze_validation_results(
        self,
        session: ValidationSession,
        characters: List[Character]
    ) -> Dict[str, Any]:
        """Analyze validation results from multiple characters."""
        analysis = {
            'overall_assessment': '',
            'consensus_level': 0,
            'key_concerns': [],
            'opportunities': [],
            'recommendations': [],
            'risk_assessment': {},
            'action_items': []
        }

        if len(session.character_responses) < 2:
            return analysis

        # Calculate consensus level
        responses = list(session.character_responses.values())
        consensus_score = await self._calculate_consensus(responses)
        analysis['consensus_level'] = consensus_score

        # Extract key concerns and opportunities
        all_text = ' '.join(responses)
        analysis['key_concerns'] = self._extract_concerns(all_text)
        analysis['opportunities'] = self._extract_opportunities(all_text)

        # Generate recommendations
        analysis['recommendations'] = await self._generate_recommendations(session, characters)

        return analysis

    async def _analyze_perspective(self, response: str, character: Character) -> Dict[str, Any]:
        """Analyze a single character's perspective."""
        return {
            'sentiment': self._analyze_sentiment(response),
            'key_points': self._extract_key_points(response),
            'concerns': self._extract_concerns(response),
            'suggestions': self._extract_suggestions(response),
            'overall_stance': self._determine_stance(response)
        }

    async def _compare_responses(self, responses: List[str]) -> Dict[str, List[str]]:
        """Compare multiple responses to find commonalities and differences."""
        # Simple comparison - in production, use proper NLP
        common = []
        differences = []

        if len(responses) >= 2:
            # Look for common words and themes
            all_words = set()
            for response in responses:
                words = set(response.lower().split())
                all_words.update(words)

            common_words = []
            for word in all_words:
                if all(word in response.lower() for response in responses):
                    common_words.append(word)

            common = common_words[:10]  # Top 10 common words

        return {'common': common, 'differences': differences}

    async def _calculate_consensus(self, responses: List[str]) -> float:
        """Calculate consensus level between responses."""
        if len(responses) < 2:
            return 1.0

        # Simple consensus calculation based on common words
        all_words = set()
        for response in responses:
            words = set(response.lower().split())
            all_words.update(words)

        common_words = set()
        for word in all_words:
            if all(word in response.lower() for response in responses):
                common_words.add(word)

        consensus_ratio = len(common_words) / len(all_words) if all_words else 0
        return min(consensus_ratio * 2, 1.0)  # Scale to 0-1

    async def _generate_recommendations(
        self,
        session: ValidationSession,
        characters: List[Character]
    ) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []

        # Analyze character types and their perspectives
        user_chars = [c for c in characters if c.type == CharacterType.USER]
        expert_chars = [c for c in characters if c.type == CharacterType.EXPERT]
        org_chars = [c for c in characters if c.type == CharacterType.ORGANIZATION]

        if user_chars and expert_chars:
            recommendations.append("用户需求与专家建议需要进一步协调")

        if expert_chars and org_chars:
            recommendations.append("考虑技术可行性与商业目标的平衡")

        if user_chars and org_chars:
            recommendations.append("关注用户价值与商业可持续性的统一")

        recommendations.append("建议进行更详细的需求分析和市场调研")

        return recommendations

    def _format_character_background(self, character: Character) -> str:
        """Format character background for validation."""
        return f"""
        角色：{character.name} ({character.type.value})
        背景：{character.info.background or 'N/A'}
        专业领域：{character.expertise.professional_field or 'N/A'}
        目标：{character.context.goals or 'N/A'}
        """

    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis."""
        positive_words = ["好", "支持", "同意", "优秀", "可行"]
        negative_words = ["问题", "困难", "风险", "挑战", "不可行"]

        positive_count = sum(word in text for word in positive_words)
        negative_count = sum(word in text for word in negative_words)

        if positive_count > negative_count:
            return "积极"
        elif negative_count > positive_count:
            return "谨慎"
        else:
            return "中性"

    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key points from text."""
        # Simple extraction - look for sentences with key indicators
        sentences = text.split('。')
        key_points = []

        for sentence in sentences:
            if any(indicator in sentence for indicator in ["重要", "关键", "核心", "必须", "建议"]):
                key_points.append(sentence.strip())

        return key_points[:5]  # Top 5 key points

    def _extract_concerns(self, text: str) -> List[str]:
        """Extract concerns from text."""
        concern_indicators = ["担心", "问题", "风险", "挑战", "困难", "障碍"]
        concerns = []

        for indicator in concern_indicators:
            if indicator in text:
                # Extract surrounding context
                start = text.find(indicator)
                if start != -1:
                    end = text.find('。', start)
                    if end != -1:
                        concern = text[start:end].strip()
                        concerns.append(concern)

        return concerns[:5]

    def _extract_opportunities(self, text: str) -> List[str]:
        """Extract opportunities from text."""
        opportunity_indicators = ["机会", "可能", "优势", "潜力", "空间"]
        opportunities = []

        for indicator in opportunity_indicators:
            if indicator in text:
                start = text.find(indicator)
                if start != -1:
                    end = text.find('。', start)
                    if end != -1:
                        opportunity = text[start:end].strip()
                        opportunities.append(opportunity)

        return opportunities[:5]

    def _extract_suggestions(self, text: str) -> List[str]:
        """Extract suggestions from text."""
        suggestion_indicators = ["建议", "应该", "可以", "需要", "最好"]
        suggestions = []

        for indicator in suggestion_indicators:
            if indicator in text:
                start = text.find(indicator)
                if start != -1:
                    end = text.find('。', start)
                    if end != -1:
                        suggestion = text[start:end].strip()
                        suggestions.append(suggestion)

        return suggestions[:5]

    def _determine_stance(self, text: str) -> str:
        """Determine overall stance from text."""
        support_words = ["支持", "同意", "可行", "好", "优秀"]
        oppose_words = ["反对", "不可行", "问题", "风险", "困难"]

        support_count = sum(word in text for word in support_words)
        oppose_count = sum(word in text for word in oppose_words)

        if support_count > oppose_count:
            return "支持"
        elif oppose_count > support_count:
            return "谨慎/反对"
        else:
            return "中立"