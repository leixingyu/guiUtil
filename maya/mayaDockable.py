"""
https://gist.github.com/leixingyu/8fb523cfd38b47c9cb1476b5c41eafd7#file-dockable-py
"""


from shiboken2 import wrapInstance
from builtins import int

import maya.cmds as cmds
from maya.api import OpenMayaUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from Qt import QtCore, QtGui, QtWidgets
from Qt import _loadUi


UI_PATH = ''
WORKSPACE_CTRL_NAME = 'CustomWidgetWorkspaceControl'
WIDGET_OBJECT_NAME = 'CustomWidget'


class DockableUI(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(DockableUI, self).__init__(parent)
        _loadUi(UI_PATH, self)


def deleteInstances():
    for ctrlName in [WIDGET_OBJECT_NAME, WORKSPACE_CTRL_NAME]:
        ctrl = OpenMayaUI.MQtUtil.findControl(ctrlName)
        if ctrl:
            widget = wrapInstance(int(ctrl), QtWidgets.QWidget)
            widget.close()
    try:
        cmds.deleteUI(WORKSPACE_CTRL_NAME)
    except:
        pass


def show():
    deleteInstances()
    global _DOCKWIDGET
    _DOCKWIDGET = DockableUI()
    _DOCKWIDGET.setObjectName(WIDGET_OBJECT_NAME)
    _DOCKWIDGET.show(dockable=True, dup=False)

    # this auto docks the widget
    cmds.workspaceControl(WORKSPACE_CTRL_NAME, e=True, dockToMainWindow=["right", 1], wp="preferred", retain=False)
