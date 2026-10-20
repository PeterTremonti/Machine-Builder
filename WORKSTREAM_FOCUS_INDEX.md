# Workstream Focus Index

Updated: 2026-10-20 18:38:16 -04:00

**Repository checkpoint:** branch `main`; local `HEAD`, `origin/main`, and live remote `main` matched at 2026-10-20 18:38:16 -04:00. The current worktree status contains 29 changed/untracked paths, and the shared index is empty. This is an observation, not a live lock.

## Purpose and use

This is a curated navigation guide, not a duplicate history archive or a complete inventory of all files. Use it to find the current mission, read-first documents, focus files, relevant tests, and owner. The living handoff remains authoritative for detailed technical state and next action; `MASTER_PLAN.md` remains authoritative for long-term direction; `CHAT_WORKFLOW.md` governs conduct and publication.

A listed path is important to inspect, not automatic authorization to edit it. Git's current tree and `git ls-files` provide the complete tracked-file inventory. Add a new file here when it becomes materially important to a workstream, not every time any file is created.

## Publication queue protocol

Planning (#1) grants exactly one active publication slot at a time. A grant names the permitted paths and commit subject and is tied to its stated baseline. The slot holder verifies branch, `HEAD`, fetched `origin/main`, live remote `main`, shared index, and the complete intended diff immediately before staging.

Publish the smallest complete, coherent, validated batch that fits the exact grant. Do not hold a slot while unrelated work remains unfinished, and do not split mutually dependent files or publish an incomplete unit merely to increase throughput. Continue permitted work while queued.

Immediately after publishing or deciding not to publish, send Planning a distinct closeout: `PUBLISHED — SLOT RELEASED`, `BLOCKED — SLOT RELEASED`, or `NOT READY — SLOT RELEASED`. Include commit, paths, validation and remote verification when published; otherwise state the exact blocker, staged/index state, remaining work, and next action. Planning advances the queue from explicit closeout and readiness evidence, not inference.

If the remote baseline advances after a grant, stop before staging and obtain explicit renewal against the new baseline. Never revert an intentional intervening commit to restore an old baseline. Preserve all owners' staged, unstaged, and untracked work; never use broad staging or force-push.

## #1 - Planning / Architecture

**Mission:** Coordinate project priorities, scope, cross-workstream dependencies, project-level documentation, and serialized publication.

**Read first:** `CHAT_WORKFLOW.md`, `MASTER_PLAN.md`, `PROJECT_CURRENT_STATE.md`, `DOCUMENTATION_AUTHORITY.md`, `WORKSTREAM_FOCUS_INDEX.md`, the Planning handoff, and the canonical Planning replacement prompt.

**Owned files:** the four root Planning documents, `WORKSTREAM_FOCUS_INDEX.md`, `machine-structure-editor/handoffs/01_PLANNING_ARCHITECTURE_WORKSTREAM_HANDOFF.md`, and `machine-structure-editor/handoffs/01_PLANNING_ARCHITECTURE_REPLACEMENT_PROMPT.md`.

**Current published baseline:** `29c2e54412c6621b112ccfee710e79e6fba46c91` — `Record integer-key persistence investigation findings`, verified on local `HEAD`, stored `origin/main`, and live remote `main` during this inspection.

**Queue:** #2's three-file Research checkpoint is published at the current baseline. Planning received its explicit closeout `MB-20261020-1149-01` (`PUBLISHED — SLOT RELEASED`). Planning's current slot covers these five documentation paths at the verified baseline; finish review and scoped validation, then publish only this batch.

**Next:** Finish review and validation of the local Planning batch. Publish only under the current five-path grant. If the baseline advances before publication, stop and request renewal.

## #2 - Research / Architecture

**Mission:** Source-backed architecture research, evidence provenance, uncertainty tracking, and research decisions. Source mappings do not establish the user's physical wiring.

**Read first:** `machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md` and `machine-builder-research/standards/STANDARDS_INDEX.md`.

**Latest published checkpoint:** `29c2e54412c6621b112ccfee710e79e6fba46c91` — `Record integer-key persistence investigation findings`. The inspected commit contains the Standards Index, Research handoff, and Research replacement prompt.

**Findings:** DYZE's historical bend-radius contradiction and removed prototype auto-pause claim are **ANSWERED**. The serializer's non-string dictionary-key rejection is source-confirmed; an Octopus save/reopen runtime failure was not reproduced, and the investigation reported no tests run.

**Queue:** The Research checkpoint is published, and Planning received closeout `MB-20261020-1149-01` (`PUBLISHED — SLOT RELEASED`). The later Research handoff and replacement-prompt refreshes remain local-only. Verify current refs and the shared index before assigning new work.

**Next:** Continue the current Research handoff's authorized next action; do not duplicate #3's contact-6 hardware-path investigation.

## #3 - Controller / Board

**Mission:** Controller-board fixtures, revision-qualified pin/connector evidence, and the distinction between reference documentation and installed hardware.

**Read first:** `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`.

**Focus files:** `machine-structure-editor/src/machine_builder/controller_board_fixtures.py`, `machine-structure-editor/tests/test_skr_mini_e3_exp1.py`, other relevant Board fixture tests, and source documents named in the handoff.

**Latest published checkpoint:** `9b3013d1cbecebbc32e6e17909a8ea09885a4833` — `Document revision-pinned TMC5160T routing evidence`, scoped to the Board handoff.

**Current investigation:** Octopus V1.1 Driver 2 contact 6 `SLEEP`/`DRIVER2_SLP` versus TMC5160T Pro V1.0 J1-6 `CLK` remains **UNRESOLVED**. Socket routing, physical mating/orientation, jumper state, and module J1-6-to-IC CLK routing remain unproven. The conditional SDO/CLK jumper hypothesis and user reports are not confirmed fault evidence.

**Separate accepted scope:** The SKR Mini E3 V3.0 EXP1 firmware-reference fixture remains a bounded accepted result. It does not resolve the Octopus/TMC5160T contact-6 discrepancy or establish installed hardware wiring.

**Current local state:** #3 isolated and fixed the Octopus receiving-interface save/reopen regression using 18 contact records with numeric positions, labels, and classifications. The reported focused suite passed 65 tests and scoped whitespace validation passed. Board source, test, handoff, and replacement-prompt changes remain local-only pending review and a separate publication slot. Contact-6 remains **UNRESOLVED**; the generic serializer and TMC5160T map were not changed.

**Next:** The Octopus receiving-interface persistence regression is implemented and focused-tested locally; retain Board source, test, and handoff changes as local-only until #3 receives a separate publication slot. Continue contact-6 research only within its existing bounded authorization. The electrical question remains **UNRESOLVED**.

## #4 - Routing / Diagnostics / Visual Integration

**Mission:** Routing behavior, connection diagnostics, and the visual editor. The current user-directed focus is progressive visual detail.

**Read first:** `machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`, the visual section of `MASTER_PLAN.md`, and current routing/functional-interface tests.

**Focus files:**
- `machine-structure-editor/src/machine_builder/canvas_ui.py` — Port detail dropdown and focus/detail selection.
- `machine-structure-editor/src/machine_builder/canvas_scene.py` — scene connection updates, endpoint anchors, and routing integration.
- `machine-structure-editor/src/machine_builder/graphics/node.py` — connector enclosure, labels, cone, and visual anchor.
- `machine-structure-editor/src/machine_builder/graphics/connection.py` — rendered connection geometry and endpoint routing.
- `machine-structure-editor/tests/test_functional_interface_connection.py` — visual-connection regression coverage.

**Current design:** The long-term goal is progressive inspection down to individual wires. The current experiment is a cone from a harness/connector group toward individual ports with per-port selection, not a completed true zoom mode. Preserve the user's approach-side sequence: `Part > Port > Wire > Cone > port list aligned to the controller edge > port labels`. Treat layout observations as user reports until GUI verification.

**User observations to preserve:** Labels may be more readable inside the part/connector enclosure beside their ports. Functional/Detailed alignment may be intentional but needs confirmation. The cone was reported only under the J9Contacts selection, where wire, cone, and box placement appeared wrong; zooming in and out did not visibly change that presentation. These remain user reports pending GUI verification.

**Latest reported validation:** The focused functional-interface, routing, wire-color, and stepper-terminal suite passed 73 tests; source compilation and `git diff --check` passed after EOF cleanup. Planning has not independently rerun these checks.

**Open GUI acceptance:** Contact-fan-out readability, connector-box placement, overlapping-wire selection, and focus behavior across deletion, undo/redo, and reopening remain outstanding. #4 reported that a guarded marker-based update stopped without writing; the current handoff and recovery prompt must be checked directly.

**Next:** Inspect the exact existing handoff and recovery-prompt structure, update both in place and validate, then continue GUI acceptance. #4 released its publication slot as NOT READY.

## #5 - Efficiency / Modularization / Audit

**Mission:** Code-health, modularity, and evidence-based scoped acceptance reviews.

**Read first:** `machine-structure-editor/handoffs/05_EFFICIENCY_MODULARIZATION_WORKSTREAM_HANDOFF.md` and `machine-structure-editor/handoffs/05_EFFICIENCY_MODULARIZATION_REPLACEMENT_PROMPT.md`.

**Ownership boundary:** #5 may inspect and change its own files. Audits of other owners' implementation remain read-only.

**Accepted checkpoint:** The editor/store mutation, undo/redo, and persistence audit found substantial source/test support for reviewed normal paths and demonstrated no blocking defect. #5 ran no tests or GUI validation for that audit.

**Backlog candidates, not implementation authorization:** persistence failure-injection tests; listener-exception semantics; deciding whether live mutable model access is intentional; and app-level canonical-model undo/redo assertions.

**Current local state:** The #5 handoff is modified and its recovery prompt is untracked. Keep both unpublished until #5 receives a slot.

**Next:** Follow the existing handoff and standing audit mission. No implementation of the accepted audit candidates has been authorized.

## New-chat recovery

Use each workstream's canonical local recovery prompt `machine-structure-editor/handoffs/NN_WORKSTREAM_REPLACEMENT_PROMPT.md` when a chat actually needs replacing. Planning's canonical file is `machine-structure-editor/handoffs/01_PLANNING_ARCHITECTURE_REPLACEMENT_PROMPT.md`.

Keep each handoff and replacement prompt current at material checkpoints. The handoff preserves detailed evidence and history; the prompt is the concise, self-contained recovery snapshot. Verify the actual file read-back: a prompt pasted in chat does not prove the repository file was saved.

For a replacement chat, read the latest accessible committed workflow, plan, current state, documentation authority, focus index, and the receiving workstream's handoff/prompt. Then inspect the actual local checkout, relevant changes, current refs, and shared index. Reconcile movement since the prompt snapshot before acting. Do not create a new prompt file for each checkpoint or replace an active chat merely because its recovery file changed.
