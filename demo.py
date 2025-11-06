#!/usr/bin/env python3
"""
AI Character Toolkit Demo (ASCII version)
"""

import asyncio
import os
import sys

# Add src to path
sys.path.insert(0, './src')

from ai_toolkit.utils.config import config
from ai_toolkit.utils.logger import get_logger
from ai_toolkit.ai.base import BaseAIProvider, AIRequest, AIResponse, AIModel
from ai_toolkit.core.character import CharacterManager
from ai_toolkit.core.exploration import CreativeExplorer
from ai_toolkit.core.dialogue import DialogueManager
from ai_toolkit.storage.file_storage import FileStorage
from ai_toolkit.models.schemas import CharacterType, Character, CharacterInfo


class MockAIProvider(BaseAIProvider):
    """Mock AI provider for demonstration"""

    def __init__(self, config):
        super().__init__(config)

    @property
    def provider_name(self) -> str:
        return "Mock Provider"

    @property
    def default_model(self) -> str:
        return "mock-model"

    async def initialize(self) -> None:
        """Initialize the AI provider"""
        pass

    def _load_models(self):
        """Load available models for this provider"""
        return [
            AIModel(
                name="mock-model",
                provider="mock",
                max_tokens=2000,
                supports_streaming=False,
                supports_function_calling=False
            )
        ]

    async def chat_completion(self, request: AIRequest) -> AIResponse:
        """Generate mock response"""
        mock_responses = [
            "This is a creative response to your idea.",
            "Let me explore this concept from multiple perspectives.",
            "Here's an innovative approach to consider.",
            "That's an interesting thought! Here are some possibilities.",
            "I can help you develop this idea further."
        ]

        # Create a simple prompt from messages
        prompt = " ".join([msg.get("content", "") for msg in request.messages])
        content = mock_responses[hash(prompt) % len(mock_responses)]

        return AIResponse(
            content=content,
            role="assistant",
            finish_reason="stop",
            usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
        )

    async def chat_completion_stream(self, request: AIRequest):
        """Generate mock streaming response"""
        response = await self.chat_completion(request)
        words = response.content.split()
        for word in words:
            yield word + " "
            await asyncio.sleep(0.1)


async def demo_basic_functionality():
    """Demonstrate basic functionality"""
    print("AI Character Toolkit - Basic Functionality Demo")
    print("=" * 50)

    # Initialize logger
    logger = get_logger("demo")
    logger.info("Starting demo")

    try:
        # 1. Setup AI provider (mock mode)
        print("\n1. Initializing AI provider...")
        ai_config = {
            'model': 'mock-model',
            'api_key': 'demo-key',
            'max_tokens': 1000,
            'temperature': 0.7
        }

        ai_provider = MockAIProvider(ai_config)
        print(f"   AI Provider: {ai_provider.provider_name}")
        print("   Using mock mode for demonstration")

        # 2. Initialize core components
        print("\n2. Initializing core components...")
        storage = FileStorage()
        character_manager = CharacterManager(ai_provider)
        explorer = CreativeExplorer(ai_provider)
        dialogue_manager = DialogueManager(ai_provider, storage)

        print("   Storage initialized")
        print("   Character manager ready")
        print("   Creative explorer ready")
        print("   Dialogue manager ready")

        # 3. Demonstrate character creation
        print("\n3. Creating a character...")
        character_info = CharacterInfo(
            name="Dr. Alice Chen",
            position="AI Research Scientist",
            experience="10 years in machine learning research"
        )

        character = Character(
            name="Dr. Alice Chen",
            type=CharacterType.EXPERT,
            description="An expert in artificial intelligence and machine learning",
            info=character_info
        )

        print(f"   Created character: {character.name}")
        print(f"   Type: {character.type.value}")
        print(f"   Description: {character.description}")

        # 4. Demonstrate exploration
        print("\n4. Creative exploration example...")
        idea = "How can AI help improve renewable energy systems?"

        print(f"   Exploring idea: {idea}")

        # Simulate exploration process
        mock_request = AIRequest(
            messages=[{"role": "user", "content": f"Explore the idea: {idea}"}],
            max_tokens=500,
            temperature=0.7
        )

        response = await ai_provider.chat_completion(mock_request)
        print(f"   AI Response: {response.content}")
        print(f"   Tokens used: {response.usage['total_tokens']}")

        # 5. Demonstrate data persistence
        print("\n5. Testing data persistence...")
        try:
            # Save character to storage
            await storage.save_character(character)
            print("   Character saved to storage")

            # Load character from storage
            loaded_character = await storage.load_character(character.id)
            print(f"   Loaded character: {loaded_character.name}")
            print("   Storage test successful")
        except Exception as e:
            print(f"   Storage test note: {e}")

        print("\n" + "=" * 50)
        print("Demo completed successfully!")
        print("Your AI Character Toolkit is ready to use.")
        print("\nNext steps:")
        print("1. Configure your API keys: python setup_keys.py")
        print("2. Try the CLI: python cli.py --help")
        print("3. Start exploring: python cli.py explore start \"your idea\"")

    except Exception as e:
        print(f"Demo failed with error: {e}")
        logger.error(f"Demo error: {e}")


if __name__ == "__main__":
    asyncio.run(demo_basic_functionality())