import sys

import finesse
from PySide6 import QtCore, QtGui, QtWidgets

import virgui
from virgui.action_runner import ActionRunner
from virgui.check_version import check_version
from virgui.console import StdRedirect
from virgui.kat_log import KatScriptLog
from virgui.katscript_viewer import KatScriptViewer
from virgui.model_layout import ModelLayout
from virgui.plotting import PlottingWidget

finesse.init_plotting()

QtCore.QLocale.setDefault(QtCore.QLocale("US"))


class ZoomableGraphicsScene(QtWidgets.QGraphicsScene):

    def wheelEvent(self, event: QtWidgets.QGraphicsSceneWheelEvent) -> None:
        scale_factor = 1.15
        if event.delta() > 0:
            self.views()[0].scale(scale_factor, scale_factor)
        else:
            self.views()[0].scale(1 / scale_factor, 1 / scale_factor)
        event.accept()
        return super().wheelEvent(event)


# https://www.pythonguis.com/tutorials/pyside6-qgraphics-vector-graphics/
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"VIRGUI [{virgui.__version__}]")
        self.setMinimumSize(1200, 900)

        self.kat_text = KatScriptViewer()
        self.kat_log = KatScriptLog()
        self.model_layout = ModelLayout(
            katscript_listener=self.kat_text.update,
            katlog_listener=self.kat_log.update,
        )
        self.plotter = PlottingWidget()
        self.action_runner = ActionRunner(plotter=self.plotter)

        # https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QMainWindow.html#PySide6.QtWidgets.QMainWindow.DockOption
        # We could eventually make dockable tabs, but it is a bit of hassle
        # And has an unsolved glitch on Wayland
        self.tabs = QtWidgets.QTabWidget(movable=True)
        self.setCentralWidget(self.tabs)

        # layout tab
        self.tabs.addTab(self.model_layout, "Layout")

        # calculate tab
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setLayout(QtWidgets.QHBoxLayout())
        self.tabs.addTab(self.tab2, "Calculate")

        self.tab2.layout().addWidget(self.action_runner)
        self.tab2.layout().addWidget(self.plotter)

        # katscript tab
        self.tab3 = QtWidgets.QWidget()
        self.tab3.setLayout(QtWidgets.QHBoxLayout())
        self.tabs.addTab(self.tab3, "KatScript")
        self.tab3.layout().addWidget(self.kat_text)
        self.tab3.layout().addWidget(self.kat_log)

        self.tab4 = QtWidgets.QTextEdit()
        self.tab4.setReadOnly(True)
        self.tab4.setAcceptRichText(True)
        self.stderr_redirect = StdRedirect()
        sys.stderr = self.stderr_redirect
        self.stderr_redirect.orig_stream = sys.__stderr__
        self.stderr_redirect.text_edits = [self.tab4]
        self.tabs.addTab(self.tab4, "Error Console")
        self.tab4.textChanged.connect(self.set_console_error_icon)
        self.tabs.currentChanged.connect(self.unset_console_error_icon)

    @QtCore.Slot()
    def set_console_error_icon(self):
        index = self.tabs.indexOf(self.tab4)
        self.tabs.setTabIcon(
            index,
            self.tab4.style().standardIcon(
                QtWidgets.QStyle.StandardPixmap.SP_MessageBoxCritical
            ),
        )

    @QtCore.Slot(int)
    def unset_console_error_icon(self, index: int):
        if index == self.tabs.indexOf(self.tab4):
            self.tabs.setTabIcon(
                index,
                QtGui.QIcon(),
            )

    def make_version_dialog(self):
        ret = check_version()
        if ret is None:
            return
        newest, current = ret
        QtWidgets.QMessageBox.information(
            self,
            "New Version!",
            f"You have version '{current}', newest version is '{newest}'",
        )


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(str(virgui.ASSETS / "miron.png")))

    w = Window()
    w.show()
    w.make_version_dialog()
    app.exec()


if __name__ == "__main__":
    main()
