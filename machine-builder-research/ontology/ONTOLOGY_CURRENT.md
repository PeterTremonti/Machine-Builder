# Machine Builder Current Ontology

## 1. Purpose

This document records the current working ontology of Machine Builder as a consolidated snapshot.

It is intended to answer:

> What does Machine Builder currently believe the machine model consists of?

This document is not a permanent final ontology.

It is a current-state reference that should change when major ontology decisions are made.

Historical reasoning, rejected concepts, and detailed research belong in the appropriate decision, research, and history files.

---

## 2. Current Ontology Philosophy

Machine Builder models machines through multiple complementary semantic dimensions rather than a single universal inheritance hierarchy.

The central pattern is:

```text
Object
├── Classification
├── Role
├── Aspect
├── Property
├── Relationship
└── Provenance

Specialized engineering concepts then participate through typed relationships.

The ontology is intended to represent:

what exists;
what kind of thing it is;
what role it serves;
how it is structured;
what it connects to;
what it does;
what it can do;
how it is controlled;
how it is measured;
how it participates in processes;
what constraints apply;
where the information came from.
3. Core Semantic Foundation
3.1 Object

An Object is an identifiable entity represented by the model.

Examples:

Machine
Motor
Sensor
Controller
Axis
Joint
Subsystem
Port
Coordinate Frame
Tool

An Object may participate in many relationships and may be viewed through multiple engineering aspects.

3.2 Classification

Classification identifies what kind or category of thing an Object is.

Examples:

Stepper Motor
Temperature Sensor
Controller
Servo Drive
Guard
Tool
Coordinate Frame

Classification is distinct from Role.

3.3 Role

Role describes how an Object participates in a specific context.

Examples:

Z-axis actuator
Extruder actuator
Filament feeder
Bed-temperature sensor
Safety interlock device

Role is contextual.

A single Object can participate in different Roles in different machine or system contexts.

3.4 Aspect

Aspect provides an engineering viewpoint or structuring dimension.

Relevant aspects may include:

Physical
Electrical
Logical
Functional
Control
Safety
Maintenance

IEC 81346 is an important architectural influence.

Aspect is not intended to duplicate Classification.

3.5 Property

A Property describes a characteristic or value associated with an Object or, where justified, a Relationship.

Examples:

current = 1.5 A
steps_per_revolution = 200
shaft_diameter = 5 mm
length = 350 mm

Important properties may require:

unit;
source;
uncertainty;
validity;
confidence;
method;
version context.
3.6 Relationship

A Relationship is a typed semantic association between modeled entities.

Examples:

contains
part_of
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

Relationships are first-class information.

3.7 Provenance

Provenance records where and how information was established.

Potential information includes:

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

Properties;
Relationships;
Classifications;
Roles;
Derived results;
Evaluations.
4. Machine Structure
4.1 Machine

A Machine is the primary system of interest.

A Machine may contain:

subsystems;
machine components;
controllers;
tools;
functions;
processes;
interfaces;
safety structures;
coordinate frames;
state.

Machine is intentionally generic enough to support:

3D printers;
CNC machines;
routers;
robots;
laser systems;
hybrid machines;
industrial equipment.
4.2 Machine Component

A Machine Component is an actual machine-specific occurrence of a physical component.

Examples:

the physical Z motor installed in a Promega
the controller board installed in an Ender 3
a specific filament sensor installed in a CFS

Machine Component is distinct from Catalog Product.

4.3 Catalog Product

A Catalog Product is an external product definition.

Examples:

motor model
controller board model
linear rail product
connector product

Catalog Products are not automatically installed machine components.

4.4 Product Version

A Product Version identifies a particular revision or variant of a Catalog Product.

This allows the model to distinguish products whose:

specifications;
behavior;
pinout;
mechanical dimensions;
firmware support

may differ between revisions.

4.5 Subsystem

A Subsystem is a bounded portion of a Machine that may contain its own:

components;
functions;
capabilities;
resources;
state;
control;
interfaces;
communication.

Subsystems may contain other Subsystems.

5. Physical and Mechanical Ontology
5.1 Axis

An Axis represents machine motion or coordinate semantics.

Examples:

X
Y
Z
A
B
C

Axis is not equivalent to Motor.

An Axis may be produced by:

one actuator;
multiple actuators;
coupled actuators;
a kinematic transformation.
5.2 Joint

A Joint represents a constrained mechanical relationship that permits relative motion.

A Joint may be:

active;
passive;
constrained;
actuated.

Joint is not synonymous with Axis.

5.3 Link

A Link represents a relatively rigid physical element in a mechanical structure.

It may connect or separate joints.

The exact formal treatment may vary by machine architecture.

5.4 Actuator

An Actuator is an element capable of producing a controlled physical effect.

An Actuator may contain or depend upon:

motor;
drive;
transmission;
mechanical interface.
5.5 Motor

A Motor is an electromechanical energy-conversion device that produces mechanical motion.

Examples:

stepper;
servo;
DC;
BLDC.

Motor is not automatically the full Actuator or Drive.

5.6 Drive

A Drive is a control system or component responsible for controlling a motor or actuator.

Depending on architecture, it may provide:

power conversion;
current control;
velocity control;
position control;
feedback processing;
communication.
5.7 Kinematic Relationship

A Kinematic Relationship expresses how motions are coupled or transformed.

Examples:

CoreXY;
belt transformations;
gears;
leadscrews;
robot mechanisms;
coordinated rotary systems.

The ontology must support many-to-many motion relationships.

6. Coordinate Ontology
6.1 Coordinate Frame

A Coordinate Frame is a reference coordinate system with a defined engineering meaning.

Examples:

Machine Frame
Work Frame
Tool Frame
Object Frame
Camera Frame
Task Frame

A Coordinate Frame may have:

parent frame;
transform;
semantic role;
reference object.
6.2 Transform

A Transform expresses the mathematical relationship between coordinate frames.

Potential components include:

translation;
rotation;
scale where appropriate;
homogeneous transformation;
other domain-specific mappings.
6.3 Canvas Coordinate

Canvas Coordinate belongs to the visual model.

It must not be treated as physical machine position.

7. Interface and Connectivity Ontology
7.1 Port

A Port is a semantic interface endpoint exposed by an Object.

Potential domains include:

Electrical
Signal
Communication
Mechanical
Material
Fluid
Logical

Ports are central to the visual builder and future compatibility system.

7.2 Connector

A Connector is a physical interface structure that may contain multiple Pins.

7.3 Pin

A Pin is a discrete contact or terminal position associated with an electrical connector or similar physical interface.

Pin and Port are distinct concepts.

7.4 Connection

A Connection represents a semantic association between compatible endpoints.

A Connection may exist within different domains:

electrical;
signal;
communication;
mechanical;
material;
fluid;
logical.

Connection is distinct from its visual representation.

7.5 Physical Connection

A Physical Connection represents an actual physical attachment or route.

Examples:

Wire
Cable
Tube
Mechanical coupling
Material path
7.6 Logical Mapping

A Logical Mapping relates logical meaning to implementation or physical representation.

Examples:

Temperature Signal
    maps_to
Controller Input

Canonical Axis
    maps_to
Firmware Axis

Logical Heater Enable
    maps_to
Physical Pin

Physical Connection and Logical Mapping remain distinct.

7.7 Path

Path represents a physical/topological route.

A Path does not automatically imply active Flow.

Potential uses include:

material routing;
fluid routing;
cable routing;
communication paths;
mechanical transmission.
7.8 Harness

A Harness is an organized collection of routed physical wires, cables, tubing, or related elements.

Harnesses may contain sub-harnesses.

8. Measurement Ontology
8.1 Sensor

A Sensor is a physical or functional element involved in obtaining information about a quantity or condition.

8.2 Measurand

A Measurand is the quantity intended to be measured.

Examples:

Temperature
Position
Pressure
Force
Distance
Current
8.3 Measurement

Measurement is the activity or process of obtaining information about a Measurand.

8.4 Measurement Result

Measurement Result is the information produced by a measurement.

It may include:

Value
Unit
Uncertainty
Time
Conditions
Method
Provenance
8.5 Feedback

Feedback is a control relationship in which information from a Measurement Result influences control behavior.

Feedback is not a subtype of Sensor.

9. Capability and Function Ontology
9.1 Capability

Capability represents an ability possessed by an Object, Machine, or Subsystem.

Examples:

Can heat build volume
Can perform tool changing
Can measure temperature
Can perform closed-loop motion control
9.2 Function

Function represents a defined machine or subsystem behavior/service independent of one particular execution instance, procedure, command, or firmware syntax.

Examples:

Maintain Build Temperature
Feed Material
Measure Temperature
Move Tool
Control Spindle Speed
Prevent Unexpected Restart

Function is not a universal parent for all process/execution concepts.

9.3 Task

Task represents an intended body of work or objective.

Examples:

Print Part
Machine Pocket
Inspect Part
Change Tool
9.4 Process

Process represents an organized activity through which an intended result is achieved.

Examples:

Additive Manufacturing
Machining
Inspection
Material Loading

The process ontology remains under refinement.

9.5 Operation

Operation represents a bounded executable work unit.

Examples:

Heat Build Volume
Probe Surface
Extrude Material
Change Tool
Machine Pocket
9.6 Action

Action represents a discrete executable behavior or change.

Examples:

Enable Heater
Advance Filament
Stop Motor
Trigger Probe
Open Valve
9.7 Procedure

Procedure represents a specified way of performing an activity.

Examples:

Z-Probe Calibration Procedure
Motor Replacement Procedure
Tool Change Procedure

Procedure describes how an activity is carried out.

9.8 Control Function

Control Function is a Function used to regulate machine behavior based on information, commands, or feedback.

Examples:

Temperature Control
Position Control
Pressure Control
Speed Control
9.9 Safety Function

Safety Function is a Function required to achieve or maintain a safe state or reduce risk.

Examples:

Prevent Unexpected Startup
Stop Hazardous Motion When Guard Opens
Emergency Stop

Safety Functions require their own engineering evidence and validation context.

9.10 Control Loop

Control Loop is a structured control arrangement involving some combination of:

Setpoint
Control Function
Control Output
Physical System
Measurement
Feedback

It is not simply another name for Function.

10. Controller Ontology
10.1 Controller

A Controller is a computing or control entity responsible for coordinating one or more machine resources or behaviors.

10.2 Controller Resource

A Controller Resource is a finite resource or capability supplied by a Controller.

Examples:

Motor Driver
GPIO
ADC Channel
PWM
Timer
UART
CAN
Ethernet
Processing Resource
10.3 Firmware

Firmware is software executing on a controller or embedded computing platform.

Firmware is an implementation representation.

10.4 Firmware Term

A Firmware Term has meaning within a particular firmware ecosystem.

Examples:

M584
M92
step_pin
dir_pin
driver section
tool definition

A Firmware Term is not automatically a canonical Machine Builder concept.

10.5 Firmware Mapping

Firmware Mapping describes the relationship between canonical concepts and firmware-specific representations.

Mappings may be:

one-to-one;
one-to-many;
many-to-one;
conditional;
calculated;
version-specific.
11. Configuration and Runtime Ontology
11.1 Configuration

Configuration represents intended setup and operating parameters.

Examples:

Motor Current
Steps per Unit
Axis Mapping
Maximum Velocity
Tool Assignment
11.2 Runtime State

Runtime State represents current machine condition.

Examples:

Axis Homed
Motor Enabled
Temperature = 205 °C
Filament Present
Drive Faulted

Runtime state is separate from Configuration.

11.3 Mode

Mode represents a defined operating context.

Examples may include:

Idle
Manual
Homing
Printing
Fault
Maintenance

The exact State/Mode ontology remains under refinement.

11.4 Fault

Fault represents a detected condition that prevents or disrupts normal operation or requires intervention.

12. Safety Ontology

The current safety structure is:

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
12.1 Hazard

Potential source of harm.

12.2 Risk

Combination of the relevant likelihood and severity associated with potential harm.

12.3 Risk Reduction Requirement

Requirement established to reduce a machine risk.

12.4 Safety-Related Control Implementation

Hardware and/or software implementing a Safety Function.

12.5 Safe State

Defined machine condition in which relevant hazards are adequately controlled within the applicable safety architecture.

Safe State is context-dependent.

12.6 Guard

Physical protective structure intended to prevent or restrict access to hazardous areas.

12.7 Interlock

Device or control relationship used to detect protective conditions and constrain machine operation.

13. Tool and Process Ontology
13.1 Tool

An object used by a machine to perform or support a process.

Examples:

extrusion tool;
cutting tool;
laser;
probe;
dispenser.
13.2 Toolhead

A physical assembly carrying one or more Tools or process elements.

Toolhead may contain:

tools;
sensors;
actuators;
electronics;
cooling;
heating;
mounts.

Toolhead is not automatically identical to Tool.

13.3 Carriage

Mechanical structure supporting or moving a Toolhead, Tool, or other machine element.

13.4 Workholding

Structure used to locate, support, or constrain a workpiece.

Examples:

Build Plate
Vice
Chuck
Clamp
Fixture
14. Evidence Ontology
14.1 Fact

A statement represented as information about an Object, Relationship, Property, or other modeled entity.

14.2 Observation

Information directly obtained from a physical machine or observed behavior.

14.3 Inference

A conclusion derived from evidence but not directly stated.

14.4 Derivation

A calculated or logically produced result from known inputs and a defined method.

14.5 Assumption

An explicitly declared condition temporarily or contextually treated as true for analysis.

14.6 Evidence

Information supporting or contradicting a claim or model element.

14.7 Confidence

An indication of how strongly available evidence supports a conclusion.

Confidence is not the same thing as truth.

15. Engineering Evaluation Ontology
15.1 Constraint

A condition that must be satisfied.

Examples:

Driver current must not exceed rating
Controller must provide required resource
Tool must fit mount
15.2 Compatibility

Degree to which entities or interfaces can work together under specified conditions.

Potential results:

Compatible
Incompatible
Conditionally Compatible
Unknown
15.3 Verification

Determination of whether a defined result or implementation conforms to specified requirements.

15.4 Validation

Determination of whether a system or implementation satisfies its intended purpose or specified validation criteria.

The exact distinction will continue to follow applicable systems-engineering and domain standards.

15.5 Evaluation Result

A derived engineering conclusion.

Possible status values:

PASS
WARNING
RECOMMENDATION
INVALID
UNKNOWN
16. Visual Ontology

The following concepts belong primarily to the application presentation layer rather than the canonical ontology.

Visual Model

Presentation-oriented representation of canonical information.

May contain:

node positions;
sizes;
grouping;
visibility;
routing;
selection;
zoom;
interaction state.
Node

Visual representation of one or more canonical entities.

A canonical Object does not necessarily require exactly one Node.

Visual Connection

Rendered representation of a canonical relationship or Connection.

Canvas

Visual workspace containing Nodes and other presentation elements.

17. Core Relationship Set

The currently important relationship vocabulary includes:

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
requires
produces_result
mounts_tool
used_by
performs_process_on
has_resource
assigned_to
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
constrained_by
evaluated_by
satisfies
violates

Not all of these are fully finalized.

Some remain candidate relationships requiring additional stress testing.

18. Important Relationship Patterns
Structural
Machine
   contains
Subsystem

Subsystem
   contains
Machine Component
Classification and Role
Machine Component
   classified_as
Stepper Motor

Machine Component
   has_role
Z-axis actuator
Motion
Motor
   participates_in
Axis

Motor
   mechanically_coupled_to
Transmission

Actuator
   drives
Joint
Measurement
Sensor
   measures
Measurand

Sensor
   produces_measurement
Measurement Result

Measurement Result
   feeds
Control Function
Control
Control Function
   controls
Actuator

Control Function
   feedback_from
Measurement Result
Connectivity
Port
   connects_to
Port

with additional physical and logical representations where required.

Firmware
Canonical Concept
   maps_to
Firmware Representation
Evidence
Fact
   supported_by
Evidence

Derived Value
   derived_from
Source Values

Inference
   inferred_from
Evidence
Safety
Hazard
   ↓
Risk
   ↓
Risk Reduction Requirement
   ↓
Safety Function
   ↓
Safety-Related Implementation
19. Cardinality Philosophy

The ontology does not assume universal one-to-one relationships.

Examples:

One Axis, Multiple Motors
Motor A ─┐
Motor B ─┼──→ Z Axis
Motor C ─┘
One Motor, Multiple Motion Contributions
Motor A
 ├──→ X contribution
 └──→ Y contribution
One Measurement, Multiple Consumers
Measurement Result
 ├──→ Control
 ├──→ Diagnostics
 ├──→ Logging
 └──→ Safety
One Controller, Many Resources
Controller
 ├── Resource 0
 ├── Resource 1
 ├── Resource 2
 └── ...

Exact cardinalities remain a later schema/constraint task.

20. Current Stress Cases

The current ontology is expected to explain at least:

Promega
SV08
LowRider
IR3
Creality CFS
CoreXY
IDEX
Tool Changers
Closed-Loop Systems
CNC Machines
Industrial Machines

These cases intentionally challenge:

one-axis/one-motor assumptions;
one-controller assumptions;
one-sensor/one-consumer assumptions;
simple Cartesian coordinates;
printer-only tool semantics;
simple linear processes;
firmware-specific ontology;
single-level subsystem structures.
21. CFS Ontology Example

The CFS is an important current example of the ontology working across several domains.

A simplified structure is:

CFS
├── Spool Mechanisms
│   ├── Rewind Motor
│   ├── Filament Sensor
│   └── Feeder Motor
├── Lower Feed Section
│   ├── Filament Sensor
│   └── Feeder Motor
├── Material Paths
├── Buffer
├── Local Controller
└── Communication Interface

Possible semantic relationships include:

CFS
    contains
    Motors

CFS
    contains
    Sensors

CFS
    provides_capability
    Material Selection

CFS
    interfaces_with
    Printer

Feeder Motor
    participates_in
    Material Feeding Function

Filament Sensor
    measures
    Filament Presence

This demonstrates why CFS cannot be reduced to a single "filament feeder" object.

22. Motion Examples
CoreXY
Motor A ──┬──→ X Motion
          └──→ Y Motion

Motor B ──┬──→ X Motion
          └──→ Y Motion

The ontology therefore separates:

Motor
Axis
Kinematic Relationship
Multiple Z Motors
Z Motor 1 ─┐
Z Motor 2 ─┼──→ Z Axis
Z Motor 3 ─┤
Z Motor 4 ─┘

The four motors remain distinct machine components.

The logical Z Axis is also distinct.

Belt Printer

A belt printer may require:

Machine Coordinate Frame
Tool Coordinate Frame
Belt Coordinate / Motion Transform
Kinematic Relationship

This demonstrates why Axis and Coordinate Frame cannot simply be inferred from standard Cartesian assumptions.

23. Measurement Example

A temperature measurement may be represented as:

Temperature Sensor
    classified_as
Thermistor

Thermistor
    measures
Temperature

Temperature Measurement
    produces_result
205 °C

205 °C Measurement Result
    feeds
Temperature Control Function

The same Measurement Result may also:

feed
    Display

feed
    Logging

feed
    Diagnostics
24. Control Example

A temperature control system may be represented as:

Temperature Setpoint
        ↓
Temperature Control Function
        ↓
Heater Control Output
        ↓
Heater
        ↓
Build Volume
        ↓
Temperature Sensor
        ↓
Temperature Measurement Result
        ↓
Feedback
        └────→ Temperature Control Function

This captures the control semantics without depending on whether the implementation uses:

PID;
bang-bang;
firmware macro;
PLC;
dedicated controller;
another control method.
25. Firmware Example

A firmware configuration may contain:

Driver 2 assigned to Z
Steps per unit = 282.7

The canonical interpretation may contain:

Controller Resource
    assigned_to
Z Axis

Z Motion Scale
    has_property
282.7 steps/unit

with provenance:

Source:
    RepRapFirmware configuration

Method:
    Firmware semantic parser

Firmware:
    RepRapFirmware

Version:
    applicable firmware version

The canonical model therefore preserves the engineering meaning rather than treating M92 or M584 as ontology concepts.

26. Safety Example

A guarded machine may contain:

Guard
    monitored_by
Interlock

Interlock
    feeds
Safety Control Function

Safety Control Function
    implements
Guard-Open Stop Function

Guard-Open Stop Function
    prevents
Hazardous Motion

The actual safety implementation would also retain:

applicable standard;
risk context;
implementation;
validation;
evidence.
27. What Is Not Yet Final

The following areas remain open or partially resolved:

Exact property/value model
Exact relationship cardinalities
Temporal validity
Detailed provenance structure
Complete controller resource ontology
State / Mode ontology
Event ontology
Flow semantics
Signal semantics
Channel semantics
Interface semantics
Formal process ontology
Formal tooling ontology
Formal safety implementation structure
Firmware mapping architecture
Engineering evaluation rule model
Knowledge graph representation
Persistent storage schema

These should not be prematurely frozen.

28. Deferred Concepts

Some concepts have intentionally been deferred because their scope is not yet sufficiently clear.

Examples:

Flow
Signal
Channel
Event
Universal Resource
Universal Interface
Universal State

The project should only formalize these when a real semantic need has been demonstrated.

29. Ontology Invariants

The following distinctions are currently considered architectural invariants.

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
30. Current Ontology Architecture

The current conceptual model can be summarized as:

                         MACHINE
                            │
                    ┌───────┴───────┐
                    │               │
               STRUCTURE         BEHAVIOR
                    │               │
          ┌─────────┼─────────┐     │
          ▼         ▼         ▼     ▼
       Objects   Aspects    Roles  Functions
          │                     │
          ├── Classifications   ├── Capabilities
          ├── Properties        ├── Tasks
          ├── Relationships     ├── Processes
          └── Provenance        ├── Operations
                                ├── Actions
                                └── Procedures

        ┌───────────────┬───────────────┬───────────────┐
        ▼               ▼               ▼               ▼
     Motion        Connectivity     Measurement      Control
        │               │               │               │
     Axis/Joints      Ports           Sensors         Controllers
     Actuators        Connections     Results         Functions
     Motors           Paths           Feedback        Resources
     Drives            Mappings                        State

        ┌───────────────┬───────────────┐
        ▼               ▼               ▼
      Process         Safety        Engineering
        │               │             Evaluation
     Tools             Hazards          │
     Workholding        Risks            │
     Operations         Safety           │
                       Functions         │
                                        │
                                   Constraints
                                   Compatibility
                                   Validation

This is a conceptual organization, not a database schema.

31. Ontology Maturity

Current approximate maturity:

Area	Maturity
Object / Classification / Role / Aspect	High
Provenance / Evidence	High
Machine / Component / Catalog	High
Motion vocabulary	High-level established
Coordinate frames	High-level established
Ports / Connections	High-level established
Measurement	High-level established
Function vocabulary	High-level established
Relationships	High-level established
Subsystems	High-level established
Control	Medium
Process	Medium
Safety	Medium
Controller Resources	Medium
Firmware Mapping	Medium
Runtime State	Medium
Engineering Evaluation	Medium
Formal Cardinalities	Early
Formal Property Model	Early
Temporal Model	Early
Storage Schema	Deferred

These maturity labels indicate semantic maturity, not software completeness.

32. Current Ontology Rule

The ontology should favor meaningful engineering distinctions over the smallest possible vocabulary.

However, it should also avoid creating concepts merely because two words happen to sound different.

The decision to create or retain a concept should be supported by at least one or more of:

real machine stress case;
standards evidence;
meaningful engineering distinction;
implementation requirement;
analysis requirement;
provenance requirement.
33. Ontology Change Rule

When new evidence challenges the current ontology:

Identify the exact semantic conflict.
Determine whether an existing distinction is incorrect or incomplete.
Test the proposed change against existing stress cases.
Check relevant standards where appropriate.
Record the decision.
Update the current ontology.
Update affected implementation handoffs.
Preserve the previous state in ontology history when the change is substantial.

The current ontology should therefore remain understandable as a snapshot while its evolution remains traceable.

34. Summary

The current Machine Builder ontology is centered on:

Object
Classification
Role
Aspect
Property
Relationship
Provenance

and expands through engineering domains including:

Machine Structure
Motion
Coordinates
Connectivity
Measurement
Functions
Control
Process
Tooling
Safety
Controllers
Firmware
Runtime State
Engineering Evaluation

The model deliberately avoids firmware-specific, UI-specific, or catalog-specific semantics as its foundation.

The most important architectural goal is that a diverse physical machine can be represented accurately before any particular firmware, UI, storage mechanism, or implementation language is selected.

This document represents the current ontology state and should be updated when major semantic decisions change.