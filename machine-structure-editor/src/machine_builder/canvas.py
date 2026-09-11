"""Main editor window and visual interaction layer.

The Qt scene is a renderer and interaction surface for the VisualModel.
It is not the authoritative data model.

Current interaction features:

* palette drag-and-drop
* double-click palette creation
* contextual component placement
* node movement with atomic undo
* multi-selection and atomic group movement
* atomic multi-delete
* canvas zoom/pan
* frame-all
* visual ports
* port hover feedback
* port-to-port connection dragging
* live connection preview
* compatibility feedback
* committed visual connections
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from PySide6.QtCore import QMimeData, QPointF, Qt
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QDrag,
    QDragEnterEvent,
    QDragMoveEvent,
    QDropEvent,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsLineItem,
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

from .compatibility import (
    CompatibilityResult,
    check_port_compatibility,
)
from .mutations import (
    CreateConnection,
    CreateNode,
    DeleteConnection,
    DeleteNodes,
    MoveNodes,
)
from .store import ModelStore
from .visual_model import (
    VisualConnection,
    VisualModel,
    VisualNode,
    VisualPort,
)


# ---------------------------------------------------------------------------
# Interaction state
# ---------------------------------------------------------------------------


@dataclass
class NodeDragState:
    """Temporary state for one continuous node-drag interaction."""

    node_ids: tuple[str, ...]
    start_positions: dict[str, tuple[float, float]]


@dataclass
class ConnectionDragState:
    """Temporary state for one continuous port connection interaction."""

    source_port_id: str
    current_scene_position: QPointF
    target_port_id: str | None = None


# ---------------------------------------------------------------------------
# Port graphics
# ---------------------------------------------------------------------------

class PortGraphicsItem(QGraphicsEllipseItem):
    """Presentation object for one VisualPort."""

    DIAMETER = 16.0

    NORMAL_FILL = QColor("#d7dde8")
    NORMAL_BORDER = QColor("#667085")

    HOVER_FILL = QColor("#58a6ff")
    HOVER_BORDER = QColor("#d7ecff")

    SOURCE_FILL = QColor("#f2c94c")
    SOURCE_BORDER = QColor("#fff3b0")

    VALID_FILL = QColor("#4caf50")
    VALID_BORDER = QColor("#d8ffd8")

    UNKNOWN_FILL = QColor("#9b8cff")
    UNKNOWN_BORDER = QColor("#ebe7ff")

    INVALID_FILL = QColor("#d9534f")
    INVALID_BORDER = QColor("#ffd7d5")

    def __init__(
        self,
        port: VisualPort,
        connection_drag_started: Any,
        connection_drag_moved: Any,
        connection_drag_finished: Any,
    ) -> None:
        radius = self.DIAMETER / 2.0

        super().__init__(
            -radius,
            -radius,
            self.DIAMETER,
            self.DIAMETER,
        )

        self.port_id = port.id
        self._side = port.side.lower().strip()

        self._connection_drag_started = (
            connection_drag_started
        )
        self._connection_drag_moved = (
            connection_drag_moved
        )
        self._connection_drag_finished = (
            connection_drag_finished
        )

        self._hovered = False
        self._connection_state: str = "normal"

        self.setBrush(
            QBrush(self.NORMAL_FILL)
        )
        self.setPen(
            QPen(
                self.NORMAL_BORDER,
                1.2,
            )
        )

        self.setZValue(20.0)

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable,
            False,
        )

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
            False,
        )

        self.setAcceptHoverEvents(True)

        self.setAcceptedMouseButtons(
            Qt.MouseButton.LeftButton
        )

        self.setToolTip(
            self._build_tooltip(port)
        )

        # Persistent port identity label.
        self._label_item = QGraphicsSimpleTextItem(
            port.label or "Interface",
            self,
        )
        self._label_item.setBrush(
            QBrush(
                QColor("#f0f0f0")
            )
        )
        self._label_item.setAcceptedMouseButtons(
            Qt.MouseButton.NoButton
        )

        # Non-color connection-status indicator.
        self._state_symbol = QGraphicsSimpleTextItem(
            "",
            self,
        )
        self._state_symbol.setBrush(
            QBrush(
                QColor("#20242b")
            )
        )
        self._state_symbol.setAcceptedMouseButtons(
            Qt.MouseButton.NoButton
        )
        self._state_symbol.setZValue(2.0)

        self._position_label()
        self._position_state_symbol()

    @staticmethod
    def _build_tooltip(
        port: VisualPort,
    ) -> str:
        """Build a concise tooltip describing the port."""
        lines = [
            port.label or "Interface",
            f"Type: {port.port_type}",
            f"Direction: {port.direction}",
        ]

        return "\n".join(lines)

    def _position_label(self) -> None:
        """Place the persistent label just outside the port."""
        label_rect = self._label_item.boundingRect()
        gap = 8.0

        if self._side == "left":
            self._label_item.setPos(
                -label_rect.width() - gap,
                -label_rect.height() / 2.0,
            )

        elif self._side == "right":
            self._label_item.setPos(
                gap,
                -label_rect.height() / 2.0,
            )

        elif self._side == "top":
            self._label_item.setPos(
                -label_rect.width() / 2.0,
                -label_rect.height() - gap,
            )

        elif self._side == "bottom":
            self._label_item.setPos(
                -label_rect.width() / 2.0,
                gap,
            )

        else:
            # Unknown presentation side: default to the right.
            self._label_item.setPos(
                gap,
                -label_rect.height() / 2.0,
            )

    def _position_state_symbol(self) -> None:
        """Center the non-color status symbol over the port."""
        symbol_rect = self._state_symbol.boundingRect()

        self._state_symbol.setPos(
            -symbol_rect.width() / 2.0,
            -symbol_rect.height() / 2.0 - 1.0,
        )

    def set_connection_state(
        self,
        state: str,
    ) -> None:
        """Set temporary connection feedback state."""
        self._connection_state = state
        self._apply_visual_state()

    def _apply_visual_state(self) -> None:
        """Apply color and non-color connection feedback."""
        if self._connection_state == "source":
            fill = self.SOURCE_FILL
            border = self.SOURCE_BORDER
            symbol = ""

        elif self._connection_state == "valid":
            fill = self.VALID_FILL
            border = self.VALID_BORDER
            symbol = "✓"

        elif self._connection_state == "unknown":
            fill = self.UNKNOWN_FILL
            border = self.UNKNOWN_BORDER
            symbol = "?"

        elif self._connection_state == "invalid":
            fill = self.INVALID_FILL
            border = self.INVALID_BORDER
            symbol = "×"

        elif self._hovered:
            fill = self.HOVER_FILL
            border = self.HOVER_BORDER
            symbol = ""

        else:
            fill = self.NORMAL_FILL
            border = self.NORMAL_BORDER
            symbol = ""

        self.setBrush(
            QBrush(fill)
        )

        self.setPen(
            QPen(
                border,
                1.5
                if self._connection_state != "normal"
                else 1.2,
            )
        )

        self._state_symbol.setText(symbol)
        self._position_state_symbol()

    def hoverEnterEvent(
        self,
        event: Any,
    ) -> None:
        """Highlight a port under the pointer."""
        self._hovered = True
        self._apply_visual_state()

        super().hoverEnterEvent(
            event
        )

    def hoverLeaveEvent(
        self,
        event: Any,
    ) -> None:
        """Restore the port appearance after hover."""
        self._hovered = False
        self._apply_visual_state()

        super().hoverLeaveEvent(
            event
        )

    def mousePressEvent(
        self,
        event: Any,
    ) -> None:
        """Start a connection directly from this port."""
        if (
            event.button()
            != Qt.MouseButton.LeftButton
        ):
            event.ignore()
            return

        event.accept()

        scene_position = event.scenePos()

        self._connection_drag_started(
            self.port_id,
            scene_position,
        )

    def mouseMoveEvent(
        self,
        event: Any,
    ) -> None:
        """Continue the connection preview."""
        if (
            event.buttons()
            & Qt.MouseButton.LeftButton
        ):
            event.accept()

            self._connection_drag_moved(
                self.port_id,
                event.scenePos(),
            )

            return

        super().mouseMoveEvent(
            event
        )

    def mouseReleaseEvent(
        self,
        event: Any,
    ) -> None:
        """Finish or cancel the connection attempt."""
        if (
            event.button()
            != Qt.MouseButton.LeftButton
        ):
            event.ignore()
            return

        event.accept()

        self._connection_drag_finished(
            self.port_id,
            event.scenePos(),
        )
        
# ---------------------------------------------------------------------------
# Connection graphics
# ---------------------------------------------------------------------------

class ConnectionGraphicsItem(QGraphicsLineItem):
    """Rendered representation of one committed VisualConnection."""

    NORMAL_COLOR = QColor("#aab4c4")
    SELECTED_COLOR = QColor("#58a6ff")

    def __init__(
        self,
        connection: VisualConnection,
        selection_callback: Any,
    ) -> None:
        super().__init__()

        self.connection_id = connection.id
        self.source_port_id = connection.source_port_id
        self.target_port_id = connection.target_port_id
        self._selection_callback = selection_callback

        self.setPen(
            QPen(
                self.NORMAL_COLOR,
                2.0,
            )
        )

        # Keep connections visually behind components and ports.
        self.setZValue(-10.0)

        # Connections now participate in mouse selection.
        self.setAcceptedMouseButtons(
            Qt.MouseButton.LeftButton
        )

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
            True,
        )

    def itemChange(
        self,
        change: QGraphicsItem.GraphicsItemChange,
        value: Any,
    ) -> Any:
        """Update the rendered selection state."""
        if (
            change
            == QGraphicsItem.GraphicsItemChange.ItemSelectedChange
        ):
            selected = bool(value)

            self.setPen(
                QPen(
                    self.SELECTED_COLOR
                    if selected
                    else self.NORMAL_COLOR,
                    3.0
                    if selected
                    else 2.0,
                )
            )

            self._selection_callback(
                self.connection_id,
                selected,
            )

        return super().itemChange(
            change,
            value,
        )

# ---------------------------------------------------------------------------
# Node graphics
# ---------------------------------------------------------------------------


class NodeGraphicsItem(QGraphicsRectItem):
    """Presentation object for one VisualNode."""

    def __init__(
        self,
        node: VisualNode,
        move_started_callback: Any,
        move_finished_callback: Any,
        selection_callback: Any,
        focus_callback: Any,
        position_changed_callback: Any,
        connection_drag_started: Any,
        connection_drag_moved: Any,
        connection_drag_finished: Any,
    ) -> None:
        super().__init__(
            0,
            0,
            node.width,
            node.height,
        )

        self.node_id = node.id

        self._move_started_callback = (
            move_started_callback
        )
        self._move_finished_callback = (
            move_finished_callback
        )
        self._selection_callback = (
            selection_callback
        )
        self._focus_callback = (
            focus_callback
        )
        self._position_changed_callback = (
            position_changed_callback
        )

        self._port_items: dict[
            str,
            PortGraphicsItem,
        ] = {}

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable,
            True,
        )

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
            True,
        )

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges,
            True,
        )

        self.setAcceptHoverEvents(True)

        self.setBrush(
            QBrush(
                QColor("#2f3440")
            )
        )

        self.setPen(
            QPen(
                QColor("#8c96a8"),
                1.5,
            )
        )

        self.setPos(
            node.x,
            node.y,
        )

        label = QGraphicsSimpleTextItem(
            node.label,
            self,
        )

        label.setBrush(
            QBrush(
                QColor("#f0f0f0")
            )
        )

        label.setPos(
            10,
            10,
        )

        self._rebuild_ports(
            node,
            connection_drag_started,
            connection_drag_moved,
            connection_drag_finished,
        )

    def _rebuild_ports(
        self,
        node: VisualNode,
        connection_drag_started: Any,
        connection_drag_moved: Any,
        connection_drag_finished: Any,
    ) -> None:
        """Synchronize the node's visible ports with its model ports."""
        current_ids = set(
            node.ports
        )

        existing_ids = set(
            self._port_items
        )

        for port_id in (
            existing_ids - current_ids
        ):
            item = self._port_items.pop(
                port_id
            )

            scene = self.scene()

            if scene is not None:
                scene.removeItem(
                    item
                )

        for port_id, port in node.ports.items():
            item = self._port_items.get(
                port_id
            )

            if item is None:
                item = PortGraphicsItem(
                    port=port,
                    connection_drag_started=connection_drag_started,
                    connection_drag_moved=connection_drag_moved,
                    connection_drag_finished=connection_drag_finished,
                )

                item.setParentItem(
                    self
                )

                self._port_items[
                    port_id
                ] = item

            else:
                item.setToolTip(
                    PortGraphicsItem._build_tooltip(
                        port
                    )
                )

        self._layout_ports(
            node
        )

    def _layout_ports(
        self,
        node: VisualNode,
    ) -> None:
        """Lay out each node's ports independently by side and order."""
        ports_by_side: dict[
            str,
            list[VisualPort],
        ] = {
            "left": [],
            "right": [],
            "top": [],
            "bottom": [],
        }

        for port in node.ports.values():
            side = port.side.lower()

            if side not in ports_by_side:
                side = "right"

            ports_by_side[
                side
            ].append(
                port
            )

        for side_ports in ports_by_side.values():
            side_ports.sort(
                key=lambda port: port.order
            )

        self._layout_side(
            ports_by_side["left"],
            "left",
            node.width,
            node.height,
        )

        self._layout_side(
            ports_by_side["right"],
            "right",
            node.width,
            node.height,
        )

        self._layout_side(
            ports_by_side["top"],
            "top",
            node.width,
            node.height,
        )

        self._layout_side(
            ports_by_side["bottom"],
            "bottom",
            node.width,
            node.height,
        )

    def _layout_side(
        self,
        ports: list[VisualPort],
        side: str,
        width: float,
        height: float,
    ) -> None:
        """Evenly distribute ports on one side of a node."""
        count = len(ports)

        if count == 0:
            return

        for index, port in enumerate(ports):
            coordinate = (
                (index + 1)
                * (
                    (
                        height
                        if side in {"left", "right"}
                        else width
                    )
                    / (count + 1)
                )
            )

            item = self._port_items.get(
                port.id
            )

            if item is None:
                continue

            if side == "left":
                item.setPos(
                    0.0,
                    coordinate,
                )

            elif side == "right":
                item.setPos(
                    width,
                    coordinate,
                )

            elif side == "top":
                item.setPos(
                    coordinate,
                    0.0,
                )

            elif side == "bottom":
                item.setPos(
                    coordinate,
                    height,
                )

    def mousePressEvent(
        self,
        event: Any,
    ) -> None:
        """Record the editing context before node movement begins."""
        if (
            event.button()
            == Qt.MouseButton.LeftButton
        ):
            self._focus_callback(
                self.node_id
            )

            self._move_started_callback(
                self.node_id
            )

        super().mousePressEvent(
            event
        )

    def mouseReleaseEvent(
        self,
        event: Any,
    ) -> None:
        """Commit the completed node movement."""
        super().mouseReleaseEvent(
            event
        )

        if (
            event.button()
            == Qt.MouseButton.LeftButton
        ):
            self._move_finished_callback(
                self.node_id
            )

    def itemChange(
        self,
        change: QGraphicsItem.GraphicsItemChange,
        value: Any,
    ) -> Any:
        """Synchronize selection and continuously update connections."""
        if (
            change
            == QGraphicsItem.GraphicsItemChange.ItemSelectedChange
        ):
            self._selection_callback(
                self.node_id,
                bool(value),
            )

        if (
            change
            == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged
        ):
            self._position_changed_callback(
                self.node_id
            )

        return super().itemChange(
            change,
            value,
        )


# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------


class PaletteList(QListWidget):
    """Palette supporting selection and drag-and-drop."""

    def startDrag(
        self,
        supported_actions: Any,
    ) -> None:
        """Start a drag containing the selected template ID."""
        item = self.currentItem()

        if item is None:
            return

        node_type = item.data(
            Qt.ItemDataRole.UserRole
        )

        if not isinstance(
            node_type,
            str,
        ):
            return

        mime_data = QMimeData()

        mime_data.setText(
            node_type
        )

        drag = QDrag(
            self
        )

        drag.setMimeData(
            mime_data
        )

        drag.exec(
            Qt.DropAction.CopyAction
        )


# ---------------------------------------------------------------------------
# Canvas
# ---------------------------------------------------------------------------


class MachineGraphicsView(QGraphicsView):
    """Interactive view providing zoom, pan, selection, and drops."""

    def __init__(
        self,
        scene: QGraphicsScene,
        canvas: "MachineCanvas",
    ) -> None:
        super().__init__(
            scene
        )

        self._canvas = canvas

        self._panning = False
        self._pan_start = QPointF()

        self.setAcceptDrops(
            True
        )

        self.viewport().setAcceptDrops(
            True
        )

        self.setDragMode(
            QGraphicsView.DragMode.RubberBandDrag
        )

        self.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        self.setRenderHint(
            QPainter.RenderHint.TextAntialiasing
        )

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

        self.setBackgroundBrush(
            QBrush(
                QColor("#17191e")
            )
        )

        self.setMouseTracking(
            True
        )

    def wheelEvent(
        self,
        event: Any,
    ) -> None:
        """Zoom smoothly around the mouse position."""
        delta = event.angleDelta().y()

        if delta == 0:
            event.ignore()
            return

        factor = (
            1.12
            if delta > 0
            else 1.0 / 1.12
        )

        self.scale(
            factor,
            factor,
        )

        event.accept()

    def mousePressEvent(
        self,
        event: Any,
    ) -> None:
        """Begin middle-button canvas panning."""
        if (
            event.button()
            == Qt.MouseButton.MiddleButton
        ):
            self._panning = True
            self._pan_start = event.position()

            self.viewport().setCursor(
                Qt.CursorShape.ClosedHandCursor
            )

            event.accept()
            return

        super().mousePressEvent(
            event
        )

    def mouseMoveEvent(
        self,
        event: Any,
    ) -> None:
        """Continue middle-button canvas panning."""
        if self._panning:
            current = event.position()
            delta = (
                current
                - self._pan_start
            )

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

        super().mouseMoveEvent(
            event
        )

    def mouseReleaseEvent(
        self,
        event: Any,
    ) -> None:
        """Finish middle-button canvas panning."""
        if (
            event.button()
            == Qt.MouseButton.MiddleButton
        ):
            self._panning = False

            self.viewport().setCursor(
                Qt.CursorShape.ArrowCursor
            )

            event.accept()
            return

        super().mouseReleaseEvent(
            event
        )

    def dragEnterEvent(
        self,
        event: QDragEnterEvent,
    ) -> None:
        """Accept palette drags containing a template ID."""
        if event.mimeData().hasText():
            event.acceptProposedAction()
            return

        event.ignore()

    def dragMoveEvent(
        self,
        event: QDragMoveEvent,
    ) -> None:
        """Keep palette drags accepted over the canvas."""
        if event.mimeData().hasText():
            event.acceptProposedAction()
            return

        event.ignore()

    def dropEvent(
        self,
        event: QDropEvent,
    ) -> None:
        """Create a node at the drop location."""
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


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------


