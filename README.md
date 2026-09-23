# Machine Builder

Machine Builder is a **Machine Development Environment (MDE)** for describing, designing, inspecting, and eventually configuring real machines.

The project is being developed around a central principle:

> **The physical machine is the machine. Firmware is a versioned implementation of that machine, not the machine's identity.**

The canonical machine model is therefore the semantic center of the project.

```text
Physical Machine
        ↓
Canonical Machine Model
        ↓
Firmware Requirements / Mapping
        ↓
Target Firmware + Version
        ↓
Generated Configuration / Representation
```

Reverse interpretation is also intended:

```text
Firmware / Configuration
        ↓
Semantic Interpretation
        ↓
Canonical Machine Model
```

---

# Where to start

Every new Machine Builder chat should read this README first.

The repository is the durable shared memory between chats, but different parts of the repository are authoritative for different subjects.

After reading this file, follow the section for the role of the current chat.

The current repository tree can also be indexed using:

```text
recursive_git_tree.txt
```

This file is a generated path index, not a substitute for reading the actual source files. It is useful for locating files; the actual files remain authoritative for their contents.

---

# Chat roles

## 1. Research / Architecture

The research chat is responsible for:

* ontology
* terminology
* semantic distinctions
* architecture
* standards research
* firmware research
* machine research
* unresolved conceptual questions
* durable architectural decisions

Start with:

```text
machine-builder-research/START_HERE.md
```

The current research checkpoint is:

```text
machine-builder-research/checkpoints/V0.2_RESEARCH_CHECKPOINT.md
```

Important research areas include:

```text
machine-builder-research/PROJECT_CONTEXT.md
machine-builder-research/RESEARCH_ROADMAP.md
machine-builder-research/architecture/
machine-builder-research/ontology/
machine-builder-research/standards/
machine-builder-research/machines/
machine-builder-research/firmware/
machine-builder-research/decisions/
machine-builder-research/questions/
machine-builder-research/checkpoints/
machine-builder-research/handoffs/
```

Research/architecture documents are authoritative for settled semantic and architectural decisions.

---

## 2. Implementation / Coder

The implementation chat is responsible for:

* Python implementation
* software architecture
* data structures
* mutations
* persistence
* UI integration
* automated tests
* executable behavior
* implementation checkpoints

Primary implementation directory:

```text
machine-structure-editor/
```

Important implementation areas include:

```text
machine-structure-editor/src/machine_builder/
machine-structure-editor/tests/
machine-structure-editor/docs/
machine-structure-editor/handoffs/
```

The current implementation state is summarized by:

```text
machine-structure-editor/handoffs/V0.2_VISUAL_EDITOR_IMPLEMENTATION_HANDOFF.md
```

The current detailed repository/file snapshot is:

```text
machine-structure-editor/handoffs/V0.2_VISUAL_EDITOR_REPOSITORY_SNAPSHOT.md
```

Those two handoff files are intended to be committed with the current implementation checkpoint. If they are not yet present in the repository, the local copies are the authoritative working documents until they are pushed.

The implementation chat must not independently redefine settled research/architecture decisions.

---

## 3. Visual Editor / UX

The visual-editor work is responsible for:

* visual interaction
* editor usability
* node presentation
* ports and icons
* zoom
* pan
* semantic zoom
* selection
* routing
* layout
* layers and filters
* visual distinction between viewing and editing
* visual presentation of semantic information

The visual editor lives inside:

```text
machine-structure-editor/src/machine_builder/
```

with presentation-specific graphics code primarily under:

```text
machine-structure-editor/src/machine_builder/graphics/
```

The current visual-editor chat should read, in this order:

```text
README.md
machine-builder-research/START_HERE.md
machine-builder-research/checkpoints/V0.2_RESEARCH_CHECKPOINT.md
machine-builder-research/handoffs/V0.2_IMPLEMENTATION_HANDOFF.md
machine-structure-editor/handoffs/V0.2_VISUAL_EDITOR_IMPLEMENTATION_HANDOFF.md
machine-structure-editor/handoffs/V0.2_VISUAL_EDITOR_REPOSITORY_SNAPSHOT.md
```

Then inspect the current source and tests before proposing changes.

---

# Important architectural rule

No chat should silently redefine the durable architecture because a new idea appears during implementation.

The working relationship is:

```text
Research / Architecture
        ↕
Implementation
        ↕
Visual Editor
```

Research may identify or propose semantic/architectural changes.

Implementation may expose concrete problems or ambiguities.

Visual-editor work may expose usability or representation problems.

Those findings should be brought back to the appropriate role and resolved before changing durable architecture.

Promising ideas may remain candidates until research and implementation agree that they belong in the durable baseline.

---

# Canonical machine model

