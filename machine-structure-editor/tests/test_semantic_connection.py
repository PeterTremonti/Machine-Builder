"""Tests for canonical physical connections."""

from machine_builder.semantic_connection import (
    SemanticConnection,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
    MachineComponent,
    SemanticPort,
)


def build_model_with_two_ports() -> (
    tuple[
        CanonicalMachineModel,
        SemanticPort,
        SemanticPort,
    ]
):
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    model.add_component(
        "machine-1",
        MachineComponent(
            id="component-a",
            role="Source",
        ),
    )

    model.add_component(
        "machine-1",
        MachineComponent(
            id="component-b",
            role="Consumer",
        ),
    )

    port_a = SemanticPort(
        id="port-a",
        component_id="component-a",
        purpose="Power",
        direction="output",
    )

    port_b = SemanticPort(
        id="port-b",
        component_id="component-b",
        purpose="Power",
        direction="input",
    )

    model.add_port(port_a)
    model.add_port(port_b)

    return (
        model,
        port_a,
        port_b,
    )


def test_connection_contains_each_endpoint() -> None:
    connection = SemanticConnection(
        id="connection-1",
        endpoint_a_id="port-a",
        endpoint_b_id="port-b",
    )

    assert connection.contains_port(
        "port-a"
    )

    assert connection.contains_port(
        "port-b"
    )


def test_connection_does_not_contain_unrelated_port() -> None:
    connection = SemanticConnection(
        id="connection-1",
        endpoint_a_id="port-a",
        endpoint_b_id="port-b",
    )

    assert not connection.contains_port(
        "port-c"
    )


def test_connection_endpoint_order_is_not_semantic() -> None:
    first = SemanticConnection(
        id="connection-1",
        endpoint_a_id="port-a",
        endpoint_b_id="port-b",
    )

    reverse = SemanticConnection(
        id="connection-2",
        endpoint_a_id="port-b",
        endpoint_b_id="port-a",
    )

    assert first.connects_same_ports(
        "port-a",
        "port-b",
    )

    assert first.connects_same_ports(
        "port-b",
        "port-a",
    )

    assert reverse.connects_same_ports(
        "port-a",
        "port-b",
    )


def test_self_connection_is_detected() -> None:
    connection = SemanticConnection(
        id="connection-1",
        endpoint_a_id="port-a",
        endpoint_b_id="port-a",
    )

    assert connection.is_self_connection()


def test_self_connection_is_not_normal_connection() -> None:
    connection = SemanticConnection(
        id="connection-1",
        endpoint_a_id="port-a",
        endpoint_b_id="port-a",
    )

    assert connection.is_self_connection()


def test_canonical_model_accepts_valid_connection() -> None:
    (
        model,
        port_a,
        port_b,
    ) = build_model_with_two_ports()

    connection = SemanticConnection(
        id="connection-1",
        endpoint_a_id=port_a.id,
        endpoint_b_id=port_b.id,
    )

    model.add_connection(
        connection
    )

    assert (
        model.connections[
            "connection-1"
        ]
        is connection
    )


def test_canonical_model_rejects_unknown_endpoint() -> None:
    (
        model,
        port_a,
        _port_b,
    ) = build_model_with_two_ports()

    try:
        model.add_connection(
            SemanticConnection(
                id="connection-1",
                endpoint_a_id=port_a.id,
                endpoint_b_id="missing-port",
            )
        )
    except ValueError as exc:
        assert (
            "Unknown connection endpoint"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected unknown connection endpoint "
            "to be rejected"
        )


def test_canonical_model_rejects_self_connection() -> None:
    (
        model,
        port_a,
        _port_b,
    ) = build_model_with_two_ports()

    try:
        model.add_connection(
            SemanticConnection(
                id="connection-1",
                endpoint_a_id=port_a.id,
                endpoint_b_id=port_a.id,
            )
        )
    except ValueError as exc:
        assert (
            "cannot connect a port to itself"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected self-connection "
            "to be rejected"
        )


def test_canonical_model_rejects_duplicate_connection_in_reverse_order() -> None:
    (
        model,
        port_a,
        port_b,
    ) = build_model_with_two_ports()

    model.add_connection(
        SemanticConnection(
            id="connection-1",
            endpoint_a_id=port_a.id,
            endpoint_b_id=port_b.id,
        )
    )

    try:
        model.add_connection(
            SemanticConnection(
                id="connection-2",
                endpoint_a_id=port_b.id,
                endpoint_b_id=port_a.id,
            )
        )
    except ValueError as exc:
        assert (
            "already exists"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected reverse duplicate "
            "to be rejected"
        )


def test_component_removal_also_removes_related_connections() -> None:
    (
        model,
        port_a,
        port_b,
    ) = build_model_with_two_ports()

    model.add_connection(
        SemanticConnection(
            id="connection-1",
            endpoint_a_id=port_a.id,
            endpoint_b_id=port_b.id,
        )
    )

    model.remove_component(
        "component-a"
    )

    assert (
        "connection-1"
        not in model.connections
    )

    assert "port-a" not in model.ports