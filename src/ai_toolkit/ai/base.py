"""
Base classes for AI providers in the AI Character Toolkit.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, AsyncGenerator
from dataclasses import dataclass
import asyncio

from ..models.schemas import Message, DialogueRole


@dataclass
class AIRequest:
    """AI request configuration."""
    messages: List[Dict[str, str]]
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    stream: bool = False
    stop: Optional[List[str]] = None
    metadata: Dict[str, Any] = None


@dataclass
class AIResponse:
    """AI response data."""
    content: str
    role: str = "assistant"
    finish_reason: Optional[str] = None
    usage: Optional[Dict[str, int]] = None
    metadata: Dict[str, Any] = None


@dataclass
class AIModel:
    """AI model information."""
    name: str
    provider: str
    max_tokens: int
    supports_streaming: bool = False
    supports_function_calling: bool = False
    cost_per_token: Optional[float] = None


class BaseAIProvider(ABC):
    """Abstract base class for AI providers."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize AI provider.

        Args:
            config: Provider configuration
        """
        self.config = config
        self._models = None

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Get provider name."""
        pass

    @property
    @abstractmethod
    def default_model(self) -> str:
        """Get default model name."""
        pass

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the AI provider."""
        pass

    @abstractmethod
    async def chat_completion(self, request: AIRequest) -> AIResponse:
        """
        Generate chat completion.

        Args:
            request: AI request configuration

        Returns:
            AI response
        """
        pass

    @abstractmethod
    async def chat_completion_stream(self, request: AIRequest) -> AsyncGenerator[str, None]:
        """
        Generate streaming chat completion.

        Args:
            request: AI request configuration

        Yields:
            Response chunks
        """
        pass

    async def validate_connection(self) -> bool:
        """
        Validate connection to AI provider.

        Returns:
            True if connection is valid
        """
        try:
            test_request = AIRequest(
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            response = await self.chat_completion(test_request)
            return bool(response.content)
        except Exception:
            return False

    def get_available_models(self) -> List[AIModel]:
        """
        Get list of available models.

        Returns:
            List of available AI models
        """
        if self._models is None:
            self._models = self._load_models()
        return self._models

    @abstractmethod
    def _load_models(self) -> List[AIModel]:
        """Load available models for this provider."""
        pass

    def _prepare_request(self, request: AIRequest) -> AIRequest:
        """
        Prepare request with provider-specific defaults.

        Args:
            request: Original request

        Returns:
            Prepared request
        """
        # Apply provider defaults if not specified
        if request.max_tokens is None:
            request.max_tokens = self.config.get('max_tokens', 2000)
        if request.temperature is None:
            request.temperature = self.config.get('temperature', 0.7)
        if request.top_p is None:
            request.top_p = self.config.get('top_p', 1.0)

        return request

    def _format_messages(self, messages: List[Message]) -> List[Dict[str, str]]:
        """
        Format Message objects to provider format.

        Args:
            messages: List of Message objects

        Returns:
            Formatted messages for provider
        """
        return [
            {
                "role": msg.role.value,
                "content": msg.content
            }
            for msg in messages
        ]

    async def chat_with_character(
        self,
        messages: List[Message],
        character_prompt: str,
        **kwargs
    ) -> AIResponse:
        """
        Chat with character-specific prompt.

        Args:
            messages: Conversation history
            character_prompt: Character-specific system prompt
            **kwargs: Additional request parameters

        Returns:
            AI response
        """
        # Combine character prompt with messages
        all_messages = [{"role": "system", "content": character_prompt}]
        all_messages.extend(self._format_messages(messages))

        request = AIRequest(
            messages=all_messages,
            **kwargs
        )

        return await self.chat_completion(request)

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text.

        Args:
            text: Input text

        Returns:
            Estimated token count
        """
        # Simple estimation: ~4 characters per token
        # Override in provider-specific implementations for better accuracy
        return len(text) // 4

    async def count_tokens(self, messages: List[Dict[str, str]]) -> int:
        """
        Count exact tokens in messages.

        Args:
            messages: List of messages

        Returns:
            Total token count
        """
        # Default implementation uses estimation
        total_text = " ".join(msg.get("content", "") for msg in messages)
        return self.estimate_tokens(total_text)

    def get_model_info(self, model_name: Optional[str] = None) -> Optional[AIModel]:
        """
        Get information about a specific model.

        Args:
            model_name: Model name (uses default if not provided)

        Returns:
            Model information or None if not found
        """
        model_name = model_name or self.default_model
        for model in self.get_available_models():
            if model.name == model_name:
                return model
        return None

    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        # Cleanup if needed
        pass


class AIProviderError(Exception):
    """Base exception for AI provider errors."""
    pass


class AIProviderConnectionError(AIProviderError):
    """Exception raised for connection errors."""
    pass


class AIProviderAuthenticationError(AIProviderError):
    """Exception raised for authentication errors."""
    pass


class AIProviderQuotaError(AIProviderError):
    """Exception raised for quota/rate limit errors."""
    pass


class AIProviderModelError(AIProviderError):
    """Exception raised for model-related errors."""
    pass


class AIProviderTimeoutError(AIProviderError):
    """Exception raised for timeout errors."""
    pass