The canonical machine model is the authoritative semantic representation.

The visual editor is a bidirectional authoring and inspection environment over that model.

```text
          Canonical Machine Model
                    ↕
          Semantic / Model Boundary
                    ↕
               Visual Editor
```

The visual model is **not** a second machine model.

Visual state may include:

* canvas position
* size
* routing geometry
* selection
* zoom
* pan
* collapsed/expanded presentation
* grouping
* view/filter state
* other presentation-only state

Canonical semantic information includes things such as:

* Machine
* Machine Component
* Hardware Definition
* Ports
* Connectors / pins / terminals
* Connections
* Functions
* Capabilities
* Controllers
* Controller Resources
* Controller Resource Assignments
* properties
* calibration
* provenance
* semantic relationships

---

# Current implementation checkpoint

The Machine Structure Editor has established a substantial V0.2 semantic-authoring and visual-editor foundation.

Latest verified automated test checkpoint:

```text
582 passed
```

Normal verification command:

```powershell
python -m pytest
```

The exact runtime duration is not itself significant; a green full-suite result is the important checkpoint.

Current implementation includes, among other foundations:

* Machine
* Machine Component
* Hardware Definition
* Semantic Port
* Function
* Capability
* Controller
* Controller Resource
* Controller Resource Assignment
* Provenance
* semantic Connections
* semantic Relationships
* visual/canonical model boundary
* semantic projection
* component authoring
* port authoring
* controller authoring
* controller-resource authoring
* controller-resource assignment validation
* undo/redo
* mutation rollback
* document persistence
* document lifecycle
* modular visual-editor canvas
* node interaction
* port interaction
* connection authoring
* semantic component editing
* semantic port editing

The current implementation should be treated as a V0.2 development checkpoint, not as a statement that every planned V0.2 user-facing feature is complete.

---

# Controller and control-board direction

Controllers are canonical machine objects.

Reusable controller/control-board hardware is represented separately from the controller instance installed in a particular machine.

The intended relationship is:

```text
Real documented control board
        ↓
Hardware Definition
        ↓
Machine Controller instance
        ↓
Controller Resources
        ↓
Controller Resource Assignments
```

For the initial hardware catalog, controller/control-board definitions should preferentially represent **real, currently available boards for which reliable specifications can be obtained**.

The initial project is not centered on users designing or fabricating their own printer controller PCBs.

Useful catalog entries therefore include actual documented boards with available specifications such as:

* manufacturer
* model
* controller type
* processor
* firmware support information
* I/O/resource information
* connector information
* electrical limits where documented
* other relevant manufacturer specifications
* provenance/source information

This does not eliminate support for unusual or custom controllers later. It simply establishes the practical initial catalog direction.

The distinction remains:

```text
Hardware Definition
    = what the reusable hardware is

Machine Controller
    = how one particular machine uses/identifies its controller
```

---

# Machine Component vs Hardware Definition

These are intentionally separate.

```text
Machine Component
    references
        ↓
Hardware Definition
```

A Machine Component is the machine-specific occurrence.

A Hardware Definition describes known hardware characteristics.

The same Hardware Definition may be referenced by multiple Machine Components.

Ports instantiated onto separate Machine Components must have separate canonical identities.

Example:

```text
Hardware Definition
    generic-4010-fan-24v

Machine Component A
    component-fan-a
    ├── component-fan-a-power
    └── component-fan-a-ground

Machine Component B
    component-fan-b
    ├── component-fan-b-power
    └── component-fan-b-ground
```

---

# Controller resources and assignments

A controller exposes resources that a machine may use or assign to semantic machine objects.

Conceptually:

```text
Machine
 ├─ Controller
 │    └─ Controller Resource
 │
 └─ source object
          ↓
     Controller Resource Assignment
          ↓
     Controller Resource
```

A Controller Resource is not automatically a physical connection endpoint.

Controller-resource assignments are semantic mappings and must remain distinct from visual/physical connection geometry.

In particular:

```text
VisualConnection
    = visual representation of machine connectivity

ControllerResourceAssignment
    = semantic mapping to a controller implementation resource
```

The current implementation enforces machine-boundary validation for controller-resource assignments.

---

# Current canvas architecture

The original canvas implementation was deliberately refactored into focused modules.

Current structure:

```text
canvas.py
    coordinator

canvas_ui.py
    window/action construction
    semantic edit entry points

canvas_palette.py
    palette
    visual template creation

canvas_interaction.py
    node movement
    selection
    deletion
    connection dragging
    previews
    compatibility feedback

canvas_scene.py
    VisualModel → QGraphicsScene synchronization
```

The canvas coordinator should remain small.

`canvas_interaction.py` is allowed to be larger than the other canvas modules because interaction behavior is a cohesive responsibility.

