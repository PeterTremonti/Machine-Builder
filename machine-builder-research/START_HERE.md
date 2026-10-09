Last reconciled by Research / Architecture 2026-10-04

# Machine Builder Research & Architecture
## O0.1 Checkpoint — Minimum 3D-Printer Machine Model

This document is the current Research / Architecture navigation and recovery entry point. It points to the durable research, architecture, terminology, ontology, standards, and machine-knowledge record for Machine Builder / Machine Development Environment (MDE) without duplicating those authorities.
## Current checkpoint

**Research / Architecture:** R0.1 — foundational research consolidated

**Ontology:** O0.1 — minimum 3D-printer machine/firmware model validated

**Implementation:** V0.2 development. The visual editor is operating as a bidirectional authoring and inspection environment over the canonical machine model. Connection and routing behavior are implementation concerns being validated against that semantic boundary.
The O0.1 scope is intentionally narrow. The first working Machine Builder is primarily intended to describe a 3D printer physically and semantically well enough to derive firmware representations for supported firmware families and versions.

### V0.2 implementation checkpoint

The current implementation milestone is V0.2.

V0.2 is built on the O0.1 canonical machine model and does not replace or reopen the O0.1 ontology checkpoint.

V0.2 focuses on turning the visual editor into a bidirectional canonical-machine authoring and inspection environment for real 3D printers.

The V0.2 stopping point is recorded in:

`checkpoints/V0.2_RESEARCH_CHECKPOINT.md`

The current Research workstream continuity and recovery document is:

`../machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md`

Future ideas may be recorded without automatically expanding V0.2. Promotion of future concepts should wait for implementation, machine, firmware, or research evidence.

O0.1 remains the foundational semantic baseline for V0.2. Historical implementation-phase handoffs are retained only for historical/reference purposes and are not part of current Research recovery or coordination.

## Core purpose

The physical machine is the machine. Firmware is an optional, versioned implementation of that machine.

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

Reverse direction:

```text
Firmware / Configuration
        ↓
Semantic Interpretation
        ↓
Canonical Machine Model
```

The canonical machine model is the semantic center and authoritative structured representation. The visual editor is a bidirectional authoring and inspection environment for that model:

```text
            Canonical Machine Model
                    ↕
          Semantic / Model Boundary
                    ↕
             Visual Machine Editor
```

Existing canonical information may be projected into the editor:

```text
Canonical Machine Model
        ↓
Visual projection
        ↓
Editor
```

User-authored semantic changes flow back into the canonical model:

```text
User action
     ↓
Semantic edit / mutation
     ↓
Canonical Machine Model
     ↓
Updated visual representation
```

The visual editor is therefore not merely a read-only consumer of canonical semantics, and it is not a second machine model.
## O0.1 supported scope

O0.1 is intentionally focused on the physical and semantic information needed for 3D printers, especially:
- machine structure and machine components
- mechanical structure and moving systems
- axes and kinematics
- motors, actuators, drives, and controller resources
- extruders and tools
- heaters and fans
- sensors, probes, and endstops
- electrical ports, connectors, pins/terminals, wires/cables, and connections
- machine functions and capabilities needed for the printer
- properties, derived values, calibration, unknown values, and provenance
- current firmware context, when known
- firmware capability/version context, mappings, and translation results
### Explicitly deferred from O0.1

- water/liquid-cooled hotend plumbing
- general fluid systems
- hydraulic systems
- automotive fuel systems
- general-purpose plumbing/couplers
- universal material/fluid interface ontology
- full process/workflow ontology
- full robotics configuration-space ontology
- full engineering simulation
- certification-grade evaluation

These are future research/architecture targets, not O0.1 blockers.
## Firmware principle

A machine can exist in the model with no firmware information at all. Controller hardware and the physical machine description must be sufficient to determine the firmware requirements and allow a target firmware representation to be generated.

A saved machine may also retain:

- current firmware family
- current firmware version
- current firmware configuration/source
- firmware-specific customizations or macros
- translation history
Those are implementation/history information about the machine, not the identity of the machine itself.
## Visual editor principle

The visual editor is a bidirectional authoring and inspection environment over the canonical machine model.

The editor may author or modify canonical semantic entities and relationships such as:

- Machine Components
- Subsystems
- Ports
- Connectors / pins / terminals
- Connections
- Functions
- Capabilities
- Controller-resource assignments
- Properties
- Calibration information
- other canonical relationships

The visual model remains separate from canonical machine semantics.

Visual presentation state includes things such as:

- canvas position
- node size
- routing
- selection
- zoom
- collapsed/expanded state
- other presentation-only state

A visual object represents or exposes a canonical entity; it is not itself the canonical entity.

