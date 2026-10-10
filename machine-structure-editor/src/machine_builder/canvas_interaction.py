"""Interactive editing behavior for the Machine Structure Editor canvas.

This module contains user-interaction behavior that operates on a canvas
host. It deliberately does not own the Qt main window, scene construction,
document persistence, or visual-model synchronization.

The host is expected to provide:

    store
    scene
    statusBar()
    _node_items
    _connection_items
    _synchronizing_scene

and the following scene-controller interface:

    scene_controller.find_port_graphics_item()
    scene_controller.find_port_graphics_at()
    scene_controller.update_connection_graphics()

The eventual rebuilt canvas can therefore compose this behavior with
separate window, scene, and document responsibilities.
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QPen
from PySide6.QtWidgets import QGraphicsLineItem

from .compatibility import (
    CompatibilityResult,
    check_port_compatibility,
)
from .connection_details import (
    ConnectionEndpointSummary,
    PhysicalConnectionDetailsDialog,
    confirm_conditional_compatibility,
    confirm_unknown_compatibility,
    confirm_visual_only_connection,
    show_incompatible_connection,
    show_invalid_canonical_reference,
)
from .graphics.connection import ConnectionGraphicsItem
from .graphics.node import NodeGraphicsItem
from .graphics.port import PortGraphicsItem
from .mutations import (
    CreateConnection,
    DeleteConnection,
    DeleteNodes,
    MoveNodes,
)
from .visual_model import VisualPort


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


class CanvasInteractionMixin:
    """Provide interactive editing behavior for a canvas host."""

    @property
    def scene_controller(self):
        """Return the host's scene controller."""
        return self._scene_controller

    def _delete_selected(self) -> None:
        """Delete selected connections or nodes as one user action."""
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

            self.statusBar().showMessage(
                f"Deleted {len(selected_connections)} connection"
                + (
                    ""
                    if len(selected_connections) == 1
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

    def _connection_selected(
        self,
        connection_id: str,
        selected: bool,
    ) -> None:
        """Show status information when a connection is selected."""
        if not selected:
            return

        connection = (
            self.store.model.connections.get(
                connection_id
            )
        )

        if connection is None:
            return

        endpoint_a = self.store.model.find_port(
            connection.endpoint_a_id
        )
        endpoint_b = self.store.model.find_port(
            connection.endpoint_b_id
        )

        if (
            endpoint_a is None
            or endpoint_b is None
        ):
            self.statusBar().showMessage(
                "Selected connection"
            )
            return

        self.statusBar().showMessage(
            f"Selected connection: "
            f"{endpoint_a.label} ↔ "
            f"{endpoint_b.label}"
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

    def _nudge_selected_nodes(
        self,
        dx: float,
        dy: float,
    ) -> None:
        """Move selected visual nodes by one precision-nudge step."""
        if self._synchronizing_scene:
            return

        selected_nodes = [
            item
            for item in self.scene.selectedItems()
            if isinstance(
                item,
                NodeGraphicsItem,
            )
        ]

        if not selected_nodes:
            self.statusBar().showMessage(
                "Select a node to nudge."
            )
            return

        positions: dict[
            str,
            tuple[float, float],
        ] = {}

        for item in selected_nodes:
            node = self.store.model.nodes.get(
                item.node_id
            )

            if node is None:
                continue

            positions[
                item.node_id
            ] = (
                node.x + dx,
                node.y + dy,
            )

        if not positions:
            return

        self.store.commit(
            MoveNodes(
                positions=positions
            )
        )

        direction = []

        if dx > 0:
            direction.append(
                f"+{dx:g} X"
            )
        elif dx < 0:
            direction.append(
                f"{dx:g} X"
            )

        if dy > 0:
            direction.append(
                f"+{dy:g} Y"
            )
        elif dy < 0:
            direction.append(
                f"{dy:g} Y"
            )

        self.statusBar().showMessage(
            "Nudged "
            f"{len(positions)} node"
            + (
                ""
                if len(positions) == 1
                else "s"
            )
            + " by "
            + ", ".join(direction)
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
                    final_positions[last_id]
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

    def _node_position_changed(
        self,
        node_id: str,
    ) -> None:
        """Update connection graphics while a node is being moved."""
        self.scene_controller.update_connection_graphics()

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

        source_item = (
            self.scene_controller.find_port_graphics_item(
                source_port_id
            )
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

        target_item = (
            self.scene_controller.find_port_graphics_at(
                scene_position
            )
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
            if (
                self._active_connection_target
                is not None
            ):
                self._active_connection_target.set_connection_state(
                    "normal"
                )

            self._active_connection_target = (
                target_item
            )

        if target_item is None:
            if (
                self._active_connection_source
                is not None
            ):
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

        semantic_source = source_port
        semantic_target = target_port

        if (
            result
            != CompatibilityResult.COMPATIBLE
        ):
            reverse_result = check_port_compatibility(
                target_port,
                source_port,
            )

            if (
                reverse_result
                == CompatibilityResult.COMPATIBLE
            ):
                result = reverse_result
                semantic_source = target_port
                semantic_target = source_port

        if (
            result
            == CompatibilityResult.COMPATIBLE
        ):
            target_item.set_connection_state(
                "valid"
            )

            message = (
                f"Compatible: "
                f"{semantic_source.label} → "
                f"{semantic_target.label}"
            )

        elif (
            result
            == CompatibilityResult.UNKNOWN
        ):
            target_item.set_connection_state(
                "unknown"
            )

            message = (
                f"Unknown compatibility: "
                f"{semantic_source.label} ↔ "
                f"{semantic_target.label}"
            )

        elif (
            result
            == CompatibilityResult.CONDITIONAL
        ):
            target_item.set_connection_state(
                "unknown"
            )

            message = (
                f"Conditional compatibility: "
                f"{semantic_source.label} ↔ "
                f"{semantic_target.label}"
            )

        else:
            target_item.set_connection_state(
                "invalid"
            )

            message = (
                f"Incompatible: "
                f"{source_port.label} ↔ "
                f"{target_port.label}"
            )

        self.statusBar().showMessage(
            message
        )

    def _connection_endpoint_summary(
        self,
        visual_port: VisualPort,
    ) -> ConnectionEndpointSummary:
        """Build a read-only endpoint summary from its canonical port."""
        reference = visual_port.semantic_reference
        if reference is None:
            raise ValueError("The visual endpoint has no canonical port reference.")

        semantic_port = self.store.semantic_model.get_port(reference)
        owner_label = "Unspecified"

        if semantic_port.component_id is not None:
            component = self.store.semantic_model.components.get(
                semantic_port.component_id
            )
            if component is not None:
                owner_label = component.label or component.role or component.id
        elif semantic_port.controller_id is not None:
            controller = self.store.semantic_model.controllers.get(
                semantic_port.controller_id
            )
            if controller is not None:
                owner_label = controller.name or controller.id

        purpose = semantic_port.purpose
        connector_id = semantic_port.connector_id
        pin_id = semantic_port.pin_id

        if not purpose or not purpose.strip():
            purpose = "Unspecified"
        if not connector_id or not connector_id.strip():
            connector_id = "Unspecified"
        if not pin_id or not pin_id.strip():
            pin_id = "Unspecified"

        return ConnectionEndpointSummary(
            owner_label=owner_label,
            port_purpose=purpose,
            connector_id=connector_id,
            pin_id=pin_id,
        )

    def _finish_connection_drag(
        self,
        source_port_id: str,
        scene_position: QPointF,
    ) -> None:
        """Create a connection only after required authoring decisions."""
        drag = self._active_connection_drag
        if drag is None:
            return

        target_item = self.scene_controller.find_port_graphics_at(
            scene_position
        )
        target_port_id = (
            target_item.port_id
            if target_item is not None
            else None
        )
        source_port = self.store.model.find_port(drag.source_port_id)
        target_port = (
            self.store.model.find_port(target_port_id)
            if target_port_id is not None
            else None
        )

        if source_port is None or target_port is None:
            self.statusBar().showMessage("Connection cancelled.")
        else:
            endpoint_a_ref = source_port.semantic_reference
            endpoint_b_ref = target_port.semantic_reference
            visual_pair = {source_port.id, target_port.id}

            duplicate_visual = any(
                {
                    connection.endpoint_a_id,
                    connection.endpoint_b_id,
                } == visual_pair
                for connection in self.store.model.connections.values()
            )

            duplicate_semantic = False
            if endpoint_a_ref is not None and endpoint_b_ref is not None:
                duplicate_semantic = any(
                    connection.connects_same_ports(
                        endpoint_a_ref,
                        endpoint_b_ref,
                    )
                    for connection
                    in self.store.semantic_model.connections.values()
                )

            if duplicate_visual or duplicate_semantic:
                self.statusBar().showMessage(
                    "That connection already exists."
                )
            elif (
                endpoint_a_ref is not None
                and endpoint_a_ref == endpoint_b_ref
            ):
                self.statusBar().showMessage(
                    "Connection rejected: both endpoints resolve to the same canonical port."
                )
            else:
                result = check_port_compatibility(
                    source_port,
                    target_port,
                )
                semantic_source = source_port
                semantic_target = target_port

                if result != CompatibilityResult.COMPATIBLE:
                    reverse_result = check_port_compatibility(
                        target_port,
                        source_port,
                    )
                    if reverse_result == CompatibilityResult.COMPATIBLE:
                        result = reverse_result
                        semantic_source = target_port
                        semantic_target = source_port

                proceed = result == CompatibilityResult.COMPATIBLE
                if result == CompatibilityResult.UNKNOWN:
                    proceed = confirm_unknown_compatibility(self)
                    if not proceed:
                        self.statusBar().showMessage("Connection cancelled.")
                elif result == CompatibilityResult.CONDITIONAL:
                    proceed = confirm_conditional_compatibility(self)
                    if not proceed:
                        self.statusBar().showMessage("Connection cancelled.")
                elif result == CompatibilityResult.INCOMPATIBLE:
                    show_incompatible_connection(self)
                    self.statusBar().showMessage(
                        "Connection rejected: incompatible ports."
                    )

                if proceed:
                    semantic_model = self.store.semantic_model
                    canonical_a = (
                        semantic_model.ports.get(endpoint_a_ref)
                        if endpoint_a_ref is not None
                        else None
                    )
                    canonical_b = (
                        semantic_model.ports.get(endpoint_b_ref)
                        if endpoint_b_ref is not None
                        else None
                    )

                    invalid_reference = (
                        endpoint_a_ref is not None
                        and canonical_a is None
                    ) or (
                        endpoint_b_ref is not None
                        and canonical_b is None
                    )

                    should_create = False
                    canonical_connection_created = False
                    connection_properties = None

                    if invalid_reference:
                        show_invalid_canonical_reference(self)
                        self.statusBar().showMessage(
                            "Connection not created: an endpoint has an invalid canonical port reference."
                        )
                    elif canonical_a is None or canonical_b is None:
                        if confirm_visual_only_connection(self):
                            should_create = True
                        else:
                            self.statusBar().showMessage("Connection cancelled.")
                    else:
                        dialog = PhysicalConnectionDetailsDialog(
                            endpoint_a=self._connection_endpoint_summary(
                                source_port
                            ),
                            endpoint_b=self._connection_endpoint_summary(
                                target_port
                            ),
                            parent=self,
                        )
                        if dialog.exec() == dialog.DialogCode.Accepted:
                            connection_properties = dialog.result_data()
                            should_create = True
                            canonical_connection_created = True
                        else:
                            self.statusBar().showMessage("Connection cancelled.")

                    if should_create:
                        connection_id = (
                            f"connection-"
                            f"{len(self.store.model.connections) + 1}"
                        )
                        self.store.commit(
                            CreateConnection(
                                connection_id=connection_id,
                                endpoint_a_id=source_port.id,
                                endpoint_b_id=target_port.id,
                                connection_type=semantic_source.port_type,
                                connection_properties=connection_properties,
                            )
                        )

                        if canonical_connection_created:
                            self.statusBar().showMessage(
                                f"Connected: "
                                f"{semantic_source.label} -> "
                                f"{semantic_target.label}"
                            )
                        else:
                            self.statusBar().showMessage(
                                "Visual connection created; no canonical physical connection was created."
                            )

        self._cancel_connection_drag(preserve_status=True)

    def _cancel_connection_drag(
        self,
        preserve_status: bool = False,
    ) -> None:
        """Remove the temporary connection state."""
        if (
            self._active_connection_target
            is not None
        ):
            self._active_connection_target.set_connection_state(
                "normal"
            )

        if (
            self._active_connection_source
            is not None
        ):
            self._active_connection_source.set_connection_state(
                "normal"
            )

        if (
            self._connection_preview
            is not None
        ):
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

        source_item = (
            self.scene_controller.find_port_graphics_item(
                drag.source_port_id
            )
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