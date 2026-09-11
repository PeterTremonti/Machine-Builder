"""Main editor window and canvas for the Machine Structure Editor.

The canvas is a presentation layer. It renders the VisualModel owned by
ModelStore and sends user actions back through explicit mutations.

V0.1 interaction goals:

* palette drag-and-drop creates nodes
* double-clicking a palette item also creates a node
* moving one or more nodes is one undoable action
* deleting one or more selected nodes is one undoable action
* the canvas supports smooth zooming and panning
* newly created nodes appear near the current editing context
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QDragEnterEvent,
    QDropEvent,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsProxyWidget,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsSimpleTextItem,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .mutations import CreateNode, DeleteNodes, MoveNodes
from .store import ModelStore
from .visual_model import VisualModel, VisualNode


@dataclass
class NodeDragState:
    """Temporary state for one continuous node-drag interaction."""

    node_ids: tuple[str, ...]
    start_positions: dict[str, tuple[float, float]]
    final_positions: dict[str, tuple[float, float]]


class NodeGraphicsItem(QGraphicsRectItem):
    """Qt presentation object for one VisualNode."""

    def __init__(
        self,
        node: VisualNode,
        move_started_callback: Any,
        move_finished_callback: Any,
        select_callback: Any,
    ) -> None:
        super().__init__(0, 0, node.width, node.height)

        self.node_id = node.id

        self._move_started_callback = move_started_callback
        self._move_finished_callback = move_finished_callback
        self._select_callback = select_callback

        self._drag_start_position: QPointF | None = None

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges,
            True,
        )

        self.setAcceptHoverEvents(True)

        self.setBrush(QBrush(QColor("#2f3440")))
        self.setPen(QPen(QColor("#8c96a8"), 1.5))

        self.setPos(node.x, node.y)

        label = QGraphicsSimpleTextItem(node.label, self)
        label.setBrush(QBrush(QColor("#f0f0f0")))
        label.setPos(10, 10)

    def mousePressEvent(self, event: Any) -> None:
        """Remember the start of a drag before Qt changes the position."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_position = self.pos()

            self._move_started_callback(self.node_id)

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: Any) -> None:
        """Commit the completed drag as one logical user action."""
        super().mouseReleaseEvent(event)

        if event.button() == Qt.MouseButton.LeftButton:
            self._move_finished_callback(self.node_id)
            self._drag_start_position = None

    def itemChange(
        self,
        change: QGraphicsItem.GraphicsItemChange,
        value: Any,
    ) -> Any:
        """Synchronize visual selection state and movement."""
        if (
            change
            == QGraphicsItem.GraphicsItemChange.ItemSelectedChange
        ):
            self._select_callback(self.node_id, bool(value))

        return super().itemChange(change, value)


class MachineGraphicsView(QGraphicsView):
    """Graphics view with smooth interaction-oriented navigation."""

    def __init__(
        self,
        scene: QGraphicsScene,
        canvas: "MachineCanvas",
    ) -> None:
        super().__init__(scene)

        self._canvas = canvas
        self._panning = False
        self._pan_start = QPointF()

        self.setAcceptDrops(True)

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )
        self.setResizeAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.setBackgroundBrush(QBrush(QColor("#17191e")))

        self.setMouseTracking(True)

    def wheelEvent(self, event: Any) -> None:
        """Zoom smoothly around the mouse position."""
        delta = event.angleDelta().y()

        if delta == 0:
            event.ignore()
            return

        # A smaller factor produces smoother, less abrupt zoom changes.
        factor = 1.12 if delta > 0 else 1.0 / 1.12

        self.scale(factor, factor)
        event.accept()

    def mousePressEvent(self, event: Any) -> None:
        """Begin middle-button canvas panning."""
        if event.button() == Qt.MouseButton.MiddleButton:
            self._panning = True
            self._pan_start = event.position()

            self.viewport().setCursor(
                Qt.CursorShape.ClosedHandCursor
            )

            event.accept()
            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: Any) -> None:
        """Continue middle-button canvas panning."""
        if self._panning:
            current = event.position()
            delta = current - self._pan_start

            self._pan_start = current

            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value()
                - int(delta.x())
            )

            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value()
                - int(delta.y())
            )

            event.accept()
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: Any) -> None:
        """Finish middle-button canvas panning."""
        if event.button() == Qt.MouseButton.MiddleButton:
            self._panning = False
            self.viewport().setCursor(
                Qt.CursorShape.ArrowCursor
            )

            event.accept()
            return

        super().mouseReleaseEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """Accept palette drags carrying a node type."""
        if event.mimeData().hasText():
            event.acceptProposedAction()
            return

        event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        """Create a node where a palette item is dropped."""
        text = event.mimeData().text().strip()

        if not text:
            event.ignore()
            return

        scene_position = self.mapToScene(
            event.position().toPoint()
        )

        self._canvas.create_node_from_template(
            node_type=text,
            scene_position=scene_position,
        )

        event.acceptProposedAction()


