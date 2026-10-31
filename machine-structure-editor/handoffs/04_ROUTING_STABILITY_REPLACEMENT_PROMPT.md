# Machine Builder #4 - Routing Stability / Diagnostics Replacement Prompt

Prepared: 2026-10-31 EDT
Message ID: MB4-STAGE1-PUBLISHED-CURRENT-02
Relationship: Current recovery snapshot; detailed chronology remains in `04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`.

## Mission and boundaries

Own Routing, diagnostics, and visual integration. Canonical semantic connections remain the electrical source of truth. Routing geometry and harness overview are presentation only. Coordinate shared canonical-contract changes with Planning and preserve other workstreams' files.

## Repository and workflow

- Repository: `C:\Users\Peter\Documents\GitHub\Machine-Builder`
- User executes local PowerShell/Git commands and supplies output. Never claim unverified local actions.
- Read root `CHAT_WORKFLOW.md`, `MASTER_PLAN.md`, `PROJECT_CURRENT_STATE.md`, this handoff, the #4 focus-index entry, and `DOCUMENTATION_AUTHORITY.md` when ownership/authority matters.
- Before editing or publishing, recheck root, branch, local HEAD, fetched `origin/main`, live remote main, shared index, and complete worktree status.
- One shared checkout and index. Preserve all staged, unstaged, and untracked work. Never use broad add, reset, clean, stash, or force-push.
- Use bounded PowerShell, Git, direct source inspection, and existing project tooling. No Python/Jupyter/pandas/notebooks or temporary analysis artifacts for repository work.
- Work one logical unit/file at a time; verify anchors, read back edits, inspect focused diffs, and run relevant checks. Keep console output bounded; plain PowerShell fences only.

## Published implementation and documentation commits

- Stage 1 implementation commit: `e6e3710786cb0c2b31ac166f6d020db153ffb84f`
- Subject: `feat: add canonical harness model and persistence`
- This commit contains exactly the seven authorized Stage 1 harness implementation paths. Normal push and post-push fetch/live-remote verification succeeded.
- Subsequent #4 documentation-only commit: `437750739c990c65de2d1b1956f7c7b39e7150a3`
- Subject: `docs: update routing handoff after harness publication`
- That documentation commit contains exactly the two #4-owned handoff/replacement-prompt paths; normal push and post-push fetch/live-remote verification succeeded.

These are publication records, not a guarantee of the current repository HEAD. Reverify branch, HEAD, fetched `origin/main`, live remote main, shared index, and worktree before further work or publication.

## Harness Stage 1 - published

Planning authorization: `MB-20261031-HARNESS-STAGE1-PUBLISH-AUTH-03`.

Published implementation:
- `src/machine_builder/semantic_harness.py`
- `src/machine_builder/semantic_model.py`
- `src/machine_builder/harness_mutations.py`
- `src/machine_builder/persistence.py`
- `tests/test_semantic_harness.py`
- `tests/test_harness_mutations.py`
- `tests/test_harness_persistence.py`

The canonical model supports direct connection membership, nested child harnesses, ownership/hierarchy validation, cycle prevention, recursive leaf-connection counts, deletion cleanup, and provenance/properties. Mutations implement create/update/delete, membership, and child attach/detach. `ModelStore.commit()` provides atomic application and existing undo/redo. Deletion is restricted to empty, detached harnesses.

Persistence remains format version 1. Legacy files without `harnesses` load with an empty collection. Legacy free-text `harness_id` data is preserved; it is not canonical harness identity.

Fresh publication-session validation:
- Three Stage 1 test files: 36 passed in 0.24 seconds.
- Full project suite: 927 passed in 10.36 seconds.
- Staged exact-path check and `git diff --cached --check` passed.

## Current remaining local work to preserve

Last reported status after Stage 1 publication:

#4 modified:
- `src/machine_builder/canvas_scene.py`
- `src/machine_builder/canvas_ui.py`
- `src/machine_builder/graphics/connection_routing_pathfinder.py`
- `tests/test_connection_routing.py`
- `tests/test_functional_interface_connection.py`

#3 modified:
- `handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`

#3 untracked:
- `tests/test_stepper_motor_terminal_profile.py`

User-owned modified fixture:
- `wiring test machines/Maestro and 4 port motor 4 wires J9 contact view.machine.json`

These paths are not part of Stage 1. Preserve them and recheck current status before acting.

## Current #4 routing/focus work and evidence

The two changed #4 regression test files most recently passed:
- `tests/test_connection_routing.py`
- `tests/test_functional_interface_connection.py`
- Result: 84 passed in 4.82 seconds.

