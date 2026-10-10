"""Regression tests for physical connection details and authoring decisions."""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QApplication, QLabel, QGroupBox

import machine_builder.canvas_interaction as canvas_interaction
import machine_builder.connection_details as connection_details
from machine_builder.canvas_interaction import (
    CanvasInteractionMixin,
    ConnectionDragState,
)
from machine_builder.compatibility import CompatibilityResult
from machine_builder.connection_details import (
    ConnectionEndpointSummary,
    PhysicalConnectionDetailsDialog,
    confirm_conditional_compatibility,
    confirm_unknown_compatibility,
)
from machine_builder.mutations import CreateConnection, CreateNode
from machine_builder.selection_inspector import SelectionInspector
from machine_builder.store import ModelStore
from machine_builder.visual_model import (
    VisualModel,
    VisualNode,
    VisualPort,
)


def _application() -> QApplication:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def _fan_node(
    node_id: str,
    port_id: str,
    label: str,
    port_type: str,
    direction: str,
) -> VisualNode:
    node = VisualNode(
        id=node_id,
        node_type="part_cooling_fan",
        label=label,
    )
    node.ports[port_id] = VisualPort(
        id=port_id,
        node_id=node_id,
        label=label,
        port_type=port_type,
        direction=direction,
        side="left",
        order=0,
    )
    return node


def _canonical_store() -> ModelStore:
    store = ModelStore()
    store.commit(
        CreateNode(
            _fan_node(
                "fan-a",
                "fan-a-power",
                "Power",
                "power",
                "input",
            )
        )
    )
    store.commit(
        CreateNode(
            _fan_node(
                "fan-b",
                "fan-b-ground",
                "Ground",
                "electrical",
                "input",
            )
        )
    )
    return store


def _create_redo_history(store: ModelStore) -> None:
    """Create a redo entry while leaving the canonical connection endpoints intact."""
    store.commit(
        CreateNode(
            _fan_node(
                "fan-history",
                "fan-history-port",
                "History",
                "signal",
                "input",
            )
        )
    )
    assert store.undo()

class _StatusBarStub:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def showMessage(self, message: str) -> None:
        self.messages.append(message)


class _ConnectionCanvasStub(CanvasInteractionMixin):
    def __init__(
        self,
        store: ModelStore,
        source_port_id: str,
        target_port_id: str,
    ) -> None:
        self.store = store
        self._scene_controller = SimpleNamespace(
            find_port_graphics_at=lambda _position: SimpleNamespace(
                port_id=target_port_id
            )
        )
        self._active_connection_drag = ConnectionDragState(
            source_port_id=source_port_id,
            current_scene_position=QPointF(),
        )
        self._active_connection_source = None
        self._active_connection_target = None
        self._connection_preview = None
        self._status_bar = _StatusBarStub()

    def statusBar(self) -> _StatusBarStub:
        return self._status_bar

    def _cancel_connection_drag(
        self,
        preserve_status: bool = False,
    ) -> None:
        self._active_connection_drag = None


class _FakeDetailsDialog:
    class DialogCode:
        Accepted = 1

    def __init__(
        self,
        endpoint_a,
        endpoint_b,
        parent=None,
    ) -> None:
        self.endpoint_a = endpoint_a
        self.endpoint_b = endpoint_b

    def exec(self) -> int:
        return 1

    def result_data(self) -> dict[str, str]:
        return {
            "wire_color": "  Blue  ",
            "harness_id": "  ",
            "notes": "Verified at assembly.",
        }


class _CancelledDetailsDialog(_FakeDetailsDialog):
    def exec(self) -> int:
        return 0


