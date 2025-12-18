from config import BROWN

class Text():
    def __init__(self, x, y, text, font, text_color = BROWN, center=True):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.text_color = text_color
        self.center = center
        
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect()
        
        # Размещаем текст по координатам
        if center:
            self.text_rect.center = (x, y)
        else:
            self.text_rect.topleft = (x, y)
    
    def draw(self, surface):
        surface.blit(self.text_surf, self.text_rect)
    
    def update_text(self, new_text):
        """Обновить текст"""
        self.text = new_text
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.text_rect.center if self.center else self.text_rect.topleft)
    
    def set_position(self, x, y):
        """Изменить позицию текста"""
        self.x = x
        self.y = y
        if self.center:
            self.text_rect.center = (x, y)
        else:
            self.text_rect.topleft = (x, y)
