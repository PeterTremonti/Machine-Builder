# Machine Builder — Routing Stability Workstream Handoff

## Recovery instructions

This file is the **living recovery handoff** for the Routing / Diagnostics workstream.

It is not a replacement for the older historical investigation records. The detailed historical records remain useful when a replacement chat needs deeper background:

```text
docs/historical/routing/ROUTING_STABILITY_INVESTIGATION_HANDOFF_4.3.md
docs/historical/routing/ROUTING_STABILITY_INVESTIGATION_HANDOFF_4.4.md

A replacement Routing chat should read, in order:

PROJECT_CURRENT_STATE.md
machine-structure-editor/handoffs/ROUTING_STABILITY_WORKSTREAM_HANDOFF.md
the current routing source and routing tests

Current source code and actual reported test results are authoritative over historical checkpoint text.

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

section.

Do not erase earlier history because the current implementation has moved on.

Maintain the current:

## Current state

section so that it describes the actual current implementation rather than only historical conclusions.

Keep:

DECIDED
IMPLEMENTATION
WATCH
NEW PRINCIPLE
RECONSIDER

distinct.

Do not promote experimental constants or local routing heuristics into architectural decisions without evidence.

When a new implementation problem exposes a technical question that may have an established solution elsewhere, formulate a specific research request for Planning / Research (#2) rather than silently inventing a new routing principle.

When a discovery affects the whole Machine Builder rather than only Routing, report it to Planning / Architecture so that PROJECT_CURRENT_STATE.md can be updated there.

The goal is that a replacement Routing chat can read:

PROJECT_CURRENT_STATE.md
this handoff
current routing source
current routing tests

and resume the work without reconstructing the entire conversation or rereading the complete historical routing investigation records.
