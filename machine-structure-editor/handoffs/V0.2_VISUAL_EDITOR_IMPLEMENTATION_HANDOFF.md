# Machine Builder — O0.2 Routing Diagnostics / Route Stability Handoff

## Purpose

This handoff continues the Machine Structure Editor implementation work on the `wip-routing-diagnostics` branch.

The immediate goal is to finish stabilizing orthogonal connection routing without compromising obstacle avoidance, then checkpoint the work before merging the WIP branch.

The repository and automated tests are authoritative. Do not assume that an idea discussed in chat is implemented unless it is verified in the current working tree.

---

# Current environment

Repository:

```text
Machine-Builder/machine-structure-editor
```

Typical home path:

```text
C:\Users\Peter\Documents\GitHub\Machine-Builder\machine-structure-editor
```

Python:

```text
Python 3.14.x
```

Test command:

```powershell
python -m pytest
```

Current working branch:

```text
wip-routing-diagnostics
```

The user prefers:

* one focused implementation change at a time
* complete terminal/PowerShell patches rather than manual source surgery
* immediate pytest after meaningful changes
* no commit/push after every tiny test
* checkpoint commits after a meaningful milestone
* do not create a pull request until the implementation is actually ready

---

# Architectural boundary

Routing geometry is visual/presentation state.

It must NOT become canonical machine semantics.

The canonical machine model remains authoritative for:

* Machine
* Machine Components
* Hardware Definitions
* Ports
* Connectors/pins/terminals
* Connections
* Functions
* Capabilities
* Controller Resources
* Assignments
* Calibration
* Provenance
* semantic relationships

Visual state includes:

* node positions
* node sizes
* routing geometry
* selection
* zoom
* pan
* visual layout
* presentation-only diagnostic overlays

The routing work belongs in the visual editor.

---

# Routing diagnostics implemented

A temporary Routing Debug Mode exists.

Main files:

```text
src/machine_builder/canvas.py
src/machine_builder/canvas_ui.py
src/machine_builder/selection_inspector.py
src/machine_builder/graphics/routing_debug.py
src/machine_builder/graphics/connection.py
```

The debug overlay shows:

* physical component bounds
* routing-clearance envelopes
* fixed endpoint stubs
* endpoint escape geometry
* main routed path
* unroutable endpoint markers
* last canvas click

The debug overlay colors currently distinguish these stages visually.

Routing Debug Mode deliberately disables endpoint escape hysteresis so that diagnostics show deterministic routing geometry rather than route-history effects.

---

# Viewport repaint fix

A visual "vapor trail" / stale repaint artifact was discovered while using Routing Debug Mode.

The fix was to use:

```python
self.view.setViewportUpdateMode(
    self.view.ViewportUpdateMode.FullViewportUpdate
)
```

while Routing Debug Mode is active and restore:

```python
self.view.ViewportUpdateMode.MinimalViewportUpdate
```

when it is disabled.

This fixed the observed repaint artifact.

Do not remove this merely as an optimization without reproducing the original diagnostic problem.

---

# Relevance / obstacle-routing fixes

Two important routing bugs were found and fixed.

## 1. Relevance omission

An obstacle could be omitted from the local relevance set even though the eventual route needed to account for it.

This could allow a wire to pass through another component.

The relevance logic now expands the relevant-obstacle set iteratively so nearby obstacle chains are included.

Relevant file:

```text
src/machine_builder/graphics/connection_routing_relevance.py
```

There is an iterative helper:

```python
expand_relevant_obstacles(...)
```

It repeatedly adds obstacles whose geometry falls within the configured relevance radius of already relevant obstacles.

## 2. Candidate-route relevance / final blocking protection

`ConnectionRoutingEngine.build_route()` was strengthened further.

After an initial route is built, the route is checked against obstacles and additional relevant obstacles can be added.

The route is rebuilt when the relevance set changes.

There is also a final blocking safety check so that a returned route does not knowingly cross an obstacle.

This fixed the live-observed case where a wire could pass through a controller/component box.

The user subsequently reported:

> "I can't get the wire to go through another box any more."

That behavior should remain protected by regression tests.

---

# Narrow-corridor protection

A pathological routing case was found where the pathfinder could exploit a subpixel/sliver-sized corridor between obstacles.

The route could technically pass through a gap that was effectively unusable.

The pathfinder now contains:

```python
MIN_ROUTING_CORRIDOR = 8.0
GEOMETRY_EPSILON = 0.001
```

