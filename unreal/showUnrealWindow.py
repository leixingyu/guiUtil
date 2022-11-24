import sys

import unreal

from Qt import QtWidgets


def show():
    global APP
    global WIN

    APP = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    WIN = TestWindow()
    WIN.show()  # this needs to happen before parenting
    unreal.parent_external_window_to_slate(int(WIN.winId()))


def show_unique():
    global APP
    global WIN

    APP = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    # handles existing instance
    exists = WIN is not None
    if not exists:
        WIN = TestWindow()
    WIN.show()
    unreal.parent_external_window_to_slate(int(WIN.winId()))

    return WIN
