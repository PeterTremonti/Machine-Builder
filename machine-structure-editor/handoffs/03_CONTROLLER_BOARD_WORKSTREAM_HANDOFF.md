# Machine Builder — Controller / Board Workstream Handoff

Updated: 2026-10-07

Current repository checkpoint: `437e674` — `Formalize handoff lifecycle and rollover`

Current branch: `main`

`origin/main`: synchronized with `main`

## 1. Workstream purpose and ownership

Workstream #3 owns Controller / Board implementation and Board-specific
hardware modeling.

Primary responsibilities:

* controller and board implementation;
* reusable hardware definitions and hardware catalog data;
* installed Controller representation;
* controller-owned physical SemanticPorts;
* Controller Resources and Board-specific resource exposure;
* concrete Controller / Board fixtures;
* Board-focused regression tests;
* Board-specific physical-interface evidence experiments;
* Controller / Board workstream handoff.

Planning owns shared architectural and ontology decisions.

Research owns research/evidence work outside bounded Board-specific verification.

Routing owns routing implementation.

Do not modify another workstream's implementation, documentation, or handoff
unless explicitly authorized.

## 2. Live-handoff rule

This file is the current continuation state for Workstream #3.

It is not a chronological transcript.

A new Board chat should be able to recover current state and continue from
this file without reconstructing prior chat history.

Historical state and provenance that are no longer required for active
continuation belong in historical material rather than this live handoff.

The previous large handoff remains preserved for historical treatment until
Planning separately authorizes archival disposition.

## 3. Repository / workflow state

The repository uses one shared active `main` branch.

Repository state is authoritative over stale handoffs or memory.

Current verified repository checkpoint:

`437e674 Formalize handoff lifecycle and rollover`

Current branch and remote:

`main...origin/main`

The working tree was clean when this handoff rollover was prepared.

Board work should use:

* PowerShell / terminal;
* Git;
* existing project tooling;
* direct source/test inspection.

Do not use Python/Jupyter/pandas/data-analysis workflows for ordinary
repository inspection, implementation, or testing.

For tracked-file edits:

* prefer small guarded edits;
* preserve UTF-8 and line endings;
* run Board-scoped `git diff --check`;
* inspect the relevant diff;
* run focused tests before the broader suite;
* do not commit/push until the appropriate Planning authorization exists;
* use GitHub Desktop for commits and pushes.

## 4. Established semantic vocabulary

### HardwareDefinition

Reusable catalog description of a physical hardware type.

### MachineComponent

Installed physical hardware instance.

### Controller

Installed controller instance associated with a HardwareDefinition.

### ControllerResource

Logical/controller-owned resource exposed by the controller.

A Controller Resource is not itself a physical connector, contact, or
SemanticPort.

### SemanticPort

Canonical physical interface/access point owned by either a Controller or a
MachineComponent.

Important properties include:

* `controller_id` or `component_id` ownership;
* optional `connector_id`;
* optional `pin_id`;
* arbitrary properties;
* provenance.

`connector_id` is currently a grouping identifier for physical contacts. It
is not a canonical Connector entity.

### ControllerResource --exposed_through--> SemanticPort

Identifies where a Controller Resource is physically exposed.

One Controller Resource may be exposed through multiple physical SemanticPorts.

### SemanticPort --mated_with--> SemanticPort

Identifies a physical interface-to-interface mating relationship, such as a
replaceable driver module and a receiving interface.

This is distinct from `exposed_through`.

### ControllerResourceAssignment

Maps a machine-semantic purpose to a Controller Resource.

It is distinct from physical exposure and physical mating.

## 5. Canonical architectural boundary

The current Controller / Board architecture is:

```text
HardwareDefinition
        |
        v
installed Controller
        |
        v
controller-owned SemanticPorts
        |
        +--> connector_id / pin_id / properties / provenance
        |
        +--> ControllerResource
        |        |
        |        +--exposed_through--> SemanticPort(s)
        |
        +--> physical mating when required
                 |
                 +--mated_with--> SemanticPort
```

