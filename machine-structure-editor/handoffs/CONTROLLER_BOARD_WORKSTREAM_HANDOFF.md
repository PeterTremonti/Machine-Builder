# Machine Builder — Controller / Board Workstream Handoff

## Recovery instructions

A replacement Controller / Board chat should read this file first, then:

1. `PROJECT_CURRENT_STATE.md`
2. the current repository source and tests

Treat the current repository and actual test results as authoritative over older checkpoint text.

This is a living recovery document. Preserve the cumulative history when updating it. Add new checkpoints rather than rewriting or removing earlier history.

The Controller / Board workstream uses the shared `main` branch and the single Machine Builder checkout.

Board implementation should preserve the established canonical semantic model / visual model boundary and should not silently promote research candidates into new ontology.

---

# What we've done so far

## Initial Controller / Board direction

The Controller / Board workstream was established to investigate:

- controller-board creation
- real documented board hardware definitions
- installed Controller instances
- Controller Resources
- physical board interfaces
- port breakouts
- controller-board visualization
- related wiring and hardware documentation

The intended hardware path remains:

```text
Real documented hardware
        ↓
Hardware Definition
        ↓
Installed Controller
        ↓
Controller Resources
        ↓
Physical interfaces / ports
        ↓
Connections / machine semantics

The workstream has deliberately used real documented hardware rather than hypothetical boards.

The first real board case became the Duet 2 Maestro v1.0.

Hardware Definition work

A reusable Duet 2 Maestro hardware definition was added to the hardware catalog using manufacturer documentation as provenance.

Known documented characteristics recorded for the Maestro include:

Duet 2 Maestro identity
Duet3D manufacturer
v1.0 variant
ATSAM4S8C processor
five onboard TMC2224 stepper drivers
three heater outputs
three controlled fan outputs
related documented controller resources

Relevant implementation files included:

machine-structure-editor/src/machine_builder/hardware_catalog.py
machine-structure-editor/tests/test_hardware_catalog.py

The Maestro definition is reusable hardware information. It is distinct from an installed Controller instance.

Controller ↔ Hardware Definition

Controller instances were linked to reusable hardware definitions through the existing hardware_definition_id relationship.

This reinforced:

Hardware Definition
        ↓
installed Controller

rather than treating the reusable board definition as the installed machine controller itself.

This boundary was subsequently documented as reinforced architecture.

Controller-owned physical ports

The implementation later established that a Controller may own semantic ports.

The canonical model now permits a SemanticPort to belong to either:

Machine Component

or:

Controller

but not both.

The Controller therefore has its own port_ids, while ControllerResource remains a separate concept.

The relevant implementation area included:

machine-structure-editor/src/machine_builder/controller.py
machine-structure-editor/src/machine_builder/semantic_model.py

The associated tests were updated as part of that implementation checkpoint.

This was an important distinction:

Controller Resource
        ≠
Physical Semantic Port

A Controller Resource represents something the installed controller provides or exposes for machine use.

A controller-owned SemanticPort represents an externally accessible physical interface.

The two concepts therefore remain separate even when they are physically related.

Physical-inventory / evidence-gathering stage

The workstream then moved into physical and documentary inventory of the Maestro.

Observed/documented physical interface examples include:

motor connectors with 4 positions
heater connections with 2 positions
temperature-sensor connections with 2 positions
endstop connectors with 3 positions
a 5-position Z-probe connector
fan connections with 2 positions and no tach/speed-sensor connection
screw/terminal-style connections for some higher-power functions
separate physical Z A and Z B motor connectors
other documented board interfaces such as display, expansion, USB, Ethernet, and related connectors

The Z A / Z B case was particularly important.

It demonstrates that:

one Controller Resource
        ↓
may be exposed through
        ↓
multiple physical access points

Therefore a ControllerResource should not simply contain one physical port_id.

The resource and physical-interface layers remain distinct.

Checkpoint 22 — Connector vs. Mating Interface

Date: 2026-09-30

What we've done so far

The Controller / Board workstream reached the physical-inventory and evidence-gathering stage for its first real documented board case: the Duet 2 Maestro.

The work used the documented Maestro hardware definition together with physical observations of the board's accessible connectors and terminals.

A potentially meaningful distinction emerged between:

Physical Connector

the actual connector or terminal physically present on the installed hardware

and:

Mating Interface

the defined characteristics that determine what another connector, housing, contact system, or harness component must provide in order to mate with that physical connector

This distinction matters because board documentation can answer not only electrical questions but also practical harness-construction questions such as:

what connector family is used
what pitch is used
how many positions are present
what retention/keying features are present
what mating parts are required
what parts are needed to replace or build a harness

At this stage the distinction was treated as a candidate architectural observation only.

No canonical MatingInterface entity was introduced.

Research result from #2

External research materially strengthened the distinction and found strong precedent for separating:

Physical Connector
        ≠
Reusable Connector Definition
        ≠
Mating Interface / interface characteristics
        ≠
Intermateability / compatibility relationship
        ≠
Actual Mated Connector Pair

These are not being treated as five new canonical entities.

They represent different kinds of information, reusable definitions, physical instances, and relationships that the architecture may eventually need to represent.

The research also found an additional manufacturer/standards distinction:

Mating-interface characteristics can be distinct from termination-interface characteristics.

It also found that:

connector housings and contacts/terminals may have separate reusable definitions.

This strengthens the case for not collapsing every connector-related fact into a single object.

The research goal was not to copy another system's ontology, but to establish terminology and modeling patterns that can inform Machine Builder.

Files touched

The intended dedicated Board workstream handoff is:

machine-structure-editor/handoffs/CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md

For this checkpoint itself, the documentation change is the handoff.

No implementation source files were changed for the Connector / Mating Interface discovery.

Earlier implementation work in this workstream did touch controller, semantic-model, hardware-catalog, and associated test files as noted in the cumulative history above.

Decisions / classifications
REINFORCE
Controller Resource and Physical Connector remain distinct.
The Maestro Z A / Z B case reinforces that one controller resource may have multiple physical access points.
Reusable hardware definitions remain distinct from installed physical instances.
Controller-owned physical SemanticPort objects remain distinct from Controller Resources.
The canonical semantic model remains distinct from visual/editor representation.
NEW PRINCIPLE — candidate

A physical connector, the reusable information describing its mating interface, and the compatibility relationship determining whether two connector definitions can mate are different kinds of information and should not automatically be collapsed into one concept.

The research also reinforces that connector housing, contact/terminal, termination-interface, and mating-interface information may have distinct identities or relationships.

This remains a candidate principle until implementation and further architecture work establish exactly what Machine Builder needs.

WATCH
whether mating-interface characteristics should be structured data within a Connector Definition or a separate reusable definition
whether intermateability/compatibility should be modeled as a relationship between reusable definitions
whether actual mating between two installed connector instances eventually needs persistent semantic representation
how connector housings, contacts, terminals, and termination interfaces should be represented later if harness/catalog requirements make that necessary
whether the existing Port / Connector / Pin model can represent the distinction cleanly without prematurely adding canonical entities
whether the first Maestro representation exposes any requirement that cannot be handled by the existing Controller / SemanticPort / HardwareDefinition boundaries
IMPLEMENTATION ONLY

None yet for this discovery.

No new canonical MatingInterface, Intermateability, BoardConnector, or similar class has been added.

No untyped property has been added merely to force the research result into the current implementation.

Current state

No implementation source change was justified by the Connector / Mating Interface research alone.

The immediate goal is to understand the physical and documentation model before deciding what canonical representation, if any, is required.

The Maestro case currently demonstrates that Machine Builder needs to account for at least:

Controller Resource
        ↓
physical access point(s)
        ↓
connector / terminal
        ↓
accessible pin or terminal positions

and separately:

physical connector
        ↔
mating/interface characteristics
        ↔
compatible mating hardware

The research strengthens this conceptual separation but does not yet justify creating every concept as a canonical entity.

The latest test result known specifically to this Board workstream at this checkpoint is:

724 passed

This is a Board-workstream-known result, not the current project-wide baseline.

Later shared main work has reported newer project-wide routing results of 730/730.

Proposed Minimal Maestro Representation

The first Maestro implementation should use the smallest representation that exercises the newly clarified boundaries without prematurely expanding the ontology.

1. Physical connector occurrence

Use the existing controller-owned SemanticPort objects for externally accessible pin/terminal endpoints.

Use the existing connector_id to group the individual SemanticPort objects belonging to one physical connector occurrence.

Conceptually:

Installed Controller
    ↓
Physical connector occurrence
    ↓
connector_id
    ↓
SemanticPort 1
SemanticPort 2
SemanticPort 3
...

For a four-position motor connector:

connector_id = "z-a-motor"

SemanticPort
    position = 1
    electrical purpose = ...

SemanticPort
    position = 2
    electrical purpose = ...

SemanticPort
    position = 3
    electrical purpose = ...

SemanticPort
    position = 4
    electrical purpose = ...

The same approach can represent the Maestro's 2-position, 3-position, and 5-position interfaces.

This does not make SemanticPort synonymous with Connector.

The ports represent accessible endpoints; connector_id groups them as belonging to a physical connector occurrence.

2. Reusable hardware-definition information

Keep reusable board-specific connector knowledge associated with the reusable Hardware Definition.

The first implementation only needs enough structured information to identify the documented connector interface accurately.

Potential information includes:

connector identity/name
position count
connector family/series where verified
pitch where verified
board-side form where verified
retention/keying information where verified
manufacturer/part information where verified
source/provenance

Do not add fields merely because they might eventually be useful.

Add only information required by the first real Maestro representation.

3. Mating-interface characteristics

Do not create a separate canonical MatingInterface object yet.

For the first Maestro implementation, retain only verified connector/interface information needed to describe and identify the board-side connector and its known mating requirements.

Do not prematurely model:

housing
contact
terminal
termination interface
mating interface

as separate canonical entities.

The research establishes that these may be distinct concepts, but the first implementation must demonstrate an actual need before they become part of the Machine Builder ontology.

4. Future compatibility / intermateability

Do not use:

ControllerResourceAssignment

or:

Connection

to represent connector compatibility.

Those concepts have different meanings.

A future compatibility relationship will likely need to relate reusable connector/interface definitions rather than actual installed connector instances, but this remains a deferred architectural question.

Conceptually:

Reusable Connector Definition A
            ↕
     compatibility /
      intermateability
            ↕
Reusable Connector Definition B

The exact canonical representation remains undecided.

5. Actual mated connector pairs

Do not model actual connector mating between two installed connector instances yet.

That is a separate question from whether two reusable connector/interface definitions are compatible.

The distinction remains:

Can these definitions mate?
        ≠
Are these two physical connector instances actually mated?

An actual persistent mating relationship should remain deferred until a real Machine Builder use case requires it.

6. Needed for the first implementation

The minimum useful Maestro representation should support:

HardwareDefinition
        ↓
installed Controller
        ↓
controller-owned SemanticPorts
        ↓
connector_id grouping
        ↓
documented pin / terminal positions

and should preserve the conceptual relationship:

Controller Resource
        ↔
one or more physical access points

without making either concept the other.

7. Deferred

For the first Maestro implementation, defer:

first-class Connector entity
first-class MatingInterface entity
first-class Intermateability entity
actual MatedConnectorPair entity
reusable Housing entity
reusable Contact entity
reusable Terminal entity
full TerminationInterface ontology
general-purpose connector compatibility engine

These remain candidates for later work only if concrete implementation or harness/catalog requirements demonstrate that the existing representation is insufficient.

Unresolved architectural questions

The following remain open:

Should a reusable Connector Definition become a first-class canonical concept, or can the required reusable information remain part of HardwareDefinition?
Should mating-interface characteristics be structured fields within a reusable Connector Definition, or a separate reusable definition?
Should intermateability be modeled as a relationship between reusable definitions?
Does Machine Builder eventually need to persist the fact that two installed connector instances are actually mated?
When harness generation becomes important, how should reusable connector housings, contacts, terminals, and termination interfaces be represented without over-expanding the core ontology?
Does the existing SemanticPort plus connector_id structure remain sufficient for the first Maestro representation?

# Checkpoint 23 — First Maestro Physical Interface Representation

Date: 2026-09-30

## What we've done so far

The first concrete Maestro physical-interface implementation experiment has now been completed and tested.

The experiment used the existing Controller-owned `SemanticPort` model together with `connector_id` grouping. No new canonical Connector, MatingInterface, Intermateability, BoardConnector, or similar entity was introduced.

The fixture represents representative externally accessible Maestro interfaces:

```text
X motor       4 positions
Z A motor     4 positions
Z B motor     4 positions
heater        2 positions
thermistor    2 positions
endstop       3 positions
Z probe       5 positions
fan           2 positions

