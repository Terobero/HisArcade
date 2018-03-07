#!/usr/bin/env python
#Hisar FRC
#copyright: Terobero
#Hisar School
import sys
import time
import pygame, serial
import RPi.GPIO as GPIO
from pygame.locals import *
import random
pygame.init()

sys.path.insert(0,"/home/pi/Desktop/HisArcade/pins")
import gamePins

gamePins.gameSetup()

scoreboard = gamePins.getScores("FRC")

screen=pygame.display.set_mode((1024,718),pygame.FULLSCREEN)

pygame.display.set_caption("Hisar FRC!")

white = [255,255,255]

#Creating 4 boxes and Background.
back = pygame.Surface((1024,718))
pygame.font.init()
fontSmall = pygame.font.Font("Fonts/ARCADECLASSIC.TTF",30)
background = back.convert()
background.fill((0,0,0))

red, yellow, green, blue=(235,53,47),(235,230,45),(0,185,10),(73,170,235)
directUp = fontSmall.render("up", True,white)
directDown = fontSmall.render("down", True,white)
directLeft = fontSmall.render("left", True,white)
directRight = fontSmall.render("right", True,white)
directExit = fontSmall.render("exit", True,white)

directPress = fontSmall.render("press", True, white)



FPS = 10

#clock and font objects
clock = pygame.time.Clock()
all_fonts = pygame.font.get_fonts()
font = pygame.font.Font("Fonts/ARCADECLASSIC.TTF",40)

#fonts and texts
font1 = pygame.font.Font("Fonts/ARCADECLASSIC.TTF",60)
font2 = pygame.font.Font("Fonts/ARCADECLASSIC.TTF",30)
font3 = pygame.font.Font("Fonts/ka1.ttf", 60)
text1 = font3.render("CITADEL", True,white)
text3 = font2.render("by	Kaan Bozkurt", True,white)
text4 = font.render("GAME OVER", True,white)
text5 = font.render("YOU WIN", True,white)

def bg(): #draws the background
	screen.blit(background,(0,0))
	text2 = font.render("Score  " + str(Score), True,white)
	screen.blit(background,(0,0))
	pygame.draw.rect(screen,white,Rect((150,150),(640,480)),2)
	screen.blit(text1,(300,30))
	screen.blit(text2,(825,150))
	screen.blit(text3,(500,680))


	screen.blit(directDown,(900,340))
	screen.blit(directUp,(900,420))
	screen.blit(directRight,(900,500))
	screen.blit(directLeft,(900,580))

	pygame.draw.polygon(screen,(225,240,229),[[825,335],[865,335],[845,370]],0)
	pygame.draw.polygon(screen,(225,240,229),[[825,450],[865,450],[845,415]],0)
	pygame.draw.polygon(screen,(225,240,229),[[825,495],[825,540],[865,518]],0)
	pygame.draw.polygon(screen,(225,240,229),[[865,575],[865,620],[825,598]],0)
	pygame.draw.circle(screen, (red), (845,680),20,0)
	screen.blit(directExit,(890,660))



def gameOver():
	text2 = font.render("Score  " + str(Score), True, white)
	screen.blit(background,(0,0))
	screen.blit(text1,(280.,100.))
	pygame.draw.circle(screen, (red), (470,450),20,0) 
	screen.blit(directExit,(520,445))
	screen.blit(text2,(450.,350.))
	screen.blit(text3,(440.,670.))



Score = 0
startTime = time.time()

level = 1 # 1 = maze, 2 = take & up/down, 3 = throw, 4 = climb

grid = [[0, 0, 0, 0, 0, 0, 3, 0, 0, 0], #1 = robot, 2 = switch/scale, 3 = cube
		[0, 0, 2, 0, 2, 2, 0, 2, 0, 0],
		[0, 3, 2, 0, 2, 2, 0, 2, 0, 0],
		[0, 0, 2, 0, 2, 2, 0, 2, 0, 0],
		[0, 0, 2, 0, 2, 2, 0, 2, 0, 3],
		[1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

x = 0 # 0-9
y = 5 # 0-5

while True:
	if not GPIO.input(gamePins.red):
		execfile('launchGPIO.py')
	
	bg()

	if level == 1:
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_q:
					exit()
				if event.key == K_w:
					if y - 1 >= 0:
						if grid[y-1][x] is not 2:
							grid[y][x] = 0
							grid[y-1][x] = 1
				elif event.key == K_s:
					if y + 1 <= 5:
						if grid[y+1][x] is not 2:
							grid[y][x] = 0
							grid[y+1][x] = 1
				elif event.key == K_a:
					if x - 1 >= 0:
						if grid[y][x-1] is not 2:
							grid[y][x] = 0
							grid[y][x-1] = 1
				elif event.key == K_d:
					if x + 1 <= 9:
						if grid[y][x+1] is not 2:
							grid[y][x] = 0
							grid[y][x+1] = 1


		if grid[y][x] == 3:
			level = 2

		pygame.draw.rect(screen,(255,0,0),Rect((150+49*x,150+55*y),(49,55))) #bizim robot

		for x in range(0,10):
			for y in range(0,6):
				if grid[y][x] == 2:
					pygame.draw.rect(screen, (0,255,0),Rect((150+49*x,150+55*y),(49,55)))

				if grid[y][x] == 3:
					pygame.draw.rect(screen, (255,255,0),Rect((150+49*x,150+55*y),(49,55)))



	#490 x 330 (ikisi icin de + 150)
	#cube --> 49 x 55

	if level == 2:
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_q:
					exit()
				if event.key == K_w:
					if y - 1 >= 0:
						if grid[y-1][x] is not 2:
							grid[y][x] = 0
							grid[y-1][x] = 1
				elif event.key == K_s:
					if y + 1 <= 5:
						if grid[y+1][x] is not 2:
							grid[y][x] = 0
							grid[y+1][x] = 1


		if not GPIO.input(gamePins.green):

	'''
	if gameEnd:
		gameOver()
		if not GPIO.input(gamePins.red):
			clearGrid()
			GameEnd=True
			time.sleep(1)
			execfile("launchGPIO.py")
	'''
	pygame.display.update()
	clock.tick(FPS)
