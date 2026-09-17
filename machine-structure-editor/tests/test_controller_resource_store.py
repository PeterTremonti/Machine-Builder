import pytest

from machine_builder.controller import Controller
from machine_builder.controller_resource import (
    ControllerResource,
)
from machine_builder.controller_resource_mutations import (
    SetControllerResourceProperty,
    UpdateControllerResource,
)
from machine_builder.store import ModelStore
from machine_builder.semantic_model import Machine


def make_store() -> ModelStore:
    store = ModelStore()

    store.semantic_model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    store.semantic_model.add_controller(
        "machine-1",
        Controller(
            id="controller-1",
            name="Main Controller",
            controller_type="test",
        ),
    )

    store.semantic_model.add_controller_resource(
        "machine-1",
        ControllerResource(
            id="resource-1",
            name="Heater",
            resource_type="heater",
            controller_id="controller-1",
        ),
    )

    return store


def test_update_resource_commits_to_store():
    store = make_store()

    store.commit(
        UpdateControllerResource(
            resource_id="resource-1",
            name="Bed Heater",
            resource_type="heater",
            controller_id="controller-1",
        )
    )

    resource = (
        store.semantic_model
        .controller_resources["resource-1"]
    )

    assert resource.name == "Bed Heater"
    assert store.is_modified is True
    assert store.can_undo is True


def test_update_resource_can_be_undone():
    store = make_store()

    store.commit(
        UpdateControllerResource(
            resource_id="resource-1",
            name="Bed Heater",
            resource_type="heater",
            controller_id="controller-1",
        )
    )

    assert store.undo() is True

    resource = (
        store.semantic_model
        .controller_resources["resource-1"]
    )

    assert resource.name == "Heater"


def test_update_resource_can_be_redone():
    store = make_store()

    store.commit(
        UpdateControllerResource(
            resource_id="resource-1",
            name="Bed Heater",
            resource_type="heater",
            controller_id="controller-1",
        )
    )

    store.undo()
    assert store.redo() is True

    resource = (
        store.semantic_model
        .controller_resources["resource-1"]
    )

    assert resource.name == "Bed Heater"


def test_resource_property_commits_to_store():
    store = make_store()

    store.commit(
        SetControllerResourceProperty(
            resource_id="resource-1",
            name="max_current",
            value=5,
        )
    )

    resource = (
        store.semantic_model
        .controller_resources["resource-1"]
    )

    assert (
        resource.properties["max_current"]
        == 5
    )


def test_resource_property_can_be_undone():
    store = make_store()

    store.semantic_model.controller_resources[
        "resource-1"
    ].properties["max_current"] = 3

    store.commit(
        SetControllerResourceProperty(
            resource_id="resource-1",
            name="max_current",
            value=5,
        )
    )

    assert store.undo() is True

    resource = (
        store.semantic_model
        .controller_resources["resource-1"]
    )

    assert resource.properties["max_current"] == 3


def test_failed_resource_update_is_atomic():
    store = make_store()

    original = (
        store.semantic_model
        .controller_resources["resource-1"]
    )

    with pytest.raises(ValueError):
        store.commit(
            UpdateControllerResource(
                resource_id="resource-1",
                name="",
                resource_type="heater",
                controller_id="controller-1",
            )
        )

    resource = (
        store.semantic_model
        .controller_resources["resource-1"]
    )

    assert resource.name == original.name
    assert store.can_undo is False