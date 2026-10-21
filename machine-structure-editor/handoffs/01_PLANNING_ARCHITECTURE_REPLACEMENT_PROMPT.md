# Machine Builder #1 - Planning / Architecture Replacement Prompt

**Prepared:** 2026-10-21 15:23 EDT

## Mission

Coordinate cross-workstream priorities, scope, dependencies, architectural decisions, project documentation, and serialized publication. Planning owns project-level state synthesis and decides what work is authorized, by whom, and against which baseline.

## Latest verified published baseline at snapshot

- Commit: `dfefa9df337bc431a0056554d5c72843075132cf`
- Subject: `Refresh Research recovery handoff and replacement prompt`
- At the last reported preflight (2026-10-21 11:16 EDT), branch `main`, local HEAD, fetched `origin/main`, and live remote `main` matched; the shared index was empty.
- This is a checkpoint, not a lock. Recheck all refs, index state, and worktree changes before acting.

## Read first

`CHAT_WORKFLOW.md`; `MASTER_PLAN.md`; `PROJECT_CURRENT_STATE.md`; `DOCUMENTATION_AUTHORITY.md`; `WORKSTREAM_FOCUS_INDEX.md`; this handoff; this replacement prompt.

Follow Section 17 of `CHAT_WORKFLOW.md` for universal workstream recovery and repository preflight.

## Architecture and authority invariants

- The canonical machine model is authoritative.
- The visual editor is both an inspection view and an authoring surface: user edits must change the actual canonical machine through the appropriate mutation and persistence paths.
- Semantic connections and endpoint identities are distinct from visual route geometry and styling.
- Reusable `HardwareDefinition`, installed `MachineComponent`, `SemanticPort`, and `SemanticConnection` remain separate concepts.
- Do not invent missing hardware/evidence or apply electrical-specific rules indiscriminately to fluid, mechanical, or other relationship types.
- Use one authoritative document per primary question and preserve separate implementation ownership.

## Published checkpoints

- Planning workflow/continuity rules: `f5c02430496ebb5afb406ac7783a7d746c09c503` - `Document publication throughput and recovery conventions`.
- Octopus receiving-interface persistence: `ae5a9a1672d151c37e392e9bff4f2421f0a465f2` - `Fix Octopus receiving-interface persistence`.
- Research recovery refresh: `dfefa9df337bc431a0056554d5c72843075132cf` - `Refresh Research recovery handoff and replacement prompt`.

Research has made later local-only edits to its two handoff files. Those edits are not part of `dfefa9d` and have not been authorized for publication.

## Current workstream status

### #1 Planning

This continuity refresh was prepared against baseline `dfefa9df337bc431a0056554d5c72843075132cf`. Verify actual refs and repository status before acting. This snapshot records the pre-publication base; do not repeat a publication that is already complete.

The proposal to add a lightweight `Prior-Art Review?` decision point to `CHAT_WORKFLOW.md` has been approved in principle. The edit should make research proportional to complexity, novelty, risk, and expected benefit; routine fixes should remain fast. It is a separate documentation task and has not yet been published.

### #2 Research

The comparative study reported in `MB-20261021-1115-01` is complete and read-only. It examined KiCad, QElectroTech, WireViz, LibrePCB, libavoid, and Qt Graphics View, and recommended future bounded improvements rather than a rewrite or immediate dependency adoption. No tests, code edits, or repository publication came from the study.

The later Research handoff/prompt refresh remains local-only and needs its own explicit publication slot.

### #3 Controller / Board

The Octopus receiving-interface persistence fix is published as `ae5a9a1`. Driver 2 contact-6 `SLEEP` versus TMC5160T Pro J1-6 `CLK` remains **UNRESOLVED**.

The Board handoff is modified locally and its replacement prompt is untracked. Both require accurate baseline and published-state references. `tests/test_stepper_motor_terminal_profile.py` imports `UpdateMachineComponentWithStepperTerminalProfile`, which was reported present only in #4's uncommitted `semantic_component_mutations.py`. Keep the Board test unpublished until the implementation prerequisite is published and validated. Then authorize a separate Board batch.

### #4 Routing / Visual

#4's complete-suite gate remains blocked by native Qt/PySide6 teardown aborts after pytest reports passing tests. Reverse-order runs were inconsistent. The selection-inspector whole-file and subset experiments did not establish a stable minimal reproducer. Source inspection did not establish a causal defect.

