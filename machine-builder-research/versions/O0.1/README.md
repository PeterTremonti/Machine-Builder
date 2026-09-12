# Ontology O0.1

## 1. Purpose

O0.1 is the first durable ontology baseline for Machine Builder.

It records the current semantic model developed from the R0.1 research and architecture work.

The purpose of O0.1 is to establish enough semantic structure that:

- implementation can proceed without repeatedly redefining basic concepts;
- machine stress cases can be evaluated consistently;
- relationships can be refined systematically;
- future ontology changes can be compared against a known baseline.

O0.1 is not intended to be the final Machine Builder ontology.

It is the first explicit ontology milestone.

---

# 2. Version Context

O0.1 belongs to the ontology version stream.

The project uses independent version streams:

```text
Research / Architecture:
    R0.x

Ontology:
    O0.x

Implementation:
    v0.x.y

O0.1 therefore does not imply a matching implementation or research version.

At this stage:

Research / Architecture:
    R0.1

Ontology:
    O0.1

Implementation:
    v0.2 development
3. Ontology Objective

The objective of O0.1 is to establish a semantic foundation capable of describing machines independently of a particular:

firmware;
controller;
UI;
database;
catalog;
drawing;
implementation language.

The ontology should describe:

What exists
What kind of thing it is
How it is used
How it is structured
How it relates to other things
What it does
What it can do
What it measures
How it is controlled
What constraints apply
Where the information came from
4. Core Ontology Pattern

The current foundation is:

Object
├── Classification
├── Role
├── Aspect
├── Property
├── Relationship
└── Provenance

This is a semantic pattern rather than a requirement for a particular software class hierarchy.

5. Object
Definition

An Object is an identifiable entity represented by the machine model.

Examples:

Machine
Motor
Sensor
Controller
Axis
Joint
Subsystem
Port
Tool
Coordinate Frame
Object Characteristics

An Object may:

have one or more classifications;
have contextual roles;
participate in aspects;
have properties;
participate in relationships;
have provenance.
Important Boundary

Object identity is distinct from Classification.

6. Classification
Definition

Classification describes what kind or category of thing an Object is.

Examples:

Stepper Motor
Temperature Sensor
Controller
Drive
Tool
Guard
Coordinate Frame
Important Boundary

Classification does not describe how an Object is being used in a particular machine.

That is the purpose of Role.

7. Role
Definition

Role describes how an Object participates in a particular context.

Examples:

Z-axis actuator
Extruder actuator
Filament feeder
Bed-temperature sensor
Safety interlock device
Context

A Role may depend on:

machine;
subsystem;
configuration;
process;
operating mode;
time/version.
Important Boundary

Role is distinct from Classification.

8. Aspect
Definition

Aspect represents an engineering structuring or viewing dimension.

Examples include:

Physical
Electrical
Logical
Functional
Control
Safety
Maintenance

IEC 81346 is an important influence.

Important Boundary

Aspect should not become a second Classification system.

An Object may participate in multiple aspects.

9. Property
Definition

A Property represents a characteristic or value associated with an Object or, where justified, a Relationship.

Examples:

current = 1.5 A
steps_per_revolution = 200
shaft_diameter = 5 mm
maximum_temperature = 250 °C
Required Future Capabilities

Properties may eventually need:

units;
dimensions;
ranges;
limits;
uncertainty;
validity;
provenance;
derivation;
confidence;
version applicability.

The exact Property model is not yet finalized.

10. Relationship
Definition

A Relationship is a typed semantic association between modeled entities.

Examples:

contains
classified_as
has_role
mounted_on
connects_to
measures
participates_in
implements
maps_to
derived_from
supported_by
Requirements

Relationships may eventually require:

direction;
inverse;
multiplicity;
context;
properties;
provenance;
validity;
derivation status.
11. Provenance
Definition

Provenance records where and how information was established.

Potential elements include:

Source
Method
Date
Version
Confidence
Evidence location
Observation
Calculation
Inference
Assumption

Provenance may apply to:

Property;
Relationship;
Classification;
Role;
derived value;
evaluation;
interpretation.
12. Information Status

O0.1 recognizes that information can have different evidentiary states.

Current conceptual categories include:

Unknown
Not Yet Investigated
Observed
Documented
Measured
Derived
Inferred
Estimated
Verified
Conflicting

These categories are not yet a finalized enum.

The important rule is:

Unknown information must remain representable.

13. Direct, Derived, and Inferred

O0.1 explicitly distinguishes:

Direct

Explicitly stated or directly observed.

Example:

Motor datasheet:
    rated current = 1.5 A
Derived

Calculated from known information.

Example:

steps/mm
    derived from
steps/revolution
microstepping
mechanical transmission
Inferred

A conclusion supported by evidence but not directly established.

Example:

motor is probably the Z actuator

These categories should retain appropriate provenance and confidence.

14. Machine
Definition

A Machine is the primary system of interest being modeled.

A Machine may contain:

machine components;
subsystems;
controllers;
tools;
functions;
capabilities;
processes;
interfaces;
coordinate frames;
safety structures;
runtime state.

Machine is intentionally broader than any one machine class.

15. Machine Component
Definition

A Machine Component is a machine-specific occurrence of a physical component.

Examples:

physical motor installed in a machine
specific controller board
specific sensor
specific linear rail
Important Boundary

Machine Component is distinct from Catalog Product.

16. Catalog Product
Definition

A Catalog Product is a reusable product definition external to a specific machine.

Examples:

motor model
controller board model
connector product
linear rail product

Catalog Products may be associated with Machine Components.

They do not automatically become Machine Components.

17. Product Version
Definition

Product Version identifies a particular revision, variant, or version of a Catalog Product.

It may affect:

dimensions;
pinout;
ratings;
behavior;
compatibility;
firmware support.
18. Subsystem
Definition

A Subsystem is a bounded portion of a Machine that may contain:

components;
functions;
capabilities;
resources;
state;
interfaces;
local control;
communication.

Subsystems may contain other Subsystems.

19. Motion Ontology

O0.1 distinguishes:

Axis
Joint
Link
Actuator
Motor
Drive
Kinematic Relationship

These are not interchangeable.

20. Axis
Definition

Axis represents machine motion or coordinate semantics.

An Axis is not inherently a physical actuator.

A single Axis may involve:

one actuator;
multiple actuators;
coupled actuators;
a kinematic transformation.
21. Joint
Definition

Joint represents a constrained mechanical relationship permitting relative motion.

A Joint may be:

active;
passive;
actuated;
constrained by mechanical structure.

Joint is distinct from Axis.

22. Link
Definition

Link represents a relatively rigid mechanical element participating in a mechanical structure.

Links may connect or separate Joints.

The exact formal model remains under refinement.

23. Actuator
Definition

Actuator represents an element capable of producing a controlled physical effect.

An Actuator may include or depend on:

Motor;
Drive;
transmission;
mechanical coupling.
24. Motor
Definition

Motor is an electromechanical energy-conversion device producing mechanical motion.

Examples:

Stepper Motor
Servo Motor
DC Motor
BLDC Motor

Motor does not automatically represent the complete Actuator system.

25. Drive
Definition

Drive represents a system or component responsible for controlling a Motor or Actuator.

Depending on architecture, a Drive may provide:

power electronics;
current control;
velocity control;
position control;
feedback processing;
communication.
26. Kinematic Relationship
Definition

Kinematic Relationship represents how physical motions are coupled or transformed.

Examples:

CoreXY
Gear train
Belt transmission
Lead screw
Robot kinematics
Coordinated rotary motion

The ontology must support many-to-many motion participation.

27. Coordinate Ontology

O0.1 includes:

Coordinate Frame
Transform
Canvas Coordinate

These are deliberately distinct.

28. Coordinate Frame
Definition

Coordinate Frame represents a meaningful reference coordinate system.

Examples:

Machine Frame
Work Frame
Tool Frame
Object Frame
Camera Frame
Task Frame

A Coordinate Frame may have:

parent;
transform;
semantic role;
reference object.
29. Transform
Definition

Transform represents the mathematical relationship between Coordinate Frames.

The storage representation remains open.

Possible mathematical forms include:

translation + rotation;
matrices;
quaternions;
other appropriate representations.
30. Canvas Coordinate

Canvas Coordinate belongs to the visual model.

It describes where something appears in the application.

It does not define physical machine location.

31. Connectivity Ontology

O0.1 distinguishes:

Port
Connector
Pin
Connection
Physical Connection
Logical Mapping
Path
Harness

These concepts must not be collapsed solely for convenience.

32. Port
Definition

Port represents a semantic interface endpoint exposed by an Object.

Possible domains include:

Electrical
Signal
Communication
Mechanical
Material
Fluid
Logical

Port is not automatically a Connector or Pin.

33. Connector
Definition

Connector represents a physical interface structure that may contain multiple Pins.

34. Pin
Definition

Pin represents a discrete contact or terminal associated with a connector or similar interface structure.

A Pin may carry:

power;
ground;
signal;
communications;
control.
35. Connection
Definition

Connection represents a semantic association between compatible endpoints.

A Connection may occur in different domains.

Connection is independent of its visual representation.

36. Physical Connection
Definition

Physical Connection represents an actual physical attachment or route.

Examples:

Wire
Cable
Tube
Mechanical coupling
Material path
37. Logical Mapping
Definition

Logical Mapping represents how logical meaning corresponds to implementation or physical representation.

Examples:

Temperature signal
    maps_to
Controller input

Canonical Axis
    maps_to
Firmware axis

Logical heater enable
    maps_to
Physical pin

Physical Connection and Logical Mapping remain distinct.

38. Path
Definition

Path represents a physical or topological route.

A Path does not automatically imply active Flow.

Potential uses include:

material;
fluid;
cables;
communication;
mechanical transmission.

The exact Path model remains under refinement.

39. Harness
Definition

Harness represents a grouped physical routing structure such as:

wires;
cables;
tubing;
sub-harnesses.

A Harness may contain lower-level physical elements.

40. Measurement Ontology

O0.1 distinguishes:

Sensor
Measurand
Measurement
Measurement Result
Feedback

The intended structure is:

Sensor
   ↓
Measurement
   ↓
Measurement Result
   ↓
Consumer
41. Sensor
Definition

Sensor represents a physical or functional element involved in obtaining information about a quantity or condition.

42. Measurand
Definition

Measurand represents the quantity intended to be measured.

Examples:

Temperature
Position
Pressure
Force
Distance
Current
43. Measurement
Definition

Measurement represents the process or activity by which information about a Measurand is obtained.

44. Measurement Result
Definition

Measurement Result represents the information produced by a measurement.

Potential information includes:

Value
Unit
Uncertainty
Time
Conditions
Method
Provenance
45. Feedback
Definition

Feedback represents the use of measurement information in a control relationship.

Feedback is not a type of Sensor.

46. Capability and Function Ontology

O0.1 distinguishes:

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

These concepts have related but distinct meanings.

47. Capability
Definition

Capability represents an ability possessed by a Machine, Subsystem, Object, or system.

Example:

Can perform automatic tool changing
48. Function
Definition

Function represents a defined machine or subsystem behavior or service independent of one specific execution instance, procedure, command, or firmware syntax.

Examples:

Maintain Build Temperature
Feed Material
Move Tool
Measure Temperature
Prevent Unexpected Restart

Function is not a universal parent for every activity or software execution concept.

49. Task
Definition

Task represents an intended body of work or objective.

Examples:

Print Part
Machine Pocket
Inspect Part
Change Tool
50. Process
Definition

Process represents an organized activity through which an intended result is achieved.

Examples:

Additive Manufacturing
Machining
Inspection
Material Loading

The exact formal process ontology remains open.

51. Operation
Definition

Operation represents a bounded executable unit of work within a Task or Process.

Examples:

Heat Build Volume
Probe Surface
Extrude Material
Change Tool
52. Action
Definition

Action represents a discrete executable behavior or change.

Examples:

Enable Heater
Stop Motor
Advance Filament
Trigger Probe
Open Valve
53. Procedure
Definition

Procedure represents a specified way of carrying out an activity.

Examples:

Z-Probe Calibration Procedure
Tool Change Procedure
Motor Replacement Procedure

Procedure is concerned substantially with how an activity is performed.

54. Control Function
Definition

Control Function represents a Function used to regulate machine behavior based on information, command intent, or feedback.

Examples:

Temperature Control
Position Control
Speed Control
Pressure Control
55. Safety Function
Definition

Safety Function represents a Function required to achieve or maintain a safe state or reduce risk.

Examples:

Prevent Unexpected Startup
Stop Hazardous Motion When Guard Opens
Emergency Stop
56. Control Loop
Definition

Control Loop represents a structured control arrangement involving some combination of:

Setpoint
Control Function
Control Output
Physical System
Measurement
Feedback

A Control Loop does not require a particular firmware implementation.

57. Controller Ontology

O0.1 distinguishes:

Controller
Controller Resource
Firmware
Firmware Mapping
Firmware Term

These represent different architectural layers.

58. Controller
Definition

Controller represents a computing or control entity responsible for coordinating one or more machine behaviors or resources.

59. Controller Resource
Definition

Controller Resource represents a finite hardware or software capability provided by a Controller.

Examples:

Motor Driver
GPIO
ADC Channel
PWM
Timer
UART
CAN
Processing Resource

The exact boundary between hardware and software resources remains under refinement.

60. Firmware
Definition

Firmware represents software executing on a controller or embedded computing environment that implements machine control behavior.

Firmware is not the canonical machine ontology.

61. Firmware Term
Definition

Firmware Term represents a concept or identifier whose meaning is defined by a particular firmware ecosystem.

Examples:

M584
M92
step_pin
dir_pin
driver section
tool definition

Firmware Terms may map to canonical concepts.

62. Firmware Mapping
Definition

Firmware Mapping represents correspondence between canonical semantics and a firmware-specific representation.

Mappings may be:

one-to-one;
one-to-many;
many-to-one;
conditional;
calculated;
version-specific.
63. Configuration and State

O0.1 distinguishes:

Configuration
Runtime State
Mode
Fault
64. Configuration
Definition

Configuration represents intended machine setup and operating parameters.

Examples:

Motor Current
Steps per Unit
Axis Assignment
Maximum Velocity
Tool Assignment
65. Runtime State
Definition

Runtime State represents the current condition of a Machine, Subsystem, Controller, or Component.

Examples:

Axis Homed
Motor Enabled
Temperature = 205 °C
Filament Present
Drive Faulted

Runtime State does not overwrite Configuration.

66. Mode
Definition

Mode represents a defined operating context.

Potential examples:

Idle
Manual
Homing
Printing
Maintenance
Fault

The relationship among Mode, State, and Fault remains under refinement.

67. Fault
Definition

Fault represents a detected condition that disrupts normal operation or requires intervention.

68. Safety Ontology

The current O0.1 safety structure is:

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
69. Hazard
Definition

Hazard represents a potential source of harm.

70. Risk
Definition

Risk represents the relevant combination of likelihood and severity associated with potential harm.

71. Risk Reduction Requirement
Definition

Risk Reduction Requirement represents a requirement established to reduce a machine risk.

72. Safety-Related Control Implementation
Definition

Safety-Related Control Implementation represents hardware and/or software through which a Safety Function is realized.

73. Safe State
Definition

Safe State represents a defined condition in which the relevant hazard is controlled according to the applicable safety architecture.

Safe State is context-dependent.

74. Guard
Definition

Guard represents a physical protective structure intended to prevent or restrict access to hazardous areas.

75. Interlock
Definition

Interlock represents a mechanism or control relationship used to detect protective conditions and constrain machine behavior.

76. Tool Ontology

O0.1 distinguishes:

Tool
Toolhead
Carriage
Workholding
77. Tool
Definition

Tool represents an object used by a Machine to perform or support a Process.

Examples:

Extrusion Tool
Cutting Tool
Laser
Probe
Dispenser
78. Toolhead
Definition

Toolhead represents a physical assembly carrying one or more Tools or process elements.

A Toolhead may contain:

Tool;
Sensor;
Actuator;
Electronics;
Heating;
Cooling;
Mounting structures.
79. Carriage
Definition

Carriage represents a mechanical structure supporting or moving a Toolhead, Tool, or other machine element.

80. Workholding
Definition

Workholding represents a structure used to locate, support, or constrain a workpiece.

Examples:

Build Plate
Vice
Chuck
Clamp
Fixture
81. Evaluation Ontology

O0.1 includes the following engineering concepts:

Constraint
Compatibility
Verification
Validation
Evaluation Result
82. Constraint
Definition

Constraint represents a condition that must be satisfied.

Examples:

Driver current must not exceed rating
Controller must provide required resource
Tool must fit mounting interface
83. Compatibility
Definition

Compatibility represents the degree to which entities, interfaces, resources, or requirements can work together under specified conditions.

Potential states:

Compatible
Incompatible
Conditionally Compatible
Unknown
84. Verification
Definition

Verification represents determination of whether a result or implementation conforms to specified requirements or criteria.

85. Validation
Definition

Validation represents determination of whether a system or implementation satisfies intended purpose or specified validation criteria.

The exact formal distinction remains subject to applicable domain standards.

86. Evaluation Result
Definition

Evaluation Result represents a derived engineering conclusion.

Potential status values:

PASS
WARNING
RECOMMENDATION
INVALID
UNKNOWN

Evaluation Result is not itself a permanent machine fact.

87. Core Relationship Vocabulary

The current O0.1 relationship vocabulary includes:

contains
part_of
classified_as
has_role
has_property

mounted_on
mechanically_coupled_to
physically_connected_to
connects_to
interfaces_with

participates_in
drives
constrains
transforms_motion_of

measures
produces_measurement
consumes_measurement

performs
provides_capability
implements

controls
commanded_by
feedback_from
feeds
regulates

part_of_process
precedes
follows
requires
produces_result

mounts_tool
used_by
performs_process_on

has_resource
assigned_to
mapped_to

maps_to
generated_from
parsed_from

supported_by
derived_from
inferred_from
contradicts
supersedes

has_parent_frame
transformed_by
referenced_by

protects
monitored_by
triggers
realizes_safety_function

constrained_by
evaluated_by
satisfies
violates

Not all relationships are formally finalized.

88. Relationship Cardinality Philosophy

O0.1 intentionally does not assume universal one-to-one cardinality.

Examples include:

Multiple Motors
    → one Axis

One Motor
    → multiple Motion Contributions

One Sensor
    → multiple Consumers

One Controller
    → many Resources

One Logical Mapping
    → multiple Physical Elements

Formal cardinalities remain a major next-stage refinement.

89. Relationship Context

Relationships may depend on context.

Examples:

Machine
Subsystem
Configuration
Firmware Version
Product Version
Time
Operating Mode

A relationship such as:

Motor
    has_role
Z-axis actuator

may be valid only within a particular Machine and configuration.

The exact representation of relationship context remains open.

90. Visual Concepts

The following are primarily implementation/presentation concepts:

Visual Model
Node
Visual Connection
Canvas
Canvas Coordinate

They may reference canonical concepts but do not define canonical meaning.

91. Major Non-Equivalences

O0.1 preserves these distinctions:

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

Inference ≠ Observation
Derived Value ≠ Direct Value

Engineering Evaluation ≠ Certification

These are currently considered ontology invariants.

92. Stress Cases for O0.1

The ontology should be tested against:

Promega
SV08
LowRider
IR3
Creality CFS
Stratasys SST1200es
CoreXY
IDEX
Tool Changer
Closed Loop
Distributed Controllers
CNC Machines
Industrial Machines

A concept is not considered mature merely because it works for a conventional Cartesian printer.

93. Promega Test

The ontology should support:

Machine
    contains
Controller

Machine
    contains
Machine Components

Motors
    participate_in
Motion

Probe
    measures
Measurand

Firmware Configuration
    maps_to
Canonical Properties / Relationships

It should also preserve firmware provenance.

94. SV08 Test

The ontology should support:

Four physical Z actuators
        ↓
One logical Z Axis

while retaining:

individual motors;
individual controller resources;
kinematic relationships;
synchronization;
machine role.
95. CoreXY Test

The ontology should support:

Motor A
    participates_in
X

Motor A
    participates_in
Y

Motor B
    participates_in
X

Motor B
    participates_in
Y

without falsely assigning each motor exclusively to one axis.

96. IR3 Test

The ontology should support:

Machine Coordinate Frame
Tool Coordinate Frame
Kinematic Relationship
Transform
Axis

without assuming standard Cartesian geometry.

97. CFS Test

The ontology should support:

CFS
    contains
Motor
Sensor
Buffer
Material Path
Controller

CFS
    provides_capability
Material Selection

CFS
    interfaces_with
Printer

while allowing its internal structure to remain visible.

98. LowRider Test

The ontology should support:

Axes
Actuators
Motors
Squaring
Tool
Workholding
CNC Process
Operations
Firmware

This tests that process and machine structure are not specific to additive manufacturing.

99. SST1200es Test

The ontology should support the difference between:

Original machine architecture

and:

Retrofit architecture

while preserving the identity of the physical machine.

This is especially important for firmware and controller independence.

100. Current O0.1 Gaps

The following are intentionally unresolved or only partially resolved:

Exact Property model
Exact Unit model
Relationship cardinalities
Relationship context model
Temporal validity
Detailed provenance model
Formal State / Mode model
Formal Event model
Formal Flow model
Formal Signal model
Formal Channel model
Formal Interface model
Detailed Process model
Detailed Calibration model
Detailed Controller Resource model
Firmware Capability model
Formal Evaluation Rule model
Knowledge Graph representation
Persistence schema

These are not failures.

They are areas where additional evidence is still needed.

101. Deferred Universal Concepts

The following should not be promoted into universal concepts solely because they are useful words:

Flow
Signal
Channel
Event
Resource
Interface
State
Device
Part

Each may have valid domain-specific meanings.

The ontology should only unify them when a sufficiently strong semantic case exists.

102. Current Ontology Maturity

Approximate maturity at O0.1:

Area	Maturity
Object / Classification / Role / Aspect	High
Provenance concept	High-level
Machine / Component / Catalog	High
Motion concepts	High-level
Coordinate Frames	High-level
Ports / Connections	High-level
Measurement	High-level
Function vocabulary	High-level
Subsystems	High-level
Relationships	High-level
Control	Medium
Safety	Medium
Controller Resources	Medium
Process	Medium
Firmware Mapping	Medium
Runtime State	Medium
Evaluation	Medium
Formal cardinalities	Early
Formal Property model	Early
Temporal model	Early
Persistence model	Deferred

Maturity describes semantic confidence, not implementation completeness.

103. O0.1 Completion Criteria

O0.1 should be considered complete enough when:

Core concepts have stable working definitions.
Major non-equivalences are documented.
Core relationships are identified.
Important relationship constraints are understood sufficiently for early implementation.
Provenance requirements are clear enough to preserve future compatibility.
Major machine stress cases have been tested conceptually.
Major contradictions are resolved or explicitly documented.
Implementation handoffs can reference a coherent ontology baseline.

O0.1 does not require:

a final database schema;
a complete graph implementation;
complete firmware mappings;
complete safety analysis;
complete process modeling;
complete engineering evaluation.
104. O0.1 to R0.2

Once the foundational ontology is stable enough, the next research stage can deepen the domains that currently remain high-level.

Potential R0.2 subjects include:

Port / Interface Semantics
Connection / Path Semantics
Machine Component Modeling
Coordinate / Kinematic Refinement
Controller Resources
Control
Measurement / Calibration
Process / Tooling
Safety
Engineering Evaluation
Firmware Mapping

The exact sequence should be driven by implementation evidence and stress cases.

105. O0.1 Relationship to v0.2

The current visual connection implementation should use O0.1 concepts conservatively.

The most immediately relevant concepts are:

Object
Machine Component
Port
Connection
Property
Relationship
Compatibility
Visual Model
Visual Connection

The implementation should prove these concepts without pretending that every unresolved ontology detail has already been finalized.

106. Ontology Change Rule

When new evidence challenges O0.1:

Identify the semantic conflict.
Determine whether an existing concept is insufficient.
Test the proposed change against stress cases.
Research relevant standards where appropriate.
Record the decision.
Update O0.1 only when justified.
Preserve significant historical changes.
Update implementation handoffs when affected.

The ontology should evolve deliberately rather than through accidental implementation drift.

107. Final O0.1 Principle

The purpose of O0.1 is not to produce the smallest possible ontology.

It is to produce the smallest semantic foundation that preserves the engineering distinctions needed to describe real machines.

The guiding rule is:

Prefer a meaningful distinction supported by engineering evidence over a convenient abstraction that erases important machine behavior.

At the same time:

Do not create a new concept merely because two words are different.

The ontology should continue to grow from evidence, stress cases, standards, and actual implementation needs.