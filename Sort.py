# -*- coding:utf-8 -*-
import sys
sys.setrecursionlimit(1000000)

import random
import time
from matplotlib import pyplot as plt


# 获取随机数据
def GetRandomData(size=10, min=0, max=100):
    ar = []
    for i in range(size):
        ar.append(random.randint(min, max))
    return ar


# 测试, 返回测试规模和对应消耗的时间
def TestSort(test_func, min_size, max_size, step):
    size_list = []
    time_list = []
    for i in range(min_size, max_size, step):
        ar = GetRandomData(i)

        start = time.time()
        test_func(ar)
        end = time.time()
        use_time = (end - start) * 1000

        size_list.append(i)
        time_list.append(use_time)
    return size_list, time_list


# 可视化测试函数返回的数据
def PlotTestData(test_func, size_list, time_list, *args):
    print('all time: {}'.format(sum(time_list)))
    plt.subplot(*args)
    plt.xlabel('size')
    plt.ylabel('time(ms)')
    plt.title(getattr(test_func, '__name__'))
    plt.plot(size_list, time_list)


# 插入排序
def InsertionSort(ar):
    for j in range(1, len(ar)):         # j从数组的第2个开始
        for i in range(0, j):           # i从数组的第1个开始, 但不能超过j
            if ar[j] < ar[i]:           # 如果 ar[j] < ar[i]
                temp = ar[i:j]
                ar[i] = ar[j]           # 将 ar[j] 插入到 ar[i] 的前面
                ar[i+1:j+1] = temp      # 并且将原来数组 ar[i] 到 ar[j-1] 的内容后移1个位置


# 归并排序
def MergeSort(ar):
    if len(ar) == 1:                    # 如果数组只有1个元素,返回
        return ar[0:1]

    mid = len(ar)//2                    # 如果数组元素多于1个, 则将数组分割成两份
    a = MergeSort(ar[0:mid])            # 并将两份继续代入函数中去
    b = MergeSort(ar[mid:len(ar)])

    c = []
    i = j = 0                           # 分割的两份数组已分别排好序
    while i < len(a) and j < len(b):    # 比较两份数组的元素大小, 并将它们按顺序放到一个数组中去
        if a[i] < b[j]:
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1

    if i < len(a):
        c += a[i:len(a)]
    elif j < len(b):
        c += b[j:len(b)]

    return c                            # 返回合并的有序的数组


if __name__ == '__main__':
    test_list = {'MergeSort': 121, 'InsertionSort': 122}

    for key, value in test_list.items():
        test_func = eval(key)
        size_list, time_list = TestSort(test_func)
        PlotTestData(test_func, size_list, time_list, value)

    plt.show()
