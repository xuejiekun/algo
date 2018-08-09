# -*- coding: utf-8 -*-
import sys
sys.setrecursionlimit(1000000)

import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import random


class Maze:
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    UP_LEFT = UP[0] + LEFT[0], UP[1] + LEFT[1]
    UP_RIGHT = UP[0] + RIGHT[0], UP[1] + RIGHT[1]
    DOWN_LEFT = DOWN[0] + LEFT[0], DOWN[1] + LEFT[1]
    DOWN_RIGHT = DOWN[0] + RIGHT[0], DOWN[1] + RIGHT[1]

    ADJ = [UP, DOWN, LEFT, RIGHT]
    ADJ_AROUND = ADJ + [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]

    def __init__(self, size, start=(1,0), end=None):
        self.height = size[0]
        self.width = size[1]
        self.map = np.zeros(size, np.uint8)
        self.marker = np.zeros(size, np.bool)
        self.marker[:, :] = False
        self.ct = 1

        self.start = start
        if end:
            self.end = end
        else:
            self.end = self.height-2, self.width-1

    def marker_it(self, x, y):
        self.marker[x][y] = True
        self.map[x][y] = 255
        # im = cv2.resize(self.map, None, fx=4, fy=4, )
        # cv2.imwrite(os.path.join('build', '{:003}.jpg'.format(self.ct)), im)
        # plt.imshow(cv2.cvtColor(self.map, cv2.COLOR_GRAY2RGB))
        # plt.savefig(os.path.join('build', '{:003}.jpg'.format(self.ct)))
        self.ct += 1

    def is_marker(self, x, y):
        return self.marker[x][y]

    def is_side(self, x ,y):
        if x <= 0 or x >= self.height-1 or y <= 0 or y >= self.width-1:
            return True
        return False

    def is_through(self, x ,y, px, py):
        adj_list = self.get_adj(x, y)
        try:
            adj_list.remove((px, py))
        except:
            pass

        for v in adj_list:
            if self.is_marker(v[0], v[1]):
                return True
        return False

    def get_adj_around(self, x, y):
        adj_list = []
        for i in self.ADJ_AROUND:
            if self.is_side(x + i[0], y + i[1]):
                continue
            adj_list.append((x + i[0], y + i[1]))
        return adj_list

    def get_adj(self, x, y):
        adj_list = []
        for i in self.ADJ:
            if self.is_side(x+i[0], y+i[1]):
                continue
            adj_list.append((x+i[0], y+i[1]))
        return adj_list

    def get_adj_random(self, x, y):
        adj_list = self.get_adj(x, y)
        random.shuffle(adj_list)
        return adj_list

    def dfs(self, x, y):
        self.marker_it(x, y)
        for v in self.get_adj_random(x, y):
            if not self.is_marker(v[0], v[1]) and not self.is_through(v[0], v[1], x, y):
                self.dfs(v[0], v[1])

    def build_maze(self):
        self.dfs(self.start[0], self.start[1])
        self.marker_it(self.end[0], self.end[1])

    def show(self):
        plt.imshow(cv2.cvtColor(self.map, cv2.COLOR_GRAY2RGB))
        plt.show()

    def __repr__(self):
        return 'map:\n{}\nmarker:\n{}'.format(self.map, self.marker)


m = Maze((40,60))
m.build_maze()
m.show()