and horizontal/vertical corridor checks that reject segments squeezed through corridors narrower than the minimum.

This is intentionally NOT implemented by simply inflating every obstacle.

Relevant file:

```text
src/machine_builder/graphics/connection_routing_pathfinder.py
```

Regression coverage was added.

---

# Current router cost model

The pathfinder is deterministic.

Candidate coordinates are derived from:

* start/end coordinates
* obstacle edges
* obstacle edges ± clearance offsets

Candidate points are sorted.

Adjacency is deterministic.

Dijkstra routing uses a cost model approximately consisting of:

```text
segment distance
+ bend penalty
+ endpoint direction penalties
```

Current constants:

```python
ROUTING_MARGIN = 16.0
STUB_LENGTH = 40.0
ROUTING_RELEVANCE_RADIUS = 50.0
BEND_PENALTY = 80.0
ENDPOINT_DIRECTION_PENALTY = 160.0
U_TURN_MIN_SEPARATION = 32.0
ESCAPE_CLEARANCE = 1.0
```

Therefore a geometrically longer route can legitimately be selected if it has fewer bends.

Do not "fix" this merely because the selected route is not the shortest Euclidean/Manhattan-distance route.

---

# Endpoint escape hysteresis

`ConnectionGraphicsItem` already has endpoint escape history.

Current constants include:

```python
OVERLAP_ESCAPE_RESELECT_DISTANCE = 24.0
OVERLAP_ESCAPE_IMPROVEMENT_RATIO = 0.20
OVERLAP_ESCAPE_MIN_IMPROVEMENT = 24.0
```

The endpoint escape history is cleared/ignored while Routing Debug Mode is active.

This is separate from the newer main-route stability mechanism described below.

---

# Main-route stability work

A route-jitter problem was identified after obstacle avoidance was fixed.

The pathfinder can legitimately select two routes whose total costs are very close, while their visible elbows differ substantially.

That causes a small movement of a component to produce a visually large elbow jump.

A route-stability layer was added locally to `ConnectionGraphicsItem`.

It currently maintains:

```python
self._stable_route: tuple[QPointF, ...] | None = None
```

and has:

```python
ROUTE_STABILITY_COST_TOLERANCE = 4.0
```

There is a helper that:

1. accepts the new candidate route
2. compares it with the previous stable route
3. verifies that the previous route is still clear
4. calculates comparable route costs
5. retains the previous route when it is still valid and not materially worse
6. accepts a materially better route
7. resets/replaces the stable route when necessary

Important:

**Routing Debug Mode bypasses this stability preference deliberately.**

That allows diagnostics to expose raw deterministic router behavior.

Therefore stability testing must normally be performed with Debug Mode OFF.

---

# Route stability test results

Three captured GUI positions were analyzed.

## Position 1

Raw route:

```text
(-41,-130)
→ (-34.107,-130)
→ (-34.107,-14.389)
→ (-49,-14.389)
→ (-49,174)
→ (-34.107,174)
→ (-34.107,209.786)
```

Approximate:

```text
length = 376.465
bends = 5
cost = 776.465
```

## Position 2

Raw route:

```text
(-41,-130)
→ (-34.107,-130)
→ (-34.107,-22)
→ (-49,-22)
→ (-49,174)
→ (-34.107,174)
→ (-34.107,209.786)
```

Approximate:

```text
length = 376.465
bends = 5
cost = 776.465
```

The Position-1 route was NOT clear at Position 2.

Therefore the route change is mandatory and stability logic must NOT prevent it.

## Position 3

Raw route:

```text
(-41,-130)
→ (-40.308,-130)
→ (-40.308,10)
→ (-49,10)
→ (-49,174)
→ (-34.107,174)
→ (-34.107,209.786)
```

Approximate:

```text
length = 364.063
bends = 5
cost = 764.063
```

The Position-2 route was STILL clear at Position 3.

The new route is approximately:

```text
12.402
```

cost units better.

Yet the visible elbow moves substantially.

This is the important jitter case.

---

# Stability tolerance experiment

The captured Position-2 → Position-3 transition was evaluated against different stability tolerances.

Approximate behavior:

```text
4 px      → switch
8 px      → switch
10 px     → switch
12 px     → switch
12.5 px   → hold previous route
16 px     → hold previous route
20 px     → hold previous route
24 px     → hold previous route
```

Therefore:

```text
4 px
```

is too small to solve the observed visual jitter.

