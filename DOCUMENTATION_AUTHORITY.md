# Machine Builder — Documentation Authority

## Purpose

This document answers one project-wide question:

> **Which document is authoritative for a particular question?**

The governing principle is:

> **One primary question → one authoritative document.**

Supporting documents may provide detail, evidence, history, or implementation continuity, but they must not silently become competing authorities.

Chats are not documentation authorities.

Chats investigate, research, implement, coordinate, and discover. Durable project knowledge belongs in repository documentation owned by the appropriate workstream.

---

# 1. Authority Scope

This document governs the **documentation map**.

It does not override:

* the current repository implementation;
* current tests;
* external technical evidence;
* source-of-truth hardware documentation;
* or the ownership of a workstream's implementation.

For actual implementation facts, the current repository and verified tests remain authoritative.

For project knowledge questions, use the authority map below.

---

# 2. Primary Authority Map

| Primary question                                                     | Authoritative document                                             |
| -------------------------------------------------------------------- | ------------------------------------------------------------------ |
| What is Machine Builder?                                             | `README.md`                                                        |
| Where is the project going?                                          | `MASTER_PLAN.md`                                                   |
| What is true across the project right now?                           | `PROJECT_CURRENT_STATE.md`                                         |
| How do the project chats/workstreams operate?                        | `CHAT_WORKFLOW.md`                                                 |
| Which document answers a project documentation question?             | `DOCUMENTATION_AUTHORITY.md`                                       |
| Where does Research start?                                           | `machine-builder-research/START_HERE.md`                           |
| What is the settled architecture?                                    | `machine-builder-research/architecture/ARCHITECTURE_OVERVIEW.md`   |
| What is the current canonical ontology?                              | `machine-builder-research/ontology/ONTOLOGY_CURRENT.md`            |
| What do project terms mean?                                          | `machine-builder-research/ontology/TERMINOLOGY_BASELINE.md`        |
| What accepted decisions have been recorded?                          | `machine-builder-research/decisions/DECISION_LOG.md`               |
| What research questions remain open?                                 | `machine-builder-research/questions/OPEN_QUESTIONS.md`             |
| What is the current research/architecture checkpoint?                | `machine-builder-research/checkpoints/V0.2_RESEARCH_CHECKPOINT.md` |
| What is the current state of a particular implementation workstream? | That workstream's living handoff                                   |
| What retired/superseded documents existed and why?                   | `HISTORICAL_DOCUMENT_ARCHIVE.md`                                   |

---

# 3. Root Project Documents

## README.md

**Status:** AUTHORITATIVE

Primary question:

> What is Machine Builder and where should a new person start?

README is an orientation document.

It should explain:

* project purpose;
* where to start;
* the current high-level repository organization;
* the current workstream structure;
* where authoritative project documents are located;
* how to recover after a chat ends.

It should not become a detailed architecture, implementation history, or project transcript.

---

## MASTER_PLAN.md

**Status:** AUTHORITATIVE

Primary question:

> Where is Machine Builder going?

It owns:

* long-term direction;
* major strategic goals;
* durable architecture direction;
* future scope;
* deferred ideas;
* future problems worth preserving;
* major planning principles.

It is not the detailed implementation schedule.

An implementation experiment does not automatically change the Master Plan.

---

## PROJECT_CURRENT_STATE.md

**Status:** AUTHORITATIVE

Primary question:

> What is true across the project right now?

It owns:

* current cross-workstream state;
* current project milestone;
* active direction;
* important verified project-level findings;
* current open project questions;
* synchronization information;
* decisions that affect multiple workstreams.

Detailed implementation history belongs primarily in the owning workstream handoff.

The Current State document should remain a snapshot, not become a second history archive.

---

## CHAT_WORKFLOW.md

**Status:** AUTHORITATIVE

Primary question:

> How are the project's chats and workstreams operated?

It owns:

* workstream roles;
* chat recovery rules;
* repository authority rules;
* editing workflow;
* checkpoint conventions;
* ownership rules;
* commit/push workflow;
* documentation process.

It should point to `DOCUMENTATION_AUTHORITY.md` for the current document authority map rather than duplicating that map indefinitely.

---

## DOCUMENTATION_AUTHORITY.md

**Status:** AUTHORITATIVE

Primary question:

> Which document is authoritative for this question?

This document defines document roles and prevents multiple project documents from silently becoming competing authorities.

It is a governance/index document, not a substitute for the content documents it identifies.

---

# 4. Research / Architecture Documents

## machine-builder-research/START_HERE.md

**Status:** AUTHORITATIVE FOR RESEARCH NAVIGATION**

Primary question:

> Where does a Research / Architecture chat start?

It is a navigation and recovery document.

It should identify the current research checkpoint, core research authorities, and recovery order.

It should not duplicate the full contents of architecture or ontology documents.

---

## machine-builder-research/architecture/ARCHITECTURE_OVERVIEW.md

**Status:** AUTHORITATIVE

Primary question:

> What architecture has currently been established?

This is the primary settled architecture baseline.