def test_physical_connection_details_dialog_shows_endpoints_and_returns_values() -> None:
    from PySide6.QtWidgets import QPushButton

    _application()
    dialog = PhysicalConnectionDetailsDialog(
        endpoint_a=ConnectionEndpointSummary(
            owner_label="Main Controller",
            port_purpose="UART TX",
            connector_id="J4",
            pin_id="3",
        ),
        endpoint_b=ConnectionEndpointSummary(
            owner_label="Temperature Sensor",
            port_purpose="Signal",
            connector_id="Unspecified",
            pin_id="Unspecified",
        ),
    )

    assert dialog.windowTitle() == "Physical Connection Details"
    assert [
        group.title()
        for group in dialog.findChildren(QGroupBox)
    ] == ["Endpoint A", "Endpoint B"]

    visible_text = "\n".join(
        label.text()
        for label in dialog.findChildren(QLabel)
    )
    assert (
        "Review both endpoints and record any known wire details. "
        "Leave fields blank when the information is unknown or "
        "unverified. Blank fields are saved as unspecified."
    ) in visible_text
    assert (
        "Endpoint A and Endpoint B are labels for this dialog only. "
        "Physical connections are not directional."
    ) in visible_text
    assert (
        "Leave any field blank if unknown. Blank or whitespace-only "
        "fields are saved as unspecified, not as confirmed absence."
    ) in visible_text
    assert "Main Controller" in visible_text
    assert "UART TX" in visible_text
    assert "J4" in visible_text
    assert "Temperature Sensor" in visible_text
    assert set(
        button.text()
        for button in dialog.findChildren(QPushButton)
    ) == {"Create Connection", "Cancel"}

    assert dialog.wire_color_edit.placeholderText() == (
        "Optional; leave blank if unknown."
    )
    assert dialog.harness_id_edit.placeholderText() == (
        "Optional; leave blank if unknown."
    )
    assert dialog.notes_edit.placeholderText() == (
        "Optional; leave blank if unknown."
    )

    dialog.wire_color_edit.setText("Blue")
    dialog.harness_id_edit.setText("H-04")
    dialog.notes_edit.setPlainText("Checked during assembly.")
    assert dialog.result_data() == {
        "wire_color": "Blue",
        "harness_id": "H-04",
        "notes": "Checked during assembly.",
    }
    dialog.close()


def test_compatibility_prompts_have_explicit_continue_and_cancel_buttons(
    monkeypatch,
) -> None:
    boxes = []
    warnings = []

    class FakeMessageBox:
        class Icon:
            Warning = "warning"

        class ButtonRole:
            AcceptRole = "accept"
            RejectRole = "reject"

        class StandardButton:
            Ok = "ok"

        def __init__(self, parent) -> None:
            self.buttons = []
            boxes.append(self)

        def setIcon(self, icon) -> None:
            self.icon = icon

        def setWindowTitle(self, title: str) -> None:
            self.title = title

        def setText(self, message: str) -> None:
            self.message = message

        def addButton(self, label: str, role):
            button = SimpleNamespace(text=label, role=role)
            self.buttons.append(button)
            return button

        def exec(self) -> None:
            self.clicked = self.buttons[-1]

        def clickedButton(self):
            return self.clicked

        @staticmethod
        def warning(parent, title, message, buttons):
            warnings.append((parent, title, message, buttons))

    monkeypatch.setattr(
        connection_details,
        "QMessageBox",
        FakeMessageBox,
    )

    assert confirm_unknown_compatibility(None) is False
    assert confirm_conditional_compatibility(None) is False
    assert connection_details.confirm_visual_only_connection(None) is False
    connection_details.show_incompatible_connection(None)

    assert [button.text for button in boxes[0].buttons] == [
        "Continue",
        "Cancel",
    ]
    assert boxes[0].title == "Compatibility Could Not Be Established"
    assert boxes[0].message == (
        "Machine Builder cannot determine whether these endpoints are "
        "compatible from the available information. Continue only if "
        "you are satisfied that this physical connection is appropriate."
    )

    assert [button.text for button in boxes[1].buttons] == [
        "Continue",
        "Cancel",
    ]
    assert boxes[1].title == "Conditional Compatibility"
    assert boxes[1].message == (
        "The available information indicates that a condition or "
        "qualification applies. This connection has not been established "
        "as unconditionally compatible. Continue only if the condition "
        "is understood and acceptable."
    )

    assert [button.text for button in boxes[2].buttons] == [
        "Draw Visual Connection",
        "Cancel",
    ]
    assert boxes[2].title == "Visual-Only Connection"
    assert boxes[2].message == (
        "At least one endpoint has no canonical physical-port record. "
        "You can draw this connection visually, but its wire color, "
        "harness ID, and notes cannot be retained as physical connection "
        "metadata. No canonical physical connection will be created."
    )

    assert warnings == [
        (
            None,
            "Connection Not Allowed",
            "These endpoints are known to be incompatible. Machine "
            "Builder cannot create this connection.",
            FakeMessageBox.StandardButton.Ok,
        )
    ]

