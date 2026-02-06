from json_classes.json_recorder import JsonRecorder
from input_classes.input import Input
from input_classes.input_type import Type
from gamepad.gamepad_super import GamepadSuper
import time
import threading


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

        self.poll_thread = None
        self.poll_interval = 0.008 #125Hz polling rate

        self.last_left_stick_timestamp = 0
        self.last_right_stick_timestamp = 0
        self.last_left_trigger_timestamp = 0
        self.last_right_trigger_timestamp = 0


    def record(self):
        """Starts the "recording" of the button inputs and axises movements

        Raises:
            RuntimeError: When is started another recording when there's one already happening
        """
        if self.isRecording:
            raise RuntimeError("Cannot start recording: another recording has been already started")

        if self.pg.joystick.get_count() == 0:
            raise SystemError("No joystick connected")

        self.joystick = self.pg.joystick.Joystick(0)
        self.joystick.init()
        self.isRecording = True
        self.start_time = time.perf_counter()

        self.poll_thread = threading.Thread(target=self._poll_axes, daemon=True)
        self.poll_thread.start()

        self._read_button_events()

    def _read_button_events(self):
        """Handle button press/release events"""
        while self.isRecording:
            for event in self.pg.event.get():
                if event.type == self.pg.JOYBUTTONDOWN:
                    timestamp = time.perf_counter() - self.start_time
                    input = Input(event.button, Type.BUTTON, DOWN, timestamp)
                    self.json_recorder.append(input)

                elif event.type == self.pg.JOYBUTTONUP:
                    timestamp = time.perf_counter() - self.start_time
                    input = Input(event.button, Type.BUTTON, UP, timestamp)
                    self.json_recorder.append(input)
            time.sleep(0.001)

    def _poll_axes(self):
        """Poll all axes at fixed intervals for smooth recording"""
        last_values = {}

        while self.isRecording:
            loop_start = time.perf_counter()
            timestamp = loop_start - self.start_time

            for axis_id in range(self.joystick.get_numaxes()):
                value = self.joystick.get_axis(axis_id)

                if abs(value) < DEAD_ZONE:
                    value = 0

                if axis_id not in last_values or abs(value - last_values[axis_id]) > 0.01:
                    input = Input(axis_id, Type.AXIS, value, timestamp)
                    self.json_recorder.append(input)
                    last_values[axis_id] = value

            elapsed = time.perf_counter() - loop_start
            sleep_time = max(0, self.poll_interval - elapsed)
            time.sleep(sleep_time)

    def stop(self):
        """Stops the "recording" that has been previously started

        Raises:
            RuntimeError: When there is no recording to stop
        """
        if not self.isRecording:
            raise RuntimeError("Cannot stop recording: no recording in progress") 

        self.isRecording = False
        if self.poll_thread:
            self.poll_thread.join(timeout=1.0)
        self.json_recorder.save()



    # def _read_input(self):

    #     self.start_time = time.perf_counter()

    #     while self.isRecording: 
    #         input = None
    #         for event in self.pg.event.get():
    #             if event.type == self.pg.QUIT:
    #                 print("Quitting.")
    #                 self.isRecording = False

    #             timestamp = time.perf_counter() - self.start_time

    #             if event.type == self.pg.JOYBUTTONDOWN:
    #                 input = Input(event.button, Type.BUTTON, DOWN, timestamp)
    #                 self.json_recorder.append(input)
                    
    #             if event.type == self.pg.JOYBUTTONUP:
    #                 input = Input(event.button, Type.BUTTON, UP, timestamp)
    #                 self.json_recorder.append(input)
                
    #             if event.type == self.pg.JOYAXISMOTION and (abs(event.value) >= DEAD_ZONE):     
    #                 input = Input(event.axis, Type.AXIS, event.value, timestamp)
    #                 axis_name = self._get_axis_name(input)

    #                 if not self._is_axis_in_offset(input, axis_name, OFFSET):
    #                     print(f"[DEBUG] Axis name {axis_name}")
    #                     self.json_recorder.append(input)

    #                     match axis_name:
    #                         case "left_stick":
    #                             self.last_left_stick_timestamp = input.timestamp
    #                             break
    #                         case "right_stick":
    #                             self.last_right_stick_timestamp = input.timestamp
    #                             break                            
    #                         case "left_trigger":
    #                             self.last_left_trigger_timestamp = input.timestamp
    #                             break
    #                         case "right_trigger":
    #                             self.last_right_trigger_timestampr = input.timestamp
    #                             break          


    #     print(f"is recording? {self.isRecording}")
    
    
    # def _is_axis_in_offset(self, input: Input, axis_name: str,  offset: float)-> bool:
    #     """Returns true if the next input timestamp for a certain axis is less than **offset**.
    #     E.g.: If the next left_trigger value happened in less than **offset** seconds, then it returns True

    #     Args:
    #         input (Input): The input got from the gamepad
    #         offset (float): The value the delta of the timestamps is compared with

    #     Raises:
    #         ValueError: If the input is not a Type.AXIS

    #     Returns:
    #         bool: True if the delta of the inputs is less than **offset**
    #     """

    #     delta = 0
    #     if input.type == Type.BUTTON:
    #         raise ValueError("Input must be a AXIS Type")

    #     if axis_name == "left_stick":
    #         delta = input.timestamp - self.last_left_stick_timestamp
    #         #print(f"[DEBUG] Delta value of left stick is {delta}")
        
    #     elif axis_name == "right_stick":
    #         delta = input.timestamp - self.last_right_stick_timestamp
    #         #print(f"[DEBUG] Delta value of right stick is {delta}")
        
    #     elif axis_name == "left_trigger":
    #         delta = input.timestamp - self.last_left_trigger_timestamp
    #         #print(f"[DEBUG] Delta value of left trigger is {delta}")
        
    #     elif axis_name == "right_trigger":
    #         delta = input.timestamp - self.last_right_trigger_timestamp
    #         #print(f"[DEBUG] Delta value of right trigger is {delta}")
        
    #     return offset >= delta
    

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



    





