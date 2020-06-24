import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtMultimedia
import random
from PyQt5 import QtWidgets
import ctypes
import os
from PIL import Image


class FirstWindow(QWidget):
    close_signal = pyqtSignal()
    sendmsg = pyqtSignal(str,float,bool,int)
    sendmsg1 = pyqtSignal(str,float,bool,int)
    def __init__(self, parent=None):
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        super(FirstWindow, self).__init__(parent)
        self.setWindowTitle("桌宠设定")
        # self.setupUi()
        self.resize(500, 150)
        layout = QVBoxLayout()

        self.rb1 = QRadioButton("拉普兰德")
        layout.addWidget(self.rb1)
        self.rb1.setChecked(True)
        self.rb2 = QRadioButton("幽灵鲨")
        layout.addWidget(self.rb2)
        self.buttonGroup1 = QtWidgets.QButtonGroup()
        self.buttonGroup1.addButton(self.rb1)
        self.buttonGroup1.addButton(self.rb2)


        self.label = QLabel('不透明度')
        self.label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(10)
        self.slider.setMaximum(100)
        self.slider.setSingleStep(10)
        self.slider.setValue(50)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        layout.addWidget(self.slider)

        self.checkBox1 = QCheckBox('鼠标可穿透')
        self.checkBox1.setChecked(False)
        #self.checkBox1.stateChanged.connect(lambda:self.checkboxState(self.checkBox1))
        layout.addWidget(self.checkBox1)

        self.rb3 = QRadioButton("站立")
        layout.addWidget(self.rb3)
        self.rb3.setChecked(True)
        self.rb4 = QRadioButton("坐下")
        layout.addWidget(self.rb4)
        self.rb5 = QRadioButton("睡觉")
        layout.addWidget(self.rb5)
        self.buttonGroup2 = QtWidgets.QButtonGroup()
        self.buttonGroup2.addButton(self.rb3)
        self.buttonGroup2.addButton(self.rb4)
        self.buttonGroup2.addButton(self.rb5)

        self.btn1 = QToolButton(self)
        self.btn1.setText("确认")
        self.btn1.clicked.connect(self.pbMin)
        self.btn1.clicked.connect(self.readandrun)
        self.btn1.clicked.connect(lambda :self.btn1.setEnabled(False))
        layout.addWidget(self.btn1)

        # self.btn2 = QToolButton(self)
        # self.btn2.setText("消除")
        # layout.addWidget(self.btn2)

        self.btn3 = QToolButton(self)
        self.btn3.setText("更改")
        self.btn3.clicked.connect(self.adjustandrun)
        layout.addWidget(self.btn3)

        self.setLayout(layout)
        self.close_signal.connect(self.close)



    def readandrun(self):
        opacity = self.slider.value()
        mousethrough = self.checkBox1.isChecked()
        if self.rb1.isChecked():
            character = "Lappland"
        else:
            character = "Specter"

        if self.rb3.isChecked():
            act = 0
        elif self.rb4.isChecked():
            act = 1
        else:
            act = 2
        # print(character,opacity,mousethrough)
        self.sendmsg.emit(character,opacity,mousethrough,act)

    def adjustandrun(self):
        opacity = self.slider.value()
        mousethrough = self.checkBox1.isChecked()
        if self.rb1.isChecked():
            character = "Lappland"
        else:
            character = "Specter"

        if self.rb3.isChecked():
            act = 0
        elif self.rb4.isChecked():
            act = 1
        else:
            act = 2
        # print(character,opacity,mousethrough)
        self.sendmsg1.emit(character,opacity,mousethrough,act)


    def closeEvent(self, event):
        self.close_signal.emit()
        self.close()

    def pbMin(self):
        self.hide()
        self.mSysTrayIcon = QSystemTrayIcon(self)
        icon = QIcon("44.png")
        self.mSysTrayIcon.setIcon(icon)
        self.mSysTrayIcon.setToolTip("我在这里哦！")
        self.mSysTrayIcon.activated.connect(self.onActivated)
        self.mSysTrayIcon.show()

    def onActivated(self, reason):
        if reason == self.mSysTrayIcon.Trigger:
            self.show()
            self.mSysTrayIcon.hide()

# class SecondWindow(QWidget):
#     def __init__(self, parent=None):
#         super(SecondWindow, self).__init__(parent)
#         self.resize(300, 300)
#         self.setStyleSheet("background: white")
#     def handle_click(self):
#         if not self.isVisible():
#             self.show()
#
#     def handle_close(self):
#         self.close()



