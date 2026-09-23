# Routing Stability Investigation Handoff — Coder 4.3

Date: 2026-09-22

## Current checkpoint

Branch:

`wip-routing-diagnostics`

Latest pushed checkpoint before the current transition-diagnostic work:

`816706a24c42154ad40a709ad070087b456f9a19`

Commit:

`Add live routing stability diagnostics`

Current local work after that checkpoint:

- `src/machine_builder/graphics/connection.py`
- `tests/test_connection_routing.py`

Current local test result:

- focused routing/inspector/canvas tests: 54 passed
- full suite: 694 passed
- git diff --check: clean

The current uncommitted change adds persistent "last recorded transition" routing diagnostics. No routing constants or routing algorithm behavior were intentionally changed.

## Main problem being investigated

The remaining routing problem is visible elbow/topology changes when components are moved through very tight geometric clearances.

The router itself is already split into focused production modules:

```text
src/machine_builder/graphics/
    connection.py
    connection_routing.py
    connection_routing_pathfinder.py
    connection_routing_relevance.py
    connection_routing_endpoint.py
Do not refactor the production router simply because tests/test_connection_routing.py is large.

Current stability behavior

Current route-stability tolerance:

16.0

Historical experiments showed:

4 px    -> switches
8 px    -> switches
10 px   -> switches
12 px   -> switches
12.5 px -> holds
16 px   -> holds
20 px   -> holds
24 px   -> holds

16 px is still an experimental value, not a final architectural decision.

The stability layer is intended to:

hold a previous valid route when the new candidate is only slightly better
switch when improvement is meaningful
switch immediately when the previous route becomes invalid
avoid rapid oscillation between near-tie routes

Debug Mode intentionally bypasses normal route-stability history.

Captured evidence

At several positions the diagnostics show:

decision: previous stable route held within tolerance
previous: 868.000
candidate: 868.000
selected: 868.000

In these cases the current previous and candidate main routes are identical.

Therefore the stability layer is not itself creating every visible elbow change.

Lower-elbow transition

A normal-mode movement eventually caused the lower elbow to pop upward.

The persistent transition diagnostic showed:

reason: previous stable route was blocked

Previous route at the transition:

(-5.000, 240.000)
-> (-1.250, 240.000)
-> (-1.250, 174.250)
-> (-25.250, 174.250)
-> (-25.250, 6.250)
-> (-10.000, 6.250)
-> (-10.000, -25.000)

Candidate route:

(-5.000, 240.000)
-> (-1.250, 240.000)
-> (-1.250, 140.250)
-> (-25.250, 140.250)
-> (-25.250, 5.750)
-> (-10.000, 5.750)
-> (-10.000, -25.000)

Candidate and selected route cost:

868.000

The transition recorder currently reports the previous cost as n/a for blocked-route transitions because it records the event before calculating the old route cost. That is a diagnostic limitation only.

The important behavioral evidence is that the previous route was declared blocked. Therefore the 16 px stability tolerance is not the cause of that particular transition.

Strange geometry

During reverse movement, a captured route contained:

(-25.250, 141.550)
-> (-25.250, -24.950)
-> (-10.000, -24.950)
-> (-10.000, -25.000)

The 0.05 px segment near -25.000 is suspicious and may be relevant to the overlapping/180-degree visual geometry.

Do not assume it is merely a rendering artifact.

Routing constants

Current known values include:

ROUTING_MARGIN = 16.0
STUB_LENGTH = 40.0
ROUTING_RELEVANCE_RADIUS = 50.0
BEND_PENALTY = 80.0
ENDPOINT_DIRECTION_PENALTY = 160.0
U_TURN_MIN_SEPARATION = 32.0
ESCAPE_CLEARANCE = 1.0
ROUTE_STABILITY_COST_TOLERANCE = 16.0

Do not change these values yet.

Next exact investigation

The next coder should inspect the actual implementation of route_is_clear() and nearby route normalization/cleanup logic.

Run these two read-only commands before changing routing behavior:

Write-Host "`n=== ALL route_is_clear REFERENCES ===" -ForegroundColor Cyan

Get-ChildItem "src\machine_builder\graphics" -Filter "*.py" -File |
    Select-String `
        -Pattern "route_is_clear" `
        -Context 3,35