class MachineCanvas(QMainWindow):
    """Main Machine Structure Editor window."""

    def __init__(
        self,
    ) -> None:
        super().__init__()

        self.store = ModelStore()

        self.store.subscribe(
            self._model_changed
        )

        self._node_items: dict[
            str,
            NodeGraphicsItem,
        ] = {}

        self._connection_items: dict[
            str,
            ConnectionGraphicsItem,
        ] = {}

        self._node_counter = 0

        self._last_edit_position = QPointF(
            100.0,
            100.0,
        )

        self._active_node_drag: NodeDragState | None = None

        self._active_connection_drag: ConnectionDragState | None = None

        self._connection_preview: QGraphicsLineItem | None = None

        self._active_connection_source: PortGraphicsItem | None = None

        self._active_connection_target: PortGraphicsItem | None = None

        self._synchronizing_scene = False

        self._build_ui()
        self._create_actions()

        self._model_changed(
            self.store.model
        )

    # ------------------------------------------------------------------
    # UI setup
    # ------------------------------------------------------------------

    def _build_ui(
        self,
    ) -> None:
        """Build the main editor window."""
        central = QWidget()

        self.setCentralWidget(
            central
        )

        main_layout = QHBoxLayout(
            central
        )

        main_layout.setContentsMargins(
            8,
            8,
            8,
            8,
        )

        main_layout.setSpacing(
            8
        )

        self.palette = PaletteList()

        self.palette.setMinimumWidth(
            180
        )

        self.palette.setDragEnabled(
            True
        )

        templates = (
            ("controller", "Controller"),
            ("motor", "Motor"),
            ("sensor", "Sensor"),
            ("component", "Component"),
            ("temperature_sensor", "Temperature Sensor"),
            ("temperature_controller", "Temperature Controller"),
        )

        for node_type, label in templates:
            item = QListWidgetItem(
                label
            )

            item.setData(
                Qt.ItemDataRole.UserRole,
                node_type,
            )

            self.palette.addItem(
                item
            )

        self.palette.itemDoubleClicked.connect(
            self._palette_item_double_clicked
        )

        palette_layout = QVBoxLayout()

        palette_title = QLabel(
            "Components"
        )

        palette_title.setStyleSheet(
            "font-weight: bold;"
        )

        add_button = QPushButton(
            "Add selected"
        )

        add_button.clicked.connect(
            self._add_selected_palette_item
        )

        palette_help = QLabel(
            "Double-click or drag a component onto the canvas."
        )

        palette_help.setWordWrap(
            True
        )

        palette_layout.addWidget(
            palette_title
        )

        palette_layout.addWidget(
            self.palette
        )

        palette_layout.addWidget(
            add_button
        )

        palette_layout.addWidget(
            palette_help
        )

        palette_panel = QWidget()

        palette_panel.setLayout(
            palette_layout
        )

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

        main_layout.addWidget(
            palette_panel
        )

        main_layout.addWidget(
            self.view,
            1,
        )

        self.statusBar().showMessage(
            "Ready"
        )

    def _create_actions(
        self,
    ) -> None:
        """Create editor actions and shortcuts."""
        delete_action = QAction(
            "Delete",
            self,
        )

        delete_action.setShortcut(
            Qt.Key.Key_Delete
        )

        delete_action.triggered.connect(
            self._delete_selected
        )

        undo_action = QAction(
            "Undo",
            self,
        )

        undo_action.setShortcut(
            "Ctrl+Z"
        )

        undo_action.triggered.connect(
            self.store.undo
        )

        redo_action = QAction(
            "Redo",
            self,
        )

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

        self.addAction(
            delete_action
        )

        self.addAction(
            undo_action
        )

        self.addAction(
            redo_action
        )

        self.addAction(
            frame_action
        )

    # ------------------------------------------------------------------
    # Palette / node creation
    # ------------------------------------------------------------------

    def _palette_item_double_clicked(
        self,
        item: QListWidgetItem,
    ) -> None:
        """Create a node from a double-clicked palette entry."""
        node_type = item.data(
            Qt.ItemDataRole.UserRole
        )

        if not isinstance(
            node_type,
            str,
        ):
            return

        self.create_node_from_template(
            node_type=node_type,
            scene_position=self._suggest_new_node_position(),
        )

    def _add_selected_palette_item(
        self,
    ) -> None:
        """Create a node from the currently selected palette entry."""
        item = self.palette.currentItem()

        if item is None:
            return

        node_type = item.data(
            Qt.ItemDataRole.UserRole
        )

        if not isinstance(
            node_type,
            str,
        ):
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
        """Create a provisional visual node."""
        labels = {
            "controller": "Controller",
            "motor": "Motor",
            "sensor": "Sensor",
            "component": "Component",
            "temperature_sensor": "Temperature Sensor",
            "temperature_controller": "Temperature Controller",
        }

        label = labels.get(
            node_type,
            node_type.replace(
                "_",
                " ",
            ).title(),
        )

        self._node_counter += 1

        node = VisualNode(
            id=f"node-{self._node_counter}",
            node_type=node_type,
            label=label,
            x=scene_position.x(),
            y=scene_position.y(),
        )

        self._add_default_ports(
            node
        )

        self.store.commit(
            CreateNode(
                node
            )
        )

        self._last_edit_position = QPointF(
            scene_position
        )

        self.statusBar().showMessage(
            f"Created {label}"
        )

    def _add_default_ports(
        self,
        node: VisualNode,
    ) -> None:
        """Add deliberately provisional prototype ports."""
        if node.node_type == "controller":
            ports = (
                VisualPort(
                    id=f"{node.id}-power",
                    node_id=node.id,
                    label="Power",
                    port_type="power",
                    direction="input",
                    side="left",
                    order=0,
                ),
                VisualPort(
                    id=f"{node.id}-motor",
                    node_id=node.id,
                    label="Motor",
                    port_type="signal",
                    direction="output",
                    side="right",
                    order=0,
                ),
                VisualPort(
                    id=f"{node.id}-aux",
                    node_id=node.id,
                    label="Aux",
                    port_type="signal",
                    direction="bidirectional",
                    side="right",
                    order=1,
                ),
            )

        elif node.node_type == "motor":
            ports = (
                VisualPort(
                    id=f"{node.id}-power",
                    node_id=node.id,
                    label="Power",
                    port_type="power",
                    direction="input",
                    side="left",
                    order=0,
                ),
                VisualPort(
                    id=f"{node.id}-signal",
                    node_id=node.id,
                    label="Signal",
                    port_type="signal",
                    direction="input",
                    side="left",
                    order=1,
                ),
            )

        elif node.node_type == "sensor":
            ports = (
                VisualPort(
                    id=f"{node.id}-power",
                    node_id=node.id,
                    label="Power",
                    port_type="power",
                    direction="input",
                    side="left",
                    order=0,
                ),
                VisualPort(
                    id=f"{node.id}-signal",
                    node_id=node.id,
                    label="Signal",
                    port_type="signal",
                    direction="output",
                    side="right",
                    order=0,
                ),
            )

        elif node.node_type == "temperature_sensor":
            ports = (
                VisualPort(
                    id=f"{node.id}-ground",
                    node_id=node.id,
                    label="Reference / Ground",
                    port_type="electrical",
                    direction="bidirectional",
                    side="left",
                    order=0,
                ),
                VisualPort(
                    id=f"{node.id}-temperature",
                    node_id=node.id,
                    label="Temperature Output",
                    port_type="signal",
                    direction="output",
                    side="right",
                    order=0,
                ),
            )

        elif node.node_type == "temperature_controller":
            ports = (
                VisualPort(
                    id=f"{node.id}-power",
                    node_id=node.id,
                    label="Power Input",
                    port_type="electrical",
                    direction="input",
                    side="left",
                    order=0,
                ),
                VisualPort(
                    id=f"{node.id}-temperature",
                    node_id=node.id,
                    label="Temperature Input",
                    port_type="signal",
                    direction="input",
                    side="right",
                    order=0,
                ),
            )

        else:
            ports = (
                VisualPort(
                    id=f"{node.id}-port",
                    node_id=node.id,
                    label="Interface",
                    port_type="unknown",
                    direction="unknown",
                    side="right",
                    order=0,
                ),
            )

        for port in ports:
            node.add_port(
                port
            )

    def _suggest_new_node_position(
        self,
    ) -> QPointF:
        """Choose a location near the current editing context."""
        if not self.store.model.nodes:
            return QPointF(
                100.0,
                100.0,
            )

        return QPointF(
            self._last_edit_position.x()
            + 40.0,
            self._last_edit_position.y()
            + 40.0,
        )

    # ------------------------------------------------------------------
    # Node editing
    # ------------------------------------------------------------------

