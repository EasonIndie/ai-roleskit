"""
Configuration management module for AI Character Toolkit.
"""

import os
import re
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class Config:
    """Configuration manager for the AI Character Toolkit."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.

        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path or self._get_default_config_path()
        self._config_data = {}
        self.load_config()

    def _get_default_config_path(self) -> str:
        """Get default configuration file path."""
        # Check environment variable first
        if 'AI_TOOLKIT_CONFIG' in os.environ:
            return os.environ['AI_TOOLKIT_CONFIG']

        # Check for config in user home directory
        home_config = Path.home() / '.ai_toolkit' / 'config.yaml'
        if home_config.exists():
            return str(home_config)

        # Use default config in project directory
        return str(Path(__file__).parent.parent.parent.parent / 'config' / 'default.yaml')

    def load_config(self) -> None:
        """Load configuration from file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                self._config_data = yaml.safe_load(file) or {}
            # Process environment variable substitution
            self._process_env_vars()
        except FileNotFoundError:
            print(f"Warning: Config file {self.config_path} not found. Using defaults.")
            self._config_data = {}
        except yaml.YAMLError as e:
            print(f"Warning: Error parsing config file {self.config_path}: {e}")
            self._config_data = {}

    def _process_env_vars(self) -> None:
        """Process environment variable substitution in configuration."""
        def replace_env_vars(obj):
            if isinstance(obj, dict):
                return {key: replace_env_vars(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [replace_env_vars(item) for item in obj]
            elif isinstance(obj, str):
                # Replace ${VAR_NAME} with environment variable value
                def env_replacer(match):
                    var_name = match.group(1)
                    return os.getenv(var_name, match.group(0))

                return re.sub(r'\$\{([^}]+)\}', env_replacer, obj)
            else:
                return obj

        self._config_data = replace_env_vars(self._config_data)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key (supports dot notation).

        Args:
            key: Configuration key (e.g., 'openai.model')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config_data

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value by key (supports dot notation).

        Args:
            key: Configuration key
            value: Value to set
        """
        keys = key.split('.')
        config = self._config_data

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def get_ai_provider(self) -> str:
        """Get default AI provider."""
        return self.get('ai.provider', 'openai')

    def get_openai_config(self) -> Dict[str, Any]:
        """Get OpenAI configuration."""
        return self.get('openai', {})

    def get_claude_config(self) -> Dict[str, Any]:
        """Get Claude configuration."""
        return self.get('claude', {})

    def get_zhipu_config(self) -> Dict[str, Any]:
        """Get ZhipuAI configuration."""
        return self.get('zhipu', {})

    def get_storage_config(self) -> Dict[str, Any]:
        """Get storage configuration."""
        return self.get('storage', {'type': 'file'})

    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return self.get('logging', {
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        })

    def save_config(self, path: Optional[str] = None) -> None:
        """
        Save configuration to file.

        Args:
            path: Path to save configuration (uses current config path if not provided)
        """
        save_path = path or self.config_path
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'w', encoding='utf-8') as file:
            yaml.dump(self._config_data, file, default_flow_style=False, allow_unicode=True)


# Global configuration instance
config = Config()