Do not recreate the former monolithic canvas unless there is compelling architectural evidence.

---

# Current graphics interaction rules

Visual ports have an intentional interaction distinction:

```text
single click / drag
    → connection interaction

double click
    → semantic port editing
```

This separation prevents semantic authoring from conflicting with connection authoring.

Similarly, visual representation of controller resources should not automatically reuse ports unless research/implementation establish that a resource is actually a connection endpoint in that context.

---

# Semantic authoring pattern

The project now uses focused layers where useful:

```text
semantic_*_queries.py
semantic_*_mutations.py
*_details.py
*_properties.py
tests/*
```

This pattern currently exists across component, port, controller, and controller-resource authoring.

The pattern should be reused when it fits, but the project should not create layers merely for symmetry.

---

# Persistence and documents

The editor state contains both canonical and visual state.

`ModelStore` owns:

* current editor state
* atomic edit commits
* undo
* redo
* save
* load
* new document
* modified state
* file path
* listeners

`DocumentController` provides application-level document lifecycle.

The persistence layer uses the editor format:

```text
machine-builder-editor
```

Format version:

```text
1
```

The canonical semantic model and visual model are persisted as part of the complete editor state.

---

# Visual model boundary

The visual model includes generic structures such as:

* `VisualNode`
* `VisualPort`
* `VisualConnection`
* `VisualGroup`
* `VisualView`
* `VisualModel`

`VisualNode` and `VisualPort` can carry a `semantic_reference` so that a visual object can refer to canonical identity without becoming a second semantic object.

This mechanism is intended to be reused rather than replaced with separate visual-only semantic hierarchies.

For example:

```text
Canonical Controller
        ↓
semantic_reference = controller.id
        ↓
VisualNode
        ↓
NodeGraphicsItem
```

The current visual-editor work is expected to build on this boundary.

---

# Hardware catalog direction

The future catalog architecture is intended to support real documented hardware:

```text
Real hardware / documentation
        ↓
Catalog / importer / adapter
        ↓
Hardware Definition
        ↓
Machine Component or Controller instance
        ↓
Canonical Machine
```

Online catalog integration is not required before the current V0.2 visual/editor foundation is stable.

Do not prematurely add a network service or vendor-specific catalog integration merely because the architecture can eventually support it.

---

# Current file organization

The repository contains a larger tree than is useful to reproduce in this README.

For the current detailed file map, use:

```text
machine-structure-editor/handoffs/V0.2_VISUAL_EDITOR_REPOSITORY_SNAPSHOT.md
```

For a generated repository-wide path index, use:

```text
recursive_git_tree.txt
```

The primary implementation source is:

```text
machine-structure-editor/src/machine_builder/
```

Tests are under:

```text
machine-structure-editor/tests/
```

Research and architecture records are under:

```text
machine-builder-research/
```

---

# Important implementation files

Some of the most important current modules are:

```text
machine-structure-editor/src/machine_builder/semantic_model.py
machine-structure-editor/src/machine_builder/visual_model.py
machine-structure-editor/src/machine_builder/editor_state.py
machine-structure-editor/src/machine_builder/store.py
machine-structure-editor/src/machine_builder/persistence.py
machine-structure-editor/src/machine_builder/document_controller.py

machine-structure-editor/src/machine_builder/canvas.py
machine-structure-editor/src/machine_builder/canvas_ui.py
machine-structure-editor/src/machine_builder/canvas_palette.py
machine-structure-editor/src/machine_builder/canvas_interaction.py
machine-structure-editor/src/machine_builder/canvas_scene.py

machine-structure-editor/src/machine_builder/controller.py
machine-structure-editor/src/machine_builder/controller_queries.py
machine-structure-editor/src/machine_builder/controller_mutations.py
machine-structure-editor/src/machine_builder/controller_details.py

machine-structure-editor/src/machine_builder/controller_resource.py
machine-structure-editor/src/machine_builder/controller_resource_queries.py
machine-structure-editor/src/machine_builder/controller_resource_mutations.py
machine-structure-editor/src/machine_builder/controller_resource_details.py
machine-structure-editor/src/machine_builder/controller_resource_properties.py

machine-structure-editor/src/machine_builder/controller_resource_assignment.py
machine-structure-editor/src/machine_builder/controller_resource_assignment_queries.py
machine-structure-editor/src/machine_builder/controller_resource_assignment_mutations.py
machine-structure-editor/src/machine_builder/controller_resource_assignment_validation.py
machine-structure-editor/src/machine_builder/controller_resource_assignment_store.py
machine-structure-editor/src/machine_builder/controller_assignment_authoring.py

machine-structure-editor/src/machine_builder/semantic_component_queries.py
machine-structure-editor/src/machine_builder/semantic_component_mutations.py
machine-structure-editor/src/machine_builder/component_details.py
machine-structure-editor/src/machine_builder/component_properties.py

machine-structure-editor/src/machine_builder/semantic_port_queries.py
machine-structure-editor/src/machine_builder/semantic_port_mutations.py
machine-structure-editor/src/machine_builder/port_details.py
machine-structure-editor/src/machine_builder/port_properties.py

machine-structure-editor/src/machine_builder/graphics/
```

