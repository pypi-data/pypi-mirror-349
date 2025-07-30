from __future__ import annotations

from finesse.element import ModelElement
from PySide6 import QtWidgets


class ModelElementRectItem(QtWidgets.QGraphicsRectItem):

    def __init__(
        self, x: float, y: float, width: float, height: float, element: ModelElement
    ):
        self.element = element
        super().__init__(x, y, width, height)
        # for now show where the hitboxes are, because there are some unresolved
        # viewbox problems
        # self.setPen(QtCore.Qt.NoPen)
