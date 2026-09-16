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
The final state of a completed version is the authoritative record of what was actually implemented.

---

# V0.1 — Visual Structure Editor Foundation

## Status

**Complete**

V0.1 established the first usable visual machine-structure editor.

The version successfully demonstrated:

* canvas interaction
* component palette
* visual nodes
* explicit ports
* persistent port labels
* compatibility feedback
* physical connection creation
* connection selection and deletion
* undo/redo
* multi-selection
* modular graphics architecture

The final automated test suite contains:

```text
20 passed
V0.1 Architectural Result
The visual graphics layer is divided into dedicated modules:
```

```text
graphics/
├── connection.py
├── node.py
├── palette.py
├── port.py
└── view.py
```

The main canvas.py remains the editor/orchestration layer.

The visual model remains separate from Qt graphics.

The visual connection model represents physical relationships as:

```text
endpoint A ↔ endpoint B
```

rather than treating the physical connection as directional.

Semantic signal relationships remain separate:

```text
source → consumer
```

## V0.1 Completion Record

The detailed implementation history is recorded in:

```text
docs/implementation/V0.1_IMPLEMENTATION_PLAN.md
```

The final V0.1 implementation milestone should be tagged:

```text
v0.1.0
```

# V0.2 — Semantic and Machine-Structure Expansion

## Status

Planning not started

V0.2 should be defined after reviewing V0.1 results.

The primary purpose of V0.2 will likely be moving the prototype from generic visual relationships toward richer machine-structure semantics.

Potential areas include:

## Port semantics

Move beyond generic categories such as:

```text
signal
electrical
unknown
```

toward richer semantic roles and domains.

Potential examples:

```text
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
```

## Compatibility

Expand the compatibility system to consider:

* semantic role
* signal identity
* electrical characteristics
* voltage
* current
* connector/pin compatibility
* domain
* machine-specific requirements

## Component definitions

Begin integrating richer component definitions that can eventually connect to the broader hardware/catalog architecture.

## Persistence

Define the first durable project/visual-model persistence mechanism.

## Connection presentation

Investigate:

* automatic routing
* orthogonal routing
* manual waypoints
* improved wire organization

## Information layers

Begin defining how users can switch between different information/detail layers without forcing every concept onto the same visual representation.

## Accessibility

Expand beyond the current color-plus-symbol approach toward a broader accessibility strategy.

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

The editor should remain independent from:

* firmware-specific configuration formats
* supplier-specific catalog identity
* source-document storage
* general project knowledge
* knowledge-graph retrieval systems

Those systems should integrate through defined boundaries.

---

# Implementation Principles

## 1. Prefer small, cohesive modules

Prefer modules with a clear, meaningful responsibility and a narrow interface.

A module should have a reason to exist beyond merely keeping individual files short.

Do not split files merely to reduce line count or file size. Cohesion and clear responsibility matter more than the number of files.

## 2. Keep coupling low

Keep dependencies between modules deliberate and limited.

Prefer narrow, understandable interfaces over reaching deeply into another module's internal state.

When one module needs knowledge of many unrelated implementation details elsewhere, consider whether the boundary between those responsibilities is wrong.

## 3. Prefer the smallest reasonable change

For a feature or bug fix, make the smallest change that correctly addresses the problem while preserving the existing architecture and behavior.

Avoid unrelated cleanup or refactoring inside an otherwise focused change unless it is necessary to make the change correct.

## 4. Treat repeated friction as architectural evidence

If a tiny change repeatedly requires editing large or unrelated sections of code, stop and consider whether the problem is actually a missing or incorrect architectural boundary.

Repeated awkward changes are evidence worth investigating.

Do not solve the same boundary problem over and over with increasingly complicated local patches.

## 5. Avoid giant "god" classes and modules

Do not allow a class or module to accumulate unrelated responsibilities simply because it is convenient to put them in one place.

As responsibilities become distinct, consider whether they belong behind separate boundaries.

This does not mean every responsibility needs its own file. The goal is coherent design, not maximal fragmentation.

## 6. Keep major concerns separated

Maintain clear boundaries between:

* canonical semantic model
* visual state
* graphics / presentation
* persistence
* mutations and state transitions
* hardware catalog
* firmware-specific concerns

These concerns may interact through defined interfaces, but one should not quietly become the implementation home for another.

## 7. Refactoring is expected and normal

A module boundary is a design decision, not a permanent commitment.

When implementation reveals that a boundary is wrong, refactor it.

Prefer a deliberate architectural correction over accumulating workarounds around a poor boundary.

## 8. Test after meaningful changes

Run the relevant automated tests after meaningful implementation or architectural changes.

For changes that affect shared behavior or boundaries, run the full test suite.

A refactor is successful when the intended behavior is preserved or deliberately changed and the change is demonstrated by tests.

## 9. Keep commits focused

Keep commits centered on one meaningful change, fix, architectural step, or checkpoint.

Avoid mixing unrelated cleanup with functional work when doing so makes the history harder to understand.

Use commits and tags to preserve implementation history rather than maintaining obsolete parallel implementation directories.

## 10. Document major architectural discoveries

When implementation reveals that an earlier assumption was incorrect:

* document the discovery
* determine whether it is an implementation issue or an architectural issue
* involve the appropriate research / architecture work when semantics are affected
* record the decision
* update the version plan when appropriate
* update the roadmap when the change affects future versions

## 11. Keep versions as milestones, not duplicate implementations

Do not create V0.2, V0.3, etc. directories for parallel implementations.

Use:

* Git commits
* Git tags
* version implementation plans
* the living roadmap

to preserve history.

---

# Version Workflow

For each version:

```text
Initial Plan
      ↓
Implementation
      ↓
Testing
      ↓
Discoveries / Decisions
      ↓
Final Plan
      ↓
Carry-Forward
      ↓
Version Tag
      ↓
Next Version Planning
```

This workflow is intentionally iterative.

The final version is allowed to differ from the original plan when testing demonstrates that a different design is better.

---

# Current State

Latest completed version:

```text
v0.1.0
```

Next version:

```text
V0.2
```

V0.2 implementation should not begin until its own plan has been created and reviewed.