This is intentionally a highlighted map, not a replacement for the recursive tree or repository snapshot.

---

# Test organization

Tests are organized around architectural boundaries and features.

Examples include:

```text
canvas / graphics
    test_canvas_interaction.py
    test_canvas_scene.py
    test_canvas_ui.py
    test_port_graphics_editing.py

semantic model
    test_semantic_model.py
    test_semantic_capability.py
    test_semantic_model_controller_resource.py
    test_semantic_model_controller_resource_assignment.py

component authoring
    test_semantic_component_queries.py
    test_semantic_component_store_integration.py
    test_component_details.py
    test_component_properties.py

port authoring
    test_semantic_port_queries.py
    test_semantic_port_store_integration.py
    test_port_details.py
    test_port_properties.py

controller/resource authoring
    test_controller_model.py
    test_controller_queries.py
    test_controller_mutations.py
    test_controller_details.py
    test_controller_resource_queries.py
    test_controller_resource_mutations.py
    test_controller_resource_properties.py
    test_controller_resource_store.py

assignment architecture
    test_controller_resource_assignment_queries.py
    test_controller_resource_assignment_mutations.py
    test_controller_resource_assignment_validation.py
    test_controller_resource_assignment_store.py

document lifecycle
    test_store.py
    test_store_document_state.py
    test_store_new_document.py
    test_store_persistence.py
    test_document_controller.py
```

The complete suite currently passes 582 tests.

---

# Repository conventions

Prefer:

* small modular files
* clear boundaries between concerns
* complete-file replacements during implementation work when practical
* automated tests for every meaningful change
* clean Git checkpoints
* durable documentation for architectural decisions
* inspecting the actual current source before modifying an existing substantial file

Avoid:

* line-by-line file surgery when a complete replacement is practical
* silently changing the architecture during implementation
* giant monolithic modules when focused modules are clearer
* making visual state the semantic authority
* inventing unknown machine information
* reconstructing large files from memory
* treating historical experiments as current architecture
* committing every tiny green test

---

# Large-file safety rule

Existing large files must not be reconstructed from memory.

Before replacing a substantial existing file:

1. inspect the exact current source
2. preserve unrelated behavior
3. make the smallest cohesive change
4. run the full test suite
5. commit only at a meaningful checkpoint

The repository is the source of truth.

---

# Current visual-editor priority

The next implementation problem is expected to be visual representation of canonical controllers and, eventually, controller resources and assignments.

The first question is:

> How should canonical controller resources and controller-resource assignments become visible and editable in the visual editor without creating a second semantic model?

The likely first step is deliberately conservative:

```text
Canonical Controller
        ↓
controller ↔ visual query/projection
        ↓
VisualNode
        ↓
NodeGraphicsItem
```

A controller may eventually be presented as a visual node that references its canonical controller identity.

Controller resources should not automatically become `VisualPort` objects because `VisualPort` already has a specific connection-authoring meaning.

Controller-resource assignments should not automatically be represented as `VisualConnection` objects because assignments and physical/logical connectivity are different semantic concepts.

Before implementing a larger controller/resource visual system, inspect the existing projection, query, details-dialog, deletion/cleanup, persistence, and visual-reference patterns.

---

# Current V0.2 scope reminder

The current implementation establishes the foundation for a much larger V0.2 feature set.

Not all planned V0.2 user-facing behavior is complete.

Future areas include:

* richer controller/resource visualization
* semantic zoom
* layers and filters
* richer connection routing
* harness/slack/routing representation
* liquid-cooling domain modeling and visualization
* firmware mapping and generation
* firmware/configuration reverse interpretation
* real hardware catalog integration
* beginner/medium/expert presentation modes
* richer live machine/firmware integration

These should be added incrementally from the established semantic foundation.

---

# Historical material

Older builder experiments and historical documentation may remain in the repository.

Do not treat an older implementation as the current architecture merely because it contains a feature that is not yet present in `machine-structure-editor`.

The current implementation, research checkpoint, current handoffs, tests, and current source files are the authoritative working set.

---

# When sources disagree

Use this priority:

