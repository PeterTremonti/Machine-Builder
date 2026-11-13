# Machine Builder #4 - Routing / Diagnostics / Visual Integration Replacement Prompt

Prepared: 2026-11-12 EST
Message ID: MB4-REPLACEMENT-20261112-PRESENTATION-ROUTE-TRANSFER-01
Relationship: Current recovery prompt. The November 12 state below is authoritative for the active branch, commits, remaining work, and next actions. Detailed evidence and chronology remain in `04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`.

## Current recovery state - 2026-11-12

This current-state section supersedes the older November 10 snapshot and immediate-next-action instructions below. The historical sections remain for context.

### Active checkout and publication status

- Laptop repository: `C:\Users\Peter\Documents\GitHub\Machine-Builder`.
- Current branch: `experiment/presentation-route-source`.
- Current HEAD: `2d98e7a66b873c4e367973aa6483e4f6b839e84d`.
- Branch base at creation: `810e29f302d81fc5a7a4ef1102e0f415eb0cd10a`.
- Five reviewed source commits are present locally.
- The branch has not yet been pushed. The two #4 handoff documents are being updated as a separate documentation-only unit before publication.
- No merge to `main` has occurred.
- The old WSL `machine-builder-review` donor was not admitted because it lacked the presentation graph and builder files. The approved source snapshot came from the laptop checkout.
- The current laptop index was empty after the canvas integration commit. Recheck before every Git write.

### Five completed source commits

1. `ee364126bcb0f11a88b2775d6e97afc61c890bdc` - runtime `PresentationRouteGraph` and tests; 19 passed in 0.07 seconds.
2. `e09d9c993e075259e29e3b2b6bdcc231b56e698c` - presentation-route builder and tests; 9 passed in 1.41 seconds; `py_compile` passed.
3. `12534669fcfce5b262e4b82838fa41b0286dc3d6` - protected-segment pathfinder and tests; 67 passed in 0.67 seconds.
4. `7b721ff2f8d42c604c64b0d892b646cb1723f214` - conductor bundle geometry primitives and tests; 20 passed in 0.13 seconds; `py_compile` passed.
5. `2d98e7a66b873c4e367973aa6483e4f6b839e84d` - grouped-route preview integration into the canvas; exact seven-file integration commit.

Each was reviewed and committed separately with exact path verification. Do not redo, amend, or collapse these commits.

### Automated validation on the committed source state

- Focused integration:
  `python -m pytest tests\test_canvas_interaction.py tests\test_canvas_scene.py tests\test_functional_interface_connection.py tests\test_connection_routing_bundle.py -q`
  **68 passed in 6.94 seconds.**
- Full project suite:
  `python -m pytest -q`
  **998 passed in 12.83 seconds.**
- `canvas_scene.py` `py_compile`: passed.
- `connection_routing_bundle.py` `py_compile`: passed.
- Two preview lifecycle/failure regressions: **2 passed in 0.20 seconds**.

The validation was run against the same combined source content now represented by the commits. No manual GUI acceptance has been performed on this branch.

### Remaining laptop worktree changes to preserve

The last verified post-commit status contained:

- Modified #1-owned: `machine-structure-editor/handoffs/01_PLANNING_ARCHITECTURE_WORKSTREAM_HANDOFF.md`
- Modified #3-owned: `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`
- Modified #4-owned: `machine-structure-editor/handoffs/04_ROUTING_STABILITY_REPLACEMENT_PROMPT.md`
- Modified #4-owned: `machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`
- Modified user-owned diagnostic fixture: `machine-structure-editor/wiring test machines/Maestro and 4 port motor 4 wires J9 contact view.machine.json`
- Untracked #3-owned test: `machine-structure-editor/tests/test_stepper_motor_terminal_profile.py`

The #4 source and test files are committed, not untracked. Do not stage the #1/#3 files, the diagnostic fixture, or the #3 test into an #4 commit. The diagnostic fixture was not included in the source-transfer branch and may not exist on the other computer.

### Technical boundaries and current implementation

