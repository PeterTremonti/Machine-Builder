# Machine Builder System Boundaries

## 1. Purpose

This document defines what belongs inside the Machine Builder system, what belongs outside it, and where important interfaces occur.

The purpose is to prevent architectural drift.

Machine Builder will eventually touch many domains:

- physical hardware;
- firmware;
- controllers;
- engineering standards;
- CAD and mechanical design;
- manufacturing processes;
- safety;
- diagnostics;
- documentation;
- databases;
- visual interfaces.

Not everything related to a machine should become part of the Machine Builder canonical model.

The system should represent information needed to understand, configure, analyze, document, and operate machine architecture while preserving clear boundaries around external systems and specialized domains.

---

## 2. System-of-Interest

The primary system of interest is:

> A machine and the information necessary to describe its structure, functions, capabilities, interfaces, resources, configuration, behavior, and engineering constraints.

A machine may be:

- a 3D printer;
- CNC machine;
- router;
- laser system;
- robot;
- material handling system;
- hybrid manufacturing machine;
- test or inspection machine;
- industrial machine;
- a custom-built machine.

The architecture must not define "machine" so narrowly that the model only works for conventional Cartesian 3D printers.

---

## 3. System Context

At the highest level:

```text
                         External Engineering Knowledge
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────┐
│                    MACHINE BUILDER                      │
│                                                         │
│  Research / Ontology / Canonical Model / Analysis       │
│  Translation / Visualization / Documentation            │
│                                                         │
└─────────────────────────────────────────────────────────┘
        ▲                 ▲                 ▲
        │                 │                 │
 Physical Machine     Firmware          External Tools
        │                 │                 │
        ▼                 ▼                 ▼
 Hardware / Devices   Controller       CAD / CAM / IDE /
 Sensors / Motors     Firmware          Databases / Tools

The boundaries between these systems are interfaces, not merely folder boundaries.

4. Inside the Machine Builder Boundary

The following areas belong conceptually inside Machine Builder.

4.1 Canonical Machine Representation

Machine Builder owns the semantic representation of the machine.

This includes concepts such as:

objects;
classifications;
roles;
aspects;
properties;
relationships;
machine components;
subsystems;
functions;
capabilities;
coordinate frames;
ports;
connections;
controller resources;
state;
process information.
4.2 Engineering Context

Machine Builder may represent engineering information needed to evaluate or understand the machine.

Examples:

electrical requirements;
motion constraints;
compatibility;
calibration;
resource availability;
thermal constraints;
mechanical relationships;
process requirements;
safety requirements.
4.3 Evidence and Provenance

Machine Builder owns the representation of evidence associated with the model.

Examples:

manufacturer documentation;
measurements;
observations;
firmware configuration;
engineering calculations;
standards references;
inferred values;
reverse-engineered information.
4.4 Interpretation and Translation

Machine Builder may interpret external representations and translate them into canonical semantics.

Examples:

Firmware configuration → Canonical model
Canonical model → Firmware configuration
Catalog data → Candidate product information
Physical observation → Machine information
4.5 Visual Representation

Machine Builder includes the visual-builder application and related visualization systems.

However, visual state remains subordinate to the canonical machine model.

4.6 Engineering Evaluation

Machine Builder may eventually perform engineering evaluations based on the canonical model.

Examples include:

compatibility;
controller resource conflicts;
motion feasibility;
voltage drop;
wire sizing;
component limits;
safety-related checks.

The system provides engineering information and calculations but must not falsely imply certification or professional approval.

5. Outside the Machine Builder Boundary

Some systems remain external even though Machine Builder exchanges information with them.

5.1 Physical Reality

The actual physical machine exists outside the software.

Machine Builder may represent observations about it, but software representation is not the physical machine.

Physical machine ≠ Machine Builder model

The model is an information representation of the physical machine.

5.2 Firmware Execution

Machine Builder does not become the firmware merely because it generates or interprets firmware configuration.

The firmware remains responsible for runtime machine control.

Machine Builder
      ↓
Configuration / Mapping
      ↓
Firmware
      ↓
Controller
      ↓
Machine
5.3 Controller Hardware

Controller boards, processors, driver ICs, sensors, motors, and other physical electronics are external physical entities.

Machine Builder models them.

It does not contain or become the hardware.

5.4 CAD and Mechanical Design Systems

CAD systems remain specialized external tools.

Machine Builder may exchange:

geometry references;
coordinate information;
component metadata;
mounting relationships;
dimensions;
transforms;
machine structure.

It should not attempt to become a general-purpose CAD system.

5.5 CAM and Process Planning Systems

CAM systems may provide:

toolpaths;
operations;
work plans;
machine-specific output.

Machine Builder may represent relevant process and machine requirements, but it is not required to replace general-purpose CAM software.

5.6 Electrical CAD / Wiring Tools

Machine Builder may represent electrical topology, ports, wires, circuits, and engineering properties.

It does not automatically need to replace dedicated electrical CAD systems.

Integration should be possible where useful.

5.7 Standards Organizations

Standards are external sources of authoritative terminology and engineering requirements.

Machine Builder stores references and interpretations of relevant standards.

It does not become an authority that replaces those standards.

5.8 Vendor Catalogs

Manufacturer catalogs and databases remain external sources.

Machine Builder may import or reference catalog information, but a catalog entry does not automatically become part of a machine.

5.9 Operating System and Hardware Interfaces

The host operating system, graphics subsystem, USB stack, network stack, storage system, and similar infrastructure remain outside the semantic machine model.

6. Machine Builder Versus Firmware

This is one of the most important boundaries.

Firmware is concerned primarily with executing machine control on a particular controller architecture.

Machine Builder is concerned with representing and engineering the machine itself.

For example:

Canonical:
    Motor participates in Z-axis motion

Firmware:
    Driver 2 controls motor
    M584 Z2

The first statement describes machine semantics.

The second describes one implementation.

Another firmware might represent the same physical architecture differently.

Therefore:

Firmware-specific identifiers must not become required canonical identities.

7. Machine Builder Versus Controller

A controller is a resource provider within the machine model.

Machine Builder may represent:

processor;
motor drivers;
GPIO;
analog inputs;
timers;
communication interfaces;
buses;
expansion interfaces;
local controllers;
distributed controllers.

But the canonical model should not become a detailed simulation of the controller's electrical circuitry unless a future feature explicitly requires it.

The important abstraction is:

Machine requirement
        ↓
Controller capability / resource
        ↓
Firmware mapping

Detailed electrical implementation may remain available as additional engineering information.

8. Machine Builder Versus Hardware Catalog

The catalog and machine workspace serve different purposes.

Catalog:
    What products exist?

Machine model:
    What is installed in this machine?

Engineering evaluation:
    Is the installed component suitable here?

A catalog may contain:

NEMA-style stepper motor
Current = 1.5 A
Step angle = 1.8°

A machine model may contain:

Component:
    actual motor installed in machine
Role:
    Z-axis actuator
Source:
    machine observation

The machine component may link back to a catalog product, but the catalog must not silently populate the machine.

9. Machine Builder Versus Physical Wiring

Physical wiring is part of the machine architecture but has multiple abstraction levels.

Machine Builder may represent:

physical ports;
connector relationships;
pins;
wires;
harnesses;
sub-harnesses;
routing;
electrical characteristics;
logical signal mappings.

However, wiring diagrams, physical harness fabrication, and detailed manufacturing documentation may eventually be handled by specialized views or external tools.

The distinction is:

Semantic topology
        ≠
Visual wiring diagram
        ≠
Physical harness fabrication data

All three can describe the same underlying machine, but they are different representations.

10. Machine Builder Versus Runtime Operation

Machine Builder may represent runtime concepts such as:

state;
modes;
faults;
feedback;
measured values;
controller status;
operating conditions.

However, it is not inherently the runtime control system.

For example:

Machine Builder model:
    Drive supports a fault state

Runtime:
    Drive is currently faulted

The first is architectural information.

The second is live machine state.

A future runtime integration layer may synchronize live state with the model, but these remain conceptually distinct.

11. Configuration Versus State

Configuration and runtime state must remain separate.

Configuration

Describes intended setup.

Examples:

motor current;
axis mapping;
endstop assignment;
steps per unit;
maximum velocity;
tool assignment.
Runtime State

Describes current condition.

Examples:

motor enabled;
axis homed;
drive fault;
current temperature;
filament present;
machine stopped.

A configuration value may affect runtime behavior, but the two should not be represented as the same fact.

12. Physical Position Versus Visual Position

A physical machine has physical geometry.

The application has visual/canvas coordinates.

These must remain separate.

Physical Position
       ↓
Coordinate Frames / Transforms
       ↓
Visual Representation
       ↓
Canvas Position

Moving a node on the canvas must not accidentally move the machine component in the physical model.

Likewise, changing physical geometry must not necessarily determine a fixed visual layout.

13. Visual Interaction Versus Semantic Mutation

A user interaction may appear visually simple but cause a semantic change.

For example:

Drag port A onto port B

may produce:

Connection:
    endpoint A
    endpoint B
    domain = electrical
    compatibility = valid

The drag itself is a UI interaction.

The connection is a semantic model mutation.

These must be kept separate so that semantic operations can later occur through:

UI;
scripts;
imports;
parsers;
APIs;
automated engineering tools.
14. Research Boundary

Research is an input to architecture, not a runtime subsystem of the machine model.

Research files may contain:

standards investigations;
terminology research;
machine studies;
firmware studies;
decisions;
unresolved questions;
experimental concepts.

The canonical model should only adopt research findings once they are sufficiently understood.

Not every research hypothesis becomes a permanent concept.

This boundary prevents exploratory terminology from immediately becoming implementation commitments.

15. Ontology Boundary

The ontology defines the semantic vocabulary used by the canonical model.

It is not the entire software implementation.

For example:

Ontology:
    Motor
    Axis
    Port
    Connection
    Function

does not specify:

Python class hierarchy
database tables
Qt widgets
serialization format
file layout

Those belong to implementation architecture.

The ontology should constrain implementation meaning without dictating unnecessary implementation details.

16. Implementation Boundary

The implementation is the software realization of the current architecture.

It may contain:

Python classes;
UI components;
persistence;
validation;
rendering;
test infrastructure;
parsers;
translators;
controllers;
services.

Implementation shortcuts must not silently redefine canonical semantics.

When implementation pressure reveals an architectural problem, the issue should return to research/architecture rather than being hidden as an arbitrary special case.

17. Knowledge Graph Boundary

A future knowledge graph may complement the structured canonical model.

It may be useful for:

traversing relationships;
discovering connected information;
querying distributed knowledge;
linking standards and evidence;
representing externally sourced knowledge.

However:

The Knowledge Graph is not automatically the canonical schema.

The structured canonical model remains the primary semantic authority unless a future architectural decision explicitly changes this.

The two may eventually coexist.

Canonical Model
       ↕
Knowledge Graph
       ↕
External Knowledge
18. External Knowledge Boundary

Machine Builder may consume information from:

standards;
manuals;
firmware documentation;
manufacturer specifications;
catalogs;
user measurements;
reverse engineering;
community documentation;
other engineering sources.

External information should retain provenance.

Imported information must not lose its distinction between:

documented fact;
observation;
inference;
derived calculation;
assumption.
19. Safety Boundary

Machine Builder may support safety engineering information and analysis.

It must not represent software output as automatically constituting certification or compliance.

For example:

Machine Builder:
    Safety Function identified
    Relevant standard identified
    Required stopping behavior modeled
    Engineering evaluation = WARNING

does not mean:

Machine certified safe

Safety claims remain subject to the applicable engineering process, standards, validation, and responsible authorities.

20. Engineering Calculation Boundary

Machine Builder may perform engineering calculations where their inputs and assumptions are sufficiently defined.

For example:

Wire:
    conductor size
    material
    insulation
    length
    current
    installation conditions

may support an engineering evaluation.

The result should retain:

inputs;
assumptions;
equations or method;
source;
date;
uncertainty;
applicable standard or engineering basis.

The calculation engine should not hide uncertainty behind a simple pass/fail result.

21. User Knowledge Versus Machine Knowledge

User-provided information is evidence about the machine, not automatically universal project truth.

For example:

User observation:
    "This motor is installed on Z."

can become:

Machine Component
Role:
    Z-axis actuator

Provenance:
    user observation

The source remains important.

A later manual or measurement may revise the interpretation.

This supports correction without rewriting the history of how the original information was obtained.

22. Boundary of Automation

Machine Builder should automate transformations where the semantics are sufficiently understood.

Examples:

calculate steps/mm;
validate compatible ports;
map firmware parameters;
detect resource conflicts;
derive engineering values;
generate configuration.

It should avoid silently automating uncertain semantic conclusions.

When information cannot be established confidently, the system should preserve:

Unknown
Uncertain
Needs verification

rather than manufacturing certainty.

23. Boundary of Specialization

Machine Builder should provide a common machine architecture layer rather than attempting to replace every specialized engineering application.

A useful boundary is:

Machine Builder:
    machine architecture + semantic integration

Specialized tools:
    deep domain-specific engineering

Examples:

Machine Builder ↔ CAD
Machine Builder ↔ CAM
Machine Builder ↔ Electrical CAD
Machine Builder ↔ Firmware
Machine Builder ↔ PLC tools
Machine Builder ↔ Simulation
Machine Builder ↔ Manufacturing systems

The integration boundary should be driven by engineering value rather than by a requirement that everything become part of one application.

24. Boundary Test

When considering a new concept, feature, or data source, ask:

Question 1

Does this describe the machine, its engineering requirements, or its implementation?

If yes, it may belong inside Machine Builder.

Question 2

Is it merely a representation of information that Machine Builder already models?

If yes, it may belong to a view or translation layer rather than the canonical model.

Question 3

Is it specialized functionality better provided by another engineering system?

If yes, define an integration boundary.

Question 4

Is it external evidence about the machine?

If yes, represent the evidence and provenance rather than absorbing the external system itself.

Question 5

Would adding it create a firmware-, vendor-, machine-, or UI-specific special case?

If yes, look for the more general semantic concept before adding it.

25. Boundary Invariants

The following boundaries should remain explicit.

Physical machine
    ≠
Canonical model

Canonical model
    ≠
Visual model

Canonical model
    ≠
Firmware configuration

Catalog
    ≠
Machine component

Port
    ≠
Connector
    ≠
Pin

Connection
    ≠
Visual line

Configuration
    ≠
Runtime state

Physical topology
    ≠
Logical mapping

Function
    ≠
Procedure
    ≠
Action
    ≠
Operation
    ≠
Task

Research
    ≠
Ontology
    ≠
Implementation

Engineering evaluation
    ≠
Certification

These distinctions are architectural safeguards.

26. Summary

Machine Builder should sit between physical machines, engineering knowledge, firmware, and specialized engineering tools.

Its core responsibility is to provide a durable semantic representation of the machine and the engineering relationships required to understand and work with it.

The central boundary can be summarized as:

External Reality / External Systems
              │
              ▼
        Evidence / Interfaces
              │
              ▼
     Canonical Machine Model
              │
       ┌──────┼──────┐
       ▼      ▼      ▼
   Analysis  Views  Translation
       │      │      │
       ▼      ▼      ▼
 Engineering UI   Firmware / Tools

The architecture should remain open to integration while protecting the canonical model from becoming a mixture of firmware syntax, UI state, vendor terminology, catalog data, or specialized-tool internals.