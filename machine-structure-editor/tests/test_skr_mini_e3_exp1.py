from __future__ import annotations

import re
from pathlib import Path

import machine_builder.controller_board_fixtures as fixtures
from machine_builder.editor_state import EditorState
from machine_builder.persistence import load_editor_state, save_editor_state
from machine_builder.semantic_model import CanonicalMachineModel, Machine
from machine_builder.visual_model import VisualModel


REPO_ROOT = Path(__file__).resolve().parents[2]
KLIPPER_PATH = (
    REPO_ROOT
    / "firmware_sources"
    / "klipper"
    / "config"
    / "generic-bigtreetech-skr-mini-e3-v3.0.cfg"
)
MARLIN_PATH = (
    REPO_ROOT
    / "firmware_sources"
    / "marlin"
    / "src"
    / "pins"
    / "stm32g0"
    / "pins_BTT_SKR_MINI_E3_V3_0.h"
)

EXPECTED_SAMPLE_POSITIONS = (1, 2, 3, 4, 8, 9, 10)

# These expectations are independently stated in the tests rather than
# importing the fixture's inventory as its own source of truth.
EXPECTED_KLIPPER_ALIASES = {
    "1": "PB5",
    "2": "PA15",
    "3": "PA9",
    "4": "<RST>",
    "5": "PA10",
    "6": "PB9",
    "7": "PB8",
    "8": "PD6",
    "9": "<GND>",
    "10": "<5V>",
}
EXPECTED_MARLIN_PIN_MACRO_VALUES = {
    "1": "PB5",
    "2": "PA15",
    "3": "PA9",
    "4": "-1",
    "5": "PA10",
    "6": "PB9",
    "7": "PB8",
    "8": "PD6",
    "9": "-1",
    "10": "-1",
}
EXPECTED_DIAGRAM_ROLE_LABELS = {
    "1": "BEEPER",
    "2": "BTN_ENC",
    "3": "BTN_EN1",
    "4": "RESET",
    "5": "BTN_EN2",
    "6": "LCD_D4",
    "7": "LCD_RS",
    "8": "LCD_EN",
    "9": "GND",
    "10": "5V",
}
EXPECTED_DOWNSTREAM_ASSIGNMENTS = {
    "1": [{"macro": "BTN_ENC", "expression": "EXP1_01_PIN"}],
    "2": [{"macro": "BEEPER_PIN", "expression": "EXP1_02_PIN"}],
    "3": [],
    "4": [],
    "5": [],
    "6": [],
    "7": [{"macro": "BTN_EN2", "expression": "EXP1_07_PIN"}],
    "8": [{"macro": "BTN_EN1", "expression": "EXP1_08_PIN"}],
    "9": [],
    "10": [],
}
EXPECTED_DOWNSTREAM_BLOCK = {
    "BEEPER_PIN": "EXP1_02_PIN",
    "BTN_EN1": "EXP1_08_PIN",
    "BTN_EN2": "EXP1_07_PIN",
    "BTN_ENC": "EXP1_01_PIN",
}


def make_test_model() -> CanonicalMachineModel:
    model = CanonicalMachineModel()
    model.add_machine(
        Machine(
            id="machine-1",
            name="Bounded SKR EXP1 test machine",
        )
    )
    return model


def build_fixture(label: str = "BIGTREETECH SKR Mini E3 V3.0"):
    model = make_test_model()
    controller, ports = (
        fixtures.add_btt_skr_mini_e3_v3_0_exp1_physical_interfaces(
            model,
            machine_id="machine-1",
            controller_id="btt-skr-mini-e3-v3-0-controller",
            label=label,
        )
    )
    return model, controller, ports


def parse_klipper_aliases(text: str) -> dict[str, str]:
    return {
        str(int(match.group(1))): match.group(2)
        for match in re.finditer(
            r"EXP1_(\d+)=([^,\s]+)",
            text,
        )
    }


def parse_marlin_pin_macro_values(text: str) -> dict[str, str]:
    return {
        str(int(match.group(1))): match.group(2)
        for match in re.finditer(
            r"(?m)^\s*#define\s+EXP1_(\d{2})_PIN\s+(\S+)\s*$",
            text,
        )
    }


