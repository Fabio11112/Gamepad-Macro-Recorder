from json_classes.json_recorder import JsonRecorder
from input.input import Input
from input.input_type import Type
import json
import time


DEAD_ZONE = 0.1
DUALSENSE_SCHEME = "controller_schemes/dualsense.json"
INPUT_FOLDER = "recordings"
OFFSET = 0.01

DUALSENSE_INPUT_RECORD = f"{INPUT_FOLDER}/dualsense_inputs.json"

DOWN = 0
UP = 1


class GamepadReader:
    """Reads and records gamepad input events
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


        self.last_left_stick = None
        self.last_right_stick = None
        self.last_left_trigger = None
        self.last_right_trigger = None

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

        self.start_time = time.perf_counter()

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
                    timestamp = time.perf_counter() - self.start_time
                    input = Input(event.axis, Type.AXIS, event.value, timestamp)
                    axis_name = self._get_axis_name(input)

                    if not self._is_axis_in_offset(input, axis_name, OFFSET):
                        print(f"[DEBUG] Axis name {axis_name}")
                        self.json_recorder.append(input)

                        match axis_name:
                            case "left_stick":
                                self.last_left_stick = input
                                break
                            case "right_stick":
                                self.last_right_stick = input
                                break                            
                            case "left_trigger":
                                self.last_left_trigger = input
                                break
                            case "right_trigger":
                                self.last_right_trigger = input
                                break          
                    else:
                        print ("IN OFFSET")         


        print(f"is recording? {self.isRecording}")
    
    
    def _is_axis_in_offset(self, input: Input, axis_name: str,  offset: float)-> bool:
        """Returns true if the next input timestamp for a certain axis is less than **offset**.
        E.g.: If the next left_trigger value happened in less than **offset** seconds, then it returns True

        Args:
            input (Input): The input got from the gamepad
            offset (float): The value the delta of the timestamps is compared with

        Raises:
            ValueError: If the input is not a Type.AXIS

        Returns:
            bool: True if the delta of the inputs is less than **offset**
        """

        delta = 0
        if input.type == Type.BUTTON:
            raise ValueError("Input must be a AXIS Type")

        if axis_name == "left_stick" and self.last_left_stick is not None:
            delta = input.timestamp - self.last_left_stick.timestamp
            #print(f"[DEBUG] Delta value of left stick is {delta}")
            return offset <= delta
        
        if axis_name == "right_stick" and self.last_right_stick is not None:
            delta = input.timestamp - self.last_right_stick.timestamp
            #print(f"[DEBUG] Delta value of right stick is {delta}")
            return offset <= delta
        
        if axis_name == "left_trigger" and self.last_left_trigger is not None:
            delta = input.timestamp - self.last_left_trigger.timestamp
            #print(f"[DEBUG] Delta value of left trigger is {delta}")
            return offset <= delta
        
        if axis_name == "right_trigger" and self.last_right_trigger is not None:
            delta = input.timestamp - self.last_right_trigger.timestamp
            #print(f"[DEBUG] Delta value of right trigger is {delta}")
            return offset <= delta
        

    def _is_left_stick(self, input):
        
        return input.id in self.scheme["axis"]["left_stick"].values()

    def _is_right_stick(self, input):
        return input.id in self.scheme["axis"]["right_stick"].values()

    def _is_left_trigger(self, input):
        return input.id == self.scheme["axis"]["triggers"]["left"]

    def _is_right_trigger(self, input):
        return input.id == self.scheme["axis"]["triggers"]["right"]
    
    

    def _get_axis_name(self, input):
        # print(f"[LEFT STICK ID]{self.scheme["axis"]["left_stick"]}")
        # print(f"[RIGHT STICK ID]{self.scheme["axis"]["right_stick"]}")
        # print(f"[LEFT TRIGGER ID]{self.scheme["axis"]["triggers"]["left"]}")
        # print(f"[RIGHT TRIGGER ID]{self.scheme["axis"]["triggers"]["right"]}")


        if self._is_left_stick(input):
            return "left_stick"
        if self._is_right_stick(input):
            return "right_stick"
        if self._is_left_trigger(input):
            return "left_trigger"
        if self._is_right_trigger(input):
            return "right_trigger"



    





