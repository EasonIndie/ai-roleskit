"""
Character generation and management module for AI Character Toolkit.
"""

import asyncio
from typing import Dict, List, Optional, Any, Tuple
import uuid
from datetime import datetime

from ..models.schemas import (
    Character, CharacterType, CharacterInfo, CharacterContext,
    CharacterExpertise, CharacterBehavior, CharacterResponse
)
from ..ai.base import BaseAIProvider, AIRequest
from ..templates.prompts import template_manager
from ..utils.logger import get_logger, LogTimer
from ..utils.config import config


class CharacterGenerator:
    """Character generation manager."""

    def __init__(self, ai_provider: BaseAIProvider):
        """
        Initialize character generator.

        Args:
            ai_provider: AI provider for character generation
        """
        self.ai_provider = ai_provider
        self.logger = get_logger(__name__)

    async def generate_character(
        self,
        exploration_summary: Dict[str, Any],
        character_type: CharacterType,
        custom_requirements: Optional[str] = None
    ) -> Character:
        """
        Generate a character based on exploration results.

        Args:
            exploration_summary: Results from creative exploration
            character_type: Type of character to generate
            custom_requirements: Additional custom requirements

        Returns:
            Generated character
        """
        self.logger.info(f"Generating {character_type.value} character")

        with LogTimer(self.logger, f"Generate {character_type.value} character"):
            # Prepare generation prompt
            prompt = template_manager.render_template(
                'character_generation',
                exploration_summary=self._format_exploration_summary(exploration_summary),
                character_type=character_type.value
            )

            # Add custom requirements if provided
            if custom_requirements:
                prompt += f"\n\n**特殊要求：**\n{custom_requirements}"

            # Generate character specification
            request = AIRequest(
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"请生成一个详细的{character_type.value}角色定义。"}
                ],
                max_tokens=2000,
                temperature=0.7
            )

            try:
                response = await self.ai_provider.chat_completion(request)
                character_spec = await self._parse_character_specification(response.content, character_type)

                # Create character object
                character = Character(
                    name=character_spec['name'],
                    type=character_type,
                    description=character_spec.get('description', ''),
                    info=CharacterInfo(**character_spec.get('info', {})),
                    context=CharacterContext(**character_spec.get('context', {})),
                    expertise=CharacterExpertise(**character_spec.get('expertise', {})),
                    behavior=CharacterBehavior(**character_spec.get('behavior', {})),
                    response=CharacterResponse(**character_spec.get('response', {})),
                    tags=character_spec.get('tags', []),
                    metadata={
                        'generation_method': 'ai_assisted',
                        'exploration_summary': exploration_summary,
                        'generation_time': datetime.now().isoformat()
                    }
                )

                self.logger.info(f"Character generated: {character.name} ({character.type.value})")
                return character

            except Exception as e:
                self.logger.error(f"Error generating character: {e}")
                raise

    async def generate_character_set(
        self,
        exploration_summary: Dict[str, Any],
        custom_requirements: Optional[Dict[CharacterType, str]] = None
    ) -> List[Character]:
        """
        Generate a complete set of characters (user, expert, organization).

        Args:
            exploration_summary: Results from creative exploration
            custom_requirements: Custom requirements for each character type

        Returns:
            List of generated characters
        """
        self.logger.info("Generating complete character set")

        characters = []
        character_types = [CharacterType.USER, CharacterType.EXPERT, CharacterType.ORGANIZATION]

        for char_type in character_types:
            custom_req = custom_requirements.get(char_type) if custom_requirements else None
            character = await self.generate_character(exploration_summary, char_type, custom_req)
            characters.append(character)

        self.logger.info(f"Generated {len(characters)} characters")
        return characters

    async def refine_character(
        self,
        character: Character,
        refinement_feedback: str,
        refinement_aspect: Optional[str] = None
    ) -> Character:
        """
        Refine an existing character based on feedback.

        Args:
            character: Existing character to refine
            refinement_feedback: Feedback for refinement
            refinement_aspect: Specific aspect to refine (optional)

        Returns:
            Refined character
        """
        self.logger.info(f"Refining character: {character.name}")

        with LogTimer(self.logger, f"Refine {character.name}"):
            # Prepare refinement prompt
            prompt = f"""
            请基于以下反馈优化角色定义：

            **当前角色定义：**
            {self._format_character_for_refinement(character)}

            **优化反馈：**
            {refinement_feedback}

            **优化重点：** {refinement_aspect or '整体优化'}

            请提供优化后的完整角色定义，保持角色的核心特征和一致性。
            """

            request = AIRequest(
                messages=[
                    {"role": "system", "content": "你是角色优化专家，擅长根据反馈改进角色定义。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.6
            )

            try:
                response = await self.ai_provider.chat_completion(request)
                refined_spec = await self._parse_character_specification(response.content, character.type)

                # Update character with refined data
                character.info = CharacterInfo(**refined_spec.get('info', character.info.__dict__))
                character.context = CharacterContext(**refined_spec.get('context', character.context.__dict__))
                character.expertise = CharacterExpertise(**refined_spec.get('expertise', character.expertise.__dict__))
                character.behavior = CharacterBehavior(**refined_spec.get('behavior', character.behavior.__dict__))
                character.response = CharacterResponse(**refined_spec.get('response', character.response.__dict__))
                character.update_timestamp()

                # Add refinement history
                if 'refinement_history' not in character.metadata:
                    character.metadata['refinement_history'] = []

                character.metadata['refinement_history'].append({
                    'timestamp': datetime.now().isoformat(),
                    'feedback': refinement_feedback,
                    'aspect': refinement_aspect
                })

                self.logger.info(f"Character refined: {character.name}")
                return character

            except Exception as e:
                self.logger.error(f"Error refining character: {e}")
                raise

    async def create_character_from_template(
        self,
        template_name: str,
        character_type: CharacterType,
        customizations: Dict[str, Any]
    ) -> Character:
        """
        Create character from predefined template.

        Args:
            template_name: Name of template to use
            character_type: Type of character
            customizations: Custom modifications to template

        Returns:
            Created character
        """
        self.logger.info(f"Creating character from template: {template_name}")

        # Get template
        template = await self._load_character_template(template_name, character_type)
        if not template:
            raise ValueError(f"Template not found: {template_name}")

        # Apply customizations
        for key, value in customizations.items():
            if hasattr(template, key):
                setattr(template, key, value)

        template.update_timestamp()
        return template

    def get_character_prompt(self, character: Character) -> str:
        """
        Get the full prompt for character interaction.

        Args:
            character: Character to get prompt for

        Returns:
            Complete character prompt
        """
        template_map = {
            CharacterType.USER: 'user_character',
            CharacterType.EXPERT: 'expert_character',
            CharacterType.ORGANIZATION: 'organization_character'
        }

        template_name = template_map.get(character.type, 'user_character')

        return template_manager.render_template(
            template_name,
            character=character,
            character_name=character.name
        )

    async def validate_character(self, character: Character) -> Dict[str, Any]:
        """
        Validate character completeness and consistency.

        Args:
            character: Character to validate

        Returns:
            Validation results
        """
        self.logger.info(f"Validating character: {character.name}")

        validation_results = {
            'is_valid': True,
            'completeness_score': 0,
            'consistency_score': 0,
            'issues': [],
            'suggestions': []
        }

        # Check completeness
        required_fields = [
            'name', 'info.name', 'context.current_situation',
            'expertise.professional_field', 'behavior.decision_style'
        ]

        missing_fields = []
        for field in required_fields:
            if not self._get_nested_field(character, field):
                missing_fields.append(field)

        completeness_score = (len(required_fields) - len(missing_fields)) / len(required_fields)
        validation_results['completeness_score'] = completeness_score

        if missing_fields:
            validation_results['issues'].append(f"Missing required fields: {missing_fields}")

        # Check consistency
        consistency_issues = await self._check_character_consistency(character)
        validation_results['consistency_score'] = max(0, 1.0 - len(consistency_issues) * 0.2)
        validation_results['issues'].extend(consistency_issues)

        # Overall validation
        validation_results['is_valid'] = (
            validation_results['completeness_score'] >= 0.8 and
            validation_results['consistency_score'] >= 0.7
        )

        # Generate suggestions
        if validation_results['completeness_score'] < 0.8:
            validation_results['suggestions'].append("Consider adding more detailed character information")

        if validation_results['consistency_score'] < 0.7:
            validation_results['suggestions'].append("Review character consistency and alignment")

        return validation_results

    async def _parse_character_specification(
        self,
        response: str,
        character_type: CharacterType
    ) -> Dict[str, Any]:
        """Parse character specification from AI response."""
        # In production, use structured extraction or parsing
        # For now, return a basic structure
        return {
            'name': f"{character_type.value.title()} Character",
            'description': response[:200] + "..." if len(response) > 200 else response,
            'info': {
                'name': f"{character_type.value.title()} Character",
                'age': '30-40',
                'position': self._get_default_position(character_type),
                'background': 'Experienced professional',
                'experience': '5+ years'
            },
            'context': {
                'current_situation': 'Exploring new opportunities',
                'goals': 'To provide valuable insights',
                'challenges': 'Complex problem solving',
                'resource_constraints': 'Time and information limitations'
            },
            'expertise': {
                'professional_field': self._get_default_field(character_type),
                'special_skills': 'Analysis and communication',
                'experience_level': 'Senior level',
                'industry_insights': 'Deep industry knowledge'
            },
            'behavior': {
                'decision_style': 'Analytical and collaborative',
                'risk_preference': 'Moderate risk tolerance',
                'communication_style': 'Clear and constructive',
                'values': 'Integrity and excellence'
            },
            'response': {
                'focus_areas': 'Practical solutions and insights',
                'avoidance_areas': 'Speculation without evidence',
                'expression_style': 'Professional and direct',
                'expected_outcomes': 'Actionable recommendations'
            },
            'tags': [character_type.value, 'generated']
        }

    def _format_exploration_summary(self, summary: Dict[str, Any]) -> str:
        """Format exploration summary for character generation."""
        return f"""
        初始想法：{summary.get('initial_idea', 'N/A')}

        关键洞察：{', '.join(summary.get('key_insights', []))}

        识别的利益相关者：{len(summary.get('stakeholders', []))} 个群体

        需要的知识领域：{', '.join([k.get('area', '') for k in summary.get('knowledge_areas', [])])}

        实施环境：{summary.get('implementation_context', {}).get('organization_type', 'N/A')}
        """

    def _format_character_for_refinement(self, character: Character) -> str:
        """Format character for refinement prompt."""
        return f"""
        角色名称：{character.name}
        角色类型：{character.type.value}

        基本信息：
        - 职位：{character.info.position}
        - 背景：{character.info.background}

        当前情况：{character.context.current_situation}
        目标：{character.context.goals}

        专业领域：{character.expertise.professional_field}
        特殊技能：{character.expertise.special_skills}

        决策风格：{character.behavior.decision_style}
        沟通风格：{character.behavior.communication_style}

        关注点：{character.response.focus_areas}
        表达方式：{character.response.expression_style}
        """

    def _get_nested_field(self, obj: Any, field_path: str) -> Any:
        """Get nested field value from object."""
        parts = field_path.split('.')
        current = obj

        for part in parts:
            if hasattr(current, part):
                current = getattr(current, part)
            elif isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None

        return current if current else None

    def _get_default_position(self, character_type: CharacterType) -> str:
        """Get default position for character type."""
        defaults = {
            CharacterType.USER: "End User",
            CharacterType.EXPERT: "Domain Expert",
            CharacterType.ORGANIZATION: "Business Manager"
        }
        return defaults.get(character_type, "Professional")

    def _get_default_field(self, character_type: CharacterType) -> str:
        """Get default professional field for character type."""
        defaults = {
            CharacterType.USER: "User Experience",
            CharacterType.EXPERT: "Technology and Innovation",
            CharacterType.ORGANIZATION: "Business Strategy"
        }
        return defaults.get(character_type, "General")

    async def _load_character_template(
        self,
        template_name: str,
        character_type: CharacterType
    ) -> Optional[Character]:
        """Load character template from storage."""
        # In production, load from template storage
        return None

    async def _check_character_consistency(self, character: Character) -> List[str]:
        """Check character internal consistency."""
        issues = []

        # Check if expertise matches background
        if (character.expertise.professional_field and
            character.info.background and
            character.expertise.professional_field.lower() not in character.info.background.lower()):
            issues.append("Expertise field may not align with background")

        # Check if goals are realistic given constraints
        if (character.context.goals and character.context.resource_constraints and
            "ambitious" in character.context.goals.lower() and
            "limited" in character.context.resource_constraints.lower()):
            issues.append("Goals may be too ambitious given resource constraints")

        return issues


class CharacterManager:
    """Character management and operations."""

    def __init__(self, ai_provider: BaseAIProvider):
        """
        Initialize character manager.

        Args:
            ai_provider: AI provider for character operations
        """
        self.ai_provider = ai_provider
        self.generator = CharacterGenerator(ai_provider)
        self.logger = get_logger(__name__)
        self.characters: Dict[str, Character] = {}

    async def create_character(
        self,
        exploration_summary: Dict[str, Any],
        character_type: CharacterType,
        name: Optional[str] = None
    ) -> Character:
        """
        Create and store a new character.

        Args:
            exploration_summary: Exploration results
            character_type: Type of character
            name: Optional custom name

        Returns:
            Created character
        """
        character = await self.generator.generate_character(exploration_summary, character_type)

        if name:
            character.name = name

        self.characters[character.id] = character
        self.logger.info(f"Character created and stored: {character.name}")

        return character

    async def get_character(self, character_id: str) -> Optional[Character]:
        """
        Get character by ID.

        Args:
            character_id: Character ID

        Returns:
            Character if found, None otherwise
        """
        return self.characters.get(character_id)

    async def update_character(self, character: Character) -> bool:
        """
        Update character in storage.

        Args:
            character: Updated character

        Returns:
            True if updated successfully
        """
        if character.id in self.characters:
            self.characters[character.id] = character
            character.update_timestamp()
            self.logger.info(f"Character updated: {character.name}")
            return True
        return False

    async def delete_character(self, character_id: str) -> bool:
        """
        Delete character from storage.

        Args:
            character_id: Character ID to delete

        Returns:
            True if deleted successfully
        """
        if character_id in self.characters:
            character_name = self.characters[character_id].name
            del self.characters[character_id]
            self.logger.info(f"Character deleted: {character_name}")
            return True
        return False

    async def list_characters(
        self,
        character_type: Optional[CharacterType] = None
    ) -> List[Character]:
        """
        List all characters, optionally filtered by type.

        Args:
            character_type: Optional type filter

        Returns:
            List of characters
        """
        characters = list(self.characters.values())

        if character_type:
            characters = [c for c in characters if c.type == character_type]

        return characters

    async def search_characters(self, query: str) -> List[Character]:
        """
        Search characters by name or description.

        Args:
            query: Search query

        Returns:
            Matching characters
        """
        query_lower = query.lower()
        results = []

        for character in self.characters.values():
            if (query_lower in character.name.lower() or
                query_lower in character.description.lower() or
                any(query_lower in tag.lower() for tag in character.tags)):
                results.append(character)

        return results