- Keep canonical `SemanticConnection` identity, endpoints, properties, signal direction, and provenance unchanged.
- Runtime presentation routing is derived state. Do not create canonical connections, electrical junctions, or Harness membership from proximity, color, shared endpoints, or route geometry.
- Explicit Harness membership remains distinct from transient canvas preview grouping.
- The canvas preview groups physical conductors using `(controller_id, connector_id, terminal_component_id)`, uses a 50 ms coalesced preview, and hides individual wires only after a successful widened route.
- Scene synchronization cleanup and failed-preview fallback have direct regression coverage.
- `PresentationRouteGraph` and `presentation_route_builder.py` are committed, but their use as the live canvas graph implementation has not been established. Do not claim that they are fully integrated merely because the modules exist.
- `connection_routing_bundle.py` supplies centered lane offsets, envelope calculation, orthogonal offset geometry, and endpoint lane-order checks. `offset_orthogonal_route()` is not a full router and has no global self-intersection/obstacle-clearance guarantee. It is not yet the final individual-conductor lane-generation path.
- `canvas_scene.py` calls `_prepare_line_geometry()` directly for representative bundle endpoint preparation and uses `setLine()` for individual connections. The convenience wrapper `prepare_line()` itself has no direct caller in the inspected source; do not claim preparation has no call site.
- `graphics/node.py` was not changed. Lost-mouse-grab cancellation remains open and outside the approved source path list.

### Required overnight work

#### 1. Acquire and verify the branch

After the user publishes the branch:

- On the other computer, inspect the repository root, `git status --short`, current branch, and current HEAD before switching branches.
- Fetch from the intended remote.
- Verify that `origin/experiment/presentation-route-source` exists and contains the five commits above.
- If the worktree is dirty, do not discard, stash, or overwrite it. Determine ownership and preserve the changes before switching.
- Switch to or create a tracking branch for `origin/experiment/presentation-route-source`; verify the resulting HEAD is `2d98e7a66b873c4e367973aa6483e4f6b839e84d` or a later commit on this same experiment branch.
- Do not assume a Windows, OneDrive, WSL, or laptop path. Verify the actual repository root.

#### 2. Perform current-branch GUI acceptance

Use an appropriate four-conductor physical-connection scenario if available. The user-owned modified diagnostic fixture was not transferred by these commits; do not assume it exists on this computer or recreate/overwrite it.

Inspect and record:

- Whether four conductors form a coherent preview with appropriate spacing and clean trunk/branch transitions.
- Whether the long detours, awkward loops, tight turns, inconsistent spacing, and crowded fan-outs seen in the November 8 screenshots have actually improved.
- Whether connector-cone stubs should terminate at the anchor or clip at the visible cone boundary. Current automated tests require the anchor; GUI appearance remains unresolved.
- Whether individual wires can be selected after preview release.
- Whether fast dragging stays responsive and routes settle correctly after release.
- Whether failed preview routing preserves the individual wires.
- Whether delete, undo, redo, save, close, and reopen restore the correct presentation and canonical connectivity.
- Test more than one module before making any scaling/performance claim.

Do not treat the November 5 drag-preview acceptance or November 8 screenshot review as acceptance of this newer branch.

#### 3. Continue geometry and lifecycle review

- Review offset-lane routing for self-crossings, obstacle collisions, clearance between lanes, short segments, tight bends, and reversal/degenerate cases.
- Do not treat the current offset primitive as a clearance-validating router.
- Inspect prepared endpoint geometry/cache lifetime if changing that code. The scene calls `_prepare_line_geometry()` directly and later calls `setLine()`; the public convenience wrapper is not the only route to preparation.
- Lost-mouse-grab cancellation needs a Planning scope amendment before modifying `src/machine_builder/graphics/node.py` or adding its tests. Until then, leave that path untouched and report the limitation.
- Make narrow fixes with focused regressions; rerun the full project suite after meaningful integration changes.

#### 4. Commit and publication discipline

