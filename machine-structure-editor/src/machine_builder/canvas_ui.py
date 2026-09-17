"""Qt user-interface construction for the Machine Structure Editor."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QGraphicsScene,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .component_details import ComponentDetailsDialog
from .controller_details import ControllerDetailsDialog
from .controller_mutations import UpdateController
from .controller_queries import (
    machine_id_for_controller,
)
from .graphics.palette import PaletteList
from .graphics.view import MachineGraphicsView
from .port_details import PortDetailsDialog
from .semantic_component_mutations import (
    UpdateMachineComponent,
)
from .semantic_component_queries import (
    component_for_visual_node,
    machine_id_for_component,
)
from .semantic_controller_queries import (
    controller_for_visual_node,
)
from .semantic_port_mutations import (
    UpdateSemanticPort,
)
from .semantic_port_queries import (
    component_for_port,
    get_port,
)


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

        main_layout.addWidget(
            palette_panel
        )

        main_layout.addWidget(
            self.view,
            1,
        )

        self.statusBar().showMessage(
            "Ready"
        )

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

    def _edit_selected_component(
        self,
    ) -> None:
        """Open the component editor for the selected visual node."""
        selected_nodes = [
            item
            for item in self.scene.selectedItems()
            if hasattr(
                item,
                "node_id",
            )
        ]

        if not selected_nodes:
            self.statusBar().showMessage(
                "Select a component first."
            )
            return

        if len(selected_nodes) > 1:
            QMessageBox.information(
                self,
                "Edit Component",
                "Select one component at a time.",
            )
            return

        node_id = selected_nodes[0].node_id

        component = component_for_visual_node(
            self.store.state,
            node_id,
        )

        if component is None:
            QMessageBox.information(
                self,
                "Edit Component",
                (
                    "The selected visual node is not "
                    "linked to a canonical component yet."
                ),
            )
            return

        machine_id = machine_id_for_component(
            self.store.state,
            component.id,
        )

        machine = (
            self.store.semantic_model.machines[
                machine_id
            ]
        )

        dialog = ComponentDetailsDialog(
            component=component,
            machine_name=machine.name,
            parent=self,
        )

        if (
            dialog.exec()
            != dialog.DialogCode.Accepted
        ):
            return

        result = dialog.result_data()

        self.store.commit(
            UpdateMachineComponent(
                component_id=component.id,
                role=result.role,
                label=result.label,
                properties=result.properties,
            )
        )

        self.statusBar().showMessage(
            f"Updated component: {result.label}"
        )

    def _edit_selected_controller(
        self,
    ) -> None:
        """Open the controller editor for the selected visual node."""
        selected_nodes = [
            item
            for item in self.scene.selectedItems()
            if hasattr(
                item,
                "node_id",
            )
        ]

        if not selected_nodes:
            self.statusBar().showMessage(
                "Select a controller first."
            )
            return

        if len(selected_nodes) > 1:
            QMessageBox.information(
                self,
                "Edit Controller",
                "Select one controller at a time.",
            )
            return

        node_id = selected_nodes[0].node_id

        node = self.store.model.nodes.get(
            node_id
        )

        if node is None:
            QMessageBox.information(
                self,
                "Edit Controller",
                "The selected visual node no longer exists.",
            )
            return

        if node.node_type != "controller":
            QMessageBox.information(
                self,
                "Edit Controller",
                "The selected visual node is not a controller.",
            )
            return

        controller = controller_for_visual_node(
            self.store.state,
            node_id,
        )

        if controller is None:
            QMessageBox.information(
                self,
                "Edit Controller",
                (
                    "The selected visual node is not "
                    "linked to a canonical controller yet."
                ),
            )
            return

        machine_id = machine_id_for_controller(
            self.store.state,
            controller.id,
        )

        machine = (
            self.store.semantic_model.machines[
                machine_id
            ]
        )

        dialog = ControllerDetailsDialog(
            controller=controller,
            machine_name=machine.name,
            parent=self,
        )

        if (
            dialog.exec()
            != dialog.DialogCode.Accepted
        ):
            return

        result = dialog.result_data()

        self.store.commit(
            UpdateController(
                controller_id=controller.id,
                name=result.name,
                controller_type=result.controller_type,
                version=result.version,
            )
        )

        self.statusBar().showMessage(
            f"Updated controller: {result.name}"
        )

    def _edit_semantic_port(
        self,
        port_id: str,
    ) -> None:
        """Open the semantic editor for one port."""
        port = get_port(
            self.store.state,
            port_id,
        )

        component = component_for_port(
            self.store.state,
            port_id,
        )

        dialog = PortDetailsDialog(
            port=port,
            component_label=component.label,
            parent=self,
        )

        if (
            dialog.exec()
            != dialog.DialogCode.Accepted
        ):
            return

        result = dialog.result_data()

        self.store.commit(
            UpdateSemanticPort(
                port_id=port_id,
                purpose=result.purpose,
                direction=result.direction,
                connector_id=result.connector_id,
                pin_id=result.pin_id,
                properties=result.properties,
            )
        )

        self.statusBar().showMessage(
            f"Updated port: {result.purpose}"
        )

    def _frame_all(self) -> None:
        """Fit all current objects into the visible canvas."""
        if not self.store.model.nodes:
            return

        bounds = self.scene.itemsBoundingRect()

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