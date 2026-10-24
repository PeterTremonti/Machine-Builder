# Machine Builder - Workstream #5: Efficiency / Modularization / Audit

Prepared: 2026-10-20 18:33:24 EDT | Message ID: MB-20261020-183324-RECOVERY-01
Relationship: Current recovery snapshot associated with handoff checkpoint MB-20261020-183324-01. Planning directives MB-20261019-1749-01, MB-20261019-1752-01, and MB-20261019-1815-01 apply.

## Recovery order and authority

Read CHAT_WORKFLOW.md, MASTER_PLAN.md, PROJECT_CURRENT_STATE.md, WORKSTREAM_FOCUS_INDEX.md, and the living #5 handoff. Inspect the actual checkout before acting.

#5 performs bounded audits and evidence-based reviews. Other workstreams files are read-only unless separately authorized. Only the two canonical #5 documentation files are updated by this operation.

## Fresh repository snapshot

Captured: 2026-10-20 18:33:24 EDT
Branch: main
HEAD: 29c2e54412c6621b112ccfee710e79e6fba46c91	Record integer-key persistence investigation findings
Local origin/main: 29c2e54412c6621b112ccfee710e79e6fba46c91	Record integer-key persistence investigation findings
Live remote main: 29c2e54412c6621b112ccfee710e79e6fba46c91
Alignment: HEAD, local origin/main, and live remote main agree.

### Staged paths before this documentation update
```text
CHAT_WORKFLOW.md
PROJECT_CURRENT_STATE.md
WORKSTREAM_FOCUS_INDEX.md
machine-structure-editor/handoffs/01_PLANNING_ARCHITECTURE_REPLACEMENT_PROMPT.md
machine-structure-editor/handoffs/01_PLANNING_ARCHITECTURE_WORKSTREAM_HANDOFF.md
```

### Working-tree status before this documentation update
```text
M  CHAT_WORKFLOW.md
M  PROJECT_CURRENT_STATE.md
M  WORKSTREAM_FOCUS_INDEX.md
A  machine-structure-editor/handoffs/01_PLANNING_ARCHITECTURE_REPLACEMENT_PROMPT.md
M  machine-structure-editor/handoffs/01_PLANNING_ARCHITECTURE_WORKSTREAM_HANDOFF.md
 M machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_REPLACEMENT_PROMPT.md
 M machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md
 M machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md
 M machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md
 M machine-structure-editor/handoffs/05_EFFICIENCY_MODULARIZATION_WORKSTREAM_HANDOFF.md
 M machine-structure-editor/src/machine_builder/canvas_editing.py
 M machine-structure-editor/src/machine_builder/canvas_scene.py
 M machine-structure-editor/src/machine_builder/canvas_ui.py
 M machine-structure-editor/src/machine_builder/graphics/connection.py
 M machine-structure-editor/src/machine_builder/graphics/connection_routing.py
 M machine-structure-editor/src/machine_builder/graphics/connection_routing_endpoint.py
 M machine-structure-editor/src/machine_builder/graphics/node.py
 M machine-structure-editor/src/machine_builder/graphics/port.py
 M machine-structure-editor/src/machine_builder/hardware_catalog.py
 M machine-structure-editor/src/machine_builder/semantic_component_mutations.py
 M machine-structure-editor/tests/test_connection_routing.py
 M machine-structure-editor/tests/test_functional_interface_connection.py
 M machine-structure-editor/tests/test_octopus_driver_mating.py
?? machine-structure-editor/handoffs/03_CONTROLLER_BOARD_REPLACEMENT_PROMPT.md
?? machine-structure-editor/handoffs/04_ROUTING_STABILITY_REPLACEMENT_PROMPT.md
?? machine-structure-editor/handoffs/05_EFFICIENCY_MODULARIZATION_REPLACEMENT_PROMPT.md
?? machine-structure-editor/tests/test_connection_wire_color.py
?? machine-structure-editor/tests/test_stepper_motor_terminal_profile.py
?? "machine-structure-editor/wiring test machines/Maestro and 4 port motor test.machine.json"
```

The status above is a pre-update snapshot. Recheck Git status and remote state before any publication.

## Current #5 files

- machine-structure-editor\handoffs\05_EFFICIENCY_MODULARIZATION_WORKSTREAM_HANDOFF.md
- machine-structure-editor\handoffs\05_EFFICIENCY_MODULARIZATION_REPLACEMENT_PROMPT.md

