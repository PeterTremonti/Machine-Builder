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

`115` controller-owned physical SemanticPorts.

Current connector groups:

* `x-motor` — 4
* `y-motor` — 4
* `e0-motor` — 4
* `e1-motor` — 4
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
* `j4` — 4
* `temp-ob` / J37 — 10
* `j21` — 13
* `e2-driver` — 8
* `e3-driver` — 8

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

The documented J24 / Always-On FAN interface is represented as:

* connector group: `always-on-fan`;
* two controller-owned SemanticPorts;
* position 1 = `GND`, `direction = unknown`, `electrical_role = ground_reference`;
* position 2 = `V_FAN_A`, `direction = output`, `electrical_role = always_on_fan_output`.

J24 is therefore represented as a heterogeneous physical interface rather
than incorrectly labeling its ground contact as a fan output.

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
* PanelDue / J30;
* PanelDue SD / P3;
* 12864 EXP1 / P2;
* 12864 EXP2 / P1;
* USB / J22;
* Ethernet / J38;
* C_GND / J27;
* J21 Expansion;
* J37 / TEMP_DB;
* J16 / E0 HEAT alternate access — design-level; production population unverified;
* J17 / E1 HEAT alternate access — design-level; production population unverified;
* uSDHC / J15;
* fan-voltage selection / J23;
* ERASE;
* A VIN;
* E 5V EN;
* 5V PS / J20.

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

The live handoff has been refreshed after the completed Maestro E0 motor /
J10 implementation checkpoint.

Current verified repository state at this checkpoint:

`HEAD = 9ffd9c4adf5a013b0a5d045fe96b8e87df072d77`

`origin/main = 9ffd9c4adf5a013b0a5d045fe96b8e87df072d77`

`HEAD == origin/main`

Completed Board implementation checkpoints:

E2 / E3 External Stepper Drivers
    `b284c53927dbcd0f775afc8a23140f24496031b1`
    Complete Maestro E2/E3 external stepper-driver interfaces

Y Motor / J8
    `9ffd9c4adf5a013b0a5d045fe96b8e87df072d77`
    Complete Maestro Y motor / J8 installed-fixture representation

E0 Motor / J10
    `2026-10-08`
    Complete Maestro E0 motor / J10 installed-fixture representation

Latest Board-specific fixture validation:

`26 passed in 0.14s`

Latest full repository validation:

`783 passed in 3.92s`

`git diff --check`:

`clean`

The current Maestro fixture produces:

* 84 controller-owned physical ports;
* 6 ControllerResources.

The current Board-specific uncommitted changes are:

* `machine-structure-editor/src/machine_builder/controller_board_fixtures.py`
* `machine-structure-editor/tests/test_controller_board_fixtures.py`
* `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`

No Routing files are modified.


## 24. Verified E2 / E3 implementation checkpoint

The Maestro-specific E2/E3 evidence verification is complete and the
authorized implementation was completed in the Board fixture.

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

The E2/E3 implementation was subsequently committed as:

`b284c53927dbcd0f775afc8a23140f24496031b1`

The 76-port fixture count recorded at the original E2/E3 checkpoint is
historical. The current fixture has 80 physical ports after the later
Y-motor addition.

## 25. Verified Y Motor / J8 implementation checkpoint

The authorized next Board target, Duet 2 Maestro v1.0 Y motor / J8, has
been implemented and locally verified.

### Maestro-specific evidence

The manufacturer-maintained Maestro `Headers.sch` identifies:

* `J8` as `Y MOT`;
* the connector as `CONN_01X04`;
* the footprint as `PIN_ARRAY_4x1`.

Source:

`https://raw.githubusercontent.com/Duet3D/Duet-2-Hardware/master/Duet2/Duet2Maestro_v1.0/Headers.sch`

The Maestro schematic connects the four numbered J8 positions to the
motor nets `Y_MOT_A1`, `Y_MOT_A2`, `Y_MOT_B1`, and `Y_MOT_B2` in schematic
net order.

Separately, Duet3D documentation identifies the four Maestro motor
contacts as `B1`, `B2`, `A1`, and `A2` on the physical board/wiring
representation.

Source:

`https://forum.duet3d.com/topic/22167/nema-14-don-t-work-with-duet-wifi-drivers`

The implementation therefore distinguishes schematic net ordering from
the established physical Maestro motor-contact labeling.

The fixture's semantic motor-contact labels follow the established
Maestro convention:

`B1`, `B2`, `A1`, `A2`

No generic Duet 2 WiFi/Ethernet pin-order source was used for this
implementation.

### Implemented semantic scope

The implementation adds:

* `y-motor` connector grouping to `DUET_2_MAESTRO_CONNECTOR_LAYOUT`;
* four controller-owned physical SemanticPorts;
* physical positions `1`, `2`, `3`, and `4`;
* `pin_label` values `B1`, `B2`, `A1`, `A2`;
* stepper motor coil-terminal purposes matching those labels;
* `direction = "unknown"` consistent with the existing motor-port
  representation.

No Y ControllerResource was added.

The existing Z-A / Z-B resource semantics were not changed.

No reusable Maestro HardwareDefinition was modified.

No machine-specific firmware or configuration was added.

No new canonical Connector, MatingInterface, DriverSocket, DriverModule,
or Contact entity was introduced.

No Routing source or test files were modified.

### Verified test state

Focused Board fixture and Maestro connector-specification tests:

`26 passed in 0.14s`

Full repository suite:

`783 passed in 3.92s`