- Work only on `experiment/presentation-route-source`.
- Preserve every unrelated, staged, unstaged, and untracked change.
- Use exact-path staging; review full staged diffs and `git diff --cached --check` before each commit.
- Keep logical source/test units separate and update the #4 handoff after validated changes.
- Normal push to the experiment branch only when appropriate. Never force-push or merge to `main`.
- Report exact commit IDs, test outputs, GUI observations, and any unresolved acceptance item. Do not claim GUI acceptance or performance results that were not observed.

### Immediate starting point

The source commits are already complete locally. Finish the two #4 handoff documents as a separate documentation-only commit, publish the experiment branch normally, then use the required overnight work above. No #1, #3, or user-owned file is part of the #4 documentation or source commit.

## Mission and ownership

Own Routing, diagnostics, topology/geometry, visual integration, and their tests. Preserve every canonical `SemanticConnection` identity, endpoint, signal direction, provenance, property, and individual wire identity. Keep canonical connectivity, derived presentation routing, and explicit physical Harness/Path concerns distinct. Presentation grouping and route geometry must not create electrical connections, junctions, or physical membership.

Coordinate shared canonical-contract changes with Planning. Preserve every other workstream's and user-owned file in the shared checkout. #4 owns these two handoff documents.

## Required recovery reading

Read the current repository copies, not just this prompt:

- Root `CHAT_WORKFLOW.md`, especially repository operation, PowerShell formatting, and current working constraints.
- `MASTER_PLAN.md`.
- `PROJECT_CURRENT_STATE.md`.
- `WORKSTREAM_FOCUS_INDEX.md`, including the #4 entry.
- `machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`, starting with the November 12 current checkpoint.
- This replacement prompt.
- `DOCUMENTATION_AUTHORITY.md` when ownership or authority matters.

Inspect relevant current source and tests before diagnosing or changing code. The checkout and fresh command output override remembered summaries.

## Repository and operating rules

Repository: `C:\Users\Peter\Documents\GitHub\Machine-Builder`.

There is one shared Windows checkout and one Git index; it is currently on the authorized `experiment/presentation-route-source` transfer branch. The user executes local PowerShell/Git commands and supplies output. Never claim an action succeeded locally unless the user's output establishes it.

Before every write, verify the normalized repository root, branch, local `HEAD`, fetched `origin/main`, live remote `main`, shared index, and complete worktree status. Preserve all staged, unstaged, and untracked work. Never broadly stage, reset, clean, stash, discard, or force-push. Never use `git add ./-A`.

Work one logical unit/file at a time. Use guarded PowerShell edits, exact anchors, read-back verification, focused diffs, and targeted tests. Do not create temporary analysis artifacts. No Python/Jupyter/pandas/notebooks for repository editing or analysis; project `.venv` commands such as `python -m pytest` and `python -m py_compile` are permitted.

Keep console output bounded. Use plain PowerShell code fences with no fence metadata. Keep handoff prose distinct from executable commands. Do not use `exit 1` in PowerShell scripts.

## Historical repository checkpoint - 2026-11-10 (superseded by the November 12 update above)

At the November 10, 2026 pre-documentation inspection:

- Repository: `C:\Users\Peter\Documents\GitHub\Machine-Builder`.
- Branch: `main`.
- Local `HEAD`, fetched `origin/main`, and live remote `main`: `810e29f302d81fc5a7a4ef1102e0f415eb0cd10a`.
- Divergence: 0 ahead / 0 behind.
- Shared Git index: empty.
- Worktree: 13 modified tracked paths and 3 untracked paths.
- All work remains local. No staging, commit, or push has been performed for the current routing work.

The shared worktree paths are:

