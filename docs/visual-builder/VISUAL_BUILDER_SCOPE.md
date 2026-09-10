# Machine Builder Visual Builder — Prototype Scope

## Status

**Document:** Visual Builder Prototype Scope  
**Version:** 0.1  
**Status:** Initial implementation handoff  
**Project:** Machine Builder / Machine Development Environment (MDE)

---

# 1. Purpose

The Machine Builder Visual Builder is intended to provide a visual environment for constructing, inspecting, and modifying a representation of a machine.

The first prototype is an **interaction and visual-model experiment**, not the finished Machine Builder application.

The primary purpose of the prototype is to answer questions such as:

- Can users construct machine structures by dragging components onto a canvas?
- Can connections be created naturally by dragging between compatible ports?
- Can the same underlying machine representation support multiple visual views?
- Can the visual system remain independent of any particular firmware?
- Can the visual representation evolve as the canonical Machine Builder ontology evolves?
- Can complex machines be represented without hard-coding one-to-one relationships that do not exist physically?

The prototype should therefore prioritize **correct interaction and sound architecture over visual polish**.

---

# 2. Core Principle

The visual builder must not become the canonical machine model.

The intended architecture is:

```text
Canonical Machine Model
        ↓
Visual / Interaction Model
        ↓
Renderer / User Interface

The visual layer represents the machine model.

It must not redefine the machine model based solely on how something happens to be drawn.

A visual node, line, group, or layout position is therefore not automatically a semantic machine object.

Likewise, a canonical machine relationship may have different visual representations depending on the current view and zoom level.

3. Prototype Goal

The first prototype should demonstrate a usable visual workspace containing:

a component palette
a canvas
draggable components
ports/interfaces on components
connection creation by dragging from one port to another
selection
movement
deletion
zoom and pan
basic grouping or subsystem representation
basic property inspection/editing
serialization and deserialization of the visual machine representation

The prototype does not need the final Machine Builder user interface.

It does need enough structure that later functionality can be added without replacing the visual architecture.

4. Initial Conceptual Objects

The prototype should be able to represent, at minimum:

Machine
Component
Subsystem
Port
Connection
Property
View

These are implementation-facing concepts for the visual prototype.

They should not be assumed to be the final canonical ontology.

Additional semantic concepts may eventually include:

Axis
Joint
Link
Actuator
Motor
Drive
Sensor
Controller
Tool
CoordinateFrame
Function
Capability
Process
Measurement
Signal
Resource

The prototype should be designed so these can be added without requiring a redesign of the basic visual engine.

5. Ports Are Fundamental to Connections

Connections should terminate on ports, not arbitrary visual nodes.

Conceptually:

Component
   ├─ Port
   ├─ Port
   └─ Port

and:

Port
   ↓
Connection
   ↓
Port

A component may have zero, one, or many ports.

A port may represent different interface domains, including:

electrical
signal
communication
mechanical
material
fluid
logical

The first prototype does not need to implement every domain, but its architecture must not assume that all ports are electrical.

6. Connections Must Be Semantic, Not Merely Graphical

A line drawn between two objects is not sufficient to represent a machine connection.

The prototype should treat a connection as a structured object containing at least:

source/endpoints
connection type/domain
visual representation

The exact canonical connection vocabulary is still under development.

The prototype must therefore avoid hard-coding a universal assumption such as:

connection = electrical wire

Instead, the visual engine should be able to support different connection types.

Examples:

electrical connection
signal connection
communication connection
mechanical connection
material connection
7. Compatibility Must Be Possible

The visual system should eventually be able to determine whether two ports are compatible.

For example:

24V power output → 24V motor power input

may be valid.

Whereas:

24V power output → thermistor input

should not silently become a valid connection.

Likewise:

RS-485 ↔ RS-485
material outlet ↔ material inlet
mechanical interface ↔ compatible mechanical interface

may be valid depending on their definitions.

The first prototype may use a simple compatibility model.

The important architectural requirement is:

Compatibility must be determined by semantic port information, not by the visual appearance of the nodes.

8. Visual Representation Must Be Separate From Machine Semantics

A component may have:

semantic identity
physical properties
functional relationships
ports
connections
location
classification

while its visual representation may contain:

x/y position
size
rotation
collapsed/expanded state
display label
icon
view-specific styling

These should not be treated as the same information.

For example:

Motor

does not inherently mean:

x = 500
y = 300

Those are visual properties.

Similarly, changing the visual position of a motor must not change its physical machine relationship.

9. Relationships May Be Many-to-Many

The visual architecture must not assume:

one axis → one motor

or:

one function → one component

or:

one sensor → one function

Examples that must remain representable include:

CoreXY
Motor A ─┐
         ├─ Kinematic relationship → X/Y motion
Motor B ─┘
Multiple motors on one logical axis
Logical Z axis
 ├─ Motor A
 ├─ Motor B
 └─ Motor C
One measurement used by multiple functions
Measurement Result
 ├─→ control
 ├─→ calibration
 └─→ diagnostics
One subsystem spanning multiple physical components
Material-handling function
 ├─ CFS feeder
 ├─ buffer
 ├─ sensors
 └─ printer extruder

The visual system must not bake one-to-one assumptions into its core data structures.

10. The Prototype Should Support Multiple Views

The long-term Machine Builder is expected to provide different ways of viewing the same machine model.

Examples include:

system view
physical/structural view
electrical view
motion/kinematic view
process view
material-flow view
control view
diagnostic view

The first prototype does not need to implement all of these.

It should, however, be designed so that a view is a representation of the underlying model, not a separate machine definition.

The same underlying component may therefore appear:

in several views
in different positions
with different visible properties
with different connection emphasis

without becoming several separate machine components.

11. Zoom Must Be Treated as a View Problem

The intended final UI has different levels of detail.

At close zoom:

individual pins
individual wires
connectors
ports
signals

At farther zoom:

component-to-component relationships
cables
harnesses
subsystems

The prototype does not need to fully implement this behavior yet.

It should avoid an architecture in which every zoom level requires a separate copy of the machine data.

Instead:

same model
   ↓
different visual detail level
12. Directionality Must Not Be Assumed From Drawing Layout

The visual representation should not imply that a connection is directional merely because one object is drawn to the left of another.

For example:

A ───────── B

does not automatically mean:

A → B

Signal direction may exist as semantic information, but it is separate from the visual geometry.

This is especially important for electrical wiring and other physical connections.

The eventual diagnostic UI may visualize signal activity through animation, glow, pulse, or other effects, but those effects should represent semantic/runtime information rather than establish direction through the base diagram itself.

13. Physical Topology and Logical Relationships Must Remain Distinct

The prototype must be capable of eventually representing cases where:

physical connection

and:

logical mapping

are not identical.

Examples include:

a connector carrying several signals
a cable containing several conductors
one logical net spanning multiple physical connections
firmware mappings that temporarily or conditionally change
communication buses containing multiple logical devices
material paths involving several physical components

The visual engine should therefore avoid treating:

one visible line = one complete semantic relationship

as a permanent architectural rule.

14. Firmware Independence

The visual prototype must not be designed specifically around:

Klipper
RepRapFirmware
Marlin
FluidNC
GRBLHAL

or any other one firmware.

Firmware-specific terms may eventually be represented as implementation mappings.

They should not define the visual model.

For example, a canonical motor should not need to know that Klipper happens to represent it using:

[stepper_x]

Similarly, an RRF representation should not redefine what a motor or axis means in the canonical model.

15. Prototype Machine

The first meaningful demonstration machine should be a simplified subset of the Promega.

The initial prototype does not need to reproduce the entire printer.

A useful minimum test system is:

Machine
 ├─ Controller
 ├─ X/Y motion system
 ├─ CoreXY motor relationships
 ├─ Z axis
 ├─ Z motor/driver
 ├─ IR probe
 ├─ heater/extrusion component
 └─ basic wiring/port relationships

The Promega is useful because it already contains several architectural challenges:

CoreXY kinematics
controller resources
motors and drivers
probing
unusual homing behavior
multiple types of electrical and signal connections

It therefore provides a better test than a trivial three-axis Cartesian diagram.

16. Second Stress-Test System

After the basic Promega case works, the next useful test is the Creality CFS material-handling subsystem.

The CFS should eventually be representable as a subsystem containing multiple:

material sources
rewind motors
filament-presence sensors
feeder motors
lower transport mechanisms
buffer
buffer sensor/switch
controller
communication interface
material paths

This is specifically intended to stress-test:

subsystem boundaries
multiple actuators
multiple sensors
material paths
local control
external communication
many-to-many functional relationships
multiple ports
different connection domains

The CFS should not be treated as merely a single "filament feeder" node.

17. What Is Out of Scope for the First Prototype

The first prototype should not attempt to implement the complete Machine Builder feature set.

Do not attempt to fully implement:

the finished canonical ontology
firmware translation
firmware parsing
automatic machine reconstruction
complete electrical validation
complete safety validation
complete kinematic solving
complete CAD integration
complete BOM management
complete parts catalog
automated engineering calculations
real-time machine control
machine diagnostics against live hardware
production-grade authentication or collaboration
every supported machine/process type

These are future features.

The prototype is primarily an experiment in visual machine representation and interaction architecture.

18. Architectural Constraints

The prototype should follow these principles:

Do not hard-code one-to-one relationships.
Do not make visual objects the canonical machine objects.
Do not make firmware terminology the canonical machine terminology.
Do not make every connection an electrical wire.
Do not make every port an electrical pin.
Do not assume every component has one parent.
Do not assume every function belongs to exactly one subsystem.
Do not assume every sensor has one purpose.
Do not assume every motor corresponds to one axis.
Do not assume every axis corresponds to one motor.
Do not assume every machine has Cartesian XYZ coordinates.
Do not make visual layout part of machine semantics.
Keep the semantic layer replaceable/evolvable.
19. Success Criteria for the Prototype

The prototype should be considered successful when it can demonstrate all of the following:

A user can place components onto a canvas.
A component can expose multiple ports.
A user can drag a connection from one port to another.
The system can determine at least basic port compatibility.
Connections remain attached correctly when components move.
Components can be selected, moved, and removed.
The machine representation can be saved and loaded.
The visual representation can be separated from the underlying machine graph.
Many-to-many relationships can be represented without special-case hacks.
The architecture allows additional port and connection types to be introduced later.
The architecture does not depend on a particular firmware.
The prototype can represent the simplified Promega test case.
20. Longer-Term Direction

The prototype is intended to become the foundation for a more capable visual Machine Builder.

Eventually the visual environment should support:

component placement
subsystem organization
port-based connections
electrical diagrams
material paths
motion/kinematic views
coordinate-frame visualization
process views
control-loop visualization
diagnostics
signal activity
validation
simulation
machine configuration
machine editing
firmware generation

The eventual interface may become substantially more sophisticated than the prototype.

The initial implementation should therefore emphasize clean boundaries and replaceable representations rather than attempting to build the final interface immediately.

21. Relationship to Ontology Work

The canonical Machine Builder ontology is still under development.

Current high-confidence concepts include:

Machine
Subsystem
Component
Function
Capability
Axis
Joint
Link
Actuator
Motor
Drive
Controller
Sensor
Measurement Result
Coordinate Frame
Process
Operation
Task
Tool
Mechanical Interface
State
Control Function
Control Loop
Safety Function
Port
Connection
Property
Quantity
Unit
Uncertainty
Provenance

Some concepts remain intentionally unresolved, including:

Resource
Channel
Flow
Route

The visual prototype must remain flexible around these concepts.

A prototype discovery that exposes an ontology problem should be reported back into the architecture/research process rather than hidden through a UI-specific workaround.

22. Guiding Principle

The prototype should make it easy to ask:

"What is this thing, what is it related to, and why?"

rather than merely:

"What should this box and line look like?"

The visual builder is ultimately intended to become a way of working with the machine model, not simply a diagram editor.