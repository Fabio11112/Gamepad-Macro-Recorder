import pygame as pg
import vgamepad as vg
from gamepad.gamepad_reader import *
from gamepad.gamepad_repeater import *
from input_classes.input_collection import *
from json_classes.json_loader import JsonLoader

#INPUT_FOLDER = "recordings"
#DUALSENSE_INPUT_RECORD = f"{INPUT_FOLDER}/dualsense_inputs.json"

RECORD = 0
REPEAT = 1
REPEAT_INDEFINITELY = 2

def main():
        menu = "What do you want to do?\n0 - Record\n1 - Repeat once your recording\n2 - Repeat Indefinitely you recording\n>>>"
        option = int(input(menu))
        configuration = ConfigManager()
        if option == RECORD:
            pg.init()
            reader = GamepadReader(pg, configuration)
            try:
                reader.record()
            except KeyboardInterrupt:
                reader.stop()
        elif option == REPEAT:
            repeater = GamepadRepeater(vg, configuration)
            input("ENTER to start")
            repeater.replay()

        elif option == REPEAT_INDEFINITELY:
            repeater = GamepadRepeater(vg, configuration)
            input("ENTER to start")

            while True:
                print("[DEBUG] START REPLAY")
                repeater.replay()
                print("[DEBUG] END OF REPLAY AND WAITING")
                time.sleep(5)
                print("[DEBUG] END OF WAITING")

        else:
            raise ValueError("Not a valid option.")


if __name__ == "__main__":
    main()
    
