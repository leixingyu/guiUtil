"""
https://gist.github.com/leixingyu/83358dedd008f6a51e7f7b2b14d2fb34#file-dock-py
"""


from builtins import int
from shiboken2 import wrapInstance

from maya import cmds, OpenMayaUI as omui
from Qt import QtWidgets, QtCore


def Dock(Widget, show=True):
    name = Widget.__class__.__name__
    label = getattr(Widget, "label", name)

    try:
        cmds.deleteUI(name)
    except RuntimeError:
        pass

    dockControl = cmds.workspaceControl(
        name,
        tabToControl=["AttributeEditor", -1],
        widthProperty="preferred",
        label=label
    )

    dockPtr = omui.MQtUtil.findControl(dockControl)
    dockWidget = wrapInstance(int(dockPtr), QtWidgets.QWidget)
    dockWidget.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    child = Widget(dockWidget)
    dockWidget.layout().addWidget(child)

    if show:
        cmds.evalDeferred(
            lambda *args: cmds.workspaceControl(
                dockControl,
                edit=True,
                restore=True
            )
        )

    return child


class Example(QtWidgets.QWidget):
    label = "My example"

    def __init__(self, parent=None):
        super(Example, self).__init__(parent)
        self.setWindowTitle(self.label)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)

        label = QtWidgets.QLabel("Hello World!")
        layout.addWidget(label)


if __name__ == '__main__':
    example = Dock(Example)
