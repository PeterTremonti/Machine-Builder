Last modified by Visual Machine Editor chat 09/15/26 11:23pm

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

# IMPORTANT: Where to start

**Every new chat working on Machine Builder should read this README first.**

Do not assume that a folder's local `START_HERE.md` is the first project document.

This README establishes:

* the current project structure
* which documents are authoritative for which subjects
* which chat role should be involved
* where implementation files live
* where research and architecture records live
* what is current versus historical

After reading this file, follow the section for the role of the current chat.

---

# Chat roles

Machine Builder uses separate working chats for different kinds of work.

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

Then follow its recovery/read order.

Important research documents include:

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
machine-builder-research/handoffs/
```

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

Important files:

```text
machine-structure-editor/IMPLEMENTATION_ROADMAP.md

machine-structure-editor/docs/implementation/
machine-structure-editor/src/machine_builder/
machine-structure-editor/tests/
```

Current implementation handoff:

```text
machine-builder-research/handoffs/V0.2_IMPLEMENTATION_HANDOFF.md
```

The implementation chat should read the current implementation handoff before making substantial changes.

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
* future visual affordances for semantic information

The visual editor lives inside:

```text
machine-structure-editor/src/machine_builder/
```

with presentation-specific code primarily under:

```text
machine-structure-editor/src/machine_builder/graphics/
```

The visual-editor chat should read:

```text
README.md

machine-builder-research/START_HERE.md
machine-builder-research/handoffs/V0.2_IMPLEMENTATION_HANDOFF.md

machine-structure-editor/docs/implementation/V0.2_IMPLEMENTATION_PLAN.md
```

and then inspect the current implementation before proposing changes.

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

Future ideas may be recorded as candidates without automatically becoming part of the current milestone.

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

The visual model is not a second machine model.

Visual state includes things such as:

* canvas position
* size
* routing geometry
* selection
* zoom
* pan
* collapsed/expanded presentation
* other presentation-only state

Canonical semantic information includes things such as:

* Machine
* Machine Component
* Hardware Definition
* Ports
* Connectors
* Pins / terminals
* Connections
* Functions
* Capabilities
* controller resources
* properties
* calibration
* provenance
* semantic relationships

---

# Current project state

## Research / architecture

The project has established the O0.1 canonical-machine foundation.

Current implementation milestone:

```text
V0.2
```

The research checkpoint is:

```text
machine-builder-research/checkpoints/V0.2_RESEARCH_CHECKPOINT.md
```

The current implementation-facing handoff is:

```text
machine-builder-research/handoffs/V0.2_IMPLEMENTATION_HANDOFF.md
```

---

## Current implementation checkpoint

The Machine Structure Editor has established the V0.2 semantic-authoring foundation.

Current automated test state:

```text
94 passed
```

The current canonical foundation includes:

* Machine
* Machine Component
* Hardware Definition
* Semantic Port
* Provenance
* canonical Connections
* visual/canonical model boundary
* semantic projection
* semantic authoring
* component-scoped instantiated port identities
* visual + canonical connection authoring
* connection deletion
* undo/redo
* mutation rollback

---

# Implementation file map

```text
machine-structure-editor/
│
├── pyproject.toml
├── IMPLEMENTATION_ROADMAP.md
│
├── docs/
│   └── implementation/
│       ├── V0.1_IMPLEMENTATION_PLAN.md
│       └── V0.2_IMPLEMENTATION_PLAN.md
│
├── src/
│   └── machine_builder/
│       ├── __init__.py
│       ├── __main__.py
│       ├── app.py
│       │
│       ├── visual_model.py
│       ├── semantic_model.py
│       ├── semantic_connection.py
│       ├── semantic_projection.py
│       ├── model_boundary.py
│       ├── editor_state.py
│       ├── mutations.py
│       ├── store.py
│       ├── compatibility.py
│       └── hardware_catalog.py
│
│       └── graphics/
│           ├── __init__.py
│           ├── connection.py
│           ├── node.py
│           ├── palette.py
│           ├── port.py
│           └── view.py
│
└── tests/
    ├── test_visual_model.py
    ├── test_compatibility.py
    ├── test_semantic_model.py
    ├── test_semantic_authoring.py
    ├── test_semantic_projection.py
    ├── test_semantic_connection.py
    ├── test_model_boundary.py
    ├── test_connection_authoring.py
    ├── test_fan_fixture.py
    ├── test_hardware_catalog.py
    └── test_store.py
```

Note:

```text
test_semantic_connection.py
```

is the correct current filename.

---

# Important implementation concepts

## Machine Component vs Hardware Definition

These are intentionally separate.

```text
Machine Component
        ↓
Hardware Definition
```

A Machine Component is the machine-specific occurrence.

A Hardware Definition describes known hardware characteristics.

The same Hardware Definition may be used by multiple Machine Components.

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

# Repository conventions

Prefer:

* small modular files
* clear boundaries between concerns
* full-file replacements during implementation work when practical
* automated tests for each meaningful change
* clean checkpoints
* durable documentation for architectural decisions

Avoid:

* silently replacing architecture during implementation
* giant monolithic modules when a small module is clearer
* making visual state the semantic authority
* inventing unknown machine information
* treating old experimental implementations as current architecture

---

# Historical / obsolete material

The old visual-builder implementation is historical.

The following should **not** be treated as the current architecture:

```text
builder_versions/
```

That directory represents the earlier visual-only builder work and should be retired rather than used as an implementation reference.

Likewise, temporary paste/workaround files in the repository root should not be treated as project documentation.

---

# Current implementation priority

The current implementation work should continue from the V0.2 implementation handoff rather than attempting to resurrect the old builder.

When in doubt:

```text
Research question
    → research / architecture documents

Implementation question
    → implementation handoff + current source/tests

Visual behavior question
    → implementation source + implementation handoff + relevant research

Semantic disagreement
    → research / architecture
```

The repository is the durable shared memory between chats.
