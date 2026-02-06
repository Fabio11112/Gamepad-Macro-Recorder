import pygame as pg
import vgamepad as vg
from gamepad.gamepad_reader import *
from gamepad.gamepad_repeater import *
from input_classes.input_collection import *
from json_classes.json_loader import JsonLoader

INPUT_FOLDER = "recordings"
DUALSENSE_INPUT_RECORD = f"{INPUT_FOLDER}/dualsense_inputs.json"

DEBUG = False
SAVE = True

def main():

    if DEBUG:
        loader = JsonLoader(DUALSENSE_INPUT_RECORD)
        loader.load()
        inputs = InputCollection(loader.getInputs())
        iterator = inputs.get_iterator()

        while iterator.hasNext():
            print(iterator.next())

    else:
        if SAVE:
            pg.init()
            reader = GamepadReader(pg)
            try:
                reader.record()
            except KeyboardInterrupt:
                reader.stop()
        else:
            repeater = GamepadRepeater(vg)


if __name__ == "__main__":
    main()
    
