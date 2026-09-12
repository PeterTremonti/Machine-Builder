# Research / Architecture R0.1

## 1. Purpose

R0.1 is the first durable research and architecture baseline for Machine Builder.

It represents the point at which the project has moved beyond initial exploration and established enough architectural direction to support continued ontology development and implementation.

R0.1 is not a final architecture.

It is a stable research snapshot.

---

# 2. R0.1 Scope

R0.1 establishes the foundational direction for:

- machine-first architecture;
- canonical machine modeling;
- ontology organization;
- physical versus logical versus functional structure;
- visual-model separation;
- firmware independence;
- machine components and catalogs;
- provenance;
- evidence;
- motion semantics;
- coordinate frames;
- measurement;
- functions;
- ports and connections;
- subsystems;
- safety foundations;
- engineering evaluation direction;
- research/implementation boundaries.

---

# 3. Version Streams

R0.1 belongs to the research/architecture version stream.

The project uses independent version streams:

```text
Research / Architecture:
    R0.x

Ontology:
    O0.x

Implementation:
    v0.x.y

R0.1 therefore does not imply:

Ontology = O0.1
Implementation = v0.1.0

The streams are related but independent.

4. R0.1 Architectural Foundation

The primary architectural direction is:

Physical Machine
      ↓
Evidence / Observation
      ↓
Semantic Interpretation
      ↓
Canonical Machine Model
      ↓
Engineering Evaluation
      ↓
Implementation / Representation

The reverse direction must also be supported:

Firmware / Configuration
      ↓
Semantic Interpretation
      ↓
Canonical Machine Model

The canonical model is the semantic center.

5. Core Modeling Pattern

The current foundational modeling pattern is:

Object
├── Classification
├── Role
├── Aspect
├── Property
├── Relationship
└── Provenance

This intentionally avoids making a rigid inheritance hierarchy the sole mechanism for representing machine semantics.

6. Major Architectural Distinctions Established in R0.1

R0.1 establishes the following distinctions as important architectural boundaries.

Object ≠ Classification
Classification ≠ Role
Role ≠ Function

Machine Component ≠ Catalog Product

Axis ≠ Motor
Axis ≠ Joint
Joint ≠ Actuator
Motor ≠ Drive
Drive ≠ Controller

Sensor ≠ Measurement Result
Measurement Result ≠ Feedback

Capability ≠ Function
Function ≠ Task
Function ≠ Operation
Operation ≠ Action
Operation ≠ Procedure

Tool ≠ Toolhead
Toolhead ≠ Carriage

Port ≠ Connector
Port ≠ Pin

Connection ≠ Visual Connection
Physical Connection ≠ Logical Mapping

Physical Position ≠ Canvas Position

Configuration ≠ Runtime State

Firmware Term ≠ Canonical Concept

Catalog Data ≠ Machine Fact

Inference ≠ Direct Observation
Derived Value ≠ Direct Value

Engineering Evaluation ≠ Certification

These distinctions are among the most important results of the R0.1 research phase.

7. Canonical Machine Model

The canonical machine model represents machine semantics independently of a specific firmware or visual representation.

Current major concept areas include:

Machine
Machine Component
Subsystem
Classification
Role
Aspect
Property
Relationship
Provenance

Axis
Joint
Link
Actuator
Motor
Drive
Coordinate Frame
Transform

Port
Connector
Pin
Connection
Physical Connection
Logical Mapping
Path
Harness

Sensor
Measurand
Measurement
Measurement Result
Feedback

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

Controller
Controller Resource
Firmware
Firmware Mapping
Firmware Term

Configuration
Runtime State
Mode
Fault

Hazard
Risk
Risk Reduction Requirement
Safety Function
Safety-Related Control Implementation
Safe State

Constraint
Compatibility
Verification
Validation
Evaluation Result

Not all concepts have equal maturity.

8. Firmware Independence

R0.1 establishes that firmware is an implementation layer.

Important firmware research systems include:

RepRapFirmware
Klipper
Marlin
FluidNC
grblHAL
GRBL
Smoothieware
TinyG / g2core
LinuxCNC
Repetier

The primary comparison set is:

RepRapFirmware
Klipper
Marlin
FluidNC

Firmware differences are treated as evidence for general machine concepts.

They should not determine the canonical ontology.

9. Machine Stress Cases

R0.1 establishes a diverse machine corpus for architectural testing.

Important stress cases include:

M3D Promega
SV08
LowRider
IR3
Creality CFS
Stratasys SST1200es
Ender 3
Carvera
K40
3018 CNC
IDEX
Tool Changers
Closed-Loop Machines
CoreXY
Distributed Controllers
Multiple-Actuator Axes

The most important current stress cases are:

Promega
SV08
LowRider
IR3
CFS
SST1200es

These machines intentionally violate assumptions that would otherwise produce an overly simple printer-centric ontology.

10. Promega Contribution

The Promega provides an important baseline for:

RepRapFirmware interpretation;
controller resource mapping;
CoreXY;
probing;
motion configuration;
firmware-to-machine interpretation;
calibration;
physical/logical connectivity.

Its configuration provides concrete examples of firmware syntax that can be interpreted semantically.

11. SV08 Contribution

The SV08 demonstrates that:

One logical Z Axis
    ≠
One Motor

A single machine axis may involve multiple independently controlled actuators.

It also contributes evidence for:

distributed control;
controller resources;
toolhead electronics;
firmware mapping;
kinematics.
12. LowRider Contribution

LowRider expands the research domain into CNC.

It tests:

multiple actuators;
coordinated motion;
squaring;
tools;
workholding;
machining processes;
CNC firmware.

It provides evidence that the canonical model must work beyond 3D printing.

13. IR3 Contribution

IR3 demonstrates the need to separate:

Machine Motion
Coordinate Frames
Transforms
Visual Coordinates

A conventional Cartesian assumption is insufficient.

14. CFS Contribution

The CFS demonstrates the need for meaningful Subsystem modeling.

It contains:

multiple motors;
multiple sensors;
material paths;
buffering;
local control;
communications.

The CFS therefore cannot be accurately reduced to a single feeder component.

15. SST1200es Contribution

The SST1200es provides an industrial/proprietary machine stress case.

Its planned retrofit further tests:

Existing Physical Machine
        ↓
Canonical Machine Model
        ↓
New Controller
        ↓
New Firmware

This demonstrates why the canonical machine identity must remain independent from its original firmware implementation.

16. Standards Foundation

R0.1 established a targeted standards foundation rather than attempting to research every possible standard.

Important references include:

ISO/IEC/IEEE 15288
ISO/IEC/IEEE 42010
IEC 81346-1
IEC 81346-2
IEC 81346-14:2026
ISO 841
ISO 8373
ISO 9787
ISO 10303 / STEP
JCGM 200 / VIM
IEC 81714-2
ISO 14649 / STEP-NC
IEC 61131-1/-3
IEC 61800 family
CiA 402
ISO 12100
ISO 13849
IEC 62061
ISO 13850
ISO 14118
ISO 14119
ISO 14120
IEC 60204-1

The standards are evidence and engineering references.

They are not automatically the Machine Builder ontology.

17. Object / Classification / Role / Aspect

One of the major R0.1 conclusions is that these concepts should remain distinct.

Example:

Object:
    physical motor

Classification:
    stepper motor

Role:
    Z-axis actuator

Aspect:
    electrical / physical / control

This supports multiple engineering perspectives without duplicating the physical object.

18. Relationships

R0.1 establishes that relationships are first-class semantic information.

Important examples include:

contains
part_of
classified_as
has_role
mounted_on
mechanically_coupled_to
connects_to
physically_connected_to
measures
participates_in
drives
controls
implements
maps_to
has_resource
assigned_to
derived_from
supported_by
inferred_from

The exact cardinality and formal representation of many relationships remain open.

19. Connectivity

R0.1 establishes:

Port
Connector
Pin
Connection
Physical Connection
Logical Mapping

as distinguishable concepts.

The important architectural rule is:

Port ≠ Connector ≠ Pin
Connection ≠ Visual Line
Physical Connection ≠ Logical Mapping

This provides the foundation for both visual connection editing and future wiring/electrical engineering.

20. Measurement

R0.1 establishes:

Sensor
Measurand
Measurement
Measurement Result
Feedback

as distinct concepts.

The basic structure is:

Sensor
   ↓
Measurement
   ↓
Measurement Result
   ↓
Consumer

Consumers may include:

control;
diagnostics;
calibration;
logging;
display;
safety.
21. Function Vocabulary

R0.1 establishes the following working distinctions:

Capability
    ability possessed by a system

Function
    defined machine/subsystem behavior or service

Task
    intended body of work

Process
    organized activity producing an intended result

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

Control Loop
    structured relationship among setpoint,
    control, physical response, measurement, and feedback

The project explicitly avoids treating these as one universal inheritance chain.

22. Control

R0.1 establishes the conceptual control loop:

Setpoint
   ↓
Control Function
   ↓
Control Output
   ↓
Actuator / Physical System
   ↓
Machine Response
   ↓
Measurement
   ↓
Feedback
   └──→ Control Function

This provides a firmware-independent control abstraction.

23. Coordinate Frames

R0.1 establishes CoordinateFrame as a first-class concept.

Potential frames include:

Machine
Work
Tool
Object
Camera
Task
Subsystem

Canvas coordinates remain separate.

This is particularly important for:

belt printers;
robotics;
rotary systems;
tool offsets;
future 3D visualization.
24. Provenance

R0.1 establishes provenance as a first-class architectural concern.

Relevant provenance includes:

Source
Method
Date
Version
Confidence
Evidence Location
Observation
Calculation
Inference
Assumption

The architecture distinguishes:

Direct
Derived
Inferred

information.

Unknown information is valid.

25. Safety Foundation

R0.1 establishes the basic safety architecture:

Hazard
   ↓
Risk
   ↓
Risk Reduction Requirement
   ↓
Safety Function
   ↓
Safety-Related Control Implementation
   ↓
Validation
   ↓
Safe State

Safety remains an engineering layer rather than a boolean compliance property.

Certification-grade automation is intentionally outside the current implementation scope.

26. Engineering Evaluation

R0.1 establishes that engineering evaluation is a derived layer operating on canonical machine information.

Potential result states include:

PASS
WARNING
RECOMMENDATION
INVALID
UNKNOWN

Evaluation must eventually retain:

inputs;
assumptions;
method;
evidence;
applicable rules/standards;
result.
27. Catalog and Machine Components

R0.1 establishes the distinction:

Catalog Product
      ↓
Product Version
      ↓
Machine Component

Catalog information is evidence or candidate information.

It does not automatically become authoritative machine information.

28. Visual Architecture

R0.1 establishes:

Canonical Model
      ↕
Visual Model
      ↓
Renderer / UI

The visual model may contain:

node positions;
node sizes;
grouping;
visibility;
routing;
selection;
zoom;
interaction state.

The visual model is not semantic authority.

29. Visual Builder Relationship Model

The current implementation-facing visual architecture establishes:

Component
   ↓
Port
   ↓
Semantic Connection
   ↓
Port
   ↓
Component

with:

Compatibility Evaluation
        ↓
Connection State
        ↓
Visual Feedback

The first implementation may be deliberately simple.

The architecture must remain capable of growing into the broader semantic model.

30. Research / Implementation Boundary

R0.1 establishes the division:

Research

Defines:

what concepts mean;
why distinctions matter;
standards evidence;
architecture;
ontology;
open questions.
Implementation

Defines:

code;
UI;
persistence;
tests;
parsers;
translators;
executable behavior.
Feedback Loop
Research
   ↓
Implementation
   ↓
Observed Behavior
   ↓
New Evidence
   ↓
Research Revision
31. Deferred Areas

R0.1 intentionally does not attempt to finalize:

Universal Flow
Universal Signal
Universal Channel
Detailed Database Schema
Knowledge Graph Storage
Advanced Kinematics
Advanced Electrical Engineering
Advanced Safety Calculations
Complete Process Ontology
Full CAD Integration
Full CAM Integration
Complete Runtime Telemetry
Full Digital Twin
Advanced Diagnostics
Automatic Machine Reconstruction

These remain visible as future research.

32. R0.1 Architectural Invariants

The following are considered stable enough to guide subsequent work:

1. Canonical Machine Model is primary.
2. Firmware is an implementation representation.
3. Visual Model is separate from canonical semantics.
4. Relationships are first-class.
5. Object, Classification, Role, and Aspect are distinct.
6. Machine Component and Catalog Product are distinct.
7. Unknown information is valid.
8. Provenance is first-class.
9. Direct, derived, and inferred information are distinct.
10. Axis is not Motor.
11. Joint, Actuator, Motor, and Drive remain distinct.
12. Coordinate Frames are first-class.
13. Ports are first-class.
14. Port, Connector, and Pin are distinct.
15. Connection is not a visual line.
16. Physical Connection and Logical Mapping are distinct.
17. Sensor is not Measurement Result.
18. Capability and Function are distinct.
19. Function, Task, Operation, Action, and Procedure are distinct.
20. Subsystems are first-class.
21. Runtime State is distinct from Configuration.
22. Firmware terminology does not define canonical terminology.
23. Engineering evaluation is derived.
24. Safety is evidence-based and contextual.
25. Stress cases drive generalization.
33. R0.1 Completion Criteria

R0.1 is considered complete enough when:

foundational architecture has been documented;
major terminology distinctions have been established;
the initial standards foundation has been researched;
key machine stress cases have been identified;
firmware comparison has begun;
research and implementation boundaries are defined;
major deferred topics are recorded;
the next ontology milestone can proceed without repeatedly reconstructing the original research.

R0.1 does not require:

final ontology;
final database schema;
complete firmware support;
complete engineering calculation;
finished visual builder.
34. Transition to O0.1

The primary outcome of R0.1 is that enough architectural groundwork exists to formalize the first ontology milestone.

The transition is:

R0.1
Research / Architecture Foundation
        ↓
O0.1
Ontology Foundation

O0.1 should focus on:

precise concept definitions;
relationship vocabulary;
relationship constraints;
provenance;
cardinality;
stress testing;
contradiction cleanup;
canonical concept promotion.
35. Transition to R0.2

After the initial ontology foundation is sufficiently mature, R0.2 can address deeper domain integration.

Potential R0.2 areas include:

Port / Interface Semantics
Machine Component Modeling
Connection / Path Semantics
Coordinate / Kinematic Refinement
Process / Tool Semantics
Control
Safety
Controller Resources
Electrical Engineering
Firmware Mapping

R0.2 should be driven by evidence rather than by a requirement to research every domain simultaneously.

36. Relationship to Implementation v0.1.0

The implementation has independently reached:

v0.1.0

This does not mean the entire R0.1 architecture is implemented.

The relationship is:

R0.1
    provides architectural direction

O0.1
    provides evolving semantic definitions

v0.1.0
    provides current software implementation

The implementation can therefore remain intentionally simpler than the long-term architecture while still following its important invariants.

37. Relationship to Implementation v0.2

The current implementation direction is focused on the visual-builder connection architecture.

The immediate proof-of-concept demonstrates:

Component
   ↓
Port
   ↓
Connection
   ↓
Compatibility
   ↓
Visual Feedback

This is deliberately narrower than the complete ontology.

The purpose is to establish a sound implementation foundation without requiring the complete long-term model first.

38. R0.1 Lessons

The most important lessons from the R0.1 research period are:

1. Simple printer assumptions are insufficient.

Real machines require more general concepts.

2. Relationships matter as much as objects.

The machine is defined by how its elements participate together.

3. Firmware terminology is not machine terminology.

The canonical model must remain firmware-independent.

4. Visual representation must remain separate.

The canvas is a view of the machine, not the machine definition.

5. Unknown information must remain unknown.

False precision is worse than incomplete information.

6. Standards are most useful when targeted.

Standards should inform specific semantic questions rather than become an end in themselves.

7. Stress cases are essential.

CoreXY, multiple-Z, CFS, IR3, CNC, distributed controllers, and industrial machines expose assumptions that conventional printers hide.

39. R0.1 Baseline Diagram

The R0.1 architecture can be summarized as:

                         EXTERNAL REALITY
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
          Evidence Sources              Physical Machine
                │                             │
                └──────────────┬──────────────┘
                               ▼
                        Interpretation
                               │
                               ▼
                  ┌──────────────────────┐
                  │ CANONICAL MACHINE    │
                  │       MODEL          │
                  │                      │
                  │ Objects              │
                  │ Classifications      │
                  │ Roles                │
                  │ Aspects              │
                  │ Properties           │
                  │ Relationships        │
                  │ Provenance           │
                  └──────────┬───────────┘
                             │
                ┌────────────┼────────────┐
                ▼            ▼            ▼
           Engineering    Visual      Translation
            Analysis      Model          Layer
                │            │            │
                ▼            ▼            ▼
           Evaluation        UI       Firmware /
              Tools                    External Systems
40. Final R0.1 Principle

R0.1 establishes the following guiding principle:

Machine Builder should model what the machine means before modeling how a particular firmware, controller, UI, database, or drawing happens to represent it.

This principle should continue into O0.1, R0.2, and later research versions unless deliberately superseded by stronger evidence.