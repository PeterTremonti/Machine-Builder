# Machine Builder — Controller / Board Workstream Handoff

Updated: 2026-10-17

Current repository checkpoint: `3d8c24f` — `Clarify console output and handoff formatting rules`

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

**Latest inspected local checkpoint (2026-10-17):**
- Branch: `main`.
- HEAD and `origin/main` matched at `3d8c24f10e0cdbe30db2e0a8c7a96c601f95afa2` before this handoff-only edit.
- The shared Git index was empty. Worktree status captured for this refresh:
- ` M machine-builder-research/standards/STANDARDS_INDEX.md`
- ` M machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md`
- ` M machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`
- ` M machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`
- ` M machine-structure-editor/src/machine_builder/canvas_scene.py`
- ` M machine-structure-editor/src/machine_builder/canvas_ui.py`
- ` M machine-structure-editor/src/machine_builder/controller_board_fixtures.py`
- ` M machine-structure-editor/src/machine_builder/graphics/connection.py`
- ` M machine-structure-editor/src/machine_builder/graphics/node.py`
- ` M machine-structure-editor/tests/test_functional_interface_connection.py`
- `?? machine-structure-editor/tests/test_skr_mini_e3_exp1.py`
- `?? "machine-structure-editor/wiring test machines/Maestro and motor test.machine.json"`

**Board-owned proposed publication scope:**
- `machine-structure-editor/src/machine_builder/controller_board_fixtures.py` — the current diff appends a bounded SKR Mini E3 V3.0 EXP1 firmware-reference specimen. It retains all ten logical source positions and instantiates positions 1, 2, 3, 4, 8, 9, and 10. The fixture separates Klipper aliases, Marlin macro names/values, diagram roles, and conditional downstream assignments. It marks physical orientation, PCB pad/net crosswalk, cable cavity identity, continuity, active configuration, and as-built wiring as unverified.
- `machine-structure-editor/tests/test_skr_mini_e3_exp1.py` — the new paired regression test. Its content was inspected and the focused test was run for this refresh; the observed outcome is recorded below.
- `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md` — this existing handoff.

**Ownership boundaries:**
- Research-owned changes remain outside this Board commit: `machine-builder-research/standards/STANDARDS_INDEX.md` and `machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md`.
- Routing/visual integration changes remain outside this Board commit: `machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`, `machine-structure-editor/src/machine_builder/canvas_scene.py`, `machine-structure-editor/src/machine_builder/canvas_ui.py`, `machine-structure-editor/src/machine_builder/graphics/connection.py`, `machine-structure-editor/src/machine_builder/graphics/node.py`, and `machine-structure-editor/tests/test_functional_interface_connection.py`.
- `machine-structure-editor/wiring test machines/Maestro and motor test.machine.json` is untracked and is excluded from the Board commit pending explicit ownership confirmation. The name suggests visual integration test scaffolding, but the file content was not inspected in the supplied diff output.

**Implemented versus validated:**
- The SKR EXP1 fixture addition is present in the working tree; prior file history shows this path has been used for Board-specific fixtures, and the current delta itself is Board-reference modeling. The paired test's focused result for this refresh: PASS (pytest exit 0; 36 passed in 0.16s). This is focused coverage, not a full-suite result.
- The supplied inspection's `git diff --check HEAD` passed with line-ending warnings. The post-edit whitespace-check result is recorded in the console output for this refresh.
- The previous handoff's `30 passed` Board-fixture result and `843 passed` full-suite result predate this uncommitted addition; they do not validate the current SKR fixture. No full-suite run is claimed here.
- The existing X Motor and SKR EXP1 dispositions are preserved. This documentation refresh does not reclassify either disposition and does not assert that firmware-logical positions establish physical orientation or wiring.

- **SKR EXP1 source-integrity regression (reported validation):** added `test_checked_in_marlin_source_matches_pinned_sha256` for the repository-root-relative source `firmware_sources/marlin/src/pins/stm32g0/pins_BTT_SKR_MINI_E3_V3_0.h`. With `core.autocrlf=true`, the reported raw working-tree byte digest and CRLF-normalized UTF-8 digest both matched the recorded SHA-256 `C8650BB4F55558CBDD85CFEB79CB49006957860E9F2826DE3B23B15E64A002DE`; the LF-normalized digest differed. The regression explicitly normalizes to CRLF before hashing.
- **Focused validation reported from the local console:** from `machine-structure-editor`, `.venv\Scripts\python.exe -m pytest -q --tb=short tests/test_skr_mini_e3_exp1.py` returned **7 passed in 0.15s**, exit code 0; the enclosing PowerShell stopwatch measured 0.64 seconds. Tracked-path `git diff --check HEAD` passed with exit code 0; the separate untracked-test whitespace check also passed. Git emitted LF-to-CRLF advisories only.
- **Evidence boundary preserved:** the digest test establishes source-snapshot integrity only. It does not establish manufacturer diagram orientation, physical PCB pad/net identity, cable mating-face/cavity correspondence, continuity, or as-built harness wiring. The separate Octopus/TMC5160T contact-6 discrepancy remains unresolved.
**Publication state at pre-publication handoff edit (2026-10-17):** the three Board paths had not yet been staged, committed, or pushed when this entry was written. Planning has since authorized owner-scoped publication after Research completed. No Routing/visual paths or the untracked Maestro/motor test-machine JSON belong in this Board commit. Proposed subject: `Add SKR Mini E3 EXP1 firmware-reference fixture`.

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

`111` controller-owned physical SemanticPorts.

Current connector groups:

* `x-motor` — 4
* `y-motor` — 4
* `e0-motor` — 4
* `e1-motor` — 4
* `z-a-motor` — 4
* `z-b-motor` — 4
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

The current fixture exposure is:

* Bed heater: J4 pins 3 and 4 only.
* E0 heater: `e0-heat-screw` (J11) and `e0-heat-molex` (J16 alternate access; production population unverified).
* E1 heater: `e1-heat-screw` (J13) and `e1-heat-molex` (J17 alternate access; production population unverified).

J4 is the sole modeled physical bed-heater connector. Do not treat the J16/J17 Molex-compatible groups as confirmed physical Promega endpoints without evidence that those connectors are populated on the applicable board.

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

`https://raw.githubusercontent.com/Duet3D/Duet-2-Hardware/56958640c73c7febf3bce6e1eefbbdffd5a2db1b/Duet2/Duet2Maestro_v1.0/Headers.sch`

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

`https://raw.githubusercontent.com/Duet3D/Duet-2-Hardware/56958640c73c7febf3bce6e1eefbbdffd5a2db1b/Duet2/Duet2Maestro_v1.0/Headers.sch`

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

