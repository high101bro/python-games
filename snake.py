#! /bin/env python3
"""
Game: Snake

Daniel Komnick (high101bro)
8 April 2022
Learning how to write games with my son Nathan

==================
|     Snake      |
|                |    
|    ====o .     |
|                |
|                |
==================
"""

import math, random, pygame
import tkinter as tk
from tkinter import messagebox

class cube(object) :
    rows = 20
    w = 500

    def __init__(self, start, dirnx = 1, dirny = 0, color = (255,0,0)) :
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny) :
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes = False) :
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        # note: the +1 and -2 is to keep the drawn cubes within the white grid without drawing over them
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))        

        if eyes :
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis+dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)


class snake(object) :
    body = []
    turns = {}

    def __init__(self, color, pos) :
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)

        # Keeps track of the direction the snake is moving
        self.dirnx = 0
        self.dirny = 1

    def move(self) :
        for event in pygame.event.get() :

            if event.type == pygame.QUIT:
                pygame.quit()
                
            keys = pygame.key.get_pressed()

            for key in keys :
                if keys[pygame.K_LEFT] :
                    # Sets the direction, note you can only move x or y at a time, no diagonal movements
                    self.dirnx = -1
                    self.dirny = 0
                    
                    # Adds a key which is the current position of the head of the snake
                    # it'll be set equal to what direction the snake turns
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
               
                elif keys[pygame.K_RIGHT] :
                    # Sets the direction, note you can only move x or y at a time, no diagonal movements
                    self.dirnx = 1
                    self.dirny = 0
                   
                    # Adds a key which is the current position of the head of the snake
                    # it'll be set equal to what direction the snake turns
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                
                elif keys[pygame.K_UP] :
                    # Sets the direction, note you can only move x or y at a time, no diagonal movements
                    self.dirnx = 0
                    self.dirny = -1
                    
                    # Adds a key which is the current position of the head of the snake
                    # it'll be set equal to what direction the snake turns
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                
                elif keys[pygame.K_DOWN] :
                    # Sets the direction, note you can only move x or y at a time, no diagonal movements
                    self.dirnx = 0
                    self.dirny = 1
                   
                    # Adds a key which is the current position of the head of the snake
                    # it'll be set equal to what direction the snake turns
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body) :
            # gets the cube positions of the snake
            p = c.pos[:]

            # turns the snake at the proper cude point
            if p in self.turns :
                turn = self.turns[p]
                c.move(turn[0],turn[1])

                # Removes the last cube of the snake when moving... otherwise it'd keep growing
                if i == len(self.body)-1 :
                    self.turns.pop(p)
            else :
                # moves the cubes left
                if   c.dirnx == -1 and c.pos[0] <= 0 :
                    c.pos = (c.rows-1, c.pos[1])
                # moves the cubes right
                elif c.dirnx ==  1 and c.pos[0] >= c.rows-1 :
                    c.pos = (0, c.pos[1])
                # moves cubes up
                elif c.dirny ==  1 and c.pos[1] >= c.rows-1 :
                    c.pos = (c.pos[0], 0)
                # moves the cubes down
                elif c.dirny == -1 and c.pos[1] <= 0 :
                    c.pos = (c.pos[0], c.rows-1)
                # else moves the cubes in the current directions
                else :
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos) :
        pass

    def addCube(self) :
        pass

    def draw(self, surface) :
        for i, c in enumerate(self.body) :
            # adds the eyes if the cube is the head
            if i == 0 :
                c.draw(surface, True)
            else :
                c.draw(surface)

def drawGrid(w, rows, surface) :
    sizeBtwn = w // rows
    x = 0
    y = 0
    for l in range(rows) :
        x += sizeBtwn
        y += sizeBtwn
        pygame.draw.line(
            surface, 
            (255,255,255), # rgb color = black
            (x,0),(x,w)    # start and end position of x
        )
        pygame.draw.line(
            surface, 
            (255,255,255), # rgb color = black
            (0,y),(w,y)    # start and end position of y
        )

def redrawWindow(surface) :
    global rows, width, s
    surface.fill((0,0,0)) # rgb color = black
    s.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, items) :
    pass

def message_box(subject, content) :
    pass

def main() :
    global width, rows, s
    width  = 500
    height = width # keeps the window squared
    rows   = 20
    window = pygame.display.set_mode((width,height))
    s = snake(
        (255,0,0), # rgb color = red
        (10, 10)   # start position
    )

    flag = True
    clock = pygame.time.Clock()
    while flag :
        pygame.time.delay(50) # 50 milliseconds
        clock.tick(10)
        s.move()
        redrawWindow(window)
    pass

main()





