from shiboken2 import wrapInstance
from builtins import int

from maya.api import OpenMayaUI
from Qt import QtWidgets


def get_maya_main_window():
    """
    Get maya's window instance

    :return: window instance, maya program window
    """
    main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)


def set_window_pos(child_only=0, x=0, y=0):
    """
    Set window position of maya's widgets

    :param child_only: bool. option to set position only for widgets parented
    to maya main window
    :param x: int. window x position
    :param y: int. window y position
    """
    for child in get_maya_main_window().children():
        if isinstance(child, QtWidgets.QWidget) and child.isWindow():
            # set visible
            if child.isHidden():
                child.setVisible(1)
            child.move(x, y)

    if not child_only:
        tops = QtWidgets.QApplication.topLevelWidgets()
        for top in tops:
            if top.isWindow() and not top.isHidden():
                if top.windowTitle() == get_maya_main_window().windowTitle():
                    continue
                top.move(x, y)


def get_maya_window_titles():
    """
    A C-like function to find maya window titles in Windows

    :return: {int: str}. a dictionary mapping of the process id of Maya as key
                         and window title as value.
    """
    import ctypes

    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(
        ctypes.c_bool,
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int)
    )
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    GetWindowProcessId = ctypes.windll.user32.GetWindowThreadProcessId
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible

    win_mapping = dict()

    def find_maya_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            # window name
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length+1)
            GetWindowText(hwnd, buff, length+1)

            if 'Autodesk Maya' in buff.value:
                # pid
                pid = ctypes.wintypes.DWORD()
                GetWindowProcessId(hwnd, ctypes.byref(pid))
                win_mapping[int(pid.value)] = buff.value
        return True

    # query the window title
    EnumWindows(EnumWindowsProc(find_maya_window), 0)
    return win_mapping.items()
