"""
File-based storage implementation for AI Character Toolkit.
"""

import json
import yaml
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import shutil

from ..models.schemas import Character, Dialogue, ExplorationSession, ValidationSession
from ..utils.logger import get_logger
from ..utils.config import config


class FileStorage:
    """File-based storage manager."""

    def __init__(self, base_path: Optional[str] = None, format_type: str = "json"):
        """
        Initialize file storage.

        Args:
            base_path: Base storage path
            format_type: Storage format (json, yaml)
        """
        self.logger = get_logger(__name__)
        storage_config = config.get('storage.file', {})

        self.base_path = Path(base_path or storage_config.get('base_path', './data'))
        self.format_type = format_type or storage_config.get('format', 'json')
        self.auto_save = config.get('dialogue.auto_save', True)

        # Create storage directories
        self._create_storage_directories()

    def _create_storage_directories(self):
        """Create necessary storage directories."""
        directories = [
            self.base_path,
            self.base_path / 'characters',
            self.base_path / 'dialogues',
            self.base_path / 'explorations',
            self.base_path / 'validations',
            self.base_path / 'backups'
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"File storage initialized at: {self.base_path}")

    async def save_character(self, character: Character) -> bool:
        """
        Save character to file.

        Args:
            character: Character to save

        Returns:
            True if saved successfully
        """
        try:
            file_path = self._get_character_path(character.id)
            data = character.to_dict()

            if self.format_type == 'yaml':
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False, default=str)

            self.logger.debug(f"Character saved: {character.name} ({character.id})")
            return True

        except Exception as e:
            self.logger.error(f"Failed to save character {character.id}: {e}")
            return False

    async def load_character(self, character_id: str) -> Optional[Character]:
        """
        Load character from file.

        Args:
            character_id: Character ID

        Returns:
            Character if found, None otherwise
        """
        try:
            file_path = self._get_character_path(character_id)
            if not file_path.exists():
                return None

            with open(file_path, 'r', encoding='utf-8') as f:
                if self.format_type == 'yaml':
                    data = yaml.safe_load(f)
                else:
                    data = json.load(f)

            return Character.from_dict(data)

        except Exception as e:
            self.logger.error(f"Failed to load character {character_id}: {e}")
            return None

    async def delete_character(self, character_id: str) -> bool:
        """
        Delete character file.

        Args:
            character_id: Character ID

        Returns:
            True if deleted successfully
        """
        try:
            file_path = self._get_character_path(character_id)
            if file_path.exists():
                file_path.unlink()
                self.logger.debug(f"Character deleted: {character_id}")
                return True
            return False

        except Exception as e:
            self.logger.error(f"Failed to delete character {character_id}: {e}")
            return False

    async def list_characters(self) -> List[str]:
        """
        List all character IDs.

        Returns:
            List of character IDs
        """
        try:
            character_dir = self.base_path / 'characters'
            if not character_dir.exists():
                return []

            extension = '.yaml' if self.format_type == 'yaml' else '.json'
            character_files = character_dir.glob(f'*{extension}')

            return [f.stem for f in character_files if f.is_file()]

        except Exception as e:
            self.logger.error(f"Failed to list characters: {e}")
            return []

    async def save_dialogue(self, dialogue: Dialogue) -> bool:
        """
        Save dialogue to file.

        Args:
            dialogue: Dialogue to save

        Returns:
            True if saved successfully
        """
        try:
            file_path = self._get_dialogue_path(dialogue.id)
            data = dialogue.to_dict()

            if self.format_type == 'yaml':
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False, default=str)

            self.logger.debug(f"Dialogue saved: {dialogue.title} ({dialogue.id})")
            return True

        except Exception as e:
            self.logger.error(f"Failed to save dialogue {dialogue.id}: {e}")
            return False

    async def load_dialogue(self, dialogue_id: str) -> Optional[Dialogue]:
        """
        Load dialogue from file.

        Args:
            dialogue_id: Dialogue ID

        Returns:
            Dialogue if found, None otherwise
        """
        try:
            file_path = self._get_dialogue_path(dialogue_id)
            if not file_path.exists():
                return None

            with open(file_path, 'r', encoding='utf-8') as f:
                if self.format_type == 'yaml':
                    data = yaml.safe_load(f)
                else:
                    data = json.load(f)

            return Dialogue.from_dict(data)

        except Exception as e:
            self.logger.error(f"Failed to load dialogue {dialogue_id}: {e}")
            return None

    async def save_exploration(self, exploration: ExplorationSession) -> bool:
        """
        Save exploration session to file.

        Args:
            exploration: Exploration session to save

        Returns:
            True if saved successfully
        """
        try:
            file_path = self._get_exploration_path(exploration.id)
            data = exploration.to_dict()

            if self.format_type == 'yaml':
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False, default=str)

            self.logger.debug(f"Exploration saved: {exploration.id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to save exploration {exploration.id}: {e}")
            return False

    async def load_exploration(self, exploration_id: str) -> Optional[ExplorationSession]:
        """
        Load exploration session from file.

        Args:
            exploration_id: Exploration session ID

        Returns:
            Exploration session if found, None otherwise
        """
        try:
            file_path = self._get_exploration_path(exploration_id)
            if not file_path.exists():
                return None

            with open(file_path, 'r', encoding='utf-8') as f:
                if self.format_type == 'yaml':
                    data = yaml.safe_load(f)
                else:
                    data = json.load(f)

            return ExplorationSession.from_dict(data)

        except Exception as e:
            self.logger.error(f"Failed to load exploration {exploration_id}: {e}")
            return None

    async def save_validation(self, validation: ValidationSession) -> bool:
        """
        Save validation session to file.

        Args:
            validation: Validation session to save

        Returns:
            True if saved successfully
        """
        try:
            file_path = self._get_validation_path(validation.id)
            data = validation.to_dict()

            if self.format_type == 'yaml':
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False, default=str)

            self.logger.debug(f"Validation saved: {validation.id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to save validation {validation.id}: {e}")
            return False

    async def load_validation(self, validation_id: str) -> Optional[ValidationSession]:
        """
        Load validation session from file.

        Args:
            validation_id: Validation session ID

        Returns:
            Validation session if found, None otherwise
        """
        try:
            file_path = self._get_validation_path(validation_id)
            if not file_path.exists():
                return None

            with open(file_path, 'r', encoding='utf-8') as f:
                if self.format_type == 'yaml':
                    data = yaml.safe_load(f)
                else:
                    data = json.load(f)

            return ValidationSession.from_dict(data)

        except Exception as e:
            self.logger.error(f"Failed to load validation {validation_id}: {e}")
            return None

    async def create_backup(self) -> str:
        """
        Create backup of all data.

        Returns:
            Backup file path
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = self.base_path / 'backups' / f"backup_{timestamp}"

            # Copy all data directories
            shutil.copytree(self.base_path, backup_dir, ignore=shutil.ignore_patterns('backups'))

            self.logger.info(f"Backup created: {backup_dir}")
            return str(backup_dir)

        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            raise

    async def restore_backup(self, backup_path: str) -> bool:
        """
        Restore data from backup.

        Args:
            backup_path: Path to backup directory

        Returns:
            True if restored successfully
        """
        try:
            backup_dir = Path(backup_path)
            if not backup_dir.exists():
                raise ValueError(f"Backup directory not found: {backup_path}")

            # Remove current data (except backups)
            for item in self.base_path.iterdir():
                if item.name != 'backups' and item.is_dir():
                    shutil.rmtree(item)

            # Restore from backup
            for item in backup_dir.iterdir():
                if item.name != 'backups' and item.is_dir():
                    shutil.copytree(item, self.base_path / item.name)

            self.logger.info(f"Data restored from: {backup_path}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to restore backup: {e}")
            return False

    async def get_storage_stats(self) -> Dict[str, Any]:
        """
        Get storage statistics.

        Returns:
            Storage statistics
        """
        try:
            stats = {
                'total_characters': len(await self.list_characters()),
                'storage_format': self.format_type,
                'storage_path': str(self.base_path),
                'total_size_mb': self._calculate_total_size()
            }

            return stats

        except Exception as e:
            self.logger.error(f"Failed to get storage stats: {e}")
            return {}

    def _get_character_path(self, character_id: str) -> Path:
        """Get character file path."""
        extension = '.yaml' if self.format_type == 'yaml' else '.json'
        return self.base_path / 'characters' / f"{character_id}{extension}"

    def _get_dialogue_path(self, dialogue_id: str) -> Path:
        """Get dialogue file path."""
        extension = '.yaml' if self.format_type == 'yaml' else '.json'
        return self.base_path / 'dialogues' / f"{dialogue_id}{extension}"

    def _get_exploration_path(self, exploration_id: str) -> Path:
        """Get exploration file path."""
        extension = '.yaml' if self.format_type == 'yaml' else '.json'
        return self.base_path / 'explorations' / f"{exploration_id}{extension}"

    def _get_validation_path(self, validation_id: str) -> Path:
        """Get validation file path."""
        extension = '.yaml' if self.format_type == 'yaml' else '.json'
        return self.base_path / 'validations' / f"{validation_id}{extension}"

    def _calculate_total_size(self) -> float:
        """Calculate total storage size in MB."""
        total_size = 0
        for file_path in self.base_path.rglob('*'):
            if file_path.is_file() and file_path.parent.name != 'backups':
                total_size += file_path.stat().st_size

        return round(total_size / (1024 * 1024), 2)  # Convert to MB