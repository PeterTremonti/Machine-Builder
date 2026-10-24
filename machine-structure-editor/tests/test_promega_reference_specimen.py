from __future__ import annotations

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QApplication

from machine_builder.canvas import MachineCanvas
from machine_builder.persistence import load_editor_state
from machine_builder.promega_fixtures import (
    add_promega_firmware_configuration_evidence,
    add_promega_operational_fan_assignments,
)
from machine_builder.semantic_component_mutations import UpdateMachineComponent
from machine_builder.semantic_model import Provenance
from machine_builder.semantic_port_mutations import UpdateSemanticPort


PROMEGA_ROLES = (
    ("X motion motor", "motor"),
    ("Y motion motor", "motor"),
    ("Z motion motor", "motor"),
    ("Compound left-drive motor", "motor"),
    ("Compound right-drive motor", "motor"),
    ("Compound mixing nozzle/tool assembly", "component"),
    ("Compound hotend heater", "component"),
    ("Compound hotend temperature sensor", "temperature_sensor"),
    ("Bed heater", "component"),
    ("Bed temperature sensor", "temperature_sensor"),
    ("Part-cooling/nozzle fan", "component"),
    ("Hotend heatsink/cold-section fan", "component"),
    ("X homing endstop", "sensor"),
    ("IR Z probe", "sensor"),
)


