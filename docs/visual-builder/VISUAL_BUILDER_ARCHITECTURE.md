# Machine Builder Visual Builder — Prototype Architecture

## Status

**Document:** Visual Builder Prototype Architecture  
**Version:** 0.1  
**Status:** Initial implementation handoff  
**Project:** Machine Builder / Machine Development Environment (MDE)

---

# 1. Purpose

This document defines the proposed architectural structure of the first Machine Builder Visual Builder prototype.

It exists to prevent the prototype from becoming tightly coupled to:

- the current experimental ontology
- one rendering technology
- one firmware
- one connection type
- one machine type
- one visual layout
- one eventual database structure

The prototype should be small enough to build quickly while preserving the architectural boundaries needed for the larger Machine Builder project.

---

# 2. Primary Architectural Principle

The visual builder should use a layered architecture:

```text
Canonical / Semantic Model
            ↓
Visual Model
            ↓
Application / Interaction Logic
            ↓
Renderer / UI

Not:

UI
 ↓
arbitrary objects
 ↓
machine semantics

The direction of dependency should generally flow downward toward more implementation-specific layers.

The renderer should not become the authority for machine semantics.

3. Major Layers

The prototype should conceptually contain at least these layers:

1. Semantic Adapter / Domain Boundary
2. Visual Model
3. Validation / Compatibility
4. Interaction / Command Layer
5. View State
6. Renderer
7. Persistence

A conceptual architecture is:

                    ┌───────────────────────┐
                    │ Canonical Machine     │
                    │ Model / Semantic      │
                    │ Layer                 │
                    └───────────┬───────────┘
                                │
                         semantic references
                                ↓
                    ┌───────────────────────┐
                    │ Visual Model           │
                    │ Nodes / Ports /        │
                    │ Connections / Groups   │
                    └───────────┬───────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ↓                       ↓
             Validation /              View State
             Compatibility                 │
                    │                       │
                    └───────────┬───────────┘
                                ↓
                    ┌───────────────────────┐
                    │ Interaction / Command │
                    │ Layer                 │
                    └───────────┬───────────┘
                                ↓
                    ┌───────────────────────┐
                    │ Renderer / UI         │
                    └───────────────────────┘

                    Persistence may operate
                    on model/view state through
                    explicit serialization.

The exact implementation structure may differ.

The separation of responsibilities should not.

4. Canonical Semantic Layer Boundary

The final Machine Builder will have a canonical machine model.

That model is still being developed.

The visual prototype must therefore treat the canonical semantic layer as an external contract, not as something it owns.

The first implementation may use a simplified placeholder semantic model.

The prototype should make it possible to replace that placeholder later.

5. Semantic Adapter

A semantic adapter should act as the boundary between canonical machine semantics and the visual model.

Conceptually:

Canonical Object
      ↓
Semantic Adapter
      ↓
Visual representation

and eventually:

Visual mutation
      ↓
Semantic validation
      ↓
Canonical model mutation

The prototype may begin with a minimal adapter.

It should not embed the entire ontology into the canvas code.

6. Visual Model

The visual model is the primary working model of the canvas.

Conceptually:

VisualModel
 ├── nodes[]
 ├── connections[]
 ├── groups[]
 └── views[]

It should be independent from rendering technology.

The renderer consumes the visual model.

The renderer must not own the visual model.

7. Visual Node

A visual node should contain conceptually:

VisualNode
 ├── id
 ├── semantic_reference?
 ├── node_type
 ├── label
 ├── geometry
 ├── ports[]
 └── visual_state

Where geometry includes:

position
size
rotation

The exact implementation representation is flexible.

8. Visual Port

A visual port belongs to a node.

Conceptually:

VisualPort
 ├── id
 ├── parent_node
 ├── semantic_reference?
 ├── port_type
 ├── directionality
 └── geometry

The implementation may store ports directly inside nodes or use a separate indexed collection.

Either representation is acceptable.

The important invariant is:

Every connection endpoint resolves to a specific port.

9. Visual Connection

A connection should reference ports.

Conceptually:

VisualConnection
 ├── id
 ├── endpoint_a
 ├── endpoint_b
 ├── connection_type
 └── visual_geometry

The semantic meaning of the connection is separate from how it is drawn.

10. Visual Group

A group is a presentation-level container.

Conceptually:

VisualGroup
 ├── id
 ├── label
 ├── members
 ├── geometry
 └── visual_state

A group may optionally reference a canonical subsystem or assembly.

Visual grouping must not automatically create semantic containment.

11. View Model

A view describes a particular visual presentation of the model.

Conceptually:

View
 ├── id
 ├── name
 ├── visible_objects
 ├── layout
 ├── zoom
 ├── pan
 └── presentation_settings

The first prototype may implement only one view.

The architecture should not require one view to be the complete machine representation.

12. Persistent Model vs Runtime UI State

The implementation should distinguish persistent visual data from temporary UI state.

Persistent visual data
nodes
ports
connections
groups
layout
properties
view definitions
Runtime UI state
selected object
hovered object
active drag
connection preview
pointer position
temporary guides
open panels

Runtime UI state should not normally be serialized with the machine representation.

13. Renderer Responsibilities

The renderer should:

draw nodes
draw ports
draw connections
draw groups
draw selection
draw hover state
draw temporary connection previews
draw compatibility feedback
respond to view state

The renderer should not:

create canonical machine semantics
decide whether a connection is valid
modify semantic relationships directly
determine what a component means
own persistent machine data
14. Interaction Layer Responsibilities

The interaction layer should interpret user input.

Examples include:

pointer down
pointer move
pointer up
drag node
drag from port
drop connection
select node
delete object
pan canvas
zoom canvas
edit property

The interaction layer should convert those interactions into explicit model operations.

15. Model Mutation Boundary

A useful conceptual flow is:

User Interaction
      ↓
Interaction Controller
      ↓
Requested Mutation
      ↓
Validation
      ↓
Apply Mutation
      ↓
Visual Model Updated
      ↓
Renderer Refresh

Avoid:

Mouse Event
   ↓
directly mutate random renderer objects

The latter will make undo/redo, validation, persistence, and semantic integration difficult later.

16. Command / Mutation Concept

The prototype should consider representing changes as explicit commands or mutations.

Examples:

CreateNode
DeleteNode
MoveNode
CreateConnection
DeleteConnection
ChangeProperty
CreateGroup
DeleteGroup
MoveIntoGroup
RemoveFromGroup

These need not become a sophisticated command framework immediately.

The important architectural idea is that a user action should correspond to an identifiable model change.

17. Why Explicit Mutations Matter

Explicit mutations eventually make it possible to support:

undo
redo
history
validation
event logging
collaboration
transaction boundaries

They also make debugging easier because a model change can be traced back to an operation.

18. Validation Layer

Validation should be isolated from rendering.

A validation service may answer:

Can these ports connect?
Is this connection allowed?
Is this relationship structurally valid?
Is this property valid?

Conceptually:

Candidate Mutation
      ↓
Validation
      ↓
valid / invalid / warning / unknown

The renderer consumes the result to provide feedback.

19. Compatibility Engine

Port compatibility should be represented as a separate service or module.

Conceptually:

Port A
Port B
  ↓
Compatibility Engine
  ↓
Compatibility Result

Possible results:

compatible
incompatible
conditionally compatible
unknown

The compatibility engine should not depend on rendering.

20. Initial Compatibility Rules

The prototype may begin with simple rules based on:

domain
direction
basic interface type

Examples:

electrical output ↔ compatible electrical input
RS-485 ↔ RS-485
material output ↔ material input

and:

24V power ↔ thermistor input

should produce an incompatible result.

The rules should be easy to expand.

21. Semantic Validation vs UI Validation

These are different.

UI validation

Examples:

pointer released outside canvas
missing selection
invalid drag state
Semantic validation

Examples:

incompatible ports
invalid relationship
forbidden connection
invalid property value

They should not become the same subsystem.

22. Persistence Layer

Persistence should be responsible for saving and loading the visual representation.

Conceptually:

VisualModel
    ↓
Serializer
    ↓
File

and:

File
    ↓
Deserializer
    ↓
VisualModel

The persistence layer should not depend on renderer implementation details.

23. Serialization Format

The exact format is intentionally undecided.

A structured text format such as JSON is a reasonable prototype candidate because it is:

easy to inspect
easy to debug
easy to version-control
widely supported
easy to generate and parse

However, the implementation may choose another suitable format.

The important requirement is that the format represents structured model data rather than storing a screenshot or renderer-specific state blob.

24. Persistence Boundary

The prototype should distinguish:

Machine semantic data
Visual model data
View/session data

even if they initially live in one file.

Do not make a renderer's internal serialization format the permanent Machine Builder file format by accident.

25. Event Flow: Node Creation

Conceptually:

User drags palette item
        ↓
Drop handler
        ↓
CreateNode mutation
        ↓
Create visual node
        ↓
Add default ports
        ↓
Update model
        ↓
Renderer displays node
26. Event Flow: Node Movement

Conceptually:

Pointer down on node
        ↓
Begin drag
        ↓
Pointer movement
        ↓
Update proposed visual position
        ↓
Pointer up
        ↓
Commit MoveNode mutation
        ↓
Renderer redraws

During drag, temporary position may be maintained separately from committed model state if useful.

27. Event Flow: Connection Creation

Conceptually:

Pointer down on Port A
        ↓
Begin connection drag
        ↓
Temporary connection
        ↓
Pointer moves
        ↓
Potential target port identified
        ↓
Compatibility check
        ↓
Feedback displayed
        ↓
Pointer up
        ↓
CreateConnection mutation
        ↓
Validation
        ↓
Commit or reject

The connection preview is transient.

28. Event Flow: Connection Rejection

Conceptually:

Release on invalid target
        ↓
Validation result = incompatible
        ↓
Do not create connection
        ↓
Display brief feedback
        ↓
Return to normal interaction state

The exact user feedback is an implementation decision.

29. Event Flow: Node Deletion

Conceptually:

Select node
        ↓
Delete
        ↓
Identify dependent visual objects
        ↓
Create deletion mutation
        ↓
Remove node
        ↓
Remove/invalidate dependent connections
        ↓
Update model
        ↓
Renderer refresh

The first implementation may use simple cascading deletion.

The architecture should eventually permit confirmation/warning behavior.

30. Event Flow: Save

Conceptually:

User selects Save
        ↓
Collect persistent visual model
        ↓
Serialize
        ↓
Write file

Transient UI state should not normally be included.

31. Event Flow: Load

Conceptually:

User selects file
        ↓
Read file
        ↓
Deserialize
        ↓
Validate basic structure
        ↓
Construct VisualModel
        ↓
Set active view
        ↓
Render

Malformed data should produce an understandable error rather than a crash.

32. Event Flow: Property Editing

Conceptually:

Select node
        ↓
Property panel
        ↓
Change property
        ↓
Proposed value validation
        ↓
ChangeProperty mutation
        ↓
Commit
        ↓
Renderer update

Not all properties need to be editable in the first prototype.

33. Scene Graph vs Semantic Graph

The prototype should conceptually separate:

Scene Graph

from:

Semantic Graph

The scene graph is concerned with:

what is visible
where it is drawn
how it is grouped
how it is styled

The semantic graph is concerned with:

what objects mean
how they relate
what functions/capabilities exist
what connections mean

The two may reference one another.

Neither should replace the other.

34. Scene Graph Requirements

A scene graph should support:

node hierarchy
visual transforms
visibility
z-order where needed
rendering state

It should not require that every scene-graph relationship be a machine relationship.

35. Semantic Graph Requirements

The semantic graph boundary should eventually support:

objects
relationships
properties
classifications
roles
functions
capabilities

The first prototype may expose only a subset.

The visual engine should not prohibit later expansion.

36. Object Identity

There are potentially multiple identities:

canonical object ID
visual node ID
template/type ID

These should not be silently conflated.

Example:

Visual Node ID:
    visual-0012

Canonical Component ID:
    component-0047

Template:
    stepper-motor

This allows multiple visual views of the same canonical object.

37. Template Identity

Templates represent reusable starting definitions for visual objects.

Example:

Stepper Motor Template

Dropping the template should create a new node.

The template itself is not the machine component.

Conceptually:

Template
   ↓
creates
   ↓
Visual Node
38. Component Library Boundary

The first prototype may use a hard-coded component template list.

It should nevertheless conceptually separate:

Template / Library Definition

from:

Actual Visual Node

The eventual Machine Builder will have a much richer hardware library.

39. Future Canonical Hardware Library Integration

Eventually a node template may reference:

Catalog Part Definition

and creation may produce:

Machine Component

The visual prototype does not need to implement this yet.

The architecture should not make it impossible.

40. Firmware Representation Boundary

Firmware-specific data should be treated as implementation metadata or mapping.

For example:

Canonical Motor
       ↓
Firmware Mapping
       ↓
Klipper:
    stepper_x

The visual node should not be fundamentally a "Klipper stepper_x node."

41. Coordinate Systems

The canvas coordinate system is a visual coordinate system.

It must remain separate from machine coordinate systems.

Conceptually:

Canvas Coordinates
    ≠
Machine Coordinates
    ≠
Work Coordinates
    ≠
Tool Coordinates

Future coordinate-aware visualization should use explicit coordinate-frame relationships.

42. Physical Geometry

The first prototype does not need full physical geometry.

Visual node geometry is sufficient.

Later the semantic layer may provide:

physical size
physical position
orientation
mounting relationships
CAD geometry

These should not be inferred from visual layout.

43. Port Geometry

A port should have visual placement relative to its node.

For example:

Node bounds
 ├─ Port at left
 ├─ Port at right
 └─ Port at bottom

Port screen position may be calculated from:

node position
node size
port layout

The semantic port identity remains independent of its screen location.

44. Connection Geometry

Connection geometry may be generated from endpoint positions.

For example:

Port A position
Port B position
       ↓
Routing algorithm
       ↓
Visual path

Changing the routing should not modify connection semantics.

45. Auto-Layout

Automatic layout is optional.

If implemented, it should modify visual positions only.

It should not change:

semantic identity
physical relationships
connection meaning
46. Interaction Coordinate Conversion

The implementation will need to distinguish:

screen coordinates
viewport coordinates
canvas coordinates
node-local coordinates

These should not be confused with machine coordinate frames.

A typical conceptual conversion is:

Pointer Screen Position
        ↓
Viewport Transform
        ↓
Canvas Position
        ↓
Node / Port Hit Testing
47. Hit Testing

The interaction layer should be able to determine whether the pointer is over:

node
port
connection
group
empty canvas

Hit testing belongs to the visual/interaction system.

It should not be implemented as semantic reasoning.

48. Selection Priority

When multiple visual objects overlap, hit testing should have a deterministic priority.

A reasonable conceptual order is:

Port
Connection
Node
Group
Canvas

The exact order can be adjusted based on usability.

49. Connection Selection

A connection should be selectable independently of its endpoints.

This is important for:

deleting
inspecting
editing
diagnostics
future routing
50. Multi-Selection

Multi-selection is desirable but not required for the first demonstration.

If implemented, the interaction layer should treat it as UI state.

It should not create a semantic "group" automatically.

51. Group Collapse

Future groups/subsystems may support:

expanded
collapsed

Collapsing changes presentation only.

Connections to contained objects may later be represented through group boundary interfaces.

The first prototype does not need to solve external-to-collapsed-group connection routing.

52. Connection Rendering Across Groups

The architecture should not assume that every connection must terminate visually inside the currently expanded representation.

Future representations may show:

Subsystem A
     │
     └──── logical connection ──── Subsystem B

while detailed views reveal internal endpoints.

This is one reason semantic and visual relationships must remain separate.

53. Port Compatibility Extensibility

Compatibility rules should be data-driven or modular where practical.

Future rules may include:

domain
direction
voltage
current
protocol
connector family
material
mechanical interface
pressure
temperature

The prototype should implement only the simplest useful subset.

54. Unknown Data

The visual system should permit objects whose semantics are incomplete.

Examples:

unknown port type
unknown compatibility
unknown component classification
unknown part number

Unknown should not be automatically converted to "valid."

55. Diagnostic Overlay Architecture

Future diagnostics should be implemented as overlays.

Conceptually:

Base Visual Model
        +
Runtime Information
        ↓
Diagnostic Overlay
        ↓
Renderer

This prevents runtime state from corrupting configuration data.

56. Signal Activity

Future signal visualization may use:

glow
pulse
animation
color/intensity changes

These should be generated from runtime/diagnostic information.

The connection itself remains a semantic relationship.

57. State Visualization

Future machine/device states may alter node or port presentation.

Examples:

enabled
disabled
moving
heating
fault
warning
homing
probing

Again, these are runtime overlays.

58. Model Events

The prototype may eventually benefit from an event system.

Examples:

NodeCreated
NodeDeleted
NodeMoved
ConnectionCreated
ConnectionDeleted
PropertyChanged
SelectionChanged
ViewChanged

This is optional during the earliest implementation.

The architecture should allow model changes to be observed by the UI.

59. Avoid Renderer-Driven Semantics

The following pattern should be avoided:

Renderer detects line between two nodes
        ↓
assumes machine relationship exists

Instead:

Semantic/Visual Model says relationship exists
        ↓
Renderer draws it

This distinction is essential.

60. Avoid UI-Driven Ontology Decisions

The renderer should not decide that a new semantic concept is required simply because a visual interaction is difficult.

For example:

"we need a node called Flow because drawing filament is difficult"

would be the wrong reasoning.

The semantic and visual problems should be investigated separately.

61. Prototype Dependency Direction

Prefer:

Domain / Semantic
        ↑
Visual Model
        ↑
Application / Interaction
        ↑
Renderer

or an equivalent dependency structure in which more generic/model layers do not depend on the UI framework.

Avoid:

Domain
   ↓
UI framework

as a fundamental dependency.

62. Replaceability

The renderer should be replaceable.

A future renderer could be:

2D canvas
SVG
WebGL
native desktop
web application
3D scene

without requiring the semantic model to change.

The first implementation only needs one renderer.

63. Testing Architecture

Tests should exist at several levels.

Model tests

Test:

node creation
connection creation
deletion
relationships
serialization
Compatibility tests

Test:

valid connection
invalid connection
unknown compatibility
Interaction tests

Test:

drag node
drag port
drop connection
selection
zoom/pan
Rendering tests

Only where practical.

Rendering correctness is less important than model correctness during the first prototype.

64. Deterministic Core

Where practical, model operations and compatibility checks should be deterministic.

For example:

same model
+
same mutation
+
same compatibility rules
=
same result

This will make debugging and automated testing much easier.

65. Logging

Basic development logging is encouraged.

Useful information includes:

mutation requested
validation result
connection created/rejected
object selected
serialization error
load error

The production logging architecture can be designed later.

66. Error Boundaries

An invalid user operation should not corrupt the visual model.

Prefer:

validate
    ↓
commit if valid

rather than:

mutate
    ↓
discover invalid state afterward

Where invalid states must be representable, they should be explicit.

67. Transaction Boundary

A user-visible operation should ideally have a recognizable beginning and end.

Examples:

drag node
create connection
edit property
delete node

This will help later with:

undo
redo
validation
history
68. First Implementation Sequence

A reasonable build sequence is:

1. Basic application shell
2. Canvas
3. Visual node model
4. Node rendering
5. Node movement
6. Selection
7. Port rendering
8. Connection creation
9. Connection rendering
10. Compatibility checking
11. Deletion
12. Grouping
13. Properties
14. Save/load
15. Promega test model
16. CFS stress test

The exact order can change if implementation experience suggests a better path.

69. Recommended Early Milestones
Milestone A — Canvas

Demonstrate:

canvas
pan
zoom
node placement
node movement
selection
Milestone B — Connections

Demonstrate:

ports
connection drag
connection preview
compatibility feedback
connection creation
connection deletion
Milestone C — Persistence

Demonstrate:

save
load
restore layout and connections
Milestone D — Real Machine Test

Demonstrate:

simplified Promega
CoreXY
multiple relationships
Milestone E — Complex Subsystem Test

Demonstrate:

CFS
multiple motors
multiple sensors
material paths
subsystem boundary
70. Promega Test Architecture

The initial semantic test data may be represented approximately as:

Machine
 ├── Controller
 ├── Motor A
 ├── Motor B
 ├── Z Motor
 ├── Driver A
 ├── Driver B
 ├── Z Driver
 ├── IR Probe
 └── Heater/Extruder

Ports should represent relevant interfaces.

Relationships should test:

motor ↔ driver
driver ↔ controller
probe ↔ controller
heater ↔ controller
CoreXY kinematic relationships

This does not need to be a complete Promega machine model.

71. CFS Test Architecture

The CFS stress test should eventually include:

CFS Subsystem
 ├── Source 1
 │   ├── spool
 │   ├── rewind motor
 │   ├── presence sensor
 │   └── feeder motor
 ├── Source 2
 ├── Source 3
 ├── Source 4
 ├── Lower feeder
 ├── Lower sensor
 ├── Buffer
 ├── Buffer switch
 └── CFS controller

The visual model should be able to represent the subsystem without reducing it to a single node.

72. CFS Relationship Tests

The test should verify that the visual architecture can represent:

multiple actuators
multiple sensors
material paths
local control
external communication
subsystem boundaries
many-to-many function/resource relationships

The exact semantic ontology of material systems is still being developed.

73. Do Not Overbuild the CFS Yet

The CFS should be used as a stress test, not as an excuse to implement the entire material-handling ontology.

The first visual prototype only needs enough CFS detail to expose weaknesses in:

nodes
ports
connections
groups
relationships
views
74. Architecture Decision: No Hard-Coded Firmware

There should be no required dependency on:

Klipper
Marlin
RepRapFirmware
FluidNC
GRBLHAL
LinuxCNC

A firmware-specific module may be added later.

The visual builder must function with no firmware information at all.

75. Architecture Decision: No Hard-Coded Machine Type

The canvas should not assume:

3D printer
CNC
laser
robot

as its fundamental type.

A machine-specific template or profile may be added later.

The core visual engine should remain generic.

76. Architecture Decision: No Hard-Coded Axis Model

Do not assume:

X
Y
Z

are the only possible machine motion concepts.

The prototype may display them.

The engine should not depend on them.

Future machines may include:

A
B
C
radial
angular
joint coordinates
custom coordinates
77. Architecture Decision: No Hard-Coded One-to-One Mapping

Never build core structures that require:

Axis → exactly one Motor
Motor → exactly one Axis
Sensor → exactly one Function
Function → exactly one Component
Tool → exactly one Carriage

These assumptions have already been disproven by real machines studied during Machine Builder research.

78. Architecture Decision: Port-Centered Connections

Connection endpoints should resolve to ports.

This is one of the highest-confidence architectural decisions in the prototype.

Prefer:

Node A
  └── Port A
        │
        └── Connection
                │
                └── Port B
                       └── Node B

over:

Node A
   │
Connection
   │
Node B
79. Architecture Decision: Semantic Connections Are Not Drawings

A connection is a model relationship.

Its graphical representation is a view.

Therefore:

Connection
    ≠
Visual Line

A visual line may represent:

wire
cable
logical relationship
material path
mechanical relationship
communication

depending on view and semantic type.

80. Architecture Decision: Visual Layout Is Not Physical Layout

Canvas position must remain separate from machine physical position.

This should be treated as an explicit invariant.

81. Architecture Decision: Unknown Is Valid

The prototype should support incomplete information.

The absence of semantic information should not automatically invalidate an object.

For example:

port_type = unknown

is different from:

port_type = incompatible
82. Architecture Decision: Runtime Is Separate

Configuration:

what the machine is

Runtime:

what the machine is doing now

These should not be merged.

83. Architecture Decision: Prototype Is Disposable in Detail, Not in Structure

The first renderer, styling system, and some model details may be replaced.

The following architectural concepts should survive:

semantic boundary
visual model
ports
connections
typed relationships
separate view state
model mutations
validation boundary
firmware independence
84. Architectural Risk Register

The prototype should actively watch for these risks.

Risk: Visual model becomes canonical model

Response:

Maintain explicit semantic references and separation.

Risk: Every connection becomes a wire

Response:

Use typed connection domains.

Risk: Nodes become the only meaningful objects

Response:

Represent ports and relationships explicitly.

Risk: One-to-one assumptions

Response:

Use flexible relationship structures.

Risk: Ontology changes break UI

Response:

Keep semantic adapter boundary.

Risk: Renderer becomes too powerful

Response:

Keep model mutations outside rendering code.

Risk: Prototype becomes a CAD program

Response:

Keep physical geometry and machine semantics separate.

Risk: Prototype becomes firmware configurator

Response:

Keep firmware mappings outside core visual model.

85. Open Architectural Questions

These remain intentionally unresolved:

Exact implementation technology
Exact renderer
Exact persistence format
Exact canonical ontology interface
Exact Resource model
Exact Flow/Path model
Exact Port subtype hierarchy
Exact connection rule language
Exact multi-view synchronization mechanism
Exact undo/redo implementation

The prototype should gather evidence about these questions rather than prematurely freezing them.

86. Expected Feedback From Implementation

The Coder should report back when implementation reveals:

a semantic distinction that is missing
a relationship that cannot be represented cleanly
a one-to-many or many-to-many case
a visual interaction that requires a new abstraction
a performance issue caused by the model
a persistence problem
a mismatch between visual and canonical identities

These should become architecture/research questions rather than being silently patched inside the UI.

87. Final Architectural Test

The architecture should be considered successful if the Coder can eventually build:

Promega

and then:

CFS subsystem

using the same fundamental visual engine.

If implementing those two systems requires hard-coding:

CoreXY-specific node types
CFS-specific connection classes
firmware-specific ports
printer-only assumptions
one-motor-per-axis structures

then the architecture should be reconsidered.

88. Final Principle

The prototype should establish a visual environment in which:

People manipulate visual representations
        ↓
of structured machine relationships
        ↓
through explicit model operations
        ↓
validated by semantic rules
        ↓
while the canonical ontology remains independent
        ↓
and the renderer remains replaceable.

The prototype is not intended to prove that the final Machine Builder architecture is complete.

It is intended to make the architecture testable.