# Machine Builder #4 - Routing Stability / Diagnostics Replacement Prompt

Prepared: 2026-10-30 09:16:49 -04:00
Message ID: MB4-HARNESS-STAGE1-CURRENT-01
Relationship: Current #4 recovery snapshot. Detailed chronology and prior investigation evidence remain in `04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`.

## Mission and ownership

Own routing, diagnostics, and visual integration work for Machine Builder. Preserve canonical semantic connections as the electrical source of truth; routing and harness presentation are views over that model. Coordinate shared-contract changes with Planning and the responsible workstream. Do not edit another workstream's owned files.

## Recovery requirements

- Repository: `C:\Users\Peter\Documents\GitHub\Machine-Builder`.
- Read root `CHAT_WORKFLOW.md`, `MASTER_PLAN.md`, `PROJECT_CURRENT_STATE.md`, this workstream's handoff, and the #4 entry in `WORKSTREAM_FOCUS_INDEX.md`. Read `DOCUMENTATION_AUTHORITY.md` when ownership or publication authority is relevant.
- Local source, tests, Git state, and fresh user-provided observations are authoritative. Recheck repository root, branch, HEAD, `origin/main`, live remote, shared index, and worktree before editing or publishing.
- This is one shared checkout and one shared Git index. Preserve all staged, unstaged, and untracked changes. Never use broad add, reset, clean, stash, or force-push operations.
- The user executes local PowerShell/Git commands and supplies output. Do not claim a change, test, or publication until returned evidence verifies it.
- For repository work, do not use Python, Jupyter, pandas, notebooks, temporary scripts, or analysis artifacts. Use bounded PowerShell, Git, direct source inspection, and existing project tooling/tests.
- Work one file or logical unit at a time. Verify exact anchors, make a guarded edit, read it back, inspect its focused diff, and run relevant checks separately. Keep console output bounded and PowerShell code fences plain.

## Verified baseline before this documentation update

At the 2026-10-30 08:40 EDT preflight, branch `main`, `HEAD`, `origin/main`, and live remote `main` all matched `367e427aa42a8c4606e09700d536b8bf73d68c19`; the shared index was empty. The #4 handoff continuity checkpoint was subsequently added locally. Reverify all refs and the index before publication; do not assume this baseline remains current.

## Stage 1 - accepted; implementation remains local-only

Planning accepted canonical harness Stage 1 under `MB-20261029-HARNESS-STAGE1-ACCEPTANCE-02`. Its exact seven implementation paths are:

1. `machine-structure-editor/src/machine_builder/semantic_harness.py` (new)
2. `machine-structure-editor/src/machine_builder/semantic_model.py` (modified)
3. `machine-structure-editor/src/machine_builder/harness_mutations.py` (new)
4. `machine-structure-editor/src/machine_builder/persistence.py` (modified)
5. `machine-structure-editor/tests/test_semantic_harness.py` (new)
6. `machine-structure-editor/tests/test_harness_mutations.py` (new)
7. `machine-structure-editor/tests/test_harness_persistence.py` (new)

The accepted model supports stable harness IDs/names, direct semantic-connection membership, child harness relationships, properties, provenance, hierarchy and ownership validation, cycle detection, and recursive leaf-wire counts. Mutations cover create/update/delete, connection membership, and child attachment/detachment. Connection/component deletion removes only invalid incident connection memberships while preserving harnesses, child relationships, and unrelated membership. Persistence remains format version 1; older version-1 files without `harnesses` load with an empty collection, and legacy free-text `harness_id` remains untouched.

Reported and Planning-accepted validation: 24 semantic-harness tests, 7 mutation tests, 5 harness-persistence tests, 25 persistence/store tests, and 24 semantic-model tests passed. The full project suite reported 927 passed in 9.01 seconds (exit 0); collection found 927 tests; implementation `git diff --check` passed. Treat these as reported automated results, not GUI acceptance.

All seven implementation paths remain local-only. They are not authorized for this documentation commit.

## Other worktree changes to preserve

The last preflight also showed #4 changes in `canvas_scene.py`, `canvas_ui.py`, `graphics/connection_routing_pathfinder.py`, `tests/test_connection_routing.py`, and `tests/test_functional_interface_connection.py`; #3 changes in its handoff and `tests/test_stepper_motor_terminal_profile.py`; a user-owned wiring diagnostic fixture; and two unusual untracked console-artifact filenames. Reinspect current status and preserve all of them. None belongs in the documentation commit.

## GUI acceptance status

The narrow Phase C delete/undo focus-recovery check was manually reported corrected: undo restored the expected view. Overall GUI acceptance remains incomplete. The latest recorded observations still report inconsistent four-wire visibility inside the contact cone, black-wire overlap/occlusion of other stubs, and responsiveness that improved but remained laggy. Keep manual GUI findings distinct from automated test results; do not mark the editor fully accepted.

## Current documentation authorization and next actions

Planning's `MB-20261029-HARNESS-STAGE1-ACCEPTANCE-02` authorizes #4 to update and publish these two #4-owned paths without another Planning approval:

- `machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`
- `machine-structure-editor/handoffs/04_ROUTING_STABILITY_REPLACEMENT_PROMPT.md`

The handoff received a new Stage 1 acceptance continuity checkpoint. This prompt now reflects that checkpoint. Publish only these two documents in a dedicated documentation-only commit:

1. Fetch and verify branch, HEAD, `origin/main`, live remote main, and an empty shared index immediately before staging.
2. Stage the two exact paths only. Inspect the complete staged diff, confirm no unrelated content is staged, and run `git diff --cached --check`.
3. Commit and push with normal, non-forced operations. Do not include implementation changes or any other workstream/user files.
4. Verify the commit locally, against fetched `origin/main`, and against live remote main. Report the exact commit and release the documentation slot to Planning.
5. Submit a concrete Stage 2 implementation boundary and test plan to Planning. Do not implement Stage 2 until explicitly authorized.

## Stage 2 proposal boundary - not authorized for implementation

The proposed Stage 2 scope is harness authoring plus dual-level presentation: a grouped overview/trunk representation and a detailed view of individual semantic wires. Harness membership remains organizational/presentational; it must not create, delete, merge, redirect, or alter electrical semantic connections, endpoint identity, or signal direction.

The Planning proposal should define:

- UI operations for creating, renaming, deleting, nesting, attaching, and detaching harnesses, including undo/redo and persistence behavior.
- Overview rendering for grouped members and detailed rendering for the original individual wires. Switching levels must preserve the exact underlying semantic connections.
- Deterministic treatment of branches, shared endpoints, nested groups, and ambiguous or disconnected topology. Ambiguous grouping must fall back safely to individual-wire presentation rather than imply an electrical junction.
- Tests for model invariance across view changes; membership and hierarchy operations; undo/redo; save/reload; nested and branched topology; selection/hit testing; and both rendering levels. Include explicit GUI acceptance cases.
- A strict separation between visual trunk geometry and electrical connectivity/direction. A visual trunk is not a physical conductor or a new semantic connection.

Stage 2 remains pending Planning review and explicit authorization. Do not change rendering or authoring code for it before that authorization.
