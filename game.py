#ALPHA DESCENT GAME
#Music: Reusenoise  (DNB Mix) by spinningmerkaba (c) copyright 2017 Licensed under a Creative Commons Attribution (3.0) license. 
#Art from Kenney.nl

import pygame as pg
import random 
from settings import *
from sprites import * 
from os import path 

game_over = True      

class Game:
	def __init__(self):
		#initalize game window
		pg.init()
		pg.mixer.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		self.running = True 
		self.game_over = True 

	def newmob(self):
		self.m = Mob()
		self.all_sprites.add(self.m)
		mobs.add(self.m)
  	
	def draw_text(self, surf, text, size, x, y):
		self.font = pg.font.Font(font_name, size)
		#true means anti-aliased
		self.text_surface = self.font.render(text, True, WHITE)
		self.text_rect = self.text_surface.get_rect()
		self.text_rect.midtop = (x, y)
		surf.blit(self.text_surface, self.text_rect)
	
	def draw_shield_bar(self,surf, x, y, pct):
		if pct < 0:
			pct = 0
		self.BAR_LENGTH = 100
		self.BAR_HEIGHT = 10
		self.fill = (pct / 100) * self.BAR_LENGTH 
		self.outline_rect = pg.Rect(x, y, self.BAR_LENGTH, self.BAR_HEIGHT)
		self.fill_rect = pg.Rect( x, y, self.fill, self.BAR_HEIGHT)
		pg.draw.rect(surf, GREEN, self.fill_rect)
		#last arg is for how wide you want rect to be
		pg.draw.rect(surf, WHITE, self.outline_rect, 2)
	
	def draw_lives(self, surf, x, y, lives, img):
		for i in range(lives):
			self.img_rect = img.get_rect()
			#gives a nice gap between image
			self.img_rect.x = x + 30 * i 
			self.img_rect.y = y
			surf.blit(img, self.img_rect)

	def new(self):
		self.all_sprites = all_sprites
		self.mobs = pg.sprite.Group()
		self.player = Player()
		self.all_sprites.add(self.player)
		self.score = 0
		for i in range(5):
  			self.newmob()
		self.run()
	
	def run(self):
		#game loop
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()
	
	def update(self):
  		#game loop update
		self.all_sprites.update()
		##### PLAYER HIT MOB / true for both so both get deleted ###########
		self.hits = pg.sprite.groupcollide(mobs, bullets, True, True)
		#respawn the mob
		for hit in self.hits:
			self.score += 50 - hit.radius
			#play random sound in list 
			random.choice(expl_snds).play()
			self.expl = Explosion(hit.rect.center, 'lg')
			self.all_sprites.add(self.expl) 
			if random.random() > 0.9:
				self.power = Power(hit.rect.center)
				self.all_sprites.add(self.power)
				powerups.add(self.power)
			self.newmob()

		#player's bullets hit mob bullets 
		self.hits = pg.sprite.groupcollide(en_bullets, bullets, True, True)
		#respawn the mob
		for hit in self.hits:
			self.score += 70 
			#play random sound in list 
			random.choice(expl_snds).play()
			self.expl = Explosion(hit.rect.center, 'sm')
			self.all_sprites.add(self.expl) 
		
		#####POWERUPS HIT PLAYER ##################
		self.hits = pg.sprite.spritecollide(self.player, powerups, True)
		for hit in self.hits:
			if hit.type == 'shield':
				powerup_shield_snd.play()
				self.player.shield += random.randrange(10, 30)
				if self.player.shield >= 100:
					self.player.shield = 100

			if hit.type == 'laser':
				powerup_bolt_snd.play() 
				self.player.powerup()
				
		##### MOB HIT PLAYER / circle specifies type of collision ##########
		self.hits = pg.sprite.spritecollide(self.player, mobs, True, pg.sprite.collide_circle)
		for hit in self.hits:
			random.choice(expl_snds).play()
			self.player.shield -= hit.radius * 2
			self.expl = Explosion(hit.rect.center, 'sm')
			self.all_sprites.add(self.expl) 
			self.newmob()
			if self.player.shield <= 0:
				player_death_snd.play() 
				self.death_expl = Explosion(self.player.rect.center, 'player')
				all_sprites.add(self.death_expl)
				self.player.hide()
				self.player.lives -= 1
				self.player.shield = 100

		self.hits = pg.sprite.spritecollide(self.player, en_bullets, True, pg.sprite.collide_circle)
		for hit in self.hits:
			random.choice(expl_snds).play()
			self.player.shield -= 2
			self.expl = Explosion(hit.rect.center, 'sm')
			self.all_sprites.add(self.expl) 
			if self.player.shield <= 0:
				player_death_snd.play() 
				self.death_expl = Explosion(self.player.rect.center, 'player')
				self.all_sprites.add(self.death_expl)
				self.player.hide()
				self.player.lives -= 1
				self.player.shield = 100
		
		# if player died and explosion finished playing
		if self.player.lives == 0 and not self.death_expl.alive():
			#game over 
			game_over = True

	def events(self):
  		#game loop - events
		for event in pg.event.get():
			if event.type == pg.QUIT:
				if self.playing:
					self.playing = False
				self.running = False

	def draw(self):
		#game loop - draw
		self.screen.fill(BLACK)
		self.screen.blit(background, background_rect)
		self.all_sprites.draw(self.screen)
		self.draw_text(self.screen, str(self.score), 18, WIDTH / 2, 10)
		self.draw_shield_bar(self.screen, 5, 5, self.player.shield)
		self.draw_lives(self.screen, WIDTH - 100, 5, self.player.lives, player_mini_img)
		pg.display.flip()
	
	def show_start_screen(self):
  		#game splash/start screen
		pass
	
	def show_gameover_screen(self):
		#game over/continue
		self.screen.blit(background, background_rect)
		self.draw_text(screen, "ALPHA DESCENT", 64, WIDTH/2, HEIGHT /4)
		self.draw_text(screen, "Arrow keys move, Spacebar to fire", 22, WIDTH / 2, HEIGHT / 2)
		self.draw_text(screen, "Press any key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
		pg.display.flip()
		self.waiting = True
		while self.waiting:
			self.clock.tick(FPS)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
				if event.type == pg.KEYUP:
					self.waiting = False 
					
	
g = Game()
g.show_start_screen()
while g.running:
	if game_over:
		g.show_gameover_screen()
		game_over = False
		g.new()
pg.quit()
	



