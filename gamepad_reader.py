import json
DEAD_ZONE = 0.1

class GamepadReader:
    def __init__(self, pg):
        record = []
        self.pg = pg
        self.joystick = None
        self.scheme = None
        isRecording = False

        with open("controller_schemes/dualsense.json") as f:
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
        self.read_input()


    def read_input(self):
        while self.isRecording: 
            for event in self.pg.event.get():
                if event.type == self.pg.QUIT:
                    done = True

                #print(self.joystick.get_axis(0))

                if event.type == self.pg.JOYBUTTONDOWN:
                    print(f"Button with id {event.button} down")

                if event.type == self.pg.JOYBUTTONUP:
                    print(f"Button with id {event.button} up")
                
                if event.type == self.pg.JOYAXISMOTION and (abs(event.value) >= DEAD_ZONE):
                    print(f"Axis with id {event.axis} with value {event.value}")



    





