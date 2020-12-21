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
        if x0 > x1:
            x0, y0, x1, y1 = x1, y1, x0, y0
        if x0 == x1:
            if y0 > y1:
                y0, y1 = y1, y0
            for y in range(y0, y1 + 1):
                result.append((int(x0), int(y)))
        else:
            k = (y1 - y0) / (x1 - x0)
            if k == 0:
                for x in range(x0, x1 + 1):
                    result.append((int(x), int(y0)))
            elif abs(k) == 1:
                x = x0
                y = y0
                while x <= x1 + 1:
                    result.append((int(x), int(y)))
                    x += 1
                    y += k
            elif abs(k) < 1:
                x_dis = x1 - x0
                y_dis = abs(y1 - y0)
                result.append((x0, y0))
                p = 2 * y_dis - x_dis
                y = y0
                for x in range(x0 + 1, x1 + 1):
                    if p < 0:
                        result.append((int(x), int(y)))
                        p += 2 * y_dis
                    else:
                        if k > 0:
                            y += 1
                        else:
                            y -= 1
                        result.append((int(x), int(y)))
                        p += (2 * y_dis - 2 * x_dis)
            else:
                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                x_dis = abs(x1 - x0)
                y_dis = y1 - y0
                result.append((x0, y0))
                p = 2 * x_dis - y_dis
                x = x0
                for y in range(y0 + 1, y1 + 1):
                    if p < 0:
                        result.append((int(x), int(y)))
                        p += 2 * x_dis
                    else:
                        if k > 0:
                            x += 1
                        else:
                            x -= 1
                        result.append((int(x), int(y)))
                        p += (2 * x_dis - 2 * y_dis)
    return result


def draw_polygon(p_list, algorithm, flag=0):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    if flag == 0:
        for i in range(len(p_list)):
            line = draw_line([p_list[i - 1], p_list[i]], algorithm)
            result += line
    elif flag == 1:
        for i in range(1, len(p_list)):
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
    if x0 > x1 and y0 > y1:
        x0, y0, x1, y1 = x1, y1, x0, y0
    elif x0 > x1 and y0 < y1:
        x0, y0, x1, y1 = x1, y0, x0, y1
    elif x0 < x1 and y0 > y1:
        x0, y0, x1, y1 = x0, y1, x1, y0
    xc = (x0 + x1) / 2
    yc = (y0 + y1) / 2
    rx = (x1 - x0) / 2
    ry = (y1 - y0) / 2
    result = []
    x = 0
    y = ry
    result.append([int(xc), int(yc + y)])
    result.append([int(xc), int(yc - y)])
    sq_rx = pow(rx, 2)
    sq_ry = pow(ry, 2)
    p1 = sq_ry - sq_rx * ry + 1 / 4 * sq_rx
    while sq_ry * x < sq_rx * y:
        x += 1
        if p1 < 0:
            p1 += 2 * sq_ry * x + sq_ry
        else:
            y -= 1
            p1 += 2 * sq_ry * x - 2 * sq_rx * y + sq_ry

        result.append([int(xc + x), int(yc + y)])
        result.append([int(xc - x), int(yc + y)])
        result.append([int(xc - x), int(yc - y)])
        result.append([int(xc + x), int(yc - y)])
    p2 = sq_ry * pow(x + 1 / 2, 2) + sq_rx * pow(y - 1, 2) - sq_rx * sq_ry
    while y > 0:
        y -= 1
        if p2 >= 0:
            p2 += (sq_rx - 2 * sq_rx * y)
        else:
            x += 1
            p2 += (2 * sq_ry * x - sq_rx * (2 * y + 1))
        result.append([int(xc + x), int(yc + y)])
        result.append([int(xc - x), int(yc + y)])
        result.append([int(xc - x), int(yc - y)])
        result.append([int(xc + x), int(yc - y)])

    return result


def draw_curve(p_list, algorithm, flag=0):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-sp1ine'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """

    result = []
    n = len(p_list)
    points = []
    px, py = [], []
    precision = 100

    for i in range(n):
        px.append(p_list[i][0])
        py.append(p_list[i][1])

    if algorithm == "Bezier":
        for u in range(0, precision):
            u = u / precision
            for i in range(1, n):
                for j in range(0, n - i):
                    px[j] = (1 - u) * px[j] + u * px[j + 1]
                    py[j] = (1 - u) * py[j] + u * py[j + 1]
            points.append((int(px[0]), int(py[0])))
        for i in range(0, len(points) - 1):
            line = [points[i], points[i + 1]]
            result.extend(draw_line(line, "DDA"))
    elif algorithm == "B-spline":
        k = 4
        n = len(p_list)
        if n < 4:
            return p_list
        du = 1 / 1000
        u = k - 1
        while u <= n:
            x, y = 0, 0
            for i in range(n):
                x0, y0 = p_list[i]
                temp = B(i, k, u)
                x += x0 * temp
                y += y0 * temp
            result.append([int(x), int(y)])
            u += du

    if flag == 1:
        for p in p_list:
            x0, y0, x1, y1 = p[0] - 5, p[1] - 5, p[0] + 5, p[1] + 5
            result.extend(draw_ellipse([[x0, y0], [x1, y1]]))

    return result