The controlled `QApplication` retention confirmation had two clean exits and two native aborts in each of its control and retention conditions. It did not distinguish the conditions. Per `MB-20261021-1137-01`, further experiments are paused while Planning refreshes continuity documentation; Experiment B is not authorized.

No #4 publication slot is open. The complete 17-path diff review and GUI acceptance requirements remain outstanding: visible framing on reopen without pressing F, fan-out readability, breakout-box/title placement, overlapping-wire selection, focus after delete and undo/redo, and saved-file reopen behavior. The Board-owned stepper-terminal test remains outside #4's publication scope.

### #5 Efficiency / Audit

The prior read-only audit remains backlog guidance, not implementation authorization. #5 **is authorized to edit, stage, commit, and push its own handoff and replacement prompt** under a bounded publication slot. The read-only audit boundary applies to project implementation and other workstreams' files. Its handoff is modified and its replacement prompt is untracked; both remain local-only until #5 receives and completes a publication slot.

## Last reported uncommitted worktree inventory

#4's preflight at 2026-10-21 11:16 EDT reported the following paths outside the published baseline. This list is historical evidence, not a lock; rerun `git status --short --untracked-files=all`.

**Modified**
- `machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_REPLACEMENT_PROMPT.md`
- `machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md`
- `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`
- `machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`
- `machine-structure-editor/handoffs/05_EFFICIENCY_MODULARIZATION_WORKSTREAM_HANDOFF.md`
- `machine-structure-editor/src/machine_builder/canvas.py`
- `machine-structure-editor/src/machine_builder/canvas_editing.py`
- `machine-structure-editor/src/machine_builder/canvas_scene.py`
- `machine-structure-editor/src/machine_builder/canvas_ui.py`
- `machine-structure-editor/src/machine_builder/graphics/connection.py`
- `machine-structure-editor/src/machine_builder/graphics/connection_routing.py`
- `machine-structure-editor/src/machine_builder/graphics/connection_routing_endpoint.py`
- `machine-structure-editor/src/machine_builder/graphics/node.py`
- `machine-structure-editor/src/machine_builder/graphics/port.py`
- `machine-structure-editor/src/machine_builder/semantic_component_mutations.py`
- `machine-structure-editor/src/machine_builder/store.py`
- `machine-structure-editor/tests/test_connection_routing.py`
- `machine-structure-editor/tests/test_functional_interface_connection.py`

**Untracked**
- `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_REPLACEMENT_PROMPT.md`
- `machine-structure-editor/handoffs/04_ROUTING_STABILITY_REPLACEMENT_PROMPT.md`
- `machine-structure-editor/handoffs/05_EFFICIENCY_MODULARIZATION_REPLACEMENT_PROMPT.md`
- `machine-structure-editor/tests/test_connection_wire_color.py`
- `machine-structure-editor/tests/test_stepper_motor_terminal_profile.py`
- `machine-structure-editor/wiring test machines/Maestro and 4 port motor test.machine.json`

## Required operating conventions

- There is one active publication slot at a time. Each slot names an exact baseline and exact paths.
- Perform fresh preflight before acting; if baseline or index conditions differ from the grant, stop and report actual evidence.
- Preserve other owners' modified, staged, and untracked files. Never broad-stage, reset/discard another owner's work, or force-push.
- Stage only authorized paths, inspect the complete staged diff, and verify content as well as path membership.
- After a normal push, fetch and verify local HEAD, fetched `origin/main`, and live remote `main` all match.
- Closeout must end with exactly one of `PUBLISHED - SLOT RELEASED`, `BLOCKED - SLOT RELEASED`, or `NOT READY - SLOT RELEASED`.
- Refresh detailed handoffs and concise recovery prompts at material checkpoints. Read the actual files back; a drafted or sent chat message does not prove that a repository document was updated.
- #5 may publish its own handoff and replacement prompt under its own bounded authorization. It must preserve all other workstreams' files and staged state.

## Planning next actions

1. Verify the actual refs and working tree. If the two-file Planning continuity refresh is still uncommitted, complete its authorized publication; if already published, do not repeat it.
2. Publish the approved `CHAT_WORKFLOW.md` prior-art decision point in a separate documentation batch.
3. Reassess the live repository before assigning separate slots for #3's corrected Board handoff/prompt, #2's later Research recovery refresh, and #5's own documentation.
4. Decide whether to resume #4's read-only diagnosis after the continuity checkpoint. Do not treat the native teardown issue as resolved or its implementation batch as publishable.
