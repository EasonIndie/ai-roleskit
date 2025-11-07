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

    async def save_exploration_formatted(self, exploration, output_format: str = "markdown") -> str:
        """
        Save exploration session with formatted output for human reading.

        Args:
            exploration: Exploration session to save
            output_format: Output format ("markdown", "html", "txt")

        Returns:
            Path to the formatted file
        """
        try:
            # Create formatted output directory
            formatted_dir = self.base_path / 'formatted'
            formatted_dir.mkdir(exist_ok=True)

            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            extension = {
                'markdown': '.md',
                'html': '.html',
                'txt': '.txt'
            }.get(output_format, '.md')

            filename = f"exploration_{exploration.id[:8]}_{timestamp}{extension}"
            file_path = formatted_dir / filename

            # Generate formatted content
            if output_format == "markdown":
                content = self._format_exploration_markdown(exploration)
            elif output_format == "html":
                content = self._format_exploration_html(exploration)
            else:  # txt
                content = self._format_exploration_text(exploration)

            # Save formatted file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            self.logger.info(f"Exploration formatted report saved: {file_path}")
            return str(file_path)

        except Exception as e:
            self.logger.error(f"Failed to save formatted exploration {exploration.id}: {e}")
            raise

    def _format_exploration_markdown(self, exploration) -> str:
        """Format exploration session as Markdown."""
        content = []

        # Header
        content.append("# 创意探索报告")
        content.append("=" * 50)
        content.append("")

        # Basic Information
        content.append("## 基本信息")
        content.append("")
        content.append(f"- **探索ID**: {exploration.id}")
        content.append(f"- **初始想法**: {exploration.initial_idea}")
        content.append(f"- **创建时间**: {exploration.created_at}")
        content.append(f"- **更新时间**: {exploration.updated_at}")
        content.append("")

        # Exploration Steps
        if hasattr(exploration, 'exploration_steps') and exploration.exploration_steps:
            content.append("## 探索步骤")
            content.append("")

            for i, step in enumerate(exploration.exploration_steps, 1):
                content.append(f"### 步骤 {i}: {step.get('analysis_type', '未知类型')}")
                content.append("")
                content.append(f"**时间**: {step.get('timestamp', 'N/A')}")
                content.append(f"**响应长度**: {step.get('response_length', 0)} 字符")
                content.append("")

                # Prompt
                content.append("#### 探索提示")
                content.append("")
                content.append("```")
                content.append(step.get('prompt', '无提示'))
                content.append("```")
                content.append("")

                # AI Response
                content.append("#### AI 分析结果")
                content.append("")
                ai_response = step.get('ai_response', '无响应')
                content.append(ai_response)
                content.append("")

        # AI Analyses
        if hasattr(exploration, 'ai_analyses') and exploration.ai_analyses:
            content.append("## AI 分析汇总")
            content.append("")

            for i, analysis in enumerate(exploration.ai_analyses, 1):
                content.append(f"### 分析 {i}")
                content.append("")
                content.append(analysis)
                content.append("")

        # Stakeholders
        if hasattr(exploration, 'stakeholders') and exploration.stakeholders:
            content.append("## 利益相关者")
            content.append("")

            for stakeholder in exploration.stakeholders:
                content.append(f"### {stakeholder.get('description', '未知群体')}")
                content.append("")
                content.append(f"- **类型**: {stakeholder.get('type', '未知')}")
                content.append(f"- **详情**: {stakeholder.get('details', '无详情')}")
                content.append("")

        # Statistics
        if hasattr(exploration, 'statistics'):
            stats = exploration.statistics
            content.append("## 统计信息")
            content.append("")
            content.append(f"- **探索步骤数**: {stats.get('total_steps', 0)}")
            content.append(f"- **分析总字符数**: {stats.get('total_analysis_chars', 0)}")
            content.append(f"- **利益相关者数量**: {stats.get('stakeholder_count', 0)}")
            content.append(f"- **探索时长**: {stats.get('duration', 'N/A')}")
            content.append("")

        # Footer
        content.append("---")
        content.append(f"*报告生成时间: {datetime.now()}*")
        content.append("")
        content.append("*本报告由 AI Character Toolkit 自动生成*")

        return "\n".join(content)

    def _format_exploration_html(self, exploration) -> str:
        """Format exploration session as HTML."""
        # Basic HTML structure with embedded CSS
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>创意探索报告 - {exploration.initial_idea}</title>
    <style>
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; margin: 40px; }}
        .header {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
        .section {{ margin-bottom: 30px; }}
        .step {{ background: #ffffff; border: 1px solid #e9ecef; padding: 20px; margin: 15px 0; border-radius: 8px; }}
        .ai-response {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        .stakeholder {{ background: #e3f2fd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .stats {{ background: #fff3e0; padding: 15px; border-radius: 5px; }}
        pre {{ background: #f1f3f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h3 {{ color: #7f8c8d; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>创意探索报告</h1>
        <p><strong>探索ID:</strong> {exploration.id}</p>
        <p><strong>初始想法:</strong> {exploration.initial_idea}</p>
        <p><strong>创建时间:</strong> {exploration.created_at}</p>
    </div>

    <div class="section">
        <h2>探索步骤</h2>
        {self._format_steps_html(exploration)}
    </div>

    <div class="section">
        <h2>利益相关者</h2>
        {self._format_stakeholders_html(exploration)}
    </div>

    <div class="section">
        <h2>统计信息</h2>
        <div class="stats">
            {self._format_stats_html(exploration)}
        </div>
    </div>

    <footer>
        <hr>
        <p><em>报告生成时间: {datetime.now()}</em></p>
        <p><em>本报告由 AI Character Toolkit 自动生成</em></p>
    </footer>
</body>
</html>
        """
        return html

    def _format_steps_html(self, exploration) -> str:
        """Format exploration steps as HTML."""
        if not hasattr(exploration, 'exploration_steps') or not exploration.exploration_steps:
            return "<p>暂无探索步骤</p>"

        steps_html = []
        for i, step in enumerate(exploration.exploration_steps, 1):
            step_html = f"""
            <div class="step">
                <h3>步骤 {i}: {step.get('analysis_type', '未知类型')}</h3>
                <p><strong>时间:</strong> {step.get('timestamp', 'N/A')}</p>
                <p><strong>响应长度:</strong> {step.get('response_length', 0)} 字符</p>

                <h4>探索提示</h4>
                <pre>{step.get('prompt', '无提示')}</pre>

                <h4>AI 分析结果</h4>
                <div class="ai-response">
                    {step.get('ai_response', '无响应').replace(chr(10), '<br>')}
                </div>
            </div>
            """
            steps_html.append(step_html)

        return "".join(steps_html)

    def _format_stakeholders_html(self, exploration) -> str:
        """Format stakeholders as HTML."""
        if not hasattr(exploration, 'stakeholders') or not exploration.stakeholders:
            return "<p>暂无利益相关者信息</p>"

        stakeholders_html = []
        for stakeholder in exploration.stakeholders:
            stakeholder_html = f"""
            <div class="stakeholder">
                <h3>{stakeholder.get('description', '未知群体')}</h3>
                <p><strong>类型:</strong> {stakeholder.get('type', '未知')}</p>
                <p><strong>详情:</strong> {stakeholder.get('details', '无详情')}</p>
            </div>
            """
            stakeholders_html.append(stakeholder_html)

        return "".join(stakeholders_html)

    def _format_stats_html(self, exploration) -> str:
        """Format statistics as HTML."""
        if not hasattr(exploration, 'statistics'):
            return "<p>暂无统计信息</p>"

        stats = exploration.statistics
        return f"""
        <ul>
            <li><strong>探索步骤数:</strong> {stats.get('total_steps', 0)}</li>
            <li><strong>分析总字符数:</strong> {stats.get('total_analysis_chars', 0)}</li>
            <li><strong>利益相关者数量:</strong> {stats.get('stakeholder_count', 0)}</li>
            <li><strong>探索时长:</strong> {stats.get('duration', 'N/A')}</li>
        </ul>
        """

    def _format_exploration_text(self, exploration) -> str:
        """Format exploration session as plain text."""
        content = []

        # Header
        content.append("=" * 60)
        content.append("创意探索报告")
        content.append("=" * 60)
        content.append("")

        # Basic Information
        content.append("基本信息:")
        content.append("-" * 20)
        content.append(f"探索ID: {exploration.id}")
        content.append(f"初始想法: {exploration.initial_idea}")
        content.append(f"创建时间: {exploration.created_at}")
        content.append(f"更新时间: {exploration.updated_at}")
        content.append("")

        # Exploration Steps
        if hasattr(exploration, 'exploration_steps') and exploration.exploration_steps:
            content.append("探索步骤:")
            content.append("-" * 20)

            for i, step in enumerate(exploration.exploration_steps, 1):
                content.append(f"\n步骤 {i}: {step.get('analysis_type', '未知类型')}")
                content.append(f"时间: {step.get('timestamp', 'N/A')}")
                content.append(f"响应长度: {step.get('response_length', 0)} 字符")
                content.append("")

                content.append("探索提示:")
                content.append("-" * 10)
                content.append(step.get('prompt', '无提示'))
                content.append("")

                content.append("AI 分析结果:")
                content.append("-" * 10)
                content.append(step.get('ai_response', '无响应'))
                content.append("")
                content.append("=" * 40)
                content.append("")

        # Stakeholders
        if hasattr(exploration, 'stakeholders') and exploration.stakeholders:
            content.append("利益相关者:")
            content.append("-" * 20)

            for stakeholder in exploration.stakeholders:
                content.append(f"\n{stakeholder.get('description', '未知群体')}")
                content.append(f"类型: {stakeholder.get('type', '未知')}")
                content.append(f"详情: {stakeholder.get('details', '无详情')}")
                content.append("")

        # Statistics
        if hasattr(exploration, 'statistics'):
            stats = exploration.statistics
            content.append("统计信息:")
            content.append("-" * 20)
            content.append(f"探索步骤数: {stats.get('total_steps', 0)}")
            content.append(f"分析总字符数: {stats.get('total_analysis_chars', 0)}")
            content.append(f"利益相关者数量: {stats.get('stakeholder_count', 0)}")
            content.append(f"探索时长: {stats.get('duration', 'N/A')}")
            content.append("")

        # Footer
        content.append("=" * 60)
        content.append(f"报告生成时间: {datetime.now()}")
        content.append("本报告由 AI Character Toolkit 自动生成")
        content.append("=" * 60)

        return "\n".join(content)