```text
Settled semantic / architectural question
    → research / architecture documents

Implementation behavior
    → current source + current tests

Visual/UI behavior
    → current implementation + visual requirements/research

Current file locations
    → repository tree / recursive_git_tree.txt

Historical discussion
    → historical documents only
```

If an idea conflicts with the durable architecture, record it as a candidate and resolve the architectural question before silently changing the baseline.

---

# Repository checkpoint practice

At a meaningful implementation checkpoint:

1. run the full test suite
2. inspect the actual changed files
3. update the relevant handoff/snapshot documentation
4. make one cohesive Git commit
5. push the checkpoint
6. use the repository as the starting point for the next chat

The repository is the durable shared memory between chats.




Note from the human:
as of 9/20/26 9:45pm, the maximum length of the chat has been reached with no warning before i was able to push to github.  Here is the last few bits of the conversation that i could copy...

I kept going, and I found one important thing before we make another change:


After that, the important live test is the controller-body case. Put the controller back where you previously got the wire to pass through it and see whether the route now recognizes the controller as an obstacle and goes around it.

686 passed in 2.51s

I can't get the wire to go through another box any more.

Excellent. That confirms the iterative relevance fix is doing what we wanted. The router is no longer allowing a component to disappear from consideration just because it wasn't near the initial probe.

Current checkpoint:

686 passed

And we now have:

Routing diagnostics working.
Debug repaint/vapor-trail problem fixed.
Narrow-corridor protection added.
Relevance-chain protection added.
Candidate-route relevance expanded iteratively.
No more reproducible wires passing through component bodies.

The remaining question is the elbow stability behavior. Now that collision avoidance is behaving properly, I'd test that with Routing Debug Mode OFF, because our stability code intentionally bypasses route-history reuse while diagnostics are enabled.

Move one of the components around where you've previously seen the elbow change. We don't need to reproduce the exact five positions; we're just checking whether an otherwise-valid elbow now stays put instead of hopping between equivalent positions.

If that looks stable, we're probably at another good checkpoint.

this is the closest i can get to a jitter. here are the 4 positions first.

Selection
----------
label: Temperature Sensor
id: node-1
type: temperature_sensor
semantic reference: component-node-1

Position
--------
x: -261.000
y: -180.000
width: 180.000
height: 100.000
rotation: 0.000

Bounds
------
left: -261.000
top: -180.000
right: -81.000
bottom: -80.000

Ports
-----
Reference / Ground [node-1-ground]
  side: left
  order: 0
  type: electrical
  direction: bidirectional
  semantic reference: none
  connections: none
Temperature Output [node-1-temperature]
  side: right
  order: 0
  type: signal
  direction: output
  semantic reference: none
  connections:
    connection-1 → Temperature Controller / Temperature Input

Selection
----------
label: Temperature Controller
id: node-2
type: temperature_controller
semantic reference: component-node-2

Position
--------
x: -254.107
y: 159.786
width: 180.000
height: 100.000
rotation: 0.000

Bounds
------
left: -254.107
top: 159.786
right: -74.107
bottom: 259.786

Ports
-----
Power Input [node-2-power]
  side: left
  order: 0
  type: electrical
  direction: input
  semantic reference: none
  connections: none
Temperature Input [node-2-temperature]
  side: right
  order: 0
  type: signal
  direction: input
  semantic reference: none
  connections:
    connection-1 → Temperature Sensor / Temperature Output

Selection
----------
label: Component
id: node-4
type: component
semantic reference: component-node-4

Position
--------
x: -33.000
y: 26.000
width: 180.000
height: 100.000
rotation: 0.000

Bounds
------
left: -33.000
top: 26.000
right: 147.000
bottom: 126.000

Ports
-----
Interface [node-4-port]
  side: right
  order: 0
  type: unknown
  direction: unknown
  semantic reference: none
  connections: none

Selection
----------
label: Component
id: node-3
type: component
semantic reference: component-node-3

Position
--------
x: -26.102
y: 1.611
width: 180.000
height: 100.000
rotation: 0.000

Bounds
------
left: -26.102
top: 1.611
right: 153.898
bottom: 101.611

Ports
-----
Interface [node-3-port]
  side: right
  order: 0
  type: unknown
  direction: unknown
  semantic reference: none
  connections: none

Got it. I’ll treat this as position 1 of 4 and hold off on analyzing the routing until you send the other three positions and what the wire is doing in each.


right now, the wire goes up from the controller stub, then left to the edge of the lower component, then up above the boundary layer of the upper component, then right past the sensor stub, then up to the sensor stub, then left into the sensor stub.

2nd location. just jumps up to the lower sensor boundary layer before turning.
Selection
----------
label: Component
id: node-3
type: component
semantic reference: component-node-3

Position
--------
x: -25.613
y: 1.285
width: 180.000
height: 100.000
rotation: 0.000

