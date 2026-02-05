import pygame as pg
from gamepad_reader import *


def main():
    pg.init()
    reader = GamepadReader(pg)
    try:
        reader.record()
    except KeyboardInterrupt:
        reader.stop()


if __name__ == "__main__":
    main()
    
