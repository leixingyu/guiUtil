"""
An example showing how to sort table widget column with custom symbol

https://gist.github.com/leixingyu/0eea1cb8e325a8d52cc3a64953faf467#file-sorting-py
"""

import sys

from Qt import QtWidgets, QtCore


class SortTableWidgetItem(QtWidgets.QTableWidgetItem):
    def __init__(self, parent=None):
        QtWidgets.QTableWidgetItem.__init__(self, parent)

    def __lt__(self, other_item):
        """
        Override the less than operator
        """
        try:
            return int(self.text().split('-')[0]) < int(
                other_item.text().split('-')[0])
        except ValueError:
            return self.text() < other_item.text()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    test_widget = QtWidgets.QTableWidget()
    test_widget.insertColumn(0)

    test_strs = ["1", "2", "10", "11", "14-15", "120", "100-115", "59-62"]
    for index in range(len(test_strs)):
        test_widget.insertRow(index)
        value = test_strs[index]
        item = SortTableWidgetItem(value)
        test_widget.setItem(index, 0, item)

    test_widget.sortItems(0, QtCore.Qt.AscendingOrder)
    test_widget.show()
    sys.exit(app.exec_())