Bounds
------
left: -25.613
top: 1.285
right: 154.387
bottom: 101.285

Ports
-----
Interface [node-3-port]
  side: right
  order: 0
  type: unknown
  direction: unknown
  semantic reference: none
  connections: none

after moving the upper component slightly, the wire jumps to the upper component boundary layer.

Selection
----------
label: Component
id: node-3
type: component
semantic reference: component-node-3

Position
--------
x: -24.308
y: 2.590
width: 180.000
height: 100.000
rotation: 0.000

Bounds
------
left: -24.308
top: 2.590
right: 155.692
bottom: 102.590

Ports
-----
Interface [node-3-port]
  side: right
  order: 0
  type: unknown
  direction: unknown
  semantic reference: none
  connections: none

Yep, I can see the pattern starting to emerge, but I don't want to diagnose it from only three states.

So far we have:

Position 1
The route takes the long path around the lower component, then above the upper component, then to the sensor.

Position 2
A tiny movement changes the elbow to the lower component's clearance boundary.

Position 3
Another tiny movement changes it again to the upper component's clearance boundary.

The especially interesting part is that these are very small movements:

position 1 → 2:
x -26.102 → -25.613
y   1.611 →   1.285

position 2 → 3:
x -25.613 → -24.308
y   1.285 →  2.590

That is exactly the sort of behavior our route-stability logic was supposed to suppress when the previous route remains valid and approximately equal in cost.

Send me the fourth position/description. Then I'll compare all four against the stability logic rather than guessing from the visual behavior.

i don't seem to be able to recreate a 4th position right now

That's okay. We don't need a fourth position anymore. The three positions are enough to investigate this because the interesting behavior is already visible: tiny movement of node-3 is changing which clearance boundary the route uses.

Rather than making you hunt for a fourth position, let's test those three exact positions against the current router and, crucially, check whether the previous route is still considered valid when the component moves.
Run this read-only test:

@'
from PySide6.QtCore import QPointF, QRectF

from machine_builder.graphics.connection_routing import (
    ConnectionRoutingEngine,
)

# Fixed endpoint ports from the three captured states.
sensor_port = QPointF(-81.0, -130.0)
controller_port = QPointF(-74.107, 209.786)

sensor_stub = ConnectionRoutingEngine.build_endpoint_stub(
    sensor_port,
    "right",
)[0]

controller_stub = ConnectionRoutingEngine.build_endpoint_stub(
    controller_port,
    "right",
)[0]

cases = [
    ("1", -26.102, 1.611),
    ("2", -25.613, 1.285),
    ("3", -24.308, 2.590),
]

lower = QRectF(
    -33.0,
    26.0,
    180.0,
    100.0,
).adjusted(
    -ConnectionRoutingEngine.ROUTING_MARGIN,
    -ConnectionRoutingEngine.ROUTING_MARGIN,
    ConnectionRoutingEngine.ROUTING_MARGIN,
    ConnectionRoutingEngine.ROUTING_MARGIN,
)

previous = None

for label, x, y in cases:
    upper = QRectF(
        x,
        y,
        180.0,
        100.0,
    ).adjusted(
        -ConnectionRoutingEngine.ROUTING_MARGIN,
        -ConnectionRoutingEngine.ROUTING_MARGIN,
        ConnectionRoutingEngine.ROUTING_MARGIN,
        ConnectionRoutingEngine.ROUTING_MARGIN,
    )

    obstacles = [lower, upper]

    route = ConnectionRoutingEngine.build_route(
        start=sensor_stub,
        end=controller_stub,
        start_direction="right",
        end_direction="right",
        obstacles=obstacles,
    )

    print()
    print(f"=== POSITION {label} ===")
    print("upper:", upper)

    if route is None:
        print("RAW ROUTE: NONE")
        previous = None
        continue

    length = 0.0

    for i in range(len(route) - 1):
        length += (
            abs(route[i + 1].x() - route[i].x())
            + abs(route[i + 1].y() - route[i].y())
        )

    bends = max(0, len(route) - 2)
    cost = (
        length
        + bends * ConnectionRoutingEngine.BEND_PENALTY
    )

    print("raw length:", round(length, 3))
    print("raw bends:", bends)
    print("raw cost:", round(cost, 3))
    print("raw route:")

    for point in route:
        print(
            "  ",
            round(point.x(), 3),
            round(point.y(), 3),
        )

    if previous is not None:
        still_clear = ConnectionRoutingEngine.route_is_clear(
            previous,
            obstacles,
        )

        print("previous route still clear:", still_clear)

    previous = route
'@ | python

This is the key question now:

When the elbow jumps, is the previous route actually becoming invalid, or is the stability mechanism failing to preserve a still-valid equal-cost route?

