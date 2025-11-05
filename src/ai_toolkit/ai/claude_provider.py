"""
Claude (Anthropic) provider implementation for AI Character Toolkit.
"""

import asyncio
from typing import Dict, List, Optional, Any, AsyncGenerator
import os

try:
    import anthropic
    from anthropic import AsyncAnthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    anthropic = None

from .base import (
    BaseAIProvider, AIRequest, AIResponse, AIModel,
    AIProviderError, AIProviderConnectionError,
    AIProviderAuthenticationError, AIProviderQuotaError,
    AIProviderModelError, AIProviderTimeoutError
)
from ..utils.logger import get_logger


class ClaudeProvider(BaseAIProvider):
    """Claude AI provider implementation."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Claude provider.

        Args:
            config: Claude configuration
        """
        super().__init__(config)
        self.client = None
        self.logger = get_logger(__name__)

        if not ANTHROPIC_AVAILABLE:
            raise AIProviderError("Anthropic library not installed. Install with: pip install anthropic")

    @property
    def provider_name(self) -> str:
        """Get provider name."""
        return "claude"

    @property
    def default_model(self) -> str:
        """Get default model name."""
        return self.config.get('model', 'claude-3-sonnet-20240229')

    async def initialize(self) -> None:
        """Initialize Anthropic client."""
        try:
            api_key = self.config.get('api_key') or os.getenv('CLAUDE_API_KEY') or os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                raise AIProviderAuthenticationError("Claude API key not provided")

            client_config = {
                'api_key': api_key,
                'timeout': self.config.get('timeout', 30)
            }

            # Optional base_url for custom endpoints
            if self.config.get('base_url'):
                client_config['base_url'] = self.config['base_url']

            self.client = AsyncAnthropic(**client_config)
            self.logger.info(f"Claude provider initialized with model: {self.default_model}")

        except Exception as e:
            self.logger.error(f"Failed to initialize Claude provider: {e}")
            raise AIProviderConnectionError(f"Failed to initialize Claude: {e}")

    def _convert_messages_to_claude_format(self, messages: List[Dict[str, str]]) -> tuple:
        """
        Convert OpenAI-style messages to Claude format.

        Args:
            messages: List of messages in OpenAI format

        Returns:
            Tuple of (system_message, claude_messages)
        """
        system_message = ""
        claude_messages = []

        for message in messages:
            if message['role'] == 'system':
                system_message = message['content']
            else:
                claude_messages.append({
                    'role': message['role'],
                    'content': message['content']
                })

        return system_message, claude_messages

    async def chat_completion(self, request: AIRequest) -> AIResponse:
        """
        Generate chat completion using Claude.

        Args:
            request: AI request configuration

        Returns:
            AI response
        """
        if not self.client:
            await self.initialize()

        try:
            request = self._prepare_request(request)

            # Convert messages to Claude format
            system_message, claude_messages = self._convert_messages_to_claude_format(request.messages)

            completion_params = {
                'model': self.config.get('model', self.default_model),
                'messages': claude_messages,
                'max_tokens': request.max_tokens,
                'temperature': request.temperature,
            }

            # Add system message if present
            if system_message:
                completion_params['system'] = system_message

            # Optional parameters
            if request.top_p is not None:
                completion_params['top_p'] = request.top_p
            if request.stop:
                completion_params['stop_sequences'] = request.stop

            response = await self.client.messages.create(**completion_params)

            # Extract content from response
            content = ""
            if response.content and len(response.content) > 0:
                content = response.content[0].text

            return AIResponse(
                content=content,
                role="assistant",
                finish_reason=response.stop_reason,
                usage={
                    'prompt_tokens': response.usage.input_tokens if response.usage else 0,
                    'completion_tokens': response.usage.output_tokens if response.usage else 0,
                    'total_tokens': (response.usage.input_tokens + response.usage.output_tokens) if response.usage else 0
                } if response.usage else None,
                metadata={
                    'model': response.model,
                    'id': response.id,
                    'stop_reason': response.stop_reason
                }
            )

        except anthropic.AuthenticationError as e:
            self.logger.error(f"Claude authentication error: {e}")
            raise AIProviderAuthenticationError(f"Claude authentication failed: {e}")
        except anthropic.RateLimitError as e:
            self.logger.error(f"Claude rate limit error: {e}")
            raise AIProviderQuotaError(f"Claude quota exceeded: {e}")
        except anthropic.APIError as e:
            self.logger.error(f"Claude API error: {e}")
            raise AIProviderError(f"Claude API error: {e}")
        except asyncio.TimeoutError as e:
            self.logger.error(f"Claude timeout error: {e}")
            raise AIProviderTimeoutError(f"Claude request timeout: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error in Claude chat completion: {e}")
            raise AIProviderError(f"Unexpected error: {e}")

    async def chat_completion_stream(self, request: AIRequest) -> AsyncGenerator[str, None]:
        """
        Generate streaming chat completion using Claude.

        Args:
            request: AI request configuration

        Yields:
            Response chunks
        """
        if not self.client:
            await self.initialize()

        try:
            request = self._prepare_request(request)

            # Convert messages to Claude format
            system_message, claude_messages = self._convert_messages_to_claude_format(request.messages)

            completion_params = {
                'model': self.config.get('model', self.default_model),
                'messages': claude_messages,
                'max_tokens': request.max_tokens,
                'temperature': request.temperature,
                'stream': True
            }

            # Add system message if present
            if system_message:
                completion_params['system'] = system_message

            # Optional parameters
            if request.top_p is not None:
                completion_params['top_p'] = request.top_p
            if request.stop:
                completion_params['stop_sequences'] = request.stop

            async with self.client.messages.stream(**completion_params) as stream:
                async for text in stream.text_stream:
                    yield text

        except anthropic.AuthenticationError as e:
            self.logger.error(f"Claude authentication error: {e}")
            raise AIProviderAuthenticationError(f"Claude authentication failed: {e}")
        except anthropic.RateLimitError as e:
            self.logger.error(f"Claude rate limit error: {e}")
            raise AIProviderQuotaError(f"Claude quota exceeded: {e}")
        except anthropic.APIError as e:
            self.logger.error(f"Claude API error: {e}")
            raise AIProviderError(f"Claude API error: {e}")
        except asyncio.TimeoutError as e:
            self.logger.error(f"Claude timeout error: {e}")
            raise AIProviderTimeoutError(f"Claude request timeout: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error in Claude streaming: {e}")
            raise AIProviderError(f"Unexpected error: {e}")

    async def count_tokens(self, messages: List[Dict[str, str]]) -> int:
        """
        Count exact tokens in messages using Claude's token counting.

        Args:
            messages: List of messages

        Returns:
            Total token count
        """
        try:
            if not self.client:
                await self.initialize()

            # Convert messages to Claude format
            system_message, claude_messages = self._convert_messages_to_claude_format(messages)

            # Use Claude's count_tokens method if available
            try:
                # Count system message tokens
                total_tokens = 0
                if system_message:
                    system_response = await self.client.messages.count_tokens(
                        model=self.default_model,
                        messages=[{"role": "user", "content": system_message}]
                    )
                    total_tokens += system_response.input_tokens

                # Count conversation messages tokens
                if claude_messages:
                    conversation_response = await self.client.messages.count_tokens(
                        model=self.default_model,
                        messages=claude_messages
                    )
                    total_tokens += conversation_response.input_tokens

                return total_tokens

            except AttributeError:
                # Fallback to estimation if count_tokens not available
                return super().count_tokens(messages)

        except Exception as e:
            self.logger.warning(f"Error counting tokens with Claude: {e}, using estimation")
            return super().count_tokens(messages)

    def _load_models(self) -> List[AIModel]:
        """Load available Claude models."""
        return [
            AIModel(
                name="claude-3-haiku-20240307",
                provider="claude",
                max_tokens=200000,
                supports_streaming=True,
                supports_function_calling=True,
                cost_per_token=0.00000025  # Example pricing
            ),
            AIModel(
                name="claude-3-sonnet-20240229",
                provider="claude",
                max_tokens=200000,
                supports_streaming=True,
                supports_function_calling=True,
                cost_per_token=0.000003  # Example pricing
            ),
            AIModel(
                name="claude-3-opus-20240229",
                provider="claude",
                max_tokens=200000,
                supports_streaming=True,
                supports_function_calling=True,
                cost_per_token=0.000015  # Example pricing
            ),
        ]