The five-file #4 diff was last reported as 564 insertions and 72 deletions. Recheck current diffs and tests before implementation publication.

Keep acceptance categories distinct:

- **Protected-segment index:** automated regression tests pass. The user now reports smooth, substantially quicker responsiveness than the former severe delay. Provisionally acceptable for the current scene; multiple-module scaling remains untested.
- **Port-detail recovery after deletion/undo:** user previously reported manual correction; automated recovery and persistence tests pass. Retain the manual result as separate evidence.
- **Connector-cone wire visibility: PROVISIONAL PASS.** The user reports that all wires remain visible inside the cones in the configurations inspected. The three screenshots committed in `e577e35f1a1412b16d79b1da7406c41bff8879f6` are consistent with that observation. This is not an exhaustive test of all geometries.
- **Route-generation reliability: OPEN DEFECT.** The user reports that a wire can fail to generate when another wire is in its way. Reproduce this separately from visibility/overlap; determine whether route selection, fallback, or scene synchronization suppresses the connection. A blocked preferred route must not silently make an existing semantic connection disappear.
- **Black-wire cone approach: OPEN.** The black route takes an awkward approach and enters the side of the cone. It should approach through the intended terminal/fan-out region rather than penetrate the cone laterally.
- **Motor terminal labels: OPEN.** In the last screenshot the labels are on the wire-facing side of the terminals and are difficult to read. Prefer the non-wire-facing side where practical; check both endpoint orientations and avoid route/terminal overlap.
- **Multi-module responsiveness: NOT YET TESTED.** Current-scene responsiveness is provisionally acceptable, but repeat interaction testing with multiple modules before making a broader performance claim.

The three screenshots show all four paths visible in those captured arrangements. They demonstrate awkward black-wire geometry and label placement; they do not by themselves reproduce the separate blocked-route generation failure.

Do not mark the routing/focus work fully accepted until route-generation reliability, black-wire approach, label placement, and multi-module responsiveness have been checked and recorded. Keep each criterion separate.

## Stage 2 sequencing decisions

Planning's decision: `MB-20261031-HARNESS-STAGE1-PUBLISH-AUTH-03`; proposal reconciliation: `MB-20261031-STAGE2-RECONCILIATION-02`.

**Stage 2A is approved in principle, not yet authorized to implement.** Wait until the current #4 routing/focus work in `canvas_ui.py` and `canvas_scene.py` is reconciled, accepted, and published as its own unit.

Candidate Stage 2A production paths:
- New `src/machine_builder/harness_panel.py`
- `src/machine_builder/canvas_ui.py`
- `src/machine_builder/canvas_editing.py`
- `src/machine_builder/canvas_selection.py`

Candidate tests:
- New `tests/test_harness_store_integration.py`
- New `tests/test_harness_authoring_ui.py`
- Extend `tests/test_canvas_ui.py`

Use the published Stage 1 mutations through `ModelStore.commit()`. Do not create a separate undo system. Preserve validation, safe empty-harness deletion, persistence, and all electrical connection identities/endpoints/properties.

**Stage 2B is approved as the following architecture increment, but requires separate authorization after Stage 2A passes.** It will derive an overview from existing member connections and routes, flatten nested harnesses to leaf connections, preserve branch distinctions, safely fall back for ambiguous/disconnected geometry, and retain individually selectable original wires in Detailed view. No new electrical connections, junctions, endpoint assignments, or route-topology changes for visual trunks.

Proposed Stage 2B paths:
- New `src/machine_builder/harness_presentation.py`
- New `src/machine_builder/graphics/harness.py`
- `src/machine_builder/canvas_scene.py`
- `src/machine_builder/canvas_ui.py`
- `src/machine_builder/canvas_selection.py`
- New tests `test_harness_presentation.py` and `test_harness_graphics.py`
- Extend `test_canvas_scene.py` and `test_canvas_ui.py`

View level belongs in presentation state, not canonical electrical semantics. Do not change Stage 1 model/persistence/store contracts or routing internals without Planning review.

## Immediate next action

Finish the current #4 routing/focus unit. Resolve four-wire cone visibility and overlap; evaluate responsiveness; retain explicit manual acceptance of focus recovery. Keep #3 and the user-owned fixture outside the #4 implementation publication. Reconcile exact paths, tests, full diffs, shared index, and remote state before publishing that unit.

Do not begin Stage 2A until that publication is accepted. Do not begin Stage 2B until Stage 2A is accepted and Stage 2B is separately authorized.
