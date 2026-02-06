from json_classes.json_loader import JsonLoader
from input_classes.input_collection import InputCollection
from input_classes.input import Input
from gamepad.gamepad_to_vg_mapper import GamepadToVGamepadMapper
from input_classes.input_type import Type
import time

BUTTON_DOWN = 0
BUTTON_UP = 1

DUALSENSE = "dualsense"

class GamepadRepeater:
    def __init__(self, vg: object, inputs_file: str, gamepad_name = DUALSENSE):
        self.gamepad = vg.VX360Gamepad()

        self.mapper = GamepadToVGamepadMapper(vg, gamepad_name)
        loader = JsonLoader(inputs_file)
        loader.load()
        inputs = InputCollection(loader.getInputs())
        self.iterator = inputs.get_iterator()

    def replay(self):
        if not self.iterator:
            raise SystemError("No inputs to iterate to")
        
        start_time = time.perf_counter()

        while self.iterator.hasNext():
            input = self.iterator.next()
            target_time = start_time + input.timestamp
            
            while time.perf_counter() < target_time:
                pass

            self._execute_input(input)


    def _execute_input(self, input: Input):
        if input.type == Type.BUTTON:       
            self._execute_button(input)
        elif input.type == Type.AXIS:
            self._execute_axis(input)

    def _execute_button(self, input: Input):
        if input.value == BUTTON_DOWN:
            self.gamepad.press_button(self.mapper.map_input(input))
            print(f"Button {input.id} pressed")
        elif input.value == BUTTON_UP:
            self.gamepad.release_button(self.mapper.map_input(input))
            print(f"Button {input.id} released")
        
        self.gamepad.update()

    def _execute_axis(self, input: Input):
        raise NotImplementedError