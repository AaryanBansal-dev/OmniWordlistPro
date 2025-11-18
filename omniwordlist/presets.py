"""
Preset management system

Save and load wordlist generation presets
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from .config import Config
from .error import PresetError


# Built-in presets
BUILTIN_PRESETS = {
    "pentest_default": {
        "name": "pentest_default",
        "description": "Standard pentesting wordlist",
        "config": {
            "min_length": 6,
            "max_length": 16,
            "charset": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
            "enabled_fields": ["company_name", "dev_handles", "first_name_male_0", "birth_year"],
            "transforms": ["leet_basic", "append_numbers_4"],
            "filters": {
                "min_len": 6,
                "max_len": 32,
            },
            "dedupe": True,
        }
    },
    "meme_humor_pack": {
        "name": "meme_humor_pack",
        "description": "Creative wordlist with humor",
        "config": {
            "min_length": 3,
            "max_length": 20,
            "enabled_fields": ["fav_meme_format", "favorite_joke", "favorite_pun", "go_to_reaction_emoji"],
            "transforms": ["emoji_insertion", "capitalize"],
            "filters": {
                "min_len": 3,
                "max_len": 50,
            },
        }
    },
    "api_dev_wordlist": {
        "name": "api_dev_wordlist",
        "description": "API endpoint patterns",
        "config": {
            "min_length": 4,
            "max_length": 20,
            "enabled_fields": ["dev_handles", "programming_language", "database_name"],
            "transforms": ["lowercase", "capitalize"],
            "prefix": "/api/",
            "filters": {
                "min_len": 4,
                "max_len": 50,
            },
        }
    },
    "social_media_usernames": {
        "name": "social_media_usernames",
        "description": "Social media handles",
        "config": {
            "min_length": 3,
            "max_length": 15,
            "enabled_fields": ["first_name_male_0", "first_name_female_0", "last_name_0"],
            "transforms": ["lowercase", "append_numbers_2"],
            "filters": {
                "min_len": 3,
                "max_len": 20,
            },
        }
    },
    "pattern_basic": {
        "name": "pattern_basic",
        "description": "Crunch-style pattern examples",
        "config": {
            "min_length": 4,
            "max_length": 8,
            "pattern": "pass%%",  # pass + 2 digits
            "filters": {
                "min_len": 4,
                "max_len": 10,
            },
        }
    },
}


class PresetManager:
    """Manage presets"""
    
    def __init__(self, preset_dir: Optional[Path] = None):
        """
        Initialize preset manager
        
        Args:
            preset_dir: Directory for custom presets
        """
        self.preset_dir = preset_dir or Path.home() / ".omniwordlist" / "presets"
        self.preset_dir.mkdir(parents=True, exist_ok=True)
    
    def list_presets(self) -> List[str]:
        """List all available presets (built-in and custom)"""
        presets = list(BUILTIN_PRESETS.keys())
        
        # Add custom presets
        if self.preset_dir.exists():
            for preset_file in self.preset_dir.glob("*.json"):
                preset_name = preset_file.stem
                if preset_name not in presets:
                    presets.append(preset_name)
        
        return sorted(presets)
    
    def get_preset(self, name: str) -> Dict:
        """
        Get preset by name
        
        Args:
            name: Preset name
            
        Returns:
            Preset dictionary
        """
        # Check built-in presets first
        if name in BUILTIN_PRESETS:
            return BUILTIN_PRESETS[name]
        
        # Check custom presets
        preset_path = self.preset_dir / f"{name}.json"
        if preset_path.exists():
            with open(preset_path, 'r') as f:
                return json.load(f)
        
        raise PresetError(f"Preset not found: {name}")
    
    def get_preset_config(self, name: str) -> Config:
        """
        Get preset as Config object
        
        Args:
            name: Preset name
            
        Returns:
            Config object
        """
        preset = self.get_preset(name)
        return Config.from_dict(preset['config'])
    
    def save_preset(self, name: str, description: str, config: Config):
        """
        Save a custom preset
        
        Args:
            name: Preset name
            description: Preset description
            config: Configuration to save
        """
        preset_data = {
            "name": name,
            "description": description,
            "config": config.to_dict(),
        }
        
        preset_path = self.preset_dir / f"{name}.json"
        with open(preset_path, 'w') as f:
            json.dump(preset_data, f, indent=2)
    
    def delete_preset(self, name: str):
        """
        Delete a custom preset
        
        Args:
            name: Preset name
        """
        if name in BUILTIN_PRESETS:
            raise PresetError(f"Cannot delete built-in preset: {name}")
        
        preset_path = self.preset_dir / f"{name}.json"
        if preset_path.exists():
            preset_path.unlink()
        else:
            raise PresetError(f"Preset not found: {name}")
    
    def show_preset(self, name: str) -> str:
        """
        Show preset details as formatted string
        
        Args:
            name: Preset name
            
        Returns:
            Formatted preset information
        """
        preset = self.get_preset(name)
        
        lines = [
            f"Preset: {preset['name']}",
            f"Description: {preset['description']}",
            "",
            "Configuration:",
        ]
        
        config = preset['config']
        for key, value in sorted(config.items()):
            if value:
                lines.append(f"  {key}: {value}")
        
        return "\n".join(lines)
