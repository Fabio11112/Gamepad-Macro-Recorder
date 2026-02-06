from json_classes.json_recorder import JsonRecorder
from input_classes.input import Input
from input_classes.input_type import Type
from gamepad.gamepad_super import GamepadSuper
import time


DEAD_ZONE = 0.03
INPUT_FOLDER = "recordings"
OFFSET = 0.008

DUALSENSE_INPUT_RECORD = f"{INPUT_FOLDER}/dualsense_inputs.json"

DOWN = 0
UP = 1


class GamepadReader(GamepadSuper):
    """Reads and records gamepad input events
    """
    def __init__(self, pg: object):
        """Constructor of the GamepadReader class.

        Args:
            pg (object): Pygame instance for handling gamepad events.
        """
        super().__init__()
        self.pg = pg
        self.joystick = None
        self.isRecording = False
        self.start_time = None
        self.json_recorder = self.json_recorder = JsonRecorder(DUALSENSE_INPUT_RECORD)

        self.last_left_stick_timestamp = 0
        self.last_right_stick_timestamp = 0
        self.last_left_trigger_timestamp = 0
        self.last_right_trigger_timestamp = 0


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

                timestamp = time.perf_counter() - self.start_time

                if event.type == self.pg.JOYBUTTONDOWN:
                    input = Input(event.button, Type.BUTTON, DOWN, timestamp)
                    self.json_recorder.append(input)
                    
                if event.type == self.pg.JOYBUTTONUP:
                    input = Input(event.button, Type.BUTTON, UP, timestamp)
                    self.json_recorder.append(input)
                
                if event.type == self.pg.JOYAXISMOTION and (abs(event.value) >= DEAD_ZONE):     
                    input = Input(event.axis, Type.AXIS, event.value, timestamp)
                    axis_name = self._get_axis_name(input)

                    if not self._is_axis_in_offset(input, axis_name, OFFSET):
                        print(f"[DEBUG] Axis name {axis_name}")
                        self.json_recorder.append(input)

                        match axis_name:
                            case "left_stick":
                                self.last_left_stick_timestamp = input.timestamp
                                break
                            case "right_stick":
                                self.last_right_stick_timestamp = input.timestamp
                                break                            
                            case "left_trigger":
                                self.last_left_trigger_timestamp = input.timestamp
                                break
                            case "right_trigger":
                                self.last_right_trigger_timestampr = input.timestamp
                                break          


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

        if axis_name == "left_stick":
            delta = input.timestamp - self.last_left_stick_timestamp
            #print(f"[DEBUG] Delta value of left stick is {delta}")
        
        elif axis_name == "right_stick":
            delta = input.timestamp - self.last_right_stick_timestamp
            #print(f"[DEBUG] Delta value of right stick is {delta}")
        
        elif axis_name == "left_trigger":
            delta = input.timestamp - self.last_left_trigger_timestamp
            #print(f"[DEBUG] Delta value of left trigger is {delta}")
        
        elif axis_name == "right_trigger":
            delta = input.timestamp - self.last_right_trigger_timestamp
            #print(f"[DEBUG] Delta value of right trigger is {delta}")
        
        return offset >= delta
    

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



    





