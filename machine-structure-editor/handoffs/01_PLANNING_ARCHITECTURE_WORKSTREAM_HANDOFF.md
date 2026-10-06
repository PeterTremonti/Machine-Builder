# Chat 01 — Planning / Architecture Workstream Handoff

## Purpose

This is the living continuity document for Planning / Architecture (#1).

Its purpose is to allow a replacement Planning chat to recover project-level architecture, planning decisions, documentation governance, cross-workstream coordination, and unresolved questions without depending on conversation history.

The repository and verified tests remain authoritative for actual implementation behavior.

---

# Recovery Instructions

A replacement Planning chat should:

1. Read this handoff.
2. Read `DOCUMENTATION_AUTHORITY.md`.
3. Read `PROJECT_CURRENT_STATE.md`.
4. Read `MASTER_PLAN.md`.
5. Read `CHAT_WORKFLOW.md`.
6. Inspect current `main`, current files, and current tests when implementation facts matter.
7. Continue from `NEXT PLANNING CHAT — START HERE`.
8. Do not reconstruct settled architecture from old conversations unless current evidence requires reconsideration.

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

Recent Maestro and Octopus implementation work has demonstrated that the existing model can represent:

* reusable hardware definitions;
* installed controller instances;
* controller-owned physical SemanticPorts;
* component-owned physical SemanticPorts;
* connector grouping;
* physical interface metadata;
* controller-resource exposure through SemanticPorts;
* physical interface mating;
* replaceable driver-module cases.

No new canonical Connector, MatingInterface, DriverSocket, DriverModule, Contact, or similar entity has been justified by current evidence.

The major remaining Board architecture question is how an installed Controller should relate to its reusable Hardware Definition.

Board discoveries belong to Workstream 03 and should be reported to Planning when they have project-level implications.

---

# Current Routing Position

Routing is a presentation/implementation concern over canonical connection semantics.

The useful distinction remains:

```text
route topology
    ≠
route geometry
```

Current routing implementation distinguishes topology selection, geometry, stability, diagnostics, endpoint escape behavior, and related routing concerns.

The recent Workstream 04 audit determined that `graphics/connection.py` is not an accidental duplicate pathfinder; it remains the active per-connection routing integration/stability layer.

No broad routing modularization is currently justified merely by file size.

The current Routing next action remains the geometry-only repair experiment for the known spacing pathology.

---

# Current Test State

Latest verified full repository test result:

```text
756 passed
```

This was verified after:

* SelectionInspector duplicate-definition cleanup;
* removal of the obsolete `_segment_clear()` helper;
* removal of tracked generated `egg-info` files.

Exact current `main` HEAD should be re-verified locally when this handoff is reconciled before its next commit.

Do not substitute an older remembered commit for the current one.

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

Research owns:

* external evidence;
* standards;
* terminology;
* ontology;
* research architecture;
* source provenance;
* research questions;
* research conclusions.

Chat 02 has completed a repository-wide documentation audit for the documentation-authority effort.

Planning's decision was required before the Research workstream could reconcile its documentation hierarchy.

The next Research instruction should be to reconcile its actual documents against `DOCUMENTATION_AUTHORITY.md`, especially:

* `PROJECT_CONTEXT.md`
* `START_HERE.md`
* architecture documents
* ontology documents
* terminology baseline
* decision log
* open questions
* research checkpoint

Chat 02 should update its own handoff rather than Planning editing it.

---

## Controller / Board (#3)

Board implementation continues independently on shared `main`.

No documentation cleanup work is currently delegated to Chat 03.

Board discoveries with architectural implications should still be reported to Planning.

---

## Routing / Diagnostics (#4)

Chat 04 has already:

* removed the duplicate SelectionInspector definitions;
* removed the unused `_segment_clear()` helper;
* validated the full 756-test suite;
* completed the `connection.py` routing-responsibility investigation.

The routing architecture is currently considered healthy enough to leave alone.

Its next normal implementation task remains the geometry-only route-repair experiment.

No further documentation cleanup is delegated to Chat 04 at this time.

---

## Efficiency / Modularization (#5)

Chat 05 has completed the initial repository audit.

It identified:

* confirmed duplicate SelectionInspector methods;
* tracked generated `egg-info`;
* unused `_segment_clear()`;
* documentation candidates;
* modularity review targets;
* historical artifacts.

Those concrete cleanup items have now been addressed where appropriate.

Chat 05 should remain available for future code-health audits but should **not continue broad repository archaeology** unless a new question requires it.

The next historical-document inventory may be requested from Chat 05 after Planning establishes the authority model.

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

1. Read this handoff.
2. Read `DOCUMENTATION_AUTHORITY.md`.
3. Read `PROJECT_CURRENT_STATE.md`.
4. Read `MASTER_PLAN.md`.
5. Read `CHAT_WORKFLOW.md`.
6. Verify current `main`, exact HEAD, working-tree state, and latest tests.
7. Treat completed Research, Board, and Routing reconciliation checkpoints as completed; do not repeat them without a new question.
8. Treat shared-contract/separate-implementation-ownership as the default cross-workstream governance rule.
9. Obey the hard Machine Builder tooling, repository-editing, and copy/paste command-formatting constraints in `CHAT_WORKFLOW.md`.
10. Continue current Planning questions from the durable handoffs and repository state.
11. When a change is needed outside Planning ownership, delegate it to the owning workstream rather than modifying its implementation directly.
12. Keep this handoff current as the Planning continuity record.

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

`machine-builder-research/handoffs/IMPLEMENTATION_HANDOFF_INDEX.md`

The Research-owned index previously presented the `docs/visual-builder/` files as the **Current Visual Builder Handoff Set**, while `HISTORICAL_DOCUMENT_ARCHIVE.md` classified those same files as HISTORICAL.

Planning delegated reconciliation of that Research-owned index to Research / Architecture (#2).

Research completed the reconciliation in commit `e2f12fd65a88a53f245717da3737d64c39a5f076` (**Reconcile historical Visual Builder handoff references**).

The index now identifies the five `docs/visual-builder/` files as historical/reference material rather than the current authoritative Visual Builder implementation handoff set, and directs current project, architecture, implementation, and workstream questions to `DOCUMENTATION_AUTHORITY.md`.

No historical Visual Builder documents were modified or deleted, and no new architecture or ontology requirement was introduced.

Status: **Resolved**.
