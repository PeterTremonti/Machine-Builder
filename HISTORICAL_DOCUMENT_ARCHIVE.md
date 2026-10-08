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

# 7. Historical Research implementation handoffs

The following files were formerly stored under `machine-builder-research/handoffs/`. They are preserved as historical/version-transition records and are no longer part of the active Research recovery or workstream coordination path.

## `docs/historical/research/IMPLEMENTATION_HANDOFF_INDEX.md`

**Original path:** `machine-builder-research/handoffs/IMPLEMENTATION_HANDOFF_INDEX.md`

**Classification:** HISTORICAL / SUPERSEDED

**Current authority:** `DOCUMENTATION_AUTHORITY.md` and the applicable current numbered workstream handoff.

**Historical value:** Preserves the earlier H-001 through H-017 implementation-handoff system and the research-to-implementation concerns tracked by that system.

## `docs/historical/research/O0.1_IMPLEMENTATION_HANDOFF.md`

**Original path:** `machine-builder-research/handoffs/O0.1_IMPLEMENTATION_HANDOFF.md`

**Classification:** HISTORICAL

**Current authority:** Current Research architecture, ontology, checkpoint, and implementation/workstream documents.

**Historical value:** Preserves the O0.1-phase interpretation of the canonical model and its early implementation expectations.

## `docs/historical/research/V0.2_IMPLEMENTATION_HANDOFF.md`

**Original path:** `machine-builder-research/handoffs/V0.2_IMPLEMENTATION_HANDOFF.md`

**Classification:** HISTORICAL / SUPERSEDED

**Current authority:** Current implementation code, milestone documents, and numbered workstream handoffs.

**Historical value:** Preserves the early V0.2 implementation checkpoint, assumptions, and implementation-state history.

## `docs/historical/research/R0.1_TO_V0.2_HANDOFF.md`

**Original path:** `machine-builder-research/handoffs/version-handoffs/R0.1_TO_V0.2_HANDOFF.md`

**Classification:** HISTORICAL

**Current authority:** Current Research and implementation/workstream authorities.

**Historical value:** Preserves the R0.1/O0.1 to V0.2 transition reasoning and the historical Research-to-implementation boundary.

# 8. Historical Visual Builder continuation artifact

## `docs/historical/visual-builder/Read me to continue 4.1 chat.txt`

**Original path:** `machine-structure-editor/Read me to continue 4.1 chat.txt`

**Classification:** HISTORICAL / STALE BOOTSTRAP

**Current authority:** `CHAT_WORKFLOW.md` and the current implementation workstream handoff.

**Historical value:** Preserves an earlier Visual Editor chat-continuation/bootstrap record, including old implementation state, commands, debugging context, and historical reasoning.

**Disposition:** Retain for provenance. It is not current implementation onboarding and should not be used to recover current project state.

# 9. Historical wiring artifact

## `docs/historical/wiring/Wiring_Map.ods`

**Original path:** `docs/Wiring_Map.ods`

**Classification:** HISTORICAL

**Current authority:** Current machine/controller/routing evidence and current canonical semantic documentation.

**Historical value:** Preserves a V7-era wiring map and connector mapping. The artifact contains incomplete and explicitly uncertain electrical details and is not authoritative current engineering data.

**Disposition:** Retain as historical wiring evidence. Do not promote its legacy pin or electrical claims into current semantic authority without independent verification.

# 10. Historical V7-era documentation

The following documents were part of the older V7/V7.x documentation system. They are preserved together under `docs/historical/legacy/` because their architecture, UI, and bootstrap conventions have been superseded by the current project authority model.

| Historical file | Classification | Historical value |
| --- | --- | --- |
| `docs/historical/legacy/MachineBuilder_Chat_Bootstrap.md` | HISTORICAL / STALE BOOTSTRAP | Preserves the old chat bootstrap and V7.9-era recovery guidance. |
| `docs/historical/legacy/MachineBuilder_Master_Brain.md` | HISTORICAL / SUPERSEDED | Preserves the earlier overall Machine Builder concept and architecture framing. |
| `docs/historical/legacy/MachineBuilder_Project_History.md` | HISTORICAL | Preserves the V7-era project/version history. |
| `docs/historical/legacy/Machine_Builder_Dev_Architecture.md` | HISTORICAL | Preserves the former V7.x implementation architecture and version plan. |
| `docs/historical/legacy/Version 7.8 Specs.md` | HISTORICAL | Preserves the V7.8 visual-builder specification. |
| `docs/historical/legacy/architecture/device_visual_schema.md` | HISTORICAL | Preserves the former hardware-database-driven device visual schema. |
| `docs/historical/legacy/architecture/firmware_generation.md` | HISTORICAL | Preserves the former firmware-generation architecture. |
| `docs/historical/legacy/architecture/hardware_database_schema.md` | HISTORICAL | Preserves the former hardware-database schema and terminology. |
| `docs/historical/legacy/architecture/machine_model.md` | HISTORICAL / SUPERSEDED | Preserves the former device/port-oriented machine-model architecture. |
| `docs/historical/legacy/architecture/wiring_system.md` | HISTORICAL / SUPERSEDED | Preserves the former device/port/connector/wire/cable/harness model. |
| `docs/historical/legacy/ui/builder_modes.md` | HISTORICAL | Preserves the former V7 UI builder-mode design. |
| `docs/historical/legacy/ui/canvas_system.md` | HISTORICAL | Preserves the former V7 canvas and zoom design. |

**Current authority:** `DOCUMENTATION_AUTHORITY.md` and the current project, Research, and implementation authorities it identifies.

**Disposition:** Retain as historical/reference material. These files must not be treated as current architecture, UI, workflow, or project-state authority.

# 11. Historical Controller / Board workstream handoff

## `docs/historical/implementation/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF_2026-10-07.md`

**Original path:** `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`

**Superseded on:** 2026-10-07

**Classification:** HISTORICAL / SUPERSEDED LIVE HANDOFF

**Current authority:** `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`

**Historical value:** Preserves the previous Controller / Board workstream continuity record, including its detailed checkpoint history, implementation evidence, architectural context, and prior-state reasoning that preceded the current handoff rollover.

**Disposition:** Retain as historical/versioned workstream provenance. It is no longer the live Board recovery document and must not compete with the current Board handoff.
