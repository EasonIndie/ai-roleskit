"""
Dialogue management module for AI Character Toolkit.
"""

import asyncio
from typing import Dict, List, Optional, Any, AsyncGenerator
import uuid
from datetime import datetime

from ..models.schemas import Dialogue, Message, DialogueRole, Character
from ..ai.base import BaseAIProvider, AIRequest
from ..templates.prompts import template_manager
from ..utils.logger import get_logger, LogTimer
from ..utils.config import config
from .character import CharacterManager


class DialogueManager:
    """Dialogue session manager."""

    def __init__(self, ai_provider: BaseAIProvider, character_manager: CharacterManager):
        """
        Initialize dialogue manager.

        Args:
            ai_provider: AI provider for dialogue
            character_manager: Character manager for character data
        """
        self.ai_provider = ai_provider
        self.character_manager = character_manager
        self.logger = get_logger(__name__)
        self.dialogues: Dict[str, Dialogue] = {}
        self.max_history = config.get('dialogue.max_history', 50)
        self.context_window = config.get('dialogue.context_window', 10)

    async def create_dialogue(
        self,
        character_id: str,
        title: Optional[str] = None
    ) -> Dialogue:
        """
        Create a new dialogue session.

        Args:
            character_id: ID of character to dialogue with
            title: Optional dialogue title

        Returns:
            Created dialogue session
        """
        # Get character
        character = await self.character_manager.get_character(character_id)
        if not character:
            raise ValueError(f"Character not found: {character_id}")

        # Create dialogue
        dialogue = Dialogue(
            character_id=character_id,
            title=title or f"Dialogue with {character.name}",
            metadata={
                'character_name': character.name,
                'character_type': character.type.value
            }
        )

        self.dialogues[dialogue.id] = dialogue
        self.logger.info(f"Dialogue created: {dialogue.id} with {character.name}")

        return dialogue

    async def send_message(
        self,
        dialogue_id: str,
        content: str,
        role: DialogueRole = DialogueRole.USER
    ) -> Message:
        """
        Send a message in dialogue.

        Args:
            dialogue_id: Dialogue session ID
            content: Message content
            role: Message role (default: user)

        Returns:
            AI response message
        """
        if dialogue_id not in self.dialogues:
            raise ValueError(f"Dialogue not found: {dialogue_id}")

        dialogue = self.dialogues[dialogue_id]
        character = await self.character_manager.get_character(dialogue.character_id)

        if not character:
            raise ValueError(f"Character not found: {dialogue.character_id}")

        # Add user message
        user_message = Message(
            role=role,
            content=content
        )
        dialogue.add_message(user_message)

        # Get character response
        with LogTimer(self.logger, f"Generate response for {dialogue_id}"):
            response_message = await self._generate_character_response(
                character, dialogue, content
            )

            dialogue.add_message(response_message)

        self.logger.info(f"Message exchanged in dialogue {dialogue_id}")
        return response_message

    async def send_message_stream(
        self,
        dialogue_id: str,
        content: str,
        role: DialogueRole = DialogueRole.USER
    ) -> AsyncGenerator[str, None]:
        """
        Send message and get streaming response.

        Args:
            dialogue_id: Dialogue session ID
            content: Message content
            role: Message role

        Yields:
            Response chunks
        """
        if dialogue_id not in self.dialogues:
            raise ValueError(f"Dialogue not found: {dialogue_id}")

        dialogue = self.dialogues[dialogue_id]
        character = await self.character_manager.get_character(dialogue.character_id)

        if not character:
            raise ValueError(f"Character not found: {dialogue.character_id}")

        # Add user message
        user_message = Message(
            role=role,
            content=content
        )
        dialogue.add_message(user_message)

        # Stream character response
        response_chunks = []
        async for chunk in self._generate_character_response_stream(character, dialogue, content):
            response_chunks.append(chunk)
            yield chunk

        # Add complete response to dialogue
        full_response = ''.join(response_chunks)
        response_message = Message(
            role=DialogueRole.ASSISTANT,
            content=full_response
        )
        dialogue.messages[-1] = response_message  # Replace last message

        self.logger.info(f"Streaming message completed in dialogue {dialogue_id}")

    async def get_dialogue(self, dialogue_id: str) -> Optional[Dialogue]:
        """
        Get dialogue by ID.

        Args:
            dialogue_id: Dialogue ID

        Returns:
            Dialogue if found, None otherwise
        """
        return self.dialogues.get(dialogue_id)

    async def get_dialogue_history(
        self,
        dialogue_id: str,
        limit: Optional[int] = None
    ) -> List[Message]:
        """
        Get dialogue message history.

        Args:
            dialogue_id: Dialogue ID
            limit: Optional message limit

        Returns:
            List of messages
        """
        if dialogue_id not in self.dialogues:
            return []

        dialogue = self.dialogues[dialogue_id]
        messages = dialogue.messages

        if limit:
            messages = messages[-limit:]

        return messages

    async def continue_dialogue(
        self,
        dialogue_id: str,
        prompt: Optional[str] = None
    ) -> Message:
        """
        Continue dialogue with optional prompt.

        Args:
            dialogue_id: Dialogue ID
            prompt: Optional continuation prompt

        Returns:
            AI response message
        """
        if not prompt:
            prompt = "请继续我们的对话，或者如果你认为有重要的点需要讨论，请提出。"

        return await self.send_message(dialogue_id, prompt)

    async def summarize_dialogue(self, dialogue_id: str) -> Dict[str, Any]:
        """
        Generate dialogue summary.

        Args:
            dialogue_id: Dialogue ID

        Returns:
            Dialogue summary
        """
        if dialogue_id not in self.dialogues:
            raise ValueError(f"Dialogue not found: {dialogue_id}")

        dialogue = self.dialogues[dialogue_id]
        character = await self.character_manager.get_character(dialogue.character_id)

        if not character:
            raise ValueError(f"Character not found: {dialogue.character_id}")

        # Prepare messages for summarization
        messages_text = '\n'.join([
            f"{msg.role.value}: {msg.content}" for msg in dialogue.messages[-20:]  # Last 20 messages
        ])

        summary_prompt = f"""
        请总结以下对话的主要内容：

        角色：{character.name} ({character.type.value})
        对话历史：
        {messages_text}

        请提供：
        1. 主要讨论话题
        2. 关键洞察和观点
        3. 提出的建议或解决方案
        4. 待解决的问题
        5. 对话的整体评价

        请以结构化的方式回应。
        """

        with LogTimer(self.logger, f"Summarize dialogue {dialogue_id}"):
            request = AIRequest(
                messages=[
                    {"role": "system", "content": "你是对话分析专家，擅长总结和提炼对话要点。"},
                    {"role": "user", "content": summary_prompt}
                ],
                max_tokens=1000,
                temperature=0.5
            )

            response = await self.ai_provider.chat_completion(request)

            summary = {
                'dialogue_id': dialogue_id,
                'character_name': character.name,
                'character_type': character.type.value,
                'message_count': len(dialogue.messages),
                'duration': self._calculate_dialogue_duration(dialogue),
                'summary_text': response.content,
                'key_topics': self._extract_key_topics(response.content),
                'sentiment': self._analyze_sentiment(dialogue.messages)
            }

            return summary

    async def delete_dialogue(self, dialogue_id: str) -> bool:
        """
        Delete dialogue.

        Args:
            dialogue_id: Dialogue ID to delete

        Returns:
            True if deleted successfully
        """
        if dialogue_id in self.dialogues:
            del self.dialogues[dialogue_id]
            self.logger.info(f"Dialogue deleted: {dialogue_id}")
            return True
        return False

    async def list_dialogues(
        self,
        character_id: Optional[str] = None
    ) -> List[Dialogue]:
        """
        List dialogues, optionally filtered by character.

        Args:
            character_id: Optional character filter

        Returns:
            List of dialogues
        """
        dialogues = list(self.dialogues.values())

        if character_id:
            dialogues = [d for d in dialogues if d.character_id == character_id]

        return dialogues

    async def search_dialogues(self, query: str) -> List[Dialogue]:
        """
        Search dialogues by content.

        Args:
            query: Search query

        Returns:
            Matching dialogues
        """
        query_lower = query.lower()
        results = []

        for dialogue in self.dialogues.values():
            if (query_lower in dialogue.title.lower() or
                any(query_lower in msg.content.lower() for msg in dialogue.messages)):
                results.append(dialogue)

        return results

    async def _generate_character_response(
        self,
        character: Character,
        dialogue: Dialogue,
        user_message: str
    ) -> Message:
        """Generate character response using AI."""
        # Get character prompt
        character_prompt = self.character_manager.generator.get_character_prompt(character)

        # Get relevant context
        context_messages = dialogue.get_last_messages(self.context_window)
        history = self._format_messages_for_ai(context_messages)

        # Render dialogue template
        prompt = template_manager.render_template(
            'dialogue_response',
            character_name=character.name,
            character_prompt=character_prompt,
            user_message=user_message,
            history=history
        )

        # Generate response
        request = AIRequest(
            messages=[
                {"role": "system", "content": character_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=config.get('dialogue.max_tokens', 1500),
            temperature=config.get('dialogue.temperature', 0.7)
        )

        response = await self.ai_provider.chat_completion(request)

        return Message(
            role=DialogueRole.ASSISTANT,
            content=response.content,
            metadata={
                'character_id': character.id,
                'model_used': response.metadata.get('model') if response.metadata else None,
                'tokens_used': response.usage.get('total_tokens') if response.usage else None
            }
        )

    async def _generate_character_response_stream(
        self,
        character: Character,
        dialogue: Dialogue,
        user_message: str
    ) -> AsyncGenerator[str, None]:
        """Generate streaming character response."""
        character_prompt = self.character_manager.generator.get_character_prompt(character)
        context_messages = dialogue.get_last_messages(self.context_window)
        history = self._format_messages_for_ai(context_messages)

        prompt = template_manager.render_template(
            'dialogue_response',
            character_name=character.name,
            character_prompt=character_prompt,
            user_message=user_message,
            history=history
        )

        request = AIRequest(
            messages=[
                {"role": "system", "content": character_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=config.get('dialogue.max_tokens', 1500),
            temperature=config.get('dialogue.temperature', 0.7),
            stream=True
        )

        async for chunk in self.ai_provider.chat_completion_stream(request):
            yield chunk

    def _format_messages_for_ai(self, messages: List[Message]) -> str:
        """Format messages for AI context."""
        formatted = []
        for msg in messages:
            formatted.append(f"{msg.role.value}: {msg.content}")
        return '\n'.join(formatted)

    def _calculate_dialogue_duration(self, dialogue: Dialogue) -> str:
        """Calculate dialogue duration."""
        if len(dialogue.messages) < 2:
            return "0:00"

        start_time = dialogue.messages[0].timestamp
        end_time = dialogue.messages[-1].timestamp
        duration = end_time - start_time

        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        seconds = duration.seconds % 60

        return f"{hours}:{minutes:02d}:{seconds:02d}"

    def _extract_key_topics(self, summary_text: str) -> List[str]:
        """Extract key topics from summary."""
        # Simple extraction - in production, use NLP
        topics = []
        if "技术" in summary_text:
            topics.append("技术讨论")
        if "用户" in summary_text:
            topics.append("用户体验")
        if "商业" in summary_text:
            topics.append("商业模式")
        if "风险" in summary_text:
            topics.append("风险管理")

        return topics or ["综合讨论"]

    def _analyze_sentiment(self, messages: List[Message]) -> str:
        """Analyze dialogue sentiment."""
        # Simple sentiment analysis - in production, use proper NLP
        positive_words = ["好", "棒", "优秀", "同意", "支持"]
        negative_words = ["问题", "困难", "挑战", "担心", "不好"]

        positive_count = sum(
            sum(word in msg.content for word in positive_words)
            for msg in messages
        )
        negative_count = sum(
            sum(word in msg.content for word in negative_words)
            for msg in messages
        )

        if positive_count > negative_count:
            return "积极"
        elif negative_count > positive_count:
            return "谨慎"
        else:
            return "中性"