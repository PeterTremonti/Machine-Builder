# Machine Builder Architectural Decisions

## 1. Purpose

This document records architectural decisions that affect the long-term structure of Machine Builder.

The purpose is to preserve the reasoning behind important choices so that future implementation work does not accidentally reverse a deliberate decision or recreate previously resolved debates.

This document is not a detailed decision history.

Detailed individual decisions may eventually be stored under:

```text
machine-builder-research/decisions/

This file contains the architectural decisions that are important enough to serve as persistent constraints on the overall system.

2. Decision Status

Architectural decisions may have different maturity states.

Proposed
Accepted
Accepted with Conditions
Deferred
Superseded
Rejected

An accepted decision should guide implementation unless new evidence demonstrates that the decision is incorrect.

Reversing an accepted architectural decision should itself be a deliberate decision.

3. Canonical Machine Model Is the Semantic Center
Decision

The canonical machine model is the central semantic representation of a machine.

Rationale

Machine Builder must support multiple representations of the same machine:

physical reality;
visual representation;
firmware configuration;
engineering documentation;
runtime state;
diagnostic information;
process information.

No single one of these should become the permanent semantic authority.

The canonical model provides the common semantic representation from which other representations can be generated or interpreted.

Consequence

Architecture and implementation should avoid treating:

firmware configuration;
UI state;
catalog records;
wiring diagrams;
generated files

as the authoritative machine definition.

Status

Accepted.

4. Firmware Is an Implementation Representation
Decision

Firmware-specific representations are mappings or implementations of canonical machine semantics.

They are not the canonical machine model.

Rationale

Different firmware systems describe similar machine behavior differently.

Examples include:

RepRapFirmware;
Klipper;
Marlin;
FluidNC;
grblHAL;
Smoothieware;
other controller or industrial systems.

A machine should not have to change its fundamental identity merely because the selected firmware changes.

Consequence

Firmware-specific concepts should be retained as source or implementation information while being mapped to canonical concepts.

Status

Accepted.

5. Reverse Interpretation Is a First-Class Direction
Decision

Machine Builder must support both:

Machine → Canonical Model → Firmware

and:

Firmware / Configuration → Canonical Model
Rationale

Existing machines frequently already have firmware configurations.

A useful engineering environment must be able to understand an existing machine rather than only generate a new configuration.

Consequence

Firmware parsers must perform semantic interpretation rather than merely copying configuration values into generic fields.

Status

Accepted.

6. Visual Model Is Separate from Canonical Model
Decision

The visual builder has a separate visual model.

Rationale

Visual concerns include:

node position;
node size;
routing;
zoom;
selection;
layout;
visibility;
interaction state.

These are not machine semantics.

Separating them allows the canonical model to support multiple views without duplicating or corrupting machine information.

Consequence

Moving a component on the canvas must not automatically alter its physical position.

Likewise, a visual connection line must not itself become the canonical connection.

Status

Accepted.

7. Relationship-First Modeling
Decision

Relationships are first-class semantic entities.

Rationale

Machines are defined not only by components but by how those components participate together.

Examples:

Motor → participates in → Axis
Sensor → measures → Measurand
Port → connects to → Port
Controller → owns → Resource
Tool → mounted on → Carriage

A collection of isolated objects would not adequately describe a machine.

Consequence

The model should support typed relationships with relevant properties, provenance, multiplicity, and constraints.

Status

Accepted.

8. Object, Classification, Role, and Aspect Are Distinct
Decision

The model distinguishes:

Object;
Classification;
Role;
Aspect.
Rationale

A physical object has an identity.

Its classification says what kind of thing it is.

Its role says what it does in a particular context.

Its aspect describes an engineering view or structuring dimension.

For example:

Object:
    physical motor

Classification:
    stepper motor

Role:
    Z-axis actuator

Aspects:
    physical
    electrical
    control
    functional

Collapsing these into a single class hierarchy would make reuse and contextual modeling difficult.

Status

Accepted.

9. Machine Component Terminology
Decision

The preferred term for an actual installed or otherwise machine-specific occurrence of a hardware item is:

Machine Component

Rationale

"Part instance" is technically useful in some systems but does not describe the project's preferred engineering meaning.

A catalog product and a physical component installed in a particular machine are different concepts.

Consequence

The architecture should distinguish:

Catalog Product
Product Version
Machine Component
Status

Accepted.

10. Catalog and Workspace Are Separate
Decision

Catalog data must not automatically populate the machine workspace.

Rationale

A catalog describes products that may exist.

The machine model describes what is actually installed or intended for a specific machine.

A catalog suggestion may be useful, but it is not proof.

Consequence

The system may provide candidate matching and suggestions, but assignment to a machine should remain explicit.

Status

Accepted.

11. Unknown Information Is Valid
Decision

Unknown or unresolved information must be representable.

Rationale

Reverse engineering and machine construction frequently begin with incomplete information.

Forcing every field to contain a value encourages:

guesses;
false precision;
accidental assumptions;
hidden uncertainty.
Consequence

The model must distinguish missing or unknown information from a verified value.

Status

Accepted.

12. Provenance Is First-Class
Decision

Important facts and relationships should carry provenance.

Rationale

Machine information may come from:

manuals;
datasheets;
measurements;
firmware;
user observations;
engineering calculations;
inferred relationships;
standards.

The source affects confidence and interpretation.

Consequence

The model should eventually be able to answer:

Where did this information come from?

and:

How was this value established?

Status

Accepted.

13. Direct, Derived, and Inferred Information Must Be Distinguished
Decision

Information should distinguish at least:

direct/documented or observed information;
derived information;
inferred information.
Rationale

These categories have different levels of certainty and should be handled differently by engineering evaluation and conflict resolution.

Example:

Direct:
    steps/revolution = 200

Derived:
    steps/mm = 80

Inferred:
    this motor is probably the X-axis motor
Status

Accepted.

14. Physical, Logical, Functional, and Visual Structures Remain Separate
Decision

The architecture explicitly distinguishes:

physical structure;
logical structure;
functional structure;
visual structure.
Rationale

A single machine relationship may have different interpretations in different engineering domains.

For example:

Physical:
    wire connects two pins

Logical:
    signal travels between endpoints

Functional:
    signal contributes to heater control

Visual:
    line is drawn between nodes

These are related but not identical.

Consequence

A generic visual edge or generic object hierarchy must not be used as a substitute for semantic relationships.

Status

Accepted.

15. Port Is a First-Class Concept
Decision

Ports are first-class endpoints of connectivity.

Rationale

Machines require connectivity across many domains:

electrical;
communication;
mechanical;
material;
fluid;
logical;
signal.

A component may expose multiple interfaces that cannot be adequately described by treating the whole component as one connection point.

Consequence

Ports should support domain-specific semantics and compatibility evaluation.

Status

Accepted.

16. Port, Connector, and Pin Are Distinct
Decision

Port, connector, and pin are separate concepts.

Rationale

A connector is a physical interface structure.

A pin is a position/contact within that connector.

A port is a semantic interface exposed by a component.

They may correspond to one another, but they are not interchangeable.

Consequence

The model must be able to express relationships between them rather than treating them as synonyms.

Status

Accepted.

17. Connection Is Distinct from Visual Line
Decision

A semantic Connection is distinct from the visual line used to display it.

Rationale

The same connection may be displayed:

as a line;
as a bundled harness;
as a wiring diagram;
as a port highlight;
in a 3D routing view.

Conversely, a visual line may represent something other than a physical wire.

Consequence

The canonical model owns the connection semantics.

The visual model owns the rendering.

Status

Accepted.

18. Physical Connection and Logical Mapping Are Separate
Decision

Physical topology and logical mapping are separate concepts.

Rationale

A physical connection can exist without a particular logical signal interpretation.

Conversely, a logical relationship may span multiple physical connections.

Example:

Physical:
    controller pin → wire → sensor connector

Logical:
    temperature measurement → control function
Status

Accepted.

19. Axis Is Not Motor
Decision

Axis and motor are distinct concepts.

Rationale

Machines frequently violate a one-axis/one-motor assumption.

Examples include:

CoreXY;
multiple Z motors;
autosquaring;
coupled motion;
rotary axes;
machines where several actuators jointly produce one logical motion.
Consequence

Canonical motion modeling must support many-to-many relationships between motion semantics and actuators.

Status

Accepted.

20. Joint, Actuator, Motor, and Drive Are Distinct
Decision

The following concepts remain separate:

Joint
Actuator
Motor
Drive
Rationale

They represent different engineering layers.

A motor is an electromechanical device.

An actuator produces physical action.

A joint describes constrained relative motion.

A drive controls a motor or actuator.

Collapsing these into one "motor" object would make many real machines impossible to model correctly.

Status

Accepted.

21. CoordinateFrame Is First-Class
Decision

Coordinate frames are first-class modeled entities.

Rationale

Modern machines can contain multiple relevant coordinate systems.

Examples:

machine;
work;
tool;
object;
camera;
task;
rotary;
subsystem-specific frames.
Consequence

Coordinate transformations should be represented explicitly.

Canvas coordinates remain separate.

Status

Accepted.

22. Sensor Is Not Measurement Result
Decision

Sensors and measurement results are distinct concepts.

Rationale

A sensor produces or participates in measurement.

A measurement result is information about a measurand.

The same measurement may be consumed by several functions.

Conceptual Flow
Sensor
   ↓
Measurement
   ↓
Measurement Result
   ↓
Consumers

Consumers may include:

control;
diagnostics;
calibration;
logging;
display;
safety.
Status

Accepted.

23. Function Vocabulary Is Layered
Decision

Function, Capability, Task, Operation, Action, Procedure, Control Function, and Safety Function are distinct concepts.

Rationale

These words have different meanings across systems engineering, manufacturing, robotics, PLCs, and safety standards.

Treating them as synonyms would cause semantic ambiguity.

Current working distinctions
Capability
    ability possessed by a system

Function
    defined machine/subsystem behavior or service

Task
    intended body of work

Operation
    bounded executable work unit

Action
    discrete executable behavior/change

Procedure
    specified way of carrying out activity

Control Function
    function used to regulate machine behavior

Safety Function
    function required for safe behavior/risk reduction
Consequence

Function should not become a universal parent class for all of these concepts.

Status

Accepted.

24. Subsystem Is a First-Class Architectural Pattern
Decision

A subsystem may contain components, functions, resources, state, interfaces, and local control.

Rationale

Real machines frequently contain autonomous or semi-autonomous subsystems.

Examples include:

material systems;
tool changers;
toolheads;
external controllers;
CFS-type material systems;
safety systems.
Consequence

Subsystems must not be modeled merely as a group of visually enclosed components.

A subsystem has semantic boundaries and interfaces.

Status

Accepted.

25. CFS Is a Subsystem Stress Case
Decision

The Creality CFS is treated as a meaningful subsystem architecture test.

Rationale

The CFS demonstrates:

multiple motors;
multiple sensors;
material paths;
local control;
buffering;
communication;
interactions with the larger machine.

Modeling it as a single "feeder" would lose important machine semantics.

Consequence

Subsystem modeling must support internal structure and external interfaces.

Status

Accepted.

26. Runtime State Is Separate from Configuration
Decision

Runtime state and configuration are distinct.

Rationale

A configuration value describes intended setup.

Runtime state describes current machine condition.

Examples:

Configuration:
    maximum temperature = 250 °C

Runtime:
    current temperature = 205 °C
Consequence

Runtime integration must not overwrite configuration data.

Status

Accepted.

27. Engineering Evaluation Is Separate from Canonical Facts
Decision

Engineering evaluation results are derived assessments rather than permanent machine facts.

Rationale

A result depends on:

current inputs;
assumptions;
calculation method;
standards;
context;
version.

A later model change may invalidate a previous result.

Consequence

Evaluation results should preserve lineage and be recalculable.

Status

Accepted.

28. Safety Is an Engineering Layer, Not a Boolean Property
Decision

Safety information must be represented through safety functions, hazards, risks, requirements, implementations, validation, and evidence rather than simple compliance flags.

Rationale

Safety standards require contextual engineering analysis.

For example:

ISO 13849 compliant = true

is not enough information to establish a valid safety claim.

Consequence

Safety conclusions must retain:

applicable standard;
edition/version;
analysis;
assumptions;
evidence;
validation state.
Status

Accepted.

29. Standards Are Evidence and Constraints
Decision

Standards should be referenced as authoritative external sources rather than converted into simplistic machine properties.

Rationale

Standards provide:

terminology;
structural concepts;
requirements;
engineering methods;
safety concepts.

A machine may be assessed against a standard without the standard becoming a boolean field.

Consequence

Standards references should include edition/version and applicability where relevant.

Status

Accepted.

30. Knowledge Graph Complements the Canonical Model
Decision

A future knowledge graph may complement the canonical model but does not replace it by default.

Rationale

Graph technologies may be useful for:

relationship traversal;
external knowledge;
semantic querying;
linked evidence.

However, adopting a graph implementation does not automatically define the project's ontology.

Consequence

The ontology remains an architectural concept independent of the eventual storage/query technology.

Status

Accepted.

31. No Premature Database Schema
Decision

The project will not freeze a detailed database schema before the ontology and relationship semantics are sufficiently mature.

Rationale

A premature schema would encourage implementation-driven semantics.

The project is still discovering:

relationships;
cardinalities;
provenance requirements;
context handling;
versioning;
subsystem structure.
Consequence

Current research should prioritize semantic correctness over database implementation details.

Status

Accepted.

32. No Premature Universal Graph
Decision

The project should not attempt to model everything as one generic graph relationship.

Rationale

Although relationships are fundamental, different relationship types have different semantics.

For example:

contains
connects_to
measures
drives
participates_in
mounted_on
derived_from
implements
maps_to

are not interchangeable.

Consequence

The model should have typed relationships with domain-specific constraints.

Status

Accepted.

33. Firmware Independence Is an Architectural Requirement
Decision

The canonical architecture must remain firmware-independent.

Rationale

The intended system must support multiple firmware and control ecosystems.

It must also represent machines that are not controlled by hobbyist 3D-printer firmware.

Consequence

Firmware modules operate as translators, interpreters, or implementation providers around the canonical model.

Status

Accepted.

34. Standards Research Is Targeted
Decision

The project will not attempt to discover every potentially relevant standard before progressing.

Rationale

The standards landscape is too broad and continuously evolving.

Broad standards hunting produces diminishing returns.

Current approach
Establish the core architecture.
Identify a genuinely new semantic domain.
Perform a targeted standards scan.
Record relevant evidence.
Adopt useful distinctions.
Continue building.
Revisit standards when new evidence requires it.
Consequence

New standards may be incorporated opportunistically as the architecture encounters new domains.

Status

Accepted.

35. Stress Cases Drive Generalization
Decision

Architectural concepts should be tested against machines that violate simple assumptions.

Rationale

A model that works only for a conventional Cartesian printer is not sufficient for the project's goals.

Important stress cases include:

CoreXY;
multiple actuators per axis;
belt printers;
tool changers;
IDEX;
CFS;
rotary axes;
closed-loop systems;
CNC;
industrial machines.
Consequence

New exceptions should prompt investigation of the underlying semantic model before adding machine-specific hacks.

Status

Accepted.

36. Research, Ontology, and Implementation Have Independent Versions
Decision

Research, ontology, and implementation use separate version streams.

Current convention
Research / Architecture:
    R0.x

Ontology:
    O0.x

Implementation:
    v0.x.y
Rationale

The three areas mature at different rates.

A software release does not imply a corresponding ontology revision.

Status

Accepted.

37. Research-to-Implementation Handoffs Are Explicit
Decision

Major research conclusions should reach implementation through explicit handoff documents or decisions.

Rationale

The research and implementation work occur in separate conversational and repository contexts.

Without explicit handoffs, implementation may operate on stale assumptions.

Consequence

Research handoffs should identify:

relevant concept;
decision;
version;
implementation impact;
unresolved issues;
affected tests.
Status

Accepted.

38. Visual Builder Is a Consumer of Semantics
Decision

The visual builder is a primary interface to the machine model, but not the semantic authority.

Rationale

The application needs visual editing because machine architecture is easier to understand spatially.

However, a canvas cannot be allowed to define the ontology.

Consequence

Visual interactions should generate semantic mutations rather than storing machine meaning only in UI objects.

Status

Accepted.

39. Compatibility Is Semantic
Decision

Connection compatibility is determined from semantic properties, not visual appearance.

Rationale

A port may be visually similar to another port while being electrically, logically, mechanically, or procedurally incompatible.

Consequence

Compatibility evaluation must consider relevant properties such as:

domain;
direction;
voltage;
current;
protocol;
interface type;
mechanical compatibility;
constraints.
Status

Accepted.

40. Architecture Favors General Concepts Over Special Cases
Decision

When a new machine exposes a modeling problem, first investigate whether the problem reveals a missing general concept.

Rationale

Repeated special cases cause the architecture to become a collection of machine-specific exceptions.

The desired direction is:

New machine
    ↓
Existing general concepts
    +
New evidence

rather than:

New machine
    ↓
Special case
Consequence

Stress cases are treated as architectural tests rather than isolated feature requests.

Status

Accepted.

41. Architecture Must Preserve Information
Decision

Transformations should avoid throwing away meaningful semantic information.

Rationale

A generated firmware configuration may contain less information than the full canonical machine model.

For example:

Canonical:
    motor identity
    role
    mechanical connection
    current
    controller resource
    provenance
    calibration

Firmware:
    driver assignment
    current
    motion scale

The firmware representation is therefore lossy relative to the canonical model.

The architecture must recognize this.

Consequence

Round-tripping is not expected to preserve every piece of information through every representation.

Information loss should be understood rather than accidental.

Status

Accepted.

42. Round-Trip Interpretation Is an Engineering Goal
Decision

Whenever practical, a machine represented in canonical form should be translatable into a supported firmware representation and later interpreted back into canonical semantics.

Rationale

This provides a powerful consistency test.

Example:

Canonical
   ↓
Generated Firmware
   ↓
Parsed Firmware
   ↓
Canonical Interpretation

The resulting model may not be byte-for-byte identical, but important semantics should remain recoverable.

Consequence

Round-trip tests should eventually become part of firmware translator validation.

Status

Accepted.

43. Unknown Is Preferable to False Certainty
Decision

When the system cannot establish a semantic conclusion with sufficient confidence, it should report uncertainty rather than manufacture certainty.

Rationale

The project is intended for real machine engineering.

False certainty can cause incorrect:

wiring;
motion configuration;
firmware generation;
component selection;
safety conclusions.
Consequence

Evaluation and UI should expose uncertainty.

Status

Accepted.

44. Current Architectural Direction

The current architectural structure can be summarized as:

                        EXTERNAL REALITY
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
              Evidence Sources      Physical Machine
                    │                   │
                    └─────────┬─────────┘
                              ▼
                       Interpretation
                              │
                              ▼
                 ┌────────────────────────┐
                 │  CANONICAL MACHINE     │
                 │        MODEL           │
                 │                        │
                 │ Objects                │
                 │ Classifications        │
                 │ Roles                  │
                 │ Aspects                │
                 │ Properties             │
                 │ Relationships          │
                 │ State                  │
                 │ Functions              │
                 │ Interfaces / Ports     │
                 │ Components / Subsystems│
                 │ Coordinate Frames      │
                 │ Provenance             │
                 └───────────┬────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
         Engineering      Visual          Translation
          / Analysis      Model             Layer
              │              │              │
              ▼              ▼              ▼
        Evaluations        UI          Firmware / Tools

This is the current architectural foundation for continued ontology development and implementation.

45. Decision Review Rule

Architectural decisions should be revisited when:

new evidence directly contradicts the decision;
a stress case demonstrates that the abstraction is insufficient;
an external standard establishes a materially better distinction;
implementation reveals an impossible or harmful constraint;
two accepted decisions become mutually inconsistent.

A decision should not be changed merely because a simpler implementation would be easier.

The long-term goal is semantic correctness, extensibility, and explainability.

46. Final Architectural Principle

The most important architectural rule is:

Model what the machine means before modeling how a particular software system happens to represent it.

Firmware syntax, UI layout, database structure, and implementation classes are all downstream representations.

The canonical machine model should remain the stable semantic foundation connecting them.