def test_canonical_connection_always_has_metadata_keys() -> None:
    store = _canonical_store()
    store.commit(
        CreateConnection(
            connection_id="connection-default",
            endpoint_a_id="fan-a-power",
            endpoint_b_id="fan-b-ground",
        )
    )

    connection = store.semantic_model.connections[
        "connection-default"
    ]
    assert connection.properties == {
        "wire_color": None,
        "harness_id": None,
        "notes": None,
    }
    assert store.model.connections[
        "connection-default"
    ].geometry == {}


def test_connection_drag_acceptance_saves_metadata_and_inspector_displays_it(
    monkeypatch,
) -> None:
    store = _canonical_store()
    canvas = _ConnectionCanvasStub(
        store,
        "fan-a-power",
        "fan-b-ground",
    )
    monkeypatch.setattr(
        canvas_interaction,
        "check_port_compatibility",
        lambda *_: CompatibilityResult.COMPATIBLE,
    )
    monkeypatch.setattr(
        canvas_interaction,
        "PhysicalConnectionDetailsDialog",
        _FakeDetailsDialog,
    )

    canvas._finish_connection_drag(
        "fan-a-power",
        QPointF(20.0, 20.0),
    )

    connection = store.semantic_model.connections["connection-1"]
    assert connection.properties == {
        "wire_color": "  Blue  ",
        "harness_id": None,
        "notes": "Verified at assembly.",
    }
    assert store.model.connections["connection-1"].geometry == {}

    _application()
    inspector = SelectionInspector()
    inspector.set_connection(
        store.model.connections["connection-1"],
        store.model,
        semantic_model=store.semantic_model,
    )
    text = inspector.debug_text()
    assert "Wire color:" in text
    assert "Blue" in text
    assert "Harness ID: Unspecified" in text
    assert "Notes: Verified at assembly." in text


def test_cancelling_details_dialog_preserves_models_and_history(
    monkeypatch,
) -> None:
    store = _canonical_store()
    _create_redo_history(store)
    canvas = _ConnectionCanvasStub(
        store,
        "fan-a-power",
        "fan-b-ground",
    )
    monkeypatch.setattr(
        canvas_interaction,
        "check_port_compatibility",
        lambda *_: CompatibilityResult.COMPATIBLE,
    )
    monkeypatch.setattr(
        canvas_interaction,
        "PhysicalConnectionDetailsDialog",
        _CancelledDetailsDialog,
    )

    undo_count = len(store._undo_stack)
    redo_count = len(store._redo_stack)
    visual_ids = set(store.model.connections)
    semantic_ids = set(store.semantic_model.connections)

    canvas._finish_connection_drag(
        "fan-a-power",
        QPointF(20.0, 20.0),
    )

    assert set(store.model.connections) == visual_ids
    assert set(store.semantic_model.connections) == semantic_ids
    assert len(store._undo_stack) == undo_count
    assert len(store._redo_stack) == redo_count


@pytest.mark.parametrize(
    ("compatibility_result", "confirmation_name"),
    [
        (
            CompatibilityResult.UNKNOWN,
            "confirm_unknown_compatibility",
        ),
        (
            CompatibilityResult.CONDITIONAL,
            "confirm_conditional_compatibility",
        ),
    ],
)
def test_cancelling_compatibility_warning_preserves_models_and_history(
    monkeypatch,
    compatibility_result,
    confirmation_name: str,
) -> None:
    store = _canonical_store()
    _create_redo_history(store)
    canvas = _ConnectionCanvasStub(
        store,
        "fan-a-power",
        "fan-b-ground",
    )
    confirmation_calls = []

    monkeypatch.setattr(
        canvas_interaction,
        "check_port_compatibility",
        lambda *_: compatibility_result,
    )

    def cancel_confirmation(parent) -> bool:
        confirmation_calls.append(parent)
        return False

    monkeypatch.setattr(
        canvas_interaction,
        confirmation_name,
        cancel_confirmation,
    )

    def unexpected_details_dialog(*args, **kwargs):
        raise AssertionError(
            "The details dialog must not open after compatibility cancellation."
        )

    monkeypatch.setattr(
        canvas_interaction,
        "PhysicalConnectionDetailsDialog",
        unexpected_details_dialog,
    )

    undo_count = len(store._undo_stack)
    redo_count = len(store._redo_stack)

    canvas._finish_connection_drag(
        "fan-a-power",
        QPointF(20.0, 20.0),
    )

    assert len(confirmation_calls) == 1
    assert store.model.connections == {}
    assert store.semantic_model.connections == {}
    assert len(store._undo_stack) == undo_count
    assert len(store._redo_stack) == redo_count


