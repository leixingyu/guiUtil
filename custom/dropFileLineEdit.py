"""
Drag and drop a file to a line edit to show its full path

reference: https://stackoverflow.com/questions/11872141/drag-a-file-into-qtgui-qlineedit-to-set-url-text/24944690#24944690
"""


import sys


from Qt import QtWidgets


class DropFileLineEdit(QtWidgets.QLineEdit):
    def __init__(self, auto_inject=True):

        super().__init__()
        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            # for some reason, this doubles up the intro slash
            filepath = str(urls[0].path())[1:]
            self.setText(filepath)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = DropFileLineEdit()
    window.show()
    sys.exit(app.exec_())
