#ALPHA DESCENT GAME
#Music: Reusenoise  (DNB Mix) by spinningmerkaba (c) copyright 2017 Licensed under a Creative Commons Attribution (3.0) license. 
#Art from Kenney.nl

import pygame
import random 
from os import path 

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60

######## COLORS ###############
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ALPHA DESCENT")
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

	def update(self):
		#default speed should be 0
		self.speedx = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx = -8
		if keystate[pygame.K_RIGHT]:
			self.speedx = 8 
		self.rect.x += self.speedx
		if self.rect.right > WIDTH:
  			self.rect.right = WIDTH
		if self.rect.left < 0:
  			self.rect.left = 0 

	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)
		shoot_snd.play()


####### MOB CLASS #############
class Mob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_orig = random.choice(meteor_images)
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
		self.rotate()
		#makes it move downward 
		self.rect.x += self.speedx 
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 8)


####### BULLET CLASS #############
class Bullet(pygame.sprite.Sprite):
  	#tell bullet to spawn at particular loc according to player
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = laser_img
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		#kill if it moves off the top of screen
		if self.rect.bottom < 0:
			self.kill()

############ LOADING GAME GRAPHICS ############
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()	
player_img = pygame.image.load(path.join(img_dir, "playership_blue.png")).convert()
laser_img = pygame.image.load(path.join(img_dir, "laser_green.png")).convert()
meteor_images = []
meteor_list = [	'meteor_big1.png', 'meteor_big2.png', 'meteor_big3.png', 'meteor_big4.png', 
				'meteor_med1.png', 'meteor_med3.png', 'meteor_small1.png', 'meteor_small2.png', 'meteor_tiny1.png', 
				'meteor_tiny2.png']
for img in meteor_list:
  	meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

############ LOADING GAME SOUNDS ############
shoot_snd = pygame.mixer.Sound(path.join(snd_dir, "Laser_Shoot2.wav"))
expl_snds = []
for snd in ['Expl3.wav','Expl4.wav', 'Expl6.wav']:
  	expl_snds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'jlbrock.mp3'))
#control music sound
pygame.mixer.music.set_volume(0.4)


########### CREATE SPRITES ###################  		  
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
	m = Mob()
	all_sprites.add(m)
	mobs.add(m)

##SCORE##
score = 0

##PLAY BG Music / loops =-1 plays music over again##
pygame.mixer.music.play(loops=-1)

############## GAME LOOP ######################


running = True
while running:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()
			 

	#UPDATE 
	all_sprites.update()

	#check for bullet/mob collision / true for both so both get deleted
	hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
	#respawn the mob
	for hit in hits:
		score += 50 - hit.radius
		#play random sound in list 
		random.choice(expl_snds).play() 
		m = Mob()
		all_sprites.add(m)
		mobs.add(m)


	#check for mob/player collision/ circle specifies type of collision
	hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
	if hits:
  		#game over 
  		running = False 


	#RENDER
	screen.fill(BLACK)
	screen.blit(background, background_rect)
	all_sprites.draw(screen)
	draw_text(screen, str(score), 18, WIDTH / 2, 10)
	pygame.display.flip()

pygame.quit()