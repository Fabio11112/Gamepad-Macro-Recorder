import pygame as pg
from gamepad_reader import *

def main():
    pg.init()
    reader = GamepadReader(pg)
    reader.read_input()

if __name__ == "__main__":
    main()