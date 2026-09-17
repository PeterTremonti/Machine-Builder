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
