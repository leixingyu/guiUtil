import sys

from Qt import QtWidgets


def register_stylesheet(file):
    global APP
    APP = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    with open(file, 'r') as f:
        qss = f.read()
        APP.setStyleSheet(qss)
