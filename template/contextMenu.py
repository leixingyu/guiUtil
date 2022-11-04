"""
Template for right-click context menu in widget

https://gist.github.com/leixingyu/74a242d46e06887cc1df426c417541c4#file-contextmenu-py
"""

from Qt import QtWidgets, QtGui, QtCore


class ContextMenuWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ContextMenuWidget, self).__init__(parent)

        # initialization object
        layout = QtWidgets.QGridLayout()
        self.widget = QtWidgets.QListWidget()

        layout.addWidget(self.widget)
        self.setLayout(layout)

        self.widget.addItem('item A')
        self.widget.addItem('item B')

        self.widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.widget.customContextMenuRequested.connect(self.openContextMenu)

        self.widget.itemClicked.connect(lambda item: self.printThings(item))

    def openContextMenu(self):
        context_menu = QtWidgets.QMenu()
        selected_indexes = list(
            set([item.row() for item in self.widget.selectedIndexes()])
        )

        # single selection action
        if len(selected_indexes) == 1:
            item = self.widget.currentItem()

            function_action = context_menu.addAction('Menu Text go here')
            function_action.triggered.connect(lambda: self.example_func(item))

            # sub-menu
            function_menu = context_menu.addMenu('More options here!')
            submenu = function_menu.addAction('Sub Menu here')
            submenu.triggered.connect(lambda: self.example_func(item))

        # multi selection action
        else:
            items = self.widget.selectedItems()

        # all other action
        other_action = context_menu.addAction('Menu Text go here')
        other_action.triggered.connect(self.example_func2)

        cursor = QtGui.QCursor()
        context_menu.exec_(cursor.pos())

    def example_func(self, argument):
        pass

    def example_func2(self):
        pass
