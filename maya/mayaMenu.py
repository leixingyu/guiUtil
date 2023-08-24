from Qt import QtWidgets, QtGui, QtCore

from . import mayaWindowUtil


def add_menu(name):
    """
    Add an entry to the maya main menu

    :param name: menu name
    :return: QMenu
    """
    menu = QtWidgets.QMenu(name)
    menu.setObjectName(name)
    main_window = mayaWindowUtil.get_maya_main_window()
    main_window.menuBar().addMenu(menu)
    menu.setTearOffEnabled(True)
    return menu
