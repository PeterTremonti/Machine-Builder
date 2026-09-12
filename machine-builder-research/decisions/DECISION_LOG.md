# Machine Builder Decision Log

## 1. Purpose

This document is the central index of important Machine Builder research and architecture decisions.

Its purpose is to preserve decisions that affect the direction of the project so they do not have to be rediscovered in later conversations.

This is an index and concise record.

Detailed reasoning may be stored in individual decision files under:

```text
machine-builder-research/decisions/decisions/

The ontology and architecture documents should describe the current result.

This document preserves the fact that a decision was made, what it established, and whether it remains current.

2. Decision Status

The project uses the following decision states:

Proposed
Accepted
Accepted with Conditions
Deferred
Superseded
Rejected
Proposed

A possible direction under consideration.

Accepted

The decision is currently part of the project architecture.

Accepted with Conditions

The decision is accepted within explicitly defined limitations.

Deferred

The issue is recognized but intentionally not resolved yet.

Superseded

A newer decision replaces the earlier one.

Rejected

The direction was considered and intentionally not adopted.

3. Decision Numbering

Current decision identifiers use:

D-001
D-002
D-003
...

The number identifies the decision record, not its priority.

Decision numbers should not be reused.

If a decision is superseded, retain the original number and point to the replacement decision.

4. Core Architecture Decisions
D-001 — Canonical Machine Model Is the Semantic Center

Status: Accepted

Decision

The canonical machine model is the semantic center of Machine Builder.

Reason

The project must represent the machine independently of:

firmware;
visual layout;
storage format;
catalog system;
generated configuration;
runtime interface.
Consequence

Other representations translate to and from canonical machine semantics.

Related
architecture/ARCHITECTURE_OVERVIEW.md
architecture/SYSTEM_BOUNDARIES.md
architecture/DATA_FLOW.md
architecture/ARCHITECTURAL_DECISIONS.md
D-002 — Firmware Is an Implementation Representation

Status: Accepted

Decision

Firmware-specific configurations and concepts are implementation representations of the machine, not the canonical ontology.

Reason

Different firmware systems represent the same machine differently.

Consequence

Firmware-specific modules perform interpretation and translation.

Related
Firmware research
Firmware mapping architecture
Reverse parsing
Configuration generation
D-003 — Reverse Firmware Interpretation Is Required

Status: Accepted

Decision

Machine Builder must support:

Firmware / Configuration
        ↓
Semantic Interpretation
        ↓
Canonical Machine Model

in addition to:

Canonical Machine Model
        ↓
Firmware Representation
Reason

The project must understand existing machines rather than only create new firmware configurations.

D-004 — Visual Model Is Separate from Canonical Model

Status: Accepted

Decision

The visual builder has a separate visual model.

Reason

Canvas position, node size, routing, selection, zoom, and other UI state are not machine semantics.

Consequence

Visual interactions become semantic model mutations where appropriate.

Related
Visual Builder documentation
architecture/DATA_FLOW.md
D-005 — Relationships Are First-Class

Status: Accepted

Decision

Typed semantic relationships are first-class ontology elements.

Reason

The machine is defined by how its objects participate together.

Consequence

The ontology must preserve distinctions such as:

contains
mounted_on
measures
participates_in
implements
maps_to
derived_from

rather than collapsing everything into a generic connection.

5. Ontology Foundation Decisions
D-006 — Object, Classification, Role, and Aspect Are Distinct

Status: Accepted

Decision

The ontology distinguishes:

Object
Classification
Role
Aspect
Reason

These concepts represent different dimensions of machine meaning.

Example:

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
Consequence

A rigid inheritance hierarchy is not the primary ontology architecture.

D-007 — Machine Component Is Preferred Terminology

Status: Accepted

Decision

The project uses Machine Component for an actual machine-specific occurrence of a hardware entity.

Reason

The term is clearer for the intended engineering context than "part instance."

Consequence

Catalog products and actual machine components remain separate concepts.

D-008 — Catalog and Machine Workspace Are Separate

Status: Accepted

Decision

Catalog information does not automatically become machine information.

Reason

A catalog says what a product is.

The machine model says what is installed, intended, or observed in a particular machine.

Consequence

Catalog matching may suggest a candidate component but should not silently instantiate it.

D-009 — Unknown Is a Valid State of Knowledge

Status: Accepted

Decision

Unknown, unresolved, and uncertain information must remain representable.

Reason

Machine reverse engineering frequently begins with incomplete information.

Consequence

The system must not manufacture certainty simply to populate fields.

D-010 — Provenance Is First-Class

Status: Accepted

Decision

Important facts and relationships should retain provenance.

Reason

Information may originate from:

documentation;
measurements;
observations;
firmware;
standards;
calculations;
inference;
user statements.
Consequence

The system must eventually be able to explain where information came from and how it was established.

D-011 — Direct, Derived, and Inferred Information Are Distinct

Status: Accepted

Decision

The ontology distinguishes at least:

Direct / Documented / Observed
Derived
Inferred
Reason

These forms of information have different evidentiary meanings.

Consequence

Derived and inferred information must retain appropriate lineage and confidence.

6. Physical and Functional Modeling Decisions
D-012 — Axis Is Not Motor

Status: Accepted

Decision

Axis and Motor are separate ontology concepts.

Reason

Real machines use:

multiple motors per axis;
coupled motors;
kinematic transformations;
motors contributing to multiple logical motions.
Consequence

Motion modeling must allow many-to-many relationships.

D-013 — Joint, Actuator, Motor, and Drive Are Distinct

Status: Accepted

Decision

The concepts remain distinct.

Reason

They represent different physical and control layers.

Consequence

The model can represent mechanisms that cannot be expressed as simple motor-to-axis relationships.

D-014 — Coordinate Frames Are First-Class

Status: Accepted

Decision

CoordinateFrame is a first-class concept.

Reason

Machine Builder must eventually support:

non-Cartesian systems;
rotary axes;
tool offsets;
robotics;
belt printers;
multi-axis machines.
Consequence

Physical coordinates and canvas coordinates remain separate.

D-015 — Physical, Logical, Functional, and Visual Structures Are Distinct

Status: Accepted

Decision

These structures remain separate architectural concerns.

Reason

A wire, signal, machine function, and visual line can represent related information without being the same thing.

Consequence

One representation cannot silently stand in for another.

7. Interface and Connectivity Decisions
D-016 — Port Is a First-Class Concept

Status: Accepted

Decision

Ports are first-class semantic interface endpoints.

Reason

Components can expose multiple interfaces across different domains.

Consequence

Ports become the primary endpoints for future compatibility and connection modeling.

D-017 — Port, Connector, and Pin Are Distinct

Status: Accepted

Decision

The ontology does not treat Port, Connector, and Pin as synonyms.

Reason

They exist at different semantic/physical abstraction levels.

D-018 — Connection Is Not a Visual Line

Status: Accepted

Decision

A semantic Connection is distinct from its visual representation.

Reason

Connections may later be displayed as:

lines;
harnesses;
wiring diagrams;
3D paths;
highlights.
Consequence

The visual builder renders semantic connections rather than owning them.

D-019 — Physical Connection and Logical Mapping Are Distinct

Status: Accepted

Decision

Physical topology is modeled separately from logical information mapping.

Reason

One logical signal may cross several physical elements, while a physical path may exist without one specific logical interpretation.

8. Measurement and Control Decisions
D-020 — Sensor Is Not Measurement Result

Status: Accepted

Decision

Sensor and Measurement Result remain separate concepts.

Reason

Measurement information has its own:

value;
unit;
uncertainty;
time;
method;
provenance.
Consequence

The same result can feed multiple consumers.

D-021 — Feedback Is a Use of Measurement Information

Status: Accepted

Decision

Feedback is treated as a control relationship rather than a Sensor subtype.

Reason

The same sensor measurement may be used for:

control;
diagnostics;
calibration;
safety;
logging.
D-022 — Function Vocabulary Is Layered

Status: Accepted

Decision

The following concepts are distinct:

Capability
Function
Task
Process
Operation
Action
Procedure
Control Function
Safety Function
Control Loop
Reason

These terms have different meanings across engineering domains.

Consequence

Function is not a universal parent for every executable or procedural concept.

D-023 — Control Is Modeled as a Relationship Structure

Status: Accepted

Decision

Control should be capable of representing:

Setpoint
→ Control Function
→ Control Output
→ Physical System
→ Measurement
→ Feedback
→ Control Function
Reason

Control behavior cannot be reduced to firmware commands or motor objects.

9. Subsystem Decisions
D-024 — Subsystem Is a First-Class Concept

Status: Accepted

Decision

A Subsystem may contain:

objects;
functions;
capabilities;
resources;
state;
interfaces;
local control.
Reason

Real machines contain complex modules that cannot be represented as single components.

D-025 — CFS Is a Subsystem Stress Case

Status: Accepted

Decision

The Creality CFS is treated as a subsystem-level architecture test.

Reason

It demonstrates:

multiple actuators;
multiple sensors;
material paths;
buffering;
local control;
communication;
interaction with the larger machine.
Consequence

CFS modeling must preserve internal and external structure.

10. Safety Decisions
D-026 — Safety Is an Engineering Layer

Status: Accepted

Decision

Safety is modeled through engineering concepts rather than a simple compliance flag.

Current structure
Hazard
↓
Risk
↓
Risk Reduction Requirement
↓
Safety Function
↓
Safety-Related Implementation
↓
Validation
↓
Safe State
D-027 — Standards References Require Context

Status: Accepted

Decision

Safety and other standards references should preserve:

standard;
edition/version;
applicability;
evidence;
evaluation context.
Reason

A property such as:

ISO 13849 = true

is not a sufficient engineering result.

11. Engineering Evaluation Decisions
D-028 — Evaluation Results Are Derived

Status: Accepted

Decision

Engineering evaluations are derived conclusions rather than permanent canonical facts.

Reason

A result depends on:

inputs;
assumptions;
method;
applicable requirements;
current model state.
Consequence

Results must retain lineage and may become stale after model changes.

D-029 — Uncertainty Must Be Visible

Status: Accepted

Decision

Engineering evaluation should support results such as:

PASS
WARNING
RECOMMENDATION
INVALID
UNKNOWN
Reason

Not every machine fact is sufficiently known for a binary decision.

12. Firmware Decisions
D-030 — Firmware Terms Do Not Become Canonical Concepts

Status: Accepted

Decision

Firmware-specific terms remain in the firmware representation unless their underlying semantics are mapped to a canonical concept.

Example
RRF:
    M584
    M92

may map to canonical concepts such as:

axis/resource assignment
motion scale

but the firmware command names do not define the ontology.

D-031 — Firmware Mapping May Be Many-to-Many

Status: Accepted

Decision

The firmware mapping layer must support:

one-to-one;
one-to-many;
many-to-one;
conditional;
calculated;
version-specific mappings.
Reason

Canonical semantics and firmware syntax rarely have guaranteed one-to-one correspondence.

D-032 — Round-Trip Semantic Testing Is a Goal

Status: Accepted

Decision

Where practical:

Canonical Model
    ↓
Generated Firmware
    ↓
Parsed Firmware
    ↓
Canonical Interpretation

should preserve important semantics.

Consequence

Round-trip tests should eventually be part of firmware translator validation.

13. Visual Builder Decisions
D-033 — Visual Builder Is a Consumer of Semantics

Status: Accepted

Decision

The visual builder is an interface to the canonical model, not the canonical model itself.

Consequence

UI state must remain separate from machine semantics.

D-034 — Compatibility Is Semantic

Status: Accepted

Decision

Connection compatibility is calculated from semantic properties.

Potential inputs
Domain
Direction
Voltage
Current
Protocol
Interface Type
Mechanical Constraints
Other Domain Rules
Consequence

Visual color is an output of compatibility evaluation, not the source of truth.

14. Research Process Decisions
D-035 — Standards Research Is Targeted

Status: Accepted

Decision

The project will not attempt to discover every potentially relevant standard before continuing implementation.

Process
New semantic domain
        ↓
Targeted standards scan
        ↓
Relevant evidence
        ↓
Ontology update if justified
Reason

Broad standards hunting provides diminishing returns.

D-036 — Stress Cases Drive Generalization

Status: Accepted

Decision

Architectural concepts are tested against machines that violate simple assumptions.

Important cases
Promega
SV08
LowRider
IR3
CFS
CoreXY
IDEX
Tool Changers
Closed-Loop Machines
CNC
Industrial Machines
Consequence

Special cases should prompt investigation of the general ontology before implementation-specific hacks are introduced.

D-037 — Research, Ontology, and Implementation Use Independent Versions

Status: Accepted

Convention
Research / Architecture:
    R0.x

Ontology:
    O0.x

Implementation:
    v0.x.y
Reason

These areas do not mature on the same schedule.

D-038 — Research-to-Implementation Handoffs Are Explicit

Status: Accepted

Decision

Important research conclusions should reach implementation through explicit handoffs.

Handoffs should identify
relevant concepts;
accepted decisions;
versions;
implementation consequences;
unresolved questions;
affected tests.
15. Deferred Decisions
D-039 — Exact Database Schema

Status: Deferred

Decision

Do not freeze a detailed persistence schema until ontology semantics and relationship constraints are sufficiently mature.

Reason

A premature schema could distort the ontology to match implementation convenience.

D-040 — Knowledge Graph as Canonical Storage

Status: Deferred

Decision

Do not currently make a Knowledge Graph the authoritative canonical storage model.

Reason

Graph representation may complement the canonical model, but storage technology should not define semantic architecture prematurely.

D-041 — Universal Flow Concept

Status: Deferred

Decision

Do not yet make Flow a universal machine ontology concept.

Reason

Flow could mean:

material flow;
fluid flow;
electrical energy;
signal;
communication;
other movement.

The semantic scope is currently too broad.

D-042 — Universal Signal Concept

Status: Deferred

Decision

Do not yet make Signal a universal top-level concept.

Reason

Signal has substantially different meanings across:

electrical engineering;
communications;
control;
logical systems;
firmware.
D-043 — Universal Channel Concept

Status: Deferred

Decision

Do not yet define Channel as a universal ontology concept.

Reason

The term can mean:

controller resource;
communications path;
analog input;
logical information path;
physical connection.
D-044 — Universal Resource Concept

Status: Deferred

Decision

Resource remains useful in specific domains, especially controller resources, but should not become an unrestricted universal abstraction yet.

D-045 — Universal Interface Concept

Status: Deferred

Decision

Do not yet collapse Port, Connector, Pin, protocol interface, API interface, and other uses under one universal Interface concept.

Reason

The distinctions may be important across domains.

D-046 — Universal State Model

Status: Deferred

Decision

State, Mode, Fault, Operating State, Configuration State, and related concepts require further refinement before being unified.

16. Rejected or Avoided Directions
D-047 — Firmware-Centric Canonical Model

Status: Rejected

Decision

Machine Builder will not define the machine primarily as a firmware configuration.

Reason

This would prevent the intended support for:

multiple firmware ecosystems;
firmware-independent machine architecture;
reverse engineering;
machines outside the 3D-printer firmware ecosystem.
D-048 — Motor-Centric Machine Ontology

Status: Rejected

Decision

The architecture will not define machine motion primarily as motors mapped one-to-one to axes.

Reason

CoreXY, multiple-Z systems, CNC mechanisms, robotics, and other machines invalidate the assumption.

D-049 — Visual-Canvas-Centric Machine Model

Status: Rejected

Decision

The canvas will not be the canonical machine representation.

Reason

Visual position and layout are presentation concerns.

D-050 — Automatic Catalog Instantiation

Status: Rejected

Decision

Selecting or finding a catalog product will not silently create authoritative machine facts.

Reason

Catalog matching is evidence or candidate information, not necessarily proof of installation.

D-051 — Generic related_to as the Canonical Relationship

Status: Rejected

Decision

The canonical model will not rely on a single generic relationship for all semantics.

Reason

Meaningful engineering distinctions require typed relationships.

17. Decision Dependencies

Some decisions depend on others.

D-001 Canonical Model
    ↓
D-005 Typed Relationships
    ↓
D-006 Object / Classification / Role / Aspect
    ↓
D-012 Motion Distinctions
    ↓
D-016 Ports
    ↓
D-030 Firmware Mapping

Another dependency chain:

D-009 Unknown
    ↓
D-010 Provenance
    ↓
D-011 Direct / Derived / Inferred
    ↓
D-028 Evaluation Results

And:

D-004 Visual Model Separation
    ↓
D-018 Connection ≠ Visual Line
    ↓
D-034 Semantic Compatibility

These dependencies help explain why apparently small implementation decisions may rely on broader architectural choices.

18. Decision Review Triggers

An accepted decision should be revisited when:

new evidence directly contradicts it;
a stress case exposes a fundamental limitation;
an applicable standard establishes a materially better distinction;
implementation demonstrates that the abstraction is impossible or harmful;
two accepted decisions become contradictory.

A decision should not be reversed merely because a temporary implementation shortcut would be easier.

19. Decision History Rule

When an important accepted decision changes:

Do not silently edit away the old decision.
Mark the old decision as Superseded.
Create a new decision number.
Explain what changed.
Record the reason.
Update affected architecture/ontology documents.
Update implementation handoffs if necessary.

This keeps the evolution of the project understandable.

20. Current Decision Set Summary

The current architectural direction can be summarized as:

Canonical Machine Model
        │
        ├── Objects
        ├── Classifications
        ├── Roles
        ├── Aspects
        ├── Properties
        ├── Relationships
        └── Provenance
                │
        ┌───────┼────────┬────────┬────────┐
        ▼       ▼        ▼        ▼        ▼
     Motion  Control  Process  Safety  Connectivity
        │       │        │        │        │
        └───────┴────────┴────────┴────────┘
                        │
                        ▼
                 Engineering Analysis
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
         Visual Model        Firmware Mapping

The key decisions are designed to keep these domains connected without collapsing them into one another.

21. Current Highest-Priority Decisions for Implementation

For implementation work currently underway, the most important accepted decisions are:

D-001  Canonical Machine Model
D-004  Separate Visual Model
D-005  First-Class Relationships
D-006  Object / Classification / Role / Aspect
D-009  Unknown Information
D-010  Provenance
D-012  Axis ≠ Motor
D-014  Coordinate Frames
D-016  Ports
D-018  Connection ≠ Visual Line
D-019  Physical ≠ Logical Mapping
D-020  Sensor ≠ Measurement Result
D-022  Layered Function Vocabulary
D-024  Subsystems
D-030  Firmware Mapping
D-034  Semantic Compatibility

These should be considered when introducing new implementation concepts.

22. Final Decision Principle

The project's decision philosophy is:

Prefer a general semantic distinction that explains multiple machines over a convenient special case that explains only one.

A new implementation problem should therefore trigger the question:

What does this teach us about the machine model?

rather than:

How can we make this particular case work?

The architecture should evolve from evidence, engineering meaning, standards, and stress cases rather than from UI convenience alone.