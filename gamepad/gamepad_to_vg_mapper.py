import json
import vgamepad as vg
from input_classes.input import Input
from input_classes.input_type import Type
from configuration_manager.config_manager import ConfigManager

class GamepadToVGamepadMapper:
    def __init__(self, vg, config: ConfigManager):
        self.scheme = None
        self.config = config
        self.last_left_stick_y = 0
        self.last_left_stick_x = 0
        self.last_right_stick_y = 0
        self.last_right_stick_x = 0
        self.dead_zone = self.config.get("gamepad.dead_zone")
        gamepad_scheme = f"{self.config.get("paths.controller_scheme_folder")}/{self.config.get("gamepad.name")}.json"

        with open(gamepad_scheme, "r") as f:
            self.scheme = json.load(f)

        self.button_table = None
        self.vg = vg
        self._set_button_table()



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
        
        if input.id == self.scheme["axis"]["left_stick"]["x"]:
            input.value = 0 if abs(input.value) <= self.dead_zone else input.value
            self.last_left_stick_x = input.value
            return (input.value, self.last_left_stick_y)
        
        elif input.id == self.scheme["axis"]["left_stick"]["y"]:
            input.value = 0 if abs(input.value) <= self.dead_zone else input.value
            y_value = -input.value
            self.last_left_stick_y = y_value
            return (self.last_left_stick_x, y_value)
        
        elif input.id == self.scheme["axis"]["right_stick"]["x"]:
            input.value = 0 if abs(input.value) <= self.dead_zone else input.value
            self.last_right_stick_x = input.value
            return (input.value, self.last_right_stick_y)
        
        elif input.id == self.scheme["axis"]["right_stick"]["y"]:
            input.value = 0 if abs(input.value) <= self.dead_zone else input.value
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
        

    def _set_button_table(self):
        buttons_gamepad = self.scheme["button"]
        self.button_table = {
            buttons_gamepad["bottom_action"] : self.vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
            buttons_gamepad["right_action"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
            buttons_gamepad["left_action"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
            buttons_gamepad["top_action"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
            buttons_gamepad["select_or_share"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
            buttons_gamepad["system_home"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE,
            buttons_gamepad["start_menu"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
            buttons_gamepad["left_stick_click"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
            buttons_gamepad["right_stick_click"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
            buttons_gamepad["left_bumper"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
            buttons_gamepad["right_bumper"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
            buttons_gamepad["dpad_up"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
            buttons_gamepad["dpad_down"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
            buttons_gamepad["dpad_left"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
            buttons_gamepad["dpad_right"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
            buttons_gamepad["aux_center_or_touchpad"]: self.vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK
        }

