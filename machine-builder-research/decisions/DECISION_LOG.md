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

## D-050 — Visual Builder Consumes Canonical Semantics

**Status:** Accepted

**Decision:** The visual editor is a view and editing interface over canonical machine semantics. Visual positions, sizes, routes, selection, and zoom are separate from machine semantics.

**Consequence:** The current connection-engine prototype is a valid implementation test of canonical Port/Connection semantics rather than a separate machine model.

## D-051 — Provenance Is Minimum-Cross-Cutting Evidence

**Status:** Accepted

**Decision:** O0.1 provenance records source, evidence type, method, time/version/context, confidence where meaningful, and supporting derivation/evidence.

**Consequence:** Direct facts, firmware-derived facts, calculations, inference, calibration, and translations remain distinguishable.

## D-052 — Calibration Does Not Replace Physical Derivation

**Status:** Accepted

**Decision:** Derived nominal values and empirically calibrated values may coexist. Differences should be visible and may produce a calibration recommendation.

**Consequence:** The model preserves both mechanical reasoning and actual working machine values.

## O0.1 exit decision

The minimum ontology has survived representative 3D-printer break tests without revealing a missing fundamental concept. O0.1 therefore moves from open conceptual research to implementation-guided validation.