def test_promega_roles_use_existing_authoring_and_persistence_paths(tmp_path):
    application = QApplication.instance()
    if application is None:
        application = QApplication([])

    canvas = MachineCanvas()
    canvas.create_node_from_template(
        "duet_2_maestro_v1_0", QPointF(100.0, 100.0)
    )
    model = canvas.store.semantic_model

    assert len(model.controllers) == 1
    controller = next(iter(model.controllers.values()))
    assert controller.hardware_definition_id is not None
    assert controller.properties["physical_revision_status"] == (
        "not_verified_as_built"
    )

    controller_node = next(
        node for node in canvas.store.model.nodes.values()
        if node.semantic_reference == controller.id
    )
    assert controller_node.node_type == "controller"

    # Record evidence on an existing board endpoint without assigning
    # a Promega component, harness, or verified physical connection.
    board_port = next(
        port for port in model.ports.values()
        if port.controller_id == controller.id and port.component_id is None
    )
    port_note = Provenance(
        source="Machine Builder Duet 2 Maestro reference-board definition",
        evidence_type="authored",
        method="manual review",
        context="Controller-owned endpoint; no component or harness assignment.",
        date="2026-10-10",
        notes=(
            "Does not verify physical continuity, the installed board revision, "
            "harness mapping, or firmware resource use."
        ),
    )
    expected_port_evidence = list(board_port.provenance) + [port_note]
    canvas.store.commit(
        UpdateSemanticPort(
            port_id=board_port.id,
            provenance_entries=expected_port_evidence,
        )
    )

    created = []
    last_original = None
    last_evidence = None

    for index, (role, node_type) in enumerate(PROMEGA_ROLES, start=1):
        node_id = f"node-{len(canvas.store.model.nodes) + 1}"
        canvas.create_node_from_template(
            node_type,
            QPointF(100.0 + index * 80.0, 160.0 + index * 35.0),
        )
        node = canvas.store.model.nodes[node_id]
        component = model.components[node.semantic_reference]

        assert component.hardware_definition_id is None
        if node_type == "motor":
            functional_port_id = (
                f"{component.id}-motor-electrical-interface"
            )
            assert component.port_ids == [functional_port_id]
            assert model.ports[functional_port_id].component_id == component.id
        else:
            assert component.port_ids == []

        if index == len(PROMEGA_ROLES):
            last_original = (
                component.role,
                component.label,
                dict(component.properties),
                list(component.provenance),
            )

        properties = dict(component.properties)
        properties.update({
            "specimen_scope": "promega_compound_reference",
            "verification_status": "role_only_identity_unverified",
            "physical_presence_status": "not_verified_as_built",
            "inventory_crosswalk_status": "not_established",
            "firmware_assignment_status": "not_established",
            "verification_notes": (
                "Role only; exact installed identity, physical variant, "
                "and wiring remain unverified."
            ),
            "inventory_crosswalk_notes": (
                "No product identity or inventory identifier inferred."
            ),
        })
        evidence = Provenance(
            source="Planning milestone: First Promega Reference Specimen",
            evidence_type="authored",
            method="manual transcription",
            context=f"Planning-defined role only: {role}.",
            date="2026-10-10",
            notes=(
                "The checkpoint lists an accepted inventory deliverable but "
                "does not contain its detailed table. Do not infer a part "
                "number, hardware definition, physical endpoint, or connection."
            ),
        )
        canvas.store.commit(
            UpdateMachineComponent(
                component_id=component.id,
                role=role,
                label=role,
                properties=properties,
                provenance_entries=[evidence],
            )
        )
        created.append((role, node_id, component.id, evidence))
        if index == len(PROMEGA_ROLES):
            last_evidence = evidence

    assert len(created) == 14
    assert len(model.components) == 14
    assert len(model.controllers) == 1
    assert len(model.machines["machine-1"].component_ids) == 14
    assert len({role for role, *_ in created}) == 14

    for role, node_id, component_id, evidence in created:
        component = model.components[component_id]
        node = canvas.store.model.nodes[node_id]
        assert component.role == role
        assert component.label == role == node.label
        assert node.semantic_reference == component.id
        assert component.hardware_definition_id is None
        if node.node_type == "motor":
            functional_port_id = (
                f"{component.id}-motor-electrical-interface"
            )
            assert component.port_ids == [functional_port_id]
            assert model.ports[functional_port_id].component_id == component.id
        else:
            assert component.port_ids == []
        assert component.provenance == [evidence]
        assert component.properties["inventory_crosswalk_status"] == (
            "not_established"
        )
        assert component.properties["firmware_assignment_status"] == (
            "not_established"
        )

    # The last edit must undo and redo without duplicating evidence.
    assert last_original is not None and last_evidence is not None
    last_role, _, last_id, _ = created[-1]
    assert canvas.store.undo()
    undone = canvas.store.semantic_model.components[last_id]
    assert (undone.role, undone.label) == last_original[:2]
    assert undone.properties == last_original[2]
    assert undone.provenance == last_original[3]

    assert canvas.store.redo()
    redone = canvas.store.semantic_model.components[last_id]
    assert redone.role == last_role
    assert redone.provenance == [last_evidence]
    assert redone.hardware_definition_id is None

    path = tmp_path / "promega-reference-specimen.machine.json"
    canvas.store.save(path)
    restored = load_editor_state(path)
    restored_model = restored.semantic_model

    assert len(restored_model.controllers) == 1
    assert len(restored_model.components) == 14
    assert len(restored.visual_model.nodes) == 15
    assert len(restored_model.machines["machine-1"].component_ids) == 14

    restored_controller = next(iter(restored_model.controllers.values()))
    assert restored_controller.properties["physical_revision_status"] == (
        "not_verified_as_built"
    )
    restored_roles = {
        component.role: component
        for component in restored_model.components.values()
    }
    assert set(restored_roles) == {role for role, _ in PROMEGA_ROLES}

    for role, node_id, component_id, evidence in created:
        component = restored_model.components[component_id]
        node = restored.visual_model.nodes[node_id]
        assert restored_roles[role].id == component_id
        assert component.label == role
        assert component.hardware_definition_id is None
        if node.node_type == "motor":
            functional_port_id = (
                f"{component.id}-motor-electrical-interface"
            )
            assert component.port_ids == [functional_port_id]
            assert restored_model.ports[
                functional_port_id
            ].component_id == component.id
        else:
            assert component.port_ids == []
        assert component.provenance == [evidence]
        assert node.label == role
        assert node.semantic_reference == component_id

    restored_port = restored_model.ports[board_port.id]
    assert restored_port.controller_id == restored_controller.id
    assert restored_port.component_id is None
    assert restored_port.provenance == expected_port_evidence

