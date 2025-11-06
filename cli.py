#!/usr/bin/env python3
"""
AI Character Toolkit CLI
Command-line interface for the Dynamic AI Character Generation Toolkit.
"""

import asyncio
import click
import sys
from pathlib import Path
from typing import Optional
import os

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from ai_toolkit.utils.config import config
from ai_toolkit.utils.logger import get_logger
from ai_toolkit.ai.openai_provider import OpenAIProvider
from ai_toolkit.ai.claude_provider import ClaudeProvider
from ai_toolkit.ai.zhipu_provider import ZhipuProvider
from ai_toolkit.core.character import CharacterManager
from ai_toolkit.core.exploration import CreativeExplorer
from ai_toolkit.core.dialogue import DialogueManager
from ai_toolkit.core.concurrent import ConcurrentValidator
from ai_toolkit.core.analysis import IntegrationAnalyzer
from ai_toolkit.storage.file_storage import FileStorage
from ai_toolkit.models.schemas import CharacterType


# Setup logger
logger = get_logger(__name__)

# Global managers
ai_provider = None
character_manager = None
explorer = None
dialogue_manager = None
validator = None
analyzer = None
storage = None


def setup_ai_provider(provider_name: Optional[str] = None):
    """Setup AI provider."""
    global ai_provider

    provider_name = provider_name or config.get_ai_provider()

    if provider_name == "openai":
        ai_provider = OpenAIProvider(config.get_openai_config())
    elif provider_name == "claude":
        ai_provider = ClaudeProvider(config.get_claude_config())
    elif provider_name == "zhipu":
        ai_provider = ZhipuProvider(config.get_zhipu_config())
    else:
        raise ValueError(f"Unsupported AI provider: {provider_name}. Supported providers: openai, claude, zhipu")

    return ai_provider


def setup_managers():
    """Setup all managers."""
    global character_manager, explorer, dialogue_manager, validator, analyzer, storage

    if not ai_provider:
        setup_ai_provider()

    storage = FileStorage()
    character_manager = CharacterManager(ai_provider)
    explorer = CreativeExplorer(ai_provider)
    dialogue_manager = DialogueManager(ai_provider, character_manager)
    validator = ConcurrentValidator(ai_provider, character_manager)
    analyzer = IntegrationAnalyzer(ai_provider, character_manager)


@click.group()
@click.option('--provider', '-p', help='AI provider to use (openai, claude)')
@click.option('--config', '-c', help='Path to config file')
def main(provider: Optional[str], config: Optional[str]):
    """AI Character Toolkit - Dynamic AI Character Generation Tool"""
    try:
        if config:
            os.environ['AI_TOOLKIT_CONFIG'] = config

        setup_ai_provider(provider)
        setup_managers()

        click.echo("🚀 AI Character Toolkit initialized")
        click.echo(f"Using AI provider: {ai_provider.provider_name}")

    except Exception as e:
        click.echo(f"❌ Error initializing: {e}", err=True)
        sys.exit(1)


@main.group()
def explore():
    """Creative exploration commands"""
    pass


@explore.command()
@click.argument('idea')
@click.option('--interactive', '-i', is_flag=True, help='Interactive exploration mode')
def start(idea: str, interactive: bool):
    """Start creative exploration for an idea"""
    async def _explore():
        try:
            session = await explorer.start_exploration(idea)
            click.echo(f"🔍 Exploration started: {session.id}")
            click.echo(f"Initial idea: {idea}")

            if interactive:
                click.echo("\n📝 Interactive exploration mode")
                click.echo("Type 'quit' to exit, 'help' for commands")

                while True:
                    user_input = click.prompt("\nYour input").strip()

                    if user_input.lower() == 'quit':
                        break
                    elif user_input.lower() == 'help':
                        click.echo("Commands: quit, help, stakeholders, knowledge, summary")
                        continue
                    elif user_input.lower() == 'stakeholders':
                        stakeholders = await explorer.identify_stakeholders(session.id)
                        click.echo(f"👥 Identified {len(stakeholders)} stakeholder groups")
                        continue
                    elif user_input.lower() == 'knowledge':
                        knowledge = await explorer.identify_knowledge_areas(session.id)
                        click.echo(f"📚 Identified {len(knowledge)} knowledge areas")
                        continue
                    elif user_input.lower() == 'summary':
                        summary = await explorer.get_exploration_summary(session.id)
                        click.echo(f"📊 Exploration readiness: {summary['character_generation_readiness']}")
                        continue

                    result = await explorer.explore_idea(session.id, user_input)
                    click.echo(f"\n🤖 AI Response:\n{result['ai_response']}")

        except Exception as e:
            click.echo(f"❌ Exploration error: {e}", err=True)

    asyncio.run(_explore())


