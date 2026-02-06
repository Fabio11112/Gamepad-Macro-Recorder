import json
import vgamepad as vg
from input_classes.input import Input
from input_classes.input_type import Type

DUALSENSE_SCHEME = "controller_schemes/dualsense.json"
DUALSENSE = "dualsense"

class GamepadToVGamepadMapper:
    def __init__(self, vg, gamepad_name=DUALSENSE):
        self.scheme = None

        if gamepad_name == DUALSENSE:
            with open(DUALSENSE_SCHEME, "r") as f:
                self.scheme = json.load(f)

        self.button_table = None
        self.vg = vg
        self._set_button_table(gamepad_name)



    def map_input(self, input: Input):
        if input.type == Type.BUTTON:
            return self._map_button(input)
        elif input.type == Type.AXIS:
            return self._map_axis(input)
        
    def _map_axis(self, input: Input):
        if input.type != Type.AXIS:
            raise ValueError("Input must be a AXIS")
        
        raise NotImplementedError
        
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