Supporting architecture documents may elaborate specific subjects, including:

* data flow;
* system boundaries;
* other focused architecture topics.

Supporting documents must not silently redefine the architecture overview.

When an accepted decision changes architecture, the architecture baseline should be reconciled.

---

## machine-builder-research/ontology/ONTOLOGY_CURRENT.md

**Status:** AUTHORITATIVE

Primary question:

> What is the current canonical ontology?

It defines the current semantic model and its boundaries.

A research note, implementation handoff, or experiment does not silently add a new canonical entity.

---

## machine-builder-research/ontology/TERMINOLOGY_BASELINE.md

**Status:** AUTHORITATIVE

Primary question:

> What do Machine Builder's important terms mean?

It is the terminology baseline.

Research notes may introduce candidate terminology, but accepted terminology belongs here.

---

## machine-builder-research/decisions/DECISION_LOG.md

**Status:** AUTHORITATIVE FOR DECISION HISTORY

Primary question:

> What durable decisions have been accepted?

The Decision Log preserves decision provenance and history.

It does not replace the current architecture, ontology, or terminology documents.

When an accepted decision changes one of those authorities, the relevant authority document should be reconciled.

---

## machine-builder-research/questions/OPEN_QUESTIONS.md

**Status:** AUTHORITATIVE

Primary question:

> What important conceptual questions remain unresolved?

A question should remain here until it is resolved, deliberately deferred, or otherwise reclassified.

---

## machine-builder-research/checkpoints/V0.2_RESEARCH_CHECKPOINT.md

**Status:** CURRENT SUPPORTING / RESEARCH MILESTONE AUTHORITY

Primary question:

> What is the current research/architecture checkpoint for V0.2?

It records the current research milestone and stopping point.

It does not override the current architecture or ontology authorities.

---

## machine-builder-research/PROJECT_CONTEXT.md

**Status:** CURRENT SUPPORTING / UNDER REVIEW

Primary question:

> What background context helps a Research chat understand the project?

This document contains useful research/project context but is not an authority for current project state, architecture, or ontology.

Its contents should eventually be compared against `START_HERE.md`, `MASTER_PLAN.md`, `PROJECT_CURRENT_STATE.md`, and the research authorities to determine what should remain, migrate, or retire.

---

# 5. Implementation Planning Documents

Implementation plans are **scoped authorities**, not project-wide authorities.

They may answer:

> How are we currently planning to implement this specific milestone?

They do not answer:

> Where is the project going?

That belongs to `MASTER_PLAN.md`.

They do not answer:

> What is true across the project right now?

That belongs to `PROJECT_CURRENT_STATE.md`.

---

## V0.2_IMPLEMENTATION_PLAN.md

**Status:** WORKING / PROVISIONAL while V0.2 is active

Primary question:

> What is the scoped implementation plan for V0.2?

It remains useful while V0.2 is in progress.

When V0.2 is complete, it becomes a historical milestone record containing:

* the original plan;
* implementation decisions;
* final V0.2 state;
* carry-forward items.

It does not become permanent architecture authority.

---

## IMPLEMENTATION_ROADMAP.md

**Status:** AUTHORITATIVE

Primary question:

> What is the overall implementation roadmap for the Machine Structure Editor?

It owns the high-level implementation path, implementation milestones, version workflow, and future implementation direction.

It is a scoped implementation authority, not the authority for overall Machine Builder direction, canonical ontology, or current project-wide state.

The version-specific implementation plan remains the detailed plan and implementation record for an individual active milestone.

---

# 6. Workstream Handoffs

Workstream handoffs are the authoritative continuity records for their own workstreams.

They answer:

> What is this workstream doing, what has it verified, what remains unresolved, and what happens next?

Current living handoffs:

```text
01_PLANNING_ARCHITECTURE_WORKSTREAM_HANDOFF.md
02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md
03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md
04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md
05_EFFICIENCY_MODULARIZATION_WORKSTREAM_HANDOFF.md
```

A workstream handoff does not silently override project architecture.

When a workstream discovers a project-level architectural implication, it reports that implication to Planning / Architecture.

---

# 7. Historical Documentation

Historical material should be preserved when it provides:

* provenance;
* architectural history;
* implementation history;
* research history;
* reasoning that explains how the current design developed;
* unique information not yet preserved elsewhere.

Historical files should not remain in active locations solely because nobody has decided what to do with them.

However, no historical file should be deleted until:

1. its contents have been reviewed;
2. unique information has been identified;
3. useful information has been migrated where appropriate;
4. its historical disposition has been recorded.

The exact historical file contents remain recoverable through Git history.

---

# 8. Historical Document Archive

The historical-disposition index is:

`HISTORICAL_DOCUMENT_ARCHIVE.md`

It will record:

* original path;
* original filename;
* approximate creation/last-relevant period;
* document purpose;
* classification;
* what replaced it;
* unique information preserved;
* migration destination where applicable;
* reason for retirement.

It is an index/provenance record, not a duplicate copy of every historical document.

