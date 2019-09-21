#!/user/bin/env python3
# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import Counter
import thulac
import re


# 绘制(价格)频率分布直方图
def price_hit_map(name):
    # 组装文件名
    file_name = str(name) + '.csv'
    # 判断文件是否存在
    if not os.path.exists(file_name):
        print('在此目录下，没有您想要分析的数据文件')
        exit()
    try:
        # 读取数据
        data = pd.read_csv(file_name)
        # 出去缺失数据
        data = data.dropna()
        # 绘制价格频率图
        plt.hist(data["价格"], bins=150, range=(0, 600), density=True,
                 weights=None, cumulative=False, bottom=None,
                 histtype=u'bar', align=u'left', orientation=u'vertical',
                 rwidth=0.8, log=False, color='green', label=None, stacked=False)
        # 保存图片
        fig = plt.gcf()
        # 设置图片大小（width，height）
        fig.set_size_inches(16, 9)
        # 设置图片名称，以及dpi(dpi数值越高，越清晰)
        fig.savefig(str(name) + '.png', dpi=100)
        # 展示频率分布图片
        plt.show()
    except Exception as e:
        print('price_hit_map function is error：', e)
        exit()


# 价格分布饼图
def price_pie_map(name):
    # 组装文件名，注意文件名后缀（目前只适用于csv类型文件）
    file_name = str(name) + '.csv'
    # 判断文件是否存在
    if not os.path.exists(file_name):
        print('您想要处理的文件不存在')
        exit()
    # 解决中文乱码
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 调节图形大小
    plt.figure(figsize=(6, 9))
    # 定义标签
    labels = ['0-50', '51-100', '101-150', '151-200', '201-300', '>300']
    # 计算价格区间每块值
    size_num = 0
    sizes = []
    while size_num < len(labels):
        sizes.append(0)
        size_num = size_num + 1
    explode = tuple(sizes)
    try:
        data = pd.read_csv(file_name)
        price = data['价格']
        for v in price:
            if v >= 0 and v <= 50:
                sizes[0] = sizes[0] + 1
            elif v >= 51 and v <= 100:
                sizes[1] = sizes[1] + 1
            elif v >= 101 and v <= 150:
                sizes[2] = sizes[2] + 1
            elif v >= 151 and v <= 200:
                sizes[3] = sizes[3] + 1
            elif v >= 201 and v <= 300:
                sizes[4] = sizes[4] + 1
            elif v > 300:
                sizes[5] = sizes[5] + 1

        # 每块颜色定义
        colors = ['red', 'yellowgreen', 'lightskyblue', 'yellow', 'seagreen', 'beige']
        # explode = (0, 0, 0, 0,)  # 将某一块分割出来，值越大分割出的间隙越大
        patches, text1, text2 = plt.pie(sizes,
                                        explode=explode,
                                        labels=labels,
                                        colors=colors,
                                        autopct='%3.2f%%',  # 数值保留固定小数位
                                        shadow=False,  # 无阴影设置
                                        startangle=90,  # 逆时针起始角度设置
                                        pctdistance=0.8)  # 数值距圆心半径倍数距离
        # patches饼图的返回值，texts1饼图外label的文本，texts2饼图内部的文本
        # x，y轴刻度设置一致，保证饼图为圆形
        plt.axis('equal')
        # 保存图片
        fig = plt.gcf()
        # 设置图片大小（width，height）
        fig.set_size_inches(16, 9)
        # 设置图片名称，以及dpi(dpi数值越高，越清晰)
        fig.savefig(str('test') + '.png', dpi=100)
        plt.show()
    except Exception as e:
        print('price_pie_map is error:', e)
        exit()


