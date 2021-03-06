#ALPHA DESCENT GAME
#Music: Reusenoise  (DNB Mix) by spinningmerkaba (c) copyright 2017 Licensed under a Creative Commons Attribution (3.0) license. 
#Art from Kenney.nl

import pygame
import random 
from os import path 

img_dir = path.join(path.dirname(__file__), 'img')
enemy_dir = path.join(path.dirname(__file__), 'img/enemy')
snd_dir = path.join(path.dirname(__file__), 'snd')
expl_dir = path.join(path.dirname(__file__), 'img/expl')
expl_1dir = path.join(path.dirname(__file__), 'img/expl_1')

#initialize pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

####### DRAWING TEXT ON SCREEN #############
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	#true means anti-aliased
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

####### CREATING NEW MOB #############
def newmob():
	m = Mob()
	all_sprites.add(m)
	mobs.add(m)
  	
####### DRAWING SHIELD BAR | LIVES #############
def draw_shield_bar(surf, x, y, pct):
	if pct < 0:
		pct = 0
	BAR_LENGTH = 100
	BAR_HEIGHT = 10
	fill = (pct / 100) * BAR_LENGTH 
	outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
	fill_rect = pygame.Rect( x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surf, GREEN, fill_rect)
	#last arg is for how wide you want rect to be
	pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
	for i in range(lives):
		img_rect = img.get_rect()
		#gives a nice gap between image
		img_rect.x = x + 30 * i 
		img_rect.y = y
		surf.blit(img, img_rect)

####### PLAYER CLASS #############
class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		# self.image = player_img
		#scale the image
		self.image = pygame.transform.scale(player_img,(50, 38))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		#giving the sprit a radius / know how big a circle to look at 
		self.radius = 20
		#draw a circle on top of the image
		# pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.centerx = WIDTH/2
		self.rect.bottom = HEIGHT - 10
		self.speedx = 0
		self.speedy = 0
		self.shield = 100
		self.shoot_delay = 250
		self.last_shot = pygame.time.get_ticks()
		#setting player lives
		self.lives = 3
		self.hidden = False
		self.hide_timer = pygame.time.get_ticks()
		#shoot one laser
		self.power = 1
		self.power_time = pygame.time.get_ticks()

	def update(self):
  		#timeout for powerups
		if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
			self.power -= 1
			self.power_time = pygame.time.get_ticks()

		#unhide if hidden after a seconds
		if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2000:
			self.hidden = False
			self.rect.center = (WIDTH / 2, HEIGHT - 30)
			# self.rect.centerx = WIDTH / 2
			# self.rect.bottom = HEIGHT - 10
		self.speedx = 0
		self.speedy = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx = -8
		if keystate[pygame.K_RIGHT]:
			self.speedx = 8
		if keystate[pygame.K_UP]:
  			self.speedy = -8
		if keystate[pygame.K_DOWN]:
			self.speedy = 8
		if keystate[pygame.K_SPACE]:
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
		self.power_time = pygame.time.get_ticks()

	def shoot(self):
		now = pygame.time.get_ticks()
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
		self.hide_timer = pygame.time.get_ticks()
		#hiding ship below the screen 
		self.rect.center = (WIDTH / 2, HEIGHT + 200)
  		
