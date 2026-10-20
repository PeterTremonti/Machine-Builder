# Chat 01 — Planning / Architecture Workstream Handoff

## Purpose

This is the living continuity document for Planning / Architecture (#1).

Its purpose is to allow a replacement Planning chat to recover project-level architecture, planning decisions, documentation governance, cross-workstream coordination, and unresolved questions without depending on conversation history.

The repository and verified tests remain authoritative for actual implementation behavior.

---

# Recovery Instructions

Follow Section 17, Workstream Recovery, in `CHAT_WORKFLOW.md` for the universal replacement-chat procedure. Planning-specific startup requirements and the current Planning Next Action are recorded in `NEXT PLANNING CHAT — START HERE` below.

---

# Current Role

Planning / Architecture (#1) owns:

* long-term architecture;
* `MASTER_PLAN.md`;
* `PROJECT_CURRENT_STATE.md`;
* cross-workstream coordination;
* project-level documentation governance;
* durable architectural decisions;
* milestone boundaries;
* future ideas;
* deferred problems;
* deciding whether implementation/research discoveries justify architecture changes.

Planning should not silently rewrite another workstream's handoff or implementation.

The intended flow remains:

```text
Planning decision
        ↓
targeted instruction to owning workstream
        ↓
owning workstream implementation / research
        ↓
owning handoff checkpoint
        ↓
report back to Planning
        ↓
Planning reconciles project-level state
```

---

# Current Repository Model

## Repository strategy

```text
main-only
one shared working checkout
```

Workstream chat instances are organizational labels only.

They are not branches, architecture versions, or separate projects.

---

# Current Project Milestone

The active implementation milestone is:

```text
V0.2
```

V0.2 is the semantic/machine-structure expansion milestone.

The current research baseline is O0.1 / R0.1, with the Research documentation treating V0.2 as development over that established foundation.

---

# Current Architecture

The machine-model-first direction remains established.

```text
Physical Machine
        ↓
Canonical Machine Model
        ↓
Firmware Requirements / Mapping
        ↓
Target Firmware + Version
        ↓
Generated Configuration / Representation
```

The visual editor is a bidirectional authoring and inspection environment over the canonical model.

```text
Canonical Machine Model
        ↕
Semantic / Model Boundary
        ↕
Visual Machine Editor
```

Important distinctions remain:

```text
Hardware Definition
    ≠ installed hardware instance

Controller
    ≠ Controller Resource

Controller Resource
    ≠ physical interface

physical Connection
    ≠ Controller Resource Assignment

Function
    ≠ Capability

canonical semantic state
    ≠ visual/editor state
```

New canonical concepts should be introduced only when concrete evidence demonstrates that existing concepts cannot represent the requirement coherently.

---

# Current Board Position

Recent Maestro and Octopus work continues to demonstrate that the existing model can represent reusable hardware definitions, installed controller instances, controller-owned and component-owned SemanticPorts, connector grouping, physical interface metadata, controller-resource exposure, physical interface mating, and replaceable driver-module cases.

No new canonical Connector, MatingInterface, DriverSocket, DriverModule, Contact, or similar entity has been justified by the current evidence.

The Controller-to-Hardware-Definition relationship is resolved for the current model through the typed `hardware_definition_id` relationship, with validation and persistence tests. Do not reopen it without concrete contrary evidence.

**Current source-evidence status (2026-10-17)**

- **SKR Mini E3 V3.0 EXP1: ACCEPTABLE for the bounded implementation and test evidence.** Research disposition `MB-20261017-0009-01`; Routing handoff update `MB-20261017-0115-01`. This does not validate physical orientation, mating geometry, continuity, or installed wiring.
- **Promega public configuration:** snapshot `fa72508fd221f9238521f33b0bcdc43c0f5d8332`. `config.g` uses `M208 X0:360`; `config.g.bak` uses `M208 X0:380`. Their listed X/Y/Z `M92` values match. The backup's purpose remains uncertain.
- **Static includes:** six of seven `M98` calls resolve in that public snapshot. `sys/resurrect.g` references `resurrect-prologue.g`, absent from that snapshot. This does not prove that the file is absent from the installed printer or used at runtime.
- **Scan limitation:** the original scan script was not recovered. The targeted substitute examined 22 top-level configuration-file candidates; 99 reported line occurrences include four supplemental `M92` occurrences and are not 99 independent configuration statements.
- **Machine-specific evidence still missing:** installed SD-card files and physical P9/P11 harness identity plus variant-specific H2/H4/S8/S6 mapping. Board workstream #3 retains ownership of collecting this evidence when available.
- **Separate unresolved compatibility issue:** Octopus Driver 2 contact 6 `SLEEP` / `DRIVER2_SLP` versus TMC5160T Pro V1.0 J1 contact 6 `CLK`. Do not infer compatibility.

The historical public sources, firmware reports, installed SD-card files, and physical as-built wiring must remain distinct evidence sources.

---

# Current Routing Position

Routing remains a presentation and implementation layer over canonical connection semantics. Keep route topology separate from route geometry; the existing per-connection routing integration/stability layer is not an accidental duplicate pathfinder.

**Accepted bounded workflows**

- **X Motor functional-interface workflow: ACCEPTABLE** for the seven defined criteria at checkpoint `a84526b28237d1e678a044c534cc9e8ad6a80444`, per the #5 review. This is not blanket approval of Promega wiring or unrelated visual work.
- **SKR Mini E3 V3.0 EXP1: ACCEPTABLE** for the bounded fixture, source inventory, stable endpoint identities, uncertainty preservation, and save/reopen tests. Research reviewed the supplied evidence in `MB-20261017-0009-01`; #4's subsequent handoff update is `MB-20261017-0115-01`.

**Still open**

- Manual GUI acceptance for connector-cone rendering and the Function-to-Detailed presentation remains pending. Do not mark visual acceptance complete without the actual GUI evidence.
- General connector/contact validation remains separate from the accepted SKR slice. The Octopus `SLEEP` versus `CLK` discrepancy and integer-keyed persistence limitation are unresolved.
- No broader Promega wiring-readiness or production-standard approval is implied by either bounded acceptance.

Keep implementation, test evidence, and handoff claims aligned to the checkpoint actually tested. Preserve unrelated concurrent Routing and Board changes.

---

# Current Test State

Latest workstream-reported full-suite result: **853 passed in 36.85 seconds**, reported by #4 for a working tree based on checkpoint `a84526b28237d1e678a044c534cc9e8ad6a80444`.

The same reported validation included:

- Dedicated SKR EXP1 tests: **6 passed in 0.14 seconds**.
- Focused regression tests: **96 passed in 4.17 seconds**.
- `git diff --check`: passed for the reported target and full worktree.

These tests included the bounded SKR fixture/test changes and concurrent working-tree changes. They are not tests attributable to the base commit alone. Research reviewed the supplied SKR evidence but did not independently rerun the tests. #4 reported that its later handoff-only correction did not trigger another Python test run.

The latest Planning preflight found local branch `main`, `HEAD`, and fetched `origin/main` all at `a84526b28237d1e678a044c534cc9e8ad6a80444`. Live remote `main` was not checked in that preflight. Planning's documentation edit requires its own `git diff --check`; it does not by itself justify a code-test claim.

---

# Documentation Governance Decision

The project is moving to the principle:

> **One primary question → one authoritative document.**

The authority map is now intended to live in:

`DOCUMENTATION_AUTHORITY.md`

The document answers:

> Which document is authoritative for this question?

This is a governance/index document, not another architecture document.

The authority structure established by Planning is:

```text
README.md
    = What is Machine Builder?

MASTER_PLAN.md
    = Where is the project going?

PROJECT_CURRENT_STATE.md
    = What is true across the project right now?

CHAT_WORKFLOW.md
    = How are the workstreams operated?

DOCUMENTATION_AUTHORITY.md
    = Which document answers which project question?

Research START_HERE.md
    = Where does Research start?

ARCHITECTURE_OVERVIEW.md
    = What is the settled architecture?

ONTOLOGY_CURRENT.md
    = What is the current canonical ontology?

TERMINOLOGY_BASELINE.md
    = What do the important terms mean?

DECISION_LOG.md
    = What decisions have been accepted?

OPEN_QUESTIONS.md
    = What remains unresolved?

V0.2_RESEARCH_CHECKPOINT.md
    = What is the current research milestone/checkpoint?

workstream handoffs
    = What is happening in each implementation/research workstream?

HISTORICAL_DOCUMENT_ARCHIVE.md
    = What documentation was retired and why?
```

---

# Documentation Authority Decisions

## MASTER_PLAN.md

**Decision:** AUTHORITATIVE project plan.

It owns long-term direction, major architecture direction, future scope, deferred ideas, and durable planning principles.

It is not a detailed implementation schedule.

---

## ARCHITECTURE_OVERVIEW.md

**Decision:** AUTHORITATIVE current architecture baseline.

`DATA_FLOW.md`, `SYSTEM_BOUNDARIES.md`, and similar documents are supporting architecture references.

They must not silently become competing architecture authorities.

When accepted decisions change architecture, the architecture baseline should be reconciled.

---

## PROJECT_CONTEXT.md

**Decision:** CURRENT SUPPORTING / UNDER REVIEW.

It remains useful research/project context, but it is not authoritative for current architecture, ontology, or cross-project current state.

Its current contents should eventually be compared against Research's newer structure to determine what should be preserved, migrated, or retired.

---

## PROJECT_CURRENT_STATE.md

**Decision:** AUTHORITATIVE current cross-project snapshot.

It should not become a second implementation-history archive.

Detailed workstream history belongs in the appropriate handoff.

The current document is already approaching the useful size/review threshold and should be reduced deliberately only after its detailed material has been mapped.

---

## V0.2_IMPLEMENTATION_PLAN.md

**Decision:** WORKING / PROVISIONAL while V0.2 is active.

It remains the scoped implementation plan for V0.2.

It should eventually become a historical V0.2 milestone record after completion.

It is not project-wide architecture authority.

Do not rewrite it solely because its old status wording is stale. Compare its contents against the current architecture/current state first.

---

## IMPLEMENTATION_ROADMAP.md

**Decision:** AUTHORITATIVE.

Primary question:

> What is the overall implementation roadmap for the Machine Structure Editor?

The roadmap owns the high-level implementation path, implementation milestones, version strategy, and future implementation direction.

It is a scoped implementation authority, not the authority for overall Machine Builder direction, canonical ontology, or current project-wide state.

The version-specific implementation plan remains the detailed plan and implementation record for an individual active milestone.

---

## CODER_CHAT_WORKFLOW.md

**Decision:** not an active competing workflow authority.

Its unique useful material should be compared against `CHAT_WORKFLOW.md`.

Useful current rules may be migrated into the authoritative workflow document.

The old document should then become historical/superseded or be retired.

---

## Older visual-builder documents

**Decision:** preservation-first review.

Do not delete or rename them merely because their structure is old.

Map:

```text
current
historical
superseded
unique information
migration destination
retirement candidate
```

before any retirement.

---

# Historical Documentation Decision

A dedicated historical archive index should exist:

`HISTORICAL_DOCUMENT_ARCHIVE.md`

It should be an index/provenance record, not a full concatenation of every retired document.

Git already preserves exact historical file contents.

The archive should explain:

* what the document was;
* when it mattered;
* what replaced it;
* what useful information was preserved;
* why it was retired.

The archive should be created after the repository-wide historical inventory and content mapping are complete.

---

# Official Documentation Status Vocabulary

Use:

```text
AUTHORITATIVE
CURRENT SUPPORTING
WORKING / PROVISIONAL
HISTORICAL
SUPERSEDED
RETIRED / ARCHIVED
UNDER REVIEW
```

Do not use `OBSOLETE` as the final durable classification.

A file can be old without being obsolete.

---

# Workstream Status

## Research / Architecture (#2)

Research owns external evidence, standards, terminology, ontology, architecture investigation, provenance, and research conclusions.

**Current status (2026-10-17)**

- The Research handoff was reported reconciled in place; the Standards Index has a bounded mapping-layer clarification. Both paths are modified in the shared working tree and remain uncommitted.
- **SKR Mini E3 V3.0 EXP1: ACCEPTABLE** for the scoped implementation and test evidence. Research reviewed the reported six dedicated tests, 96 focused regression tests, 853 full-suite tests, and whitespace check; it did not independently rerun tests against the live checkout.
- The accepted scope keeps logical position-to-MCU mapping distinct from Marlin drawing labels, downstream conditional peripheral assignments, and unverified physical wiring.
- General connector/contact validation remains open. The Octopus `SLEEP`/`CLK` discrepancy, the group-level `mated_with` limitation, physical evidence gaps, Marlin provenance/role interpretation, and general integer-key persistence limitation remain unresolved.

**Next action and owner:** #5's proposed next action is to resume the separate, read-only review of the general connector/contact validation proposal, checking `MB-20261015-1154-01` against current source and baseline evidence. #1 coordinates any resulting scope/disposition decision; #2 reviews research-evidence assumptions for follow-on work. Do not reopen the accepted SKR slice without concrete contrary evidence or a defined new scope.

---

## Controller / Board (#3)

Controller/Board owns board and controller research, board fixtures, physical-interface identity, and the associated implementation/tests. Implementation changes remain on the shared `main` checkout and must not be mixed into Planning-only publication.

**Current status (2026-10-17)**

- The Board handoff records the Promega public-configuration research checkpoint `MB-20261017-0953-01`. #3 reported that the existing handoff was already reconciled at its last recorded verification; no new edit was needed at that checkpoint. The current worktree shows the Board handoff modified, but the prior verification was not freshly rerun after the latest message.
- Public-snapshot findings are historical evidence only: `config.g` uses `M208 X0:360`; `config.g.bak` uses `M208 X0:380`; six of seven static `M98` calls resolve, with `resurrect-prologue.g` absent from the collected snapshot. The original scan script was not recovered; a targeted scan covered 22 candidate files.
- **Still missing:** direct retrieval of the installed printer's SD-card files and confirmation of physical P9/P11 harness identity and variant-specific H2/H4/S8/S6 assignments.
- Keep the user's reported backup rationale tentative. Do not infer an installed configuration or wiring assignment from the public snapshot.

**Next action and owner:** #3 retains responsibility for the installed-SD and physical-harness evidence when those materials are available. No further Board handoff edit is requested unless a concrete inconsistency is found.

---

## Routing / Diagnostics (#4)

Routing owns routing/visual integration, diagnostic presentation, implementation evidence, and its own handoff.

**Current status (2026-10-17)**

- The Routing handoff was reconciled in place and now records Research's **ACCEPTABLE** disposition for the bounded SKR EXP1 implementation/test evidence.
- #4 reports six dedicated SKR tests, 96 focused regression tests, 853 full-suite tests, and successful `git diff --check` at the tested working-tree checkpoint based on `a84526b28237d1e678a044c534cc9e8ad6a80444`. Research reviewed that evidence and did not independently rerun the tests.
- The X Motor functional-interface acceptance remains scoped to its seven criteria at its accepted checkpoint. Neither that result nor SKR EXP1 acceptance constitutes complete Promega wiring readiness.
- Connector-cone rendering and Function-to-Detailed presentation remain pending manual GUI acceptance.
- The fixture/source/test and visual integration paths remain part of a shared working tree with uncommitted concurrent changes. Do not stage or publish them as part of a Planning-only documentation change.

**Next action and owner:** #4 owns follow-through on its remaining GUI evidence and any separately authorized Routing work. General connector/contact validation must stay separate from the accepted SKR EXP1 slice.

---

## Efficiency / Modularization (#5)

Workstream #5 is the read-only efficiency, modularization, code-health, and evidence-audit workstream. It reviews responsibilities, coupling, duplication, documentation, test organization, and acceptance evidence; under its current boundary it does not edit, stage, commit, push, or run tests.

**Current disposition**

- The X Motor functional-interface workflow is **ACCEPTABLE** for the seven stated criteria at checkpoint `a84526b28237d1e678a044c534cc9e8ad6a80444`. #4 reported the tests and publication evidence; #5 reviewed the supplied evidence but did not independently rerun tests or refresh the live remote.
- This does not approve the entire Promega wiring model, installed wiring, all visual integration, or general connector/contact validation.
- #5 supplied the proposed audit-handoff correction in `MB-20261016-1813-01`. It is a proposed correction for Planning to incorporate, not a report that #5 edited the repository.

**Next action and owner:** #5's next audit action is the separate, read-only general connector/contact proposal review described in `MB-20261016-1813-01`. It remains distinct from the accepted SKR EXP1 slice. #1 coordinates any resulting scope/disposition decision.

---

# What Has Already Been Completed

The project has recently established:

* `MASTER_PLAN.md`;
* `PROJECT_CURRENT_STATE.md`;
* `CHAT_WORKFLOW.md`;
* numbered Planning / Research / Board / Routing / Efficiency handoffs;
* main-only development;
* the current documentation ownership model;
* a generated repository tree;
* the initial Efficiency / Modularization audit;
* the first concrete code-health cleanup milestone.

Recent cleanup results:

```text
SelectionInspector duplicate definitions
    removed and validated

_unused _segment_clear()
    removed and validated

tracked generated egg-info
    removed from version control

Full suite
    756 passed
```

---

# Current Documentation Contradictions / Risks

The remaining documentation problem is not simply "old files."

The real risk is multiple documents expressing different answers to the same question.

Known examples include:

* old implementation roadmaps using historical planning gates;
* old V0.2 documents describing their original planning state;
* older chat workflow guidance that overlaps newer workflow rules;
* older visual-builder material whose current/historical status is unclear;
* `PROJECT_CURRENT_STATE.md` containing more detailed implementation history than its role ideally requires;
* Research onboarding/context documents whose useful content overlaps newer research authorities.

No bulk deletion should occur until these are mapped.

---

# Current Documentation Strategy

The desired structure is:

```text
CURRENT AUTHORITATIVE DOCUMENTS
        ↓
CURRENT SUPPORTING DOCUMENTS
        ↓
WORKING / PROVISIONAL DOCUMENTS
        ↓
HISTORICAL / SUPERSEDED DOCUMENTS
        ↓
RETIRED / ARCHIVED
```

The repository should become easier to recover from without losing the reasoning that produced the current architecture.

---

# Documentation Reorganization Checkpoint
Planning has now adjudicated the current documentation dispositions and completed the Research/Routing documentation delegations from the previous checkpoint.
* Research and Routing documentation reconciliation is complete.
* `CODER_CHAT_WORKFLOW.md` is superseded by `CHAT_WORKFLOW.md`.
* `IMPLEMENTATION_ROADMAP.md` remains the authoritative scoped implementation roadmap.
* `V0.2_IMPLEMENTATION_PLAN.md` is the active V0.2 working plan and will become the milestone record after completion.
* Older visual-builder documents are historical/reference material.
* `HISTORICAL_DOCUMENT_ARCHIVE.md` exists as the designated historical-disposition index; its population remains a Planning task after historical mapping is finalized.
* `PROJECT_CURRENT_STATE.md` remains authoritative; its future reduction is still an open Planning decision.
No further workstream documentation migration is delegated by this checkpoint.

---

# Important "Do Not Repeat" Items

Do not reopen merely because a new chat starts:

* the machine-model-first principle;
* physical machine vs firmware identity;
* canonical model vs visual state;
* Hardware Definition vs installed hardware;
* Controller vs Controller Resource;
* Function vs Capability;
* the basic Board semantic boundary;
* broad connector terminology research already completed;
* broad routing topology-vs-geometry research already completed.

Reopen these only when concrete implementation, research, testing, or real-machine evidence creates a new question.

---

# Open Planning Questions

### Documentation

* Major documentation questions now have an assigned primary authority.
* Historical/legacy document mapping remains to be finalized in HISTORICAL_DOCUMENT_ARCHIVE.md.
* How much detail should remain in `PROJECT_CURRENT_STATE.md`?
* Which historical documents should remain as individual files even after the archive index exists?

### Architecture

* Does current real-hardware work continue to fit the semantic model?
* Are any implementation structures beginning to become unwanted canonical architecture?
* Does the Board work eventually require richer reusable interface/compatibility concepts?
* Does Routing eventually need persisted topology/presentation semantics?
* When do broader Process / Operation / Task concepts become necessary?

---

# Latest Planning State

**Workstream:** Planning / Architecture

**Chat instance:** current Chat 01

**Date/time:** 2026-10-05 22:36 -04:00

**Repository branch:** `main`

**Exact current HEAD:** `46059b17516ee30c3557efeb92a50d1c91b333d8`

**Latest verified full test state:** `765 passed in 2.69s`

**Test-state qualification:** the 765-test result was verified against the current working tree. The working tree contains four uncommitted Board/Routing workstream changes, so the 765 result must not be attributed to committed HEAD `46059b1`.

**Uncommitted workstream files at this checkpoint:**

- `machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`
- `machine-structure-editor/src/machine_builder/controller_board_fixtures.py`
- `machine-structure-editor/src/machine_builder/hardware_catalog.py`
- `machine-structure-editor/tests/test_controller_board_fixtures.py`

**Primary current effort:** complete the Planning-owned documentation reconciliation while preserving clear authority, supporting, working, and historical roles.

---

# NEXT PLANNING CHAT — START HERE

Follow Section 17 in `CHAT_WORKFLOW.md` first. Then complete these Planning-specific steps:

1. Read `DOCUMENTATION_AUTHORITY.md`, which Planning uses for project-wide documentation authority and governance.
2. Verify the current `main`, exact `HEAD`, working-tree state, and relevant current test results before making implementation claims.
3. Treat completed Research, Board, and Routing reconciliation checkpoints as complete unless a new question or current evidence justifies reopening them.
4. Apply the shared-contract/separate-implementation-ownership rule. Coordinate and delegate changes outside Planning ownership to the owning workstream.
5. Continue current Planning questions from this handoff and repository state. Keep the handoff current as material decisions and Next Actions change.

The current Planning principle is:

> **One primary question → one authoritative document, with explicit ownership of implementation files and stable shared contracts between workstreams.**

# Recovery Principle

The Planning chat should not need the old conversation to understand the project's current documentation governance.

The intended system is:

```text
question
    ↓
DOCUMENTATION_AUTHORITY.md
    ↓
authoritative document
    ↓
supporting detail where necessary
    ↓
historical record when retired
```

A chat can end without the project's knowledge ending.

# Planning Decision - Cross-Workstream File Ownership

Status: DECIDED

Date: 2026-10-05

The project adopts shared contract, separate implementation ownership as the default cross-workstream pattern.

Workstream-specific implementation files have one owning workstream.

Shared implementation, infrastructure, and canonical-model files also have one explicit owner.

A file does not become jointly owned because multiple workstreams depend on it.

Workstreams should interact through established canonical model types, interfaces, identifiers, and other agreed contracts.

A workstream needing a change outside its ownership reports the requirement to Planning / Architecture.

Planning decides whether the change is warranted and delegates implementation to the owning workstream.

Changes affecting shared canonical contracts or semantic boundaries require Planning / Architecture review.

The owning workstream performs and tests the approved change.

Chat 05 remains read-only outside its own handoff.

---

# Board Physical Evidence Update - 2026-10-05

Chat 03 reported additional physical inspection evidence from the Duet 2 Maestro V1.0.

The evidence reinforces, rather than changes, the current architecture:

- physical controller interfaces are not synonymous with Controller Resources;
- the E2/E3 external driver headers are physical interfaces for additional driver modules while the logical resources remain separate controller resources;
- meaningful PCB connector labels and manufacturer documentation may identify physical interfaces even when individual contact numbers are not printed on the PCB;
- an unreadable/unidentified endstop connector must remain unidentified until documentation establishes its identity rather than being inferred;
- the possible `PanelDue_SD` label remains pending documentation verification;
- the heater multi-access-point interpretation should be treated as pending evidence until the documentation is verified.

Planning decision:

> **No new canonical interface entity is justified by this evidence.**

The Board work should continue testing the existing Controller, Controller Resource, SemanticPort, connector grouping, and related relationships against the documented physical inventory.

---

# Documentation Reference Reconciliation - 2026-10-05

Chat 05 identified a remaining documentation inconsistency:

`docs/historical/research/IMPLEMENTATION_HANDOFF_INDEX.md` (archived from `machine-builder-research/handoffs/IMPLEMENTATION_HANDOFF_INDEX.md`)

The Research-owned index previously presented the `docs/visual-builder/` files as the **Current Visual Builder Handoff Set**, while `HISTORICAL_DOCUMENT_ARCHIVE.md` classified those same files as HISTORICAL.

Planning delegated reconciliation of that Research-owned index to Research / Architecture (#2).

Research completed the reconciliation in commit `e2f12fd65a88a53f245717da3737d64c39a5f076` (**Reconcile historical Visual Builder handoff references**).

The index now identifies the five `docs/historical/visual-builder/` files as historical/reference material rather than the current authoritative Visual Builder implementation handoff set, and directs current project, architecture, implementation, and workstream questions to `DOCUMENTATION_AUTHORITY.md`.

No historical Visual Builder documents were modified or deleted, and no new architecture or ontology requirement was introduced.

Status: **Resolved**.

## Planning Closeout — Promega Integration and Documentation Recovery (2026-10-10)

### Accepted direction

Planning has adopted the Promega vertical slice as the immediate integration focus. The existing ontology remains adequate for the cases reviewed so far; implementation and evidence gaps should be addressed before considering new canonical entities.

The physical connection-authoring checkpoint is published as `c445bef287d736afd20807f29d2506aab2434eaa`. #5's final read-only review returned **ACCEPTABLE**. The reported full-suite result was 827 passed, and the reported focused suite was 46 passed. These results are attributed to #4; #5 did not rerun the tests.

### Workstream closeout

* **#2 Research:** Six Promega research deliverables accepted. Research handoff and V0.2 checkpoint updates applied locally and whitespace-checked. Their baseline and update timestamp are recorded in the snapshot above.
* **#3 Board:** J4 bed-heater evidence and correction plan recorded in the Board handoff. The manufacturer's up-to-18 A statement remains qualified by thermal testing; the complete J4 path's verified safe maximum remains unassigned. Implementation is not authorized.
* **#4 Routing:** Connection-authoring implementation committed and pushed; Checkpoint 23 appended to the Routing handoff. The exact handoff-edit timestamp was not recorded.
* **#5 Audit:** Final connection-authoring review accepted; handoff updated and whitespace-checked at `2026-10-10 00:43:56 -04:00`. Reported tests were not independently rerun by #5.

### Documentation commit scope

The specialist handoff/checkpoint updates and the Planning-owned documentation changes are to be committed separately from the published implementation commit. The intended documentation files are:

* `CHAT_WORKFLOW.md`
* `MASTER_PLAN.md`
* `PROJECT_CURRENT_STATE.md`
* `machine-structure-editor/handoffs/01_PLANNING_ARCHITECTURE_WORKSTREAM_HANDOFF.md`
* `machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md`
* `machine-builder-research/checkpoints/V0.2_RESEARCH_CHECKPOINT.md`
* `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`
* `machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md`
* `machine-structure-editor/handoffs/05_EFFICIENCY_MODULARIZATION_WORKSTREAM_HANDOFF.md`

Before committing, verify the actual branch, HEAD, working-tree status, intended file list, and combined diff. Run `git diff --check`. Do not stage or commit `.vscode/launch.json` or any unrelated source, test, or catalog change. The documentation-only commit does not require a full test-suite rerun; report the actual whitespace and diff verification.

### Current Planning Next Action

**Current checkpoint (2026-10-18):** Planning is introducing a curated Workstream Focus Index and a single-publication-slot protocol. `CHAT_WORKFLOW.md` owns the operating rules; `MASTER_PLAN.md` owns long-term feature direction; `PROJECT_CURRENT_STATE.md` is the project snapshot; each living handoff owns detailed implementation, evidence, and next actions.

**Queue coordination:** Workstreams may continue editing, validating, and refreshing their own handoffs while queued, but only the explicitly named slot holder may stage, commit, and push. Planning assigns queue positions based on readiness, dependencies, project priority, and age of the complete readiness report. The shared Git index and live remote must still be checked immediately before publication. #5 may edit and publish its own files; its read-only boundary applies when auditing other workstreams' changes.

**Current visual direction:** The user's current #4 task is to explore progressive visual detail, beginning with a harness/connector cone toward individual ports and a per-port Port detail dropdown selection. Individual-wire inspection is a longer-term goal; this is not yet a completed true zoom mode. Planning records the overarching intent, while #4 must preserve the detailed design preferences and GUI acceptance observations in its own handoff.

**Next action:** Finish validating and publishing this Planning-owned documentation package. Then use each workstream's readiness report to assign the next explicit publication slot. #4 may continue its visual implementation and update its handoff while queued; no other workstream should stage during the active Planning publication slot.

## Planning Coordination Update — 2026-10-10

### Latest shared workflow checkpoint

The latest reported shared-main publication is `783c3b56b9f549fbb443c3f7a9a905c413f6a36a` — `Standardize commit and handoff cadence`. The workstream report says `CHAT_WORKFLOW.md` was the only committed path, publication was verified, and the code suite was not rerun because this was a documentation-only change. The preflight for this documentation update verified local HEAD, fetched origin/main, and live remote main all at 783c3b56b9f549fbb443c3f7a9a905c413f6a36a before writing.

The common workflow now distinguishes:
- each workstream's handoff update after five successfully published commits attributable to that workstream, with earlier updates for milestones; and
- Planning's responsibility to refresh cross-workstream project records when a material change is established, regardless of the individual five-commit count.

### Current project-level decisions

- The Maestro J4 correction is already published as `e85a1e38af74622de3a1b62cf1641af4b707fd26`; the old planning statement that it was awaiting implementation authorization is superseded. The documented interface mapping does not establish a safe current limit for the full output circuit.
- The Promega specimen, assembly endpoint labels, and three IR-probe reference connections are incremental checkpoints. They do not establish complete physical wiring, active firmware configuration, or verified as-built machine identity.
- **SKR Mini E3 V3.0 EXP1 bounded implementation/test evidence: ACCEPTABLE** following Research review `MB-20261017-0009-01` and Routing's update `MB-20261017-0115-01`. This replaces NEEDS A BOUNDED REVISION only for that slice; it does not establish physical orientation, mating geometry, continuity, installed wiring, or general connector/contact validation.
- **General connector/contact validation remains open.** #5's next action is the separate read-only review of proposal `MB-20261015-1154-01` against current source and baseline evidence, per `MB-20261016-1813-01`. Planning coordinates any resulting scope/disposition decision.
- The source-supported SKR mapping for EXP1 position 8 is PD6. Keep logical position-to-MCU mapping distinct from Marlin diagram/comment labels and downstream conditional peripheral assignments. The Marlin role-label/configuration relationship, manufacturer-PDF visual confirmation, physical orientation, mating geometry, continuity, and as-built wiring remain unresolved.
- Octopus contact 6 remains `SLEEP` / `DRIVER2_SLP` against TMC5160T Pro V1.0 J1-6 `CLK`. Preserve the unresolved incompatibility and distinguish in-memory structure from successful save/reopen.
- Keep source evidence, firmware aliases, functional relationships, canonical physical connections, and user-specific as-built facts separate. No new ontology entity is warranted by the current evidence.

### Immediate Planning sequence

1. **Planning (#1):** Finish reviewing the current `PROJECT_CURRENT_STATE.md` and Planning handoff diffs. Check content accuracy, spacing/word integrity, and preservation of historical checkpoints. Run `git diff --check`; do not stage or publish until the full diffs are reviewed.

2. **Audit (#5):** Own the separate read-only review of connector/contact validation proposal `MB-20261015-1154-01` against current source and baseline evidence, as identified in `MB-20261016-1813-01`. Report ACCEPTABLE or BLOCKED with concrete evidence and remaining gaps. This review is separate from the accepted SKR EXP1 slice.

3. **Controller/Board (#3):** Retain responsibility for retrieving the installed Promega SD-card files and confirming physical P9/P11 harness identity and variant-specific H2/H4/S8/S6 mapping when the relevant materials are available. Public historical source alone does not close this evidence gap.

4. **Routing (#4):** Retain follow-through on manual GUI acceptance evidence for connector-cone rendering and Function-to-Detailed presentation. Do not claim visual acceptance complete until that evidence has been reviewed.

5. Before any later publication, refresh the actual worktree and remote state. Preserve all other workstream modifications and untracked files; stage only explicitly selected Planning-owned paths after full path and diff review.

### Scope and evidence status

This handoff records reports supplied through the October 10, 2026 workflow publication. It does not claim new test execution. The recent test counts remain checkpoint-specific, and this local update must not include the concurrent modified Board handoff or the untracked `.vscode/launch.json`.

## Planning Coordination Update - Autonomous Workstream Continuity and Future Intake (2026-10-11)

### Operating decisions

- `MASTER_PLAN.md` Section 13 is the single canonical register for future features, usability issues, and deferred opportunities.
- `CHAT_WORKFLOW.md` Sections 36-37 require autonomous continuation, durable workstream-owned findings, milestone-based reporting, and non-duplicative future-feature intake.
- Section 26 clarifies command-line Git as an authorized normal publication route for workstreams with standing publication authority. GitHub Desktop remains an alternative, not a requirement.
- Section 34 remains mandatory: cross-workstream messages begin inside their copy-ready block with `From #N -> To #M - Topic`.

### Durable findings captured

- The port-layout readability issue has been recorded in `MASTER_PLAN.md` Section 13 as a future GUI-inspection item. Its cause and solution remain unverified.
- #2's hardware-catalog schema proposal has been recorded in Section 13 and is deferred until after the Promega milestone.
- #3's old-versus-new Promega cable-assembly findings and evidence qualifications have been summarized in `PROJECT_CURRENT_STATE.md`. P4/P2, the new assembly's exact mapping, P9/P11 variation, and the active RRF 3.5.4 configuration remain unresolved.
- The last supplied local inspection showed in-progress #4 changes in `test_promega_ir_probe_connections.py` and untracked `promega_fixtures.py`, alongside the existing modified #3 handoff and untracked `.vscode/launch.json`. This Planning edit must not stage those files or claim their tests passed.

### Next action

Review the five Planning-owned document changes, run `git diff --check`, and inspect the complete diff. Stage only the five paths explicitly owned by this update. Do not stage Routing implementation, the Board handoff, or `.vscode/launch.json`. No code tests are claimed by this documentation update. Publish only after staged-path and staged-diff verification, then verify local HEAD, fetched `origin/main`, and live remote main.

## Planning Coordination Update - Promega Fixture Published (2026-10-11)

### Verified publication report

#4 supplied a publication sequence reporting:

- Commit: `9f3626b5b3117c2aef691eec4b04ae9b863485d0`
- Subject: `Add reusable Promega IR-probe reference wiring fixture`
- Full-suite result before publication: `838 passed in 8.07s`
- Published paths: `machine-structure-editor/src/machine_builder/promega_fixtures.py` and `machine-structure-editor/tests/test_promega_ir_probe_connections.py`
- Reported final verification: local HEAD, fetched `origin/main`, and live remote `main` matched the published commit.

This result is established from the user's supplied command output. Do not inflate it into a claim that the entire Promega connection graph or actual as-built wiring is complete.

### Project priority and next steps

The immediate priority remains the Promega source-supported wiring vertical slice. The newly published fixture is the current implementation checkpoint. #4 should continue by checking the precise covered behavior and advancing the next justified wiring milestone within its standing scope.

#3's ongoing Promega connector/harness research supports that work but need not block independent #4 progress while evidence questions remain open. #2's declarative catalog/schema proposal and the port-layout readability issue are preserved in `MASTER_PLAN.md` Section 13 and deferred according to current priority.

The previous immediate SKR connector/contact spike is no longer the active priority. No ontology expansion or broad catalog loader is authorized by these findings.

### Planning documentation publication

The outstanding Planning-owned documentation paths remain:

- `CHAT_WORKFLOW.md`
- `DOCUMENTATION_AUTHORITY.md`
- `MASTER_PLAN.md`
- `PROJECT_CURRENT_STATE.md`
- `machine-structure-editor/handoffs/01_PLANNING_ARCHITECTURE_WORKSTREAM_HANDOFF.md`

Review and publish only these paths after the state and remote checkpoint are reconfirmed. Keep the modified Board handoff and untracked `.vscode/launch.json` out of the Planning commit.

## Planning Replacement Checkpoint — 2026-10-12

**Historical checkpoint notice (2026-10-12):** This section preserves the recovery state and next-action list as recorded on that date; it is not the current status. Use the reconciled current summaries above, updated 2026-10-17, for current ownership, acceptance, blockers, and next actions. Recheck the live checkout before acting on any historical instructions below.

**Purpose:** Preserve Planning state during replacement of this chat after the user encountered a ChatGPT usage-limit pause.

### Verified repository checkpoint

- Local branch, local HEAD, fetched `origin/main`, and live remote `main` were verified at `bca612ed3ae6c1b3da8f09f9ec9a5c173ec8dd3a`.
- Checkpoint subject: `Clarify directed fluid-transfer contract`.
- The commit advances the Research documentation and handoff. Its exact contract content still needs to be considered alongside the actual reply from #2 before Planning decides whether the previous review blockers are resolved.
- The latest verification is supplied by the user's PowerShell output. A replacement chat must recheck repository state before taking further action.

### Working-tree state at this checkpoint

- `CHAT_WORKFLOW.md`: unstaged Planning change adding `### Rendered copy-block presentation` under Section 34. The user supplied successful subsection verification and `git diff --check` results. This change remains uncommitted and unpushed.
- `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`: unstaged Board changes.
- `machine-structure-editor/src/machine_builder/controller_board_fixtures.py`: unstaged Board changes.
- `machine-structure-editor/tests/test_controller_board_fixtures.py`: unstaged Board changes.
- No files were staged at the reported checkpoint.
- Preserve all these changes. Do not blanket-stage, discard, overwrite, or publish another workstream's changes.

### Incoming workstream reports

The user has sent instructions to workstream chats #2 through #5 and intends to provide their replies to the replacement Planning chat. These replies have not been included in this checkpoint.

Review each actual reply before deciding what to do. Distinguish verified repository evidence from claims supplied by a workstream. Do not infer that a commit subject alone proves the requested technical criteria are satisfied.

### Research / Architecture (#2)

The last Planning review requested clarification of the proposed `fluid_transfer` contract:

- Specify where medium-scoped `fluid_role` (inlet/outlet) is represented and how across-connection and within-component roles are validated.
- Distinguish synthetic acceptance-fixture assumptions from manufacturer-verified coolant topology.

A commit titled `Clarify directed fluid-transfer contract` is now present at the verified shared checkpoint. Inspect the committed change and the incoming #2 report before recording a final Planning disposition.

### Controller / Board (#3)

The Board handoff and controller-board fixture source/test currently have unstaged changes. Preserve them. Review the actual #3 report and its stated tests and boundary before deciding the next Planning action. Do not assume uncommitted fixture work is complete or accepted.

### Routing / Connections (#4)

Promega remains the known routing priority. Review the actual incoming #4 message and current evidence before assigning further work or claiming publication.

### Efficiency / Modularization / Audit (#5)

Preserve the read-only audit/acceptance boundary. Formal acceptance reviews must state `ACCEPTABLE` or `BLOCKED`, grounded in explicit criteria and evidence. Missing evidence is not a pass.

### Communication convention

- For cross-workstream prose, use one dedicated styled writing/draft block with a copy control when supported. The complete message, beginning `From #N -> To #M - Topic`, must be inside the block.
- Use a separate plain `powershell`-labeled code block for complete executable PowerShell, without fence metadata.
- Standardize the block type and copy boundary, not exact colors or fonts, which can vary by interface.
- The user has already sent the formatting instruction to the labeled chats; do not unnecessarily ask them to repeat it.

### Immediate next action

1. Re-establish the live repository state read-only.
2. Read current `CHAT_WORKFLOW.md`, `DOCUMENTATION_AUTHORITY.md`, `MASTER_PLAN.md`, `PROJECT_CURRENT_STATE.md`, and this Planning handoff before editing any project file.
3. Review the actual replies from #2, #3, #4, and #5 as supplied by the user.
4. Resolve concrete Planning decisions against current evidence. Provide an actionable, copy-ready command whenever the next step is clear.
5. Preserve all existing staged/unstaged work and workstream authority. Do not commit or push the formatting-rule change merely because this chat is being replaced.

### Platform warning

The user saw a pause message citing usage limits for chats that include files or images. The cause has not been established; do not attribute it to a particular file or action without evidence.

## Planning Review of Incoming Workstream Reports - 2026-10-12

**Evidence basis:** User-supplied #2, #3, #4, and #5 reports; supplied local diff and committed Research specification; bounded inspection of the cited public Duet 2 Maestro PCB source. No local tests were rerun as part of this Planning review.

### Research / Architecture (#2) - ACCEPTABLE, documentation-only

The directed fluid-transfer specification is accepted as a bounded proposed contract. Port roles scoped by medium, explicit directed relationships, and separate across-connection/within-component rules fit the existing model. The specification correctly identifies the current validation gap and labels the Cooling Unit/LCX path synthetic rather than manufacturer-verified or as-built. No implementation or ontology change is authorized.

### Controller / Board and Routing (#3 / #4) - architecture accepted; correction required before publication

The property-based PCB identity design is consistent with current SemanticPort and Provenance concepts. Preserve existing identity and compatibility fields and keep PCB pad identity separate from PCB-view, guide-view, and cable-cavity coordinates.

The current shared fixture diff still uses a mutable master URL and a revision string that says an immutable SHA is not pinned. The reported immutable snapshot `56958640c73c7febf3bce6e1eefbbdffd5a2db1b` is accessible and identifies the Duet 2 Maestro PCB V1.0 title block dated 2018-02-20. Spot checks support the J9 pad mapping and J36/J7 shared-Z net arrangement. This is a fixed repository snapshot, not a commit specifically changing the PCB layout.

Before publication, #3 and #4 must coordinate to pin the exact source URL/SHA in metadata, assert it in regression coverage, and accurately describe the tests as checks against the manually reviewed expected crosswalk. The full bounded crosswalk must be checked against the pinned source. The Board handoff must also state that connectors absent from this subset are outside its inventory, not thereby disconnected or known to have unknown PCB identity.

The reported 33 focused and 842 full-suite passes belong to #4's prior checkpoint and do not validate the pending source-pin correction. Rerun the focused and full suites and `git diff --check` after the correction. No new canonical fields, separate provenance system, guide-view positions, cavity mapping, or E0/E1 motor expansion is authorized.

### Efficiency / Audit (#5) - ACKNOWLEDGED

#5 adopted the rendered copy-block convention. No repository inspection or change was reported or required by that formatting-only acknowledgement.

### Project priority and next action

The Promega source-supported wiring vertical slice remains the active implementation priority. Continue the bounded Board identity correction above without displacing Promega work, expanding V0.2 ontology, or beginning the deferred catalog loader. Preserve all concurrent shared-checkout changes and keep implementation paths separate from Planning and Board handoffs.

## Planning Validation Checkpoint - PCB Identity and Promega Guide-View Validation (2026-10-12)

**Verification baseline:** The user's supplied output confirmed local `main`, `HEAD`, and `origin/main` at `83d30c8cd60f0335cdf7b89757fba506e3cc2a3e`. The implementation and test modifications below were uncommitted; results apply to that tested working tree, not to the HEAD commit alone.

### Controller / Board - bounded PCB identity correction

The current fixture implementation pins its source URL to repository commit `56958640c73c7febf3bce6e1eefbbdffd5a2db1b` and records the source file path separately from PCB title-block revision `V1.0` and date `2018-02-20`. PCB pad identity and exact source net spelling are stored in existing `SemanticPort.properties`, with source evidence recorded through the existing `Provenance` type.

The manually reviewed expected crosswalk covers J9/J8 motor connectors, J36/J7 shared-Z nets, J32/J33 endstops, J28 probe contacts, and J37 including pad 10's unassigned-in-reference-PCB state. Regression assertions protect the immutable URL/SHA and explicitly state that the test does not automatically parse the external PCB source. Connectors outside the reviewed subset remain outside this inventory; missing metadata does not establish disconnection or unknown PCB design state.

### Promega - source-qualified J28 guide positions

The bounded reference fixture now records J28 guide-view positions separately from PCB pad numbers. The Promega helper requires explicit source-qualified guide-view identity instead of deriving it from legacy `pin_id` or the port-ID suffix. This describes the cited manufacturer's reference guide, not the physical mating orientation, cable cavity positions, or actual wiring on the user's installed printer.

### Validation result

The user's supplied PowerShell output reports the following results using `machine-structure-editor\.venv\Scripts\python.exe`:

- Focused Board fixture and Promega IR-probe tests: **31 passed in 3.75 seconds**.
- Full repository suite: **842 passed in 8.05 seconds**.
- `git diff --check`: passed.

These results were obtained after the current PCB source-pinning and guide-position changes were present. They do not prove the installed printer's as-built wiring or a complete Promega connection graph.

### Disposition and next actions

The property-based PCB identity architecture remains ACCEPTABLE. The earlier mutable source-reference defect is corrected in the current working diff and has passing regression evidence. No new canonical entity or parallel provenance system is justified.

The two staged Research documents separately record Planning's coolant-contract acceptance and the DYZE cooling-loop follow-up. Their staged whitespace check passed. The Planning workflow/handoff changes, Board-owned source/test/handoff changes, and Promega source/test changes remain uncommitted. Keep ownership boundaries intact and do not combine unrelated paths into a cross-workstream commit.

The Promega source-supported wiring vertical slice remains the active project priority. These reference fixtures do not establish a complete or as-built machine model.

## Planning Coordination Checkpoint — Publication Throughput and Recovery Freshness (2026-10-20)

**Verified baseline at inspection:** `29c2e54412c6621b112ccfee710e79e6fba46c91` — `Record integer-key persistence investigation findings`; branch `main`, local `HEAD`, stored `origin/main`, and live remote `main` agreed at 2026-10-20 18:38:16 -04:00. The shared index was empty at inspection. This is a historical snapshot, not a lock. No application tests were run for this documentation-only checkpoint.

### Queue ownership and next actions

- **#2 Research:** The three-file integer-key checkpoint is published at `29c2e54412c6621b112ccfee710e79e6fba46c91`. Planning received closeout `MB-20261020-1149-01` (`PUBLISHED — SLOT RELEASED`). The source-level rejection of non-string dictionary keys is confirmed; that Research investigation did not demonstrate runtime save/reopen failure. Later Research handoff/prompt refreshes remain local-only.
- **#3 Controller/Board:** Published `9b3013d1cbecebbc32e6e17909a8ea09885a4833` for the Board handoff. Contact-6 remains **UNRESOLVED**. #3 isolated the receiving-interface test from the TMC5160T module definition and converted only Octopus contacts to 18 numeric-position records. The save/reopen regression and focused 65-test suite are reported passing, as is scoped whitespace validation. Board changes remain local-only pending review and their own future slot; the generic serializer and TMC5160T map remain unchanged.
- **#4 Routing/Visual:** Yielded `NOT READY — SLOT RELEASED`. It reported 73 focused tests passing and compilation/whitespace checks passing, while GUI acceptance remains open. Its implementation, tests, handoff, and recovery prompt are outside this Planning batch.
- **#5 Efficiency/Audit:** The read-only editor/store state, undo/redo, and persistence audit is accepted as backlog guidance only; no tests or GUI validation were run for that audit.
- **#1 Planning:** The five-path Planning batch is local and unpublished. Planning's current slot covers exactly these paths at the verified baseline. After scoped validation, publish this batch only; keep all other workstream paths separate.

### Operating rules recorded

`CHAT_WORKFLOW.md` now records the publish-and-yield throughput rule, explicit closeout outcomes, baseline-specific grants, and the requirement to keep canonical recovery prompts and detailed handoffs current at material checkpoints. A prompt in chat is not proof of a repository write. Local recovery-file changes do not independently authorize publication.

### Next action

Review the complete Planning-only diff; verify strict UTF-8 read-back and the Planning-scoped whitespace check. #2's explicit closeout has been received. After validation, request a fresh Planning publication slot against the actual current baseline. Preserve every other workstream's staged, unstaged, and untracked changes.
