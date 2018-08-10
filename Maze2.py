# -*- coding: utf-8 -*-
import sys
sys.setrecursionlimit(100000)

import os
import random
import cv2
import numpy as np
from matplotlib import pyplot as plt


class Maze2:
    # 方向
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    ADJ = [UP, DOWN, LEFT, RIGHT]

    def __init__(self, size):
        # 记录输入尺寸
        self.height = size[0]
        self.width = size[1]

        # 辅助变量
        self.ct = 0
        self.set = set()
        self.get_end = False

        # 其它初始化
        self.init_map()
        self.init_video()
        self.init_point()

    # 地图初始化
    def init_map(self):
        self.map = np.zeros((self.height, self.width), np.uint8)
        self.map[1::2, 1::2] = 255      # 将每个奇数坐标设为路

    # 视频初始化
    def init_video(self):
        self.rec = False
        self.play = False
        self.cv2_fx = 5
        self.cv2_fy = 5

    # 起止点初始化
    def init_point(self):
        self.START = (1, 0)
        self.END = (self.height - 2, self.width - 1)

    # 设置视频缩放比例
    def set_scale(self, fx, fy):
        self.cv2_fx = fx
        self.cv2_fy = fy

    # 记录视频
    def use_recorder(self, outfile='out.avi', fps=20):
        self.rec = True
        self.fourcc = cv2.VideoWriter_fourcc(*'X264')
        self.out = cv2.VideoWriter(outfile, self.fourcc, fps, (self.width*self.cv2_fx, self.height*self.cv2_fy))

    # 即时播放
    def use_player(self, wait_key=1):
        self.play = True
        self.wait_key = wait_key

    # 判断视频参数, 并采取动作
    def cv2_video(self):
        im = cv2.resize(self.map, None, fx=self.cv2_fx, fy=self.cv2_fy, interpolation=cv2.INTER_AREA)
        if self.rec:
            self.out.write(cv2.cvtColor(im, cv2.COLOR_GRAY2BGR))
        if self.play:
            cv2.imshow('cv2', im)
            cv2.waitKey(self.wait_key)

    # 判断点是否属于边界
    def in_side(self, x, y):
        if x <= 0 or x >= self.height - 1 or y <= 0 or y >= self.width - 1:
            return True
        return False

    # 判断点是否属于集合
    def in_set(self, x, y):
        return (x, y) in self.set

    # 将点添加到集合
    def add_set(self, x, y):
        self.set.add((x, y))

    # 清空集合
    def clear_set(self):
        self.set.clear()

    # 打通墙
    def break_it(self, x, y):
        self.map[x][y] = 255
        self.cv2_video()

    # 前进
    def walk_it(self, x, y):
        self.map[x][y] = 127
        self.cv2_video()

    # 回退
    def walk_back(self, x, y):
        self.map[x][y] = 255
        self.cv2_video()

    # 获取随机方向列表
    def get_adj_random(self):
        adj = self.ADJ.copy()
        random.shuffle(adj)
        return adj

    # 按随机顺序获取邻近边以及边对应的点
    def get_edge_random(self, x, y):
        edge_list = []
        vertex_list = []

        for i in self.get_adj_random():
            # 排除边界点
            if not self.in_side(x + i[0], y + i[1]):
                edge_list.append((x + i[0], y + i[1]))
                vertex_list.append((x + i[0]*2, y + i[1]*2))

        return edge_list, vertex_list

    # 添加点到集合, 并递归访问邻近的点(dfs)
    def build(self, x=1, y=1):
        self.add_set(x, y)
        edge_list, vertex_list = self.get_edge_random(x, y)

        for e, v in zip(edge_list, vertex_list):
            if not self.in_set(v[0], v[1]):
                self.break_it(e[0], e[1])
                self.build(v[0], v[1])

    # 创建地图
    def build_map(self):
        self.build()
        self.break_it(self.START[0], self.START[1])
        self.break_it(self.END[0], self.END[1])

    def is_road(self, x, y):
        if self.map[x][y] == 255:
            return True
        return False

    def is_end(self, x, y):
        if x == self.END[0] and y == self.END[1]:
            self.get_end = True
            return True
        return False

    def play_map(self, x=1, y=0):
        self.walk_it(x, y)

        for i in self.ADJ:
            if self.is_end(x+i[0], y+i[1]):
                self.walk_it(x+i[0], y+i[1])
                return

            if not self.get_end and not self.in_side(x+i[0], y+i[1]) and self.is_road(x+i[0], y+i[1]):
                self.play_map(x+i[0], y+i[1])
                if not self.get_end:
                    self.walk_back(x+i[0], y+i[1])

    def save_pic(self):
        plt.imshow(cv2.cvtColor(self.map, cv2.COLOR_GRAY2RGB))
        plt.savefig(os.path.join('build', '{:04}.jpg'.format(self.ct)))

    def show(self):
        plt.imshow(cv2.cvtColor(self.map, cv2.COLOR_GRAY2RGB))
        plt.show()


m = Maze2((21, 31))
m.set_scale(15, 15)
m.use_player()
# m.use_recorder()
m.build_map()
m.play_map()
