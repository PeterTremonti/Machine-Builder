# Chat 02 — Research / Architecture Workstream Handoff

## Purpose

This is the living continuity document for Chat 02 — Research / Architecture.

Its purpose is to preserve research questions, evidence, standards, source material, conclusions, uncertainties, and research already completed so that a replacement Research chat does not unnecessarily repeat previous work.

The goal is evidence-driven guidance for Planning and Implementation.

---

# Recovery Instructions

A replacement Research chat should:

1. Read this handoff completely.
2. Read `MASTER_PLAN.md` and `PROJECT_CURRENT_STATE.md`.
3. Review the current repository when a research question concerns implementation behavior.
4. Treat authoritative external sources as evidence.
5. Preserve source provenance for important findings.
6. Distinguish documented facts from interpretation.
7. Report uncertainty rather than filling gaps with assumptions.
8. Re-check current sources when time-sensitive information may have changed.
9. Classify findings appropriately before recommending architectural changes.

---

# Current Role of Chat 02

Chat 02 investigates questions that arise from Planning and Implementation.

Primary responsibilities:

* standards research
* terminology research
* manufacturer documentation
* CAD/system conventions
* established engineering practices
* software architecture precedent
* implementation-pattern research
* comparison of existing approaches
* reporting evidence and limitations back to Chat 01

Chat 02 should not independently redefine durable project architecture.

---

# Research Reporting Classifications

Use:

```text
IMPLEMENTATION ONLY
```

for useful implementation knowledge that does not alter architecture.

```text
WATCH
```

for an important distinction or possibility not yet established as required.

```text
REINFORCE
```

for external evidence supporting an architecture already being used.

```text
NEW PRINCIPLE — candidate
```

for a potentially durable architectural principle that requires Planning review.

```text
RECONSIDER
```

when evidence indicates an existing architecture may be insufficient or contradictory.

---

# Source Preservation Rule

Important research must preserve enough information for a replacement Research chat to identify the original evidence.

For each important source, record as much of the following as available:

```text
Source title:
Organization / author:
Document or standard identifier:
Publication/version:
URL or repository location:
Date accessed:
Relevant section/page:
What it establishes:
What it does NOT establish:
How it affects Machine Builder:
```

Do not keep only a conclusion without the source that supports it.

Do not keep only a URL without recording why the source mattered.

Standards should include the standard number and relevant terminology/section where practical.

---

# Connector / Interface Research

Research into connector terminology has established important conceptual distinctions around:

```text
Physical Connector
    ≠
Reusable Connector Definition
    ≠
Mating Interface
    ≠
Intermateability / compatibility
    ≠
Actual Mated Connector Pair
```

Manufacturer and engineering-system evidence also supports distinctions involving:

* housing/body
* contact/terminal
* mating interface
* termination interface
* keying/polarization
* retention
* mating parts
* reusable definitions versus installed instances

Current architectural conclusion:

These concepts should not automatically become individual canonical Machine Builder entities.

The current model should introduce additional entities only when an actual machine case demonstrates the need.

---

# Routing Research

Research has identified established precedent for separating routing concerns such as:

```text
route/topology generation
        ↓
route geometry
        ↓
spacing/nudging/adjustment
        ↓
final visual route
```

Research has also identified precedent for:

* preserving existing topology during incremental editing
* minimizing unnecessary rerouting
* edge/segment separation preferences
* orthogonal nudging
* movable and protected route segments
* bend penalties
* incremental topology preservation

Important examples investigated include:

* yFiles orthogonal routing and minimum-edge-distance concepts
* libavoid routing/nudging concepts
* Microsoft Automatic Graph Layout / MSAGL routing and nudging
* academic work on orthogonal graph drawing and segment separation

The architectural interpretation remains cautious:

```text
preferred spacing
    ≠
hard geometric legality

topology preservation
    ≠
a particular router implementation
```

Routing research should inform the implementation without automatically dictating architecture.

---

# Board / Connector Research

Current Board research has examined real hardware interface representation and connector terminology.

Important evidence includes:

* IEC connector terminology and intermateability concepts
* Molex connector/interface documentation
* TE Connectivity connector and mating terminology
* Autodesk Inventor connector/mating/interface concepts
* manufacturer documentation for actual controller boards and driver modules