The canonical semantic model remains authoritative.

Board fixtures construct canonical objects directly and do not maintain a
parallel Board semantic model.

Board implementation must not directly depend on Routing implementation.

The intended cross-workstream seam remains:

```text
Board / Controller
        |
        v
canonical semantic model
        |
        v
visual representation
        |
        v
Routing
```

No new canonical Connector, Contact, DriverSocket, MatingInterface,
DriverModule, or other Board-specific ontology entity has been justified by
the current evidence.

## 6. Current primary Board specimen

Primary real-board specimen:

`Duet 2 Maestro V1.0`

Installed Controller fixture:

`duet-2-maestro-v1-0-controller`

Reusable HardwareDefinition:

`duet-2-maestro-v1-0`

Current installed Maestro fixture contains:

`60` controller-owned physical SemanticPorts.

Current connector groups:

* `x-motor` — 4
* `z-a-motor` — 4
* `z-b-motor` — 4
* `bed-heat-molex` — 2
* `bed-heat-screw` — 2
* `e0-heat-molex` — 2
* `e0-heat-screw` — 2
* `e1-heat-molex` — 2
* `e1-heat-screw` — 2
* `bed-temp` — 2
* `e0-temp` — 2
* `e1-temp` — 2
* `c-temp` — 2
* `x-stop` — 3
* `y-stop` — 3
* `z-stop` — 3
* `e0-stop` — 3
* `e1-stop` — 3
* `z-probe` — 5
* `fan0` — 2
* `fan1` — 2
* `fan2` — 2
* `always-on-fan` — 2

The fixture does not yet instantiate every interface present in the
hardware catalog.

## 7. Verified motor representation

The Maestro motor family uses controller-owned SemanticPorts with connector
grouping and verified pin labels.

The Z motor outputs are represented as distinct physical groups:

* `z-a-motor`
* `z-b-motor`

The existing Z-stepper Controller Resource is exposed through the physical
ports belonging to both groups.

This establishes the existing one-resource-to-multiple-physical-access-point
pattern.

## 8. Verified endstop representation

Five documented Maestro endstop groups are represented:

* `x-stop`
* `y-stop`
* `z-stop`
* `e0-stop`
* `e1-stop`

Each is a three-position physical interface.

Current documented role pattern:

```text
position 1 -> axis-specific endstop signal
position 2 -> +3.3V supply
position 3 -> GND
```

The signal position is modeled as input.

Power/reference contacts retain their own electrical-role properties.

## 9. Verified heater representation

Three heater resources are represented:

* Bed heater
* E0 heater
* E1 heater

Each resource is exposed through two physical access-point groups:

* Molex-compatible heater interface;
* screw-terminal heater interface.

The fixture therefore demonstrates:

```text
ControllerResource
    --exposed_through--> physical interface A
    --exposed_through--> physical interface B
```

The two physical access types retain their differing documented output
characteristics in the reusable hardware catalog.

## 10. Verified temperature-interface representation

Four two-position temperature-input groups are now represented:

* `bed-temp`
* `e0-temp`
* `e1-temp`
* `c-temp`

All four use:

```text
direction = input
electrical_role = temperature_sensor_input
```

The physical input channel is not automatically assigned to a machine-semantic
sensor or firmware configuration.

### Completed C TEMP checkpoint

Commit:

`8058700e60bbcd96faf4afe0e97482788730ffcb`

Message:

`Complete Maestro C TEMP interface semantics`

Result:

* added explicit `c-temp` physical interface;
* two controller-owned SemanticPorts;
* temperature-input semantics;
* regression coverage;
* focused Board tests: `17 passed`;
* full repository suite: `776 passed`.

## 11. Verified Z Probe representation

The existing five-position `z-probe` physical interface is represented with
controller-owned SemanticPorts.

Position-specific roles:

```text
position 1 -> Z_PROBE_IN
                input
                z_probe_signal_input

position 2 -> GND
                reference
                ground_reference

position 3 -> Z_PROBE_MOD
                output
                z_probe_mod_output

position 4 -> +3.3V
                supply
                power_supply_3v3

position 5 -> +5V
                supply
                power_supply_5v
```

