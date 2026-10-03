# Chat 01 — Planning / Architecture Workstream Handoff

## Purpose

This is the living continuity document for Chat 01 — Planning / Architecture.

It exists so a replacement Planning chat can recover the current architectural thinking, decisions, unresolved questions, future ideas, and workstream coordination without relying on conversation history.

The repository and current `main` state remain authoritative for implementation facts.

---

# Recovery Instructions

A replacement Planning chat should:

1. Read this handoff completely.
2. Read `MASTER_PLAN.md`.
3. Read `PROJECT_CURRENT_STATE.md`.
4. Inspect the current repository state when implementation details matter.
5. Treat newer repository/test evidence as authoritative over stale remembered conversation.
6. Preserve settled architecture unless concrete evidence requires reconsideration.
7. Maintain the distinction between current decisions, candidates, experiments, and future ideas.

The handoff is continuity, not a substitute for the repository.

---

# Current Role of Chat 01

Chat 01 is the main Planning / Architecture / coordination space.

Primary responsibilities:

* overall architecture
* semantic model
* long-term direction
* feature planning
* milestone boundaries
* cross-workstream coordination
* deciding whether implementation discoveries justify architecture changes
* deciding what belongs in `PROJECT_CURRENT_STATE.md`
* preserving future ideas that should not be lost
* coordinating questions between Research and Implementation

Chat 01 should avoid unnecessary implementation work.

---

# Current Planning Position

The current architecture is machine-model-first.

The physical machine is the machine.

Firmware is a versioned implementation of the machine.

The canonical semantic model is authoritative.

The visual editor is presentation and authoring state over the canonical model.

The current working chain remains:

```text
Physical Machine
→ Machine Component
→ Hardware Definition
→ Controller
→ Controller Resource
→ Port / Connector / Pin
→ Connection
→ Function / Capability
```

This remains a working architecture rather than a command to create every named concept as a class.

Concrete implementation evidence should drive reconsideration.

---

# Current Architectural Principles

Important distinctions currently preserved:

```text
Hardware Definition
    ≠
installed hardware instance

Controller
    ≠
Controller Resource

Controller Resource
    ≠
physical interface

physical Connection
    ≠
Controller Resource Assignment

Function
    ≠
Capability

canonical semantic state
    ≠
visual/editor state
```

The system should not invent unknown information.

New canonical entities should not be introduced merely because they would make an implementation concept easier to name.

---

# Current Board Architecture Position

Recent Board work provides implementation evidence that the current model can represent:

* documented reusable hardware definitions
* installed controllers and machine components
* controller-owned physical SemanticPorts
* component-owned physical SemanticPorts
* connector grouping
* physical interface metadata
* resource exposure through SemanticPorts
* physical interface mating through semantic relationships
* replaceable driver-module cases

Recent Maestro and Octopus experiments have not, so far, justified new canonical entities such as:

* Connector
* BoardConnector
* MatingInterface
* DriverSocket
* DriverModule
* Contact

This remains subject to future concrete evidence.

---

# Current Routing Architecture Position

Routing is a presentation/implementation concern over canonical connection semantics.

The current important distinction is:

```text
Route topology
    ≠
Route geometry
```

Topology concerns structural choices.

Geometry concerns exact spatial placement.

The active routing investigation has emphasized preserving topology where practical and repairing geometry without unnecessarily rerouting.

Implementation heuristics should not automatically become durable architecture.

---

# Research Coordination

Chat 01 sends concrete research questions to Chat 02.

Research results should distinguish:

```text
IMPLEMENTATION ONLY
WATCH
REINFORCE
NEW PRINCIPLE — candidate
RECONSIDER
```

Research findings should be incorporated into durable architecture only after architectural review.

Chat 02 should preserve research continuity and source information in its own handoff.

---

# Workstream Coordination

Current workstreams:

```text
01 Planning / Architecture
02 Research / Architecture
03 Controller / Board
04 Routing / Diagnostics
05 Efficiency / Modularization
```

Implementation workstreams report durable project-level implications to Chat 01 rather than independently rewriting `PROJECT_CURRENT_STATE.md`.

Chat 05 reviews efficiency/modularity/code-health concerns and reports recommendations to the owning workstream.

---

# Current Documentation Architecture

