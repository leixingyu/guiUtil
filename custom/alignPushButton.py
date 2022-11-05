"""
A custom QPushButton with left-aligned icon and center-aligned text
"""

from Qt import QtWidgets, QtCore, QtGui


class AlignPushButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(AlignPushButton, self).__init__(*args, **kwargs)
        self.pixmap = None

    def setPixmap(self, pixmap):
        self.pixmap = pixmap

    def sizeHint(self):
        parent_size = QtWidgets.QPushButton.sizeHint(self)
        return QtCore.QSize(
            parent_size.width() + self.pixmap.width(),
            max(parent_size.height(), self.pixmap.height())
        )

    def paintEvent(self, event):
        QtWidgets.QPushButton.paintEvent(self, event)

        pos_x = 5  # hardcoded horizontal margin
        pos_y = (self.height()-self.pixmap.height()) / 2

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        painter.drawPixmap(pos_x, pos_y, self.pixmap)


# Example

class TestUI(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(TestUI, self).__init__(parent)

        # initialization object
        layout = QtWidgets.QGridLayout()
        pb = AlignPushButton('test')

        path = r"xxx"
        pixmap = QtGui.QPixmap(path).scaled(
            40,
            40,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)
        pb.setPixmap(pixmap)

        layout.addWidget(pb)
        self.setLayout(layout)
