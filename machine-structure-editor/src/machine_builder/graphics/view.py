"""Graphics view for the Machine Structure Editor.

This module contains the Qt graphics-view class that provides zoom, pan,
selection, and palette-drop interaction for the editor canvas.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..canvas import MachineCanvas

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import (
    QBrush,
    QColor,
    QDragEnterEvent,
    QDragMoveEvent,
    QDropEvent,
    QPainter,
)
from PySide6.QtWidgets import (
    QGraphicsScene,
    QGraphicsView,
)


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

        if (
            event.button()
            == Qt.MouseButton.LeftButton
        ):
            scene_position = self.mapToScene(
                event.position().toPoint()
            )

            self._canvas._record_last_click(
                scene_position
            )

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