Prepare a concrete implementation design for the first Maestro connector representation using the existing Machine Builder concepts.

The design should first identify the smallest set of changes needed to represent several real Maestro examples, such as:

4-position motor connector
2-position heater connection
2-position thermistor connection
3-position endstop connector
5-position Z-probe connector
2-position fan connector

Before implementation, verify the exact current source/test state on shared main.

Do not add MatingInterface, Intermateability, BoardConnector, or similar canonical classes unless subsequent evidence demonstrates that the existing architecture cannot represent the required Maestro case cleanly.

The next implementation checkpoint should include tests demonstrating the relationship between controller resources and their externally accessible physical interfaces without collapsing those concepts.

# Checkpoint 24 — Controller Resource Exposure Through Physical Interfaces

Date: 2026-10-01

## Classification

DECIDED

## What we've done so far

Inspected the current Controller Resource, Controller Resource Assignment,
and SemanticRelationship implementations and their tests to determine the
smallest existing architectural mechanism for representing the physical
interfaces through which a Controller Resource is externally accessible.

`ControllerResource` contains the identity and controller ownership of a
usable controller-supplied resource, but does not contain a physical-port
reference.

`ControllerResourceAssignment` has a distinct semantic purpose: it records
the mapping between a machine-semantic object and a Controller Resource.
It is therefore not appropriate for recording the physical exposure of a
resource on a controller board.

