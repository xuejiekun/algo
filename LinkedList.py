# -*- coding:utf-8 -*-
import time
from datetime import datetime


class Node:
    def __init__(self):
        now = datetime.now()
        self.build_time = datetime(now.year, now.month, now.day,
                                   now.hour, now.minute, now.second)
        self.next = None

    def __repr__(self):
        return '<Node {}>'.format(self.build_time)


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.ct = 0

    def add(self, node):
        if self.head is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self.ct += 1

    def remove(self, node):
        prev = None
        seek = self.head
        while seek:
            if seek.build_time == node.build_time:
                # Only one
                if self.head == self.tail:
                    self.head = None
                    self.tail = None
                # Del end
                elif node.next == None:
                    prev.next = None
                    self.tail = prev
                # Del start
                elif prev is None:
                    self.head = node.next
                # Normal
                else:
                    prev.next = node.next
                del node
                self.ct -= 1
                return True
            prev = seek
            seek = seek.next
        return False

    def get_all(self):
        seek = self.head
        node_list = []
        while seek:
            node_list.append(seek)
            seek = seek.next
        return node_list

    def __len__(self):
        return self.ct

    def __repr__(self):
        return '<LinkedList has:{} Node>'.format(self.ct)


l = LinkedList()

a = Node()
l.add(a)
time.sleep(1)

for i in range(5):
    l.add(Node())
    time.sleep(1)

b = Node()
l.add(b)
