import pygame as pg

class Button():
	def __init__(self, x, y, image, scale, text, font):
		width = image.get_width()
		height = image.get_height()
		self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.action = False
		self.text = "text"
		self.font = font
		self.text_surf = self.font.render(self.text, True)
		self.text_rect = self.text_surf.get_rect(center=self.rect.center)

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pg.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pg.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))
		return action