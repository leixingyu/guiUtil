"""
Template for drawing Pie Charts in Qt Application
"""


import sys
from collections import namedtuple
from functools import partial

from PyQt5 import QtCore, QtWidgets, QtGui, QtChart


Data = namedtuple('Data', ['name', 'value', 'color'])


class SimpleChart(QtChart.QChart):
    """
    A bare minimum implementation of pie chart in Qt
    """

    def __init__(self, datas, parent=None):
        """
        Initialization with layout and population

        :param datas: pieChart.Data. data to be fed into the chart
        """
        super(SimpleChart, self).__init__(parent)
        self._datas = datas
        offset = 40

        self.legend().setAlignment(QtCore.Qt.AlignRight)
        self.legend().setMarkerShape(QtChart.QLegend.MarkerShapeCircle)

        self.series = QtChart.QPieSeries()
        self.series.setPieStartAngle(offset)
        self.series.setPieEndAngle(offset+360)
        self.set_series()
        self.addSeries(self.series)

    def set_series(self):
        """
        Set design of the chart series
        """
        slices = list()
        for data in self._datas:
            slice_ = QtChart.QPieSlice(data.name, data.value)
            slice_.setColor(QtGui.QColor(data.color))
            slice_.setLabelBrush(QtGui.QColor(data.color))
            slice_.setLabelArmLengthFactor(0.3)

            slices.append(slice_)
            self.series.append(slice_)

        # label styling
        for slice_ in slices:
            label = "<p align='center' style='color:black'>{} {}%</p>".format(
                slice_.label(),
                round(slice_.percentage()*100, 2))
            slice_.setLabel(label)

            if slice_.percentage() > 0.03:
                slice_.setLabelVisible()


class SmartChart(QtChart.QChart):
    """
    A slightly smarter implementation of pie chart in Qt, with
    double looped pie chart layout design and hover animation.
    """

    def __init__(self, datas, parent=None):
        """
        Initialization with layout and population

        :param datas: pieChart.Data. data to be fed into the chart
        """
        super(SmartChart, self).__init__(parent)
        self._datas = datas
        offset = 140

        self.setMargins(QtCore.QMargins(0, 0, 0, 0))
        self.legend().hide()
        self.setAnimationOptions(QtChart.QChart.SeriesAnimations)

        self.outer = QtChart.QPieSeries()
        self.inner = QtChart.QPieSeries()
        self.outer.setHoleSize(0.35)
        self.outer.setPieStartAngle(offset)
        self.outer.setPieEndAngle(offset+360)
        self.inner.setPieSize(0.35)
        self.inner.setHoleSize(0.3)
        self.inner.setPieStartAngle(offset)
        self.inner.setPieEndAngle(offset+360)

        self.set_outer_series()
        self.set_inner_series()

        self.addSeries(self.outer)
        self.addSeries(self.inner)

    def set_outer_series(self):
        """
        Set design of the outer looped chart series
        """
        slices = list()
        for data in self._datas:
            slice_ = QtChart.QPieSlice(data.name, data.value)
            slice_.setColor(QtGui.QColor(data.color))
            slice_.setLabelBrush(QtGui.QColor(data.color))

            slices.append(slice_)
            self.outer.append(slice_)
            slice_.hovered.connect(partial(self.explode, slice_))

        # label styling
        for slice_ in slices:
            color = 'black'
            if slice_.percentage() > 0.1:
                slice_.setLabelPosition(QtChart.QPieSlice.LabelInsideHorizontal)
                color = 'white'

            label = "<p align='center' style='color:{}'>{}<br>{}%</p>".format(
                color,
                slice_.label(),
                round(slice_.percentage()*100, 2)
                )
            slice_.setLabel(label)

            if slice_.percentage() > 0.03:
                slice_.setLabelVisible()

    def set_inner_series(self):
        """
        Set design of the inner looped chart series
        """
        for data in self._datas:
            slice_ = self.inner.append(data.name, data.value)
            slice_.setColor(self.get_secondary_color(data.color))
            slice_.setBorderColor(self.get_secondary_color(data.color))

    def explode(self, slice_, is_hovered):
        """
        Explode function slot for hovering effect

        :param slice_: QtChart.QPieSlice. the slice hovered
        :param is_hovered: bool. hover enter (True) or leave (False)
        """
        if is_hovered:
            start = slice_.startAngle()
            end = slice_.startAngle()+slice_.angleSpan()
            self.inner.setPieStartAngle(end)
            self.inner.setPieEndAngle(start+360)
        else:
            self.inner.setPieStartAngle(0)
            self.inner.setPieEndAngle(360)

        slice_.setLabelVisible(is_hovered)
        slice_.setExplodeDistanceFactor(0.1)
        slice_.setExploded(is_hovered)

        if slice_.percentage() > 0.03:
            slice_.setLabelVisible()

    @staticmethod
    def get_secondary_color(hexcode):
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

            chart = SimpleChart(datas)
            chart.resize(700, 400)
            chart_view = SimpleChartView(chart)

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