@main.group()
def character():
    """Character management commands"""
    pass


@character.command()
@click.argument('exploration_id')
@click.option('--type', '-t', type=click.Choice(['user', 'expert', 'organization']), help='Character type')
@click.option('--name', '-n', help='Character name')
def generate(exploration_id: str, type: str, name: str):
    """Generate AI character from exploration"""
    async def _generate():
        try:
            # Load exploration session
            exploration = await storage.load_exploration(exploration_id)
            if not exploration:
                click.echo(f"❌ Exploration not found: {exploration_id}", err=True)
                return

            # Get exploration summary
            summary = await explorer.get_exploration_summary(exploration_id)

            if type:
                # Generate single character
                char_type = CharacterType(type)
                character = await character_manager.create_character(summary, char_type, name)
                click.echo(f"✅ Character generated: {character.name} ({character.id})")
            else:
                # Generate character set
                characters = await character_manager.generator.generate_character_set(summary)
                for char in characters:
                    await character_manager.create_character(summary, char.type, char.name)
                    click.echo(f"✅ Character generated: {char.name} ({char.id})")

        except Exception as e:
            click.echo(f"❌ Character generation error: {e}", err=True)

    asyncio.run(_generate())


@character.command()
def list():
    """List all characters"""
    async def _list():
        try:
            characters = await character_manager.list_characters()
            if not characters:
                click.echo("No characters found")
                return

            click.echo(f"📋 Found {len(characters)} characters:")
            for char in characters:
                click.echo(f"  • {char.name} ({char.type.value}) - {char.id}")

        except Exception as e:
            click.echo(f"❌ Error listing characters: {e}", err=True)

    asyncio.run(_list())


@character.command()
@click.argument('character_id')
def show(character_id: str):
    """Show character details"""
    async def _show():
        try:
            character = await character_manager.get_character(character_id)
            if not character:
                click.echo(f"❌ Character not found: {character_id}", err=True)
                return

            click.echo(f"🎭 Character Details: {character.name}")
            click.echo(f"Type: {character.type.value}")
            click.echo(f"Description: {character.description}")
            click.echo(f"Position: {character.info.position}")
            click.echo(f"Background: {character.info.background}")

        except Exception as e:
            click.echo(f"❌ Error showing character: {e}", err=True)

    asyncio.run(_show())


@main.group()
def dialogue():
    """Dialogue management commands"""
    pass


@dialogue.command()
@click.argument('character_id')
@click.option('--title', '-t', help='Dialogue title')
def start(character_id: str, title: str):
    """Start dialogue with character"""
    async def _start_dialogue():
        try:
            dialogue = await dialogue_manager.create_dialogue(character_id, title)
            click.echo(f"💬 Dialogue started: {dialogue.id}")
            click.echo(f"Character: {dialogue.metadata['character_name']}")
            click.echo("Type your messages (use 'quit' to exit)")

            while True:
                user_message = click.prompt("\nYou").strip()

                if user_message.lower() == 'quit':
                    break

                response = await dialogue_manager.send_message(dialogue.id, user_message)
                click.echo(f"\n🤖 {dialogue.metadata['character_name']}: {response.content}")

        except Exception as e:
            click.echo(f"❌ Dialogue error: {e}", err=True)

    asyncio.run(_start_dialogue())


@dialogue.command()
def list():
    """List all dialogues"""
    async def _list():
        try:
            dialogues = await dialogue_manager.list_dialogues()
            if not dialogues:
                click.echo("No dialogues found")
                return

            click.echo(f"💬 Found {len(dialogues)} dialogues:")
            for dialogue in dialogues:
                click.echo(f"  • {dialogue.title} - {dialogue.id}")

        except Exception as e:
            click.echo(f"❌ Error listing dialogues: {e}", err=True)

    asyncio.run(_list())


