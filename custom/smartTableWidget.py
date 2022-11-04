"""
Smart auto resize table
"""

import sys

from Qt import QtWidgets, QtCore, QtGui


class SmartTableWidget(QtWidgets.QTableWidget):

    def __init__(self, parent=None):
        """
        Initialization
        Vertical header (no. column) is removed for visual purpose
        """
        super(SmartTableWidget, self).__init__(parent)
        self.min_width = 0
        self.verticalHeader().setVisible(False)

    def setHorizontalHeaderLabels(self, *args, **kwargs):
        """
        Override. determine the minimum table width based on header
        """
        super(SmartTableWidget, self).setHorizontalHeaderLabels(*args, **kwargs)

        header = self.horizontalHeader()
        for i in range(self.columnCount()):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
            min_size = header.sectionSize(i) + 5
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Interactive)
            self.min_width += min_size

    def sizeHint(self):
        """
        Override.
        """
        return QtCore.QSize(500, -1)

    def resizeEvent(self, event):
        """
        Override. whenever the table gets resized, we check whether the width
        exceeds the minimum width; if so, we add scroll bar and retain each
        header to the minimum width, if not, we stretch each header
        """
        super(SmartTableWidget, self).resizeEvent(event)

        if not self.columnCount():
            return

        # needs to stretch
        if self.min_width < self.width():
            self.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)

            width_remain = self.width() % self.columnCount()
            for i in range(self.columnCount()):
                if width_remain > 0:
                    self.setColumnWidth(i, int(self.width() / self.columnCount())+1)
                    width_remain -= 1
                else:
                    self.setColumnWidth(i, int(self.width() / self.columnCount()))

        # retain minimum size
        else:
            header = self.horizontalHeader()
            self.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOn)
            for i in range(self.columnCount()):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Interactive)


if __name__ == "__main__":
    """
    Example
    """
    app = QtWidgets.QApplication(sys.argv)

    table = SmartTableWidget()
    table.setColumnCount(5)
    table.setHorizontalHeaderLabels(
        ['apple', 'orange', 'banana', 'strawberry', 'pineapple'])

    table.show()
    sys.exit(app.exec_())
