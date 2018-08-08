# -*- coding:utf-8 -*-


# 图
class Graph:
    def __init__(self, file):
        # 顶点数目
        self.V = []
        self.adj = {}

        self.marker = {}
        self.toedge = {}
        self.loads(file)

    def loads(self, file):
        with open(file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                item = i.strip('\n').split(':')
                # 读取顶点
                self.V.append(item[0])
                # 读取邻接表
                self.adj[item[0]] = item[1].split(' ')

    def init_marker(self):
        for v in self.V:
            self.marker[v] = False

    def dfs(self, start):
        self.marker[start] = True
        print(start)

        for p in self.adj[start]:
            if not self.marker[p]:
                self.toedge[p] = start
                self.dfs(p)

    def path(self, start, end):
        path_list = [end]

        while self.toedge.get(end, None):
            path_list.append(self.toedge[end])
            end = self.toedge[end]
            if end == start:
                return path_list[::-1]
        return None

    def __repr__(self):
        return '<Graph V:{}>\n' \
               '<adj:{}>'.format(self.V, self.adj)


g = Graph('src/graph_test.txt')
g.init_marker()
g.dfs('1')
print(g.path('1', '7'))