@main.group()
def validate():
    """Validation commands"""
    pass


@validate.command()
@click.argument('question')
@click.option('--characters', '-c', help='Comma-separated character IDs')
def concurrent(question: str, characters: str):
    """Run concurrent validation with multiple characters"""
    async def _validate():
        try:
            if not characters:
                click.echo("❌ Please provide character IDs", err=True)
                return

            char_ids = [c.strip() for c in characters.split(',')]
            session = await validator.create_validation_session(question, char_ids)
            click.echo(f"🔍 Validation started: {session.id}")
            click.echo(f"Question: {question}")

            result = await validator.run_concurrent_validation(session.id, char_ids)

            click.echo(f"\n📊 Validation Results:")
            for char_id, response in result['character_responses'].items():
                character = await character_manager.get_character(char_id)
                char_name = character.name if character else char_id
                click.echo(f"\n🎭 {char_name}:")
                click.echo(f"  {response[:200]}...")

            # Show analysis
            if result['analysis']:
                click.echo(f"\n🔬 Analysis:")
                click.echo(f"  Consensus level: {result['analysis'].get('consensus_level', 0):.2f}")
                click.echo(f"  Key concerns: {len(result['analysis'].get('key_concerns', []))}")
                click.echo(f"  Opportunities: {len(result['analysis'].get('opportunities', []))}")

        except Exception as e:
            click.echo(f"❌ Validation error: {e}", err=True)

    asyncio.run(_validate())


@main.group()
def analysis():
    """Analysis commands"""
    pass


@analysis.command()
@click.argument('validation_id')
def report(validation_id: str):
    """Generate analysis report for validation"""
    async def _report():
        try:
            validation = await storage.load_validation(validation_id)
            if not validation:
                click.echo(f"❌ Validation not found: {validation_id}", err=True)
                return

            report = await analyzer.generate_decision_report(validation)

            click.echo(f"📋 Analysis Report for: {validation.question}")
            click.echo(f"\n📊 Executive Summary:")
            click.echo(f"  {report['executive_summary']}")

            if report['key_findings']:
                click.echo(f"\n🔍 Key Findings:")
                for finding in report['key_findings']:
                    click.echo(f"  • {finding}")

            if report['recommendations']:
                click.echo(f"\n💡 Recommendations:")
                for rec in report['recommendations']:
                    click.echo(f"  • {rec}")

            if report['next_steps']:
                click.echo(f"\n🚀 Next Steps:")
                for step in report['next_steps']:
                    click.echo(f"  • {step}")

        except Exception as e:
            click.echo(f"❌ Analysis error: {e}", err=True)

    asyncio.run(_report())


@main.group()
def storage():
    """Storage management commands"""
    pass


@storage.command()
def stats():
    """Show storage statistics"""
    async def _stats():
        try:
            stats = await storage.get_storage_stats()
            click.echo("📊 Storage Statistics:")
            click.echo(f"  Total characters: {stats.get('total_characters', 0)}")
            click.echo(f"  Storage format: {stats.get('storage_format', 'unknown')}")
            click.echo(f"  Storage path: {stats.get('storage_path', 'unknown')}")
            click.echo(f"  Total size: {stats.get('total_size_mb', 0)} MB")

        except Exception as e:
            click.echo(f"❌ Error getting stats: {e}", err=True)

    asyncio.run(_stats())


@storage.command()
def backup():
    """Create backup of all data"""
    async def _backup():
        try:
            backup_path = await storage.create_backup()
            click.echo(f"✅ Backup created: {backup_path}")

        except Exception as e:
            click.echo(f"❌ Backup error: {e}", err=True)

    asyncio.run(_backup())


@main.command()
def version():
    """Show version information"""
    from ai_toolkit import __version__
    click.echo(f"AI Character Toolkit v{__version__}")
    click.echo(f"AI Provider: {ai_provider.provider_name if ai_provider else 'Not initialized'}")


if __name__ == '__main__':
    main()