def test_checked_in_firmware_sources_support_ten_position_inventory() -> None:
    klipper_text = KLIPPER_PATH.read_text(encoding="utf-8")
    marlin_text = MARLIN_PATH.read_text(encoding="utf-8")

    actual_klipper = parse_klipper_aliases(klipper_text)
    actual_marlin = parse_marlin_pin_macro_values(marlin_text)

    assert actual_klipper == EXPECTED_KLIPPER_ALIASES
    assert actual_marlin == EXPECTED_MARLIN_PIN_MACRO_VALUES

    # The diagram is source evidence separate from the MCU pin macros.
    marlin_lines = marlin_text.splitlines()
    diagram_start = next(
        index
        for index, line in enumerate(marlin_lines)
        if "(BEEPER)" in line and re.search(r"\|\s*1\s+2\s*\|", line)
    )
    actual_diagram_rows = [
        " ".join(line.strip().split())
        for line in marlin_lines[diagram_start : diagram_start + 5]
    ]
    assert actual_diagram_rows == [
        "* (BEEPER) PB5 | 1 2 | PA15 (BTN_ENC)",
        "* (BTN_EN1) PA9 | 3 4 | RESET",
        "* (BTN_EN2) PA10 5 6 | PB9 (LCD_D4)",
        "* (LCD_RS) PB8 | 7 8 | PD6 (LCD_EN)",
        "* GND | 9 10 | 5V",
    ]

    # Assert the observed sequence in one conditional downstream macro block.
    # This is source-block evidence, not proof that the block is active.
    downstream_pattern = re.compile(
        r"(?m)^[ \t]*#define[ \t]+BEEPER_PIN[ \t]+EXP1_02_PIN[ \t]*\r?\n"
        r"^[ \t]*#define[ \t]+BTN_EN1[ \t]+EXP1_08_PIN[ \t]*\r?\n"
        r"^[ \t]*#define[ \t]+BTN_EN2[ \t]+EXP1_07_PIN[ \t]*\r?\n"
        r"^[ \t]*#define[ \t]+BTN_ENC[ \t]+EXP1_01_PIN[ \t]*$"
    )
    match = downstream_pattern.search(marlin_text)
    assert match is not None

    actual_downstream = {
        macro: expression
        for macro, expression in re.findall(
            r"(?m)^\s*#define\s+(\w+)\s+(EXP1_\d{2}_PIN)\s*$",
            match.group(0),
        )
    }
    assert actual_downstream == EXPECTED_DOWNSTREAM_BLOCK


def test_ten_position_inventory_matches_sources_and_stays_separate_from_sample() -> None:
    inventory = fixtures.BTT_SKR_MINI_E3_V3_0_EXP1_SOURCE_INVENTORY

    assert set(inventory) == {str(position) for position in range(1, 11)}
    assert tuple(fixtures.BTT_SKR_MINI_E3_V3_0_EXP1_SAMPLE_POSITIONS) == (
        EXPECTED_SAMPLE_POSITIONS
    )

    for key in sorted(inventory, key=int):
        record = inventory[key]
        assert record["connector_position"] == int(key)
        assert record["klipper_alias"] == EXPECTED_KLIPPER_ALIASES[key]
        assert (
            record["marlin_mcu_pin_macro_name"]
            == f"EXP1_{int(key):02d}_PIN"
        )
        assert (
            record["marlin_mcu_pin_macro_value"]
            == EXPECTED_MARLIN_PIN_MACRO_VALUES[key]
        )
        assert (
            record["marlin_diagram_role_label"]
            == EXPECTED_DIAGRAM_ROLE_LABELS[key]
        )
        assert (
            record[
                "marlin_downstream_peripheral_assignments_in_reviewed_conditional_block"
            ]
            == EXPECTED_DOWNSTREAM_ASSIGNMENTS[key]
        )

    # Positions 5-7 are source-inventoried even though they are not instantiated.
    _, _, ports = build_fixture()
    assert {
        str(port.properties["connector_position"]) for port in ports
    } == {str(position) for position in EXPECTED_SAMPLE_POSITIONS}
    assert {"5", "6", "7"}.isdisjoint(
        {str(port.properties["connector_position"]) for port in ports}
    )


