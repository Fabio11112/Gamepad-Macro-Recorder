import json
import os
from pathlib import Path
from typing import Any, Dict

class ConfigManager:
    """Manages application configuration."""
    
    DEFAULT_CONFIG = {
        "paths": {
            "recording_folder_location": "recordings/",
            "controller_scheme_folder": "controller_schemes/"
        },
        "gamepad":{
            "dead_zone": 0.06, #0.03
            "name": ""
        },
        "repetition":{
            "offset": 0.008,
            "busy_waiting_time": 0.002
        }
    }
    
    def __init__(self, gamepad_name:str = "dualsense", config_path: str = "config/config.json"):
        self.DEFAULT_CONFIG["gamepad"]["name"] = gamepad_name
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self):
        """Load configuration from file, create default if not exists."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            print(f"Configuration loaded from {self.config_path}")
        else:
            print(f"Config file not found. Creating default at {self.config_path}")
            self.config = self.DEFAULT_CONFIG.copy()
            self.save_config()
    
    def save_config(self):
        """Save current configuration to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"Configuration saved to {self.config_path}")
    
    def get(self, key_path: str, default=None) -> Any:
        """
        Get config value using dot notation.
        Example: get("paths.controller_schemes_dir")
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_controller_scheme_path(self, scheme_name: str = None) -> str:
        """Get full path to controller scheme file."""
        schemes_dir = self.get("paths.controller_schemes_dir")
        if scheme_name is None:
            scheme_name = self.get("paths.default_controller_scheme")
        return os.path.join(schemes_dir, scheme_name)
    
    def get_recording_path(self, filename: str = None) -> str:
        """Get full path to recording file."""
        recordings_dir = self.get("paths.recordings_dir")
        if filename is None:
            filename = self.get("paths.default_recording")
        return os.path.join(recordings_dir, filename)