Modified tracked:
- #3-owned: `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`
- #4-owned: `machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`
- #4-owned: `machine-structure-editor/handoffs/04_ROUTING_STABILITY_REPLACEMENT_PROMPT.md`
- #4: `machine-structure-editor/src/machine_builder/canvas_interaction.py`
- #4: `machine-structure-editor/src/machine_builder/canvas_scene.py`
- #4: `machine-structure-editor/src/machine_builder/canvas_ui.py`
- #4: `machine-structure-editor/src/machine_builder/graphics/connection.py`
- #4: `machine-structure-editor/src/machine_builder/graphics/connection_routing_pathfinder.py`
- #4: `machine-structure-editor/tests/test_canvas_interaction.py`
- #4: `machine-structure-editor/tests/test_canvas_scene.py`
- #4: `machine-structure-editor/tests/test_connection_routing.py`
- #4: `machine-structure-editor/tests/test_functional_interface_connection.py`
- User-owned diagnostic fixture: `machine-structure-editor/wiring test machines/Maestro and 4 port motor 4 wires J9 contact view.machine.json`

Untracked:
- #4: `machine-structure-editor/src/machine_builder/graphics/connection_routing_bundle.py`
- #4: `machine-structure-editor/tests/test_connection_routing_bundle.py`
- #3: `machine-structure-editor/tests/test_stepper_motor_terminal_profile.py`

This inventory is not permission to alter or publish all listed paths. Preserve the #3 handoff, #3 test, and user-owned fixture. Recheck status before every later write.

## Published harness baseline and architecture boundary

Stage 1 harness implementation was published under Planning authorization `MB-20261031-HARNESS-STAGE1-PUBLISH-AUTH-03`:

- Commit: `e6e3710786cb0c2b31ac166f6d020db153ffb84f`
- Subject: `feat: add canonical harness model and persistence`
- The published Stage 1 model groups existing semantic connections; it does not create electrical connections or change endpoint identity.

Planning direction `MB-20261105-SHARED-ENVELOPE-DIRECTION-01` accepts shared-envelope/centerline/offset-lane routing in principle, subject to these constraints:

- Membership must be explicit and physically meaningful. Never infer it solely from color, proximity, shared connector, or similar geometry.
- Preserve every original `SemanticConnection`, endpoint assignment, direction, provenance, properties, and individual wire identity.
- Centerlines and clearance envelopes are routing constructs, not electrical connections or fabricated junctions.
- Expand obstacle clearance by the full bundle envelope.
- Generate deterministic lanes; validate corners, spacing, crossings, obstacles, and endpoint escapes.
- Preserve individual terminal fan-outs.
- Never silently drop a member when shared routing fails; define a fallback or report failure.
- Handle ambiguous or branched physical topologies conservatively.

This is architecture approval in principle, not permission to change canonical Harness schema, persistence, Stage 2 authoring UI, or publish the current implementation. Stage 2A and Stage 2B remain separately gated.

## November 10 multi-wire presentation architecture

The November 8 screenshot review is complete. Its evidence is commit `810e29f302d81fc5a7a4ef1102e0f415eb0cd10a`. All four conductors were visible, but route quality failed: long black-wire detour, awkward loops/tight turns, inconsistent spacing, and visually converged endpoint fan-outs. Do not ask the user to repeat that static screenshot review. Individual selection, post-November-8 drag responsiveness, multi-module performance, and delete/undo/reopen recovery were not established by those screenshots.

The November 8 routing-priority correction changes the order of independent pathfinder calls. It does not generate a shared centerline or coordinated final conductor lanes. `connection_routing_bundle.py` remains an unintegrated geometry foundation.

**Recommended design:** a derived, presentation-only `PresentationRouteGraph` (tentative name). Every displayed segment resolves exact canonical `member_connection_ids`; branches have their own membership sets. Generated route branches are not electrical junctions, and shared-looking strokes do not prove a physical cable exists. Start runtime-derived and non-persistent.

Keep three concerns separate:

- Canonical `SemanticConnection` records remain individual and authoritative.
- Quick hookup may aggregate real connections into readable shared-looking segments and branches, with exact selection and trace resolution.
- Physical routing requires explicit physical information and physical grouping. Preserve the existing Stage 1 Harness meaning; never infer membership from color, proximity, shared endpoints, connector identity, or generated geometry.

