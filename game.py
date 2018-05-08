#ALPHA DESCENT GAME
#Music: Reusenoise  (DNB Mix) by spinningmerkaba (c) copyright 2017 Licensed under a Creative Commons Attribution (3.0) license. 
#Art from Kenney.nl

import pygame as pg
import random 
from settings import *
from sprites import * 
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
		self.game_over = True
		self.counter = 300
		# self.text = '10'.rjust(3) 
		self.timer = pg.time.set_timer(pg.USEREVENT, 1000)
		self.timer_str = ""
  		
	def newenemy_1(self):
		self.e1 = Enemy_1()
		self.all_sprites.add(self.e1)
		enemy_1s.add(self.e1)

	def newenemy_2(self):
		self.e2 = Enemy_2()
		self.all_sprites.add(self.e2)
		enemy_2s.add(self.e2)
	
	def newmeteors(self):
		self.m = Meteor()
		self.all_sprites.add(self.m)
		meteors.add(self.m)
  	
	def draw_text(self, surf, text, size, x, y, color):
		self.font = pg.font.Font(font_name, size)
		#true means anti-aliased
		self.text_surface = self.font.render(text, True, color)
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
		self.score = 0
		self.phase = 0 
		self.player = Player()
		self.all_sprites.add(self.player)
		for i in range(5):
			self.newenemy_1()
		self.run()
	
	def run(self):
		#game loop
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()
	
	def laser_hits_e1(self):
		self.hits = pg.sprite.groupcollide(enemy_1s, bullets, True, True)
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
			self.newenemy_1()

	def laser_hits_e2(self):
		self.hits = pg.sprite.groupcollide(enemy_2s, bullets, True, True)
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
			
	def e1_hits_player(self):
		self.hits = pg.sprite.spritecollide(self.player, enemy_1s, True, pg.sprite.collide_circle)
		for hit in self.hits:
			random.choice(expl_snds).play()
			self.player.shield -= hit.radius * 2
			self.expl = Explosion(hit.rect.center, 'sm')
			self.all_sprites.add(self.expl) 
			self.newenemy_1()
			if self.player.shield <= 0:
				player_death_snd.play() 
				self.death_expl = Explosion(self.player.rect.center, 'player')
				all_sprites.add(self.death_expl)
				self.player.hide()
				self.player.lives -= 1
				self.player.shield = 100

	def e2_hits_player(self):
		self.hits = pg.sprite.spritecollide(self.player, enemy_2s, True, pg.sprite.collide_circle)
		for hit in self.hits:
			random.choice(expl_snds).play()
			self.player.shield -= hit.radius * 2
			self.expl = Explosion(hit.rect.center, 'sm')
			self.all_sprites.add(self.expl) 
			self.newenemy_2()
			if self.player.shield <= 0:
				player_death_snd.play() 
				self.death_expl = Explosion(self.player.rect.center, 'player')
				all_sprites.add(self.death_expl)
				self.player.hide()
				self.player.lives -= 1
				self.player.shield = 100
	
	def enbullets_hit_player(self):
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

	def enbullets2_hit_player(self):
		self.hits = pg.sprite.spritecollide(self.player, en2_bullets, True, pg.sprite.collide_circle)
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
		
	def laser_hits_enbullets(self):
  		#player's bullets hit mob bullets 
		self.hits = pg.sprite.groupcollide(en_bullets, bullets, True, True)
		#respawn the mob
		for hit in self.hits:
			self.score += 70 
			#play random sound in list 
			random.choice(expl_snds).play()
			self.expl = Explosion(hit.rect.center, 'sm')
			self.all_sprites.add(self.expl) 

	def laser_hits_en2bullets(self):
		#player's bullets hit mob bullets 
		self.hits = pg.sprite.groupcollide(en2_bullets, bullets, True, True)
		#respawn the mob
		for hit in self.hits:
			self.score += 90 
			#play random sound in list 
			random.choice(expl_snds).play()
			self.expl = Explosion(hit.rect.center, 'sm')
			self.all_sprites.add(self.expl) 
	
	def laser_hits_meteors(self):
		self.hits = pg.sprite.groupcollide(meteors, bullets, True, True)
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
			self.newmeteors()
		
	def meteors_hit_player(self):
		self.hits = pg.sprite.spritecollide(self.player, meteors, True, pg.sprite.collide_circle)
		for hit in self.hits:
			random.choice(expl_snds).play()
			self.player.shield -= hit.radius * 2
			self.expl = Explosion(hit.rect.center, 'sm')
			self.all_sprites.add(self.expl)
			self.newmeteors()
			if self.player.shield <= 0:
				player_death_snd.play() 
				self.death_expl = Explosion(self.player.rect.center, 'player')
				all_sprites.add(self.death_expl)
				self.player.hide()
				self.player.lives -= 1
				self.player.shield = 100

	def power_hits_player(self):
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

	def update_phase(self):
		if self.playing:
			if self.counter <= 280:
				self.phase = 1
				for sprite in enemy_1s:
					sprite.kill() 
				if random.random() > 0.8:
					self.newmeteors()
			if self.counter <= 260:
				self.phase = 2
				for sprite in meteors:
  					sprite.kill() 
				if random.random() > 0.9:
					self.newenemy_2()

	def player_death(self):
  		# if player died and explosion finished playing
		if self.player.lives == 0 and not self.death_expl.alive():
			#game over 
			self.playing = False
			for sprite in self.all_sprites:
				sprite.kill() 
			self.counter = 300 
		
	def update(self):
  		#game loop update
		self.all_sprites.update()
		# self.timer()
		self.laser_hits_e1()
		self.laser_hits_e2()
		self.laser_hits_enbullets()
		self.laser_hits_en2bullets()
		self.power_hits_player()
		self.e1_hits_player()
		self.e2_hits_player()
		self.enbullets_hit_player()
		self.enbullets2_hit_player()
		self.meteors_hit_player()
		self.laser_hits_meteors()
		self.update_phase()
		self.player_death()
		
	def events(self):
  		#game loop - events
		for event in pg.event.get():
			if event.type == pg.USEREVENT:
				self.counter -= 1
				self.timer_str = str(self.counter).rjust(3)
				if self.counter == 0: 
					self.playing = False 
					for sprite in self.all_sprites:
  						sprite.kill() 
					self.counter = 300
			if event.type == pg.QUIT:
				if self.playing:
					self.playing = False
				self.running = False

	def draw(self):
		#game loop - draw
		self.screen.fill(BLACK)
		self.screen.blit(background, background_rect)
		self.all_sprites.draw(self.screen)
		#draw levels
		self.draw_text(self.screen, "PHASE: " + str(self.phase), 18, WIDTH * 1.3 / 4, 10, WHITE)
		self.draw_text(self.screen, self.timer_str, 18, WIDTH * 1 / 2, 10, WHITE)
		self.draw_text(self.screen, "SCORE: " + str(self.score), 18, WIDTH * 2.7 / 4, 10, WHITE)
		self.draw_shield_bar(self.screen, 5, 5, self.player.shield)
		self.draw_lives(self.screen, WIDTH - 100, 5, self.player.lives, player_mini_img)
		pg.display.flip()
	
	def wait_for_key(self):
		waiting = True
		while waiting:
			self.clock.tick(30)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					waiting = False
					self.running = False
				if event.type == pg.MOUSEBUTTONDOWN:
					waiting = False
			
	def show_start_screen(self):
		#game splash/start screen
		self.screen.blit(start_screen, start_screen_rect)
		self.draw_text(screen, "ALPHA DESCENT", 64, WIDTH/2, HEIGHT /4, WHITE)
		self.draw_text(screen, "Arrow keys to move | Spacebar to fire.", 22, WIDTH / 2, HEIGHT / 2, WHITE)
		self.draw_text(screen, "Click mouse to continue.", 18, WIDTH / 2, HEIGHT * 3 / 4, WHITE)
		self.draw_text(screen, "© 2018 Carla Severe", 15, WIDTH / 2, HEIGHT * 3.6 / 4, WHITE)
		pg.display.flip()
		self.wait_for_key() 
				
	def show_gameover_screen(self):
		#game over
		if not self.running:
  			return
		self.screen.fill(BLACK)
		self.screen.blit(background, background_rect)
		self.draw_text(screen, "GAME OVER", 64, WIDTH / 2, HEIGHT / 4, RED)
		self.draw_text(screen, "Score: " + str(self.score), 64, WIDTH / 2, HEIGHT * 3 / 4, RED)
		self.draw_text(screen, "Click mouse to play again", 18, WIDTH / 2, HEIGHT * 3.6 / 4, WHITE)
		pg.display.flip()
		self.wait_for_key() 


g = Game()
g.show_start_screen()
while g.running:
	g.new()
	g.show_gameover_screen()
pg.quit()
	



