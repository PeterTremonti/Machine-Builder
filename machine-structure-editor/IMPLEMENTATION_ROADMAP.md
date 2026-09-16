# Machine Structure Editor — Implementation Roadmap

## Purpose

This roadmap describes the implementation path for the Machine Structure Editor portion of Machine Builder.

It is an implementation roadmap, not the canonical machine ontology.

The roadmap is expected to change as the software is tested and architectural decisions are made. Significant changes should be documented in the implementation plan for the affected version.

---

# Version Strategy

Each implementation version has two related records:

1. **Implementation Roadmap**
   - The current overall direction.
   - High-level milestones and planned architecture.

2. **Version Implementation Plan**
   - Initial plan for the version.
   - Decisions and changes made during implementation.
   - Final implemented state.
   - Items deliberately carried into the next version.

The plan for a version may change during implementation.

The final state of a completed version is the authoritative record of what was actually implemented.

---

# V0.1 — Visual Structure Editor Foundation

## Status

**Complete**

V0.1 established the first usable visual machine-structure editor.

The version successfully demonstrated:

- canvas interaction
- component palette
- visual nodes
- explicit ports
- persistent port labels
- compatibility feedback
- physical connection creation
- connection selection and deletion
- undo/redo
- multi-selection
- modular graphics architecture

The final automated test suite contains:

```text
20 passed
V0.1 Architectural Result

The visual graphics layer is divided into dedicated modules:

graphics/
├── connection.py
├── node.py
├── palette.py
├── port.py
└── view.py

The main canvas.py remains the editor/orchestration layer.

The visual model remains separate from Qt graphics.

The visual connection model represents physical relationships as:

endpoint A ↔ endpoint B

rather than treating the physical connection as directional.

Semantic signal relationships remain separate:

source → consumer
V0.1 Completion Record

The detailed implementation history is recorded in:

docs/implementation/V0.1_IMPLEMENTATION_PLAN.md

The final V0.1 implementation milestone should be tagged:

v0.1.0
V0.2 — Semantic and Machine-Structure Expansion
Status

Planning not started

V0.2 should be defined after reviewing V0.1 results.

The primary purpose of V0.2 will likely be moving the prototype from generic visual relationships toward richer machine-structure semantics.

Potential areas include:

Port semantics

Move beyond generic categories such as:

signal
electrical
unknown

toward richer semantic roles and domains.

Potential examples:

temperature measurement
step command
direction command
heater control
power
ground
communication
material
fluid
mechanical
Compatibility

Expand the compatibility system to consider:

semantic role
signal identity
electrical characteristics
voltage
current
connector/pin compatibility
domain
machine-specific requirements
Component definitions

Begin integrating richer component definitions that can eventually connect to the broader hardware/catalog architecture.

Persistence

Define the first durable project/visual-model persistence mechanism.

Connection presentation

Investigate:

automatic routing
orthogonal routing
manual waypoints
improved wire organization
Information layers

Begin defining how users can switch between different information/detail layers without forcing every concept onto the same visual representation.

Accessibility

Expand beyond the current color-plus-symbol approach toward a broader accessibility strategy.

Long-Term Implementation Direction

The Machine Structure Editor is one layer of the broader Machine Builder system.

The intended relationship is:

Canonical / Semantic Machine Model
            ↓
     Semantic Adapter
            ↓
        Visual Model
            ↓
    Editor / Interaction
            ↓
      Qt Presentation

The editor should remain independent from:

firmware-specific configuration formats
supplier-specific catalog identity
source-document storage
general project knowledge
knowledge-graph retrieval systems

Those systems should integrate through defined boundaries.

## Implementation Principles

### 1. Prefer meaningful, cohesive modules

Separate code when it represents a genuinely distinct responsibility.

A module should have a clear purpose and a small, understandable public boundary.

Do not split files merely to make them smaller.

Do not create one-file-per-function unless the responsibility genuinely benefits from that separation.

The goal is:

```text
high cohesion
+
low coupling
+
clear boundaries
```

### 2. Prefer small changes over broad rewrites

A normal feature or bug fix should change the smallest reasonable set of modules.

If a seemingly small change repeatedly requires modifying large portions of the codebase, stop and consider whether an architectural boundary is missing or misplaced before continuing.

The preferred direction is:

```text
small change
    ↓
focused tests
    ↓
small refactor if needed
    ↓
continue
```

rather than:

```text
small change
    ↓
large unrelated rewrite
    ↓
large regression surface
```

### 3. Keep responsibilities separated

Code that changes for different reasons should normally live behind separate boundaries.

Examples include:

```text
canonical semantic model
visual model
graphics / rendering
persistence
undo / redo
mutations
hardware catalog
firmware mapping
```

A feature may legitimately cross multiple boundaries, but each module should remain responsible for its own concern.

### 4. Keep module interfaces narrow

Modules should communicate through explicit, understandable interfaces rather than reaching into one another's implementation details.

Prefer:

```text
Module A
    ↓
small public interface
    ↓
Module B
```

over:

```text
Module A
    ↓
reaches into Module B internals
    ↓
depends on private implementation details
```

This allows individual modules to be redesigned without forcing unrelated modules to change.

### 5. Preserve the model/presentation boundary

Canonical machine semantics must remain independent from visual and Qt implementation details.

Qt objects must not become the canonical machine model.

Visual behavior must not silently become machine semantics.

For example:

```text
visual routing
    ≠
canonical Connection

mouse drag direction
    ≠
physical connection direction

canvas position
    ≠
machine placement unless explicitly authored as such
```

### 6. Prefer composition over monolithic classes

When a class begins accumulating several unrelated responsibilities, consider extracting cohesive collaborators rather than continuing to grow the class.

Avoid "god objects" that own unrelated:

```text
modeling
rendering
persistence
business rules
input handling
routing
```

in one place.

### 7. Test after meaningful changes

A successful refactor is one that preserves intended behavior.

After a meaningful architectural or behavioral change:

```text
change
    ↓
focused tests
    ↓
full test suite
```

Tests should protect module boundaries and important behavior, not merely implementation details.

### 8. Refactoring is normal

Modular code is expected to evolve.

When implementation reveals that a responsibility belongs somewhere else:

```text
identify responsibility
    ↓
move/refactor it
    ↓
preserve public behavior
    ↓
run tests
    ↓
document important architectural changes
```

Do not preserve a bad boundary merely because changing it would require moving code.

### 9. Use whole-file replacement when it reduces implementation errors

During early development, whole-file replacements are preferred when they are clearer and safer than complicated incremental editing.

This is an editing workflow preference, not a reason to create large files.

### 10. Keep commits focused

Prefer commits that represent one coherent change.

For example:

```text
Add semantic routing boundary
Add routing tests
Add orthogonal router
Connect router to graphics
```

is easier to understand, test, revert, and debug than one large commit containing several unrelated changes.

### 11. Ask whether a broad change reveals a missing boundary

When a small feature requires changing many apparently unrelated modules, consider two possibilities:

```text
A. The feature legitimately crosses several subsystems.

B. The architecture has not established the correct boundary yet.
```

Do not automatically choose either explanation.

Investigate before expanding the change.

### 12. Document major architectural decisions

When implementation reveals that an earlier assumption was incorrect:

```text
document the discovery
record the decision
update the version plan
update the roadmap when the change affects future versions
```

Implementation convenience must not silently redefine the canonical architecture or ontology.
