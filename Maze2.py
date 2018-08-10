# -*- coding: utf-8 -*-
import os
import sys
sys.setrecursionlimit(100000)

import random
import cv2
import numpy as np
from matplotlib import pyplot as plt


class Maze2:
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    ADJ = [UP, DOWN, LEFT, RIGHT]

    def __init__(self, size):
        self.height = size[0]
        self.width = size[1]
        self.map = np.zeros(size, np.uint8)
        self.set = set()
        self.ct = 1

        self.init_map()

    def init_map(self):
        self.map[1::2, 1::2] = 255

    def in_side(self, x, y):
        if x <= 0 or x >= self.height - 1 or y <= 0 or y >= self.width - 1:
            return True
        return False

    def in_set(self, x, y):
        return (x, y) in self.set

    def add_set(self, x, y):
        self.set.add((x, y))
        plt.imshow(cv2.cvtColor(self.map, cv2.COLOR_GRAY2RGB))
        plt.savefig(os.path.join('build', '{:04}.jpg'.format(self.ct)))
        self.ct += 1

    def through_it(self, x, y):
        self.map[x][y] = 255

    def get_adj_random(self):
        adj = self.ADJ.copy()
        random.shuffle(adj)
        return adj

    def get_edge(self, x, y, random=False):
        edge_list = []
        vertex_list = []

        adj = self.ADJ.copy()
        if random:
            adj = self.get_adj_random()

        for i in adj:
            if not self.in_side(x + i[0], y + i[1]):
                edge_list.append((x + i[0], y + i[1]))
                vertex_list.append((x + i[0]*2, y + i[1]*2))
        return edge_list, vertex_list

    def build_map(self, x=1, y=1):
        self.add_set(x, y)

        edge_list, vertex_list = self.get_edge(x, y, True)
        for e, v in zip(edge_list, vertex_list):
            if not self.in_set(v[0], v[1]):
                self.through_it(e[0], e[1])
                self.build_map(v[0], v[1])

    def show(self):
        plt.imshow(cv2.cvtColor(self.map, cv2.COLOR_GRAY2RGB))
        plt.show()


m = Maze2((23, 31))
m.build_map()
# m.show()
