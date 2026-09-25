# Machine Builder — Project Current State

**Purpose:** Cross-workstream synchronization for the Machine Builder project.

**Status:** Living project snapshot; not a replacement for architecture/decision documents.

**Last updated:** 2026-09-25

---

## 1. Purpose of this document

Machine Builder is being developed through several parallel chats/workstreams.

This document provides a shared project-level snapshot so that a new or returning workstream can understand:

* what the project currently considers settled
* what implementation work is active
* what implementation has recently discovered
* what architectural questions are currently being watched
* where workstreams intersect
* which facts are current versus historical

This document is intentionally smaller and more operational than the detailed architecture and research records.

### Authority

This document is a **synchronization aid**, not the canonical source for individual technical decisions.

Use:

* canonical architecture/decision documents for settled architectural decisions
* source code and tests for actual implementation state
* current branch state for work-in-progress implementation details
* this document for cross-workstream context

Do not turn an exploratory observation in this document into an architectural decision without the appropriate research/architecture review.

---

# 2. Current project structure

Machine Builder currently uses multiple parallel workstreams.

```text
main
├── wip-routing-diagnostics
│   └── wire routing / interactive routing investigation
│
└── wip-controller-board-breakout
    └── controller boards / board visualization /
       controller resources / ports / related work
```

The workstreams are intentionally independent.

They are **not competing architectures**.

Their purpose is to allow implementation to proceed in focused areas while concrete implementation discoveries feed back into research and architecture.

The intended feedback loop is:

```text
Research / Architecture
        ↓
Implementation
        ↓
Tests / real behavior
        ↓
New evidence
        ↓
Architecture review
        ↓
Reinforce / Watch / Reconsider / New Principle
```

Most implementation discoveries should remain implementation details.

Only discoveries that expose a missing distinction, contradiction, or insufficient abstraction should modify the architecture.

---

# 3. Established architectural direction

The project currently treats the **physical machine as the machine**.

Firmware is a versioned implementation of the machine rather than the identity of the machine.

The broad direction remains:

```text
Physical Machine
    ↓
Canonical Machine Model
    ↓
Firmware Requirements / Mapping
    ↓
Target Firmware + Version
    ↓
Generated Configuration
```

and in the reverse direction:

```text
Firmware / Configuration
    ↓
Semantic Interpretation
    ↓
Canonical Machine Model
```

The canonical semantic model is authoritative.

Visual/editor state is separate presentation and authoring state.

Important existing boundaries include:

* physical machine identity vs firmware implementation
* canonical semantic model vs visual/editor state
* reusable Hardware Definition vs installed hardware instance
* Controller vs Controller Resource
* Controller Resource vs physical Port / Connector / Pin
* physical Connection vs functional participation
* Function vs Capability
* machine semantics vs visual layout/routing
* known information vs unknown/unspecified information

Unknown information is valid and must not be fabricated simply to satisfy a UI or schema.

---

# 4. V0.2 architecture status

The V0.2 semantic checkpoint remains in force.

Current research evidence does **not** justify reopening the core ontology.

The current model already distinguishes concepts including:

* Machine
* Machine Component
* Subsystem
* Hardware Definition
* Port
* Connector
* Pin / Terminal
* Connection
* Controller
* Controller Resource
* Controller Resource Assignment
* Function
* Capability
* calibration / provenance
* firmware mapping concepts

Function and Capability remain separate.

Task / Process / Operation / Action / Procedure distinctions remain deferred rather than being prematurely folded into Function.

Future semantic additions should require concrete evidence from:

* real machines
* firmware
* implementation
* testing
* external research

The increasing complexity of implementation is not, by itself, evidence that the V0.2 ontology is wrong.

---

# 5. Active workstream: Routing / Diagnostics

## Branch

`wip-routing-diagnostics`

## Current reported status

Latest directly reported routing workstream result:

```text
Full suite: 695 passed
tests/test_connection_routing.py: 38 passed
```

An earlier broader routing-focused group was reported as 54 tests with 694 full-suite tests.

For current synchronization purposes:

