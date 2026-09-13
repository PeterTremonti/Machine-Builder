# Machine Builder Architecture Overview
## O0.1 Minimum Model

## 1. Semantic center

The canonical machine model is the semantic center of Machine Builder.

```text
Physical Machine
        ↓
Canonical Machine Model
        ↓
Firmware / Control Representation
```

Reverse interpretation is equally important:

```text
Firmware / Configuration
        ↓
Semantic Interpretation
        ↓
Canonical Machine Model
```

The visual editor consumes the same canonical model.

---

# 2. Physical machine first

The physical machine is the machine. Firmware does not create machine identity.

A machine may have:

- no firmware information yet;
- a current firmware implementation;
- historical firmware implementations;
- one or more target firmware representations.

Changing firmware does not create a new machine.

---

# 3. Minimum machine layers

## Physical / mechanical

- Machine
- Machine Component
- Subsystem
- Axis
- Joint where needed
- Link where needed
- Actuator
- Motor
- Drive
- Kinematic Relationship
- Tool / Extruder

## Electrical

- Port
- Connector
- Pin / terminal
- Wire / cable
- Electrical Connection

O0.1 intentionally treats electrical connectivity as the first physical connection domain.

## Control / sensing

- Controller
- Controller Resource
- Sensor
- Probe
- Endstop
- Heater
- Fan
- measurement/configuration properties

## Semantic behavior

- Function
- Capability
- Control Function where needed
- Homing and similar machine functions

Operation, task, process, procedure, and action remain research concepts but are not required as a large execution ontology for O0.1 firmware generation.

## Evidence

- Property
- Provenance
- derived/inferred/calibrated information

## Firmware

- Firmware Context
- Firmware Family
- Firmware Version / applicability
- Firmware Capability
- Firmware Term
- Firmware Mapping
- Translation Result

These represent implementation context, not machine identity.

---

# 4. Relationship principles

Relationships are typed semantic information.

Important examples include:

- contains / part_of
- classified_as
- has_role
- mounted_on
- connected_to
- mapped_to
- drives
- realizes / supports
- requires / uses
- measures
- derived_from
- assigned_to
- decomposes_into

Relationship multiplicity belongs to the relationship definition and may be refined by contextual constraints.

Many-to-many relationships are allowed where the machine requires them.

---

# 5. Motion principle

Axis is a machine-level motion/coordinate concept.

Axis is not synonymous with:

- Motor
- Drive
- Joint
- firmware channel

An axis may be realized by one or multiple actuators, and actuators may participate in coupled kinematic relationships.

Examples that must remain representable:

- ordinary Cartesian axis
- multi-Z
- CoreXY
- IDEX-style multiple carriages
- belt printers

---

# 6. Electrical connectivity principle

Port is a semantic interface endpoint.

Connector is a physical connector structure.

Pin/terminal is a discrete electrical contact or terminal concept used by the electrical model.

Connection is a semantic relationship between appropriate endpoints.

A physical electrical connection is normally nondirectional.

Direction belongs to relevant semantic signals/flows/interface meanings, not inherently to the physical wire itself.

A visual line is not the canonical connection.

---

# 7. Controller resource principle

A Controller Resource is a finite resource or capability supplied by a Controller that can be allocated or used by machine components/functions.

Examples include:

- stepper-driver channels
- GPIO
- ADC inputs
- PWM outputs
- timers
- UART
- CAN
- Ethernet
- related controller capabilities actually required by the supported machine

Resources remain associated with their controller. Shared-resource use is modeled through allocation/usage relationships and constraints rather than special-case machine types.

---

# 8. Function principle

Function describes meaningful machine behavior/service.

The same Function concept may be classified or associated differently depending on machine purpose and context.

The set presented to a user should be determined from machine applicability and the current view, not by duplicating Functions for every UI category.

For O0.1, examples include:

- Move Axis
- Home Axis
- Heat Hotend
- Heat Bed
- Measure Temperature
- Extrude Material
- Control Part Cooling
- Probe Surface

A machine without a heated bed simply has no applicable Heat Bed function.

---

# 9. Property and calibration principle

Properties may be:

- direct/documented
- observed/measured
- derived
- inferred
- configured
- calibrated
- unknown

A derived nominal value and a calibrated working value may coexist.

Example:

```text
nominal steps/mm = 80.0
calibrated steps/mm = 80.37
```

The difference should be visible rather than silently overwritten. A new machine may simply be flagged for calibration.

Unknown must remain distinct from absent and from not-applicable.

---

# 10. Firmware principle

The canonical model stores machine semantics.

Firmware-specific commands, configuration keys, and macros stay in the firmware layer.

The target context may include:

- firmware family
- firmware version or applicable version range
- controller hardware
- board revision where relevant
- configuration/schema version where relevant
- target capabilities

Mappings may vary between firmware versions.

---

# 11. Visual model principle

The visual model is separate from canonical semantics.

Visual state includes things such as:

- canvas position
- node size
- routing
- selection
- zoom
- collapsed/expanded state

A visual connection renders a canonical relationship.

The current visual editor is intentionally testing only a small slice of this architecture first.
