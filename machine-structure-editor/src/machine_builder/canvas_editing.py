"""Semantic editing workflows for the Machine Structure Editor canvas.

This module owns feature-specific editing workflows for selected canonical
objects. It deliberately does not own window construction, palette
construction, scene synchronization, or interactive connection behavior.
"""

from __future__ import annotations

from PySide6.QtWidgets import QMessageBox

from .component_details import ComponentDetailsDialog
from .controller_details import ControllerDetailsDialog
from .controller_mutations import UpdateController
from .controller_queries import (
    machine_id_for_controller,
)
from .controller_resource_assignment_queries import (
    assignments_for_resource,
)
from .controller_resource_details import (
    ControllerResourceDetailsDialog,
)
from .controller_resource_mutations import (
    UpdateControllerResource,
)
from .controller_resource_queries import (
    get_controller_resource,
    resources_for_controller,
)
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


class CanvasEditingMixin:
    """Provide semantic editing workflows for a canvas host."""

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
            resources=resources_for_controller(
                self.store.semantic_model,
                controller.id,
            ),
        )

        dialog.resource_edit_requested.connect(
            lambda resource_id: (
                self._edit_controller_resource(
                    resource_id=resource_id,
                    controller_id=controller.id,
                    controller_name=controller.name,
                    controller_dialog=dialog,
                )
            )
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

    def _edit_controller_resource(
        self,
        resource_id: str,
        controller_id: str,
        controller_name: str,
        controller_dialog: ControllerDetailsDialog,
    ) -> None:
        """Edit a controller resource from Controller Details."""
        resource = get_controller_resource(
            self.store.semantic_model,
            resource_id,
        )

        if resource.controller_id != controller_id:
            QMessageBox.information(
                self,
                "Controller Resource",
                (
                    "The selected resource is not currently "
                    "owned by this controller."
                ),
            )
            return

        dialog = ControllerResourceDetailsDialog(
            resource=resource,
            controller_name=controller_name,
            parent=controller_dialog,
            assignments=assignments_for_resource(
                self.store.semantic_model,
                resource.id,
            ),
        )

        if (
            dialog.exec()
            != dialog.DialogCode.Accepted
        ):
            return

        result = dialog.result()

        if result is None:
            return

        self.store.commit(
            UpdateControllerResource(
                resource_id=resource.id,
                name=result.name,
                resource_type=result.resource_type,
                controller_id=resource.controller_id,
                properties=dict(
                    resource.properties
                ),
                provenance=list(
                    resource.provenance
                ),
            )
        )

        updated_resource = get_controller_resource(
            self.store.semantic_model,
            resource.id,
        )

        controller_dialog.refresh_resource(
            updated_resource
        )

        self.statusBar().showMessage(
            f"Updated controller resource: {result.name}"
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