@pytest.mark.parametrize(
    ("compatibility_result", "confirmation_name"),
    [
        (
            CompatibilityResult.UNKNOWN,
            "confirm_unknown_compatibility",
        ),
        (
            CompatibilityResult.CONDITIONAL,
            "confirm_conditional_compatibility",
        ),
    ],
)
def test_confirming_unknown_or_conditional_compatibility_creates_connection(
    monkeypatch,
    compatibility_result,
    confirmation_name: str,
) -> None:
    store = _canonical_store()
    canvas = _ConnectionCanvasStub(
        store,
        "fan-a-power",
        "fan-b-ground",
    )
    confirmation_calls = []

    def accept_confirmation(parent) -> bool:
        confirmation_calls.append(parent)
        return True

    monkeypatch.setattr(
        canvas_interaction,
        "check_port_compatibility",
        lambda *_: compatibility_result,
    )
    monkeypatch.setattr(
        canvas_interaction,
        confirmation_name,
        accept_confirmation,
    )
    monkeypatch.setattr(
        canvas_interaction,
        "PhysicalConnectionDetailsDialog",
        _FakeDetailsDialog,
    )

    undo_count = len(store._undo_stack)
    redo_count = len(store._redo_stack)

    canvas._finish_connection_drag(
        "fan-a-power",
        QPointF(20.0, 20.0),
    )

    assert len(confirmation_calls) == 1
    assert set(store.model.connections) == {"connection-1"}
    assert set(store.semantic_model.connections) == {"connection-1"}
    assert store.semantic_model.connections["connection-1"].properties == {
        "wire_color": "  Blue  ",
        "harness_id": None,
        "notes": "Verified at assembly.",
    }
    assert store.model.connections["connection-1"].geometry == {}
    assert len(store._undo_stack) == undo_count + 1
    assert len(store._redo_stack) == redo_count

def _add_visual_only_port(store: ModelStore) -> None:
    """Add a genuinely unlinked visual endpoint for interaction tests."""
    node = VisualNode(
        id="provisional-node",
        node_type="test",
        label="Provisional Endpoint",
    )
    node.ports["provisional-port"] = VisualPort(
        id="provisional-port",
        node_id=node.id,
        label="Provisional",
        port_type="signal",
        direction="input",
    )
    store.commit(CreateNode(node))
    assert (
        store.model.find_port("provisional-port").semantic_reference
        is None
    )


@pytest.mark.parametrize(
    ("endpoint_a_id", "endpoint_b_id"),
    [
        ("fan-a-power", "provisional-port"),
        ("provisional-port", "fan-a-power"),
    ],
)
def test_stale_reference_with_provisional_endpoint_rejected_without_mutation(
    endpoint_a_id: str,
    endpoint_b_id: str,
) -> None:
    store = _canonical_store()
    _add_visual_only_port(store)
    _create_redo_history(store)

    stale_port = store.model.find_port("fan-a-power")
    stale_port.semantic_reference = "missing-canonical-port"

    visual_nodes_before = set(store.model.nodes)
    visual_connections_before = set(store.model.connections)
    semantic_connections_before = set(store.semantic_model.connections)
    undo_count_before = len(store._undo_stack)
    redo_count_before = len(store._redo_stack)

    with pytest.raises(
        ValueError,
        match="Visual port references unknown canonical port",
    ):
        store.commit(
            CreateConnection(
                connection_id="stale-reference-connection",
                endpoint_a_id=endpoint_a_id,
                endpoint_b_id=endpoint_b_id,
            )
        )

    assert set(store.model.nodes) == visual_nodes_before
    assert set(store.model.connections) == visual_connections_before
    assert (
        set(store.semantic_model.connections)
        == semantic_connections_before
    )
    assert len(store._undo_stack) == undo_count_before
    assert len(store._redo_stack) == redo_count_before
    assert store.can_redo


