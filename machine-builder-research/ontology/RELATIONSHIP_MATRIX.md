# Machine Builder Relationship Matrix

## 1. Purpose

This document defines the current working vocabulary of semantic relationships in the Machine Builder ontology.

The purpose is to prevent relationships from becoming an unstructured collection of generic links such as:

```text
Object A → Object B

A useful machine model must explain what the relationship means.

For each relationship, the ontology should eventually define:

source type;
target type;
semantic meaning;
direction;
multiplicity;
whether it is physical, logical, functional, structural, or contextual;
allowable properties;
provenance requirements;
whether it can be derived;
relevant constraints;
relevant standards or evidence.

This document records the current semantic direction. Exact cardinalities and formal constraints remain subject to refinement.

2. Relationship Design Principles
2.1 Relationships Carry Meaning

A relationship is not merely an edge in a graph.

For example:

Motor → Axis

is incomplete without knowing whether the intended meaning is:

drives;
participates_in;
mounted_on;
associated_with;
mechanically_coupled_to;
maps_to.

The relationship type carries the engineering meaning.

2.2 Direction Matters Where Meaning Requires It

Some relationships are inherently directional.

Examples:

Sensor → measures → Measurand
Controller → owns → Resource
Object → derived_from → Evidence
Firmware Term → maps_to → Canonical Concept

Other relationships may be physically symmetric or can have inverse representations.

2.3 Relationship Inverses Should Be Deliberate

An inverse may be useful for querying.

Examples:

Machine contains Component
Component is_part_of Machine

However, inverse terms should not automatically become independent semantic relationships if one can be derived from the other.

The ontology should avoid unnecessary duplication.

2.4 Relationship Multiplicity Must Not Be Assumed

Many important relationships are many-to-many.

Examples:

Many Motors ↔ One Axis
One Sensor ↔ Many Consumers
One Controller ↔ Many Resources
One Function ↔ Many Implementations
Many Physical Connections ↔ One Logical Mapping

Cardinality must therefore be established per relationship.

2.5 Context May Be Required

Some relationships are only meaningful within a context.

For example:

Motor → has_role → Z-axis actuator

is machine-specific.

The same motor may participate differently in another machine.

Context may therefore include:

Machine;
Subsystem;
Process;
Configuration;
Time/version;
Operating mode.
3. Relationship Categories

Current relationships can be grouped into several broad categories.

Structural
    contains
    part_of

Classification / Context
    classified_as
    has_role
    applies_to

Physical
    mounted_on
    mechanically_coupled_to
    physically_connected_to

Connectivity
    connects_to
    interfaces_with
    linked_to

Motion / Kinematics
    participates_in
    drives
    constrains
    transforms_motion_of

Measurement
    measures
    produces_measurement
    consumes_measurement

Functional
    performs
    provides_capability
    implements
    realizes

Control
    controls
    commanded_by
    feedback_from
    feeds
    regulates

Process
    part_of_process
    precedes
    follows
    requires
    produces_result

Tooling
    mounts_tool
    used_by
    performs_process_on

Controller / Resources
    has_resource
    assigned_to
    mapped_to

Firmware
    maps_to
    implements
    generated_from
    parsed_from

Evidence / Provenance
    supported_by
    derived_from
    inferred_from
    contradicts
    supersedes

Coordinate Systems
    has_parent_frame
    transformed_by
    referenced_by

Safety
    protects
    monitored_by
    triggers
    realizes_safety_function

Engineering Evaluation
    constrained_by
    evaluated_by
    satisfies
    violates

Not every listed relationship is finalized.

Some remain candidates requiring additional testing.

4. Structural Relationships
4.1 contains
Meaning

Indicates structural containment of one entity within another.

Examples:

Machine contains Subsystem
Subsystem contains Machine Component
Toolhead contains Sensor
Controller contains Controller Resource
Typical source
Machine
Subsystem
Assembly
Controller
Toolhead
Typical target
Subsystem
Machine Component
Resource
Assembly
Nature

Structural.

Inverse

part_of may be used as a derived inverse.

Notes

Containment does not necessarily imply:

physical enclosure;
ownership;
electrical connection;
functional dependency.

Those meanings should remain separate.

4.2 part_of
Meaning

Indicates membership in a larger structure.

Examples:

Motor part_of Extruder Assembly
Subsystem part_of Machine
Pin part_of Connector
Notes

Whether part_of and contains are formal inverse relationships should be finalized during cardinality/schema work.

5. Classification and Context Relationships
5.1 classified_as
Meaning

Associates an Object with a Classification.

Example:

Motor A
    classified_as
Stepper Motor
Nature

Semantic classification.

Distinct from

has_role

Classification describes what something is.

Role describes how it participates.

5.2 has_role
Meaning

Associates an Object with a contextual Role.

Example:

Motor A
    has_role
Z-axis actuator
Context

Normally machine- or system-specific.

Important distinction
classified_as = Stepper Motor
has_role = Z-axis actuator

The classification can remain constant while the role changes.

5.3 applies_to
Meaning

Associates a rule, constraint, standard requirement, property, or other contextual definition with an entity or context.

Examples:

Standard Requirement applies_to Machine Type
Firmware Mapping applies_to Firmware Version
Constraint applies_to Controller Resource
Status

Candidate relationship requiring further refinement.

6. Physical Relationships
6.1 mounted_on
Meaning

Indicates physical mounting or attachment.

Examples:

Motor mounted_on Gantry
Tool mounted_on Carriage
Controller mounted_on Machine Frame
Distinct from

contains

A mounted object is not necessarily structurally contained.

6.2 mechanically_coupled_to
Meaning

Indicates that two entities participate in a mechanical transmission or coupling.

Examples:

Motor mechanically_coupled_to Pulley
Motor mechanically_coupled_to Screw
Motor mechanically_coupled_to Joint
Importance

This relationship is useful for distinguishing mechanical transmission from logical motion assignment.

6.3 physically_connected_to
Meaning

Indicates a physical connection between entities.

Examples:

Wire physically_connected_to Connector Pin
Tube physically_connected_to Fitting
Cable physically_connected_to Port
Notes

The exact treatment of wires, paths, harnesses, and ports remains under refinement.

7. Connectivity Relationships
7.1 connects_to
Meaning

Indicates that compatible endpoints or interfaces are connected.

Example:

Port A connects_to Port B
Domain

Potentially:

electrical;
signal;
communication;
mechanical;
material;
fluid;
logical.
Notes

Domain should be explicit rather than inferred only from endpoint appearance.

7.2 interfaces_with
Meaning

Indicates that two entities interact through an interface.

Examples:

Toolhead interfaces_with Controller
Subsystem interfaces_with Machine
Firmware interfaces_with Controller
Distinction

interfaces_with is broader than connects_to.

An interface may exist even when a specific physical connection is not being modeled.

7.3 linked_to
Meaning

A deliberately generic relationship indicating association where a more specific relationship has not yet been established.

Warning

This relationship should be used sparingly.

It must not become a substitute for defining the real semantic relationship.

Status

Candidate / temporary modeling aid.

8. Motion and Kinematic Relationships
8.1 participates_in
Meaning

Indicates that an Object contributes to a larger behavior, axis, function, process, or mechanism.

Examples:

Motor participates_in Z Axis
Sensor participates_in Homing Function
Actuator participates_in Motion Function
Subsystem participates_in Printing Process
Importance

This is intentionally broader than drives.

It allows an element to contribute without claiming a specific direct control relationship.

8.2 drives
Meaning

Indicates that an actuator or drive produces or controls motion or another physical effect in a target.

Examples:

Drive drives Motor
Motor drives Screw
Actuator drives Joint
Caution

The exact source/target semantics need to be finalized.

In some systems "drive" refers to the controller electronics rather than the motor itself.

Machine Builder must avoid silently importing one domain's usage into another.

8.3 constrains
Meaning

Indicates that one entity limits or defines the allowed behavior or motion of another.

Examples:

Joint constrains Link Motion
Mechanical Stop constrains Axis travel
Guide constrains Carriage motion
Status

Candidate requiring additional kinematic stress testing.

8.4 transforms_motion_of
Meaning

Indicates that one mechanism transforms the motion relationship of another.

Examples:

CoreXY Kinematic System transforms_motion_of Motor Pair
Gear Train transforms_motion_of Motor
Belt System transforms_motion_of Motor
Status

Candidate.

9. Measurement Relationships
9.1 measures
Meaning

Indicates that a Sensor or measurement system obtains information about a Measurand.

Example:

Thermistor measures Temperature
Encoder measures Position
Load Cell measures Force
Important distinction

The relationship points toward the Measurand, not necessarily toward a numeric Measurement Result.

9.2 produces_measurement
Meaning

Associates a Sensor or Measurement System with the Measurement or Measurement Result it produces.

Example:

Temperature Sensor produces_measurement Temperature Result
Status

Candidate distinction between Measurement and Measurement Result remains under refinement.

9.3 consumes_measurement
Meaning

Indicates that a Function, Control Loop, Diagnostic System, or other entity uses a Measurement Result.

Example:

Temperature Control Function consumes_measurement Temperature Result
Notes

This relationship is useful for representing fan-out from one measurement source.

10. Functional Relationships
10.1 performs
Meaning

Indicates that an entity performs or carries out a Function, Operation, Task, or Action.

Examples:

Subsystem performs Function
Controller performs Control Function
Operation performs Action
Caution

Because "perform" has broad meanings, exact source/target constraints should be defined carefully.

10.2 provides_capability
Meaning

Associates an entity with a Capability it possesses.

Example:

CFS provides_capability Automatic Material Selection
Controller provides_capability Closed-loop Motion Control
Distinct from

implements

Capability describes ability.

Implementation describes realization.

10.3 implements
Meaning

Indicates that an entity realizes a Function, Requirement, Interface, or other abstract specification.

Examples:

Firmware implements Control Function
Hardware implements Safety Function
Controller implements Communication Interface
Caution

The target concept must be explicit.

"Implements" should not become a generic synonym for "associated with."

10.4 realizes
Meaning

Indicates that an implementation or concrete structure realizes an abstract requirement, function, or architecture.

This may overlap with implements.

Status

Candidate relationship requiring terminology cleanup.

The project should eventually choose whether both terms are necessary.

11. Control Relationships
11.1 controls
Meaning

Indicates that one entity determines or regulates behavior of another.

Examples:

Control Function controls Heater
Controller controls Drive
Safety Function controls Motion Enable
Notes

controls is intentionally broader than drives.

11.2 commanded_by
Meaning

Indicates that a target receives command intent from a source.

Example:

Motor commanded_by Controller
Action commanded_by Control Function
Important distinction

A command is not necessarily the same as a signal.

commanded_by expresses intent/control authority.

11.3 feedback_from
Meaning

Indicates that a control function receives feedback derived from another entity.

Example:

Temperature Control Function
    feedback_from
Temperature Measurement
Notes

This should normally represent the control relationship, not physical wiring.

11.4 feeds
Meaning

Indicates that one information-producing entity supplies information to another consumer.

Examples:

Measurement Result feeds Control Function
Sensor Result feeds Diagnostic Function
Signal feeds Controller
Caution

feeds is intentionally broad and should not replace domain-specific relationships where exact semantics matter.

11.5 regulates
Meaning

Indicates that one Function or Control System regulates a target quantity or behavior.

Example:

Temperature Control Function regulates Build Temperature
Status

Candidate relationship requiring formal control vocabulary refinement.

12. Process Relationships
12.1 part_of_process
Meaning

Indicates that an Operation, Action, Task, or Function participates in a Process.

Example:

Extrusion Operation part_of_process Additive Manufacturing Process
12.2 precedes
Meaning

Indicates ordering between process activities.

Example:

Heat Build Volume precedes Begin Extrusion
Notes

Temporal ordering may need a separate formal mechanism later.

12.3 follows
Meaning

Inverse of precedes.

It may be derived rather than independently stored.

12.4 requires
Meaning

Indicates that one entity depends on another prerequisite, capability, resource, condition, or result.

Examples:

Operation requires Heated Bed
Function requires Controller Resource
Process requires Material
Caution

requires is broad and may require specialized subrelationships in the future.

12.5 produces_result
Meaning

Indicates that an Operation, Process, Measurement, or other activity produces a result.

Examples:

Measurement produces_result Measurement Result
Machining Operation produces_result Finished Feature
Calibration Procedure produces_result Calibration Value
13. Tooling Relationships
13.1 mounts_tool
Meaning

Indicates that an entity provides a mounting relationship for a Tool.

Example:

Toolhead mounts_tool Extrusion Tool
Carriage mounts_tool Probe
13.2 used_by
Meaning

Indicates that a Tool, Resource, or Capability is used by another entity or process.

Examples:

Tool used_by Operation
Controller Resource used_by Function
Measurement Equipment used_by Calibration Procedure
Caution

This relationship is broad and should not replace more precise semantic relationships.

13.3 performs_process_on
Meaning

Indicates that a Tool or machine operation acts on a workpiece, material, or object as part of a process.

Example:

End Mill performs_process_on Workpiece
Extrusion Tool performs_process_on Material
Status

Candidate for process ontology development.

14. Controller and Resource Relationships
14.1 has_resource
Meaning

Associates a Controller with a resource it provides.

Example:

Controller has_resource Driver 2
Controller has_resource ADC 3
Controller has_resource CAN Interface
14.2 assigned_to
Meaning

Indicates that a resource or component has been allocated to a specific machine role or function.

Examples:

Driver 2 assigned_to Z Axis
GPIO 17 assigned_to Filament Sensor
Context

Usually configuration-specific.

14.3 mapped_to
Meaning

Associates one representation or resource with another through an explicit mapping.

Examples:

Controller Resource mapped_to Firmware Pin
Canonical Axis mapped_to Firmware Axis
Physical Pin mapped_to Logical Signal
Importance

This is a central translation relationship.

15. Firmware Relationships
15.1 maps_to
Meaning

Indicates semantic correspondence between a canonical concept and a firmware-specific representation.

Examples:

Canonical Z Axis maps_to RRF Z Axis
Canonical Driver Resource maps_to RRF Driver 2
Canonical motion scale maps_to M92 parameter
15.2 implements

Firmware may implement canonical Functions, Control Functions, or Safety Functions.

Example:

Firmware implements Control Function

However, the exact implementation claim must be supported by evidence.

15.3 generated_from
Meaning

Indicates that an output representation was generated from canonical or other source information.

Example:

Firmware Configuration generated_from Canonical Machine Model

This is distinct from maps_to.

maps_to describes semantic correspondence.

generated_from describes production lineage.

15.4 parsed_from
Meaning

Indicates that an interpreted semantic representation originated from a particular external source.

Example:

Canonical Fact parsed_from Firmware Configuration

This is useful for provenance and reverse engineering.

16. Evidence and Provenance Relationships
16.1 supported_by
Meaning

Indicates that evidence supports a Fact, Relationship, Classification, or Interpretation.

Example:

Motor current = 1.5 A
    supported_by
Manufacturer Datasheet
16.2 derived_from
Meaning

Indicates that a result is mathematically or logically derived from other information.

Example:

Steps/mm derived_from
    steps/revolution
    microstepping
    pulley geometry
16.3 inferred_from
Meaning

Indicates that an interpretation was inferred from evidence rather than directly stated.

Example:

Motor role = Z-axis actuator
    inferred_from
    wiring + physical observation + firmware mapping
16.4 contradicts
Meaning

Indicates that one piece of evidence, claim, or result conflicts with another.

Example:

Datasheet A contradicts Measurement B
Importance

Contradictions must not silently overwrite information.

They should remain visible until resolved.

16.5 supersedes
Meaning

Indicates that a newer or more authoritative representation replaces an earlier applicable representation.

Example:

New Product Revision supersedes Older Product Revision
Caution

Supersession does not mean the earlier evidence should be deleted.

17. Coordinate Relationships
17.1 has_parent_frame
Meaning

Associates a Coordinate Frame with its parent frame.

Example:

Tool Frame has_parent_frame Machine Frame
17.2 transformed_by
Meaning

Associates an Object or Coordinate Frame with a Transform used to relate it to another frame.

Example:

Tool Frame transformed_by Tool Offset
Status

Exact transform modeling remains under development.

17.3 referenced_by
Meaning

Indicates that an object, position, measurement, or operation is expressed relative to a Coordinate Frame.

Example:

Tool Position referenced_by Tool Frame
Caution

This relationship may eventually be represented more formally as a property of a position/measurement rather than as a generic relationship.

18. Safety Relationships
18.1 protects
Meaning

Associates a Guard, Safety Function, or protective mechanism with a hazard, area, or machine behavior it protects against.

Example:

Guard protects Hazardous Motion Zone
Safety Function protects against Unexpected Startup
18.2 monitored_by
Meaning

Indicates that an Object or condition is monitored by a sensing or safety mechanism.

Example:

Guard State monitored_by Interlock
Temperature monitored_by Safety Sensor
18.3 triggers
Meaning

Indicates that an event, condition, or device initiates an Action, Function, or safety response.

Example:

Guard Open triggers Safety Stop
Temperature Fault triggers Heater Shutdown
18.4 realizes_safety_function
Meaning

Indicates that a concrete implementation realizes a Safety Function.

Example:

Safety Relay + Interlock realizes_safety_function Emergency Stop
Status

Candidate; may later be represented through a more general implements relationship with safety-specific typing.

19. Engineering Evaluation Relationships
19.1 constrained_by
Meaning

Indicates that an entity is subject to a Constraint.

Example:

Motor Driver constrained_by Maximum Current Rating
Wire constrained_by Ampacity Requirement
Controller constrained_by Available Resources
19.2 evaluated_by
Meaning

Associates a machine element or requirement with an Evaluation Method or Evaluation Result.

Example:

Wire evaluated_by Voltage Drop Calculation
Port Pair evaluated_by Compatibility Rule
19.3 satisfies
Meaning

Indicates that an entity or design satisfies a Requirement or Constraint.

Example:

Controller satisfies Motion Resource Requirement
Safety Implementation satisfies Risk Reduction Requirement
Caution

This should only be asserted when the evidence and applicable evaluation are sufficient.

19.4 violates
Meaning

Indicates that an entity fails to satisfy a known Requirement or Constraint.

Example:

Driver assignment violates Current Limit

This should normally be an evaluated result rather than a casual assertion.

20. Relationship Properties

Relationships may themselves require properties.

Examples:

Connection
Connection:
    domain
    direction
    voltage
    current
    protocol
    physical_path
    provenance
Mechanical Coupling
Mechanical Coupling:
    ratio
    direction
    efficiency
    backlash
    provenance
Role
Role:
    context
    start
    end
    confidence
    provenance
Mapping
Mapping:
    firmware_version
    transformation
    conditions
    confidence
    provenance

This is one reason relationships should not be reduced to bare two-node links.

21. Relationship Context

Some relationships require a context object or contextual properties.

For example:

Motor has_role Z-axis actuator

may only be valid:

Machine = Promega
Configuration = current machine configuration
Time = installation period

Similarly:

Driver 2 assigned_to Z Axis

may depend on:

Controller Revision
Firmware Version
Configuration Version

The architecture should support contextual validity without forcing every relationship to become a separate object prematurely.

22. Relationship Provenance

Important relationships need provenance just like Properties.

Example:

Motor participates_in Z Axis

Source:
    physical inspection

Method:
    observed belt connection + firmware configuration

Confidence:
    high

Date:
    2026-...

This is especially important for inferred relationships.

23. Relationship Confidence

Relationship confidence may differ from property confidence.

Example:

Motor:
    steps/revolution = 200
    confidence = high

Motor:
    participates_in Z Axis
    confidence = medium

The motor specification may be documented while the machine role is inferred.

The ontology should therefore permit confidence at the relationship level.

24. Relationship Lifecycle

Relationships may change over time.

Example:

Motor A participates_in Z Axis

followed by a machine modification:

Motor A removed
Motor B participates_in Z Axis

The architecture should eventually support historical validity rather than overwriting the previous fact without trace.

Potential context:

valid_from
valid_to
configuration_version
machine_revision

Exact temporal modeling is deferred.

25. Relationship Cardinality Candidates

The following are working expectations, not final schema constraints.

Relationship	Typical Source	Typical Target	Expected Cardinality
contains	Machine/Subsystem	Object	One-to-many
classified_as	Object	Classification	Many-to-many possible
has_role	Object	Role	Many-to-many
mounted_on	Object	Object	Many-to-one or many-to-many
connects_to	Port	Port	Many-to-many
measures	Sensor	Measurand	Many-to-many
participates_in	Object	Axis/Function/Process	Many-to-many
drives	Drive/Actuator	Target	One-to-many / many-to-many
has_resource	Controller	Resource	One-to-many
assigned_to	Resource	Role/Function/Axis	Many-to-many
maps_to	Entity	Entity	Many-to-many
derived_from	Result	Source	Many-to-many
supported_by	Fact	Evidence	Many-to-many
has_parent_frame	Frame	Frame	Many-to-one
requires	Entity	Requirement/Resource	Many-to-many
implements	Entity	Function/Requirement	Many-to-many

These should be validated against stress cases before becoming schema constraints.

26. Relationships That Should Not Be Generic

The following should not be replaced by a generic related_to relationship in the canonical model:

measures
drives
mounted_on
contains
maps_to
derived_from
implements
controls
connects_to

A generic relationship may be useful for exploratory data or incomplete evidence, but canonical semantics should use the most specific established relationship available.

27. Candidate Relationship Consolidation

Several current relationships may eventually collapse into broader patterns.

Potential consolidation candidates include:

implements
realizes
realizes_safety_function

connected_to
physically_connected_to
interfaces_with

feeds
consumes_measurement
feedback_from

maps_to
mapped_to

derived_from
inferred_from

These should not be merged yet.

The distinction should be preserved until actual stress cases and standards research demonstrate whether they carry genuinely different semantics.

28. Relationship Stress Tests

Relationships should be tested against difficult machine architectures.

CoreXY

Must support:

Motor A participates_in X
Motor A participates_in Y
Motor B participates_in X
Motor B participates_in Y

without falsely claiming that each motor is independently an X or Y motor.

SV08

Must support:

Motor Z1 participates_in Z Axis
Motor Z2 participates_in Z Axis
Motor Z3 participates_in Z Axis
Motor Z4 participates_in Z Axis

while preserving the distinct physical actuators.

CFS

Must support:

CFS contains Motors
CFS contains Sensors
CFS contains Material Paths
CFS interfaces_with Printer
CFS provides_capability Material Selection
IR3

Must support:

Motor participates_in Belt Motion
Coordinate Frame transformed_by Kinematic Transform

without pretending the physical machine is a conventional Cartesian mechanism.

Tool Changer

Must support:

Carriage mounts_tool Tool
Tool used_by Operation
Toolhead interfaces_with Tool
Closed Loop

Must support:

Sensor produces_measurement Measurement Result
Measurement Result feeds Control Function
Control Function controls Actuator
CNC

Must support:

Tool used_by Operation
Operation part_of_process Process
Tool performs_process_on Workpiece
29. Relationship Questions Still Open

The following questions remain intentionally open.

29.1 Should connects_to be universal?

A universal connectivity relationship may be convenient, but electrical, mechanical, material, and logical connections have different constraints.

29.2 Should paths be explicit objects?

A physical path may require its own identity when routing, length, material, or topology matters.

29.3 Should feeds and consumes be inverse relationships?

Likely, but the formal treatment has not yet been finalized.

29.4 Should implements and realizes be merged?

This requires clearer distinctions across systems engineering, software, and safety contexts.

29.5 How should temporal validity work?

Relationships can change when hardware is modified, firmware changes, or configurations change.

29.6 How should relationship context be represented?

Some relationships depend on:

machine;
subsystem;
configuration;
firmware version;
time;
operating mode.
29.7 Which relationships require first-class relationship objects?

Some relationships have enough properties that treating them as bare edges may become insufficient.

30. Current Relationship Architecture

The current direction can be summarized as:

Object
  │
  ├── classified_as ─────→ Classification
  │
  ├── has_role ──────────→ Role
  │
  ├── has_property ──────→ Property
  │
  ├── contains ──────────→ Object
  │
  └── [typed relationships]
           │
           ├── physical
           ├── logical
           ├── functional
           ├── control
           ├── process
           ├── safety
           ├── coordinate
           └── provenance

This allows the machine to be represented as an interconnected semantic system without reducing every relationship to the same generic edge.

31. Relationship Modeling Rule

When adding a relationship, ask:

What exactly does this relationship mean?

Why is the source related to the target?

Is the relationship directional?

What is its domain?

What is its inverse, if any?

What are the possible cardinalities?

What properties belong to the relationship?

Can the relationship be inferred?

What evidence establishes it?

Does the relationship remain valid across machine configurations?

Does a relevant standard support this distinction?

If these questions cannot yet be answered, the relationship should remain explicitly provisional.

32. Summary

The Machine Builder ontology treats relationships as first-class semantic information.

The current model requires relationships to distinguish:

structure;
classification;
contextual roles;
physical attachment;
physical connectivity;
logical mapping;
motion and kinematics;
measurement;
control;
process;
tooling;
controller resources;
firmware mappings;
evidence;
coordinates;
safety;
engineering evaluation.

The project deliberately avoids a universal related_to model because real machine engineering depends on the meaning of each relationship.

The immediate goal is not to finalize every relationship.

The goal is to establish a vocabulary strong enough to continue ontology development without losing important engineering distinctions.