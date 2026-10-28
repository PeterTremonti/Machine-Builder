<!-- MB4-PROTECTED-SEGMENT-INDEX-VALIDATION-20261028 -->

## Authoritative checkpoint - 2026-10-28: protected-segment index production validation

Prepared: 2026-10-28 EDT | Message ID: MB-20261028-ROUTING-PROTECTED-INDEX-VALIDATION-RESULTS-01
Relationship: Implements the results requested by Planning authorization MB-20261027-ROUTING-PROTECTED-INDEX-PROD-AUTH-13 and standing documentation authority MB-20261028-WORKSTREAM-HANDOFF-AUTONOMY-01. This checkpoint supersedes older "pending implementation" and test-count statements as current status; historical checkpoints below are retained.

### Implementation scope and exact diff

The orientation-aware protected-segment candidate index was implemented in the two paths authorized by Planning:
- `machine-structure-editor/src/machine_builder/graphics/connection_routing_pathfinder.py`
- `machine-structure-editor/tests/test_connection_routing.py`

Against the approved baseline `cb65c45dd768dd9c3fd56865c2a74c07f73d4f53`, the current diff summary is **428 insertions and 2 deletions**: 153 insertions / 2 deletions in the pathfinder and 275 added lines in the routing test file. The index retrieves a conservative candidate set and still invokes the original exact separation predicate for those candidates. Existing lane generation, route cost logic, endpoint behavior, route ordering, retry/fallback behavior, and refresh cadence were not intentionally changed.

### Verified automated results

- Index-specific routing regressions: 2 passed.
- Complete `test_connection_routing.py`: 65 passed.
- Functional-interface test file: 18 passed in 5.06 seconds.
- Full project `.venv` suite, using `machine-structure-editor\.venv\Scripts\python.exe` (Python 3.14.7): **890 passed in 10.30 seconds**.
- Syntax validation passed for both changed code files.
- Final whitespace check for the two implementation/test diffs passed.

### Differential and geometry verification

A fresh disposable baseline and candidate used published source baseline `cb65c45dd768dd9c3fd56865c2a74c07f73d4f53` and the verified J9 fixture SHA-256 `3E6FB97FBBFC0C9FB2B4968448846A17560370A504F828566F11A652EDF68F82`. The committed fixture in the archive has a different hash; the matching fixture was copied from the prior validated disposable experiment. The pre-existing shared diagnostic fixture was not edited by this task.

Production-candidate differential check:
- Routing-edge decisions checked: **289,623**
- Differential mismatches: **0**
- Full-scan entries presented: 4,178,871
- Indexed candidate entries presented: 36,145
- Candidate-entry reduction: **99.14%**
- Index builds: 11
- Route builds / grid searches: 7 / 11
- Route-clear checks / failures: 31 / 4

### Controlled performance results

Three baseline/candidate pairs were run with the same automatic invocation trace, fixed `PYTHONHASHSEED=0`, differential checking disabled, and equivalent fixture/refresh operations. All three pairs passed exact route geometry, pathfinder input/result, grid-search input/result, scene-state, and operation-count comparisons.

Baseline refresh samples: 17,814.051 ms; 18,303.513 ms; 18,120.274 ms.
Candidate refresh samples: 1,891.339 ms; 1,862.801 ms; 1,885.272 ms.

- Baseline median: **18,120.27 ms**
- Candidate median: **1,885.27 ms**
- Baseline spread (max - min): **489.46 ms**
- Candidate spread: **28.54 ms**
- Median reduction: **89.60%**
- Speedup: **9.61x**

The earlier differential-enabled run took approximately 46.3 seconds because it deliberately executed extra full-scan checks; that timing is not part of the performance benchmark.

### Route-repeatability caveat

A manually triggered refresh pair once showed a 0.5-unit difference at `connection-1` point index 3 (Y: `-1328.2648075282284` versus `-1328.7648075282284`). This was not concealed or reported as a pass. Startup geometry matched, and subsequent automatic, fixed-seed traces and all three controlled timing pairs matched exactly. The 0.5-unit difference was **not reproduced** under those controlled runs; its original cause remains unproven. Retain this as a repeatability observation rather than claiming that every possible interaction sequence is proven equivalent.

### Repository and publication state

Final safety audit before documentation publication:
- Branch `main`; local `HEAD`, tracking `origin/main`, and live `origin/main` all at `cb65c45dd768dd9c3fd56865c2a74c07f73d4f53`.
- Shared index empty.
- Only task-owned implementation/test paths are the pathfinder and routing test file.
- Preserved other local work: #3 controller-board handoff; the other two #4-owned handoff/prompt documents until this documentation-only publication; the user-owned J9 diagnostic fixture; and the untracked Board-owned stepper-terminal test.
- No implementation commit, push, or publication is authorized by this checkpoint. Only the two #4-owned documentation paths are covered by the standing handoff-autonomy authority.

### Remaining editor acceptance blockers

- **Editor remains NOT ACCEPTED.**
- **In-cone wire visibility remains unresolved:** the user previously reported that wire lines are not visible inside the cone. The index timing improvement does not prove that visual defect is fixed.
- **Focus after deletion / undo / redo remains NOT TESTED** for this post-index state.
- GUI responsiveness has improved substantially in the controlled refresh measurement, but fresh hands-on GUI acceptance after the performance change has not been recorded. Do not equate benchmark success with GUI acceptance.
- The manual 0.5-unit route-repeatability observation above remains documented.

### Next action

Finish and publish this dedicated documentation-only checkpoint by staging and committing only:
- `machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`
- `machine-structure-editor/handoffs/04_ROUTING_STABILITY_REPLACEMENT_PROMPT.md`

Keep the pathfinder and routing test unstaged. After documentation publication, continue with fresh GUI verification for in-cone wire visibility and post-delete focus. The implementation files remain subject to a separate Planning publication decision.

---

## Fresh GUI acceptance observations — 2026-10-26

Source: user's direct manual observations of the editor. No screenshots were supplied in this report.

- **Wire crossing / shared cone tip — PASS for geometry.** The wires no longer appear to pass through the cone in the previous strange way. After fanning out along the route, they appear to align at the shared point, based on the user's visual check.
- **Wire visibility inside the cone — FAIL / regression to investigate.** Wire lines are no longer visible inside the cone, unlike the prior behavior. The visible endpoint alignment does not establish that the in-cone segment is rendered correctly.
- **Individual wire selection — PASS.** The user can now select any/all wires individually fairly easily.
- **Breakout title and part-label overlap — PASS.** The titles in breakout boxes and the parts themselves are visible without the previous overlap/interference.
- **Focus and selection after deleting connections — NOT TESTED.** No fresh result was reported for deletion, undo/redo, or focus restoration.
- **Overall GUI responsiveness — FAIL / blocking usability issue.** The editor has become so laggy that it is too difficult to use. Reproduction timing, workload, and screenshots have not yet been captured.

**Acceptance disposition: NOT ACCEPTED YET.** The geometric routing, picking, and label layout are reported as improved, but severe responsiveness degradation and missing in-cone wire visibility remain. Post-delete focus behavior is still unverified. Do not infer acceptance from the 888 passing automated tests.

**Next decision needed from Planning:** prioritize a bounded performance diagnosis and the in-cone rendering regression. Separately complete the delete/focus check when the GUI is responsive enough to test. Make no implementation change or publication from this acceptance pass without Planning's next scope decision.

The accepted published baseline remains `cb65c45dd768dd9c3fd56865c2a74c07f73d4f53`. Both publication commits remain published; do not rewrite history or force-push. The missing separately recorded Planning authorization for the earlier 16-file publication remains documented as a process deviation.

The three excluded paths remain outside #4 scope and must remain untouched: #3's controller-board handoff, the Board-owned stepper-terminal test, and the user-owned Maestro diagnostic fixture. This checkpoint is local documentation only; do not stage, commit, or push it during the acceptance pass.

---
## Authoritative checkpoint — 2026-10-26: Planning GUI acceptance follow-up

Prepared: 2026-10-26 21:51 EDT | Planning message: MB-20261026-ROUTING-GUI-ACCEPTANCE-05
Relationship: Authoritative post-publication status; supersedes earlier pending-publication statements without deleting historical checkpoints.

## Published baseline and commits

- Accepted baseline: `cb65c45dd768dd9c3fd56865c2a74c07f73d4f53`.
- Routing/fan-out commit: `2863e2ce3077bd5fff43a359ca19e2a014746952` — `fix: stabilize functional connection fan-out routing`.
- Remaining editor-integration commit: `cb65c45dd768dd9c3fd56865c2a74c07f73d4f53` — `fix: complete routing stability editor integration`.
- Both pushes succeeded normally. After the second push, local `HEAD`, `origin/main`, and live remote `main` agreed at `cb65c45dd768dd9c3fd56865c2a74c07f73d4f53`.
- Reported full-suite results: 888 passed in 19.87 seconds before the first publication; 888 passed in 19.30 seconds before the second publication.

## Publication authorization reconciliation

- Planning authorization `MB-20261026-FANOUT-FINAL-PUBLISH-AUTH-04` explicitly covered the seven-file routing/fan-out patch and its conditional publication.
- The subsequent 16-file #4 batch was pushed after the user clarified that the remaining #4-owned files should be committed together. This conversation contains no separate recorded explicit Planning authorization for that broader batch.
- Record this as a process deviation. Both commits remain published; do not rewrite history or force-push. No further publication is authorized by this checkpoint.

## Fresh manual GUI acceptance — NOT TESTED

The GUI was not directly accessible to this assistant. No manual outcomes are claimed and no screenshots were captured in this conversation. Automated tests do not count as GUI acceptance.

1. **Cone crossing — NOT TESTED.** Open the diagnostic machine without saving over its user-owned fixture. Zoom into the connector cone and the black wire. Follow the visible wire path to determine whether it passes through the cone instead of meeting the intended anchor. Capture a zoomed screenshot and record PASS/FAIL with the wire and endpoint identified.
2. **Individual wire selection — NOT TESTED.** With multiple close wires visible, click each wire separately at a clear mid-segment and near its endpoint. Record which connection becomes selected each time; repeat for the black and red wires. Capture a screenshot if a click selects the wrong connection or cannot select the intended one.
3. **Breakout versus Maestro title — NOT TESTED.** Fit the board and connector breakout in view. Check whether breakout artwork overlaps or obscures the Maestro board name. Capture a screenshot showing the board title, outline, and breakout at once.
4. **Focus after deleting connections — NOT TESTED.** Record the current connector-focus mode and selected connection. Delete one connection, then test deleting several; observe focus/selection after each deletion. Repeat with undo/redo and, if feasible, reopen a disposable copy to check persistence. Do not overwrite the user-owned fixture. Record unexpected fallback to a broad Functional-interfaces selection or lost focus.

For every GUI item, report PASS, FAIL, or NOT TESTED based on a fresh observation. If a defect is found, record reproduction steps and screenshot evidence where useful, then request Planning direction before implementation changes or publication.

## Ownership and local state

