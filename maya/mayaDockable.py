"""
https://gist.github.com/leixingyu/8fb523cfd38b47c9cb1476b5c41eafd7#file-dockable-py
"""


from shiboken2 import wrapInstance
from builtins import int

import maya.cmds as cmds
import maya.mel as mel
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


def delete_instances():
    for ctrlName in [WIDGET_OBJECT_NAME, WORKSPACE_CTRL_NAME]:
        ctrl = OpenMayaUI.MQtUtil.findControl(ctrlName)
        if ctrl:
            widget = wrapInstance(int(ctrl), QtWidgets.QWidget)
            widget.close()
    try:
        cmds.deleteUI(WORKSPACE_CTRL_NAME)
    except:
        pass


def get_dockables():
    """
    Get all the UI element names in Maya that is dockable

    :return: dict. dockable UI element name mappings
    """
    dockables = {
        "CHANNEL_BOX": mel.eval('getUIComponentDockControl("Channel Box / Layer Editor", false)'),
        "ATTRIBUTE_EDITOR": mel.eval('getUIComponentDockControl("Attribute Editor", false)'),
        "TOOL_SETTINGS": mel.eval('getUIComponentDockControl("Tool Settings", false)'),
        "OUTLINER": mel.eval('getUIComponentDockControl("Outliner", false)'),

        "SHELF": mel.eval('getUIComponentToolBar("Shelf", false)'),
        "TIME_SLIDER": mel.eval('getUIComponentToolBar("Time Slider", false)'),
        "RANGE_SLIDER": mel.eval('getUIComponentToolBar("Range Slider", false)'),
        "COMMAND_LINE": mel.eval('getUIComponentToolBar("Command Line", false)'),
        "HELP_LINE": mel.eval('getUIComponentToolBar("Help Line", false)'),
        "TOOL_BOX": mel.eval('getUIComponentToolBar("Tool Box", false)'),

        "UV_EDITOR": "polyTexturePlacementPanel1Window",
        "UV_TOOLKIT": "UVToolkitDockControl"
    }
    return dockables


def show():
    delete_instances()
    global _DOCKWIDGET
    _DOCKWIDGET = DockableUI()
    _DOCKWIDGET.setObjectName(WIDGET_OBJECT_NAME)
    _DOCKWIDGET.show(dockable=True, dup=False)

    # this auto docks the widget
    cmds.workspaceControl(WORKSPACE_CTRL_NAME, e=True, dockToMainWindow=["right", 1], wp="preferred", retain=False)