It is populated as historical inventory and content mapping are finalized; Git remains the source for the exact historical document contents.

---

# 9. Status Vocabulary

Use these statuses consistently.

## AUTHORITATIVE

The document is the primary answer to its defined question.

## CURRENT SUPPORTING

The document is current and useful but does not own a primary project question.

## WORKING / PROVISIONAL

The document is actively used for a scoped task or milestone but may change as evidence accumulates.

## HISTORICAL

The document describes a previous state and is intentionally retained for provenance/reference.

## SUPERSEDED

A newer document has replaced its active role.

Useful historical material may still justify keeping the file.

## RETIRED / ARCHIVED

The document has been removed from the active documentation structure after its useful information and provenance were preserved.

## UNDER REVIEW

The document's final disposition has not yet been established.

---

# 10. Governance Rules

1. One primary question should have one authoritative document.

2. Supporting documents may contain detail but should not silently become competing authorities.

3. A stale document is not automatically an obsolete document.

4. An old document should be compared against its current replacement before its status is changed.

5. Historical information should be preserved before retiring a document.

6. Git preserves exact historical contents; the historical archive index preserves the explanation of what happened.

7. Workstream handoffs own workstream continuity, not project-wide architecture.

8. Planning / Architecture owns project-wide architectural decisions and decides whether workstream discoveries become durable project architecture.

9. Research documents preserve external evidence and source provenance.

10. Current implementation behavior is determined by the current repository and verified tests, not by documentation alone.

11. When two authoritative documents appear to conflict, the conflict must be resolved explicitly rather than allowing both documents to remain silently authoritative.

12. A document's filename or age is never sufficient evidence for retirement.

---

# 11. Change Protocol

When a documentation role changes:

```text
Identify the question
        ↓
Identify the current authority
        ↓
Identify the proposed replacement/supporting document
        ↓
Compare contents
        ↓
Preserve unique information
        ↓
Update references
        ↓
Assign status
        ↓
Update this authority map if the authority changed
        ↓
Archive/retire the old document if justified
```

For structural changes:

```text
documents finalized
        ↓
references checked
        ↓
recursive_git_tree.txt regenerated
        ↓
diff inspected
        ↓
coherent commit
        ↓
push
```

---

# 12. Relationship to Chat Workflow

`CHAT_WORKFLOW.md` defines **how the workstreams operate**.

`DOCUMENTATION_AUTHORITY.md` defines **which document answers which question**.

The two documents are complementary.

The workflow document should point to this authority map rather than maintaining a second competing document hierarchy.

---

### Canonical future-feature register

`MASTER_PLAN.md` Section 13 ("Future problems / deferred ideas") is the authoritative project-level register. `CHAT_WORKFLOW.md` Section 37 defines intake and duplicate avoidance. Supporting technical evidence remains in the owning workstream's research notes and handoff. Do not create a competing backlog without an explicit Planning decision.

# 13. Current Initial Classification

The current starting classification is:

```text
README.md
    AUTHORITATIVE

MASTER_PLAN.md
    AUTHORITATIVE

PROJECT_CURRENT_STATE.md
    AUTHORITATIVE

CHAT_WORKFLOW.md
    AUTHORITATIVE

DOCUMENTATION_AUTHORITY.md
    AUTHORITATIVE

Research START_HERE.md
    AUTHORITATIVE FOR RESEARCH NAVIGATION

ARCHITECTURE_OVERVIEW.md
    AUTHORITATIVE

ONTOLOGY_CURRENT.md
    AUTHORITATIVE

TERMINOLOGY_BASELINE.md
    AUTHORITATIVE

DECISION_LOG.md
    AUTHORITATIVE FOR DECISION HISTORY

OPEN_QUESTIONS.md
    AUTHORITATIVE

V0.2_RESEARCH_CHECKPOINT.md
    CURRENT SUPPORTING / RESEARCH MILESTONE AUTHORITY

PROJECT_CONTEXT.md
    CURRENT SUPPORTING / UNDER REVIEW

V0.2_IMPLEMENTATION_PLAN.md
    WORKING / PROVISIONAL

IMPLEMENTATION_ROADMAP.md
    AUTHORITATIVE

CODER_CHAT_WORKFLOW.md
    SUPERSEDED

Older visual-builder documentation
    HISTORICAL

Historical routing handoffs
    HISTORICAL

HISTORICAL_DOCUMENT_ARCHIVE.md
    AUTHORITATIVE FOR HISTORICAL DOCUMENT DISPOSITION

Workstream handoffs
    CURRENT SUPPORTING / WORKSTREAM CONTINUITY
```

These classifications are the Planning-adjudicated dispositions for the current documentation checkpoint. Future disposition changes must follow the documented Change Protocol.

---

# 14. Decision Principle

The purpose of this system is not to eliminate documentation.

It is to prevent multiple documents from answering the same primary question with different versions of the truth.

The desired result is:

```text
one question
    ↓
one authority
    ↓
supporting detail where necessary
    ↓
historical material preserved separately
```