def test_promega_operational_fan_assignments_are_provenanced_and_persisted(tmp_path):
    application = QApplication.instance()
    if application is None:
        application = QApplication([])

    canvas = MachineCanvas()
    canvas.create_node_from_template(
        "duet_2_maestro_v1_0", QPointF(100.0, 100.0)
    )
    model = canvas.store.semantic_model
    controller = next(iter(model.controllers.values()))

    fan_roles = (
        "Hotend heatsink/cold-section fan",
        "Part-cooling/nozzle fan",
    )
    fan_component_ids = {}

    for index, role in enumerate(fan_roles, start=1):
        old_node_ids = set(canvas.store.model.nodes)
        canvas.create_node_from_template(
            "component", QPointF(180.0 + index * 120.0, 220.0)
        )
        new_nodes = [
            node for node in canvas.store.model.nodes.values()
            if node.id not in old_node_ids and node.node_type == "component"
        ]
        assert len(new_nodes) == 1
        component_id = new_nodes[0].semantic_reference
        assert component_id is not None
        component = model.components[component_id]

        properties = dict(component.properties)
        properties.update({
            "specimen_scope": "promega_compound_reference",
            "physical_presence_status": "not_verified_as_built",
            "physical_wiring_status": "not_verified_as_built",
            "inventory_crosswalk_status": "not_established",
            "firmware_assignment_status": "not_established",
        })
        role_evidence = Provenance(
            source="Planning milestone: First Promega Reference Specimen",
            evidence_type="authored",
            method="manual transcription",
            context=f"Planning-defined role only: {role}.",
            date="2026-10-23",
            notes=(
                "Exact installed identity and physical cable/contact mapping "
                "remain unverified."
            ),
        )
        canvas.store.commit(
            UpdateMachineComponent(
                component_id=component_id,
                role=role,
                label=role,
                properties=properties,
                provenance_entries=[role_evidence],
            )
        )
        fan_component_ids[role] = component_id

    semantic_connections_before = set(model.connections)
    assignments = add_promega_operational_fan_assignments(
        canvas, fan_component_ids, controller.id
    )

    assert set(assignments) == set(fan_roles)
    assert set(model.connections) == semantic_connections_before

    resource_suffixes = {
        "fan0": "fan-0",
        "fan1": "fan-1",
        "fan2": "fan-2",
        "always-on-fan": "always-on-fan",
    }
    for connector_id, suffix in resource_suffixes.items():
        resource_id = f"{controller.id}-{suffix}"
        resource = model.controller_resources[resource_id]
        assert resource.controller_id == controller.id
        assert resource.resource_type == "fan_output"
        assert resource.properties["board_connector_id"] == connector_id

        board_ports = [
            port for port in model.ports.values()
            if port.controller_id == controller.id
            and port.component_id is None
            and port.connector_id == connector_id
        ]
        assert len(board_ports) == 2
        expected_roles = (
            {"ground_reference", "always_on_fan_output"}
            if connector_id == "always-on-fan"
            else {"controlled_fan_output"}
        )
        assert {port.properties.get("electrical_role") for port in board_ports} == expected_roles
        for port in board_ports:
            relationship_id = f"{resource_id}-exposed-through-{port.id}"
            relationship = model.relationships[relationship_id]
            assert relationship.source_id == resource_id
            assert relationship.target_id == port.id
            assert relationship.relationship_type == "exposed_through"
            assert relationship.properties["physical_conductor_mapping_status"] == (
                "not_established"
            )

    source_ids = set(fan_component_ids.values())
    fan_assignments = [
        assignment for assignment in model.controller_resource_assignments.values()
        if assignment.source_id in source_ids
    ]
    assert len(fan_assignments) == 2
    assert {assignment.source_id for assignment in fan_assignments} == source_ids
    inactive_resource_ids = {
        f"{controller.id}-{resource_suffixes['fan1']}",
        f"{controller.id}-{resource_suffixes['always-on-fan']}",
    }
    assert all(
        assignment.resource_id not in inactive_resource_ids
        for assignment in fan_assignments
    )

    expected = {
        "Hotend heatsink/cold-section fan": ("fan0", "0", "FAN0/P0"),
        "Part-cooling/nozzle fan": ("fan2", "2", "FAN2/P2"),
    }
    for role, (connector_id, fan_index, output_label) in expected.items():
        component = model.components[fan_component_ids[role]]
        evidence = assignments[role]
        assignment_id = f"{component.id}-promega-operational-fan-assignment"
        assignment = model.controller_resource_assignments[assignment_id]
        assert assignment.source_id == component.id
        assert assignment.resource_id == f"{controller.id}-fan-{fan_index}"
        assert assignment.assignment_type == "controls"
        assert assignment.properties["operational_assignment_status"] == (
            "user_reported_operational"
        )
        assert assignment.properties["board_connector_id"] == connector_id
        assert assignment.properties["output_label"] == output_label
        assert assignment.properties["physical_cable_crosswalk_status"] == (
            "not_established"
        )
        assert assignment.provenance == [evidence]

        assert component.properties["operational_assignment_status"] == (
            "user_reported_operational"
        )
        assert component.properties["operational_assignment_basis"] == (
            "user_reported_working_installation"
        )
        assert component.properties["operational_controller_id"] == controller.id
        assert component.properties["operational_output_connector_id"] == connector_id
        assert component.properties["operational_output_index"] == fan_index
        assert component.properties["operational_output_label"] == output_label
        assert component.properties["physical_output_contact_mapping_status"] == (
            "not_established"
        )
        assert component.properties["physical_cable_crosswalk_status"] == (
            "not_established"
        )
        assert evidence.evidence_type == "user_report"
        assert evidence.source == (
            "User-reported installed Promega operational configuration"
        )
        assert evidence.method == "user report"
        assert "P9/P11 cable-to-output crosswalk" in evidence.notes
        assert component.provenance[-1] == evidence

    inactive_port_ids = {
        port.id for port in model.ports.values()
        if port.controller_id == controller.id
        and port.component_id is None
        and port.connector_id in {"fan1", "always-on-fan"}
    }
    assert inactive_port_ids
    assert all(
        connection.endpoint_a_id not in inactive_port_ids
        and connection.endpoint_b_id not in inactive_port_ids
        for connection in model.connections.values()
    )

    path = tmp_path / "promega-fan-assignments.machine.json"
    canvas.store.save(path)
    restored = load_editor_state(path)
    restored_model = restored.semantic_model

    assert set(restored_model.connections) == semantic_connections_before
    restored_roles = {
        component.role: component
        for component in restored_model.components.values()
    }
    for role, (connector_id, fan_index, output_label) in expected.items():
        component = restored_roles[role]
        evidence = assignments[role]
        assignment_id = f"{component.id}-promega-operational-fan-assignment"
        assignment = restored_model.controller_resource_assignments[assignment_id]
        assert assignment.source_id == component.id
        assert assignment.resource_id == f"{controller.id}-fan-{fan_index}"
        assert assignment.assignment_type == "controls"
        assert assignment.properties["operational_assignment_status"] == (
            "user_reported_operational"
        )
        assert assignment.properties["board_connector_id"] == connector_id
        assert assignment.properties["output_label"] == output_label
        assert assignment.properties["physical_cable_crosswalk_status"] == (
            "not_established"
        )
        assert assignment.provenance == [evidence]
        assert component.properties["operational_assignment_status"] == (
            "user_reported_operational"
        )
        assert component.properties["operational_controller_id"] == controller.id
        assert component.properties["operational_output_connector_id"] == connector_id
        assert component.properties["operational_output_index"] == fan_index
        assert component.properties["operational_output_label"] == output_label
        assert component.properties["physical_output_contact_mapping_status"] == (
            "not_established"
        )
        assert component.properties["physical_cable_crosswalk_status"] == (
            "not_established"
        )
        assert component.provenance[-1] == evidence

    for connector_id, suffix in resource_suffixes.items():
        resource_id = f"{controller.id}-{suffix}"
        resource = restored_model.controller_resources[resource_id]
        assert resource.controller_id == controller.id
        assert resource.resource_type == "fan_output"
        assert resource.properties["board_connector_id"] == connector_id
        board_ports = [
            port for port in restored_model.ports.values()
            if port.controller_id == controller.id
            and port.component_id is None
            and port.connector_id == connector_id
        ]
        assert len(board_ports) == 2
        for port in board_ports:
            relationship_id = f"{resource_id}-exposed-through-{port.id}"
            relationship = restored_model.relationships[relationship_id]
            assert relationship.source_id == resource_id
            assert relationship.target_id == port.id
            assert relationship.relationship_type == "exposed_through"
            assert relationship.properties["physical_conductor_mapping_status"] == (
                "not_established"
            )

    restored_fan_assignments = [
        assignment
        for assignment in restored_model.controller_resource_assignments.values()
        if assignment.source_id in source_ids
    ]
    assert len(restored_fan_assignments) == 2
    assert {assignment.source_id for assignment in restored_fan_assignments} == source_ids
    assert all(
        assignment.resource_id not in inactive_resource_ids
        for assignment in restored_fan_assignments
    )
    restored_inactive_port_ids = {
        port.id for port in restored_model.ports.values()
        if port.controller_id == controller.id
        and port.component_id is None
        and port.connector_id in {"fan1", "always-on-fan"}
    }
    assert restored_inactive_port_ids
    assert all(
        connection.endpoint_a_id not in restored_inactive_port_ids
        and connection.endpoint_b_id not in restored_inactive_port_ids
        for connection in restored_model.connections.values()
    )

