#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        xDis = x1 - x0
        yDis = y1 - y0
        maxDis = max(abs(xDis), abs(yDis))
        if maxDis == 0:
            result.append((x0, y0))
        else:
            xStep = xDis / maxDis
            yStep = yDis / maxDis
            i = 0
            x = x0
            y = y0
            while i < maxDis:
                result.append((int(x), int(y)))
                x += xStep
                y += yStep
                i += 1
    elif algorithm == 'Bresenham':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            k = (y1-y0) / (x1-x0)
            if k==0:
                for x in range(x0, x1 + 1):
                    result.append((x, y0))
            elif abs(k) == 1:
                x = x0
                y = y0
                while x <= x1 + 1:
                    result.append((x, y))
                    x += 1
                    y += k
            elif abs(k) < 1:
                if x0 > x1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                x_dis = x1 - x0
                y_dis = abs(y1 - y0)
                result.append((x0, y0))
                p = 2 * y_dis - x_dis
                y = y0
                for x in range(x0+1, x1 + 1):
                    if p < 0:
                        result.append((x, y))
                        p += 2 * y_dis
                    else:
                        if k>0:
                            y+=1
                        else:
                            y-=1
                        result.append((x, y))
                        p += (2 * y_dis - 2 * x_dis)
            else:
                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                x_dis = abs(x1 - x0)
                y_dis = y1 - y0
                result.append((x0, y0))
                p = 2 * x_dis - y_dis
                x = x0
                for y in range(y0+1, y1 + 1):
                    if p < 0:
                        result.append((x, y))
                        p += 2 * x_dis
                    else:
                        if k>0:
                            x+=1
                        else:
                            x-=1
                        result.append((x, y))
                        p += (2 * x_dis - 2 * y_dis)
    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result



def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    if x0 > x1 and y0>y1:
        x0, y0, x1, y1 = x1, y1, x0, y0
    elif x0 > x1 and y0<y1:
        x0, y0, x1, y1 = x1, y0, x0, y1
    elif x0 < x1 and y0>y1:
        x0, y0, x1, y1 = x0, y1, x1, y0
    xc=(x0+x1)/2
    yc=(y0+y1)/2
    rx=(x1-x0)/2
    ry=(y1-y0)/2
    result=[]
    x=0
    y=ry
    result.append([int(xc),int(yc+y)])
    result.append([int(xc),int(yc-y)])
    sq_rx=pow(rx,2)
    sq_ry=pow(ry,2)
    p1=sq_ry-sq_rx*ry+1/4*sq_rx
    while sq_ry*x<sq_rx*y:
        x+=1
        if p1<0:
            p1+=2*sq_ry*x+sq_ry
        else:
            y-=1
            p1+=2*sq_ry*x-2*sq_rx*y+sq_ry
        result.append([int(xc+x),int(yc+y)])
        result.append([int(xc-x),int(yc+y)])
        result.append([int(xc-x),int(yc-y)])
        result.append([int(xc+x),int(yc-y)])
    p2=sq_ry*pow(x+1/2,2)+sq_rx*pow(y-1,2)-sq_rx*sq_ry
    while y>=0 and x<=rx:
        y-=1
        if p2>0:
            p2+=(sq_rx-2*sq_rx*y)
        else:
            x+=1
            p2+=(2*sq_ry*x-2*sq_rx*y+sq_rx)
        result.append([int(xc+x),int(yc+y)])
        result.append([int(xc-x),int(yc+y)])
        result.append([int(xc-x),int(yc-y)])
        result.append([int(xc+x),int(yc-y)])
    return result
    

def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-sp1ine'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    pass


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    pass
