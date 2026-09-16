"""Tests for semantic value status handling."""

import pytest

from machine_builder.semantic_value import (
    SemanticValue,
    SemanticValueStatus,
)


def test_known_value_can_store_value() -> None:
    value = SemanticValue(
        status=SemanticValueStatus.KNOWN,
        value=24,
    )

    assert value.status is SemanticValueStatus.KNOWN
    assert value.value == 24
    assert value.has_value


def test_measured_value_can_store_value() -> None:
    value = SemanticValue(
        status=SemanticValueStatus.MEASURED,
        value=23.8,
    )

    assert (
        value.status
        is SemanticValueStatus.MEASURED
    )
    assert value.value == 23.8


def test_derived_value_can_store_value() -> None:
    value = SemanticValue(
        status=SemanticValueStatus.DERIVED,
        value=240,
    )

    assert (
        value.status
        is SemanticValueStatus.DERIVED
    )
    assert value.value == 240


def test_unknown_value_has_no_value() -> None:
    value = SemanticValue(
        status=SemanticValueStatus.UNKNOWN,
    )

    assert (
        value.status
        is SemanticValueStatus.UNKNOWN
    )
    assert value.value is None
    assert not value.has_value


def test_unspecified_value_has_no_value() -> None:
    value = SemanticValue(
        status=SemanticValueStatus.UNSPECIFIED,
    )

    assert (
        value.status
        is SemanticValueStatus.UNSPECIFIED
    )
    assert not value.has_value


def test_not_applicable_value_has_no_value() -> None:
    value = SemanticValue(
        status=SemanticValueStatus.NOT_APPLICABLE,
    )

    assert (
        value.status
        is SemanticValueStatus.NOT_APPLICABLE
    )
    assert not value.has_value


def test_value_required_status_cannot_be_empty() -> None:
    with pytest.raises(
        ValueError,
        match="requires a value",
    ):
        SemanticValue(
            status=SemanticValueStatus.KNOWN,
        )


def test_value_forbidden_status_cannot_store_value() -> None:
    with pytest.raises(
        ValueError,
        match="cannot contain a value",
    ):
        SemanticValue(
            status=SemanticValueStatus.UNKNOWN,
            value="not known",
        )


def test_all_statuses_are_explicitly_defined() -> None:
    assert {
        status.value
        for status in SemanticValueStatus
    } == {
        "absent",
        "unknown",
        "unspecified",
        "not_applicable",
        "known",
        "measured",
        "derived",
        "inferred",
        "configured",
        "calibrated",
    }