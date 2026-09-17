"""Palette and template authoring for the Machine Structure Editor.

This module owns:
- palette population
- palette selection handling
- node-template creation
- provisional default ports for visual templates

Canonical controller authoring is delegated to the controller visual
mutation layer so that a controller palette item creates a real canonical
Controller and a linked VisualNode.

It does not own:
- the Qt main-window layout
- scene synchronization
- document persistence
- undo/redo
- interactive node movement
- connection interaction
"""

from __future__ import annotations

from PySide6.QtCore import QPointF, Qt
from PySide6.QtWidgets import QListWidgetItem

from .controller import Controller
from .controller_visual_mutations import (
    CreateControllerNode,
)
from .mutations import CreateNode
from .visual_model import VisualNode, VisualPort


class CanvasPaletteMixin:
    """Provide palette and visual-template authoring behavior."""

    def _build_palette(self) -> None:
        """Populate the component palette."""
        self.palette.setMinimumWidth(
            180
        )
        self.palette.setDragEnabled(
            True
        )

        templates = (
            (
                "controller",
                "Controller",
            ),
            (
                "motor",
                "Motor",
            ),
            (
                "sensor",
                "Sensor",
            ),
            (
                "part_cooling_fan",
                "Part Cooling Fan",
            ),
            (
                "component",
                "Component",
            ),
            (
                "temperature_sensor",
                "Temperature Sensor",
            ),
            (
                "temperature_controller",
                "Temperature Controller",
            ),
        )

        for (
            node_type,
            label,
        ) in templates:
            item = QListWidgetItem(
                label
            )

            item.setData(
                Qt.ItemDataRole.UserRole,
                node_type,
            )

            self.palette.addItem(
                item
            )

        self.palette.itemDoubleClicked.connect(
            self._palette_item_double_clicked
        )

    def _palette_item_double_clicked(
        self,
        item: QListWidgetItem,
    ) -> None:
        """Create a node from a double-clicked palette entry."""
        node_type = item.data(
            Qt.ItemDataRole.UserRole
        )

        if not isinstance(
            node_type,
            str,
        ):
            return

        self.create_node_from_template(
            node_type=node_type,
            scene_position=(
                self._suggest_new_node_position()
            ),
        )

    def _add_selected_palette_item(
        self,
    ) -> None:
        """Create a node from the selected palette entry."""
        item = self.palette.currentItem()

        if item is None:
            return

        node_type = item.data(
            Qt.ItemDataRole.UserRole
        )

        if not isinstance(
            node_type,
            str,
        ):
            return

        self.create_node_from_template(
            node_type=node_type,
            scene_position=(
                self._suggest_new_node_position()
            ),
        )

    def create_node_from_template(
        self,
        node_type: str,
        scene_position: QPointF,
    ) -> None:
        """Create a canonical or provisional visual node."""
        labels = {
            "controller": "Controller",
            "motor": "Motor",
            "sensor": "Sensor",
            "part_cooling_fan": "Part Cooling Fan",
            "component": "Component",
            "temperature_sensor": "Temperature Sensor",
            "temperature_controller": (
                "Temperature Controller"
            ),
        }

        label = labels.get(
            node_type,
            node_type.replace(
                "_",
                " ",
            ).title(),
        )

        self._node_counter += 1

        node = VisualNode(
            id=f"node-{self._node_counter}",
            node_type=node_type,
            label=label,
            x=scene_position.x(),
            y=scene_position.y(),
        )

        if node_type == "controller":
            controller = Controller(
                id=f"controller-{self._node_counter}",
                name=label,
                controller_type="controller",
            )

            self.store.commit(
                CreateControllerNode(
                    controller=controller,
                    node=node,
                )
            )
        else:
            self._add_default_ports(
                node
            )

            self.store.commit(
                CreateNode(
                    node
                )
            )

        self._last_edit_position = QPointF(
            scene_position
        )

        self.statusBar().showMessage(
            f"Created {label}"
        )

    def _add_default_ports(
        self,
        node: VisualNode,
    ) -> None:
        """Add provisional visual ports for non-controller templates."""
        if node.node_type == "controller":
            return

        if node.node_type == "motor":
            ports = (
                VisualPort(
                    id=f"{node.id}-power",
                    node_id=node.id,
                    label="Power",
                    port_type="power",
                    direction="input",
                    side="left",
                    order=0,
                ),
                VisualPort(
                    id=f"{node.id}-signal",
                    node_id=node.id,
                    label="Signal",
                    port_type="signal",
                    direction="input",
                    side="left",
                    order=1,
                ),
            )
        elif node.node_type == "sensor":
            ports = (
                VisualPort(
                    id=f"{node.id}-power",
                    node_id=node.id,
                    label="Power",
                    port_type="power",
                    direction="input",
                    side="left",
                    order=0,
                ),
                VisualPort(
                    id=f"{node.id}-signal",
                    node_id=node.id,
                    label="Signal",
                    port_type="signal",
                    direction="output",
                    side="right",
                    order=0,
                ),
            )
        elif node.node_type == "temperature_sensor":
            ports = (
                VisualPort(
                    id=f"{node.id}-ground",
                    node_id=node.id,
                    label="Reference / Ground",
                    port_type="electrical",
                    direction="bidirectional",
                    side="left",
                    order=0,
                ),
                VisualPort(
                    id=f"{node.id}-temperature",
                    node_id=node.id,
                    label="Temperature Output",
                    port_type="signal",
                    direction="output",
                    side="right",
                    order=0,
                ),
            )
        elif node.node_type == "temperature_controller":
            ports = (
                VisualPort(
                    id=f"{node.id}-power",
                    node_id=node.id,
                    label="Power Input",
                    port_type="electrical",
                    direction="input",
                    side="left",
                    order=0,
                ),
                VisualPort(
                    id=f"{node.id}-temperature",
                    node_id=node.id,
                    label="Temperature Input",
                    port_type="signal",
                    direction="input",
                    side="right",
                    order=0,
                ),
            )
        elif node.node_type == "part_cooling_fan":
            ports = (
                VisualPort(
                    id=f"{node.id}-power",
                    node_id=node.id,
                    label="Power",
                    port_type="power",
                    direction="input",
                    side="left",
                    order=0,
                ),
                VisualPort(
                    id=f"{node.id}-ground",
                    node_id=node.id,
                    label="Ground",
                    port_type="electrical",
                    direction="input",
                    side="left",
                    order=1,
                ),
            )
        else:
            ports = (
                VisualPort(
                    id=f"{node.id}-port",
                    node_id=node.id,
                    label="Interface",
                    port_type="unknown",
                    direction="unknown",
                    side="right",
                    order=0,
                ),
            )

        for port in ports:
            node.add_port(
                port
            )

    def _suggest_new_node_position(
        self,
    ) -> QPointF:
        """Choose a location near the current editing context."""
        if not self.store.model.nodes:
            return QPointF(
                100.0,
                100.0,
            )

        return QPointF(
            self._last_edit_position.x()
            + 40.0,
            self._last_edit_position.y()
            + 40.0,
        )