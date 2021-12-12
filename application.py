import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWidgets import *
import pts
import circle

myUIClass = uic.loadUiType("main2.ui")[0]

class MyApp(QWidget, myUIClass):
    def __init__(self):
        super().__init__()
        self.pt = pts.Points()
        self.ANIMA = False
        self.INDEX1 = 1
        self.INDEX2 = -1
        self.t = 0
        self.L_FT = []
        self.L_FIT = []
        
        self.ui = uic.loadUi("main2.ui", self)
        self.main_layout = QVBoxLayout()
        
        self.timer = QTimer(self)
        
        self.label_xy.setText('(x,y) = ({0},{1}), {2} points plotted'.format(0,0,0))
        self.label_N.setText('2N-1 = {0} '.format(2 * self.slider.value() - 1))
        
        self.pt.N = self.slider.value()
        
        self.view1 = CView1(self)
        self.view2 = CView2(self)
        
        self.vbox.addWidget(self.view1)
        self.verticalLayout_2.addWidget(self.view2)
        
        self.spliter = QSplitter(Qt.Horizontal)
        
        self.frame.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShape(QFrame.Box)
        
        self.spliter.addWidget(self.frame)
        self.spliter.addWidget(self.frame_2)
        self.main_layout.addWidget(self.spliter)
        
        self.setLayout(self.main_layout)
        
        self.slider.valueChanged.connect(self.slider_changed)
        self.btn.clicked.connect(self.btn_pressed)
        self.slider_INDEX1.valueChanged.connect(self.slider_INDEX1_changed)
        self.slider_INDEX2.valueChanged.connect(self.slider_INDEX2_changed)
        
    def slider_changed(self):
        self.pt.N = self.slider.value()
        self.label_N.setText('2N-1 = {0} '.format(2 * self.slider.value() - 1))
        
    def slider_INDEX1_changed(self):
        self.INDEX1 = self.slider_INDEX1.value()
        if self.slider_INDEX1.value() >= self.pt.N:
            self.INDEX1 = self.pt.N - 1
        if self.slider_INDEX1.value() <= (-1) * self.pt.N:
            self.INDEX1 = 1- self.pt.N
        self.label_INDEX1.setText('INDEX1 = {0} '.format(self.INDEX1))
        
    def slider_INDEX2_changed(self):
        self.INDEX2 = self.slider_INDEX2.value()
        if self.slider_INDEX2.value() >= self.pt.N:
            self.INDEX2 = self.pt.N - 1
        if self.slider_INDEX2.value() <= (-1) * self.pt.N:
            self.INDEX2 = 1 - self.pt.N
        self.label_INDEX2.setText('INDEX2 = {0} '.format(self.INDEX2))
        
    def btn_pressed(self):
        self.ANIMA = True
        if len(self.pt) > 0 and self.ANIMA:
            self.t = 0
            self.timer.timeout.connect(self.animation)
            self.timer.start()     
            
    def animation(self):
        self.view1.animation(self.t)
        self.view2.animation(self.t)
        self.t += 0.0005 * self.pt.N
        
