#!/usr/bin/env python

import PyQt5.QtCore as QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
        QMenu, QPushButton, QRadioButton, QBoxLayout, QWidget,QSlider,QLabel,QDoubleSpinBox,QHBoxLayout)


class MySlider(QGroupBox):

    valueChanged = QtCore.pyqtSignal(int)

    def __init__(self, title, parent=None):
        super(MySlider, self).__init__(title, parent)

        self.slider = QSlider(QtCore.Qt.Horizontal)
        self.slider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setTickInterval(10)
        self.slider.setSingleStep(1)
        self.slider.valueChanged[int].connect(self.valueChanged)

        slidersLayout = QBoxLayout(QBoxLayout.TopToBottom)
        slidersLayout.addWidget(self.slider)
        self.setLayout(slidersLayout)    

    def setValue(self, value):    
        self.slider.setValue(value)    

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.sliderGroup = QGroupBox()
        self.sigmaGain = 10.0
        self.sigmaSlider = MySlider("Spatial filter sigma:")
        self.tauGain = 100.0
        self.tauSlider = MySlider("Temporal filter factor:")
        self.deltaGain = 100.0
        self.deltaSlider = MySlider("Delta log(I) threshold:")

        sliderLayout = QBoxLayout(QBoxLayout.TopToBottom)
        sliderLayout.addWidget(self.sigmaSlider)
        sliderLayout.addWidget(self.tauSlider)
        sliderLayout.addWidget(self.deltaSlider)
        self.sliderGroup.setLayout(sliderLayout)
        self.createControls()

        self.sigmaSlider.valueChanged[int].connect(self.updateSSpinBox)
        self.sigmaSpinBox.valueChanged[float].connect(self.updateSSlider)
        self.tauSlider.valueChanged[int].connect(self.updateTSpinBox)
        self.tauSpinBox.valueChanged[float].connect(self.updateTSlider)
        self.deltaSlider.valueChanged[int].connect(self.updateDSpinBox)
        self.deltaSpinBox.valueChanged[float].connect(self.updateDSlider)

        layout = QHBoxLayout()
        layout.addWidget(self.controlsGroup)
        layout.addWidget(self.sliderGroup)
        self.setLayout(layout)

        self.sigmaSpinBox.setValue(0)
        self.tauSpinBox.setValue(0)
        self.deltaSpinBox.setValue(0.3)

        self.setWindowTitle("Camera Control")

    def updateSSlider(self, value):
        self.sigmaSlider.setValue(value*self.sigmaGain)
    
    def updateSSpinBox(self, value):
        self.sigmaSpinBox.setValue(value/self.sigmaGain)
    
    def updateTSlider(self, value):
        self.tauSlider.setValue(value*self.tauGain)
    
    def updateTSpinBox(self, value):
        self.tauSpinBox.setValue(value/self.tauGain)
    
    def updateDSlider(self, value):
        self.deltaSlider.setValue(value*self.deltaGain)
    
    def updateDSpinBox(self, value):
        self.deltaSpinBox.setValue(value/self.deltaGain)
    
    def createControls(self):
        self.controlsGroup = QGroupBox()

        sigmaLabel = QLabel("Sigma:")
        self.sigmaSpinBox = QDoubleSpinBox()
        self.sigmaSpinBox.setRange(0, 100/self.sigmaGain)
        self.sigmaSpinBox.setSingleStep(1/self.sigmaGain)

        tauLabel = QLabel("Tau:")
        self.tauSpinBox = QDoubleSpinBox()
        self.tauSpinBox.setRange(0, 100/self.tauGain)
        self.tauSpinBox.setSingleStep(1/self.tauGain)

        deltaLabel = QLabel("Delta:")
        self.deltaSpinBox = QDoubleSpinBox()
        self.deltaSpinBox.setRange(0, 100/self.deltaGain)
        self.deltaSpinBox.setSingleStep(1/self.deltaGain)

        controlsLayout = QGridLayout()
        controlsLayout.addWidget(sigmaLabel, 0, 0)
        controlsLayout.addWidget(self.sigmaSpinBox, 0, 1)
        controlsLayout.addWidget(tauLabel, 1, 0)
        controlsLayout.addWidget(self.tauSpinBox, 1, 1)
        controlsLayout.addWidget(deltaLabel, 2, 0)
        controlsLayout.addWidget(self.deltaSpinBox, 2, 1)
        self.controlsGroup.setLayout(controlsLayout)


if __name__ == '__main__':

    from sys import argv, exit
    import cv2 as cv2
    from numpy import size, uint8, zeros, save
    from time import time

    height = 260
    width = 346
    savevid = True
    datapath = "./videos/"

    app = QApplication(argv)
    desktop = QApplication.desktop()
                
    # initialise the video capture
    video_src = 'moving_pattern_for_sampling.avi'                       # inbuilt camera
    cam = cv2.VideoCapture(video_src)   # activate the camera
    ret, img = cam.read()               # get one default frame
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    native_width = size(img,1)          # get native frame width
    native_height = size(img,0)         # get native frame height
    ret = cam.set(3,width)              # set frame height            
    ret = cam.set(4,height)             # set frame width
    ret, img = cam.read()               # get one frame of set size
    
    # calculate first background frame
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bg = cv2.flip(img,1).astype('float64')
    bg = cv2.log(cv2.add(bg,1))
    bgra = zeros([height, width, 3], dtype=uint8)

    # initialise the windows and their positions
    cv2.namedWindow("Event Based Camera | q: quit", 1)
    cv2.moveWindow("Event Based Camera | q: quit", int((desktop.width()-width)/2), 0) 
    window = Window()
    window.setGeometry((desktop.width()-width)/2, height+70, 640, 100)
    window.show()
    
    frame = 0
    last_t = time()
    while True:
        # get a frame
        ret, img = cam.read()
        # calculate frame rate
        t = time()
        rate = 1.0/(t-last_t)
        last_t = t
        # make image greyscale
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # flip it so it behaves like a mirror
        img = cv2.flip(img,1).astype('float64')
        # logarithmic compression (log(1.0 + I))
        img = cv2.log(cv2.add(img,1))
        # calculate difference with background
        dif = cv2.subtract(img, bg)
        # detect on and off events
        on = cv2.compare(dif, window.deltaSpinBox.value(), cv2.CMP_GT)
        off = cv2.compare(-1.0*dif, window.deltaSpinBox.value(), cv2.CMP_GT)      
        if savevid:
            save(datapath + "on%03d.npy"%frame, on)
            save(datapath + "off%03d.npy"%frame, off)
            frame += 1
        # spatial filter image
        bgnew = cv2.GaussianBlur(img, (0,0), window.sigmaSpinBox.value()+0.00001)
        # update background via temporal LPF
        cLPF = window.tauSpinBox.value()
        bg = cv2.add(cLPF*bg, (1-cLPF)*bgnew)
        # create image
        bgra[:, :, 0] = off
        bgra[:, :, 1] = on
        bgra[:, :, 2] = on
        cv2.putText(bgra,"FPS = %f"%rate, (10,height-10), cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255))
        cv2.imshow("Event Based Camera | q: quit", bgra)
    
        # monitor the keyboard
        c = cv2.waitKey(10) % 0x100            
        # for 'q', quit
        if c == ord("q"):
            break
    
    # clean up for exit
    cam.release()    
    cv2.destroyAllWindows()
    window.destroy()
    app.exit()
