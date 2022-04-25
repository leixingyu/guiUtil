import sys
from collections import namedtuple
from functools import partial

from PyQt5 import QtCore, QtWidgets, QtGui, QtChart


Data = namedtuple('Data', ['name', 'value', 'primary_color', 'secondary_color'])


class MySimpleChart(QtChart.QChart):

    def __init__(self, datas, parent=None):
        super(MySimpleChart, self).__init__(parent)
        self._datas = datas

        self.legend().setAlignment(QtCore.Qt.AlignRight)
        self.legend().setMarkerShape(QtChart.QLegend.MarkerShapeCircle)

        self.outer = QtChart.QPieSeries()
        self.outer.setPieStartAngle(40)
        self.outer.setPieEndAngle(40+360)
        self.set_outer_series()
        self.addSeries(self.outer)

        # separate legend & slice title (may be bad being order dependent)
        for index, marker in enumerate(self.legend().markers()):
            marker.setLabel(self._datas[index].name)

    def set_outer_series(self):
        slices = list()
        for data in self._datas:
            slice_ = QtChart.QPieSlice(data.name, data.value)
            slice_.setLabelVisible()
            slice_.setColor(data.primary_color)
            slice_.setLabelBrush(data.primary_color)
            slice_.setLabelArmLengthFactor(0.3)

            slices.append(slice_)
            self.outer.append(slice_)

        # label styling
        for slice_ in slices:
            label = "<p align='center' style='color:black'>{}%</p>".format(
                round(slice_.percentage()*100, 2))
            slice_.setLabel(label)


class MyChart(QtChart.QChart):

    def __init__(self, datas, parent=None):
        super(MyChart, self).__init__(parent)
        self._datas = datas

        self.legend().hide()
        self.setAnimationOptions(QtChart.QChart.SeriesAnimations)

        self.outer = QtChart.QPieSeries()
        self.inner = QtChart.QPieSeries()
        self.outer.setHoleSize(0.35)
        self.inner.setPieSize(0.35)
        self.inner.setHoleSize(0.3)

        self.set_outer_series()
        self.set_inner_series()

        self.addSeries(self.outer)
        self.addSeries(self.inner)

    def set_outer_series(self):
        slices = list()
        for data in self._datas:
            slice_ = QtChart.QPieSlice(data.name, data.value)
            slice_.setLabelVisible()
            slice_.setColor(data.primary_color)
            slice_.setLabelBrush(data.primary_color)

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

    def set_inner_series(self):
        for data in self._datas:
            slice_ = self.inner.append(data.name, data.value)
            slice_.setColor(data.secondary_color)
            slice_.setBorderColor(data.secondary_color)

    def explode(self, slice_, is_hovered):
        if is_hovered:
            start = slice_.startAngle()
            end = slice_.startAngle()+slice_.angleSpan()
            self.inner.setPieStartAngle(end)
            self.inner.setPieEndAngle(start+360)
        else:
            self.inner.setPieStartAngle(0)
            self.inner.setPieEndAngle(360)

        slice_.setExplodeDistanceFactor(0.1)
        slice_.setExploded(is_hovered)


class ChartView(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(ChartView, self).__init__(parent)
        self.setFixedSize(QtCore.QSize(700, 400))

        node = Data('Node', 333, QtGui.QColor("#82d3e5"), QtGui.QColor("#cfeef5"))
        connection = Data('Connection', 105, QtGui.QColor("#fd635c"), QtGui.QColor("#fdc4c1"))
        other = Data('Other', 20, QtGui.QColor("#feb543"), QtGui.QColor("#ffe3b8"))

        datas = [node, connection, other]
        chart = MySimpleChart(datas)

        chart_view = QtChart.QChartView(chart)
        chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setCentralWidget(chart_view)


if __name__ == '__main__':
    global win
    app = QtWidgets.QApplication(sys.argv)
    win = ChartView()
    win.show()
    sys.exit(app.exec_())
