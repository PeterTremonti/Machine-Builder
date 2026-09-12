# Machine Builder Implementation Handoff Index

## 1. Purpose

This document is the index for information that must pass from Machine Builder research and architecture into implementation.

The research and implementation work are intentionally separate.

Research establishes:

- concepts;
- architecture;
- terminology;
- standards evidence;
- decisions;
- constraints;
- unresolved questions.

Implementation turns sufficiently mature decisions into:

- code;
- data structures;
- validation;
- UI behavior;
- persistence;
- tests;
- parsers;
- translators.

The purpose of this handoff system is to keep those two activities synchronized without requiring every implementation conversation to reconstruct the entire research history.

---

# 2. Research-to-Implementation Flow

The intended flow is:

```text
Research Evidence
       ↓
Concept / Finding
       ↓
Architecture or Ontology Decision
       ↓
Implementation Requirement
       ↓
Handoff
       ↓
Implementation
       ↓
Test / Observation
       ↓
Research Feedback

An implementation handoff should communicate conclusions that are sufficiently mature for implementation.

It should not turn every unresolved research idea into a coding requirement.

3. Responsibility Boundary
Research / Architecture

Responsible for:

semantic definitions;
architecture;
ontology;
standards interpretation;
machine research;
firmware research;
decisions;
open questions;
architectural constraints.
Implementation

Responsible for:

executable behavior;
UI;
persistence;
code structure;
validation implementation;
tests;
parsers;
firmware translators;
performance;
usability.
Shared Boundary

Some areas require both sides:

canonical model APIs;
validation behavior;
visual semantic interactions;
compatibility;
provenance implementation;
serialization;
firmware mapping.

The research side defines meaning.

The implementation side determines how that meaning is realized in software.

4. Version Streams

Handoffs must identify the research and implementation versions involved.

Current convention:

Research / Architecture:
    R0.x

Ontology:
    O0.x

Implementation:
    v0.x.y

Example:

Research:
    R0.1

Ontology:
    O0.1

Implementation:
    v0.1.0

A handoff may apply to one implementation version while being based on a different research or ontology version.

5. Handoff Status

Handoffs may have the following states:

Draft
Ready
In Implementation
Implemented
Verified
Superseded
Deferred
Rejected
Draft

Still being prepared or reviewed.

Ready

Sufficiently mature for implementation.

In Implementation

The Coder/implementation work has begun.

Implemented

The requested behavior exists in software.

Verified

Tests or implementation review confirm the intended behavior.

Superseded

A newer handoff replaces it.

Deferred

Implementation intentionally postponed.

Rejected

The implementation direction was not adopted.

6. Handoff Numbering

Current handoff identifiers use:

H-001
H-002
H-003
...

Numbers identify handoff records.

Numbers should not be reused.

A superseded handoff remains in history and points to the replacement.

7. Current Implementation Baseline

The implementation is currently:

Project:
    Machine Structure Editor

Repository:
    Machine-Builder

Implementation location:
    machine-structure-editor/

Current implementation version:
    v0.1.0

Current development direction:
    v0.2

The implementation has already established:

a working Python/PySide6 application;
component creation;
component selection;
component movement;
deletion;
undo/redo;
a visual model foundation;
early port/connection behavior.

The implementation is intentionally progressing before the entire long-term ontology is finalized.

8. Current Visual Builder Handoff Set

The current visual-builder implementation is supported by five major documents:

docs/visual-builder/
├── VISUAL_BUILDER_SCOPE.md
├── VISUAL_MODEL.md
├── VISUAL_BUILDER_REQUIREMENTS.md
├── VISUAL_BUILDER_ARCHITECTURE.md
└── VISUAL_BUILDER_CODER_HANDOFF.md

These documents define the current implementation-facing visual-builder requirements.

They should be considered alongside the research ontology and architecture.

9. Handoff H-001 — Canonical Model / Visual Model Separation

Status: Ready / Implemented Direction

Research Basis:

D-001 — Canonical Machine Model
D-004 — Separate Visual Model
D-033 — Visual Builder Is a Consumer of Semantics
Requirement

The visual builder must not become the canonical semantic machine model.

The implementation may maintain visual objects that reference canonical entities.

Required Separation
Canonical:
    machine meaning

Visual:
    node position
    node size
    layout
    selection
    routing
    zoom
    visibility
Implementation Consequence

Moving a node on the canvas must not imply movement of the physical component.

Priority

Critical.

10. Handoff H-002 — Ports Are First-Class Visual Endpoints

Status: In Implementation

Research Basis:

D-016 — Port Is a First-Class Concept
D-017 — Port, Connector, and Pin Are Distinct
D-034 — Compatibility Is Semantic
Requirement

Visual components should expose explicit Ports.

Users should be able to interact with ports rather than connecting entire nodes indiscriminately.

Initial Test Case

The first simple semantic connection prototype may use:

Temperature Sensor
    Temperature Output

connected to:

Temperature Controller
    Temperature Input

This is intentionally an abstract signal example for visual connection testing.

Priority

Critical for visual-builder connection work.

11. Handoff H-003 — Connection Is a Semantic Object

Status: In Implementation

Research Basis:

D-018 — Connection Is Not a Visual Line
D-019 — Physical Connection and Logical Mapping Are Distinct
Requirement

A connection between two ports must have semantic identity independent of its rendered line.

Conceptually:

Port A
   ↓
Semantic Connection
   ↓
Port B

The visual builder may render:

Port A ───────── Port B

but the line is only the presentation.

Priority

Critical.

12. Handoff H-004 — Compatibility Is Semantic

Status: In Implementation

Research Basis:

D-034 — Compatibility Is Semantic
D-016 — Port Is First-Class
Requirement

Connection compatibility should be evaluated from semantic information.

Potential inputs include:

domain;
direction;
signal type;
voltage;
current;
protocol;
interface requirements;
other applicable constraints.
Initial Implementation

The first implementation may use a deliberately small compatibility system.

Example:

Temperature Output
        ↓
Temperature Input

= compatible.

This is a proof of semantic connection behavior, not the final compatibility engine.

Priority

High.

13. Handoff H-005 — Visual Connection Color Is an Output

Status: In Implementation

Requirement

Visual color coding must represent semantic connection state.

It must not become the source of truth.

Conceptually:

Port compatibility
       ↓
Connection state
       ↓
Visual color

Possible future states include:

Compatible
Incompatible
Conditional
Unknown
Disconnected
Error
Priority

High.

14. Handoff H-006 — Canonical Axis Is Not a Motor

Status: Ready

Research Basis:

D-012 — Axis Is Not Motor
SV08 stress case
CoreXY stress case
LowRider stress case
Requirement

Implementation data structures must not enforce:

Axis → exactly one Motor

The model must support:

Many Motors → One Axis
One Motor → Multiple Motion Contributions
Priority

Critical for canonical-model implementation.

15. Handoff H-007 — Coordinate Frames Are Distinct from Canvas Coordinates

Status: Ready

Research Basis:

D-014 — Coordinate Frames Are First-Class
IR3 stress case
Requirement

Implementation must distinguish:

Machine / Engineering Coordinates

from:

Visual Canvas Coordinates
Consequence

A Node's x/y position is not a physical machine position.

Priority

High.

16. Handoff H-008 — Machine Component and Catalog Product Are Distinct

Status: Ready

Research Basis:

D-007 — Machine Component terminology
D-008 — Catalog and Machine Workspace Are Separate
Requirement

The implementation should eventually distinguish:

Catalog Product
Product Version
Machine Component

Catalog selection may suggest or populate candidate information but should not silently create authoritative machine facts.

Priority

High for future hardware database integration.

17. Handoff H-009 — Unknown Information Must Be Representable

Status: Ready

Research Basis:

D-009 — Unknown Is Valid
Requirement

The data model must allow information to remain:

Unknown
Unresolved
Uncertain
Not Yet Investigated

rather than requiring a fabricated value.

Priority

High.

18. Handoff H-010 — Provenance Must Be Preserved

Status: Ready

Research Basis:

D-010 — Provenance Is First-Class
D-011 — Direct / Derived / Inferred
Requirement

Important model information should eventually retain:

Source
Method
Date
Version
Confidence
Evidence
Direct / Derived / Inferred
Implementation Guidance

Do not prematurely build the complete provenance system if the current milestone does not need it.

However, implementation structures should not make provenance impossible to add later.

Priority

High architectural constraint.

19. Handoff H-011 — Function Vocabulary Must Remain Layered

Status: Ready

Requirement

Implementation must not assume:

Function
    = Task
    = Operation
    = Action
    = Procedure

Current working distinctions are:

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
Priority

Medium for current UI work.

High for future canonical model and process implementation.

20. Handoff H-012 — Subsystems Are First-Class

Status: Ready

Research Basis:

D-024 — Subsystem Is a First-Class Concept
D-025 — CFS Is a Subsystem Stress Case
Requirement

A Subsystem may contain:

components;
functions;
resources;
state;
interfaces;
local control;
communication.

A Subsystem must not be represented merely as a visual group.

Priority

High for canonical-model architecture.

21. Handoff H-013 — Firmware Terms Are Not Canonical Concepts

Status: Ready

Research Basis:

D-002
D-030
firmware research index
Requirement

Firmware-specific concepts must be mapped to canonical semantics where appropriate.

Example:

RRF:
    M584

Canonical interpretation:
    motion-resource assignment
Priority

Critical for future parser/generator work.

22. Handoff H-014 — Firmware Mapping Must Support Lossy Translation

Status: Ready

Research Basis:

D-031 — Many-to-Many Firmware Mapping
Open Question Q-060 — Lossy Translation
Requirement

The translator must be capable of identifying:

Unsupported
Not Represented
Ambiguous
Requires Manual Configuration

rather than silently dropping canonical information.

Priority

High for firmware-generation architecture.

23. Handoff H-015 — Runtime State Is Separate from Configuration

Status: Ready

Requirement

Implementation must keep intended setup separate from current machine state.

Example:

Configuration:
    Z maximum travel = 380 mm

Runtime:
    Z position = 120 mm
Priority

Medium for early implementation.

High for future runtime integration.

24. Handoff H-016 — Engineering Evaluations Are Derived

Status: Ready

Requirement

Engineering evaluation results must be treated as derived outputs.

They should eventually retain:

input values;
assumptions;
method;
applicable rule/standard;
result;
provenance.
Possible Results
PASS
WARNING
RECOMMENDATION
INVALID
UNKNOWN
Priority

Medium.

25. Handoff H-017 — Safety Claims Must Not Be Reduced to Booleans

Status: Ready

Requirement

Implementation must not represent safety merely as:

safe = true

or:

ISO compliant = true

Safety information requires context, evidence, evaluation, and applicable standards.

Priority

Medium now; high when safety analysis is implemented.

26. Current Visual Builder Implementation Priority

The current implementation sequence is approximately:

A. Canvas / interaction foundation
        ↓
B. Ports and semantic connections
        ↓
C. Persistence
        ↓
D. Compatibility / validation
        ↓
E. Promega model
        ↓
F. CFS subsystem stress test

This sequence may change as implementation evidence appears.

27. V0.2 Implementation Guidance

The current V0.2 work is primarily concerned with the visual-builder connection architecture.

The implementation should currently favor:

Simple semantic model
       ↓
Clear behavior
       ↓
Tests
       ↓
Generalization

rather than attempting to implement the complete long-term ontology immediately.

The first connection prototype is deliberately small.

Its purpose is to prove that:

ports can exist;
connections can be semantic;
compatibility can be evaluated;
visual feedback can derive from semantic state.
28. What Should Not Be Implemented Yet

The following should not become blockers for the current visual-builder milestone unless implementation evidence requires them:

Full provenance engine
Full safety engine
Complete process ontology
Full controller resource allocation engine
Complete firmware parser framework
Knowledge graph
Full electrical engineering evaluator
Advanced 3D topology
Complete catalog/version model
Formal temporal history

These are architectural directions, not immediate requirements.

29. Implementation-to-Research Feedback

Implementation findings should be returned to research when they expose:

missing concepts;
incorrect distinctions;
relationship cardinality problems;
impossible assumptions;
ambiguous semantics;
useful new abstractions;
unexpected machine behavior.

Example:

Implementation:
    connecting two ports requires more information

        ↓

Research finding:
    Connection needs domain and direction context

        ↓

Ontology update:
    Connection semantics refined

        ↓

New handoff

Implementation feedback is therefore evidence, not merely bug reporting.

30. Handoff Acceptance Criteria

A research finding is usually ready for implementation when:

The concept has a clear working definition.
Important non-equivalences are known.
Relevant relationships are understood sufficiently.
No known stress case directly invalidates it.
Required implementation behavior can be described.
Remaining uncertainty is explicit.
The expected implementation impact is understood.

Not every concept needs complete ontology formalization before implementation can begin.

31. Handoff Review Rule

Before beginning a major implementation task, the implementation conversation should verify:

Research version
Ontology version
Relevant decision(s)
Relevant handoff(s)
Known open questions
Known deferred areas

This prevents an implementation effort from silently using obsolete architectural assumptions.

32. Handoff History

Major handoffs should remain available after implementation.

A completed handoff should record:

Implemented Version
Implementation Date
Relevant Tests
Known Deviations
Follow-up Research

A handoff should not be deleted merely because the code now exists.

The handoff provides historical context for why the implementation behaves as it does.

33. Future Handoff Categories

As the project develops, additional handoff categories are expected:

Canonical Model
Visual Builder
Persistence
Hardware Catalog
Connectivity
Motion / Kinematics
Measurement
Control
Safety
Process / Tooling
Firmware Parsing
Firmware Generation
Engineering Evaluation
Diagnostics
Runtime
3D Visualization
External Integrations

Each category may eventually have its own handoff sequence.

34. Implementation Handoff Checklist

Before issuing a new major handoff, record:

[ ] Handoff ID
[ ] Status
[ ] Research version
[ ] Ontology version
[ ] Implementation target
[ ] Decision references
[ ] Concept definitions
[ ] Required behavior
[ ] Important constraints
[ ] Stress cases
[ ] Known open questions
[ ] Deferred areas
[ ] Expected tests
[ ] Expected implementation impact
35. Current Handoff Priorities

The most important current handoffs are:

H-001  Canonical / Visual Separation
H-002  First-Class Ports
H-003  Semantic Connections
H-004  Semantic Compatibility
H-005  Visual State Derived from Semantic State
H-006  Axis ≠ Motor
H-007  Coordinate Frame ≠ Canvas Coordinate
H-009  Unknown Information
H-010  Provenance
H-013  Firmware Terms ≠ Canonical Concepts

These have the strongest connection to the current visual-builder and canonical-model architecture.

36. Final Principle

The implementation handoff system exists to preserve the boundary:

Research determines what the machine model means.

Implementation determines how the software realizes that meaning.

Neither side should silently redefine the other.

When implementation reveals that the current model is insufficient, the correct response is to return the finding to research, update the architecture or ontology where justified, and issue a new handoff.

The goal is a continuous loop:

Research
   ↓
Decision
   ↓
Handoff
   ↓
Implementation
   ↓
Test
   ↓
Evidence
   ↓
Research

That loop is the mechanism by which Machine Builder can evolve without losing the architectural reasoning behind it.