# -*- coding:utf-8 -*-


# 图
class Graph:
    def __init__(self, file):
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

    # 深度优先
    def dfs(self, start):
        self.marker[start] = True

        for v in self.adj[start]:
            # 是否已记录, 未记录则继续搜索
            if not self.marker[v]:
                self.toedge[v] = start
                self.dfs(v)

    # 查找两点之间的路径
    def path(self, start, end):
        # 先进行dfs, 获取所有能通向start的顶点
        self.init_marker()
        self.dfs(start)

        path_list = [end]
        while self.toedge.get(end, None):
            path_list.append(self.toedge[end])
            end = self.toedge[end]
            if end == start:
                return path_list[::-1]
        return None

    def __repr__(self):
        adj_message = ''
        for key, value in self.adj.items():
            adj_message += '{}:{}\n'.format(key, value)

        return '<Graph>\n' \
               'V:{}\n' \
               '{}'.format(self.V, adj_message)


g = Graph('src/graph_test.txt')
print(g)
print(g.path('1', '4'))
