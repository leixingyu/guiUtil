from Qt import QtWidgets, QtGui, QtCore


class CustomTreeItemWidget(QtWidgets.QTreeWidgetItem):
    """
    A custom widget that can be embedded in QTreeWidget as QTreeWidgetItem
    """

    def __init__(self, *args, **kwargs):
        super(CustomTreeItemWidget, self).__init__()

        # create custom layout and sub-widgets
        self.widget = QtWidgets.QWidget()

        """
        # example
        self.widget.layout = QtWidgets.QHBoxLayout(self.widget)
        
        self.ui_combo_box = QtWidgets.QCheckBox()
        self.ui_name_label = QtWidgets.QLabel()

        self.widget.layout.addWidget(self.ui_combo_box)
        self.widget.layout.addWidget(self.ui_name_label)
        """

    def add_to_widget(self, parent):
        """
        Add the tree widget item to the tree widget

        :param parent: QtWidgets.QTreeWidget. parent tree widget
        """
        self.widget.setParent(parent)
        parent.addTopLevelItem(self)
        parent.setItemWidget(self, 0, self.widget)
