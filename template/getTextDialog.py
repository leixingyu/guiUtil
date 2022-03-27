from Qt import QtWidgets, QtCore, QtGui


class GetTextDialog(QtWidgets.QDialog):
    """
    Custom pop-up dialog for entering a short text
    """

    def __init__(self, text='', title=''):
        """
        Initializing the dialog ui elements and connect signals

        :param text: str. pre-displayed text
        :param title: str. dialog title
        """
        super(GetTextDialog, self).__init__()

        self.setWindowTitle(title)
        self.ui_text_edit = QtWidgets.QLineEdit(text)
        self.ui_accept_btn = QtWidgets.QPushButton("Confirm")

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.ui_text_edit, 0, 0)
        layout.addWidget(self.ui_accept_btn, 0, 1)

        self.setLayout(layout)
        self.ui_accept_btn.clicked.connect(self.on_click_accept)

    def closeEvent(self):
        """
        Overwrite the close event as it handles accept by default
        """
        self.close()

    def on_click_accept(self):
        """
        Trigger accept event when clicking the confirm button
        """
        self.accept()

    def get_text(self):
        """
        Get the text from text edit field

        :return: str. text from text edit field
        """
        return self.ui_text_edit.text()