def test_sparse_fixture_uses_distinct_stable_controller_owned_endpoints() -> None:
    model, controller, ports = build_fixture()

    assert tuple(port.properties["connector_position"] for port in ports) == (
        EXPECTED_SAMPLE_POSITIONS
    )
    assert len(ports) == 7
    assert len({port.id for port in ports}) == 7
    assert all(port.id for port in ports)

    for port in ports:
        position = port.properties["connector_position"]
        assert port.id == (
            f"{controller.id}-exp1-position-{position}"
        )
        assert port.component_id is None
        assert port.controller_id == controller.id
        assert port.connector_id == "exp1"
        assert port.pin_id is None
        assert port.direction == "unknown"
        assert port.properties["connector_position_count"] == 10
        assert port.properties["source_inventory_key"] == str(position)

    assert controller.port_ids == [port.id for port in ports]
    assert set(controller.properties["exp1_source_inventory"]) == {
        str(position) for position in range(1, 11)
    }
    assert model.machines["machine-1"].controller_ids == [controller.id]


def test_endpoint_ids_do_not_depend_on_label_or_sample_order(monkeypatch) -> None:
    _, controller_a, ports_a = build_fixture("First display label")
    ids_a = {
        port.properties["connector_position"]: port.id for port in ports_a
    }

    monkeypatch.setattr(
        fixtures,
        "BTT_SKR_MINI_E3_V3_0_EXP1_SAMPLE_POSITIONS",
        tuple(reversed(EXPECTED_SAMPLE_POSITIONS)),
    )
    _, controller_b, ports_b = build_fixture("Different display label")
    ids_b = {
        port.properties["connector_position"]: port.id for port in ports_b
    }

    assert controller_a.id == controller_b.id
    assert controller_a.name != controller_b.name
    assert ids_a == ids_b
    assert tuple(
        port.properties["connector_position"] for port in ports_b
    ) == tuple(reversed(EXPECTED_SAMPLE_POSITIONS))


def test_sample_preserves_separate_mapping_layers_and_unresolved_values() -> None:
    _, controller, ports = build_fixture()
    inventory = controller.properties["exp1_source_inventory"]

    assert controller.properties["marlin_role_configuration_relationship_status"] == (
        "unresolved"
    )
    assert controller.properties["marlin_upstream_origin_status"] == "unknown"
    assert controller.properties[
        "marlin_downstream_assignment_configuration_status"
    ] == "conditional_active_configuration_not_established"

    for port in ports:
        position_key = str(port.properties["connector_position"])
        record = inventory[position_key]

        assert port.properties["klipper_alias"] == record["klipper_alias"]
        assert (
            port.properties["marlin_mcu_pin_macro_name"]
            == record["marlin_mcu_pin_macro_name"]
        )
        assert (
            port.properties["marlin_mcu_pin_macro_value"]
            == record["marlin_mcu_pin_macro_value"]
        )
        assert (
            port.properties["marlin_diagram_role_label"]
            == record["marlin_diagram_role_label"]
        )
        assert (
            port.properties[
                "marlin_downstream_peripheral_assignments_in_reviewed_conditional_block"
            ]
            == record[
                "marlin_downstream_peripheral_assignments_in_reviewed_conditional_block"
            ]
        )
        assert port.properties[
            "marlin_role_configuration_relationship_status"
        ] == "unresolved"
        assert port.properties[
            "marlin_downstream_assignment_configuration_status"
        ] == "conditional_active_configuration_not_established"

        for status_key in (
            "physical_orientation_status",
            "pcb_pad_net_crosswalk_status",
            "cable_mating_face_cavity_status",
            "contact_continuity_status",
            "as_built_harness_wiring_status",
        ):
            assert port.properties[status_key] == "unverified"

        assert len(port.provenance) == 2
        assert any(
            fixtures.BTT_SKR_MINI_E3_V3_0_KLIPPER_REFERENCE_COMMIT
            in entry.source
            for entry in port.provenance
        )
        assert any(
            entry.source == fixtures.BTT_SKR_MINI_E3_V3_0_MARLIN_SOURCE
            for entry in port.provenance
        )

    # Special interface roles must not be silently rewritten as MCU GPIOs.
    ports_by_position = {
        port.properties["connector_position"]: port for port in ports
    }
    assert ports_by_position[4].properties["klipper_alias"] == "<RST>"
    assert ports_by_position[4].properties["marlin_mcu_pin_macro_value"] == "-1"
    assert ports_by_position[9].properties["klipper_alias"] == "<GND>"
    assert ports_by_position[9].properties["marlin_mcu_pin_macro_value"] == "-1"
    assert ports_by_position[10].properties["klipper_alias"] == "<5V>"
    assert ports_by_position[10].properties["marlin_mcu_pin_macro_value"] == "-1"


