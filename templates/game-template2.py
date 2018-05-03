#ALPHA DESCENT GAME
#Music: Reusenoise  (DNB Mix) by spinningmerkaba (c) copyright 2017 Licensed under a Creative Commons Attribution (3.0) license. 
#Art from Kenney.nl

import pygame as pg
import random 
from settings import *
from os import path

class Game:
	def __init__(self):
		#initalize game window
		pg.init()
		pg.mixer.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
    	self.running = True 

	def new(self):
		all_sprites = pg.sprite.Group()
		self.run()
	
	def run(self):
  		#game loop
  		self.play = True
		while self.play:
  			self.clock.ticks(FPS)
			self.events()
			self.update()
			self.draw()
	
	def update(self):
  		#game loop update
		self.all_sprites.update()
	
	def events(self):
  		#game loop - events
		for event in pg.event.get():
			if event.type == pg.QUIT:
  				if self.playing
  					self.playing = False
				self.running = False
	
	def draw(self):
		#game loop - draw
		self.screen.fill(BLACK)
		self.screen.blit(background, background_rect)
		self.all_sprites.draw(self.screen)
		pg.display.flip()
	
	def show_start_screen(self):
  		#game splash/start screen
		pass
	
	def show_gameover_screen(self):
  		#game over/continue
		pass 
	
g = Game()
g.show_start_screen()
while g.running:
  	g.new()
	g.show_gameover_screen()
pg.quit()
	