Prefer shared geometry/pathfinding/validation primitives with distinct quick-hookup, connector-aware individual-wire, diagnostics, and future physical-harness strategies. Connection authoring remains a separate workflow using established mutations, validation, undo/redo, and persistence. Route-geometry edits must not silently change canonical endpoints.

The #2 industry investigation covered Autodesk Inventor, SOLIDWORKS Electrical, EPLAN, AutoCAD Electrical, CATIA Electrical Harness, and Siemens Capital. Their documented practices support distinguishing individual electrical connections, grouped schematic representations, and explicit physical routing segments/membership. Do not assume their internal data models are identical.

Planning must decide the presentation-only graph boundary, segment membership and branch semantics, relationship to `VisualModel`/`VisualConnection`, runtime-derived initial scope, and separation from physical Harness membership. The November 5 shared-envelope decision is approval in principle subject to explicit, physically meaningful membership; it does not itself authorize inferred quick-hookup grouping or a new persistent/canonical contract.

Do not change canonical schema, persistence, Stage 2A/2B, or physical Path/Cable/Harness semantics as part of this work. After Planning direction, the first implementation increment should be a bounded pure/runtime-derived route-graph prototype tested with 2, 4, 8, 12, 24, and 32+ conductors, branches, membership changes, endpoint fan-outs, crossings, obstacles, and explicit failure reporting.## November 8 independent-conductor routing-priority correction

The failing contact-view regression represents a controller and a four-lead stepper motor with four independent physical conductors: `connection-4` through `connection-7`.

The saved `Maestro and 4 port motor 4 wires J9 contact view.machine.json` diagnostic fixture has no explicit Harness membership for these conductors; their `harness_id` values are null. Do not add Harness membership merely to make their routes work.

In the reproduced close/skewed layout, the original connection-ID order routed only two of the four conductors. A diagnostic tried all 24 orderings on fresh fixtures; only two orderings produced all four routes. Both successful orderings began with `connection-7`, then `connection-6`.

The production change is local in `machine-structure-editor/src/machine_builder/canvas_scene.py`:

- `_routing_ordered_connection_items()` starts with the existing `_ordered_connection_items()` result.
- It identifies physical conductor groups by controller ID, connector ID, and terminal component ID.
- It derives average contact-to-terminal route direction and the physical lane positions at both ends.
- It uses `lane_order_is_compatible()` to reject ambiguous, duplicate, or reversed lane arrangements.
- It reorders only the compatible physical-conductor group, preserving unrelated connection slots.
- The scene route-update loop now uses `_routing_ordered_connection_items()`.

For the failing fixture, the selected order is `connection-7`, `connection-6`, `connection-5`, `connection-4`, and all four routes are produced.

The existing `_ordered_connection_items()` remains the explicit-Harness ordering mechanism. This routing-priority calculation does not create Harness membership, modify persistence, or merge independent semantic connections. It is a targeted ordering correction, not a general proof that all geometries, branches, crossings, and obstacle arrangements will succeed.

## Historical automated validation - November 8 baseline

The November 8 source and test state produced:

- Two focused route regressions: **2 passed in 4.67 seconds**:
  - `test_connector_level_functional_link_is_hidden_after_four_contact_refinement`
  - `test_contact_focus_routes_contacts_to_shared_cone_tip_and_contact_origins`
- Affected scene/routing surface (`tests/test_canvas_scene.py`, `tests/test_functional_interface_connection.py`, `tests/test_connection_routing_bundle.py`): **60 passed in 6.96 seconds**.
- Full project `.venv` suite: **968 passed in 11.65 seconds**.
- `git diff --check` on `canvas_scene.py` and `test_canvas_scene.py`: passed.
- `python -m py_compile src/machine_builder/canvas_scene.py`: passed.

Four new tests in `tests/test_canvas_scene.py` cover compatible independent-lane priority, preservation of unrelated slots, rejection of reversed lanes, and rejection of ambiguous lanes. The priority test also confirms that no Harness is created.

