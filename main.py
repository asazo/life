# -*- coding: utf-8 -*-
# @Author: alejandro
# @Date:   2016-12-04 15:52:15
# @Last Modified by:   Alejandro Sazo
# @Last Modified time: 2016-12-05 16:53:35

import numpy as np
import pygame as pg
from pygame.locals import *
import sys

class WorldSimulator:
    """
        World cell simulator
    """

    def __init__(self, screen_size, cell_size):
        """ """
        self.screen_size = screen_size
        self.cell_size = cell_size
        # store current state
        self.world = np.zeros((screen_size / cell_size))
        # Indices
        self.xx = np.arange(self.world.shape[0])
        self.yy = np.arange(self.world.shape[1])


    def activate(self, pos):
        """ Activate or deactivate a cell in a position """
        pos = np.array(pos) / self.cell_size
        self.world[pos[0], pos[1]] = not self.world[pos[0], pos[1]]


    def draw(self, screen):
        """ """
        for i in self.xx:
            for j in self.yy:
                rect = [i*self.cell_size, j*self.cell_size, self.cell_size, self.cell_size]
                color = (255, (1-self.world[i][j])*255, (1-self.world[i][j])*255)
                pg.draw.rect(screen, color, rect)


    def sum_over_neighbors(self, i, j):
        """ Sum over neighbors states. """
        il = (i-1) % (self.screen_size[0] / self.cell_size)
        ir = (i+1) % (self.screen_size[0] / self.cell_size)
        jl = (j-1) % (self.screen_size[1] / self.cell_size)
        jr = (j+1) % (self.screen_size[1] / self.cell_size)
        neighbors = self.world[np.ix_([il,i,ir],[jl,j,jr])]
        return np.sum(neighbors, dtype=np.int32)


    def update(self):
        # store temp state
        tmp = np.copy(self.world)
        for i in self.xx:
            for j in self.yy:
                alive = self.sum_over_neighbors(i, j)
                if self.world[i][j] == 0 and alive == 3:
                    tmp[i][j] = 1
                elif self.world[i][j] == 1 and (alive == 3 or alive == 2):
                    tmp[i][j] = 1
                else:
                    tmp[i][j] = 0
        self.world = tmp
        del tmp


pg.init()
np.random.seed(35)
screen_size = np.array([800, 600])
cell_size = 50
screen = pg.display.set_mode(screen_size)
pg.display.set_caption('Life')

w = WorldSimulator(screen_size, cell_size)

running = False
print "Stopped. Press 'e' to start."

while True:
    ev = pg.event.get()
    for event in ev:
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONUP:
            w.activate(pg.mouse.get_pos())

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                running = not running
                if running:
                    print "Running."
                else:
                    print "Stopped."

    if running:
        w.update()
    w.draw(screen)
    pg.display.update()
