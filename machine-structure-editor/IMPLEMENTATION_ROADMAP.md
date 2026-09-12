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

Implementation Principles
1. Prefer meaningful modules

Separate code when it represents a genuinely distinct responsibility.

Do not split files merely to make them smaller.

2. Prefer whole-file replacement for major restructuring

During early development, whole-file replacements are preferred when they reduce editing errors.

3. Test after every architectural change

A successful refactor is one that preserves behavior.

4. Keep model and presentation separate

Qt objects should not become the canonical machine model.

5. Do not encode accidental UI behavior as machine semantics

For example:

Mouse drag direction

must not silently become:

Physical machine connection direction
6. Document major architectural decisions

When implementation reveals that an earlier assumption was incorrect:

document the discovery
record the decision
update the version plan
update the roadmap when the change affects future versions
7. Versions are milestones, not folders

Do not create V0.2, V0.3, etc. directories for parallel implementations.

Use:

Git commits
Git tags
version implementation plans
the living roadmap

to preserve history.

Version Workflow

For each version:

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

This workflow is intentionally iterative.

The final version is allowed to differ from the original plan when testing demonstrates that a different design is better.

Current State

Latest completed version:

v0.1.0

Next version:

V0.2

V0.2 implementation should not begin until its own plan has been created and reviewed.