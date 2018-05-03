# pygame template - skeleton for a new pygame project
import pygame
import random 
import os 

#create the window

WIDTH = 800
HEIGHT = 600
#frames per second / how fast the game runs
FPS = 30

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#set up assets 
game_folder = os.path.dirname(__file__)
#folder to join two folders together
img_folder = os.path.join(game_folder, "img")

class Player(pygame.sprite.Sprite):
    #sprite for the player 
    def __init__(self):
      #run the init of the sprit
      pygame.sprite.Sprite.__init__(self)
      # self.image = pygame.Surface((50, 50))
      #convert changes img into something can manipulate easily 
      self.image = pygame.image.load(os.path.join(img_folder,"p2_jump.png")).convert()
      #sets a color transparent 
      self.image.set_colorkey(BLACK)
      #the rectangle that encloses the sprite
      # self.image.fill(GREEN)
      #all sprites have rectangles around them 
      self.rect = self.image.get_rect()
      self.rect.center = (WIDTH / 2, HEIGHT / 2)
      self.y_speed = 10

    #add an update on our player sprite
    def update(self):
      self.rect.x += 5
      self.rect.y += self.y_speed 
      if self.rect.bottom > HEIGHT - 100:
        self.y_speed = -5
      if self.rect.top < 200:
        self.y_speed = 10 
      #prevent it from sliding off the screen forever 
      if self.rect.left > WIDTH:
        self.rect.right = 0

#initializes pygame and create window 
pygame.init()
#handles playing sound effects and music
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#set the caption on top of the window for game
pygame.display.set_caption("Game Template")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

#game loop
running = True
while running:
	#keep loop running at the right speed
	clock.tick(FPS)
	#Process input (events)
	for event in pygame.event.get():
		#check for closing the window 
		if event.type == pygame.QUIT:
  			running = False 
	#update
	all_sprites.update()

	#draw/render
	screen.fill(BLUE)
	all_sprites.draw(screen)
	#after drawing everything, flip the display
	pygame.display.flip()

pygame.quit()