Board source/test `git diff --check` validation:

`clean`

The E0 implementation did not modify Routing or any other workstream files.

Current Board-specific uncommitted changes are:

* `machine-structure-editor/src/machine_builder/controller_board_fixtures.py`
* `machine-structure-editor/tests/test_controller_board_fixtures.py`
* `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`

## 26. Verified E0 Motor / J10 implementation checkpoint

The authorized next Board target, Duet 2 Maestro v1.0 E0 motor / J10, has
been implemented and locally verified.

### Maestro-specific evidence

The manufacturer-maintained Maestro `Headers.sch` identifies:

* `J10` as `E0 MOT`;
* the connector as `CONN_01X04`;
* the footprint as `PIN_ARRAY_4x1`.

Source:

`https://raw.githubusercontent.com/Duet3D/Duet-2-Hardware/master/Duet2/Duet2Maestro_v1.0/Headers.sch`

The Maestro schematic associates the four J10 positions with the E0 motor
nets `E0_MOT_A1`, `E0_MOT_A2`, `E0_MOT_B1`, and `E0_MOT_B2`.

The reusable Maestro catalog already defines `e0-motor` as part of the
board's motor connector family with:

* `position_count = 4`;
* established contact labels `B1`, `B2`, `A1`, `A2`;
* stepper motor coil-terminal semantics.

### Implemented semantic scope

The implementation adds:

* `e0-motor` connector grouping to `DUET_2_MAESTRO_CONNECTOR_LAYOUT`;
* four controller-owned physical SemanticPorts;
* physical positions `1`, `2`, `3`, and `4`;
* `pin_label` values `B1`, `B2`, `A1`, `A2`;
* corresponding stepper motor coil-terminal purposes;
* `direction = "unknown"` consistent with the established Maestro motor
  representation.

No E0 ControllerResource was added.

The existing E2/E3 and Y-motor implementations were preserved.

No reusable Maestro HardwareDefinition was modified.

No machine-specific firmware or configuration was added.

No new canonical Connector, MatingInterface, DriverSocket, DriverModule,
or Contact entity was introduced.

No Routing source or test files were modified.

### Verified test state

Focused Board fixture and Maestro connector-specification tests:

`26 passed in 0.14s`

Full repository suite:

`783 passed in 3.92s`

`git diff --check`:

`clean`

The fixture now produces:

* 88 controller-owned physical ports;
* 6 ControllerResources.

E1 / J6 is now implemented as the sixth onboard Maestro motor interface.

Evidence basis: the Duet3D Maestro V1.0 `Headers.sch` identifies J6 as
`E1 MOT`, a four-position motor interface. The established Maestro motor
semantic mapping is preserved as positions `1..4` with `B1`, `B2`, `A1`,
and `A2` coil-terminal labels and unknown direction.

The E0 / J10 and E1 / J6 implementations are complete and verified.

### J21 / Expansion implementation

J21 / Expansion is now represented as a thirteen-contact heterogeneous
physical interface using the existing SemanticPort model.

J21 contact mapping:

1  +5V
2  GND
3  RESET
4  EXP_0
5  EXP_1
6  ADVREF
7  VSSA
8  TWCK0
9  TWD0
10 +3.3V
11 SERVO
12 +5V
13 GND

Per-contact electrical roles are represented where established. The SERVO
contact is represented as an output. Expansion, RESET, and I2C signal
directions remain `unknown` where the evidence does not establish a
controller-side direction. Power and reference contacts retain explicit
electrical-role metadata.

No new ControllerResource or Board-specific ontology entity was introduced.

Evidence basis: Duet3D Maestro V1.0 manufacturer schematic, `Headers.sch`,
including the individual J21 contact identities.


### J37 / TEMP_DB implementation

J37 / TEMP_DB is represented as a ten-contact heterogeneous physical
interface using the existing SemanticPort model.

J37 contact mapping:

1  SPI0_CS2
2  GND
3  SPI0_CS1
4  SPI0_SCK
5  SPI0_MOSI
6  SPI0_MISO
7  TWCK0
8  +3.3V
9  TWD0
10 NC

The SPI and I2C signal directions remain `unknown` because the evidence
establishes the signal identities but does not justify controller-side
direction claims. GND and +3.3V retain explicit electrical-role metadata.
NC is retained as an identified non-connection rather than omitted.

Catalog disposition:
interface_role = auxiliary_header
usage_classification = expansion_or_service
evidence_source = DUET2_MAESTRO_HEADERS_SOURCE

No ControllerResource or Board-specific ontology entity was introduced.

Evidence basis: Duet 2 Maestro V1.0 manufacturer Headers.sch identifies
J37 / TEMP_DB and the complete ten-contact signal map.
### J16 / J17 alternate heater-access disposition

J16 and J17 are identified in the Maestro V1.0 design as alternate access
points electrically associated with the E0 and E1 heater circuits:

* J16 — E0 HEAT alternate access;
* J17 — E1 HEAT alternate access.

The available evidence establishes their electrical association and physical
two-position design representation, but does not establish that these
alternate contacts are populated as production-accessible connectors across
the Maestro V1.0 board population.

They are now represented in the reusable Maestro HardwareDefinition under
catalog-level `properties["board_features"]["alternate_heater_access"]`,
with the design-level population status explicitly recorded as unverified.

They are therefore still not projected into the installed Controller fixture
as ordinary SemanticPorts, and they are not added as additional
ControllerResource exposure targets.

