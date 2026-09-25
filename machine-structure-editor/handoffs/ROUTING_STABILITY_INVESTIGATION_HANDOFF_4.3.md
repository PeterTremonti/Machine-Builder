# Routing Stability Investigation Handoff — Coder 4.4

Date: 2026-09-25

## Purpose

This handoff continues the focused single-wire routing investigation on:

`wip-routing-diagnostics`

The immediate goal is to understand and, if appropriate, improve route continuity during tiny component movements without rewriting the routing system.

The next experiment must distinguish route geometry changes from route topology changes.

Do not add a second wire until the single-wire behavior is understood.

---

# Current checkpoint

## Branch

```text
wip-routing-diagnostics
```

## Current reported local state

The latest developer-reported working state was:

```text
working tree clean
branch pushed
```

The developer has also created a separate branch from `main` for controller-board work:

```text
wip-controller-board-breakout
```

That branch is intentionally independent of routing.

## Current tests

Latest directly reported local results:

```text
tests/test_connection_routing.py
38 passed

full suite
695 passed
```

The full suite produced a Windows pytest cleanup warning after all tests passed:

```text
PermissionError: [WinError 5]
...
pytest-current
```

This occurred during pytest's post-suite cleanup and was not a test failure.

An earlier project checkpoint referenced:

```text
54 focused tests
694 full tests
```

That appears to have represented a broader focused routing/inspector/canvas test selection rather than only `tests/test_connection_routing.py`.

Use current local test output as authority.

---

# Tool-use constraint for Coder 4.4

The Coder 4.4 routing experiment is intentionally being run without:

* Python
* Jupyter
* ChatGPT Data Analysis
* new file uploads
* new image uploads

GitHub/web inspection remains explicitly allowed.

Normal local development should use:

* PowerShell
* pasted source/output when necessary
* local pytest
* local GUI testing
* GitHub/web research when useful

The reason for the restriction is experimental: recent chats have shown capability-specific usage pauses that appear to affect different conversations.

Recent observed banners included:

```text
You've reached the limit for chats that include data analysis.
```

and:

```text
You've reached the limit for chats that include files or images.
```

One routing conversation became blocked while several other Machine Builder conversations remained usable.

The exact service-side accounting is unknown.

Coder 4.4 should therefore remain text/GitHub/local-console based so that its own behavior does not introduce Python/Data Analysis or file/image usage into the experiment.

---

# Current architecture boundary

Routing remains a visual/editor/runtime concern.

Canonical machine semantics remain authoritative for:

* Machine
* Machine Components
* Hardware Definitions
* Ports
* Connectors
* Pins/terminals
* Connections
* Functions
* Capabilities
* Controller Resources
* Assignments
* Calibration
* provenance
* semantic relationships

Visual/editor state includes:

* node positions
* node sizes
* visual layout
* routing geometry
* route continuity state
* selection
* zoom
* pan
* diagnostics
* temporary routing debug information

Do not move routing heuristics into the canonical machine model.

---

# Important conceptual distinction

The investigation now has concrete evidence supporting the distinction between:

## Route geometry

The exact spatial realization:

* segment coordinates
* elbow coordinates
* distances
* offsets
* endpoint-adjacent adjustments

## Route topology

The structural path organization:

* side/corridor selection
* sequence of bends
* structural direction pattern
* which spatial corridor the route uses

These are related but not identical.

A tiny component movement can require a small geometric adjustment without necessarily requiring a topology change.

That distinction is now considered an important visual-editor concept.

Whether route topology needs explicit persistent representation remains an architecture/persistence question and has not been decided.

---

# Current production routing modules

The router remains modular:

```text
src/machine_builder/graphics/
    connection.py
    connection_routing.py
    connection_routing_pathfinder.py
    connection_routing_relevance.py
    connection_routing_endpoint.py
```

The canvas remains modular:

```text
canvas.py
canvas_ui.py
canvas_editing.py
canvas_palette.py
canvas_selection.py
canvas_interaction.py
canvas_scene.py
```

Do not move routing behavior back into a monolithic canvas implementation.

Do not refactor the routing modules merely because the routing test file is large.

---

# Current routing constants

Known current values:

```text
ROUTING_MARGIN = 16.0
STUB_LENGTH = 40.0
ROUTING_RELEVANCE_RADIUS = 50.0
BEND_PENALTY = 80.0
ENDPOINT_DIRECTION_PENALTY = 160.0
U_TURN_MIN_SEPARATION = 32.0
ESCAPE_CLEARANCE = 1.0
ROUTE_STABILITY_COST_TOLERANCE = 16.0
```

`ROUTE_STABILITY_COST_TOLERANCE = 16.0` remains experimental.

