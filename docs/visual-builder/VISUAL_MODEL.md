# Machine Builder Visual Builder — Visual Model

## Status

**Document:** Visual Builder Visual Model  
**Version:** 0.1  
**Status:** Initial implementation handoff  
**Project:** Machine Builder / Machine Development Environment (MDE)

---

# 1. Purpose

This document defines the implementation-facing model used by the first Machine Builder Visual Builder prototype.

It is deliberately **not** the final canonical Machine Builder ontology.

The visual model exists to provide a stable abstraction between:

```text
Canonical Machine Model
        ↓
Visual Model
        ↓
Renderer / Interaction System

The purpose of this layer is to allow the visual builder to evolve while the canonical ontology continues to be researched and refined.

2. Core Principle

The visual model describes how the machine is represented visually and interactively.

It does not define the complete semantics of the machine.

A visual object may represent:

a canonical machine object
several canonical objects
a temporary editing object
a group or presentation construct
an implementation-specific representation

Likewise, one canonical object may have multiple visual representations in different views.

Therefore:

Visual Object ≠ Canonical Object

although a visual object may reference a canonical object.

3. Conceptual Model

The minimum visual model is:

VisualModel
    ├── Nodes
    ├── Ports
    ├── Connections
    ├── Groups
    ├── Properties
    └── Views

Conceptually:

Node
 ├─ ports
 ├─ properties
 ├─ semantic reference
 └─ visual state

Port
 ├─ parent node
 ├─ semantic type
 ├─ direction/interface role
 └─ visual state

Connection
 ├─ endpoints
 ├─ semantic type
 └─ visual representation

View
 ├─ visible nodes
 ├─ visible connections
 ├─ layout
 └─ presentation state
4. Node

A Node is the fundamental visual representation of something that can be placed, selected, moved, grouped, or displayed on the canvas.

A node should have, conceptually:

Node
 ├─ id
 ├─ semantic_reference
 ├─ node_type
 ├─ label
 ├─ position
 ├─ size
 ├─ rotation
 ├─ ports
 ├─ properties
 ├─ parent/group
 └─ visual_state

The exact implementation language and representation are intentionally unspecified in this document.

5. Node Identity

Every visual node requires a unique identity within the visual model.

The visual ID identifies the visual object.

It does not necessarily identify the underlying machine component.

Example:

visual node ID:
    visual-node-024

semantic reference:
    machine-component-017

This allows the same semantic object to appear in multiple views or potentially multiple visual contexts.

6. Semantic Reference

A node may reference an object in the canonical machine model.

Conceptually:

Node
   └── semantic_reference → Canonical Object

The semantic reference should be optional during early experimentation.

A visual object may exist before its canonical semantic identity has been established.

This is useful for:

temporary components
design exploration
imported graphics
partially defined machines
objects whose semantic classification is still unresolved

The visual layer must therefore not require every visual node to have a finalized canonical identity.

7. Node Type

node_type describes the visual/editor classification of the node.

Examples may include:

component
subsystem
controller
motor
sensor
tool
axis
assembly
annotation
group

These classifications are provisional.

They should not be treated as the final Machine Builder ontology.

A node type is primarily useful for:

default visual appearance
palette filtering
interaction behavior
initial port templates
view presentation

It should not become a substitute for canonical semantic relationships.

8. Node Position

Position is visual information.

It should not be interpreted as physical machine position unless the canonical model explicitly establishes such a relationship.

For example:

node.position = (500, 300)

means:

Draw this node at this canvas location.

It does not mean:

The physical component exists at X=500, Y=300 in machine coordinates.

Physical location should eventually be represented semantically through the canonical model.

9. Node Size

Node size is also visual information.

It may represent:

fixed component dimensions for display
automatically calculated layout dimensions
user-adjusted display size
collapsed/expanded presentation

It should not automatically represent physical dimensions.

A motor node that is displayed as 120 × 60 pixels does not imply that the physical motor is 120 × 60 mm.

10. Rotation

Visual rotation represents how the node is displayed.

It must be possible for a node to be rotated visually without necessarily changing its physical orientation.

Physical orientation belongs to the semantic/coordinate model.

This distinction will become particularly important when visualizing:

belt printers
robotic systems
rotary axes
angled toolheads
machine assemblies
coordinate transformations
11. Port

A Port is a connection/interface location belonging to a visual node.

Conceptually:

Node
 ├── Port
 ├── Port
 └── Port

A port should have, conceptually:

Port
 ├─ id
 ├─ parent_node
 ├─ semantic_type
 ├─ interface_role
 ├─ directionality
 ├─ compatibility information
 └─ visual representation

The implementation should not assume that a port is an electrical pin.

Ports may eventually represent:

electrical
signal
communication
mechanical
material
fluid
logical
other domain-specific interfaces
12. Port Identity

A port requires a unique visual-model identity.

Example:

visual-port-013

The port may optionally reference a semantic port in the canonical machine model.

This allows the visual editor to support incomplete or provisional designs.

13. Port Semantic Type

A port should have enough semantic information to support compatibility checking.

A simplified initial representation might distinguish:

electrical
signal
communication
mechanical
material
fluid
logical

A more detailed implementation may eventually add properties such as:

voltage
current
signal type
protocol
connector type
direction
media/material type
pressure
mechanical interface type

The first prototype does not need to implement every property.

The architecture should allow these fields to be added later without redesigning the connection system.

14. Port Directionality

Directionality is semantic information, not visual geometry.

Possible values may eventually include:

input
output
bidirectional
passive
unknown

However, not every physical connection is meaningfully directional.

For example:

electrical wire
mechanical attachment

may be represented without a directional implication.

The editor must not infer direction simply because one port appears on the left and another appears on the right.

15. Connection

A Connection represents a relationship between one or more endpoints in the visual model.

The minimum conceptual form is:

Connection
 ├─ id
 ├─ endpoints
 ├─ semantic type
 └─ visual state

The first prototype may restrict connections to two endpoints.

The internal architecture should not make it impossible to support more complex topologies later.

16. Connection Endpoints

A connection should reference ports rather than arbitrary nodes whenever practical.

Preferred:

Connection
 ├── Port A
 └── Port B

Avoid:

Connection
 ├── Node A
 └── Node B

because this loses the semantic information about which interface participates in the connection.

This distinction becomes essential when a component has many ports.

For example, a controller could have:

24V input
GND
CAN
USB
STEP
DIR
endstop
thermistor
heater output
fan output

A connection to the controller is meaningless unless the relevant port is known.

17. Connection Type

Connections should have an explicit semantic domain/type.

Initial candidate values:

electrical
signal
communication
mechanical
material
fluid
logical
unknown

These categories are provisional.

The visual system should make them extensible.

A connection type should influence:

compatibility
rendering
filtering
visual styling
future validation

but should not dictate the complete canonical semantics.

18. Connection Geometry

The visual path of a connection is presentation information.

It may include:

straight line
polyline
curve
routing points
automatic route
manual route

The visual geometry must not redefine the semantic connection.

For example:

Connection A → B

remains the same semantic relationship whether it is displayed as:

A ───────── B

or:

A ───┐
    ├────── B
    └───┐

The geometry is editable without changing the underlying relationship.

19. Connection Direction and Activity

Visual connection geometry must not imply signal direction.

Direction may be shown through additional visual information when relevant.

Future examples include:

animated pulse
glow
flow indicator
active-state marker

These visual effects should be driven by semantic/runtime information.

They should not redefine the connection itself.

20. Groups and Subsystems

A Group is a visual organization construct.

It may represent:

a subsystem
an assembly
an organizational grouping
a collapsed detail region
a temporary editing group

A group may contain nodes and possibly nested groups.

However:

Visual Group ≠ Canonical Subsystem

A group may reference a canonical subsystem, but grouping should remain a view-level construct.

This permits different views to organize the same objects differently.

21. Parent/Child Relationships

Visual parentage is primarily about display/layout.

For example:

Group A
 ├─ Node 1
 ├─ Node 2
 └─ Node 3

means that those nodes are visually contained by Group A.

It does not automatically establish a physical or functional relationship in the canonical model.

Canonical containment should be represented separately.

22. Properties

A visual node may expose properties for editing or display.

Examples:

label
description
color/theme
collapsed
display mode
icon

Semantic properties may also be displayed:

part number
voltage
motor type
firmware representation

but semantic properties should come from the underlying machine model rather than being duplicated as unrelated visual fields whenever practical.

23. Views

A View represents a particular visual presentation of the same underlying machine model.

A view may define:

View
 ├─ id
 ├─ name
 ├─ visible nodes
 ├─ visible connections
 ├─ layout positions
 ├─ zoom
 ├─ pan
 ├─ detail level
 └─ presentation settings

Examples:

System View
Electrical View
Motion View
Process View
Material View
Control View
Diagnostic View

The first prototype may implement only one view.

The architecture should not assume that one view is the machine.

24. Multiple Views of the Same Object

A canonical machine object may appear in several views.

Example:

Motor A

may appear in:

Motion View
Electrical View
Physical View
Control View

It remains the same semantic object.

Each view may have independent:

position
visibility
display detail
connection emphasis
labels
25. View-Specific Connections

The same semantic relationship may be displayed differently in different views.

For example:

Electrical View:
    individual wires

System View:
    cable between assemblies

Control View:
    logical signal relationship

The visual model should therefore distinguish:

semantic connection

from:

visual representation of connection

This is important for future multi-level wiring views.

26. Selection State

Selection is temporary interaction state.

It should not be stored as machine semantics.

Possible state includes:

selected
hovered
focused
active
disabled
hidden

Selection may apply to:

node
port
connection
group
27. Interaction State

The editor may also maintain transient interaction state such as:

dragging node
creating connection
dragging connection endpoint
panning
zooming
multi-selecting
editing property

These states should not be serialized as part of the canonical machine model.

They may or may not be serialized in a view/session representation depending on implementation needs.

28. Temporary Objects

The visual editor may create temporary objects during interaction.

Examples:

temporary connection
drag preview
uncommitted node
selection rectangle
connection compatibility indicator

These are UI state, not machine model entities.

The implementation should distinguish:

committed visual model

from:

temporary interaction state
29. Compatibility Checking

Compatibility should be evaluated using semantic information associated with ports.

Conceptually:

Port A
    ↓
Compatibility Engine
    ↓
Port B

Possible results:

compatible
incompatible
conditionally compatible
unknown

The editor should not require all compatibility rules to exist before allowing experimentation.

For the first prototype, a small ruleset is sufficient.

The architecture should eventually support:

domain compatibility
direction compatibility
voltage compatibility
current compatibility
protocol compatibility
interface compatibility
material compatibility
mechanical compatibility
30. Connection Creation

The intended interaction is:

User presses on Port A
        ↓
drag begins
        ↓
temporary connection appears
        ↓
user moves toward Port B
        ↓
compatibility feedback is displayed
        ↓
user releases
        ↓
valid connection is committed

For an invalid destination:

release
   ↓
connection rejected
or
warning/confirmation

The exact UX is a later implementation decision.

The semantic validation should remain separate from the visual interaction code.

31. Node Creation

The intended initial interaction is:

Component Palette
       ↓
drag component
       ↓
canvas
       ↓
drop
       ↓
create visual node

The initial node may contain:

a default label
default visual dimensions
predefined ports
a provisional semantic type

The user should then be able to modify properties.

32. Moving Nodes

Dragging a node changes its visual position.

Existing connections should remain associated with the same ports.

Example:

Node A ───── Node B

Moving Node A should produce:

            Node A
              │
              └──────── Node B

without creating a new semantic connection.

The connection follows its endpoints.

33. Deletion

Deleting a node should explicitly handle dependent visual objects.

For example:

Node
 └─ Ports
      └─ Connections

Deleting a node may require:

deleting dependent visual ports
deleting or invalidating connections
warning about consequences
preserving semantic objects separately if appropriate

This behavior should be implemented through explicit model mutations rather than direct renderer manipulation.

34. Model Mutation

Changes made by the user should eventually be represented as explicit operations/mutations rather than arbitrary UI-side object manipulation.

Examples:

CreateNode
DeleteNode
MoveNode
CreatePort
CreateConnection
DeleteConnection
ChangeProperty
CreateGroup
MoveIntoGroup
RemoveFromGroup

This is recommended because it will eventually support:

undo/redo
validation
event logging
collaboration
change history
command-based editing
future automation

The exact command architecture is an implementation decision.

35. Undo / Redo

The first prototype may implement minimal undo/redo or defer it.

The visual model should nevertheless be designed so user changes can eventually be represented as discrete mutations.

Avoid architectures where a user drag directly mutates many unrelated objects with no identifiable operation.

36. Serialization

The visual model must eventually be serializable.

At minimum it should be possible to persist:

nodes
ports
connections
groups
properties
view layout

The serialized visual model must not assume that it is the permanent canonical Machine Builder file format.

It is an implementation format for the prototype unless later adopted.

37. Canonical-to-Visual Relationship

The intended direction is:

Canonical Object
       ↓
Visual Node

and:

Canonical Relationship
       ↓
Visual Connection

A visual edit may eventually produce a requested canonical mutation:

Visual Action
       ↓
Semantic Validation
       ↓
Canonical Model Mutation
       ↓
Visual Model Update

This is preferable to allowing the renderer to become the authoritative source of machine semantics.

38. Visual-Only Objects

Some visual objects will have no direct canonical equivalent.

Examples include:

annotation
separator
label
legend
group boundary
measurement ruler
temporary guide
layout helper

The visual model must support these without forcing them into the canonical machine ontology.

39. Canonical Objects Without Visual Nodes

Not every canonical object needs to be visible in every view.

A machine model may contain:

internal controller state
measurement definition
hidden wiring relationship
coordinate frame
safety function

without the current visual view displaying a dedicated node.

The view controls presentation.

The canonical model remains independent.

40. Many-to-Many Relationships

The visual model must support relationships that do not correspond to a simple pair of parent/child nodes.

Examples:

one axis ↔ multiple motors
one motor ↔ multiple axes
one sensor result ↔ multiple functions
one function ↔ multiple components
one subsystem ↔ multiple functions

A visual representation may choose how to display these relationships, but the underlying model must not prohibit them.

41. Example: CoreXY

A simplified visual representation might look like:

 ┌─────────┐               ┌─────────┐
 │ Motor A │               │ Motor B │
 └────┬────┘               └────┬────┘
      │                          │
      └────────┬───────┬─────────┘
               ↓       ↓
             KINEMATIC SYSTEM
               ↓       ↓
              X AXIS  Y AXIS

The implementation must not require:

Motor A = X
Motor B = Y

The kinematic relationship is what defines how the motors contribute to X/Y motion.

42. Example: Multiple Z Motors

A machine may visually contain:

             Z Axis
          /     |     \
         /      |      \
     Motor A  Motor B  Motor C

The visual model must permit all three motors to participate in the same logical motion system.

43. Example: CFS

A CFS may be represented at several levels.

High-level view:

Printer ───────── CFS ───────── Extruder

Detailed view:

CFS
 ├─ Source 1
 ├─ Source 2
 ├─ Source 3
 ├─ Source 4
 ├─ feeders
 ├─ sensors
 ├─ lower transport
 ├─ buffer
 └─ controller

Material-flow view:

Source
   ↓
Feeder
   ↓
Transport Path
   ↓
Buffer
   ↓
Printer

Electrical/communication view:

Power
  +
RS-485
  +
buffer signals

These views represent the same underlying system.

44. Visual Detail Levels

The visual model should permit different detail levels.

Conceptually:

Level 1:
Machine → Subsystem → Component

Level 2:
Component → ports → major connections

Level 3:
individual pins/signals/wires

Detail level is presentation state.

It should not require multiple copies of the canonical machine model.

45. Styling

Visual styling should be treated as presentation.

Possible future properties include:

shape
icon
border
fill
line style
line width
label style
state indicator
domain indicator
warning indicator

The styling system should eventually permit semantic-driven styling without requiring semantic data to be stored directly as presentation values.

For example:

semantic:
    port type = communication

presentation:
    communication-port visual style
46. Runtime/Diagnostic Visualization

Future runtime information may modify the visual presentation:

active signal
moving axis
temperature rising
sensor triggered
faulted drive
material moving
connection active

These should be treated as runtime overlays or visual state.

They should not mutate the machine configuration simply because something is currently active.

47. Physical Layout vs Visual Layout

The machine may eventually contain physical placement information such as:

mounted on
position relative to
orientation relative to
distance
coordinate frame

The visual layout may independently contain:

canvas position
display orientation
view-specific spacing

These are intentionally different.

A useful implementation rule is:

Never infer physical placement from visual placement.

48. Relationship to the Future Canonical Ontology

The visual model should be considered an adapter/view layer over the canonical ontology.

The canonical ontology currently includes concepts such as:

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

This list is still evolving.

The visual model must therefore avoid relying on a fixed final class hierarchy.

49. Relationship to Firmware

Firmware-specific concepts may eventually be displayed in the visual UI.

Examples:

Klipper:
    [stepper_x]

RRF:
    M584 mapping

Marlin:
    stepper configuration

These are implementation mappings.

The visual model should not make them the canonical identity of the component.

A machine component may have:

canonical identity
    +
firmware implementation mapping

and the visual layer may choose to display either or both.

50. Visual Model Design Rule

The visual model should answer:

What should the user see and interact with?

The canonical model should answer:

What does the machine actually mean?

The renderer should answer:

How is that visual representation drawn?

The interaction system should answer:

How does the user's action modify the model?

These responsibilities should remain separate.

51. Initial Minimal Data Shape

A conceptual first implementation might look approximately like:

VisualModel
 ├─ nodes[]
 │   ├─ id
 │   ├─ semantic_reference?
 │   ├─ node_type
 │   ├─ label
 │   ├─ position
 │   ├─ size
 │   ├─ rotation
 │   └─ ports[]
 │
 ├─ connections[]
 │   ├─ id
 │   ├─ endpoint_a
 │   ├─ endpoint_b
 │   └─ connection_type
 │
 ├─ groups[]
 │   ├─ id
 │   ├─ label
 │   └─ members[]
 │
 └─ views[]
     ├─ id
     ├─ name
     └─ presentation state

This is intentionally conceptual.

The Coder should choose the implementation representation after considering the rest of the codebase and technology stack.

52. Non-Goals

This visual model does not currently attempt to define:

complete canonical ontology
complete electrical semantics
complete kinematics
complete process semantics
complete safety semantics
firmware schema
database schema
CAD geometry model
machine simulation model

Those remain separate areas of Machine Builder development.

53. Design Test

The visual model should be considered structurally sound if it can represent all of the following without special-case redesign:

simple Cartesian printer
CoreXY printer
multi-motor Z axis
IDEX printer
toolchanger
CFS material system
CNC machine with rotary axis
laser machine
robotic manipulator
multi-controller machine
machine with closed-loop motion
machine containing non-motion subsystems

The first prototype does not need to fully implement each one.

The model must simply avoid making them impossible.

54. Final Principle

The visual builder should be a window into the machine model, not the machine model itself.

A user should be able to:

see
place
connect
move
organize
inspect
edit
filter
and eventually diagnose

machine objects visually.

But every important machine meaning should ultimately belong to the semantic/canonical model and its typed relationships.

The visual system should make those semantics easier to understand and manipulate without becoming responsible for inventing them.