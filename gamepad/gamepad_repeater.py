from json_classes.json_loader import JsonLoader
from input_classes.input_collection import InputCollection
import time
from input_classes.input import Input

class GamepadRepeater:
    def __init__(self, vg: object, inputs_file: str):
        self.gamepad = vg.VX360Gamepad()
        
        loader = JsonLoader(inputs_file)
        loader.load()
        inputs = InputCollection(loader.getInputs())
        
        self.iterator = inputs.get_iterator()

    def replay(self):
        if not self.inputs:
            raise SystemError("No inputs to replay")
        
        start_time = time.perf_counter()

        while self.iterator.hasNext():
            input = self.iterator.next()
            target_time = start_time + input.timestamp
            
            while time.perf_counter() < target_time:
                pass

            self._execute_input(input)

    def _execute_input(self, input: Input):
        pass