Do not tune it further as the next step.

Do not use a huge hysteresis value to conceal an underlying topology problem.

---

# Existing routing protections

The router already contains several protections/fixes.

## Obstacle relevance

Relevant obstacles are expanded through nearby obstacle chains rather than considering only the initially detected obstacle set.

This prevents the router from ignoring a component that becomes important through a chain of nearby obstacles.

## Candidate-route relevance

The route can trigger additional obstacle relevance checking and rebuilding.

There is also final blocking protection so a returned route does not knowingly cross an obstacle.

## Narrow-corridor protection

The pathfinder has geometry safeguards including:

```text
MIN_ROUTING_CORRIDOR = 8.0
GEOMETRY_EPSILON = 0.001
```

These protect against effectively unusable sliver corridors.

## Boundary floating-point fix

The orthogonal collision test was updated to treat exact/sub-epsilon boundary contact robustly instead of letting microscopic floating-point drift turn a boundary-aligned segment into a blocked route.

Regression coverage was added for:

* exact boundary
* sub-epsilon penetration
* meaningful penetration

This fix passed the reported routing tests and full suite.

Do not revert it merely because the topology issue remains.

---

# Routing Debug Mode

Routing Debug Mode deliberately bypasses route stability history.

It is useful for observing raw deterministic route selection.

It should not be used as the normal-mode stability test.

When Debug Mode is ON:

```text
debug mode bypassed route stability
```

When Debug Mode is OFF:

normal stable-route history and cost comparison apply.

---

# Current route-selection behavior

The current route-selection process is approximately:

```text
candidate route generated
        ↓
candidate cost calculated
        ↓
debug-mode bypass
        ↓
previous stable route exists?
        ↓
previous route structurally valid?
        ↓
prepared endpoint coordinates still match?
        ↓
previous route still clear of obstacles?
        ↓
compare previous/candidate cost
        ↓
apply stability tolerance
```

The important point is that several conditions can discard the previous route before the normal cost/tolerance comparison.

---

# Endpoint mismatch hypothesis

The current implementation does contain an endpoint-mismatch branch.

When:

```text
previous[0] != start
or
previous[-1] != end
```

the previous route can be rejected before normal cost/tolerance comparison.

Therefore the hypothesis:

> a prepared endpoint movement can bypass the existing hysteresis mechanism

is valid as a property of the current code.

However, it has NOT been established as the cause of the current node-4 elbow jump.

---

# Critical captured transition

Saved test machine:

```text
wiring test machines/4 parts.machine.json
```

Important nodes:

```text
node-1 Temperature Sensor
x = -230
y = -75
width = 180
height = 100
temperature output on right

node-2 Temperature Controller
x = -225
y = 190
width = 180
height = 100
temperature input on right

node-3 Component
x = -222
y = 55
width = 180
height = 100

node-4 Controller
x = -8
width = 180
height = 100
Y varied during testing
```

Connection:

```text
connection-1
Temperature Sensor output
        →
Temperature Controller input
```

---

# Node-4 transition: Y = 24.250 → 24.260

This is the most important captured case.

## At Y = 24.250

The route was:

```text
(-5.000, 240.000)
→ (-1.250, 240.000)
→ (-1.250, 141.500)
→ (-25.250, 141.500)
→ (-25.250, 6.250)
→ (-10.000, 6.250)
→ (-10.000, -25.000)
```

The wire looked normal.

## At Y = 24.260

The route became:

```text
(-5.000, 240.000)
→ (-1.250, 240.000)
→ (-1.250, 141.510)
→ (-25.250, 141.510)
→ (-25.250, -24.990)
→ (-10.000, -24.990)
→ (-10.000, -25.000)
```

The visual result became the unwanted T/180-degree-like shape.

The change occurred when the user moved the controller down by only:

```text
0.010
```

---

# Critical diagnostic finding

In this transition, the diagnostics reported:

```text
reason: previous stable route was blocked
```

The endpoint escapes remained unchanged:

```text
Start Escape
(-45.000, 240.000) -> (-5.000, 240.000)

End Escape
(-50.000, -25.000) -> (-10.000, -25.000)
```

Therefore the transition is NOT an endpoint mismatch.

The obstacle moved.

The previous route became technically blocked.

The stability mechanism therefore had no opportunity to preserve the old route through its normal cost/tolerance comparison.

This is a key correction to the original endpoint-mismatch hypothesis.

---

# Why the old route becomes blocked

At:

```text
node-4 Y = 24.250
```

the relevant routing boundary is approximately:

```text
141.500
```

At:

```text
node-4 Y = 24.260
```

the corresponding boundary becomes approximately:

```text
141.510
```

The previous route remains at:

