import logging

from Qt import QtWidgets, QtGui


logger = logging.getLogger(__name__)


class EditTextDialog(QtWidgets.QDialog):
    """
    Custom pop-up dialog for editing text purpose, or getting long text input
    """

    def __init__(self, text='', title=''):
        """
        Initializing the dialog ui elements and connect signals

        :param text: str. pre-displayed text
        :param title: str. dialog title
        """
        super(EditTextDialog, self).__init__()

        self.setWindowTitle(title)
        self.ui_text_edit = QtWidgets.QPlainTextEdit(text)
        self.ui_text_edit.setTabStopWidth(self.ui_text_edit.fontMetrics().width(' ') * 4)
        self.ui_accept_button = QtWidgets.QPushButton("Confirm")

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.ui_text_edit, 0, 0)
        layout.addWidget(self.ui_accept_button, 1, 0)

        self.setLayout(layout)
        self.ui_accept_button.clicked.connect(self.on_click_accept)

    def closeEvent(self, event):
        """
        Overwrite the close event as it handles accept by default
        """
        self.close()

    def on_click_accept(self):
        """
        Trigger accept event when clicking the confirm button
        """
        if self.ui_text_edit.toPlainText():
            self.accept()
        else:
            logger.error('value cannot be empty')

    def get_text(self):
        """
        Get the text from text edit field

        :return: str. text from text edit field
        """
        return self.ui_text_edit.toPlainText()
