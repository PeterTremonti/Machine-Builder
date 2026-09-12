# Machine Builder Terminology Baseline

## 1. Purpose

This document establishes the current working meanings of important Machine Builder terms.

It is intended to prevent the same word from being used to mean different things in different parts of the project.

These definitions are a working semantic baseline, not a claim that every term is permanently finalized.

Where a term has meanings in an external standard that differ from Machine Builder's usage, the distinction should be recorded rather than silently conflated.

---

## 2. General Modeling Vocabulary

### Object

An identifiable entity represented by the canonical machine model.

Examples:

- machine;
- motor;
- sensor;
- controller;
- axis;
- joint;
- subsystem;
- port;
- coordinate frame.

An Object may have classifications, roles, properties, relationships, and provenance.

---

### Classification

A statement about what kind or category of thing an Object is.

Examples:

```text
Stepper Motor
Temperature Sensor
Controller
Servo Drive
Guard
Coordinate Frame

Classification is distinct from Role.

Role

A contextual description of how an Object participates in a particular machine or situation.

Examples:

Z-axis actuator
Filament feeder
Temperature sensing element
Safety interlock device

The same physical object may have different roles in different contexts.

Aspect

An engineering view or structuring dimension through which an Object or relationship may be considered.

Relevant aspects may include:

physical;
electrical;
functional;
control;
logical;
safety;
maintenance.

IEC 81346 provides important architectural precedent for this concept.

Machine Builder Aspect is not automatically identical to every use of the word "aspect" in external standards.

Property

A characteristic, attribute, or value associated with an Object or Relationship.

Examples:

current = 1.5 A
steps_per_revolution = 200
shaft_diameter = 5 mm

A Property should be capable of carrying appropriate units, provenance, validity, and uncertainty where required.

Relationship

A typed semantic association between modeled entities.

Examples:

contains
mounted_on
drives
measures
connects_to
participates_in
implements
maps_to
derived_from

Relationships are first-class semantic information.

Provenance

Information describing where a fact, relationship, classification, or derived result came from and how it was established.

Possible provenance information includes:

source;
method;
date;
version;
confidence;
observation;
calculation;
inference;
evidence location.
3. Machine Structure Vocabulary
Machine

A system of physical and logical elements organized to perform one or more intended purposes.

A Machine may contain:

components;
subsystems;
controllers;
interfaces;
functions;
resources;
processes;
safety functions;
state.

"Machine" is intentionally broader than "3D printer."

Machine Component

A machine-specific occurrence of a hardware or physical component.

Examples:

the motor physically installed on the Promega Z mechanism
the controller board installed in an Ender 3
the specific sensor installed in a CFS

Machine Component is distinct from a catalog product definition.

Catalog Product

A product definition describing something that can exist or be purchased independently of a particular machine.

Examples:

manufacturer motor model
controller board model
connector product
linear rail model
Product Version

A specific revision, variant, or version of a Catalog Product.

This distinction matters when specifications or behavior change between revisions.

Occurrence

An actual occurrence of a product or classified entity within a particular machine or system context.

Machine Component is the preferred project terminology for hardware occurrences.

Subsystem

A bounded portion of a machine that participates in the larger machine while potentially containing its own:

structure;
components;
functions;
capabilities;
resources;
state;
control behavior;
interfaces;
communication.

A subsystem may contain other subsystems.

4. Motion Vocabulary
Axis

A machine motion or coordinate concept representing an independently meaningful degree or mode of motion.

An Axis is not necessarily a physical actuator or a motor.

Examples:

X axis
Y axis
Z axis
A rotary axis

A logical Axis may be produced by multiple physical actuators.

Joint

A constrained mechanical relationship between physical elements that permits relative motion.

A Joint may be:

active;
passive;
mechanically constrained;
associated with one or more actuators.

A Joint is not automatically the same thing as an Axis.

Link

A relatively rigid physical body or structural element connecting or separating joints in a mechanical system.

The exact formal treatment may vary by machine type.

Actuator

A component or functional element capable of producing physical motion or another controlled physical effect.

A motor may form part of an actuator.

Actuator is intentionally broader than Motor.

Motor

An electromechanical device that converts energy into mechanical motion.

Examples include:

stepper motor;
servo motor;
DC motor;
BLDC motor.

A Motor is not automatically a complete Drive or Actuator system.

Drive

A system or component responsible for controlling an actuator or motor.

A Drive may include:

power electronics;
control logic;
feedback processing;
current control;
velocity control;
position control;
communication interfaces.

The exact scope depends on context and implementation.

Kinematic Relationship

A relationship describing how physical motion of components and joints produces or constrains another machine motion.

Examples include:

CoreXY coupling;
belt-driven transformations;
lead screw transmission;
robot kinematics;
coordinated rotary motion.

Kinematics must not assume one motor corresponds to one axis.

5. Coordinate Vocabulary
Coordinate Frame

A defined coordinate reference system with a relationship to another frame and a meaningful engineering purpose.

A Coordinate Frame may have:

parent frame;
transform;
semantic role;
reference object.

Examples:

Machine Frame
Work Frame
Tool Frame
Object Frame
Camera Frame
Task Frame
Transform

A mathematical relationship describing the change of coordinates between frames.

A Transform may include:

translation;
rotation;
scaling where appropriate;
homogeneous transformation representation;
other mathematically valid mappings.

The exact representation remains an implementation concern until formally selected.

Canvas Coordinate

A coordinate used by the visual interface to position objects on a 2D or 3D display.

Canvas coordinates are not physical machine coordinates.

6. Interface and Connectivity Vocabulary
Port

A semantic interface exposed by an Object for interaction or connectivity.

Potential domains include:

electrical;
signal;
communication;
mechanical;
material;
fluid;
logical.

A Port is not automatically a connector or pin.

Connector

A physical interface structure used to establish one or more physical connections.

A Connector may contain multiple Pins.

Pin

A discrete contact or terminal position associated with a connector or other physical interface.

A Pin may carry:

power;
ground;
signal;
communication;
control;
other electrical functions.

A Pin is not necessarily the same semantic abstraction as a Port.

Connection

A semantic association between compatible endpoints, normally represented through Ports or more detailed interface elements.

A Connection may describe:

physical connectivity;
logical connectivity;
electrical connectivity;
communication connectivity;
mechanical connectivity;
material connectivity;
other domain-specific relationships.

A Connection is not the same thing as a visual line.

Physical Connection

A relationship representing a physical path or attachment between entities.

Examples:

wire between pins
tube between fittings
shaft coupled to mechanism
material path between feeder and tool
Logical Mapping

A relationship describing how a logical signal, information channel, command, resource, or function is represented or transported through physical or implementation elements.

A logical mapping may span multiple physical connections.

Path

A physical or structural route through which something may be connected or transported.

Potential uses include:

material;
fluid;
electrical routing;
communication routing;
mechanical transmission.

Path is intentionally more general than Flow.

A path does not imply that something is currently flowing.

Harness

A grouped set of physical wires, cables, tubing, or similar routed elements organized as a physical assembly.

A Harness may contain sub-harnesses.

7. Measurement Vocabulary
Sensor

A physical or functional element involved in obtaining information about a physical quantity or condition.

A Sensor is not itself the Measurement Result.

Measurand

The quantity or property intended to be measured.

Examples:

temperature
position
pressure
force
distance
electrical current
Measurement

The process or activity by which information about a measurand is obtained.

Measurement Result

The result produced by a measurement process.

A Measurement Result may contain:

value;
unit;
uncertainty;
time;
conditions;
method;
provenance.
Feedback

A use of information derived from a measurement to influence a control or decision process.

Feedback is a functional/control relationship.

A Sensor is not automatically "a feedback sensor."

8. Functional Vocabulary
Capability

An ability possessed by a Machine, Subsystem, Object, or other system.

Examples:

can heat build volume
can perform closed-loop position control
can perform tool changing
can measure filament presence

Capability describes what the system is able to do.

Function

A defined behavior or service that a Machine or Subsystem provides or performs, independent of one particular execution instance, procedure, command, or firmware representation.

Examples:

Maintain Build Temperature
Feed Material
Measure Temperature
Move Tool
Control Spindle Speed
Prevent Unexpected Restart

Function is intentionally not a universal parent class for Task, Operation, Action, or Procedure.

Task

An intended body of work or objective.

Examples:

Print Part
Machine Pocket
Inspect Part
Change Tool

A Task may require many Functions and Operations.

Process

An organized set of activities or operations through which an intended result is achieved.

Examples:

Additive Manufacturing Process
Machining Process
Inspection Process
Material Loading Process

The exact process ontology remains under development.

Operation

A bounded executable unit of work within a process or task.

Examples:

Heat Build Volume
Probe Surface
Extrude Material
Change Tool
Machine Pocket

Operation is not synonymous with Function.

Action

A discrete executable behavior or change.

Examples:

Enable Heater
Open Valve
Advance Filament
Stop Motor
Trigger Probe

An Action may implement or contribute to a Function or Operation.

Procedure

A specified way of carrying out an activity or process.

A Procedure answers substantially:

How is this carried out?

Examples:

Z-Probe Calibration Procedure
Motor Replacement Procedure
Heating Procedure
Tool Change Procedure

Procedure is distinct from the activity being performed.

Control Function

A Function that evaluates information and determines outputs or activities used to regulate machine behavior.

A Control Function may participate in:

open-loop control;
closed-loop control;
feedforward;
feedback;
cascaded control.
Safety Function

A Function required to achieve or maintain a safe state or reduce risk.

A Safety Function belongs to the safety architecture and must retain its applicable engineering context and evidence.

Control Loop

A control arrangement in which a controller uses one or more measured or estimated values to regulate a system relative to a desired condition.

A simplified form is:

Setpoint
   ↓
Controller
   ↓
Actuator
   ↓
Physical System
   ↓
Measurement
   ↓
Feedback
   └──→ Controller

Control Loop is a structural/control concept, not a generic synonym for Function.

9. Process and Tool Vocabulary
Tool

An object used by a machine to perform or support a process.

Examples:

cutting tool;
extrusion tool;
laser;
probe;
dispensing tool.
Toolhead

A physical assembly carrying one or more tools or process elements.

A Toolhead may include:

tool;
sensors;
actuators;
cooling;
heating;
electronics;
mounts.

Toolhead is not automatically synonymous with Tool.

Carriage

A mechanical structure that moves or supports a Toolhead, Tool, or other machine element.

End Effector

A tool or tool-carrying interface positioned at the operational end of a robot or similar mechanism.

The exact applicability depends on machine architecture.

Workholding

A structure or mechanism that locates, supports, or constrains a workpiece.

Examples:

build plate;
vice;
chuck;
clamps;
fixture.
10. Controller Vocabulary
Controller

A computing or control entity responsible for coordinating one or more machine functions or resources.

A Controller may contain or expose:

processing resources;
motion resources;
GPIO;
ADC;
PWM;
timers;
communication interfaces;
motor-control resources;
safety-related resources.
Controller Resource

A finite capability or hardware/software resource provided by a Controller.

Examples:

Motor Driver 0
GPIO 17
ADC Channel 3
CAN Interface
UART Interface
Timer 2

Controller Resource is intentionally distinct from a physical component where appropriate.

Firmware

Software executing on a controller or embedded computing platform that implements machine control behavior.

Firmware is an implementation representation, not the canonical machine ontology.

Firmware Mapping

A defined relationship between canonical machine semantics and a firmware-specific representation.

Examples:

Canonical Axis → firmware axis
Canonical motor current → firmware driver current parameter
Canonical controller resource → firmware pin/resource assignment
Firmware Term

A term whose meaning is defined within a particular firmware ecosystem.

Firmware Terms may map to canonical concepts but do not automatically become canonical concepts.

11. State and Configuration Vocabulary
Configuration

Information describing intended machine setup or operating parameters.

Examples:

motor current
steps per unit
maximum velocity
axis mapping
tool assignment
Runtime State

Information describing the machine's current condition.

Examples:

axis homed
motor enabled
drive faulted
temperature = 205 °C
filament present

Runtime State is distinct from Configuration.

Mode

A defined operating condition in which a machine or subsystem behaves according to a particular set of rules.

Examples may include:

Idle
Homing
Printing
Manual
Fault
Maintenance

The exact state/mode model remains subject to further research.

Fault

A detected condition in which a machine, subsystem, or component cannot continue normal operation or requires intervention.

A Fault is runtime information, although its classification may be based on configuration or engineering rules.

12. Safety Vocabulary
Hazard

A potential source of harm.

Risk

The combination of likelihood and severity associated with potential harm.

Risk Reduction Requirement

A requirement identified as necessary to reduce a machine risk to an acceptable level.

Safety-Related Control Implementation

The hardware and/or software implementation through which a Safety Function is realized.

Safe State

A defined condition in which the relevant hazard has been reduced or controlled according to the applicable safety architecture.

"Safe State" is context-dependent and must not be treated as one universal machine state.

Guard

A physical barrier or protective structure intended to prevent or limit access to hazardous areas.

Interlock

A mechanism or control relationship intended to prevent or constrain machine operation based on the state of a guard or other protective condition.

13. Information and Evidence Vocabulary
Fact

A statement represented by the system as information about an Object or Relationship.

A Fact should retain provenance and confidence where appropriate.

Observation

Information directly obtained from inspecting or measuring the physical machine or its behavior.

Inference

A conclusion derived from available evidence that is not directly stated by the source.

Derivation

A result calculated or logically produced from known inputs using a defined method.

Assumption

An explicitly declared condition treated as true for the purpose of analysis or calculation.

Assumptions should not be silently converted into facts.

Confidence

An indication of how strongly the available evidence supports a Fact or Interpretation.

Confidence is not the same as truth.

Evidence

Information supporting or contradicting a claim, relationship, property, or interpretation.

14. Engineering Evaluation Vocabulary
Constraint

A condition that must be satisfied.

Examples:

driver current must not exceed rating
tool must fit mounting interface
controller must provide required resource
Compatibility

The degree to which two or more entities, interfaces, resources, or requirements can work together under specified conditions.

Potential results include:

Compatible
Incompatible
Conditionally Compatible
Unknown
Validation

The process of determining whether a system, implementation, or result satisfies specified requirements or intended behavior.

Validation is context-dependent and should retain evidence.

Verification

The process of determining whether a result or implementation conforms to specified requirements, specifications, or criteria.

The exact distinction between Verification and Validation may vary by domain and will be refined as systems-engineering work progresses.

Evaluation Result

A derived result produced by applying a rule, calculation, constraint, or engineering method to available information.

Possible statuses include:

PASS
WARNING
RECOMMENDATION
INVALID
UNKNOWN
15. Visual Vocabulary
Visual Model

The presentation-oriented representation used by the visual builder.

It may contain:

node positions;
node sizes;
grouping;
visibility;
routing;
selection;
zoom;
interaction state.

It is not the canonical machine model.

Node

A visual representation of one or more canonical entities.

A Node is primarily a visual construct.

It should not be assumed that every canonical Object corresponds to exactly one Node.

Visual Connection

A rendered visual representation of a semantic relationship or Connection.

A Visual Connection is not the canonical Connection itself.

Canvas

The visual workspace in which nodes, connections, groups, and related objects are displayed.

Canvas coordinates are distinct from physical machine coordinates.

16. Relationship Vocabulary

The following relationship terms are currently preferred where their meanings apply.

Contains

Indicates structural containment.

Machine contains Subsystem
Subsystem contains Component
Part Of

Indicates membership in a larger structure.

Depending on context, this may be similar to containment but should not automatically be treated as identical.

Mounted On

Indicates that an object is physically attached or mounted to another object.

Connected To

Indicates a connectivity relationship.

Specific physical, logical, electrical, or other semantics should be added where required.

Measures

Indicates that a Sensor or measurement system obtains information about a Measurand.

Drives

Indicates that one object controls or produces motion/behavior in another context.

This term must not be used as a substitute for precise actuator/drive semantics where greater specificity is required.

Participates In

Indicates that an Object contributes to or participates in a larger function, axis, process, or behavior.

This relationship is intentionally broader than Drives.

Implements

Indicates that one entity realizes another semantic definition or requirement.

Examples:

Firmware implementation implements Control Function
Hardware implementation implements Safety Function
Maps To

Indicates a correspondence between two representations or semantic domains.

Examples:

Canonical concept maps to firmware parameter
Physical resource maps to logical resource
Derived From

Indicates that information was calculated or logically derived from other information.

Supported By

Indicates that a Fact, claim, or interpretation has supporting evidence.

17. Terms Currently Avoided as Universal Concepts

The following terms should not be used as generic catch-all entities without a clearly defined context:

Flow
Signal
Channel
Resource
Interface
Device
Part
Component
Process
State
Function
Operation
Command
Event

These words may still be valid concepts.

The issue is that each has multiple domain-specific meanings.

For example:

Signal may mean an electrical waveform, logical information, or control information.
Channel may mean an ADC input, communication path, data channel, or logical route.
Resource may mean controller hardware, software capacity, or physical machine capability.
Interface may mean a physical connector, logical API, protocol, or semantic Port.

A generic concept should not be introduced merely because the word is convenient.

18. Important Non-Equivalences

The following distinctions are architectural safeguards.

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
Connection ≠ Logical Mapping
Physical Connection ≠ Logical Mapping

Physical Position ≠ Canvas Position

Configuration ≠ Runtime State

Firmware Term ≠ Canonical Concept

Catalog Data ≠ Machine Fact

Inference ≠ Direct Observation
Derived Value ≠ Direct Value

Engineering Evaluation ≠ Certification

These distinctions should remain visible during ontology development and implementation.

19. Terminology Maintenance Rule

When a new term is introduced, determine:

What does the term mean here?
What does it explicitly not mean?
Is the term already used by a relevant standard?
Is the Machine Builder usage compatible with that standard?
Does another existing term already cover the concept?
Is the term describing an Object, Classification, Role, Aspect, Property, Relationship, Function, or another semantic category?
Does a real machine stress case demonstrate the need for the distinction?

A new term should be added because it resolves a meaningful semantic problem, not simply because the word sounds useful.

20. Current Baseline Principle

The terminology baseline follows one overarching rule:

Similar words should be combined only when their underlying engineering meanings are actually the same.

Where meanings differ, the architecture should preserve the distinction even when doing so requires more concepts.

The goal is not to maximize the number of classes or terms.

The goal is to preserve the distinctions necessary to accurately describe real machines across physical, functional, logical, control, safety, process, and firmware domains.