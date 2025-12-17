import pygame as pg
import random
import time
import os
from director import Director
def main():
    dir = Director()
    dir.run()
if __name__ == '__main__':
    pg.init()
    main()