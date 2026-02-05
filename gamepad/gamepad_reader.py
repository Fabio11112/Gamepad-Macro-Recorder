from json.json_recorder import JsonRecorder
from input.input import Input
from input.input_type import Type
import json
import time


DEAD_ZONE = 0.1
DUALSENSE_SCHEME = "controller_schemes/dualsense.json"
INPUT_FOLDER = "recordings"

DUALSENSE_INPUT_RECORD = f"{INPUT_FOLDER}/dualsense_inputs.json"

DOWN = 0
UP = 1


class GamepadReader:
    """_summary_Reads and records gamepad input events
    """
    def __init__(self, pg: object):
        """Constructor of the GamepadReader class.

        Args:
            pg (object): Pygame instance for handling gamepad events.
        """
        self.pg = pg
        self.joystick = None
        self.scheme = None
        self.isRecording = False
        self.start_time = None
        self.json_recorder = self.json_recorder = JsonRecorder(DUALSENSE_INPUT_RECORD)

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
        """Starts the "recording" of the button inputs and axises movements

        Raises:
            RuntimeError: When is started another recording when there's one already happening
        """
        if self.isRecording:
            raise RuntimeError("Cannot start recording: another recording has been already started")

        self.isRecording = True
        self._read_input()


    def stop(self):
        """Stops the "recording" that has been previously started

        Raises:
            RuntimeError: When there is no recording to stop
        """
        if not self.isRecording:
            raise RuntimeError("Cannot stop recording: no recording in progress") 

        self.isRecording = False
        self.json_recorder.save()

    def _read_input(self):

        self.start_time = time.time()

        while self.isRecording: 
            input = None
            for event in self.pg.event.get():
                if event.type == self.pg.QUIT:
                    print("Quitting.")
                    self.isRecording = False

                if event.type == self.pg.JOYBUTTONDOWN:
                    input = Input(event.button, Type.BUTTON, DOWN, self.start_time)
                    self.json_recorder.append(input)
                    
                if event.type == self.pg.JOYBUTTONUP:
                    input = Input(event.button, Type.BUTTON, UP, self.start_time)
                    self.json_recorder.append(input)
                
                if event.type == self.pg.JOYAXISMOTION and (abs(event.value) >= DEAD_ZONE):
                    input = Input(event.axis, Type.AXIS, event.value, self.start_time)
                    self.json_recorder.append(input)

        print(f"is recording? {self.isRecording}")
    
    



    





