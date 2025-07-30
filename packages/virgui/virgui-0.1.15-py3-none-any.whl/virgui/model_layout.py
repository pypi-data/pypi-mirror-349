from __future__ import annotations

import tempfile
import warnings
from typing import TYPE_CHECKING, Callable

# import xml.etree.ElementTree as ET
import lxml.etree
from finesse.components.general import ModelElement
from finesse.components.node import OpticalNode
from finesse.detectors import Detector
from PySide6 import QtCore, QtGui, QtSvgWidgets, QtWidgets

from virgui import ASSETS
from virgui.component import ModelElementRectItem
from virgui.graph import write_node_overview
from virgui.parameter_table import ParameterTableModel
from virgui.parse_layout import parse_layout

if TYPE_CHECKING:
    pass

import virgui


class ZoomableGraphicsScene(QtWidgets.QGraphicsScene):

    def wheelEvent(self, event: QtWidgets.QGraphicsSceneWheelEvent) -> None:
        scale_factor = 1.15
        if event.delta() > 0:
            self.views()[0].scale(scale_factor, scale_factor)
        else:
            self.views()[0].scale(1 / scale_factor, 1 / scale_factor)
        event.accept()
        return super().wheelEvent(event)

    def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent, /) -> None:
        super().mousePressEvent(event)
        print(event)


