# Machine Builder - Historical Document Archive

## Purpose

This document is the authoritative index of retired, superseded, and intentionally historical documentation.

It records the historical role of a document, its current authority or replacement, useful information preserved elsewhere, and why the document is no longer a current authority.

Git preserves the exact historical contents of the files themselves.

---

# 1. Superseded workflow documentation

## `docs/historical/workflow/CODER_CHAT_WORKFLOW.md`

**Classification:** SUPERSEDED

**Current authority:** `CHAT_WORKFLOW.md`

**Historical value:** Preserves the earlier coder-chat workflow, implementation coordination rules, routing-specific guidance, and recovery practices.

Its reusable workflow concepts are now represented by the project-wide `CHAT_WORKFLOW.md`. Its older implementation handoff references and routing-specific details are historical.

---

# 2. Historical V0.1 Visual Builder documentation

These documents describe the original V0.1 Visual Builder prototype and are retained as historical/reference material.

## `docs/historical/visual-builder/VISUAL_BUILDER_ARCHITECTURE.md`

**Classification:** HISTORICAL

**Current authority:** `machine-builder-research/architecture/ARCHITECTURE_OVERVIEW.md` for settled architecture, with current milestone implementation documents for implementation-specific decisions.

**Historical value:** Records the original Visual Builder architectural framing used during V0.1.

## `docs/historical/visual-builder/VISUAL_BUILDER_CODER_HANDOFF.md`

**Classification:** HISTORICAL

**Current authority:** `CHAT_WORKFLOW.md` for project-wide workflow and the applicable current workstream handoff for implementation continuity.

**Historical value:** Records the original V0.1 implementation handoff and coder-oriented execution context.

## `docs/historical/visual-builder/VISUAL_BUILDER_REQUIREMENTS.md`

**Classification:** HISTORICAL

**Current authority:** MASTER_PLAN.md for project direction and the active milestone implementation plan for milestone-specific scope.

**Historical value:** Records the original V0.1 Visual Builder requirements and prototype objectives.

## `docs/historical/visual-builder/VISUAL_BUILDER_SCOPE.md`

**Classification:** HISTORICAL

**Current authority:** `MASTER_PLAN.md` and the active milestone implementation plan.

**Historical value:** Records the original V0.1 prototype scope and its boundaries.

## `docs/historical/visual-builder/VISUAL_MODEL.md`

**Classification:** HISTORICAL

**Current authority:** Current architecture documentation for the canonical/visual model boundary, with current implementation code providing the implementation.

**Historical value:** Records the original V0.1 visual-model concepts and terminology.

---

# 3. Historical Routing handoff

## Original path

`machine-structure-editor/handoffs/V0.2_VISUAL_EDITOR_IMPLEMENTATION_HANDOFF.md`

## Current path

`docs/historical/routing/ROUTING_DIAGNOSTICS_HISTORICAL_HANDOFF.md`

**Classification:** HISTORICAL

**Current authority:** `machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`

**Historical value:** Preserves Routing Diagnostics material that was originally stored under the misleading Visual Editor filename.

---

# 4. Historical Routing investigation handoffs

## `docs/historical/routing/ROUTING_STABILITY_INVESTIGATION_HANDOFF_4.3.md`

**Classification:** HISTORICAL

**Current authority:** `machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`

**Historical value:** Preserves the 4.3 routing investigation checkpoint and its historical reasoning.

## `docs/historical/routing/ROUTING_STABILITY_INVESTIGATION_HANDOFF_4.4.md`

**Classification:** HISTORICAL

**Current authority:** `machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`

**Historical value:** Preserves the 4.4 routing investigation checkpoint and its historical reasoning.

---

# 5. Archive rules

A historical document should remain preserved when it provides:

* provenance;
* architectural history;
* implementation history;
* research history;
* reasoning that explains how the current design developed;
* unique information not preserved elsewhere.

No historical document should be deleted merely because it is no longer current.

Before future retirement or deletion:

1. review its contents;
2. identify unique information;
3. migrate useful current information where appropriate;
4. record its historical disposition here.

This archive is an index/provenance record, not a replacement copy of the historical documents.

Git remains the source for the exact historical file contents.

# 6. Chat 1 recovery and reconstruction record

## `MACHINE_BUILDER_CHAT_1_RECOVERY_AND_RECONSTRUCTION_2026-10-04.md`

**Classification:** HISTORICAL

**Current authority:** `CHAT_WORKFLOW.md`, `MASTER_PLAN.md`, `PROJECT_CURRENT_STATE.md`, and the current Research authority documents listed in `DOCUMENTATION_AUTHORITY.md`.

**Historical value:** Preserves the October 4, 2026 recovery/reconstruction record created after the original Chat 1 transcript was no longer available. It records recovery confidence levels, surviving architectural substance, terminology evolution, major semantic distinctions, and the boundary between verified surviving evidence and uncertain or lost conversation material.

**Disposition:** Retain as historical provenance. It is not a current architectural authority and should not be used in preference to the current authority documents when they provide the same information.
