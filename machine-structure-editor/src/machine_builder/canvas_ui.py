"""Qt user-interface construction for the Machine Structure Editor."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QComboBox,
    QGraphicsScene,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .graphics.palette import PaletteList
from .graphics.routing_debug import RoutingDebugOverlay
from .graphics.view import MachineGraphicsView
from .selection_inspector import SelectionInspector


class CanvasUIMixin:
    """Build the main editor window and its actions."""

    def _build_ui(self) -> None:
        """Build the main editor window."""
        central = QWidget()

        self.setCentralWidget(
            central
        )

        main_layout = QHBoxLayout(
            central
        )

        main_layout.setContentsMargins(
            8,
            8,
            8,
            8,
        )

        main_layout.setSpacing(
            8
        )

        self.palette = PaletteList()

        self._build_palette()

        palette_layout = QVBoxLayout()

        palette_title = QLabel(
            "Components"
        )

        palette_title.setStyleSheet(
            "font-weight: bold;"
        )

        add_button = QPushButton(
            "Add selected"
        )

        add_button.clicked.connect(
            self._add_selected_palette_item
        )

        edit_button = QPushButton(
            "Edit Component..."
        )

        edit_button.clicked.connect(
            self._edit_selected_component
        )

        edit_controller_button = QPushButton(
            "Edit Controller..."
        )

        edit_controller_button.clicked.connect(
            self._edit_selected_controller
        )

        palette_help = QLabel(
            "Double-click a port to edit it. "
            "Single-click/drag ports to connect them."
        )

        palette_help.setWordWrap(
            True
        )

        palette_layout.addWidget(
            palette_title
        )

        palette_layout.addWidget(
            self.palette
        )

        palette_layout.addWidget(
            add_button
        )

        palette_layout.addWidget(
            edit_button
        )
        add_port_button = QPushButton(
            "Add Port..."
        )

        add_port_button.clicked.connect(
            self._add_port_to_selected_component
        )

        palette_layout.addWidget(
            add_port_button
        )

        palette_layout.addWidget(
            edit_controller_button
        )

        palette_layout.addWidget(
            palette_help
        )

        palette_panel = QWidget()

        palette_panel.setLayout(
            palette_layout
        )

        self.scene = QGraphicsScene()

        self.scene.setSceneRect(
            -100000,
            -100000,
            200000,
            200000,
        )

        self.view = MachineGraphicsView(
            scene=self.scene,
            canvas=self,
        )

        self._routing_debug_overlay = RoutingDebugOverlay(
            self,
        )

        self.scene.addItem(
            self._routing_debug_overlay,
        )

        self.selection_inspector = (
            SelectionInspector(
                routing_debug_callback=(
                    self.set_routing_debug_mode
                ),
                nudge_callback=(
                    self._nudge_selected_nodes
                ),
            )
        )

        main_layout.addWidget(
            palette_panel
        )

        focus_panel = QWidget()
        focus_layout = QVBoxLayout(focus_panel)
        focus_layout.setContentsMargins(0, 0, 0, 0)

        focus_row = QHBoxLayout()
        focus_row.addWidget(QLabel("Port detail:"))
        self.controller_connector_focus_combo = QComboBox()
        self.controller_connector_focus_combo.setObjectName(
            "controller_connector_focus_combo"
        )
        self.controller_connector_focus_combo.addItem(
            "Functional interfaces",
            "",
        )
        self.controller_connector_focus_combo.addItem(
            "Detailed ports (all nodes)",
            "__all__::all::details",
        )
        self.controller_connector_focus_combo.currentIndexChanged.connect(
            self._controller_connector_focus_changed
        )
        focus_row.addWidget(self.controller_connector_focus_combo, 1)
        focus_layout.addLayout(focus_row)

        self.controller_connector_focus_help = QLabel()
        self.controller_connector_focus_help.setWordWrap(True)
        focus_layout.addWidget(self.controller_connector_focus_help)
        focus_layout.addWidget(self.view, 1)

        main_layout.addWidget(
            focus_panel,
            1,
        )

        main_layout.addWidget(
            self.selection_inspector
        )

        self.statusBar().showMessage(
            "Ready"
        )

    def _refresh_controller_connector_choices(self) -> None:
        """Populate view-only focus choices from canonical controller ports."""
        combo = self.controller_connector_focus_combo
        old_focus = self._controller_port_focus
        old_key = "::".join(old_focus) if old_focus is not None else ""

        was_blocked = combo.blockSignals(True)
        combo.clear()
        combo.addItem("Functional interfaces", "")
        combo.addItem("Detailed ports (all nodes)", "__all__::all::details")
        options = []
        model = self.store.semantic_model

        for node in self.store.model.nodes.values():
            controller_id = node.semantic_reference
            if node.node_type != "controller" or not controller_id:
                continue

            grouped = {}
            for visual_port in node.ports.values():
                port = model.ports.get(visual_port.semantic_reference)
                if (
                    port is None
                    or port.controller_id != controller_id
                    or not port.connector_id
                ):
                    continue

                group = grouped.setdefault(
                    port.connector_id,
                    {"interface": [], "contacts": []},
                )
                if (
                    port.pin_id is None
                    and port.properties.get("interface_granularity")
                    == "connector_level"
                ):
                    group["interface"].append(port)
                elif port.pin_id is not None:
                    group["contacts"].append(port)

            for connector_id, group in grouped.items():
                candidates = group["interface"] + group["contacts"]
                designator = next(
                    (
                        port.properties.get("pcb_reference_designator")
                        for port in candidates
                        if port.properties.get("pcb_reference_designator")
                    ),
                    connector_id,
                )
                owner_label = node.label or controller_id
                if group["interface"]:
                    options.append((
                        f"{owner_label} — {designator} interface",
                        f"{controller_id}::{connector_id}::interface",
                    ))
                if group["contacts"]:
                    options.append((
                        f"{owner_label} — {designator} contacts",
                        f"{controller_id}::{connector_id}::contacts",
                    ))

        for label, key in sorted(
            options,
            key=lambda entry: (entry[0].casefold(), entry[1]),
        ):
            combo.addItem(label, key)

        selected_index = 0
        for index in range(combo.count()):
            if combo.itemData(index) == old_key:
                selected_index = index
                break
        combo.setCurrentIndex(selected_index)
        combo.blockSignals(was_blocked)

        selected = combo.currentData()
        parts = selected.split("::", 2) if isinstance(selected, str) and selected else []
        self._controller_port_focus = tuple(parts) if len(parts) == 3 else None
        self._update_controller_focus_help()

    def _controller_connector_focus_changed(self, _index: int = -1) -> None:
        """Change visible controller ports without committing a model mutation."""
        selected = self.controller_connector_focus_combo.currentData()
        parts = selected.split("::", 2) if isinstance(selected, str) and selected else []
        self._controller_port_focus = tuple(parts) if len(parts) == 3 else None
        self._apply_controller_connector_focus()
        self._update_controller_focus_help()

    def _build_connector_group_info(
        self,
        node,
        controller_id: str,
        connector_id: str,
    ) -> dict | None:
        """Resolve existing connector/contact semantics for presentation only."""
        model = self.store.semantic_model
        group_matches = [
            port
            for port in model.ports.values()
            if port.controller_id == controller_id
            and port.component_id is None
            and port.connector_id == connector_id
            and port.pin_id is None
            and port.properties.get("interface_granularity") == "connector_level"
        ]
        if len(group_matches) != 1:
            return None

        group_port = group_matches[0]
        pins = {}
        for visual_port in node.ports.values():
            port = model.ports.get(visual_port.semantic_reference)
            if (
                port is None
                or port.controller_id != controller_id
                or port.component_id is not None
                or port.connector_id != connector_id
                or port.pin_id is None
            ):
                continue
            pins[visual_port.id] = {
                "pin_label": port.properties.get("pin_label") or port.label,
                "purpose": getattr(port, "purpose", "") or "",
            }

        connected = False
        direction = "right"
        for connection in model.connections.values():
            endpoints = (connection.endpoint_a_id, connection.endpoint_b_id)
            if group_port.id not in endpoints:
                continue
            other_id = (
                connection.endpoint_b_id
                if connection.endpoint_a_id == group_port.id
                else connection.endpoint_a_id
            )
            other_port = model.ports.get(other_id)
            if (
                other_port is None
                or other_port.properties.get("interface_granularity")
                != "functional_interface"
                or other_port.properties.get("interface_role")
                != "motor_electrical_interface"
            ):
                continue

            connected = True
            target_node = next(
                (
                    candidate
                    for candidate in self.store.model.nodes.values()
                    if any(
                        visual_port.semantic_reference == other_id
                        for visual_port in candidate.ports.values()
                    )
                ),
                None,
            )
            if target_node is not None and target_node.x < node.x:
                direction = "left"
            break

        return {
            "endpoint_port_id": group_port.id,
            "title": (
                group_port.properties.get("connector_label")
                or group_port.label
                or connector_id
            ),
            "pins": pins,
            "connected": connected,
            "direction": direction,
        }

    def _apply_controller_connector_focus(self) -> None:
        """Filter port graphics by detail level without editing the model."""
        focus = self._controller_port_focus
        model = self.store.semantic_model
        all_details = focus == ("__all__", "all", "details")

        for node in self.store.model.nodes.values():
            graphics = self._node_items.get(node.id)
            if graphics is None:
                continue

            visible_ids = set()
            if all_details:
                visible_ids.update(node.ports)
            elif node.node_type == "controller":
                for visual_port in node.ports.values():
                    port = model.ports.get(visual_port.semantic_reference)
                    if port is None:
                        continue

                    if focus is None:
                        visible = (
                            port.properties.get("interface_granularity")
                            == "connector_level"
                        )
                    else:
                        controller_id, connector_id, mode = focus
                        visible = (
                            node.semantic_reference == controller_id
                            and port.controller_id == controller_id
                            and port.connector_id == connector_id
                            and (
                                (
                                    mode == "interface"
                                    and port.pin_id is None
                                    and port.properties.get("interface_granularity")
                                    == "connector_level"
                                )
                                or (mode == "contacts" and port.pin_id is not None)
                            )
                        )
                    if visible:
                        visible_ids.add(visual_port.id)
            else:
                for visual_port in node.ports.values():
                    port = model.ports.get(visual_port.semantic_reference)
                    if (
                        port is not None
                        and port.component_id == node.semantic_reference
                        and port.properties.get("interface_granularity")
                        == "functional_interface"
                    ):
                        visible_ids.add(visual_port.id)

                # Components without a canonical functional endpoint retain
                # their existing visible detail ports.
                if not visible_ids:
                    visible_ids.update(node.ports)

            connector_group_info = None
            if (
                focus is not None
                and not all_details
                and node.node_type == "controller"
            ):
                controller_id, connector_id, mode = focus
                if (
                    mode == "contacts"
                    and node.semantic_reference == controller_id
                ):
                    connector_group_info = self._build_connector_group_info(
                        node, controller_id, connector_id
                    )

            graphics.set_controller_port_focus(
                visible_ids,
                connector_group_info,
            )

        self._scene_controller.update_connection_graphics()
        self.view.viewport().update()

    def _update_controller_focus_help(self) -> None:
        """Explain the chosen port detail level."""
        focus = self._controller_port_focus
        if focus == ("__all__", "all", "details"):
            text = (
                "Detailed-port view: shows all available port details on all nodes. "
                "This changes presentation only; machine semantics are unchanged."
            )
        elif focus is not None:
            _controller_id, connector_id, mode = focus
            if mode == "contacts":
                text = (
                    f"Contact detail: {connector_id}. Hidden ports and connections "
                    "remain in the model. This selector changes presentation only."
                )
            else:
                text = (
                    f"Functional interface: {connector_id}. This is a connector-level "
                    "endpoint, not an individual contact or conductor mapping."
                )
        elif any(
            port.properties.get("interface_granularity") == "connector_level"
            for port in self.store.semantic_model.ports.values()
        ):
            text = (
                "Functional-interface view. Select a connector to inspect its "
                "individual contacts, or choose Detailed ports to show all available "
                "detail. Focus does not edit machine semantics."
            )
        else:
            text = (
                "A generic Controller has no hardware-specific ports. Add a "
                "board-specific controller to expose documented interfaces; "
                "this view does not fabricate contacts."
            )
        self.controller_connector_focus_help.setText(text)

    def _create_actions(self) -> None:
        """Create editor actions and shortcuts."""
        delete_action = QAction(
            "Delete",
            self,
        )

        delete_action.setShortcut(
            Qt.Key.Key_Delete
        )

        delete_action.triggered.connect(
            self._delete_selected
        )

        undo_action = QAction(
            "Undo",
            self,
        )

        undo_action.setShortcut(
            "Ctrl+Z"
        )

        undo_action.triggered.connect(
            self.store.undo
        )

        redo_action = QAction(
            "Redo",
            self,
        )

        redo_action.setShortcut(
            "Ctrl+Y"
        )

        redo_action.triggered.connect(
            self.store.redo
        )

        frame_action = QAction(
            "Frame All",
            self,
        )

        frame_action.setShortcut(
            "F"
        )

        frame_action.triggered.connect(
            self._frame_all
        )

        edit_component_action = QAction(
            "Edit Component...",
            self,
        )

        edit_component_action.setShortcut(
            "Ctrl+E"
        )

        edit_component_action.triggered.connect(
            self._edit_selected_component
        )

        edit_controller_action = QAction(
            "Edit Controller...",
            self,
        )

        edit_controller_action.setShortcut(
            "Ctrl+Shift+E"
        )

        edit_controller_action.triggered.connect(
            self._edit_selected_controller
        )

        self.addAction(
            delete_action
        )

        self.addAction(
            undo_action
        )

        self.addAction(
            redo_action
        )

        self.addAction(
            frame_action
        )

        self.addAction(
            edit_component_action
        )

        self.addAction(
            edit_controller_action
        )

    def _frame_all(self) -> None:
        """Fit all current objects into the visible canvas."""
        if not self.store.model.nodes:
            return

        frame_items = list(self._node_items.values())
        frame_items.extend(self._connection_items.values())
        if not frame_items:
            return

        bounds = frame_items[0].sceneBoundingRect()
        for item in frame_items[1:]:
            bounds = bounds.united(item.sceneBoundingRect())

        for node_graphics in self._node_items.values():
            overlay_bounds = node_graphics.connector_group_overlay_bounds()
            if overlay_bounds is not None:
                bounds = bounds.united(overlay_bounds)

        if bounds.isNull():
            return

        bounds = bounds.adjusted(
            -100,
            -100,
            100,
            100,
        )

        self.view.fitInView(
            bounds,
            Qt.AspectRatioMode.KeepAspectRatio,
        )