No new ontology entity or classification vocabulary was introduced.

This is a deliberate distinction between:

design-level interface evidence
    and
verified production physical interface evidence.

Production-board population evidence may promote these later if justified.
### Maestro service/storage/display interface evidence completion

The remaining targeted external interfaces are now represented at the
appropriate catalog/service level based on the available Maestro V1.0
schematic evidence:

* J15 / uSDHC — nine-contact micro-SD storage/service interface;
* J20 / 5V_PS — three-position five-volt supply / PSU-control header;
* J22 / USB — five-contact USB Micro-B service/communication interface;
* J23 — three-position fan-voltage selection header;
* J27 / C_GND — single-point chassis/ground-bond terminal;
* J30 / PanelDue — four-contact display/serial interface;
* J38 / Ethernet — RJ45 with integrated magnetics;
* P1 / 12864_EXP2;
* P2 / 12864_EXP1;
* P3 / PanelDue_SD.

These remain catalog/service/infrastructure features and are not projected
into the installed Maestro fixture as ordinary machine-topology SemanticPorts.

Evidence boundaries retained:

* J15 contact 9 / SD_CD is physically present in the manufacturer schematic;
  actual firmware card-detect use is not established by current evidence;
* J38 Ethernet connector identity/function is verified, but no generic RJ45
  contact-number mapping is inferred;
* P1 / 12864_EXP2 now has a complete ten-contact mapping:
  1 = SPI0_MISO_BUFF, 2 = SPI0_SCK_BUFF, 3 = ENC_B, 4 = SPI0_CS0,
  5 = ENC_A, 6 = SPI0_MOSI_BUFF, 7 = NC, 8 = RESET_EXT,
  9 = GND, 10 = NC;
* P2 / 12864_EXP1 now has a complete ten-contact mapping:
  1 = BEEP, 2 = ENC_SW, 3 = SPI0_MOSI_LCD_BUFF, 4 = LCD_CS_BUFF,
  5 = SPI0_SCK_LCD_BUFF, 6 = NC, 7 = NC, 8 = NC, 9 = GND,
  10 = +5V.

No new canonical ontology entity was introduced.
### J4 / High Current Terminal implementation

J4 is represented as a four-contact heterogeneous physical interface
using the existing SemanticPort model.

J4 contact mapping:

1  GND
2  V_IN
3  V_IN
4  BED-

The two V_IN contacts remain distinct physical SemanticPorts even though
they are electrically common. Pin 1 retains a ground-reference role.
Pins 2 and 3 are evidenced V_IN power contacts but introduce no new
electrical-role vocabulary. Pin 4 is the bed-heater output return and
is the only J4 contact exposed through the existing Bed Heater
ControllerResource.

No new ControllerResource or Board-specific ontology entity was introduced.

Evidence basis: Duet 2 Maestro V1.0 manufacturer schematic identifies
J4 as the high-current terminal with GND, V_IN, V_IN, and BED- contacts.
## 27. Verified Maestro test/ATE and board-status/observability checkpoint

Verified 2026-10-08 after implementation and test-suite validation.

The Maestro board-level completeness inventory now represents the remaining
test/ATE, board-status/observability, and service-control features at the
catalog level rather than promoting them into ordinary machine topology.

### Test / ATE inventory

`properties["board_features"]["test_ate"]` now records the complete
manufacturer-schematic test-point inventory:

* TP1-TP5 are three-contact Step/Dir/UART ATE test-point arrays for Z, Y, X,
  E0, and E1 respectively;
* TP6-TP14 and TP16 are individual ATE/test points for heater, PWM, fan, and
  diagnostic/test nets;
* 15 test-point features represent 25 physical test contacts in total;
* the manufacturer schematic states that all test points are DNP;
* TP15 is not present and is explicitly not modeled.

These features are catalog metadata only. They are not installed
`SemanticPort` objects and do not become ordinary machine-topology
interfaces.

### Board-status / observability inventory

The catalog now records:

* D3 USB power indicator;
* D4 "Diag" board indicator on the SERVO net, through R104 = 2.2 kΩ to GND;
  exact Maestro-specific firmware diagnostic/status semantics remain unresolved;
* D6 Bed Heat indicator;
* D7 E0 Heat indicator;
* D20 E1 Heat indicator;
* D15 VIN indicator;
* D16 3.3V indicator;
* D17 5V+ indicator;
* J38 integrated Ethernet ACTLED and LINKLED indicators.

D20 is explicitly identified as E1 Heat in the Maestro V1.0 board evidence.

### Service-control inventory

The catalog now records the identified board-level controls:

* S1 RESET;
* JP1 ERASE, already associated with catalog entry `erase`;
* JP9 I 5V EN;
* JP10 E 5V EN, already associated with catalog entry `e-5v-en`.

These remain service/configuration or power-configuration features rather than
ordinary machine-topology `SemanticPort`s.

### Semantic boundary

No new `SemanticPort`, `ControllerResource`, `Connector`, `MatingInterface`,
`DriverSocket`, `DriverModule`, or `Contact` ontology entity was introduced.

The board completeness criterion remains:

* identify relevant board features;
* preserve evidence and uncertainty;
* classify each feature at the appropriate level;
* do not infer unresolved physical or firmware semantics.

### Verification

Focused Maestro interface/specification tests: 11 passed.

Full project test suite: 793 passed in 4.49s.

`git diff --check` passes; the only reported messages are the existing
LF-to-CRLF working-copy normalization warnings.

## 28. Historical handoff disposition

