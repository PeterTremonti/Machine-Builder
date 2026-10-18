# Workstream Focus Index

Updated: 2026-10-18 01:06:25 -04:00

**Repository checkpoint:** branch `main`; local `HEAD`, `origin/main`, and live remote `main` matched at `3a1421af82b8d1dfa8e0c95f53f155135e0c4b3d` immediately before this update. Working-tree status observed at that moment: `clean`. This is a timestamped snapshot, not a live lock or a substitute for checking current Git state.

## Purpose and use

This is a curated navigation guide, not a duplicate history archive or a complete inventory of all files. Use it to find the current mission, read-first documents, focus files, relevant tests, and owner. The living handoff remains authoritative for detailed technical state and next action; `MASTER_PLAN.md` remains authoritative for long-term direction; `CHAT_WORKFLOW.md` governs conduct and publication.

A listed path is important to inspect, not automatic authorization to edit it. Git's current tree and `git ls-files` provide the complete tracked-file inventory. Add a new file here when it becomes materially important to a workstream, not every time any file is created.

## Publication queue protocol

Planning (#1) assigns one explicit active publication slot at a time. A message saying work has started is not the same as a READY-to-publish report. Ready owners must provide exact paths, a reconciled handoff, validation results, a proposed commit subject, and any ownership uncertainty. Planning announces queue position and slot status in its current coordination message.

Other owners may continue to edit, test, and update their handoffs while queued. They must not stage, commit, or push until their slot is granted. The slot holder verifies the actual index and live remote immediately before staging; a previously clean status report is not a lock. If any unrelated path is staged, stop and report it without unstaging or resetting it.

## #1 - Planning / Architecture

**Mission:** coordinate project priorities, maintain project-level documentation and the focus index, resolve scope/ownership questions, and serialize publication.

**Read first:** `CHAT_WORKFLOW.md`, `MASTER_PLAN.md`, `PROJECT_CURRENT_STATE.md`, `DOCUMENTATION_AUTHORITY.md`, this index, and `machine-structure-editor/handoffs/01_PLANNING_ARCHITECTURE_WORKSTREAM_HANDOFF.md`.

**Owned focus files:** the four root planning documents above, the Planning handoff, and `WORKSTREAM_FOCUS_INDEX.md`.

**Next:** reconcile material cross-workstream reports, update this index when focus/ownership/status materially changes, and explicitly tell the next READY owner its queue position and publication slot.

## #2 - Research / Architecture

**Mission:** source-backed architecture research, evidence provenance, uncertainty tracking, and research decisions. Do not imply source mapping establishes physical wiring.

**Read first:** `machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md` and `machine-builder-research/standards/STANDARDS_INDEX.md`.

**Focus files:** the Standards Index, Research handoff, and the specific source snapshots and research authorities named by that handoff.

**Known recent checkpoint:** Research reported publishing `0578c2d` (`Refresh Research handoff and reconcile bounded validation disposition`). Verify the present commit and the current handoff before treating this as the latest state. SolidCraft is an accepted optional future CAD candidate, not a V0.2 dependency. The broader catalog/loader proposal remains deferred without separate Planning authorization.

**Next:** follow the current Research handoff. If an assigned task is complete, continue the next already-authorized in-scope research item; ask Planning for a fresh priority only if no clear authorized action remains.

## #3 - Controller / Board

**Mission:** controller-board fixtures, source-backed pin/connector mapping, and the distinction between reference documents and the user's installed hardware.

**Read first:** `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`.

**Focus files:** `machine-structure-editor/src/machine_builder/controller_board_fixtures.py`, `machine-structure-editor/tests/test_skr_mini_e3_exp1.py`, the relevant Board fixture tests, and source documents named by the handoff.

**Known recent checkpoint:** Board reported publishing `8b9e90f` (`Add SKR Mini E3 EXP1 firmware-reference fixture`) with seven dedicated SKR EXP1 tests passing. The accepted result is bounded. The Octopus/TMC5160T contact-6 discrepancy and Promega installed-harness/configuration questions remain separate evidence tasks; do not infer physical orientation, continuity, or as-built wiring from a firmware fixture.

**Next:** follow the Board handoff's current owner action and preserve the boundary between source mapping and physical evidence.

## #4 - Routing / Diagnostics / Visual Integration

**Mission:** routing behavior, connection diagnostics, and the visual editor. The present user-directed focus is the visual builder.

**Read first:** `machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`, the visual section of `MASTER_PLAN.md`, and the tests below.

**Focus files:**
- `machine-structure-editor/src/machine_builder/canvas_ui.py` - Port detail dropdown and focus/detail selection.
- `machine-structure-editor/src/machine_builder/canvas_scene.py` - scene connection updates, endpoint anchors, and routing integration.
- `machine-structure-editor/src/machine_builder/graphics/node.py` - connector enclosure, labels, cone, and visual anchor.
- `machine-structure-editor/src/machine_builder/graphics/connection.py` - rendered connection geometry and endpoint routing behavior.
- `machine-structure-editor/tests/test_functional_interface_connection.py` - automated regression coverage for the implemented visual connection behavior.

**Current design direction:** The long-term goal is progressive inspection down to individual wires. The present experiment is a cone from a harness/connector group toward its ports and per-port selection via the Port detail dropdown. It is not yet a completed true zoom mode.

**User observations to preserve in #4's handoff:** labels may be more readable inside the part/connector enclosure next to their ports; the preferred relationship from the wire-approach side is `Part > Port > Wire > Cone > port list aligned to the controller edge > port labels`; Functional/Detailed alignment may be intentional but needs confirmation; the cone has been observed only under the J9 Contacts selection, where the wire and cone/box placement appeared wrong; zooming in and out did not visibly change that presentation. Treat these as user-reported observations and design preferences pending GUI verification, not as proof of current implementation behavior.

**Acceptance boundary:** Retain the accepted X Motor workflow and bounded SKR EXP1 result. They do not approve unrelated connector/contact mappings. Confirm exact current modified paths and actual test state from the live checkout; this index does not assume that all listed files are currently modified.

**Next:** #4 should update its own handoff in place with the latest design intent, current per-port/cone experiment, exact visual gaps, and next GUI/automated validation. Continue editing and testing while queued, but wait for an explicit publication slot before staging.

## #5 - Efficiency / Modularization / Audit

**Mission:** code-health, modularity, and scoped acceptance reviews.

**Read first:** `machine-structure-editor/handoffs/05_EFFICIENCY_MODULARIZATION_WORKSTREAM_HANDOFF.md`.

**Ownership boundary:** #5 may inspect and edit its own implementation/documentation and handoff, validate its own changes, and publish its own scoped work through the queue. It is read-only when auditing another workstream's changes and must not edit or publish on that owner's behalf.

**Next:** follow its current handoff. Every audit must distinguish supplied evidence from independently run checks; missing evidence is not a pass. When an audit is complete, record the disposition, evidence, unresolved criteria, and next owner in the existing handoff.

## New-chat recovery

At the beginning of a replacement chat, retrieve the latest committed versions of the workflow, plan, project state, this index, and the receiving workstream's handoff directly from the canonical remote when accessible. Then verify the local checkout once and inspect only the listed focus files and tests needed for the active action. Ask for targeted local output only when uncommitted work cannot otherwise be inspected.

Keep the handoff and this focus entry current at material checkpoints. Do not wait for a predictable length-limit warning; no exact early-warning threshold is guaranteed. When context replacement is needed, create a dated, copy-ready startup prompt from these records. Old prompt text need not be archived separately if meaningful history and decisions are preserved in the handoff.
