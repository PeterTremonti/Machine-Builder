# Machine Builder Visual Builder — Prototype Requirements

## Status

**Document:** Visual Builder Prototype Requirements  
**Version:** 0.1  
**Status:** Initial implementation handoff  
**Project:** Machine Builder / Machine Development Environment (MDE)

---

# 1. Purpose

This document defines the functional behavior expected from the first Machine Builder Visual Builder prototype.

It translates the scope and visual model into concrete user-facing and system-facing requirements.

These requirements are intended to guide implementation and testing.

They do not define the final Machine Builder application.

---

# 2. Primary Prototype Objective

The prototype should demonstrate that a user can construct and manipulate a machine representation visually while the underlying model remains structured, semantic-aware, and independent from the renderer.

The prototype should prioritize:

1. Reliable interaction.
2. Correct model behavior.
3. Clear separation between visual and semantic information.
4. Extensibility.
5. Ease of experimentation.

Visual polish is secondary.

---

# 3. Workspace Requirements

The prototype shall provide a workspace containing, at minimum:

```text
Component Palette
Canvas
Selection / Property Area
Basic navigation controls

A possible conceptual arrangement is:

┌───────────────────────────────────────────────────────────────┐
│ Toolbar / navigation                                           │
├───────────────┬───────────────────────────────────────────────┤
│               │                                               │
│ Component     │                                               │
│ Palette       │                  Canvas                        │
│               │                                               │
│               │                                               │
│               │                                               │
├───────────────┴───────────────────────────────────────────────┤
│ Optional status / property area                               │
└───────────────────────────────────────────────────────────────┘

The exact UI layout is an implementation decision.

The architecture must allow the layout to change without changing the underlying machine representation.

4. Canvas

The canvas shall support:

placing nodes
selecting nodes
moving nodes
selecting connections
creating connections
deleting objects
panning
zooming
displaying groups/subsystems
displaying ports
displaying connection feedback

The canvas is a view of the visual model.

It is not the machine model itself.

5. Pan

The user shall be able to pan the canvas independently of machine data.

Panning must not alter:

node semantic identity
node relationships
physical machine position
connection semantics

Panning changes only the current view.

6. Zoom

The user shall be able to zoom in and out.

Zoom should affect presentation scale only.

Zooming must not alter:

machine dimensions
physical locations
coordinate-frame relationships
connection topology

The visual system should remain usable at multiple zoom levels.

7. Node Placement

The user shall be able to drag a component from the component palette onto the canvas.

Dropping the component shall create a new visual node.

A newly created node should receive:

unique visual ID
node type
default visual dimensions
default label
default ports where appropriate

The exact defaults may be implementation-defined.

8. Node Movement

The user shall be able to move a node by dragging it.

When a node moves:

its visual position changes
connected visual relationships remain attached to the same ports
semantic references remain unchanged
connection topology remains unchanged

Moving a node must not create or destroy semantic relationships.

9. Node Selection

The user shall be able to select a node.

Selection should provide clear visual feedback.

Selection should not alter the canonical machine semantics.

The system should support, at minimum:

single selection
deselect
select another object

Multi-select may be added if straightforward, but is not required for the first demonstration.

10. Port Selection

Ports should be individually identifiable and selectable when the current zoom/detail level supports it.

The user should be able to start connection creation from a port.

Port selection must not require the user to select the entire node first.

11. Connection Creation

The primary connection interaction shall be:

Press / grab Port A
        ↓
Drag
        ↓
Temporary connection follows pointer
        ↓
Hover Port B
        ↓
Compatibility feedback
        ↓
Release
        ↓
Connection created or rejected

The interaction should feel direct and predictable.

12. Connection Preview

During connection creation, the visual system should display a temporary connection.

The preview should:

originate from the selected port
follow the pointer
visually distinguish itself from committed connections
indicate compatible/incompatible targets where practical

The preview is temporary interaction state.

It is not committed machine data.

13. Connection Compatibility

The system shall support basic compatibility evaluation between ports.

The compatibility engine may initially use a small rule set.

Possible results:

compatible
incompatible
unknown
conditionally compatible

The implementation should not require a complete electrical or machine-engineering rules engine for the prototype.

14. Compatibility Examples

The prototype should be capable of expressing basic examples such as:

Electrical power output
        ↔
Compatible electrical power input

as potentially compatible.

And:

24V power output
        ↔
Thermistor input

as incompatible.

Likewise:

RS-485 communication port
        ↔
RS-485 communication port

may be compatible.

The initial implementation may simplify these rules.

It must not architecturally prevent richer rules later.

15. Invalid Connection Handling

When the user attempts to create an invalid connection, the system should not silently create a semantically invalid connection.

Acceptable initial behaviors include:

reject connection
display incompatibility
require explicit confirmation

The preferred default for the first prototype is simple rejection with clear visual feedback.

16. Unknown Compatibility

The system may encounter ports whose compatibility cannot yet be determined.

Unknown compatibility should not automatically mean:

valid

or:

invalid

The system should represent the distinction.

Possible prototype behavior:

allow with warning
allow as provisional
show unknown state

The implementation should keep this state distinguishable from confirmed compatibility.

17. Connection Deletion

The user shall be able to select a committed connection and delete it.

Deleting a visual connection should remove the visual relationship.

If the visual model is currently backed by a canonical model mutation system, the change should eventually propagate through that layer.

The renderer should not directly manipulate unrelated semantic objects.

18. Node Deletion

The user shall be able to delete a node.

Deleting a node must account for dependent visual connections and ports.

At minimum:

Node deleted
    ↓
its visual ports cease to exist
    ↓
associated visual connections are removed or invalidated

The implementation should avoid leaving orphaned connections.

19. Grouping

The prototype should support basic grouping or subsystem representation.

A group may contain:

nodes
nested groups
visual relationships

A group may have:

id
label
position
size
collapsed/expanded state

Grouping is primarily a visual organization mechanism.

It should not automatically create a canonical subsystem relationship.

20. Group Movement

Moving a visual group may move the visual objects contained within it.

The operation should not change the semantic identity of the contained objects.

The exact implementation of nested-group movement is flexible.

21. Basic Property Editing

The user should be able to inspect basic properties of a selected node.

At minimum, the prototype should be able to display:

label
node type
visual ID
semantic reference if present

Where practical, the user should be able to edit the label.

Semantic properties may be displayed but should remain distinguishable from visual properties.

22. Property Types

The implementation should distinguish, conceptually:

Visual Property
Semantic Property
Derived Property
Runtime State

For example:

x/y canvas position

is a visual property.

motor part number

is a semantic property.

estimated steps/mm

may be a derived property.

motor currently moving

is runtime state.

The prototype need not implement all four categories fully.

It must avoid conflating them architecturally.

23. Component Palette

The palette should provide a small set of component templates.

Initial candidates:

Controller
Motor
Driver
Sensor
Heater
Extruder
Tool
Generic Component
Subsystem

The initial palette is only for demonstrating the visual engine.

The final Machine Builder palette will be much larger.

24. Node Templates

A node template may define default:

node type
label
visual appearance
ports
default property set

Templates must not be confused with actual machine components.

Dropping a template creates a new visual node.

25. Generic Component

The prototype should include a generic component type.

A generic component should allow the user to experiment with:

label
ports
basic properties
connections

This provides a useful way to test the visual system without requiring every possible machine component to have a predefined type.

26. Port Creation

If practical during the first prototype, ports should be definable on a generic component.

If this is too much for the initial implementation, ports may instead be provided only through predefined templates.

The architecture should still allow arbitrary port definitions later.

27. Port Editing

Long-term, users will need to define or edit:

port name
port type
domain
direction
compatibility

The first prototype need not implement all of these.

At minimum, the data model should not make these properties impossible to add.

28. Multiple Connection Domains

The implementation must not assume all connections are electrical.

At minimum, the architecture must remain extensible for:

electrical
signal
communication
mechanical
material
fluid
logical

The first prototype may visually distinguish only a subset.

29. Connection Styling

Different connection types may eventually use different visual styles.

Examples:

electrical connection
communication connection
material path
mechanical connection

The first prototype may use a simple default style.

The semantic connection type should remain available independently of the style.

30. Connection Routing

The initial prototype may use:

straight lines
simple curves
simple orthogonal routing

No sophisticated routing engine is required.

Routing is visual information.

Changing the route must not change the semantic endpoints.

31. Relationship Labels

Connections may eventually have labels.

Examples:

24V
GND
RS-485
CAN
Filament
Tool interface

Labels are presentation unless explicitly tied to semantic properties.

The first prototype may omit labels or provide simple editable labels.

32. Direction Indicators

The first prototype should not imply direction through connection geometry.

If a connection has semantic direction, the UI may later display:

arrow
flow marker
signal pulse

The baseline connection should remain visually nondirectional unless a particular view intentionally chooses otherwise.

33. Visual State

The visual system may provide state indicators for:

selected
hovered
active
disabled
warning
error
hidden

These are visual/editor states.

They should not automatically modify the canonical machine state.

34. Runtime State Separation

Future live machine integration may provide runtime states such as:

moving
heating
faulted
probing
loading
unloading
active

These must be treated separately from configuration.

For example:

Motor state = moving

does not mean:

Motor configuration has changed

The first prototype does not need live-machine integration.

35. Semantic References

A visual node may optionally reference a semantic machine object.

Example:

visual_node:
    id = "visual-001"
    semantic_reference = "component-017"

The prototype should support nodes without semantic references.

This allows visual experimentation before semantic validation is complete.

36. Duplicate Visual Representations

The architecture should permit one semantic object to be represented more than once when necessary.

Examples:

same motor shown in:
    physical view
    electrical view
    motion view

The representations may share a semantic reference while having different visual state.

The prototype does not need to implement multiple-view synchronization fully, but its data model must not forbid it.

37. View Creation

The first prototype may begin with a single default view.

The visual model should nevertheless conceptually support:

View
 ├── visible nodes
 ├── visible connections
 ├── layout
 └── presentation settings

A later implementation may create multiple views without replacing the underlying machine model.

38. Save

The user shall be able to save the current visual model.

The saved representation should include enough information to restore:

nodes
ports
connections
groups
properties
view layout

The exact file format is an implementation decision.

The prototype's visual serialization format should not be assumed to be the final Machine Builder canonical file format.

39. Load

The user shall be able to load a previously saved visual model.

Loading should restore:

nodes
node positions
ports
connections
groups
properties
view information

The visual system should validate loaded data sufficiently to avoid crashing on malformed or incomplete input.

40. Incomplete Data

Incomplete semantic information is expected.

For example:

component exists
but part number unknown

or:

port exists
but compatibility unknown

The visual editor should permit incomplete designs.

Unknown must remain distinguishable from:

blank
unset
not applicable
false
unused

The prototype does not need a complete null/unknown framework yet, but should avoid treating missing information as confirmed information.

41. Undo / Redo

Undo/redo is desirable.

At minimum, implementation architecture should make it possible to add undo/redo later.

User actions should therefore be representable as identifiable mutations, such as:

CreateNode
DeleteNode
MoveNode
CreateConnection
DeleteConnection
ChangeProperty
CreateGroup

The first prototype may implement a minimal subset.

42. Model Mutations

The interaction layer should ideally request changes through model operations rather than modifying renderer objects directly.

Conceptually:

User Action
    ↓
Interaction Handler
    ↓
Model Mutation
    ↓
Validation
    ↓
Visual Update

The renderer should display the resulting model.

43. Error Handling

The prototype should handle ordinary user errors without crashing.

Examples include:

dropping a component outside the canvas
dropping a connection on empty space
connecting incompatible ports
deleting a selected object with dependent relationships
loading malformed data

Errors should preferably be visible and understandable.

44. Performance Requirements

The first prototype does not need to establish production-scale performance targets.

It should nevertheless remain responsive while displaying a modest machine graph.

A useful initial target is:

dozens to a few hundred visual nodes

with multiple ports and connections.

The architecture should avoid obviously quadratic or uncontrolled update patterns where practical.

45. Extensibility Requirement

Adding a new component or port type should not require changes throughout the rendering and interaction system.

For example, adding:

PressureSensor

should primarily involve defining its semantic/template information.

It should not require rewriting:

canvas interaction
connection rendering
selection
zooming
serialization
46. Semantic Compatibility Requirement

Compatibility rules should be isolated from basic connection rendering.

Conceptually:

Port A
Port B
   ↓
Compatibility Service
   ↓
Compatibility Result

The renderer should consume the result.

This allows compatibility rules to become more sophisticated later without rewriting the visual interaction engine.

47. Canonical Model Independence

The prototype should remain usable while the canonical ontology changes.

For example, if:

Resource

is later split into multiple concepts, the visual editor should not require a complete rewrite.

Similarly, if:

Toolhead

is later replaced or refined through:

Carriage
MechanicalInterface
Tool

the visual layer should be able to accommodate the change.

48. Firmware Independence

The first prototype should not contain firmware-specific logic for:

Klipper
Marlin
RepRapFirmware
FluidNC
GRBLHAL
LinuxCNC

Firmware-specific concepts belong in a future implementation/mapping layer.

The visual system may eventually display firmware information as metadata.

It should not require firmware to function.

49. Promega Demonstration

The first demonstration should construct a simplified Promega representation.

Suggested nodes:

Promega Machine
Duet 2 Maestro
X Motor
Y Motor
X/Y Driver resources
Z Motor
Z Driver
IR Probe
Extruder/Heater

Suggested relationships:

Motor ports
Driver ports
Controller ports
Probe connection
Heater connection
CoreXY kinematic relationship

The exact semantic implementation of these relationships may remain provisional.

The point is to test the visual architecture with a real machine rather than an abstract example.

50. Promega Acceptance Test

The prototype should allow the user to:

Place the controller.
Place motors.
Place the probe.
Place the heater/extrusion component.
Create ports as defined by templates.
Drag compatible connections.
Move components after connections are created.
Zoom and pan.
Select components and inspect properties.
Save the resulting machine representation.
Reload it successfully.
Continue editing after reload.

The prototype should not require a firmware configuration to perform this test.

51. CFS Demonstration

The second major demonstration should represent the CFS as a subsystem.

It should eventually support at least:

CFS subsystem
 ├─ four material sources
 ├─ source/rewind motors
 ├─ filament-present sensors
 ├─ feeder motors
 ├─ lower transport mechanism
 ├─ lower filament sensor
 ├─ buffer
 ├─ buffer switch/sensor
 ├─ CFS controller
 └─ communication interface

The purpose is to stress-test the visual architecture with a subsystem containing many interacting objects.

52. CFS Acceptance Test

The prototype should eventually allow visualization of:

source
  ↓
feeder
  ↓
transport path
  ↓
lower feeder
  ↓
buffer
  ↓
printer

while also allowing:

sensors
motors
controller
communication

to be represented separately.

The test should confirm that the visual model does not require a subsystem to be represented as one monolithic node.

53. Many-to-Many Acceptance Tests

The visual model must be able to represent:

CoreXY:
    multiple motors → multiple logical axes

Multi-Z:
    multiple motors → one logical axis

Sensor:
    one measurement → multiple consumers

Function:
    one function → multiple implementing components

Subsystem:
    one function → multiple subsystems

The prototype does not have to calculate the full semantics of all examples.

It must not structurally prevent them.

54. Coordinate-System Acceptance Test

The visual architecture must not assume:

X = horizontal screen direction
Y = vertical screen direction
Z = depth

The canvas coordinates are display coordinates.

Future machine coordinate frames may be represented separately.

A later coordinate-aware view must be able to display:

Machine Frame
Work Frame
Tool Frame
Camera Frame

without requiring the canvas itself to become a machine coordinate system.

55. Physical vs Visual Position Acceptance Test

Moving a node on the canvas must not automatically alter:

physical machine position
coordinate-frame transform
mechanical relationship

unless a future explicit semantic operation intentionally changes those values.

56. Separation of Concerns Acceptance Test

The prototype architecture should make it possible to modify:

renderer

without rewriting:

semantic/model layer

and to modify:

semantic model

without rewriting:

basic canvas interaction

where reasonable.

This separation is one of the primary reasons for the prototype.

57. Future Diagnostic Compatibility

The design should leave room for future overlays representing:

signal activity
motor movement
temperature
sensor state
fault
material movement
communication activity

These should appear as visual/runtime overlays.

They should not require the visual model to be rebuilt.

58. Future Validation Compatibility

The eventual Machine Builder will need validation at several levels:

visual validity
model validity
connection validity
semantic validity
electrical validity
kinematic validity
configuration validity
firmware validity
safety validity

The first prototype only needs basic connection compatibility.

Its architecture should allow additional validation services later.

59. Explicit Non-Requirements

The first prototype does not require:

3D rendering
full CAD geometry
live machine control
complete simulation
automatic firmware generation
automatic firmware parsing
complete electrical-rule engine
complete kinematic solver
complete safety analysis
cloud collaboration
multi-user editing

These should not be allowed to delay the basic visual prototype.

60. Implementation Philosophy

The implementation should favor:

simple
explicit
testable
extensible
replaceable

over:

clever
highly optimized
over-generalized
framework-heavy

The first prototype exists to teach us what the actual Machine Builder visual system needs.

Implementation discoveries should be fed back into architecture work rather than hidden behind increasingly complicated code.

61. Primary Success Condition

The prototype is successful when a user can visually construct a small but non-trivial machine graph and manipulate it naturally without the implementation having to pretend that:

axis = motor
connection = wire
component = node
position = machine coordinate
sensor = feedback
function = firmware setting

The prototype should instead demonstrate that the visual system can preserve the distinctions established by the emerging Machine Builder semantic model.

62. Secondary Success Condition

The prototype should be sufficiently modular that the next stages can add:

richer port semantics
more connection domains
multiple views
semantic validation
machine properties
coordinate frames
kinematics
process representation
runtime state
diagnostics
firmware mappings

without replacing the fundamental canvas/interaction engine.

63. Final Design Principle

The first visual builder is an experiment in how a human should interact with a machine model.

It should therefore optimize for:

making machine structure and relationships understandable and editable

rather than:

making a diagram that merely looks like a machine.