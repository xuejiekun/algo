# -*- coding: utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt


class Maze:
    START = (1, 0)
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    ADJ = [UP, DOWN, LEFT, RIGHT]

    def __init__(self, size):
        self.map = np.zeros(size, np.uint8)
        self.marker = np.zeros(size, np.bool)
        self.set_marker()
        self.set_start()

    def set_marker(self):
        self.marker[:,:] = 0

    def set_start(self):
        self.map[1][0] = 255

    def is_marker(self, x, y):
        return self.marker[x][y]

    def get_adj(self, x, y):
        adj_list = []
        for i in self.ADJ:
            adj_list.append((x+i[0], y+i[1]))
        return adj_list

    def dfs(self, x, y):
        self.map[x][y] = 255
        self.marker[x][y] = True

        for v in self.get_adj(x, y):
            if not self.is_marker(v[0], v[1]):
                self.dfs(v[0], v[1])

    def show(self):
        plt.imshow(cv2.cvtColor(self.map, cv2.COLOR_GRAY2RGB))
        plt.show()

    def __repr__(self):
        return 'map:\n{}\nmarker:\n{}'.format(self.map, self.marker)


m = Maze((20,30))
# print(m)
print(m.get_adj(0,0))
# m.show()