Those are two very different problems, and this test should tell us which one we're dealing with.



=== POSITION 1 ===
upper: PySide6.QtCore.QRectF(-42.102000, -14.389000, 212.000000, 132.000000)
raw length: 376.465
raw bends: 5
raw cost: 776.465
raw route:
   -41.0 -130.0
   -34.107 -130.0
   -34.107 -14.389
   -49.0 -14.389
   -49.0 174.0
   -34.107 174.0
   -34.107 209.786

=== POSITION 2 ===
upper: PySide6.QtCore.QRectF(-41.613000, -14.715000, 212.000000, 132.000000)
raw length: 376.465
raw bends: 5
raw cost: 776.465
raw route:
   -41.0 -130.0
   -34.107 -130.0
   -34.107 -22.0
   -49.0 -22.0
   -49.0 174.0
   -34.107 174.0
   -34.107 209.786
previous route still clear: False

=== POSITION 3 ===
upper: PySide6.QtCore.QRectF(-40.308000, -13.410000, 212.000000, 132.000000)
raw length: 364.063
raw bends: 5
raw cost: 764.063
raw route:
   -41.0 -130.0
   -40.308 -130.0
   -40.308 10.0
   -49.0 10.0
   -49.0 174.0
   -34.107 174.0
   -34.107 209.786
previous route still clear: True
(.venv) PS C:\Users\Peter\Documents\GitHub\Machine-Builder\machine-structure-editor> 

That result finally gives us a very clear answer.

Position 1 → Position 2

The old route becomes invalid:

previous route still clear: False

So the router must change routes. That's correct behavior.

Position 2 → Position 3

This is the interesting one:

previous route still clear: True

but the newly calculated route is:

old cost: 776.465
new cost: 764.063
difference: 12.402

Both routes have 5 bends, so the entire improvement is geometric distance.

Our stability rule currently says:

keep old route when:
old cost <= new cost + 4

But here the new route is 12.4 cost units better, so the code deliberately switches.

And that's exactly why you're seeing the elbow jump.

So the stability fix is working — but our threshold is probably too small

We successfully eliminated arbitrary equal-cost switching. Now we've uncovered a subtler UX issue:

A very small improvement in route cost can produce a large visible relocation of an elbow.

The path moves from approximately:

(-49, -22)

to:

(-49, 10)

That's a 32-pixel vertical jump, even though the route only became 12.4 cost units better.

I would not call the routing algorithm broken anymore. The question is now what visual stability policy we want.

My instinct is to increase the route-stability tolerance from:

ROUTE_STABILITY_COST_TOLERANCE = 4.0

to something closer to the existing 24 px hysteresis scale.

But I don't want to blindly choose 24 just because that number already exists elsewhere. The next sensible step is to test the same three positions with a few candidate tolerances and see what would happen.

We can do that entirely from the console before touching the code.

ok. go for it

That gives us a pretty clean result.

For the captured position 2 → position 3 transition:

Stability tolerance	Result
4 px	switches
8 px	switches
10 px	switches
12 px	switches
12.5 px	holds previous route
16 px	holds
20 px	holds
24 px	holds

The candidate route is only 12.402 px cheaper, while moving the visible elbow by roughly 32 px. So the current 4 px tolerance is definitely too small for the visual behavior we're trying to achieve.

The important part is that position 1 → 2 still must change because the previous route is no longer clear. The stability tolerance does not interfere with that safety condition.

What I'd use

I recommend changing:

ROUTE_STABILITY_COST_TOLERANCE = 4.0

to:

ROUTE_STABILITY_COST_TOLERANCE = 16.0

That gives us some room above the 12.402 px case without going all the way to the existing 24 px endpoint hysteresis.

I would not use 24 yet. That's enough of a preference that it could start making legitimate route improvements feel sluggish.

No code has been changed from this experiment.

Today 3:34 PM
so do i do anything now or do you keep testing different positions?

Don’t change anything yet.

For the three positions we already captured, the evidence is clear: 4 px is too small, and 16 px looks like a sensible candidate. But I would rather test a few more different movements before locking that value in.

The important distinction is that I can analyze the captured geometry here, but I can’t generate new GUI positions from your running editor. So the next useful step is for you to move the controller through a few nearby positions and send me the debug geometry/cost output when you see the route change.

Leave the code exactly as it is for now.

ok. keep it going

I kept going, and I found one important thing before we make another change:

The GitHub WIP branch I can access does not contain the newer route-stability code yet. Its connection.py still goes directly from build_route() to drawing the result, while the endpoint escape hysteresis is present at 24 px.

The routing grid itself is deterministic: candidate coordinates are built from obstacle edges, and the horizontal/vertical adjacency lists are sorted before pathfinding. So this is not looking like random router behavior.

