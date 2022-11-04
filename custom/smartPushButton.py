"""
An extension to QPushButton that is able to detect different click events
including left-click, right-click and double-click
"""

from Qt import QtWidgets, QtCore


class SmartPushButton(QtWidgets.QPushButton):
    right_clicked = QtCore.Signal()
    left_clicked = QtCore.Signal()
    double_clicked = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(SmartPushButton, self).__init__(*args, **kwargs)

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.timeout)

        self.is_double = False
        self.is_left_click = True

        self.installEventFilter(self)

        self.double_clicked.connect(self.double_click_event)
        self.left_clicked.connect(self.left_click_event)
        self.right_clicked.connect(self.right_click_event)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if not self.timer.isActive():
                self.timer.start()

            self.is_left_click = False
            if event.button() == QtCore.Qt.LeftButton:
                self.is_left_click = True

            return True

        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            self.is_double = True
            return True

        return False

    def timeout(self):
        if self.is_double:
            self.double_clicked.emit()
        else:
            if self.is_left_click:
                self.left_clicked.emit()
            else:
                self.right_clicked.emit()

        self.is_double = False

    def left_click_event(self):
        print('left clicked')

    def right_click_event(self):
        print('right clicked')

    def double_click_event(self):
        print('double clicked')