The previous 1,860-line handoff remains preserved at:

`docs/historical/implementation/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF_2026-10-07.md`

The live handoff remains:

`machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`

The archival migration is separate from the implementation checkpoints.

## 29. Immediate next Board action

The Maestro E0 / J10 and E1 / J6 motor interfaces are complete and verified.
Maestro test/ATE, board-status/observability, and identified service-control
inventory are also complete at the appropriate catalog level.

The Maestro V1.0 evidence/coverage boundary is complete at the currently
supported evidence level.

Intentionally retained Maestro evidence boundaries are:
* J38 exact external RJ45 contact numbering;
* J16/J17 universal production population;
* D4 Maestro-specific firmware diagnostic/status semantics.

These are documented evidence boundaries, not missing ontology or unsupported
catalog gaps.

The BTT Octopus V1.1 receiving driver-interface / TMC5160T mating
investigation and its authorized evidence refinement are now complete.

Continue using the completeness criterion:

* every relevant board feature is identified, evidenced, classified, and
  represented at the appropriate semantic level;
* ordinary machine interfaces remain distinguishable from service,
  configuration, power, test/ATE, and board-observability features;
* unresolved contact or net ordering is not guessed.

Additional evidence now available for later coverage includes the resolved
J24 Always-On FAN mapping, the complete J37 TEMP_DB contact mapping, and
the conservative design-level classification of J16/J17 pending production
population evidence.

Promega-specific controller-side application evidence is also closed:
standard single-Z uses J36 / Z A, and the standard Compound PT1000 uses
J14 / E1 TEMP. These are machine-specific application facts and do not
change the reusable Maestro board definition.

## 30. Octopus V1.1 MOTOR_DRIVER receiving-interface evidence checkpoint

Date: 2026-10-08

The Board workstream recorded the verified Octopus V1.1 driver-receiving
interface using the existing catalog/evidence structures.

Established receiving-interface evidence:

* generic interface type: `MOTOR_DRIVER`;
* 18 physical contacts total;
* contacts 1-16 are active driver contacts;
* contact 17 is `NC`;
* contact 18 is `DIAG`;
* Driver 2 is module position M3;
* Driver 2 motor outputs are `MOTOR2_1` and `MOTOR2_2`;
* Octopus Driver 2 contact 6 is `SLEEP` on `DRIVER2_SLP`.

The TMC5160T Pro V1.0 module evidence separately establishes J1-6 as
`CLK` / external clock input.

The cross-interface relationship is intentionally preserved as unresolved:

* Octopus contact 6 remains `SLEEP`;
* TMC5160T J1-6 remains `CLK`;
* they are not represented as equivalent;
* the exact SPI/jumper electrical state remains unresolved.

No new canonical `DriverSocket`, `DriverModule`, `MatingInterface`,
`Connector`, or `Contact` entity was introduced.

The physical mating relationship remains the existing interface-level
`mated_with` relationship between the controller-owned receiving
`SemanticPort` and component-owned TMC5160T module-interface `SemanticPort`.

Implementation files for this checkpoint:

* `machine-structure-editor/src/machine_builder/hardware_catalog.py`
* `machine-structure-editor/src/machine_builder/controller_board_fixtures.py`
* `machine-structure-editor/tests/test_octopus_driver_mating.py`

Verification:

* focused Octopus mating/evidence tests: 8 passed in 0.24s;
* full project suite: 795 passed in 6.18s;
* `git diff --check`: passes.

## 31. Planning Acceptance — Octopus V1.1 / TMC5160T Pro V1.0 Evidence Checkpoint

Planning has reviewed and accepted the Octopus V1.1 / TMC5160T Pro V1.0 evidence checkpoint documented in §30.

The accepted checkpoint is already committed as:

`54ca8e356ffff32e26c8bd4e9be2b75175d042e1`

Do not create a duplicate commit or push.

The accepted evidence boundary remains unchanged:

- Octopus V1.1 Driver 2 contact 6 remains `SLEEP` / `DRIVER2_SLP`.
- TMC5160T Pro V1.0 J1-6 remains `CLK` / external clock input.
- Signal equivalence and the exact SPI/jumper electrical state remain unresolved.
- Existing `SemanticPort` and interface-level `mated_with` semantics are retained. No new canonical ontology entity is required.

Planning acceptance satisfies the review gate for this checkpoint. **Do not begin another Board-family or mating-case investigation without a new Planning assignment.**

## 32. Octopus board-level silkscreen errata evidence checkpoint

Date: 2026-10-09

Classification: Evidence refinement of the accepted Octopus board checkpoint.
This does not introduce another board family or mating case.

Implementation commit: `57299aa` (`Record Octopus board silkscreen errata evidence`).

### Board-level evidence added

`hardware_catalog.py` now defines `BTT_OCTOPUS_BOARD_REVISION_EVIDENCE`
separately from `BTT_OCTOPUS_MOTOR_DRIVER_RECEIVING_INTERFACE_SPEC`.

The board-level evidence is referenced from both the generic Octopus
controller fixture and the Octopus/TMC5160T mating experiment controller.
The controller properties retain `silkscreen_inspection_status` as
`uninspected`. Nominal V1.1 identity does not prove that an individual
board has corrected silkscreen.

Manufacturer evidence recorded:

* Fan polarity markings: the underside markings were incorrectly swapped
  on some early boards. The manufacturer does not enumerate every affected
  connector or establish a precise production boundary. Use the documented
  pinout and schematic, not an affected printed polarity marking, to
  determine electrical mapping.
