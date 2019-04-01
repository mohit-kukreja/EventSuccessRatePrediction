#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PyQt4.QtCore import pyqtSlot


def window():
# Create an PyQT4 application object.
    app = QApplication(sys.argv)

    # The QWidget widget is the base class of all user interface objects in PyQt4.
    w = QWidget()

    # Set window size.
    w.resize(3200, 2400)

    # Set window title
    textbox_eventName = QLineEdit(w)
    textbox_eventName.move(20, 40)
    textbox_eventName.resize(280, 40)

    textbox_Technology = QLineEdit(w)
    textbox_Technology.move(20, 100)
    textbox_Technology.resize(280, 40)

    textbox_Location = QLineEdit(w)
    textbox_Location.move(20, 160)
    textbox_Location.resize(280, 40)

    button = QPushButton('get event success', w)
    button.move(20, 220)
    button.clicked.connect(button_clicked())

    w.setWindowTitle("Event Success Rate prediction")
    w.show()
    sys.exit(app.exec_())



def button_clicked():
    print "button clicked"

if __name__ == '__main__':
   window()



