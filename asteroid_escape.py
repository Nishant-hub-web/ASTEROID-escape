import pygame
import time
import sys
import random
import math
pygame.init()


HEIGHT,WIDTH=600,800
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
ASTEROID=pygame.image.load('assets/asteroid.png')
PLAYER=pygame.image.load('assets/spaceship.png')
FPS=62
pygame.display.set_caption('ASTEROID escape')
pygame.display.set_icon(ASTEROID)
fonty=pygame.font.SysFont('comicsans',64)
BG=pygame.transform.scale(pygame.image.load('assets/bg.png'),(WIDTH,HEIGHT)).convert()


class Enemy:
	def __init__(self,img,x,y):
		self.x,self.y=x,y
		self.img=img

	def draw(self,WIN):
		WIN.blit(self.img,(self.x,self.y))

	def collision(self,obj,enemies):
		distance=math.sqrt(math.pow(obj.x-self.x,2)+math.pow(obj.y-self.y,2))
		if distance <= 32:
			enemies.remove(self)
			obj.lives-=1


class Player:
	def __init__(self,img,HEIGHT):
		self.img=img
		self.y=HEIGHT//2-self.img.get_height()//2
		self.x=50
		self.lives=5
		self.score=0
		self.lost=False

	def draw(self,WIN):
		WIN.blit(self.img,(self.x,self.y))



def main():
	clock=pygame.time.Clock()
	player=Player(PLAYER,HEIGHT)
	k=11
	level=0
	enemies=[]
	lost_count=0
	run=True


	def redrawwindow():
		WIN.blit(BG,(0,0)) 
		player.draw(WIN)
		lost_label=fonty.render(f'You lost , Your Score:{player.score}',1,(255,0,0))
		score_label=fonty.render(f'Score:{player.score}',1,(255,255,255))
		level_label=fonty.render(f'Lives:{player.lives}   Level:{level}',1,(255,255,255))
		WIN.blit(score_label,(10,20))
		WIN.blit(level_label,(WIDTH-10-level_label.get_width(),20))
		if player.lost:
			WIN.blit(lost_label,(WIDTH//2-lost_label.get_width()//2,HEIGHT//2-lost_label.get_height()//2))
		pygame.display.update()

	while run:
		clock.tick(FPS)		
		redrawwindow()
		if player.lives == 0:
			lost_count+=1
			player.lost=True

		if player.lost:
			if lost_count > FPS*4:
				run=False
			else:
				continue

		if len(enemies)==0:
			level+=1
			for i in range(k):
				enemies.append(Enemy(ASTEROID,random.randrange(1600,2800),random.randrange(0,HEIGHT)))
			k+=1


		keys=pygame.key.get_pressed()
		if keys[pygame.K_RIGHT] and (player.x+64+5 <= WIDTH):
			player.x+=5
		if keys[pygame.K_LEFT] and (player.x-5 >= 0):
			player.x-=5
		if keys[pygame.K_UP] and (player.y-5 >= 0):
			player.y-=5
		if keys[pygame.K_DOWN] and (player.y+64+5 <= HEIGHT):
			player.y+=5
		for enemy in enemies:
			enemy.draw(WIN)
			enemy.collision(player,enemies)
			if (enemy.x - 5) < 0:
				enemies.remove(enemy)
			else:
				enemy.x-=5
		player.score+=1#/8931844280
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		pygame.display.update()
		


def mainmenu():
	star_label=fonty.render('Press any key to begin',1,(255,255,255))
	while True:
		WIN.blit(BG,(0,0)) 		
		WIN.blit(star_label,(WIDTH//2-star_label.get_width()//2,HEIGHT//2-star_label.get_height()//2))
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
				main()
			elif event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		pygame.display.update()


mainmenu()