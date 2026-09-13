# Machine Builder — Research & Architecture Roadmap

## Current checkpoint

### R0.1
Foundational research is sufficiently complete for the first implementation-oriented ontology checkpoint.

### O0.1
The minimum 3D-printer machine/firmware ontology has been consolidated and stress-tested against representative printer topologies.

### Implementation
The Machine Structure Editor is continuing development. Its current visual connection engine is deliberately smaller than the final machine editor and is being used to validate nodes, ports, semantic connections, compatibility, selection, mutation, and related logic before richer machine semantics are layered in.

---

# 1. Project purpose

Machine Builder is a machine-description and machine-development environment whose primary initial purpose is:

1. describe a physical 3D printer independently of firmware;
2. use that machine description to derive firmware requirements;
3. generate or convert firmware representations for supported firmware families and versions;
4. parse existing firmware back into the canonical machine model;
5. expose the same canonical model to a visual machine editor.

The canonical machine model is the semantic center.

---

# 2. O0.1 scope

O0.1 supports the machine information needed to describe ordinary and nontrivial 3D printers, including:

- mechanical structure
- moving axes and kinematics
- motors / actuators / drives
- extruders and tools
- heaters
- fans
- sensors / probes / endstops
- controllers and controller resources
- electrical connections
- machine functions and capabilities
- properties and calibration
- provenance
- optional current firmware context
- firmware capability, version, mapping, and translation context

The electrical connection model is intentionally the first physical connection domain.

## Deferred to O0.2 or later

The next planned expansion is physical description of:

- water/liquid-cooled hotends and their coolant/plumbing structure
- richer filament/material paths, including guide tubing and couplers

Later expansions may address broader fluid, hydraulic, fuel, and other non-electrical physical interfaces.

The wider research can continue as evidence, but those domains are not O0.1 implementation requirements.

---

# 3. O0.1 architectural test

O0.1 is successful when a machine can be modeled without requiring firmware to exist first, and the resulting model contains enough information to derive an implementable representation for a supported firmware target.

The reciprocal test is also required:

```text
Existing firmware
      ↓
Semantic parser
      ↓
Canonical machine model
      ↓
Different firmware target/version
      ↓
Generated representation
```

---

# 4. Minimum canonical model

```text
Machine
├── Machine Components
├── Subsystems
├── Axes / Kinematics
├── Motors / Actuators / Drives
├── Extruders / Tools
├── Heaters / Fans
├── Sensors / Probes / Endstops
├── Controller(s)
│   └── Controller Resources
├── Electrical Ports / Connectors / Pins / Wires / Connections
├── Functions / Capabilities
├── Properties / Calibration
└── Provenance
```

Firmware is associated with the machine but is not required for machine identity.

---

# 5. Firmware architecture direction

Firmware knowledge is a separate implementation-oriented information set.

```text
Canonical Machine Model
        ↓
Machine Requirements
        ↓
Target Firmware Family + Version + Hardware Context
        ↓
Firmware Knowledge / Mapping
        ↓
Generated Firmware Representation
```

Firmware mappings may be:

- one-to-one
- one-to-many
- many-to-one
- conditional
- calculated
- version-specific
- transformed
- unsupported
- manual/intervention-required

Firmware version is part of the translation context because the same firmware family can change commands, configuration syntax, semantics, capabilities, or compatibility between versions.

Firmware-specific G-code, M-code, configuration keys, macros, and object-model terms remain firmware-layer representations. They do not define canonical machine concepts.

---

# 6. Translation integrity

Translation must distinguish semantic preservation from representation differences.

A different command or configuration structure does not constitute information loss when the underlying machine meaning is preserved.

Loss or incomplete translation must be explicit. Useful result statuses include:

- exact / semantic-preserving
- transformed
- approximated
- partial
- unsupported
- manual intervention required

User-created macros and other firmware customizations are separate from the physical machine description. They may be migrated when possible, but inability to migrate a customization must not falsely imply that the physical machine itself could not be represented.

---

# 7. Visual editor integration

The visual editor is a view over canonical semantics.

```text
Canonical Connection
        ↓
Visual representation
```

Canvas coordinates, node size, routing, selection, zoom, and similar presentation state remain outside the canonical machine model.

The current connection-engine test should continue independently while the research model supplies the eventual semantic definitions behind Node/Component, Port, Connection, and Compatibility.

---

# 8. O0.1 completion checkpoint

O0.1 has been stress-tested against representative cases including:

- printer without a heated bed
- single, dual, and multi-Z
- CoreXY
- moving-bed arrangements
- multiple extruders / tools
- tool changing
- IDEX-style multiple carriages
- probe-based and sensorless homing
- multiple controller boards
- shared controller resources
- heaters controlled through intermediate electrical components
- existing firmware
- no existing firmware
- old-to-new firmware conversion
- cross-family conversion among Klipper, Marlin, and RepRapFirmware

No missing fundamental O0.1 ontology concept was identified by the break-test.

---

# 9. O0.2 — next research direction

O0.2 should expand the physical machine model without destabilizing the O0.1 foundation.

Highest-priority expansion topics:

1. water/liquid-cooled hotends and coolant/plumbing topology;
2. richer filament/material path modeling, including guide tubes and couplers;
3. richer electrical interface semantics where implementation requires them;
4. firmware knowledge-base structure for supported families and versions;
5. translator/parser implementation feedback and round-trip validation;
6. only then broader fluid/hydraulic/material domains as justified by actual machine requirements.

The broader ontology should continue to expand from real-machine needs rather than from abstract completeness.

---

# 10. Research policy after O0.1

New standards and machine examples should be researched when a new semantic domain or implementation problem appears. The project does not need to discover every potentially relevant standard before continuing development.

Stress cases remain the preferred reason to generalize the model.