A value around:

```text
16 px
```

was identified as a promising candidate.

However, **16 px has not yet been committed as the final design value.**

Do not blindly change it without checking additional cases.

---

# What still needs to be done

## Step 1 — Validate stability policy

Use the current local working tree, not an older GitHub copy.

Test additional real movement cases.

We specifically want to determine:

### A. Small route improvement

Previous route remains clear.

New route is only slightly cheaper.

Expected:

```text
keep previous route
```

### B. Clearly better route

Previous route remains clear.

New route is substantially cheaper or materially simpler.

Expected:

```text
accept new route
```

### C. Previous route becomes blocked

Expected:

```text
immediately use new route
```

The stability tolerance must NEVER override obstacle safety.

### D. Repeated movement

Move a component back and forth around the transition boundary.

Expected:

```text
no rapid elbow oscillation
```

### E. Debug mode

With Routing Debug Mode ON:

```text
stable-route preference is bypassed
```

so diagnostics expose the raw route.

---

# Important design question

The route-stability threshold should be treated as a **visual hysteresis policy**, not as a router correctness parameter.

The router is responsible for finding a valid route.

The stability layer is responsible for deciding whether a small cost improvement is worth visibly changing an already-valid route.

That distinction should remain explicit in the code.

---

# Existing regression tests

`tests/test_connection_routing.py` already contains extensive routing coverage, including tests for:

* relevance near direct route
* relevance near orthogonal probe
* distant irrelevant obstacles
* distant obstacles not changing routes
* rerouting around obstacles
* routing margin
* orthogonal rerouting
* multiple obstacles
* U-turn avoidance
* endpoint scene obstacles
* fixed endpoint routes
* route cleanup
* narrow-corridor protection
* obstacle relevance chains
* candidate-route relevance

Additional stability tests were added for:

* equal route cost
* retaining an equal-cost previous route
* accepting a materially better route

The full suite reached:

```text
685 passed
```

during the route-stability implementation.

A subsequent relevance adjustment brought the working state to:

```text
686 passed
```

The next chat MUST run:

```powershell
python -m pytest
```

against the user's actual current working tree rather than relying on these historical numbers.

---

# Do not do yet

Do NOT:

* merge the WIP branch
* create a pull request
* rewrite the routing algorithm
* change bend penalty
* remove deterministic sorting
* remove narrow-corridor protection
* inflate all obstacles globally
* make routing geometry canonical
* blindly set stability tolerance to 24 px
* treat the 12.402-cost improvement as evidence that the router is broken

---

# Recommended next implementation sequence

1. Verify the user's current branch and working tree.
2. Run the full pytest suite.
3. Inspect the actual current `connection.py` and routing files.
4. Verify the route-stability implementation really exists locally.
5. Test several captured/constructed route transitions.
6. Tune `ROUTE_STABILITY_COST_TOLERANCE`.
7. Add regression coverage for the specific jitter transition.
8. Run the full suite again.
9. Do GUI testing with Debug Mode OFF.
10. Test Debug Mode separately.
11. Only after the behavior is satisfactory, commit the complete routing-diagnostics checkpoint.
12. Push the WIP branch.
13. Then tell the user that the WIP branch is ready for merge.

---

# Git checkpoint state

The user is expected to commit/push the current local WIP state before starting the next chat.

The next chat should treat that pushed commit as the baseline and inspect it directly.

The branch should remain:

```text
wip-routing-diagnostics
```

Do not merge to `main` until the routing-stability work is finished.

---

# User workflow

The user prefers the implementation chat to provide:

```text
1. What we are changing
2. Why
3. Complete PowerShell command/patch
4. Exact pytest command
5. Expected result
```

Keep changes focused.

Do not ask the user to manually edit individual lines when a terminal replacement script can safely perform the edit.

The user is comfortable running commands and reporting results.

---

# Current bottom line

The routing system has progressed substantially.

The major correctness problems have been addressed:

```text
obstacle relevance
→ obstacle-chain relevance
→ route blocking protection
→ narrow corridor protection
→ deterministic diagnostic visualization
→ viewport repaint artifact
```

The remaining issue is primarily:

```text
visual route stability / elbow jitter
```

The first captured case strongly suggests that the current:

```text
4 px
```

stability tolerance is too small.

Approximately:

```text
16 px
```

is the current candidate for further testing, but it is NOT yet a finalized architectural decision.

The next chat should continue from here rather than restarting routing research.
