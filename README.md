# Machine Builder

Machine Builder is a **Machine Development Environment (MDE)** for describing, designing, inspecting, documenting, validating, and eventually configuring real machines.

The central principle is:

> **The physical machine is the machine. Firmware is a versioned implementation of that machine, not the machine's identity.**

The canonical machine model is therefore the semantic center of the project.

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

Reverse interpretation is also intended:

```text
Firmware / Configuration
        ↓
Semantic Interpretation
        ↓
Canonical Machine Model
```

---

# Where to Start

Machine Builder uses several complementary project documents.

Read these in this order when you need project-wide context:

```text
README.md
MASTER_PLAN.md
PROJECT_CURRENT_STATE.md
CHAT_WORKFLOW.md
```

Then read the handoff for the workstream you are joining.

The repository is the durable shared memory between chats.

When documentation and the actual repository disagree, current repository contents and current tests take precedence for implementation facts.

---

# Project Documentation

## Master Plan

```text
MASTER_PLAN.md
```

Defines the long-term direction of Machine Builder.

Contains:

* original project idea
* current working concept
* major architecture direction
* long-term goals
* future features
* deferred ideas
* future problems worth preserving
* major development principles

The Master Plan is intentionally not a project transcript.

---

## Project Current State

```text
PROJECT_CURRENT_STATE.md
```

Defines the current project-wide snapshot.

Contains:

* current architecture status
* active workstreams
* verified implementation checkpoints
* important architectural observations
* open project-level questions
* current coordination state
* things that should not be reopened without evidence

