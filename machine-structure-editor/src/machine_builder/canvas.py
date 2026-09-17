"""Main Machine Structure Editor canvas.

The canvas is a coordinator between Qt UI, visual interaction,
semantic editing, visual-model synchronization, and the editor store.

Feature responsibilities are delegated to focused modules.
"""

from __future__ import annotations

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QMainWindow

from .canvas_editing import CanvasEditingMixin
from .canvas_interaction import (
    CanvasInteractionMixin,
    ConnectionDragState,
    NodeDragState,
)
from .canvas_palette import CanvasPaletteMixin
from .canvas_scene import CanvasSceneController
from .canvas_selection import CanvasSelectionMixin
from .canvas_ui import CanvasUIMixin
from .store import ModelStore
from .visual_model import VisualModel


class MachineCanvas(
    CanvasUIMixin,
    CanvasEditingMixin,
    CanvasPaletteMixin,
    CanvasSelectionMixin,
    CanvasInteractionMixin,
    QMainWindow,
):
    """Main Machine Structure Editor window coordinator."""

    def __init__(
        self,
    ) -> None:
        super().__init__()

        self.store = ModelStore()

        self._node_items = {}
        self._connection_items = {}

        self._node_counter = 0

        self._last_edit_position = QPointF(
            100.0,
            100.0,
        )

        self._active_node_drag: (
            NodeDragState | None
        ) = None

        self._active_connection_drag: (
            ConnectionDragState | None
        ) = None

        self._connection_preview = None
        self._active_connection_source = None
        self._active_connection_target = None
        self._synchronizing_scene = False

        self._scene_controller = (
            CanvasSceneController(
                self
            )
        )

        self._build_ui()
        self._create_actions()

        self.store.subscribe(
            self._model_changed
        )

        self._model_changed(
            self.store.model
        )

    def _model_changed(
        self,
        model: VisualModel,
    ) -> None:
        """Synchronize graphics and selection inspection."""
        self._scene_controller.synchronize(
            model
        )

        self._refresh_selection_inspector()

    def _update_connection_graphics(
        self,
    ) -> None:
        """Compatibility wrapper for connection updates."""
        self._scene_controller.update_connection_graphics()

    def _find_port_graphics_item(
        self,
        port_id: str,
    ):
        """Compatibility wrapper for port lookup."""
        return (
            self._scene_controller.find_port_graphics_item(
                port_id
            )
        )

    def _find_port_graphics_at(
        self,
        scene_position: QPointF,
    ):
        """Compatibility wrapper for scene port lookup."""
        return (
            self._scene_controller.find_port_graphics_at(
                scene_position
            )
        )