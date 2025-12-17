import pygame as pg
from config import BLACK
class Button():
    def __init__(self, x, y, image, scale, text, font, text_color= BLACK):
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False
        self.text = text
        self.font = font
        self.text_color = text_color
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        action = False
        pos = pg.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True

        if not pg.mouse.get_pressed()[0]:
            self.clicked = False

        # пересчитываем центр текста
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

        surface.blit(self.image, self.rect)
        surface.blit(self.text_surf, self.text_rect)

        return action
