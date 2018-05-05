#Sprite classes for game
import pygame as pg
import random 
from settings import *
from os import path 

all_sprites = pg.sprite.Group()
enemy_1s = pg.sprite.Group()
bullets = pg.sprite.Group() 
en_bullets = pg.sprite.Group()
powerups = pg.sprite.Group()
meteors = pg.sprite.Group()

####### PLAYER CLASS #############
class Player(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		# self.image = player_img
		#scale the image
		self.image = pg.transform.scale(player_img,(50, 38))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		#giving the sprit a radius / know how big a circle to look at 
		self.radius = 20
		#draw a circle on top of the image
		# pg.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.centerx = WIDTH/2
		self.rect.bottom = HEIGHT - 10
		self.speedx = 0
		self.speedy = 0
		self.shield = 100
		self.shoot_delay = 250
		self.last_shot = pg.time.get_ticks()
		#setting player lives
		self.lives = 3
		self.hidden = False
		self.hide_timer = pg.time.get_ticks()
		#shoot one laser
		self.power = 1
		self.power_time = pg.time.get_ticks()

	def update(self):
  		#timeout for powerups
		if self.power >= 2 and pg.time.get_ticks() - self.power_time > POWERUP_TIME:
			self.power -= 1
			self.power_time = pg.time.get_ticks()

		#unhide if hidden after a seconds
		if self.hidden and pg.time.get_ticks() - self.hide_timer > 2000:
			self.hidden = False
			self.rect.center = (WIDTH / 2, HEIGHT - 30)
			# self.rect.centerx = WIDTH / 2
			# self.rect.bottom = HEIGHT - 10
		self.speedx = 0
		self.speedy = 0
		keystate = pg.key.get_pressed()
		if keystate[pg.K_LEFT]:
			self.speedx = -8
		if keystate[pg.K_RIGHT]:
			self.speedx = 8
		if keystate[pg.K_UP]:
  			self.speedy = -8
		if keystate[pg.K_DOWN]:
			self.speedy = 8
		if keystate[pg.K_SPACE]:
			self.shoot() 
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.right > WIDTH:
  			self.rect.right = WIDTH
		if self.rect.left < 0:
  			self.rect.left = 0 
		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT
		if self.rect.top < 0:
			self.rect.top = 0 

	def powerup(self):
		self.power += 1
		self.power_time = pg.time.get_ticks()

	def shoot(self):
		now = pg.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			if self.power == 1:
				bullet = Bullet(self.rect.centerx, self.rect.top, laser_img, -10)
				all_sprites.add(bullet)
				bullets.add(bullet)
				shoot_snd.play()
			if self.power >= 2:
				bullet1 = Bullet(self.rect.left, self.rect.centery, p_laser_img, -20)
				bullet2 = Bullet(self.rect.right, self.rect.centery, p_laser_img, -20)
				all_sprites.add(bullet1)
				all_sprites.add(bullet2)
				bullets.add(bullet1)
				bullets.add(bullet2)
				shoot_snd.play()
	
	#temporarily hide the player
	def hide(self):
		self.hidden = True
		self.hide_timer = pg.time.get_ticks()
		#hiding ship below the screen 
		self.rect.center = (WIDTH / 2, HEIGHT + 200)
  		
####### Enemy_1 CLASS #############
class Enemy_1(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image_orig = random.choice(enemy_images)
		self.image_orig.set_colorkey(BLACK)
		self.image = self.image_orig.copy()
		self.rect = self.image.get_rect()
		# find the width of rectangle / 2
		self.radius = int(self.rect.width * .85/ 2)
		# pg.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-150, -100)
		self.speedy = random.randrange(1, 8)
		self.speedx = random.randrange(-3, 3)
		#grabs number of ticks since clock started 
		self.last_update = pg.time.get_ticks()
		self.shoot_delay = 500
		self.last_shot = pg.time.get_ticks()

	def update(self):
		#makes it move downward 
		self.shoot()
		# enemy_shoot.play() 
		self.rect.x += self.speedx 
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 8)
	
	def shoot(self):
		now = pg.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			en_bullet = Bullet(self.rect.centerx, self.rect.bottom + 10, enemy_laser_img, 10)
			all_sprites.add(en_bullet)
			en_bullets.add(en_bullet)
			# enemy_shoot.play()

####### METEOR CLASS #############
class Meteor(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image_orig = random.choice(meteor_images)
		self.image_orig.set_colorkey(BLACK)
		self.image = self.image_orig.copy()
		self.rect = self.image.get_rect()
		# find the width of rectangle / 2
		self.radius = int(self.rect.width * .85/ 2)
		# pg.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-150, -100)
		self.speedy = random.randrange(1, 8)
		self.speedx = random.randrange(-3, 3)
		#how far in degree sprite should rotate
		self.rot = 0
		#have mod rotate in diff directions / how fast it rotates
		self.rot_speed = random.randrange(-8, 8)
		#grabs number of ticks since clock started 
		self.last_update = pg.time.get_ticks()
		self.shoot_delay = 500
		self.last_shot = pg.time.get_ticks()

	def rotate(self):
		now = pg.time.get_ticks()
		if now - self.last_update > 50:
			self.last_update = now
			#keep track of rotation, making it loop around
			self.rot = (self.rot + self.rot_speed) % 360
			new_image = pg.transform.rotate(self.image_orig, self.rot)
			#change rectange shape and size and keep the sprite centered when rotating 
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center 

	def update(self):
		self.rotate()
		#makes it move downward 
		self.rect.x += self.speedx 
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 8)
			if self.rect.top > HEIGHT or self.rect.left < WIDTH or self.rect.right > WIDTH:
  				self.kill()


####### BULLET CLASS #############
class Bullet(pg.sprite.Sprite):
  	#tell bullet to spawn at particular loc according to player
	def __init__(self, x, y, img, speedy):
		pg.sprite.Sprite.__init__(self)
		# self.image = laser_img
		self.image = img
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = speedy

	def update(self):
		self.rect.y += self.speedy
		#kill if it moves off the top of screen
		if self.rect.bottom < 0:
			self.kill()

####### POWERUPS CLASS #############
class Power(pg.sprite.Sprite):
	def __init__(self, center):
		pg.sprite.Sprite.__init__(self)
		self.type = random.choice(['shield', 'laser'])
		self.image = powerup_images[self.type]
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.speedy = 5

	def update(self):
		self.rect.y += self.speedy
		#kill if it moves off the top of screen
		if self.rect.top > HEIGHT:
			self.kill()

####### EXPLOSION CLASS #############
class Explosion(pg.sprite.Sprite):
	def __init__(self, center, size):
		pg.sprite.Sprite.__init__(self)
		self.size = size
		self.image = explosion_anim[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		#check the last time it updated
		self.last_update = pg.time.get_ticks()
		#set frame rate / how long we wait between each frame
		self.frame_rate = 20

	def update(self):
		#change image after enough time elapsed
		now = pg.time.get_ticks()
		#if it's been enough time; go again
		if now - self.last_update > self.frame_rate: 
			self.last_update = now
			self.frame += 1
			#destroy once animation is over 
			if self.frame == len(explosion_anim[self.size]):
				self.kill()
			else:
				#save center and create new image and set new center
				center = self.rect.center
				self.image = explosion_anim[self.size][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center