@pytest.mark.parametrize(
    "compatibility_result",
    [
        CompatibilityResult.UNKNOWN,
        CompatibilityResult.CONDITIONAL,
    ],
)
@pytest.mark.parametrize(
    "accept_visual_only_prompt",
    [False, True],
)
def test_compatibility_confirmation_then_visual_only_prompt(
    monkeypatch,
    compatibility_result: CompatibilityResult,
    accept_visual_only_prompt: bool,
) -> None:
    store = _canonical_store()
    _add_visual_only_port(store)
    _create_redo_history(store)
    canvas = _ConnectionCanvasStub(
        store,
        "fan-a-power",
        "provisional-port",
    )
    decisions = []

    monkeypatch.setattr(
        canvas_interaction,
        "check_port_compatibility",
        lambda *_: compatibility_result,
    )

    def accept_compatibility(_parent) -> bool:
        decisions.append("compatibility")
        return True

    def decide_visual_only(_parent) -> bool:
        decisions.append("visual-only")
        return accept_visual_only_prompt

    monkeypatch.setattr(
        canvas_interaction,
        "confirm_unknown_compatibility",
        accept_compatibility,
    )
    monkeypatch.setattr(
        canvas_interaction,
        "confirm_conditional_compatibility",
        accept_compatibility,
    )
    monkeypatch.setattr(
        canvas_interaction,
        "confirm_visual_only_connection",
        decide_visual_only,
    )

    def unexpected_details_dialog(*args, **kwargs):
        raise AssertionError(
            "The physical details dialog must not open for a visual-only endpoint."
        )

    monkeypatch.setattr(
        canvas_interaction,
        "PhysicalConnectionDetailsDialog",
        unexpected_details_dialog,
    )

    undo_count_before = len(store._undo_stack)
    redo_count_before = len(store._redo_stack)

    canvas._finish_connection_drag(
        "fan-a-power",
        QPointF(20.0, 20.0),
    )

    assert decisions == ["compatibility", "visual-only"]

    if accept_visual_only_prompt:
        assert set(store.model.connections) == {"connection-1"}
        assert store.semantic_model.connections == {}
        assert store.model.connections["connection-1"].geometry == {}
        assert len(store._undo_stack) == undo_count_before + 1
        assert store._redo_stack == []
    else:
        assert store.model.connections == {}
        assert store.semantic_model.connections == {}
        assert len(store._undo_stack) == undo_count_before
        assert len(store._redo_stack) == redo_count_before
        assert store.can_redo


def test_controller_to_component_connection_keeps_endpoint_id_spaces_distinct(
    monkeypatch,
) -> None:
    from machine_builder.controller import Controller
    from machine_builder.controller_visual_mutations import (
        CreateControllerVisualNode,
    )
    from machine_builder.semantic_model import SemanticPort

    store = _canonical_store()
    controller = Controller(
        id="controller-1",
        name="Duet 2 Maestro",
        controller_type="motion_controller",
    )
    store.semantic_model.add_controller("machine-1", controller)
    store.semantic_model.add_port(
        SemanticPort(
            id="controller-1-output",
            component_id=None,
            controller_id=controller.id,
            purpose="Power",
            direction="output",
        )
    )
    store.commit(
        CreateControllerVisualNode(
            controller_id=controller.id,
            node=VisualNode(
                id="controller-node-1",
                node_type="controller",
                label="Controller",
            ),
        )
    )

    visual_controller_port_id = "controller-node-1-power"
    visual_component_port_id = "fan-a-power"
    assert store.model.find_port(visual_controller_port_id) is not None

    canvas = _ConnectionCanvasStub(
        store,
        visual_controller_port_id,
        visual_component_port_id,
    )
    monkeypatch.setattr(
        canvas_interaction,
        "check_port_compatibility",
        lambda *_: CompatibilityResult.COMPATIBLE,
    )
    monkeypatch.setattr(
        canvas_interaction,
        "PhysicalConnectionDetailsDialog",
        _FakeDetailsDialog,
    )

    canvas._finish_connection_drag(
        visual_controller_port_id,
        QPointF(20.0, 20.0),
    )

    semantic_connection = store.semantic_model.connections["connection-1"]
    assert {
        semantic_connection.endpoint_a_id,
        semantic_connection.endpoint_b_id,
    } == {
        "controller-1-output",
        "component-fan-a-power",
    }

    visual_connection = store.model.connections["connection-1"]
    assert visual_connection.endpoint_a_id == visual_controller_port_id
    assert visual_connection.endpoint_b_id == visual_component_port_id
    assert {
        visual_connection.endpoint_a_id,
        visual_connection.endpoint_b_id,
    }.isdisjoint(
        {
            semantic_connection.endpoint_a_id,
            semantic_connection.endpoint_b_id,
        }
    )

    restored_controller = store.semantic_model.controllers["controller-1"]
    controller_port = store.semantic_model.ports["controller-1-output"]
    component_port = store.semantic_model.ports["component-fan-a-power"]
    assert restored_controller.port_ids == ["controller-1-output"]
    assert controller_port.controller_id == "controller-1"
    assert controller_port.component_id is None
    assert controller_port.id in restored_controller.port_ids
    assert component_port.component_id == "component-fan-a"
    assert component_port.controller_id is None
    assert component_port.id in store.semantic_model.components[
        "component-fan-a"
    ].port_ids


