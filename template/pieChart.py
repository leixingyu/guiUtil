"""
Template for drawing Pie Charts in Qt Application
"""


import sys
from collections import namedtuple

from PyQt5 import QtCore, QtWidgets, QtGui, QtChart


Data = namedtuple('Data', ['name', 'value', 'color'])


class SimpleChart(QtChart.QChart):
    """
    A bare minimum implementation of pie chart in Qt
    """

    def __init__(self, parent=None):
        """
        Initialization with layout and population
        """
        super(SimpleChart, self).__init__(parent)
        offset = 140

        self.legend().setAlignment(QtCore.Qt.AlignRight)
        self.legend().setMarkerShape(QtChart.QLegend.MarkerShapeCircle)

        self.__series = QtChart.QPieSeries()
        self.__series.setPieStartAngle(offset)
        self.__series.setPieEndAngle(offset+360)
        self.addSeries(self.__series)

    def clear(self):
        """
        Clear all slices in the pie chart
        """
        for slice_ in self.__series.slices():
            self.__series.take(slice_)

    def add_slice(self, name, value, color):
        """
        Add one slice to the pie chart

        :param name: str. name of the slice
        :param value: value. value of the slice (contribute to how much the
                      slice would span in angle)
        :param color: str. hex code for slice color
        """
        slice_ = QtChart.QPieSlice(name, value)
        slice_.setColor(QtGui.QColor(color))
        slice_.setLabelBrush(QtGui.QColor(color))
        slice_.percentageChanged.connect(lambda: self.__update_label(slice_, name))

        self.__series.append(slice_)

    @staticmethod
    def __update_label(slice_, title):
        """
        Update the label of a slice

        :param slice_: QPieSlice. the slice the label is applied
        :param title: str. title of the label
        """
        label = "<p align='center' style='color:black'>{} {}%</p>".format(
            title,
            round(slice_.percentage() * 100, 2))
        slice_.setLabel(label)
        slice_.setLabelArmLengthFactor(0.3)
        if slice_.percentage() > 0.03:
            slice_.setLabelVisible()


class SmartChart(QtChart.QChart):
    """
    A slightly smarter implementation of pie chart in Qt, with
    double looped pie chart layout design and hover animation.
    """

    def __init__(self, parent=None):
        """
        Initialization with layout and population
        """
        super(SmartChart, self).__init__(parent)
        offset = 140

        self.setMargins(QtCore.QMargins(0, 0, 0, 0))
        self.legend().hide()
        self.setAnimationOptions(QtChart.QChart.SeriesAnimations)

        self.__outer = QtChart.QPieSeries()
        self.__inner = QtChart.QPieSeries()
        self.__outer.setHoleSize(0.35)
        self.__outer.setPieStartAngle(offset)
        self.__outer.setPieEndAngle(offset+360)
        self.__inner.setPieSize(0.35)
        self.__inner.setHoleSize(0.3)
        self.__inner.setPieStartAngle(offset)
        self.__inner.setPieEndAngle(offset+360)

        self.addSeries(self.__outer)
        self.addSeries(self.__inner)

    def clear(self):
        """
        Clear all slices in the pie chart
        """
        for slice_ in self.__outer.slices():
            self.__outer.take(slice_)

        for slice_ in self.__inner.slices():
            self.__inner.take(slice_)

    def add_slice(self, name, value, color):
        """
        Add one slice to the pie chart

        :param name: str. name of the slice
        :param value: value. value of the slice (contribute to how much the
                      slice would span in angle)
        :param color: str. hex code for slice color
        """
        # outer
        outer_slice = QtChart.QPieSlice(name, value)
        outer_slice.setColor(QtGui.QColor(color))
        outer_slice.setLabelBrush(QtGui.QColor(color))

        outer_slice.hovered.connect(lambda is_hovered: self.__explode(outer_slice, is_hovered))
        outer_slice.percentageChanged.connect(lambda: self.__update_label(outer_slice, name))

        self.__outer.append(outer_slice)

        # inner
        inner_color = self.__get_secondary_color(color)
        inner_slice = QtChart.QPieSlice(name, value)
        self.__inner.append(inner_slice)
        inner_slice.setColor(inner_color)
        inner_slice.setBorderColor(inner_color)

    @staticmethod
    def __update_label(slice_, title):
        """
        Update the label of a slice

        :param slice_: QPieSlice. the slice the label is applied
        :param title: str. title of the label
        """
        text_color = 'black'
        if slice_.percentage() > 0.1:
            slice_.setLabelPosition(QtChart.QPieSlice.LabelInsideHorizontal)
            text_color = 'white'

        label = "<p align='center' style='color:{}'>{}<br>{}%</p>".format(
            text_color,
            title,
            round(slice_.percentage()*100, 2)
            )
        slice_.setLabel(label)

        if slice_.percentage() > 0.03:
            slice_.setLabelVisible()

    def __explode(self, slice_, is_hovered):
        """
        Explode function slot for hovering effect

        :param slice_: QtChart.QPieSlice. the slice hovered
        :param is_hovered: bool. hover enter (True) or leave (False)
        """
        if is_hovered:
            start = slice_.startAngle()
            end = slice_.startAngle() + slice_.angleSpan()
            self.__inner.setPieStartAngle(end)
            self.__inner.setPieEndAngle(start+360)
        else:
            self.__inner.setPieStartAngle(0)
            self.__inner.setPieEndAngle(360)

        slice_.setLabelVisible(is_hovered)
        slice_.setExplodeDistanceFactor(0.1)
        slice_.setExploded(is_hovered)

        if slice_.percentage() > 0.03:
            slice_.setLabelVisible()

    @staticmethod
    def __get_secondary_color(hexcode):
        """
        Get secondary color which is blended 50% with white
        to appear lighter

        :param hexcode: str. color hex code starting with '#'
                        eg. ('#666666')
        :return: QtGui.QColor
        """
        from pipelineUtil.dataType import color

        new_color = color.ColorRGB.from_hex(hexcode).blend().hexcode
        return QtGui.QColor(new_color)


class SimpleChartView(QtChart.QChartView):
    """
    A simple wrapper chart view, to be expanded
    """
    def __init__(self, chart):
        super(SimpleChartView, self).__init__(chart)

        self.setRenderHint(QtGui.QPainter.Antialiasing)


if __name__ == '__main__':
    """
    Example
    """

    class Example(QtWidgets.QMainWindow):
        def __init__(self, datas, parent=None):
            super(Example, self).__init__(parent)

            chart = SmartChart()
            chart.resize(700, 400)
            chart_view = SimpleChartView(chart)

            for data in datas:
                chart.add_slice(data.name, data.value, data.color)

            self.setCentralWidget(chart_view)

    global win
    app = QtWidgets.QApplication(sys.argv)

    node = Data('Node', 333, "#82d3e5")
    connection = Data('Connection', 105, "#fd635c")
    other = Data('Other', 20, "#feb543")
    datas = [node, connection, other]

    win = Example(datas)
    win.show()
    sys.exit(app.exec_())
