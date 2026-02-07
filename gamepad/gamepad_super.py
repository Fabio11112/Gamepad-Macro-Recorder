from configuration_manager.config_manager import ConfigManager
import json

class GamepadSuper:
    def __init__(self, config: ConfigManager):
        self.scheme = None
        self.config = config
        file_path = f"{self.config.get("paths.controller_scheme_folder")}/{self.config.get("gamepad.name")}.json"
        with open(file_path) as f:
            self.scheme = json.load(f)

    
    def _is_left_stick(self, input):
        
        return input.id in self.scheme["axis"]["left_stick"].values()

    def _is_right_stick(self, input):
        return input.id in self.scheme["axis"]["right_stick"].values()

    def _is_left_trigger(self, input):
        return input.id == self.scheme["axis"]["triggers"]["left"]

    def _is_right_trigger(self, input):
        return input.id == self.scheme["axis"]["triggers"]["right"]
    