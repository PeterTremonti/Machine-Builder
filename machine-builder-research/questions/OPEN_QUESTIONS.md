# Machine Builder Open Questions
## O0.1 Checkpoint Status

This file now emphasizes questions that remain relevant after the minimum 3D-printer model was established.

## Status definitions

- Open — recognized but not resolved
- Investigating — actively researched
- Blocked — waiting on another dependency
- Deferred — intentionally postponed
- Resolved — decision made and recorded
- Superseded — replaced by another direction

## O0.1 priority questions completed

The original first-round priority set has now been worked through at the level required for O0.1:

- Q-005 — Formal Property Model — Resolved enough for O0.1
- Q-009 — First-Class Relationships — Resolved enough for O0.1
- Q-011 — Universal / Domain-Specific Connections — Resolved with electrical-only O0.1 scope
- Q-015 — Relationship Cardinality — Resolved enough for O0.1
- Q-016 — Provenance Model — Resolved enough for O0.1
- Q-020 — Formal Axis Model — Resolved enough for O0.1
- Q-022 — Kinematic Representation — Resolved enough for O0.1
- Q-028 — Calibration Modeling — Resolved enough for O0.1
- Q-031 — Function Organization — Resolved enough for O0.1
- Q-032 — Operation ↔ Function — Operation hierarchy deferred; Function remains in scope
- Q-038 — Controller Resource — Resolved enough for O0.1
- Q-039 — Shared Resources — Resolved enough for O0.1
- Q-041 — Port Definition — Resolved enough for O0.1
- Q-042 — Port ↔ Connector ↔ Pin — Resolved for electrical O0.1 scope
- Q-044 — Direction — Resolved enough for O0.1
- Q-055 — Evaluation Engine Scope — Scoped; detailed evaluator deferred
- Q-058 — Firmware Capabilities — Resolved enough for O0.1
- Q-059 — Firmware Version Differences — Resolved
- Q-060 — Lossy Translation — Resolved enough for O0.1
- Q-075 — Ontology Maturity Threshold — Satisfied for O0.1 checkpoint

## Remaining O0.1 issues

There are no known unresolved conceptual blockers preventing implementation of the minimum O0.1 machine/firmware model.

Remaining questions should be handled by implementation evidence rather than reopening foundational ontology work prematurely.

## O0.2 research candidates

The highest-priority next questions are:

1. How should water-cooled hotends and coolant/plumbing topology be represented?
2. How should richer filament/material paths, tubing, and couplers be represented?
3. How should the firmware knowledge base be stored/versioned locally?
4. What mapping data is required for each supported firmware family/version?
5. Which canonical-to-firmware mappings can be generated/calculated versus requiring curated rules?
6. What additional electrical-interface semantics are required by the visual connection engine?
7. Which broader fluid/mechanical/material interfaces should become first-class after real use cases require them?

These questions belong to O0.2/R0.2 or later unless implementation discovers an O0.1 blocker.

## Policy

Do not invent new ontology questions simply because a future domain could eventually need them. Add a new question when a real machine, firmware, implementation test, or evidence gap demonstrates that the current model is insufficient.