class PaletteList(QListWidget):
    """Palette supporting both normal selection and drag-and-drop."""

    def startDrag(self, supported_actions: Any) -> None:
        """Start a text-based drag containing the selected node template."""
        item = self.currentItem()

        if item is None:
            return

        from PySide6.QtCore import QMimeData
        from PySide6.QtGui import QDrag

        node_type = item.data(Qt.ItemDataRole.UserRole)

        if not isinstance(node_type, str):
            return

        mime_data = QMimeData()
        mime_data.setText(node_type)

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.exec(Qt.DropAction.CopyAction)


class MachineCanvas(QMainWindow):
    """Main Machine Structure Editor window."""

    def __init__(self) -> None:
        super().__init__()

        self.store = ModelStore()
        self.store.subscribe(self._model_changed)

        self._node_items: dict[str, NodeGraphicsItem] = {}

        self._node_counter = 0
        self._last_edit_position = QPointF(100.0, 100.0)

        self._active_drag: NodeDragState | None = None

        # Prevent model synchronization from triggering another mutation.
        self._synchronizing_scene = False

        self._build_ui()
        self._create_actions()

        self._model_changed(self.store.model)

    def _build_ui(self) -> None:
        """Build the application window."""
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        self.palette = PaletteList()
        self.palette.setMinimumWidth(180)
        self.palette.setDragEnabled(True)

        templates = (
            ("controller", "Controller"),
            ("motor", "Motor"),
            ("sensor", "Sensor"),
            ("component", "Component"),
        )

        for node_type, label in templates:
            item = QListWidgetItem(label)
            item.setData(Qt.ItemDataRole.UserRole, node_type)
            self.palette.addItem(item)

        self.palette.itemDoubleClicked.connect(
            self._palette_item_double_clicked
        )

        palette_layout = QVBoxLayout()

        palette_title = QLabel("Components")
        palette_title.setStyleSheet("font-weight: bold;")

        add_button = QPushButton("Add selected")
        add_button.clicked.connect(
            self._add_selected_palette_item
        )

        palette_help = QLabel(
            "Double-click or drag a component onto the canvas."
        )
        palette_help.setWordWrap(True)

        palette_layout.addWidget(palette_title)
        palette_layout.addWidget(self.palette)
        palette_layout.addWidget(add_button)
        palette_layout.addWidget(palette_help)

        palette_panel = QWidget()
        palette_panel.setLayout(palette_layout)

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(
            -100000,
            -100000,
            200000,
            200000,
        )

        self.view = MachineGraphicsView(
            scene=self.scene,
            canvas=self,
        )

        main_layout.addWidget(palette_panel)
        main_layout.addWidget(self.view, 1)

        self.statusBar().showMessage("Ready")

    def _create_actions(self) -> None:
        """Create editor commands and their keyboard shortcuts."""
        delete_action = QAction("Delete", self)
        delete_action.setShortcut(
            Qt.Key.Key_Delete
        )
        delete_action.triggered.connect(
            self._delete_selected
        )

        undo_action = QAction("Undo", self)
        undo_action.setShortcut(
            "Ctrl+Z"
        )
        undo_action.triggered.connect(
            self.store.undo
        )

        redo_action = QAction("Redo", self)
        redo_action.setShortcut(
            "Ctrl+Y"
        )
        redo_action.triggered.connect(
            self.store.redo
        )

        frame_action = QAction(
            "Frame All",
            self,
        )
        frame_action.setShortcut(
            "F"
        )
        frame_action.triggered.connect(
            self._frame_all
        )

        self.addAction(delete_action)
        self.addAction(undo_action)
        self.addAction(redo_action)
        self.addAction(frame_action)

    def _palette_item_double_clicked(
        self,
        item: QListWidgetItem,
    ) -> None:
        """Create a node from a double-clicked palette item."""
        node_type = item.data(Qt.ItemDataRole.UserRole)

        if not isinstance(node_type, str):
            return

        self.create_node_from_template(
            node_type=node_type,
            scene_position=self._suggest_new_node_position(),
        )

    def _add_selected_palette_item(self) -> None:
        """Create a node from the selected palette template."""
        item = self.palette.currentItem()

        if item is None:
            return

        node_type = item.data(Qt.ItemDataRole.UserRole)

        if not isinstance(node_type, str):
            return

        self.create_node_from_template(
            node_type=node_type,
            scene_position=self._suggest_new_node_position(),
        )

    def create_node_from_template(
        self,
        node_type: str,
        scene_position: QPointF,
    ) -> None:
        """Create a provisional visual node at a requested position."""
        labels = {
            "controller": "Controller",
            "motor": "Motor",
            "sensor": "Sensor",
            "component": "Component",
        }

        label = labels.get(
            node_type,
            node_type.replace("_", " ").title(),
        )

        self._node_counter += 1

        node_id = f"node-{self._node_counter}"

        node = VisualNode(
            id=node_id,
            node_type=node_type,
            label=label,
            x=scene_position.x(),
            y=scene_position.y(),
        )

        self.store.commit(
            CreateNode(node)
        )

        self._last_edit_position = scene_position

        self.statusBar().showMessage(
            f"Created {label}"
        )

    def _suggest_new_node_position(self) -> QPointF:
        """Choose a useful location near the current editing context."""
        if self.store.model.nodes:
            base = self._last_edit_position

            # Offset each new component enough to avoid immediate overlap
            # while keeping it in the area where the user is working.
            return QPointF(
                base.x() + 40.0,
                base.y() + 40.0,
            )

        return QPointF(
            100.0,
            100.0,
        )

    def _delete_selected(self) -> None:
        """Delete all selected visual nodes as one user action."""
        selected_ids = tuple(
            item.node_id
            for item in self.scene.selectedItems()
            if isinstance(item, NodeGraphicsItem)
        )

        if not selected_ids:
            return

        self.store.commit(
            DeleteNodes(
                node_ids=selected_ids,
            )
        )

        self.statusBar().showMessage(
            f"Deleted {len(selected_ids)} node"
            + ("" if len(selected_ids) == 1 else "s")
        )

    def _begin_node_move(self, node_id: str) -> None:
        """Begin tracking one physical drag interaction."""
        if self._synchronizing_scene:
            return

        node = self.store.model.nodes.get(node_id)

        if node is None:
            return

        selected_nodes = [
            item
            for item in self.scene.selectedItems()
            if isinstance(item, NodeGraphicsItem)
        ]

        if node_id not in {
            item.node_id
            for item in selected_nodes
        }:
            selected_nodes = [
                self._node_items[node_id]
            ]

        node_ids = tuple(
            item.node_id
            for item in selected_nodes
        )

        start_positions = {
            item.node_id: (
                self.store.model.nodes[item.node_id].x,
                self.store.model.nodes[item.node_id].y,
            )
            for item in selected_nodes
        }

        self._active_drag = NodeDragState(
            node_ids=node_ids,
            start_positions=start_positions,
            final_positions=dict(start_positions),
        )

    def _finish_node_move(self, node_id: str) -> None:
        """Commit one or more moved nodes as one mutation."""
        if (
            self._active_drag is None
            or self._synchronizing_scene
        ):
            return

        drag = self._active_drag

        final_positions: dict[str, tuple[float, float]] = {}

        for dragged_id in drag.node_ids:
            item = self._node_items.get(dragged_id)

            if item is None:
                continue

            position = item.pos()

            final_positions[dragged_id] = (
                position.x(),
                position.y(),
            )

        changed = any(
            abs(final_positions[node_id][0] - start[0]) > 0.001
            or abs(final_positions[node_id][1] - start[1]) > 0.001
            for node_id, start in drag.start_positions.items()
            if node_id in final_positions
        )

        if changed:
            self.store.commit(
                MoveNodes(
                    positions=final_positions,
                )
            )

            for node_id, (x, y) in final_positions.items():
                self._last_edit_position = QPointF(x, y)

        self._active_drag = None

    def _node_selected(
        self,
        node_id: str,
        selected: bool,
    ) -> None:
        """Update presentation feedback for one node."""
        item = self._node_items.get(node_id)

        if item is None:
            return

        if selected:
            item.setPen(
                QPen(
                    QColor("#58a6ff"),
                    2.0,
                )
            )
        else:
            item.setPen(
                QPen(
                    QColor("#8c96a8"),
                    1.5,
                )
            )

    def _model_changed(
        self,
        model: VisualModel,
    ) -> None:
        """Synchronize the Qt scene with the authoritative visual model."""
        self._synchronizing_scene = True

        try:
            current_ids = set(model.nodes)
            existing_ids = set(self._node_items)

            for node_id in existing_ids - current_ids:
                item = self._node_items.pop(node_id)
                self.scene.removeItem(item)

            for node_id, node in model.nodes.items():
                item = self._node_items.get(node_id)

                if item is None:
                    item = NodeGraphicsItem(
                        node=node,
                        move_started_callback=self._begin_node_move,
                        move_finished_callback=self._finish_node_move,
                        select_callback=self._node_selected,
                    )

                    self._node_items[node_id] = item
                    self.scene.addItem(item)

                else:
                    item.setRect(
                        0,
                        0,
                        node.width,
                        node.height,
                    )

                item.setPos(
                    node.x,
                    node.y,
                )

        finally:
            self._synchronizing_scene = False

    def _frame_all(self) -> None:
        """Fit all current objects into view."""
        if not self.store.model.nodes:
            return

        self.scene.setSceneRect(
            self.scene.itemsBoundingRect().adjusted(
                -100,
                -100,
                100,
                100,
            )
        )

        self.view.fitInView(
            self.scene.sceneRect(),
            Qt.AspectRatioMode.KeepAspectRatio,
        )