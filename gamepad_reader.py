from json_recorder import JsonRecorder
from input import Input
from input_type import Type
import json
import time


DEAD_ZONE = 0.1
DUALSENSE_SCHEME = "controller_schemes/dualsense.json"
DUALSENSE_INPUT_RECORD = "dualsense_inputs.json"

DOWN = 0
UP = 1

class GamepadReader:
    def __init__(self, pg: object):
        self.pg = pg
        self.joystick = None
        self.scheme = None
        self.isRecording = False
        self.start_time = None

        with open(DUALSENSE_SCHEME) as f:
            self.scheme = json.load(f)

        pg.joystick.init()
        if not pg.joystick.get_init():
            print("Error when using 'pygame' library.")
            return
        print(f"There are {pg.joystick.get_count()} gamepads")

        self.joystick = pg.joystick.Joystick(0)

        if not self.joystick.get_init():
            print(f"Error when using the gamepad with id = {self.joystick.get_id()}")

        print(self.joystick.get_name())


        print(f"Num of joysticks = {self.joystick.get_numaxes()}")
        print(f"Num of buttons = {self.joystick.get_numbuttons()}")
        print(f"NUm of hats = {self.joystick.get_numhats()}")


    def record(self):
        self.isRecording = True
        self._read_input()


    def _read_input(self):

        json_recorder = JsonRecorder(DUALSENSE_INPUT_RECORD)
        self.start_time = time.time()

        while self.isRecording: 
            input = None
            for event in self.pg.event.get():
                if event.type == self.pg.QUIT:
                    print("Quitting.")
                    self.isRecording = False

                if event.type == self.pg.JOYBUTTONDOWN:
                    input = Input(event.button, Type.BUTTON, DOWN, self.start_time)
                    json_recorder.append(input)
                    #print(f"Button with id {event.button} down.")
                if event.type == self.pg.JOYBUTTONUP:
                    input = Input(event.button, Type.BUTTON, UP, self.start_time)
                    json_recorder.append(input)
                   #print(f"Button with id {event.button} up.")
                
                if event.type == self.pg.JOYAXISMOTION and (abs(event.value) >= DEAD_ZONE):
                    input = Input(event.axis, Type.AXIS, event.value, self.start_time)
                    json_recorder.append(input)
                    #print(f"Axis with id {event.axis} with value {event.value}.")

        print(f"is recording? {self.isRecording}")



    