* **695** = latest reported full-suite result
* **38** = current directly targeted `tests/test_connection_routing.py` result
* **54 / 694** = historical checkpoint information

The exact local branch state should be verified from the developer's checkout when implementation work resumes.

---

## Current routing investigation

The active problem is:

> A very small movement of a component can cause a disproportionately large change in an orthogonal wire elbow or route shape.

Recent diagnostics exposed a particularly useful case:

```text
node-4 Y = 24.250
        ↓
existing route topology

node-4 Y = 24.260
        ↓
large route/topology change
```

The diagnostic reason for the transition was:

```text
previous stable route was blocked
```

The transition was **not** caused by endpoint mismatch; the endpoint escape geometry remained unchanged.

The important observed chain is:

```text
tiny obstacle movement
        ↓
previous route becomes blocked
        ↓
normal stability comparison is bypassed
        ↓
fresh candidate route is selected
        ↓
route topology changes substantially
```

This distinguishes the current problem from a simple "stability tolerance is too small" problem.

---

## Routing implementation progress

The routing implementation now has substantially richer diagnostics around:

* previous stable route
* candidate route
* selected route
* route costs
* stability tolerance
* decision reason
* route transitions
* transition costs
* endpoint escape geometry

A temporary Routing Debug Mode can bypass history-based stability behavior to expose the underlying candidate route.

A geometry-boundary issue involving floating-point movement was also isolated and addressed with a focused geometry epsilon, with regression coverage.

The router remains modularized across focused routing modules rather than moving back toward a monolithic canvas.

---

# 6. Routing architectural observation

## Established / reinforced

The existing architecture is strongly reinforced by the routing work:

```text
Canonical Connection
        ≠
Visual Route
```

The semantic Connection answers:

> What is physically/semantically connected?

The visual route answers:

> How is that Connection represented spatially in the editor?

Routing diagnostics, route history, stability state, transition reasons, debug state, and similar information are presentation/runtime concerns.

They do not belong in canonical machine semantics.

---

## New architectural candidate

The routing investigation provides concrete evidence that the visual route itself is usefully distinguished into:

### Route topology

Structural organization of the path:

* corridor choice
* side choice
* bend sequence
* structural path organization

### Route geometry

Exact spatial realization:

* segment coordinates
* elbow coordinates
* offsets
* lengths
* distances

The observed behavior demonstrates why this distinction matters:

```text
small geometric change
        can produce
large topology change
```

An intended interactive-editing behavior may instead be:

```text
same topology
+
adjusted geometry
```

rather than:

```text
discard topology
+
fresh path selection
```

### Current status

**NEW PRINCIPLE — candidate**

This is currently considered a **visual/presentation-layer concept**, not a new canonical machine entity.

The following remain implementation concerns unless future evidence says otherwise:

* incremental routing
* bend nudging
* corridor reuse
* stability/hysteresis tolerance
* topology penalties
* route-cost formulas
* pathfinding graph construction
* endpoint escape behavior

In particular, numeric routing parameters must not become architecture merely because they are important to the current implementation.

---

# 7. Routing questions still open

These remain under investigation:

### Topology-preserving repair

Can an existing route with a locally invalid segment be repaired by adjusting geometry while preserving its topology before a full reroute is attempted?

### Repair vs reroute boundary

Under what conditions is topology-preserving repair valid, and when must a genuinely new route topology be selected?

### Persistence of topology

Does route topology need to become explicit persisted presentation state, or can the necessary continuity be reconstructed from existing saved route/waypoint state?

This is currently a **WATCH** item, not a decision.

---

# 8. Active workstream: Controller / Board

## Branch

`wip-controller-board-breakout`

This branch was created from `main`.

Its purpose is to investigate and implement:

* controller-board creation
* board/node presentation
* controller resources
* ports / connectors / pins
* resource assignment presentation
* related board functionality

It remains independent of the routing branch.

---

# 9. Controller / board architecture currently supported

The existing conceptual chain remains:

```text
Physical Machine
    ↓
Machine Component
    ↓
Hardware Definition
    ↓
Controller
    ↓
Controller Resource
    ↓
Port / Connector / Pin
    ↓
Connection
    ↓
Function / Capability
```

However, the arrows above should not automatically be interpreted as containment.

The current architecture deliberately distinguishes reusable hardware description from installed machine state and distinguishes controller resources from physical interfaces.

---

# 10. Existing board-related implementation foundation

The current implementation already contains substantial infrastructure relevant to board work.

### Hardware Definition

`HardwareDefinition` already exists as a canonical reusable object.

`MachineComponent` already references reusable hardware definitions and provides an implementation precedent for:

```text
HardwareDefinition
        ↓
MachineComponent
        ↓
instance-specific SemanticPorts
```

This is important because it demonstrates that reusable hardware information and machine-specific instances can already coexist without creating a new ontology for every hardware category.

---

## Controller

A canonical `Controller` already exists.

It can be:

* attached to a Machine
* queried
* edited
* persisted

The current Controller model does **not** currently contain an explicit `hardware_definition_id`.

This has become an architectural **WATCH** item.

---

## Controller Resource

`ControllerResource` already exists and is associated with a Controller.

The resource remains its own semantic object rather than becoming a visual port or physical connection endpoint.

---

## Controller Resource Assignment

`ControllerResourceAssignment` already exists and records relationships such as:

```text
source
    ↓
Controller Resource
```

This is distinct from a physical Connection.

The board work should preserve that distinction.

---

## Visual controller representation

A controller can already be projected into a `VisualNode` using a semantic reference.

Existing implementation/test coverage explicitly keeps controller visual nodes from automatically becoming collections of ordinary visual ports.

This is an important architectural guard.

The board UI can therefore become richer without automatically implying:

```text
Controller Resource
        ↓
VisualPort
```

That shortcut should be avoided unless concrete evidence requires a new representation.

---

# 11. Controller / board architectural watch items

## WATCH 1 — Installed Controller ↔ Hardware Definition

`MachineComponent` already has an explicit hardware-definition relationship.

`Controller` currently does not.

The board work should test a real documented controller board and answer:

> How should an installed Controller identify or reference its reusable Hardware Definition?

Do not solve this prematurely by putting a board identifier into an untyped property bag.

At present this is a **WATCH** item, not an architectural change.

---

## WATCH 2 — Controller Resource ↔ Connector / Pin

A Controller Resource and a physical connector/pin are not necessarily the same thing.

A resource may represent something such as:

* a driver channel
* GPIO
* PWM
* ADC
* communication resource
* other controller capability

while a connector/pin represents a physical/electrical interface.

A real documented board should determine whether an explicit relationship between these concepts is required.

For now:

```text
Controller Resource
        ≠
Port / Connector / Pin
```

is **REINFORCED**.

---

## WATCH 3 — Board-level visual detail

A controller board may need to visually expose:

* board identity
* resource information
* connector information
* pin information
* assignments
* grouped or board-specific presentation

The visual representation should not force a new canonical semantic entity merely because the UI becomes more detailed.

The first real board should test whether existing primitives compose cleanly.

---

## WATCH 4 — Board connector/pin modeling

The canonical model already has Port, Connector, and Pin/Terminal concepts.

`SemanticPort` already provides `connector_id` and `pin_id`.

The board work should determine whether these concepts are sufficient for documented controller-board interfaces or whether a missing relationship becomes evident.

No new `BoardConnector`, `BoardPin`, or similar ontology has been justified yet.

---

# 12. First useful board experiment

The preferred first experiment is deliberately small:

```text
One real documented controller board
        ↓
Hardware Definition
        ↓
installed Controller
        ↓
a small set of documented Controller Resources
        ↓
existing Controller VisualNode
        ↓
board-oriented visual presentation
```

The experiment should answer:

1. Can the installed Controller cleanly identify/reference the reusable board definition?

2. Can documented board resources be represented without turning them into VisualPorts?

3. Can connectors and pins be represented without confusing physical interfaces with controller resources?

The objective is to **test composition of existing concepts**, not invent a new Board ontology before evidence exists.

