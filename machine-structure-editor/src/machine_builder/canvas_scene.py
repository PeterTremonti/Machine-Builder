"""Scene synchronization for the Machine Structure Editor canvas.

This module owns the relationship between the VisualModel and the Qt
graphics scene.
"""

from __future__ import annotations

from PySide6.QtCore import QPointF

from .graphics.connection import ConnectionGraphicsItem
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

    def update_connection_graphics(
        self,
    ) -> None:
        """Recalculate all committed connection lines."""
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

            graphics.setLine(
                start.x(),
                start.y(),
                end.x(),
                end.y(),
            )

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