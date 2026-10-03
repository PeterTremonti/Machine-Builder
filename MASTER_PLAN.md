# Machine Builder — Master Plan

## 1. Purpose

Machine Builder is intended to become a machine-model-first engineering environment for describing, inspecting, documenting, validating, configuring, and eventually designing real machines.

The initial practical focus is 3D printers and related motion-control machines.

The underlying architecture is intentionally broader so that the system can eventually support CNC, laser machines, hybrid manufacturing systems, and other machines without replacing the canonical machine model.

The central principle is:

> The physical machine is the machine. Firmware is a versioned implementation of that machine, not the machine's identity.

---

# 2. Original idea

The project originally began as a way to configure and ultimately convert a real printer to working firmware.

The original problem exposed a larger need:

* hardware identification
* board and resource mapping
* wiring documentation
* compatibility checking
* diagnostics
* firmware translation
* machine documentation
* eventually physical machine representation

The project therefore evolved from a firmware configurator into a machine-building/modeling system.

---

# 3. Working idea

The current working concept is a machine-model-first system built around a canonical semantic representation.

The broad pipeline is:

```text
Physical Machine
        ↓
Canonical Machine Model
        ↓
Firmware Requirements / Mapping
        ↓
Target Firmware + Version
        ↓
Generated Configuration
```

The reverse direction is also important:

```text
Firmware / Configuration
        ↓
Semantic Interpretation
        ↓
Canonical Machine Model
```

The canonical machine model is authoritative.

Visual/editor state is an authoring and presentation layer over that model rather than a second semantic model.

---

# 4. Core architecture

The current working semantic chain is approximately:

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
Port / Connector / Pin
        ↓
Connection
        ↓
Function / Capability
```

Important distinctions must remain explicit.

```text
Hardware Definition
    ≠
installed hardware instance

Controller
    ≠
Controller Resource

Controller Resource
    ≠
physical Port / Connector / Pin

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

New entities should not be introduced merely because an implementation concept has a useful name. Concrete evidence should demonstrate that the existing model cannot represent the required meaning.

---

# 5. V0.2

V0.2 is the current implementation milestone.

The goal is to establish a dependable canonical machine model and a usable visual/editor foundation rather than prematurely implementing the entire long-term vision.

The current implementation includes substantial semantic-authoring and visual-editor infrastructure.

The repository and automated tests are authoritative for actual implementation status.

---

# 6. Current hardware direction

The initial hardware catalog should prioritize real, documented hardware for which reliable specifications and provenance can be established.

Important current examples include:

* Duet 2 Maestro
* BTT Octopus V1.1
* BIGTREETECH TMC5160T V1.0
* real motors, heaters, sensors, fans, probes, and other documented machine hardware

Reusable Hardware Definitions describe known hardware.

Installed Machine Components and Controllers represent the machine-specific instances.

---

# 7. Current Board architecture direction

Board work is currently using:

```text
HardwareDefinition
        ↓
installed Controller / MachineComponent
        ↓
controller-owned or component-owned SemanticPort
        ↓
connector grouping / interface metadata
        ↓
semantic relationships and physical/electrical connections
```

Recent Maestro and Octopus implementation experiments have provided evidence that the current model can represent:

* multiple connector groups
* different connector sizes and interface types
* one Controller Resource exposed through multiple physical access points
* replaceable driver-module interfaces
* controller-owned and component-owned physical mating endpoints
* `mated_with` relationships without requiring a new canonical Connector, DriverSocket, MatingInterface, or DriverModule entity for the cases tested so far

These conclusions remain subject to concrete evidence from additional hardware cases.

---

# 8. Current routing direction

Routing is an implementation subsystem over canonical connection semantics.

An important working distinction is:

```text
Route topology
    = corridor/side choices, bend sequence, structural organization

Route geometry
    = exact coordinates, segment positions, lengths, and spacing
```

The routing system should preserve stable route structure when practical while allowing geometry to change.

Preferred visual spacing and hard legality constraints should remain conceptually distinct.

Routing behavior should not redefine canonical machine connectivity.

---

# 9. Visual editor direction

The visual editor is an authoring and inspection environment over the canonical model.

Visual state may include:

* canvas position
* size
* selection
* zoom
* pan
* routing geometry
* grouping
* layers and filters
* semantic zoom
* presentation details

These are not substitutes for canonical machine meaning.

The editor should allow different levels of detail without creating multiple semantic representations of the same machine.

---

# 10. Firmware direction

