<!-- MB4-PROTECTED-INDEX-CURRENT-PROMPT-20261028 -->
## Current replacement-chat checkpoint - 2026-10-28
Message ID: MB-20261028-ROUTING-PROTECTED-INDEX-VALIDATION-RESULTS-01

This is the authoritative current state for replacement-chat startup. Older entries below are retained as history and may describe earlier authorization or validation states. Use this checkpoint when those entries conflict with the current state.

### Current repository and authorization boundary
- Repository: `C:\Users\Peter\Documents\GitHub\Machine-Builder`; shared `main` checkout and shared Git index.
- Last verified publication baseline before this documentation update: `cb65c45dd768dd9c3fd56865c2a74c07f73d4f53`; `HEAD`, local `origin/main`, and live `origin/main` matched, and the shared index was empty. Reverify all refs and the index before any stage, commit, or push.
- #1 explicitly authorizes #4 to publish only these two #4-owned documents in a dedicated documentation-only commit, after exact-diff and whitespace gates pass:
  - `machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`
  - `machine-structure-editor/handoffs/04_ROUTING_STABILITY_REPLACEMENT_PROMPT.md`
- This does not authorize publishing the pathfinder source or routing tests. Keep all implementation changes and every other workstream's changes intact. Never stage broadly, reset, discard, or force-push.

### Protected-segment index implementation and validation
- The production pathfinder now uses an orientation-aware spatial index to narrow protected-segment checks. The existing `route_respects_segment_separation` remains authoritative for each returned candidate; lane generation and unrelated routing behavior were not intentionally changed.
- Syntax validation passed. Focused protected-segment-index tests: 2 passed. Complete routing test file: 65 passed. Functional-interface tests: 18 passed. Full project suite: 890 passed in 10.30 seconds.
- Differential validation checked 289,623 routing-edge decisions with zero mismatches. The index presented 36,145 candidates versus 4,178,871 entries for full scans, about 99.14% fewer entries presented.
- Three controlled fixed-seed baseline/candidate pairs produced identical route geometry, pathfinder inputs/results (excluding elapsed time), grid inputs/results, scene state, and operation counts. Baseline median refresh: 18,120.27 ms. Indexed candidate median: 1,885.27 ms. Measured reduction: 89.60%, or 9.61x speedup under this controlled workload. These figures are workload-specific, not a universal performance guarantee.
- A separate manual F6/F8 comparison once observed a 0.5-unit Y difference at connection 1, point index 3. It did not reproduce in the controlled deterministic runs, where geometry matched exactly. Its original cause remains unexplained; document it as an unresolved repeatability observation, not as a confirmed fix.

### Acceptance status and next actions
- The editor is **NOT ACCEPTED** yet. GUI acceptance is separate from automated tests and performance measurements.
- Still unresolved: wire visibility inside the shared cone. Still not tested in the post-index state: focus behavior after deletion, undo, and redo. Run hands-on GUI checks for these items and responsiveness; record actual observed results rather than assuming a pass.
- Immediate task: finish validating these two #4-owned handoff documents, then publish only those two documents in a dedicated documentation-only commit. Before staging, recheck branch/HEAD/tracking/live refs and an empty shared index. Stage explicit paths only, inspect the exact staged diff, run `git diff --cached --check`, and confirm no unrelated content is staged.
- Push only with normal, non-forced Git operations and only if the baseline and remote safety gates remain satisfied. Verify the resulting commit and live remote state after publication.
- After the documentation publication, continue the GUI acceptance checks. Any source/test publication requires a separate authorization decision.

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