```text
Y = 141.500
```

Thus the old route becomes approximately:

```text
0.010
```

inside the moved routing boundary.

The router correctly classifies that previous route as blocked.

The important problem is what happens NEXT.

Instead of making only the small geometric adjustment needed to maintain the same route structure, the fresh candidate changes the lower section from:

```text
... → 141.500
    → 6.250
    → -25.000
```

to:

```text
... → 141.510
    → -24.990
    → -25.000
```

That creates the tiny:

```text
0.010
```

segment near the endpoint escape.

---

# Current interpretation

The problem is no longer best described as:

```text
stability tolerance is too small
```

It is better described as:

```text
tiny obstacle movement
    ↓
previous topology becomes technically illegal
    ↓
previous route discarded
    ↓
fresh shortest-path search
    ↓
new topology selected
    ↓
large visible elbow change
```

The fresh search is legal, but its structural change is disproportionately large compared with the physical movement.

---

# Incremental-routing hypothesis

The next experiment should test whether the previous route can be treated as a topology candidate even after becoming microscopically geometrically invalid.

Conceptually:

```text
previous route
      |
      v
old topology still recognizable?
      |
      +-- no --> normal fresh route
      |
      +-- yes
           |
           v
      adjust geometry
           |
           v
      repaired route legal?
           |
           +-- no --> normal fresh route
           |
           +-- yes
                |
                v
         preserve topology
```

This is deliberately smaller than implementing libavoid, yFiles, or another mature routing system.

The aim is only to introduce a limited continuity preference into the existing modular architecture.

---

# Important constraint

Do not automatically implement the above mechanism yet.

First establish the smallest safe definition of:

```text
topology-preserving repair
```

The repair should be:

* deterministic
* obstacle-aware
* local
* small
* understandable
* compatible with the existing route representation
* entirely visual/runtime routing state

It should not change Connection semantics.

---

# What the repair experiment should eventually test

A route should ideally be able to behave like:

```text
original:
      ┌──────────────┐
      │              │
──────┘              └──────

tiny obstacle movement:
      ┌──────────────┐
      │              │
──────┘              └──────
            ↑
     elbows shift slightly
```

rather than:

```text
original topology
       ↓
tiny geometry change
       ↓
completely different corridor
       ↓
large elbow jump
```

The exact visual diagrams are conceptual only.

---

# Required regression categories

Before moving to multi-wire routing, add regression tests covering at least:

## 1. Tiny geometric movement, same topology

Previous route remains conceptually usable.

A small obstacle/end geometry change should permit a topology-preserving repair.

Expected:

```text
same topology
different coordinates
```

## 2. Tiny movement that makes old topology impossible

The old structural route cannot legally be repaired.

Expected:

```text
fresh route
```

## 3. Endpoint-adjacent geometry movement

A small endpoint movement changes local geometry without necessarily requiring a global topology change.

Expected:

```text
same topology where legal
```

## 4. Genuine topology improvement

A different route is substantially better.

Expected:

```text
new topology accepted
```

The existing stability policy must not prevent a legitimate improvement.

## 5. Endpoint mismatch behavior

Construct an explicit case where the prepared endpoint really moves.

Verify that the endpoint-mismatch branch is understood and does not produce accidental topology churn.

## 6. Repeated movement around the threshold

Move the obstacle/component back and forth across the transition.

Look for:

```text
no unnecessary topology oscillation
```

---

# What not to do

Do NOT:

* increase `ROUTE_STABILITY_COST_TOLERANCE` just to suppress this transition
* rewrite the router
* replace the pathfinder
* move routing into the canvas
* alter canonical Connection semantics
* introduce routing state into firmware mappings
* add a second wire before this single-wire case is understood
* assume every topology change is bad
* assume every geometry change should preserve topology
* use a crude minimum-segment threshold as the first fix

A near-zero segment remains a diagnostic clue, not yet a justification for a generic minimum-length rule.

---

# Open implementation questions

## How is topology represented?

The current route is stored as a sequence of points.

There is not yet a separate explicit topology object.

One likely approach is to derive a topology signature from the route's segment directions/corridor relationships rather than introducing a large new data model.

Do not choose this until the route-repair experiment establishes what information is actually needed.

## How much movement can be repaired?

This should not become an arbitrary large tolerance.

The intended mechanism is local and geometry-driven.

## How should obstacle boundaries be handled?

The existing:

```text
GEOMETRY_EPSILON = 0.001
```

and boundary-safe collision behavior remain in force.

A repair must use the same legality model as ordinary routing.

---

# Diagnostic limitations still known

For transitions caused by a blocked previous route, the transition recorder currently reports:

```text
previous cost: n/a
```

This is because the transition is recorded before the previous-route cost is calculated.

