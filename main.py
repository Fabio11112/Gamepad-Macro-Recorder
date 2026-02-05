import pygame as pg
from gamepad_reader import *

def main():
    pg.init()
    reader = GamepadReader(pg)
    reader.record()

    

if __name__ == "__main__":
    main()