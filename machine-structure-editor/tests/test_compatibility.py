from machine_builder.compatibility import (
    CompatibilityResult,
    check_port_compatibility,
)
from machine_builder.visual_model import VisualPort


def make_port(
    port_id: str,
    *,
    port_type: str,
    direction: str,
) -> VisualPort:
    """Create a test port."""
    return VisualPort(
        id=port_id,
        node_id=f"node-{port_id}",
        label=port_id,
        port_type=port_type,
        direction=direction,
    )


def test_signal_output_to_signal_input_is_compatible() -> None:
    source = make_port(
        "temperature-output",
        port_type="signal",
        direction="output",
    )

    target = make_port(
        "temperature-input",
        port_type="signal",
        direction="input",
    )

    assert (
        check_port_compatibility(source, target)
        == CompatibilityResult.COMPATIBLE
    )


def test_signal_output_to_power_input_is_incompatible() -> None:
    source = make_port(
        "temperature-output",
        port_type="signal",
        direction="output",
    )

    target = make_port(
        "power-input",
        port_type="electrical",
        direction="input",
    )

    assert (
        check_port_compatibility(source, target)
        == CompatibilityResult.INCOMPATIBLE
    )


def test_ground_to_temperature_input_is_incompatible() -> None:
    source = make_port(
        "ground",
        port_type="electrical",
        direction="bidirectional",
    )

    target = make_port(
        "temperature-input",
        port_type="signal",
        direction="input",
    )

    assert (
        check_port_compatibility(source, target)
        == CompatibilityResult.INCOMPATIBLE
    )


def test_unknown_port_type_produces_unknown_result() -> None:
    source = make_port(
        "source",
        port_type="unknown",
        direction="output",
    )

    target = make_port(
        "target",
        port_type="signal",
        direction="input",
    )

    assert (
        check_port_compatibility(source, target)
        == CompatibilityResult.UNKNOWN
    )


def test_electrical_to_electrical_is_conditional() -> None:
    source = make_port(
        "power-source",
        port_type="electrical",
        direction="output",
    )

    target = make_port(
        "power-input",
        port_type="electrical",
        direction="input",
    )

    assert (
        check_port_compatibility(source, target)
        == CompatibilityResult.CONDITIONAL
    )


def test_same_port_cannot_connect_to_itself() -> None:
    port = make_port(
        "port-1",
        port_type="signal",
        direction="output",
    )

    assert (
        check_port_compatibility(port, port)
        == CompatibilityResult.INCOMPATIBLE
    )


def test_reversed_signal_direction_is_incompatible() -> None:
    source = make_port(
        "signal-input",
        port_type="signal",
        direction="input",
    )

    target = make_port(
        "signal-output",
        port_type="signal",
        direction="output",
    )

    assert (
        check_port_compatibility(source, target)
        == CompatibilityResult.INCOMPATIBLE
    )