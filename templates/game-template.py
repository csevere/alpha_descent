# pygame template - skeleton for a new pygame project
import pygame
import random 

#create the window

WIDTH = 368
HEIGHT = 480
#frames per second / how fast the game runs
FPS = 30

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#initializes pygame and create window 
pygame.init()
#handles playing sound effects and music
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#set the caption on top of the window for game
pygame.display.set_caption("Game Template")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

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
	screen.fill(BLACK)
	all_sprites.draw(screen)
	#after drawing everything, flip the display
	pygame.display.flip()

pygame.quit()