Planning / Architecture (#1) owns this document.

---

## Chat Workflow

```text
CHAT_WORKFLOW.md
```

Defines how Machine Builder workstreams operate.

It covers:

* chat recovery
* repository authority
* main-only development
* workstream ownership
* full-file replacement preference
* surgical-edit rules
* line numbers and anchors
* multiple-edit ordering
* timestamps
* testing/checkpoints
* README maintenance
* generated repository-tree maintenance
* project-state update requests
* source/research handling
* documentation expectations

All workstreams should read this document.

---

# Current Workstreams

## 01 — Planning / Architecture

Living handoff:

```text
machine-structure-editor/handoffs/01_PLANNING_ARCHITECTURE_WORKSTREAM_HANDOFF.md
```

Responsible for:

* overall architecture
* canonical semantic model
* long-term planning
* project coordination
* durable architectural decisions
* future ideas
* deferred problems
* project-wide state

---

## 02 — Research / Architecture

Living handoff:

```text
machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md
```

Responsible for:

* standards research
* terminology
* manufacturer documentation
* CAD/system precedent
* engineering practices
* external technical evidence
* source provenance
* research conclusions
* unresolved research questions

Important research should preserve its sources and explain what the evidence does and does not establish.

---

## 03 — Controller / Board

Living handoff:

```text
machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md
```

Responsible for:

* controller boards
* Hardware Definitions
* controller resources
* physical interfaces
* board fixtures
* connector/interface research as needed
* Board implementation tests

Current Board work is validating whether the existing canonical model remains sufficient for increasingly realistic controller hardware cases.

---

## 04 — Routing / Diagnostics

Living handoff:

```text
machine-structure-editor/handoffs/04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md
```

Responsible for:

* connection routing
* routing diagnostics
* route stability
* topology/geometry behavior
* routing implementation
* routing tests

Routing is a presentation/implementation concern over canonical connection semantics.

The project distinguishes route topology from route geometry.

---

## 05 — Efficiency / Modularization

Living handoff:

```text
machine-structure-editor/handoffs/05_EFFICIENCY_MODULARIZATION_WORKSTREAM_HANDOFF.md
```

Responsible for inspection and recommendations concerning:

* large files
* module boundaries
* dependencies
* duplication
* coupling
* documentation gaps
* test organization
* code health

This workstream normally recommends changes rather than independently rewriting code owned by another workstream.

---

# Chat Instance Numbering

Workstream numbers identify roles.

Replacement-chat suffixes identify individual ChatGPT conversation instances for human organization.

For example:

```text
3
3.1
3.2
3.3
```

means successive Controller / Board chat instances.

The suffix does not represent a software version, branch, architecture identifier, or repository component.

---

# Repository Structure

Primary implementation:

```text
machine-structure-editor/
```

Python source:

```text
machine-structure-editor/src/machine_builder/
```

Tests:

```text
machine-structure-editor/tests/
```

Implementation documentation and handoffs:

```text
machine-structure-editor/handoffs/
```

Research:

```text
machine-builder-research/
```

The generated repository path index is:

```text
recursive_git_tree.txt
```

It is useful for locating files but is not authoritative for file contents.

---

# Canonical Architecture

Machine Builder is built around a canonical semantic model.

The visual editor is an authoring and presentation layer over that model.

It is not a second semantic model.

The current working controller/hardware chain is approximately:

```text
Physical Machine
        ↓
Machine Component
        ↓
Hardware Definition
        ↓
Controller
        ↓
Controller Resource
        ↓
SemanticPort / physical interface
        ↓
Connection / relationship
        ↓
Function / Capability
```

Important distinctions include:

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

physical connection
    ≠
Controller Resource Assignment

canonical semantic state
    ≠
visual/editor state
```

New canonical entities should not be introduced merely because an implementation concept has a convenient name.

Concrete evidence should establish that the existing model is insufficient before the durable ontology is expanded.

---

# Current Development State

The active implementation milestone is V0.2.

Not every planned V0.2 user-facing feature is complete.

The current verified implementation status should be obtained from:

```text
PROJECT_CURRENT_STATE.md
```

and from the current repository/tests.

Workstream-specific details belong in the appropriate living handoff.

---

# Development Principles

The project prefers:

* machine-model-first design
* clear semantic boundaries
* real documented hardware
* provenance for important facts
* automated tests
* cohesive modular source files
* full-file replacements when practical
* durable documentation
* explicit architectural review before introducing major new concepts

Unknown information should remain unknown rather than being fabricated.

Implementation experiments should not silently become permanent architecture.

---

# Historical Material

Historical documents and experiments may remain in the repository.

They should not be treated as current architecture merely because they contain useful or previously implemented ideas.

Current implementation should be determined from:

```text
current main
current source
current tests
current workstream handoffs
current project-state documentation
```

Historical files are reference material unless explicitly promoted back into the current architecture.

---

# Recovery After a Chat Ends

When a workstream reaches its conversation-length limit, follow Section 17, Workstream Recovery, in `CHAT_WORKFLOW.md`. That section is the single authoritative replacement-chat procedure and distinguishes universal required reading, additional workstream-specific required reading, task-dependent references, and historical/reference material.

This README does not maintain a separate recovery checklist. The current living handoff for each workstream is listed in the workstream sections above.

---

# Repository Authority

For implementation facts:

```text
current repository / current main
        >
current tests
        >
current workstream handoff
        >
PROJECT_CURRENT_STATE.md
        >
MASTER_PLAN.md
        >
conversation memory
```

For external technical facts:

```text
current authoritative source
        >
research evidence / source record
        >
conversation memory
```

The project deliberately favors current evidence over remembered chat state.

---

# Getting Started with Development

Before modifying the repository:

1. Read the relevant project documentation.
2. Read the appropriate workstream handoff.
3. Inspect the current source and tests.
4. Determine whether the change is architectural, implementation-only, or exploratory.
5. Preserve established architecture unless concrete evidence requires reconsideration.
6. Run tests after meaningful changes.
7. Document meaningful checkpoints.
8. Commit and push at sensible milestones.

For detailed chat operating rules, use:

```text
CHAT_WORKFLOW.md
```

For the long-term direction, use:

```text
MASTER_PLAN.md
```

For current project status, use:

```text
PROJECT_CURRENT_STATE.md
```