`SemanticRelationship` is already a directed relationship between canonical
objects and is capable of relating a Controller Resource to a SemanticPort.
The existing relationship vocabulary contains:

- `realizes`
- `supports`
- `requires`
- `depends_on`
- `participates_in`

None of these has a sufficiently precise meaning for physical exposure of
a Controller Resource through an externally accessible interface.

## Decision

Use the existing `SemanticRelationship` mechanism with one new relationship
type:

`exposed_through`

The direction is:

`ControllerResource → SemanticPort`

The meaning is:

> A Controller Resource is externally accessible through this physical
> interface.

The relationship may occur multiple times for one Controller Resource.

The Maestro Z resource is the concrete test case:

`Z stepper resource`
→ four Z A physical access-point ports

and

`Z stepper resource`
→ four Z B physical access-point ports

The two connector groups remain distinguishable through the existing
`SemanticPort.connector_id` grouping.

This does not introduce:

- a new Connector canonical entity
- a new Resource-to-Port association dataclass
- a `port_id` field on Controller Resource
- reuse of Controller Resource Assignment for physical exposure
- a list of physical port IDs inside untyped properties

## Semantic rationale

A Controller Resource and a physical access point answer different semantic
questions.

Controller Resource:

> What usable controller capability/resource does the installed controller
> provide?