def test_physical_connection_metadata_survives_undo_redo(
    monkeypatch,
) -> None:
    store = _canonical_store()
    canvas = _ConnectionCanvasStub(
        store,
        "fan-a-power",
        "fan-b-ground",
    )
    monkeypatch.setattr(
        canvas_interaction,
        "check_port_compatibility",
        lambda *_: CompatibilityResult.COMPATIBLE,
    )
    monkeypatch.setattr(
        canvas_interaction,
        "PhysicalConnectionDetailsDialog",
        _FakeDetailsDialog,
    )

    canvas._finish_connection_drag(
        "fan-a-power",
        QPointF(20.0, 20.0),
    )

    visual_connection_before = store.model.connections["connection-1"]
    semantic_connection_before = store.semantic_model.connections[
        "connection-1"
    ]
    expected_visual_endpoints = (
        visual_connection_before.endpoint_a_id,
        visual_connection_before.endpoint_b_id,
    )
    expected_semantic_endpoints = (
        semantic_connection_before.endpoint_a_id,
        semantic_connection_before.endpoint_b_id,
    )
    expected_properties = {
        "wire_color": "  Blue  ",
        "harness_id": None,
        "notes": "Verified at assembly.",
    }

    assert semantic_connection_before.properties == expected_properties
    assert store.undo()
    assert "connection-1" not in store.model.connections
    assert "connection-1" not in store.semantic_model.connections

    assert store.redo()
    visual_connection_after = store.model.connections["connection-1"]
    semantic_connection_after = store.semantic_model.connections[
        "connection-1"
    ]
    assert (
        visual_connection_after.endpoint_a_id,
        visual_connection_after.endpoint_b_id,
    ) == expected_visual_endpoints
    assert (
        semantic_connection_after.endpoint_a_id,
        semantic_connection_after.endpoint_b_id,
    ) == expected_semantic_endpoints
    assert semantic_connection_after.properties == expected_properties
    assert visual_connection_after.geometry == {}

def test_known_incompatibility_is_blocked_without_mutation(
    monkeypatch,
) -> None:
    store = _canonical_store()
    canvas = _ConnectionCanvasStub(
        store,
        "fan-a-power",
        "fan-b-ground",
    )
    warnings = []

    monkeypatch.setattr(
        canvas_interaction,
        "check_port_compatibility",
        lambda *_: CompatibilityResult.INCOMPATIBLE,
    )
    monkeypatch.setattr(
        canvas_interaction,
        "show_incompatible_connection",
        lambda parent: warnings.append(parent),
    )

    undo_count = len(store._undo_stack)
    redo_count = len(store._redo_stack)

    canvas._finish_connection_drag(
        "fan-a-power",
        QPointF(20.0, 20.0),
    )

    assert len(warnings) == 1
    assert store.model.connections == {}
    assert store.semantic_model.connections == {}
    assert len(store._undo_stack) == undo_count
    assert len(store._redo_stack) == redo_count


def test_duplicate_connection_is_rejected_before_compatibility_or_dialogs(
    monkeypatch,
) -> None:
    store = _canonical_store()
    store.commit(
        CreateConnection(
            connection_id="connection-1",
            endpoint_a_id="fan-a-power",
            endpoint_b_id="fan-b-ground",
        )
    )
    canvas = _ConnectionCanvasStub(
        store,
        "fan-a-power",
        "fan-b-ground",
    )

    def unexpected_check(*args, **kwargs):
        raise AssertionError(
            "A duplicate must be rejected before compatibility checks."
        )

    monkeypatch.setattr(
        canvas_interaction,
        "check_port_compatibility",
        unexpected_check,
    )

    undo_count = len(store._undo_stack)
    redo_count = len(store._redo_stack)

    canvas._finish_connection_drag(
        "fan-a-power",
        QPointF(20.0, 20.0),
    )

    assert set(store.model.connections) == {"connection-1"}
    assert set(store.semantic_model.connections) == {"connection-1"}
    assert len(store._undo_stack) == undo_count
    assert len(store._redo_stack) == redo_count
    assert canvas._status_bar.messages[-1] == (
        "That connection already exists."
    )


