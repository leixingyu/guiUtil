from Qt import QtWidgets, QtGui, QtCore


QUESTION = 0
INFO = 1
WARNING = 2
ERROR = 3


def pick_color(qcolor=None):
    """
    Prompt user to pick a color

    :param qcolor: QtGui.QColor. pre-selected color
    :return: QtGui.QColor. user selected color
    """
    if not qcolor:
        qcolor = QtGui.QColor(0, 0, 0)

    return QtWidgets.QColorDialog.getColor(qcolor)


def get_path_export(title='Export', default_path='C:/', typ='*'):
    """
    Get directory/folder full path for export

    :param title: str. export window title, defaults to 'Export'
    :param default_path: str. default path opened in the window
    :param typ: str. file filter pattern
    :return: str. export folder full path
    """
    path = QtWidgets.QFileDialog.getSaveFileName(
        None,
        title,
        default_path,
        filter=typ)[0]
    return path


def get_path_import(title='Import', default_path='C:/', typ='*'):
    """
    Get file full path for export

    :param title: str. import window title, defaults to 'Import'
    :param default_path: str. default path opened in the window
    :param typ: str. file filter pattern
    :return: str. import file full path
    """
    path = QtWidgets.QFileDialog.getOpenFileName(
        None,
        title,
        default_path,
        filter=typ)[0]
    return path


def message(msg, typ=ERROR, title=''):
    """
    Activate a message box prompt with one confirm button

    :param msg: str. custom message
    :param typ: str ('error' or 'info'). type of the log
    :param title: str. message box title
    :return: widget instance
    """
    if typ == ERROR:
        icon = QtWidgets.QMessageBox.Critical
    elif typ == INFO:
        icon = QtWidgets.QMessageBox.Information
    elif typ == WARNING:
        icon = QtWidgets.QMessageBox.Warning
    elif typ == QUESTION:
        icon = QtWidgets.QMessageBox.Question
    else:
        icon = QtWidgets.QMessageBox.NoIcon

    msg_box = QtWidgets.QMessageBox()

    msg_box.setIcon(icon)
    msg_box.setWindowTitle(title)
    msg_box.setText(msg)

    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    return msg_box.exec_()


def yes_no(msg, title=''):
    """
    Raise a message box prompt for user to choose

    :param msg: str. custom message
    :param title: str. message box title
    :return: QtWidgets.QMessageBox.Yes or No. user's choice
    """
    msg_box = QtWidgets.QMessageBox()

    msg_box.setIcon(QtWidgets.QMessageBox.Question)
    msg_box.setWindowTitle(title)
    msg_box.setText(msg)

    msg_box.setStandardButtons(
        QtWidgets.QMessageBox.Yes |
        QtWidgets.QMessageBox.No
    )
    user_choice = msg_box.exec_()
    return user_choice
