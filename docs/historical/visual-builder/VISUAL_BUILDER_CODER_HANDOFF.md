# Machine Builder Visual Builder — Coder Handoff

## Status

**Document:** Visual Builder Coder Handoff  
**Version:** 0.1  
**Status:** Initial implementation handoff  
**Project:** Machine Builder / Machine Development Environment (MDE)

---

# 1. Purpose of This Handoff

This document transfers the current visual-builder work from the Machine Builder architecture/research process into the implementation-focused development process.

The implementation conversation should use this document together with:

```text
VISUAL_BUILDER_SCOPE.md
VISUAL_MODEL.md
VISUAL_BUILDER_REQUIREMENTS.md
VISUAL_BUILDER_ARCHITECTURE.md

These documents define the initial implementation boundary.

They do not represent a final Machine Builder ontology or final application architecture.

The implementation team should therefore build the first visual prototype while preserving the ability of the semantic model to evolve.

2. What Machine Builder Is

Machine Builder is intended to become a Machine Development Environment (MDE) rather than a firmware configuration generator.

The long-term vision is:

Physical Machine
       ↓
Canonical Machine Model
       ↓
Firmware / Control Representation

and also:

Firmware / Configuration
       ↓
Semantic Interpretation
       ↓
Canonical Machine Model

The canonical machine model is intended to describe the machine independently of any particular firmware.

The visual builder will eventually become one way of creating, inspecting, editing, and understanding that canonical model.

3. Why We Are Starting the Visual Prototype Now

The semantic architecture is still under active research.

However, enough high-confidence concepts have now emerged to begin testing the visual interaction model.

The objective is not to wait until the ontology is mathematically complete.

Instead:

Use the visual prototype to test whether the emerging ontology works naturally when a human actually tries to build and manipulate a machine representation.

The visual prototype is therefore part of architectural validation.

It is not merely UI development.

4. Current Architectural Philosophy

The project has deliberately moved away from a simple hierarchical machine tree.

The current model is increasingly understood as:

Objects
+
Properties
+
Classifications
+
Roles
+
Typed Relationships

with different semantic views/aspects of the same underlying system.

This is influenced by research into:

ISO 841
ISO 8373
ISO 9787
IEC 81346
ISO 10303 / STEP
ISO/ASTM 52900
ISO 14649
IEC 61131
IEC 61800
CiA 402
VIM / JCGM 200
ISO 13849
IEC 62061
ISO/IEC/IEEE 15288
ISO/IEC/IEEE 42010
related industrial information-modeling standards

These standards are being used as vocabulary and architectural evidence.

Machine Builder is not intended to simply implement any one of them.

5. Important Architectural Conclusions So Far

The following concepts have survived repeated research and machine stress-testing reasonably well.

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
Measurand
Measurement System / Procedure
Measurement Result

Coordinate Frame
Transform

Process
Operation
Working Step
Task
Action
Procedure

Tool
Mechanical Interface

State
Control Function
Control Loop
Command
Signal
Fault

Safety Function
Hazard
Risk

Port
Connection
Path

Property
Quantity
Unit
Uncertainty
Provenance

Not all of these have been formally frozen.

The implementation should nevertheless use the distinctions where they affect the visual architecture.

6. Important Concepts That Must NOT Be Collapsed

The following distinctions are especially important.

Axis ≠ Motor

Axis ≠ Joint

Joint ≠ Actuator

Motor ≠ Drive

Drive ≠ Controller

Sensor ≠ Measurement Result

Measurement Result ≠ Feedback

Function ≠ Capability

Function ≠ Action

Function ≠ Operation

Operation ≠ Procedure

Task ≠ Function

Tool ≠ Toolhead

Tool ≠ Carriage

Port ≠ Connector

Port ≠ Pin

Connection ≠ Visual Line

Physical Connection ≠ Logical Mapping

Visual Position ≠ Physical Position

Runtime State ≠ Configuration

Firmware Term ≠ Canonical Concept

The first visual prototype does not have to expose all of these distinctions to the user.

Its internal architecture must not make the distinctions impossible.

7. Current Thinking About Function

The word Function has been found to be heavily overloaded across engineering standards.

For Machine Builder, the current working definition is:

A defined machine or subsystem behavior/service that the machine provides or is intended to provide, independent of a particular execution instance, procedure, command, or implementation.

Examples:

home an axis
maintain chamber temperature
extrude material
detect filament
load filament
cut filament
change tool
probe a surface
control spindle speed

A function is not automatically a software routine.

The Machine Builder model also distinguishes:

Capability
Function
Control Function
Safety Function
Task
Operation
Action
Procedure

Do not collapse these concepts merely because they all involve something "doing something."

8. Current Thinking About Capability

A capability describes an ability.

A function describes a behavior/service.

Conceptually:

Capability
    ↓ enables
Function
    ↓ realized by
Implementation

Examples:

Capability:
    automatic tool changing

Function:
    change active tool

Implementation:
    tool changer + controller + mechanics

or:

Capability:
    multi-source material handling

Functions:
    select material
    load material
    unload material
    detect material
    transport material

This distinction is likely to become important later for machine-feasibility analysis.

9. Current Thinking About Coordinate Frames

Coordinate systems are being treated as first-class semantic objects.

The current conceptual direction is:

CoordinateFrame
 ├─ parent
 ├─ transform
 ├─ semantic role
 └─ reference object

The visual canvas coordinate system is separate from machine coordinates.

Do not infer machine physical position from node position on the canvas.

Future Machine Builder representations may include:

Machine Frame
Work Frame
Tool Frame
Object Frame
Camera Frame
Task Frame

The first prototype does not need to implement all of them.

It must not hard-code the canvas as the machine coordinate system.

10. Current Thinking About Ports

Ports are increasingly regarded as one of the most important visual-model concepts.

A connection should normally be:

Port
   ↓
Connection
   ↓
Port

rather than:

Node
   ↓
Connection
   ↓
Node

because a node can expose many different interfaces.

Examples:

controller
 ├─ power input
 ├─ ground
 ├─ USB
 ├─ CAN
 ├─ endstop input
 ├─ heater output
 ├─ fan output
 └─ motor/driver interface

The connection endpoint must therefore identify the relevant port.

11. Current Thinking About Connection Domains

A connection is not necessarily an electrical wire.

The architecture needs to remain extensible for:

electrical
signal
communication
mechanical
material
fluid
logical

A physical wire, logical signal, material path, or communication relationship may have different semantic meaning even if they are visually represented as lines.

The prototype should therefore keep:

semantic connection

separate from:

visual connection geometry
12. Current Thinking About Paths

A recent architecture investigation found that Path may be more fundamental than a universal Flow.

A path describes where something can travel.

A flow describes an actual transfer or movement.

For example:

filament path

can exist while filament is stationary.

The visual prototype does not need a complete flow model.

However, it should not make future material paths, fluid paths, communication paths, or electrical topology impossible.

13. Current Thinking About Resource

Resource remains intentionally unresolved.

IEC 61131 uses the word in a specific controller/runtime context.

Other engineering standards use similar language differently.

Machine Builder has historically used Resource more broadly to mean something available to a function.

Do not make Resource the structural center of the visual prototype.

Where possible, use explicit concepts such as:

Port
Component
Controller resource
Capability
Function
Connection

instead of assuming everything is a generic resource.

14. Current Thinking About Object / Role / Classification / Aspect

A major architectural insight from IEC 81346 research is that an underlying object may be described through several different aspects.

For example, one physical motor may simultaneously be:

Physical object
Product/component
Motor type
Actuator
Z-axis actuator
Part of a subsystem
Participant in a safety function

These should not become separate physical objects merely because they have different classifications or roles.

This is a strong reason to avoid a rigid inheritance-only ontology.

15. Visual Model vs Canonical Model

The visual model is not the canonical model.

Conceptually:

Canonical Model
       ↓
Visual Model
       ↓
Renderer

The visual model may contain:

visual node
visual port
visual connection
visual group
view
layout
presentation state

while the canonical model contains:

semantic object
semantic relationship
properties
classifications
roles
functions
capabilities
etc.

A visual object may reference a canonical object.

A visual object may temporarily exist without one.

16. Why Visual Nodes Are Separate

A canonical object may appear:

in multiple views
at multiple detail levels
with different labels
with different visual organization

Therefore:

Visual Node ≠ Canonical Object

A visual node may contain a reference such as:

semantic_reference = component-017

but the visual node's canvas coordinates remain presentation state.

17. Multiple Views

The long-term system is expected to support multiple views of the same machine.

Potential views include:

System
Physical
Electrical
Motion
Kinematic
Process
Material
Control
Diagnostic

One canonical motor could therefore appear in multiple views.

The first prototype can use one view.

Its architecture should not make multiple views impossible.

18. Why Real Machines Are Being Used as Tests

The prototype is intentionally being tested conceptually against actual machines already researched.

Important examples include:

Promega
SV08
LowRider 3
IdeaFormer IR3
Creality Hi / CFS
Carvera
K40
3018 CNC
IDEX systems
industrial servo systems
robotic systems

These machines expose unusual relationships that a toy three-axis Cartesian printer does not.

The prototype should not accidentally encode assumptions that work only for a conventional printer.

19. Promega as First Visual Test

The first meaningful visual test should be a simplified Promega.

The initial model may include:

Promega Machine
Duet 2 Maestro
X motor
Y motor
Z motor
X/Y driver resources
Z driver
IR probe
heater/extrusion component

The important test is not exact completeness.

The important test is whether the engine can represent:

CoreXY relationship
motor/driver/controller relationships
probe connection
heater connection
multiple port types

without special-case hacks.

20. Why Promega Is Useful

Promega already challenges simplistic assumptions.

It includes:

CoreXY
unusual Z homing
probe-based behavior
controller resources
multiple electrical/signal interfaces

It is therefore a useful first test for the visual architecture.

21. CFS as Second Visual Stress Test

The Creality CFS provides a more complicated subsystem case.

A CFS can contain approximately:

CFS subsystem
 ├─ material source ×4
 │   ├─ spool
 │   ├─ rewind motor
 │   ├─ filament-present sensor
 │   └─ feeder motor
 │
 ├─ lower transport section
 │   ├─ filament sensor
 │   └─ feeder motor
 │
 ├─ buffer
 │   ├─ material paths
 │   └─ switch/sensor
 │
 ├─ controller
 └─ communication interface

It may contain several motors and multiple sensors before material reaches the printer extruder.

This should not be represented as one monolithic "filament feeder" object.

22. Why CFS Is Architecturally Valuable

The CFS demonstrates that:

one subsystem
    ↓
many physical components
    ↓
many sensors
    ↓
many actuators
    ↓
local control
    ↓
external communication
    ↓
multiple functions

It also demonstrates that a higher-level function can cross subsystem boundaries.

For example:

Maintain material path to extruder

may involve:

CFS
Buffer
Printer feeder
Extruder
Sensors
Controllers

The visual model must therefore support relationships that cross group/subsystem boundaries.

23. Why the Prototype Should Not Be Firmware-Specific

Machine Builder is explicitly not a Klipper-only configurator.

The canonical model must eventually support firmware such as:

Klipper
RepRapFirmware
Marlin
FluidNC
GRBLHAL
LinuxCNC

and potentially additional systems.

The visual builder must therefore function with no firmware information.

Firmware-specific representations can later appear as mappings.

For example:

Canonical Motor
      ↓
Implementation Mapping
      ↓
Klipper [stepper_x]

The visual engine should not make stepper_x the identity of the motor.

24. Important Firmware Independence Rule

Do not build visual classes such as:

KlipperStepper
RRFMotor
MarlinAxis

as the foundational visual abstraction.

Instead, use generic machine concepts and attach firmware implementation metadata separately.

25. Relationship Model

Current high-value relationships include:

contains
part_of

connects
attached_to
mounted_on

drives
acts_on
associated_with
participates_in

provides
implements
requires
uses
enables
supports

produces_measurement
measured_by
feeds
feedback_to

commands
reports_state_of
transitions_to

communicates_with
uses_protocol

performs
contains_operation
consists_of
realizes

constrained_by
protected_by

maps_to
configured_by

derived_from
validated_by
specified_by

These are semantic candidates, not a frozen API.

The visual layer should not require every relationship to be displayed as a line.

26. Why Typed Relationships Matter

"Connected to" is too vague.

For example:

CFS ↔ printer

might mean:

physically connected
electrically connected
communicates with
provides material to
functionally depends on

These are not interchangeable.

The visual architecture therefore needs room for relationship types.

27. Physical, Functional, and Logical Relationships

The same two objects may have several independent relationships.

For example:

Motor
 ├─ physically mounted_on → frame
 ├─ electrically connected_to → driver
 ├─ controlled_by → controller
 ├─ drives → joint
 └─ participates_in → motion function

Do not collapse these into one generic edge.

28. Measurement and Feedback

The current conceptual model is:

Measurand
      ↓
Measurement System / Procedure
      ↓
Measurement Result
      ↓
consumer

Consumers may include:

control
calibration
diagnostics
display
logging
safety

Feedback is a use of information, not a physical sensor category.

29. Control Model

The current conceptual control model is:

Setpoint
    ↓
Controller / Control Function
    ↓
Control Output
    ↓
Actuator
    ↓
Physical System
    ↓
Measurement
    ↓
Feedback
    └────────→ Control Function

States, faults, constraints, and safety functions interact with this structure.

The visual prototype does not need to implement closed-loop simulation.

It should not make closed-loop systems impossible to represent.

30. Process Model

The current conceptual process hierarchy is:

Product / Workpiece
       ↓
Process
       ↓
Task
       ↓
Operation / Working Step
       ↓
Action

and separately:

Procedure

describes how an activity/process is performed.

Machine functions may be realized during operations/actions.

This is not the same thing as firmware command syntax.

31. Safety Model

Safety is treated as a separate semantic concern.

Current conceptual structure:

Hazard
   ↓
Risk
   ↓
Risk-reduction requirement
   ↓
Safety Function
   ↓
Safety-related implementation

A normal machine component may participate in a safety function.

Do not make components inherently "normal" or "safety" objects simply because they happen to participate in one context.

32. Current Visual Architecture

The preferred conceptual architecture is:

                   Canonical Model
                         │
                         ↓
                Semantic Adapter
                         │
                         ↓
                    Visual Model
                         │
            ┌────────────┴────────────┐
            ↓                         ↓
       Validation                  View State
            │                         │
            └────────────┬────────────┘
                         ↓
                 Interaction Layer
                         ↓
                  Model Mutations
                         ↓
                     Renderer

Persistence operates on explicit model/view data rather than renderer internals.

The implementation may organize modules differently.

The responsibility boundaries should remain.

33. Renderer Responsibilities

The renderer is responsible for:

drawing nodes
drawing ports
drawing connections
drawing groups
drawing selection
drawing hover state
drawing connection previews
drawing compatibility feedback

The renderer should not:

define machine semantics
decide semantic compatibility
create canonical relationships
own persistent machine data
34. Interaction Responsibilities

The interaction layer interprets user input such as:

pointer down
pointer move
pointer up
drag
drop
select
delete
pan
zoom
edit

It should translate those actions into model mutations.

35. Model Mutation Principle

Preferred flow:

User Action
     ↓
Interaction Handler
     ↓
Requested Mutation
     ↓
Validation
     ↓
Commit
     ↓
Model Update
     ↓
Renderer Update

Avoid:

Mouse Event
   ↓
directly mutate renderer objects

This will make later undo/redo, validation, persistence, and semantic integration much easier.

36. Persistence

The visual prototype should eventually save/load:

nodes
ports
connections
groups
properties
view layout

The format should be structured and inspectable.

JSON is a reasonable prototype choice, but implementation technology is not prescribed by this handoff.

The visual persistence format is not automatically the final canonical Machine Builder file format.

37. Compatibility

Compatibility checking should be an isolated subsystem.

Conceptually:

Port A
Port B
   ↓
Compatibility Engine
   ↓
compatible
incompatible
unknown
conditionally compatible

The first implementation may use simple rules.

The architecture should support richer rules later.

38. Unknown Values

The machine builder is expected to handle incomplete information.

Examples:

port type unknown
compatibility unknown
part number unknown
property unspecified

Unknown information must remain distinguishable from confirmed false/incompatible information.

Do not silently convert missing data into a default truth value.

39. Visual State vs Runtime State

Visual state may include:

selected
hovered
active
hidden
collapsed
focused

Runtime state may include:

moving
heating
faulted
probing
loading
unloading

These are different categories.

A runtime state should not silently modify configuration.

40. Connection Geometry

The visual path of a connection is presentation information.

It may use:

straight line
curve
polyline
orthogonal routing
manual routing
automatic routing

The semantic endpoints remain the same.

Changing visual routing does not change machine semantics.

41. Visual Layout

Canvas coordinates are presentation data.

Do not infer:

physical X
physical Y
physical Z

from:

screen X
screen Y

Machine physical placement will eventually use coordinate frames and transforms.

42. Groups

Visual groups may represent:

subsystem
assembly
organizational grouping
collapsed region

but:

Visual Group ≠ Canonical Subsystem

A group may reference a canonical subsystem.

Grouping alone does not create semantic containment.

43. Multiple Views

The same semantic object may appear in several visual views.

Example:

Motor A
  ├─ Physical View
  ├─ Electrical View
  ├─ Motion View
  └─ Control View

The visual representation can differ between views.

The underlying semantic object remains the same.

44. Zoom / Detail Level

The eventual UI should support different detail levels.

Close:

pins
ports
individual wires
signals

Far:

components
cables
subsystems
high-level relationships

The prototype does not need complete semantic level-of-detail rendering.

It should avoid requiring multiple copies of the underlying machine model.

45. Directionality

Base physical connection drawings should not imply direction based on layout.

For example:

A ───── B

does not automatically mean:

A → B

A signal may have semantic direction.

A physical wire may not.

Diagnostic visualization may later show activity through:

pulse
glow
animation

without changing the connection's base semantics.

46. First Prototype Technology

The existing project repository should be inspected before choosing implementation technology.

Do not assume:

framework
language
renderer
build system
directory structure

from this handoff alone.

The implementation should fit the repository rather than creating an unrelated application alongside it.

47. First Implementation Milestone

The first milestone should be the smallest useful interactive canvas.

It should demonstrate:

canvas
pan
zoom
component palette
node placement
node movement
selection

No advanced machine semantics are required yet.

The implementation should nevertheless follow the architectural boundaries in this handoff.

48. Second Milestone

The next milestone should be:

ports
connection drag
connection preview
compatibility feedback
connection creation
connection deletion

This is the first major test of the port/connection architecture.

49. Third Milestone

Then:

save
load
restore nodes
restore ports
restore connections
restore layout

The saved file should remain understandable and debuggable.

50. Fourth Milestone

Then create a simplified Promega machine.

The purpose is to test:

multiple motors
CoreXY
drivers
controller
probe
heater
multiple relationship types

Do not attempt to recreate the entire Promega configuration.

51. Fifth Milestone

Then construct the CFS stress-test subsystem.

The purpose is to test:

subsystem
multiple motors
multiple sensors
material paths
buffer
local controller
communication
many-to-many relationships

This is intentionally a harder test than the Promega.

52. What the Coder Should Avoid

Do not:

build a firmware configurator
build a CAD system
build a full circuit-design application
build a complete machine simulator
build the final ontology
build a complete parts database
build every validation rule
build complete safety analysis

The first visual prototype is an architectural experiment.

53. Do Not Over-Generalize

The opposite danger also exists.

Do not spend the first implementation milestone building an abstract universal graph engine capable of representing every conceivable engineering system.

Start with the concrete requirements.

Generalize only where the current use cases justify it.

The goal is:

simple enough to build
structured enough to survive
54. Do Not Encode Temporary Assumptions

Some concepts are intentionally unresolved.

Examples:

Resource
Flow
Route
Channel
exact Port subtype hierarchy
exact canonical Function structure

Do not create permanent architecture around these terms merely because an implementation shortcut appears convenient.

55. Feedback to Architecture

Implementation should report back when it reveals:

a relationship that cannot be represented
a missing concept
a false one-to-one assumption
a difficult view transition
a persistence problem
a semantic/visual identity conflict
a port/connection problem
a performance problem caused by the model

These discoveries are valuable.

They should be brought back to the architecture/research process rather than hidden through UI-specific hacks.

56. Expected Relationship Between Coder and Architecture Work

The intended workflow is:

Architecture / Research
        ↓
Checkpoint
        ↓
Implementation
        ↓
Implementation discovery
        ↓
Architecture refinement
        ↓
Implementation update

The architecture conversation remains responsible for long-term semantic decisions.

The implementation conversation is responsible for turning sufficiently mature decisions into working software and reporting implementation evidence.

57. Current Repository Workflow

Repository changes are currently being handled manually.

The architecture/research process will produce complete file contents at meaningful checkpoints.

The project owner will place those files into the repository.

The Coder should therefore treat Git history as the durable project record but should not assume that it can directly push changes from this conversation.

58. Documentation Expectations

Implementation discoveries that materially affect architecture should be documented.

Do not leave critical architectural assumptions buried only inside source code.

Examples:

why connections terminate at ports
why visual nodes are separate from canonical objects
why one-to-many axis/motor relationships are supported
why firmware-specific terminology is not canonical

The exact documentation location may evolve.

59. First Engineering Question for the Coder

Before writing substantial code, inspect the existing repository and determine:

current language(s)
current application structure
existing UI code
existing build system
existing dependencies
existing entry point
existing tests
existing conventions

Then recommend the smallest implementation path consistent with the repository.

Do not replace or restructure the repository unnecessarily.

60. First Implementation Review

Before moving beyond the first milestone, review whether the implementation has accidentally introduced assumptions such as:

one node = one machine object
one connection = one wire
one axis = one motor
one motor = one axis
one sensor = one function
one parent = one hierarchy
canvas coordinates = machine coordinates
firmware term = canonical concept

Correct those assumptions early.

61. Prototype Definition of Done

The visual prototype has reached its first useful architectural checkpoint when it can:

create nodes
move nodes
select nodes
display ports
create port-to-port connections
reject obvious incompatible connections
delete connections
delete nodes
save
load
represent many-to-many relationships
represent a simplified Promega

while maintaining the architectural boundaries defined in this handoff.

62. What Comes After the First Prototype

Later development may add:

multiple views
richer port semantics
typed relationships
semantic validation
coordinate frames
kinematics
process views
material paths
runtime state
diagnostics
signal activity
hardware library integration
machine component creation
firmware mappings

These should be added incrementally.

63. Final Guidance

The implementation should not attempt to prove the ontology is complete.

The implementation should make the ontology testable.

When an implementation choice conflicts with the emerging semantic model, prefer bringing the conflict back to architecture rather than hiding it behind a special case.

Likewise, when implementation reveals that an architectural assumption is unnecessarily complicated, report that back to the architecture process.

The project is intentionally using both directions:

Architecture informs implementation
Implementation tests architecture
64. Final Principle

The visual builder is intended to become:

A visual interface for working with a structured machine model.

It is not intended to become:

A drawing program that happens to contain machines.

The first prototype should therefore demonstrate that a human can construct and manipulate machine relationships visually while the underlying representation remains:

semantic
typed
extensible
firmware-independent
view-independent
and capable of representing real-world complexity.