# Machine Structure Editor — Implementation Roadmap

## Purpose

This roadmap describes the implementation path for the Machine Structure Editor portion of Machine Builder.

It is an implementation roadmap, not the canonical machine ontology.

The roadmap is expected to change as the software is tested and architectural decisions are made. Significant changes should be documented in the implementation plan for the affected version.

---

# Version Strategy

Each implementation version has two related records:

1. **Implementation Roadmap**

   * The current overall direction.
   * High-level milestones and planned architecture.

2. **Version Implementation Plan**

   * Initial plan for the version.
   * Decisions and changes made during implementation.
   * Final implemented state.
   * Items deliberately carried into the next version.

The plan for a version may change during implementation.

The final state of a completed version is considered the authoritative record of what was actually implemented.

---

# V0.1 — Visual Structure Editor Foundation

## Goal

Create a usable visual machine-structure editor that establishes the basic interaction, visual-model, mutation, compatibility, and undo/redo foundations without attempting to implement the complete machine ontology.

## V0.1 Functional Scope

### Canvas

* Pan the workspace.
* Zoom the workspace.
* Frame all objects.
* Place visual components on the canvas.
* Move individual components.
* Select multiple components.
* Move multiple selected components as one user action.
* Delete selected components.
* Undo and redo editing actions.

### Component Palette

* Display prototype component types.
* Add components to the canvas.
* Support palette drag-and-drop.
* Place newly created components near the current editing context.
* Keep palette implementation separate from the main editor.

### Visual Nodes

* Display component boxes.
* Display component names.
* Display ports attached to their owning component.
* Keep port presentation independent from canonical machine semantics.
* Allow future component-specific visual sizing and presentation.

### Ports

* Represent ports as explicit visual objects.
* Display persistent port labels.
* Display port type and direction as part of the visual model.
* Provide hover feedback.
* Provide connection-state feedback.
* Use both color and non-color symbols for compatibility feedback.

Prototype feedback states:

* Neutral
* Hover
* Connection source
* Compatible
* Unknown / conditional
* Incompatible

Non-color indicators:

* `✓` compatible
* `?` unknown or conditional
* `×` incompatible

### Connections

* Connect specific ports rather than merely connecting nodes.
* Display connection preview while dragging.
* Evaluate provisional compatibility.
* Commit compatible connections.
* Reject incompatible and unresolved connections.
* Keep committed connections attached to ports when nodes move.
* Select an existing connection by clicking its line.
* Delete a selected connection.
* Undo connection creation and deletion.
* Redo connection creation and deletion.

### Compatibility

V0.1 uses a deliberately small provisional compatibility system.

It must distinguish at least:

* compatible
* incompatible
* unknown
* conditional

Unknown information must not silently become a confirmed connection.

The compatibility engine remains separate from the renderer.

### Visual Model

The visual model remains separate from:

* Qt graphics objects
* canonical machine semantics
* compatibility logic
* mutation history

The visual model contains the presentation relationships required by the editor, including:

* nodes
* ports
* connections
* groups/views as future-capable structures

### Mutations and Editing

User-visible changes should be represented by explicit mutations where practical.

Initial mutation vocabulary includes:

* CreateNode
* MoveNodes
* DeleteNodes
* CreateConnection
* DeleteConnection

One meaningful user action should correspond to one mutation.

### Undo / Redo

Undo and redo must operate at the level of meaningful user actions.

V0.1 uses reliable model snapshots rather than an unnecessarily complicated command-reversal system.

### Testing

V0.1 should maintain automated tests for:

* visual-model behavior
* port ownership
* connection ownership
* node deletion behavior
* compatibility results
* mutation behavior

Interactive testing remains important for:

* mouse interaction
* selection
* dragging
* visual feedback
* connection creation
* connection deletion
* zoom/pan behavior

---

# V0.1 Architecture Refactor

Before adding substantial new behavior, the oversized canvas implementation should be divided into smaller modules.

The purpose is maintainability, not abstraction for its own sake.

Initial intended separation:

