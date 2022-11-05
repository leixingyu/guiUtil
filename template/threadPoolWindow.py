"""
A template for a tool window with multiple threading capability

https://gist.github.com/leixingyu/f5fc3cc1ef03db1f254dab2a23b85bc7#file-qtheadpool-py
"""


import random
import sys
from time import sleep

from Qt import QtWidgets, QtCore, QtGui


class RunnerSignals(QtCore.QObject):
    progressed = QtCore.Signal(int)
    messaged = QtCore.Signal(str)


class Runner(QtCore.QRunnable):
    def __init__(self):
        super(Runner, self).__init__()
        self.signals = RunnerSignals()

    def run(self):
        for i in range(1, 11):
            self.signals.progressed.emit(int(i*10))
            self.signals.messaged.emit(str(i))
            sleep(random.uniform(0.3, 0.7))


class ThreadPoolWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.__pool = QtCore.QThreadPool()
        self.__pool.setMaxThreadCount(3)

        # ui setup: please ignore
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()

        button = QtWidgets.QPushButton('run task!')
        button.clicked.connect(self.run_long_task)
        edit = QtWidgets.QLineEdit()
        self.ui_progress_1 = QtWidgets.QProgressBar()
        self.ui_progress_2 = QtWidgets.QProgressBar()
        self.ui_progress_3 = QtWidgets.QProgressBar()

        layout.addWidget(edit, 0, 0)
        layout.addWidget(self.ui_progress_1, 1, 0)
        layout.addWidget(self.ui_progress_2, 2, 0)
        layout.addWidget(self.ui_progress_3, 3, 0)
        layout.addWidget(button, 4, 0)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def run_long_task(self):
        worker_1 = Runner()
        worker_1.signals.progressed.connect(
            lambda value: update_progress(self.ui_progress_1, value))

        worker_2 = Runner()
        worker_2.signals.progressed.connect(
            lambda value: update_progress(self.ui_progress_2, value))

        worker_3 = Runner()
        worker_3.signals.progressed.connect(
            lambda value: update_progress(self.ui_progress_3, value))

        # QThreadPool deletes the QRunnable automatically by default
        self.__pool.start(worker_1)
        self.__pool.start(worker_2)
        self.__pool.start(worker_3)


def update_progress(progress_bar, value):
    progress_bar.setValue(value)

    if value >= 100:
        progress_bar.setVisible(False)
    elif progress_bar.isHidden():
        progress_bar.setVisible(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ThreadPoolWindow()
    win.show()
    sys.exit(app.exec_())