So I don't want you changing or pushing anything yet. Our local 685-test stability patch is ahead of what's on GitHub, and I can't reliably generate new-position results against that exact unpushed state from here.

The next useful experiment is therefore still with the three-position sequence you already have, plus a few more nearby movements in the running editor. Keep Routing Debug Mode OFF while doing this, since the stability logic intentionally bypasses history when diagnostics are enabled.

You haven't broken anything or reached a dead end—we've narrowed this down to tuning the route-hold behavior rather than rewriting the router.

ok. keep it going and let me know when to merge the branch or whatever

Yep. I’m continuing with the code-side analysis, and you do not merge anything yet.

I checked the current wip-routing-diagnostics branch again. The router is deterministic: its candidate points are sorted, and Dijkstra uses an explicit cost consisting of distance plus bend and endpoint-direction penalties. The existing endpoint escape hysteresis is also already 24 px.

The one thing that is not yet on GitHub is our newer main-route stability layer; the remote connection.py still sends the freshly calculated route directly to the graphics path.

So our order is:

1. Finish validating the stability behavior.
2. Choose the tolerance.
3. Add/finish regression tests for the actual jitter case.
4. Run the full suite.
5. Commit/push the completed WIP checkpoint.
6. Then I’ll tell you “this is ready to merge.”

Until I say that, stay on wip-routing-diagnostics and don't merge it into main.

One useful thing I confirmed from the existing tests is that the project already treats routing persistence/hysteresis as presentation/runtime behavior rather than canonical machine data, which is exactly where this stability fix belongs.

So we're still on the right track; nothing for you to change right now.

ok. what's next?

Next is one targeted GUI test pass, not a code change.

We have already established that:

Position 1 → 2: the old route becomes invalid, so changing routes is required.
Position 2 → 3: the old route is still valid, but the router finds a route only 12.402 cost units cheaper, causing the large elbow jump.
That tells us the stability mechanism works, but we don't yet know whether 16 px is the right threshold across other geometries.

So, on your current WIP branch, leave the code alone and do this:

Turn Routing Debug Mode OFF.
Put the controller/sensor in the geometry where you were seeing the elbow jump.
Move the controller in small increments around that area.
Watch for three kinds of behavior:
route stays put while the box moves slightly;
route moves smoothly when it actually needs to;
route changes abruptly even though the previous route is still visibly valid.

We only need a handful of distinct examples. Don't try to reproduce an exact sequence unless it happens naturally.

Once we've got those cases, I'll decide whether the final rule should simply be 16.0, or whether the stability logic needs a slightly better criterion than raw route-cost tolerance.

And still don't merge anything. The next checkpoint will be: code finalized → full pytest run → commit/push → then I'll tell you it's ready to merge.

You've reached the maximum length for this conversation, but you can keep talking by starting a new chat.

Start new chat



Here's a message from the last chat on updating the readme file. it said to put this near the implementatino/current status section but i didn't look for it and just pasted it here instead:

## Current Routing Diagnostics Work

The visual editor currently has a temporary **Routing Debug Mode** used to inspect connection-routing behavior during development.

The diagnostic view can show:

* physical component bounds
* routing-clearance envelopes
* fixed endpoint stubs
* endpoint escape geometry
* main routed paths
* unroutable endpoints
* the last canvas click

Routing Debug Mode is intentionally diagnostic/presentation-only. Routing geometry is not part of the canonical machine semantics.

Recent routing work has addressed several correctness problems:

* incomplete obstacle relevance
* chains of nearby obstacles being omitted from local routing
* routes crossing component/controller bodies
* pathological subpixel-width obstacle corridors
* stale viewport repaint artifacts during routing diagnostics

The routing system is currently deterministic and uses orthogonal pathfinding with distance, bend, and endpoint-direction costs.

### Current routing-stability work

A visual route-stability layer is being evaluated to prevent an already-valid wire from jumping to a different, nearly equal-cost route when a component moves slightly.

The stability mechanism:

* preserves the previous route when it remains valid
* allows a materially better route to replace it
* never allows stability to override obstacle collision safety
* is bypassed in Routing Debug Mode so raw router behavior remains inspectable

The current working branch for this investigation is:

```text
wip-routing-diagnostics
```

The stability threshold is still under evaluation and should not be treated as finalized until additional movement cases have been tested.

The current implementation checkpoint should be verified with:

```powershell
python -m pytest
```

before further routing changes are made.

Implementation Chat Workflow

For implementation/coder chats, read CODER_CHAT_WORKFLOW.md.

The current routing investigation is tracked in:
machine-structure-editor/handoffs/ROUTING_STABILITY_INVESTIGATION_HANDOFF_4.3.md
