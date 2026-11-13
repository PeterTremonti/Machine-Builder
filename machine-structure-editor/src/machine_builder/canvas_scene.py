"""Scene synchronization for the Machine Structure Editor canvas.

This module owns the relationship between the VisualModel and the Qt
graphics scene.
"""

from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QPainterPath, QPen
from PySide6.QtWidgets import QGraphicsPathItem

from .graphics.connection import ConnectionGraphicsItem
from .graphics.connection_routing import ConnectionRoutingEngine
from .graphics.connection_routing_bundle import (
    bundle_envelope_half_width,
    lane_order_is_compatible,
)
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
        self._drag_preview_items: dict[tuple[str, str, str], QGraphicsPathItem] = {}
        self._drag_preview_hidden_connections: dict[
            str, tuple[ConnectionGraphicsItem, bool]
        ] = {}
        self._drag_preview_timer = QTimer()
        self._drag_preview_timer.setSingleShot(True)
        self._drag_preview_timer.setInterval(50)
        self._drag_preview_timer.timeout.connect(
            self._update_node_move_preview
        )

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

    def _should_hide_redundant_contact_functional_link(
        self,
        connection_id: str,
    ) -> bool:
        """Hide a refined coarse link only in contact-focus presentation."""
        focus = getattr(self.canvas, "_controller_port_focus", None)
        if (
            not isinstance(focus, tuple)
            or len(focus) != 3
            or focus[2] != "contacts"
        ):
            return False

        controller_id, connector_id, _mode = focus
        semantic_model = self.store.semantic_model
        current = semantic_model.connections.get(connection_id)
        if current is None:
            return False

        endpoints = (current.endpoint_a_id, current.endpoint_b_id)
        for contact_id, peer_id in (endpoints, tuple(reversed(endpoints))):
            contact = semantic_model.ports.get(contact_id)
            functional_peer = semantic_model.ports.get(peer_id)
            if (
                contact is None
                or contact.controller_id != controller_id
                or contact.connector_id != connector_id
                or contact.pin_id is None
                or functional_peer is None
                or functional_peer.component_id is None
                or functional_peer.properties.get("interface_granularity")
                != "functional_interface"
                or functional_peer.properties.get("interface_role")
                != "motor_electrical_interface"
            ):
                continue

            # If this same controller contact already has a direct conductor
            # connection to a physical terminal on this component, don't render
            # the contact-to-functional-interface link as a second wire.
            for candidate in semantic_model.connections.values():
                if candidate.id == connection_id:
                    continue
                candidate_endpoints = (
                    candidate.endpoint_a_id,
                    candidate.endpoint_b_id,
                )
                if contact_id not in candidate_endpoints:
                    continue

                terminal_id = (
                    candidate.endpoint_b_id
                    if candidate.endpoint_a_id == contact_id
                    else candidate.endpoint_a_id
                )
                terminal = semantic_model.ports.get(terminal_id)
                if (
                    terminal is not None
                    and terminal.component_id == functional_peer.component_id
                    and terminal.properties.get("interface_role")
                    == "motor_conductor_terminal"
                    and terminal.properties.get("interface_granularity")
                    == "physical_terminal"
                ):
                    return True

        return False
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

    def _connection_routing_bundle_member(self, connection_id: str):
        """Return physical endpoint data for one conductor connection."""
        connection = self.store.model.connections.get(connection_id)
        if connection is None:
            return None
        semantic_model = getattr(self.store, "semantic_model", None)
        if semantic_model is None:
            return None
        ports = getattr(semantic_model, "ports", None)
        if ports is None:
            return None
        for contact_visual_id, terminal_visual_id in (
            (connection.endpoint_a_id, connection.endpoint_b_id),
            (connection.endpoint_b_id, connection.endpoint_a_id),
        ):
            contact_item = self.find_port_graphics_item(contact_visual_id)
            terminal_item = self.find_port_graphics_item(terminal_visual_id)
            if contact_item is None or terminal_item is None:
                continue
            contact_node = contact_item.parentItem()
            terminal_node = terminal_item.parentItem()
            contact_visual = getattr(contact_node, "_visual_ports", {}).get(
                getattr(contact_item, "port_id", None)
            )
            terminal_visual = getattr(terminal_node, "_visual_ports", {}).get(
                getattr(terminal_item, "port_id", None)
            )
            contact_id = (
                getattr(contact_visual, "semantic_reference", None)
                or contact_visual_id
            )
            terminal_id = (
                getattr(terminal_visual, "semantic_reference", None)
                or terminal_visual_id
            )
            contact = ports.get(contact_id)
            terminal = ports.get(terminal_id)
            if contact is None or terminal is None:
                continue
            properties = getattr(terminal, "properties", {}) or {}
            if (
                not contact.controller_id
                or not contact.connector_id
                or contact.pin_id is None
                or not terminal.component_id
                or properties.get("interface_role")
                != "motor_conductor_terminal"
                or properties.get("interface_granularity")
                != "physical_terminal"
            ):
                continue
            return (
                (
                    str(contact.controller_id),
                    str(contact.connector_id),
                    str(terminal.component_id),
                ),
                QPointF(contact_item.scenePos()),
                QPointF(terminal_item.scenePos()),
            )
        return None

    def _ordered_connection_items(self):
        """Order only explicitly grouped, physically consistent Harness members."""
        items = sorted(self.connection_items.items(), key=lambda item: item[0])
        semantic_model = getattr(self.store, "semantic_model", None)
        if semantic_model is None:
            return items

        harnesses = getattr(semantic_model, "harnesses", None)
        if not isinstance(harnesses, dict) or not harnesses:
            return items

        try:
            semantic_model.validate_harnesses()
        except (AttributeError, KeyError, TypeError, ValueError):
            return items

        nested_harness_ids = {
            child_id
            for parent in harnesses.values()
            for child_id in getattr(parent, "child_harness_ids", ())
        }
        visual_connection_ids = set(self.connection_items)
        model_connection_ids = set(self.store.model.connections)
        semantic_connection_ids = set(semantic_model.connections)
        bundles = {}
        bundle_for_connection = {}

        for harness_id, harness in sorted(harnesses.items()):
            member_ids = getattr(harness, "member_connection_ids", None)
            child_ids = getattr(harness, "child_harness_ids", None)
            if (
                not isinstance(member_ids, list)
                or len(member_ids) < 2
                or len(member_ids) != len(set(member_ids))
                or not isinstance(child_ids, list)
                or child_ids
                or harness_id in nested_harness_ids
            ):
                continue

            if any(
                not isinstance(member_id, str) or not member_id.strip()
                for member_id in member_ids
            ):
                continue

            member_id_set = set(member_ids)
            if not (
                member_id_set.issubset(visual_connection_ids)
                and member_id_set.issubset(model_connection_ids)
                and member_id_set.issubset(semantic_connection_ids)
            ):
                continue

            members = []
            physical_group_key = None
            valid_bundle = True
            for member_id in member_ids:
                physical_member = self._connection_routing_bundle_member(
                    member_id
                )
                if physical_member is None:
                    valid_bundle = False
                    break
                key, contact, terminal = physical_member
                if physical_group_key is None:
                    physical_group_key = key
                elif key != physical_group_key:
                    valid_bundle = False
                    break
                members.append((
                    member_id,
                    self.connection_items[member_id],
                    contact,
                    terminal,
                ))

            if not valid_bundle or len(members) != len(member_ids):
                continue

            # Compare both ends along the same normal to the average
            # contact-to-terminal direction. Reversed or ambiguous
            # physical lane order cannot form a parallel shared trunk.
            dx = sum(
                terminal.x() - contact.x()
                for _, _, contact, terminal in members
            ) / len(members)
            dy = sum(
                terminal.y() - contact.y()
                for _, _, contact, terminal in members
            ) / len(members)
            if abs(dx) + abs(dy) <= 1e-6:
                continue

            normal_x = -dy
            normal_y = dx
            start_lane_positions = {
                member_id: (
                    contact.x() * normal_x
                    + contact.y() * normal_y
                )
                for member_id, _, contact, _ in members
            }
            end_lane_positions = {
                member_id: (
                    terminal.x() * normal_x
                    + terminal.y() * normal_y
                )
                for member_id, _, _, terminal in members
            }
            if not lane_order_is_compatible(
                start_lane_positions, end_lane_positions
            ):
                continue

            bundles[harness_id] = members
            for member_id in member_ids:
                bundle_for_connection[member_id] = harness_id

        ordered = []
        emitted = set()
        for connection_id, graphics in items:
            harness_id = bundle_for_connection.get(connection_id)
            if harness_id is None:
                ordered.append((connection_id, graphics))
                continue
            if harness_id in emitted:
                continue

            emitted.add(harness_id)
            members = bundles[harness_id]
            dx = sum(
                terminal.x() - contact.x()
                for _, _, contact, terminal in members
            ) / len(members)
            dy = sum(
                terminal.y() - contact.y()
                for _, _, contact, terminal in members
            ) / len(members)
            if abs(dx) >= abs(dy):
                reverse = dy <= 0.0
                members.sort(
                    key=lambda member: (
                        -member[2].y() if reverse else member[2].y(),
                        member[2].x(),
                        member[0],
                    )
                )
            elif dx >= 0.0:
                members.sort(
                    key=lambda member: (
                        member[2].x(), member[2].y(), member[0]
                    )
                )
            else:
                members.sort(
                    key=lambda member: (
                        -member[2].x(), member[2].y(), member[0]
                    )
                )
            ordered.extend(
                (member[0], member[1]) for member in members
            )

        return ordered

    def _routing_ordered_connection_items(self):
        """Prioritize physical conductor lanes without changing membership."""
        items = self._ordered_connection_items()
        members_by_physical_route_key = {}

        for index, (connection_id, graphics) in enumerate(items):
            physical_member = self._connection_routing_bundle_member(
                connection_id
            )
            if physical_member is None:
                continue

            key, contact, terminal = physical_member
            members_by_physical_route_key.setdefault(key, []).append(
                (index, connection_id, graphics, contact, terminal)
            )

        ordered = list(items)

        for members in members_by_physical_route_key.values():
            if len(members) < 2:
                continue

            dx = sum(
                terminal.x() - contact.x()
                for _, _, _, contact, terminal in members
            ) / len(members)
            dy = sum(
                terminal.y() - contact.y()
                for _, _, _, contact, terminal in members
            ) / len(members)

            if abs(dx) + abs(dy) <= 1e-6:
                continue

            normal_x = -dy
            normal_y = dx
            start_lane_positions = {
                connection_id: (
                    contact.x() * normal_x
                    + contact.y() * normal_y
                )
                for _, connection_id, _, contact, _ in members
            }
            end_lane_positions = {
                connection_id: (
                    terminal.x() * normal_x
                    + terminal.y() * normal_y
                )
                for _, connection_id, _, _, terminal in members
            }

            if not lane_order_is_compatible(
                start_lane_positions, end_lane_positions
            ):
                continue

            if abs(dx) >= abs(dy):
                reverse = dy <= 0.0
                sorted_members = sorted(
                    members,
                    key=lambda member: (
                        -member[3].y() if reverse else member[3].y(),
                        member[3].x(),
                        member[1],
                    ),
                )
            elif dx >= 0.0:
                sorted_members = sorted(
                    members,
                    key=lambda member: (
                        member[3].x(), member[3].y(), member[1]
                    ),
                )
            else:
                sorted_members = sorted(
                    members,
                    key=lambda member: (
                        -member[3].x(), member[3].y(), member[1]
                    ),
                )

            # Replace only the positions occupied by these conductors.
            # Independent connections retain their own identities and slots.
            for (index, _, _, _, _), member in zip(members, sorted_members):
                ordered[index] = (member[1], member[2])

        return ordered

    def _nearby_routed_connection_segments(self, start, end, segments):
        """Limit prior-wire constraints to the current route neighborhood."""
        padding = (
            ConnectionRoutingEngine.ROUTING_RELEVANCE_RADIUS
            + ConnectionRoutingEngine.ROUTING_MARGIN
            + ConnectionRoutingEngine.STUB_LENGTH
            + ConnectionRoutingEngine.U_TURN_MIN_SEPARATION
        )
        left = min(start.x(), end.x()) - padding
        right = max(start.x(), end.x()) + padding
        top = min(start.y(), end.y()) - padding
        bottom = max(start.y(), end.y()) + padding
        nearby = []
        for first, second in segments:
            if (
                max(first.x(), second.x()) < left
                or min(first.x(), second.x()) > right
                or max(first.y(), second.y()) < top
                or min(first.y(), second.y()) > bottom
            ):
                continue
            nearby.append((first, second))
        return nearby

    def request_node_move_preview(self) -> None:
        """Schedule one coalesced harness preview update during a node drag."""
        if (
            getattr(self.canvas, "_active_node_drag", None) is None
            or getattr(self.canvas, "_synchronizing_scene", False)
        ):
            return

        if not self._drag_preview_timer.isActive():
            self._drag_preview_timer.start()

    def _restore_drag_preview_connections(self) -> None:
        """Restore individual conductor visibility after a preview update."""
        for graphics, was_visible in self._drag_preview_hidden_connections.values():
            if graphics.scene() is self.scene:
                graphics.setVisible(was_visible)
        self._drag_preview_hidden_connections.clear()

    def finish_node_move_preview(self) -> None:
        """Remove transient harness previews and restore individual wires."""
        self._drag_preview_timer.stop()
        self._restore_drag_preview_connections()

        for item in self._drag_preview_items.values():
            if item.scene() is self.scene:
                self.scene.removeItem(item)
        self._drag_preview_items.clear()

    def _connection_routing_bundle_preview_details(self, connection_id: str):
        """Resolve the physical contact/terminal pair for one bundle member."""
        connection = self.store.model.connections.get(connection_id)
        semantic_model = getattr(self.store, "semantic_model", None)
        ports = getattr(semantic_model, "ports", None)

        if connection is None or ports is None:
            return None

        for contact_visual_id, terminal_visual_id in (
            (connection.endpoint_a_id, connection.endpoint_b_id),
            (connection.endpoint_b_id, connection.endpoint_a_id),
        ):
            contact_item = self.find_port_graphics_item(contact_visual_id)
            terminal_item = self.find_port_graphics_item(terminal_visual_id)
            if contact_item is None or terminal_item is None:
                continue

            contact_node = contact_item.parentItem()
            terminal_node = terminal_item.parentItem()
            contact_visual = getattr(contact_node, "_visual_ports", {}).get(
                getattr(contact_item, "port_id", None)
            )
            terminal_visual = getattr(terminal_node, "_visual_ports", {}).get(
                getattr(terminal_item, "port_id", None)
            )

            contact_id = (
                getattr(contact_visual, "semantic_reference", None)
                or contact_visual_id
            )
            terminal_id = (
                getattr(terminal_visual, "semantic_reference", None)
                or terminal_visual_id
            )
            contact = ports.get(contact_id)
            terminal = ports.get(terminal_id)

            if contact is None or terminal is None:
                continue

            properties = getattr(terminal, "properties", {}) or {}
            if (
                not contact.controller_id
                or not contact.connector_id
                or contact.pin_id is None
                or not terminal.component_id
                or properties.get("interface_role") != "motor_conductor_terminal"
                or properties.get("interface_granularity") != "physical_terminal"
            ):
                continue

            contact_position = QPointF(contact_item.scenePos())
            anchor_getter = getattr(
                contact_node, "connector_group_anchor_for_port", None
            )
            if callable(anchor_getter):
                anchor = anchor_getter(contact_id)
                if anchor is not None:
                    contact_position = QPointF(anchor)

            terminal_position = QPointF(terminal_item.scenePos())
            terminal_anchor_getter = getattr(
                terminal_node, "connector_group_anchor_for_port", None
            )
            if callable(terminal_anchor_getter):
                terminal_anchor = terminal_anchor_getter(terminal_id)
                if terminal_anchor is not None:
                    terminal_position = QPointF(terminal_anchor)
            return {
                "key": (
                    str(contact.controller_id),
                    str(contact.connector_id),
                    str(terminal.component_id),
                ),
                "contact_endpoint_id": contact_visual_id,
                "terminal_endpoint_id": terminal_visual_id,
                "contact_semantic_id": contact_id,
                "contact_position": contact_position,
                "terminal_position": terminal_position,
                "contact_node_id": getattr(contact_node, "node_id", None),
                "terminal_node_id": getattr(terminal_node, "node_id", None),
                "contact_node": contact_node,
            }

        return None

    def _update_preview_endpoint_stub(
        self,
        connection_id: str,
        endpoint_id: str,
    ) -> None:
        """Refresh an existing connector-group stub at either bundle endpoint."""
        stub = self._connector_wire_stub_items.get(
            (connection_id, endpoint_id)
        )
        if stub is None:
            return

        endpoint_item = self.find_port_graphics_item(endpoint_id)
        if endpoint_item is None:
            return

        node_graphics = endpoint_item.parentItem()
        if node_graphics is None:
            return

        visual_port = getattr(node_graphics, "_visual_ports", {}).get(
            getattr(endpoint_item, "port_id", None)
        )
        semantic_id = (
            getattr(visual_port, "semantic_reference", None) or endpoint_id
        )
        contact_anchors = getattr(
            node_graphics, "_connector_group_contact_anchors_local", {}
        )
        if semantic_id not in contact_anchors:
            return

        origin_getter = getattr(
            node_graphics, "connector_group_contact_origin_for_port", None
        )
        anchor_getter = getattr(
            node_graphics, "connector_group_anchor_for_port", None
        )
        if not callable(origin_getter) or not callable(anchor_getter):
            return

        origin = origin_getter(semantic_id)
        anchor = anchor_getter(semantic_id)
        if origin is None or anchor is None:
            return

        stub_path = QPainterPath(QPointF(origin))
        stub_path.lineTo(QPointF(anchor))
        stub.setPath(stub_path)

    @staticmethod
    def _average_preview_position(points: list[QPointF]) -> QPointF:
        """Find the center of a bundle's endpoint group."""
        return QPointF(
            sum(point.x() for point in points) / len(points),
            sum(point.y() for point in points) / len(points),
        )

    def _update_node_move_preview(self) -> None:
        """Route one widened preview path per affected physical conductor bundle."""
        drag = getattr(self.canvas, "_active_node_drag", None)
        if drag is None or getattr(self.canvas, "_synchronizing_scene", False):
            self.finish_node_move_preview()
            return

        self._restore_drag_preview_connections()
        moved_node_ids = set(drag.node_ids)
        bundles = {}

        for connection_id, graphics in self.connection_items.items():
            details = self._connection_routing_bundle_preview_details(
                connection_id
            )
            if details is None:
                continue

            endpoint_node_ids = {
                details["contact_node_id"],
                details["terminal_node_id"],
            }
            if not moved_node_ids.intersection(endpoint_node_ids):
                continue

            bundles.setdefault(details["key"], []).append(
                (connection_id, graphics, details)
            )

        active_preview_keys = set()

        for bundle_key, members in bundles.items():
            members.sort(key=lambda member: member[0])
            bundle_connection_ids = {
                member[0] for member in members
            }
            contact_center = self._average_preview_position(
                [member[2]["contact_position"] for member in members]
            )
            terminal_center = self._average_preview_position(
                [member[2]["terminal_position"] for member in members]
            )

            representative_id, representative_graphics, representative_details = members[0]
            connection = self.store.model.connections.get(representative_id)
            if connection is None:
                continue

            if connection.endpoint_a_id == representative_details["contact_endpoint_id"]:
                route_start = contact_center
                route_end = terminal_center
            else:
                route_start = terminal_center
                route_end = contact_center

            half_width = bundle_envelope_half_width(
                len(members),
                ConnectionRoutingEngine.MIN_ROUTE_SEGMENT_SEPARATION,
                conductor_radius=1.0,
            )

            # Use the group center rather than one conductor's individual
            # fan-out lane. Restore transient routing state immediately after
            # preparing the representative endpoint escapes.
            previous_offsets = dict(
                getattr(representative_graphics, "_endpoint_route_fanout_offsets", {})
            )
            previous_stub_lengths = dict(
                getattr(representative_graphics, "_endpoint_route_stub_lengths", {})
            )
            previous_escape_state = {
                key: dict(value)
                for key, value in getattr(
                    representative_graphics, "_overlap_escape_state", {}
                ).items()
            }

            representative_graphics.set_endpoint_route_fanout_offsets({})
            representative_graphics.set_endpoint_route_stub_lengths({})
            try:
                geometry = representative_graphics._prepare_line_geometry(
                    route_start.x(),
                    route_start.y(),
                    route_end.x(),
                    route_end.y(),
                )
            finally:
                representative_graphics.set_endpoint_route_fanout_offsets(
                    previous_offsets
                )
                representative_graphics.set_endpoint_route_stub_lengths(
                    previous_stub_lengths
                )
                representative_graphics._overlap_escape_state = previous_escape_state

            endpoint_obstacles = []
            for endpoint_id in (
                representative_graphics.endpoint_a_id,
                representative_graphics.endpoint_b_id,
            ):
                endpoint_node = representative_graphics._find_endpoint_node(
                    endpoint_id
                )
                if endpoint_node is not None:
                    endpoint_obstacles.append(
                        endpoint_node.sceneBoundingRect().adjusted(
                            -ConnectionRoutingEngine.ROUTING_MARGIN,
                            -ConnectionRoutingEngine.ROUTING_MARGIN,
                            ConnectionRoutingEngine.ROUTING_MARGIN,
                            ConnectionRoutingEngine.ROUTING_MARGIN,
                        )
                    )

            route_obstacles = []
            for obstacle in geometry["obstacles"]:
                is_endpoint_obstacle = any(
                    abs(obstacle.left() - endpoint.left()) <= 1e-6
                    and abs(obstacle.top() - endpoint.top()) <= 1e-6
                    and abs(obstacle.right() - endpoint.right()) <= 1e-6
                    and abs(obstacle.bottom() - endpoint.bottom()) <= 1e-6
                    for endpoint in endpoint_obstacles
                )
                route_obstacles.append(
                    QRectF(obstacle)
                    if is_endpoint_obstacle
                    else obstacle.adjusted(
                        -half_width,
                        -half_width,
                        half_width,
                        half_width,
                    )
                )

            route = ConnectionRoutingEngine.build_route(
                start=geometry["start_escape"][-1],
                end=geometry["end_escape"][-1],
                start_direction=geometry["start_direction"],
                end_direction=geometry["end_direction"],
                obstacles=route_obstacles,
                direct_start=geometry["start_route_position"],
                direct_end=geometry["end_route_position"],
            )
            if route is None:
                continue

            preview_path = QPainterPath(QPointF(geometry["start"]))
            if geometry["start_route_position"] != geometry["start"]:
                preview_path.lineTo(geometry["start_route_position"])
            for point in geometry["start_escape"][1:]:
                preview_path.lineTo(point)
            for point in route[1:]:
                preview_path.lineTo(point)
            for point in reversed(geometry["end_escape"][:-1]):
                preview_path.lineTo(point)
            preview_path.lineTo(geometry["end"])

            preview_item = self._drag_preview_items.get(bundle_key)
            if preview_item is None:
                preview_item = QGraphicsPathItem()
                preview_item.setZValue(-9.0)
                preview_item.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
                self.scene.addItem(preview_item)
                self._drag_preview_items[bundle_key] = preview_item

            preview_item.setPath(preview_path)
            preview_item.setPen(
                QPen(
                    QColor(75, 135, 195, 95),
                    2.0 * half_width,
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.RoundCap,
                    Qt.PenJoinStyle.RoundJoin,
                )
            )
            preview_item.setVisible(True)
            active_preview_keys.add(bundle_key)

            for connection_id, graphics, details in members:
                if connection_id not in self._drag_preview_hidden_connections:
                    self._drag_preview_hidden_connections[connection_id] = (
                        graphics,
                        graphics.isVisible(),
                    )
                graphics.setVisible(False)
                for endpoint_id in (
                    details["contact_endpoint_id"],
                    details["terminal_endpoint_id"],
                ):
                    self._update_preview_endpoint_stub(
                        connection_id, endpoint_id
                    )

        for bundle_key, item in list(self._drag_preview_items.items()):
            if bundle_key not in active_preview_keys:
                if item.scene() is self.scene:
                    self.scene.removeItem(item)
                del self._drag_preview_items[bundle_key]

    def update_connection_graphics(
        self,
    ) -> None:
        """Recalculate all committed connection lines."""
        if getattr(self.canvas, "_active_node_drag", None) is not None:
            self.request_node_move_preview()
            return

        self.finish_node_move_preview()
        active_connector_stubs: set[tuple[str, str]] = set()
        routed_connection_segments: list[tuple[QPointF, QPointF]] = []
        for connection_id, graphics in self._routing_ordered_connection_items():
            connection = (
                self.store.model.connections.get(
                    connection_id
                )
            )

            if connection is None:
                continue
            if self._should_hide_redundant_contact_functional_link(connection_id):
                graphics.setVisible(False)
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

            if endpoint_a_item is None or endpoint_b_item is None:
                graphics.setVisible(False)
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

                anchored_endpoint_ids.add(endpoint_id)
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

            nearby_routed_segments = self._nearby_routed_connection_segments(
                start, end, routed_connection_segments
            )

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
                        nearby_routed_segments,
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
                set_protected_segments(nearby_routed_segments)

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
            # A model-driven rebuild supersedes any unfinished interactive move.
            self.canvas._active_node_drag = None
            self.finish_node_move_preview()

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

            semantic_model = getattr(self.store, "semantic_model", None)
            semantic_connections = getattr(semantic_model, "connections", {})
            semantic_connection = semantic_connections.get(connection_id)
            wire_color = (
                semantic_connection.properties.get("wire_color")
                if semantic_connection is not None
                else None
            )
            graphics.set_wire_color(wire_color)

        self.update_connection_graphics()