Physical SemanticPort:

> Where is that capability/resource externally accessible on the installed
> hardware?

Controller Resource Assignment answers another question:

> Which machine-semantic purpose is using this controller resource?

Keeping these as separate concepts preserves the distinction between
semantic resource allocation and physical board topology.

## Maestro Z A / Z B evidence

The Duet 2 Maestro has one Z stepper-driver resource with two separate
external motor connector groups, Z A and Z B.

This is the required one-resource-to-multiple-physical-access-points case.

The current physical-interface fixture already represents the connector
contacts as controller-owned SemanticPorts and groups their positions with
`connector_id`.

The new relationship therefore needs to connect the single Z resource to
the individual Z A and Z B SemanticPorts rather than attempting to create a
new connector-level canonical object.

## Current state

The architectural mechanism is now settled, but the association has not yet
been implemented.

The next implementation slice should:

1. add `exposed_through` to the relationship vocabulary;
2. add focused relationship tests for the new semantic type;
3. extend the Maestro fixture with a representative Z Controller Resource;
4. create `exposed_through` relationships from that resource to the four Z A
   and four Z B physical access-point ports;
5. add tests proving one resource can be related to both connector groups;
6. preserve the existing absence of Controller Resource Assignment in this
   physical-exposure test.

A lifecycle check is also warranted because relationship records involving
Controller Resources and Ports must not become dangling references when
those canonical objects are removed.