Both are local working-tree documentation files. They have not been staged, committed, or pushed by this operation.

## Publish-and-yield and mandatory closeout

A publication turn requires fresh verification of branch, HEAD, local origin/main, live remote main, the whole working tree, and the shared staged index. Publish only a coherent, complete, validated batch inside the exact grant. Stage only authorized paths, inspect the entire staged diff, commit and push normally, verify remote state, and release the slot.

Immediately afterward, send Planning a distinct closeout:
- PUBLISHED - SLOT RELEASED: full commit hash and subject, exact paths, validations, confirmation local HEAD/origin/main/live remote agree, remaining local work, and next action.
- BLOCKED - SLOT RELEASED: failed guard, staged status, modified files, and safe next action.
- NOT READY - SLOT RELEASED: why no coherent complete batch can publish, what would make it ready, and next development action.

If blocked or not ready, do not publish. Report and release the slot. Never disturb another workstream staged/unstaged files, never force-push, and never unstage without verifying that the index contains only paths authorized to #5.

No #5 publication slot is granted by this snapshot. Recovery files remain outside other workstreams publication scope unless explicitly authorized.

## Accepted audit state

Planning accepted the read-only editor-state/undo-redo/persistence audit in MB-20261018-1312-01. No blocking defect was demonstrated in inspected normal paths. #5 ran no tests and performed no GUI validation.

Backlog only: persistence failure-injection tests; listener-exception semantics; assessment of live mutable store access as a potential risk unless a concrete bypass is demonstrated; optional canonical-model assertions in app-level undo/redo integration.

The suspected canvas_editing.py bypass was withdrawn because the referenced machine dictionary expressions were reads. No ordinary UI bypass was demonstrated.

Previously accepted modularity backlog: narrow route-stability/diagnostics boundary in graphics/connection.py after characterization tests; a small Qt-independent focus-projection helper for canvas_ui.py/canvas_scene.py after #4 interaction work stabilizes; defer graphics/node.py overlay separation while it overlaps active #4 work.

## Exact next action

Recheck the #5 diff and current status after this update. Await the next bounded review assignment or explicit publication grant. Do not stage, commit, or push until Planning grants a slot. At the next granted turn, publish only a complete authorized batch or send the required BLOCKED/NOT READY closeout and yield.

## Planning Disposition - 2026-10-23 - Large-File Audit Accepted

Prepared: 2026-10-23 15:15 EDT | Message ID: MB-20261023-1515-02
Relationship: Supersedes the 2026-10-20 recovery snapshot for startup continuity. Records Planning handoff MB-20261023-1136-01 and matching #5 handoff checkpoint MB-20261023-1515-01.

### Completed audit and Planning disposition

The read-only large-file audit is complete. Planning disposition: AUDIT ACCEPTED; BROAD REFACTORS DEFERRED. Findings below are recommendations, not implementation authorization. No source or test files were changed and no tests were run as part of this large-file audit.

1. Pathfinder efficiency candidate: in machine-structure-editor/src/machine_builder/graphics/connection_routing_pathfinder.py, consider hoisting repeated sorted(coordinates_y) outside the X-coordinate loop. First confirm the Y-coordinate set remains unchanged throughout the loop, measure representative before/after performance, and verify routing regressions and route output. Keep this separate from grid/adjacency extraction. This is #4-owned routing code; #5 must not implement it.

2. Pathfinder modularity candidate: separately consider extracting grid and adjacency construction from _find_grid_route(). Defer until routing stabilizes and Planning assigns the work.

3. Controller fixtures: board-specific fixture-builder extraction is future maintainability work. #3 active Promega/Maestro work takes precedence. Do not edit #3-owned files.

4. Hardware catalog: consider modularization by generic hardware and controller-board family while preserving compatible public imports. Do not introduce a database solely because the file is large. Do not edit #3-owned files.

5. Connection graphics and canvas interaction: defer refactoring graphics/connection.py and canvas_interaction.py until #4 completes routing and GUI acceptance. Do not touch or reorganize #4-owned files.

6. Canonical model: retain CanonicalMachineModel as the central aggregate. Do not split it merely to reduce line count; extraction requires a concrete, independent responsibility and preservation of canonical invariants.

7. Large test modules: defer test-file organization. Preserve behavioral coverage, hardware-evidence assertions, and regression checks. Do not reorganize tests that overlap active #3/#4 work.

