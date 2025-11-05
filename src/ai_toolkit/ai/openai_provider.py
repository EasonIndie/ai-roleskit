"""
OpenAI provider implementation for AI Character Toolkit.
"""

import asyncio
from typing import Dict, List, Optional, Any, AsyncGenerator
import os

try:
    import openai
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None

from .base import (
    BaseAIProvider, AIRequest, AIResponse, AIModel,
    AIProviderError, AIProviderConnectionError,
    AIProviderAuthenticationError, AIProviderQuotaError,
    AIProviderModelError, AIProviderTimeoutError
)
from ..utils.logger import get_logger


class OpenAIProvider(BaseAIProvider):
    """OpenAI AI provider implementation."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize OpenAI provider.

        Args:
            config: OpenAI configuration
        """
        super().__init__(config)
        self.client = None
        self.logger = get_logger(__name__)

        if not OPENAI_AVAILABLE:
            raise AIProviderError("OpenAI library not installed. Install with: pip install openai")

    @property
    def provider_name(self) -> str:
        """Get provider name."""
        return "openai"

    @property
    def default_model(self) -> str:
        """Get default model name."""
        return self.config.get('model', 'gpt-4')

    async def initialize(self) -> None:
        """Initialize OpenAI client."""
        try:
            api_key = self.config.get('api_key') or os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise AIProviderAuthenticationError("OpenAI API key not provided")

            client_config = {
                'api_key': api_key,
                'timeout': self.config.get('timeout', 30)
            }

            # Optional configuration
            if self.config.get('base_url'):
                client_config['base_url'] = self.config['base_url']
            if self.config.get('organization'):
                client_config['organization'] = self.config['organization']

            self.client = AsyncOpenAI(**client_config)
            self.logger.info(f"OpenAI provider initialized with model: {self.default_model}")

        except Exception as e:
            self.logger.error(f"Failed to initialize OpenAI provider: {e}")
            raise AIProviderConnectionError(f"Failed to initialize OpenAI: {e}")

    async def chat_completion(self, request: AIRequest) -> AIResponse:
        """
        Generate chat completion using OpenAI.

        Args:
            request: AI request configuration

        Returns:
            AI response
        """
        if not self.client:
            await self.initialize()

        try:
            request = self._prepare_request(request)

            completion_params = {
                'model': self.config.get('model', self.default_model),
                'messages': request.messages,
                'max_tokens': request.max_tokens,
                'temperature': request.temperature,
            }

            # Optional parameters
            if request.top_p is not None:
                completion_params['top_p'] = request.top_p
            if request.stream:
                completion_params['stream'] = request.stream
            if request.stop:
                completion_params['stop'] = request.stop

            response = await self.client.chat.completions.create(**completion_params)

            return AIResponse(
                content=response.choices[0].message.content,
                role=response.choices[0].message.role,
                finish_reason=response.choices[0].finish_reason,
                usage={
                    'prompt_tokens': response.usage.prompt_tokens if response.usage else 0,
                    'completion_tokens': response.usage.completion_tokens if response.usage else 0,
                    'total_tokens': response.usage.total_tokens if response.usage else 0
                } if response.usage else None,
                metadata={
                    'model': response.model,
                    'created': response.created,
                    'id': response.id
                }
            )

        except openai.AuthenticationError as e:
            self.logger.error(f"OpenAI authentication error: {e}")
            raise AIProviderAuthenticationError(f"OpenAI authentication failed: {e}")
        except openai.RateLimitError as e:
            self.logger.error(f"OpenAI rate limit error: {e}")
            raise AIProviderQuotaError(f"OpenAI quota exceeded: {e}")
        except openai.APIError as e:
            self.logger.error(f"OpenAI API error: {e}")
            raise AIProviderError(f"OpenAI API error: {e}")
        except asyncio.TimeoutError as e:
            self.logger.error(f"OpenAI timeout error: {e}")
            raise AIProviderTimeoutError(f"OpenAI request timeout: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error in OpenAI chat completion: {e}")
            raise AIProviderError(f"Unexpected error: {e}")

    async def chat_completion_stream(self, request: AIRequest) -> AsyncGenerator[str, None]:
        """
        Generate streaming chat completion using OpenAI.

        Args:
            request: AI request configuration

        Yields:
            Response chunks
        """
        if not self.client:
            await self.initialize()

        try:
            request = self._prepare_request(request)

            completion_params = {
                'model': self.config.get('model', self.default_model),
                'messages': request.messages,
                'max_tokens': request.max_tokens,
                'temperature': request.temperature,
                'stream': True
            }

            # Optional parameters
            if request.top_p is not None:
                completion_params['top_p'] = request.top_p
            if request.stop:
                completion_params['stop'] = request.stop

            stream = await self.client.chat.completions.create(**completion_params)

            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

        except openai.AuthenticationError as e:
            self.logger.error(f"OpenAI authentication error: {e}")
            raise AIProviderAuthenticationError(f"OpenAI authentication failed: {e}")
        except openai.RateLimitError as e:
            self.logger.error(f"OpenAI rate limit error: {e}")
            raise AIProviderQuotaError(f"OpenAI quota exceeded: {e}")
        except openai.APIError as e:
            self.logger.error(f"OpenAI API error: {e}")
            raise AIProviderError(f"OpenAI API error: {e}")
        except asyncio.TimeoutError as e:
            self.logger.error(f"OpenAI timeout error: {e}")
            raise AIProviderTimeoutError(f"OpenAI request timeout: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error in OpenAI streaming: {e}")
            raise AIProviderError(f"Unexpected error: {e}")

    async def count_tokens(self, messages: List[Dict[str, str]]) -> int:
        """
        Count exact tokens in messages using OpenAI's tokenizer.

        Args:
            messages: List of messages

        Returns:
            Total token count
        """
        try:
            # Use tiktoken if available for accurate counting
            try:
                import tiktoken
                encoding = tiktoken.encoding_for_model(self.default_model)
            except ImportError:
                # Fallback to estimation
                return super().count_tokens(messages)

            total_tokens = 0
            for message in messages:
                total_tokens += len(encoding.encode(message.get('content', '')))

            return total_tokens

        except Exception as e:
            self.logger.warning(f"Error counting tokens with tiktoken: {e}, using estimation")
            return super().count_tokens(messages)

    def _load_models(self) -> List[AIModel]:
        """Load available OpenAI models."""
        return [
            AIModel(
                name="gpt-3.5-turbo",
                provider="openai",
                max_tokens=4096,
                supports_streaming=True,
                supports_function_calling=True,
                cost_per_token=0.000002  # Example pricing
            ),
            AIModel(
                name="gpt-4",
                provider="openai",
                max_tokens=8192,
                supports_streaming=True,
                supports_function_calling=True,
                cost_per_token=0.00003  # Example pricing
            ),
            AIModel(
                name="gpt-4-turbo",
                provider="openai",
                max_tokens=128000,
                supports_streaming=True,
                supports_function_calling=True,
                cost_per_token=0.00001  # Example pricing
            ),
        ]