def test_cancelling_visual_only_prompt_preserves_models_and_history(
    monkeypatch,
) -> None:
    visual_model = VisualModel()
    node_a = VisualNode(
        id="visual-only-a",
        node_type="provisional",
        label="Provisional A",
    )
    node_a.ports["visual-only-port-a"] = VisualPort(
        id="visual-only-port-a",
        node_id=node_a.id,
        label="A",
        port_type="signal",
        direction="output",
    )
    node_b = VisualNode(
        id="visual-only-b",
        node_type="provisional",
        label="Provisional B",
    )
    node_b.ports["visual-only-port-b"] = VisualPort(
        id="visual-only-port-b",
        node_id=node_b.id,
        label="B",
        port_type="signal",
        direction="input",
    )
    visual_model.add_node(node_a)
    visual_model.add_node(node_b)

    store = ModelStore(model=visual_model)
    _create_redo_history(store)
    canvas = _ConnectionCanvasStub(
        store,
        "visual-only-port-a",
        "visual-only-port-b",
    )

    monkeypatch.setattr(
        canvas_interaction,
        "check_port_compatibility",
        lambda *_: CompatibilityResult.COMPATIBLE,
    )
    monkeypatch.setattr(
        canvas_interaction,
        "confirm_visual_only_connection",
        lambda _parent: False,
    )

    def unexpected_details_dialog(*args, **kwargs):
        raise AssertionError(
            "Physical details must not open after visual-only cancellation."
        )

    monkeypatch.setattr(
        canvas_interaction,
        "PhysicalConnectionDetailsDialog",
        unexpected_details_dialog,
    )

    undo_count = len(store._undo_stack)
    redo_count = len(store._redo_stack)
    visual_node_ids = set(store.model.nodes)
    semantic_component_ids = set(store.semantic_model.components)

    canvas._finish_connection_drag(
        "visual-only-port-a",
        QPointF(20.0, 20.0),
    )

    assert store.model.connections == {}
    assert store.semantic_model.connections == {}
    assert set(store.model.nodes) == visual_node_ids
    assert set(store.semantic_model.components) == semantic_component_ids
    assert len(store._undo_stack) == undo_count
    assert len(store._redo_stack) == redo_count

def test_visual_only_connection_does_not_store_physical_metadata(
    monkeypatch,
) -> None:
    visual_model = VisualModel()

    node_a = VisualNode(
        id="visual-only-a",
        node_type="provisional",
        label="Provisional A",
    )
    node_a.ports["visual-only-port-a"] = VisualPort(
        id="visual-only-port-a",
        node_id=node_a.id,
        label="A",
        port_type="signal",
        direction="output",
    )

    node_b = VisualNode(
        id="visual-only-b",
        node_type="provisional",
        label="Provisional B",
    )
    node_b.ports["visual-only-port-b"] = VisualPort(
        id="visual-only-port-b",
        node_id=node_b.id,
        label="B",
        port_type="signal",
        direction="input",
    )
    visual_model.add_node(node_a)
    visual_model.add_node(node_b)

    store = ModelStore(model=visual_model)
    canvas = _ConnectionCanvasStub(
        store,
        "visual-only-port-a",
        "visual-only-port-b",
    )

    monkeypatch.setattr(
        canvas_interaction,
        "check_port_compatibility",
        lambda *_: CompatibilityResult.COMPATIBLE,
    )
    prompts = []
    monkeypatch.setattr(
        canvas_interaction,
        "confirm_visual_only_connection",
        lambda parent: prompts.append(parent) or True,
    )

    def unexpected_details_dialog(*args, **kwargs):
        raise AssertionError(
            "Physical connection details must not be offered for visual-only endpoints."
        )

    monkeypatch.setattr(
        canvas_interaction,
        "PhysicalConnectionDetailsDialog",
        unexpected_details_dialog,
    )

    canvas._finish_connection_drag(
        "visual-only-port-a",
        QPointF(20.0, 20.0),
    )

    assert len(prompts) == 1
    assert set(store.model.connections) == {"connection-1"}
    assert store.semantic_model.connections == {}
    visual_connection = store.model.connections["connection-1"]
    assert visual_connection.geometry == {}