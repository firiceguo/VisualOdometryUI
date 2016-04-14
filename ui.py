# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VisualOdometry.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import os
import sys
import lk_track
# from numpy import asarray
# import numpy as np
# import PySide
# from PySide.QtGui import QImage
from PyQt4 import QtCore, QtGui
# from PyQt4.QtCore import QString
# from PIL import Image, ImageQt
import cv2


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_VisualOdometryUI(object):
    def setupUi(self, VisualOdometryUI):
        VisualOdometryUI.setObjectName(_fromUtf8("VisualOdometryUI"))
        VisualOdometryUI.setWindowModality(QtCore.Qt.NonModal)
        VisualOdometryUI.resize(724, 480)
        VisualOdometryUI.setAutoFillBackground(False)
        VisualOdometryUI.setStyleSheet(_fromUtf8("background-color: rgb(229, 229, 229);"))
        VisualOdometryUI.setSizeGripEnabled(False)
        VisualOdometryUI.setModal(False)
        self.graphicsView = QtGui.QLabel(VisualOdometryUI)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 501, 461))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.tracked_2 = QtGui.QLineEdit(VisualOdometryUI)
        self.tracked_2.setGeometry(QtCore.QRect(600, 40, 113, 20))
        self.tracked_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tracked_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tracked_2.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.tracked_2.setAutoFillBackground(False)
        self.tracked_2.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.tracked_2.setObjectName(_fromUtf8("tracked_2"))
        self.Features = QtGui.QLabel(VisualOdometryUI)
        self.Features.setGeometry(QtCore.QRect(520, 10, 71, 21))
        self.Features.setAutoFillBackground(False)
        self.Features.setFrameShape(QtGui.QFrame.NoFrame)
        self.Features.setFrameShadow(QtGui.QFrame.Plain)
        self.Features.setLineWidth(1)
        self.Features.setTextFormat(QtCore.Qt.RichText)
        self.Features.setScaledContents(False)
        self.Features.setWordWrap(False)
        self.Features.setObjectName(_fromUtf8("Features"))
        self.tracked = QtGui.QLabel(VisualOdometryUI)
        self.tracked.setGeometry(QtCore.QRect(520, 40, 51, 21))
        self.tracked.setFrameShape(QtGui.QFrame.NoFrame)
        self.tracked.setLineWidth(1)
        self.tracked.setTextFormat(QtCore.Qt.AutoText)
        self.tracked.setObjectName(_fromUtf8("tracked"))
        self.view = QtGui.QLabel(VisualOdometryUI)
        self.view.setGeometry(QtCore.QRect(520, 90, 71, 21))
        self.view.setAutoFillBackground(False)
        self.view.setFrameShape(QtGui.QFrame.NoFrame)
        self.view.setFrameShadow(QtGui.QFrame.Plain)
        self.view.setLineWidth(1)
        self.view.setTextFormat(QtCore.Qt.RichText)
        self.view.setScaledContents(False)
        self.view.setWordWrap(False)
        self.view.setObjectName(_fromUtf8("view"))
        self.frame_2 = QtGui.QLineEdit(VisualOdometryUI)
        self.frame_2.setGeometry(QtCore.QRect(600, 120, 113, 20))
        self.frame_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.frame_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.frame_2.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.frame_2.setAutoFillBackground(False)
        self.frame_2.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.frame = QtGui.QLabel(VisualOdometryUI)
        self.frame.setGeometry(QtCore.QRect(520, 120, 51, 21))
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setLineWidth(1)
        self.frame.setTextFormat(QtCore.Qt.AutoText)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.fps_2 = QtGui.QLineEdit(VisualOdometryUI)
        self.fps_2.setGeometry(QtCore.QRect(600, 150, 113, 20))
        self.fps_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.fps_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.fps_2.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.fps_2.setAutoFillBackground(False)
        self.fps_2.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.fps_2.setObjectName(_fromUtf8("fps_2"))
        self.fps = QtGui.QLabel(VisualOdometryUI)
        self.fps.setGeometry(QtCore.QRect(520, 150, 51, 21))
        self.fps.setFrameShape(QtGui.QFrame.NoFrame)
        self.fps.setLineWidth(1)
        self.fps.setTextFormat(QtCore.Qt.AutoText)
        self.fps.setObjectName(_fromUtf8("fps"))
        self.odometry = QtGui.QLabel(VisualOdometryUI)
        self.odometry.setGeometry(QtCore.QRect(520, 210, 71, 21))
        self.odometry.setAutoFillBackground(False)
        self.odometry.setFrameShape(QtGui.QFrame.NoFrame)
        self.odometry.setFrameShadow(QtGui.QFrame.Plain)
        self.odometry.setLineWidth(1)
        self.odometry.setTextFormat(QtCore.Qt.RichText)
        self.odometry.setScaledContents(False)
        self.odometry.setWordWrap(False)
        self.odometry.setObjectName(_fromUtf8("odometry"))
        self.location = QtGui.QLabel(VisualOdometryUI)
        self.location.setGeometry(QtCore.QRect(520, 250, 61, 21))
        self.location.setFrameShape(QtGui.QFrame.NoFrame)
        self.location.setLineWidth(1)
        self.location.setTextFormat(QtCore.Qt.AutoText)
        self.location.setObjectName(_fromUtf8("location"))
        self.location_2 = QtGui.QLineEdit(VisualOdometryUI)
        self.location_2.setGeometry(QtCore.QRect(600, 250, 113, 20))
        self.location_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.location_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.location_2.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.location_2.setAutoFillBackground(False)
        self.location_2.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.location_2.setObjectName(_fromUtf8("location_2"))
        self.heading = QtGui.QLabel(VisualOdometryUI)
        self.heading.setGeometry(QtCore.QRect(520, 280, 51, 21))
        self.heading.setFrameShape(QtGui.QFrame.NoFrame)
        self.heading.setLineWidth(1)
        self.heading.setTextFormat(QtCore.Qt.AutoText)
        self.heading.setObjectName(_fromUtf8("heading"))
        self.heading_2 = QtGui.QLineEdit(VisualOdometryUI)
        self.heading_2.setGeometry(QtCore.QRect(600, 280, 113, 20))
        self.heading_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.heading_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.heading_2.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.heading_2.setAutoFillBackground(False)
        self.heading_2.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.heading_2.setObjectName(_fromUtf8("heading_2"))
        self.pathlen = QtGui.QLabel(VisualOdometryUI)
        self.pathlen.setGeometry(QtCore.QRect(520, 310, 61, 21))
        self.pathlen.setFrameShape(QtGui.QFrame.NoFrame)
        self.pathlen.setLineWidth(1)
        self.pathlen.setTextFormat(QtCore.Qt.AutoText)
        self.pathlen.setObjectName(_fromUtf8("pathlen"))
        self.pathlen_2 = QtGui.QLineEdit(VisualOdometryUI)
        self.pathlen_2.setGeometry(QtCore.QRect(600, 310, 113, 20))
        self.pathlen_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.pathlen_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pathlen_2.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.pathlen_2.setAutoFillBackground(False)
        self.pathlen_2.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.pathlen_2.setObjectName(_fromUtf8("pathlen_2"))
        self.distance = QtGui.QLabel(VisualOdometryUI)
        self.distance.setGeometry(QtCore.QRect(520, 340, 131, 21))
        self.distance.setFrameShape(QtGui.QFrame.NoFrame)
        self.distance.setLineWidth(1)
        self.distance.setTextFormat(QtCore.Qt.AutoText)
        self.distance.setObjectName(_fromUtf8("distance"))
        self.distance_2 = QtGui.QLineEdit(VisualOdometryUI)
        self.distance_2.setGeometry(QtCore.QRect(600, 370, 113, 20))
        self.distance_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.distance_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.distance_2.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.distance_2.setAutoFillBackground(False)
        self.distance_2.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.distance_2.setObjectName(_fromUtf8("distance_2"))
        self.config = QtGui.QPushButton(VisualOdometryUI)
        self.config.setGeometry(QtCore.QRect(530, 410, 181, 23))
        self.config.setStyleSheet(_fromUtf8("background-color: rgb(191, 191, 191);"))
        self.config.setObjectName(_fromUtf8("config"))
        self.clear = QtGui.QPushButton(VisualOdometryUI)
        self.clear.setGeometry(QtCore.QRect(530, 440, 181, 23))
        self.clear.setStyleSheet(_fromUtf8("background-color: rgb(189, 189, 189);"))
        self.clear.setObjectName(_fromUtf8("clear"))

        self.retranslateUi(VisualOdometryUI)
        QtCore.QMetaObject.connectSlotsByName(VisualOdometryUI)

        self.connect(self.config, QtCore.SIGNAL('clicked()'), self.openconfig)

        self.thread = lk_track.TrackLK()
        self.thread._signal.connect(self.getimg)
        self.thread.start()

    def openconfig(self):
        os.system('notepad conf')

    def getimg(self, ch):
        try:
            path = QtGui.QPixmap(r'image.png')
            path.scaled(path.width(), path.height(), QtCore.Qt.KeepAspectRatio)
            self.graphicsView.setPixmap(path)
        except:
            pass
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            self.thread.stop()

    def retranslateUi(self, VisualOdometryUI):
        VisualOdometryUI.setWindowTitle(_translate("VisualOdometryUI", "VisualOdometryUI", None))
        self.Features.setText(
            _translate("VisualOdometryUI", "<html><head/><body><p><span style=\" font-size:12pt;\">Features</span></p></body></html>", None))
        self.tracked.setText(_translate("VisualOdometryUI", "Tracked：", None))
        self.view.setText(
            _translate("VisualOdometryUI", "<html><head/><body><p><span style=\" font-size:12pt;\">View</span></p></body></html>", None))
        self.frame.setText(_translate("VisualOdometryUI", "Frame：", None))
        self.fps.setText(_translate("VisualOdometryUI", "fps：", None))
        self.odometry.setText(
            _translate("VisualOdometryUI", "<html><head/><body><p><span style=\" font-size:12pt;\">Odometry</span></p></body></html>", None))
        self.location.setText(_translate("VisualOdometryUI", "Location：", None))
        self.heading.setText(_translate("VisualOdometryUI", "Heading：", None))
        self.pathlen.setText(_translate("VisualOdometryUI", "Path Len：", None))
        self.distance.setText(_translate("VisualOdometryUI", "Distance From Start：", None))
        self.config.setText(_translate("VisualOdometryUI", "Open Configure File", None))
        self.clear.setText(_translate("VisualOdometryUI", "Clear", None))
