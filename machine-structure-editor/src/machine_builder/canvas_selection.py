"""Selection coordination for the Machine Structure Editor canvas."""

from __future__ import annotations

from .graphics.connection import ConnectionGraphicsItem
from .graphics.node import NodeGraphicsItem


class CanvasSelectionMixin:
    """Keep the selection inspector synchronized with canvas selection."""

    def _refresh_selection_inspector(
        self,
    ) -> None:
        """Refresh the selection inspector from the current scene selection."""
        selected_items = self.scene.selectedItems()

        if not selected_items:
            self.selection_inspector.clear()
            return

        if len(selected_items) > 1:
            self.selection_inspector.set_multiple_selection(
                len(selected_items)
            )
            return

        item = selected_items[0]

        if isinstance(
            item,
            NodeGraphicsItem,
        ):
            node = self.store.model.nodes.get(
                item.node_id
            )

            if node is None:
                self.selection_inspector.clear()
                return

            self.selection_inspector.set_node(
                node,
                self.store.model,
            )

            return

        if isinstance(
            item,
            ConnectionGraphicsItem,
        ):
            connection = (
                self.store.model.connections.get(
                    item.connection_id
                )
            )

            if connection is None:
                self.selection_inspector.clear()
                return

            self.selection_inspector.set_connection(
                connection,
                self.store.model,
                item,
            )

            return

        self.selection_inspector.clear()

    def _node_selected(
        self,
        node_id: str,
        selected: bool,
    ) -> None:
        """Update selection presentation and inspector."""
        super()._node_selected(
            node_id,
            selected,
        )

        self._refresh_selection_inspector()

    def _connection_selected(
        self,
        connection_id: str,
        selected: bool,
    ) -> None:
        """Update connection selection and inspector."""
        super()._connection_selected(
            connection_id,
            selected,
        )

        self._refresh_selection_inspector()

    def _node_position_changed(
        self,
        node_id: str,
    ) -> None:
        """Keep the inspector current while a node moves."""
        super()._node_position_changed(
            node_id
        )

        self._refresh_selection_inspector()