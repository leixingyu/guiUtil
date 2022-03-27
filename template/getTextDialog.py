from Qt import QtWidgets, QtCore, QtGui


class GetTextDialog(QtWidgets.QDialog):
    def __init__(self):
        super(GetTextDialog, self).__init__()

        self.ui_text_edit = QtWidgets.QLineEdit()
        self.ui_accept_btn = QtWidgets.QPushButton("Confirm")

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.ui_text_edit, 0, 0)
        layout.addWidget(self.ui_accept_btn, 0, 1)

        self.setLayout(layout)
        self.ui_accept_btn.clicked.connect(self.on_click_accept)

    def closeEvent(self):
        self.close()

    def on_click_accept(self):
        self.accept()

    def get_text(self):
        return self.ui_text_edit.text()