Current Board research supports the following working model:

```text
Hardware Definition
        ↓
installed hardware instance
        ↓
physical interface SemanticPort(s)
        ↓
relationships / physical connections
```

Current implementation evidence from Maestro and Octopus does not yet require a canonical Connector or MatingInterface entity.

---

# Current Research Findings of Interest

### Controller Resource vs Physical Interface

A Controller Resource is not automatically a physical connector or pin.

It may be exposed through one or more physical access points.

Research should continue to distinguish:

```text
resource identity
physical interface identity
contact/pin identity
electrical connection
assignment
```

### Mating

A physical mating relationship can be conceptually distinct from resource exposure and resource assignment.

Current implementation experiments use:

```text
SemanticPort
    --mated_with-->
SemanticPort
```

without requiring a dedicated mating entity.

The research question remains whether future hardware cases eventually require additional reusable interface/compatibility concepts.

---

# Research That Should Not Be Repeated Without a New Question

Do not repeat broad connector/mating terminology research merely because a new Board chat starts.

The following questions have already received substantial investigation:

* connector versus mating interface terminology
* reusable connector definition versus physical connector
* intermateability concept
* housing/contact distinctions
* general orthogonal-routing topology versus geometry distinctions
* established routing nudging/separation concepts

Repeat research only when a new implementation case asks a materially different question or the relevant standard/documentation has changed.

---

# Research Queue

Current useful questions include:

### Board

* Does the Octopus receiving driver socket and TMC5160T J1/J2 documentation introduce a requirement for richer contact-level reusable definitions?
* What do other replaceable-driver or pluggable-module systems require?
* When does connector compatibility become an actual canonical machine requirement?

### Routing

* What is the appropriate boundary between topology selection, geometric repair, and preferred spacing?
* Which routing behaviors deserve durable architecture versus implementation heuristics?

### General Machine Model

* How should Function, Capability, Process, Operation, Task, and sequencing relate in broader manufacturing systems?
* What does a modular hybrid manufacturing machine require that conventional printer cases do not?

---

# Research-to-Planning Protocol

When reporting a research result to Chat 01, use:

```text
RESEARCH FINDING

Question:
...

Sources:
...

Documented evidence:
...

Interpretation:
...

What the evidence does NOT establish:
...

Classification:
IMPLEMENTATION ONLY / WATCH / REINFORCE /
NEW PRINCIPLE — candidate / RECONSIDER

Implication for Machine Builder:
...

Recommended next research or implementation question:
...
```

This keeps evidence separate from conclusion.

---

# Current State

Updated:
2026-10-03

Research role:
evidence and external precedent for Planning and Implementation.

Current major research themes:

* connector/interface semantics
* board hardware representation
* mating relationships
* orthogonal routing architecture
* modular machine/process architecture

Current documentation priority:

Preserve source provenance and research conclusions so that replacement chats do not have to reconstruct the research history from conversation memory.

---

# Repository Change Rule

Chat 02 should not independently rewrite `PROJECT_CURRENT_STATE.md`.

When research reveals a project-level implication, report:

```text
PROJECT CURRENT STATE UPDATE REQUEST

Why:
...

Proposed location:
...

Proposed content:
...

Source:
...
```

Planning / Architecture decides whether to incorporate it.

If Chat 02 needs a repository file changed for research documentation:

```text
REPOSITORY CHANGE REQUIRED

File:
exact repository path

Action:
...

Location:
exact section / line range / anchor

Change:
complete paste-ready text
```

---

# Surgical Edit Rules

When a surgical edit is necessary:

* identify the repository commit inspected;
* give exact line numbers;
* give an exact text/class/function anchor;
* describe the location in plain language;
* for multiple edits, give edits from highest line number to lowest when possible;
* explicitly warn when an earlier edit changes the location of a later edit;
* never rely on programmer shorthand that is not meaningful to a non-programmer user.

If the expected line or anchor cannot be found, stop and re-inspect the current file.

---

# Recovery Rule

When a future Chat 02 reaches the conversation limit:

```text
Read this handoff
    ↓
Read MASTER_PLAN.md
    ↓
Read PROJECT_CURRENT_STATE.md
    ↓
Review the source register
    ↓
Continue the current research queue
```

Do not redo completed research unless a new question requires it or the source has materially changed.
