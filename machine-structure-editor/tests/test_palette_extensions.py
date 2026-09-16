"""Tests for optional palette entries."""

from PySide6.QtCore import Qt

from machine_builder.palette_extensions import (
    add_chamber_heater_template,
)


class FakePalette:
    """Minimal palette test double."""

    def __init__(self) -> None:
        self.items = []

    def addItem(
        self,
        item,
    ) -> None:
        self.items.append(
            item
        )


class FakeWindow:
    """Minimal editor-window test double."""

    def __init__(self) -> None:
        self.palette = FakePalette()


def test_chamber_heater_template_is_added() -> None:
    window = FakeWindow()

    add_chamber_heater_template(
        window
    )

    assert len(
        window.palette.items
    ) == 1


def test_chamber_heater_template_has_expected_label() -> None:
    window = FakeWindow()

    add_chamber_heater_template(
        window
    )

    item = (
        window.palette.items[0]
    )

    assert item.text() == (
        "Chamber Heater"
    )


def test_chamber_heater_template_has_expected_node_type() -> None:
    window = FakeWindow()

    add_chamber_heater_template(
        window
    )

    item = (
        window.palette.items[0]
    )

    assert (
        item.data(
            Qt.ItemDataRole.UserRole
        )
        == "chamber_heater"
    )