- [`Headers.sch`](https://github.com/Duet3D/Duet-2-Hardware/blob/56958640c73c7febf3bce6e1eefbbdffd5a2db1b/Duet2/Duet2Maestro_v1.0/Headers.sch) identifies J4 as a four-position high-current terminal and shows the connector labels.
- [`Htr_Fan.sch`](https://github.com/Duet3D/Duet-2-Hardware/blob/56958640c73c7febf3bce6e1eefbbdffd5a2db1b/Duet2/Duet2Maestro_v1.0/Htr_Fan.sch) shows the bed MOSFET control path and the `BED-` switched return.

Do not infer a verified J4 rating from the separate input-connector rating, generic screw-terminal statements, terminal-block family specifications, the MOSFET's individual datasheet, or heater-resistance calculations.

### Accepted physical-interface correction plan (historical plan; superseded by implementation)

J4 remains the only modeled physical bed-heater connector. The following records the accepted pre-implementation plan. The J4 correction was subsequently implemented in commit e85a1e38af74622de3a1b62cf1641af4b707fd26 ("Correct Maestro bed heater interface mapping"). This list is retained as historical context, not pending work:

- Remove the unsupported synthetic `bed-heat-molex` and `bed-heat-screw` groups.
- Preserve J4 pins 1–4 and the net labels `GND`, `V_IN`, `V_IN`, and `BED-`.
- Distinguish the board power-input purpose of pin 2 from the bed-supply purpose of pin 3 without inventing different electrical nets.
- Relate the existing `bed-heater` resource to J4 pins 3 and 4 only.
- Do not relate the bed-heater resource to J4 pins 1 or 2.
- Preserve the E0/E1 Molex and screw-terminal definitions, ratings, and relationships.
- Do not assign a numeric verified maximum current to J4's contacts or the complete bed-output path.

Keep the manufacturer-stated bed-heater capability, the machine-specific wiring, and the verified safe current limit for the complete circuit distinct. Evidence for one does not establish the others.

The previous J4 implementation description in §26 is retained as a record of the earlier represented state. This section records the accepted correction plan and its subsequent implementation. The corrected J4 mapping is implemented, but the verified safe current limit for the complete bed-output path remains unassigned.

### Historical authorization state (superseded by implementation)

At the time this section was written, Planning had accepted the correction plan, but implementation was not yet authorized. That authorization status was superseded by implementation commit e85a1e38af74622de3a1b62cf1641af4b707fd26 ("Correct Maestro bed heater interface mapping").

The J4 mapping correction is implemented. The verified safe current limit for the complete bed-output path remains unassigned. Preserve the thermal-testing qualification on the manufacturer-stated 18 A capability; the separate 25 A input-connector figure does not establish a safe J4 output rating.

## 34. Maestro V1.0 Controller-Side Endpoint Evidence for Promega Wiring

**Date:** October 10, 2026
**Classification:** Bounded, read-only board-side evidence investigation
**Status:** Endpoint identities substantially documented; machine-side harness mappings remain separate evidence work
**Implementation:** No source or fixture changes authorized or performed by this investigation.

### Scope and source authority

This report establishes the controller/board-side endpoints that can support the first actual Promega wiring graph. It does not infer machine-specific harness connections merely from the presence of a connector on the Duet 2 Maestro.

Primary Duet3D sources:

1. [Maestro V1.0 Headers.sch](https://raw.githubusercontent.com/Duet3D/Duet-2-Hardware/56958640c73c7febf3bce6e1eefbbdffd5a2db1b/Duet2/Duet2Maestro_v1.0/Headers.sch) — schematic sheet 4 of 7, dated 2017-12-05, revision 1.0. This is the primary source for connector reference designators, labels, contact counts, and electrical net identities.
2. [Maestro V1.0 Htr_Fan.sch](https://raw.githubusercontent.com/Duet3D/Duet-2-Hardware/56958640c73c7febf3bce6e1eefbbdffd5a2db1b/Duet2/Duet2Maestro_v1.0/Htr_Fan.sch) — schematic sheet 6 of 7, dated 2017-12-05, revision 1.0. This establishes the bed/E0/E1 heater control paths and FAN0/FAN1/FAN2 output circuits.
3. [Duet2Maestro_Wiring_V1.0_drawing_v1.3.svg](https://github.com/Duet3D/Duet-2-Hardware/blob/56958640c73c7febf3bce6e1eefbbdffd5a2db1b/Duet2/Duet2Maestro_v1.0/Duet2Maestro_Wiring_V1.0_drawing_v1.3.svg) — manufacturer wiring drawing for the Maestro V1.0 board, drawing revision v1.3. Use this for the physical wiring/contact-label convention, rather than reordering physical contacts solely from net names.
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

**Promega guide-view positions versus KiCad PCB pad numbers**

| Promega guide view position (left to right) | Function / documented lead | KiCad PCB pad number | PCB net | Promega use |
|---:|---|---:|---|---|
| 1 | Probe signal / S10 | 5 | `Z_PROBE_IN` | Connected |
| 2 | GND / P5 | 4 | `GND` | Connected |
| 3 | MOD | 3 | `Z_PROBE_MOD` | Left empty |
| 4 | +3.3 V / S9 | 2 | `+3.3V` | Connected |
| 5 | +5 V | 1 | `+5V` | Left empty |

The Promega wiring guide documents its connector-view positions from left to right: position 1 is the signal lead S10, position 2 is GND/P5, position 3 (MOD) is left empty, position 4 supplies 3.3 V/S9, and position 5 (+5 V) is left empty. The official revision-1.0 PCB layout independently numbers J28 pads in the opposite order: pad 1 is +5V, pad 2 is +3.3V, pad 3 is Z_PROBE_MOD, pad 4 is GND, and pad 5 is Z_PROBE_IN. These are two different numbering conventions for the same reference interface. Do not treat the Promega view-position number as a KiCad pad number. The current model's connector_position/pin-ID convention must be checked before altering the canonical port mapping. Installed board revision and physical harness remain unverified.

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

Controller-side connector/contact identity does not establish which harness is fitted to an installed Promega. The manufacturer's [Extruder Assembly Wiring guide](https://promega.printm3d.com/documentation/electronics/extruder-assembly-wiring) distinguishes the newer black ABS-R cable assembly from the older silver assembly and says the first 50 printers used the older assembly. Establish the applicable assembly version before applying side-specific harness mappings.

### Variant-qualified Promega extruder harness evidence

**Sources and revision qualifications**

* [Promega Extruder Assembly Wiring](https://promega.printm3d.com/documentation/electronics/extruder-assembly-wiring), New Extruder Assembly steps 7-16 and Old Extruder Assembly Wiring section. Retrieved 2026-10-11. The live page does not expose an immutable documentation revision.
* Black-assembly figures linked from the [Promega-Docs source Markdown](https://github.com/PrintM3D/Promega-Docs/blob/master/documentation/electronics/extruder-assembly-wiring.md): [S8 placement](https://raw.githubusercontent.com/PrintM3D/Promega-Docs/master/.gitbook/assets/new_extruder_wiring_s8.jpg), [S6 placement](https://raw.githubusercontent.com/PrintM3D/Promega-Docs/master/.gitbook/assets/new_extruder_wiring_s6.jpg), [H2/H4 placement](https://raw.githubusercontent.com/PrintM3D/Promega-Docs/master/.gitbook/assets/cnofx5dxdnpft6qv-heaterconnectorplacement.jpg), and [step 15 routing photo](https://raw.githubusercontent.com/PrintM3D/Promega-Docs/master/.gitbook/assets/610hfv9gt9oszycr-wheretorouteleftsidestuff.jpg). Inspected 2026-10-11; upstream `master` is mutable.
* [Promega Extruder install/uninstall](https://promega.printm3d.com/repair-and-maintenance/install-uninstall/extruder). Retrieved 2026-10-11; documents Compound and K'tana heater/PT1000 routing; mutable manufacturer page with no immutable revision identified.
* [Promega Duet Maestro Wiring](https://promega.printm3d.com/documentation/electronics/duet-maestro-wiring), including motor identification, probe, fan jumper and resistance guidance. Retrieved 2026-10-11; no immutable page revision exposed.
* [Duet2Maestro.kicad_pcb - official Duet3D Duet-2-Hardware repository](https://github.com/Duet3D/Duet-2-Hardware/blob/56958640c73c7febf3bce6e1eefbbdffd5a2db1b/Duet2/Duet2Maestro_v1.0/Duet2Maestro.kicad_pcb). The board-file title block identifies Duet 2 Maestro revision 1.0, dated 2018-02-20. Inspected 2026-10-11; the repository master branch is mutable.
* [Promega Tool Definitions](https://promega.printm3d.com/documentation/software-firmware/tool-definitions). Retrieved 2026-10-11; no immutable page revision exposed.
* [Promega SD Card Structure](https://promega.printm3d.com/documentation/software-firmware/sd-card-structure). Retrieved 2026-10-11; documents startup includes, machine configuration files, and homing macros; no immutable revision exposed.
* [Promega Adjust Homing Macros](https://promega.printm3d.com/documentation/software-firmware/adjust-homing-macros). Retrieved 2026-10-11; documents the published CoreXY homing behavior; no immutable revision exposed.
* [Promega Homing The Printer](https://promega.printm3d.com/beginners-setup-guides/homing-the-printer). Retrieved 2026-10-11; documents axis orientation and the published Home All motion sequence; no immutable revision exposed.
* [Promega Help! My Extruders Are Backwards](https://promega.printm3d.com/how-to-troubleshoot/common-troubleshooting/help-my-extruders-are-backwards). Retrieved 2026-10-11; the page reports last updated seven years ago and exposes no immutable revision.
* [PrintM3D Promega release v1.0.0](https://github.com/PrintM3D/Promega/releases/tag/v1.0.0), first SD-card release; commit `b89928cd3dda6e43c93919d120a18d41dd2f4187`.
* [Compound config.g at pinned v1.0.0 commit](https://github.com/PrintM3D/Promega/blob/b89928cd3dda6e43c93919d120a18d41dd2f4187/SD%20Card%20Structure/Compound/sys/config.g), historical release configuration for comparison only.
* [PrintM3D Promega release v1.0.1](https://github.com/PrintM3D/Promega/releases/tag/v1.0.1), source commit `5936e84b33ed3f9bf0183a960dc952513cac258b`, released 2018-07-09 and described as the new black cable-assembly SD-card structure. Its release notes direct older silver-assembly users to v1.0.0.
* [Compound config.g at the pinned release](https://github.com/PrintM3D/Promega/blob/5936e84b33ed3f9bf0183a960dc952513cac258b/SD%20Card%20Structure/Compound/sys/config.g), [Compound tool definitions](https://github.com/PrintM3D/Promega/blob/5936e84b33ed3f9bf0183a960dc952513cac258b/SD%20Card%20Structure/Compound/sys/machine_compound_tools.g), and [Compound Z-probe file](https://github.com/PrintM3D/Promega/blob/5936e84b33ed3f9bf0183a960dc952513cac258b/SD%20Card%20Structure/Compound/sys/machine_zprobe.g).
* [RepRapFirmware 3.x changelog](https://github.com/Duet3D/RepRapFirmware/wiki/Changelog-RRF-3.x), including the 3.5.3 and 3.5.4 notes. This is a mutable manufacturer wiki rather than an immutable file revision.

The Promega documentation pages are published manufacturer references but do not expose immutable page revisions in this audit. The PrintM3D firmware package is commit-pinned historical evidence. Neither source establishes the actual assembly fitted to the installed machine or proves its current SD-card configuration.

**Maestro V1.0 temperature connector physical-contact assignments**

The official revision-1.0 PCB layout source assigns the following physical pad numbers and nets:

| Board connector | Function | Pad 1 | Pad 2 |
|---|---|---|---|
| J5 | BED TEMP | `VSSA` | `THERMISTOR0` |
| J12 | E0 TEMP | `VSSA` | `THERMISTOR1` |
| J14 | E1 TEMP | `VSSA` | `THERMISTOR2` |
| J1 | C TEMP | `VSSA` | `THERMISTOR3` |

The PCB file represents J1 C TEMP as a two-position `PIN_ARRAY_2X1` footprint, with pad 1 connected to VSSA and pad 2 to THERMISTOR3. The same pad-number-to-net evidence is explicit for J5, J12 and J14.

This establishes reference-board contact labels and pad numbers for these four two-position temperature connectors. It is suitable evidence for assigning board-side `pin_label` values from physical connector positions 1 and 2. It does not establish which installed sensor or harness reaches each connector, whether the installed board is revision 1.0, or how the Promega black-assembly S8/S6 labels map to the left/right PT1000 cartridges. Keep those machine-side mappings unresolved.

**Variant-specific cable evidence**

| Machine-side cable/role | Older silver assembly | Newer black assembly | Board-side interpretation and remaining gap |
|---|---|---|---|
| P4/P2 extruder motors | The guide identifies both as extruder-motor connectors and shows their placement in the old assembly, but the available text does not state a universal label-to-side mapping. | Step 12 shows P4/P2 placement; steps 15-16 separately say to connect the right-side and left-side motor, heater and thermistor. The text does not explicitly map each P label to a side. | Board references are J10 / `e0-motor` and J6 / `e1-motor`. Do not equate harness label P4 with firmware drive P4. Confirm the new assembly mapping from a readable manufacturer figure or trace the applicable harness. |
| H2/H4 heater cartridges | Explicit old-assembly placement: H4 goes to the left heater position and H2 to the right, as identified in that guide's old-assembly section. | Steps 13-16 identify H2/H4 and the left/right connection procedure; the text does not explicitly pair each H label with a side. It warns that H4 must follow the red-line routing path to avoid print interference. | Board references are J11 / `e0-heat-screw` and J13 / `e1-heat-screw`. Do not transfer the old assembly's side mapping to the new assembly without confirming its figure or tracing the harness. J16/J17 remain unverified alternate populated endpoints. |
| S8/S6 PT1000 sensors | Explicit old-assembly placement: S8 goes left and S6 goes right. | Steps 10-11 show where to route S8/S6 but explicitly warn that the pictured wire colors are wrong and say to follow the labels. Steps 15-16 then discuss the right-side and left-side connections without textually pairing each S label to a side. | Board references are J12 / `e0-temp` and J14 / `e1-temp`. The new assembly's side mapping remains unresolved; do not infer it from color. |
| P9/P11 fans | The old-assembly guide explicitly says there is no universal rule determining which is the nozzle fan and which is the cold-section fan. It recommends testing or tracing them. | Step 7 says the nozzle fan is P9 or P11 depending on the printer and recommends continuity testing or tracing wires to the Duet board. Color examples are only aids because multiple wires share colors. | The documented reference setup uses controlled FAN2/J2 (`fan2`) for the 5 V nozzle fan and the distinct Always-On connector J24 (`always-on-fan`) for the 24 V cold-section fan. Identify each actual termination before authoring a definite edge or applying voltage. |
| X/Y/Z motors | Maestro Wiring guide: the X cable is an otherwise-unlabelled four-pin connection with red, green, blue and black wires; the Z cable is described as coiled/rope-like and the Y cable as not coiled. | Same published identification guidance; it is not a wire-to-coil pinout. | Board references J9 / `x-motor`, J8 / `y-motor`, and J36/J7 / `z-a-motor` / `z-b-motor`. The installed cable-to-board termination and coil-contact order still require evidence. |

The extruder replacement guide warns that the side where a cable emerges or wraps around the assembly is not necessarily the side where its plug terminates. Image-level audit of the newer black cable assembly figures: the repository's linked `new_extruder_wiring_s8.jpg` and `new_extruder_wiring_s6.jpg` images show labelled connector positions and routing arrows, but do not trace either lead end-to-end to a named left/right PT1000 cartridge. The `cnofx5dxdnpft6qv-heaterconnectorplacement.jpg` image marks the H2 and H4 holder positions and H4's routing path, but does not identify each heater cartridge endpoint. The step 15 text instructs connection of the right-side heater, thermistor and stepper motor, while the linked photograph filename is `wheretorouteleftsidestuff.jpg`; that filename conflicts with the step text and must not be used to infer a wiring assignment. The images therefore do not resolve the newer assembly's H2/H4 or S8/S6 label-to-component-side mapping. The separate manufacturer [Extruder install/uninstall guide](https://promega.printm3d.com/repair-and-maintenance/install-uninstall/extruder) independently specifies that Compound nozzle heater/PT1000 wires wrap around the right side of the extruder but plug into the left side of the cable assembly. For K'tana, right-side heater/PT1000 wires plug into the left cable-assembly side, while left-side wires plug into the right. This confirms a routing crossover in the instructions; it does not explicitly resolve the newer black assembly's H2/H4 or S8/S6 label-to-component-side mapping. Keep those mappings unresolved until the figures can be interpreted unambiguously or the applicable harness is physically traced. It also describes routing exceptions for Compound versus K'Tana arrangements. Do not infer the motor, heater or sensor's logical left/right identity solely from the cable's exit direction or holder slot.

**Historical logical firmware assignments: not as-built proof**

Comparison of the commit-pinned v1.0.0 and v1.0.1 SD-card releases:

- Release v1.0.0 (commit `b89928cd3dda6e43c93919d120a18d41dd2f4187`) is identified by its release page as the first Promega SD-card release. Its Compound `config.g` has inline definitions `M563 P1 D0 ... S"Mixing as Single Right"` and `M563 P2 D1 ... S"Mixing as Single Left"`, while its `M569` comments label physical drive P3 as the left extruder and P4 as the right extruder.
- Release v1.0.1 (commit `5936e84b33ed3f9bf0183a960dc952513cac258b`) is explicitly for the new black extruder cable assembly; its release notes direct older silver-assembly users to v1.0.0. Its `config.g` delegates Compound tool definitions to `machine_compound_tools.g`, where P1/D0 is named Single Left and P2/D1 Single Right, with comments matching those logical names.
- This is a version-specific change in historical logical tool naming/drive assignments. It must not be flattened into one universal mapping or used to infer the active firmware setup of an installed printer. The installed SD-card configuration and actual harness remain unverified.
- Neither pinned configuration establishes how the newer black assembly's cable labels H2/H4 or S8/S6 map to the left/right heater or PT1000 cartridges. Cable labels are not firmware heater numbers; retain the unresolved mapping until the applicable harness is physically traced or a clear manufacturer source resolves it.

The pinned 2018 Compound `config.g` labels P0/P1 as the CoreXY drives, P2 as Z, P3 as left extruder and P4 as right extruder. It uses `M667 S1` for CoreXY, old `M305` temperature definitions (P0 bed, P1 left PT1000, P2 right PT1000), old `M574` endstop syntax, and `M106` fan channels P0-P2. These are logical firmware channel numbers, not machine-side cable labels P2/P4, S8/S6 or P9/P11.

The separate Compound tool definitions use H2 for the Compound mixing tool and its associated tool definitions. Promega's Tool Definitions page describes the ordinary K'Tana two-tool arrangement with bed H0, left heater H1 and right heater H2, and describes Compound as a special configuration. Heater cable label H2 must not be equated with logical heater H2 as a universal physical mapping.

The current manufacturer Tool Definitions page contains contradictory left/right statements for Compound T1 and T2: T1 is labeled Single Left and assigned Extruder 0 (Left), but its prose says it extrudes with only the right extruder; T2 is labeled Single Right and assigned Extruder 1 (Right), but its prose says it extrudes with only the left. The commit-pinned historical v1.0.1 `machine_compound_tools.g` clarifies the intent in that release: `M563 P1 D0 ... S"Mixing as Single Left"` is commented as using the left extruder motor, and `M563 P2 D1 ... S"Mixing as Single Right"` is commented as using the right extruder motor. The page prose therefore appears reversed relative to the pinned historical configuration and its tool/drive assignments. Promega's Help! My Extruders Are Backwards troubleshooting guide independently states that drive 0 should move the left extruder and drive 1 the right, and repeats the M563 P1 D0 / M563 P2 D1 assignments. This corroborates the intended logical mapping in those sources but does not prove which drive the installed physical harness actually moves; physical wiring or the applicable as-built configuration must still be verified. Treat this as historical logical configuration evidence only; the actual installed `machine_compound_tools.g` and physical harness terminations still need verification before confirming the as-built left/right mapping.

The public 2018 PrintM3D release is not a verified active RepRapFirmware 3.5.4 configuration. The RRF 3.x changelog says `M667` is no longer supported from RRF 3.5.3 and `M669 K1` selects CoreXY; its 3.5.3 notes also document removal of the `I` parameter from `M558`. RRF3 sensor setup uses `M308`, and heater/fan setup commonly uses `M950`. The project context reports RRF 3.5.4 / ConfigTool 3.5.12 as the target baseline. The installed SD-card files were not retrieved directly in this public-source research pass; live-controller runtime output is separate evidence and does not identify the exact source file for each setting.

A reliable active-configuration audit requires the applicable installed `sys/config.g` and the files it calls through `M98`. Promega's SD Card Structure guide identifies separate machine files including `machine_axisdimensions.g`, `machine_axissteps.g`, `machine_maxtemp.g`, `machine_zendstop.g`, and `machine_zprobe.g`, as well as the `homex.g`, `homey.g`, `homez.g`, and `homeall.g` homing macros. Inspect the actual include targets and any nested includes; do not assume `config.g` alone defines the active assignments. Check motor and axis mapping (`M584`, `M569`, `M92`, `M350`, `M208`, `M669`), sensors/heaters/fans (`M308`, `M950`, `M558`, `G31`, `M307`, `M106`), endstops (`M574`), and tool definitions (`M563`, `M568`, `M567`). Include any files under `macros` that are actually called. Do not describe historical assignments as active machine facts without reading those files.

The Promega Adjust Homing Macros guide states that `homex.g` and `homey.g` are both CoreXY homing files and each homes both X and Y. Do not infer active physical endstop-input assignments from whether Home X or Home Y was selected; inspect the installed homing macros and `M574` configuration. This is published manufacturer guidance, not confirmation of the installed printer's current configuration.

The Promega Homing The Printer guide states that X spans left-to-right across the front, Y spans front-to-back, positive Z points down, and the machine origin is top-front-left. Its published Home All sequence sends the CoreXY gantry to the rear Y-limit switch first, then to the X-limit switch, and then moves the bed to its Z limit. This establishes the documented functional reference sequence only; it does not establish which installed harness conductors reach the switches or which physical input channels the active configuration uses. Confirm the installed homing macros and `M574` settings before assigning those machine-side connections.

Manufacturer-reference mapping: X-labeled limit-switch harness to Maestro J33 / X STOP; Y-labeled limit-switch harness to Maestro J32 / Y STOP.

The Promega Duet Maestro Wiring guide states that its main diagram text boxes reproduce labels printed near cable connectors and that blue identifies the limit-switch cable group. Inspection of the readable [main connection diagram](https://raw.githubusercontent.com/PrintM3D/Promega-Docs/master/.gitbook/assets/eegr4vx3jeacoiyn-guideswiringdiagram.png) shows the X and Y label callouts at their corresponding endstop connector locations. This supports the intended manufacturer-reference mapping. The [detailed Maestro diagram](https://raw.githubusercontent.com/PrintM3D/Promega-Docs/master/.gitbook/assets/detailed-maestro-wiring-guide.PNG) and [wiring-assemblies photograph](https://raw.githubusercontent.com/PrintM3D/Promega-Docs/master/.gitbook/assets/75w5fdmofqhmwc8n-promegawiringassemblies.jpg) did not independently provide a readable, continuous trace of each machine-side harness; no contradictory mapping was found. The [Homing The Printer guide](https://promega.printm3d.com/beginners-setup-guides/homing-the-printer) corroborates functional axis identity by describing the rear Y-limit switch before the X-limit switch during homing.

Evidence status: strong for the manufacturer's intended reference mapping; not verified for the installed printer. The installed harness and active `M574`/homing configuration have not been inspected. These labels do not establish conductor-to-contact pin order. If the labels are absent or ambiguous, power the printer off and trace each physical harness to its board connector; verify the active configuration before treating the as-built endpoints as established.

### Published electrical reference values and inspection safety

The Promega Duet Maestro Wiring guide publishes the following expected component resistances:

| Component | Manufacturer reference |
|---|---:|
| Extruder PT1000 sensor | 1,090 ohms |
| Extruder heater | 13.1 ohms |
| Heated bed | 2.2 ohms |
| Bed thermistor | 106,800 ohms |
| Extruder stepper motor | 19.3 ohms |
| Axis stepper motor | 9.0 ohms |

The manufacturer states that thermistor values vary with temperature; its listed sensor values were measured around 24 C. Treat the table as diagnostic reference information, not as a guaranteed pass/fail tolerance for an unidentified component or harness.

The same guide warns of board damage from shorts, electrostatic discharge, voltage generated by manually moving motors, connecting or disconnecting components while powered, and touching electrical components while powered. It recommends switching off the Duet board before resistance measurements. Record actual measurement conditions and confirm the component and endpoints being measured. Do not perform powered continuity or resistance checks.
### X/Y motor board-plug reference slice - locally validated, uncommitted

The shared working tree now implements the reference-only X/Y motor cable board-plug mating slice. Four cable-plug contact positions per axis mate by corresponding connector position to Maestro J9 / X MOT and J8 / Y MOT. The current model and focused test explicitly preserve the distinction between connector mating and internal cable or motor wiring.

Established by the current implementation and validation:
- Eight electrical reference connections are created, four for X and four for Y.
- The contact labels and mating positions are represented with connection metadata and provenance.
- Focused validation: 14 passed in 5.46 seconds for `test_promega_xy_motor_reference.py`, `test_promega_ir_probe_connections.py`, and `test_connection_authoring.py`.
- Full project validation: 841 passed in 8.22 seconds.
- `git diff --check`: passed.

These test results validate the current reference-model implementation, not the user's installed machine. Wire-colour-to-contact mapping, motor-coil terminal mapping, physical as-built wiring, and firmware drive assignment remain unestablished. Do not add direct cable-to-motor-coil connections or assert as-built drive assignments without additional evidence.

The implementation and this handoff update remain uncommitted. Preserve concurrent work from other workstreams and do not stage unrelated files.

### Manufacturer diagram: physical endstop contact-role order

The official [Duet 2 Maestro V1.0 wiring diagram](https://docs.duet3d.com/duet_boards/duet_2_wifi_ethernet_maestro/duet_2_maestro_v1.0_wiring.png) depicts the three contact roles on J19 Z STOP, J32 Y STOP, J33 X STOP, J34 E0 STOP, and J35 E1 STOP. In the diagram's displayed connector orientation, the contact-role order is axis-specific STOP signal, GND, then +3.3 V. This adds board-side physical-position evidence beyond the connector-level contact inventory.

**KiCad-confirmed numbered-pad mapping**

The official [Duet2Maestro.kicad_pcb source](https://github.com/Duet3D/Duet-2-Hardware/blob/56958640c73c7febf3bce6e1eefbbdffd5a2db1b/Duet2/Duet2Maestro_v1.0/Duet2Maestro.kicad_pcb), titled Duet 2 Maestro revision 1.0 and dated 2018-02-20, explicitly binds these connector pad numbers to their nets:

| Connector | Pad 1 | Pad 2 | Pad 3 |
|---|---|---|---|
| J19 / Z STOP | `GND` | `+3.3V` | `Z_STOP_CONN` |
| J32 / Y STOP | `GND` | `+3.3V` | `Y_STOP_CONN` |
| J33 / X STOP | `GND` | `+3.3V` | `X_STOP_CONN` |
| J34 / E0 STOP | `GND` | `+3.3V` | `E0_STOP_CONN` |
| J35 / E1 STOP | `GND` | `+3.3V` | `E1_STOP_CONN` |

This PCB source resolves the reference-board numbered-pad mapping. It supersedes the preceding uncertainty about whether numbered pad assignments could be inferred from the diagram's displayed orientation. Preserve the distinction between PCB net names (for example, `X_STOP_CONN`) and fixture-level functional aliases (for example, `xstop`).

This is a revision-1.0 design reference, not verification of the installed controller revision, switch harness, or active `M574`/homing configuration. The repository `master` source link is mutable; the PCB title block identifies the referenced design revision.

### KiCad-confirmed extruder heater connector pads and shared nets

The official Duet 2 Maestro revision 1.0 PCB layout source explicitly defines the following heater connector pad/net assignments:

| Connector | Board label | Pad 1 | Pad 2 | Connector type in PCB source |
|---|---|---|---|---|
| J11 | E0 HEAT | `V_IN` | `E0-` | 3.5 mm screw-terminal footprint |
| J16 | E0 HEAT | `V_IN` | `E0-` | 2-position pin-header footprint |
| J13 | E1 HEAT | `V_IN` | `E1-` | 3.5 mm screw-terminal footprint |
| J17 | E1 HEAT | `V_IN` | `E1-` | 2-position pin-header footprint |

The CAD layout therefore establishes that J11 and J16 are assigned to the same two electrical nets for E0, and J13 and J17 to the same two electrical nets for E1. The alternate connector footprint is not a separate heater resource or a different switched output in this design; it is drawn on the same net pair as its corresponding screw-terminal.

**Population and installation boundary:** Presence of a footprint in the revision-1.0 PCB file does not prove that the connector is populated on every manufactured board. Keep J11/J13 as the documented screw-terminal reference endpoints. Keep J16/J17 as design-defined alternate endpoints whose physical population on the applicable board remains unverified. Do not create a confirmed machine-side connection to J16/J17 without evidence for the actual board, and do not infer H2/H4 cable-label-to-heater-side mapping from the PCB nets.

Source: [Official Duet2Maestro.kicad_pcb, Duet-2-Hardware repository](https://github.com/Duet3D/Duet-2-Hardware/blob/56958640c73c7febf3bce6e1eefbbdffd5a2db1b/Duet2/Duet2Maestro_v1.0/Duet2Maestro.kicad_pcb), revision 1.0 design dated 2018-02-20. Repository `master` is mutable.

### KiCad-confirmed fan contacts and selectable supply banks

The official Duet 2 Maestro revision 1.0 PCB source assigns these numbered pad nets:

| Connector | Pad 1 | Pad 2 | Reference function |
|---|---|---|---|
| J24 | `V_FAN_A` | `GND` | Separate always-on fan supply |
| J25 | `V_FAN_A` | `FAN0-` | Controlled FAN0 connector |
| J29 | `V_FAN_A` | `FAN1-` | Controlled FAN1 connector |
| J2 | `V_FAN_B` | `FAN2-` | Controlled FAN2 connector |

The supply selectors are:

| Selector | Pad 1 | Pad 2 | Pad 3 |
|---|---|---|---|
| J3 | `+5V` | `V_FAN_A` | `V_IN` |
| J23 | `+5V` | `V_FAN_B` | `V_IN` |

The official `Headers.sch` identifies J24 as "Always on FAN 0". J25, J29 and J2 are the separate FAN0, FAN1 and FAN2 connectors. `Htr_Fan.sch` shows the controlled FAN0, FAN1 and FAN2 MOSFET paths. Therefore, do not conflate always-on J24 with controlled FAN0 at J25.

**J24 label/net qualification:** The footprint value text reads `GND V_IN`, but the PCB assigns pad 1 to `V_FAN_A`. Preserve the explicit pad/net mapping. J3 selects `V_FAN_A` between `+5V` and `V_IN`; J23 selects `V_FAN_B` between `+5V` and `V_IN`. Do not assume J24 is always at `V_IN` or 24 V without confirming the selector configuration.

These are reference-board assignments for the revision 1.0 design. They do not verify the installed board revision, selector positions, actual connector voltages, fan wiring, or firmware channel configuration. Keep connector identity, physical pad, selectable supply bank, controlled output, and installed fan termination as separate facts.

### Historical motor numeric pad/net mapping audit (bounded crosswalk subsequently implemented)

An independent reading of the official Duet 2 Maestro V1.0 PCB layout identifies these numbered pad/net mappings for the four standard motor connectors:

| Connector | Pad 1 | Pad 2 | Pad 3 | Pad 4 |
|---|---|---|---|---|
| J9 / X MOT | `X_MOT_A1` | `X_MOT_A2` | `X_MOT_B1` | `X_MOT_B2` |
| J8 / Y MOT | `Y_MOT_A1` | `Y_MOT_A2` | `Y_MOT_B1` | `Y_MOT_B2` |
| J10 / E0 MOT | `E0_MOT_A1` | `E0_MOT_A2` | `E0_MOT_B1` | `E0_MOT_B2` |
| J6 / E1 MOT | `E1_MOT_A1` | `E1_MOT_A2` | `E1_MOT_B1` | `E1_MOT_B2` |

The board source gives a different, non-simple shared-net pattern on the dual-Z connectors:

| Connector | Pad 1 | Pad 2 | Pad 3 | Pad 4 |
|---|---|---|---|---|
| J36 / Z A | `Z_MOT_A1` | `Net-(J36-Pad2)` | `Z_MOT_B1` | `Net-(J36-Pad4)` |
| J7 / Z B | `Net-(J36-Pad2)` | `Z_MOT_A2` | `Net-(J36-Pad4)` | `Z_MOT_B2` |

**Historical finding (before the bounded PCB crosswalk was implemented):** Section 34 records the functional motor labels in the order `B1`, `B2`, `A1`, `A2`, while the official PCB numbers J9/J8/J10/J6 pads in `A1`, `A2`, `B1`, `B2` order. The bounded crosswalk now explicitly records the corresponding PCB pad numbers and net names for J9/J8/J36/J7/J10/J6 while preserving the existing functional labels and internal port IDs. The regression test checks fixed expected values reviewed against the pinned PCB source; it does not parse the external PCB file. At the time of that historical finding, E0/E1 motor connectors J10/J6 were outside the reviewed inventory; the J10/J6 crosswalk added below supersedes that scope boundary.

For the bounded motor inventory, preserve the distinction between legacy numeric contact identity, functional `pin_label`, and explicit `pcb_pad_number`/`pcb_net_name` metadata. J9/J8, J10/J6, and the separate dual-Z J36/J7 shared-net pattern are represented explicitly in the reviewed crosswalk. This reference crosswalk does not establish cable mating-face orientation, cavity numbering, internal conductor order, coil pairing, firmware assignment, or installed wiring.

Source: [Official Duet2Maestro.kicad_pcb, Duet-2-Hardware repository](https://github.com/Duet3D/Duet-2-Hardware/blob/56958640c73c7febf3bce6e1eefbbdffd5a2db1b/Duet2/Duet2Maestro_v1.0/Duet2Maestro.kicad_pcb). The PCB title block identifies revision 1.0, dated 2018-02-20; the board source is pinned to commit `56958640c73c7febf3bce6e1eefbbdffd5a2db1b`.

This is a board-source consistency finding, not a claim about installed motor wiring or coil order. Do not infer wire colors, coil terminals, firmware assignments, or motor direction from this table alone.

### PCB footprint orientation versus numbered-pad identity

Pinned-source checkpoint: the referenced Duet 2 Maestro V1.0 PCB and schematic files in this handoff use immutable repository commit `56958640c73c7febf3bce6e1eefbbdffd5a2db1b`. The PCB title block identifies design revision 1.0 dated 2018-02-20. This provides a repeatable source snapshot for pad/net assignments, footprint rotations, and the related schematic sheets; it does not establish the installed controller revision.

The official [Duet2Maestro.kicad_pcb source](https://github.com/Duet3D/Duet-2-Hardware/blob/56958640c73c7febf3bce6e1eefbbdffd5a2db1b/Duet2/Duet2Maestro_v1.0/Duet2Maestro.kicad_pcb), revision 1.0, places connector footprints at different rotations. Their numbered pad identity is therefore not interchangeable with left-to-right or top-to-bottom order in a viewer. The following orientation summary is derived from the footprint rotation, local pad coordinates, and pad/net assignments in that PCB file. "Top/bottom/left/right" means the PCB front-side board-coordinate view, not the mating-face view of an unplugged cable.

| Connector group | Footprint rotation | Pad layout in PCB front-side coordinates |
|---|---:|---|
| J9 / J8 / J10 / J6 motor headers | 270 degrees | Pads 1 through 4 run bottom to top. For the single-axis X/Y/E0/E1 connectors: bottom-to-top pads 1-4 are A1, A2, B1, B2; top-to-bottom are B2, B1, A2, A1. |
| J36 / J7 dual-Z motor headers | 270 degrees | Pads 1 through 4 run bottom to top, but use the documented shared-net pattern in the motor pad table above; do not substitute the simple X/Y/E0/E1 sequence. |
| J19 / J32 / J33 / J34 / J35 endstops | 270 degrees | Pad 1 at bottom (GND), pad 2 middle (+3.3V), pad 3 top (axis-specific STOP net). |
| J24 / J25 / J29 / J2 fan connectors | 270 degrees | Pad 1 at bottom (V_FAN_A or V_FAN_B), pad 2 top (GND on J24, controlled FANx- on J25/J29/J2). |
| J11 / J13 screw heater connectors | 90 degrees | Pad 1 above pad 2: V_IN above the corresponding switched E0- or E1- net. |
| J16 / J17 alternate heater headers | 90 degrees | Pad 1 above pad 2: V_IN above the corresponding switched E0- or E1- net. Physical population remains unverified. |
| J3 / J23 fan supply selectors | 180 degrees | Pad 1 right (+5V), pad 2 centre (V_FAN_A or V_FAN_B), pad 3 left (V_IN). |
| J5 bed temperature | 180 degrees | Pad 1 right (VSSA), pad 2 left (THERMISTOR0). |
| J1 / J12 / J14 temperature connectors | 270 degrees | Pad 1 bottom (VSSA), pad 2 top (THERMISTOR3, THERMISTOR1, and THERMISTOR2 respectively). |
| J28 probe | 270 degrees | Pads 1 through 5 run bottom to top: +5V, +3.3V, Z_PROBE_MOD, GND, Z_PROBE_IN. This is the reverse order of the Promega guide's left-to-right view positions. |

**Canonical-model rule to audit:** A controller port ID ending in `pin-N` should be interpreted as numbered PCB pad N only if that is the declared convention for the controller definition. A connector-view position and a cable-side cavity position are separate identities. Never infer either of them from board-view top/bottom/left/right ordering alone.

For any reference wiring edge, preserve the basis used to connect the endpoints: exact PCB pad number/net, a documented connector-view position, or a documented cable cavity identity. When the mating orientation or view convention is not established, keep the mapping unresolved instead of relying on array order.

This orientation audit describes the revision-1.0 reference PCB design. It does not verify the installed controller revision, cable orientation, harness population, internal conductor order, or firmware configuration.

### J37 TEMP_DB numbered pad/net crosswalk

The official Duet 2 Maestro V1.0 PCB source defines J37 as footprint `MAX_TEMP_DB`, a two-row, five-contact header. The footprint is placed at PCB coordinates X = 162.875 mm, Y = 95.55848 mm, with a 90-degree footprint rotation. These are KiCad board coordinates and placement metadata, not a connector mating-face view.

| J37 PCB pad number | Net assigned in the revision-1.0 PCB source |
|---:|---|
| 1 | `SPI0_CS2` |
| 2 | `GND` |
| 3 | `SPI0_CS1` |
| 4 | `SPI0_SCK` |
| 5 | `SPI0_MOSI` |
| 6 | `SPI0_MISO` |
| 7 | `TWCK0` |
| 8 | `+3.3V` |
| 9 | `TWD0` |
| 10 | No net assigned in the PCB file |

This is a direct numbered-pad/net crosswalk from the PCB source. J37's listed nets are a digital/interface and power set; they are not a fifth direct `THERMISTORx` input. Preserve J37 as the TEMP_DB interface rather than inventing a direct analog temperature channel. Keep the literal net names as source labels unless another authoritative source establishes their intended functional descriptions.

The source also contains the footprint user text `<10mm max height` (hidden in the saved PCB view); retain that as board-design documentation if physical clearance becomes relevant. Do not interpret it as verification of a daughterboard's presence or height on the installed machine.

This establishes the revision-1.0 board design only. It does not establish whether a temperature daughterboard is fitted to the user's machine, what daughterboard is compatible, or how an external sensor is routed through it.

Source: [Official Duet2Maestro.kicad_pcb, Duet-2-Hardware repository](https://github.com/Duet3D/Duet-2-Hardware/blob/56958640c73c7febf3bce6e1eefbbdffd5a2db1b/Duet2/Duet2Maestro_v1.0/Duet2Maestro.kicad_pcb), PCB title block revision 1.0 dated 2018-02-20. The repository `master` URL is mutable.

### Source-to-model identity audit: PCB pad versus canonical port position

**Audit received from #4:** Read-only source-to-model consistency audit at baseline `f959e14601ada7d0f024ece8a15677c3b3ddd229` (`Standardize cross-workstream reporting format`). The audit ran no tests; `git diff --check` passed.

The inspected code in `src/machine_builder/controller_board_fixtures.py`, `hardware_catalog.py`, and `promega_fixtures.py` does not establish a consistent identity contract between the canonical controller port's numeric suffix, `pin_id`, functional `pin_label`, KiCad PCB pad number, and a connector-view/cable-cavity position. The inspected port initialization uses IDs of the form `pin-{position}` and `pin_id=str(position)` with connector-specific functional-label sequences; no explicit `connector_position` property was found in that initialization. `_contact_position()` falls back to numeric `pin_id` or port-ID suffix.

Consequently, passing positional-connection tests does not by itself prove that canonical port number N means KiCad PCB pad N or cable cavity N. The earlier PCB footprint-orientation summary describes the reference PCB view; it must not be read as proof that existing canonical port labels or a cable-side view use the same sequence.

**Source-to-model discrepancies identified by #4**

| Connector group | Existing canonical fixture order described by #4 | Official revision-1.0 PCB pad/net order | Required treatment |
|---|---|---|---|
| J9/J8/J10/J6 motors | `B1`, `B2`, `A1`, `A2` by numeric position | Pads 1–4: `A1`, `A2`, `B1`, `B2` | Do not interpret the canonical numeric suffix as a PCB pad number until reconciled. |
| J32/J33 and other three-contact endstops | Signal alias first, +3.3 V second, GND third | Pad 1 GND, pad 2 +3.3 V, pad 3 axis-specific STOP net | Represent explicit PCB pad/net identities; retain functional aliases separately. |
| J28 probe | Numeric positions reflect Promega guide-view order: signal, GND, MOD, +3.3 V, +5 V | PCB pads 1–5: +5 V, +3.3 V, MOD, GND, signal | Preserve the guide-view-to-PCB-pad crosswalk; do not change the working IR-probe functional mapping in isolation. |
| XY reference helper | Directly mates cable positions 1–4 to board positions 1–4 | Board pad numbering has a different sequence from the existing B1/B2/A1/A2 labels | Positional tests do not establish the cable mating-face orientation or cavity-to-pad correspondence. |

The dual-Z connectors J36/J7 have a separate shared-net pattern documented above; do not apply the ordinary four-pad motor sequence to them.

**Identity contract to resolve before further fixture expansion**

Evaluate an explicit distinction between:
- stable internal port identity (`id` / `pin_id`), which must not silently imply a different physical coordinate system;
- KiCad PCB pad number and exact PCB net name;
- PCB front-side spatial position or footprint orientation when relevant;
- manufacturer diagram connector-view position; and
- cable mating-face/cavity position.

Candidate metadata such as `pcb_pad_number` and `pcb_net_name` could preserve PCB identity, with separately named view/cavity fields where supported. This is a proposal for the identity-contract review, not an adopted schema or authorization to edit production fixtures.

**Implementation gate:** Before expanding the motor/endstop helpers or changing J28 mappings, reconcile the controller fixture and hardware catalog against the official [Duet2Maestro.kicad_pcb, revision-1.0 design](https://github.com/Duet3D/Duet-2-Hardware/blob/56958640c73c7febf3bce6e1eefbbdffd5a2db1b/Duet2/Duet2Maestro_v1.0/Duet2Maestro.kicad_pcb). Add focused source-to-model assertions for motor, endstop, and J28 pad/net identities only after the convention is explicit. Then run the affected tests and full suite.

Do not infer motor coil pairings, wire colours, cable cavity numbering, active firmware assignments, or installed wiring from the current labels alone. Preserve the established IR-probe functional connections and keep the installed board revision/harness unverified until direct evidence is available.

### Proposed controller-port identity contract for #4 agreement

**Status: proposal for cross-workstream agreement; not yet an adopted implementation contract.** This proposal responds to the read-only source-to-model audit from #4 at baseline `f959e14601ada7d0f024ece8a15677c3b3ddd229`. No production implementation is authorized by recording this proposal.

The current `SemanticPort` model exposes `id`, `connector_id`, `pin_id`, `properties`, and provenance, but no dedicated PCB pad-number or PCB net-name field. The controller fixture derives its `pin_id` and `pin-{position}` ID suffix from a loop position, then assigns `pin_label` through connector-specific sequences. `connector_position_count` records the number of contacts, not an individual contact's position. The Promega `_contact_position()` helper may fall back to `pin_id` or the numeric ID suffix. These values do not, by themselves, establish a shared coordinate system.

**Proposed identity meanings**

| Field/concept | Proposed contract |
|---|---|
| `id` | Stable internal semantic identity. Preserve current IDs for compatibility. The numeric suffix is not sufficient evidence of a physical coordinate. |
| `pin_id` | Existing identifier used by current code and consumers. Do not universally interpret it as a KiCad pad number unless explicitly established for that connector definition. |
| `pin_label` | Existing functional/readable contact label, such as `B1`, `xstop`, or `Z_PROBE_IN`. It is not necessarily equal to the PCB net name. |
| `pcb_reference_designator` | Exact physical board reference, such as `J9`, `J33`, or `J28`. This is distinct from the canonical `connector_id`. |
| `pcb_pad_number` | One-based numbered pad explicitly established by the applicable PCB source. Store as a number, not an inferred position. |
| `pcb_net_name` | Exact source net name, for example `X_MOT_B1` or `X_STOP_CONN`. For a pad without a net, represent that separately from unknown, e.g. `pcb_net_status: unassigned_in_reference_pcb`. |
| `pcb_front_view_location` | Optional position in an explicitly identified PCB front-side view, derived from the footprint geometry/rotation. It is not a pad number and not a cable mating-face position. |
| `promega_diagram_view_position` | Position in a specifically named Promega diagram view, stored with a source/view identifier. Do not treat it as a PCB pad number. |
| `cable_cavity_position` | Cable-side cavity position only when the applicable cable mating-face view and numbering are supported by evidence. Do not infer it from `pin_id`, board orientation, or equal numeric ordinals. |

For the initial compatible implementation, use the existing `SemanticPort.properties` dictionary to carry `pcb_reference_designator`, `pcb_pad_number`, and `pcb_net_name` for every contact whose identity is established by the reference PCB. Include provenance for the source. This proposal does not require changing the `SemanticPort` dataclass or persistence schema; first-class typed fields, if later desired, require separate review.

Do not give `connector_position` a universal meaning. Where it remains for compatibility, its coordinate basis must be explicit. Connector view positions and cable cavity positions require a named view and source. Connection metadata should identify the mapping basis used to relate endpoint coordinate systems. If that relationship is not established, keep the corresponding mating mapping unresolved.

**Representative mappings that require source-to-model assertions**

- J9 / X MOT: PCB pads 1–4 are `X_MOT_A1`, `X_MOT_A2`, `X_MOT_B1`, `X_MOT_B2`. If the existing functional `pin_label` sequence is retained as `B1`, `B2`, `A1`, `A2`, its explicit PCB pad numbers would correspond to 3, 4, 1, 2 respectively. This source crosswalk must be checked against the canonical fixture before changing it.
- J33 / X STOP: PCB pad 1 is GND, pad 2 is +3.3 V, pad 3 is `X_STOP_CONN`. The current fixture assigns its internal sequence as signal, +3.3 V, GND; retain the labels/IDs only as legacy identifiers while adding explicit PCB identities.
- J28 / probe: the Promega guide-view positions map to PCB pads in reverse order: guide position 1 signal maps to pad 5 `Z_PROBE_IN`; position 2 GND maps to pad 4; position 3 MOD maps to pad 3; position 4 +3.3 V maps to pad 2; position 5 +5 V maps to pad 1. Keep the documented functional probe wiring unchanged until the board-port lookup and identity contract are reconciled together.

**Validation gate before extending positional connections**

1. Agree the field meanings and compatibility approach with #4 before production fixture edits.
2. Populate PCB source identities from the pinned revision-1.0 KiCad board source. Do not infer the net or pad solely from current loop sequence or `pin_label`.
3. Preserve existing IDs and explicitly test each source-backed contact mapping: motor labels/pads, endstop labels/pads, J28 guide-position/pad crosswalk, and J37's unassigned-pad status where relevant.
4. Ensure serialization round-trips preserve the new metadata.
5. Do not accept equal ordinal values alone as evidence that a cable cavity mates to a PCB pad. Require a documented cross-coordinate mapping basis.
6. Run focused source-to-model and affected behavior tests, then the full project suite after the focused tests pass. Check `git diff --check` and preserve all other workstream changes.

Source baseline: [Duet2Maestro.kicad_pcb, Duet-2-Hardware repository](https://github.com/Duet3D/Duet-2-Hardware/blob/56958640c73c7febf3bce6e1eefbbdffd5a2db1b/Duet2/Duet2Maestro_v1.0/Duet2Maestro.kicad_pcb), pinned commit `56958640c73c7febf3bce6e1eefbbdffd5a2db1b`; board title block revision 1.0, dated 2018-02-20.

### Bounded PCB-contact crosswalk inventory boundary

The PCB contact map is a bounded, manually reviewed expected crosswalk, not a complete inventory of every board connector. The exact reference PCB is [`Duet2/Duet2Maestro_v1.0/Duet2Maestro.kicad_pcb`](https://raw.githubusercontent.com/Duet3D/Duet-2-Hardware/56958640c73c7febf3bce6e1eefbbdffd5a2db1b/Duet2/Duet2Maestro_v1.0/Duet2Maestro.kicad_pcb), pinned to repository commit `56958640c73c7febf3bce6e1eefbbdffd5a2db1b`. The repository commit SHA is source identity, separate from the PCB title-block revision `V1.0` and date `2018-02-20`. The legacy `pcb_source_revision` property remains a compatibility alias for the repository commit SHA.

The implemented motor-pad subset covers J9 (X), J8 (Y), J36 (Z A), J7 (Z B), J10 (E0), and J6 (E1). The reviewed subset also covers X/Y/E0 endstops J33/J32/J34, Z probe J28, and TEMP_DB J37. Each fixture port is explicitly classified as covered by or outside the reviewed PCB identity inventory. Regression tests compare fixture metadata with fixed expected values manually reviewed against the pinned KiCad source; they do not automatically parse the external PCB file.

### E0/E1 motor PCB identity extension

The pinned Duet 2 Maestro V1.0 PCB assigns named nets to all four numbered pads on J10 / E0 MOT and J6 / E1 MOT. The following expected crosswalk is in legacy fixture-position order, not PCB pad-number order. Source inspected 2026-10-12.

| Stable SemanticPort endpoint ID | Fixture connector | PCB reference | Legacy fixture position / `pin_label` | PCB pad number | PCB net name |
|---|---|---|---|---:|---|
| `duet-2-maestro-v1-0-controller-e0-motor-pin-1` | `e0-motor` | J10 | 1 / `B1` | 3 | `E0_MOT_B1` |
| `duet-2-maestro-v1-0-controller-e0-motor-pin-2` | `e0-motor` | J10 | 2 / `B2` | 4 | `E0_MOT_B2` |
| `duet-2-maestro-v1-0-controller-e0-motor-pin-3` | `e0-motor` | J10 | 3 / `A1` | 1 | `E0_MOT_A1` |
| `duet-2-maestro-v1-0-controller-e0-motor-pin-4` | `e0-motor` | J10 | 4 / `A2` | 2 | `E0_MOT_A2` |
| `duet-2-maestro-v1-0-controller-e1-motor-pin-1` | `e1-motor` | J6 | 1 / `B1` | 3 | `E1_MOT_B1` |
| `duet-2-maestro-v1-0-controller-e1-motor-pin-2` | `e1-motor` | J6 | 2 / `B2` | 4 | `E1_MOT_B2` |
| `duet-2-maestro-v1-0-controller-e1-motor-pin-3` | `e1-motor` | J6 | 3 / `A1` | 1 | `E1_MOT_A1` |
| `duet-2-maestro-v1-0-controller-e1-motor-pin-4` | `e1-motor` | J6 | 4 / `A2` | 2 | `E1_MOT_A2` |

All eight contacts have `named_net_assigned_in_reference_pcb` status. None is unassigned or unknown in this pinned PCB source. The expected values are manually reviewed against the PCB; the regression test does not automatically parse the external PCB file.

This establishes reference-board pad/net identity only. It does not establish the installed board revision, connector mating orientation, cable-cavity numbering, conductor order, motor-coil pairing, firmware drive assignment, installed harness wiring, or as-built connectivity. Those identities require separate evidence or physical verification.

### E0 STOP J34 PCB identity crosswalk

The existing controller-owned `e0-stop` SemanticPort endpoints and their IDs, labels, and fixture-position semantics are preserved. The pinned Duet 2 Maestro V1.0 PCB identifies J34 as E0 STOP and assigns named nets to all three numbered pads. This expected crosswalk is in existing fixture-position order, not PCB pad-number order. Source inspected 2026-10-12.

| Stable SemanticPort endpoint ID | Fixture connector | PCB reference | Fixture position / `pin_label` | PCB pad number | PCB net name |
|---|---|---|---|---:|---|
| `duet-2-maestro-v1-0-controller-e0-stop-pin-1` | `e0-stop` | J34 | 1 / `e0stop` | 3 | `E0_STOP_CONN` |
| `duet-2-maestro-v1-0-controller-e0-stop-pin-2` | `e0-stop` | J34 | 2 / `+3.3V` | 2 | `+3.3V` |
| `duet-2-maestro-v1-0-controller-e0-stop-pin-3` | `e0-stop` | J34 | 3 / `GND` | 1 | `GND` |

All three contacts have `named_net_assigned_in_reference_pcb` status. The expected pad/net values are manually reviewed against the pinned KiCad source; the regression tests do not automatically parse the external PCB file.

This crosswalk records reference-PCB pad/net identity only. It does not establish the installed board revision, connector mating orientation, cable-cavity numbering, harness wiring, as-built connectivity, or active firmware STOP configuration. It creates no firmware-resource assignment.

Source: [Official `Duet2Maestro.kicad_pcb`, Duet-2-Hardware repository](https://github.com/Duet3D/Duet-2-Hardware/blob/56958640c73c7febf3bce6e1eefbbdffd5a2db1b/Duet2/Duet2Maestro_v1.0/Duet2Maestro.kicad_pcb), pinned to commit `56958640c73c7febf3bce6e1eefbbdffd5a2db1b`; title-block revision V1.0, dated 2018-02-20.

A connector/contact omitted from the map is outside the inventory only. Omission does not mean its PCB design identity or net assignment is unknown, that the pad is unassigned, or that a real-world conductor is disconnected. Use the unknown net state only for a represented contact whose PCB net status has not been established; use the unassigned state only where the pinned reference PCB explicitly has no net assigned. J37 pad 10 is an explicit reference-PCB unassigned case, but that does not establish physical disconnection on an installed board.

The map does not establish PCB-view coordinates or cable mating-face/cavity positions. Those identities require their own source-qualified evidence.

### Current validation record

Validation performed on the working tree after adding the J34 / E0 STOP PCB identity crosswalk:

- Focused Board fixture test command, run from `machine-structure-editor`: `.venv\Scripts\python.exe -m pytest -q tests/test_controller_board_fixtures.py` — **30 passed in 0.18s**.
- Full project test command, run from `machine-structure-editor`: `.venv\Scripts\python.exe -m pytest -q` — **843 passed in 12.08s**.
- `git diff --check`: **passed** for the three authorized Board paths.

The J34 expected pad/net values were manually reviewed against the pinned KiCad PCB source. The tests validate fixture metadata and provenance; they do not parse the external PCB file. The mapping establishes reference-board pad/net identity only, not installed-board revision, cable orientation/cavities, actual wiring, or firmware STOP configuration.

### Promega RRF 3.5.4 Configuration-Source Investigation Refresh
From #3 -> To #3 - Promega RRF 3.5.4 Research Check Results
Prepared: 2026-10-17 09:40 EDT | Message ID: MB-20261017-0940-01
Relationship: Follow-up to MB-20261017-0928-01

**Owner and current task.** Controller/Board (#3) owns the bounded Promega configuration-source closeout and maintenance of the controller-side hardware evidence. This is research/documentation only; it does not authorize model, fixture, or source-code changes.

**Public source locations and checkpoint — historical evidence.**
- Repository: `https://github.com/PeterTremonti/M3D-Promega`, under `SD Contents/`. The inspected tree snapshot is commit `fa72508fd221f9238521f33b0bcdc43c0f5d8332` (2026-04-11), containing 171 files.
- Inspected candidates include `SD Contents/sys/config.g`, `sys/config.g.bak`, `sys/config-override.g`, `sys/homeall.g`, `sys/homex.g`, `sys/homey.g`, `sys/homez.g`, `sys/machine_zprobe.g`, `sys/machine_compound_tools.g`, tool macros, and the firmware/sys ConfigTool JSON files.
- `SD Contents/promega_rrf_354_irprobe_bundle.zip` contains five members: `configtool.json`, `sys/homez.g`, `sys/homeall.g`, `sys/bed.g`, and `sys/deployprobe.g`.
- The public `config.g.bak` is not identical to `config.g`. After normalizing line endings, their only content difference is line 31: `config.g` has `M208 X0:360 Y0:380 Z0:380`, while `config.g.bak` has `M208 X0:380 Y0:380 Z0:380`. Their `M92` lines match at lines 30 and 40. The base file identifies ConfigTool 3.5.12 and is dated 2025-06-20; `config-override.g` is dated 2025-06-28 and contains heater-model and G10 workplace-offset settings. The base configuration invokes M501.
- The inspected candidate-file history queries completed and trace to the single SD-card upload commit `8d8385d2efce` (2025-09-21). This is an uploaded snapshot, not an active configuration-change history.

**What the historical public configuration establishes.**
- The snapshot records assignments such as `M584 X0 Y1 Z2`, `M584 E3:4`, CoreXY via `M669 K1`, probe settings, sensors, heaters, fans, and tool definitions.
- The public configuration has `G31 ... Z1.10`, defines sensor S2 as PT1000, and maps the tools to fan index F1. These are historical values only; they are not proof of current installed files or physical wiring.

**Separate live-controller evidence.**
- Live `M115` reported RRF 3.5.4, build date 2024-11-24. Live `M503` differed from the public snapshot, including `G31 ... Z1.50` before later temporary calibration and S2 on `e1temp` as a 100 kΩ B4138 thermistor rather than PT1000. Live heater models also differed. Controller runtime output does not identify the exact SD-card file that supplied each setting.
- Live fan inventory identified F0 as the thermostatically controlled nozzle-heatsink fan associated with heater H2 and a 45°C threshold, F2 as part cooling, and F1 as unconfigured. Physical inspection found wires on FAN0 and FAN2, not FAN1 or the always-on output. `M106 P2 S255` ran both side-mounted part-cooling fans.
- Temporary tool remapping to F2 made part cooling respond during a print, but those temporary `M563` changes were lost at power-off. No permanent tool-mapping edit has been made.
- P9/P11 fan harness identity and variant-specific H2/H4 heater and S8/S6 sensor-side assignments remain physically unverified. Do not infer them from historical diagrams for a different assembly.

**Research-process check results (public snapshot; 2026-10-17).**
- **M98 path-resolution check — completed against the pinned snapshot.** The prior executable research script was not recovered. The batch read public archive commit `fa72508fd221f9238521f33b0bcdc43c0f5d8332` in memory and indexed 171 files, including 34 G-code-like text files. It found seven static `M98` calls; six targets exist exactly, with no case mismatches, dynamic targets, or unparsed includes reported.
- **Existing targets:** `sys/homeall.g:10` -> `sys/homey.g`; `sys/homeall.g:11` -> `sys/homex.g`; `sys/homeall.g:12` -> `sys/homez.g`; `sys/homex.g:5` -> `sys/homey.g`; `sys/homez.g:3` -> `sys/homex.g`; `sys/homez.g:6` -> `sys/homey.g`.
- **Missing target in the public snapshot:** `sys/resurrect.g:9` calls `M98 P"resurrect-prologue.g"`, resolving to `sys/resurrect-prologue.g`, which is absent from that snapshot. This does not establish whether `resurrect.g` is used during normal startup, nor whether the file exists on the installed printer. The full set of static `M98` lines found in the scanned text sources is listed above.
- **Configuration-line inventory — completed as a targeted substitute; original skipped block not recovered.** The executable research script and exact skipped section were not recovered, so this is not represented as a replay of the original script.
- Scope: 22 top-level `SD Contents/sys/*.g` and `*.g.bak` candidates were scanned. Generated `gcodes/*.gcode` and nested subdirectories were excluded.
- The initial configuration scan found 95 command-line occurrences; a separate `M92` supplement found four lines, bringing the total to 99 occurrences across 21 command families. Counts include the backup file and therefore are not 99 independent configuration statements.
- **Exact M92 evidence:** `config.g:30` — `M92 X79.48 Y80.44 Z283.92`; `config.g:40` — `M92 E208.25:208.25`. The same two lines occur in `config.g.bak`.
- **Backup comparison and user-reported reason for the X-limit change:** Raw-byte and normalized-text comparisons both differ. After normalizing line endings, line 31 is the only content difference: `config.g` uses `M208 X0:360 Y0:380 Z0:380`; `config.g.bak` uses `M208 X0:380 Y0:380 Z0:380`. The user confirms they have not modified `config.g.bak` and are unsure of its intended purpose; they tentatively believe it represents earlier/original settings. The user attributes reducing the X maximum in `config.g` from 380 mm to 360 mm to the dual part-cooling fan setup protruding about 20 mm farther and needing clearance. This is user-reported context consistent with the file difference, not independently established file history.
- This scoped scan found no `M581`, `M581.1`, or `M500` command lines in the inspected candidates. `M501` occurs at line 91 in both `config.g` and the backup; the duplicate is not independent evidence. These are public-snapshot findings only.
- **Public configuration-line inventory completed as a targeted substitute:** 22 top-level `sys/*.g` / `sys/*.g.bak` files scanned, excluding generated G-code. The first pass omitted `M92`; the supplemental query verified both M92 statements at lines 30 and 40 in `config.g` and its backup. The backup differs only at M208 line 31, as recorded above. Do not rerun this inventory or claim that the unrecovered original skipped script block was replayed. If further file-level attribution is needed, obtain the installed printer SD-card files separately.
- **History and evidence boundaries:** the earlier candidate-file history queries remain complete and converge on upload commit `8d8385d2efce` (2025-09-21). No history queries were run in the latest batch. Public historical configuration, live controller reports, installed SD-card files, physical board evidence, and physical harness assignments remain distinct evidence classes. The installed files and P9/P11/H2/H4/S8/S6 harness assignments remain unverified.

**Latest physical diagnostic — separate from firmware-source attribution.**
On 2026-10-15/16, IR-probe calibration did not reach a verified conclusion. Repeated `G30 S-1` trigger-height readings drifted systematically, reaching 1.236 mm down to 0.990 mm on 2026-10-16 after repeated Z cycles. The user observed that the bed appeared slightly lower at the same commanded Z position. Live Z settings were reduced to `M201 Z75` and `M203 Z600`; a rail lubricant was later applied, but the mechanical cause remains unresolved. No final calibrated `G31` offset or post-adjustment `G32` mesh is verified. Do not turn these drifting readings into a saved offset or recommend a faster print before Z-position repeatability is established.

**Repository state before this documentation refresh.**
Branch `main`, HEAD and `origin/main` both `a84526b28237d1e678a044c534cc9e8ad6a80444` (`Close X motor functional interface acceptance gaps`). This handoff had no local or staged changes. The shared checkout had ten other modified tracked paths and one untracked test-machine JSON file, with nothing staged. Preserve all of them. This refresh is documentation-only and must remain unstaged/uncommitted unless a later, separately authorized publication step is requested.

**Acceptance gate.** The public-source checks are complete to the extent supported by recoverable evidence: seven static M98 calls were examined (six targets exist and `sys/resurrect-prologue.g` is absent from the pinned snapshot), and a configuration-only inventory covered 22 top-level `sys` `.g` / `.g.bak` files, including the supplemental M92 check. The exact original skipped script block was not recovered, so this is a documented targeted substitute rather than a claim that the original skipped code ran. The public backup's single normalized content difference is the M208 X lower bound on line 31. Installed SD-card configuration and physical harness assignments remain unverified.

### Concrete next research steps

1. **Immediate next action — #3:** complete the rendered manufacturer-PDF visual verification of the SKR Mini E3 V3.0 EXP1 diagram. This public-source check can proceed independently of Promega SD-card evidence and other workstream publication. Preserve the existing X Motor and SKR EXP1 dispositions; do not infer a physical cavity map from MCU aliases.

2. **Independent Board research — #3:** continue the reference-board coverage and geometry work from manufacturer/KiCad sources, including connector locations/orientation and mounting-hole relationships where source evidence supports them. This does not depend on the installed Promega harness.

3. **Promega configuration comparison — blocked only on installed-file evidence:** when back at work, the user plans to add the current SD-card contents to a second, clearly named folder in the Promega-specific repository, leaving the existing historical `SD Contents/` snapshot untouched. #3 will compare the installed configuration and its `M98` include tree after that repository update. No direct upload, photo, or new artifact is requested here.

4. **Promega physical harness facts remain unresolved:** P9/P11 fan identity and the applicable H2/H4 heater and S8/S6 sensor mappings must not be asserted from a historical configuration alone. Continue using available public sources; retain unknown status for facts those sources cannot establish.

The existing IR-probe reference connections and corrected J4 mapping remain established project context. No duplicate implementation is proposed here. No new ontology, fixtures or source changes are authorized by this research update.

## 35. Octopus V1.1 / TMC5160T Pro V1.0 Contact-6 Source Investigation

**Date:** October 18, 2026

**Classification:** Independent manufacturer-source investigation
**Publication state:** Planning granted the publication slot on October 18, 2026 (MB-20261018-1043-01). This record documents an unresolved investigation and does not close it.

**Disposition:** UNRESOLVED — documented pin/function labels do not establish the complete electrical path or configured-state behavior.

### Question and established facts

The open question concerns Octopus V1.1 Driver 2 connector contact 6, documented as `SLEEP` on net `DRIVER2_SLP`, versus BIGTREETECH TMC5160T Pro V1.0 module J1-6, documented as `CLK`. These are different documented function labels. Matching contact numbers or labels alone do not establish continuity, electrical equivalence, physical mating, or the as-built connection.

The official BIGTREETECH Octopus schematic PDF is available at this immutable repository snapshot:

- https://github.com/bigtreetech/BIGTREETECH-OCTOPUS-V1.0/blob/9526ff16f68839626cb8875a299e73f99f2e57e8/Hardware/BIGTREETECH%20Octopus%20-%20SCH.pdf

The manufacturer hardware README states that the V1.0 and V1.1 schematics are the same, while V1.1 changes include corrections to fan/SPI3/UART2 silkscreen and a power-supply IC package change:

- https://github.com/bigtreetech/BIGTREETECH-OCTOPUS-V1.0/tree/master/Hardware

That README URL uses mutable `master`; its exact commit revision still needs to be captured before treating it as a revision-pinned bridge between hardware versions.

The official Octopus guide cautions that its simplified step/dir pin table is not the actual pinout and describes driver jumper settings, including the SPI-related arrangement. This reinforces that an abbreviated pin table or silkscreen is not a substitute for tracing the schematic and the applicable jumper configuration:

- https://github.com/bigtreetech/docs/blob/master/docs/Octopus.md

The TMC5160T Pro V1.0 manufacturer documentation distinguishes module J1-6 `CLK` (external clock input) from J1-3 `SCK/CFG2` (SPI serial clock); it identifies SPI as the operating mode:

- https://github.com/bigtreetech/docs/blob/master/docs/TMC5160T%20Pro%20V1.0.md

This documentation also uses mutable `master`; its exact repository revision was not captured in this investigation.

The Analog Devices/Trinamic TMC5160A datasheet, Rev. 1.18 dated March 1, 2023, describes IC CLK as a clock input, explains that grounding CLK selects the internal oscillator, and describes external-clock behavior:

- https://www.analog.com/media/en/technical-documentation/data-sheets/tmc5160a_datasheet_rev1.18.pdf

That datasheet establishes the IC-level meaning of `CLK`, but does not prove that the specific TMC5160T Pro V1.0 module's J1-6 connects to the IC CLK pin through its PCB and associated components.

### Additional manufacturer-repository finding

The official BIGTREETECH-Stepper-Motor-Driver repository exposes separate version-named directories. At repository snapshot `9f9680040e7f696f132b1c0d75a6f79c9f288b13`, the `TMC5160_Pro V1.0/Hardware` directory lists `TMC5160_Pro V1.0-PIN.pdf` but no schematic in that directory. The separate `TMC5160(T) Pro V1.1/Hardware` directory lists `BIGTREETECH TMC5160T_Pro-SCH.pdf`, `BIGTREETECH TMC5160_Pro-SCH.pdf`, and V1.1 pin/layout files.

Revision-pinned manufacturer directory listings:
- https://github.com/bigtreetech/BIGTREETECH-Stepper-Motor-Driver/tree/9f9680040e7f696f132b1c0d75a6f79c9f288b13/TMC5160_Pro%20V1.0/Hardware
- https://github.com/bigtreetech/BIGTREETECH-Stepper-Motor-Driver/tree/9f9680040e7f696f132b1c0d75a6f79c9f288b13/TMC5160%28T%29%20Pro%20V1.1/Hardware

The naming difference between `TMC5160_Pro V1.0` and `TMC5160T Pro V1.0` is not reconciled by these directory names alone. The presence of a V1.1 schematic therefore does not prove its internal electrical path applies to the V1.0 module under investigation. This narrows the source gap but does not close it: no revision-qualified V1.0 schematic or manufacturer statement bridging the relevant versions has been verified. No continuity claim is inferred from these file listings.

### Evidence gap and disposition

The available evidence does not yet demonstrate the full electrical route from Octopus connector contact 6 through the relevant board-side jumper/configuration network in the applicable SPI arrangement. Nor has a revision-qualified TMC5160T Pro V1.0 schematic or PCB trace been verified to establish J1-6 continuity to the module IC CLK input and clock-selection circuitry.

A generic TMC5160 module schematic, a third-party schematic transcription, or an unpinned documentation page is not sufficient by itself to close these revision-specific gaps. No conclusion is made about the final electrical state, compatibility, or the user's as-built hardware.

### Revision-qualified contact-5/contact-6 evidence checkpoint - 2026-10-19

**Immutable manufacturer-source references**
- `bigtreetech/docs`: `bc29be3812cf1615633705a5e946f5500ea3780c`.
- `bigtreetech/BIGTREETECH-Stepper-Motor-Driver`: `9f9680040e7f696f132b1c0d75a6f79c9f288b13`, matching the previous investigation snapshot.
- Regular Octopus schematic file: `https://github.com/bigtreetech/BIGTREETECH-OCTOPUS-V1.0/blob/9526ff16f68839626cb8875a299e73f99f2e57e8/Hardware/BIGTREETECH%20Octopus%20-%20SCH.pdf`. It is published in the V1.0-named repository, not as a separately identified regular Octopus V1.1 schematic.
- Octopus guide: `https://github.com/bigtreetech/docs/blob/bc29be3812cf1615633705a5e946f5500ea3780c/docs/Octopus.md`.
- TMC5160T Pro V1.0 pin description: `https://github.com/bigtreetech/docs/blob/bc29be3812cf1615633705a5e946f5500ea3780c/docs/TMC5160T%20Pro%20V1.0.md`.
- Driver repository V1.0 directory: `https://github.com/bigtreetech/BIGTREETECH-Stepper-Motor-Driver/tree/9f9680040e7f696f132b1c0d75a6f79c9f288b13/TMC5160_Pro%20V1.0`.

**Manufacturer-listed pairing.** BIQU's Octopus V1.1 product page offers bundles with six or eight TMC5160T V1.0 drivers: `https://biqu.equipment/products/bigtreetech-octopus-v1-1`. This is evidence of intended commercial pairing, not a netlist or proof of every contact's electrical path.

**Octopus guide revision limitation.** The pinned guide describes the first-column lower-row jumper as connecting SLP and RST and warns that microstepping configuration pins are shared with SPI. Its product profile calls the board Octopus V1.0 while its product link points to Octopus V1.1. It therefore does not independently establish revision-qualified Driver 2 contact-5/contact-6 routing on regular Octopus V1.1.

**Module pin assignment and orientation.** The pinned TMC5160T Pro V1.0 documentation lists J1-5 as SDO/CFG0 and J1-6 as CLK (external clock input). Its pin diagram marks the EN corner for orientation. The pin table and illustration do not establish the complete PCB trace from J1-6 to the IC CLK pad, nor do they by themselves establish which physical Octopus socket contacts mate with J1-5 and J1-6.

**Manual-version cross-link.** The BIQU TMC5160T Pro V1.0 product page links a user manual titled TMC5160 PRO-V1.1. That explains the available V1.1 documentation lead, but does not establish identical V1.0 pad layout or routing. The separate `TMC5160(T) Pro V1.1` directory's schematics are not substituted for missing V1.0 evidence. BIGTREETECH driver repository issue #25 contains user reports, not manufacturer confirmation of the electrical path.
- Product page: `https://biqu.equipment/collections/motor-driver/products/tmc5160-pro-v1-0`
- Linked manual: `https://cdn.shopify.com/s/files/1/1619/4791/files/BIGTREETECH_TMC5160_PRO-V1.1_user_manual_1.pdf?v=1699435321`
- Issue #25: `https://github.com/bigtreetech/BIGTREETECH-Stepper-Motor-Driver/issues/25`

**Separate Pro-board warning.** The official `BIGTREETECH-OCTOPUS-Pro` repository has a schematic named `BIGTREETECH Octopus Pro V1.1-sch.pdf`. It is explicitly the Pro variant and cannot fill the regular Octopus V1.1 schematic gap: `https://github.com/bigtreetech/BIGTREETECH-OCTOPUS-Pro/blob/master/Hardware/BIGTREETECH%20Octopus%20Pro%20V1.1-sch.pdf`.

**SPI-mode jumper evidence.** At the pinned manufacturer documentation revision `bc29be3812cf1615633705a5e946f5500ea3780c`, the `Octopus.md` guide places the lower-row first-column SLP/RST bridging instruction in its STEP/DIR MODE section and separately directs users to the `Octopus_DRI4.webp` illustration for SPI MODE jumper configuration. Source image: `https://raw.githubusercontent.com/bigtreetech/docs/bc29be3812cf1615633705a5e946f5500ea3780c/docs/img/Octopus/Octopus_DRI4.webp`. The STEP/DIR instruction alone does not establish an SLP/RST bridge in the intended SPI configuration. The guide identifies its product profile as Octopus V1.0 while linking to the V1.1 product page, so it does not establish revision-qualified regular Octopus V1.1 routing or the as-built jumper state.

**Conditional hypothesis only.** A possible bridge involving module J1-5 (SDO/CFG0) and J1-6 (CLK) cannot be inferred from the STEP/DIR jumper note alone. The regular Octopus V1.1 Driver 2 contact-5/contact-6 net mapping, module mating orientation, applicable SPI jumper routing, and installed jumper state remain unverified. This is not a confirmed short, incompatibility, or as-built path.

**Disposition remains UNRESOLVED.**

### Next evidence avenue

1. Continue searching manufacturer-published sources for a revision-qualified regular Octopus V1.1 schematic, netlist, or board-trace evidence for Driver 2 contacts 5 and 6 and their SLP/RST/SPI-related paths.
2. Seek a manufacturer-issued TMC5160T Pro V1.0 schematic or reliable revision-specific PCB trace from J1-6 to IC CLK. Do not infer V1.0 routing from the Pro V1.1 manual or schematic.
3. Cross-check the module's EN-corner orientation against an official, revision-matched Octopus socket drawing or photograph; preserve the distinction between intended product pairing and proven contact mapping.
4. If no new primary public evidence exists, record that limitation and request Planning's direction before expanding beyond the bounded public-source investigation.

## 36. Octopus Receiving-Interface Persistence Regression Checkpoint

**Date:** October 20, 2026

**Classification:** Bounded runtime persistence implementation and regression validation. This is separate from the manufacturer-source investigation in section 35.

**Planning authorization:** `MB-20261020-1639-01`; scope clarification `MB-20261020-1722-01`. Planning did not authorize conversion of the separate TMC5160T module-interface contact map or changes to the generic persistence encoder.

### Reproduced failure and isolation

- The initial save/reopen regression used `add_octopus_tmc5160t_mating_experiment`, which adds the TMC5160T hardware definition to the model. Its first failure occurred in `save_editor_state()` on the TMC5160T module-interface map, whose integer-keyed contacts included labels such as `EN`, `SDI/CFG1`, `SCK/CFG2`, and `CSN/CFG3`. This full-fixture result did not isolate the Octopus receiving-interface map.
- Following Planning's scope decision, the regression setup was narrowed to a minimal Octopus V1.1 controller and a socket `SemanticPort` carrying only `BTT_OCTOPUS_MOTOR_DRIVER_RECEIVING_INTERFACE_SPEC`. It excludes `build_btt_tmc5160t()` and the separate module hardware definition.
- Before the catalog change, this isolated test also failed in `save_editor_state()` with `TypeError: Persistence currently requires string dictionary keys.` The traceback showed the Octopus receiving-interface `contacts` map itself had integer keys 1 through 18.

### Implementation and assertions

`machine-structure-editor/src/machine_builder/hardware_catalog.py` now represents the Octopus receiving-interface `contacts` as a list of 18 records. Every record carries a numeric `position` plus its original `label` and `classification`; positions 1-16 remain active, position 17 remains `NC`/`not_connected`, and position 18 remains `DIAG`/`diagnostic`.

`machine-structure-editor/tests/test_octopus_driver_mating.py` updates the contact assertions to check ordered positions and the final two contact records. The new `test_octopus_receiving_interface_contacts_survive_save_reopen` saves and reloads an `EditorState` through the actual persistence APIs, then verifies that all contact records and positions survive the round trip.

No change was made to `persistence.py` or to the separate TMC5160T module-interface catalog.

### Focused validation

Exact command run from `machine-structure-editor`:

`python -m pytest -q tests/test_octopus_driver_mating.py tests/test_persistence.py tests/test_store_persistence.py tests/test_controller_board_fixtures.py`

**Published implementation validation (2026-10-20):** `65 passed in 0.33s`; pytest exit code `0`. The staged whitespace check passed, and post-push local `HEAD`, `origin/main`, and live remote `main` converged on the published commit.

Whitespace validation:

`git diff --check -- machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md machine-structure-editor/src/machine_builder/hardware_catalog.py machine-structure-editor/tests/test_octopus_driver_mating.py`

**Result at publication-slot pre-stage validation:** exit code `0`.

These are local runtime test results. They are not manufacturer-source evidence and do not resolve any electrical path.

### Published implementation and current dependency status

The Octopus receiving-interface contact-list persistence correction and its save/reopen regression were published in commit `ae5a9a1672d151c37e392e9bff4f2421f0a465f2` (`Fix Octopus receiving-interface persistence`). Published paths were `machine-structure-editor/src/machine_builder/hardware_catalog.py`, `machine-structure-editor/tests/test_octopus_driver_mating.py`, and this handoff. Publication validation passed `65 passed in 0.33s`; the staged whitespace check and post-push ref convergence checks passed. The generic persistence encoder and the separate TMC5160T module-interface contact map were not changed.

**Stepper-terminal dependency hold (Planning messages `MB-20261020-2045-03` and `MB-20261021-1618-01`).** The local-only `machine-structure-editor/tests/test_stepper_motor_terminal_profile.py` and `tests/test_controller_board_fixtures.py` passed together with `34 passed in 0.20s` on 2026-10-20 in the combined working tree. That result depends on `UpdateMachineComponentWithStepperTerminalProfile`, which is present in the modified local `machine-structure-editor/src/machine_builder/semantic_component_mutations.py` but absent from the published baseline. The result therefore does not demonstrate that the test passes against published code. Planning directed #3 to hold the test until #4 publishes its semantic/routing dependency, after which Planning will reassess the baseline and authorize a separate Board slot. The current documentation-only slot authorizes these two documents only; it does not authorize the test or #4 product code.

**Local-change boundary.** The additional section 35 V1.0 manual/source-note hunk was already local before this refresh. It is intentionally separate from the continuity edit and must remain unstaged in this slot. Its third-party/manual and issue-tracker leads do not prove the disputed electrical path. Preserve it and all other #2/#4/#5 paths without staging, discarding, or rewriting them. Contact-6 remains **UNRESOLVED**.

The Octopus V1.1 Driver 2 contact-6 / `DRIVER2_SLP` versus TMC5160T Pro V1.0 J1-6 / `CLK` question remains **UNRESOLVED**. The persistence regression is independent of that electrical investigation.

**Publication-slot baseline:** `f5c02430496ebb5afb406ac7783a7d746c09c503` (Document publication throughput and recovery conventions). Local HEAD, `origin/main`, and live remote `main` matched this baseline before the authorized publication work.
