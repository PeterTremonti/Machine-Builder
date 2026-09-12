# Machine Builder — Research & Architecture Roadmap

## Purpose

This roadmap tracks the research and architecture work independently from software implementation versions.

Research and ontology milestones are allowed to advance at a different pace from implementation releases.

Implementation versions use:

    v0.1.0
    v0.2.0
    ...

Research / architecture versions use:

    R0.1
    R0.2
    ...

Ontology versions use:

    O0.1
    O0.2
    ...

---

# 1. Current Status

## Implementation

Machine Structure Editor:

    v0.1.0

The visual implementation has established a working foundation for:

- visual nodes
- explicit ports
- port-to-port connections
- connection compatibility feedback
- selection
- deletion
- undo/redo
- multi-selection
- component palette
- automated tests

The visual builder is continuing into its next implementation stage.

## Research / Architecture

The research side is completing the foundational semantic model required for future Machine Builder development.

Current research milestone:

    R0.1 — foundational architecture and ontology consolidation

Current ontology milestone:

    O0.1 — first canonical semantic ontology

---

# 2. Roadmap Principles

The roadmap is a living planning document.

Research may change planned work.

New information should not automatically reopen completed decisions.

When a new discovery affects the architecture:

1. determine whether the existing decision is actually invalid
2. determine whether the discovery is merely an extension
3. record the result in the decision log
4. update the roadmap only if necessary

Use the following categories:

- Foundation — required for the current architecture
- Next — directly supports the next milestone
- Later — important but not currently blocking
- Deferred — intentionally postponed
- Research Evidence — useful information that does not currently require architectural change

---

# 3. R0.1 — Foundational Research and Architecture

## Initial Plan

Establish the conceptual foundation for Machine Builder by researching:

- machine-control terminology
- CNC terminology
- robotics terminology
- additive-manufacturing terminology
- industrial-control terminology
- drive/control terminology
- measurement/metrology terminology
- safety terminology
- engineering information models
- product/assembly modeling
- machine examples that violate simple assumptions

## Major Results

The research established strong candidate distinctions among:

- Machine
- Subsystem
- Component
- Axis
- Joint
- Link
- Actuator
- Motor
- Drive
- Controller
- Sensor
- Measurement Result
- Coordinate Frame
- Transform
- Function
- Capability
- Task
- Operation
- Action
- Procedure
- Control Function
- Safety Function
- Control Loop
- Tool
- Mechanical Interface
- Port
- Connection
- Property
- Quantity
- Unit
- Uncertainty
- Provenance

The research also established that:

- physical and semantic relationships must remain distinct
- firmware terminology must not define the canonical model
- many-to-many relationships are fundamental
- coordinate frames should be first-class concepts
- measurement results should be distinct from sensors
- feedback is a use of information rather than a sensor subtype
- safety functions can span multiple components
- subsystems can contain local control and communication
- catalog definitions must remain distinct from machine component occurrences

## Standards Foundations

Important standards families identified include:

- ISO 841
- ISO 8373
- ISO 9787
- IEC 81346
- IEC 81346-14
- ISO 10303 / STEP
- ISO/ASTM 52900
- ISO 14649
- IEC 61131
- IEC 61800
- CiA 402
- JCGM 200 / VIM
- ISO 12100
- ISO 13849
- IEC 62061
- ISO 13850
- ISO 14118
- ISO 14119
- ISO 14120
- ISO/IEC/IEEE 15288
- ISO/IEC/IEEE 42010
- ISO 15926
- OPC UA information models

## Final State

R0.1 establishes sufficient architectural evidence to begin formal ontology O0.1.

---

# 4. O0.1 — Foundational Ontology

## Status

Current major research task.

## Objectives

Finalize the first canonical semantic model without prematurely designing a database schema.

## Work Areas

### 4.1 Object Foundation

Resolve and document:

- Object
- Classification
- Role
- Aspect
- Occurrence
- Property
- Relationship
- Provenance

### 4.2 Core Concepts

Define each surviving canonical concept by:

- definition
- what it is not
- semantic scope
- important relationships
- examples
- standards evidence
- real-machine examples
- confidence
- deferred questions

### 4.3 Relationship Model

Finalize the major semantic relationship vocabulary, including candidates such as:

- contains
- part_of
- implements
- provides
- requires
- uses
- enables
- connects
- attached_to
- mounted_on
- drives
- acts_on
- participates_in
- produces_measurement
- feeds
- feedback_to
- commands
- reports_state_of
- transitions_to
- communicates_with
- uses_protocol
- performs
- realizes
- constrained_by
- protected_by
- maps_to
- derived_from
- validated_by
- specified_by

### 4.4 Constraints

Establish semantic cardinality where useful.

Examples include:

- one-to-many axis/actuator
- many-to-many function/component
- many-to-many measurement/consumer
- coordinate-frame parent relationships
- port/connection endpoint relationships

### 4.5 Provenance

Finalize the evidence model for:

- direct facts
- inferred facts
- derived values
- relationships
- classifications
- standards references
- validation results

### 4.6 Stress Testing

Test the ontology against:

- Promega
- SV08
- LowRider 3
- IdeaFormer IR3
- Creality CFS
- Carvera
- IDEX systems
- closed-loop servo systems
- K40
- CNC examples
- industrial machine examples

## Completion Criteria

O0.1 is complete when the model:

- has stable definitions for its core concepts
- has a coherent relationship vocabulary
- preserves many-to-many relationships
- separates physical, functional, behavioral, and implementation information
- survives the major machine stress tests
- records provenance and source evidence
- explicitly identifies unresolved concepts
- does not require a database schema to explain its semantics

---

# 5. Visual Builder Integration

The visual builder is being developed in parallel.

Current implementation:

    v0.1.0

The visual builder is already testing:

- Node
- Port
- Connection
- Compatibility
- Visual state
- Selection
- Model mutation

## Research Responsibility

The research side should refine the semantics behind these concepts without blocking basic implementation progress.

## Important Current Test

A very small sensor/controller port-to-port example is being used to validate:

    Component
        ↓
    Port
        ↓
    typed Connection
        ↓
    Compatibility

The visual implementation has already demonstrated that this abstraction is practical.

---

# 6. R0.2 — Post-O0.1 Architecture

After O0.1 is established, R0.2 should focus on the next architectural areas required by implementation.

Likely areas include:

### Port and Interface Semantics

Define richer meanings for:

- electrical ports
- signal ports
- communication ports
- mechanical interfaces
- material interfaces
- fluid interfaces
- logical interfaces

Determine how ports relate to:

- connectors
- pins
- conductors
- signals
- connections
- functions
- capabilities

### Machine Component Model

Formalize the relationship between:

- catalog definition
- product version
- machine component occurrence
- classification
- role
- placement
- provenance

### Connection / Path Model

Investigate and define the relationships among:

- physical connection
- logical connection
- network
- path
- route
- material path
- electrical topology
- communication topology

### Coordinate / Kinematic Model

Formalize:

- CoordinateFrame
- Transform
- Axis
- Joint
- Link
- Actuator
- KinematicModel

and their relationships.

### Process / Tool / Material Model

Expand:

- Process
- Task
- Operation
- Working Step
- Action
- Procedure
- Tool
- Tool interface
- Material subsystem
- material path

### Control Model

Expand:

- Command
- Signal
- State
- Fault
- Control Function
- Control Loop
- Setpoint
- Feedback
- Measurement Result

### Safety Model

Expand the relationship among:

- Hazard
- Risk
- Risk-reduction requirement
- Safety Function
- Safety-related control system
- protective mechanism
- validation

---

# 7. Future Electrical / Engineering Evaluation Work

This area is intentionally later than O0.1.

Potential future capabilities include:

## Circuit and Wiring Evaluation

Evaluate:

- voltage
- current
- AC/DC
- phase
- wire gauge
- conductor material
- conductor length
- ampacity
- voltage drop
- insulation
- ambient temperature
- installation conditions
- overcurrent protection
- terminations
- connector ratings
- load requirements

Potential result states:

- pass
- warning
- recommendation
- fail
- unknown

Results should retain:

- inputs
- assumptions
- calculation method
- applicable standard
- standard edition
- result
- provenance

This belongs to the future engineering-validation layer rather than the core visual ontology.

---

# 8. Future Safety Engineering

Research already supports a layered safety architecture:

Hazard
    ↓
Risk
    ↓
Risk Reduction Requirement
    ↓
Safety Function
    ↓
Safety-related Control Implementation
    ↓
Validation

Future work may incorporate:

- emergency stop
- unexpected-start prevention
- guards
- interlocks
- protective devices
- safety-related control architectures
- validation
- functional-safety calculations