## Unresolved / WATCH

The current model does not make a connector group itself a canonical object.
That is acceptable for this implementation because the physical access
points are already canonical SemanticPorts and `connector_id` provides the
grouping.

Future evidence may justify richer connector-definition or mating-interface
modeling, but this checkpoint does not introduce those concepts.

## Next action

Implement and test `exposed_through` using the Maestro Z resource with the
Z A / Z B physical-interface fixture as the concrete many-access-point case.

# Checkpoint 25 — Controller Resource Physical Exposure

Date: 2026-10-02

## Classification

DECIDED / IMPLEMENTATION

## What we've done so far

Implemented the Controller Resource → physical interface relationship
established by Checkpoint 24.

The existing `SemanticRelationship` mechanism is now used with the new
relationship type:

`exposed_through`

The relationship direction is:

`ControllerResource → SemanticPort`

and means:

> A Controller Resource is externally accessible through this physical
> interface.

The Duet 2 Maestro fixture now includes a representative Z stepper
Controller Resource and relates that single resource to all eight physical
access-point ports belonging to the separate Z A and Z B motor connector
groups.

The implementation deliberately does not introduce a canonical Connector
entity, a new Resource-to-Port association class, or a physical-port list
field on Controller Resource.

## Files changed

`machine-structure-editor/src/machine_builder/semantic_relationship.py`

Added `exposed_through` to the existing relationship vocabulary.

`machine-structure-editor/src/machine_builder/controller_board_fixtures.py`

Extended the Maestro fixture with a representative Z stepper Controller
Resource and eight `exposed_through` relationships to the Z A and Z B
physical access-point ports.

`machine-structure-editor/src/machine_builder/semantic_model.py`

Updated Controller Resource removal so relationships referencing a removed
Controller Resource are also removed, preventing dangling semantic
relationships.

`machine-structure-editor/tests/test_semantic_relationship.py`

Added coverage proving that `exposed_through` is accepted and preserves the
directed relationship semantics.

`machine-structure-editor/tests/test_controller_board_fixtures.py`

Added coverage for:

- creation of the representative Z stepper resource;
- eight physical exposure relationships;
- exposure through both Z A and Z B connector groups;
- preservation of the distinction from Controller Resource Assignment;
- cleanup of exposure relationships when the resource is removed.

## Test result

Focused tests:

`19 passed in 0.22s`

Full repository suite:

`740 passed in 4.50s`

The full suite is the current authoritative regression result for this
implementation checkpoint.

## Semantic result

The Maestro Z A / Z B case confirms that one Controller Resource can be
represented as externally accessible through multiple physical access
points without conflating:

`Controller Resource`

with:

`Physical SemanticPort`

or:

`Controller Resource Assignment`

The individual physical contacts remain canonical SemanticPorts. Their
existing `connector_id` values continue to group them into physical
connector/access-point groups.

## Important limitation

The current Maestro fixture remains intentionally representative rather
than a complete electrical pinout.

The physical ports currently carry generic connector-contact purposes and
do not yet model verified electrical roles, exact connector specifications,
mating parts, or harness construction details.

Those details remain future Board catalog work and should be added only as
documented evidence supports them.

## Rejected approaches

The implementation did not:

- add `port_id` or `port_ids` to Controller Resource;
- reuse Controller Resource Assignment for physical exposure;
- add a canonical Connector entity;
- encode the relationship as an arbitrary list of IDs in `properties`;
- model internal MCU/package wiring.

## Current state

Controller Resources can now be related to one or more externally accessible
physical SemanticPorts through the canonical semantic relationship graph.

The Duet 2 Maestro Z resource is the first concrete many-access-point
example, with one resource exposed through both Z A and Z B motor connector
groups.

The relationship vocabulary, fixture behavior, and lifecycle cleanup are
covered by tests, and the complete repository suite passes.

# Checkpoint 26 — Verified Maestro Motor Connector Information

Date: 2026-10-02

## Classification

IMPLEMENTATION / DECIDED

## What we've done so far

Extended the first Maestro physical-interface representation with verified
motor-connector information.

The reusable Duet 2 Maestro Hardware Definition now contains connector
specification data for the six external stepper-motor connector groups:

