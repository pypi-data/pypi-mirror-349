from PySide6 import QtGui, QtWidgets


class ScientificSpinbox(QtWidgets.QDoubleSpinBox):

    def valueFromText(self, text: str) -> float:
        try:
            return float(text)
        except Exception:
            return super().valueFromText(text)

    def textFromValue(self, val: float) -> str:
        return f"{val:.3e}"

    def validate(self, input: str, pos: int):
        return QtGui.QValidator.State.Acceptable
