#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import cg_algorithms as alg
from typing import Optional
from PyQt5.QtWidgets import (QApplication, QMainWindow, qApp, QGraphicsScene,
                             QGraphicsView, QGraphicsItem, QListWidget,
                             QHBoxLayout, QWidget, QStyleOptionGraphicsItem,
                             QSlider, QLabel,QPushButton)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor
from PyQt5.QtCore import QRectF, Qt, QByteArray


class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None
        #color
        self.red_val = 0
        self.blue_val = 0
        self.green_val = 0
        #curve
        self.curve_stage=0
        self.curve_pid=-1
        self.curve_ok=QPushButton("OK",self)
        self.curve_ok.setEnabled(False)
        self.curve_ok.clicked.connect(self.finish_draw)
        self.curve_ok.move(495,550)
        self.curve_ok.setVisible(False)
        #translate,
        self.transform_stage=0
        self.start_point=[]
        self.start_pos=[]

        self.pos_label=QLabel(self)
        self.pos_label.move(100,200)
        self.red_sld = QSlider(Qt.Horizontal, self)
        self.red_sld.hide()

    def set_pen(self):
        self.red_sld.setFocusPolicy(Qt.NoFocus)
        self.red_sld.setGeometry(30, 40, 100, 30)
        self.red_sld.setMinimum(0)
        self.red_sld.setMaximum(255)
        self.red_sld.valueChanged.connect(self.pen_color)
        self.red_sld.show()
        #red_label=QLabel(self)

        #red_label.setText(QByteArray::number(red_sld.value()))
        #red_sld.valueChanged[int].connect(self.changeValue)

    def pen_color(self):
        self.red_val = self.red_sld.value()

    def start_draw_line(self, algorithm, item_id):
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_ellipse(self, item_id):
        self.status = 'ellipse'
        self.temp_algorithm = 'ellipse'
        self.temp_id = item_id

    def start_draw_polygon(self,algorithm,item_id):
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_curve(self,algorithm,item_id):
        self.status = 'curve'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_translate(self):
        self.status = 'translate'


    def finish_draw(self):
        if self.status=='curve':
            self.temp_item.flag=0
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.curve_stage=0
            self.curve_pid=-1
            self.curve_ok.setEnabled(False)
            self.curve_ok.setVisible(False)
            
        self.temp_id = self.main_window.get_id()
        self.temp_item=None
        self.updateScene([self.sceneRect()])

    def clear_selection(self):
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed(self, selected):
        print(selected)
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        self.status = ''
        self.updateScene([self.sceneRect()])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line' or self.status == 'ellipse':
            self.temp_item = MyItem(self.temp_id, self.status,
                                    [[x, y], [x, y]], self.red_val,
                                    self.blue_val, self.green_val,
                                    self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        elif self.status=='polygon':
            if event.buttons()==Qt.LeftButton:
                if self.temp_item is None:
                    self.temp_item = MyItem(self.temp_id, self.status, 
                                            [[x, y],[x,y]], self.red_val,
                                            self.blue_val,self.green_val,
                                            self.temp_algorithm)
                    self.scene().addItem(self.temp_item)
                else:
                    self.temp_item.p_list.append([x,y])
            elif event.buttons()==Qt.RightButton:
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
                self.finish_draw()
        elif self.status=='curve':
            if self.temp_item is None:
                self.temp_item = MyItem(self.temp_id, self.status,
                                        [[x, y], [x, y],[x,y]], self.red_val,
                                        self.blue_val, self.green_val,
                                        self.temp_algorithm)
                self.scene().addItem(self.temp_item)
            if self.curve_stage==1:
                for i in range(len(self.temp_item.p_list)):
                    x0,y0=self.temp_item.p_list[i]
                    if pow(x-x0,2)+pow(y-y0,2)<=25:
                        self.curve_pid=i
        elif self.status=='translate':
            if event.buttons()==Qt.LeftButton:
                for key in self.item_dict:
                    if self.item_dict[key].boundingRect().contains(x,y):
                        self.selection_changed(key)
                        self.transform_stage=1
                        self.status='translate'
                        self.start_pos=self.item_dict[self.selected_id].p_list
                        self.start_point=[x,y]
                        break
            elif event.buttons()==Qt.RightButton:
                self.clear_selection()
        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line' or self.status == 'ellipse':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'curve':
            if self.curve_stage==0:
                self.temp_item.p_list[2]=[x, y]
                x0,y0=self.temp_item.p_list[0]
                self.temp_item.p_list[1]=[int((x0+x)/2),int((y0+y)/2)]#[int((x0+x)/2),int((y0+y)/2)]
            else:#adjust
                self.temp_item.p_list[self.curve_pid]=[x,y]
        elif self.status=='translate':
            #if self.transform_stage==1:
            if self.selected_id!='':
                self.item_dict[self.selected_id].p_list=alg.translate(self.start_pos,x-self.start_point[0],y-self.start_point[1])
        #self.pos_label.setText(x)
        #pos_label.setText(QByteArray::number(x))
        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    #def adjust_curve(self):


    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.status == 'line' or self.status == 'ellipse':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        if self.status=='curve':
            self.temp_item.flag=1
            self.curve_stage=1
            self.curve_ok.setEnabled(True)
            self.curve_ok.setVisible(True)
            
            #self.item_dict[self.temp_id] = self.temp_item
            #self.list_widget.addItem(self.temp_id)
            #self.finish_draw()
        self.updateScene([self.sceneRect()])
        super().mouseReleaseEvent(event)


class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """
    def __init__(self,
                 item_id: str,
                 item_type: str,
                 p_list: list,
                 red_val: int,
                 blue_val: int,
                 green_val: int,
                 algorithm: str = '',
                 parent: QGraphicsItem = None,
                 flag: int = 0):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id  # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list  # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False
        self.red_val = red_val
        self.blue_val = blue_val
        self.green_val = green_val
        self.flag=flag

    def paint(self,
              painter: QPainter,
              option: QStyleOptionGraphicsItem,
              widget: Optional[QWidget] = ...) -> None:
        painter.setPen(QColor(self.red_val, self.green_val, self.blue_val))
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'polygon':
            item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'curve':
            item_pixels = alg.draw_curve(self.p_list,self.algorithm,self.flag)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())

    def boundingRect(self) -> QRectF:
        if self.item_type == 'line' or self.item_type == 'ellipse':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'polygon':
            x_min, y_min = self.p_list[0]
            x_max, y_max = self.p_list[0]
            for p in self.p_list:
                x_min = min(x_min, p[0])
                y_min = min(y_min, p[1])
                x_max = max(x_max, p[0])
                y_max = max(y_max, p[1])
            w=x_max-x_min
            h=y_max-y_min
            return QRectF(x_min - 1, y_min - 1, w + 2, h + 2)
        elif self.item_type == 'curve':
            res=alg.draw_curve(self.p_list,self.algorithm)
            x_min, y_min = res[0]
            x_max, y_max = res[0]
            for p in res:
                x_min = min(x_min, p[0])
                y_min = min(y_min, p[1])
                x_max = max(x_max, p[0])
                y_max = max(y_max, p[1])
            w=x_max-x_min
            h=y_max-y_min
            return QRectF(x_min - 1, y_min - 1, w + 2, h + 2)


class MainWindow(QMainWindow):
    """
    主窗口类
    """
    def __init__(self):
        super().__init__()
        self.item_cnt = 0

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        set_pen_act = file_menu.addAction('设置画笔')
        reset_canvas_act = file_menu.addAction('重置画布')
        exit_act = file_menu.addAction('退出')
        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        '''
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')
        '''
        # 连接信号和槽函数
        exit_act.triggered.connect(qApp.quit)
        line_naive_act.triggered.connect(self.line_naive_action)
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)
        set_pen_act.triggered.connect(self.set_pen_action)
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)
        ellipse_act.triggered.connect(self.ellipse_action)
        curve_bezier_act.triggered.connect(self.curve_bezier_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)
        translate_act.triggered.connect(self.translate_action)
        '''
        rotate_act.triggered.connect(self.rotate_action)
        scale_act.triggered.connect(self.scale_action)
        clip_cohen_sutherland_act.triggered.connect(self.clip_cohen_sutherland_action)
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)
        '''
        self.list_widget.currentTextChanged.connect(
            self.canvas_widget.selection_changed)

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('CG Demo')

    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id

    def line_naive_action(self):
        self.canvas_widget.start_draw_line('Naive', self.get_id())
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_dda_action(self):
        self.canvas_widget.start_draw_line('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_bresenham_action(self):
        self.canvas_widget.start_draw_line('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_dda_action(self):
        self.canvas_widget.start_draw_polygon('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        

    def polygon_bresenham_action(self):
        self.canvas_widget.start_draw_polygon('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def ellipse_action(self):
        self.canvas_widget.start_draw_ellipse(self.get_id())
        self.statusBar().showMessage('中点圆生成算法绘制椭圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def curve_bezier_action(self):
        self.canvas_widget.start_draw_curve('Bezier',self.get_id())
        self.statusBar().showMessage('Bezier算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_b_spline_action(self):
        self.canvas_widget.start_draw_curve('B-spline',self.get_id())
        self.statusBar().showMessage('B-spline算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def translate_action(self):
        self.canvas_widget.start_translate()
        self.statusBar().showMessage('平移')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    '''    
    def rotate_action(self):
        self.canvas_widget.start_rotate()
        self.statusBar().showMessage('旋转')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def scale_action(self):
        self.canvas_widget.start_translate()
        self.statusBar().showMessage('缩放')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def clip_cohen_sutherland_action(self):
        self.canvas_widget.start_translate()
        self.statusBar().showMessage('Cohen-Sutherland裁剪')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def clip_liang_barsky_action(self):
        self.canvas_widget.start_translate()
        self.statusBar().showMessage('Liang-barsky裁剪')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    '''

    def set_pen_action(self):
        self.canvas_widget.set_pen()
        self.statusBar().showMessage('设置画笔')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