- X motor
- Y motor
- Z A motor
- Z B motor
- E0 motor
- E1 motor

The specification records the four-position 2.54 mm board interface, the
Molex KK 254-compatible mating interface family, representative mating
housing and contact part numbers, and the verified motor pin-label
convention.

The installed physical SemanticPorts for motor connectors now carry the
corresponding pin labels and more specific semantic purposes.

## Maestro motor pin representation

Each four-position motor connector is represented using the documented
contact convention:

- Pin 1 → B1
- Pin 2 → B2
- Pin 3 → A1
- Pin 4 → A2

For both Z A and Z B, the resulting physical representation is therefore:

`Z A / Z B → B1, B2, A1, A2`

The Z A and Z B connector groups remain separate physical access-point
groups through `connector_id`.

## Semantic boundary preserved

The reusable connector information is stored as catalog information on the
Duet 2 Maestro Hardware Definition.

The installed connector contacts remain controller-owned SemanticPorts.

The Controller Resource → physical interface relationship remains:

`ControllerResource --exposed_through--> SemanticPort`

No canonical Connector entity was introduced.

No connector housing, contact, terminal, mating-interface, or intermateability
ontology was introduced.

Those remain deferred until broader hardware evidence requires them.

## Files changed

`machine-structure-editor/src/machine_builder/hardware_catalog.py`

Added reusable Maestro motor connector specification data and verified motor
pin labels.

`machine-structure-editor/src/machine_builder/controller_board_fixtures.py`

Applied the verified motor pin labels and semantic purposes to the installed
Maestro physical-interface fixture.

`machine-structure-editor/tests/test_duet_2_maestro_connector_specs.py`

Added focused coverage for the reusable motor connector specifications and
the installed Z A / Z B pin labels.

## Test result

Full repository suite:

`742 passed in 3.84s`

This confirms that the connector-information implementation does not regress
the existing semantic model, relationship model, or Board fixture behavior.

## Current state

The Board workstream now has a working chain from:

`Duet 2 Maestro Hardware Definition`

to:

`installed Controller`

to:

`controller-owned physical SemanticPorts`

to:

`verified motor connector/pin information`

and:

`Controller Resource --exposed_through--> physical SemanticPorts`

The representation remains intentionally incomplete for non-motor Maestro
interfaces.

## WATCH

The current connector specification is reusable catalog information, but
its exact abstraction boundary should continue to be tested against the
next connector families.

The next useful Maestro evidence targets are the non-motor interfaces:
heater, thermistor, endstop, fan, and Z probe.

The objective is to determine whether their connector and pin information can
continue to use the existing structures without introducing unnecessary new
canonical entities.

## Next action

Investigate and model the next verified Maestro connector family, using the
heater or endstop interface as the next test case, and compare its physical
and mating-interface characteristics against the motor-connector
representation.

## Next action

Use this established resource-to-physical-interface pattern to investigate
the next level of real Maestro board detail: verified connector identity,
connector grouping, pin electrical purpose, and mating-interface information,
while preserving the distinction between reusable connector information and
installed physical interfaces.

# Next action

## PROJECT CURRENT STATE UPDATE REQUEST

Why: The first real Board implementation experiment provides project-level evidence that the existing `Controller → controller-owned SemanticPort → connector_id → pin position` structure can represent externally accessible controller interfaces without requiring a new canonical Connector entity. It also reinforces the distinction between Controller Resources and physical access points.

Proposed location: The Controller / Board or controller-resource portion of `PROJECT_CURRENT_STATE.md`.

Proposed content:

```markdown
### Controller / Board physical-interface checkpoint — REINFORCE

The first real documented board implementation experiment, using the Duet 2 Maestro, demonstrated that the existing canonical structure can represent externally accessible controller interfaces without introducing a new canonical Connector entity.

A Controller can own `SemanticPort` objects, with `connector_id` grouping the accessible positions belonging to a physical connector and `pin_id` identifying positions within that group.

The Maestro `Z A` / `Z B` case also reinforces that Controller Resources and physical connectors are distinct concepts and that a single controller resource may ultimately correspond to multiple physical access points.

The experiment did not implement Resource → Physical Interface mapping; that relationship remains the next Board architecture question.