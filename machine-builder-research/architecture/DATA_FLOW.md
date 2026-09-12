# Machine Builder Data Flow

## 1. Purpose

This document describes how information moves through Machine Builder.

The purpose is to establish a consistent architectural flow between:

- physical observations;
- external documentation;
- catalogs;
- firmware;
- the canonical machine model;
- engineering evaluation;
- visual representation;
- generated outputs;
- runtime information.

The central rule is:

> Information should move through explicit semantic boundaries rather than being copied directly between unrelated representations.

---

## 2. Core Data Flow

The primary flow is:

```text
External Evidence
      ↓
Interpretation
      ↓
Canonical Machine Model
      ↓
Engineering / Analysis
      ↓
Output Representation

A reverse flow is equally important:

Existing Machine / Firmware
      ↓
Observation / Parsing
      ↓
Interpretation
      ↓
Canonical Machine Model

The canonical model is therefore the common semantic interchange point.

3. Canonical Model as the Hub

Conceptually:

                         ┌──────────────┐
                         │    Manuals   │
                         └──────┬───────┘
                                │
                         ┌──────▼───────┐
                         │  Standards   │
                         └──────┬───────┘
                                │
┌──────────────┐         ┌──────▼───────┐         ┌───────────────┐
│ Physical     │────────▶│              │────────▶│ Firmware      │
│ Machine      │         │   Canonical  │         │ Configuration │
└──────────────┘         │    Machine   │         └───────────────┘
                         │    Model     │
┌──────────────┐         │              │────────▶┌───────────────┐
│ Hardware     │────────▶│              │         │ Engineering   │
│ Catalog      │         └──────┬───────┘         │ Evaluation    │
└──────────────┘                │                 └───────────────┘
                                │
                         ┌──────▼───────┐
                         │ Visual Model │
                         └──────────────┘

Each incoming source has its own interpretation process.

Each outgoing representation has its own translation process.

4. Evidence Acquisition

Information can enter the system through multiple channels.

Physical Observation

Examples:

identifying a motor;
tracing a wire;
measuring resistance;
measuring dimensions;
observing machine behavior;
identifying a connector;
recording a component location.
Documentation

Examples:

manuals;
datasheets;
schematics;
service documentation;
manufacturer drawings.
Firmware

Examples:

configuration files;
source code;
command syntax;
pin definitions;
controller definitions;
macros.
Standards

Examples:

terminology;
structural concepts;
engineering requirements;
measurement vocabulary;
safety concepts.
Catalogs

Examples:

manufacturer product data;
part numbers;
dimensions;
electrical ratings;
product versions.
User Knowledge

Examples:

historical machine information;
modifications;
known failures;
measured characteristics;
observations from disassembly.

All of these are evidence sources.

They should not automatically be treated as equally authoritative.

5. Evidence Normalization

Incoming information should first be converted into a form that can be evaluated.

For example:

Manufacturer document:
    "Rated current: 1.5 A"

        ↓

Normalized fact:
    property = current
    value = 1.5
    unit = A
    source = manufacturer documentation

Another example:

Firmware:
    M92 Z282.7

        ↓

Parsed information:
    firmware parameter = steps per unit
    axis = Z
    value = 282.7

        ↓

Canonical interpretation:
    Z motion scale = 282.7 steps/unit

The raw source should remain available as provenance.

6. Interpretation Layer

Interpretation transforms evidence into candidate semantic information.

The interpretation layer answers questions such as:

What machine concept does this evidence describe?
What object is being referenced?
What property is being established?
What relationship is being established?
Is the information direct or derived?
Is the interpretation certain?
Is additional evidence required?

Example:

Source:
    "Driver 2 is Z."

Interpretation:
    Controller Resource 2
        participates in
    Z-axis motion

The interpretation should preserve enough provenance to explain the conclusion.

7. Canonical Model Update

Once information has been interpreted, it may update the canonical model.

A conceptual update contains:

Object
Property / Relationship
Value
Provenance
Confidence
Validity

For example:

Object:
    Z Axis

Relationship:
    associated_controller_resource → Driver 2

Provenance:
    RRF configuration

Confidence:
    High

The canonical model may contain several pieces of evidence supporting the same fact.

Conflicting evidence must not simply overwrite earlier information without traceability.

8. Direct, Derived, and Inferred Information

The data flow must distinguish at least three cases.

Direct

Explicitly stated or directly observed.

Motor current = 1.5 A
Derived

Calculated from known information.

steps_per_mm = steps_per_revolution /
               (belt_pitch × pulley_teeth)
Inferred

A conclusion based on evidence but not directly stated.

This unidentified motor is probably the Z actuator.

These categories require different confidence and provenance behavior.

9. Unknown and Uncertain Values

Data flow must allow incomplete information.

The states are not simply:

known
unknown

Useful distinctions may eventually include:

Unknown
Not Applicable
Not Yet Investigated
Uncertain
Estimated
Derived
Observed
Documented
Verified
Conflicting

For early implementation, the exact enumeration may remain simplified.

The important architectural rule is that missing information must not silently become a fabricated value.

10. Multiple Evidence Sources

A canonical fact may have multiple sources.

Example:

Motor:
    steps_per_revolution = 200

Evidence A:
    manufacturer datasheet

Evidence B:
    measurement / test

Evidence C:
    firmware configuration

The system should be able to retain all relevant evidence.

A later source may:

confirm an existing fact;
refine it;
contradict it;
replace its confidence;
reveal that the original interpretation was wrong.

This supports iterative reverse engineering.

11. Conflict Handling

Conflicting evidence should become explicit information.

Example:

Source A:
    Motor current = 1.0 A

Source B:
    Motor current = 1.5 A

The system should not silently choose one.

Instead, it should represent:

Fact A
Fact B
Conflict
Source provenance
Resolution status

A future resolution process may establish:

Accepted value = 1.5 A
Reason = newer manufacturer revision

The original evidence should remain traceable.

12. Catalog-to-Machine Flow

Catalog information follows a different path.

Catalog Product
      ↓
Product Version
      ↓
Candidate Match
      ↓
User / System Assignment
      ↓
Machine Component

The important boundary is:

Catalog information is not automatically machine information.

For example:

Catalog:
    Motor Model X
    1.5 A
    200 steps/rev

Machine:
    Z Motor

A system may suggest that the machine motor is Model X.

That suggestion should not become an authoritative machine fact until the association is established.

13. Physical Machine to Canonical Model

A machine may be reverse-engineered through a series of observations.

Example:

Physical Motor
      ↓
Identify component
      ↓
Identify mounting position
      ↓
Identify connected wiring
      ↓
Identify controller resource
      ↓
Determine mechanical relationship
      ↓
Determine machine role
      ↓
Canonical Machine Component

The process may be iterative.

The first result may be:

Unknown Motor

Later:

Stepper Motor

Later:

Specific Manufacturer Product

Later:

Z-axis actuator

The model should support this gradual increase in knowledge.

14. Firmware-to-Canonical Flow

Firmware interpretation follows:

Firmware Source
      ↓
Parser
      ↓
Firmware Semantic Representation
      ↓
Canonical Mapping
      ↓
Canonical Machine Model

Example:

Firmware:
    X driver = 0

        ↓

Firmware meaning:
    Driver 0 controls X

        ↓

Canonical meaning:
    Controller Resource 0
        participates in
    X-axis motion

Firmware terminology remains available as source information but does not become the permanent semantic vocabulary.

15. Canonical-to-Firmware Flow

The forward direction is:

Canonical Machine Model
      ↓
Firmware Capability Check
      ↓
Firmware Mapping
      ↓
Firmware-Specific Representation
      ↓
Generated Configuration

The capability check is important.

The system must not assume that every canonical machine can be represented by every firmware.

For example:

Canonical requirement:
    4 independently controlled Z actuators

may be:

directly supported;
supported through a specific configuration;
unsupported;
supported only with additional hardware;
ambiguous.

Generation should occur only after capability and resource constraints are evaluated.

16. Firmware Mapping Is Not Simple Translation

A canonical concept and firmware term may not have a one-to-one relationship.

Examples:

Canonical Axis
    ↕
multiple firmware settings

or:

Firmware parameter
    ↕
canonical property + relationship + constraint

Therefore translation should support:

one-to-one mapping;
one-to-many mapping;
many-to-one mapping;
conditional mapping;
calculated mapping;
firmware-version-specific mapping.
17. Visual Model Data Flow

The visual builder consumes canonical information.

Conceptually:

Canonical Object
      ↓
Visual Projection
      ↓
Visual Model
      ↓
Renderer
      ↓
Canvas

The visual model may add:

node position;
node size;
layout;
visual grouping;
visibility;
routing information;
selection;
interaction state.

These values do not become machine semantics merely because they exist in the visual model.

18. Visual Interaction Back to the Model

A user interaction may cause a canonical update.

Example:

User drags:
    Port A → Port B

        ↓

Compatibility check

        ↓

Semantic connection created

        ↓

Canonical model updated

        ↓

Visual connection rendered

Another interaction:

User edits:
    Motor current = 1.5 A

        ↓

Property mutation

        ↓

Provenance:
    user-provided value

        ↓

Engineering evaluations rerun

The UI is therefore one interface to the canonical model, not a separate authoritative database.

19. Compatibility Data Flow

Compatibility is evaluated from semantics.

Port A
   +
Port B
   ↓
Compatibility Engine
   ↓
Compatible
Incompatible
Conditional
Unknown

The result may depend on:

domain;
direction;
voltage;
current;
protocol;
signal type;
mechanical interface;
material;
constraints;
firmware support.

Visual color is an output of the evaluation.

Example:

Semantic result:
    Compatible

Visual result:
    connection rendered as valid

The color itself is not the compatibility state.

20. Connection Data Flow

A connection may have several associated representations.

Semantic Connection
      │
      ├── Physical topology
      │
      ├── Logical mapping
      │
      ├── Electrical properties
      │
      └── Visual representation

For example:

Physical:
    wire connects connector pin A to connector pin B

Logical:
    signal "heater_enable" is mapped across the connection

Visual:
    line rendered between nodes

These are related but not identical.

21. Control Data Flow

A simplified control path is:

Command / Setpoint
       ↓
Control Function
       ↓
Controller Resource
       ↓
Drive / Actuator
       ↓
Physical Machine
       ↓
Sensor
       ↓
Measurement Result
       ↓
Feedback
       ↓
Control Function

The same physical information may branch.

For example:

Temperature Measurement
        ├──→ Heater Control
        ├──→ Display
        ├──→ Logging
        ├──→ Diagnostics
        └──→ Safety Logic

The architecture must support such fan-out rather than assuming a single consumer.

22. Process Data Flow

A process-oriented machine may follow:

Task
  ↓
Process
  ↓
Operation
  ↓
Action
  ↓
Machine Functions
  ↓
Physical Effects
  ↓
Measurement / Result

For example:

Task:
    Print Part

Process:
    Additive Manufacturing

Operation:
    Extrude Material

Action:
    Advance Filament

Machine Function:
    Feed Material

Physical Effect:
    Filament moves

The same machine function can participate in many different processes.

23. Safety Data Flow

Safety information follows a separate but connected path.

Machine
   ↓
Hazard Identification
   ↓
Risk Assessment
   ↓
Risk Reduction Requirement
   ↓
Safety Function
   ↓
Safety-Related Implementation
   ↓
Validation

Safety information can reference canonical components and functions.

Example:

Guard
   ↓
Interlock
   ↓
Safety Signal
   ↓
Safety Function
   ↓
Motion Stop

The safety architecture may reuse machine objects but must retain its own engineering context and evidence.

24. Engineering Evaluation Data Flow

Engineering evaluation operates on canonical information.

Canonical Model
      ↓
Relevant Properties
      ↓
Constraints / Standards
      ↓
Calculation / Rule
      ↓
Evaluation Result
      ↓
Diagnostic / Recommendation

Example:

Motor:
    current = 2.0 A

Driver:
    maximum current = 1.5 A

        ↓

Compatibility Evaluation

        ↓

INVALID

Another example:

Wire:
    length = 2 m
    current = 5 A
    conductor size = ...
    installation = ...

        ↓

Voltage Drop / Ampacity Evaluation

        ↓

WARNING

Results should preserve the assumptions and evidence used.

25. Runtime Data Flow

A future runtime integration may look like:

Physical Machine
      ↓
Controller / Firmware
      ↓
Runtime Telemetry
      ↓
Runtime Interpretation
      ↓
Canonical Runtime State
      ↓
UI / Diagnostics / Logging

Runtime state should not overwrite configuration.

For example:

Configuration:
    Maximum temperature = 250 °C

Runtime state:
    Current temperature = 205 °C

Both may coexist.

26. Calibration Data Flow

Calibration creates a particularly important relationship between observation and configuration.

A simplified flow is:

Physical Measurement
      ↓
Measurement Result
      ↓
Calibration Analysis
      ↓
Derived Parameter
      ↓
Configuration Candidate
      ↓
User / System Approval
      ↓
Canonical Configuration

For example:

Measured travel
      ↓
Observed discrepancy
      ↓
Motion scale calculation
      ↓
Updated steps/unit

The calibration process should preserve:

original measurement;
method;
calculated result;
resulting parameter;
date;
equipment;
uncertainty where applicable.
27. Change Propagation

Changing canonical information may affect several downstream representations.

Example:

Motor current changed
        ↓
Canonical property updated
        ├──→ Compatibility checks
        ├──→ Driver configuration
        ├──→ Electrical evaluation
        ├──→ Documentation
        └──→ Visual warnings

The system should eventually support dependency tracking so that affected results can be invalidated or recalculated.

A stale derived value should not silently remain authoritative.

28. Version-Sensitive Data Flow

Machine information may depend on versions.

Examples:

Machine hardware version
Firmware version
Controller revision
Product version
Standard edition
Configuration version

Therefore a fact may need contextual applicability.

For example:

Property:
    firmware parameter meaning

Applies to:
    RepRapFirmware 3.5.x

A different firmware version may interpret the same parameter differently.

Version information belongs in the provenance and applicability context where relevant.

29. Provenance Flow

Provenance should travel with information when practical.

Conceptually:

Source
  ↓
Observation / Fact
  ↓
Interpretation
  ↓
Canonical Property / Relationship
  ↓
Derived Result
  ↓
Engineering Evaluation
  ↓
Output

A final result should remain traceable to the information on which it depends.

Example:

Generated firmware value
      ↓
Canonical property
      ↓
Derived calculation
      ↓
Motor specification
      ↓
Manufacturer document

This allows the system to answer:

Why does Machine Builder believe this value?

30. Data Lineage

Important derived information should retain lineage.

Example:

Z steps/mm
   ↓
derived from
   ├── motor steps/revolution
   ├── microstepping
   ├── leadscrew pitch
   └── mechanical ratio

Changing one input should make the dependency visible.

This enables future features such as:

recalculation;
stale-data detection;
audit trails;
engineering explanations;
change impact analysis.
31. Import Flow

External structured data may enter through importers.

Conceptually:

External File
      ↓
Importer
      ↓
Raw Parsed Representation
      ↓
Semantic Interpretation
      ↓
Validation
      ↓
Canonical Model Changes

Examples:

firmware configuration;
BOM;
CAD metadata;
hardware catalog;
machine description;
wiring information.

The importer should not bypass semantic validation merely because the input is machine-readable.

32. Export Flow

Export follows the reverse direction:

Canonical Model
      ↓
Validation
      ↓
Target Representation
      ↓
Serializer / Generator
      ↓
External File / System

Examples:

firmware configuration;
wiring documentation;
machine report;
BOM;
maintenance documentation;
machine description.

Export should identify unsupported or unresolved information rather than silently dropping important semantics.

33. Handoff Flow Between Research and Implementation

Research findings move toward implementation through explicit handoffs.

Research
   ↓
Concept / Decision
   ↓
Architecture or Ontology Update
   ↓
Implementation Handoff
   ↓
Implementation
   ↓
Observed Result
   ↓
Research Feedback

An implementation discovery may expose:

missing concept;
incorrect distinction;
impossible constraint;
terminology conflict;
useful new relationship.

That discovery returns to the research stream.

34. Error and Uncertainty Flow

Errors should be represented as information rather than hidden.

Potential states include:

Invalid
Unknown
Uncertain
Conflicting
Unsupported
Insufficient Evidence
Needs Verification

These states can propagate into downstream results.

Example:

Motor current = Unknown
        ↓
Driver compatibility = Unknown
        ↓
Firmware generation = Needs Verification

The system should avoid presenting the final output as valid merely because the missing information was never checked.

35. Data Flow Invariants

The following rules should remain stable:

The canonical machine model is the semantic hub.
External evidence enters through interpretation.
Raw evidence should remain traceable.
Direct, derived, and inferred information must remain distinguishable.
Unknown information must remain representable.
Conflicting evidence should not be silently discarded.
Catalog information does not automatically become machine information.
Firmware terminology does not automatically become canonical terminology.
Visual state is not semantic authority.
Engineering results should retain their inputs and assumptions.
Runtime state does not overwrite configuration.
Version-sensitive information must retain applicability context.
Derived values should retain lineage.
Changing source information should eventually invalidate affected derived results.
Export should not silently discard unresolved important information.
36. Simplified End-to-End Example

Consider a machine containing a stepper motor used for Z motion.

Step 1 — Observation
Physical observation:
    motor is mechanically connected to Z mechanism
Step 2 — Documentation
Motor datasheet:
    200 steps/revolution
Step 3 — Firmware
Firmware:
    Driver 2 assigned to Z
Step 4 — Interpretation
Motor:
    classification = stepper motor

Role:
    Z-axis actuator

Relationship:
    motor participates in Z motion

Controller resource:
    Driver 2
Step 5 — Derived Information

Given:

200 steps/revolution
16 microsteps
2 mm/revolution

the system may derive:

steps/mm = 1600

with the calculation stored as provenance.

Step 6 — Engineering Evaluation

The system checks:

Driver current capability
Motor current requirement

and produces:

PASS

or another result depending on the evidence.

Step 7 — Firmware Generation

The canonical result is translated into the selected firmware's syntax.

Step 8 — Visual Representation

The visual builder displays:

Z Axis
   │
   └── Z Motor
          │
          └── Driver 2

The visual arrangement is presentation state, not canonical semantics.

37. Long-Term Data Flow

The eventual system is expected to support a continuous lifecycle:

Design
  ↓
Build
  ↓
Document
  ↓
Configure
  ↓
Validate
  ↓
Operate
  ↓
Measure
  ↓
Diagnose
  ↓
Calibrate
  ↓
Modify
  ↓
Reconfigure
  ↓
Document

The canonical machine model provides continuity across these stages.

This is one of the reasons the project must not be designed as only a firmware configuration generator.

38. Summary

The architectural data flow is centered on semantic interpretation and a canonical machine model.

The core pattern is:

Evidence
   ↓
Interpretation
   ↓
Canonical Model
   ↓
Evaluation
   ↓
Representation / Action

with feedback:

Observed Result
      ↓
Evidence
      ↓
Updated Model

This creates a system in which physical machines, firmware, catalogs, standards, engineering calculations, and visual representations can interact without becoming conflated.

The canonical model is the common semantic boundary through which these systems exchange meaning.