def _delete_selected(
    self,
) -> None:
    """Delete the currently selected connection or nodes."""
    selected_connections = tuple(
        item.connection_id
        for item in self.scene.selectedItems()
        if isinstance(
            item,
            ConnectionGraphicsItem,
        )
    )

    if selected_connections:
        for connection_id in selected_connections:
            self.store.commit(
                DeleteConnection(
                    connection_id=connection_id
                )
            )

        count = len(selected_connections)

        self.statusBar().showMessage(
            f"Deleted {count} connection"
            + (
                ""
                if count == 1
                else "s"
            )
        )

        return

    selected_ids = tuple(
        item.node_id
        for item in self.scene.selectedItems()
        if isinstance(
            item,
            NodeGraphicsItem,
        )
    )

    if not selected_ids:
        return

    self.store.commit(
        DeleteNodes(
            node_ids=selected_ids
        )
    )

    self.statusBar().showMessage(
        f"Deleted {len(selected_ids)} node"
        + (
            ""
            if len(selected_ids) == 1
            else "s"
        )
    )

    def _focus_node(
        self,
        node_id: str,
    ) -> None:
        """Make one node the current editing context."""
        node = self.store.model.nodes.get(
            node_id
        )

        if node is None:
            return

        self._last_edit_position = QPointF(
            node.x,
            node.y,
        )

    def _begin_node_move(
        self,
        node_id: str,
    ) -> None:
        """Begin one node/group movement action."""
        if self._synchronizing_scene:
            return

        if self._active_connection_drag is not None:
            return

        node = self.store.model.nodes.get(
            node_id
        )

        if node is None:
            return

        selected_nodes = [
            item
            for item in self.scene.selectedItems()
            if isinstance(
                item,
                NodeGraphicsItem,
            )
        ]

        selected_ids = {
            item.node_id
            for item in selected_nodes
        }

        if node_id not in selected_ids:
            selected_nodes = [
                self._node_items[node_id]
            ]

        node_ids = tuple(
            item.node_id
            for item in selected_nodes
        )

        start_positions = {
            item.node_id: (
                self.store.model.nodes[
                    item.node_id
                ].x,
                self.store.model.nodes[
                    item.node_id
                ].y,
            )
            for item in selected_nodes
        }

        self._active_node_drag = NodeDragState(
            node_ids=node_ids,
            start_positions=start_positions,
        )

    def _finish_node_move(
        self,
        node_id: str,
    ) -> None:
        """Commit the completed node/group movement."""
        if (
            self._active_node_drag is None
            or self._synchronizing_scene
        ):
            return

        drag = self._active_node_drag

        final_positions: dict[
            str,
            tuple[float, float],
        ] = {}

        for dragged_id in drag.node_ids:
            item = self._node_items.get(
                dragged_id
            )

            if item is None:
                continue

            position = item.pos()

            final_positions[
                dragged_id
            ] = (
                position.x(),
                position.y(),
            )

        changed = any(
            abs(
                final_positions[node_id][0]
                - start[0]
            ) > 0.001
            or abs(
                final_positions[node_id][1]
                - start[1]
            ) > 0.001
            for node_id, start
            in drag.start_positions.items()
            if node_id in final_positions
        )

        if changed:
            self.store.commit(
                MoveNodes(
                    positions=final_positions
                )
            )

            moved_ids = tuple(
                final_positions
            )

            if moved_ids:
                last_id = moved_ids[-1]

                last_x, last_y = (
                    final_positions[
                        last_id
                    ]
                )

                self._last_edit_position = QPointF(
                    last_x,
                    last_y,
                )

        self._active_node_drag = None

    def _node_selected(
        self,
        node_id: str,
        selected: bool,
    ) -> None:
        """Update node selection appearance."""
        item = self._node_items.get(
            node_id
        )

        if item is None:
            return

        if selected:
            item.setPen(
                QPen(
                    QColor("#58a6ff"),
                    2.0,
                )
            )

            self._focus_node(
                node_id
            )

        else:
            item.setPen(
                QPen(
                    QColor("#8c96a8"),
                    1.5,
                )
            )