A visual line represents or edits a canonical semantic Connection; it does not own or replace that Connection.

### Viewing and Editing modes

**Viewing mode** is primarily for inspection, navigation, filtering, and exploration of canonical machine information.

**Editing mode** is for authoring and modifying canonical machine semantics and relationships.

Both modes operate on the canonical machine model. Viewing mode is not a separate semantic model.

### Partially specified machines

A machine does not need every component specification or hardware identity to be known before the machine can exist as a valid canonical model.

Known and unknown information may coexist intentionally. For example, a Machine Component may have:

- a known machine role
- a known physical placement
- known connections
- known relationships
- an unspecified hardware definition
- unknown specifications

Unknown / unspecified information is a valid modeled state. The editor must not force invented or placeholder values merely to satisfy a UI or implementation requirement.

### Machine Component and hardware definition

A Machine Component is the machine-specific semantic object representing a component occurrence within that machine.

Its hardware definition or catalog identity is separate from the Machine Component itself and may be absent until known.

A Machine Component may therefore exist before the exact purchased hardware is identified.

### Replace Component

Replace Component is a semantic editing operation, not a delete/create shortcut.

The intended behavior is:

```text
Existing Machine Component
        ↓
preserve machine identity and existing relationships
        ↓
replace / enrich hardware definition
        ↓
updated Machine Component
```

The operation should preserve, unless explicitly changed:

- Machine Component identity
- machine role
- physical placement
- existing connections
- subsystem membership
- relevant ports/interfaces
- Functions / other semantic relationships

The exact hardware definition/specifications may be replaced or enriched with the newly identified item.

### Provenance of authored information

Canonical information authored through the visual editor remains canonical machine information, but its provenance must identify how it was established.

For example, provenance may record:

```text
source: user
evidence type: authored
method: visual editor
context: editor session
```

This must remain distinguishable from documented, observed, measured, inferred, derived, calibrated, or firmware-derived information.

### Future change review

The architecture should eventually support a semantic change-review mechanism in which complex editing operations can produce a proposed change set before the changes become committed canonical model state.

Example:

```text
Added Temperature Sensor
Connected Sensor → Controller
Assigned role: temperature measurement
Hardware definition: unspecified
```

This is an architectural direction, not a requirement for the first V0.2 implementation.
## Recovery and Research-document navigation

### Universal recovery — every workstream

Follow `../CHAT_WORKFLOW.md` §17 for the universal replacement-chat recovery procedure. That section is authoritative for the shared startup sequence; this file does not define a competing universal sequence.

### Required Research-specific reading

Read this `START_HERE.md` on every Research / Architecture replacement, in addition to the universal reading defined by §17. This file remains the authoritative Research navigation and recovery entry point.

The current Research continuity record is `../machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md`. The handoff is included in universal recovery under §17; use its current state and Next Action to resume work. Research-specific evidence and reporting requirements are retained in that handoff.

### Consult according to the current Research Next Action

The following documents remain authoritative for their respective subjects. They are task-dependent reading, not obsolete documents and not a mandatory full reread on every replacement.

- `RESEARCH_ROADMAP.md` — consult for Research priorities, sequencing, and roadmap dependencies.
- `PROJECT_CONTEXT.md` — consult for background and supporting project context; do not use it in place of authoritative project state or architecture records.
- `architecture/ARCHITECTURE_OVERVIEW.md` — consult for established architecture and system-boundary questions.
- `ontology/TERMINOLOGY_BASELINE.md` — consult when terminology definitions or naming distinctions matter.
- `ontology/ONTOLOGY_CURRENT.md` — consult for the current canonical ontology, entities, and relationship semantics.
- `decisions/DECISION_LOG.md` — consult before recommending changes to a settled decision or when decision rationale matters.
- `questions/OPEN_QUESTIONS.md` — consult to identify existing unresolved questions and avoid duplicating work.
- `checkpoints/V0.2_RESEARCH_CHECKPOINT.md` — consult for the current V0.2 Research milestone, its scope, and stopping point.

Use each relevant document as authority for its own subject. If records appear to conflict, follow `DOCUMENTATION_AUTHORITY.md` and Planning's accepted project-level decisions; do not resolve conflicts by relying on this navigation list alone.

### Historical and detailed reference material

Historical implementation-phase handoffs and superseded checkpoints are for historical/reference purposes, not routine startup reading. Consult them when the current Next Action needs earlier chronology, rationale, or evidence. Likewise, consult standards, machine, firmware, and detailed source indexes when the research question requires those sources.

Historical material preserves what was known and decided at its checkpoint; it does not automatically supersede newer current-state or subject-matter authorities.