Important safety standards should retain edition/version provenance because standards may be revised or replaced.

---

# 9. Firmware Semantic Mapping

Future research will formalize a firmware terminology and relationship library.

Potential structure:

```text
Firmware
Version
Firmware Term
Canonical Concept
Definition
Mapping Type
Scope
Related Concepts
Constraints
Source
Examples
Notes

Mapping types include candidates such as:

DIRECT
COMPOSITE
SPLIT
DERIVED
IMPLEMENTATION-SPECIFIC
PARTIAL
UNSUPPORTED

The purpose is to prevent the canonical ontology from becoming one firmware's terminology with other firmware names attached.

10. Firmware Parsing and Generation

Later work will support:

Firmware / Configuration
        ↓
Parser
        ↓
Semantic Interpretation
        ↓
Canonical Machine Model

and:

Canonical Machine Model
        ↓
Target Validation
        ↓
Firmware Adapter
        ↓
Generated Configuration

Potential targets include:

Klipper
RepRapFirmware
Marlin
FluidNC
GRBL
grblHAL
LinuxCNC
Repetier
Smoothieware
TinyG / g2core
other systems as justified by research
11. Future Machine Research

Research should continue selectively rather than as an unrestricted search for firmware names.

High-value research targets are machines that violate assumptions.

Examples:

multiple motors per logical axis
one actuator affecting multiple motions
tool changing
IDEX
rotary axes
distributed controllers
local intelligent subsystems
shared controller resources
closed-loop systems
multiple coordinate systems
material-handling subsystems
industrial power architectures
hybrid machines
machines with unusual process/tool relationships

Research should stop expanding a topic once the evidence is sufficient for the architectural question being asked.

12. Future Engineering Concepts

Deferred topics include:

electrical power architecture
facility power
conductor sizing
voltage-drop calculations
thermal/electrical constraints
torque/load calculations
machine capability evaluation
geometric accuracy
motion performance
diagnostic models
upgrade feasibility
engineering recommendations

These should be added when the foundational model can support them cleanly.

13. Research Handoffs

When a research topic reaches implementation readiness, create a handoff containing:

Concept
Definition
Reason for decision
Relationships
Constraints
Examples
Evidence
Implementation implications
Open questions

Implementation work should be referenced by software version where appropriate.

Example:

Research:
O0.1

Implementation:
v0.1.0

Decision:
Ports are explicit connection endpoints.

Implementation result:
Visual builder supports port-to-port connections.
14. Decision Management

Major architectural decisions belong in:

decisions/DECISION_LOG.md

Current architectural documents should describe the resulting state.

The decision log should preserve:

decision
context
evidence
alternatives
decision made
consequences
implementation impact
later changes

Historical decisions must remain identifiable when later superseded.

15. Open Questions

Unresolved questions belong in:

questions/OPEN_QUESTIONS.md

They should not be scattered across many unrelated files.

Examples may include:

exact Resource semantics
exact Port/Interface boundary
Path/Flow/Route distinctions
controller-resource modeling
representation of roles
aspect architecture
configuration vs runtime boundaries
capability evaluation
relationship constraints
firmware mapping semantics

A question should leave the list when it becomes an established decision, with the decision recorded separately.

16. Deferred Work Principle

New discoveries should be categorized rather than automatically inserted into the current milestone.

Use:

Foundation
Next
Later
Deferred
Research Evidence

A discovery should change the current ontology only when it exposes a genuine deficiency.

Interesting future capability should not be allowed to destabilize the foundational model unnecessarily.

17. Current Priority Order

The active priority order is:

Complete Ontology O0.1.
Finalize the core concept matrix.
Finalize the relationship matrix.
Complete ontology stress testing.
Record decisions and provenance.
Publish the O0.1 checkpoint.
Begin R0.2 research based on implementation needs and remaining architectural gaps.

The visual builder may continue independently during this work.

18. Definition of Research Success

The research architecture is progressing successfully when:

a new machine can be described without inventing firmware-specific concepts
unusual machine architectures do not require one-off ontology exceptions
physical and semantic relationships remain distinct
multiple views of the same machine can coexist
evidence can be traced to sources
derived values retain their derivation
safety can be represented as a cross-cutting function
firmware mappings remain implementation-specific
implementation can consume mature research decisions without importing the entire research history

The ultimate goal is not a giant taxonomy.

The goal is a durable semantic foundation for the Machine Development Environment.