# Machine Builder Research & Architecture
## O0.1 Checkpoint — Minimum 3D-Printer Machine Model

This directory is the durable research, architecture, terminology, ontology, standards, and machine-knowledge record for Machine Builder / Machine Development Environment (MDE).

## Current checkpoint

**Research / Architecture:** R0.1 — foundational research consolidated

**Ontology:** O0.1 — minimum 3D-printer machine/firmware model validated

**Implementation:** v0.2 development; the visual editor is currently being used as a connection-engine test harness.

The O0.1 scope is intentionally narrow. The first working Machine Builder is primarily intended to describe a 3D printer physically and semantically well enough to derive firmware representations for supported firmware families and versions.

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

The same canonical machine model also feeds the visual editor:

```text
Canonical Machine Model
        ├── Firmware representation
        └── Visual representation
```

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

The visual editor is a consumer of canonical semantics. Visual position, node size, routing, selection, zoom, and similar UI state are not machine semantics.

A visual line represents a semantic connection; it does not own the connection.

The current editor's simple Controller → Motor connection test is therefore a valid early implementation test of the canonical connection model.

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