def _connection_selected(
    self,
    connection_id: str,
    selected: bool,
) -> None:
    """Update the current connection selection state."""
    if selected:
        connection = self.store.model.connections.get(
            connection_id
        )

        if connection is not None:
            source = self.store.model.find_port(
                connection.source_port_id
            )
            target = self.store.model.find_port(
                connection.target_port_id
            )

            if source is not None and target is not None:
                self.statusBar().showMessage(
                    f"Selected connection: "
                    f"{source.label} ↔ {target.label}"
                )
        else:
            self.statusBar().showMessage(
                "Selected connection"
            )

    def _node_position_changed(
        self,
        node_id: str,
    ) -> None:
        """Update connection graphics while a node is being moved."""
        self._update_connection_graphics()

    # ------------------------------------------------------------------
    # Port connections
    # ------------------------------------------------------------------

    def _start_connection_drag(
        self,
        source_port_id: str,
        scene_position: QPointF,
    ) -> None:
        """Begin a temporary connection preview from a port."""
        if self._synchronizing_scene:
            return

        source_port = self.store.model.find_port(
            source_port_id
        )

        if source_port is None:
            return

        if self._active_connection_drag is not None:
            self._cancel_connection_drag()
        
        source_item = self._find_port_graphics_item(
            source_port_id
        )

        if source_item is None:
            return

        self._active_connection_drag = (
            ConnectionDragState(
                source_port_id=source_port_id,
                current_scene_position=QPointF(
                    scene_position
                ),
            )
        )

        self._active_connection_source = (
            source_item
        )

        source_item.set_connection_state(
            "source"
        )

        preview = QGraphicsLineItem()

        preview.setPen(
            QPen(
                QColor("#f2c94c"),
                2.0,
                Qt.PenStyle.DashLine,
            )
        )

        preview.setZValue(
            5.0
        )

        preview.setAcceptedMouseButtons(
            Qt.MouseButton.NoButton
        )

        self.scene.addItem(
            preview
        )

        self._connection_preview = (
            preview
        )

        self._update_connection_preview(
            scene_position
        )

        self.statusBar().showMessage(
            f"Connecting from {source_port.label}"
        )

    def _move_connection_drag(
        self,
        source_port_id: str,
        scene_position: QPointF,
    ) -> None:
        """Update the live connection preview and target feedback."""
        drag = self._active_connection_drag

        if drag is None:
            return

        if (
            drag.source_port_id
            != source_port_id
        ):
            return

        drag.current_scene_position = QPointF(
            scene_position
        )

        self._update_connection_preview(
            scene_position
        )

        target_item = self._find_port_graphics_at(
            scene_position
        )

        if (
            target_item is not None
            and target_item
            is self._active_connection_source
        ):
            target_item = None

        if (
            target_item
            is not self._active_connection_target
        ):
            if self._active_connection_target is not None:
                self._active_connection_target.set_connection_state(
                    "normal"
                )

            self._active_connection_target = (
                target_item
            )

        if target_item is None:
            if self._active_connection_source is not None:
                self._active_connection_source.set_connection_state(
                    "source"
                )

            self.statusBar().showMessage(
                "Connecting..."
            )

            return

        source_port = self.store.model.find_port(
            drag.source_port_id
        )

        target_port = self.store.model.find_port(
            target_item.port_id
        )

        if (
            source_port is None
            or target_port is None
        ):
            return

        result = check_port_compatibility(
            source_port,
            target_port,
        )

        if result == CompatibilityResult.COMPATIBLE:
            target_item.set_connection_state(
                "valid"
            )

            message = (
                f"Compatible: "
                f"{source_port.label} → "
                f"{target_port.label}"
            )

        elif result == CompatibilityResult.UNKNOWN:
            target_item.set_connection_state(
                "unknown"
            )

            message = (
                f"Unknown compatibility: "
                f"{source_port.label} → "
                f"{target_port.label}"
            )

        elif result == CompatibilityResult.CONDITIONAL:
            target_item.set_connection_state(
                "unknown"
            )

            message = (
                f"Conditional compatibility: "
                f"{source_port.label} → "
                f"{target_port.label}"
            )

        else:
            target_item.set_connection_state(
                "invalid"
            )

            message = (
                f"Incompatible: "
                f"{source_port.label} → "
                f"{target_port.label}"
            )

        self.statusBar().showMessage(
            message
        )

    def _finish_connection_drag(
        self,
        source_port_id: str,
        scene_position: QPointF,
    ) -> None:
        """Commit a valid connection or cancel the preview."""
        drag = self._active_connection_drag

        if drag is None:
            return

        target_item = self._find_port_graphics_at(
            scene_position
        )

        target_port_id = (
            target_item.port_id
            if target_item is not None
            else None
        )

        source_port = self.store.model.find_port(
            drag.source_port_id
        )

        target_port = (
            self.store.model.find_port(
                target_port_id
            )
            if target_port_id is not None
            else None
        )

        if (
            source_port is not None
            and target_port is not None
        ):
            result = check_port_compatibility(
                source_port,
                target_port,
            )

            if result == CompatibilityResult.COMPATIBLE:
                existing = any(
                    connection.source_port_id
                    == source_port.id
                    and connection.target_port_id
                    == target_port.id
                    for connection
                    in self.store.model.connections.values()
                )

                if not existing:
                    connection_id = (
                        f"connection-"
                        f"{len(self.store.model.connections) + 1}"
                    )

                    self.store.commit(
                        CreateConnection(
                            connection_id=connection_id,
                            source_port_id=source_port.id,
                            target_port_id=target_port.id,
                            connection_type=source_port.port_type,
                        )
                    )

                    self.statusBar().showMessage(
                        f"Connected: "
                        f"{source_port.label} → "
                        f"{target_port.label}"
                    )

                else:
                    self.statusBar().showMessage(
                        "That connection already exists."
                    )

            elif result == CompatibilityResult.UNKNOWN:
                self.statusBar().showMessage(
                    "Connection not committed: compatibility is unknown."
                )

            elif result == CompatibilityResult.CONDITIONAL:
                self.statusBar().showMessage(
                    "Connection not committed: compatibility is conditional."
                )

            else:
                self.statusBar().showMessage(
                    "Connection rejected: incompatible ports."
                )

        else:
            self.statusBar().showMessage(
                "Connection cancelled."
            )

        self._cancel_connection_drag(
            preserve_status=True
        )

    def _cancel_connection_drag(
        self,
        preserve_status: bool = False,
    ) -> None:
        """Remove the temporary connection state."""
        if self._active_connection_target is not None:
            self._active_connection_target.set_connection_state(
                "normal"
            )

        if self._active_connection_source is not None:
            self._active_connection_source.set_connection_state(
                "normal"
            )

        if self._connection_preview is not None:
            self.scene.removeItem(
                self._connection_preview
            )

        self._connection_preview = None
        self._active_connection_source = None
        self._active_connection_target = None
        self._active_connection_drag = None

        if not preserve_status:
            self.statusBar().showMessage(
                "Ready"
            )

    def _update_connection_preview(
        self,
        scene_position: QPointF,
    ) -> None:
        """Draw the temporary line from source port to cursor."""
        drag = self._active_connection_drag

        preview = self._connection_preview

        if (
            drag is None
            or preview is None
        ):
            return

        source_item = self._find_port_graphics_item(
            drag.source_port_id
        )

        if source_item is None:
            return

        start = source_item.scenePos()
        end = QPointF(
            scene_position
        )

        preview.setLine(
            start.x(),
            start.y(),
            end.x(),
            end.y(),
        )

    def _find_port_graphics_item(
        self,
        port_id: str,
    ) -> PortGraphicsItem | None:
        """Find the rendered port for a visual port ID."""
        for node_item in self._node_items.values():
            port_item = node_item._port_items.get(
                port_id
            )

            if port_item is not None:
                return port_item

        return None

    def _find_port_graphics_at(
        self,
        scene_position: QPointF,
    ) -> PortGraphicsItem | None:
        """Find a port directly under the pointer."""
        items = self.scene.items(
            scene_position
        )

        for item in items:
            if isinstance(
                item,
                PortGraphicsItem,
            ):
                return item

        return None

    # ------------------------------------------------------------------
    # Connection rendering
    # ------------------------------------------------------------------

    def _update_connection_graphics(
        self,
    ) -> None:
        """Recalculate all committed connection lines."""
        for connection_id, graphics in (
            self._connection_items.items()
        ):
            connection = (
                self.store.model.connections.get(
                    connection_id
                )
            )

            if connection is None:
                continue

            source_item = (
                self._find_port_graphics_item(
                    connection.source_port_id
                )
            )

            target_item = (
                self._find_port_graphics_item(
                    connection.target_port_id
                )
            )

            if (
                source_item is None
                or target_item is None
            ):
                continue

            start = source_item.scenePos()
            end = target_item.scenePos()

            graphics.setLine(
                start.x(),
                start.y(),
                end.x(),
                end.y(),
            )

    # ------------------------------------------------------------------
    # Model → renderer synchronization
    # ------------------------------------------------------------------

    def _model_changed(
        self,
        model: VisualModel,
    ) -> None:
        """Synchronize the Qt scene with the visual model."""
        self._synchronizing_scene = True

        try:
            current_node_ids = set(
                model.nodes
            )

            existing_node_ids = set(
                self._node_items
            )

            for node_id in (
                existing_node_ids
                - current_node_ids
            ):
                item = self._node_items.pop(
                    node_id
                )

                self.scene.removeItem(
                    item
                )

            current_connection_ids = set(
                model.connections
            )

            existing_connection_ids = set(
                self._connection_items
            )

            for connection_id in (
                existing_connection_ids
                - current_connection_ids
            ):
                item = self._connection_items.pop(
                    connection_id
                )

                self.scene.removeItem(
                    item
                )

            for node_id, node in (
                model.nodes.items()
            ):
                item = self._node_items.get(
                    node_id
                )

                if item is None:
                    item = NodeGraphicsItem(
                        node=node,
                        move_started_callback=self._begin_node_move,
                        move_finished_callback=self._finish_node_move,
                        selection_callback=self._node_selected,
                        focus_callback=self._focus_node,
                        position_changed_callback=self._node_position_changed,
                        connection_drag_started=self._start_connection_drag,
                        connection_drag_moved=self._move_connection_drag,
                        connection_drag_finished=self._finish_connection_drag,
                    )

                    self._node_items[
                        node_id
                    ] = item

                    self.scene.addItem(
                        item
                    )

                else:
                    item.setRect(
                        0,
                        0,
                        node.width,
                        node.height,
                    )

                    item._rebuild_ports(
                        node=node,
                        connection_drag_started=self._start_connection_drag,
                        connection_drag_moved=self._move_connection_drag,
                        connection_drag_finished=self._finish_connection_drag,
                    )

                item.setPos(
                    node.x,
                    node.y,
                )

            for connection_id, connection in (
                model.connections.items()
            ):
                graphics = (
                    self._connection_items.get(
                        connection_id
                    )
                )

                if graphics is None:
                    graphics = ConnectionGraphicsItem(
                        connection=connection,
                        selection_callback=self._connection_selected,
                    )

                    self._connection_items[
                        connection_id
                    ] = graphics

                    self.scene.addItem(
                        graphics
                    )

            self._update_connection_graphics()

        finally:
            self._synchronizing_scene = False

    # ------------------------------------------------------------------
    # View
    # ------------------------------------------------------------------

    def _frame_all(
        self,
    ) -> None:
        """Fit all current objects into the visible canvas."""
        if not self.store.model.nodes:
            return

        bounds = (
            self.scene.itemsBoundingRect()
        )

        if bounds.isNull():
            return

        bounds = bounds.adjusted(
            -100,
            -100,
            100,
            100,
        )

        self.view.fitInView(
            bounds,
            Qt.AspectRatioMode.KeepAspectRatio,
        )