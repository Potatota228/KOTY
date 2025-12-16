import pygame as pg
from Scenes.scene import Scene
from config import BLUE
class MenuScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:  # или любая клавиша
                    self.director.switch_scene("creation")
    
    def render(self, screen):
        screen.fill(BLUE)

