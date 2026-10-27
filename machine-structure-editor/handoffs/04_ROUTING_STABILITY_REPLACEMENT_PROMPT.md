## Current checkpoint — 2026-10-26: post-routing publication

This checkpoint supersedes earlier statements below that the routing publication had not occurred or that the previous baseline was still current.

- Published commit: `2863e2ce3077bd5fff43a359ca19e2a014746952` — `fix: stabilize functional connection fan-out routing`.
- Verified after push: local `HEAD`, `origin/main`, and live remote `main` all matched that commit.
- Validation before publication: all seven staged Python files compiled; the complete test suite passed, **888 passed in 19.87 seconds**.
- The published commit contains the seven authorized routing/fan-out paths. Three of those paths still have separate working-tree edits; those edits remain part of the unpublished work.
- Remaining shared-checkout status: 19 paths. The intended next batch is the 17 #4-owned paths; preserve `handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md` and `tests/test_stepper_motor_terminal_profile.py` as #3-owned.
- The remaining 17-file batch is not yet staged, committed, or pushed. Before publication, verify exact path scope, whitespace, staged syntax, and the full test suite against the final candidate.
# Machine Builder #4 — Routing / Diagnostics / Visual Integration

Prepared: 2026-10-22
Canonical repository: `C:\Users\Peter\Documents\GitHub\Machine-Builder`
Worktree: `machine-structure-editor`
Detailed history and current checkpoints: `handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`
Latest checkpoint: `MB4-ROUTING-REMEDIATION-RESULTS-20261022`

## Mission and boundaries

Maintain the visual connection-routing/editor integration while keeping canonical semantics authoritative. Connector-level functional references do not prove individual conductor mapping, coil pairing, as-built wiring, or firmware correctness.

All workstreams share a checkout and Git index. Preserve concurrent edits. Do not stage, commit, or push without a separate explicit Planning publication authorization.

## Latest verified baseline and index

Last verified baseline remained branch `main`, with local HEAD, fetched `origin/main`, and live remote main at `9b51df9ce2cfdcefcd47f1910343b0b7e694b301`. The shared index was empty before the current validation and remains expected to stay empty.