That is a diagnostics limitation, not evidence that the cost is unknowable.

Do not confuse that with route selection behavior.

---

# Existing GUI evidence

Normal mode has demonstrated:

```text
decision: previous stable route held within tolerance
```

when the previous and candidate routes were effectively equivalent.

This proves that route stability can hold a route.

It also demonstrates that not every visible movement or elbow change is caused by the stability layer itself.

The specific node-4 transition instead reported:

```text
reason: previous stable route was blocked
```

That distinction must remain explicit.

---

# Boundary-precision investigation result

Before the geometry-epsilon fix, direct collision testing showed that microscopic positive penetration could change a segment from clear to blocked.

The behavior flipped around approximately:

```text
+1e-13
```

of penetration.

The new geometry-epsilon logic suppresses this sub-epsilon sensitivity while still identifying meaningful penetration.

A focused regression was added for horizontal and vertical cases.

This fixed one genuine numerical stability issue but did not eliminate the larger topology-change problem.

---

# Architectural classification

## REINFORCE

### Connection semantics vs visual routing

Routing behavior remains presentation/runtime state and should stay separate from canonical Connection semantics.

### Controller Resource vs visual Port

Nothing in routing requires these concepts to be collapsed.

### Hardware Definition vs Controller instance

Routing provides no reason to change this distinction.

### Firmware implementation vs machine identity

Routing provides no firmware-specific semantic identity issue.

### Modular canvas/routing structure

The existing modular structure remains appropriate.

## NEW PRINCIPLE

### Route topology vs route geometry

The current behavior provides concrete evidence that the distinction is useful and meaningful in the visual/editor layer.

## WATCH

### Incremental topology-preserving routing

The current bug strongly motivates testing this strategy, but no implementation or schema change has yet been justified.

### Persisted topology representation

It is not yet known whether topology needs explicit persistence or can remain an internal derived routing concept.

---

# Cross-workstream notes

## Planning / Architecture

The routing work supports a visual-layer distinction between:

```text
route topology
route geometry
```

It does NOT currently justify changing the canonical semantic model.

The architecture question is limited to whether this distinction eventually needs to become an explicit persisted presentation concept.

## Controller / Board Breakout

The board work should continue independently.

Do not treat:

```text
Controller Resource
Port
Connector
Pin
visual routing endpoint
```

as interchangeable concepts.

Board visualization may present them together, but the semantic distinctions remain important.

## Firmware Mapping

No routing finding currently changes firmware mapping.

A route represents visual presentation of a connection, not the firmware-specific implementation of that connection.

## Semantic Authoring

A user may move a component and therefore change visual route geometry without changing the semantic machine relationship.

That is further evidence for strong semantic/presentation separation.

---

# Startup procedure for Coder 4.4

At the beginning of Coder 4.4:

1. Establish the actual branch and worktree state locally.
2. Confirm the repository is on `wip-routing-diagnostics`.
3. Run the focused routing tests.
4. Run the full suite at the next meaningful checkpoint.
5. Keep Python/Jupyter/Data Analysis disabled for this workstream.
6. Keep new file/image uploads disabled.
7. GitHub/web inspection remains allowed.
8. Do not add a second wire yet.
9. Read this handoff before modifying routing code.

The first coding task should be investigation, not immediate implementation.

The first goal is:

> Determine the smallest topology-preserving repair that can absorb a tiny obstacle movement without forcing a fresh topology selection.

Only after that mechanism is understood should a focused implementation be proposed.

---

# Current project branch structure

The project now has intentionally separate WIP branches:

```text
main
│
├── wip-routing-diagnostics
│   └── single-wire routing / diagnostics / route continuity
│
└── wip-controller-board-breakout
    └── controller boards / ports / controller resources / board presentation
```

The board branch starts from `main`.

The routing branch remains separate until its routing milestone is coherent.

Do not merge either WIP branch merely because another chat needs a clean starting point.

---

# Merge guidance

`wip-routing-diagnostics` should eventually return to `main` after a coherent routing milestone rather than after every experiment.

A reasonable routing milestone is:

```text
single-wire topology problem understood
+
focused regression tests
+
full suite passing
+
GUI behavior validated
+
documentation updated
```

The second-wire experiment may occur before or after that milestone depending on what the single-wire investigation establishes.

The controller-board branch should merge independently when that work reaches its own coherent milestone.

---

# Final immediate objective

The immediate objective for Coder 4.4 is NOT:

```text
make the wire never move
```

It is:

```text
preserve route topology when a small geometry change can be absorbed
and permit genuine rerouting when preservation is no longer legal
or a materially different route is actually warranted.
```

That distinction should guide the next implementation experiment.
