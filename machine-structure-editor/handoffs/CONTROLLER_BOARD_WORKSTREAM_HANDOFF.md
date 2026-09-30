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
Next action

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