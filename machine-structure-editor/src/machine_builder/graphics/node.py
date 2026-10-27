"""Node graphics for the Machine Structure Editor.

This module contains the Qt presentation class for a visual machine node.
The underlying node data remains in visual_model.py.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QPainterPath,
    QPen,
)
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsPathItem,
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
        self._base_width = float(node.width)
        self._base_height = float(node.height)
        self._visual_ports = dict(node.ports)
        self._controller_focus_active = False
        self._focused_port_ids: set[str] = set()

        self._connector_group_info: dict[str, Any] | None = None
        self._connector_group_original_labels: dict[str, str] = {}
        self._connector_group_anchor_local: QPointF | None = None
        self._connector_group_endpoint_port_id: str | None = None

        self._connector_group_cone = QGraphicsPathItem(self)
        self._connector_group_cone.setBrush(
            QBrush(QColor(165, 178, 196, 75))
        )
        self._connector_group_cone.setPen(
            QPen(QColor(185, 198, 215, 130), 1.0)
        )
        self._connector_group_cone.setZValue(4.0)
        self._connector_group_cone.setAcceptedMouseButtons(
            Qt.MouseButton.NoButton
        )
        self._connector_group_cone.setVisible(False)

        self._connector_group_box = QGraphicsPathItem(self)
        self._connector_group_box.setBrush(
            QBrush(QColor(47, 55, 68, 205))
        )
        self._connector_group_box.setPen(
            QPen(QColor(183, 197, 216, 220), 1.3)
        )
        self._connector_group_box.setZValue(5.0)
        self._connector_group_box.setAcceptedMouseButtons(
            Qt.MouseButton.NoButton
        )
        self._connector_group_box.setVisible(False)

        self._connector_group_title = QGraphicsSimpleTextItem("", self)
        self._connector_group_title.setBrush(
            QBrush(QColor("#f0f0f0"))
        )
        self._connector_group_title.setZValue(7.0)
        self._connector_group_title.setAcceptedMouseButtons(
            Qt.MouseButton.NoButton
        )
        self._connector_group_title.setVisible(False)

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

        self._visual_ports = dict(node.ports)
        self._layout_ports(
            node
        )
        if self._controller_focus_active:
            self._apply_controller_port_focus()

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

    def set_controller_port_focus(
        self,
        visible_port_ids: set[str],
        connector_group_info: dict[str, Any] | None = None,
    ) -> None:
        """Apply presentation-only port focus and optional connector grouping."""
        self._controller_focus_active = True
        self._focused_port_ids = set(visible_port_ids)
        self._connector_group_info = connector_group_info
        self._apply_controller_port_focus()

    def _apply_controller_port_focus(self) -> None:
        """Hide off-focus ports and lay out the selected contact group."""
        if not self._controller_focus_active:
            return

        visible_ids = self._focused_port_ids.intersection(self._port_items)
        for port_id, item in self._port_items.items():
            item.setVisible(port_id in visible_ids)

        focused_ports = [
            self._visual_ports[port_id]
            for port_id in visible_ids
            if port_id in self._visual_ports
        ]
        if not focused_ports:
            self.setRect(0.0, 0.0, self._base_width, self._base_height)
            self._update_connector_group_overlay()
            return

        by_side = {
            "left": [],
            "right": [],
            "top": [],
            "bottom": [],
        }
        group_info = self._connector_group_info or {}
        grouped_port_ids = set(group_info.get("pins", {}))
        group_side_override = group_info.get("port_side_override")
        if group_side_override not in {"left", "right"}:
            group_side_override = None

        for port in focused_ports:
            side = port.side.lower()
            if port.id in grouped_port_ids and group_side_override is not None:
                side = group_side_override
            if side not in by_side:
                side = "right"
            by_side[side].append(port)

        for ports in by_side.values():
            ports.sort(key=lambda port: (port.order, port.id))

        width = max(
            self._base_width,
            48.0 + 34.0 * max(
                len(by_side["top"]),
                len(by_side["bottom"]),
            ),
        )
        height = max(
            self._base_height,
            48.0 + 34.0 * max(
                len(by_side["left"]),
                len(by_side["right"]),
            ),
        )
        self.setRect(0.0, 0.0, width, height)

        self._layout_side(by_side["left"], "left", width, height)
        self._layout_side(by_side["right"], "right", width, height)
        self._layout_side(by_side["top"], "top", width, height)
        self._layout_side(by_side["bottom"], "bottom", width, height)
        self._update_connector_group_overlay()

    def _hide_connector_group_overlay(self) -> None:
        for port_id, original_text in self._connector_group_original_labels.items():
            item = self._port_items.get(port_id)
            label_item = getattr(item, "_label_item", None) if item else None
            if label_item is not None:
                label_item.setText(original_text)

        self._connector_group_original_labels.clear()
        self._connector_group_box.setVisible(False)
        self._connector_group_title.setVisible(False)
        self._connector_group_cone.setVisible(False)
        self._connector_group_anchor_local = None
        self._connector_group_endpoint_port_id = None
        self._connector_group_contact_anchors_local = {}

    def _update_connector_group_overlay(self) -> None:
        """Draw one connector enclosure and, if connected, one neutral cone."""
        info = self._connector_group_info
        if not info or not self._controller_focus_active:
            self._hide_connector_group_overlay()
            return

        pins = info.get("pins", {})
        bounds = None
        for port_id, pin_info in pins.items():
            item = self._port_items.get(port_id)
            if item is None or not item.isVisible():
                continue

            label_item = getattr(item, "_label_item", None)
            if label_item is not None:
                if port_id not in self._connector_group_original_labels:
                    self._connector_group_original_labels[port_id] = (
                        label_item.text()
                    )
                pin_label = str(pin_info.get("pin_label") or "Contact")
                purpose = str(pin_info.get("purpose") or "").strip()
                label_item.setText(pin_label)
                label_item.setToolTip(
                    f"{pin_label} — {purpose}" if purpose else pin_label
                )

            item_bounds = item.mapRectToParent(item.boundingRect())
            bounds = (
                item_bounds
                if bounds is None
                else bounds.united(item_bounds)
            )
            if label_item is not None:
                label_bounds = label_item.mapRectToItem(
                    self, label_item.boundingRect()
                )
                bounds = bounds.united(label_bounds)

        if bounds is None:
            self._hide_connector_group_overlay()
            return

        title = str(info.get("title") or "Connector")
        self._connector_group_title.setText(title)
        box = bounds.adjusted(-8.0, -24.0, 8.0, 8.0)
        minimum_width = self._connector_group_title.boundingRect().width() + 16.0
        if box.width() < minimum_width:
            box.setWidth(minimum_width)

        # Keep the connector enclosure inside the board and clear of its title.
        node_bounds = self.rect().adjusted(4.0, 4.0, -4.0, -4.0)
        title_bounds = self._label_item.mapRectToParent(
            self._label_item.boundingRect()
        )
        box_top = max(node_bounds.top(), title_bounds.bottom() + 8.0)
        available_height = max(1.0, node_bounds.bottom() - box_top)
        box.setWidth(min(box.width(), node_bounds.width()))
        box.setHeight(min(box.height(), available_height))
        box.moveLeft(
            min(max(box.left(), node_bounds.left()), node_bounds.right() - box.width())
        )
        box.moveTop(
            min(max(box.top(), box_top), node_bounds.bottom() - box.height())
        )

        enclosure_path = QPainterPath()
        enclosure_path.addRect(box)
        self._connector_group_box.setPath(enclosure_path)
        self._connector_group_title.setPos(
            box.left() + 8.0,
            box.top() + 3.0,
        )
        self._connector_group_box.setVisible(True)
        self._connector_group_title.setVisible(True)

        connected = bool(info.get("connected"))
        direction = "left" if info.get("direction") == "left" else "right"
        center_y = box.center().y()
        base_top = min(box.bottom() - 8.0, box.top() + 28.0)
        base_bottom = max(box.top() + 28.0, box.bottom() - 8.0)
        base_x = box.left() if direction == "left" else box.right()
        tip_x = base_x - 112.0 if direction == "left" else base_x + 112.0

        path = QPainterPath()
        path.moveTo(QPointF(tip_x, center_y))
        path.lineTo(QPointF(base_x, base_top))
        path.lineTo(QPointF(base_x, base_bottom))
        path.closeSubpath()
        self._connector_group_cone.setPath(path)
        self._connector_group_cone.setVisible(connected)

        self._connector_group_anchor_local = (
            QPointF(tip_x, center_y) if connected else None
        )
        self._connector_group_endpoint_port_id = (
            info.get("endpoint_port_id") if connected else None
        )

        # Preserve each contact's actual breakout-port position for its
        # transient colored conductor. External connections share the cone tip.
        contact_anchors: dict[str, QPointF] = {}
        if connected:
            for visual_port_id, pin_info in pins.items():
                semantic_port_id = str(
                    pin_info.get("semantic_port_id") or ""
                ).strip()
                item = self._port_items.get(visual_port_id)
                if not semantic_port_id or item is None:
                    continue
                contact_anchors[semantic_port_id] = item.mapToItem(
                    self,
                    item.boundingRect().center(),
                )

        self._connector_group_contact_anchors_local = contact_anchors

    def connector_group_anchor_for_port(
        self,
        semantic_port_id: str,
    ) -> QPointF | None:
        """Return the shared cone tip for ports in the focused connector group."""
        if (
            self._connector_group_anchor_local is None
            or not self._connector_group_cone.isVisible()
        ):
            return None

        contact_anchors = getattr(
            self, "_connector_group_contact_anchors_local", {}
        )
        if (
            semantic_port_id != self._connector_group_endpoint_port_id
            and semantic_port_id not in contact_anchors
        ):
            return None

        return self.mapToScene(self._connector_group_anchor_local)

    def connector_group_contact_origin_for_port(
        self,
        semantic_port_id: str,
    ) -> QPointF | None:
        """Return the actual focused breakout-contact position in scene space."""
        if not self._connector_group_cone.isVisible():
            return None
        local_origin = getattr(
            self, "_connector_group_contact_anchors_local", {}
        ).get(semantic_port_id)
        if local_origin is None:
            return None
        return self.mapToScene(local_origin)

    def connector_group_endpoint_side_for_port(
        self,
        semantic_port_id: str,
    ) -> str | None:
        if not self._connector_group_cone.isVisible():
            return None
        contact_anchors = getattr(
            self,
            "_connector_group_contact_anchors_local",
            {},
        )
        if (
            semantic_port_id != self._connector_group_endpoint_port_id
            and semantic_port_id not in contact_anchors
        ):
            return None
        return (
            "left"
            if self._connector_group_info
            and self._connector_group_info.get("direction") == "left"
            else "right"
        )

    def connector_group_overlay_bounds(self):
        """Return scene bounds for visible group graphics, if any."""
        if not self._connector_group_box.isVisible():
            return None
        bounds = self._connector_group_box.path().boundingRect()
        if self._connector_group_cone.isVisible():
            bounds = bounds.united(
                self._connector_group_cone.path().boundingRect()
            )
        return self.mapRectToScene(bounds)

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
            if side in {"left", "right"}:
                start_margin = 64.0
                end_margin = 18.0
                if count == 1:
                    coordinate = (start_margin + height - end_margin) / 2.0
                else:
                    coordinate = start_margin + index * (
                        (height - start_margin - end_margin) / (count - 1)
                    )
            else:
                coordinate = (index + 1) * width / (count + 1)

            item = self._port_items.get(
                port.id
            )

            if item is None:
                continue

            if side == "left":
                item.setPos(
                    18.0,
                    coordinate,
                )

            elif side == "right":
                item.setPos(
                    width - 18.0,
                    coordinate,
                )

            elif side == "top":
                item.setPos(
                    coordinate,
                    56.0,
                )

            elif side == "bottom":
                item.setPos(
                    coordinate,
                    height - 16.0,
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