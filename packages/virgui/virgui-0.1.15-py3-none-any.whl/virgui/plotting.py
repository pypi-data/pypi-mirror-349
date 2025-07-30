from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PySide6 import QtWidgets


# based on https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_qt_sgskip.html
class PlottingWidget(QtWidgets.QWidget):

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent=parent)
        self.tabs = QtWidgets.QTabWidget()
        self.static_canvas = FigureCanvas(Figure())
        self.plot_toolbar = NavigationToolbar(self.static_canvas)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.tabs)

    # this is not the correct way to do it according to the matplotlib docs
    # but finesse returns a new figure object, so I can't update the existing one
    # except by replacing it.
    def update_figures(self, figs: dict[str, Figure]):
        self.tabs.clear()
        for name, fig in figs.items():
            widget = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout()
            widget.setLayout(layout)
            self.tabs.addTab(widget, str(name))
            static_canvas = FigureCanvas(fig)
            toolbar = NavigationToolbar(static_canvas)
            layout.addWidget(toolbar)
            layout.addWidget(static_canvas)