The endpoint-preview fixture correction now unpacks coordinate tuples into `QPointF(*coords)`. Its focused regression, affected suite, and full suite passed. This was a test-fixture correction, not a production routing change.

These are automated results. The November 8 screenshot review is complete and recorded below. Screenshots do not establish interactive selection, post-change drag responsiveness, multi-module performance, or delete/undo/reopen recovery.

## User-accepted drag and preview behavior

The latest recorded manual acceptance is the November 5 motor-with-four-conductors test:

- Deferring full individual-wire rerouting until node movement is committed on release eliminated the freeze/crash in that tested scene.
- Release regeneration took approximately half a second and was acceptable.
- A translucent widened corridor follows the moving node during drag.
- Preview updates are coalesced by a 50 ms timer. Slight twitching was accepted; do not tune the interval without new evidence.
- Individual colored conductors return after release.

This is acceptance for the November 5 tested scene only. The November 8 screenshots subsequently reviewed static routing appearance and found route quality unacceptable; they did not establish interactive behavior. Multi-module responsiveness remains untested.

## November 8 GUI screenshot review - completed

Evidence: commit `810e29f302d81fc5a7a4ef1102e0f415eb0cd10a`. Nine screenshots reviewed:

- `164933`, `164948`, `165002`
- `170434`, `170503`, `170527`, `170531`, `170625`, `170636`

Observed:
- All four independent conductor paths are visible in the reviewed arrangements.
- Overall route quality fails: one black conductor takes a long rectangular detour; other paths form awkward loops/tight turns with inconsistent spacing.
- Endpoint fan-outs converge visually too closely and need clearer individual presentation.
- Route shape is sensitive to component placement and small nudges.

The screenshots do not establish individual selection, drag responsiveness after the November 8 correction, multi-module performance, or delete/undo/redo/reopen recovery. Do not ask the user to repeat this screenshot review.

The current next step is architecture reconciliation, not another screenshot pass or a special-case black-wire adjustment.## Other investigation leads

`ConnectionGraphicsItem.prepare_line()` prepares and caches endpoint geometry and returns escape segments, but no caller was found in the searched production source or tests. The scene and drag preview use `setLine()` directly. Separately drawn contact `origin`-to-`anchor` stubs were not included in the inspected `routed_connection_segments` collection.

This is an investigation lead, not a proven blocked-route root cause. Do not wire `prepare_line()` into the scene merely because it exists. Review self-obstruction, endpoint protection, and cache validity against changed obstacles, fan-out offsets, and endpoint-side overrides before modifying sequential route constraints.

## Historical immediate next action from November 10 (superseded)

1. Do not repeat the November 8 static screenshot review; it is complete and recorded in the living handoff.
2. #4 prepares a concise Planning decision request for the proposed derived, presentation-only `PresentationRouteGraph`: exact per-segment connection membership, visual branch semantics, relationship to `VisualModel`/`VisualConnection`, runtime-derived initial scope, and strict separation from physical Harness membership.
3. Do not begin production implementation or change canonical schema/persistence before applicable Planning direction. The November 5 shared-envelope decision does not itself approve inferred quick-hookup grouping.
4. After Planning direction, design a bounded pure/runtime-derived prototype. Test segment membership, branches, selection resolution, endpoint fan-outs, crossings, obstacles, membership changes, and 2/4/8/12/24/32+ conductor cases.
5. Retain the independent routing-priority correction as interim behavior. Preserve #3 work and the user-owned diagnostic fixture.
6. Recheck refs, complete worktree, and shared index before every later Git write. No staging, commit, or push is authorized by this prompt.## Authority and publication

Planning owns architecture and shared canonical semantics. #4 owns routing implementation, routing diagnostics, visual integration, and these two #4 handoff documents.

Planning's shared-envelope direction is approval in principle only. It is not authorization for canonical schema/persistence changes, Stage 2A/2B implementation, or publication. No staging, commit, or push is authorized by this recovery prompt. Obtain the applicable explicit authorization before publication, and keep unrelated #3 and user-owned changes out of any #4 publication.