The MOD contact remains a physical SemanticPort.

It was not promoted to a Controller Resource.

### Completed Z Probe checkpoint

Commit:

`643c85347edc2ffeeb40473dc5be83e8f934a70b`

Message:

`Complete Maestro Z Probe interface semantics`

Result:

* position-specific five-contact representation;
* existing SemanticPort model retained;
* regression coverage;
* focused Board tests: `18 passed`;
* full repository suite: `777 passed`.

## 12. Verified controlled-fan representation

Three controlled fan output groups are represented:

* `fan0`
* `fan1`
* `fan2`

Each uses:

```text
direction = output
electrical_role = controlled_fan_output
```

No separate fan ontology was introduced.

## 13. Verified Always-On Fan representation

The documented Always-On Fan interface is represented as:

* connector group: `always-on-fan`;
* two controller-owned SemanticPorts;
* positions `1` and `2`;
* `direction = output`;
* `electrical_role = always_on_fan_output`.

No separate fan Controller Resource or new ontology was introduced.

### Completed Always-On Fan checkpoint

Commit:

`2f90c32593a635f28aad51385743389148a4c32f`

Message:

`Complete Maestro Always-On Fan interface`

Result:

* added explicit two-position Always-On Fan interface;
* output semantics;
* connector-position coverage;
* dedicated semantic regression test;
* focused Board tests: `19 passed`;
* full repository suite: `778 passed`.

## 14. Current Controller Resources in Maestro fixture

The representative Maestro fixture currently creates four Controller
Resources:

* Bed heater;
* E0 heater;
* E1 heater;
* Z stepper driver.

The fixture intentionally does not yet create E2 or E3 Controller Resources.

No Controller Resource assignments are created by the fixture.

## 15. Octopus / replaceable-driver precedent

The Board workstream contains a minimal BTT Octopus / TMC5160T experiment.

It demonstrates that the existing canonical objects are sufficient for a
replaceable driver-module case:

```text
controller-owned receiving SemanticPort
        --mated_with-->
component-owned module SemanticPort
```

The installed TMC5160T is a `MachineComponent` linked to a reusable
HardwareDefinition.

The module mating interface is interface-level with `pin_id = None`.

The experiment did not justify new DriverSocket, DriverModule,
MatingInterface, Connector, or contact-level entities.

## 16. Maestro hardware catalog state

The reusable Maestro catalog contains verified reusable interface
specifications beyond the currently instantiated fixture.

Important documented/current catalog entries include:

* motor interfaces;
* endstop interfaces;
* heater interfaces;
* `bed-temp`;
* `e0-temp`;
* `e1-temp`;
* `c-temp`;
* `z-probe`;
* `fan0`;
* `fan1`;
* `fan2`;
* `always-on-fan`;
* `e2-driver`;
* `e3-driver`;
* PanelDue;
* PanelDue SD;
* 12864 expansion;
* USB;
* Ethernet;
* C_GND;
* J21 Expansion;
* TEMP_OB;
* ERASE;
* A VIN;
* E 5V EN;
* 5V PS.

The broader inventory is catalog evidence, not a statement that all interfaces
are already modeled in the installed fixture.

## 17. Current E2/E3 status

E2 and E3 are already present in the Maestro HardwareDefinition catalog as:

### E2

```text
board_label = E2
position_count = 8
interface_type =
    8-position external stepper-driver module interface
interface_role =
    external_stepper_driver_module_interface
usage_classification =
    expansion_io
evidence_source =
    DUET2_MAESTRO_HEADERS_SOURCE
```

### E3

Equivalent eight-position external stepper-driver module interface.

The existing architecture is considered sufficient for eventual E2/E3
treatment:

```text
E2 Controller Resource
        --exposed_through-->
E2 physical SemanticPorts

E3 Controller Resource
        --exposed_through-->
E3 physical SemanticPorts
```