- Preserve the three remaining excluded paths: `handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md` (#3); `tests/test_stepper_motor_terminal_profile.py` (Board); and `wiring test machines/Maestro and 4 port motor 4 wires J9 contact view.machine.json` (user-owned diagnostic fixture).
- No further #4 implementation files were reported unpublished after the 16-file commit. The documentation changes made for this checkpoint are local only and must remain unstaged and uncommitted.

Historical checkpoint entries follow unchanged. If they describe an earlier baseline, publication as pending, or a prior authorization boundary, treat that statement as historical rather than current.

## Current checkpoint — 2026-10-26: post-routing publication

This checkpoint supersedes earlier statements below that the routing publication had not occurred or that the previous baseline was still current.

- Published commit: `2863e2ce3077bd5fff43a359ca19e2a014746952` — `fix: stabilize functional connection fan-out routing`.
- Verified after push: local `HEAD`, `origin/main`, and live remote `main` all matched that commit.
- Validation before publication: all seven staged Python files compiled; the complete test suite passed, **888 passed in 19.87 seconds**.
- The published commit contains the seven authorized routing/fan-out paths. Three of those paths still have separate working-tree edits; those edits remain part of the unpublished work.
- Remaining shared-checkout status: 19 paths. The intended next batch is the 17 #4-owned paths; preserve `handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md` and `tests/test_stepper_motor_terminal_profile.py` as #3-owned.
- The remaining 17-file batch is not yet staged, committed, or pushed. Before publication, verify exact path scope, whitespace, staged syntax, and the full test suite against the final candidate.
# Machine Builder — Routing Stability Workstream Handoff

## Recovery instructions

This file is the **living recovery handoff** for the Routing / Diagnostics workstream.

It is not a replacement for the older historical investigation records. The detailed historical records remain useful when a replacement chat needs deeper background:

```text
docs/historical/routing/ROUTING_STABILITY_INVESTIGATION_HANDOFF_4.3.md
docs/historical/routing/ROUTING_STABILITY_INVESTIGATION_HANDOFF_4.4.md

Follow `CHAT_WORKFLOW.md` §17 for the universal replacement-chat recovery procedure. This file is the living Routing / Diagnostics workstream handoff required by that procedure.

After completing that procedure, inspect the current Routing source and relevant Routing tests as needed for the active Next Action. Current source and actual reported test results are authoritative over historical checkpoint text.

Do not assume that an old branch, worktree, commit description, or historical diagnosis still matches the current implementation.

The current Machine Builder workflow uses:

main
single checkout
shared implementation work

Routing and Controller / Board remain separate implementation responsibility areas, but they coordinate through the shared main branch and project-level architecture/research process.

What we've done so far
Checkpoint 1 — Initial routing-stability investigation

Purpose

Investigate a reproducible routing problem in which very small component movements could produce disproportionately large changes in an orthogonal wire route.

The investigation established the need to distinguish:

route geometry

from:

route topology

Route geometry includes exact segment coordinates, elbow positions, lengths, and endpoint-adjacent movement.

Route topology includes corridor choice, side choice, bend sequence, and the structural organization of the route.

The initial working hypothesis was that the router could sometimes discard an existing route and select a substantially different topology when only a small geometric adjustment should have been necessary.

Files involved

machine-structure-editor/src/machine_builder/graphics/connection.py
machine-structure-editor/src/machine_builder/graphics/connection_routing.py
machine-structure-editor/src/machine_builder/graphics/connection_routing_pathfinder.py
machine-structure-editor/src/machine_builder/graphics/connection_routing_relevance.py
machine-structure-editor/src/machine_builder/graphics/connection_routing_endpoint.py
machine-structure-editor/tests/test_connection_routing.py

These are the primary routing implementation and routing-test files used by the workstream.

What changed

Routing behavior was separated into clearer stages involving endpoint preparation, relevant-obstacle collection, pathfinding, route cleanup, and route-stability selection.

Diagnostics were added so the routing system could expose the major intermediate stages rather than only the final rendered path.

What was learned

The important problem was not simply "the router picked a different line." In several cases, the more useful distinction was:

same topology, changed geometry

versus:

different topology

This distinction became the basis for later stability and transition diagnostics.

Checkpoint 2 — Route stability / hysteresis work

Purpose

Reduce unnecessary route popping or twitching when component geometry changes only slightly.

Files changed in this phase

machine-structure-editor/src/machine_builder/graphics/connection.py
machine-structure-editor/src/machine_builder/graphics/connection_routing_pathfinder.py
machine-structure-editor/tests/test_connection_routing.py

What changed

Route selection gained explicit stability behavior intended to preserve an existing route when a new candidate did not provide enough improvement to justify changing it.

The implementation introduced a route-stability tolerance and logic for comparing the previous stable route with the newly generated candidate.

The current stability tolerance is:

ROUTE_STABILITY_COST_TOLERANCE = 16.0

What was learned

A cost tolerance can suppress some unnecessary topology changes, but it cannot solve cases where the previous route is no longer legal.

This led to a crucial distinction between:

candidate is different but previous route is still legal

and:

previous route is blocked, so stability cannot preserve it

Stability logic therefore cannot be treated as a universal solution for all route changes.

Checkpoint 3 — Precision / geometry movement investigation

Purpose

Investigate cases where tiny coordinate changes appeared to trigger larger-than-expected routing transitions.

One important case involved a movement of approximately:

0.010 units

The investigation examined whether the resulting transition represented ordinary geometric adjustment or a genuine topology change.

Files involved

machine-structure-editor/src/machine_builder/graphics/connection.py
machine-structure-editor/src/machine_builder/graphics/connection_routing_pathfinder.py
machine-structure-editor/tests/test_connection_routing.py

What changed

Routing diagnostics were expanded so that the previous route, candidate route, selected route, costs, stability decision, and transition information could be inspected directly.

What was learned

The transition diagnostics showed that the router could distinguish a small geometry movement from a genuine topology change, but that the triggering condition could still be difficult to understand without explicit reporting.

This reinforced the need to record the reason for a route transition instead of treating every candidate change as equivalent.

Checkpoint 4 — Obstacle-boundary geometry epsilon

Purpose

Investigate precision-sensitive behavior around obstacle boundaries and near-equal coordinates.

Files changed

machine-structure-editor/src/machine_builder/graphics/connection_routing_pathfinder.py
machine-structure-editor/tests/test_connection_routing.py

What changed

Collision and boundary-sensitive routing calculations were adjusted to use the routing geometry epsilon consistently rather than relying on exact floating-point equality.

What was learned

The issue was not safely solved by simply changing route-stability tolerance.

The boundary calculations themselves needed to distinguish meaningful geometry from insignificant floating-point differences.

This change was retained because the resulting routing tests passed and it addressed geometry correctness directly.

Do not revert the geometry-epsilon handling as a way of experimenting with route stability.

Checkpoint 5 — Previous-route transition diagnostics

Purpose

Determine why the stability selector changes away from a previously stable route.

Files changed

machine-structure-editor/src/machine_builder/graphics/connection.py
machine-structure-editor/tests/test_connection_routing.py

What changed

The routing diagnostics were expanded to expose:

previous stable route
candidate route
selected route
previous cost
candidate cost
selected cost
candidate improvement
transition reason
previous route at transition
candidate route at transition
selected route at transition
transition costs

The diagnostics also preserve endpoint escape geometry separately.

What was learned

Two particularly important transition classes emerged:

endpoint mismatch

and:

previous stable route was blocked

These are materially different.

An endpoint mismatch indicates that a previous route no longer corresponds to the current route endpoints.

A previous-route-blocked transition means the old topology may otherwise be comparable, but its actual geometry is no longer legal.

For the known pathology, the endpoint escapes remained unchanged while the previous main route became blocked. Therefore that particular transition was not an endpoint mismatch.

Checkpoint 6 — Deterministic visibility-grid ordering

Purpose

Investigate a smaller topology-flapping case where tiny coordinate changes caused the raw pathfinder to alternate between route topologies.

Files changed

machine-structure-editor/src/machine_builder/graphics/connection_routing_pathfinder.py
machine-structure-editor/tests/test_connection_routing.py

What changed

Visibility-grid coordinate iteration was made deterministic by using sorted coordinate ordering.

Conceptually:

for x in sorted(coordinates_x):
    for y in sorted(coordinates_y):

What was learned

This removed one observed 0.001-unit topology oscillation.

The result was important because it demonstrated that at least some route flapping was caused by deterministic search ordering rather than route-stability hysteresis.

This approach was retained.

It does not prove that all remaining topology changes are search-order artifacts.

Checkpoint 7 — Topology-preserving route repair experiment

Purpose

Test whether a small movement could be handled by preserving route structure and adjusting geometry rather than allowing an entirely different route topology.

Files changed

machine-structure-editor/src/machine_builder/graphics/connection.py
machine-structure-editor/src/machine_builder/graphics/connection_routing_pathfinder.py
machine-structure-editor/tests/test_connection_routing.py

What changed

The routing logic was extended to attempt continuity-preserving geometry behavior in conjunction with the existing stability mechanism.

What was learned

This removed some visible popping/twitching but produced an undesirable geometry in the known case, including a T-like or overly sticky arrangement.

The experiment demonstrated that:

preserving topology

is not sufficient by itself.

The geometry chosen while preserving topology also has to remain visually and geometrically sensible.

This approach was therefore not adopted as the final routing solution in its experimental form.

Checkpoint 8 — Minimum route segment separation identified

Purpose

Find a more general concept for the observed near-coincident parallel segments.

The workstream initially considered endpoint-specific approaches such as minimum endpoint approach distance or U-turn separation.

Research instead supported treating the issue as a general minimum route segment separation problem.

The useful conceptual terminology became:

Minimum Route Segment Separation

with the important distinction that this is about the perpendicular spacing between eligible parallel route segments whose projections overlap.

The predicate deliberately ignores:

perpendicular segments
non-overlapping parallel segments
ordinary direct adjacency where segments meet at a shared endpoint

Files changed

machine-structure-editor/src/machine_builder/graphics/connection_routing_pathfinder.py
machine-structure-editor/tests/test_connection_routing.py

Commit

3ce40bb Add route segment separation predicate

Tests

52 focused routing tests passed

What was learned

The original pathology was not best described as an endpoint approach problem.

It was better described as:

two eligible parallel route segments whose spacing becomes effectively zero

This introduced a more general routing geometry concept without requiring an architectural rewrite.

Checkpoint 9 — Hard protected-segment separation experiment

Purpose

Test whether an explicit minimum spacing rule could eliminate the original approximately 0.001-unit near-coincident geometry.

The initial controlled experiment used an experimental value of:

8 px

The endpoint escape segments were treated as protected geometry for the main pathfinder.

Files changed

machine-structure-editor/src/machine_builder/graphics/connection.py
machine-structure-editor/src/machine_builder/graphics/connection_routing.py
machine-structure-editor/src/machine_builder/graphics/connection_routing_pathfinder.py

The focused routing tests remained in:

machine-structure-editor/tests/test_connection_routing.py

Commit

ef57ad8 Integrate route segment separation

What changed

Protected endpoint segments were threaded through the routing stack.

The pathfinder received:

protected_segments
minimum_segment_separation

and rejected candidate edges that violated the protected spacing requirement.

The visibility grid was also given coordinates at the requested protected-segment offsets so that legal alternate geometry remained available.

The current experimental constant is:

MIN_ROUTE_SEGMENT_SEPARATION = 8.0

Tests

52 focused routing tests passed
730 full-suite tests passed

What was learned

The hard constraint successfully eliminated the original near-coincident segment geometry.

For example, the known end geometry became approximately:

main route:
(-25.250, -17.000) -> (-10.000, -17.000)

end escape:
(-50.000, -25.000) -> (-10.000, -25.000)

giving approximately:

8.000 units

of separation.

However, the hard requirement also caused the pathfinder to create visible U-turns, jogs, or loops to satisfy the requested spacing.

At another tested position, the route included:

(-5.000, 240.000)
-> (-1.250, 240.000)
-> (-1.250, 231.999)
-> (-25.250, 231.999)

The 231.999 segment was approximately 8 units from the protected start-escape segment at y = 240.

The lower side showed analogous behavior, with the router producing small U-turn geometry and eventually a loop as the available geometry changed.

This was a useful experiment because it demonstrated that the spacing constraint itself works, but that enforcing preferred spacing as a hard pathfinding rule can force undesirable topology or local geometry.

The 8 px value is therefore an experiment, not a project-level design decision.

Checkpoint 10 — Latest research result from Planning / Research (#2)

Purpose

Determine whether the spacing problem belongs primarily in pathfinding legality or in a later route-geometry quality stage.

Research conclusion

Established orthogonal-routing systems provide precedent for distinguishing:

hard geometric legality

from:

preferred geometric quality

A useful conceptual pipeline is:

route/topology generation
        ↓
route geometry
        ↓
preferred spacing / geometric nudging
        ↓
final visual route

The research specifically supports these observations:

mature routing systems may treat requested edge distance as a preference rather than an unconditional legality rule
yFiles provides a minimum-distance concept and can relax the requested distance when there is insufficient room
libavoid and related systems use post-route nudging/separation concepts
topology-preserving geometry repair is a useful pattern
same-connection segments and stubs may require different treatment from unrelated edges

What was learned

The current hard-8 px experiment is valuable as a baseline, but the desired spacing may belong in a geometric repair/nudging stage rather than being imposed unconditionally during pathfinding.

The recommended next experiment is therefore:

existing legal route
        ↓
identify nearby parallel same-connection segments/stubs
        ↓
detect insufficient preferred separation
        ↓
attempt geometry-only adjustment
        ↓
preserve existing segment/bend topology
        ↓
relax the preferred spacing when necessary

The repair should not create new bends merely to satisfy preferred visual spacing.

Topology-changing rerouting should remain available when the existing topology cannot remain legal or otherwise cannot be repaired acceptably.

Current state
What currently works

The routing workstream currently has:

explicit routing diagnostics
previous/candidate/selected route reporting
route transition reasons and cost information
endpoint escape diagnostics
route-stability / hysteresis behavior
deterministic visibility-grid ordering
geometry-epsilon handling around obstacle boundaries
distinction between endpoint mismatch and previous-route-blocked transitions
tested minimum parallel-segment separation geometry
protected-segment routing support
a hard 8 px protected-segment experiment retained as a historical baseline
generic controller-owned SemanticPort projection through project_controller_ports()
VisualPort.semantic_reference resolution for controller visual ports
controller visual ports participating in the existing connection-authoring path
a tested topology-preserving preferred-spacing geometry-only repair experiment for the known single-connection pathology
a 4.0 scene-unit experimental preferred-spacing target kept separate from pathfinding legality
What is currently being investigated

The narrow preferred-spacing geometry-only repair experiment is now implemented and focused-tested for the known single-connection pathology.

The remaining investigation is how broadly this repair strategy should apply beyond the proven case.

The working question is:

When a legal route contains nearby parallel same-connection geometry, how robustly can existing geometry be repaired toward a preferred visual spacing without creating unnecessary new bends or changing route topology?

The immediate follow-up should remain narrow and should emphasize visual validation plus constrained cases rather than global multi-wire optimization.
What has not yet been solved

The workstream has not yet established:

how preferred-spacing repair should generalize beyond the known single-connection case
how preferred-spacing relaxation should behave across constrained channels beyond the current fallback behavior
how geometry-only repair should coordinate movement of several related interior segments
when a route should be repaired versus discarded and fully rerouted under broader conditions
how same-connection geometry should eventually interact with nearby unrelated connections
whether route topology should eventually become explicit persistent presentation state

The current hard 8 px implementation should not be mistaken for the final answer to these questions.

Important files
Routing presentation / connection behavior
machine-structure-editor/src/machine_builder/graphics/connection.py

Owns the rendered connection behavior and route-selection/stability integration.

Important responsibilities include:

endpoint escape preparation
route selection
route-stability decisions
routing diagnostics
visual connection construction
current protected-segment integration
Routing engine
machine-structure-editor/src/machine_builder/graphics/connection_routing.py

Coordinates the routing process above the raw pathfinder.

Important responsibilities include:

routing constants
relevant-obstacle collection
endpoint-prepared routing
pathfinder invocation
protected-segment forwarding
routing-stage coordination
Pathfinding and route geometry
machine-structure-editor/src/machine_builder/graphics/connection_routing_pathfinder.py

Contains the lower-level orthogonal routing and geometry logic.

Important responsibilities include:

visibility-grid construction
deterministic grid traversal
pathfinding
route cleanup
obstacle collision tests
route simplification
U-turn handling
minimum parallel-segment separation geometry
protected-segment route checks
Routing relevance
machine-structure-editor/src/machine_builder/graphics/connection_routing_relevance.py

Controls which nearby obstacles are considered relevant to the routing calculation.

Endpoint preparation
machine-structure-editor/src/machine_builder/graphics/connection_routing_endpoint.py

Handles endpoint-side preparation and endpoint escape/stub geometry used before main pathfinding.

Routing tests
machine-structure-editor/tests/test_connection_routing.py

Contains the focused routing regression and geometry tests.

This is the primary automated test file for the workstream's current routing investigation.

Historical routing records
docs/historical/routing/ROUTING_STABILITY_INVESTIGATION_HANDOFF_4.3.md
docs/historical/routing/ROUTING_STABILITY_INVESTIGATION_HANDOFF_4.4.md

These contain deeper historical investigation detail.

Do not use them as a substitute for inspecting current source code.

Decisions / classifications
DECIDED
Canonical Connection semantics are distinct from visual routing

The semantic Connection answers what is physically or semantically connected.

The visual route answers how that connection is represented spatially in the editor.

Routing/layout behavior must not redefine the canonical semantic relationship merely because visual routing changes.

Route topology and route geometry are distinct visual concepts

A route can preserve its structural organization while its exact coordinates change.

Conversely, a route can change topology even when the triggering coordinate change is very small.

The routing implementation should continue to preserve this distinction.

Routing remains a presentation / graphics concern

The current routing investigation does not require changing the canonical machine semantic model.

Endpoint escape geometry is distinct from the main route

The fixed endpoint escape/stub geometry is prepared first and the main pathfinder operates between the prepared escape endpoints.

IMPLEMENTATION
Route stability / hysteresis

Current route-stability logic compares previous and candidate routes and can preserve an existing route when the candidate does not justify a change.

Current reported tolerance:

16.0

This is an implementation parameter, not an architectural principle.

Deterministic visibility-grid ordering

Grid coordinates are traversed deterministically using sorted coordinate sets.

This has already eliminated one observed tiny-coordinate topology oscillation.

Geometry epsilon

Routing collision and boundary-sensitive calculations use routing geometry tolerance rather than exact floating-point equality.

Transition diagnostics

Current routing diagnostics distinguish, among other things:

endpoint mismatch
previous route blocked
debug-mode stability bypass

and report previous/candidate/selected route geometry and costs.

Minimum route segment separation

A tested geometric predicate exists for overlapping parallel segments.

Current implementation also supports protected segments in the pathfinder.

Hard 8 px protected-segment experiment

The current implementation uses:

MIN_ROUTE_SEGMENT_SEPARATION = 8.0

and supplies endpoint escape segments as protected geometry.

This is experimental implementation behavior only.

WATCH
Hard minimum versus preferred separation

The current evidence does not establish that preferred visual spacing should be a hard legality rule.

The 8 px experiment demonstrates that hard enforcement can create undesirable geometry.

Same-connection versus unrelated edges

The current investigation is intentionally narrow.

The next implementation should first reason about the current connection's own route segments and endpoint stubs rather than beginning global multi-wire optimization.

Route repair versus rerouting

A future repair stage needs a clear rule for when:

repair current geometry

versus:

discard topology and reroute

The workstream should derive that rule from observed behavior rather than introducing arbitrary thresholds prematurely.

NEW PRINCIPLE
Route topology and route geometry may require separate processing stages

Current evidence increasingly supports a staged model:

topology generation
        ↓
geometry generation
        ↓
preferred geometry refinement / nudging
        ↓
final visual route

This should remain a principle candidate rather than an excuse for an immediate router rewrite.

Visual route quality is not identical to geometric legality

A route can be legal and still visually undesirable.

Conversely, a preferred spacing value may be useful for presentation quality without being a condition that every legal route must satisfy.

This distinction is now strongly reinforced by both implementation evidence and external routing research.

RECONSIDER
Hard 8 px separation as the final mechanism

The current hard 8 px implementation successfully prevents the original near-coincident geometry, but it can create:

visible U-turns
small jogs
loops
unnecessary local geometry changes

It should therefore remain a controlled baseline rather than automatically becoming the final routing policy.

Solving endpoint proximity with endpoint-specific special cases

The investigation started near concepts such as endpoint approach distance and U-turn separation.

The broader minimum-route-segment-separation formulation is more general and better aligned with the observed geometry.

Do not reintroduce endpoint-specific special cases unless new evidence requires them.

Using cost tolerance as the primary solution

The stability tolerance can preserve an old route while it remains legal, but it cannot solve a route that has become geometrically blocked.

Do not increase hysteresis tolerance simply to hide a geometry problem.

Current research context

The latest research result from Planning / Research (#2) should be carried forward as follows.

Mature orthogonal-routing systems distinguish:

hard route legality

from:

preferred route quality

A requested minimum edge distance can be treated as a preference and relaxed when the available geometry does not support it.

Post-route nudging and separation adjustment are established patterns in routing systems such as those researched in this workstream.

The current research particularly points toward:

legal topology / route
        ↓
geometry refinement
        ↓
preferred spacing

rather than assuming that every preferred spacing value belongs in the pathfinding legality test.

The research also suggests that segments belonging to the same connection may deserve different handling from unrelated edges.

The next experiment should therefore remain narrow:

one connection
its existing route
its own endpoint escape/stub geometry
existing topology preserved where possible
geometry moved before topology is changed

No global routing-system rewrite is indicated by the current evidence.

Known unresolved issues
Preferred separation repair

Can insufficient spacing be corrected by moving existing geometry while preserving the ordered segment/bend structure?

Selection of movable geometry

If several connected segments participate in the spacing problem, which segments should move, and how should the movement propagate through the route while remaining orthogonal?

Topology preservation

Can the route's existing ordered bend structure be preserved during geometry repair without producing new U-turns, loops, or self-intersections?

Preference relaxation

What should happen when the preferred spacing cannot be achieved within the existing topology?

The research currently suggests that the spacing preference should be allowed to relax rather than forcing increasingly strange geometry.

Repair versus reroute

The implementation still needs a concrete rule for when geometric repair should be attempted and when full rerouting should take over.

Same-connection handling

The current investigation strongly concerns geometry within one connection and its endpoint stubs.

A generalized treatment of nearby unrelated connections has not yet been designed and should not be introduced prematurely.

Persistent topology state

The workstream has evidence that topology and geometry are meaningfully distinct, but it has not established whether route topology needs to become an explicit persistent presentation-state field.

That remains a project-level architectural question rather than a current implementation requirement.

Latest test state
Current latest reported checkpoint
Full Routing suite:

57/57 passed

Preferred-spacing focused tests:

4 passed, 53 deselected

Full repository suite:

The last known green full repository result before the later unrelated Board-owned fixture corruption was 772/772 passed.

The current full repository run is blocked during collection by the unrelated literal `rn` error in src/machine_builder/controller_board_fixtures.py. That file is owned by Workstream 03 and was not modified by Routing.

The Routing implementation itself is currently verified by the focused Routing suite, including the exact known preferred-spacing pathology.
Earlier historical routing results

The routing investigation passed through several earlier checkpoints with smaller focused routing suites and full-suite totals.

Those historical numbers remain useful when reading the older investigation records.

The current authoritative Routing-focused result is:

57/57 focused Routing tests passed

The last known green complete repository result is 772/772 passed, recorded before the unrelated Board-owned fixture import error appeared.

Do not use the older 765/765 or 52/52 values as the current Routing test state.
Next action

Perform visual/manual validation of the known single-connection preferred-spacing pathology with Routing diagnostics enabled.

Compare the repaired geometry against the earlier hard-8 scene-unit baseline and verify:

1. endpoint escape geometry remains fixed
2. the existing route topology remains unchanged
3. the intended interior geometry moves rather than introducing new bends
4. constrained cases fall back cleanly when the preferred target cannot be achieved
5. no unwanted U-turn, jog, or loop behavior appears

After Workstream 03 repairs the unrelated Board fixture collection error, rerun the full repository suite.

Keep the investigation limited to this Routing behavior. Do not begin global multi-wire optimization or rewrite the Routing architecture.
# Checkpoint 11 — 2026-10-04 10:11 AM — SelectionInspector duplicate-definition cleanup

Purpose

Record a verified repository-maintenance cleanup discovered during the broader modularization/audit work, without changing the routing implementation or routing conclusions.

What was found

The file:

machine-structure-editor/src/machine_builder/selection_inspector.py

contained duplicate definitions of three methods:

_routing_debug_toggled
set_routing_debug_mode
set_last_click_position

Inspection established that both copies of each method were byte-for-byte identical.

The later copies were technically the active Python definitions because they appeared later in the class, but they provided exactly the same behavior as the earlier copies.

What changed

Only the redundant second block was removed.

The retained definitions are the first copies of:

_routing_debug_toggled
set_routing_debug_mode
set_last_click_position

The removed block ended immediately before:

def clear(self) -> None:

No routing logic, route-generation behavior, canonical semantic model, or routing-test implementation was changed.

The source file also received the normal terminating newline while being rewritten.

Validation

Focused visual/editor tests were run before the cleanup:

tests/test_selection_inspector.py
tests/test_canvas_interaction.py
tests/test_canvas_ui.py

Result:

20/20 passed

The same focused tests were run again after the cleanup:

20/20 passed

The complete repository test suite was then run:

756/756 passed

This confirms that the duplicate-method cleanup produced no observed behavioral regression.

Files touched

Implementation:

machine-structure-editor/src/machine_builder/selection_inspector.py

Documentation:

machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md

Commit status

The implementation and handoff changes are currently uncommitted at this checkpoint.

What was learned

The duplicate definitions were accidental redundancy rather than two competing implementations.

Because the retained and removed definitions were identical, removing the later block was a safe structural cleanup rather than a behavioral change.

This also reinforces the need to distinguish audit cleanup from routing experimentation: this checkpoint does not alter the current routing strategy, hard-8 px baseline, preferred-spacing investigation, or geometry-only repair plan.

Decisions / classifications

DECIDED

- Retain the first definitions of the three duplicated SelectionInspector methods.
- Remove only the later identical definitions.
- Treat this as a behavior-preserving cleanup.
- Keep all routing investigation decisions and experiments unchanged.

IMPLEMENTATION

- Removed the redundant SelectionInspector method block.
- Preserved existing visual-editor behavior.
- Verified 20/20 focused tests and 756/756 full-suite tests.

WATCH

- No new routing behavior is introduced by this cleanup.
- The broader audit findings concerning _segment_clear() and routing responsibilities in connection.py remain separate and unresolved.

NEW PRINCIPLE

None.

RECONSIDER

None.

Current routing state remains unchanged

This maintenance checkpoint does not replace the current Routing workstream conclusions.

The active routing investigation remains the geometry-only repair experiment described above:

existing legal route
        ↓
identify nearby parallel same-connection segments/stubs
        ↓
detect insufficient preferred separation
        ↓
attempt geometry-only adjustment
        ↓
preserve existing segment/bend topology
        ↓
relax preferred spacing when necessary

The 730/730 full-suite and 52/52 focused-routing results recorded in the Routing checkpoint remain the latest dedicated routing-focused test results until the routing experiment is re-run.

The newer 756/756 result is the latest complete repository test result and includes the routing tests, but the focused routing suite was not separately re-run as part of this SelectionInspector cleanup.

# Checkpoint 12 — 2026-10-04 10:53 AM — _segment_clear() obsolete-helper cleanup

Purpose

Record the separate routing-test cleanup identified during the repository audit.

What was found

The helper _segment_clear() in:

machine-structure-editor/tests/test_connection_routing.py

was confirmed to be unused.

A repository-wide search across the Python source and test trees found exactly one _segment_clear( reference, and that occurrence was the helper's own definition. No callers or indirect uses were found.

The routing-test baseline before removal was:

52/52 passed

The full repository baseline before removal was:

756/756 passed

What changed

Only the unused _segment_clear() helper was removed from:

machine-structure-editor/tests/test_connection_routing.py

No routing implementation, other test helper, test case, or routing behavior was changed.

Validation after removal

Focused routing tests:

52/52 passed

Full repository suite:

756/756 passed

The resulting implementation diff contained only the removal of the 25-line unused helper.

Commit

467933875ca0547a5a6885017d3b10c77efbafb2

What was learned

The helper was genuinely obsolete rather than an indirectly referenced testing utility. Removing it produced no change in routing-test behavior or repository-wide test behavior.

Decisions / classifications

DECIDED

- _segment_clear() was obsolete and safe to remove.
- The cleanup is separate from routing implementation work.
- No routing architecture or behavior was changed.

IMPLEMENTATION

- Removed only the unused _segment_clear() helper.
- Verified 52/52 routing tests and 756/756 full-suite tests after removal.

WATCH

- No new routing behavior was introduced.
- The connection.py routing-responsibility audit is recorded separately in Checkpoint 13.

NEW PRINCIPLE

None.

RECONSIDER

None.

Current routing investigation remains unchanged.

The next routing implementation action remains the geometry-only repair experiment for the known single-connection spacing pathology.

# Checkpoint 13 — 2026-10-04 11:06 AM — connection.py routing-responsibility audit

Purpose

Determine whether the routing and stability logic remaining inside:

machine-structure-editor/src/machine_builder/graphics/connection.py

is active route-generation logic, fallback behavior, an adapter/presentation layer around the dedicated routing modules, or duplicated/legacy routing logic.

Investigation result

The evidence shows that connection.py is an active per-connection orchestration and presentation/state layer, not a second independent route generator.

The production route-generation flow is:

Canvas / connection preview
        ↓
ConnectionGraphicsItem.setLine()
        ↓
endpoint escape preparation
        ↓
ConnectionRoutingEngine.build_route()
        ↓
stable-route selection in ConnectionGraphicsItem
        ↓
final QPainterPath construction

ConnectionRoutingEngine is an active façade/coordinator. It delegates:

- endpoint stub/escape construction to connection_routing_endpoint.py
- relevance detection to connection_routing_relevance.py
- orthogonal pathfinding to connection_routing_pathfinder.py

The only source-level production caller of ConnectionRoutingEngine.build_route() is connection.py.

No duplicate implementations of the connection-level stability methods were found in the other graphics routing modules.

Active responsibilities owned by ConnectionGraphicsItem

The class currently owns connection-instance runtime/presentation state including:

- _stable_route
- _overlap_escape_state
- routing-debug state
- previous/candidate/selected route diagnostics
- route transition history
- route stability tolerance
- route continuity selection
- topology-preserving geometry repair
- route-cost comparison
- endpoint escape integration
- scene obstacle collection
- final QPainterPath construction

The route-selection logic in connection.py is active behavior rather than legacy fallback code.

Tests provide direct coverage for this boundary.

The routing tests directly exercise:

- _route_cost()
- _select_stable_route()
-
outing_diagnostics()

The routing tests also directly exercise the ConnectionRoutingEngine APIs.

Production callers of setLine() include:

- canvas_scene.py for committed visual connections
- canvas_interaction.py for connection previews

The selection inspector also consumes
outing_diagnostics().

Recommendation

Leave connection.py alone for now.

No surgical routing cleanup is justified by this audit.

No route-generation duplication was established.

Do not begin a larger routing modularization project solely because connection.py is large.

A future extraction of the route-stability/policy layer could be considered as a deliberate modularization project if that logic grows substantially, becomes independently reusable, or develops a separate testing/ownership boundary.

This investigation does not change the current routing architecture.

No implementation source files were changed for Part 2.

Decisions / classifications

DECIDED

- connection.py contains active routing orchestration, connection-level stability policy, runtime state, diagnostics, and final visual path construction.
- ConnectionRoutingEngine remains the reusable routing façade for endpoint, relevance, and pathfinding operations.
- No duplicated independent route generator was found in connection.py.
- No routing refactor is justified by the audit findings.

IMPLEMENTATION

- None.

WATCH

- Whether the connection-level stability/policy logic grows enough to justify a dedicated module in a future deliberate modularization effort.
- _build_endpoint_stub() remains a compatibility helper in connection.py; no removal is justified by this investigation.

NEW PRINCIPLE

None.

RECONSIDER

- Revisit modular extraction only if the stability layer develops an independent ownership boundary or meaningful reuse requirement.

Tests

No new implementation test run was required for this investigation because no implementation source was changed.

The latest complete repository result remains:

756/756 passed

The latest dedicated routing checkpoint remains:

52/52 focused routing tests passed

No implementation commit was created for Part 2.

# Checkpoint 14 — 2026-10-04 9:05 PM — Legacy Routing handoff reconciliation

The former V0.2_VISUAL_EDITOR_IMPLEMENTATION_HANDOFF.md was compared with the current Routing continuity handoff and the historical 4.3/4.4 Routing records.

The old document contains historical Routing / Diagnostics material rather than a current Visual Editor implementation handoff. It has been renamed to docs/historical/routing/ROUTING_DIAGNOSTICS_HISTORICAL_HANDOFF.md so its historical provenance is preserved while its misleading current-authority identity is removed.

Most substantive Routing investigation from the old document is already preserved in the current Routing handoff and the historical 4.3/4.4 records.

Useful historical Routing details additionally retained in the renamed file include the Routing Debug Mode viewport repaint fix (FullViewportUpdate while Debug Mode is active, restored to MinimalViewportUpdate when disabled) and the historical Debug Mode overlay inventory covering physical component bounds, routing-clearance envelopes, fixed endpoint stubs, endpoint escape geometry, the main routed path, unroutable endpoint markers, and the last canvas click.

Current Routing continuity belongs to  4_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md. Historical Routing material remains preserved in docs/historical/routing/ROUTING_DIAGNOSTICS_HISTORICAL_HANDOFF.md, docs/historical/routing/ROUTING_STABILITY_INVESTIGATION_HANDOFF_4.3.md, and docs/historical/routing/ROUTING_STABILITY_INVESTIGATION_HANDOFF_4.4.md.

No routing implementation, routing behavior, or topology-versus-geometry architectural investigation was changed.

# Checkpoint 15 — 2026-10-05 1:55 PM — Real-data Duet 2 Maestro integration review

The Routing / Diagnostics workstream completed its focused review for the first real-data integration using the Duet 2 Maestro.

The current Routing implementation boundary remains healthy:

visual/presentation geometry → ConnectionGraphicsItem → ConnectionRoutingEngine → endpoint/relevance/pathfinder.

Routing has no direct dependency on Board/controller implementation internals, and Board/controller implementation has no direct dependency on Routing implementation internals. The existing synthetic/example Routing work is not considered defective merely because real Board data is now being introduced, and no Routing refactor is warranted on that basis.

The canonical model already provides the relevant real-data identity chain:

HardwareDefinition → Controller/MachineComponent → SemanticPort → SemanticConnection.

SemanticPort supports both component-owned and controller-owned ports and carries canonical identity, connector/pin identity where known, semantic properties, and provenance.

The existing component-owned projection path is:

MachineComponent → project_component_ports() → VisualPort.semantic_reference.

The clearest first real-data visual integration seam is the missing generic controller-owned projection:

Controller → controller.port_ids → SemanticPort → VisualPort.semantic_reference → PortGraphicsItem.

Existing connection editing already resolves visual endpoint references through VisualPort.semantic_reference before creating the canonical SemanticConnection. Therefore controller-owned port projection can reuse the existing connection architecture.

The intended real-data path is:

Controller → controller-owned SemanticPorts → VisualPorts → connection editing → canonical SemanticConnection → existing Routing geometry.

Real Maestro visualization should remain generic rather than hard-coded to Maestro.

Documented physical board dimensions, outline, connector locations, and connector orientation are Hardware Definition information when they describe the manufactured hardware and trustworthy evidence exists. User-controlled node placement, visual rotation, zoom/detail level, filters, layers, selection, and highlighting remain visual/document state.

Routing continues to own route geometry, endpoint escape geometry, obstacle handling, pathfinding, route legality, route stability, geometry repair, routing costs, routing state/caches, and diagnostics.

Current Maestro data does not yet provide trustworthy structured physical connector positions/orientations. The first generic board visualization may therefore legitimately use a simple board rectangle with real sorted/grouped interface labels rather than inventing physical locations.

Recovered editor constraint: basic/intermediate/extreme detail levels are presentation modes over the same underlying canonical + visual dataset. Filters and layers are independent view-state controls. Changing detail or zoom must never create or mutate a second semantic model.

No new Protocol, adapter, or Board → Routing contract is currently justified.

Potential future semantic query boundaries remain WATCH items only:
- visual endpoint → canonical SemanticPort resolution;
- semantic compatibility evaluation;
- canonical connection-invariant queries.

These should be introduced only when a concrete consumer need demonstrates that direct canonical-model access is no longer appropriate.

Recommended first #4 implementation slice:
- use the real canonical Maestro controller;
- project controller-owned SemanticPorts into VisualPorts;
- display them using the existing visual-port mechanism;
- support basic grouping/filtering as view state;
- verify semantic endpoint resolution;
- then exercise candidate connections against a real reusable external component.

No implementation files, tests, Routing behavior, visual-editor code, or other workstream files were changed as part of this documentation checkpoint.

# Checkpoint 16 — 2026-10-05 8:03 PM EDT — Controller-owned SemanticPort -> VisualPort implementation

Purpose

Record the completion and verification of the first approved real-data integration slice identified in Checkpoint 15.

Repository state

Commit:

a1f9c6a — Expand Maestro interfaces and controller-owned port projection

The commit is present on both local main and origin/main.

The commit also includes Board-owned Maestro hardware/catalog changes from Workstream 03. Those changes are not Routing-owned.

Implementation files relevant to this #4 integration slice:

src/machine_builder/semantic_projection.py
src/machine_builder/controller_visual_mutations.py
tests/test_semantic_projection.py
tests/test_controller_visual_mutations.py
tests/test_connection_authoring.py

What changed

The existing component-port projection was generalized through a shared projection mechanism. Controller-owned ports now use the same canonical-to-visual path:

Controller -> controller.port_ids -> canonical SemanticPort -> project_controller_ports() -> VisualPort.semantic_reference -> existing connection editing -> canonical SemanticConnection -> existing Routing

Controller visual creation now projects its canonical ports into the existing VisualNode.

No Maestro-specific visual or routing implementation was added.

Why it matters

Controller-owned and component-owned SemanticPorts now use the same visual-port projection and connection-authoring mechanism. Routing does not need to know which kind of canonical owner produced the endpoint.

What was verified

Focused controller/projection/connection/controller-port tests: 30 passed.
Full repository test suite: 765 passed.

The committed validation recorded in a1f9c6a reports 32 focused tests passed, 765 full-suite tests passed, and git diff --check clean.

Architecture classification

IMPLEMENTATION ONLY
- Controller-owned SemanticPort -> VisualPort projection extends the existing canonical/visual boundary.
- No new canonical ontology entity or semantic contract was introduced.

REINFORCE
- The canonical model remains the semantic authority.
- The visual model remains presentation/authoring state.
- Routing remains independent of Board/controller implementation details.
- Basic/intermediate/extreme detail levels remain presentation modes over the same canonical + visual dataset.
- Filters and layers remain independent view-state controls.
- Zoom/detail/filter/layer changes must never create or mutate a second semantic model.

WATCH
- Visual endpoint -> canonical SemanticPort resolution may become a stronger query boundary only if concrete reuse needs arise.
- Semantic compatibility evaluation and canonical connection-invariant queries remain WATCH items.
- Physical connector positions/orientations remain unmodeled where trustworthy structured evidence is absent.

Rejected / not required

- No Routing refactor.
- No Board -> Routing adapter.
- No speculative Protocol or contract.
- No second semantic model.
- No Maestro-specific visual/routing implementation.

Current unresolved issues

The known single-connection preferred-spacing pathology remains unresolved. The hard-8 px experiment remains a baseline rather than a durable routing principle.

Next action

Return to the existing Routing next action: implement and test the small geometry-only repair experiment for the known spacing pathology. Preserve route topology where possible and do not begin global multi-wire optimization.

No change is made here to the existing Routing architecture or canonical Connection model.

# Checkpoint 17 — 2026-10-06 12:43 AM EDT — Routing experiment recovery / replacement-chat handoff

Purpose

Record the verified Routing workstream state after Checkpoint 16 and before replacing the current Routing chat.

This checkpoint does not represent a completed Routing implementation change.

Repository/source inspection

The following Routing files were directly inspected:

src/machine_builder/graphics/connection.py
src/machine_builder/graphics/connection_routing.py
src/machine_builder/graphics/connection_routing_pathfinder.py
tests/test_connection_routing.py

The inspection confirmed the current route-stability behavior, existing topology-preserving blocked-route repair, current parallel-segment separation support, and relevant Routing test coverage.

No Routing implementation was completed after Checkpoint 16.

No Routing tests were changed.

No tests were run after Checkpoint 16.

A temporary nudging source file was created during an abandoned implementation attempt and was subsequently removed. It was not a completed implementation and is not part of the current Routing architecture.

No alternate permanent Routing handoff was created.

Current unresolved issue

The known preferred-spacing pathology remained unresolved at this checkpoint.

The existing 8.0 scene-unit protected-segment experiment remained a useful baseline, but 8.0 scene units was not a permanent Routing rule. The experiment demonstrated that hard spacing can eliminate near-coincident geometry while also producing undesirable U-turns, jogs, loops, or awkward local geometry.

Current objective

The next Routing experiment remained the small topology-preserving geometry-only repair experiment:

existing route geometry

↓

detect insufficient preferred spacing

↓

move existing geometry rather than inventing new bends

↓

preserve existing bend/segment topology where possible

↓

relax preferred spacing when the available geometry cannot satisfy it cleanly

↓

fall back to existing routing when geometry-only repair is not legal or clean

An initial preferred separation of approximately 4 scene units may be used as the experimental preference, but it is not a hard minimum.

Next action

The replacement Routing chat should continue from this existing handoff and implement/test the small geometry-only repair experiment for the known preferred-spacing pathology.

Measure:

minimum/legal separation
preferred separation
bend count
route length
topology identity
geometry movement
U-turn/jog/loop behavior
fallback when geometry-only repair is insufficient

Do not modify Board, Planning, Research, or other workstream files.

Do not make documentation changes as part of the implementation experiment.

Recovery state

The authoritative live Routing handoff remains:

machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md

There is exactly one live Routing workstream handoff.

# Checkpoint 18 — 2026-10-06 12:59 PM EDT — Preferred-spacing geometry-only repair experiment

Purpose

Record the completed and tested first implementation of the narrow topology-preserving geometry-only repair experiment identified by the earlier Routing checkpoints.

Files touched

src/machine_builder/graphics/connection.py
tests/test_connection_routing.py
handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md

No Board, Planning, Research, or other workstream implementation files were changed by this Routing experiment.

Commit status

The Routing implementation and this handoff update are currently uncommitted.

What changed

The Routing connection graphics layer now has an experimental preferred-spacing repair step.

A preferred target of 4.0 scene units is represented by PREFERRED_ROUTE_SEGMENT_SEPARATION. This is a visual-quality preference, not a new hard legality rule.

The repair:

- examines the existing legal route rather than immediately inventing a new topology
- detects nearby parallel protected geometry
- considers only movable interior route segments
- preserves the existing ordered segment/bend topology
- proposes moving existing horizontal or vertical geometry
- rejects candidate positions that intersect obstacles
- verifies the repaired route still has the same topology
- verifies the preferred separation when the candidate can achieve it cleanly
- leaves normal route selection available when geometry-only repair cannot be applied

The first and last route segments remain tied to the endpoint escape geometry and are not moved by this repair.

The preferred-spacing repair is attempted before normal continuity blending when the previously stable route is still clear.

The stability diagnostic bookkeeping was also corrected so the reported previous-route cost remains the actual previous-route cost rather than the repaired candidate cost.

Why it changed

The hard protected-segment spacing experiment proved that a minimum-spacing rule can eliminate the original near-coincident geometry, but it could also force undesirable U-turns, jogs, loops, or awkward topology.

The implementation therefore moves the preferred-spacing concern into a later geometry-quality stage. The goal is to improve visual spacing without turning the preference into a pathfinding legality constraint.

What was learned

The known historical endpoint-spacing pathology is repairable without changing topology.

The problematic route segment is the penultimate interior horizontal segment, not the terminal endpoint segment itself. Moving that existing interior geometry away from the protected endpoint segment preserves the endpoint escape while removing the approximately 0.001-unit near-coincident parallel geometry.

The exact historical pathology test passes with the route topology and total route cost preserved while the affected geometry moves to the preferred spacing.

Verification

Preferred-spacing tests:

4 passed, 53 deselected

Full Routing suite:

57/57 passed

The exact historical preferred-spacing pathology is covered and passes.

git diff --check was clean for the Routing implementation/test changes before this handoff update.

A later full repository suite is currently blocked during collection by an unrelated Board-owned import error in:

src/machine_builder/controller_board_fixtures.py

The reported problem is a stray literal `rn` immediately before an existing fixture tuple. Routing intentionally did not modify that file.

The last known green full repository suite before that unrelated Board corruption was:

772/772 passed

Architectural classification

IMPLEMENTATION ONLY

- The 4.0 scene-unit value is an experimental preferred visual spacing target.
- Preferred spacing is not promoted to a new hard Routing legality rule.
- No canonical semantic Connection model change was introduced.
- No new semantic entity was introduced.
- Endpoint escape geometry remains distinct from movable interior route geometry.
- Existing topology-changing route selection remains available as the fallback when geometry-only repair cannot produce a legal/clean result.

Rejected / superseded

- The earlier hard-8 scene-unit experiment remains a diagnostic/baseline result, not the final preferred-spacing policy.
- The abandoned temporary standalone nudging source file is not part of the architecture.
- No global multi-wire optimization was introduced.
- No rule requiring every legal parallel segment to maintain 4.0 scene-unit spacing was introduced.

Current unresolved issues

- The current repair mechanism has only been established for the narrow known single-connection pathology.
- More constrained geometries need visual validation.
- Preference relaxation in narrow channels is currently handled by declining the geometry-only repair and allowing normal routing to remain in control; a more general soft-spacing optimization has not been established.
- Coordinated movement of several related interior segments has not yet been generalized.
- The interaction between repair, continuity hysteresis, and broader topology transitions needs real visual validation.

Next action

Perform visual/manual validation of the known pathology with routing diagnostics enabled and compare the result against the earlier hard-8 baseline.

Then rerun the full repository suite after Workstream 03 repairs its unrelated Board fixture import error.

Do not begin global multi-wire routing optimization from this checkpoint.

No canonical semantic Connection model change is required.

Recovery rule

This handoff is a living recovery document.

Update it after meaningful tested implementation progress, not only at large milestones.

A successful test run after meaningful progress is a natural checkpoint.

For every meaningful checkpoint, record:

exact repository-relative files touched
approximate checkpoint purpose
commit hash or hashes when known
tests run and their results
what changed
why it changed
what was learned
approaches that were rejected or superseded
current unresolved issues
next concrete action

Maintain the cumulative:

## What we've done so far

Checkpoint 1 established the core Routing distinction between route geometry and route topology and identified small-motion route instability as the primary investigation target.

Checkpoints 2–6 established route-stability tolerance, precision-sensitive geometry handling, transition diagnostics, deterministic visibility-grid ordering, and the distinction between legal continuity and genuinely blocked previous routes.

The subsequent Routing work established topology-preserving geometry repair, fixed endpoint-escape behavior, blocked-route repair, route-segment separation predicates, and focused regression coverage for the observed stability pathologies.

Checkpoint 11 cleaned up duplicate SelectionInspector definitions. Checkpoint 12 removed an obsolete routing helper. Checkpoint 13 confirmed the intended Routing responsibility boundary in connection.py. Checkpoint 14 reconciled older Routing documentation into the historical archive.

Checkpoints 15–16 verified the Routing boundary against the first real Duet 2 Maestro data and the controller-owned SemanticPort -> VisualPort integration. No Board-specific Routing coupling was introduced.

Checkpoint 17 captured the recovery state before the preferred-spacing experiment.

Checkpoint 18 completed the narrow preferred-spacing geometry-only repair experiment. The known endpoint-parallel pathology is now repaired by moving existing movable interior geometry while preserving topology and route cost. The 4.0 scene-unit value remains an experimental visual-quality preference rather than a hard legality rule.

Checkpoint 19 added and verified an end-to-end GUI regression test using the real saved "4 parts.machine.json" document. The test exercises the actual Precision Nudge path against node-2 and connection-1 and verifies repeated 0.001-unit X nudges preserve topology, interior route geometry, endpoint behavior, and route-stability decisions.

# Checkpoint 19 — 2026-10-07 9:01 PM EDT — Real-machine precision-nudge GUI validation

Purpose

Record the completed end-to-end GUI validation of Routing stability after the preferred-spacing implementation and the committed GUI regression test.

Files touched

machine-structure-editor/tests/test_routing_gui_validation.py

The preferred-spacing implementation and its deterministic Routing tests were already committed in:

7ac7cfc — Add topology-preserving preferred-spacing routing repair

The GUI validation regression test was committed in:

db2538862bd0b4d3407df299ad6f779b35d73965 — Add GUI precision-nudge routing regression test

No Routing production implementation was changed by this checkpoint.

What changed

Added a permanent GUI regression test that:

- loads the real saved machine:
  wiring test machines/4 parts.machine.json
- selects the real visual node:
  node-2 / Temperature Controller
- exercises the same Precision Nudge callback used by the GUI
- applies ten +X nudges of 0.001 scene units
- processes Qt events after each move
- captures the real ConnectionGraphicsItem routing state
- writes the validation report outside the repository

Validation result

GUI regression test:

1 passed

Routing regression suite:

57 passed

Real-machine validation reported:

Topology failures: 0
Interior geometry failures: 0
Endpoint motion failures: 0
Stability decision failures: 0
Final route points: 7

The ten nudges moved node-2 from X = -225.000000 to X = -224.990000 exactly as expected.

The selected route retained the same seven-point topology and unchanged interior geometry. Only the endpoint-adjacent geometry followed the 0.001-unit node movement. The route-stability decision remained:

previous stable route held within tolerance

The preferred-spacing repair did not trigger in this four-node saved machine. That is expected because this document does not contain the specific near-coincident protected-segment pathology.

Important validation correction

The initial temporary validation counted any exact route-coordinate difference as "Route changed". That was too literal because the endpoint-adjacent route point legitimately follows the nudged node.

The permanent validation instead distinguishes:

- topology change
- interior geometry change
- endpoint motion
- stability-decision change

This produces a meaningful regression signal.

Debug-mode note

Routing Debug Mode was deliberately not enabled for the permanent stability validation because the current implementation explicitly bypasses route stability while Debug Mode is active. The runtime diagnostics were therefore captured with debug mode false.

No Routing production defect was identified by this validation.

Current state

DECIDED

- Route geometry and route topology remain distinct concepts.
- Canonical semantic Connection identity is separate from visual route geometry.
- Route stability is a selection/stability policy, not a replacement for legal pathfinding.
- Endpoint escape geometry remains fixed/tied to endpoint behavior; preferred-spacing repair moves only eligible interior route geometry.
- The preferred 4.0 scene-unit spacing value is an experimental visual-quality preference, not a hard routing legality rule.
- No global multi-wire optimization is part of the current scope.
- No Routing dependency on Board/controller implementation internals is required.

IMPLEMENTATION

- ConnectionGraphicsItem owns visual connection integration, endpoint geometry acquisition, route stability, geometry repair, diagnostics, and painting.
- connection_routing.py remains the routing coordination façade.
- connection_routing_endpoint.py owns endpoint stubs, escapes, and endpoint hysteresis.
- connection_routing_relevance.py owns relevant-scene reduction.
- connection_routing_pathfinder.py owns orthogonal search, route legality, cleanup, fallback, and geometry predicates.
- Preferred-spacing geometry repair is implemented as a later stability/geometry-quality operation.
- Routing diagnostics expose previous, candidate, selected, endpoint-escape, obstacle, cost, and transition information.
- Deterministic GUI regression coverage now exercises the actual saved-document and Precision Nudge path.

WATCH

- The preferred-spacing repair has been established only for the narrow known single-connection pathology.
- More constrained geometries still need visual validation.
- Preference relaxation in narrow channels remains intentionally conservative: geometry-only repair can decline and leave normal routing in control.
- Coordinated movement of multiple related interior segments has not been generalized.
- The interaction between preferred-spacing repair, continuity hysteresis, and broader topology transitions needs additional real visual evidence.
- Broader real-machine routing validation should continue as trustworthy physical geometry and controller/component data become available.

NEW PRINCIPLE

None promoted by Checkpoint 19.

The GUI validation confirms current behavior but does not justify a new architectural Routing principle.

RECONSIDER

- The historical hard-8 scene-unit experiment remains a baseline/rejected hard-spacing policy, not the current rule.
- A general soft-spacing optimization should be reconsidered only if additional real geometries demonstrate a concrete need.
- Global multi-wire optimization remains explicitly out of scope for the current work.

Current unresolved issues

- Visual/manual validation of the exact historical preferred-spacing pathology remains desirable, but must not enable Debug Mode when the objective is to observe route-stability repair because Debug Mode bypasses stability.
- The broader full repository suite remains blocked by the unrelated Board-owned fixture import problem in:
  src/machine_builder/controller_board_fixtures.py
- The Board-owned changes must remain untouched by Routing.

Next concrete action

1. Continue targeted visual validation of constrained preferred-spacing geometries using normal Routing mode and the existing runtime diagnostics.
2. Rerun the full repository suite once Workstream 03 repairs its unrelated Board fixture import error.
3. Incorporate the separate PowerShell parser research from Research / #2 into the shared workflow when that report is returned.

No canonical semantic Connection change is required.
No Board -> Routing adapter is required.
Do not begin global multi-wire routing optimization from this checkpoint.

# Checkpoint 20 — 2026-10-07 10:53 PM EDT — Quantitative preferred-spacing repair comparison

Purpose

Record the tested comparison between the narrow topology-preserving preferred-spacing geometry repair and the earlier hard-8 scene-unit protected-segment experiment.

Verification

Current repository state at verification:

b284c53 — Implement Maestro E2/E3 external driver interfaces

Routing production files and Routing tests were clean before this documentation-only checkpoint.

Focused Routing validation:

57 passed in 0.24s

Focused Routing plus the permanent real-machine GUI regression:

58 passed in 2.82s

Known pathology geometry-only repair result

The exact historical preferred-spacing test uses the seven-point route:

(-5.000, 240.000)
-> (-1.250, 240.000)
-> (-1.250, 141.510)
-> (-25.250, 141.510)
-> (-25.250, -24.999)
-> (-10.000, -24.999)
-> (-10.000, -25.000)

The repair moves only the existing interior geometry at points 4 and 5 from y = -24.999 to y = -21.000.

Measured result:

- minimum achieved preferred separation: 4.000 scene units
- route length before repair: 308.000 scene units
- route length after repair: 308.000 scene units
- route point count: 7
- ordered segment topology: unchanged
- endpoint escape geometry: unchanged
- moved interior points: 2
- movement per affected point: 3.999 scene units
- total pointwise movement: 7.998 scene units
- new bends introduced: none
- topology identity: unchanged
- route cost: unchanged within test tolerance
- stability decision: "previous stable route received preferred-spacing geometry repair"

The repair therefore improves the visual spacing of the known near-coincident geometry without creating a new route topology or adding local detour geometry.

Historical hard-8 baseline

The earlier protected-segment experiment is retained as the comparison baseline.

Its documented result was approximately:

- minimum achieved separation: 8.000 scene units
- topology-changing pathfinder enforcement: yes, when necessary
- unwanted geometry observed: visible U-turns, jogs, and loops
- documented example: a horizontal route segment at y = 231.999 was approximately 8 scene units from the protected y = 240 endpoint escape
- lower-side variants produced analogous U-turn/jog behavior and eventually a loop

The archived material does not preserve a complete exact route for the hard-8 case, so a complete independently calculated hard-8 route length and full bend/segment count are not asserted here.

Conclusion

For the known single-connection pathology, the geometry-only repair experiment provides the better result demonstrated by current evidence:

- the 4.000-unit preferred spacing is achieved;
- existing route topology is preserved;
- existing interior geometry moves instead of creating new bends;
- route length and route cost remain unchanged;
- endpoint escape geometry remains fixed;
- the repair avoids the documented U-turn/jog/loop side effects of hard 8-unit pathfinding enforcement.

The hard-8 mechanism therefore remains a historical diagnostic baseline rather than the preferred final mechanism.

Scope boundary

This checkpoint does not introduce a generalized soft-spacing optimizer, global multi-wire optimization, canonical Connection changes, or Board coupling.

The permanent GUI regression remains valuable for real application behavior, but its saved four-node machine does not contain the exact historical near-coincident pathology, so the preferred-spacing repair itself continues to rely on the deterministic exact-pathology regression for direct coverage.

Current next action

No further production Routing change is justified by this single-connection experiment. Broader preferred-spacing behavior should remain observational and constrained until additional real geometries provide evidence for a generalized policy.
# Checkpoint 21 - 2026-10-07 11:49 PM EDT - Preferred-spacing relaxation boundary regression

Purpose

Record the tested repair-versus-reroute boundary for preferred-spacing refinement.

What changed

Added one Routing regression test:

tests/test_connection_routing.py
test_route_stability_relaxes_preferred_spacing_when_repair_declines

The test establishes that:

- the previous stable route remains legal;
- the preferred-spacing repair explicitly returns None because the available geometry cannot legally move the fixed endpoint-adjacent segment;
- the previous route still has insufficient preferred spacing;
- the candidate route has a different topology;
- normal Routing mode retains the previous legal topology rather than forcing the preferred spacing;
- the stability decision remains:
  "previous stable route held within tolerance"

This makes preference relaxation an explicit tested behavior rather than relying only on the lower-level repair-decline test.

The opposite boundary is already covered by the existing blocked-route stability regression: when the previous route is no longer legal, normal topology-changing routing remains available.

Verification

Focused Routing suite:

59 passed in 2.21s

Full repository suite:

782 passed in 4.11s

No Routing production implementation was changed by this checkpoint.

Conclusion

The current evidence now supports the following narrow Routing policy:

1. Prefer an existing legal route.
2. Attempt topology-preserving geometry repair when preferred spacing is insufficient.
3. If repair cannot produce a legal/clean result, relax the preferred spacing rather than forcing new local geometry.
4. If the previous topology is no longer legal, allow normal topology-changing rerouting to take over.

This is a behavioral boundary for the current Routing implementation, not a new canonical semantic rule and not a generalized soft-spacing optimizer.

Scope boundary

No global multi-wire optimization, topology persistence model, canonical Connection change, Board coupling, or Routing architecture rewrite was introduced.

Current next action

No additional production Routing change is justified by this boundary test alone. Broader repair behavior should remain observational until additional real machine geometries provide evidence for a concrete need.

# Checkpoint 22 - 2026-10-09 - Generic palette canonical component checkpoint

Purpose and disposition

Planning accepted this bounded checkpoint for commit after the #5 audit was rated
ACCEPTABLE FOR COMMIT REVIEW. The goal was to ensure generic non-controller palette
entries have canonical installed MachineComponent identity and remain usable through
component-owned port authoring and persistence.

Implementation retained

The existing production path already creates canonical components through `CreateNode` in
src/machine_builder/mutations.py. It registers a `MachineComponent`, links the
corresponding `VisualNode` through `semantic_reference`, and leaves generic
`hardware_definition_id` unset. No production source files were changed.

Changed test files

- machine-structure-editor/tests/test_controller_palette_authoring.py
- machine-structure-editor/tests/test_component_authoring_ui.py

Regression coverage added

- Generic Motor, Sensor, Temperature Sensor, Component, and Temperature Controller
  palette templates register canonical components with distinct identities and machine
  membership.
- Generic creation leaves hardware identity unknown, does not fabricate a
  HardwareDefinition, and does not create a Controller.
- Generic palette creation is undoable and redoable.
- A palette-created Motor supports component-owned Add Port authoring.
- Canonical port projection preserves unmatched provisional visual ports.
- Save/reopen coverage asserts canonical component and port identities, machine
  membership, visual linkage, and provisional visual-port IDs.

Verification against the final test files

- Focused suite: 70 passed in 3.04 seconds.
- Full suite: 805 passed in 7.42 seconds, exit code 0, no collection errors.
- `git diff --check`: passed.

Nonblocking coverage limitation from the #5 audit

Save/reopen tests do not compare every field of every provisional `VisualPort` instance,
and they do not directly assert preservation of wire endpoints attached to provisional
ports. This remains a future coverage consideration; it was not expanded in this checkpoint.

Scope boundary

This checkpoint does not establish real Maestro instantiation, detailed physical
connection authoring, or a complete persisted Promega machine. It adds no catalog/import
work, ontology changes, or broader feature implementation.

Planning-authorized commit scope

The authorized commit contains these two test files and this living handoff only.
Exclude unrelated Board/catalog changes, the root `.vscode/` directory, and all other
files outside this checkpoint.

# Checkpoint 23 — 2026-10-10 — Physical connection metadata authoring

Purpose and disposition

Record the accepted physical connection authoring implementation as a separate integration checkpoint. The implementation extends connection creation and inspection while preserving the existing canonical-model, visual-model, and Routing boundaries.

Repository and commit state

Commit: c445bef287d736afd20807f29d2506aab2434eaa

Subject: Add physical connection metadata authoring

Commit timestamp: 2026-10-10T00:22:38-04:00

Publication was independently confirmed after fetching origin: local main and origin/main both resolved to the accepted commit.

Review disposition: #5 accepted the corrected implementation. Planning authorized the seven-file implementation commit and its subsequent push.

Implementation files in the commit

- src/machine_builder/canvas_interaction.py
- src/machine_builder/canvas_selection.py
- src/machine_builder/connection_details.py
- src/machine_builder/mutations.py
- src/machine_builder/selection_inspector.py
- tests/test_connection_details.py
- tests/test_store_persistence.py

What changed

The connection-authoring path supports creation-time entry of wire_color, harness_id, and notes for canonical physical connections. These values are stored in SemanticConnection.properties under exactly those keys. Blank or whitespace-only values normalize to None; nonblank values are preserved as entered.

Connection creation retains compatibility handling: compatible endpoints proceed, unknown and conditional compatibility require explicit confirmation, and known incompatibility blocks creation. Canonically linked endpoints receive the physical-details dialog. Genuinely unlinked/provisional endpoints use a separate visual-only prompt and create no canonical physical connection.

The mutation boundary independently validates every non-null canonical port reference before choosing between canonical and visual-only creation. A stale reference cannot silently downgrade into visual-only creation. The selected-connection inspector displays saved physical metadata read-only.

Regression coverage includes warning and cancellation paths, stale references in both endpoint orientations, visual-only acceptance and cancellation, controller-to-component endpoint identity, undo/redo, and integrated save/reopen persistence for embedded hardware definition/provenance, port ownership, connection metadata, visual endpoint IDs, and route geometry.

Verification reported from the local checkout before commit

- Focused connection-authoring, persistence, and inspector suite: 46 passed in 0.73 seconds.
- Full repository suite: 827 passed in 4.27 seconds.
- Scoped implementation whitespace check: clean.

These are the reported pre-commit test results, not new test runs by the reviewer. The accepted commit was subsequently confirmed published on origin/main.

Architectural boundary

No Routing production implementation or route geometry algorithm was changed by this checkpoint. Canonical physical connection identity and metadata remain distinct from visual endpoint identifiers and visual route geometry. No new ontology entity, generalized compatibility redesign, or global routing optimization was introduced.

Nonblocking follow-ups

- #5 did not separately certify exact word-for-word UX-copy equivalence. The dialog and warning copy has dedicated assertions, but that specific reviewer certification was not recorded as complete.
- Reversed-order duplicate-pair rejection is implemented, but that orientation still lacks a dedicated duplicate-rejection regression assertion.

These are follow-ups, not blockers for the accepted commit. Do not expand the completed commit or imply that either item was part of the reviewer's acceptance.

Current status and next action

The accepted connection-authoring implementation is committed and published. Continue the existing Routing investigation according to Planning's direction; this checkpoint does not justify a new Routing production change. Address the two listed coverage follow-ups only when Planning assigns that work.

The three Research/Board document changes and the root .vscode/ configuration remained outside the implementation commit and push. This checkpoint changes Routing handoff documentation only; it does not include those other files.

# Checkpoint 24 — 2026-10-10 — Board-backed Maestro palette authoring

Purpose and disposition

Record the completion of the bounded user-facing path for creating a board-backed Duet 2 Maestro controller as the first controller in the M3D Promega compound reference specimen. This is an implementation checkpoint, not a commit checkpoint.

Checkout metadata captured immediately before the handoff edit

Branch: main

HEAD: 8ce8102539f10a46d4d057934dfff7570cc92164

Local handoff edit timestamp, captured immediately before writing this checkpoint: 2026-10-10 01:38:47 -04:00

The working-tree status below was captured in the same pre-edit command sequence:

 M machine-structure-editor/src/machine_builder/canvas_palette.py
 M machine-structure-editor/src/machine_builder/controller_board_fixtures.py
 M machine-structure-editor/src/machine_builder/controller_visual_mutations.py
 M machine-structure-editor/src/machine_builder/hardware_catalog.py
 M machine-structure-editor/tests/test_controller_board_fixtures.py
 M machine-structure-editor/tests/test_controller_palette_authoring.py
 M machine-structure-editor/tests/test_duet_2_maestro_heater_specs.py
 M machine-structure-editor/tests/test_duet_2_maestro_interface_specs.py
 M machine-structure-editor/tests/test_store_persistence.py
?? .vscode/launch.json

No files were staged. No commit or push was performed for this implementation or this documentation update.

Implemented files

- machine-structure-editor/src/machine_builder/canvas_palette.py
- machine-structure-editor/src/machine_builder/controller_visual_mutations.py
- machine-structure-editor/tests/test_controller_palette_authoring.py
- machine-structure-editor/tests/test_store_persistence.py

The five concurrent Board/catalog/Board-test modifications and root .vscode/launch.json were outside this implementation scope and were not edited by this workstream.

What changed

The component palette now includes a named "Duet 2 Maestro v1.0" option while preserving the generic Controller option. Its tooltip explicitly clarifies that choosing the V1.0 reference-board model does not verify the physical board revision.

The new board-backed mutation reuses add_duet_2_maestro_physical_interfaces() and project_controller_ports() instead of duplicating the documented connector/contact map. Definition registration, installed controller and canonical physical ports, machine membership, controller resources and relationships created by the helper, visual node linkage, and port projection occur inside one ModelStore mutation.

The installed controller references the reusable HardwareDefinition ID duet-2-maestro-v1-0. Its physical board revision remains marked as not verified as-built; the installed Controller version field is not used to assert that the physical board is V1.0. The new-machine default name is "M3D Promega — Compound reference specimen (not verified as-built)".

The committed baseline's reusable definition carries its source provenance. The existing physical-interface helper initializes installed SemanticPort provenance lists as empty. This milestone preserves that behavior rather than inventing per-port evidence.

The connector-position count is source-state dependent. At the pre-J4-correction audit baseline (HEAD 8ce8102539f10a46d4d057934dfff7570cc92164), the layout contained 115 positions, including two synthetic bed-connector groups. After the J4 correction published in commit e85a1e38af74622de3a1b62cf1641af4b707fd26, the corrected definition's layout contains 111 positions. The implementation and test results recorded in this checkpoint were validated in the shared working tree after that correction and correspond to the 111-position layout.

Regression coverage added

- Named palette entry and reference-board revision caveat.
- Board-backed palette creation with definition identity, machine membership, physical port ownership/identity, and visual projection assertions.
- One-step undo and redo of the board-backed creation.
- Save/reopen of the selected HardwareDefinition and its provenance, installed controller identity/reference, specimen machine membership, canonical ports and their ownership, and visual node/port references.

Verification reported from the shared checkout

Focused palette/controller/persistence command:

67 passed in 0.56s; exit code 0.

Full repository suite:

830 passed in 4.27s; exit code 0.

Whole-working-tree git diff --check:

Exit code 0.

Scoped four-file git diff --check:

Exit code 0.

The whole-tree check printed Git line-ending notices for the concurrent Board-owned tests test_controller_board_fixtures.py and test_duet_2_maestro_heater_specs.py. They were notices that LF would be replaced by CRLF on a future Git touch, not whitespace-check failures. Those Board-owned files were not edited by this milestone.

These tests ran at HEAD 8ce8102539f10a46d4d057934dfff7570cc92164 against the shared working tree, which also contained the listed uncommitted Board/catalog changes. The results are recorded as reported checkout validation, not as a claim that the implementation was independently tested on a pristine checkout.

Scope boundary and disposition

This checkpoint adds one named board-backed creation path. It does not add a general catalog browser, change the canonical ontology, duplicate the Maestro port map, claim verification of the user's physical board revision, or alter Routing algorithms.

The four implementation/test files remain uncommitted pending Planning's separate commit-gate decision. No stage, commit, or push is authorized by this checkpoint.

Next action

Return the changed-file scope, baseline, edit metadata, full and focused test results, and whitespace-check outcomes to Planning for review. Do not stage or commit until Planning separately authorizes it.

# Checkpoint 25 - 2026-10-10 - Evidence-aware component and port provenance authoring

Purpose and disposition

Record the implementation and follow-up verification of user-facing editing for existing Provenance records on MachineComponent and component-owned SemanticPort. This uses the canonical schema and the existing mutation/store pattern.

Implementation

- Added a reusable six-field provenance editor for source, evidence_type, method, context, date, and notes, with add/remove evidence controls.
- Component and port detail dialogs return multiple provenance entries.
- Component and port mutations support provenance list replacement while retaining the existing append-one-record behavior.
- Canvas editing forwards provenance on component editing, component-owned port creation, and component-owned port editing.
- Generic components retain hardware_definition_id=None when hardware identity is unknown.
- Port IDs used in the regression tests are explicitly synthetic fixture identifiers; they do not assert real Promega connector/contact identity.
- The follow-up fix adds provenance_entries to UpdateSemanticPort, matching its apply method.
- No ontology entities, schema fields, catalog records, or automatic physical connections were added.

Verification on the follow-up run

Focused command: .venv\Scripts\python.exe -m pytest -q tests/test_provenance_details.py tests/test_component_authoring_ui.py tests/test_component_details.py tests/test_component_properties.py tests/test_port_details.py tests/test_port_properties.py tests/test_semantic_component_mutations.py tests/test_semantic_port_mutations.py tests/test_semantic_component_store_integration.py tests/test_semantic_port_store_integration.py tests/test_store_persistence.py tests/test_controller_palette_authoring.py

Focused result: 98 passed in 1.27s (exit 0).

Full command: .venv\Scripts\python.exe -m pytest -q

Full result: 834 passed in 3.23s (exit 0).

The initial checkpoint text failed git diff --check because of malformed whitespace on verification lines. Those lines were corrected. After the port mutation repair, the focused suite passed (98 passed in 1.27s, exit 0), the full suite passed (834 passed in 3.23s, exit 0), and both whole-worktree and staged git diff --check passed (exit 0) before follow-up commit 1b84f0f8e2451b31b8603fe7093cbf284ee6b62f.

# Checkpoint 26 - 2026-10-10 - Published Promega IR Z-probe reference connections

Purpose and disposition

Record the Planning-authorized completion of three manufacturer-documented reference connections between the existing IR Z probe role and the board-backed Duet 2 Maestro reference controller. This advances the Promega specimen integration; it does not verify the user's installed wiring or board revision.

Checkpoint timestamp, captured immediately before this handoff edit: 2026-10-10 18:24:00 -04:00

Repository and commit state

Commit: 3ba0253dc5231b822c23aa2b0eb19065ca0880cb

Subject: Model Promega IR probe reference connections

Git author timestamp observed in local history: 2026-10-10T18:10:48-04:00

The local post-push verification fetched origin and confirmed that origin/main matched this commit. The implementation and its new integration test were committed together.

What changed since Checkpoint 25

- Extended CreateConnection with optional connection provenance and conditional support for the documented_cable_label connection property. Existing callers retain their default connection-property set.
- Added an integration test that creates the established 14-role Promega specimen and extends its existing IR Z probe role through component-owned functional SemanticPorts.
- Resolved the board endpoints from the instantiated controller's canonical z-probe ports and their contact metadata; no duplicate Maestro ports or hardcoded controller identity were introduced.
- The probe-side functional ports retain connector_id=None and pin_id=None. Cable labels belong to connection properties and source evidence, not invented probe connector or pin identities.

The three published reference connections

- Cable lead S10 -> controller-owned Maestro z-probe contact position 1, pin label Z_PROBE_IN.
- Cable lead P5 -> controller-owned Maestro z-probe contact position 2, pin label GND.
- Cable lead S9 -> controller-owned Maestro z-probe contact position 4, pin label +3.3V.

Each SemanticConnection records its documented cable label and provenance from the Promega Duet Maestro Wiring guide (https://promega.printm3d.com/documentation/electronics/duet-maestro-wiring) and the #3 Controller/Board J28 crosswalk. The evidence explicitly qualifies these as manufacturer-documented reference wiring, not verified as-built.

J28 positions 3 (Z_PROBE_MOD) and 5 (+5V) remain unconnected in this reference mapping. This does not establish that those contacts are unused on every physical machine.

Verification reported from the local checkout

- Focused regression suite: 47 passed in 5.28 seconds.
- Full repository suite: 837 passed in 6.81 seconds.
- The integration test covers the 14-role specimen, canonical endpoint ownership, cable labels and provenance, unused contacts, undo/redo, and save/reopen persistence.
- The implementation commit's git diff --check passed. The handoff-only update must pass its own diff checks before it is committed.

These test results were reported from the user's local checkout before this handoff edit. They are not a new test run on this documentation-only change.

Physical and firmware scope boundary

The machine and installed Maestro board revision remain not verified as-built. These reference connections do not mean the IR probe is the active firmware-selected probing method: the reviewed Promega v1.0.1 configuration selects limit-switch probing while the IR alternative is commented out. No active firmware assignment was created by this milestone.

The following physical mappings remain unresolved and must not be inferred or wired speculatively by this workstream:

- P2/P4 extruder motor cable endpoints and joins.
- H2/H4 heater cable endpoints and joins.
- S8/S6 PT1000 sensor cable endpoints and joins.
- P9/P11 fan roles and endpoints.

The three IR-probe connections do not establish any of these additional mappings, and no other physical connections were added by this milestone.

Historical reconciliation and next action

This checkpoint advances the integration recorded by Checkpoints 23-25: physical connection metadata authoring, board-backed Maestro palette authoring, and evidence-aware component/port provenance authoring. Those checkpoints remain valid historical records of their respective baselines; their earlier scope limits are not rewritten as though they had observed this later commit. No earlier checkpoint or decision requires separate archival relocation for this incremental milestone, so HISTORICAL_DOCUMENT_ARCHIVE.md is unchanged.

Wait for #2's connector/contact representation validation result before expanding Board/contact modeling conventions. Planning will use that result to select the next narrowly scoped implementation milestone. Do not begin speculative physical wiring for P2/P4, H2/H4, S8/S6, or P9/P11 without a new explicit assignment.


# Checkpoint 27 - 2026-10-11 - Reusable Promega IR-probe reference wiring fixture

Purpose and disposition

Record the published reusable construction path for the three Promega IR Z-probe manufacturer-reference connections. This advances a testable reference-wiring slice, not a complete machine wiring graph or verification of the user's installed harness.

Implementation commit

Commit: 9f3626b5b3117c2aef691eec4b04ae9b863485d0
Subject: Add reusable Promega IR-probe reference wiring fixture

The published commit contains exactly:
- machine-structure-editor/src/machine_builder/promega_fixtures.py
- machine-structure-editor/tests/test_promega_ir_probe_connections.py

The publication output confirmed that local HEAD, fetched origin/main, and live remote main matched. The current repository baseline for this handoff update is 8c3e9902dd612877d71a66c1cd99077025b88cc6.

Implementation and coverage

- Extracted `add_promega_ir_probe_reference_connections(...)` into a reusable fixture.
- It reuses the specimen's role-only IR probe component, instantiated controller, controller-owned canonical contacts, and normal editor mutation path.
- It creates probe-owned functional ports without inventing probe connector/pin identities, and adds canonical physical connections with corresponding visual connections.
- It preserves deterministic IDs, documented cable labels, and evidence from the Promega Duet Maestro Wiring guide and the #3 Controller/Board J28 crosswalk.
- Tests cover endpoint ownership and identity, non-directional physical connection semantics, provenance, unused J28 contacts, undo/redo, and persistence.
- Full suite before publication: 838 passed in 8.07 seconds; staged whitespace check passed.

The three reference connections

- Cable lead S10 ↔ Maestro J28 position 1, `Z_PROBE_IN`.
- Cable lead P5 ↔ Maestro J28 position 2, `GND`.
- Cable lead S9 ↔ Maestro J28 position 4, `+3.3V`.

J28 positions 3 (`Z_PROBE_MOD`) and 5 (`+5V`) are not connected by this reference mapping. Their omission does not establish that those contacts are unused on every physical machine.

Evidence boundary

These are manufacturer-reference mappings, not observations of the user's installed harness. The installed controller revision, probe-side connector/pin identity, actual wiring, and active firmware probing selection remain unverified by this fixture. Persistence passed for this specimen; that does not establish universal catalog serializability or resolve the known integer-key persistence limitation for other records.

Next implementation increment: reusable assembly-side cable endpoints

`test_promega_assembly_labels.py` currently adds eight component-owned printed-label endpoints to the Compound mixing nozzle/tool assembly: P2/P4 (extruder motor cable labels), H2/H4 (heater cable labels), S8/S6 (PT1000 sensor cable labels), and P9/P11 (fan cable labels whose roles vary by printer). This useful behavior remains test-local rather than a reusable fixture path.

Extract and test reusable assembly-side endpoint authoring using the existing evidence and uncertainty metadata. Do not create physical connection edges to Maestro contacts or firmware resources until both endpoints and their mapping are adequately supported. Preserve assembly-variant uncertainty and the not-verified-as-built status.

UI inspection milestone

`MASTER_PLAN.md` Section 13 already records the user's report that crowded ports and unreadable labels prevented effective manual testing. Do not submit a duplicate intake. Revisit it at a dedicated GUI-inspection milestone, reproduce the symptom, then establish acceptance criteria before choosing spacing, grouping, filtering/layers, label placement, or other potential approaches. Do not interrupt this wiring increment with an unverified UI rewrite.

The SKR hardware spike and broad catalog schema/loader work remain deferred.

## 1. Promega X/Y Motor Reference Connections — Validated (2026-10-11)

**Classification:** Implementation and validation.

**Verified repository baseline:** `4d96f3d0bcaaade8524d3eb997e646d5fd954601` — Document directed fluid-transfer research contract.

**Durable destination:** `machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`; `machine-structure-editor/src/machine_builder/promega_fixtures.py`; `machine-structure-editor/src/machine_builder/mutations.py`; `machine-structure-editor/tests/test_promega_xy_motor_reference.py`; `machine-structure-editor/tests/test_promega_ir_probe_connections.py`; `machine-structure-editor/tests/test_connection_authoring.py`.

**Validation:** Python compilation passed. Focused tests: 14 passed in 4.61s. Full suite: 841 passed in 7.49s. `git diff --check` passed after this checkpoint was corrected.

**Publication:** Included in the dedicated #4-owned commit containing this handoff entry; the final commit identifier is reported in the durable milestone message.

## Durable update completed

1. Added the XY reference API and four cable-side contacts per axis, mating by documented positions to Maestro J9 / X MOT and J8 / Y MOT.
2. Updated `CreateConnection` to preserve supplied connection metadata while retaining default properties and blank-value normalization.
3. Added mutation-contract coverage and XY tests for metadata, provenance, save/reopen persistence, and numeric-suffix position fallback.
4. Restored the IR-probe implementation from the committed baseline before appending the separate XY helper.

## Findings preserved

1. The reference model maps mating positions 1–4 to documented board contacts B1, B2, A1, A2. This does not establish conductor order or internal motor wiring.
2. Wire-colour-to-contact mapping and motor-coil terminal mapping remain `not_established`.
3. Firmware drive assignment remains `not_established`; installed physical wiring remains `not_verified_as_built`.
4. Cable-side reference ports do not establish direct connections to motor terminals or prove the installed harness endpoints.
5. The focused tests cover the XY reference model, existing IR-probe connections, and connection-authoring metadata; the full suite passed.

## Recommended next steps

Resume manual GUI/connection testing against this bounded reference slice. Any extension to motor-coil terminals, wire-colour mapping, firmware drives, or installed harness endpoints requires specific documentary or as-built evidence.

### Promega J28 guide-view identity integration (2026-10-12)

**Status:** Bounded manufacturer-reference integration. The Board PCB identity
checkpoint is published at `8c7e94efa3f0d691bbd678ad836ea81a283335f8`.
Post-Board-checkpoint validation passed on the working tree with the Routing
code and test changes present, before this Routing slice was published.

#### Scope implemented

- The controller-board fixture assigns J28's controller-owned contacts an explicit
  `promega_diagram_view_position` and source-qualified
  `promega_diagram_view_source`. This guide coordinate is distinct from PCB pad
  identity and physical cable mating-face/cavity identity.
- `promega_fixtures.py` resolves J28 contacts through
  `_promega_diagram_view_position()`. The lookup requires both the guide-view
  position and the exact Promega guide URL; it does not derive that coordinate
  from `pin_id` or the port-ID suffix.
- The generic `_contact_position()` helper and existing XY motor helper are
  unchanged.
- The IR-probe helper creates three manufacturer-reference connections: S10 to
  `Z_PROBE_IN` at guide-view position 1, P5 to GND at position 2, and S9 to
  +3.3 V at position 4. J28 MOD at position 3 and +5 V at position 5 are not
  connected by this helper.

#### Regression coverage

- `test_promega_ir_probe_connections.py` covers source-qualified guide-view
  lookup, the three reference connections and their provenance,
  persistence/undo-redo behavior, and the unused MOD and +5 V contacts remaining
  unconnected by this helper.
- `test_controller_board_fixtures.py` checks the manually reviewed J28
  guide-position-to-PCB-pad crosswalk. It does not automatically parse the
  external KiCad source.
- `test_promega_xy_motor_reference.py` was included in the post-Board-checkpoint
  focused test command to confirm that existing XY helper behavior remains
  intact.

#### Post-Board-checkpoint validation

At local `HEAD` and `origin/main` both equal to
`8c7e94efa3f0d691bbd678ad836ea81a283335f8`, the focused command was run from
`machine-structure-editor` with `.venv\Scripts\python.exe -m pytest` over:

- `tests\test_controller_board_fixtures.py`
- `tests\test_promega_ir_probe_connections.py`
- `tests\test_promega_xy_motor_reference.py`

**Result: 33 passed in 5.73 seconds.**

The same interpreter then ran `python -m pytest -q` for the full suite:
**842 passed in 8.44 seconds.**

`git diff --check` returned 0 for the Routing paths, the complete unstaged
working tree, and the staged diff check. Git displayed line-ending warnings for
the two modified Python files, but the checks succeeded. There were no staged
paths at the time of that validation.

These results apply to the working tree tested after the published Board
checkpoint was integrated and before the Routing changes were committed. They
document that actual run and do not assert test results for later code changes.

#### Routing publication scope and next steps

Only these Routing-owned paths may be staged for this publication:

- `machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`
- `machine-structure-editor/src/machine_builder/promega_fixtures.py`
- `machine-structure-editor/tests/test_promega_ir_probe_connections.py`

Before committing, inspect the complete staged diff and exact staged path list.
Preserve the Planning handoff and `CHAT_WORKFLOW.md`, as well as all staged or
unstaged work belonging to other workstreams. After publication, verify local
`HEAD`, fetched `origin/main`, and live remote `main`.

#### Evidence and limitations

This is a bounded manufacturer-reference integration, not a complete machine
graph and not evidence of the user's installed wiring or verified as-built
connector mating. The Promega guide-view position is source-qualified
documentation identity only; it does not establish cable-cavity orientation.
The helper connects only the three documented IR-probe endpoints. Do not infer
additional connections, complete Promega wiring, motor-coil pairing, firmware
assignment, or E0/E1 motor-pad metadata from this milestone.

### Standard single-Z / J36-Z-A contact-correspondence gate (2026-10-12)

**Status:** Held at the source-evidence gate. No Z-A cable-to-board connections are created by this finding.

**Planning authorization:** A bounded standard single-Z reference slice is authorized for four source-supported reference connections to J36/Z-A. J7/Z-B is outside this slice.

**Research finding:** The reviewed official Promega wiring guide and related manufacturer diagrams identify the intended Z-motor cable by its coiled construction and establish its assembly-level destination at the Z bed motor and board connection. They do not establish the numbered four-contact order of the cable relative to J36/Z-A fixture positions, nor a defined mating-face/cavity convention linking the cable side to the controller-side positions.

**Controller-side reference map:** The Board fixture supplies the following source-backed J36/Z-A fixture-position mapping:

| Z-A fixture position | PCB reference | PCB pad | Reference net |
|---:|---|---:|---|
| 1 | J36 | 3 | `Z_MOT_B1` |
| 2 | J36 | 4 | `Net-(J36-Pad4)` |
| 3 | J36 | 1 | `Z_MOT_A1` |
| 4 | J36 | 2 | `Net-(J36-Pad2)` |

This identifies the controller-side PCB pads and nets. It does not identify which cable-side contact mates with each fixture position.

**Required evidence to release the gate:** An authoritative, applicable source must identify the Z-cable contact numbering and orientation and establish its correspondence to J36/Z-A. A specimen-specific continuity inspection could document the installed machine, but must be recorded as as-built evidence rather than generalized into a source-backed reference mapping without further authority.

Do not infer the missing mapping from XY symmetry, cable appearance, wire colours, connector shape, PCB pad ordinals, or motor-coil assumptions. Do not create direct motor-terminal connections or infer coil pairing, firmware drive assignment, installed harness identity, or as-built connectivity. Keep J7/Z-B outside the standard single-Z slice.

**Independent reconciliation:** The accepted J28 reference slice and existing XY reference slice remain closed and unchanged. The current supplied evidence does not establish another new connection slice with a sufficiently supported complete endpoint mapping to implement here. Variant-sensitive P4/P2, H2/H4, S8/S6, and P9/P11 relationships remain unresolved where their applicable contact mappings are not established.

**Board checkpoint:** The published J34/E0 STOP PCB identity crosswalk is included at `287a1489a53dc695d5dc5a55defd795151de3719`. Its existing `e0-stop` SemanticPort IDs are preserved; fixture position 1 maps to J34 pad 3 (`E0_STOP_CONN`), position 2 to pad 2 (`+3.3V`), and position 3 to pad 1 (`GND`). These are PCB reference identities, not cable-cavity or as-built wiring evidence.

**Overall readiness:** Promega wiring readiness remains **BLOCKED** pending the remaining endpoint and connection coverage, provenance, persistence, version-qualified firmware relationships, and physical/as-built evidence.

### DYZE Cooling Unit tubing bend radius and protection capability correction (2026-10-13)

**Evidence:** DYZE Technical Support response received October 13, 2026.

**Specified tubing bend radius:** For the supplied soft, high-temperature rubber tubing, 1/4-inch ID × 3/8-inch OD, the minimum bend radius is 2 inches (50 mm), never smaller. DYZE specifies the measurement to the tubing's outside diameter (OD). Preserve this OD-based wording rather than substituting a centerline or inner-wall radius. The stated minimum applies both while stationary and while moving.

**Blockage detection and automatic pausing:** These are not features of the current Cooling Unit. DYZE states that the claim originated in an earlier prototype and is being corrected; the feature was removed because of false positives and inadequate reliability. Do not model or describe the current product as detecting a blockage or automatically pausing a print.

**Evidence limits and routing implications:** The support response does not establish dynamic-flex cycle life or additional temperature or pressure ratings. Do not infer those ratings. Any machine-level coolant-loss or blockage protection is a separate requirement that must be based on separately established hardware and control capabilities; it is not supplied by an undocumented Cooling Unit sensing function.

### Promega extruder/fan harness and RRF configuration evidence gate (2026-10-13)

**Classification:** Research/Board evidence update for Routing. Preserve unresolved mappings; no schema or ontology change is proposed.

**Fan harness — P9/P11:** The manufacturer extruder-assembly wiring guide says nozzle-fan assignment to P9 versus P11 varies by printer. The companion fan guide identifies the cold-section fan as 24 V and intended for the Duet Maestro always-on port, while nozzle fans are 5 V and PWM-controllable. The manufacturer warns that routing a nozzle fan to the cold-section output can destroy nozzle fans. Do not create a universal P9/P11-to-function mapping. Establish the actual harness lead by continuity inspection or direct, applicable board-side evidence before asserting routing.

Source:
- https://promega.printm3d.com/documentation/electronics/extruder-assembly-wiring

**Heater and thermistor harness — H2/H4/S8/S6:** The older silver assembly's documented arrangement places H4/S8 on the left and H2/S6 on the right. This is variant-specific evidence and must not be transferred automatically to the newer black assembly. The new-assembly guide identifies connector roles but warns that the S8/S6 image wire colors are wrong and H4 must follow the corrected route. The separate installation guide documents left/right routing crossovers for Compound and K'Tana. Together, these sources do not establish a complete revision-qualified new-assembly label-to-component map. Preserve the cable-to-component edges as unresolved unless the applicable assembly is identified and stronger source or physical-trace evidence becomes available.

Sources:
- https://promega.printm3d.com/documentation/electronics/extruder-assembly-wiring
- https://promega.printm3d.com/repair-and-maintenance/install-uninstall/extruder

**Firmware configuration:** The publicly visible SD-card releases distinguish old and new cable assemblies, but the reviewed files are historical examples: Compound `devel` is dated January 16, 2019, and K'Tana is dated October 1, 2018. They use `M667 S1`, which the official RRF changelog says is unsupported from RRF 3.5.1 onward. They are not verified RRF 3.5.4 configurations and must not establish current fan or heater assignments. The necessary evidence is the actual installed SD-card configuration set, including `config.g`, override files, nested system-file calls, and relevant tool macros; the Board workstream has not yet inspected that installed set.

Source:
- https://github.com/PrintM3D/Promega

**Routing disposition:** Retain the validated X/Y reference slice. Do not expand physical extruder/fan connections based solely on older assembly documentation or historical firmware examples. Keep unsupported cable-to-component edges unresolved until the applicable variant and its mappings are substantiated. J34, J28, and the held Z-A contact-correspondence gate remain unaffected.

## X Motor Functional-Interface Acceptance Closeout (2026-10-15)

**Implementation base checkpoint:** `5e235be1232d9b42f2c50a4018160e9740205798` — Add generic motor functional interface workflow.

**Formal acceptance:** #5 reported **ACCEPTABLE for all seven acceptance criteria** at checkpoint `a84526b28237d1e678a044c534cc9e8ad6a80444`. Acceptance report: `MB-20261015-1553-02`. This is the bounded X Motor functional-interface workflow; it is not approval of complete Promega wiring readiness. The acceptance report must not be described as evidence that #5 independently reran #4's automated tests.

### Criterion 4 — Preserve existing J9 contact connections

`tests/test_functional_interface_connection.py::test_interface_drag_creates_reference_scoped_connection` creates the four existing X-motor cable-to-J9 reference connections before adding the functional-interface relationship. It verifies that adding the relationship does not replace or mutate the existing contact or connection records.

### Criterion 6 — Presentation-only focus and undo/redo

`test_interface_focus_preserves_contacts_and_persistence` verifies that connector-focus changes preserve canonical ports and connections, visual connections, undo/redo stack depths, and the modified flag. The functional-connection test separately verifies restoration of the prior semantic and visual records during undo/redo.

### Criterion 7 — Acceptance and subsequent visual follow-up

#5's recorded disposition remains ACCEPTABLE for the bounded workflow. The following GUI observations are user-reported; they are not independent reproductions and do not silently redefine the historical acceptance decision.

**Earlier observations retained from the original closeout:**

- The user dragged between the controller functional endpoint and generic Motor endpoint, confirmed the UNKNOWN-compatibility prompt, accepted the physical-connection details dialog, and observed a visible functional relationship.
- In J9 contact focus, the four individual contacts were visible while the functional relationship remained anchored at the hidden connector-level endpoint and appeared detached.
- Detailed-port view made the Maestro node very tall and repeated labels crowded.
- After saving and reopening, the machine nodes/data returned, but viewport pan/zoom did not. Viewport persistence remains separate work.

**Latest follow-up observations:**

- The user sees `Motor electrical interface` as the motor-side port to which the Maestro connection goes.
- When switching from Function to Detailed view, the single visible Maestro-side port on the right still appears connected to one of the many motor-side ports on the left that match by function.
- GUI verification still needs to confirm that the wire lands at the tip of the highlighted Maestro connector cone while retaining the intended motor functional-interface attachment, and that the connector labels and cone restore correctly after focus changes.
- Whether the detailed-view edge presentation misleadingly suggests an arbitrary one-to-many motor-port choice remains unresolved.
- The connector-group/enclosure/cone visual changes are published in commit `58301ceca0f1788f4b44aa08ee4ca0f2cb4fdd6a`; GUI verification remains outstanding. Automated tests do not substitute for this GUI verification.

### Connector-group cone and Function-to-Detailed visual integration — current status (2026-10-18)

**Design intent and scope**

The long-term visual-builder goal is progressive detail down to inspection of individual wires. The current experiment is narrower: represent a connector or harness group with a cone leading to its individual ports, exposed through the per-port `Port detail` selection. The interaction model remains exploratory. This is not an implemented true zoom mode, and a cone appearing or disappearing with a selection must not be documented as zoom-driven detail navigation.

This feature is presentation-only. It must preserve the canonical `SemanticPort` identities and connection relationships. A connector-level functional relationship is not proof of individual-contact continuity, conductor mapping, physical wiring, or firmware correctness. View filtering must not mutate the semantic model.

**User-reported design input — preferences, not verified guarantees**

The following observations and preferences were supplied by the user and are retained as such:

1. **Labels inside the part/connector enclosure:** The user thinks labels beside their ports inside the box may be easier to read than the current sequence of part box, port circle, wire, and label overlapping the wire. This is a visual preference to implement and assess, not an accepted result.
2. **Functional/detailed alignment:** The user noticed detailed ports on the left side of the controller that appear to line up with functional ports directly across the controller. The user likes this if intentional. Whether the alignment is intentional and stable remains to be verified; it is not a guaranteed architectural rule.
3. **Functional wire relationship:** The user reports that the Maestro wire still connects to the motor's `Motor electrical interface` in the usual view. That observation does not establish that the wire remains visible and correctly attached in every focused view.
4. **J9 Contacts observation:** The user reports that the cone is visible only when `J9 Contacts` is selected. On selecting it, the wire disappears; the functional port appears unlabelled; the cone appears within the Maestro board, beginning some distance past the functional port; and the triangular area expands to a contact box that overlaps the board. The contact ports appear aligned with the board edge underneath the breakout box rather than with the breakout-box edge. This is reported GUI behavior and remains an unresolved rendering defect.
5. **Preferred spatial relationship:** From the side where the wire approaches, the desired reading order is `Part → Port → Wire → Cone → port list aligned with the controller edge → port labels`. The labels do not have to occupy a large independent box if a smaller layout is legible.
6. **Zoom observation:** The user reports that zooming in or out while `J9 Contacts` is selected does not visibly change the cone or other visible presentation. No zoom-responsive behavior has been accepted.

**Published implementation and exact source/test paths**

- Implementation commit `58301ceca0f1788f4b44aa08ee4ca0f2cb4fdd6a`, subject `Integrate connector-group cone routing and focus presentation`.
- Prior handoff reconciliation commit `2ec026cbee3a696446661b7edd1326c953865837`, subject `Reconcile Routing workstream handoff after visual integration`.
- Current checkpoint verified before this handoff edit: `HEAD`, `origin/main`, and live remote `main` all equal `3a1421af82b8d1dfa8e0c95f53f155135e0c4b3d`.

Relevant implementation paths:

- `machine-structure-editor/src/machine_builder/canvas_ui.py` — `Port detail` choices, focus filtering, semantic connector/contact lookup, and deciding when to provide connector-group overlay information.
- `machine-structure-editor/src/machine_builder/canvas_scene.py` — connection endpoint lookup and routing connections to the connector-group anchor.
- `machine-structure-editor/src/machine_builder/graphics/connection.py` — routed connection path and endpoint-side overrides; connection graphics use a negative z-value and are drawn behind nodes.
- `machine-structure-editor/src/machine_builder/graphics/node.py` — focused-port layout, connector enclosure/title, cone geometry, anchor, and overlay bounds.
- `machine-structure-editor/src/machine_builder/graphics/port.py` — individual port label placement and text positioning.
- `machine-structure-editor/tests/test_functional_interface_connection.py` — functional-interface, contact-focus, connection, anchor-geometry, label, and persistence regression coverage.
- User-used GUI fixture: `machine-structure-editor/wiring test machines/Maestro and motor test.machine.json`.

At the inspected checkpoint, the selector contains `Functional interfaces`, `Detailed ports (all nodes)`, and connector-specific interface/contact selections. The requested `Detailed ports (unused nodes)` and `Detailed ports (used nodes)` options are not yet present in the inspected implementation; they remain a requested enhancement, not a completed feature.

The current cone path is created by `_update_connector_group_overlay()` in `graphics/node.py`. Its tip is placed a fixed 112 scene units away from the connector enclosure, and the direction is currently derived from the connected node's horizontal location. `canvas_ui.py` supplies the connector-group overlay only for the `contacts` focus mode. Those code paths are relevant to the observed missing cone in other views and possible incorrect placement inside the board. They are implementation evidence and a basis for the next correction, not proof of the sole cause of the disappearing rendered wire.

**Automated test evidence and its limit**

Before the current rendering follow-up, the reported pre-commit run of `tests/test_functional_interface_connection.py` and `tests/test_promega_xy_motor_reference.py` passed **6 tests in 11.07 seconds**. The existing functional-interface test checks that the connection graphics item is visible in its test state and that the routed path endpoint equals the computed cone-tip anchor.

That assertion establishes geometric agreement between the path endpoint and the anchor in that test state. It does **not** prove that the wire is visibly rendered in the GUI, that the tip is outside the controller rectangle, or that the wire is not hidden by a node or overlay. The user's report that the wire disappears therefore remains valid contrary evidence to visual acceptance. The earlier test count is historical and does not validate any subsequent, unexecuted rendering changes.

**Latest local implementation checkpoint (2026-10-18, unpublished)**

- The dropdown/filter changes in `canvas_ui.py` and the matching selector assertion in `tests/test_functional_interface_connection.py` passed 6 tests in 11.47 seconds before the label-layout edit.
- The subsequent label-layout edit changed `graphics/port.py` and added a label-position assertion. The next focused run failed during test collection because `)    def _position_status(self) -> None:` was joined on line 345. Both test modules reported collection errors; no tests ran on that malformed snapshot.
- Local #4 implementation paths: `machine-structure-editor/src/machine_builder/canvas_ui.py`, `machine-structure-editor/src/machine_builder/graphics/port.py`, and `machine-structure-editor/tests/test_functional_interface_connection.py`. This handoff is also locally modified. The cone/breakout geometry in `graphics/node.py` has not yet been changed.
- Syntax repair: py_compile passed; focused suite passed with 6 passed in 11.77s. Next: continue the connector breakout/cone geometry in graphics/node.py and strengthen its boundary assertions; GUI acceptance remains open.
- Publication remains queued: keep these changes unstaged and do not commit or push until Planning grants #4 an explicit publication slot.
<!-- MB4_RECOVERY_PROMPT_CHECKPOINT_START -->
### Manual GUI acceptance checkpoint — 2026-10-19, post-restart review

#### Automated baseline before this manual review
- Python compilation passed.
- Focused regression suite: 96 passed in 2.92 seconds.
- `git diff --check` passed; Git emitted only its LF-to-CRLF conversion warning.
- These automated results do not constitute manual acceptance. The GUI review below found remaining defects.

#### User-observed behavior after saving, closing, and reopening
- The saved test artifact is `machine-structure-editor/Maestro and 4 port motor test.machine.json`. It is user-owned diagnostic data. Preserve it; do not edit or overwrite it as part of code changes.
- On reopening, the camera did not restore the prior framing. Pressing `F` brought the parts back into view, but the focus selector returned to Functional interfaces. The selected J9 Contacts view did not return automatically.
- Deleting the last connection also caused the selector to return to Functional interfaces. Undo restored the connections but did not restore J9 Contacts focus.
- After reopening, the Functional interfaces and J9 interface views both showed a single gray functional-reference line. Controller/motor rectangles appeared wider than the user remembered; treat the size change as an observation to investigate, not a confirmed persistence defect.
- Detailed ports (all) showed overlapping black, red, and gray routes. Red appeared on top and obscured the other lines; labels on opposite sides of the Maestro were difficult to distinguish.
- The user deliberately created temporary black/red connections to identify the repeated-function controller ports. These exploratory links are not evidence of actual wire-to-contact mapping, coil pairing, or as-built connectivity.
- Detailed ports (unused) hid connected ports and their lines; Detailed ports (used) restored the connected ports and connections. Confirm the intended per-port filter contract and make sure lines do not remain visible when their endpoints are hidden.
- Wire hit testing/selection was unreliable when paths overlapped: clicking selected the wrong line, clicking above the visible line sometimes selected the intended one, and selecting an overlapping line made it difficult to select another. Investigate path overlap, click shape, and selection behavior together.
- In J9 Contacts view, the cone was finally on the correct side of the Maestro—positive progress. However, the breakout enclosure overlapped the board title, was too high/off-center, and floated across the board's left boundary. Adjust it so its edge is deliberately aligned to the controller-board boundary or kept completely inside it, without covering the board title.
- Individual orthogonal paths from X Motor lead endpoints still routed directly to B1/B2 and did not visually fan into the connector cone/harness area. The cone represents the bundled-wire transition when conductor detail is absent; with conductor paths present, those paths should visually pass through/under the bundle region rather than ignore it. Do not change the canonical endpoints merely to obtain this appearance.
- Screenshot supplied by the user: https://github.com/PeterTremonti/Machine-Builder/blob/main/machine-structure-editor/screenshots/Screenshot%202026-10-19%20170905.png

#### Canonical-model and visual-behavior boundaries
- The canonical connection/functional-interface relationship is semantic truth. Connector focus, selection, highlighting, visibility and cone display are presentation state. Connection paths and cone anchors are routing/rendering geometry.
- A functional-reference connection must remain distinct from individual conductor connections. It must not be counted as an additional physical wire. In contact focus, prefer a visual bundle/cone representation when detailed conductors are present without mutating or silently remapping the canonical model.
- The cone direction must derive from the selected controller contact side, not from whether the motor component happens to be left or right of the board.
- Preserve the generic motor functional interface and the four opt-in stepper lead endpoints. Remove obsolete provisional ports only when unused; preserve any endpoint that already has a connection. Do not automatically connect terminals.
- Wire color must derive from canonical physical connection details (`SemanticConnection.properties["wire_color"]`). Distinct coincident routes still need understandable rendering and selectable hit targets; a color field alone does not solve overlapping paths.

#### Physical Promega observations to preserve
- Y MOT is at the upper-left rear when viewed from the front of the printer toward the rear.
- X MOT is at the upper-right rear, opposite Y MOT.
- The Z motor is underneath and mounted to the moving bed.
- X MOT and Y MOT pigtail wire order: Black, Green, Red, Blue, viewed into the motor harness connector from the board-side viewpoint described by the user.
- ZA pigtail order: Blue, Red, Green, Black, looking into the female connector from the board's viewpoint.
- ZB has no motor harness connected. The two contacts marked `1` are jumpered together and the two contacts marked `2` are jumpered together.
- These are physical observations only. They do not by themselves establish contact numbers for the motor leads, coil pairing, or firmware assignment.

#### Research reference from #2
- Message ID: `MB-20261019-1638-01`, dated 2026-10-19 16:38 EDT.
- Mitchell 1 ProDemand and ALLDATA are UX references for interactive wire highlighting/tracing, not routing standards or authority for Machine Builder connection semantics.
- Keep the architecture boundary: canonical relationships are semantic truth; selection/highlighting/focus/cone visibility are presentation state; path/endpoint anchors are routing/rendering geometry.
- The reference is bounded UX guidance, not authorization to expand the ontology or redefine canonical connection semantics.

#### Next implementation/acceptance priorities
1. Fix wire overlap, path hit testing, and selection so the visible wire corresponds to the line selected. Use distinct, comprehensible routes when multiple conductors share portions of a path.
2. In J9 Contacts view, keep the cone on the contact side and align the breakout to the board boundary/title. Make conductor paths visually enter/fan through the cone bundle, while preserving each actual contact-to-terminal connection.
3. Keep the gray functional reference visible as the functional-interface abstraction in the functional view. Do not show it as an additional conductor when detailed conductor paths are being represented in contact focus.
4. Keep port-detail filtering per port. A connection with a hidden endpoint should be hidden unless a visible connector cone intentionally substitutes for that endpoint.
5. Preserve connector focus and camera/framing across connection deletion and undo/redo. Investigate whether saved view focus and framing should be persisted on save/reopen; the user expects to return to the working view rather than lose it.
6. Verify label readability in detailed views and the connector breakout's position after focus switches, save/reopen, and undo/redo.
7. Add focused regression coverage for the reported GUI behavior. Re-run manual acceptance after the fixes; 96 passing tests are the baseline before this GUI review, not acceptance of these remaining issues.

Do not infer physical mapping from the exploratory wires. No files staged, committed, or pushed.

### Contact-specific connector-cone landing checkpoint — 2026-10-19
- Functional-interface connections retain the single cone-tip anchor. Contact-level connections can resolve individual semantic contact IDs to distinct, deterministic landing points along the cone outline. This is rendering geometry only; canonical endpoints and physical wiring evidence are unchanged.
- `canvas_ui.py` includes contact semantic IDs in connector presentation data. `graphics/node.py` resolves the group tip and contact-specific anchors. The regression test `test_contact_focus_routes_contacts_to_distinct_cone_landings` covers two contact wires and their separate rendered endpoints.
- Validation: focused functional-interface, connection-routing, wire-color and stepper-terminal suite passed (73 tests); source compilation passed; `git diff --check` passed after removing the reported surplus EOF blank line in `tests/test_connection_routing.py`.
- This is automated validation, not manual GUI acceptance. Multi-wire readability, enclosure placement, overlapping-wire selection, focus retention through delete/undo/redo and reopen, and camera restoration remain open.
- Current publication state: no #4 publication has occurred. The latest observed staged-path list was empty; preserve all other workstreams' unstaged changes. Obtain explicit Planning authorization before any future publication.


### Latest GUI acceptance — user report, October 19, 2026
<!-- MB4-GUI-ACCEPTANCE-POST-CONE-LANDING -->

- **Routing:** red X Motor endpoint 2 now approaches the cone's small end, but black endpoint 1 still ignores the cone and follows its previous route. Check the actual selected anchor and rendered endpoint for each connection.
- **Harness appearance:** the desired view has individual conductors taper into a cone, disappear within the bundled harness span, emerge separately at the second cone, and taper to connected terminals. A complete two-ended bundle representation has not been achieved.
- **Breakout position:** the enclosure still overlaps the Maestro board label; no meaningful placement change was observed.
- **Wire selection:** black, red, and gray wires are individually selectable in the upper-left area. Below the board, the red wire's selection region prevents selecting the other wires.
- **Focus:** deleting all connections resets the selector to Functional interfaces. Undo restores connections but does not restore the previous focus.
- **Save/reopen:** parts are outside the visible viewport after reopening. Pressing F reveals them, but their positions appear shifted. Compare saved and loaded node coordinates separately from camera framing; the apparent shift is not yet proven to be a coordinate change.
- The user report ended with an empty item 6, so no additional finding is inferred.

The most recent automated result remains 73 focused tests passed in 2.39 seconds. Source compilation passed. The most recent successful whitespace check preceded this documentation refresh. These results do not close the GUI acceptance gaps above.

Preserve the user-owned project `machine-structure-editor/wiring test machines/Maestro and 4 port motor test.machine.json` exactly. Its diagnostic black/red links are not proof of physical harness wiring, motor-coil pairing, or contact mapping. Keep canonical contact-to-terminal connections distinct from the functional-interface abstraction. The cone/harness remains presentation geometry unless a separate semantic design is authorized.


### Redundant functional-link presentation filter — 2026-10-20
<!-- MB4-REDUNDANT-LINK-FILTER-20261020 -->

- Added a presentation-only filter in `canvas_scene.py`: in connector-contact focus, a contact-to-motor-functional-interface line is hidden when that same contact also has a direct connection to a physical terminal on the same component.
- The filter does not delete, rewrite, or remap semantic or visual connections. Detailed-all view is expected to retain access to both stored relationships.
- Added regression coverage in `tests/test_functional_interface_connection.py` for the redundant functional link and direct terminal path.
- Validation reported by the user: focused functional-interface, routing, wire-color, and stepper-terminal suite **74 passed in 3.54 seconds**; source compilation passed; `git diff --check` passed. No staging, commit, or push occurred.
- Manual GUI acceptance is still required. Verify the black and red wires, connector-cone/harness appearance, breakout-box placement, overlapping-wire selection, focus after delete/undo/redo, and save/reopen framing/focus. The code change is not accepted solely from automated tests.
- Preserve the saved diagnostic project `machine-structure-editor/wiring test machines/Maestro and 4 port motor test.machine.json` exactly. Its links do not prove physical wiring or coil mapping.


<!-- MB4-GUI-ACCEPTANCE-20261020-02 -->
- Manual GUI acceptance report (2026-10-20 17:09 -04:00): **BLOCKED — visual and view-state issues remain**.
- J9 Contacts: gray path appears to run from the X motor functional interface to the Maestro breakout cone tip; red from endpoint 2 stops just above that point; black from endpoint 1 passes near the cone tip, travels between B1 and B2, and ends around the upper-middle cone edge. The expected contact-focus suppression is not visually demonstrated; verify connection/port IDs before altering the filter.
- Detailed ports (all nodes): three apparent X-motor paths; gray is obscured by red until endpoint-2 height, then becomes visible toward the right-side Maestro port. The upper black path cannot be selected over/around the top of the board; clicking that area selects the red B2 path. Investigate geometry and hit-test overlap together.
- Breakout placement: J9/X Motor box remains too far left/up, overlaps the board border, and obscures the Maestro label.
- Focus: deleting all connections switches to Functional interfaces; undo/redo does not restore J9 Contacts.
- Reopen: a file saved in J9 Contacts opens in Functional interfaces with parts outside the visible canvas toward the upper right. Compare serialized node coordinates against viewport/camera restoration; do not conflate them.
- Diagnostic-project wire colors and terminals remain exploratory, not evidence of as-built wiring, coil mapping, or physical truth.

<!-- MB4-GUI-REVIEW-20261020-05 -->
- GUI acceptance remains BLOCKED (2026-10-20 18:42 -04:00).
- J9 Contacts: gray functional-interface route reaches the cone tip; red endpoint 2 ends just above it; black endpoint 1 passes near the cone tip, crosses between B1 and B2, and ends near the upper-middle cone edge.
- Detailed ports: gray is obscured by red until near endpoint-2 height. Clicking the black path above/around the Maestro board selects the red B2 path.
- Breakout overlay still overlaps the left board border and covers the Maestro label.
- Delete-all resets focus to Functional interfaces. Undo does not restore J9 Contacts. Reopening the saved J9 Contacts file selects Functional interfaces and leaves parts outside the viewport at the upper right.
- Project mapping verified: visual connection-1 is gray connector-level to motor functional interface; connection-2/3 are contact-to-functional-interface links; connection-4/5 are black/red direct contact-to-unassigned-motor-lead links. Visual-port semantic references map to the intended endpoints; shared IDs alone do not establish an ID collision.
- Investigate routing geometry and hit testing together; handle breakout placement separately. Trace focus through delete/undo/redo and project-open framing separately from serialized node coordinates.
- Last reported automated validation: 74 focused tests passed; compileall and git diff --check passed. These results predate the unresolved GUI acceptance observations.
- The diagnostic project is exploratory and does not establish as-built wiring or coil mapping.

<!-- MB4-LOAD-FRAMING-20261020-01 -->
- Load-framing increment (2026-10-20 18:52 -04:00): added a load-generation marker to ModelStore and schedules _frame_all() on the next Qt event-loop turn when a document load is detected. This is intended to frame loaded contents after scene synchronization; manual GUI verification remains outstanding.
- Added regression test `test_loading_document_schedules_canvas_framing`.
- Validation: four focused suites reported **75 passed in 2.38 seconds**; `compileall` passed; `git diff --check` returned exit code 0. Git reported an LF/CRLF advisory for the test file, not a whitespace error.
- The change does not persist the selected controller-focus choice or camera state. Those remain separate open presentation-state tasks.
- Manual GUI acceptance is still required: reopen the saved diagnostic project and verify the parts are visible immediately, then check wire overlaps/selection, connector overlay placement, and focus through delete/undo.

<!-- MB4-CONDITIONAL-GRANT-CLOSEOUT-20261020-01 -->
- Conditional publication grant closeout (2026-10-20 20:53 -04:00): BLOCKED - SLOT RELEASED.
- Required full suite reported 868 passed in 7.92 seconds, but the pytest process returned Windows exit code -1073740791 (0xC0000409). Do not classify this gate as clean until the abnormal process exit is understood.
- Isolated diagnostics exited cleanly: load-framing regression 1 passed; canvas scene tests 5 passed; Board-owned stepper terminal test 4 passed. The Board test remains excluded from #4 staging and commit.
- Source compilation passed and git diff --check returned exit code 0. A Git LF/CRLF advisory was seen for the modified functional-interface test.
- GUI acceptance is still outstanding after the load-framing patch: verify parts appear immediately on reopen without pressing F; assess fan-out readability, box/title placement, overlapping-wire selection, focus, undo/redo, delete, and saved-file reopen behavior.
- The complete coherent 17-path diff review and a clean full-suite process exit have not been established. No files were staged, committed, or pushed under this grant.
- The stepper-terminal mutation and Board dependency require a renewed validation/publication decision after the full-suite process exit is resolved. Keep tests/test_stepper_motor_terminal_profile.py Board-owned and excluded from #4 publication.
<!-- MB4_RECOVERY_PROMPT_CHECKPOINT_END -->

**Acceptance gaps — still open**

- Establish why the connection is not visibly rendered in `J9 Contacts`; verify route endpoint location against the actual controller and breakout geometry, not only against the calculated anchor.
- Put the cone on the side facing the actual focused contact list, and ensure its tip is outside the controller body when it represents the external incoming/outgoing wire relationship.
- Rework the contact breakout geometry so contact ports align with its intended edge and the overlay does not obscure the board unnecessarily.
- Improve the label layout, including restoring original labels correctly after changing focus.
- Verify view switching and focus changes for the functional interface, all-detail, connector-interface, and contact views.
- Determine whether detailed controller ports are intentionally aligned with opposing functional interfaces.
- Implement and test the requested used-node and unused-node detail filters without changing canonical semantics.
- Treat the reported zoom behavior as unresolved. Decide separately how a future progressive-detail/true-zoom interaction should work; do not claim the current selection experiment implements it.
- Complete manual GUI acceptance only after the rendering correction is in place. Automated geometry assertions and GUI inspection are separate acceptance evidence.

**Current next action and publication boundary**
- Publication authorization MB-20261020-2045-02 is closed as BLOCKED - SLOT RELEASED because the full pytest process returned -1073740791 after reporting 868 passed, and GUI acceptance remains unverified.
- Before any new publication request, diagnose the full-suite process exit; retain isolated results (load framing 1 passed, canvas scene 5 passed, Board-owned stepper test 4 passed) as supporting evidence only.
- Manually verify load framing after reopening the saved diagnostic project, then assess fan-out readability, connector-box placement, overlapping-wire selection, focus persistence, delete/undo/redo, and reopen state.
- Complete and review the entire authorized #4 diff as one batch, including validation/state-update/persistence behavior for UpdateMachineComponentWithStepperTerminalProfile. The Board-owned stepper test must remain excluded from any #4 commit.
- No stage, commit, or push under the released grant. Request a new explicit Planning authorization against the then-current baseline after all required gates pass.
### Automated validation — results reported by #4

**Original closeout validation (historical; implementation base `5e235be1232d9b42f2c50a4018160e9740205798`, before the closeout publication):** focused tests — 6 passed in 10.21s; full suite — 847 passed in 31.76s. These original timings are retained as historical records, not as validation of the later connector-group visual changes and not as independent test runs by #5.
These historical validation results were measured against a working tree based on `a84526b28237d1e678a044c534cc9e8ad6a80444`, before visual-integration commit `58301ceca0f1788f4b44aa08ee4ca0f2cb4fdd6a`. They are #4's results, not independent #5 test runs.

- Visual-focused command: `.venv\Scripts\python.exe -m pytest -q --tb=short tests/test_functional_interface_connection.py tests/test_promega_xy_motor_reference.py` — previously reported 6 passed in 11.57s.
- Latest bounded source/controller/mating/persistence baseline — 96 passed in 4.34s across `test_controller_board_fixtures.py`, `test_hardware_catalog.py`, `test_octopus_driver_mating.py`, `test_semantic_relationship.py`, `test_semantic_relationship_queries.py`, `test_persistence.py`, `test_store_persistence.py`, and `test_promega_xy_motor_reference.py`.
- Latest full-suite command: `.venv\Scripts\python.exe -m pytest -q --tb=short` — 847 passed in 38.91s.

These results document the tested working tree. They do not constitute the still-missing SKR-specific identity and persistence tests, and automated results do not substitute for GUI inspection.

## Bounded Connector/Contact Validation — SKR EXP1 Revision Accepted; Independent Evidence Gates Open (2026-10-17)

**Disposition:** Research's review of the requested bounded SKR Mini E3 V3.0 EXP1 revision is **ACCEPTABLE** (`MB-20261017-0009-02`). This acceptance is limited to the bounded fixture, source inventory, identity, evidence-preservation, and persistence scope. The original proposal is `MB-20261015-1154-01`. The review and disposition lineage is:

- Planning's bounded-work assignment: `MB-20261015-2142-02` and `MB-20261016-0024-01`.
- #4's evidence review to #2: `MB-20261015-1836-01`; #4's disposition to #1: `MB-20261015-1836-02`.
- Research's corrected source inventory: `MB-20261016-1755-01`.
- Research implementation review: `MB-20261017-0009-02` — ACCEPTABLE for the requested bounded revision.
- Planning's reconciled source instructions: `MB-20261016-1806-01`.
- Planning's Routing-handoff recovery request: `MB-20261016-1808-03`.

### Existing API and implementation paths

- `machine-structure-editor/src/machine_builder/semantic_model.py`: `SemanticPort` already supports controller ownership, connector grouping, `pin_id`, properties, and provenance; this bounded implementation requires no ontology expansion.
- `machine-structure-editor/src/machine_builder/controller_board_fixtures.py`: added `add_btt_skr_mini_e3_v3_0_exp1_physical_interfaces()` and the reviewed ten-position `BTT_SKR_MINI_E3_V3_0_EXP1_SOURCE_INVENTORY`.
- `machine-structure-editor/tests/test_skr_mini_e3_exp1.py`: added six dedicated tests for independent source mapping, the full ten-position inventory, sparse sample identity, deterministic endpoint IDs, evidence-layer separation, unresolved status preservation, and save/reopen persistence.
- `machine-structure-editor/src/machine_builder/persistence.py` provides the existing `save_editor_state()` and `load_editor_state()` APIs. The new test exercises the JSON round trip using `EditorState`, `VisualModel()`, and the canonical model.

### Implemented bounded sample

The fixture instantiates only logical EXP1 positions **1, 2, 3, 4, 8, 9, and 10**. The source inventory separately records all ten logical positions, including 5–7. Omission from the sample does not mean those contacts are absent, disconnected, or NC.

Each sample endpoint uses a stable ID derived from controller ID, connector ID, and numeric position. Contacts use `connector_id="exp1"`, `pin_id=None`, and an independent numeric `connector_position`. Repeated construction with a different display label or reversed sample order preserves the position-to-ID mapping.

The controller-level inventory and sampled ports keep these layers separate:

- Logical connector position to Klipper alias and Marlin `EXP1_nn_PIN` value.
- Marlin diagram/comment role label.
- Downstream Marlin peripheral macro assignment observed in the reviewed conditional block.

Marlin conditional assignments are not asserted to be active. The fixture records `marlin_downstream_assignment_configuration_status="conditional_active_configuration_not_established"`, `marlin_role_configuration_relationship_status="unresolved"`, and `marlin_upstream_origin_status="unknown"`. Physical orientation, PCB pad/net crosswalk, cable mating-face/cavity identity, continuity, and as-built harness wiring remain `unverified`.

### The latest bounded SKR EXP1 implementation run

**Tested checkpoint:** `HEAD` and `origin/main` both equalled `a84526b28237d1e678a044c534cc9e8ad6a80444`. Tests ran against the dirty working tree with the new fixture and dedicated test file plus other concurrent changes present. No files were staged or committed.

**Dedicated source, identity, and persistence tests**

Command: `.venv\Scripts\python.exe -m pytest -q --tb=short tests/test_skr_mini_e3_exp1.py`

Result: **6 passed in 0.14s**.

The six tests cover:

- `test_checked_in_firmware_sources_support_ten_position_inventory`
- `test_ten_position_inventory_matches_sources_and_stays_separate_from_sample`
- `test_sparse_fixture_uses_distinct_stable_controller_owned_endpoints`
- `test_endpoint_ids_do_not_depend_on_label_or_sample_order`
- `test_sample_preserves_separate_mapping_layers_and_unresolved_values`
- `test_sparse_fixture_save_reopen_preserves_identity_evidence_and_unknowns`

**Focused regression tests**

Command: `.venv\Scripts\python.exe -m pytest -q --tb=short tests/test_controller_board_fixtures.py tests/test_hardware_catalog.py tests/test_octopus_driver_mating.py tests/test_semantic_relationship.py tests/test_semantic_relationship_queries.py tests/test_persistence.py tests/test_store_persistence.py tests/test_promega_xy_motor_reference.py`

Result: **96 passed in 4.17s**.

**Full test suite**

Command: `.venv\Scripts\python.exe -m pytest -q --tb=short`

Result: **853 passed in 36.85s**.

**Whitespace checks:** `git diff --check` returned 0 for the fixture source and for the full worktree. The new test file had no trailing whitespace. Git emitted line-ending warnings for existing concurrent files; the checks succeeded.

### Remaining blockers and disposition

Research returned **ACCEPTABLE for the requested bounded revision** in `MB-20261017-0009-02`. The review accepts the bounded source inventory and sparse sample, mapping-layer separation, stable endpoint IDs, provenance, unresolved-status preservation, deterministic construction, and JSON save/reopen behavior. The separate physical-evidence gaps and other unresolved issues below remain open; this is not broader production-standard approval.

- Marlin's precise upstream source origin remains unknown; the local source-move commit is not an upstream revision.
- The downstream peripheral assignments are evidence from a conditional code block. The active firmware configuration and its relationship to the diagram labels remain unresolved.
- Applicable manufacturer drawing/orientation, PCB pad/net identity, cable mating-face/cavity correspondence, actual continuity, and as-built harness evidence remain open.
- The Octopus/TMC5160T contact-6 discrepancy and known integer-keyed persistence limitation remain separate unresolved issues. Passing SKR persistence tests does not resolve Octopus persistence.

**Next action:** No additional change is requested within the accepted bounded SKR EXP1 scope. Keep physical orientation, PCB pad/net identity, cable mating-face/cavity correspondence, continuity, as-built wiring, Marlin upstream provenance, and the conditional role/configuration interpretation unresolved. Keep the Octopus/TMC5160T contact-6 discrepancy and integer-key persistence limitation separate. Any work beyond this accepted bounded slice requires its own evidence and scope decision.

## SKR Mini E3 V3.0 EXP1 — Source and Mapping Gate

**Source inventory and scope:** Research inventory `MB-20261016-1755-01`; Planning reconciliation `MB-20261016-1806-01`. The source evidence was inspected at checkpoint `a84526b28237d1e678a044c534cc9e8ad6a80444`, and the two checked-in source-file SHA-256 hashes were captured during #4's review.

- Klipper file: `firmware_sources/klipper/config/generic-bigtreetech-skr-mini-e3-v3.0.cfg`, lines 122-123. Research records upstream reference commit `6e6ad7b5201d3452aa605f4ae852c51239c2c7d8`; the checked-in snapshot hash is `55517A544978655DB010BF5C920389B39CF03475BE1D9AB5A0060A64F7C786C0`.
- Marlin file: `firmware_sources/marlin/src/pins/stm32g0/pins_BTT_SKR_MINI_E3_V3_0.h`, diagram/comment lines 159-163, position macros lines 167-176, and downstream peripheral macros lines 208-211. The checked-in local snapshot hash is `C8650BB4F55558CBDD85CFEB79CB49006957860E9F2826DE3B23B15E64A002DE`. Local commit `eacdb5f6a3f5d184ef29f017157948dc6f213e84` records the source-file move; it does not identify Marlin's upstream revision. Its precise upstream origin remains unknown.

### Ten-position mapping inventory

| Logical position | Klipper alias | Marlin MCU pin macro | Interpretation |
|---:|---|---|---|
| 1 | `PB5` | `PB5` | GPIO mapping |
| 2 | `PA15` | `PA15` | GPIO mapping |
| 3 | `PA9` | `PA9` | GPIO mapping |
| 4 | `<RST>` | `-1` | Reset/special role, not an MCU GPIO mapping |
| 5 | `PA10` | `PA10` | GPIO mapping |
| 6 | `PB9` | `PB9` | GPIO mapping |
| 7 | `PB8` | `PB8` | GPIO mapping |
| 8 | `PD6` | `PD6` | Source-supported firmware mapping |
| 9 | `<GND>` | `-1` | Ground/special role, not an MCU GPIO mapping |
| 10 | `<5V>` | `-1` | Supply/special role, not an MCU GPIO mapping |

The logical position-to-MCU mapping agrees for positions 1-3 and 5-8. Position 8 → `PD6` is directly supported by both firmware sources. The `-1` Marlin macros for positions 4, 9, and 10 do not imply the connector contacts are absent.

### Keep three evidence layers separate

- **Logical connector position to MCU/special-function mapping:** source-backed at the positions above.
- **Marlin diagram/comment role labels:** lines 159-163 label positions with roles such as `BEEPER`, `BTN_ENC`, `BTN_EN1`, `RESET`, `BTN_EN2`, `LCD_D4`, `LCD_RS`, and `LCD_EN`.
- **Downstream Marlin firmware peripheral assignments:** lines 208-211 include `BEEPER_PIN -> EXP1_02_PIN`, `BTN_EN1 -> EXP1_08_PIN`, `BTN_EN2 -> EXP1_07_PIN`, and `BTN_ENC -> EXP1_01_PIN` in that conditional code section.

The diagram/comment labels and downstream peripheral assignments are not a single reconciled mapping. The header also contains alternative conditional display configurations with their own macro definitions; a global first/last-match scan does not establish which configuration is active. Keep the role-label/configuration relationship unresolved rather than reconciling it implicitly.

**Physical-evidence blockers remain:** applicable manufacturer drawing and silkscreen/orientation identification; PCB pad/net crosswalk; cable mating-face/cavity correspondence; and actual contact continuity or as-built harness evidence. Firmware mappings do not establish those facts.

## Separate Octopus / TMC5160T unresolved issue

Do not merge the Octopus/TMC5160T contact-6 issue with the SKR EXP1 evidence gate.

- Octopus Driver 2 contact 6 remains `SLEEP` / `DRIVER2_SLP`; TMC5160T Pro V1.0 J1 contact 6 remains `CLK`.
- The discrepancy remains explicitly unresolved, with no asserted electrical equivalence or contact continuity. The fixture relationship is interface-level `mated_with`.
- The known integer-keyed persistence limitation is still unresolved. Successful persistence for another fixture is not evidence that this exact experiment can be saved and reopened. Reproduce and address that limitation separately without silently changing the catalog or claiming it is fixed by the SKR tests.

**Current recovery boundary:** no complete Promega wiring graph, as-built harness, contact mapping, firmware assignment, physical mating, or production-standard approval is inferred by this handoff. The existing J28/XY references and held Z-A contact-correspondence gate remain unchanged.
<!-- MB4-ROUTING-REMEDIATION-CLOSEOUT-20261022 -->

## Routing remediation continuity closeout — 2026-10-22

Planning task: `MB-20261022-2136-01`, clarified by `MB-20261022-2137-01`.
Readiness review: `MB-20261022-READINESS-01`.

### Confirmed repository and ownership boundary

- Last verified baseline: branch `main`; local HEAD, fetched `origin/main`, and live remote `main` all equal `9b51df9ce2cfdcefcd47f1910343b0b7e694b301`.
- At the last verified preflight, the shared Git index was empty. No stage, commit, or push is authorized by this remediation task.
- `tests/test_canvas_ui.py` was confirmed tracked, present, and clean during the read-only inspection. Reconfirm that condition immediately before editing it.
- The shared checkout contains changes from multiple workstreams. Preserve all concurrent changes; never stage broadly or reset/discard work.
- Explicit exclusions: Board-owned `tests/test_stepper_motor_terminal_profile.py`; the diagnostic fixture `wiring test machines/Maestro and 4 port motor test.machine.json`; #3-owned `handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`; #5-owned `handoffs/05_EFFICIENCY_MODULARIZATION_WORKSTREAM_HANDOFF.md` and `handoffs/05_EFFICIENCY_MODULARIZATION_REPLACEMENT_PROMPT.md`. These are not #4 publication candidates and must remain unchanged.

### October 22 validation evidence — baseline, not post-remediation

The earlier candidate's `.venv` runs used Python 3.14.7, pytest 8.4.2, and PySide6 6.11.2.

- `.\.venv\Scripts\python.exe -X faulthandler -m pytest -q tests/test_connection_routing.py` — 59 passed; process exit `0`.
- `.\.venv\Scripts\python.exe -X faulthandler -m pytest -q tests/test_functional_interface_connection.py` — 9 passed; process exit `0`.
- `.\.venv\Scripts\python.exe -X faulthandler -m pytest -q tests/test_connection_wire_color.py` — 3 passed; process exit `0`.
- `.\.venv\Scripts\python.exe -X faulthandler -m pytest -q tests/test_canvas_scene.py` — 5 passed; process exit `0`.
- `.\.venv\Scripts\python.exe -X faulthandler -m pytest -q tests/test_node_graphics.py` — 7 passed; process exit `0`.
- `.\.venv\Scripts\python.exe -X faulthandler -m pytest -q tests/test_port_graphics_editing.py` — 3 passed; process exit `0`.
- Focused total: 86 passed across six isolated processes, all exit `0`.
- `.\.venv\Scripts\python.exe -X faulthandler -m pytest -q` — 868 passed in 6.90 seconds; process exit `0`.
- The tracked-candidate `git diff --check` returned `0`, with LF/CRLF advisory messages. The check did not cover untracked files.

These are results for the prior candidate before the newly authorized mutation-validation, selector-label, docstring, and associated regression-test fixes. They do not validate those fixes.

The separate global-interpreter teardown failure remains unexplained. Earlier runs with global Python/PySide6 6.12.0 reported passing tests followed by Qt teardown warnings/access violation, including exit `-1073741819` (`0xC0000005`). The historical October 20 checkpoint also records `-1073740791` (`0xC0000409`). Do not merge these distinct process exits, claim a root cause, or treat the clean `.venv` result as resolving the global-interpreter failure.

### GUI acceptance — still blocked

The latest documented manual report is October 20 and remains historical evidence, not a fresh observation after the current changes. It reports:
- Black/red/gray connector paths overlapping or ending at different places near the cone, with incomplete two-ended bundle representation.
- Overlapping wires not independently selectable in all areas.
- Connector breakout/enclosure overlapping the Maestro board label or boundary.
- Deleting connections resetting focus, with undo/redo not reliably restoring the prior focus.
- Reopening a saved connector-focused document resetting focus and leaving components outside the viewport until framing is invoked.

No fresh GUI acceptance check has yet been completed for this remediation task. Do not mark any of these as resolved without rechecking the running editor.

### Remediation attempt and next action

A PowerShell remediation script stopped during in-memory source preparation because it expected `Detailed ports (all nodes)` to occur once even though it occurs in both initial construction and refresh. The script had not entered its write phase, so that attempt applied no implementation or test edits. Correct the script to replace both occurrences intentionally, first preparing and validating every edit in memory before writing.

The authorized work remaining is:
1. Recheck baseline/index and the `tests/test_canvas_ui.py` edit gate.
2. Tighten `UpdateMachineComponentWithStepperTerminalProfile` to validate existing terminal ownership, `interface_role`, `interface_granularity`, `motor_terminal_profile`, and `terminal_display_index` before mutating the component. Cover conflicting metadata, rejection/rollback, undo/redo, and persistence with #4-owned tests; keep the Board-owned stepper test excluded.
3. Use per-port terminology consistently in all selector labels and assert the displayed labels both on construction and after refresh.
4. Restore the `_model_changed` docstring to the actual start of the method.
5. Run focused tests and the full suite with `.\.venv\Scripts\python.exe -X faulthandler -m pytest -q`. Record pytest counts and actual process exit codes separately.
6. Launch the editor and inspect the diagnostic project without saving changes to the user-owned fixture. Obtain fresh evidence for rendered endpoint placement, individual wire hit-testing, breakout/title overlap, delete/undo/redo focus, and save/reopen framing. If visual evidence cannot be gathered, explicitly leave GUI acceptance blocked.
7. Refresh this handoff and the replacement prompt with the actual post-fix results and the exact remaining next action.

The corrected remediation script has not yet been successfully applied. The batch therefore remains incomplete. No publication slot is open; no staging, commit, or push is authorized.
<!-- MB4-ROUTING-REMEDIATION-CLOSEOUT-20261022 -->
<!-- MB4-ROUTING-REMEDIATION-RESULTS-20261022 -->

## Routing remediation results and acceptance status — 2026-10-22

Planning task: `MB-20261022-2136-01`, clarified by `MB-20261022-2137-01`.
Prior readiness review: `MB-20261022-READINESS-01`.

### Implementation changes applied

- `semantic_component_mutations.py`: stepper-terminal updates validate an existing expected terminal's component ownership, `interface_role`, `interface_granularity`, `motor_terminal_profile`, and `terminal_display_index` before applying component edits. An invalid visual node type is rejected before the mutation changes component details.
- `canvas_ui.py`: the all/unused/used detail choices consistently say ports rather than nodes.
- `canvas.py`: the `_model_changed` docstring is now the method's first statement.
- `tests/test_functional_interface_connection.py`: added regression coverage for conflicting terminal metadata, invalid motor type rejection, store rollback/no partial mutation, undo/redo, and persistence.
- `tests/test_canvas_ui.py`: added an assertion that selector text and data keys match both on construction and after refresh. The file was confirmed clean before being edited.

The first two post-change validation attempts failed because of defects in the temporary regression-test fixture: first it used a controller ID as a component ID, and then it assumed a second canonical component existed. Both were corrected in the test fixture only. The final results below are from the corrected test code, and the targeted regression now passes.

### Post-remediation automated results

Environment: project `.venv`, Python 3.14.7, pytest 8.4.2, PySide6 6.11.2.

- Targeted terminal-conflict command: `.\.venv\Scripts\python.exe -X faulthandler -m pytest -q tests/test_functional_interface_connection.py -k 'stepper_terminal_profile_rejects_conflicting_existing_terminal_metadata'`
  - **5 passed, 11 deselected in 0.97s; process exit 0.**
- Focused command: `.\.venv\Scripts\python.exe -X faulthandler -m pytest -q tests/test_functional_interface_connection.py tests/test_canvas_ui.py tests/test_connection_routing.py tests/test_connection_wire_color.py`
  - **87 passed in 2.47s; process exit 0.**
- Full command: `.\.venv\Scripts\python.exe -X faulthandler -m pytest -q`
  - **876 passed in 6.19s; process exit 0.**
- Whitespace check: `git diff --check -- src/machine_builder/canvas.py src/machine_builder/canvas_ui.py src/machine_builder/semantic_component_mutations.py tests/test_canvas_ui.py tests/test_functional_interface_connection.py`
  - **Exit 0.** Git emitted its LF/CRLF advisory for `tests/test_functional_interface_connection.py`; this was not a whitespace-check failure.
- The focused suite and full suite ran against the current dirty shared working tree. Test discovery includes the locally present Board-owned stepper test; its execution does not authorize publishing it.

### Keep the older global-interpreter result separate

The earlier global Python/PySide6 6.12.0 environment reported passing tests followed by a native Qt teardown/access-violation failure. The documented exit codes include `-1073741819` (`0xC0000005`) and a separate historical October 20 exit `-1073740791` (`0xC0000409`). Those are distinct observations. Their cause remains unresolved; the clean `.venv` result does not prove that the global-interpreter failure is resolved.

### Fresh GUI acceptance — still not established

The latest available manual GUI observations are historical reports from October 20. They described:
- Black/red/gray wires ending or overlapping around the connector cone, with the expected routing not visually demonstrated.
- Some overlapping wires not independently selectable in the affected area.
- The connector breakout/enclosure overlapping the Maestro board outline/title.
- Deleting connections changing focus and undo/redo failing to restore the previous focus.
- A saved connector-focused document reopening with another focus and contents outside the visible viewport.

No post-remediation GUI results have been provided yet. Do not treat the automated tests as acceptance of rendered geometry, hit-testing, overlay placement, focus restoration, or save/reopen framing.

### Ownership and publication boundary

The shared index remains empty. No stage, commit, push, or publication grant is authorized.

The #4 candidate now has 17 paths:
- `handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`
- `handoffs/04_ROUTING_STABILITY_REPLACEMENT_PROMPT.md`
- `src/machine_builder/canvas.py`
- `src/machine_builder/canvas_editing.py`
- `src/machine_builder/canvas_scene.py`
- `src/machine_builder/canvas_ui.py`
- `src/machine_builder/graphics/connection.py`
- `src/machine_builder/graphics/connection_routing.py`
- `src/machine_builder/graphics/connection_routing_endpoint.py`
- `src/machine_builder/graphics/node.py`
- `src/machine_builder/graphics/port.py`
- `src/machine_builder/semantic_component_mutations.py`
- `src/machine_builder/store.py`
- `tests/test_canvas_ui.py`
- `tests/test_connection_routing.py`
- `tests/test_functional_interface_connection.py`
- `tests/test_connection_wire_color.py`

Explicit exclusions remain unchanged:
- Board-owned `tests/test_stepper_motor_terminal_profile.py`.
- User-owned `wiring test machines/Maestro and 4 port motor test.machine.json`.
- #3-owned `handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`.
- #5-owned `handoffs/05_EFFICIENCY_MODULARIZATION_WORKSTREAM_HANDOFF.md` and `handoffs/05_EFFICIENCY_MODULARIZATION_REPLACEMENT_PROMPT.md`.

The Board-owned, #5-owned, and diagnostic-fixture hashes were checked after remediation and remained unchanged. No paths from those ownership areas are part of the #4 candidate.

### Exact next action and disposition

**Next action:** run the editor against the diagnostic project without saving over the user-owned fixture. Check actual rendered endpoint locations, black/red/gray wire hit-testing, breakout placement relative to the board title/outline, focus after deleting connections and using undo/redo, and saved-file reopen focus/framing. Record each as freshly observed pass/fail/not checked, distinct from the October 20 history. Then perform a final bounded complete-diff review before asking Planning for a separate publication decision.

**Status: NOT READY — SLOT RELEASED.** Automated validation is clean in `.venv`, but GUI acceptance and final integrated diff review are outstanding. No publication slot is open.
<!-- MB4-ROUTING-REMEDIATION-RESULTS-20261022 -->

<!-- MB4-GUI-ACCEPTANCE-FRESH-20261022 -->

## Fresh GUI acceptance and inspection-console failure — 2026-10-22

User-reported fresh GUI observations:
1. **FAIL — endpoint/cone routing:** no visible improvement; the black wire still goes up and through the cone.
2. **FAIL — overlapping-wire selection:** the user can still only select the red wire near the bottom.
3. **FAIL — breakout placement:** the box is unchanged and still covers the Maestro board name.
4. **FAIL — delete/undo focus:** focus switches to “Functional interfaces”; undoing everything leaves it there.
5. **FAIL — saved focus restoration:** opening a saved file retains whatever focus is currently selected when opened instead of restoring the focus used when saved.
6. No additional observation was supplied. Reopen viewport framing and actual saved component coordinates were not separately checked in this report.

A subsequent large read-only PowerShell inspection block was pasted into the console; the user immediately saw “The window terminated unexpectedly (reason: 'crashed', code: '-1073741819')”. This is recorded as a console/inspection interruption only. It does not identify a source-code cause, and no inspection output was obtained. The cause remains unknown.

The prior automated remediation results remain: targeted metadata regressions 5 passed (exit 0); focused suite 87 passed (exit 0); full `.venv` suite 876 passed in 6.19 seconds (exit 0); tracked `git diff --check` exit 0, with an LF/CRLF advisory. These automated results do not supersede the fresh GUI failures.

**Next action:** resume source inspection in small bounded excerpts, then fix the confirmed routing/hit-testing, breakout geometry, focus-after-delete/undo, and persistence of focus where these behaviors can be corrected within #4-owned paths. Recheck the live GUI after each relevant change. Do not claim viewport framing or coordinate persistence passed without separate evidence.
<!-- MB4-GUI-ACCEPTANCE-FRESH-20261022 -->

<!-- MB4-CONSOLE-RECOVERY-20261025 -->

## Console command failures and routing recovery — 2026-10-25

**Verified state at recovery:** branch `main`, `HEAD` `e4d2387bbde9b67f664f49c9bc7ef777518160b3`; the earlier preflight found `origin/main` and live `origin/main` at the same commit. The shared index was empty. Existing local changes across workstreams remain in place.

**Confirmed fail-closed incidents:**
- Manually constructed patch preflights failed with `patch fragment without header` and `corrupt patch`. `git apply --check` rejected the malformed patch before application.
- A baseline guard expected `b5e2d079...` but found `e4d2387...`; it stopped before writing.
- A later in-memory source-replacement attempt failed because the fan-out loop anchor occurred twice, not once. The failure happened before the script's write phase. Do not treat the proposed cone-base geometry correction as applied or tested.

**Diagnostic findings, not confirmed root cause:**
- Connector contact stubs are separate scene items drawn from contact origin to the cone tip at the time of inspection. They are a leading hypothesis for the visible wire-crossing failure.
- The test comparing a child cone's `zValue()` directly with a top-level connection's `zValue()` does not establish their actual stacking order.
- Existing checks verify the main route endpoint at the cone tip but do not prove that the visible wire avoids the cone interior. The actual first offending segment still needs runtime evidence.
- Historical GUI failures remain unresolved: wire crossing the cone, wrong overlapping-wire selection, breakout/title overlap, delete/undo focus behavior, and saved-focus restoration. Do not report these as fixed without fresh GUI acceptance.

**Prevention:** use bounded commands; guard source replacements with surrounding context that distinguishes repeated blocks; validate all anchors before writing; keep edit, focused test, and full-suite runs separate; preserve the caller's PowerShell location in `finally`; never infer GUI success from endpoint-only assertions or automated test passes.

**Next action:** capture one diagnostic for the actual black connection, including stub endpoints, fan-out point, endpoint escape, and the first main-route segments. Identify the first segment that deviates from the intended geometry before changing code. Make any correction one file at a time, inspect the focused diff, and run its relevant check separately. GUI acceptance remains blocked. No staging, commit, push, or publication authorization.

<!-- MB4-POWERSHELL-HASH-COMPATIBILITY-20261025 -->

### Additional command failure — PowerShell SHA-256 API compatibility (2026-10-25)

**Observed:** a guarded replacement-prompt script called `[Security.Cryptography.SHA256]::HashData($bytes)` and failed with `MethodInvocationException`, stating that `System.Security.Cryptography.SHA256` has no method named `HashData`.

**Cause:** the PowerShell/.NET runtime in this environment does not expose that static method. This was a command/runtime API compatibility issue, not a repository or source-code failure.

**Outcome:** the exception occurred in the pre-write guard. A subsequent read-only check confirmed the replacement prompt retained its earlier SHA-256 and did not contain the intended checkpoint marker. That failed attempt did not write the prompt or change the Git index. A later, separately guarded update succeeded using `Get-FileHash`.

**Prevention:** use `Get-FileHash -Algorithm SHA256` for file-hash checks in this environment rather than relying on newer .NET static hash APIs. Keep the write phase after the guard and verify the resulting file independently.