Then:

Write-Host "`n=== PATHFINDER ROUTE BUILD / CLEANUP ===" -ForegroundColor Cyan

Get-ChildItem "src\machine_builder\graphics" -Filter "*.py" -File |
    Select-String `
        -Pattern "simplif|normalize|collinear|orthogonal|route.*clear|segment.*intersect" `
        -Context 2,8

The goal is to determine whether the old route is considered blocked because of:

a true collision with an expanded obstacle
touching/boundary precision rules
endpoint escape geometry
a tiny/near-overlapping segment created by the pathfinder
another route-state condition

Do not tune the stability tolerance until this is understood.

Saved test machine

Use the existing saved machine from:

machine-structure-editor/wiring test machines/

Do not rebuild the test geometry from scratch.

Key nodes in the current troublesome geometry:

Temperature Sensor:
node-1
x=-230
y=-75
w=180
h=100
output on right

Temperature Controller:
node-2
x=-225
y=190
w=180
h=100
input on right

Component obstacle:
node-3
x=-222
y=55
w=180
h=100

Controller obstacle:
node-4
x≈-8
y varied
w=180
h=100

Connection:
connection-1
Temperature Sensor output -> Temperature Controller input
Do not do yet

Do not:

merge the WIP branch
create a PR
declare 16 px final
raise the stability tolerance just to suppress forced blocked-route transitions
replace the router
refactor the production routing modules
split the large routing test file during this investigation

The immediate objective is evidence-driven diagnosis of the exact blocking transition.

---

# Known follow-up cleanup

These items were identified during the 4.2 / Research coordination review.
They are intentionally NOT part of the current routing-behavior experiment.

## Selection Inspector duplicate definitions

The current `selection_inspector.py` WIP source has duplicate definitions of:

```text
_routing_debug_toggled()
set_routing_debug_mode()
set_last_click_position()
The later Python definitions override the earlier definitions.

This appears to be accidental duplication from routing-debug work.

Clean it up as a small isolated maintenance change when convenient. Do not mix
the cleanup into a routing-behavior experiment unless doing so is necessary.

Implementation roadmap documentation

machine-structure-editor/IMPLEMENTATION_ROADMAP.md contains stale V0.2
planning text that no longer reflects the current implementation state, including
language equivalent to:

V0.2 — Planning not started
V0.2 implementation should not begin until its own plan has been created and reviewed.

That documentation should be refreshed at a natural implementation checkpoint.

Do not stop the active routing investigation merely to perform this cleanup.

Older V0.2 implementation handoff

The durable V0.2 implementation handoff should eventually be refreshed to
describe the current modular visual-editor architecture and current test state.

The authoritative implementation handoff filename is:

machine-structure-editor/handoffs/V0.2_VISUAL_EDITOR_IMPLEMENTATION_HANDOFF.md

Do not substitute the similarly named Research/O0.2 documents for this
implementation handoff.

The handoff should remain the implementation-facing bridge and should not
redefine research/ontology decisions.

Current modular canvas architecture

The canvas implementation has already been split into focused modules,
including:

canvas_ui.py
canvas_editing.py
canvas_palette.py
canvas_selection.py
canvas_interaction.py
canvas_scene.py

canvas.py is intended to remain a coordinator rather than becoming a
repository for routing or interaction logic.


Coder 4.3 startup

At the beginning of the next coder chat:

Read Machine-Builder/CODER_CHAT_WORKFLOW.md.
Read machine-structure-editor/handoffs/V0.2_VISUAL_EDITOR_IMPLEMENTATION_HANDOFF.md.
Read machine-structure-editor/IMPLEMENTATION_ROADMAP.md.
Read this routing handoff.
Establish the actual current local branch/commit/status before relying on
historical conversation details.
Run the local test suite and treat that result as authoritative.

Current reported implementation checkpoint:

Focused routing/inspector/canvas tests: 54 passed
Full suite: 694 passed
git diff --check: clean

The active routing investigation should continue from the current working tree.
Do not reconstruct the entire routing history from the previous chat.

The next investigation should begin with the two exact read-only source
inspection commands documented above, especially the implementation of
route_is_clear() and nearby route normalization/cleanup logic.

