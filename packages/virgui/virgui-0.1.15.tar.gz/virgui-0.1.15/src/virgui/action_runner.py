from finesse.analysis.actions import Xaxis
from finesse.detectors import Detector
from PySide6 import QtCore, QtWidgets

import virgui
from virgui.plotting import PlottingWidget
from virgui.scientific_spinbox import ScientificSpinbox


class ActionRunner(QtWidgets.QWidget):

    def __init__(
        self,
        plotter: PlottingWidget,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent=parent)
        self.plotter = plotter  # could be multiple plotters?
        self.setLayout(QtWidgets.QVBoxLayout())
        self.header = QtWidgets.QLabel(
            text="# Xaxis",
            textFormat=QtCore.Qt.TextFormat.MarkdownText,
        )
        self.header.setMaximumHeight(40)
        self.layout().addWidget(self.header)

        self.form = QtWidgets.QWidget()
        self.form_layout = QtWidgets.QFormLayout()
        self.form.setLayout(self.form_layout)
        self.layout().addWidget(self.form)

        self.parameter_dropdown = QtWidgets.QComboBox()
        self.parameter_dropdown.addItems(
            [
                p.full_name
                for p in virgui.GLOBAL_MODEL.all_parameters
                if (p.datatype is float and p.changeable_during_simulation)
            ]
        )
        self.parameter_dropdown.currentTextChanged.connect(self.on_parameter_changed)
        self.form_layout.addRow("Sweep Parameter:", self.parameter_dropdown)

        self.mode_dropdown = QtWidgets.QComboBox()
        self.mode_dropdown.addItems(["lin", "log"])
        self.form_layout.addRow("Sweep mode:", self.mode_dropdown)

        self.start_spinbox = ScientificSpinbox()
        self.start_spinbox.setRange(-1e6, 1e6)
        self.form_layout.addRow("Start:", self.start_spinbox)

        self.end_spinbox = ScientificSpinbox()
        self.end_spinbox.setRange(-1e6, 1e6)
        self.form_layout.addRow("End:", self.end_spinbox)

        self.steps_spinbox = QtWidgets.QSpinBox()
        self.steps_spinbox.setRange(0, int(1e6))
        self.form_layout.addRow("Steps:", self.steps_spinbox)

        self.run_button = QtWidgets.QPushButton()
        self.run_button.setIcon(
            self.run_button.style().standardIcon(
                QtWidgets.QStyle.StandardPixmap.SP_MediaPlay
            )
        )
        self.run_button.clicked.connect(self.run_xaxis)
        self.form_layout.addRow("Run sweep:", self.run_button)

    @QtCore.Slot()
    def run_xaxis(self):
        xaxis = Xaxis(
            self.parameter_dropdown.currentText(),
            mode=self.mode_dropdown.currentText(),
            start=self.start_spinbox.value(),
            stop=self.end_spinbox.value(),
            steps=self.steps_spinbox.value(),
        )
        sol = virgui.GLOBAL_MODEL.run(xaxis)
        fig_dict = sol.plot(show=False)
        filtered_fig_dict = {}
        # we want to show one tab for every type of detector
        for key, fig in fig_dict.items():
            print(key, type(key), isinstance(key, type))
            if isinstance(key, type) and issubclass(key, Detector):
                filtered_fig_dict[key.__name__] = fig
        print(filtered_fig_dict)
        self.plotter.update_figures(filtered_fig_dict)
        print(f"ran xaxis with: {xaxis.args}")

    @QtCore.Slot()
    def on_parameter_changed(self):
        p = virgui.GLOBAL_MODEL.get(self.parameter_dropdown.currentText())
        for spinbox in (self.start_spinbox, self.end_spinbox):
            if p.units:
                spinbox.setSuffix(f" [{p.units}]")
            else:
                spinbox.setSuffix("")
