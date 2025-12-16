import pygame as pg
from Scenes.scene import Scene
from config import RED
class CreationScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:  # или любая клавиша
                    self.manager.switch_scene("menu")
    
    def render(self, screen):
        screen.fill(RED)