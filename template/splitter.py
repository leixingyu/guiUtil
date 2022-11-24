import sys

from Qt import QtWidgets, QtCore


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # initialization object
        splitter = QtWidgets.QSplitter()
        splitter.setHandleWidth(10)
        splitter.setOrientation(QtCore.Qt.Vertical)

        # set
        self.setCentralWidget(splitter)

        listview = QtWidgets.QListView()
        tableview = QtWidgets.QTableWidget()

        splitter.addWidget(listview)
        splitter.addWidget(tableview)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
