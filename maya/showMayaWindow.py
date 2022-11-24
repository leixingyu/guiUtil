import maya.cmds as cmds


def show_unique():
    if cmds.window('xxx', q=1, exists=1):
        cmds.deleteUI('xxx')

    global WIN
    WIN = TestWindow()
    WIN.setObjectName('xxx')
    WIN.show()


def show():
    win = TestWindow()
    win.show()
    return win
