import json
DUALSENSE_SCHEME = "controller_schemes/dualsense.json"

class GamepadSuper:
    def __init__(self):
        self.scheme = None
        with open(DUALSENSE_SCHEME) as f:
            self.scheme = json.load(f)

    
    def _is_left_stick(self, input):
        
        return input.id in self.scheme["axis"]["left_stick"].values()

    def _is_right_stick(self, input):
        return input.id in self.scheme["axis"]["right_stick"].values()

    def _is_left_trigger(self, input):
        return input.id == self.scheme["axis"]["triggers"]["left"]

    def _is_right_trigger(self, input):
        return input.id == self.scheme["axis"]["triggers"]["right"]
    