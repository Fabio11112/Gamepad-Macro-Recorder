import json
import vgamepad as vg
from input_classes.input import Input
from input_classes.input_type import Type

DUALSENSE_SCHEME = "controller_schemes/dualsense.json"
DUALSENSE = "dualsense"

class GamepadToVGamepadMapper:
    def __init__(self, vg, gamepad_name=DUALSENSE):
        self.scheme = None

        self.last_left_stick_y = 0
        self.last_left_stick_x = 0
        self.last_right_stick_y = 0
        self.last_right_stick_x = 0

        if gamepad_name == DUALSENSE:
            with open(DUALSENSE_SCHEME, "r") as f:
                self.scheme = json.load(f)

        self.button_table = None
        self.vg = vg
        self._set_button_table(gamepad_name)



    def map_input(self, input: Input):
        """It maps the correct input from a gamepad from the pygame library to the
        XINPUT X360 controller from the vgamepad library

        Args:
            input (Input): An input object that refers to the input from a recording

        Returns:
            object, (int, int): A button enum from vgamepad if it is a button, a tuple (x, y)
            if the input was an axis from a joystick, or just x in the input was a axis from 
            a trigger
        """
        if input.type == Type.BUTTON:
            return self._map_button(input)
        elif input.type == Type.AXIS:
            return self._map_axis(input)
        
    def _map_axis(self, input: Input):
        if input.type != Type.AXIS:
            raise ValueError("Input must be a AXIS")
        
        if input.id == self.scheme["axis"]["left_stick"]["left_right"]:
            self.last_left_stick_x = input.value
            return (input.value, self.last_left_stick_y)
        
        elif input.id == self.scheme["axis"]["left_stick"]["up_down"]:
            y_value = -input.value
            self.last_left_stick_y = y_value
            return (self.last_left_stick_x, y_value)
        
        elif input.id == self.scheme["axis"]["right_stick"]["left_right"]:
            self.last_right_stick_x = input.value
            return (input.value, self.last_right_stick_y)
        
        elif input.id == self.scheme["axis"]["right_stick"]["up_down"]:
            y_value = -input.value
            self.last_right_stick_y = y_value
            return (self.last_right_stick_x, y_value)
        
        elif input.id in self.scheme["axis"]["triggers"].values():
            value = (input.value + 1) / 2   #[-1, 1] -> [0, 1]
            return value
        
        
    def _map_button(self, input: Input):
        if input.type != Type.BUTTON:
            raise ValueError("Input must be a BUTTON")
        return self.button_table[input.id]
        

    def _set_button_table(self, gamepad_name: str):
        buttons_gamepad = self.scheme["button"]
        if gamepad_name == DUALSENSE:
            self.button_table = {
                buttons_gamepad["cross"] : self.vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
                buttons_gamepad["circle"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
                buttons_gamepad["square"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
                buttons_gamepad["triangle"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
                buttons_gamepad["share"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
                buttons_gamepad["ps"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE,
                buttons_gamepad["options"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
                buttons_gamepad["l3"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
                buttons_gamepad["r3"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
                buttons_gamepad["l1"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
                buttons_gamepad["r1"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
                buttons_gamepad["dpad_up"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
                buttons_gamepad["dpad_down"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
                buttons_gamepad["dpad_left"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
                buttons_gamepad["dpad_right"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
                buttons_gamepad["touchpad"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK
            }

