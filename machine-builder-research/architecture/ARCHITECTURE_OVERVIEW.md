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

The visual editor is a bidirectional authoring and inspection environment over the same canonical model. It is not a second machine model and is not merely a read-only consumer.

```text
            Canonical Machine Model
                    ↕
          Semantic / Model Boundary
                    ↕
             Visual Machine Editor
```

The editor may project canonical information into visual representations and may author or modify canonical semantic information through user actions.

```text
Canonical Machine Model
        ↓
Visual projection
        ↓
Editor
```

```text
User action
     ↓
Semantic edit / mutation
     ↓
Canonical Machine Model
     ↓
Updated visual representation
```

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

Semantic relationships may be created, modified, inspected, or removed through the visual editor. They are canonical machine information; the editor is an authoring interface to them, not their semantic owner.

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

A visual line represents or edits the canonical connection; it is not the canonical connection itself.

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

The visual editor may author and edit Function-related canonical information when supported. Such semantic edits update the canonical machine model and are then projected back into the visual representation.

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
# 11. Canonical model / visual model boundary

The architecture distinguishes three things:

```text
Canonical semantic objects
        ↓
Visual representations
        ↓
Visual presentation state
```

Canonical semantic objects include entities and relationships such as:

- Machine Components
- Subsystems
- Ports
- Connectors / pins / terminals
- Connections
- Functions
- Capabilities
- Controller resources and assignments
- Properties
- Calibration information
- other canonical relationships

Visual representations are editor objects that represent or expose those canonical entities.

Visual presentation state includes:

- canvas position
- node size
- routing
- selection
- zoom
- collapsed/expanded state
- other UI-only state

Presentation state must not silently become canonical machine semantics.

The distinction is therefore:

```text
Canonical Connection
        ↓
Visual representation
        ↓
Rendered line
```

and also:

```text
User edits visual representation
        ↓
semantic mutation
        ↓
Canonical Connection
        ↓
updated visual representation
```

The visual editor may create, modify, inspect, and remove canonical semantic entities and relationships, but visual geometry itself is never the authoritative source of machine meaning.

---
# 12. Visual editor modes

The visual editor supports two conceptual operating modes.

### Viewing mode

Viewing mode is primarily intended for:

- inspection
- navigation
- filtering
- relationship exploration
- semantic inspection
- reviewing machine structure

Viewing mode operates on the canonical machine model and does not require a separate read-only machine representation.

### Editing mode

Editing mode permits authoring and changing canonical machine semantics.

Examples include:

- creating Machine Components
- assigning machine roles
- creating Ports
- creating Connections
- assigning Controller Resources
- adding Functions or Capabilities
- editing Properties
- changing relationships
- identifying or replacing hardware definitions

Semantic mutations made by Editing mode update the canonical machine model and are then reflected in the visual projection.

The visual editor may eventually support an explicit change-review/confirmation mechanism in which a collection of semantic edits is represented as a change set before commit. That mechanism is an architectural direction and is not required for the first V0.2 implementation.

---
# 13. Partially specified machines

The canonical machine model permits intentional partial specification.

A machine may contain a valid Machine Component even when its exact hardware definition is unknown.

For example:

```text
Machine Component:
  role: temperature measurement
  physical placement: known
  connections: known
  hardware definition: unspecified
  specifications: unknown
```

Unknown / unspecified information is distinct from:

- absent
- not applicable
- known but uncertain
- inferred
- derived

The editor must not force fake values merely because a UI form or implementation class would prefer every field to be populated.

This permits machine structure and intended relationships to be authored before exact hardware purchasing or identification has occurred.

---
# 14. Machine Component and hardware definition

A Machine Component represents the machine-specific semantic occurrence.

A Catalog Product represents an external reusable product definition.

A hardware definition may reference or derive from a Catalog Product or Product Version and may carry hardware specifications, identifiers, manufacturer information, and related provenance.

Therefore:

```text
Machine Component
      ↕
hardware definition /
product identification
      ↕
Catalog Product / Product Version
```

The Machine Component may exist while the hardware-definition layer is unspecified.

Do not use Component Instance as a competing canonical synonym for Machine Component unless later research establishes a specific semantic distinction that Machine Component cannot express.

### Replace Component

Replacing hardware must not normally be modeled as deletion followed by creation of a different Machine Component.

Instead:

```text
existing Machine Component
        ↓
retain identity and machine relationships
        ↓
replace / enrich hardware definition
        ↓
resulting Machine Component
```

The operation should preserve existing semantic relationships such as:

- machine role
- physical placement
- subsystem membership
- connections
- relevant ports/interfaces
- Functions
- other machine-specific relationships

while allowing hardware-definition information and associated properties/specifications to change.

The exact identity semantics of hardware-definition replacement remain implementation-detail work, but the canonical distinction between Machine Component and hardware definition is architectural.

---
# 15. Provenance of user-authored semantics

Canonical information authored through the visual editor is canonical machine information, but its provenance must identify that it was authored through the editor rather than presenting it as externally verified documentation.

At minimum, provenance must remain capable of distinguishing user-authored information from documented, observed, measured, inferred, derived, calibrated, and firmware-derived information.

For example:

```text
source: user
evidence type: authored
method: visual editor
context: editor session
```

---
# 16. Future semantic change review

The architecture should eventually permit editor operations to produce a semantic change set before commit.

Example:

```text
Added Temperature Sensor
Connected Sensor → Controller
Assigned role: temperature measurement
Hardware definition: unspecified
```

The user may eventually review and confirm this set before it becomes committed canonical model state.

This is a future architectural direction, not an immediate V0.2 implementation requirement.

The important invariant is:

```text
Canonical Machine Model
    = semantic truth /
      authoritative structured representation

Visual Editor
    = bidirectional authoring,
      editing, viewing, and inspection environment

Visual State
    = presentation only
```
