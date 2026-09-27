# Routing Stability Investigation Handoff — Coder 4.4

Date: 2026-09-24

## Current checkpoint

Branch:

`wip-routing-diagnostics`

Current reported repository state:

* working tree clean
* branch up to date with `origin/wip-routing-diagnostics`
* focused connection-routing tests: 38 passed
* full test suite: 695 passed

The latest local commit attempt reported:

`nothing to commit, working tree clean`

Therefore the current branch already contains the latest committed routing state.

A Windows pytest cleanup `PermissionError` occurred after the full suite reported all tests passing. This is treated as a post-test cleanup warning, not a test failure.

## Current routing problem

The remaining visual problem is an abrupt wire/elbow topology change when a component is moved by a very small amount through a tight clearance.

The observed visual result can become a 180-degree / overlapping T-like shape.

The active investigation is intentionally limited to a single connection.

Do not add a second wire until the single-wire behavior is understood.

## Current production routing modules

The production router remains split into focused modules:

```text
src/machine_builder/graphics/
    connection.py
    connection_routing.py
    connection_routing_pathfinder.py
    connection_routing_relevance.py
    connection_routing_endpoint.py
```

Do not refactor these modules merely because the routing test file is large.

The canvas remains modular, with focused modules including:

```text
canvas_ui.py
canvas_editing.py
canvas_palette.py
canvas_selection.py
canvas_interaction.py
canvas_scene.py
canvas.py
```

`canvas.py` remains a coordinator.

## Current routing constants

Known values currently include:

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

Do not change these values merely to suppress the observed transition.

The stability tolerance remains experimental and is not a final architectural decision.

## Important geometry-boundary fix already present

The routing pathfinder's segment collision test was updated to use `GEOMETRY_EPSILON` when testing whether a horizontal or vertical segment lies inside an obstacle rectangle.

The purpose is to prevent microscopic floating-point penetration from turning an effectively boundary-aligned route into a blocked route.

Regression coverage was added for:

* exact boundary contact
* sub-epsilon penetration
* meaningful penetration

The routing tests and full suite passed after this change.

This change should not be reverted merely because other routing behavior remains under investigation.

## Stability behavior

The intended stability behavior remains:

* hold a previous valid route when the new candidate is only slightly better
* switch when improvement is meaningful
* switch immediately when the previous route is genuinely invalid
* avoid rapid oscillation between near-tie routes

Routing Debug Mode bypasses route-stability history and is used to observe raw route selection.

## Critical observed transition at node-4 Y = 24.250 -> 24.260

Saved test machine:

`machine-structure-editor/wiring test machines/4 parts.machine.json`

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
Y varied during the test
```

Connection:

```text
connection-1
Temperature Sensor output -> Temperature Controller input
```

At:

```text
node-4 Y = 24.250
```

the route was:

```text
(-5.000, 240.000)
-> (-1.250, 240.000)
-> (-1.250, 141.500)
-> (-25.250, 141.500)
-> (-25.250, 6.250)
-> (-10.000, 6.250)
-> (-10.000, -25.000)
```

Moving node-4 downward by only 0.010 px to:

```text
node-4 Y = 24.260
```

produced:

```text
(-5.000, 240.000)
-> (-1.250, 240.000)
-> (-1.250, 141.510)
-> (-25.250, 141.510)
-> (-25.250, -24.990)
-> (-10.000, -24.990)
-> (-10.000, -25.000)
```

The resulting visual geometry is the unwanted T-like / overlapping 180-degree appearance.

The diagnostic reason was:

`previous stable route was blocked`

The candidate and selected route costs were both:

`868.000`

The current normal-mode stability tolerance therefore did not cause this transition.

## Important endpoint finding

The current implementation performs this decision sequence inside `_select_stable_route()`:

1. candidate route is calculated
2. candidate cost is calculated
3. debug mode may bypass stability
4. previous route is checked
5. previous route length is checked
6. previous route endpoint coordinates are compared with the current prepared start/end
7. previous route is checked for collision with current obstacles
8. only then is previous cost compared with candidate cost and stability tolerance

The endpoint-mismatch branch is:

```text
if previous[0] != start or previous[-1] != end:
    ...
    reason = "previous stable route endpoint mismatch"
    ...
    return candidate
```

So the user's hypothesis that a prepared-endpoint mismatch can bypass the normal hysteresis comparison is valid as a property of the current implementation.

However, the observed node-4 transition above does NOT exercise that condition.

In the captured transition:

```text
Start Escape:
(-45.000, 240.000) -> (-5.000, 240.000)