def test_promega_reported_firmware_configuration_is_provenanced_and_persisted(tmp_path):
    application = QApplication.instance()
    if application is None:
        application = QApplication([])

    canvas = MachineCanvas()
    canvas.create_node_from_template(
        "duet_2_maestro_v1_0", QPointF(100.0, 100.0)
    )
    model = canvas.store.semantic_model
    controller = next(iter(model.controllers.values()))

    expected_commands = [
        "M584 X0 Y1 Z2",
        "M350 X16 Y16 Z16 I1",
        "M92 X80 Y80 Z282.7",
        "M208 X0:380 Y0:380 Z0:380",
        "M669 K1",
        "G31 P500 X30.4 Y30.7 Z0.7",
    ]

    from machine_builder.promega_fixtures import (
        PROMEGA_REPORTED_FIRMWARE_CONFIGURATION_COMMANDS,
    )

    assert list(PROMEGA_REPORTED_FIRMWARE_CONFIGURATION_COMMANDS) == (
        expected_commands
    )

    original_properties = dict(controller.properties)
    original_provenance = list(controller.provenance)
    connection_ids_before = set(model.connections)
    port_ids_before = set(model.ports)
    resource_ids_before = set(model.controller_resources)
    assignment_ids_before = set(model.controller_resource_assignments)

    evidence = add_promega_firmware_configuration_evidence(
        canvas, controller.id
    )

    controller = canvas.store.semantic_model.controllers[controller.id]
    configuration = controller.properties["reported_firmware_configuration"]

    assert configuration == {
        "status": "user_reported_working_configuration",
        "commands": expected_commands,
        "installed_sd_card_verification_status": "not_independently_verified",
    }
    assert {
        key: value
        for key, value in controller.properties.items()
        if key != "reported_firmware_configuration"
    } == original_properties
    assert controller.provenance == original_provenance + [evidence]

    assert evidence.source == (
        "User-reported working Promega firmware configuration"
    )
    assert evidence.evidence_type == "user_report"
    assert evidence.method == "user report"
    assert "supplied order are preserved" in evidence.context
    assert "not been independently" in evidence.notes
    assert "E-driver" in evidence.notes
    assert "endstop mappings" in evidence.notes
    assert "driver-index-to-physical-connector/contact mappings" in evidence.notes

    # Firmware evidence alone must not assert new physical wiring or mappings.
    assert set(model.connections) == connection_ids_before
    assert set(model.ports) == port_ids_before
    assert set(model.controller_resources) == resource_ids_before
    assert set(model.controller_resource_assignments) == assignment_ids_before
    assert set(controller.properties) - set(original_properties) == {
        "reported_firmware_configuration"
    }
    assert set(configuration) == {
        "status",
        "commands",
        "installed_sd_card_verification_status",
    }

    path = tmp_path / "promega-reported-firmware-configuration.machine.json"
    canvas.store.save(path)
    restored = load_editor_state(path)
    restored_model = restored.semantic_model
    restored_controller = restored_model.controllers[controller.id]

    assert restored_controller.properties["reported_firmware_configuration"] == (
        configuration
    )
    assert {
        key: value
        for key, value in restored_controller.properties.items()
        if key != "reported_firmware_configuration"
    } == original_properties
    assert restored_controller.provenance == original_provenance + [evidence]

    assert set(restored_model.connections) == connection_ids_before
    assert set(restored_model.ports) == port_ids_before
    assert set(restored_model.controller_resources) == resource_ids_before
    assert (
        set(restored_model.controller_resource_assignments)
        == assignment_ids_before
    )