class ModelLayout(QtWidgets.QWidget):

    def __init__(
        self,
        katscript_listener: Callable,
        katlog_listener: Callable,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent=parent)
        # it would be cleaner to define these in their respective classes
        # maybe there is something like an event listener
        self.katscript_listener = katscript_listener
        self.katlog_listener = katlog_listener

        self.setLayout(QtWidgets.QHBoxLayout())
        self.scene = ZoomableGraphicsScene(
            0, 0, 600, 600, backgroundBrush=QtGui.QBrush(QtCore.Qt.white)
        )
        self.scene.selectionChanged.connect(self.on_selection)
        self.switch_layout("virgo_test")

        # info window
        self.info_vbox = QtWidgets.QVBoxLayout()
        self.table_title = QtWidgets.QLabel(
            textFormat=QtCore.Qt.TextFormat.MarkdownText,
            textInteractionFlags=QtCore.Qt.TextInteractionFlag.TextBrowserInteraction,
            openExternalLinks=True,
        )
        self.table_view = QtWidgets.QTableView()
        self.detector_overview = QtWidgets.QTextEdit()
        self.detector_overview.setReadOnly(True)
        self.detector_overview.setAcceptRichText(True)
        self.ports_overview_tab = QtWidgets.QTabWidget()
        self.ports_overview_scene_svg = ZoomableGraphicsScene(
            backgroundBrush=QtGui.QBrush(QtCore.Qt.white)
        )
        self.ports_overview_scene_graphviz = ZoomableGraphicsScene(
            backgroundBrush=QtGui.QBrush(QtCore.Qt.white)
        )
        ports_overview_view_svg = QtWidgets.QGraphicsView(self.ports_overview_scene_svg)
        ports_overview_view_graphviz = QtWidgets.QGraphicsView(
            self.ports_overview_scene_graphviz
        )

        self.ports_overview_tab.addTab(ports_overview_view_svg, "Option A")
        self.ports_overview_tab.addTab(ports_overview_view_graphviz, "Option B")

        self.info_vbox.addWidget(self.table_title)
        self.info_vbox.addWidget(self.table_view)
        self.info_vbox.addWidget(self.detector_overview)
        self.info_vbox.addWidget(self.ports_overview_tab)

        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)

        self.layout().addWidget(self.view)
        self.layout().addLayout(self.info_vbox)

    def switch_layout(self, layout_name: str):
        self.scene.clear()
        model, hitbox_mapping, svg_path = parse_layout(virgui.LAYOUTS / layout_name)
        virgui.GLOBAL_MODEL = model
        svg_graphics_item = QtSvgWidgets.QGraphicsSvgItem(svg_path)
        # TODO would prefer to do this from memory, but can't get below to work
        # svg_graphics_item.renderer().load(svg_b_string)
        self.scene.addItem(svg_graphics_item)

        # add completely transparent rectangles as hitboxes, so users can select elements
        for comp_name, rect in hitbox_mapping.items():
            hitbox = ModelElementRectItem(
                rect.x, rect.y, rect.width, rect.height, model.get(comp_name)
            )
            print(comp_name, rect)
            self.scene.addItem(hitbox)

        for item in self.scene.items():
            if item is not svg_graphics_item:
                item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

        self.katscript_listener()
        # TODO maybe adjust the view here so everything is in focus?

    @QtCore.Slot()
    def on_selection(self):
        items = self.scene.selectedItems()
        if len(items) == 0:
            self.table_view.hide()
            self.table_title.setText("")
            self.detector_overview.clear()
            self.ports_overview_scene_svg.clear()
            self.ports_overview_scene_graphviz.clear()
        elif len(items) == 1:
            item = items[0]
            assert isinstance(item, ModelElementRectItem)
            assert isinstance(item.element, ModelElement)
            el: ModelElement = item.element
            # maybe pre-create these instead of on the fly
            par_table = el.parameter_table(return_str=False)
            info_table = ParameterTableModel(par_table, el)
            info_table.dataChanged.connect(self.katscript_listener)
            info_table.parameter_changed.connect(self.katlog_listener)
            self.table_view.setModel(info_table)
            self.table_view.resizeRowsToContents()
            self.table_view.show()
            modules = el.__class__.__module__.split(".")
            doc_url = f"https://finesse.ifosim.org/docs/latest/api/{modules[1]}/{modules[2]}/{el.__class__.__module__}.{el.__class__.__name__}.html#{el.__class__.__module__}.{el.__class__.__name__}"
            self.table_title.setText(
                f"# [{el.__class__.__name__}]({doc_url}): {el.name}"
            )

            self.detector_overview.clear()
            self.detector_overview.setMarkdown(self._detectors_for_component(el))
            self.ports_overview_scene_svg.clear()
            self.ports_overview_scene_svg.addItem(self._make_node_overview_svg(el))

            self.ports_overview_scene_graphviz.clear()
            self.ports_overview_scene_graphviz.addItem(
                self._make_node_overview_graphviz(el)
            )

        else:
            raise

    def _detectors_for_component(self, comp: ModelElement) -> str:
        detectors: list[Detector] = []
        for detector in virgui.GLOBAL_MODEL.detectors:
            if detector.node.component is comp:
                detectors.append(detector)
        if not len(detectors):
            return ""
        md = "# Attached detectors\n"
        for detector in detectors:
            md += f"- {detector.node.__class__.__name__} {detector.node.full_name} -> {detector.__class__.__name__} {detector.name}\n"
        return md

    def _make_node_overview_svg(
        self, comp: ModelElement
    ) -> QtSvgWidgets.QGraphicsSvgItem:

        tree = lxml.etree.parse(ASSETS / "2-port.svg", lxml.etree.XMLParser())
        root = tree.getroot()

        # this may be slow to do all the time
        g = virgui.GLOBAL_MODEL.optical_network.to_undirected()

        # only implemented for two port components
        if not (hasattr(comp, "p1") and hasattr(comp, "p2")):
            warnings.warn(f"Could not generate node overview for {comp}")
            return QtSvgWidgets.QGraphicsSvgItem()

        for node in (comp.p1.i, comp.p1.o, comp.p2.i, comp.p2.o):
            node: OpticalNode
            connect_to = None
            for nb in g.neighbors(node.full_name):
                if nb.split(".")[0] != node.component.name:
                    connect_to = nb
                    break
            # if not node.port.is_connected:
            #     assert connect_to is not None

            el = root.find(
                path=f".//{{http://www.w3.org/2000/svg}}text[@id='{node.port.name}.{node.name}']/{{http://www.w3.org/2000/svg}}tspan"
            )
            if connect_to:
                fsize = int(7.0 / len(connect_to) * 10)
                el.text = connect_to
                el.attrib["font-size"] = f"{fsize}px"
            else:
                el.text = "N/A"
        el = root.find(
            path=".//{http://www.w3.org/2000/svg}text[@id='comp_name']/{http://www.w3.org/2000/svg}tspan"
        )
        el.text = comp.name
        path = tempfile.NamedTemporaryFile(suffix=".svg", delete=False).name
        with open(path, "w") as f:
            f.write(lxml.etree.tounicode(tree))
        svg_item = QtSvgWidgets.QGraphicsSvgItem(path)
        return svg_item

    def _make_node_overview_graphviz(
        self, comp: ModelElement
    ) -> QtSvgWidgets.QGraphicsSvgItem:
        path = tempfile.NamedTemporaryFile(suffix=".svg", delete=False).name
        write_node_overview(virgui.GLOBAL_MODEL, comp, path)
        svg_item = QtSvgWidgets.QGraphicsSvgItem(path)
        return svg_item
