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
            "Detailed ports (all ports)",
            "__all__::all::details",
        )
        self.controller_connector_focus_combo.addItem(
            "Detailed ports (unused ports)",
            "__all__::unused::details",
        )
        self.controller_connector_focus_combo.addItem(
            "Detailed ports (used ports)",
            "__all__::used::details",
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
        if old_focus is None:
            saved_focus = self.store.state.view_state.get("controller_port_focus")
            if (
                isinstance(saved_focus, (list, tuple))
                and len(saved_focus) == 3
                and all(isinstance(part, str) for part in saved_focus)
            ):
                old_focus = tuple(saved_focus)
        old_key = "::".join(old_focus) if old_focus is not None else ""

        was_blocked = combo.blockSignals(True)
        combo.clear()
        combo.addItem("Functional interfaces", "")
        combo.addItem("Detailed ports (all ports)", "__all__::all::details")
        combo.addItem("Detailed ports (unused ports)", "__all__::unused::details")
        combo.addItem("Detailed ports (used ports)", "__all__::used::details")
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
        self.store.state.view_state["controller_port_focus"] = (
            list(self._controller_port_focus)
            if self._controller_port_focus is not None
            else None
        )
        self._update_controller_focus_help()

    def _controller_connector_focus_changed(self, _index: int = -1) -> None:
        """Change visible controller ports without committing a model mutation."""
        selected = self.controller_connector_focus_combo.currentData()
        parts = selected.split("::", 2) if isinstance(selected, str) and selected else []
        self._controller_port_focus = tuple(parts) if len(parts) == 3 else None
        self.store.state.view_state["controller_port_focus"] = (
            list(self._controller_port_focus)
            if self._controller_port_focus is not None
            else None
        )
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
        contact_semantic_ids: set[str] = set()
        contact_sides: list[str] = []
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
                "semantic_port_id": port.id,
            }
            contact_semantic_ids.add(port.id)
            side = str(visual_port.side).lower().strip()
            if side in {"left", "right"}:
                contact_sides.append(side)

        group_side = str(
            group_port.properties.get("visual_side") or "right"
        ).lower().strip()
        if group_side not in {"left", "right"}:
            group_side = "right"

        left_count = contact_sides.count("left")
        right_count = contact_sides.count("right")
        if left_count > right_count:
            direction = "left"
        elif right_count > left_count:
            direction = "right"
        elif contact_sides:
            direction = group_side if group_side in contact_sides else contact_sides[0]
        else:
            direction = group_side

        connected = False
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
            break

        # If individual contact-level conductors exist without a coarse
        # functional-reference edge, keep the cone visible over that bundle.
        if not connected and contact_semantic_ids:
            for connection in model.connections.values():
                endpoints = (
                    connection.endpoint_a_id,
                    connection.endpoint_b_id,
                )
                if (
                    contact_semantic_ids.intersection(endpoints)
                    and any(endpoint not in contact_semantic_ids for endpoint in endpoints)
                ):
                    connected = True
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

    def _build_motor_terminal_group_info(
        self,
        node,
        controller_id: str,
        connected_peer_ids: set[str],
    ) -> dict | None:
        """Resolve explicit motor terminals for presentation without a group endpoint."""
        component_id = getattr(node, "semantic_reference", None)
        if not component_id:
            return None

        model = self.store.semantic_model
        component = model.components.get(component_id)
        if (
            component is None
            or component.properties.get("motor_terminal_profile")
            != "stepper_four_lead"
        ):
            return None

        terminal_ports = [
            port
            for port in model.ports.values()
            if port.component_id == component_id
            and port.properties.get("interface_role")
            == "motor_conductor_terminal"
            and port.properties.get("interface_granularity")
            == "physical_terminal"
            and port.properties.get("motor_terminal_profile")
            == "stepper_four_lead"
        ]
        if len(terminal_ports) != 4:
            return None

        terminal_by_id = {port.id: port for port in terminal_ports}
        terminal_ids = set(terminal_by_id)
        try:
            display_indexes = {
                port.id: int(port.properties.get("terminal_display_index"))
                for port in terminal_ports
            }
        except (TypeError, ValueError):
            return None

        if set(display_indexes.values()) != {1, 2, 3, 4}:
            return None
        if not terminal_ids.intersection(connected_peer_ids):
            return None

        visual_by_semantic_id = {
            visual_port.semantic_reference: visual_port
            for visual_port in node.ports.values()
            if visual_port.semantic_reference in terminal_ids
        }
        if set(visual_by_semantic_id) != terminal_ids:
            return None

        pins = {}
        for semantic_port_id in sorted(
            terminal_ids,
            key=lambda port_id: display_indexes[port_id],
        ):
            semantic_port = terminal_by_id[semantic_port_id]
            visual_port = visual_by_semantic_id[semantic_port_id]
            display_index = display_indexes[semantic_port_id]
            pins[visual_port.id] = {
                "pin_label": (
                    semantic_port.properties.get("terminal_label")
                    or f"Terminal {display_index}"
                ),
                "purpose": getattr(semantic_port, "purpose", "") or "",
                "semantic_port_id": semantic_port.id,
            }

        direction = "right"
        motor_graphics = self._node_items.get(node.id)
        controller_node = next(
            (
                candidate
                for candidate in self.store.model.nodes.values()
                if candidate.node_type == "controller"
                and candidate.semantic_reference == controller_id
            ),
            None,
        )
        controller_graphics = (
            self._node_items.get(controller_node.id)
            if controller_node is not None
            else None
        )
        if motor_graphics is not None and controller_graphics is not None:
            controller_x = controller_graphics.sceneBoundingRect().center().x()
            motor_x = motor_graphics.sceneBoundingRect().center().x()
            direction = "left" if controller_x < motor_x else "right"

        return {
            "endpoint_port_id": None,
            "title": "Motor electrical interface",
            "pins": pins,
            "connected": True,
            "direction": direction,
            "port_side_override": direction,
        }

    def _apply_controller_connector_focus(self) -> None:
        """Filter port graphics by detail level without editing the model."""
        focus = self._controller_port_focus
        model = self.store.semantic_model
        detail_scope = (
            focus[1]
            if focus is not None
            and len(focus) == 3
            and focus[0] == "__all__"
            and focus[2] == "details"
            else None
        )
        detail_mode = detail_scope in {"all", "used", "unused"}
        connected_port_ids = {
            endpoint_id
            for connection in self.store.model.connections.values()
            for endpoint_id in (
                connection.endpoint_a_id,
                connection.endpoint_b_id,
            )
        }
        focus_connected_peer_ids: set[str] = set()
        if focus is not None and len(focus) == 3 and focus[2] == "contacts":
            focus_controller_id, focus_connector_id, _mode = focus
            focus_contact_ids = {
                port.id
                for port in model.ports.values()
                if (
                    port.controller_id == focus_controller_id
                    and port.connector_id == focus_connector_id
                    and port.pin_id is not None
                )
            }
            for semantic_connection in model.connections.values():
                endpoints = (
                    semantic_connection.endpoint_a_id,
                    semantic_connection.endpoint_b_id,
                )
                if not focus_contact_ids.intersection(endpoints):
                    continue
                for endpoint_id in endpoints:
                    if endpoint_id in focus_contact_ids:
                        continue
                    endpoint_port = model.ports.get(endpoint_id)
                    if endpoint_port is not None and endpoint_port.component_id is not None:
                        focus_connected_peer_ids.add(endpoint_id)


        for node in self.store.model.nodes.values():
            graphics = self._node_items.get(node.id)
            if graphics is None:
                continue

            visible_ids = set()
            if detail_mode:
                for visual_port in node.ports.values():
                    is_used = visual_port.id in connected_port_ids
                    should_show = (
                        detail_scope == "all"
                        or (detail_scope == "used" and is_used)
                        or (detail_scope == "unused" and not is_used)
                    )
                    if should_show:
                        visible_ids.add(visual_port.id)
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
                        and (
                            port.properties.get("interface_granularity")
                            == "functional_interface"
                            or port.id in focus_connected_peer_ids
                        )
                    ):
                        visible_ids.add(visual_port.id)

                # Components without a canonical functional endpoint retain
                # their existing visible detail ports.
                if not visible_ids:
                    visible_ids.update(node.ports)

            connector_group_info = None
            if (
                focus is not None
                and not detail_mode
                and len(focus) == 3
                and focus[2] == "contacts"
            ):
                controller_id, connector_id, _mode = focus
                if node.node_type == "controller":
                    if node.semantic_reference == controller_id:
                        connector_group_info = self._build_connector_group_info(
                            node, controller_id, connector_id
                        )
                else:
                    motor_group_info = self._build_motor_terminal_group_info(
                        node,
                        controller_id,
                        focus_connected_peer_ids,
                    )
                    if motor_group_info is not None:
                        connector_group_info = motor_group_info
                        visible_ids.update(motor_group_info["pins"].keys())

                        # The physical terminals are the detailed presentation
                        # of this same functional electrical interface.
                        for visual_port in node.ports.values():
                            semantic_port = model.ports.get(
                                visual_port.semantic_reference
                            )
                            if (
                                semantic_port is not None
                                and semantic_port.component_id == node.semantic_reference
                                and semantic_port.properties.get("interface_granularity")
                                == "functional_interface"
                                and semantic_port.properties.get("interface_role")
                                == "motor_electrical_interface"
                            ):
                                visible_ids.discard(visual_port.id)

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
        elif focus == ("__all__", "unused", "details"):
            text = (
                "Detailed-port view: shows unconnected ports across all nodes. "
                "Connections to hidden ports are hidden in this view."
            )
        elif focus == ("__all__", "used", "details"):
            text = (
                "Detailed-port view: shows connected ports across all nodes. "
                "Only individual ports with connections are shown."
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