Firmware is an implementation target rather than the definition of the machine.

The long-term system should support semantic translation between the machine model and multiple firmware ecosystems, including examples such as:

* Klipper
* RepRapFirmware
* Marlin
* GRBL and related machine-control systems where appropriate

Translation should operate on machine concepts rather than textual substitution between configuration files.

---

# 11. Documentation and provenance

Hardware facts should be traceable to appropriate sources.

Useful source categories include:

* manufacturer manuals
* pinout documentation
* electrical specifications
* CAD models
* photographs
* wiring diagrams
* firmware documentation
* configuration examples
* standards
* other authoritative technical sources

Known information should not be fabricated merely to make a model complete.

Unknown information should remain unknown or explicitly flagged.

---

# 12. Future machine scope

The architecture is intended to expand beyond the initial printer use cases.

Future stress-test machines and systems include:

* resin printers
* laser-equipped printers
* laser cutters
* LowRider machines
* CNC machines
* hybrid machines
* modular manufacturing systems
* unusual motion systems
* machines with multiple tools or processes

The architecture should be tested against these increasingly difficult cases rather than being optimized only for conventional Cartesian printers.

---

# 13. Future problems / deferred ideas

This section is a durable holding area for good ideas that are not yet part of the active implementation.

Ideas should not be lost merely because they are intentionally deferred.

Each future item should record:

```text
Idea
Why it may matter
Current status
Evidence currently available
What would justify revisiting it
```

Examples currently worth preserving include:

* richer reusable connector definitions
* deeper connector compatibility/intermateability modeling
* more detailed board and connector visualization
* wire/harness-level engineering
* richer machine geometry and mechanical representation
* machine/process/task modeling for hybrid manufacturing
* reusable assemblies and tool modules
* increasingly detailed diagnostics
* broader firmware import and reverse reconstruction
* additional manufacturing processes
* machine-level sequencing and shared-resource modeling

These remain future/candidate areas unless promoted by evidence and architecture review.

---

# 14. Modularity and code health

The project should favor cohesive modules with clear responsibilities.

A file approaching roughly 1,000 lines is a useful prompt to reevaluate its responsibilities.

This is not a hard maximum.

A larger file may remain appropriate when it represents one cohesive responsibility.

A smaller file may still deserve decomposition when it contains unrelated concerns.

Refactoring decisions should consider:

* responsibility boundaries
* dependency direction
* testability
* reuse
* readability
* coupling
* ownership by the relevant workstream

---

# 15. Development workflow

The repository uses one active `main` branch and one shared working checkout.

Specialized chats are workstreams, not competing branches.

Current workstream roles are:

```text
01 Planning / Architecture
02 Research / Architecture
03 Controller / Board
04 Routing / Diagnostics
05 Efficiency / Modularization
```

Chat-instance suffixes such as `3.1`, `3.2`, or `4.3` identify replacement chat instances for human organization. They are not architectural identifiers.

The repository, tests, and current `main` state are authoritative.

---

# 16. Long-term goal

The long-term goal is a general machine-engineering environment in which a real machine can be:

```text
described
→ inspected
→ documented
→ validated
→ wired
→ diagnosed
→ mapped to firmware
→ converted between firmware systems
→ modified
→ expanded
→ eventually designed
```

while maintaining one canonical semantic representation of the machine underneath the different views and outputs.

---

# 17. Planning rule

The Master Plan describes long-term direction and durable future ideas.

It should evolve deliberately.

It should not become a transcript.

It should not be rewritten merely because an implementation experiment produces a temporary idea.

The durable decision flow is:

```text
Idea
    ↓
Research / experiment
    ↓
Evidence
    ↓
Architecture review
    ↓
Current-state decision
    ↓
Implementation
```

Deferred ideas remain recorded rather than forgotten.

---

# 18. Relationship to other project documentation

```text
MASTER_PLAN.md
    = long-term direction and durable future ideas

PROJECT_CURRENT_STATE.md
    = current project-wide status, active direction, and open questions

01_PLANNING_ARCHITECTURE_WORKSTREAM_HANDOFF.md
    = Planning / Architecture continuity

02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md
    = Research continuity and source/evidence history

03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md
    = Controller / Board implementation continuity

04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md
    = Routing / Diagnostics implementation continuity

05_EFFICIENCY_MODULARIZATION_WORKSTREAM_HANDOFF.md
    = Code-health and modularity review continuity
```

No document should silently become a replacement for another document's role.
