"""Main editor window and canvas for the Machine Structure Editor.

The canvas is a presentation layer.  It renders the VisualModel owned by
ModelStore and sends user actions back through explicit mutations.

No Qt graphics item is treated as authoritative machine or visual-model data.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QAction, QBrush, QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QGraphicsItem,
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

from .mutations import CreateNode, DeleteNode, MoveNode
from .store import ModelStore
from .visual_model import VisualModel, VisualNode


class NodeGraphicsItem(QGraphicsRectItem):
    """Qt presentation object for one VisualNode."""

    def __init__(
        self,
        node: VisualNode,
        move_callback: Any,
        select_callback: Any,
    ) -> None:
        super().__init__(0, 0, node.width, node.height)

        self.node_id = node.id
        self._move_callback = move_callback
        self._select_callback = select_callback

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        self.setBrush(QBrush(QColor("#2f3440")))
        self.setPen(QPen(QColor("#8c96a8"), 1.5))

        self.setPos(node.x, node.y)

        label = QGraphicsSimpleTextItem(node.label, self)
        label.setBrush(QBrush(QColor("#f0f0f0")))
        label.setPos(10, 10)

    def itemChange(
        self,
        change: QGraphicsItem.GraphicsItemChange,
        value: Any,
    ) -> Any:
        """Synchronize committed movement back into the visual model."""
        if (
            change
            == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged
        ):
            position = value
            if isinstance(position, QPointF):
                self._move_callback(
                    self.node_id,
                    position.x(),
                    position.y(),
                )

        if change == QGraphicsItem.GraphicsItemChange.ItemSelectedChange:
            self._select_callback(self.node_id, bool(value))

        return super().itemChange(change, value)


class MachineCanvas(QMainWindow):
    """Main Machine Structure Editor window."""

    def __init__(self) -> None:
        super().__init__()

        self.store = ModelStore()
        self.store.subscribe(self._model_changed)

        self._node_items: dict[str, NodeGraphicsItem] = {}
        self._suppress_item_callbacks = False
        self._node_counter = 0

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

        self.palette = QListWidget()
        self.palette.setMinimumWidth(180)

        for node_type in (
            ("controller", "Controller"),
            ("motor", "Motor"),
            ("sensor", "Sensor"),
            ("component", "Component"),
        ):
            item = QListWidgetItem(node_type[1])
            item.setData(Qt.ItemDataRole.UserRole, node_type[0])
            self.palette.addItem(item)

        self.palette.itemDoubleClicked.connect(self._palette_item_activated)

        palette_layout = QVBoxLayout()

        palette_title = QLabel("Components")
        palette_title.setStyleSheet("font-weight: bold;")

        add_button = QPushButton("Add selected")
        add_button.clicked.connect(self._add_selected_palette_item)

        palette_layout.addWidget(palette_title)
        palette_layout.addWidget(self.palette)
        palette_layout.addWidget(add_button)

        palette_panel = QWidget()
        palette_panel.setLayout(palette_layout)

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-5000, -5000, 10000, 10000)

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.view.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )
        self.view.setResizeAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )
        self.view.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.view.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.view.setBackgroundBrush(QBrush(QColor("#17191e")))

        main_layout.addWidget(palette_panel)
        main_layout.addWidget(self.view, 1)

        self.statusBar().showMessage("Ready")

    def _create_actions(self) -> None:
        """Create the initial editor actions and keyboard shortcuts."""
        delete_action = QAction("Delete", self)
        delete_action.setShortcut("Delete")
        delete_action.triggered.connect(self._delete_selected)

        undo_action = QAction("Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.store.undo)

        redo_action = QAction("Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.store.redo)

        self.addAction(delete_action)
        self.addAction(undo_action)
        self.addAction(redo_action)

    def _palette_item_activated(self, item: QListWidgetItem) -> None:
        """Add a node when a palette entry is double-clicked."""
        self._create_from_palette_item(item)

    def _add_selected_palette_item(self) -> None:
        """Add the currently selected palette item."""
        item = self.palette.currentItem()
        if item is not None:
            self._create_from_palette_item(item)

    def _create_from_palette_item(self, item: QListWidgetItem) -> None:
        """Create a provisional visual node from a palette template."""
        node_type = item.data(Qt.ItemDataRole.UserRole)

        if not isinstance(node_type, str):
            return

        self._node_counter += 1
        node_id = f"node-{self._node_counter}"

        node = VisualNode(
            id=node_id,
            node_type=node_type,
            label=item.text(),
            x=100.0 + (self._node_counter - 1) * 30.0,
            y=100.0 + (self._node_counter - 1) * 30.0,
        )

        self.store.commit(CreateNode(node))
        self.statusBar().showMessage(f"Created {node.label}")

    def _delete_selected(self) -> None:
        """Delete the currently selected visual nodes."""
        selected = self.scene.selectedItems()

        node_ids: list[str] = []

        for item in selected:
            if isinstance(item, NodeGraphicsItem):
                node_ids.append(item.node_id)

        for node_id in node_ids:
            if node_id in self.store.model.nodes:
                self.store.commit(DeleteNode(node_id))

        if node_ids:
            self.statusBar().showMessage(
                f"Deleted {len(node_ids)} node"
                + ("" if len(node_ids) == 1 else "s")
            )

    def _node_moved(self, node_id: str, x: float, y: float) -> None:
        """Commit a node movement to the visual model."""
        if self._suppress_item_callbacks:
            return

        node = self.store.model.nodes.get(node_id)
        if node is None:
            return

        # Avoid recording redundant movement mutations while Qt emits
        # geometry notifications during rendering/synchronization.
        if abs(node.x - x) < 0.001 and abs(node.y - y) < 0.001:
            return

        self.store.commit(MoveNode(node_id=node_id, x=x, y=y))

    def _node_selected(self, node_id: str, selected: bool) -> None:
        """Update presentation feedback for selection."""
        item = self._node_items.get(node_id)
        if item is None:
            return

        if selected:
            item.setPen(QPen(QColor("#58a6ff"), 2.0))
        else:
            item.setPen(QPen(QColor("#8c96a8"), 1.5))

    def _model_changed(self, model: VisualModel) -> None:
        """Synchronize the Qt scene to the current visual model."""
        self._suppress_item_callbacks = True

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
                        move_callback=self._node_moved,
                        select_callback=self._node_selected,
                    )

                    self._node_items[node_id] = item
                    self.scene.addItem(item)

                else:
                    if abs(item.rect().width() - node.width) > 0.001 or abs(
                        item.rect().height() - node.height
                    ) > 0.001:
                        item.setRect(0, 0, node.width, node.height)

                item.setPos(node.x, node.y)

                item.setSelected(
                    item.node_id
                    in {
                        selected.node_id
                        for selected in self.scene.selectedItems()
                        if isinstance(selected, NodeGraphicsItem)
                    }
                )

        finally:
            self._suppress_item_callbacks = False

    def wheelEvent(self, event: Any) -> None:
        """Zoom the canvas around the mouse position."""
        delta = event.angleDelta().y()

        if delta == 0:
            event.ignore()
            return

        factor = 1.15 if delta > 0 else 1 / 1.15

        self.view.scale(factor, factor)
        event.accept()

    def mousePressEvent(self, event: Any) -> None:
        """Provide middle-button panning for the canvas."""
        if event.button() == Qt.MouseButton.MiddleButton:
            self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            self.view.viewport().setCursor(Qt.CursorShape.ClosedHandCursor)
            self.view.mousePressEvent(event)
            return

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: Any) -> None:
        """Restore normal canvas interaction after panning."""
        if event.button() == Qt.MouseButton.MiddleButton:
            self.view.mouseReleaseEvent(event)
            self.view.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
            self.view.viewport().setCursor(Qt.CursorShape.ArrowCursor)
            return

        super().mouseReleaseEvent(event)