```text
MASTER_PLAN.md
    ↓
long-term direction / future ideas

PROJECT_CURRENT_STATE.md
    ↓
current project-wide status

01 Planning handoff
02 Research handoff
03 Board handoff
04 Routing handoff
05 Efficiency handoff
    ↓
workstream continuity
```

Chat-instance numbers such as `1.2`, `2.3`, and `3.2` are human organizational labels only.

---

# Future Problems / Good Ideas

This is a durable holding area for ideas that should not be forgotten simply because they are not currently being implemented.

Examples currently worth preserving:

* richer reusable connector-definition modeling
* compatibility/intermateability modeling
* richer board visualization
* connector-aware and harness-aware wiring
* wire-level engineering detail
* broader mechanical representation
* reusable assemblies and tool modules
* richer diagnostics
* firmware reverse reconstruction
* multiple manufacturing processes
* Function vs Process vs Operation vs Task distinctions
* shared resources in hybrid manufacturing
* sequencing and process relationships
* future machine stress tests such as modular hybrid manufacturing systems

Each idea should eventually record:

```text
Idea
Why it matters
Current status
Evidence
Reason deferred
Condition for revisiting
```

---

# Important Active Questions

Current Planning should monitor:

### Architecture

* Is the current semantic model continuing to hold under real hardware cases?
* Are any implementation shortcuts starting to become unwanted architecture?
* Are new named concepts actually entities, relationships, definitions, or merely implementation structures?

### Board

* How should detailed reusable connector/interface information evolve if current representations become insufficient?
* What additional cases does Octopus reveal?
* When does contact-level information require richer modeling?

### Routing

* Where should topology selection stop and geometry repair/nudging begin?
* Which routing behaviors are architecture and which are heuristics?

### General Machine Model

* What additional abstractions are needed for machines beyond conventional printers?
* When should future manufacturing-process concepts enter the canonical model?

---

# Development / Repository Edit Rule

When Planning requests a repository change, it must provide:

```text
REPOSITORY CHANGE REQUIRED

File:
exact repository path

Action:
CREATE / EDIT EXISTING / FULL FILE REPLACEMENT

Repository state inspected:
branch
commit

Location:
exact section, class, function, or line range

Anchor:
exact nearby text

Change:
complete paste-ready text
```

Full-file replacement is preferred when practical.

For multiple surgical edits:

* provide edits in descending line-number order when possible;
* explain that earlier edits may shift the line numbers of later edits;
* use exact anchors in addition to line numbers;
* do not rely on phrases such as "the port loop" without identifying the actual function/block.

If the cited line or anchor does not exist in the user's checkout, the edit should stop and the file should be re-inspected rather than guessed.

---

# Checkpoint Format

Every meaningful Planning checkpoint should record:

```text
Checkpoint N
Date/time:
Current commit:
Repository state:
Current test state if relevant:

What changed:
Why it matters:
Architectural interpretation:
Decisions:
Open questions:
Next action:
```

The `Next action` belongs to the current-state section, not inside the chronological checkpoint history.

New checkpoints should normally be appended to history rather than inserted around `Next action`.

---

# Current State

Updated:
2026-10-03

Current repository model:
main-only shared checkout

Current major coordination concern:
preserve durable architectural continuity across chat-length boundaries.

Current documentation improvement:
dedicated living handoffs for Planning, Research, Board, Routing, and Efficiency.

Current next Planning action:

1. Establish the Master Plan as the long-term project plan.
2. Establish the Research handoff as the durable research/source record.
3. Continue coordinating Board and Routing discoveries against the project-wide architecture.
4. Preserve good future ideas without promoting them prematurely.

---

# What Has Been Established Recently

Recent Board work has demonstrated with real documented hardware that the existing model can represent multiple physical interface forms, resource exposure, replaceable driver-module mating, and module-specific hardware definitions without immediately requiring new canonical entities.

Recent Routing work has produced implementation evidence around topology preservation, geometric stability, deterministic routing behavior, spacing, and the distinction between route topology and route geometry.

These are implementation-informed architectural observations and should continue to be tested rather than treated as immutable doctrine.

---

# Recovery Rule

When a future Chat 01 reaches the conversation limit:

```text
Read this handoff
    ↓
Read MASTER_PLAN.md
    ↓
Read PROJECT_CURRENT_STATE.md
    ↓
Inspect current main/repository when needed
    ↓
Continue from Current State / Next action
```

Do not reconstruct Planning history from memory when the handoff contains the needed information.
