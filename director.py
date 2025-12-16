import pygame as pg
import sys
import time
from config import WIDTH, HEIGHT, FPS
from Scenes import *
class Director():
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.current_scene = None
        self.running = True
        self.clock = pg.time.Clock()
        self.FPS = FPS
        self.scenes = {
            "menu": MenuScene(self),
            "creation": CreationScene(self),
        }
        pg.init()
        pg.mixer.init()
        pg.display.set_caption("KOTY")
        self.current_scene = self.scenes["menu"]

    def switch_scene(self, scene_name):
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]
            
    def quit(self):
        self.running = False
    
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS)/1000
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.running = False
            
            self.current_scene.handle_events(events)
            self.current_scene.update(dt)
            self.current_scene.render(self.screen)
            pg.display.flip()
        
        pg.quit()
        sys.exit()
    