class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        #self.initUI()

    def get(self,character,opacity,mousethrough,act):
        #print(character,opacity,mousethrough,act)
        self.character = character
        self.opacity = opacity/100
        self.mouseThrough = mousethrough
        self.act = act
        print(self.character,self.opacity,self.mouseThrough,self.act)


    def initUI(self):
        #self.character = character
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.timecon,self.gifwidth,self.gifheight = self.gifPro(self.character+"/"+self.character+"Touch.gif")

        self.repaint()
        screen_geo = QDesktopWidget().screenGeometry()
        self.resize(screen_geo.width(), screen_geo.height())
        self.lable = QLabel("", self)
        self.lable.setScaledContents(True)
        self.randomPosition()
        self.is_follow_mouse = False
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(self.opacity)
        self.lable.setGraphicsEffect(op)
        self.lable.setAttribute(Qt.WA_TransparentForMouseEvents,True)

        #self.mouseThrough = mouseThrough
        self.toggleMouseThrough()

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # 创建QMenu信号事件
        self.customContextMenuRequested.connect(self.showMenu)
        self.contextMenu = QMenu(self)
        self.wechat = self.contextMenu.addAction('微信')
        self.surf = self.contextMenu.addAction('百度')
        self.tran = self.contextMenu.addAction('转换动作')
        self.talk = self.contextMenu.addMenu("交谈")
        self.exit = self.contextMenu.addAction('退出')
        # 二级菜单
        self.talk1 = self.talk.addAction('交谈1')
        self.talk2 = self.talk.addAction('交谈2')
        self.talk3 = self.talk.addAction('交谈3')
        # 事件绑定
        self.wechat.triggered.connect(self.wechatEvent)
        self.surf.triggered.connect(self.surfEvent)
        self.tran.triggered.connect(self.tranEvent)
        self.exit.triggered.connect(self.exitEvent)
        self.talk1.triggered.connect(self.talkEvent1)
        self.talk2.triggered.connect(self.talkEvent2)
        self.talk3.triggered.connect(self.talkEvent3)

        self.movie = [QMovie(self.character+"/"+self.character+"RestLoop.gif"),
                      QMovie(self.character+"/"+self.character+"SitLoop.gif"),
                      QMovie(self.character+"/"+self.character+"SleepLoop.gif"),
                      QMovie(self.character+"/"+self.character+"Touch.gif")]

        #self.Play(0)
        self.Play(self.act)
        self.cur = self.act
        self.playBGM()

    def getandadjust(self,character,opacity,mousethrough,act):
        self.character = character
        self.opacity = opacity / 100
        self.mouseThrough = mousethrough
        self.act = act
        print(self.character, self.opacity, self.mouseThrough, self.act)
        self.timecon, self.gifwidth, self.gifheight = self.gifPro(self.character + "/" + self.character + "Touch.gif")
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(self.opacity)
        self.lable.setGraphicsEffect(op)
        self.toggleMouseThrough()
        self.movie = [QMovie(self.character+"/"+self.character+"RestLoop.gif"),
                      QMovie(self.character+"/"+self.character+"SitLoop.gif"),
                      QMovie(self.character+"/"+self.character+"SleepLoop.gif"),
                      QMovie(self.character+"/"+self.character+"Touch.gif")]
        self.Play(self.act)
        self.cur = self.act


    def handle_click(self):
        if not self.isVisible():
            self.show()

    def handle_close(self):
        self.close()

    def gifPro(self,url):
        im = Image.open(url)
        n = 0
        width = im.width
        height = im.height
        try:
            while True:
                im.seek(im.tell() + 1)
                n += 1
        except:
            #print(n / 12.5 * 1000, width, height)
            return n / 12.5 * 1000, width, height


    def quit(self):
        self.close()
        sys.exit()

    def showMenu(self, pos):
        # pos 鼠标位置
        #print(pos)
        # 菜单显示前,将它移动到鼠标点击的位置
        self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示
    def Event(self):
        QMessageBox.information(self, "提示：", '   您选择了' + self.sender().text())

    def tranEvent(self):
        self.cur = (self.cur+1)%3
        self.Play(self.cur)

    def wechatEvent(self):
        os.startfile("微信.lnk")

    def playMusic(self,url):
        content = QtMultimedia.QMediaContent(url)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)
        self.player.play()

    def talkEvent1(self):
        url = QUrl.fromLocalFile(self.character+"/"+self.character+"_C1.wav")
        self.playMusic(url)

    def talkEvent2(self):
        url = QUrl.fromLocalFile(self.character+"/"+self.character+"_C2.wav")
        self.playMusic(url)

    def talkEvent3(self):
        url = QUrl.fromLocalFile(self.character+"/"+self.character+"_C3.wav")
        self.playMusic(url)


    def playBGM(self):
        url = QUrl.fromLocalFile("Sound/bgm.wav")
        content = QtMultimedia.QMediaContent(url)
        self.bgmPlayer = QtMultimedia.QMediaPlayer()
        self.bgmPlayer.setMedia(content)
        self.bgmPlayer.setVolume(100)
        self.bgmPlayer.play()



    #退出功能
    def exitEvent(self):
        self.quit()

    #上网功能
    def surfEvent(self):
        os.system('"Google Chrome.lnk" http://www.baidu.com')

    #鼠标穿透效果
    def toggleMouseThrough(self):
        selfWnd = int(self.winId())
        ret = ctypes.windll.user32.GetWindowLongA(selfWnd, -20)
        if self.mouseThrough:
            ret = ret | 0x00000020
        else:
            ret = ret & ~0x00000020
        ctypes.windll.user32.SetWindowLongA(selfWnd, -20, ret)

    #随机初始位置
    def randomPosition(self):
        screen_geo = QDesktopWidget().screenGeometry()
        pet_geo = self.geometry()
        width = (screen_geo.width() - 622) * random.random()
        height = (screen_geo.height() - 488) * random.random()
        self.move(width, height)

    #播放动画效果
    def Play(self, no=0):
        self.lable.setMovie(self.movie[no])
        self.movie[no].start()

    # def playSet(self):
    #     self.Play(self.act)


    # def drop(self):
    #     if self.lable.y() != 680:
    #         self.path = QPainterPath()
    #         self.path.moveTo(self.lable.x(), self.lable.y())
    #         self.path.lineTo(self.lable.x(), 680)
    #         self.anim = QPropertyAnimation(self.lable, b'pos')
    #         self.anim.setDuration(100)
    #         self.anim.setStartValue(QPointF(self.lable.x(), self.lable.y()))
    #         vals = [p / 100 for p in range(0, 101)]
    #         for i in vals:
    #             self.anim.setKeyValueAt(i, self.path.pointAtPercent(i))  # 设置100个关键帧
    #         self.anim.setEndValue(QPointF(self.lable.x(), 680))
    #         self.anim.start()

    # def displacement(self,disp):
    #     self.path = QPainterPath()
    #     self.path.moveTo(self.lable.x(), self.lable.y())
    #     self.path.lineTo(self.lable.x() + disp, self.lable.y())
    #     self.anim = QPropertyAnimation(self.lable, b'pos')
    #     self.anim.setDuration(2000)
    #     self.anim.setStartValue(QPointF(self.lable.x(), self.lable.y()))
    #     vals = [p / 100 for p in range(0, 101)]
    #     for i in vals:
    #         self.anim.setKeyValueAt(i, self.path.pointAtPercent(i))  # 设置100个关键帧
    #     self.anim.setEndValue(QPointF(self.lable.x() + disp, self.lable.y()))
    #     self.anim.start()
    #     #print(self.x(),self.y())



    # def Animation(self):
    #     if self.lable.x() <= -400-self.x():
    #         self.displacement(100)
    #     elif self.lable.x() >= 500-self.x():
    #         self.displacement(-100)
    #     else:
    #         direction = random.randint(0, 1)
    #         if direction == 0:
    #             self.displacement(100)
    #         if direction == 1:
    #             self.displacement(-100)


    #单击左键事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    #双击鼠标事件
    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            url = QUrl.fromLocalFile(self.character+"/"+self.character+"_Greeting.wav")
            content = QtMultimedia.QMediaContent(url)
            self.interactPlayer = QtMultimedia.QMediaPlayer()
            self.interactPlayer.setMedia(content)
            self.interactPlayer.play()
            # 播放Interact动作
            self.Play(3)
            # Interact结束后才播放Rest动作
            self.timer = QTimer()
            self.timer.timeout.connect(lambda:self.Play(self.cur))
            self.timer.start(self.timecon)

    #鼠标移动, 则宠物也移动
    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()

    #鼠标释放时, 取消绑定
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def delete(self):
        self.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('44.png'))
    major = FirstWindow()
    pet = SecondWindow()
    major.sendmsg.connect(pet.get)
    major.sendmsg1.connect(pet.getandadjust)
    major.btn1.clicked.connect(pet.initUI)
    major.btn1.clicked.connect(pet.handle_click)
    #major.btn2.clicked.connect(pet.delete)
    major.show()
    sys.exit(app.exec())





