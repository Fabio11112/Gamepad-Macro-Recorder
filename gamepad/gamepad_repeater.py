from json_classes.json_loader import JsonLoader
from input_classes.input_collection import InputCollection
from input_classes.input import Input
from gamepad.gamepad_to_vg_mapper import GamepadToVGamepadMapper
from gamepad.gamepad_super import GamepadSuper
from input_classes.input_type import Type
import time

BUTTON_DOWN = 0
BUTTON_UP = 1
TIME_FOR_WAITING = 0.002

DUALSENSE = "dualsense"

class GamepadRepeater(GamepadSuper):
    def __init__(self, vg: object, inputs_file: str, gamepad_name = DUALSENSE):
        super().__init__()
        self.gamepad = vg.VX360Gamepad()

        self.mapper = GamepadToVGamepadMapper(vg, gamepad_name)
        loader = JsonLoader(inputs_file)
        loader.load()
        self.inputs = InputCollection(loader.getInputs())

    def _initialize(self):
        self.iterator = self.inputs.get_iterator()

    def replay(self):
        self._initialize()
        
        if not self.iterator:
            raise SystemError("No inputs to iterate to")
        
        start_time = time.perf_counter()

        while self.iterator.hasNext():
            input = self.iterator.next()
            target_time = start_time + input.timestamp
            
            time_remaining = target_time - time.perf_counter()
            if time_remaining > TIME_FOR_WAITING: # If more that this time remaining (2ms)
                time.sleep(max(0, time_remaining - TIME_FOR_WAITING)) # Sleep most of it

            while time.perf_counter() < target_time:
                pass

            self._execute_input(input)


    def _execute_input(self, input: Input):
        if input.type == Type.BUTTON:       
            self._execute_button(input)
        elif input.type == Type.AXIS:
            self._execute_axis(input)

        self.gamepad.update()

    def _execute_button(self, input: Input):
        if input.value == BUTTON_DOWN:
            self.gamepad.press_button(self.mapper.map_input(input))
            print(f"Button {input.id} pressed")
        elif input.value == BUTTON_UP:
            self.gamepad.release_button(self.mapper.map_input(input))
            print(f"Button {input.id} released")
        


    def _execute_axis(self, input: Input):
        value = self.mapper.map_input(input)

        if self._is_left_stick(input):
            x, y = value
            self.gamepad.left_joystick_float(x_value_float=x, y_value_float=y)
        elif self._is_right_stick(input):
            x, y = value
            self.gamepad.right_joystick_float(x_value_float=x,y_value_float=y)
        elif self._is_left_trigger(input):
            self.gamepad.left_trigger_float(value)
        elif self._is_right_trigger(input):
            self.gamepad.right_trigger_float(value)