####### MOB CLASS #############
class Mob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_orig = random.choice(enemy_images)
		self.image_orig.set_colorkey(BLACK)
		self.image = self.image_orig.copy()
		self.rect = self.image.get_rect()
		# find the width of rectangle / 2
		self.radius = int(self.rect.width * .85/ 2)
		# pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-150, -100)
		self.speedy = random.randrange(1, 8)
		self.speedx = random.randrange(-3, 3)
		#how far in degree sprite should rotate
		self.rot = 0
		#have mod rotate in diff directions / how fast it rotates
		self.rot_speed = random.randrange(-8, 8)
		#grabs number of ticks since clock started 
		self.last_update = pygame.time.get_ticks()
		self.shoot_delay = 500
		self.last_shot = pygame.time.get_ticks()

	def rotate(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > 50:
			self.last_update = now
			#keep track of rotation, making it loop around
			self.rot = (self.rot + self.rot_speed) % 360
			new_image = pygame.transform.rotate(self.image_orig, self.rot)
			#change rectange shape and size and keep the sprite centered when rotating 
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center 

	def update(self):
		# self.rotate()
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
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			en_bullet = Bullet(self.rect.centerx, self.rect.bottom + 10, enemy_laser_img, 10)
			all_sprites.add(en_bullet)
			en_bullets.add(en_bullet)
			# enemy_shoot.play()

####### BULLET CLASS #############
class Bullet(pygame.sprite.Sprite):
  	#tell bullet to spawn at particular loc according to player
	def __init__(self, x, y, img, speedy):
		pygame.sprite.Sprite.__init__(self)
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
class Power(pygame.sprite.Sprite):
	def __init__(self, center):
		pygame.sprite.Sprite.__init__(self)
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
class Explosion(pygame.sprite.Sprite):
	def __init__(self, center, size):
		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.image = explosion_anim[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		#check the last time it updated
		self.last_update = pygame.time.get_ticks()
		#set frame rate / how long we wait between each frame
		self.frame_rate = 20

	def update(self):
		#change image after enough time elapsed
		now = pygame.time.get_ticks()
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

############ SHOW GAME OVER SCREEN ############
def show_gameover_screen():
	screen.blit(background, background_rect)
	draw_text(screen, "ALPHA DESCENT", 64, WIDTH/2, HEIGHT /4)
	draw_text(screen, "Arrow keys move, Spacebar to fire", 22, WIDTH / 2, HEIGHT / 2)
	draw_text(screen, "Press any key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False 

############ LOADING GAME GRAPHICS ############
background = pygame.image.load(path.join(img_dir, "spacefield.png")).convert()
background_rect = background.get_rect()	
player_img = pygame.image.load(path.join(img_dir, "playership_blue.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
laser_img = pygame.image.load(path.join(img_dir, "laser_green.png")).convert()
p_laser_img = pygame.image.load(path.join(img_dir, "laserBlue02.png")).convert()
enemy_laser_img = pygame.image.load(path.join(enemy_dir, "laserRed02.png")).convert()
#powerups
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, "shield_gold.png")).convert()
powerup_images['laser'] = pygame.image.load(path.join(img_dir, "bolt_gold.png")).convert()
enemy_images = []
enemy_list = [	'enemyBlack1.png', 'enemyBlack4.png', 'enemyBlue1.png', 'enemyBlue4.png', 
				'enemyGreen1.png', 'enemyGreen4.png', 'enemyRed1.png', 'enemyRed4.png',  
			]
for img in enemy_list:
  	enemy_images.append(pygame.image.load(path.join(enemy_dir, img)).convert())

#EXPLOSIONS: create dic with lists, load, scale igs
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []

for i in range(31):
	#brackets are placeholders
	filename = 'expl_06_0{}.png'.format(i)
	img = pygame.image.load(path.join(expl_dir, filename)).convert()
	img.set_colorkey(BLACK)
	img_lg = pygame.transform.scale(img, (75, 75))
	explosion_anim['lg'].append(img_lg)
	img_sm = pygame.transform.scale(img, (32, 32))
	explosion_anim['sm'].append(img_sm)

#exploding player ship for lives 
for i in range(23):
	#brackets are placeholders
	filename_2 = 'expl_01_0{}.png'.format(i)
	img_2 = pygame.image.load(path.join(expl_1dir, filename_2)).convert()
	img_2.set_colorkey(BLACK)
	explosion_anim['player'].append(img_2)

############ LOADING GAME SOUNDS ############
pygame.mixer.music.load(path.join(snd_dir, 'jlbrock.mp3'))
shoot_snd = pygame.mixer.Sound(path.join(snd_dir, "Laser_Shoot2.wav"))
enemy_shoot = pygame.mixer.Sound(path.join(snd_dir, "Laser_ShootE.wav"))
player_death_snd = pygame.mixer.Sound(path.join(snd_dir, 'Expl8.wav'))
powerup_bolt_snd = pygame.mixer.Sound(path.join(snd_dir, 'Powerup.wav'))
powerup_shield_snd = pygame.mixer.Sound(path.join(snd_dir, 'Powerup4.wav'))
expl_snds = []
for snd in ['Expl3.wav','Expl4.wav', 'Expl6.wav']:
  	expl_snds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
#control music sound
pygame.mixer.music.set_volume(0.4)

##PLAY BG Music / loops =-1 plays music over again##
pygame.mixer.music.play(loops=-1)

############## GAME LOOP ######################
running = True
game_over = True
while running:
	if game_over:
		show_gameover_screen()
		game_over = False 

########### CREATE SPRITES ###################  		  
		all_sprites = pygame.sprite.Group()
		mobs = pygame.sprite.Group()
		bullets = pygame.sprite.Group() 
		en_bullets = pygame.sprite.Group()
		powerups = pygame.sprite.Group()
		player = Player()
		all_sprites.add(player) 
		for i in range(5):
			newmob()
		##SCORE##
		score = 0

	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			 
	#UPDATE 
	all_sprites.update()

	##### PLAYER HIT MOB / true for both so both get deleted ###########
	hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
	#respawn the mob
	for hit in hits:
		score += 50 - hit.radius
		#play random sound in list 
		random.choice(expl_snds).play()
		expl = Explosion(hit.rect.center, 'lg')
		all_sprites.add(expl) 
		if random.random() > 0.9:
			power = Power(hit.rect.center)
			all_sprites.add(power)
			powerups.add(power)
		newmob()

	#player's bullets hit mob bullets 
	hits = pygame.sprite.groupcollide(en_bullets, bullets, True, True)
	#respawn the mob
	for hit in hits:
		score += 70 
		#play random sound in list 
		random.choice(expl_snds).play()
		expl = Explosion(hit.rect.center, 'sm')
		all_sprites.add(expl) 
	
	#####POWERUPS HIT PLAYER ##################
	hits = pygame.sprite.spritecollide(player, powerups, True)
	for hit in hits:
		if hit.type == 'shield':
			powerup_shield_snd.play()
			player.shield += random.randrange(10, 30)
			if player.shield >= 100:
				player.shield = 100

		if hit.type == 'laser':
			powerup_bolt_snd.play() 
			player.powerup()
  			
	##### MOB HIT PLAYER / circle specifies type of collision ##########
	hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
	for hit in hits:
		random.choice(expl_snds).play()
		player.shield -= hit.radius * 2
		expl = Explosion(hit.rect.center, 'sm')
		all_sprites.add(expl) 
		newmob()
		if player.shield <= 0:
			player_death_snd.play() 
			death_expl = Explosion(player.rect.center, 'player')
			all_sprites.add(death_expl)
			player.hide()
			player.lives -= 1
			player.shield = 100

	hits = pygame.sprite.spritecollide(player, en_bullets, True, pygame.sprite.collide_circle)
	for hit in hits:
		random.choice(expl_snds).play()
		player.shield -= 2
		expl = Explosion(hit.rect.center, 'sm')
		all_sprites.add(expl) 
		if player.shield <= 0:
			player_death_snd.play() 
			death_expl = Explosion(player.rect.center, 'player')
			all_sprites.add(death_expl)
			player.hide()
			player.lives -= 1
			player.shield = 100
	
	# if player died and explosion finished playing
	if player.lives == 0 and not death_expl.alive():
		#game over 
		game_over = True 

	#RENDER
	screen.fill(BLACK)
	screen.blit(background, background_rect)
	all_sprites.draw(screen)
	draw_text(screen, str(score), 18, WIDTH / 2, 10)
	draw_shield_bar(screen, 5, 5, player.shield)
	draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
	pygame.display.flip()


pygame.quit()