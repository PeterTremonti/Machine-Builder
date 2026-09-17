"""Node graphics for the Machine Structure Editor.

This module contains the Qt presentation class for a visual machine node.
The underlying node data remains in visual_model.py.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QPen,
)
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsSimpleTextItem,
)

from ..visual_model import VisualNode, VisualPort
from .port import PortGraphicsItem


class NodeGraphicsItem(QGraphicsRectItem):
    """Presentation object for one VisualNode."""

    _DEFAULT_BRUSH = QColor(
        "#2f3440"
    )

    _DEFAULT_PEN = QColor(
        "#8c96a8"
    )

    _DEFAULT_PEN_WIDTH = 1.5

    _CONTROLLER_PEN_WIDTH = 2.5

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
        port_edit_requested: Any,
        double_click_callback: Any | None = None,
    ) -> None:
        super().__init__(
            0,
            0,
            node.width,
            node.height,
        )

        self.node_id = node.id
        self._node_type = node.node_type

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

        self._port_edit_requested = (
            port_edit_requested
        )

        self._double_click_callback = (
            double_click_callback
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

        self.setAcceptHoverEvents(
            True
        )

        self.setBrush(
            QBrush(
                self._DEFAULT_BRUSH
            )
        )

        self._label_item = QGraphicsSimpleTextItem(
            node.label,
            self,
        )

        self._label_item.setBrush(
            QBrush(
                QColor("#f0f0f0")
            )
        )

        self._label_item.setPos(
            10,
            10,
        )

        self._apply_node_style(
            node
        )

        self.setPos(
            node.x,
            node.y,
        )

        self._rebuild_ports(
            node=node,
            connection_drag_started=(
                connection_drag_started
            ),
            connection_drag_moved=(
                connection_drag_moved
            ),
            connection_drag_finished=(
                connection_drag_finished
            ),
            port_edit_requested=(
                port_edit_requested
            ),
        )

    def _apply_node_style(
        self,
        node: VisualNode,
    ) -> None:
        """Apply presentation styling based on the visual node type."""
        pen_width = (
            self._CONTROLLER_PEN_WIDTH
            if node.node_type == "controller"
            else self._DEFAULT_PEN_WIDTH
        )

        self.setPen(
            QPen(
                self._DEFAULT_PEN,
                pen_width,
            )
        )

        font = QFont()

        font.setBold(
            node.node_type == "controller"
        )

        self._label_item.setFont(
            font
        )

    def _rebuild_ports(
        self,
        node: VisualNode,
        connection_drag_started: Any,
        connection_drag_moved: Any,
        connection_drag_finished: Any,
        port_edit_requested: Any,
    ) -> None:
        """Synchronize the node's visible ports and label with its model."""
        self._label_item.setText(
            node.label
        )

        self._apply_node_style(
            node
        )

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
                    connection_drag_started=(
                        connection_drag_started
                    ),
                    connection_drag_moved=(
                        connection_drag_moved
                    ),
                    connection_drag_finished=(
                        connection_drag_finished
                    ),
                    port_edit_requested=(
                        port_edit_requested
                    ),
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
        count = len(
            ports
        )

        if count == 0:
            return

        for index, port in enumerate(
            ports
        ):
            coordinate = (
                (index + 1)
                * (
                    (
                        height
                        if side in {
                            "left",
                            "right",
                        }
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

    def _activate_double_click(self) -> None:
        """Activate the controller editor from a controller node."""
        if (
            self._node_type != "controller"
            or self._double_click_callback is None
        ):
            return

        self._focus_callback(
            self.node_id
        )

        self.setSelected(
            True
        )

        self._double_click_callback()

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

    def mouseDoubleClickEvent(
        self,
        event: Any,
    ) -> None:
        """Open the controller editor when a controller node is double-clicked."""
        if (
            event.button()
            == Qt.MouseButton.LeftButton
        ):
            self._activate_double_click()

        super().mouseDoubleClickEvent(
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