"""Selection inspection and debug information for the visual editor."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .visual_model import (
    VisualConnection,
    VisualModel,
    VisualNode,
)


class SelectionInspector(QWidget):
    """Display detailed information about the current visual selection."""

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setMinimumWidth(
            280
        )

        self.setMaximumWidth(
            380
        )

        self._current_debug_text = ""

        layout = QVBoxLayout(
            self
        )

        title = QLabel(
            "Selection Inspector"
        )

        title.setStyleSheet(
            "font-weight: bold;"
        )

        self._selection_label = QLabel(
            "Nothing selected"
        )

        self._selection_label.setWordWrap(
            True
        )

        self._details = QPlainTextEdit()

        self._details.setReadOnly(
            True
        )

        self._details.setLineWrapMode(
            QPlainTextEdit.LineWrapMode.NoWrap
        )

        self._copy_button = QPushButton(
            "Copy Debug Info"
        )

        self._copy_button.clicked.connect(
            self.copy_debug_info
        )

        layout.addWidget(
            title
        )

        layout.addWidget(
            self._selection_label
        )

        layout.addWidget(
            self._details,
            1,
        )

        layout.addWidget(
            self._copy_button
        )

        self.clear()

    def _routing_debug_toggled(
        self,
        enabled: bool,
    ) -> None:
        if self._routing_debug_callback is not None:
            self._routing_debug_callback(
                enabled
            )

    def set_routing_debug_mode(
        self,
        enabled: bool,
    ) -> None:
        self._routing_debug_check.blockSignals(
            True
        )

        self._routing_debug_check.setChecked(
            enabled
        )

        self._routing_debug_check.blockSignals(
            False
        )

        if enabled:
            self._routing_debug_legend.setText(
                "DEBUG COLORS<br>"
                "<span style='color:#ff6666'>"
                "red tint"
                "</span> = physical component bounds<br>"
                "<span style='color:#f2c94c'>"
                "amber dashed"
                "</span> = routing clearance envelope<br>"
                "<span style='color:#168a52'>"
                "dark green"
                "</span> = fixed endpoint stub<br>"
                "<span style='color:#00b894'>"
                "teal"
                "</span> = endpoint escape<br>"
                "<span style='color:#66ff33'>"
                "bright green"
                "</span> = main route<br>"
                "<span style='color:#ff3030'>"
                "red marker"
                "</span> = no legal main route<br>"
                "<b>Hysteresis: OFF</b>"
            )
        else:
            self._routing_debug_legend.clear()

        self._routing_debug_legend.setVisible(
            enabled
        )

    def set_last_click_position(
        self,
        scene_position: QPointF,
    ) -> None:
        self._last_click_label.setText(
            "Last canvas click: "
            f"x={scene_position.x():.3f}, "
            f"y={scene_position.y():.3f}"
        )

    def clear(self) -> None:
        """Clear the inspector."""
        self._selection_label.setText(
            "Nothing selected"
        )

        self._set_debug_text(
            "Select a node or connection to inspect it."
        )

    def set_multiple_selection(
        self,
        count: int,
    ) -> None:
        """Show a summary for multiple selected graphics items."""
        self._selection_label.setText(
            f"{count} items selected"
        )

        self._set_debug_text(
            "Select one node or connection to inspect it."
        )

    def set_node(
        self,
        node: VisualNode,
        model: VisualModel,
    ) -> None:
        """Display one visual node and its connections."""
        self._selection_label.setText(
            f"Node: {node.label}"
        )

        self._set_debug_text(
            self._build_node_debug_text(
                node,
                model,
            )
        )

    def set_connection(
        self,
        connection: VisualConnection,
        model: VisualModel,
    ) -> None:
        """Display one visual connection and its endpoints."""
        self._selection_label.setText(
            "Connection"
        )

        self._set_debug_text(
            self._build_connection_debug_text(
                connection,
                model,
            )
        )

    def debug_text(self) -> str:
        """Return the complete currently displayed debug text."""
        return self._current_debug_text

    def copy_debug_info(self) -> str:
        """Copy the current debug information to the system clipboard."""
        QApplication.clipboard().setText(
            self._current_debug_text
        )

        return self._current_debug_text

    def _set_debug_text(
        self,
        text: str,
    ) -> None:
        self._current_debug_text = text

        self._details.setPlainText(
            text
        )

    @staticmethod
    def _build_node_debug_text(
        node: VisualNode,
        model: VisualModel,
    ) -> str:
        right = (
            node.x
            + node.width
        )

        bottom = (
            node.y
            + node.height
        )

        lines = [
            "Selection",
            "----------",
            f"label: {node.label}",
            f"id: {node.id}",
            f"type: {node.node_type}",
            (
                "semantic reference: "
                f"{node.semantic_reference or 'none'}"
            ),
            "",
            "Position",
            "--------",
            f"x: {node.x:.3f}",
            f"y: {node.y:.3f}",
            f"width: {node.width:.3f}",
            f"height: {node.height:.3f}",
            f"rotation: {node.rotation:.3f}",
            "",
            "Bounds",
            "------",
            f"left: {node.x:.3f}",
            f"top: {node.y:.3f}",
            f"right: {right:.3f}",
            f"bottom: {bottom:.3f}",
            "",
            "Ports",
            "-----",
        ]

        if not node.ports:
            lines.append(
                "none"
            )

        else:
            ports = sorted(
                node.ports.values(),
                key=lambda port: (
                    port.side,
                    port.order,
                    port.id,
                ),
            )

            for port in ports:
                lines.append(
                    (
                        f"{port.label or port.id} "
                        f"[{port.id}]"
                    )
                )

                lines.append(
                    f"  side: {port.side}"
                )

                lines.append(
                    f"  order: {port.order}"
                )

                lines.append(
                    f"  type: {port.port_type}"
                )

                lines.append(
                    f"  direction: {port.direction}"
                )

                lines.append(
                    (
                        "  semantic reference: "
                        f"{port.semantic_reference or 'none'}"
                    )
                )

                connection_lines = (
                    SelectionInspector
                    ._connection_lines_for_port(
                        port.id,
                        model,
                    )
                )

                if connection_lines:
                    lines.append(
                        "  connections:"
                    )

                    lines.extend(
                        f"    {line}"
                        for line
                        in connection_lines
                    )

                else:
                    lines.append(
                        "  connections: none"
                    )

        return "\n".join(
            lines
        )

    @staticmethod
    def _build_connection_debug_text(
        connection: VisualConnection,
        model: VisualModel,
    ) -> str:
        lines = [
            "Selection",
            "----------",
            "type: connection",
            f"id: {connection.id}",
            f"connection type: {connection.connection_type}",
            "",
            "Endpoint A",
            "----------",
        ]

        lines.extend(
            SelectionInspector
            ._endpoint_lines(
                connection.endpoint_a_id,
                model,
            )
        )

        lines.extend(
            [
                "",
                "Endpoint B",
                "----------",
            ]
        )

        lines.extend(
            SelectionInspector
            ._endpoint_lines(
                connection.endpoint_b_id,
                model,
            )
        )

        return "\n".join(
            lines
        )

    @staticmethod
    def _endpoint_lines(
        port_id: str,
        model: VisualModel,
    ) -> list[str]:
        port = model.find_port(
            port_id
        )

        if port is None:
            return [
                f"port id: {port_id}",
                "port: missing",
            ]

        node = model.find_node_for_port(
            port_id
        )

        if node is None:
            return [
                f"port id: {port.id}",
                f"port label: {port.label}",
                "node: missing",
            ]

        return [
            f"node: {node.label}",
            f"node id: {node.id}",
            f"node type: {node.node_type}",
            f"node x: {node.x:.3f}",
            f"node y: {node.y:.3f}",
            f"node width: {node.width:.3f}",
            f"node height: {node.height:.3f}",
            f"port: {port.label or port.id}",
            f"port id: {port.id}",
            f"port side: {port.side}",
            f"port order: {port.order}",
        ]

    @staticmethod
    def _connection_lines_for_port(
        port_id: str,
        model: VisualModel,
    ) -> list[str]:
        lines: list[str] = []

        for connection in model.connections.values():
            if not connection.contains_port(
                port_id
            ):
                continue

            other_port_id = (
                connection.endpoint_b_id
                if connection.endpoint_a_id
                == port_id
                else connection.endpoint_a_id
            )

            other_port = model.find_port(
                other_port_id
            )

            other_node = model.find_node_for_port(
                other_port_id
            )

            if (
                other_port is None
                or other_node is None
            ):
                lines.append(
                    (
                        f"{connection.id} "
                        "→ missing endpoint"
                    )
                )

                continue

            lines.append(
                (
                    f"{connection.id} "
                    f"→ {other_node.label} / "
                    f"{other_port.label or other_port.id}"
                )
            )

        return lines