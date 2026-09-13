# Machine Builder Decision Log
## O0.1 Checkpoint Additions

This file records the active architectural decisions. Earlier decision history may remain below/elsewhere in the repository; the following are the O0.1 checkpoint decisions that must be treated as current.
## D-041 — Physical Machine Is Independent of Firmware

**Status:** Accepted

**Decision:** The physical/canonical machine exists independently of firmware. Firmware is an optional implementation context associated with the machine.

**Consequence:** A firmware-less machine can still be described sufficiently to generate firmware for a compatible target.
## D-042 — Firmware Version Is Part of Translation Context

**Status:** Accepted

**Decision:** Firmware family alone is not a sufficient target identity when syntax, commands, capabilities, or compatibility can vary by version. Target generation/import must support firmware version or version-range context.

**Consequence:** The same canonical machine may produce different valid representations for different versions of the same firmware family.
## D-043 — Firmware Knowledge Is Separate from Canonical Machine Semantics

**Status:** Accepted

**Decision:** Firmware commands, G/M-codes, configuration keys, macros, and firmware object-model terms remain firmware-layer representations. They map to canonical concepts but do not define them.

**Consequence:** Multiple firmware families can share the same canonical machine model.
## D-044 — Translation Must Expose Information Loss or Transformation

**Status:** Accepted

**Decision:** Translation must explicitly distinguish semantic-preserving transformations from approximation, partial transfer, unsupported information, and manual intervention.

**Consequence:** Machine Builder must not silently produce a configuration that falsely appears equivalent to the source machine.
## D-045 — Machine Component Is the Physical Source of Firmware Requirements

**Status:** Accepted

**Decision:** Physical components, their relationships, controller resources, machine functions, properties, and calibration form the information from which firmware requirements are derived.

**Consequence:** Firmware generation should not require an existing firmware configuration.
## D-046 — O0.1 Connection Scope Is Electrical

**Status:** Accepted with Conditions

**Decision:** The first ontology implementation focuses on electrical connectivity: ports, connectors, pins/terminals, wires/cables, and electrical connections.

**Consequence:** Fluid, hydraulic, fuel, general plumbing, and broader physical-interface semantics are deferred rather than forced into O0.1.
## D-047 — Function Applicability Is Contextual

**Status:** Accepted

**Decision:** Functions are semantic machine behaviors/services. Which Functions are applicable and displayed depends on machine structure, purpose, configuration, role, and view context.

**Consequence:** A printer without a heated bed does not need a fabricated Heat Bed function instance merely because other printers support it.
## D-048 — Rich Process/Operation Ontology Is Deferred

**Status:** Deferred

**Decision:** Function is in O0.1, but a complete Task/Process/Operation/Action/Procedure execution hierarchy is not required for the first firmware-oriented implementation.

**Consequence:** The ontology can later expand without blocking the initial machine/firmware model.
## D-049 — O0.1 Includes Only the Minimum Required Domain

**Status:** Accepted

**Decision:** O0.1 is intentionally optimized for 3D-printer modeling and firmware generation/conversion. Generalization is driven by real stress cases rather than abstract completeness.

**Consequence:** Water-cooled hotends, richer filament plumbing/material paths, and other fluid domains move to O0.2+.
## D-050 — Visual Builder Is a Bidirectional Canonical-Model Authoring Environment

**Status:** Accepted

**Decision:** The visual editor is a bidirectional authoring, editing, viewing, and inspection environment for the canonical machine model.

The canonical machine model remains the semantic center and authoritative structured representation of the machine.

The editor supports both directions:

```text
Canonical Machine Model
        ↓
Visual projection
        ↓
Editor
```

and:

```text
User action
     ↓
Semantic mutation
     ↓
Canonical Machine Model
     ↓
Updated visual projection
```

The editor may therefore create, modify, inspect, and remove canonical machine entities and relationships.

Visual positions, sizes, routes, selection, zoom, and other presentation state remain separate from canonical machine semantics.

**Consequence:** The visual editor is not a second machine model, but it is also not merely a read-only consumer of one. It is a primary authoring interface through which canonical machine semantics may be created and changed.
## D-051 — Provenance Is Minimum-Cross-Cutting Evidence

**Status:** Accepted

**Decision:** O0.1 provenance records source, evidence type, method, time/version/context, confidence where meaningful, and supporting derivation/evidence.

**Consequence:** Direct facts, firmware-derived facts, calculations, inference, calibration, translations, and user-authored facts remain distinguishable.
## D-052 — Calibration Does Not Replace Physical Derivation

**Status:** Accepted

**Decision:** Derived nominal values and empirically calibrated values may coexist. Differences should be visible and may produce a calibration recommendation.

**Consequence:** The model preserves both mechanical reasoning and actual working machine values.
## D-053 — Machine Component Identity Is Distinct from Hardware Definition

**Status:** Accepted

**Decision:** A Machine Component is the machine-specific semantic object representing a component occurrence within a particular Machine. Its hardware definition and catalog/product identity are separate information associated with that Machine Component.

A Machine Component may exist before its exact hardware definition is known.

**Consequence:** Machine structure can be authored before exact hardware selection or identification. Existing role, placement, connections, subsystem membership, and other relationships can survive later hardware identification or replacement.

Replace Component should preserve the Machine Component and its machine-specific relationships while replacing or enriching its hardware-definition/specification information. It must not normally be implemented as delete-old/create-new.
## D-054 — Authored Semantic Information Retains Provenance

**Status:** Accepted

**Decision:** Semantic information created through the visual editor is canonical machine information, but its provenance must identify that it was authored through the editor rather than presenting it as externally verified documentation.

At minimum, provenance must remain capable of distinguishing user-authored information from documented, observed, measured, inferred, derived, calibrated, and firmware-derived information.

**Consequence:** User-authored machine semantics can participate fully in the canonical model without losing evidence about how they were established.
## D-055 — Partial Machine Specification Is Valid

**Status:** Accepted

**Decision:** The canonical machine model permits intentionally partially specified machines.

A Machine Component or relationship may be structurally known while exact hardware identity, specifications, or other properties remain unknown or unspecified.

**Consequence:** The editor does not need to force every machine entity into a complete catalog identity before the machine can be constructed and semantically useful.
## Future Direction — Semantic Change Review

Machine Builder should eventually support a change-review mechanism in which complex visual editing operations can produce a proposed semantic change set before committing those changes to canonical model state.

Example:

```text
Added Temperature Sensor
Connected Sensor → Controller
Assigned role: temperature measurement
Hardware definition: unspecified
```

This is architectural direction only and is not an O0.2 prerequisite.
## O0.1 exit decision

The minimum ontology has survived representative 3D-printer break tests without revealing a missing fundamental concept. O0.1 therefore moves from open conceptual research to implementation-guided validation.