class CView1(QGraphicsView):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent 
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        self.items = []
        self.items_ANIMATION = []
        self.items_TRACE = []

        self.start = QPointF()
        self.end = QPointF()

        self.setRenderHint(QPainter.HighQualityAntialiasing)

    def moveEvent(self, e):
        rect = QRectF(self.rect())
        rect.adjust(0,0,-2,-2)

        self.scene.setSceneRect(rect)

    def mousePressEvent(self, e):
        self.parent.pt.reset()
        self.parent.ANIMA = False
        
        for item in self.items:
            self.scene.removeItem(item)          
        self.items = []

        if e.button() == Qt.LeftButton:
            self.start = e.pos()
            self.end = e.pos()

    def mouseMoveEvent(self, e):
        if e.buttons() and Qt.LeftButton:
            self.parent.pt.addpoint((e.x(),e.y()))
            self.end = e.pos()

            pen = QPen(QColor(0,0,0),1)
            path = QPainterPath()
            path.moveTo(self.start)
            path.lineTo(self.end)
            self.items.append(self.scene.addPath(path, pen))

            self.start = e.pos()
            
            self.parent.label_xy.setText('(x,y) = ({0},{1}), {2} points plotted'.format(e.x(), e.y(), len(self.parent.pt)))

    def mouseReleaseEvent(self, e):       
        self.parent.L_FIT = self.parent.pt.lfit()
        
        for item in self.items_TRACE:
            self.scene.removeItem(item)
        self.items_TRACE = []
        
        for i in range(len(self.parent.L_FIT)):
            pen = QPen(QColor(255,0,0),4)
            brush = QBrush(QColor(255,0,0))            
            rect = QRectF(QPointF(self.parent.L_FIT[i][0], self.parent.L_FIT[i][1]), QSizeF(2, 2))
            self.items.append(self.scene.addEllipse(rect, pen, brush))
            
        self.parent.L_FT = self.parent.pt.ft()

    def animation(self, t):
        for item in self.items_ANIMATION:
            self.scene.removeItem(item)
            
        if len(self.items_TRACE) > 4000:
            self.scene.removeItem(self.items_TRACE[0])
            self.items_TRACE.pop(0)
                
        self.items_ANIMATION = []
            
        N = self.parent.pt.N
        
        tup =  circle.POLAR(self.parent.L_FT[0], 0)
        (x1, y1) = (tup[0], tup[1])

        for i in range(1, N):   
            (dx, dy) = circle.POLAR(self.parent.L_FT[i], i * t)
            (x2, y2) = (x1 + dx, y1 + dy)
            
            pen = QPen(QColor(0,0,255), 2)
            path = QPainterPath()
            path.moveTo(QPointF(x1, y1))
            path.lineTo(QPointF(x2, y2))
            self.items_ANIMATION.append(self.scene.addPath(path, pen))
            
            (x1, y1) = (x2, y2)
            
            (dx, dy) = circle.POLAR(self.parent.L_FT[(-1)*i], (-1)*i * t)
            (x2, y2) = (x1 + dx, y1 + dy)
            
            pen = QPen(QColor(0,0,255), 2)
            path = QPainterPath()
            path.moveTo(QPointF(x1, y1))
            path.lineTo(QPointF(x2, y2))
            self.items_ANIMATION.append(self.scene.addPath(path, pen))
            
            (x1, y1) = (x2, y2)
        
        pen = QPen(QColor(0,0,255),1)
        brush = QBrush(QColor(0,0,255))            
        rect = QRectF(QPointF(x1, y1), QSizeF(1, 1))
        self.items_TRACE.append(self.scene.addEllipse(rect, pen, brush))
        
class CView2(QGraphicsView):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        self.items_ANIMATION = []
        
    def moveEvent(self, e):
        rect = QRectF(self.rect())
        rect.adjust(0,0,-2,-2)

        self.scene.setSceneRect(rect)
        
    def animation(self, t):
        for item in self.items_ANIMATION:
            self.scene.removeItem(item)
                
        self.items_ANIMATION = []
            
        N = self.parent.pt.N
        
        (x1, y1) = (200, 200)
        (dx, dy) = circle.POLAR(self.parent.L_FT[self.parent.INDEX1], self.parent.INDEX1 * t)
        (x2, y2) = (x1 + dx, y1 + dy)
            
        pen = QPen(QColor(0,0,255), 2)
        path = QPainterPath()
        path.moveTo(QPointF(x1, y1))
        path.lineTo(QPointF(x2, y2))
        self.items_ANIMATION.append(self.scene.addPath(path, pen))

        (x1, y1) = (200, 450)                     
        (dx, dy) = circle.POLAR(self.parent.L_FT[self.parent.INDEX2], self.parent.INDEX2 * t)
        (x2, y2) = (x1 + dx, y1 + dy)
            
        pen = QPen(QColor(0,0,255), 2)
        path = QPainterPath()
        path.moveTo(QPointF(x1, y1))
        path.lineTo(QPointF(x2, y2))
        self.items_ANIMATION.append(self.scene.addPath(path, pen))
    