End Escape:
(-50.000, -25.000) -> (-10.000, -25.000)
```

The endpoint escapes did not move.

Therefore:

`endpoint mismatch` is NOT the cause of the node-4 Y = 24.250 -> 24.260 transition.

The actual cause of that transition is that the previous route became blocked according to the current obstacle geometry.

## Why the previous route becomes blocked

Node-4's expanded routing boundary moves with its Y coordinate.

At:

```text
Y = 24.250
```

the relevant lower boundary is:

```text
141.500
```

At:

```text
Y = 24.260
```

the relevant lower boundary is:

```text
141.510
```

The old route's upper horizontal is at:

```text
141.500
```

Therefore, after the movement, the old route is approximately:

```text
0.010 px
```

inside the expanded obstacle.

The router consequently rejects the old route before stability/cost hysteresis can preserve it.

## Important incremental-routing observation

This exposes a more useful routing question than simply increasing the stability tolerance.

The old route and the new candidate are not unrelated shortest paths.

The old route could plausibly be viewed as the same basic topology with its upper horizontal moved from:

```text
141.500
```

to:

```text
141.510
```

while much of the existing corridor structure remains unchanged.

The fresh candidate instead changes the lower portion dramatically:

```text
old:
141.500
-> 6.250
-> -25.000

new:
141.510
-> -24.990
-> -25.000
```

This creates the tiny:

```text
0.010 px
```

segment near the endpoint escape.

This is evidence supporting investigation of a small topology-preserving repair step before falling back to a completely fresh route.

This is an investigation target, not yet an implementation decision.

## Revised investigation goal

Distinguish two concepts:

### Route geometry

The route retains the same basic topology/corridor sequence while coordinates move slightly to remain legal.

### Route topology

The route changes which sides/corridors/elbows it uses.

The undesirable behavior appears to be a topology change triggered by a tiny geometric movement.

The next implementation experiment should therefore ask:

Can the existing route topology be preserved with small geometric adjustments when the previous route becomes microscopically illegal?

Only if the old topology cannot be repaired legally should a full new route be selected.

## Next investigation

Do not tune:

`ROUTE_STABILITY_COST_TOLERANCE`

Do not add another wire.

Do not replace the router.

Do not perform a broad architecture rewrite.

First inspect the current route-selection and route-normalization behavior in enough detail to determine the smallest topology-preserving mechanism.

A promising conceptual location is between:

```text
previous route exists
```

and:

```text
previous stable route was blocked
```

Possible future shape:

```text
previous route
    |
    +-- endpoint mismatch? ---- yes --> normal new candidate
    |
    +-- malformed? ------------ yes --> normal new candidate
    |
    +-- currently clear? ------- yes --> normal stability comparison
    |
    +-- blocked
          |
          +-- can existing topology be repaired slightly?
                  |
                  +-- yes --> compare/use repaired topology
                  |
                  +-- no --> normal fresh candidate
```

The repair mechanism must be small, deterministic, obstacle-aware, and limited to presentation/runtime routing.

It should not enter the canonical machine model.

## Required regression coverage before moving to multi-wire

At minimum, establish tests for:

1. A tiny obstacle movement that can be absorbed by preserving the existing topology.
2. A tiny movement that genuinely makes the old topology impossible.
3. A route with a small endpoint-adjacent geometric change that does not require a topology change.
4. A genuine topology-improvement case that should still permit a new route.
5. Endpoint movement where the prepared endpoint really does change, so the endpoint-mismatch branch is explicitly understood and tested.

The tests should verify both:

* route point geometry
* route topology / segment-direction sequence

Do not test only total route cost.

## Current diagnostic interpretation

Captured normal-mode evidence:

```text
decision: previous stable route held within tolerance
```

occurs in positions where previous and candidate routes can be identical.

This shows that the stability layer is capable of holding the route and is not itself responsible for every elbow movement.

Captured transition evidence:

```text
reason: previous stable route was blocked
```

is the important trigger for the current node-4 experiment.

The current diagnostic recorder reports previous cost as `n/a` for blocked-route transitions because the transition is recorded before calculating previous-route cost.

That is only a diagnostic limitation.

## Deferred maintenance

Do not mix these into the active routing behavior experiment unless necessary:

* duplicate routing-debug definitions in `selection_inspector.py`
* stale V0.2 planning text in `IMPLEMENTATION_ROADMAP.md`
* refresh of `V0.2_VISUAL_EDITOR_IMPLEMENTATION_HANDOFF.md`

These remain maintenance/documentation items.

## Tool-use constraint for Coder 4.4

For the 4.4 routing experiment:

* do not use Python
* do not use Jupyter
* do not use ChatGPT Data Analysis
* use local PowerShell commands and user-reported output
* use pytest locally
* use GUI testing locally
* GitHub/web inspection is explicitly allowed

The purpose is to isolate whether Python/Data Analysis usage is contributing to the cross-chat usage pauses observed by the developer.

## Startup for the next coder chat

At the beginning of the next coder chat:

1. Read `Machine-Builder/CODER_CHAT_WORKFLOW.md`.
2. Read `machine-structure-editor/handoffs/V0.2_VISUAL_EDITOR_IMPLEMENTATION_HANDOFF.md`.
3. Read `machine-structure-editor/IMPLEMENTATION_ROADMAP.md`.
4. Read this 4.4 routing handoff.
5. Establish actual local branch, commit, and status.
6. Run focused routing tests.
7. Run the full suite at the appropriate checkpoint.
8. Treat the user's local results as authoritative.

Do not reconstruct the entire routing history from previous chat messages.

The immediate goal is a small, evidence-driven experiment in incremental route continuity for the existing single-wire case.
