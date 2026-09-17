"""Visual editor for canonical controller details."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
)

from .controller import Controller
from .controller_resource import ControllerResource


@dataclass(frozen=True)
class ControllerDetailsResult:
    """Editable controller values returned by the dialog."""

    name: str
    controller_type: str
    version: str | None


class ControllerDetailsDialog(QDialog):
    """Edit and inspect the basic identity of one controller."""

    resource_edit_requested = Signal(str)

    def __init__(
        self,
        controller: Controller,
        machine_name: str,
        parent=None,
        resources: list[ControllerResource] | None = None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle(
            "Controller Details"
        )

        self.setModal(True)

        self._resources = list(
            resources or []
        )

        self._build_ui(
            controller,
            machine_name,
        )

    def _build_ui(
        self,
        controller: Controller,
        machine_name: str,
    ) -> None:
        layout = QVBoxLayout(
            self
        )

        form = QFormLayout()

        self._id_value = QLabel(
            controller.id
        )

        self._id_value.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self._machine_value = QLabel(
            machine_name
        )

        self._machine_value.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self._name_edit = QLineEdit(
            controller.name
        )

        self._type_edit = QLineEdit(
            controller.controller_type
        )

        self._version_edit = QLineEdit(
            ""
            if controller.version is None
            else controller.version
        )

        form.addRow(
            "ID:",
            self._id_value,
        )

        form.addRow(
            "Machine:",
            self._machine_value,
        )

        form.addRow(
            "Name:",
            self._name_edit,
        )

        form.addRow(
            "Type:",
            self._type_edit,
        )

        form.addRow(
            "Version:",
            self._version_edit,
        )

        layout.addLayout(
            form
        )

        resources_label = QLabel(
            f"Controller Resources ({len(self._resources)})"
        )

        layout.addWidget(
            resources_label
        )

        self._resource_list = QListWidget()

        self._resource_list.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self._resource_list.setMinimumHeight(
            100
        )

        self._resource_list.itemDoubleClicked.connect(
            self._resource_item_double_clicked
        )

        if self._resources:
            for resource in self._resources:
                self._resource_list.addItem(
                    self._resource_item(
                        resource
                    )
                )
        else:
            self._resource_list.addItem(
                "No controller resources."
            )

        layout.addWidget(
            self._resource_list
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(
            self.accept
        )

        buttons.rejected.connect(
            self.reject
        )

        layout.addWidget(
            buttons
        )

    @staticmethod
    def _resource_text(
        resource: ControllerResource,
    ) -> str:
        return (
            f"{resource.name} — "
            f"{resource.resource_type}"
        )

    @classmethod
    def _resource_item(
        cls,
        resource: ControllerResource,
    ) -> QListWidgetItem:
        item = QListWidgetItem(
            cls._resource_text(
                resource
            )
        )

        item.setData(
            Qt.ItemDataRole.UserRole,
            resource.id,
        )

        return item

    def _resource_item_double_clicked(
        self,
        item: QListWidgetItem,
    ) -> None:
        resource_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        if not isinstance(
            resource_id,
            str,
        ):
            return

        self.resource_edit_requested.emit(
            resource_id
        )

    def refresh_resource(
        self,
        resource: ControllerResource,
    ) -> bool:
        """Refresh one resource row after semantic editing."""

        for index in range(
            self._resource_list.count()
        ):
            item = self._resource_list.item(
                index
            )

            item_resource_id = item.data(
                Qt.ItemDataRole.UserRole
            )

            if item_resource_id != resource.id:
                continue

            item.setText(
                self._resource_text(
                    resource
                )
            )

            return True

        return False

    def result_data(
        self,
    ) -> ControllerDetailsResult:
        """Return edited controller values."""

        version = (
            self._version_edit.text().strip()
        )

        return ControllerDetailsResult(
            name=self._name_edit.text(),
            controller_type=self._type_edit.text(),
            version=(
                version
                if version
                else None
            ),
        )

    def accept(self) -> None:
        """Validate required controller fields."""

        if not self._name_edit.text().strip():
            self._name_edit.setFocus()
            return

        if not self._type_edit.text().strip():
            self._type_edit.setFocus()
            return

        super().accept()