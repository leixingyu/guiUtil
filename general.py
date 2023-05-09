import sys
from functools import wraps

from Qt import QtWidgets


def refreshTreeWidget(attribute):
    """
    Post-refresh widget ui element

    ：param attribute: str. name of the widget ui element
    """
    def decorator(func):
        @wraps(func)
        def wrap(self, *args, **kwargs):
            widget = getattr(self, attribute)
            widget.clear()
            try:
                func(self, *args, **kwargs)
            except Exception:
                raise
            finally:
                for i in range(widget.columnCount()):
                    widget.resizeColumnToContents(i)
        return wrap
    return decorator


def register_stylesheet(file):
    global APP
    APP = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    with open(file, 'r') as f:
        qss = f.read()
        APP.setStyleSheet(qss)