An installed external driver module would remain a separate physical mating
case:

```text
receiving SemanticPort
        --mated_with-->
module SemanticPort
```

## 18. Exact E2/E3 evidence blocker

The unresolved issue is physical evidence, not ontology.

Manufacturer-specific Maestro evidence has established named E2/E3 signals
including:

```text
E2_STEP
E2_DIR
E2_EN
E2_UART

E3_STEP
E3_DIR
E3_EN
E3_UART
```

However, the current evidence captured by Board work has not established a
trustworthy complete mapping of:

```text
E2 position 1..8 -> exact signal/role
E3 position 1..8 -> exact signal/role
```

Do not copy the numbered signal mapping from the generic Duet 2
WiFi/Ethernet external-driver table.

Do not infer the Maestro contact numbering from that unrelated connector.

The pending evidence task is specifically to inspect the Maestro-specific
`Headers.sch` / equivalent manufacturer source and establish:

* E2 positions 1–8;
* E3 positions 1–8;
* stepper-resource signal contacts;
* power contacts;
* ground/reference contacts;
* support/configuration contacts;
* any genuinely unresolved contacts.

Anything not established by the Maestro-specific source must remain unknown.

## 19. E2/E3 resource-exposure decision boundary

Once the Maestro-specific position mapping is established:

* E2 resource should be exposed through the exact E2 physical SemanticPorts
  corresponding to the externally accessible E2 resource signals;
* E3 resource should be exposed through the exact E3 physical SemanticPorts
  corresponding to the externally accessible E3 resource signals.

Contacts that are only power, reference, support, or otherwise not part of the
logical stepper-resource exposure should remain separately classified and
should not automatically become `exposed_through` targets.

The architecture does not require another association entity.

## 20. E2/E3 implementation status

Do not implement E2/E3 yet.

Current disposition:

```text
Architecture sufficiency:
    CONFIRMED

Existing physical-interface representation:
    SUFFICIENT

Existing Controller Resource representation:
    SUFFICIENT

Existing mated_with representation for future module installation:
    SUFFICIENT

Exact Maestro position mapping:
    NOT YET SUFFICIENTLY EVIDENCED

Implementation authorization:
    NOT YET GRANTED
```

Planning must authorize implementation only after the Maestro-specific
position mapping is sufficiently established.

## 21. Important implementation watches

### Controller-owned SemanticPort query support

Existing semantic-port query helpers have historically been more
component-oriented and may not expose controller-owned physical ports
through equivalent convenience queries.

This is a query-layer limitation, not evidence that controller-owned
SemanticPorts are wrong.

Address it when broader Board/UI query support requires it.

### Hardware catalog ownership

`hardware_catalog.py` contains reusable generic hardware definitions together
with Board-specific Maestro/TMC5160T material.

Do not reorganize that catalog during ordinary Board interface work without
Planning authorization.

### Physical board geometry

Reusable HardwareDefinition data may eventually include trustworthy geometry
of the manufactured board.

Editor placement, rotation, routing geometry, and other presentation/document
state remain separate from reusable physical Board data.

### Machine-specific firmware configuration

RRF versions, Promega-specific settings, axis assignments, and other
machine-specific firmware configuration must not be baked into the reusable
Maestro HardwareDefinition.

## 22. Important files for continuation

Board fixture implementation:

`machine-structure-editor/src/machine_builder/controller_board_fixtures.py`

Reusable hardware catalog:

`machine-structure-editor/src/machine_builder/hardware_catalog.py`

Primary Board fixture tests:

`machine-structure-editor/tests/test_controller_board_fixtures.py`

Maestro connector tests:

`machine-structure-editor/tests/test_duet_2_maestro_connector_specs.py`

Maestro heater tests:

`machine-structure-editor/tests/test_duet_2_maestro_heater_specs.py`

Maestro interface tests:

`machine-structure-editor/tests/test_duet_2_maestro_interface_specs.py`

Octopus mating tests:

`machine-structure-editor/tests/test_octopus_driver_mating.py`

Canonical semantic model:

`machine-structure-editor/src/machine_builder/semantic_model.py`

Semantic relationships:

`machine-structure-editor/src/machine_builder/semantic_relationship.py`

Controller resources:

`machine-structure-editor/src/machine_builder/controller_resource.py`

Workflow authority:

`CHAT_WORKFLOW.md`

## 23. Completed implementation checkpoint summary

```text
C TEMP
    8058700e60bbcd96faf4afe0e97482788730ffcb
    Complete Maestro C TEMP interface semantics

Z Probe
    643c85347edc2ffeeb40473dc5be83e8f934a70b
    Complete Maestro Z Probe interface semantics

Always-On Fan
    2f90c32593a635f28aad51385743389148a4c32f
    Complete Maestro Always-On Fan interface

E2 / E3 External Stepper Drivers
    2026-10-07 22:18:41 -04:00
    Complete Maestro E2/E3 external stepper-driver interfaces
```

Latest Board-specific fixture validation:

`21 passed in 0.10s`

Latest recorded full repository validation associated with the completed
E2/E3 implementation checkpoint:

`780 passed in 3.56s`

The current repository also contains later workflow-history commits, but the
completed Board checkpoints above remain present in `main`.

## 24. Verified E2 / E3 implementation checkpoint

The Maestro-specific E2/E3 evidence verification is complete and the
authorized implementation has been completed in the Board fixture.

Verified physical mapping:

E2 / J18:
1 = V_IN
2 = GND
3 = E2_UART
4 = E2_EN
5 = E2_STEP
6 = E2_DIR
7 = GND
8 = +3.3V

E3 / J26:
1 = V_IN
2 = GND
3 = E3_UART
4 = E3_EN
5 = E3_STEP
6 = E3_DIR
7 = GND
8 = +3.3V

STEP, DIR, and EN are represented as controller-to-driver output signals.
UART is represented as a separate driver configuration/communication
contact.

V_IN, GND, and +3.3V are represented as physical support/power contacts.
The two GND positions remain distinct physical SemanticPorts even though
they share the same electrical net.

Unsupported semantic roles remain unknown rather than being inferred.

The implementation adds:

* `e2-driver` with 8 controller-owned physical ports;
* `e3-driver` with 8 controller-owned physical ports;
* `e2-stepper` ControllerResource;
* `e3-stepper` ControllerResource;
* eight `exposed_through` relationships from `e2-stepper` to the E2 ports;
* eight `exposed_through` relationships from `e3-stepper` to the E3 ports.

The implementation preserves the existing architecture:

HardwareDefinition -> installed Controller -> controller-owned SemanticPort

ControllerResource -> exposed_through -> SemanticPort

No new canonical Connector, DriverSocket, DriverModule, MatingInterface,
or Contact entity was introduced.

No Routing source or test files were modified.

### Verified test state

Focused Board fixture suite:

`21 passed in 0.10s`

Full repository suite:

`780 passed in 3.56s`

`git diff --check`:

`clean`

Current uncommitted changes remain limited to:

* `machine-structure-editor/src/machine_builder/controller_board_fixtures.py`
* `machine-structure-editor/tests/test_controller_board_fixtures.py`
* `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`

The fixture now produces 76 controller-owned physical ports and 6 controller
resources.

## 25. Historical handoff disposition

The previous 1,860-line handoff remains preserved at:

`docs/historical/implementation/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF_2026-10-07.md`

The live handoff remains:

`machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`

The archival migration is separate from this implementation checkpoint.

## 26. Immediate next Board action

The Maestro E2/E3 external stepper-driver implementation is complete and
verified.

Before starting another Board implementation:

1. verify current `git status`;
2. verify current HEAD and `origin/main`;
3. read this live handoff;
4. identify the next authorized Controller / Board task;
5. inspect the existing Board implementation and tests before changing source.

Do not modify Routing files unless a future task explicitly requires a
cross-workstream contract change and that change is separately authorized.

The E2/E3 implementation is currently uncommitted. Commit and push remain
separate actions after final review.