8. Heater-builder estimate correction: the heater builder itself spans approximately 96 lines, not hundreds. The earlier larger estimate incorrectly included following data constants.

### Queue, authority, and next action

The last recorded queue context gave #2 Research priority for publication, #3 bounded Promega/Maestro fan-assignment work, and #4 routing/GUI remediation. Treat that queue as historical until current handoffs and the focus index are checked. The local snapshot inspected for this prompt had branch main, HEAD and origin/main at ef3185cbd09e0a65faeb09166cd75e592bce0885, and an empty shared index. Live remote main was not queried during that inspection.

Continue protecting all concurrent work. Finish validating the two #5-owned documentation updates, then report the exact paths, read-back results, focused diffs, whitespace validation, index state, and any blocker to Planning in a distinct timestamped message.

No source or test edits are authorized by this task. No #5 publication slot is granted. Do not stage, commit, or push.

## Latest Planning Disposition - Stable-Code Efficiency Audit - 2026-10-24

Prepared: 2026-10-24 17:40 EDT | Message ID: MB-20261024-1740-01
Relationship: Supersedes the stale repository snapshot above for current recovery; records Planning disposition MB-20261024-1203-01 for audit MB-20261024-1141-01.

### Repository state and timestamp boundaries

Audit snapshot at 2026-10-24 11:58:58 EDT: local HEAD, fetched origin/main, and live remote main were 2973f0798878484010d0a0a94daa30b03d31e330 (model Promega Z-motor driver assignment). The assigned baseline d976a90d7eed78fa11924baad9f6dc52cd882f11 was an ancestor. The shared index was empty at that inspection.

Subsequent published advances observed: 7e25fe51c0f39f9e28ebfa063a813040949e679e (test Promega specimen round-trip acceptance), then 4b72c625d7103d5c04311f2ed6436191d19941b7 (screenshots of the current wiring issues). At the read-only check at 2026-10-24 17:40:34 EDT, local HEAD, origin/main, and live remote main all matched 4b72c625d7103d5c04311f2ed6436191d19941b7. The shared staged diff was empty and this prompt was clean before this edit.

At 2026-10-24 17:35:59 EDT, concurrent unstaged work remained in #3 and #4 handoffs, canvas/routing/store code, associated tests, and a wiring test-machine JSON. The #5 handoff was subsequently updated locally and its focused diff/read-back/whitespace checks passed at 17:38:34 EDT. These are dated snapshots, not claims about later repository state.

### Candidate 1 - semantic-model ownership lookup

Path: machine-structure-editor/src/machine_builder/semantic_model.py, CanonicalMachineModel._machine_for_canonical_object() and controller-resource assignment callers.

The ownership helper repeatedly searches component port memberships even though component-owned SemanticPort values carry component_id and the model has a ports dictionary. This is a likely inefficiency, not a demonstrated material runtime bottleneck; no before/after timing was performed.

Planning decision: DEFER. Reassess only after #3 model/resource and combined specimen persistence work and #4 GUI work stabilize. No implementation is authorized.

Future acceptance gate: focused tests for same-machine ownership, cross-machine rejection, controller-owned-port behavior, and assignment save/reopen, plus a small before/after timing comparison. Preserve all existing ownership semantics.

### Candidate 2 - store deep-copy snapshot cost

Path: machine-structure-editor/src/machine_builder/store.py, published ModelStore.commit(), undo(), and redo() snapshot paths. This file had concurrent local changes during the audit and was treated as provisional.

Planning decision: MEASUREMENT FIRST; implementation deferred. After the owning store/editor changes stabilize, benchmark commit, undo, and redo latency on the Promega specimen and a larger representative model.

Future acceptance gate: record representative timings and establish a material problem before proposing a change. Preserve rollback, undo/redo, and cross-model consistency regressions.

### Authority and next action

Planning accepted this audit and deferred both candidates. Do not split modules solely for line count. Do not interfere with #3 or #4 active files or revisit pathfinder/connection-graphics/canvas refactors during #4 work. No implementation is authorized. No source or test files were changed by this audit.

Next action: no #5 implementation is pending. Reassess candidate 1 after #3/#4 changes stabilize; consider candidate 2 only if measurements justify it. Await a new bounded Planning assignment. This update is local continuity documentation only: do not stage, commit, or push.