* SPI3 power labels: the underside 3.3V and GND markings were swapped on
  early boards. The published pinout records contact 1 as GND, contact 2
  as 3.3V, contact 3 as MISO/PB4, contact 4 as MOSI/PB5, contact 5 as
  SCK/PB3, and contact 6 as CS/PA15. The silkscreen error does not establish
  that the actual electrical nets were swapped.
* Raspberry Pi UART: the manufacturer reports two mislabeled pins on the
  underside interface in the very first production run. The corrected
  signal mapping is RX2/PD6 and TX2/PD5. The original incorrect printed
  labels are not individually specified by the reviewed written notice.

### Explicit evidence limits

* No precise serial-number, date, lot, or V1.0/V1.1 production boundary
  is established for identifying an individual board's markings.
* A complete, directly comparable, separately versioned non-Pro V1.0/V1.1
  schematic pair was not established from the reviewed official artifacts.
* The claimed regulator-package transition remains unconfirmed and is
  not represented as an established revision difference.
* Physical inspection is required before assigning an observed silkscreen
  status to a particular installed board.

Sources recorded in the implementation include the official BIGTREETECH
Octopus documentation, the manufacturer's Octopus pinout SVG, and the
official non-Pro hardware repository.

### Semantic boundary and verification

The evidence remains at controller/board level. No new ontology entity
was introduced, and the motor-driver receiving-interface specification
was kept separate.

The accepted TMC5160T discrepancy is unchanged:

* Octopus Driver 2 contact 6 remains SLEEP / DRIVER2_SLP.
* TMC5160T Pro V1.0 J1-6 remains CLK / external clock input.
* Equivalence and the exact SPI/jumper electrical state remain unresolved.

Verification for implementation commit `57299aa`:

* Focused Octopus and generic controller tests: 15 passed.
* Full project test suite: 805 passed in 7.16 seconds.
* `git diff --check`: passed.

No additional board-family or mating-case investigation is authorized by
this evidence refinement.

## 33. Maestro J4 Bed-Heater Capability Evidence and Accepted Correction Plan

**Classification:** Bounded manufacturer-evidence investigation / read-only follow-up
**Follow-up report timestamp:** October 9, 2026, 10:13 p.m. EDT
**Status:** PARTIALLY RESOLVED — J4 correction plan accepted; implementation not authorized
**Repository baseline:** **NOT VERIFIED FOR THIS FOLLOW-UP**

### Investigation scope and baseline boundary

The manufacturer-evidence follow-up itself was read-only and did not inspect or modify the repository. No tests were run as part of that follow-up. Its repository baseline was not verified and must not be backfilled from a different checkout state. Preserve any earlier audit commit and timestamp already recorded in this handoff as a separate historical checkpoint.

This section records the accepted result of that follow-up. It is a later documentation closeout and does not retroactively change the investigation's timestamp or baseline designation.

### Accepted manufacturer capability statement

Duet3D's official [Duet 2 Maestro hardware reference](https://github.com/Duet3D/wiki-content/blob/master/Duet3D_hardware/Duet_2_family/Duet_2_Maestro.md), in the **Operating limits** and **Heating** sections, states that the bed heater supports up to 18 A. The Heating section explicitly qualifies the maximum 18 A figure as subject to thermal testing.

**Accepted capability statement:** Manufacturer-stated bed-heater capability: up to 18 A, subject to thermal testing.

The same reference separately lists the input connector at 25 A maximum. That is not a J4 bed-output rating and must not be treated as one.

The available evidence does not include thermal-test results establishing 18 A as a verified safe operating maximum. It does not establish a distinct numerical ampacity for J4's terminal contacts or a verified safe current limit for the complete bed-output path. Leave the complete circuit's verified safe current limit unassigned.

The official V1.0 schematics support the physical-path identification but do not independently establish the bed path's verified safe current limit:

- [`Headers.sch`](https://github.com/Duet3D/Duet-2-Hardware/blob/master/Duet2/Duet2Maestro_v1.0/Headers.sch) identifies J4 as a four-position high-current terminal and shows the connector labels.
- [`Htr_Fan.sch`](https://github.com/Duet3D/Duet-2-Hardware/blob/master/Duet2/Duet2Maestro_v1.0/Htr_Fan.sch) shows the bed MOSFET control path and the `BED-` switched return.

Do not infer a verified J4 rating from the separate input-connector rating, generic screw-terminal statements, terminal-block family specifications, the MOSFET's individual datasheet, or heater-resistance calculations.

### Accepted physical-interface correction plan

J4 remains the only modeled physical bed-heater connector. When implementation is separately authorized:

- Remove the unsupported synthetic `bed-heat-molex` and `bed-heat-screw` groups.
- Preserve J4 pins 1–4 and the net labels `GND`, `V_IN`, `V_IN`, and `BED-`.
- Distinguish the board power-input purpose of pin 2 from the bed-supply purpose of pin 3 without inventing different electrical nets.
- Relate the existing `bed-heater` resource to J4 pins 3 and 4 only.
- Do not relate the bed-heater resource to J4 pins 1 or 2.
- Preserve the E0/E1 Molex and screw-terminal definitions, ratings, and relationships.
- Do not assign a numeric verified maximum current to J4's contacts or the complete bed-output path.

Keep the manufacturer-stated bed-heater capability, the machine-specific wiring, and the verified safe current limit for the complete circuit distinct. Evidence for one does not establish the others.

The previous J4 implementation description in §26 is retained as a record of the earlier represented state. This section records the subsequently accepted correction plan; it does not claim that the fixture or catalog has already been corrected.

### Authorization and next action

Planning has accepted the J4 physical-interface correction plan. **Implementation remains NOT AUTHORIZED.**

The next action is to await separate explicit implementation authorization. Until then, do not change application source, fixtures, tests, or catalog definitions. Any authorized future implementation must retain the thermal-testing qualification on the 18 A manufacturer statement and leave the complete bed-output path's verified safe current limit unassigned unless adequate evidence establishes it.





-------------------------------------

This is most likely in the wrong place and will need to be fixed by the #3 chat at the next handoff update but it was provided by #3 as the chat limit was reached.

## 34. Maestro V1.0 Controller-Side Endpoint Evidence for Promega Wiring

**Date:** October 10, 2026
**Classification:** Bounded, read-only board-side evidence investigation
**Status:** Endpoint identities substantially documented; machine-side harness mappings remain separate evidence work
**Implementation:** No source or fixture changes authorized or performed by this investigation.

### Scope and source authority

This report establishes the controller/board-side endpoints that can support the first actual Promega wiring graph. It does not infer machine-specific harness connections merely from the presence of a connector on the Duet 2 Maestro.

Primary Duet3D sources:

1. [Maestro V1.0 Headers.sch](https://raw.githubusercontent.com/Duet3D/Duet-2-Hardware/master/Duet2/Duet2Maestro_v1.0/Headers.sch) — schematic sheet 4 of 7, dated 2017-12-05, revision 1.0. This is the primary source for connector reference designators, labels, contact counts, and electrical net identities.
2. [Maestro V1.0 Htr_Fan.sch](https://raw.githubusercontent.com/Duet3D/Duet-2-Hardware/master/Duet2/Duet2Maestro_v1.0/Htr_Fan.sch) — schematic sheet 6 of 7, dated 2017-12-05, revision 1.0. This establishes the bed/E0/E1 heater control paths and FAN0/FAN1/FAN2 output circuits.
3. [Duet2Maestro_Wiring_V1.0_drawing_v1.3.svg](https://github.com/Duet3D/Duet-2-Hardware/blob/master/Duet2/Duet2Maestro_v1.0/Duet2Maestro_Wiring_V1.0_drawing_v1.3.svg) — manufacturer wiring drawing for the Maestro V1.0 board, drawing revision v1.3. Use this for the physical wiring/contact-label convention, rather than reordering physical contacts solely from net names.
4. [Duet3D Duet 2 Maestro hardware reference](https://github.com/Duet3D/wiki-content/blob/master/Duet3D_hardware/Duet_2_family/Duet_2_Maestro.md) and [Wiring your Duet 2](https://docs.duet3d.com/en/How_to_guides/Wiring_your_Duet_2) — supplementary manufacturer documentation.
5. [Promega Duet Maestro Wiring guide](https://promega.printm3d.com/documentation/electronics/duet-maestro-wiring) — machine-specific evidence for the Promega's documented Z-probe wiring and Z-motor jumper considerations.
6. Current published Machine Builder sources: [controller_board_fixtures.py](https://github.com/PeterTremonti/Machine-Builder/blob/main/machine-structure-editor/src/machine_builder/controller_board_fixtures.py) and [hardware_catalog.py](https://github.com/PeterTremonti/Machine-Builder/blob/main/machine-structure-editor/src/machine_builder/hardware_catalog.py). These establish the currently published canonical identifiers and fixture behavior. They are not a fresh inspection of the local checkout.

### Canonical controller and port identity

The canonical reusable HardwareDefinition identifier is:

`duet-2-maestro-v1-0`

The fixture's default Controller identifier is:

`duet-2-maestro-v1-0-controller`

The physical connector groups use the existing SemanticPort model. Port IDs are generated as:

`{controller_id}-{connector_id}-pin-{position}`

These ports are controller-owned (`component_id = None`). A physical connector identity, its individual contact ports, and a logical ControllerResource are distinct concepts. A resource's `exposed_through` relationship identifies which physical ports expose that resource; it is not itself a machine harness connection.

### Motor interfaces

The Maestro hardware catalog identifies five onboard stepper-driver channels and six four-contact physical motor connector groups because the Z driver has two physical access connectors.

| Function             | Board reference and label | Machine Builder canonical connector ID | Evidence and status                                                                 |
| -------------------- | ------------------------- | -------------------------------------- | ----------------------------------------------------------------------------------- |
| X motor              | J9 — X MOT                | `x-motor`                              | Documented in Headers.sch and the V1.0 wiring drawing; four contacts.               |
| Y motor              | J8 — Y MOT                | `y-motor`                              | Documented; four contacts.                                                          |
| Z motor, connector A | J36 — Z A                 | `z-a-motor`                            | Documented; four contacts.                                                          |
| Z motor, connector B | J7 — Z B                  | `z-b-motor`                            | Documented; four contacts. Shares the onboard Z driver, not a sixth onboard driver. |
| E0 motor             | J10 — E0 MOT              | `e0-motor`                             | Documented; four contacts.                                                          |
| E1 motor             | J6 — E1 MOT               | `e1-motor`                             | Documented; four contacts.                                                          |

The published fixture labels the four contacts of these motor groups `B1`, `B2`, `A1`, and `A2` in the established physical contact convention. Schematic net names such as `X_MOT_A1` and `Y_MOT_B1` provide the electrical associations; physical pin ordering should follow the manufacturer wiring drawing.

The existing controller resource `duet-2-maestro-v1-0-controller-z-stepper` is exposed through the Z A and Z B physical connector groups. The Promega guide notes that jumper configuration is required when only one Z motor is used. The two Z connectors should therefore not be represented as two independent onboard Z-driver resources.

The published fixture contains physical motor endpoint groups for X, Y, Z A/B, E0, and E1. It does not currently create separate onboard X/Y/E0/E1 stepper ControllerResources. Their physical endpoints are available; do not invent resource IDs or change the ontology within this wiring task.

### Heater outputs

#### E0 and E1

The primary Headers.sch source identifies:

* J11 — E0 HEAT, two-position terminal, `complib:3.5MM_2X1`;
* J13 — E1 HEAT, two-position terminal, `complib:3.5MM_2X1`.

The Htr_Fan.sch sheet documents the E0 and E1 MOSFET-controlled heater circuits, with `E0_PWM` / `E1_PWM`, `E0-` / `E1-`, and `V_IN` connections. The manufacturer wiring drawing states generic heater-output ratings of 2 A at 24 V for Molex-compatible heater outputs and 5 A at 24 V for screw-terminal heater outputs. Those generic classes should not be reused as ratings for a different connector or complete circuit.

The canonical logical resources are:

* `duet-2-maestro-v1-0-controller-e0-heater`
* `duet-2-maestro-v1-0-controller-e1-heater`

The published fixture currently exposes each resource through the corresponding `e0-heat-screw` / `e0-heat-molex` and `e1-heat-screw` / `e1-heat-molex` groups.

**Important catalog/fixture discrepancy:** The manufacturer schematic identifies J16 (E0 HEAT) and J17 (E1 HEAT) as two-position alternate heater-access points with `PIN_ARRAY_2X1` footprints. The catalog's `board_features["alternate_heater_access"]` explicitly says that production population of J16/J17 is unverified. However, the installed fixture currently instantiates `e0-heat-molex` and `e1-heat-molex` as physical endpoint groups and includes them in the heater resources' exposure relationships.

These facts are not yet reconciled. Do not treat the E0/E1 Molex groups as confirmed populated Promega-board endpoints until population evidence for the actual board is available. Retain the existing catalog and fixture without editing under this report.

#### Bed heater — J4

J4 is the sole modeled physical bed-heater connector following the accepted and implemented correction.

| J4 position | Manufacturer net label | Current fixture purpose  |
| ----------- | ---------------------- | ------------------------ |
| 1           | `GND`                  | Ground reference         |
| 2           | `V_IN`                 | Board power input        |
| 3           | `V_IN`                 | Bed heater supply        |
| 4           | `BED-`                 | Bed heater output return |

The two `V_IN` contacts are electrically common but are distinct physical contact endpoints. The existing resource `duet-2-maestro-v1-0-controller-bed-heater` is exposed through J4 pins 3 and 4 only.

The manufacturer hardware reference states bed-heater capability up to 18 A, subject to thermal testing, and separately lists the input connector at 25 A maximum. The latter is not a J4 output rating. No reviewed thermal-test results establish 18 A as a verified safe maximum for J4 contacts or the complete bed-output path. The verified safe current limit of that complete path remains unassigned.

### Temperature inputs and temperature-daughterboard interface

The manufacturer Headers.sch identifies four direct two-position temperature inputs:

| Function        | Board reference and label | Canonical connector ID | Manufacturer net pair    |
| --------------- | ------------------------- | ---------------------- | ------------------------ |
| Bed temperature | J5 — BED TEMP             | `bed-temp`             | `THERMISTOR0` and `VSSA` |
| E0 temperature  | J12 — E0 TEMP             | `e0-temp`              | `THERMISTOR1` and `VSSA` |
| E1 temperature  | J14 — E1 TEMP             | `e1-temp`              | `THERMISTOR2` and `VSSA` |
| C temperature   | J1 — C TEMP               | `c-temp`               | `THERMISTOR3` and `VSSA` |

These are documented two-position temperature inputs. The catalog classifies them as thermistor/PT1000 inputs and the installed fixture gives their contacts input direction. The precise physical net/contact ordering should be retained from the manufacturer schematic when building individual contact-level connections. The interpretation of `C` as a specific machine subsystem should not be used as a substitute for Promega machine-side evidence.

J37 — TEMP_DB is a separate ten-contact temperature-daughterboard/service interface, canonically `temp-ob`. It is not a fifth direct thermistor input. Do not connect an ordinary thermistor endpoint to TEMP_DB as though it were one of J1/J5/J12/J14; a daughterboard or suitable interface model would be required for that case.

A visualization-relevant limitation remains: the current fixture instantiates two ports per direct temperature input but does not give them explicit contact-level `pin_label` values for `THERMISTOR0`–`THERMISTOR3` and `VSSA`. Connector identities are documented, but individual net-labeled temperature contact endpoints are not fully reflected in the current fixture representation.

### X endstop

The manufacturer schematic identifies J33 as the three-position `X_STOP` connector. Its signal net is `X_STOP_CONN`, with the shared endstop +3.3 V supply and GND contacts.

The canonical fixture connector ID is `x-stop`, with three contact ports. It assigns the first contact the functional/canonical pin label `xstop` and input role, followed by `+3.3V` and `GND`. This is a useful functional alias, but it is not the same string as the schematic's electrical net label `X_STOP_CONN`.

The board-side endpoint is therefore documented; the X endstop switch, connector housing, wire-side pinout, and machine cable termination remain separate machine/harness facts.

### Z-probe interface

The manufacturer schematic identifies J28 — Probe as a five-position interface. The published fixture's canonical connector ID is `z-probe`.

| J28 position | Board-side label | Board-side role          |
| ------------ | ---------------- | ------------------------ |
| 1            | `Z_PROBE_IN`     | Probe signal input       |
| 2            | `GND`            | Ground reference         |
| 3            | `Z_PROBE_MOD`    | Probe MOD control output |
| 4            | `+3.3V`          | 3.3 V supply             |
| 5            | `+5V`            | 5 V supply               |

The Promega wiring guide specifically documents its J28 use: position 1 is the signal wire identified as S10, position 2 is GND/P5, position 3 (MOD) is left empty, position 4 supplies 3.3 V/S9, and position 5 (5 V) is left empty.

This distinction matters: positions 3 and 5 remain physical contacts on the board connector even though the documented Promega harness leaves them unwired. The catalog field `unused_position_numbers: [3, 5]` should not be interpreted as physical contacts being absent. Machine-side unconnected contacts must be represented on the harness/component side, not deleted from the board's physical interface.

### Fan outputs and Always-On FAN

The manufacturer schematic identifies three two-position PWM-controlled fan interfaces:

| Function         | Board reference | Canonical connector ID | Main electrical facts                                     |
| ---------------- | --------------- | ---------------------- | --------------------------------------------------------- |
| Controlled fan 0 | J25 — FAN0      | `fan0`                 | Switched `FAN0-`; positive supply from bank A, `V_FAN_A`. |
| Controlled fan 1 | J29 — FAN1      | `fan1`                 | Switched `FAN1-`; positive supply from bank A, `V_FAN_A`. |
| Controlled fan 2 | J2 — FAN2       | `fan2`                 | Switched `FAN2-`; positive supply from bank B, `V_FAN_B`. |

The supply for bank A is selected via J3 (`+5V`, `V_FAN_A`, `V_IN`); bank B is selected via J23 (`+5V`, `V_FAN_B`, `V_IN`). These are power-configuration interfaces. The controller-side ports for `fan0`, `fan1`, and `fan2` are PWM-controlled outputs.

J24 is the separate two-position Always-On fan connection. The schematic annotates it as “Always on FAN 0” and its connector symbol label says “GND V_IN”; its positive electrical net is `V_FAN_A`, fed from the selectable bank-A supply. The canonical fixture connector ID is `always-on-fan`, with position 1 `GND` and position 2 `V_FAN_A`.

**Always-On discrepancy to preserve:** J24's manufacturer annotation includes “FAN 0,” but it is not the controlled `FAN0` connector J25. The current fixture correctly distinguishes `always-on-fan` from `fan0`. Keep that distinction in labels, visualization, and endpoint authoring. Do not treat J24 as another PWM output or assume the selected bank-A voltage without checking the machine's jumper configuration.

Another visualization limitation is that the current fan output groups have two physical contacts each but do not assign individual port labels for `FANn-` and the corresponding `V_FAN_A` / `V_FAN_B` rail. The catalog identifies each group as a controlled fan output; an explicit per-contact visualization would need those documented contact roles.

### Connector, controller-resource, and harness boundaries

For wiring authoring, preserve these separate layers:

1. **Board connector/interface:** The physical manufacturer identity and connector reference, e.g. J9/X MOT or J28/Probe.
2. **Board contact:** A specific controller-owned SemanticPort such as `duet-2-maestro-v1-0-controller-x-motor-pin-1` or `duet-2-maestro-v1-0-controller-j4-pin-3`.
3. **ControllerResource:** A logical controller facility, such as `...-bed-heater`, `...-e0-heater`, `...-e1-heater`, or `...-z-stepper`, with its `exposed_through` relationships to relevant board contacts.
4. **Machine-side physical endpoint and harness:** The installed motor, heater, sensor, probe, fan, switch, harness connector, and any named cable termination. These require machine-specific evidence and must not be inferred just because an endpoint exists on the controller.

A board's port labels and capabilities do not by themselves establish which Promega cable is connected to which contact, nor whether a design-level alternate connector is populated on the actual board.

### Explicit Promega harness evidence boundary

This report does not resolve the following machine-side mappings:

* P4 / P2;
* H2 / H4;
* S8 / S6;
* P9 / P11.

Those mappings must remain unresolved until backed by the applicable machine-specific wiring evidence or physical inspection. Do not infer them from the board connector inventory or port adjacency. The J28 probe connections mentioned above are included because the Promega wiring guide explicitly describes those five connector positions and which positions are left empty.

### Smallest concrete follow-up for #4

Proceed with the confirmed board-side connector/contact IDs above, and author a physical machine connection only when both endpoints and the machine-side wire/harness evidence are established.

Before using the E0/E1 Molex-compatible endpoints in the Promega connection graph, verify whether J16/J17 are populated on the applicable Promega Maestro board or keep those endpoints provisional. Preserve the known J11/J13 screw-terminal endpoints separately. For J4, use the existing committed bed-resource exposure through pins 3 and 4; do not add an independent safe-current limit.

For unresolved P4/P2, H2/H4, S8/S6, and P9/P11, the immediate deliverable should be a machine-side evidence table containing the source page/figure, exact endpoint labels, confidence/status, and any still-unknown contact—not guessed connections or new ontology. No Board source edit is part of this follow-up.