# 热词出现的次数
def hit_Word(name):
    # 组装文件名
    file_name = str(name) + '.csv'
    # 判断文件是否存在
    if not os.path.exists(file_name):
        print('文件不存在')
        exit()
    try:
        # 读取csv文件
        word_data = pd.read_csv(file_name)
        # 实例切词工具
        thul = thulac.thulac()
        hit_word = []
        # 获取数据中的热词
        for v in word_data['商品名称']:
            thul_res = thul.cut(v, text=False)
            for val in thul_res:
                hit_word.append(val[0])
        # 统计热词出现的次数
        result = Counter(hit_word).most_common(20)
        # 定义空数据
        goods = []
        goods_sale = []
        # 组装xy轴数据
        for v in result:
            goods.append(v[0])
            goods_sale.append(v[1])
        # 改变字符集，确保内容文字不会乱码
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 创建图版
        plt.figure(figsize=(16, 9), dpi=50)
        # 再创建一个规格为 1 x 1 的子图
        plt.subplot(1, 1, 1)
        # 绘制柱状图
        plt.bar(range(len(goods)), tuple(goods_sale), width=0.35, label="热词出现的次数", color="#87CEEB")
        # 设置抬头
        plt.title('前20个热词统计图')
        # 设置横轴标签
        plt.xlabel('热词')
        # 设置纵轴标签
        plt.ylabel('数量 (个)')
        # 添加纵横轴的刻度
        plt.xticks(np.arange(len(goods)), tuple(goods))
        plt.yticks(np.arange(0, goods_sale[0], 100))
        # 添加图例
        plt.legend(loc="upper right")
        # 保存图片
        fig = plt.gcf()
        # 设置图片大小（width，height）
        fig.set_size_inches(16, 9)
        # 设置图片名称，以及dpi(dpi数值越高，越清晰)
        fig.savefig('前20个热词统计图.png', dpi=100)
        plt.show()
    except Exception as e:
        print('hit_Word is error :', e)
        exit()


# 价格与销售量关系
def price_sale_plt(name):
    # 组装文件名高
    file_name = str(name) + '.csv'
    # 判断文件是否存在
    if not os.path.exists(file_name):
        print('文件不存在')
        exit()
    # 读取文件
    data = pd.read_csv(file_name)
    # 判断文件是否有数据
    if os.path.getsize(file_name) == 0:
        print('您想要分析的数据为空，请检查！')
        exit()
    x_labels = ['0-50', '51-100', '101-150', '151-200', '201-300', '>300']
    y_labels = []
    # 初始化y轴数据
    num = 0
    while num < len(x_labels):
        y_labels.append(0)
        num = num + 1

    try:
        for i, price in enumerate(data['价格']):
            # 处理销售量数值
            split_data = data['购买人数'][i].split('人')[0]
            split_data = re.sub(r'\+', '', split_data)
            if split_data.find('万') and not split_data.find('万') == -1:
                sale = re.sub(r'万', '', split_data)
                sale = float(sale) * 10000
            else:
                sale = int(split_data)
            # 根据价格区间组装数据
            if price >= 0 and price <= 50:
                y_labels[0] = y_labels[0] + sale
            elif price >= 51 and price <= 100:
                y_labels[1] = y_labels[1] + sale
            elif price >= 101 and price <= 150:
                y_labels[2] = y_labels[2] + sale
            elif price >= 151 and price <= 200:
                y_labels[3] = y_labels[3] + sale
            elif price >= 201 and price <= 300:
                y_labels[4] = y_labels[4] + sale
            elif price > 300:
                y_labels[5] = y_labels[5] + sale

    except Exception as e:
        print('price_sale_plt is error:', e)

    # 改变字符集，确保内容文字不会乱码
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 创建图版
    plt.figure(figsize=(16, 9), dpi=100)
    # 设置抬头
    plt.title('价格与销售量流程图')
    # 绘制柱状图
    plt.bar(range(len(x_labels)), tuple(y_labels), width=0.35, label='销售量', color='#87CEEB')
    # 设置横轴标签
    plt.xlabel('价格区间')
    # 设置纵轴标签
    plt.ylabel('销售数量')
    # 添加纵横轴的刻度
    plt.xticks(np.arange(len(x_labels)), tuple(x_labels))
    plt.yticks(np.arange(0, max(y_labels), 50000), )
    # 保存图片
    fig = plt.gcf()
    # 设置图片大小（width，height）
    fig.set_size_inches(16, 9)
    # 设置图片名称，以及dpi(dpi数值越高，越清晰)
    fig.savefig('价格与销售量关系图.png', dpi=100)
    plt.show()


if __name__ == '__main__':
    price_pie_map('男装秋季')