---

# 13. What the board work has NOT justified

There is currently no evidence requiring new canonical entities such as:

```text
Board
BoardResource
BoardPort
BoardPin
BoardBreakout
ControllerBoardInstance
```

The current architecture should be tested before expanding the ontology.

The default assumption remains:

> Use the existing model until a real documented board proves that something is missing.

---

# 14. Cross-workstream interaction

## Routing ↔ architecture

Routing provides evidence for:

```text
Connection semantics
        ≠
visual route topology
        ≠
visual route geometry
```

The topology/geometry distinction currently belongs inside visual/editor state.

It does not imply a change to Connection semantics.

---

## Routing ↔ board work

The routing system's use of graphical endpoints and scene geometry does not make Controller Resources into physical Ports.

The board work should preserve:

```text
Controller Resource
        ≠
Visual Port
```

and:

```text
Controller Resource Assignment
        ≠
Physical Connection
```

The routing branch should remain independent of the board branch unless a concrete dependency appears.

---

## Board ↔ semantic authoring

Board implementation should continue to support the existing principle that canonical semantic editing flows through the semantic model.

A board visual is a projection of canonical data, not a second canonical model.

---

## Board ↔ firmware mapping

No board evidence currently changes the existing firmware architecture.

The intended relationship remains roughly:

```text
physical hardware/resource
        ↓
machine-specific use / assignment
        ↓
firmware-specific implementation/mapping
```

Firmware remains an implementation of the machine rather than the machine's identity.

---

# 15. Current architecture status summary

| Area                                      | Status                    | Current understanding                                                                   |
| ----------------------------------------- | ------------------------- | --------------------------------------------------------------------------------------- |
| Canonical machine model                   | REINFORCE                 | V0.2 remains coherent                                                                   |
| Canonical vs visual state                 | REINFORCE                 | Strongly reinforced by routing and board UI work                                        |
| Physical machine vs firmware              | REINFORCE                 | No evidence of a problem                                                                |
| Hardware Definition vs installed hardware | REINFORCE                 | Existing MachineComponent precedent holds                                               |
| Controller vs Controller Resource         | REINFORCE                 | Existing model is holding                                                               |
| Controller Resource vs Port/Pin           | REINFORCE                 | Do not collapse these concepts                                                          |
| Assignment vs Connection                  | REINFORCE                 | Distinct semantic relationships                                                         |
| Route topology vs route geometry          | NEW PRINCIPLE — candidate | Useful visual-layer distinction exposed by implementation                               |
| Incremental/topology-preserving routing   | WATCH                     | Strong implementation/UX candidate, not yet architecture                                |
| Persistent route topology                 | WATCH                     | Need further evidence                                                                   |
| Controller ↔ Hardware Definition          | WATCH                     | First real board should test this boundary                                              |
| Resource ↔ Connector/Pin                  | WATCH                     | Real board should determine whether relationship is needed                              |
| Board visual structure                    | WATCH                     | Existing visual infrastructure should be tested before introducing new semantic objects |
| New Board ontology                        | REINFORCE                 | No evidence currently requires one                                                      |
| Task / Process / Operation ontology       | WATCH                     | Deferred; future machine stress cases may revisit                                       |
| General manufacturing-cell ontology       | WATCH                     | Future work; not a V0.2 requirement                                                     |

---

# 16. Documentation / synchronization note

Repository documentation is currently behind portions of the active implementation.

Examples previously observed include historical test counts and older implementation handoffs that no longer represent the latest WIP state.

Therefore:

```text
actual source code + actual tests + current branch state
        >
historical handoff/test-count documentation
```

This file exists partly to reduce that synchronization problem, but it must itself be updated when a meaningful project checkpoint occurs.

Do not treat an old test count in an older handoff as the current implementation baseline.

---

# 17. Rules for future workstreams

A new Machine Builder chat should:

1. Read this document first.
2. Locate the relevant detailed architecture/research/implementation handoff documents.
3. Inspect the actual code and tests before making implementation claims.
4. Preserve settled architecture unless concrete evidence shows it is insufficient.
5. Clearly distinguish implementation heuristics from architectural principles.
6. Report discoveries that may affect other workstreams.
7. Update this document only when a meaningful project-level state change has occurred.

The purpose is not to eliminate independent work.

The purpose is to make independent work **compatible and mutually visible**.

---

# 18. Current "do not reopen without evidence" list

Do not reopen these simply because implementation has become more complex:

* V0.2 core ontology
* physical machine identity vs firmware
* canonical semantic model vs visual/editor state
* Hardware Definition vs installed hardware
* Controller vs Controller Resource
* Controller Resource vs Port/Connector/Pin
* Connection vs functional participation
* Function vs Capability

Revisit them only when concrete implementation, testing, research, or real-machine evidence demonstrates:

* insufficiency
* ambiguity
* contradiction
* an implementation dead end caused by the model
* a semantic distinction that cannot be represented coherently

---

# 19. Open project-level questions

These are deliberately limited to questions that currently have enough evidence to matter.

### Routing

* Should visual route topology eventually become an explicit persisted presentation concept?
* What is the correct boundary between topology-preserving repair and full reroute?

### Controller / Board

* How should an installed Controller reference or inherit its reusable Hardware Definition?
* How should documented board connectors/pins relate to Controller Resources when a real board demonstrates a need for that relationship?
* What board-level visual structure provides useful authoring/inspection without creating a second semantic model?

### Future semantic scope

* When do Process / Operation / Task concepts become necessary for machines that behave more like configurable manufacturing cells?
* Does a future hybrid machine such as XYZO expose a missing relationship rather than a missing ontology entity?

These remain open questions, not decisions.

---

# 20. Recent project-level lesson

The project is now using implementation as an architectural feedback mechanism rather than merely as execution of a finished design.

A useful pattern has emerged:

```text
implementation symptom
        ↓
targeted investigation
        ↓
research / evidence
        ↓
candidate conceptual distinction
        ↓
focused experiment
        ↓
architecture decision only if warranted
```

The routing investigation is a good example:

```text
large elbow jump
        ↓
diagnostics
        ↓
previous route was blocked
        ↓
topology vs geometry becomes useful vocabulary
        ↓
test topology-preserving repair
        ↓
decide later whether persistence/architecture needs to change
```

The controller-board work is intended to follow the same pattern:

```text
real documented board
        ↓
attempt composition using existing concepts
        ↓
identify actual boundary failures
        ↓
only then consider architectural change
```

This is the current project strategy.

---

# 21. Current workstream handoff targets

### Research / Architecture

Continue evaluating concrete implementation findings without unnecessarily reopening V0.2.

Current focus:

* route topology vs route geometry
* Controller ↔ Hardware Definition question
* board/resource/port boundaries
* maintaining project-wide architectural coherence

### Controller / Board

Use `wip-controller-board-breakout`.

Start with one real documented board and test whether the existing concepts compose cleanly.

### Routing / Diagnostics

Use `wip-routing-diagnostics`.

Continue investigating topology-preserving route repair rather than simply increasing stability tolerance.

### All workstreams

When a durable project-level discovery occurs, report it back to Planning / Architecture and consider updating this document at the next meaningful checkpoint.

---

# 22. Last known cross-workstream synchronization

As of this document:

* V0.2 architecture remains intact.
* Routing provides concrete evidence supporting a topology/geometry distinction in visual route state.
* Routing's current failure mode appears to involve invalidation of the previous route followed by fresh path selection.
* A topology-preserving repair mechanism is a promising implementation experiment, not yet an architectural requirement.
* Controller-board implementation has a separate branch: `wip-controller-board-breakout`.
* Existing controller, resource, assignment, hardware-definition, semantic-port, and controller-visual infrastructure provides a substantial foundation.
* The main unresolved board architecture question is how an installed Controller relates to its reusable Hardware Definition.
* No new canonical Board ontology has yet been justified.
* The project should continue using implementation evidence to reinforce or refine architecture rather than allowing implementation complexity alone to trigger redesign.
