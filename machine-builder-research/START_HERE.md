# Machine Builder Research & Architecture
## O0.1 Checkpoint — Minimum 3D-Printer Machine Model

This directory is the durable research, architecture, terminology, ontology, standards, and machine-knowledge record for Machine Builder / Machine Development Environment (MDE).
## Current checkpoint

**Research / Architecture:** R0.1 — foundational research consolidated

**Ontology:** O0.1 — minimum 3D-printer machine/firmware model validated

**Implementation:** v0.2 development; the visual editor is currently being used as a connection-engine test harness and is intended to become a bidirectional authoring and inspection environment for the canonical machine model.
The O0.1 scope is intentionally narrow. The first working Machine Builder is primarily intended to describe a 3D printer physically and semantically well enough to derive firmware representations for supported firmware families and versions.

### V0.2 implementation checkpoint

The current implementation milestone is V0.2.

V0.2 is built on the O0.1 canonical machine model and does not replace or reopen the O0.1 ontology checkpoint.

V0.2 focuses on turning the visual editor into a bidirectional canonical-machine authoring and inspection environment for real 3D printers.

The V0.2 stopping point is recorded in:

`checkpoints/V0.2_RESEARCH_CHECKPOINT.md`

The implementation-facing handoff is:

`handoffs/V0.2_IMPLEMENTATION_HANDOFF.md`

Future ideas may be recorded without automatically expanding V0.2. Promotion of future concepts should wait for implementation, machine, firmware, or research evidence.
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
## Recovery order

1. `PROJECT_CONTEXT.md`
2. `RESEARCH_ROADMAP.md`
3. `architecture/ARCHITECTURE_OVERVIEW.md`
4. `ontology/TERMINOLOGY_BASELINE.md`
5. `ontology/ONTOLOGY_CURRENT.md`
6. `decisions/DECISION_LOG.md`
7. `questions/OPEN_QUESTIONS.md`
8. `handoffs/O0.1_IMPLEMENTATION_HANDOFF.md`

Use the standards, machines, and firmware research indexes when detailed evidence is required.
