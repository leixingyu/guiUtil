"""
A template for a tool window with threading capability

https://gist.github.com/leixingyu/9601e352eba22124a0f97e1fc574a262#file-qthreading-py
"""


import sys
from time import sleep

from Qt import QtWidgets, QtCore, QtGui


class Worker(QtCore.QObject):
    progressed = QtCore.Signal(int)
    messaged = QtCore.Signal(str)
    finished = QtCore.Signal()

    def run(self):
        for i in range(1, 11):
            self.progressed.emit(int(i*10))
            self.messaged.emit(str(i))
            sleep(0.5)

        self.finished.emit()


class ThreadWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.__thread = QtCore.QThread()

        # ui setup: please ignore
        self.ui_progress = QtWidgets.QProgressBar()
        self.statusBar().addPermanentWidget(self.ui_progress)

        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()
        button = QtWidgets.QPushButton('run task!')
        button.clicked.connect(self.run_long_task)
        edit = QtWidgets.QLineEdit()

        layout.addWidget(edit, 0, 0)
        layout.addWidget(button, 1, 0)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def run_long_task(self):
        if not self.__thread.isRunning():
            self.__thread = self.__get_thread()
            self.__thread.start()

    def __get_thread(self):
        thread = QtCore.QThread()
        worker = Worker()
        worker.moveToThread(thread)

        # this is essential when worker is in local scope!
        thread.worker = worker

        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)

        worker.progressed.connect(lambda value: update_progress(
            self.ui_progress, value))
        worker.messaged.connect(lambda msg: update_status(
            self.statusBar(), msg))

        return thread


def update_status(status_bar, msg):
    status_bar.showMessage(msg, 2000)


def update_progress(progress_bar, value):
    progress_bar.setValue(value)

    if value >= 100:
        progress_bar.setVisible(False)
    elif progress_bar.isHidden():
        progress_bar.setVisible(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ThreadWindow()
    win.show()
    sys.exit(app.exec_())