```text
machine_builder/
│
├── app.py
├── canvas.py
│
├── graphics/
│   ├── __init__.py
│   ├── node.py
│   ├── port.py
│   ├── connection.py
│   └── palette.py
│
├── visual_model.py
├── mutations.py
├── store.py
└── compatibility.py
```

The exact final module boundaries may change during refactoring.

## Module Responsibilities

### app.py

Application startup.

Responsible for:

* creating QApplication
* launching the main editor
* application-level metadata

### canvas.py

Main editor orchestration.

Responsible for coordinating:

* the scene
* the view
* the model store
* editor actions
* node creation/deletion
* connection creation/deletion
* selection
* undo/redo
* synchronization between model and graphics

It should not contain the implementation details of every graphics object.

### graphics/node.py

Visual node presentation.

Responsible for:

* drawing component nodes
* node selection
* node movement presentation
* node-local port placement
* node-specific visual behavior

### graphics/port.py

Visual port presentation.

Responsible for:

* drawing ports
* port labels
* hover state
* connection status state
* connection drag initiation
* port-local interaction

### graphics/connection.py

Visual connection presentation.

Responsible for:

* drawing connections
* connection selection
* visual selected state
* connection-local interaction

### graphics/palette.py

Component palette presentation.

Responsible for:

* palette display
* palette drag interaction
* prototype component selection

### visual_model.py

Presentation model.

Responsible for:

* VisualNode
* VisualPort
* VisualConnection
* VisualGroup
* VisualView
* model relationships

It must remain independent of Qt.

### mutations.py

Explicit editing operations.

Responsible for representing user-visible model changes.

### store.py

Model state and editing history.

Responsible for:

* current visual model
* mutation application
* undo
* redo
* change notification

### compatibility.py

Compatibility evaluation.

Responsible for answering whether a proposed port connection is:

* compatible
* incompatible
* unknown
* conditional

It must not draw UI.

---

# V0.1 Deliberately Not Included

The following are intentionally outside the V0.1 completion target:

* canonical machine ontology implementation
* firmware generation
* firmware parsing
* persistent machine-file format
* complete hardware catalog integration
* automatic catalog-to-machine population
* semantic machine validation
* advanced port semantics
* detailed electrical constraints
* voltage/current compatibility modeling
* signal-level semantics
* automatic routing
* manual routing waypoints
* orthogonal routing
* harness modeling
* sub-harnesses
* wire-length calculation
* service slack
* manufacturing slack
* 3D geometry generation
* Blender integration
* hierarchical subsystem editing
* persistent groups
* component locking
* node resizing
* advanced semantic zoom
* multiple simultaneous information layers
* diagnostic visualization
* complete accessibility system
* production-grade theme system

These may be introduced in later versions after the V0.1 interaction foundation is proven.

---

# V0.2 Direction

V0.2 should be defined from what is learned during V0.1 testing rather than predetermined in detail.

Likely areas include:

* richer port semantics
* improved compatibility rules
* direction-independent physical connection creation
* more precise distinction between physical connection and signal direction
* component-specific port definitions
* improved connection routing
* improved node presentation
* persistence
* more realistic machine component examples
* stronger testing around the visual editor

V0.2 planning should be created from the completed V0.1 findings rather than simply extending the original V0.1 plan.

---

# Long-Term Implementation Direction

The Machine Structure Editor is one layer of the broader Machine Builder system.

The intended relationship is:

```text
Canonical / Semantic Machine Model
            ↓
     Semantic Adapter
            ↓
        Visual Model
            ↓
    Editor / Interaction
            ↓
      Qt Presentation
```

The visual editor should remain useful without forcing the canonical machine ontology to become Qt-specific.

Likewise, catalog data, firmware representations, engineering documentation, and knowledge/retrieval systems should integrate through defined boundaries rather than being embedded directly into the visual editor.

---

# Roadmap Maintenance Rules

When a significant implementation decision changes the planned structure:

1. Record the decision in the current version's implementation plan.
2. Update the roadmap only when the change affects the longer-term direction.
3. Do not preserve an obsolete plan merely for consistency.
4. Keep the final implementation state of each completed version documented.

The roadmap is a living engineering document.
The version plans provide the historical record of how each implementation milestone evolved.
