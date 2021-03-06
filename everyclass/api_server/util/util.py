# -*- coding: utf-8 -*-
"""
被其他运行包所引用的工具包
提供了大部分常用功能
"""
import os
import sys


# 自定义异常
class ErrorSignal(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def process_bar(now, total, attach=''):
    # 在窗口底部动态显示进度条
    rate = now / total
    rate_num = int(rate * 100)
    bar_length = int(rate_num / 2)
    blank = '                                                    '
    if rate_num == 100:
        bar = 'Pid:%5d:%s%s' % (os.getpid(), attach, blank)
        bar = '\r' + bar[0:30]
        bar += '%s>%d%%\n' % ('=' * bar_length, rate_num)
    else:
        bar = 'Pid:%5d:%s%s' % (os.getpid(), attach, blank)
        bar = '\r' + bar[0:30]
        bar += '%s>%d%%' % ('=' * bar_length, rate_num)
    sys.stdout.write(bar)
    sys.stdout.flush()


def save_to_cache(semester, folder, name, data):
    # 将获取到的数据缓存至本地，减少数据操作失败后的网络下载时间
    if folder != '':
        cache_file_name = './cache/%s/%s/%s' % (semester, folder, name)
    else:
        cache_file_name = './cache/%s/%s' % (semester, name)
    with open(cache_file_name, 'w', encoding='utf8') as file:
        data = str(data)
        if sys.getsizeof(data) < 104857600:
            file.write(data)
        else:
            for i in range(0, len(data), 4096):
                file.write(data[i: i + 4096])

    # print_i('数据已缓存至 ' + cache_file_name)


def del_from_cache(semester, folder, name):
    # 删除本地的数据缓存，此操作可避免软件读取到错误的缓存
    if folder != '':
        cache_file_name = './cache/%s/%s/%s' % (semester, folder, name)
    else:
        cache_file_name = './cache/%s/%s' % (semester, name)
    if os.path.exists(cache_file_name) is False:
        raise ErrorSignal('文件不存在，请检查本地缓存')
    os.remove(cache_file_name)


def query_from_cache(semester, folder, name):
    # 检查本地缓存是否存在，没有提示
    if folder != '':
        cache_file_name = './cache/%s/%s/%s' % (semester, folder, name)
    else:
        cache_file_name = './cache/%s/%s' % (semester, name)
    if os.path.exists(cache_file_name) is True:
        return True
    else:
        return False


def read_from_cache(semester, folder, name):
    # 读取本地的数据缓存，减少数据操作失败后的网络下载时间
    if folder != '':
        cache_file_name = './cache/%s/%s/%s' % (semester, folder, name)
    else:
        cache_file_name = './cache/%s/%s' % (semester, name)
    if os.path.exists(cache_file_name) is False:
        raise ErrorSignal('文件不存在，请检查本地缓存')
    with open(cache_file_name, 'r', encoding='utf8') as file:
        data = file.read()
    return data
