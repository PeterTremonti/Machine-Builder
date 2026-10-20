# Machine Builder #1 — Planning / Architecture Replacement Prompt

**Prepared:** 2026-10-20 18:38:16 -04:00

## Mission

Coordinate cross-workstream priorities, scope, dependencies, project-level documentation, and publication. Planning owns the workflow, current-state synthesis, focus index, and serialized publication queue.

## Latest verified published baseline at snapshot

- Commit: `29c2e54412c6621b112ccfee710e79e6fba46c91`
- Subject: `Record integer-key persistence investigation findings`
- Branch `main`; local `HEAD`, stored `origin/main`, and live remote `main` matched at `2026-10-20 18:38:16 -04:00`.
- This is a timestamped snapshot, not a lock. Recheck refs, status, and the shared index before acting.

## Read first

`CHAT_WORKFLOW.md`; `MASTER_PLAN.md`; `PROJECT_CURRENT_STATE.md`; `DOCUMENTATION_AUTHORITY.md`; `WORKSTREAM_FOCUS_INDEX.md`; `machine-structure-editor/handoffs/01_PLANNING_ARCHITECTURE_WORKSTREAM_HANDOFF.md`; this file.

## Planning-owned files and validation state

Planning's local batch contains:
- `CHAT_WORKFLOW.md`
- `WORKSTREAM_FOCUS_INDEX.md`
- `PROJECT_CURRENT_STATE.md`
- `machine-structure-editor/handoffs/01_PLANNING_ARCHITECTURE_WORKSTREAM_HANDOFF.md`
- `machine-structure-editor/handoffs/01_PLANNING_ARCHITECTURE_REPLACEMENT_PROMPT.md`

At this snapshot, the five Planning-owned paths are staged together as the sole contents of the shared index and remain uncommitted and unpublished. The focus index, current-state snapshot, handoff, and recovery prompt have been reviewed and passed the Planning-scoped whitespace and read-back checks. No application tests were run for this documentation-only batch.

## Queue snapshot

- **#2 Research:** Published `29c2e54412c6621b112ccfee710e79e6fba46c91` — `Record integer-key persistence investigation findings`, covering the Standards Index, Research handoff, and Research recovery prompt. Planning received closeout `MB-20261020-1149-01` (`PUBLISHED — SLOT RELEASED`). The serializer rejection is source-confirmed; the Research investigation did not reproduce runtime save/reopen failure. Later Research handoff/prompt refreshes remain local-only.
- **#3 Board:** Published checkpoint `9b3013d1cbecebbc32e6e17909a8ea09885a4833` — `Document revision-pinned TMC5160T routing evidence`. Contact-6 remains **UNRESOLVED**. #3 isolated the receiving-interface test and converted only Octopus contacts to 18 numeric-position records. The save/reopen regression and focused suite are reported passing (65 tests); Board changes remain local-only pending review and a separate Board publication slot. The generic serializer and TMC5160T map remain unchanged.
- **#4 Routing/Visual:** Yielded `NOT READY — SLOT RELEASED`. The reported 73-test focused suite and compilation/whitespace checks passed, but manual GUI acceptance gaps remain. Continue from the actual handoff and prompt structure.
- **#5 Efficiency/Audit:** The read-only editor/store mutation, undo/redo, and persistence audit is accepted as backlog guidance. It ran no tests or GUI validation; implementation candidates remain unauthorized.
- **#1 Planning:** Planning's current slot covers exactly the five listed Planning paths at the verified baseline. Complete the diff review and scoped validation, then publish this batch only. Keep every other workstream path separate.

## Required operating conventions

- One active publication slot at a time. Publish the smallest complete, coherent, validated batch within the exact grant promptly. If blocked or not ready, report the actual blocker and explicitly release the slot.
- Closeout must say `PUBLISHED — SLOT RELEASED`, `BLOCKED — SLOT RELEASED`, or `NOT READY — SLOT RELEASED`. Include exact paths, commit and verification for publication; otherwise report staged/index state, remaining local work, and next action.
- Grants are tied to the authorized paths and named baseline. If remote `main` advances, stop and request explicit renewal.
- Preserve other owners' staged, unstaged, and untracked work. Never broad-stage, reset/discard unrelated files, or force-push.
- Refresh the detailed handoff and canonical recovery prompt at material checkpoints and after publication/yield. The handoff preserves history; the prompt is the concise recovery snapshot. A chat message alone does not prove the file was written.
- Do not replace an active chat merely because its prompt is updated. Do not publish again after closeout until Planning grants another slot.

## Other local worktree paths observed in this snapshot

These 24 paths are outside Planning's ownership in this snapshot (29 changed/untracked paths total, including the five Planning-owned paths). Recheck actual status; this list is not a lock.

- ` M machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_REPLACEMENT_PROMPT.md`
- ` M machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md`
- ` M machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`
- ` M machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`
- ` M machine-structure-editor/handoffs/05_EFFICIENCY_MODULARIZATION_WORKSTREAM_HANDOFF.md`
- ` M machine-structure-editor/src/machine_builder/canvas_editing.py`
- ` M machine-structure-editor/src/machine_builder/canvas_scene.py`
- ` M machine-structure-editor/src/machine_builder/canvas_ui.py`
- ` M machine-structure-editor/src/machine_builder/graphics/connection.py`
- ` M machine-structure-editor/src/machine_builder/graphics/connection_routing.py`
- ` M machine-structure-editor/src/machine_builder/graphics/connection_routing_endpoint.py`
- ` M machine-structure-editor/src/machine_builder/graphics/node.py`
- ` M machine-structure-editor/src/machine_builder/graphics/port.py`
- ` M machine-structure-editor/src/machine_builder/hardware_catalog.py`
- ` M machine-structure-editor/src/machine_builder/semantic_component_mutations.py`
- ` M machine-structure-editor/tests/test_connection_routing.py`
- ` M machine-structure-editor/tests/test_functional_interface_connection.py`
- ` M machine-structure-editor/tests/test_octopus_driver_mating.py`
- `?? machine-structure-editor/handoffs/03_CONTROLLER_BOARD_REPLACEMENT_PROMPT.md`
- `?? machine-structure-editor/handoffs/04_ROUTING_STABILITY_REPLACEMENT_PROMPT.md`
- `?? machine-structure-editor/handoffs/05_EFFICIENCY_MODULARIZATION_REPLACEMENT_PROMPT.md`
- `?? machine-structure-editor/tests/test_connection_wire_color.py`
- `?? machine-structure-editor/tests/test_stepper_motor_terminal_profile.py`
- `?? "machine-structure-editor/wiring test machines/Maestro and 4 port motor test.machine.json"`

## Planning next action

Planning's five-path batch is staged under its current slot at the verified baseline. Commit with subject `Document publication throughput and recovery conventions`, push normally, and verify local `HEAD`, fetched `origin/main`, and live remote `main`. Preserve all other workstream paths outside this commit.
