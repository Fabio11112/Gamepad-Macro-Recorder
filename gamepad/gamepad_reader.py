from json_classes.json_recorder import JsonRecorder
from input_classes.input import Input
from input_classes.input_type import Type
from gamepad.gamepad_super import GamepadSuper
from configuration_manager.config_manager import ConfigManager
import time
import threading

DOWN = 0
UP = 1


class GamepadReader(GamepadSuper):
    """Reads and records gamepad input events
    """
    def __init__(self, pg: object, config: ConfigManager):
        """Constructor of the GamepadReader class.

        Args:
            pg (object): Pygame instance for handling gamepad events.
        """
        super().__init__(config)
        self.pg = pg
        self.joystick = None
        self.isRecording = False
        self.start_time = None
        gamepad_record = f"{self.config.get("paths.recording_folder_location")}/{self.config.get("gamepad.name")}_inputs.json"
        self.json_recorder = self.json_recorder = JsonRecorder(gamepad_record)

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

                if abs(value) < self.config.get("gamepad.dead_zone"):
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

    

    def _get_axis_name(self, input):
        if self._is_left_stick(input):
            return "left_stick"
        if self._is_right_stick(input):
            return "right_stick"
        if self._is_left_trigger(input):
            return "left_trigger"
        if self._is_right_trigger(input):
            return "right_trigger"



    





