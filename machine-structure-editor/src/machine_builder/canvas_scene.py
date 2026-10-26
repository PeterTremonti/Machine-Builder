"""Scene synchronization for the Machine Structure Editor canvas.

This module owns the relationship between the VisualModel and the Qt
graphics scene.
"""

from __future__ import annotations

from PySide6.QtCore import QPointF

from .graphics.connection import ConnectionGraphicsItem
from .graphics.connection_routing import ConnectionRoutingEngine
from .graphics.node import NodeGraphicsItem
from .graphics.port import PortGraphicsItem
from .visual_model import VisualModel


class CanvasSceneController:
    """Maintain Qt graphics items for a VisualModel."""

    def __init__(
        self,
        canvas,
    ) -> None:
        self.canvas = canvas
        self._connector_wire_stub_items: dict[tuple[str, str], QGraphicsPathItem] = {}

    @property
    def scene(self):
        """Return the canvas graphics scene."""
        return self.canvas.scene

    @property
    def store(self):
        """Return the canvas model store."""
        return self.canvas.store

    @property
    def node_items(
        self,
    ) -> dict[str, NodeGraphicsItem]:
        """Return rendered node items."""
        return self.canvas._node_items

    @property
    def connection_items(
        self,
    ) -> dict[str, ConnectionGraphicsItem]:
        """Return rendered connection items."""
        return self.canvas._connection_items

    def find_port_graphics_item(
        self,
        port_id: str,
    ) -> PortGraphicsItem | None:
        """Find the rendered port for a visual port ID."""
        for node_item in self.node_items.values():
            port_item = node_item._port_items.get(
                port_id
            )

            if port_item is not None:
                return port_item

        return None

    def find_port_graphics_at(
        self,
        scene_position: QPointF,
    ) -> PortGraphicsItem | None:
        """Find a port directly under a scene position."""
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
    def _grouped_contact_fanout_offset(
        self,
        endpoint_id: str,
        origin: QPointF,
        anchor: QPointF,
    ) -> float:
        """Return a stable, evenly spaced lane offset for a grouped contact."""

        def fallback_offset() -> float:
            offset = max(
                -14.0,
                min(14.0, (origin.y() - anchor.y()) * 0.25),
            )
            if abs(offset) < 3.0:
                offset = 3.0 if origin.y() >= anchor.y() else -3.0
            return offset

        endpoint_item = self.find_port_graphics_item(endpoint_id)
        if endpoint_item is None:
            return fallback_offset()

        node_graphics = endpoint_item.parentItem()
        if node_graphics is None:
            return fallback_offset()

        visual_port = getattr(node_graphics, "_visual_ports", {}).get(
            getattr(endpoint_item, "port_id", None)
        )
        semantic_endpoint_id = (
            getattr(visual_port, "semantic_reference", None) or endpoint_id
        )
        contact_anchors = getattr(
            node_graphics, "_connector_group_contact_anchors_local", {}
        )
        origin_getter = getattr(
            node_graphics, "connector_group_contact_origin_for_port", None
        )
        if semantic_endpoint_id not in contact_anchors or not callable(origin_getter):
            return fallback_offset()

        members = []
        for member_id in contact_anchors:
            member_origin = origin_getter(member_id)
            if member_origin is None:
                continue
            members.append(
                (
                    float(member_origin.y()),
                    float(member_origin.x()),
                    str(member_id),
                )
            )

        members.sort()
        member_ids = [member[2] for member in members]
        if len(member_ids) < 2 or str(semantic_endpoint_id) not in member_ids:
            return fallback_offset()

        rank = member_ids.index(str(semantic_endpoint_id))
        lane_spacing = ConnectionRoutingEngine.MIN_ROUTE_SEGMENT_SEPARATION
        return (rank - (len(member_ids) - 1) / 2.0) * lane_spacing

    def _grouped_contact_start_stub_length(
        self,
        anchor: QPointF,
        offset: float,
        side: str | None,
        protected_segments: list[tuple[QPointF, QPointF]],
    ) -> float | None:
        """Shorten a left-facing fan-out escape around a protected vertical lane."""
        if side != "left" or not protected_segments:
            return None

        route_position_x = anchor.x() - 18.0
        lane_y = anchor.y() + offset
        blocking_xs = []
        for start, end in protected_segments:
            if abs(start.x() - end.x()) > 1e-6:
                continue
            if abs(start.y() - end.y()) <= 1e-6:
                continue
            if not (
                min(start.y(), end.y()) - 1e-6
                <= lane_y
                <= max(start.y(), end.y()) + 1e-6
            ):
                continue
            segment_x = (start.x() + end.x()) / 2.0
            if segment_x < route_position_x - 1e-6:
                blocking_xs.append(segment_x)

        if not blocking_xs:
            return None

        default_core_x = route_position_x - ConnectionRoutingEngine.STUB_LENGTH
        required_core_x = (
            max(blocking_xs)
            + ConnectionRoutingEngine.MIN_ROUTE_SEGMENT_SEPARATION
            + 1.0
        )
        if required_core_x <= default_core_x + 1e-6:
            return None
        if required_core_x >= route_position_x - 1e-6:
            return None
        return route_position_x - required_core_x

    def update_connection_graphics(
        self,
    ) -> None:
        """Recalculate all committed connection lines."""
        active_connector_stubs: set[tuple[str, str]] = set()
        routed_connection_segments: list[tuple[QPointF, QPointF]] = []
        for (
            connection_id,
            graphics,
        ) in self.connection_items.items():
            connection = (
                self.store.model.connections.get(
                    connection_id
                )
            )

            if connection is None:
                continue

            endpoint_a_item = (
                self.find_port_graphics_item(
                    connection.endpoint_a_id
                )
            )

            endpoint_b_item = (
                self.find_port_graphics_item(
                    connection.endpoint_b_id
                )
            )

            if (
                endpoint_a_item is None
                or endpoint_b_item is None
            ):
                continue

            start = endpoint_a_item.scenePos()
            end = endpoint_b_item.scenePos()
            endpoint_side_overrides = {}
            anchored_endpoint_ids: set[str] = set()
            connector_stub_specs: list[tuple[str, QPointF, QPointF]] = []

            for endpoint_id, endpoint_item, endpoint_name in (
                (connection.endpoint_a_id, endpoint_a_item, "start"),
                (connection.endpoint_b_id, endpoint_b_item, "end"),
            ):
                node_graphics = endpoint_item.parentItem()
                anchor_getter = getattr(
                    node_graphics,
                    "connector_group_anchor_for_port",
                    None,
                )
                visual_port = getattr(node_graphics, "_visual_ports", {}).get(
                    getattr(endpoint_item, "port_id", None)
                )
                semantic_endpoint_id = (
                    getattr(visual_port, "semantic_reference", None)
                    or endpoint_id
                )
                anchor = (
                    anchor_getter(semantic_endpoint_id)
                    if callable(anchor_getter)
                    else None
                )
                if anchor is None:
                    continue

                if endpoint_name == "start":
                    start = anchor
                else:
                    end = anchor

                side_getter = getattr(
                    node_graphics,
                    "connector_group_endpoint_side_for_port",
                    None,
                )
                side = (
                    side_getter(semantic_endpoint_id)
                    if callable(side_getter)
                    else None
                )
                if side in {"left", "right", "top", "bottom"}:
                    endpoint_side_overrides[endpoint_id] = side
                    contact_anchors = getattr(
                        node_graphics, "_connector_group_contact_anchors_local", {}
                    )
                    origin_getter = getattr(
                        node_graphics, "connector_group_contact_origin_for_port", None
                    )
                    origin = origin_getter(semantic_endpoint_id) if callable(origin_getter) else None
                    if (
                        semantic_endpoint_id in contact_anchors
                        and side in {"left", "right"}
                        and origin is not None
                    ):
                        connector_stub_specs.append(
                            (endpoint_id, QPointF(origin), QPointF(anchor))
                        )

            endpoints_available = (
                (
                    endpoint_a_item.isVisible()
                    or connection.endpoint_a_id in anchored_endpoint_ids
                )
                and (
                    endpoint_b_item.isVisible()
                    or connection.endpoint_b_id in anchored_endpoint_ids
                )
            )
            graphics.setVisible(endpoints_available)
            if not endpoints_available:
                continue

            set_overrides = getattr(graphics, "set_endpoint_side_overrides", None)
            if callable(set_overrides):
                set_overrides(endpoint_side_overrides)

            fanout_offsets: dict[str, float] = {}
            fanout_stub_lengths: dict[str, float] = {}
            for endpoint_id, origin, anchor in connector_stub_specs:
                offset = self._grouped_contact_fanout_offset(
                    endpoint_id, origin, anchor
                )
                fanout_offsets[endpoint_id] = offset
                if endpoint_id == connection.endpoint_a_id:
                    stub_length = self._grouped_contact_start_stub_length(
                        anchor,
                        offset,
                        endpoint_side_overrides.get(endpoint_id),
                        routed_connection_segments,
                    )
                    if stub_length is not None:
                        fanout_stub_lengths[endpoint_id] = stub_length

            set_fanout = getattr(
                graphics, "set_endpoint_route_fanout_offsets", None
            )
            if callable(set_fanout):
                set_fanout(fanout_offsets)

            set_stub_lengths = getattr(
                graphics, "set_endpoint_route_stub_lengths", None
            )
            if callable(set_stub_lengths):
                set_stub_lengths(fanout_stub_lengths)

            set_protected_segments = getattr(
                graphics,
                "set_external_route_protected_segments",
                None,
            )
            if callable(set_protected_segments):
                set_protected_segments(routed_connection_segments)

            graphics.setLine(
                start.x(),
                start.y(),
                end.x(),
                end.y(),
            )

            route_points = getattr(graphics, "_debug_route", None)
            if route_points:
                routed_connection_segments.extend(
                    (QPointF(route_start), QPointF(route_end))
                    for route_start, route_end in zip(
                        route_points,
                        route_points[1:],
                    )
                    if route_start != route_end
                )
            wire_color = getattr(graphics, "_wire_color", QColor("#aab4c4"))
            for endpoint_id, origin, anchor in connector_stub_specs:
                key = (connection_id, endpoint_id)
                item = self._connector_wire_stub_items.get(key)
                if item is None:
                    item = QGraphicsPathItem()
                    item.setZValue(6.0)
                    item.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
                    self.scene.addItem(item)
                    self._connector_wire_stub_items[key] = item
                stub_end = QPointF(anchor)
                endpoint_item = self.find_port_graphics_item(endpoint_id)
                node_graphics = (
                    endpoint_item.parentItem()
                    if endpoint_item is not None
                    else None
                )
                cone = getattr(node_graphics, "_connector_group_cone", None)
                if cone is not None and cone.isVisible():
                    cone_path = cone.path()
                    if cone_path.elementCount() >= 3:
                        base_top = cone_path.elementAt(1)
                        base_bottom = cone_path.elementAt(2)
                        base_start = cone.mapToScene(
                            QPointF(base_top.x, base_top.y)
                        )
                        base_end = cone.mapToScene(
                            QPointF(base_bottom.x, base_bottom.y)
                        )
                        dx = anchor.x() - origin.x()
                        dy = anchor.y() - origin.y()
                        sx = base_end.x() - base_start.x()
                        sy = base_end.y() - base_start.y()
                        denominator = dx * sy - dy * sx
                        if abs(denominator) > 1e-9:
                            qx = base_start.x() - origin.x()
                            qy = base_start.y() - origin.y()
                            t = (qx * sy - qy * sx) / denominator
                            u = (qx * dy - qy * dx) / denominator
                            if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
                                line_length = (dx * dx + dy * dy) ** 0.5
                                if line_length > 1e-9:
                                    t = max(0.0, t - 1.0 / line_length)
                                    stub_end = QPointF(
                                        origin.x() + t * dx,
                                        origin.y() + t * dy,
                                    )
                conductor_path = QPainterPath(origin)
                conductor_path.lineTo(stub_end)
                item.setPath(conductor_path)
                item.setPen(
                    QPen(
                        wire_color,
                        2.0,
                        Qt.PenStyle.SolidLine,
                        Qt.PenCapStyle.RoundCap,
                        Qt.PenJoinStyle.RoundJoin,
                    )
                )
                item.setVisible(True)
                active_connector_stubs.add(key)

        for key, item in list(self._connector_wire_stub_items.items()):
            if key not in active_connector_stubs:
                self.scene.removeItem(item)
                del self._connector_wire_stub_items[key]

    def synchronize(
        self,
        model: VisualModel,
    ) -> None:
        """Synchronize the Qt scene with the visual model."""
        self.canvas._synchronizing_scene = True

        try:
            self._remove_deleted_items(
                model
            )

            self._synchronize_nodes(
                model
            )

            self._synchronize_connections(
                model
            )

            self.update_connection_graphics()

            # Scene-only hosts need not construct the Canvas focus UI.
            refresh_focus_choices = getattr(
                self.canvas,
                "_refresh_controller_connector_choices",
                None,
            )
            apply_focus = getattr(
                self.canvas,
                "_apply_controller_connector_focus",
                None,
            )
            if callable(refresh_focus_choices):
                refresh_focus_choices()
            if callable(apply_focus):
                apply_focus()

        finally:
            self.canvas._synchronizing_scene = False

    def _remove_deleted_items(
        self,
        model: VisualModel,
    ) -> None:
        current_node_ids = set(
            model.nodes
        )

        existing_node_ids = set(
            self.node_items
        )

        for node_id in (
            existing_node_ids - current_node_ids
        ):
            item = self.node_items.pop(
                node_id
            )

            self.scene.removeItem(
                item
            )

        current_connection_ids = set(
            model.connections
        )

        existing_connection_ids = set(
            self.connection_items
        )

        for connection_id in (
            existing_connection_ids
            - current_connection_ids
        ):
            item = self.connection_items.pop(
                connection_id
            )

            self.scene.removeItem(
                item
            )

    def _synchronize_nodes(
        self,
        model: VisualModel,
    ) -> None:
        double_click_callback = getattr(
            self.canvas,
            "_edit_selected_controller",
            None,
        )

        for node_id, node in model.nodes.items():
            item = self.node_items.get(
                node_id
            )

            if item is None:
                item = NodeGraphicsItem(
                    node=node,
                    move_started_callback=(
                        self.canvas._begin_node_move
                    ),
                    move_finished_callback=(
                        self.canvas._finish_node_move
                    ),
                    selection_callback=(
                        self.canvas._node_selected
                    ),
                    focus_callback=(
                        self.canvas._focus_node
                    ),
                    position_changed_callback=(
                        self.canvas._node_position_changed
                    ),
                    connection_drag_started=(
                        self.canvas._start_connection_drag
                    ),
                    connection_drag_moved=(
                        self.canvas._move_connection_drag
                    ),
                    connection_drag_finished=(
                        self.canvas._finish_connection_drag
                    ),
                    port_edit_requested=(
                        self.canvas._edit_semantic_port
                    ),
                    double_click_callback=(
                        double_click_callback
                    ),
                )

                self.node_items[
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
                    connection_drag_started=(
                        self.canvas._start_connection_drag
                    ),
                    connection_drag_moved=(
                        self.canvas._move_connection_drag
                    ),
                    connection_drag_finished=(
                        self.canvas._finish_connection_drag
                    ),
                    port_edit_requested=(
                        self.canvas._edit_semantic_port
                    ),
                )

            item.setPos(
                node.x,
                node.y,
            )

    def _synchronize_connections(
        self,
        model: VisualModel,
    ) -> None:
        for (
            connection_id,
            connection,
        ) in model.connections.items():
            graphics = (
                self.connection_items.get(
                    connection_id
                )
            )

            if graphics is None:
                graphics = ConnectionGraphicsItem(
                    connection=connection,
                    selection_callback=(
                        self.canvas._connection_selected
                    ),
                )

                self.connection_items[
                    connection_id
                ] = graphics

                self.scene.addItem(
                    graphics
                )

        self.update_connection_graphics()