def B(i, k, u):
    if k == 1:
        if u >= i and u < i + 1:
            return 1
        else:
            return 0
    else:
        return (u - i) / (k - 1) * B(i, k - 1, u) + (i + k - u) / (k - 1) * B(
            i + 1, k - 1, u)


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for p in p_list:
        result.append((p[0] + dx, p[1] + dy))
    return result


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    h = math.radians(r)
    result = []
    for p in p_list:
        x1 = x + (p[0] - x) * math.cos(h) - (p[1] - y) * math.sin(h)
        y1 = y + (p[0] - x) * math.sin(h) + (p[1] - y) * math.cos(h)
        result.append((int(x1), int(y1)))
    return result


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for p in p_list:
        x1 = p[0] * s + x * (1 - s)
        y1 = p[1] * s + y * (1 - s)
        result.append((int(x1), int(y1)))
    return result


def encode(x, y, x_min, y_min, x_max, y_max):
    c = (int(y > y_max) << 3) + (int(y < y_min) << 2) + (
        int(x > x_max) << 1) + int(x < x_min)
    return c  #Liang-Barsky


def inter_point(border, x1, y1, x2, y2):
    if x1 != x2:
        u = (border - x1) / (x2 - x1)
        if u >= 0 and u <= 1:  #valid
            return [border, int(y1 + u * (y2 - y1))]
        else:
            return [x1, y1]


def update(p, q, u):
    res = True
    if p == 0 and q < 0:
        res = False
    if p < 0:
        u[0] = max(u[0], q / p)
    elif p > 0:
        u[1] = min(u[1], q / p)
    if u[0] > u[1]:
        res = False
    return res


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
    x1, y1 = p_list[0]
    x2, y2 = p_list[1]
    result = []
    if algorithm == 'Cohen-Sutherland':
        flag = 1
        i = 0
        while flag:
            i += 1
            if i > 4:
                break
            c1 = encode(x1, y1, x_min, y_min, x_max, y_max)
            c2 = encode(x2, y2, x_min, y_min, x_max, y_max)
            if (c1 & c2) == 0:  #probably part of line in window
                if (c1 or c2) != 0:  #at least one point out of window
                    if c1 == 0:  # p1 in window,exchange p1 and p2 to ensure p1 out of window
                        temp_x = x1
                        temp_y = y1
                        x1 = x2
                        y1 = y2
                        x2 = temp_x
                        y2 = temp_y
                    if c1 & 1:  #left
                        x1, y1 = inter_point(x_min, x1, y1, x2, y2)
                    elif c1 & 2:  #right
                        x1, y1 = inter_point(x_max, x1, y1, x2, y2)
                    elif c1 & 4:  #down
                        y1, x1 = inter_point(y_min, y1, x1, y2, x2)
                    elif c1 & 8:  #up
                        y1, x1 = inter_point(y_max, y1, x1, y2, x2)
                else:  #p1 and p2 both in window
                    flag = 0
            else:  # line out of window
                flag = 0
        result = [[int(x1), int(y1)], [int(x2), int(y2)]]
    elif algorithm == 'Liang-Barsky':
        u = [0, 1]
        dx = x2 - x1
        dy = y2 - y1
        p1, p2, p3, p4 = dx, dx, dy, dy
        q1, q2, q3, q4 = x1 - x_min, x_max - x1, y1 - y_min, y_max - y1
        if update(-p1, q1, u):
            if update(p2, q2, u):
                if update(-p3, q3, u):
                    if update(p4, q4, u):
                        u1, u2 = u
                        if u2 < 1:
                            x2 = x1 + u2 * dx
                            y2 = y1 + u2 * dy
                        if u1 > 0:
                            x1 = x1 + u1 * dx
                            y1 = y1 + u1 * dy
        result = [[int(x1), int(y1)], [int(x2), int(y2)]]
    return result
