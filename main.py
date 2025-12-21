import pygame as pg
import random
import time
from director import Director
from cat.cat_manager import CatManager
def main():
    dir = Director()
    dir.run()
    cat_manager = CatManager()
if __name__ == '__main__':
    pg.init()
    main()