def test_sparse_fixture_save_reopen_preserves_identity_evidence_and_unknowns(
    tmp_path: Path,
) -> None:
    model, controller, ports = build_fixture()
    state = EditorState(
        visual_model=VisualModel(),
        semantic_model=model,
    )
    destination = tmp_path / "skr-mini-e3-v3-exp1-reference.machine.json"

    save_editor_state(state, destination)
    restored = load_editor_state(destination)

    restored_model = restored.semantic_model
    restored_controller = restored_model.controllers[controller.id]
    restored_ports = {
        port.properties["connector_position"]: port
        for port in restored_model.ports.values()
        if port.controller_id == controller.id
    }

    assert len(restored_ports) == 7
    assert set(restored_ports) == set(EXPECTED_SAMPLE_POSITIONS)
    assert restored_controller.port_ids == controller.port_ids
    assert restored_controller.properties == controller.properties
    assert restored_controller.provenance == controller.provenance

    original_by_position = {
        port.properties["connector_position"]: port for port in ports
    }
    for position, restored_port in restored_ports.items():
        original = original_by_position[position]
        assert restored_port.id == original.id
        assert restored_port.connector_id == "exp1"
        assert restored_port.pin_id is None
        assert restored_port.properties == original.properties
        assert restored_port.provenance == original.provenance

    # The inventory survives as a distinct ten-position map; the instantiated
    # semantic endpoints remain the approved sparse set.
    assert set(
        restored_controller.properties["exp1_source_inventory"]
    ) == {str(position) for position in range(1, 11)}
    assert [
        restored_controller.properties["exp1_source_inventory"][key][
            "connector_position"
        ]
        for key in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
    ] == list(range(1, 11))

    assert restored_controller.properties[
        "marlin_role_configuration_relationship_status"
    ] == "unresolved"
    assert restored_controller.properties[
        "marlin_upstream_origin_status"
    ] == "unknown"

    for port in restored_ports.values():
        assert port.properties[
            "marlin_role_configuration_relationship_status"
        ] == "unresolved"
        assert port.properties["physical_orientation_status"] == "unverified"
        assert port.properties["contact_continuity_status"] == "unverified"
        assert port.properties["as_built_harness_wiring_status"] == "unverified"

def test_checked_in_marlin_source_matches_pinned_sha256() -> None:
    """Pin the reviewed source bytes using canonical line endings."""
    import hashlib
    from pathlib import Path

    from machine_builder.controller_board_fixtures import (
        BTT_SKR_MINI_E3_V3_0_MARLIN_SOURCE,
        BTT_SKR_MINI_E3_V3_0_MARLIN_SNAPSHOT_SHA256,
    )

    expected_source = (
        "firmware_sources/marlin/src/pins/stm32g0/"
        "pins_BTT_SKR_MINI_E3_V3_0.h"
    )
    assert BTT_SKR_MINI_E3_V3_0_MARLIN_SOURCE == expected_source

    repository_root = Path(__file__).resolve().parents[2]
    source_path = repository_root / expected_source
    source_bytes = source_path.read_bytes()
    normalized_source_bytes = source_bytes.replace(b"\r\n", b"\n").replace(b"\r", b"\n").replace(b"\n", b"\r\n")

    actual_sha256 = hashlib.sha256(normalized_source_bytes).hexdigest().upper()
    assert actual_sha256 == BTT_SKR_MINI_E3_V3_0_MARLIN_SNAPSHOT_SHA256, (
        f"Reviewed Marlin snapshot changed: {source_path}; "
        f"expected {BTT_SKR_MINI_E3_V3_0_MARLIN_SNAPSHOT_SHA256}, "
        f"got {actual_sha256}. Review the source before updating its pinned digest."
    )