Never edit #3/#5 files or the user-owned diagnostic fixture. Explicitly exclude:
- `tests/test_stepper_motor_terminal_profile.py` (Board-owned).
- `wiring test machines/Maestro and 4 port motor test.machine.json` (user-owned diagnostic fixture).
- `handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md` (#3).
- `handoffs/05_EFFICIENCY_MODULARIZATION_WORKSTREAM_HANDOFF.md` and `handoffs/05_EFFICIENCY_MODULARIZATION_REPLACEMENT_PROMPT.md` (#5).

## Current #4 remediation changes

- Stepper-terminal mutation now validates owner, interface role, physical-terminal granularity, stepper-four-lead profile, and expected display index for existing generated terminal IDs before changing component details.
- The mutation rejects an invalid visual motor type before mutation.
- Selector choices now consistently say all ports, unused ports, and used ports in both initial construction and refresh.
- The `_model_changed` docstring is in method-docstring position.
- `tests/test_functional_interface_connection.py` adds conflict and invalid-type rejection/rollback coverage plus undo/redo and persistence coverage.
- `tests/test_canvas_ui.py` checks selector labels and data keys before and after refresh.

The current candidate consists of the two #4 handoff/prompt files, eleven implementation/store files (`canvas.py`, `canvas_editing.py`, `canvas_scene.py`, `canvas_ui.py`, five graphics files, `semantic_component_mutations.py`, `store.py`), and four tests (`test_canvas_ui.py`, `test_connection_routing.py`, `test_functional_interface_connection.py`, `test_connection_wire_color.py`). This is 17 candidate paths. Verify exact current status before any publication request.

## Post-remediation test results

Environment: project `.venv`, Python 3.14.7, pytest 8.4.2, PySide6 6.11.2.

1. `.venv\Scripts\python.exe -X faulthandler -m pytest -q tests/test_functional_interface_connection.py -k 'stepper_terminal_profile_rejects_conflicting_existing_terminal_metadata'` — 5 passed, 11 deselected in 0.97s; actual process exit `0`.
2. `.venv\Scripts\python.exe -X faulthandler -m pytest -q tests/test_functional_interface_connection.py tests/test_canvas_ui.py tests/test_connection_routing.py tests/test_connection_wire_color.py` — 87 passed in 2.47s; actual process exit `0`.
3. `.venv\Scripts\python.exe -X faulthandler -m pytest -q` — 876 passed in 6.19s; actual process exit `0`.
4. `git diff --check` on the changed tracked source/test paths — exit `0`; Git emitted an LF/CRLF advisory for `tests/test_functional_interface_connection.py`, not a whitespace failure.

Two earlier attempts failed because the new test fixture was invalid; the final corrected targeted, focused, and full runs above all passed. Do not reuse those failed-run counts as current results.

## Separate environment issue — do not conflate

The global interpreter with PySide6 6.12.0 separately showed a native Qt teardown/access-violation failure after passing-test output. Historical exits include `-1073741819` (`0xC0000005`) and `-1073740791` (`0xC0000409`). The cause has not been established. The project `.venv` pass must not be described as resolving that separate failure.

## GUI acceptance — FAILED on 2026-10-22

Fresh user report:
- The black wire still runs up and through the cone.
- Near the bottom, only the red wire can be selected.
- The breakout still covers the Maestro board name.
- Delete changes focus to “Functional interfaces”; undo does not restore the previous focus.
- Reopening a saved file retains the focus currently selected at open time rather than restoring the saved focus.
- Viewport framing and saved component-coordinate changes were not separately assessed.

A subsequent large read-only source-inspection paste was followed immediately by a console/window crash, exit `-1073741819` (`0xC0000005`). No inspection result was captured and no cause is established. Do not repeat the large paste; inspect source in smaller bounded excerpts.

The project `.venv` automated results remain clean: targeted metadata regressions 5 passed (exit 0), focused suite 87 passed (exit 0), full suite 876 passed in 6.19 seconds (exit 0), and tracked diff check exit 0 with an LF/CRLF advisory. These tests do not close GUI acceptance.

Next action: inspect routing/hit testing, breakout geometry, focus change/undo behavior, and focus persistence in small source excerpts; make only authorized #4-owned fixes; retest the live GUI and record each observation. Keep the global Python/PySide6 6.12.0 teardown failure separate and unresolved.

## Current closeout

`NOT READY — SLOT RELEASED`.

Automated remediation tests pass in the project `.venv`. Current visual acceptance and final integrated diff review remain outstanding, so the candidate must not be published. The global-interpreter native teardown issue remains separate and unresolved.

<!-- MB4-CURRENT-CHECKPOINT-20261025 -->

## Current continuity checkpoint - 2026-10-25

This checkpoint supersedes the older baseline recorded above.

- Repository: `C:\Users\Peter\Documents\GitHub\Machine-Builder`
- Branch: `main`
- Latest verified HEAD, `origin/main`, and live remote main: `e4d2387bbde9b67f664f49c9bc7ef777518160b3`
- The shared Git index was empty at the latest check. Preserve all concurrent changes. Do not reset, clean, stash, or broadly stage files.
- The #4 handoff contains the console-command incident notes. The separate prompt update and code correction remain independent tasks.
- The proposed cone-base intersection correction has NOT been applied or tested. The last guarded source-replacement attempt stopped before writing because a fan-out loop anchor occurred twice.
- A later prompt-edit attempt stopped before writing because the local PowerShell/.NET runtime does not support `SHA256.HashData()`. Use `Get-FileHash` for SHA-256 comparison in this environment.
- Current GUI failures remain unresolved: wire crossing the cone, overlapping-wire selection, breakout/title overlap, delete/undo focus behavior, and saved-focus restoration. Reopen framing and saved coordinate persistence still lack separate acceptance evidence.
- Treat contact-stub overlap as a leading hypothesis, not a proven root cause. The raw `zValue()` comparison between a child cone and a top-level connection is a test weakness, not proof of the visual failure's cause.

## Immediate next action

Capture one bounded diagnostic for the actual black connection: contact-stub endpoints, grouped fan-out point, endpoint escape points, and the first main-route segments. Identify the first segment that deviates from intended geometry before changing code.

Continue one operation at a time. Inspect current source and status; make a single-file guarded edit only when supported by evidence; read back and inspect that file's focused diff; run its relevant check in a separate command. Do not automatically run the full suite in the same operation.

Record fresh GUI results separately from automated tests. Do not save over the user-owned diagnostic fixture. Preserve #3 files/tests and user-owned wiring fixtures. No staging, commit, push, or publication authorization.
