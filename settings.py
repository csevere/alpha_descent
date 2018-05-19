import pygame as pg
from os import path 

pg.init()
pg.mixer.init()

#GAME OPTIONS AND SETTINGS
TITLE = "ALPHA DESCENT"
WIDTH = 480
HEIGHT = 800
FPS = 300
POWERUP_TIME = 5000

screen = pg.display.set_mode((WIDTH, HEIGHT))
font_name = pg.font.match_font('arial')

######## COLORS ###############
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

########## IMAGES ###############
img_dir = path.join(path.dirname(__file__), 'img')
enemy_dir = path.join(path.dirname(__file__), 'img/enemy')
expl_dir = path.join(path.dirname(__file__), 'img/expl')
expl_1dir = path.join(path.dirname(__file__), 'img/expl_1')
meteors_dir = path.join(path.dirname(__file__), 'img/meteors')
snd_dir = path.join(path.dirname(__file__), 'snd')

############ LOADING GAME GRAPHICS ############
background = pg.image.load(path.join(img_dir, "spacefield.png")).convert()
background_rect = background.get_rect()	
start_screen = pg.image.load(path.join(img_dir, "Background-4.jpg")).convert()
start_screen_rect = start_screen.get_rect()
player_img = pg.image.load(path.join(img_dir, "playership_blue.png")).convert()
player_mini_img = pg.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
laser_img = pg.image.load(path.join(img_dir, "laser_green.png")).convert()
p_laser_img = pg.image.load(path.join(img_dir, "laserBlue02.png")).convert()
guide = pg.image.load(path.join(img_dir, "guide.png")).convert()
###### POWERUPS #################
powerup_images = {}
powerup_images['shield'] = pg.image.load(path.join(img_dir, "shield_gold.png")).convert()
powerup_images['laser'] = pg.image.load(path.join(img_dir, "bolt_gold.png")).convert()
##### ENEMIES #################
boss_img = pg.image.load(path.join(enemy_dir, "boss_ship.png")).convert()
boss_laser = pg.image.load(path.join(enemy_dir, "laserRed05.png")).convert()
enemy_laser_img = pg.image.load(path.join(enemy_dir, "laserRed01.png")).convert()
laser_ball = pg.image.load(path.join(enemy_dir, "laser_ball.png")).convert() 
enemy_images = []
enemy_list = [	'enemyBlack1.png', 'enemyBlack4.png', 'enemyBlue1.png', 'enemyBlue4.png', 
				'enemyGreen1.png', 'enemyGreen4.png', 'enemyRed1.png', 'enemyRed4.png',  
			]
for img in enemy_list:
  	enemy_images.append(pg.image.load(path.join(enemy_dir, img)).convert())

enemy2_img = pg.image.load(path.join(enemy_dir, "ufoRed.png")).convert()
boss_img = pg.image.load(path.join(enemy_dir, "boss_ship.png")).convert()

###### METEORS
meteor_images = []
meteor_list = ['meteor_big1.png', 'meteor_med1.png']
for img in meteor_list:
  	meteor_images.append(pg.image.load(path.join(meteors_dir, img)).convert())

#EXPLOSIONS: create dic with lists, load, scale igs
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []

for i in range(31):
	#brackets are placeholders
	filename = 'expl_06_0{}.png'.format(i)
	img = pg.image.load(path.join(expl_dir, filename)).convert()
	img.set_colorkey(BLACK)
	img_lg = pg.transform.scale(img, (75, 75))
	explosion_anim['lg'].append(img_lg)
	img_sm = pg.transform.scale(img, (32, 32))
	explosion_anim['sm'].append(img_sm)

#exploding player ship for lives 
for i in range(23):
	#brackets are placeholders
	filename_2 = 'expl_01_0{}.png'.format(i)
	img_2 = pg.image.load(path.join(expl_1dir, filename_2)).convert()
	img_2.set_colorkey(BLACK)
	explosion_anim['player'].append(img_2)

########### LOADING GAME SOUNDS ############
pg.mixer.music.load(path.join(snd_dir, 'jlbrock.mp3'))
shoot_snd = pg.mixer.Sound(path.join(snd_dir, "Laser_Shoot2.wav"))
enemy_shoot = pg.mixer.Sound(path.join(snd_dir, "Laser_ShootE.wav"))
player_death_snd = pg.mixer.Sound(path.join(snd_dir, 'Expl8.wav'))
powerup_bolt_snd = pg.mixer.Sound(path.join(snd_dir, 'Powerup.wav'))
powerup_shield_snd = pg.mixer.Sound(path.join(snd_dir, 'Powerup4.wav'))
expl_snds = []
for snd in ['Expl3.wav','Expl4.wav', 'Expl6.wav']:
  	expl_snds.append(pg.mixer.Sound(path.join(snd_dir, snd)))
#control music sound
pg.mixer.music.set_volume(0.4)

##PLAY BG Music / loops =-1 plays music over again##
# pg.mixer.music.play(loops=-1)



