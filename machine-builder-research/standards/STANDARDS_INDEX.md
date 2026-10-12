# Machine Builder Standards Index

## 1. Purpose

This document is the working index of standards and standards-related sources that have materially influenced Machine Builder research.

It is not intended to be a complete list of every standard that could possibly apply to machine development.

The project uses a targeted standards strategy:

```text
New semantic domain
        ↓
Targeted standards scan
        ↓
Relevant standards identified
        ↓
Useful distinctions / requirements extracted
        ↓
Ontology or architecture updated if justified

The standards themselves remain external authoritative sources.

Machine Builder records their relevance, terminology, evidence, and applicability rather than attempting to reproduce the standards.

2. Standards Research Principles
2.1 Standards Are Evidence, Not Automatic Ontology

A standard may provide:

terminology;
definitions;
engineering distinctions;
structural models;
requirements;
methods;
safety concepts.

Machine Builder does not automatically adopt every concept in a standard.

A distinction should be incorporated when it is useful to the project's semantic model.

2.2 Standards Do Not Override Machine Evidence Automatically

A standard describes a domain or establishes requirements.

A particular machine may still contain:

nonconforming behavior;
proprietary structures;
undocumented modifications;
obsolete implementations;
intentional deviations.

The canonical model should represent what the machine actually is while retaining the applicable standard context.

2.3 Standard Versions Matter

Standards references should retain, where relevant:

organization;
standard number;
edition;
publication date;
amendment;
current status;
applicability.

A reference to a standard without edition/version context may be insufficient for engineering evaluation.

2.4 Standards Should Not Become Boolean Properties

Avoid representations such as:

ISO 13849 compliant = true

Instead preserve:

Applicable standard
Edition
Requirement
Evidence
Evaluation
Validation
Status

A standards reference and an engineering compliance determination are different things.

3. Standards Priority Tiers

The current working tiers are:

Tier 1 — Core Architectural Influence

Standards that materially affect the canonical architecture or major ontology distinctions.

Tier 2 — Important Domain Vocabulary / Constraints

Standards that provide strong domain-specific terminology or requirements.

Tier 3 — Supporting / Targeted Reference

Standards useful for particular features or future domains.

Tier 4 — Investigate When Needed

Standards that may become relevant later but should not currently affect architecture.

4. Systems Engineering and Architecture
ISO/IEC/IEEE 15288:2023

Area: Systems engineering life cycle processes

Relevance: Tier 1

Important Contribution

Provides systems-engineering lifecycle terminology and a useful basis for distinguishing:

system;
stakeholder needs;
requirements;
architecture;
implementation;
verification;
validation;
lifecycle processes.
Machine Builder Use

Supports the separation between:

Requirements
Architecture
Implementation
Verification
Validation

and helps prevent the visual builder or firmware generator from being mistaken for the complete machine-development system.

Important Boundary

Machine Builder should not copy the entire lifecycle framework into its ontology.

It provides architectural context rather than a complete application schema.

ISO/IEC/IEEE 42010:2022

Area: Architecture descriptions

Relevance: Tier 1

Important Contribution

Provides concepts related to:

stakeholders;
concerns;
viewpoints;
views;
architecture descriptions;
model kinds.
Machine Builder Use

Strong support for the distinction between:

Canonical Machine Model
        ↓
Different Engineering Views

and therefore supports the architectural separation between:

canonical semantics;
physical view;
functional view;
electrical view;
safety view;
visual builder view.
Important Insight

A view is not necessarily the underlying system itself.

This aligns closely with the project's canonical-model/visual-model distinction.

5. Structuring and Engineering Aspects
IEC 81346-1

Area: Industrial systems, installations and equipment — structuring principles and reference designations

Relevance: Tier 1

Important Contribution

Provides principles for structuring systems according to different aspects.

Machine Builder Use

Strong influence on:

Aspect;
structural decomposition;
multiple engineering views;
separating different ways of organizing the same system.
Important Distinction

IEC 81346 terminology must not be copied uncritically into Machine Builder.

In particular, IEC 81346's use of concepts such as inherent function should not be assumed to mean the same thing as the project's Function concept.

IEC 81346-2

Area: Classification of objects and codes for reference designations

Relevance: Tier 1 / Tier 2

Important Contribution

Provides structured classification and reference-designation concepts.

Machine Builder Use

Supports the distinction between:

Object
Classification
Aspect
Reference Designation

and informs future identification systems.

IEC 81346-14:2026

Area: Structuring principles for industrial systems, installations and equipment; application to manufacturing and processing systems

Relevance: Tier 1

Important Contribution

Particularly relevant to Machine Builder because it applies the 81346 structuring approach to manufacturing and processing systems.

Machine Builder Use

Useful for:

manufacturing-system decomposition;
structuring;
aspects;
equipment relationships;
industrial machine architecture.
Important Note

This standard should be treated as a current reference and its 2026 publication context retained in the research record.

6. Machine Tool and Coordinate Vocabulary
ISO 841

Area: Numerical control of machines — axis and motion nomenclature

Relevance: Tier 1

Important Contribution

Provides vocabulary and conventions for machine axes and motion.

Machine Builder Use

Supports the distinction:

Axis
≠
Motor

and provides machine-motion terminology for CNC and related equipment.

ISO 230 Series

Area: Test code for machine tools

Relevance: Tier 2

Important Contribution

Provides machine-tool accuracy, geometry, testing, and performance terminology.

Machine Builder Use

Potentially relevant to:

machine geometry;
positioning;
motion accuracy;
calibration;
verification;
machine performance.
Current Scope

Useful primarily as a future engineering/evaluation reference rather than a v0 ontology dependency.

ISO 2806

Area: Industrial automation systems / machine tools — vocabulary relating to numerically controlled machines

Relevance: Tier 2

Important Contribution

Supports CNC and numerical-control terminology.

Machine Builder Use

Useful when extending the ontology beyond additive machines.

7. Robotics and Mechanical Motion
ISO 8373

Area: Robotics — vocabulary

Relevance: Tier 1

Important Contribution

Provides vocabulary including concepts related to:

robot;
manipulator;
joint;
link;
actuator;
motion;
task.
Machine Builder Use

Strong evidence for keeping:

Joint
Link
Actuator
Axis
Task

distinct.

Important Boundary

Robotics terminology should not automatically define all machine-builder concepts.

The standard is evidence for distinctions, not a complete ontology for all machines.

ISO 9787

Area: Robotics — coordinate systems and motion

Relevance: Tier 1

Important Contribution

Supports formal treatment of:

coordinate systems;
frames;
robot motion;
reference relationships.
Machine Builder Use

Strengthens the case for:

CoordinateFrame
Transform

as distinct concepts.

8. Additive Manufacturing
ISO/ASTM 52900

Area: Additive manufacturing — general principles and vocabulary

Relevance: Tier 2

Important Contribution

Provides additive-manufacturing terminology and process vocabulary.

Machine Builder Use

Useful for:

additive manufacturing classification;
process terminology;
material/process terminology;
machine capabilities.
Important Boundary

It should not define the entire Machine Builder ontology.

ISO/ASTM 52902

Area: Additive manufacturing — system performance / capability evaluation

Relevance: Tier 2

Important Contribution

Provides concepts relevant to evaluating additive-manufacturing machine capability.

Machine Builder Use

Potential future support for:

capability evaluation;
machine characterization;
process performance;
engineering evaluation.
ISO/ASTM 52903-2

Area: Additive manufacturing / material extrusion equipment

Relevance: Tier 2

Important Contribution

Provides terminology and requirements relevant to material-extrusion equipment.

Machine Builder Use

Useful for printer-specific terminology while maintaining a broader machine-independent architecture.

ISO 17295

Area: Additive manufacturing — coordinates, orientations, and related conventions

Relevance: Tier 2

Important Contribution

Supports machine/build coordinate and orientation concepts.

Machine Builder Use

Relevant to:

coordinate frames;
build orientation;
tool/work relationships;
additive-specific coordinate semantics.
9. Numerical Control and Manufacturing Process
ISO 14649 / STEP-NC

Area: Data model for computerized numerical controllers and manufacturing process planning

Relevance: Tier 1 / Tier 2

Important Contribution

Provides important distinctions among:

process;
workplan;
workingstep;
operation;
machining context.
Machine Builder Use

Strong evidence that:

Task
Process
Operation
Action
Procedure

should not automatically be collapsed into one concept.

Important Boundary

Machine Builder is not intended to become a complete CAM/STEP-NC replacement.

STEP-NC is primarily useful as architectural and terminology evidence.

10. PLC and Control Execution
IEC 61131-1

Area: Programmable controllers — general information

Relevance: Tier 2

Important Contribution

Provides context for PLC/controller terminology and architecture.

Machine Builder Use

Useful when modeling:

controllers;
programs;
control resources;
execution concepts.
IEC 61131-3

Area: Programmable controllers — programming languages

Relevance: Tier 2

Important Contribution

Provides software execution concepts including:

programs;
tasks;
functions;
function blocks;
actions;
program organization units.
Important Warning

IEC 61131-3 uses terms such as Function, Task, and Action in a particular software-execution context.

Machine Builder must not import those meanings wholesale into the canonical machine ontology.

Machine Builder Use

The standard is evidence that these terms have domain-specific meanings and therefore reinforces the need to define Machine Builder terminology explicitly.

11. Drives and Motion Control
IEC 61800-2

Area: Adjustable speed electrical power drive systems — general requirements

Relevance: Tier 2

Machine Builder Use

Useful for:

drive-system scope;
ratings;
drive architecture;
electrical/motion relationships.
IEC 61800-5-1

Area: Adjustable speed electrical power drive systems — safety requirements

Relevance: Tier 2

Machine Builder Use

Useful when modeling drive-system safety and electrical constraints.

IEC 61800-7

Area: Adjustable speed electrical power drive systems — generic interface and use of profiles

Relevance: Tier 1 / Tier 2

Important Contribution

Provides concepts for:

drive behavior;
profiles;
parameterization;
state/control interfaces.
Machine Builder Use

Supports separating:

Motor
Drive
Controller
Runtime State
Control Interface
CiA 402

Area: CANopen device profile for drives and motion control

Relevance: Tier 2

Important Contribution

Provides a well-established drive profile including:

state machine;
control word;
status word;
operating modes;
position;
velocity;
fault handling.
Machine Builder Use

Important evidence for the principle that:

A drive is not merely a command-to-motor mapping.

It has its own control state and operational semantics.

12. Measurement and Metrology
JCGM 200 — International Vocabulary of Metrology (VIM)

Area: Metrology vocabulary

Relevance: Tier 1

Important Contribution

Provides vocabulary for:

quantity;
measurement;
measurand;
measurement result;
uncertainty;
measurement procedure.
Machine Builder Use

Strong foundation for distinguishing:

Sensor
Measurand
Measurement
Measurement Result
Feedback
Important Boundary

Machine Builder should use the metrology terminology consistently where applicable rather than inventing overlapping meanings.

13. Safety
ISO 12100:2010

Area: Safety of machinery — general principles for design — risk assessment and risk reduction

Relevance: Tier 1

Important Contribution

Provides the foundational machinery-safety framework involving:

hazards;
risk assessment;
risk reduction;
inherently safe design;
safeguarding;
information for use.
Machine Builder Use

Supports the architecture:

Hazard
↓
Risk
↓
Risk Reduction
↓
Safety Function / Implementation
Current Status Note

The project should verify the applicable current edition/status whenever safety research is frozen for implementation.

ISO 13849-1:2023

Area: Safety of machinery — safety-related parts of control systems

Relevance: Tier 1

Important Contribution

Provides concepts concerning:

safety-related control systems;
safety functions;
architectures/categories;
performance levels;
safety-related parts.
Machine Builder Use

Supports explicit Safety Function and Safety-Related Control Implementation modeling.

ISO 13849-2:2012

Area: Safety of machinery — validation of safety-related parts of control systems

Relevance: Tier 1

Important Contribution

Provides validation concepts for safety-related control systems.

Machine Builder Use

Relevant to future representation of:

validation methods;
evidence;
test results;
validation status.
Current Status Note

Revision status should be checked when this becomes implementation-relevant.

ISO/TR 13849-3:2026

Area: Safety-related parts of control systems — calculation/support methods

Relevance: Tier 3

Important Contribution

Relevant to future safety calculation and reliability/PFH-oriented analysis.

Machine Builder Use

Future engineering evaluation layer.

Not a v0 semantic dependency.

IEC 62061:2021 + Amendments

Area: Safety of machinery — functional safety of safety-related control systems

Relevance: Tier 1

Important Contribution

Provides machinery functional-safety architecture and validation concepts.

Machine Builder Use

Important companion to ISO 13849 for:

Safety Functions;
safety-related control systems;
validation;
functional safety engineering.
Current Version Context

Research should preserve the applicable amendment/version context rather than treating "IEC 62061" as timeless.

ISO 13850:2015

Area: Emergency stop function

Relevance: Tier 2

Important Contribution

Provides emergency-stop concepts and requirements.

Machine Builder Use

Supports modeling Emergency Stop as a safety function rather than merely a button or input.

ISO 14118:2017

Area: Safety of machinery — prevention of unexpected start-up

Relevance: Tier 2

Important Contribution

Relevant to:

restart prevention;
isolation;
stored energy;
unexpected startup.
Machine Builder Use

Useful for Safety Function modeling.

ISO 14119:2024

Area: Interlocking devices associated with guards

Relevance: Tier 2

Important Contribution

Relevant to:

guards;
interlocks;
position monitoring;
safety-related control behavior.
Machine Builder Use

Supports the relationship:

Guard
↓
Interlock
↓
Safety Function
ISO 14120:2015

Area: Guards — general requirements

Relevance: Tier 2

Important Contribution

Provides guard-related engineering requirements.

Machine Builder Use

Supports Guard as a meaningful safety object rather than simply a visual object.

14. Product, Assembly, and Information Modeling
ISO 10303 / STEP

Area: Product data representation and exchange

Relevance: Tier 1

Important Contribution

STEP provides extensive concepts for representing:

products;
product definitions;
versions;
assemblies;
geometry;
properties;
relationships.
Machine Builder Use

Strong architectural evidence for distinguishing:

Catalog Product
Product Version
Machine Component / Occurrence

and for preserving structured product information.

Important Boundary

Machine Builder does not need to implement STEP in full.

STEP is primarily an architectural precedent and potential future integration target.

15. Industrial Information Architecture
ISO 15926

Area: Integration of lifecycle data for process plants

Relevance: Tier 2 / Tier 3

Important Contribution

Provides extensive experience with:

lifecycle information;
classes;
relationships;
temporal information;
engineering data integration.
Machine Builder Use

Useful as architectural evidence for:

persistent engineering information;
lifecycle relationships;
semantic integration.
Important Boundary

Machine Builder should not adopt ISO 15926 wholesale.

The domain is considerably broader and more process-industry-specific than the immediate project needs.

16. Industrial Interoperability and Information Modeling
OPC UA Information Modeling

Area: Industrial interoperability and information modeling

Relevance: Tier 2

Important Contribution

Useful information-modeling patterns include:

Objects;
Variables;
Methods;
typed References;
hierarchical organization;
reusable information models.
Machine Builder Use

Useful architectural evidence for machine-state and interoperability models.

Related Domains

OPC UA companion models for CNC, robotics, and other industrial systems may become useful during future machine/industrial integration work.

17. Engineering Diagram and Connectivity Semantics
IEC 81714-2

Area: Design of graphical symbols and connection-related representation for technical products

Relevance: Tier 1 / Tier 2

Important Contribution

Important precedent for:

connection nodes;
ports/interfaces;
technical-system representations;
connectivity across domains.
Machine Builder Use

Supports treating connection/interface endpoints as meaningful semantic entities rather than relying solely on drawing geometry.

18. Fluid Power and Flow Representation
ISO 1219 Series

Area: Fluid power systems — graphical symbols and circuit diagrams

Relevance: Tier 3

Important Contribution

Useful for:

flow paths;
fluid connections;
valves;
actuators;
fluid-power diagram semantics.
Machine Builder Use

Useful evidence for future fluid/material path modeling.

Current Scope

No universal Flow ontology should be created solely because fluid-power diagrams use flow concepts.

19. Additional Domain References

The following standards or standard families may become relevant as the project expands.

Electrical Equipment of Machines
IEC 60204-1

Area: Safety of machinery — electrical equipment of machines

Relevance: Tier 1 / Tier 2

Potential Contributions
electrical supply;
overcurrent protection;
protective bonding;
control circuits;
emergency-stop circuits;
documentation;
wiring considerations.
Machine Builder Use

Potential future engineering evaluation layer.

Wire sizing, voltage drop, protective devices, conductor selection, and termination constraints should not be reduced to a simple voltage/current calculation.

Robotics Interoperability

Additional robot-specific standards and information models may become relevant if robot architectures become a major supported domain.

Current approach:

use ISO 8373 and ISO 9787 as foundational references;
perform targeted research when detailed robot modeling begins.
CNC Interoperability

OPC UA CNC models and related industrial information models may become useful when CNC interoperability becomes an implementation target.

20. Standards by Ontology Domain
Domain	Important References
Systems Engineering	ISO/IEC/IEEE 15288
Architecture	ISO/IEC/IEEE 42010
Structuring / Aspects	IEC 81346-1/-2/-14
Machine Axes	ISO 841
Robotics	ISO 8373, ISO 9787
Machine Tools	ISO 230, ISO 2806
Additive Manufacturing	ISO/ASTM 52900, 52902, 52903-2, ISO 17295
Manufacturing Process	ISO 14649 / STEP-NC
PLC / Control	IEC 61131-1/-3
Drives	IEC 61800-2, -5-1, -7, CiA 402
Metrology	JCGM 200 / VIM
Product Information	ISO 10303 / STEP
Industrial Information	ISO 15926
Interoperability	OPC UA Information Modeling
Technical Connectivity	IEC 81714-2
Fluid Systems	ISO 1219
Machinery Safety	ISO 12100
Safety Control Systems	ISO 13849-1/-2, IEC 62061
Emergency Stop	ISO 13850
Unexpected Startup	ISO 14118
Guard Interlocking	ISO 14119
Guards	ISO 14120
Machinery Electrical Equipment	IEC 60204-1
21. Standards and Current Ontology Concepts
Object / Classification / Role / Aspect

Strongest architectural references:

IEC 81346-1
IEC 81346-2
IEC 81346-14:2026
ISO 10303
ISO/IEC/IEEE 42010
Axis / Joint / Actuator / Coordinate Frame

Important references:

ISO 841
ISO 8373
ISO 9787
ISO 230
Measurement / Result / Uncertainty

Important reference:

JCGM 200 / VIM
Function / Task / Operation / Procedure

Important references:

ISO 8373
IEC 61131-3
ISO 14649
ISO 9000 family where appropriate

These must be interpreted by domain.

Safety Function

Important references:

ISO 12100
ISO 13849-1
ISO 13849-2
IEC 62061
ISO 13850
ISO 14118
ISO 14119
ISO 14120
Controller / Drive / State

Important references:

IEC 61800 family
CiA 402
IEC 61131
OPC UA information modeling
Product / Occurrence

Important reference:

ISO 10303 / STEP
Ports / Connectivity

Important references:

IEC 81714-2
IEC 81346
ISO 1219 for domain-specific fluid representation
22. Standards That Influenced Explicit Architectural Decisions

The following standards have had particularly strong influence on current architecture.

IEC 81346

Influenced:

Aspect
structuring
multiple engineering views
classification/reference organization
ISO 10303 / STEP

Influenced:

Product
Product Version
Occurrence / Machine Component distinction
structured product information
ISO 8373

Influenced:

Joint
Link
Actuator
Task
robot/machine motion distinctions
ISO 841

Influenced:

Axis
machine motion semantics
ISO 9787

Influenced:

Coordinate Frame
machine/robot coordinate relationships
JCGM 200 / VIM

Influenced:

Measurand
Measurement
Measurement Result
Uncertainty
ISO 14649 / STEP-NC

Influenced:

Process
Operation
Working-step/process distinctions
IEC 61131-3

Influenced the decision to define Machine Builder's:

Function
Task
Action

terms explicitly rather than assuming common software meanings.

ISO 12100 / ISO 13849 / IEC 62061

Influenced:

Hazard
Risk
Safety Function
Safety-related Control
Validation
IEC 81714-2

Influenced:

Port / connection-node thinking
semantic connectivity
23. Standards Research That Should Not Block Current Work

The following areas should be researched only when the related implementation or ontology domain becomes active:

Advanced robot interoperability
Detailed CNC interoperability
Full fluid-power modeling
Advanced electrical CAD integration
Complete industrial information models
Detailed product lifecycle exchange
Advanced safety reliability calculation
Full CAM process planning
Detailed plant lifecycle modeling

The project does not need to understand every relevant standard before continuing development.

24. Targeted Research Rule

When a new domain appears, use the following process:

1. Identify the semantic question.
2. Search for established terminology.
3. Identify major international/industry standards.
4. Prefer current editions.
5. Compare definitions and boundaries.
6. Identify useful distinctions.
7. Test them against Machine Builder stress cases.
8. Record the result.
9. Update ontology only when justified.

The goal is not to accumulate standards.

The goal is to prevent Machine Builder from unnecessarily reinventing established engineering concepts.

25. Standards Conflict Rule

If two standards use the same term differently:

Record the difference.
Identify the domain of each definition.
Do not silently choose one.
Determine whether Machine Builder needs a broader concept or separate terms.
Preserve the source context.
Make the project terminology explicit.

Example:

Function

has different meanings in:

systems engineering;
PLC programming;
robotics;
machinery safety;
manufacturing process descriptions.

The correct response is not to declare one usage universally correct.

26. Standards Currency Rule

Standards are living documents.

Before a standards-based architectural statement becomes a frozen implementation requirement:

verify current edition/status;
verify whether amendments apply;
verify whether a newer edition or draft materially changes the concept;
record the source date.

This is especially important for safety standards and other standards with active revisions.

27. Current Standards Strategy

The current project strategy is:

                Broad Standards Hunt
                        │
                        X
                        │
                        ▼
              Targeted Standards Research
                        │
                 ┌──────┴──────┐
                 ▼             ▼
          New Semantic      New Engineering
              Domain            Requirement
                 │             │
                 └──────┬──────┘
                        ▼
                Relevant Standards
                        │
                        ▼
                  Evidence / Model
                        │
                        ▼
              Ontology / Architecture

Broad standards research has diminishing returns.

Targeted research at the point where a new domain is actually entered is preferred.

28. Current Tier-1 Reference Set

The current standards most important to the core architecture are approximately:

ISO/IEC/IEEE 15288
ISO/IEC/IEEE 42010
IEC 81346-1
IEC 81346-2
IEC 81346-14:2026
ISO 841
ISO 8373
ISO 9787
ISO 10303 / STEP
JCGM 200 / VIM
IEC 81714-2
ISO 12100
ISO 13849-1
IEC 62061
ISO 14649 / STEP-NC

This is not a claim that every one of these standards must be implemented directly.

They provide the strongest current external evidence for the architecture and ontology.

29. Current Tier-2 Reference Set

The current supporting standards include:

ISO 230
ISO 2806
ISO/ASTM 52900
ISO/ASTM 52902
ISO/ASTM 52903-2
ISO 17295
IEC 61131-1
IEC 61131-3
IEC 61800-2
IEC 61800-5-1
IEC 61800-7
CiA 402
ISO 13850
ISO 14118
ISO 14119
ISO 14120
ISO 13849-2
IEC 60204-1
OPC UA Information Modeling
ISO 15926

These may become more central as their domains become implementation targets.

30. Current Tier-3 / Future Reference Set

Examples include:

ISO/TR 13849-3
ISO 1219 series
Additional CNC interoperability standards
Additional robotics interoperability standards
Additional electrical engineering standards
Additional manufacturing-process standards

These should be researched when concrete requirements justify them.

31. Final Principle

Machine Builder should use standards as an engineering knowledge source, not as a decorative bibliography.

A useful standards reference should answer at least one of these questions:

What does this concept mean?

Why should these concepts remain separate?

How should this relationship behave?

What engineering constraint applies?

What vocabulary already exists?

What evidence supports the architectural decision?

If a standard does not materially answer one of those questions, it does not need to become part of the current architecture.

The goal is a machine model that is informed by established engineering practice while remaining coherent, extensible, and useful across different machines, firmware systems, and engineering disciplines.

## Hardware Catalog and Interchange Formats — Research Proposal (2026-10-11)

**Status:** Research recommendation only. This does not authorize a catalog loader, schema implementation, ontology expansion, file migration, or firmware-adapter implementation. The Promega wiring vertical slice remains the immediate priority. Future catalog architecture work belongs in the canonical future-feature register in `MASTER_PLAN.md`, Section 13.

### Executive recommendation

Evaluate a declarative, versioned hardware catalog with stable product/revision identity, source-backed claims, and format-specific import adapters. YAML is a reasonable human-authored candidate if its accepted subset is restricted to a JSON-compatible data model and records are validated. JSON remains a viable alternative. JSON Schema Draft 2020-12 is a candidate for structural validation, not a replacement for domain validation or the canonical machine model.

Keep three concerns separate:

1. **Catalog facts:** manufacturer identity, product and hardware revision, documented connector/contact information, electrical limits, mechanical characteristics, and sources.
2. **Installed machine structure:** the particular installed `MachineComponent`, `Controller`, `SemanticPort`, `SemanticConnection`, `ControllerResource`, and relevant assignments/relationships.
3. **Firmware interpretation:** provider, firmware version, board-specific mapping, configuration syntax, and settings for a target.

The catalog informs the canonical model; it must not silently replace the installed model with generic product assumptions. Unknown, inferred, conflicting, and unverified facts must remain distinguishable. Each material claim should be traceable to evidence at the claim/property level, not merely to a source listed on the overall object.

### Architecture requirements and boundaries

**Identity and versioning**

- Give each reusable record a stable internal identifier rather than relying on its display name.
- Separate schema version, record version, product/variant identity, and hardware revision.
- Do not merge variants merely because they share a marketing name or connector family.
- Record the source document's identity, revision, and date where available. A current web page does not prove an older board revision has the same pinout.
- Preserve conflicting source claims rather than choosing one unqualified value.

**Evidence and uncertainty**

- Represent claim values, units where applicable, supporting source, applicable revision/variant, and status such as documented, inferred, conflicting, or unverified.
- Keep manufacturer reference data, firmware sample/configuration data, and observations of the actual as-built machine separate.
- Record assumptions and rationale for derived values. Object-level provenance does not prove which source supports each property.
- Absence of evidence means unknown, not an empty connector, disconnected wire, default electrical value, or permission to infer a mapping.
- Associate claims with the revision or assembly variant to which their evidence applies.

**Installed structure and electrical semantics**

- `HardwareDefinition` is a reusable catalog specification; `MachineComponent` represents the installed component or role in a particular machine.
- Physical `SemanticPort` endpoints and `SemanticConnection` objects describe installed topology. `ControllerResource` describes a controller resource and is not itself a physical connector.
- Firmware resource assignment is distinct from wiring. Board resource IDs, firmware channel names, connector labels, cable labels, and physical contact identities must not be conflated.
- Catalog connector facts do not establish the identity or contact-to-contact connectivity of the actual installed cable.
- Represent connector contacts as records with numeric `position` fields. Avoid integer dictionary keys in catalog records: the current persistence layer has a string-key restriction, and a serialization `TypeError` demonstrates that limitation rather than successful persistence.
- Geometry, board artwork, contact locations, and drawing references are supporting data, distinct from electrical meaning and installed topology.

### Format and interchange comparison

| Format or source | Appropriate use | Important limits |
|---|---|---|
| YAML 1.2.2 | Readable, editable catalog records | Restrict accepted features; avoid custom tags and values that cannot round-trip to the chosen data model. Validate after loading. |
| JSON | Programmatic records and interchange | Less pleasant for humans to maintain directly; still needs schema and semantic validation. |
| JSON Schema Draft 2020-12 | Required fields, types, enums, and nested structure validation | Does not validate electrical truth, revision compatibility, machine topology, or source credibility. |
| KiCad schematic and PCB formats | Import ECAD symbols, nets, footprints, and board layout when source files exist | Requires version-aware adapters. ECAD files do not prove the user's cable, board population, exact installed revision, or as-built assembly. |
| IPC-2581, including the C revision when supported | Structured ECAD exchange for board, component, and net data | Confirm actual revision and tool support. Do not assume it contains all mechanical, harness, assembly, or as-built facts needed by this application. |
| STEP AP242 / ISO 10303-242 | Mechanical geometry and supplied product/manufacturing information | Not a replacement for electrical connectivity, controller resources, or firmware mappings. Verify the actual model profile and content. |
| 3MF | 3D-printable model data and associated information | Not a canonical controller, net, wiring, or firmware schema. |
| Manufacturer PDFs, schematics, drawings, and manuals | Primary evidence for revision, pin labels, wiring options, mechanical drawings, and instructions | Preserve document revision/date and a page/sheet/section locator where possible. A document supports only claims it actually establishes. |
| BOM and CSV exports | Part-number lists, quantities, and repeatable import/export | Columns and semantics vary. A BOM alone does not establish nets, installed position, cable routing, or configuration meaning. |
| Native firmware configuration | Firmware-specific settings, names, pins, and supported behavior | Must be tied to the firmware/provider/version. A sample configuration does not prove the user's actual machine matches it. |

### Standards and reference leads

These are research leads, not a claim that the project must adopt a complete standard or that conformance has been audited.

- **YAML 1.2.2:** https://yaml.org/spec/1.2.2/ — candidate human-editable syntax; define a restricted subset.
- **JSON Schema Draft 2020-12:** https://json-schema.org/draft/2020-12 — structural schema validation.
- **KiCad file formats:** https://dev-docs.kicad.org/en/file-formats/ — format-specific import research.
- **IPC-2581:** https://www.ipc2581.com/ — verify revision, data coverage, implementation support, and source/toolchain conditions.
- **ISO 10303 / STEP AP242:** https://www.iso.org/search.html?q=ISO%2010303-242 — mechanical/product interchange; evaluate actual source contents.
- **3MF specifications:** https://3mf.io/specification/ — 3D model interchange.
- **IEC 61360-1:** https://webstore.iec.ch/en/search?query=IEC%2061360-1 — standardized data-element types and classification concepts.
- **ISO 8000 series:** https://www.iso.org/search.html?q=ISO%208000 — data quality and master-data research.
- **IEC 61076 series:** https://webstore.iec.ch/en/search?query=IEC%2061076 — connector-interface research where a specific connector family/revision is relevant; do not infer compatibility from physical resemblance.
- **W3C PROV-O:** https://www.w3.org/TR/prov-o/ — provenance vocabulary for source/activity/agent relationships; not an automatic reason to add a new V0.2 ontology.
- **Dublin Core Metadata Terms:** https://www.dublincore.org/specifications/dublin-core/dcmi-terms/ — metadata concepts for source documents.
- **Marlin configuration reference:** https://marlinfw.org/docs/configuration/configuration.html
- **Klipper configuration reference:** https://www.klipper3d.org/Config_Reference.html
- **Duet firmware documentation:** https://docs.duet3d.com/ — use the exact version-specific reference for each claim.

Adopt standards only when a concrete requirement and bounded validation case justify them. Relevance is not a reason to implement an entire external provenance, classification, or interchange system.

### Firmware adapters

Marlin, Klipper, and RepRapFirmware should have separate, version-aware adapters rather than one universal firmware parser.

- **Marlin:** configurations and pin/feature definitions depend on target board, build environment, enabled options, and firmware revision. A configuration or board pin file does not alone establish the actual machine.
- **Klipper:** configuration files and includes describe Klipper-specific pins, steppers, heaters, sensors, and modules. Preserve include paths and firmware context during import.
- **RepRapFirmware (RRF):** G-code configuration and board mappings must be associated with the target board and RRF version. A legacy vendor release does not prove compatibility with a later RRF configuration.

An adapter translates recognized firmware-specific facts into the canonical model without redefining physical hardware facts. Preserve original text or source locations where practical, record adapter/version information, and distinguish parsed values from inferred intent. Ambiguous or unsupported syntax should not be silently reinterpreted.

### Proposed catalog directory layout

Proposal for later Planning review only; do not create this scaffolding now.

    catalog/
      catalog-manifest.yaml
      schemas/
        hardware-definition.schema.json
        firmware-adapter.schema.json
        source-record.schema.json
      hardware/
        controllers/<manufacturer>/<family>/<revision>/hardware.yaml
        driver-modules/<manufacturer>/<model>/<revision>/hardware.yaml
        motors/<manufacturer>/<model>/<revision>/hardware.yaml
        sensors/<manufacturer>/<model>/<revision>/hardware.yaml
        assemblies/<manufacturer>/<family>/<variant>/hardware.yaml
      firmware-adapters/<provider>/<board-variant>/adapter.yaml
      evidence/sources.yaml
      assets/
      examples/machines/
      tests/

A separate harness/assembly-definition layer should be justified by real reuse and evidence. Do not create empty catalog scaffolding or relocate existing model data as part of this research checkpoint.

### Candidate record fields

A future common record could evaluate:

- **Identity:** stable ID, schema version, record version, record kind/category, manufacturer, product/family, model, variant, hardware revision, aliases, and documented manufacturer part number.
- **Evidence:** source ID, document title/revision/date, URL or repository revision, page/sheet/section locator, claim/value/unit, status, applicable variant, and assumption/conflict note.
- **Connectors and contacts:** local IDs, printed connector designator/name, connector family where known, contact array with numeric `position`, contact label, documented electrical role, qualified voltage/current constraints, and source references.
- **Controller resources:** board-local resource ID, type, hardware mapping, limitations, and claim evidence. Do not confuse resource IDs with physical terminals.
- **Geometry and assets:** sourced dimensions/outlines, coordinate system, orientation, asset reference, and exact board-revision evidence.
- **Firmware adapter references:** provider, version range, board/variant condition, native configuration key, source path, mapping rule, and limitations.
- **Compatibility and conflicts:** explicit scope and conditions rather than unsupported Boolean compatibility claims.

A conceptual contact record could use an array like this:

    contacts:
      - position: 1
        label: "GND"
        claims:
          - value: "ground"
            state: documented
            source: "source-duet-maestro-v1"
      - position: 2
        label: "SIGNAL"
        claims:
          - value: null
            state: unverified
            note: "Role has not been confirmed for this exact connector revision."

This is illustrative only. Field names, enumerations, null behavior, units, and claim structures require an explicit decision and tests before implementation.

### Candidate cases for a bounded pilot

Use real, revision-identified cases that challenge different parts of the proposal:

1. **BIGTREETECH Octopus:** multiple connectors/resources and revision-specific evidence.
2. **BIGTREETECH SKR Mini E3 V3.0:** a contrasting board family and board-specific firmware mapping.
3. **TMC5160T Pro driver module:** reusable driver module kept distinct from controller board and installed motor wiring.
4. **Duet IR probe:** electrical terminals, physical mounting, firmware interpretation, and readings/configuration must remain distinct facts.
5. **Promega harness and assembly variants:** uncertain or variant-dependent wiring, board ports, cable labels, and firmware channels.

These are pilot candidates, not declarations that every detail has already been verified. Record exact source revisions and unresolved claims before using examples as schema acceptance fixtures.

### Gap analysis

Candidate capability gaps to evaluate after the Promega milestone:

- No established, common versioned catalog contract and loader across the expected sources.
- No accepted convention ensuring material claims have their own supporting evidence.
- No demonstrated validation and migration process for schema revisions.
- Electrical quantities, units, tolerances, conditions, and rating scope need consistent representation.
- Revision, option, assembly, and harness variants must be representable without flattening disagreement into a universal pinout.
- Source adapters need semantic validation; conversion to YAML/JSON alone does not preserve correct meaning.
- Geometry and asset coordinates need source, revision, and coordinate context.
- Persistence compatibility must be tested with actual records; numeric-position contact arrays avoid the known integer-dictionary-key problem.
- Firmware import must preserve provider/version boundaries and source evidence.
- Catalog data must not become an asserted as-built connection without evidence.

### Staged adoption proposal

**Stage 0 — current priority:** complete and validate Promega wiring with source-grounded details. Keep unknown connections unknown; do not interrupt that work to implement a catalog framework.

**Stage 1 — after Promega, with Planning decision:** consider a bounded pilot using one controller board and one contrasting board/module or sensor. Demonstrate stable identity, schema validation, claim-level evidence, revision handling, contact arrays, persistence, and explicit unknown/conflict behavior end to end.

**Stage 2 — if the pilot demonstrates value:** evaluate adapters for manufacturer drawings/ECAD, geometry, BOMs, harness/assembly definitions, and the three firmware families. Add formats based on documented needs.

**Stage 3 — separate broader decision:** evaluate migrations, maintenance, source-update tracking, tests, and ownership.

### Open decisions for Planning — deferred

- YAML with a restricted JSON-compatible data model versus JSON-authored records.
- Identity, schema versioning, and migration policy.
- Minimum claim-level evidence and uncertainty vocabulary.
- Units, revision applicability, conflicts, and derived-value representation.
- Separation between reusable connector/part definitions and installed endpoint mappings.
- Whether geometry, external standards, harness/assembly definitions, and firmware adapters belong in later phases.
- Which real records and checks would make a bounded pilot acceptable.

Record deferred ideas in `MASTER_PLAN.md` Section 13, the canonical future-problem/future-feature register. Do not create a competing backlog or interpret this research as implementation approval. V0.2 remains the working ontology boundary unless a real case demonstrates a representation blocker.

### Follow-on research: liquid-cooled hotend and coolant loop

**Checkpoint and source-access date:** 2026-10-11.

**Status:** Manufacturer-source research and V0.2 representation assessment. This record does not authorize ontology expansion, new catalog infrastructure, or application implementation. The Promega wiring vertical slice remains the active implementation priority.

#### Primary manufacturer sources and revision context

1. **Typhoon LCX & Typhoon Air 2.85 mm Filament Extruder — DYZE DESIGN Docs:** https://docs.dyzedesign.com/typhoon.html
   - The mutable manufacturer documentation page contains a revision table listing R001 dated 2023-09-29 and R002 dated 2026-06-12. The R002 entry says it added details about heater PWM frequency.
   - The page footer reports a last update of October 1, 2026. Treat R002 as the revision label in the page's revision table; do not mistake this live page for an archived, independently frozen copy of a particular revision.
   - Relevant sections include What's Included, What's Required, LCX Liquid Cooling, Air Cooling, and Wiring.

2. **Liquid Cooling — DYZE DESIGN Docs:** https://docs.dyzedesign.com/liquid-cooling.html
   - This is a separate mutable manufacturer guide. Its footer reports a last update of October 1, 2026 at 2:30 PM.
   - Relevant sections include Dyze Design Liquid Cooling Kit, First Setup, Mounting, Wiring, Tube Routing, Maintenance, and the build-your-own recommendations.

The source dates above are the revision/update labels displayed by the manufacturer, not the date of an independent bench test. Sources accessed for this checkpoint on 2026-10-11.

#### Manufacturer-documented hardware and loop facts

**LCX interface and fittings**

- The Typhoon LCX included-parts list specifies a liquid-cooling fitting kit containing two M8 x 1.00 elbow or compression fittings and two M8 x 1.00 plugs.
- The LCX liquid-cooling section says to use one inlet and one outlet, plug the unused ports, and put the inlet on the opposite side from the outlet.
- The documentation does not establish the exact side/orientation of a particular installed unit or the fittings actually present in an as-built machine.

**Tubing and loop topology**

- Recommended tubing is high-temperature rubber tubing with 6.35 mm (1/4 inch) internal diameter and 9.53 mm (3/8 inch) outside diameter.
- The cooling guide describes a complete loop from the Cooling Unit to the cooled component(s) and back to the Cooling Unit. Its fitting instructions describe the Cooling Unit output as cold water from the unit and the input as hot water returning from the hotend.
- This supports a source-consistent supply/return representation: Cooling Unit output to LCX inlet, then the LCX outlet back to Cooling Unit input. It does not justify inventing internal passage geometry or asserting measured flow direction/rate for an installed assembly.
- The guide recommends safely routing the tubes across the machine's full motion range and avoiding kinks, pinches, abrasion, hot surfaces, stretching, and interference with moving parts.

**Cooling unit nominal specifications**

The manufacturer's kit list specifies:

- Pump: 800 L/h nominal rating.
- Transparent reservoir: 300 ml.
- Radiator: 360 x 120 mm.
- Three 120 x 120 mm fans.

These are the guide's product specifications, not measured coolant flow, installed performance, or proof that a particular kit is fitted to a user's printer. For a self-built loop, the same guide separately recommends at least 600 L/h pump capacity for a Typhoon or Pulsar; do not conflate that recommendation with the listed 800 L/h kit pump.

**Materials and coolant**

- The Typhoon LCX documentation states that its cooled parts are aluminum alloy and calls for an aluminum radiator to prevent galvanic-corrosion concerns. The liquid-cooling guide separately warns about potential galvanic corrosion involving copper/brass components and advises against copper or brass radiators.
- The guide recommends deionized water with about 5 ppm of minerals, a corrosion inhibitor, and a biocide.
- These are the manufacturer's application-specific recommendations. They do not establish universal compatibility of every fluid, tubing, metal, fitting, or mixed-material loop.

**Electrical supplies and operating constraints**

- The liquid-cooling guide says its Cooling Unit needs 12 V DC for its pump, fans, sensors, and circuit board. Its table lists 12 V typical input, 13.5 V maximum, and 2 A typical current; these figures should not be misreported as measured current or as a printer-controller output rating.
- The same guide identifies the Cooling Unit supply terminals as bottom pin V+ and top pin V-. These are Cooling Unit supply terminals, not a printer-controller pin assignment.
- The Typhoon page separately lists a 24 V DC supply requirement for the LCX when using DYZE DESIGN liquid cooling. Its separate front cooling fan is specified as 70 mm, 24 V DC, 0.19 A, and 4.6 W.
- The LCX cooling section says its water pump must remain operational whenever the additive-manufacturing machine is in use. The integrated 70 mm cooling fan must also remain operational during use.
- Keep the Cooling Unit's 12 V supply, the Typhoon/fan 24 V requirements, any verified printer-board wiring, and firmware resource assignments as distinct facts. The manufacturer supply requirements alone do not establish how an installed printer powers or controls these devices.

**Kink/blockage and print-pause behavior**

- The liquid-cooling guide states that tube kinks and blockages will be detected by the system and will pause the print.
- The Typhoon product page does not describe this pause behavior in its LCX section. The inspected cooling guide documents the Cooling Unit's supply terminals but does not identify the detector, sensor output interface, external signal path, controller input, firmware setting, or pause command.
- Therefore the system-level behavior is manufacturer-reported, while the detection subsystem and end-to-end signal path remain unresolved. Do not fabricate a sensor-to-controller connection or a firmware assignment.

**Conflicting tubing bend-radius instructions**

The same mutable liquid-cooling guide contains inconsistent limits:

- In First Setup / Route the Tubing, it says the bend radius should never be smaller than 2 inches (50 mm).
- In Mounting, it says the bend radius should not exceed 2 inches (50 mm).

The inequalities conflict. Preserve this as conflicting manufacturer guidance and seek clarification before translating either limit into an acceptance requirement; do not silently select one interpretation.

#### Official standards records and applicability

The official ISO records were checked on 2026-10-11. These standards inform diagram presentation; this research does not declare conformance or require ontology changes.

- **ISO 1219-1:2012:** https://www.iso.org/standard/60184.html
  - Covers graphical symbols for fluid-power systems. The official record lists the 2012 edition as published and includes review/status information indicating the base standard is under review and to be revised. **ISO 1219-1:2012/Amd 1:2016** is separately listed as published: https://www.iso.org/standard/66287.html.
  - It is a relevant fluid-power symbol reference, but the fact that it provides useful symbols does not establish that this standalone thermal-cooling loop falls under a mandatory fluid-power application.

- **ISO 1219-2:2012:** https://www.iso.org/standard/51200.html
  - The official record identifies the 2012 edition as published and reports confirmation in December 2023. Its scope includes diagrams for cooling systems, lubrication systems, cooling-lubricant systems, and technical-gas systems used in conjunction with fluid-power applications.
  - The conjunction condition matters. This research has not established that it applies to the complete standalone Typhoon LCX cooling assembly. Check the live lifecycle record again before freezing an external standards requirement.

- **ISO 14617-1:2025:** https://www.iso.org/standard/85641.html
  - Published in March 2025, it supplies general rules and guidance for preparing and presenting graphical symbols for diagrams related to industrial components, products, and processing. It supersedes the withdrawn ISO 14617-1:2005 edition.

- **ISO 14617-2:2025:** https://www.iso.org/standard/83364.html
  - Published in April 2025, it provides a graphical-symbol library for diagrams. Its official scope explicitly excludes fluid-power objects (referred to ISO 1219-1), measurement/control-function symbols, and electrotechnical symbols (referred to IEC 60617).
  - It is not a universal library for a combined coolant, electrical, sensor, and firmware/control view.

Architectural implication: coolant, electrical, and firmware/resource diagrams may need domain-appropriate symbols and view-specific conventions while remaining presentations of one canonical machine model. The drawing convention does not justify duplicating physical facts in competing models.

#### Current official-source follow-up (2026-10-12)

**Sources reviewed:** DYZE DESIGN's current [Liquid Cooling guide](https://docs.dyzedesign.com/liquid-cooling.html), [Typhoon/LCX guide](https://docs.dyzedesign.com/typhoon.html), and official [Products Changelog](https://docs.dyzedesign.com/general-support/changelog.html).

**Bend-radius contradiction remains unresolved:** The current Liquid Cooling guide says under "Route the tubing" that the radius must never be smaller than 2 inches (50 mm), while its "Mounting" section says it should not exceed 2 inches (50 mm). Read literally for the same radius, these instructions permit exactly 50 mm. The guide does not resolve the opposing minimum/maximum or identify the radius measurement datum. Do not guess which statement is intended.

**Kink/blockage pause behavior remains unexplained:** The guide says tubing kinks or blockages will be detected and printing paused, but does not identify the detector, measured physical quantity, threshold, electrical output/interface, controller signal path, or firmware pause mechanism. The adjacent wiring section identifies the Cooling Unit's 12 V supply and V+/V- terminals but does not document a sensor output or printer signal path. The Typhoon/LCX guide says the pump must remain operational while the machine is in use, but does not explain the claimed kink-detection pause. Do not infer a flow sensor, pressure sensor, or specific interface.

**Product revision matters:** Public changelog PCN-00006 describes the original Typhoon being phased out in favor of LCX/Air variants, with liquid cooling streamlined to pressure-plate cooling and revised elbow fittings. The current kit listing specifies an 800 L/h pump, 300 ml reservoir, 360 x 120 mm radiator, three 120 mm fans, and 8 m of tubing with 1/4 inch ID and 3/8 inch OD. Its build-your-own guidance separately recommends at least a 600 L/h pump for Typhoon/Pulsar, a reservoir of 500 ml or larger, an aluminum radiator, and avoiding copper/brass radiators. These published specifications are reference data only, not evidence of the hardware installed on the Promega.

**Bounded public-source search result:** The accessible current official pages and public changelog did not resolve the radius contradiction or explain the detector-to-firmware path. This does not prove that no older, private, or otherwise unavailable manufacturer documentation exists. The installed Cooling Unit revision, pump/radiator, hose and fitting arrangement, wiring, active configuration/macros, and firmware integration remain unverified.

**Follow-up:** Request written DYZE clarification of the intended radius limits and measurement datum, and ask what detects kink/blockage, what interface it uses, and how the pause signal reaches printer firmware. When physically possible, identify the installed unit revision and record its hoses, fittings, and wiring. Once the SD card is accessible, inspect the active configuration/macros before making claims about firmware integration. Keep this follow-up parallel to Promega wiring; it is not a prerequisite for that work.

#### Official Cooling Unit drawing and support-path evidence (2026-10-12)

**Official sources and asset qualification:** DYZE DESIGN's [CAD and Drawings index](https://docs.dyzedesign.com/general-support/cad-drawings.html), which reports an October 1, 2026 update, lists a Liquid Cooling System STEP file and a resource labelled "Liquid Cooling System Detailed DWG." The STEP link resolves to [STEP - Cooling Unit Support - 2022-05-16.step](https://drive.google.com/file/d/1EYFy_o-2LH8SqqEQ21tl1sxn3ycEJKuX/view?usp=drive_link). The detailed-drawing link resolves to [PDF - Cooling Unit Support - 2025-09-09.pdf](https://drive.google.com/file/d/198CSpWS_hVGhBKBwZjXM5DPbr_oTPoGw/view?usp=drive_link). The inspected PDF is one sheet titled "T - MAIN ASSEMBLY" and dated September 9, 2025. The CAD index label says DWG, but the linked asset inspected here is a PDF drawing.

**What the drawing establishes:** The assembly drawing labels a 438.17 mm vertical dimension and a 238.35 mm front-view width. It labels separate input, output, and fill holes with G1/4 threaded compression fittings. Its electrical callout identifies a "Power connector / 2P Term Block Plug / 282805-2." [TE Connectivity's product entry](https://www.te.com/en/product-282805-2.html) identifies 282805-2 as a two-position wire-to-board terminal-block plug with 5 mm pitch. This corroborates the connector's form factor, not the Cooling Unit's internal circuit or a detector-to-printer interface.

**Tubing product listing cross-check (2026-10-12):** DYZE DESIGN's official [High Temperature Tubing product listing](https://dyzedesign.com/shop/liquid-cooling/high-temperature-tubing-9-53mm-od-7-94mm-od/) says the tube fits its water-cooling blocks and lists two size options: 1/4 inch ID x 3/8 inch OD (6.35 x 9.53 mm) and 3/16 inch ID x 5/16 inch OD (4.76 x 7.94 mm). The Liquid Cooling guide identifies the supplied kit tubing as 1/4 inch ID x 3/8 inch OD (8 m). The product listing does not publish a bend-radius limit or explain kink detection. This corroborates available product dimensions, not the hose installed on the Promega or the intended interpretation of the conflicting radius instructions.

**Low-water indication is a separate unresolved detail:** The assembly drawing labels a "Low water level indication" beside the water-level slot. It does not specify an electrical output for that feature, nor identify it as the kink/blockage detector. Do not turn this callout into a sensor port, safety interlock, or controller input without additional evidence.

**Implications for the pause-path investigation:** DYZE's current [Liquid Cooling guide](https://docs.dyzedesign.com/liquid-cooling.html) claims that kinked or blocked tubing will be detected and printing paused, and says the Cooling Unit needs 12 V for its pump, fans, sensors, and circuit board. The guide identifies V+ and V- as supply connections; the drawing labels the depicted two-position connector as the power connector. Neither source documents a separate detector output connector, signal pin, measured quantity, trip threshold, controller connection, or firmware configuration that implements the claimed pause. The exact pause mechanism therefore remains unknown.

**Revision caution:** The public STEP asset is dated 2022-05-16 while the inspected PDF assembly drawing is dated 2025-09-09. Do not assume they describe one identical revision, or that either one establishes the installed Promega Cooling Unit revision. The drawing is evidence about the published assembly, not physical inspection evidence of the user's machine.

**Support escalation:** DYZE's [documentation home](https://docs.dyzedesign.com/) and [official contact page](https://dyzedesign.com/contact/) direct users with unanswered technical questions to open a support ticket. Ask DYZE to clarify (1) the intended tubing bend-radius minimum/maximum and measurement datum for the specified 1/4 inch ID by 3/8 inch OD tube; (2) the physical quantity, detector, and threshold behind kink/blockage detection; (3) the external electrical interface, connector/pins, signal levels, controller path, and firmware mechanism for pausing; and (4) whether "Low water level indication" is visual only or has a separately documented electrical output. The accessible public support-group listing did not expose a matching kink/radius thread in its displayed text; that limited search does not rule out older, unindexed, or private support material.

#### V0.2 source-contract and test assessment

Local source and test files were inspected against checkout HEAD `25d8268600c0979ecfccfccb8a1b0b04bcf89014` on 2026-10-11. This research update did not run the tests; the test names below are existing inspected coverage.

**Reusable definition versus installed component**

- `machine-structure-editor/src/machine_builder/semantic_model.py` defines `HardwareDefinition` with family/manufacturer/variant, properties, and provenance; `MachineComponent` has a role, optional `hardware_definition_id`, port IDs, properties, and provenance.
- This supports keeping reusable LCX and cooling-unit specifications distinct from installed component records and their machine-specific ports/connections.

**Ports and physical connections**

- `SemanticPort` provides a component owner (or controller owner), purpose, a string `direction`, properties, and provenance.
- `SemanticConnection` in `machine-structure-editor/src/machine_builder/semantic_connection.py` stores two endpoint IDs, `connection_type`, properties, and provenance. Its documented contract explicitly says endpoint order is nonsemantic.
- `machine-structure-editor/tests/test_semantic_connection.py::test_connection_endpoint_order_is_not_semantic` confirms that reversing the endpoint order still identifies the same physical connection.
- The record can technically store a medium label in `connection_type` or arbitrary properties, and a port can store direction text. The inspected contracts do not define a shared validated vocabulary for fluid medium and flow direction, enforce consistency between port direction and a connection, or provide a dedicated semantic-connection flow traversal/query contract. The existing tests do not demonstrate a fluid-loop query.

**Directed semantic relationships**

- `SemanticRelationship` in `machine-structure-editor/src/machine_builder/semantic_relationship.py` has ordered `source_id` and `target_id`, a registered `relationship_type`, properties, and provenance. The relationship query helpers support source/target and type queries.
- Its fixed allow-list is `realizes`, `supports`, `requires`, `depends_on`, `participates_in`, `exposed_through`, and `mated_with`. `machine-structure-editor/tests/test_semantic_relationship.py::test_unknown_relationship_type_is_rejected` verifies that an unregistered type is rejected; `test_relationship_can_match_endpoints` verifies that endpoint order matters for a relationship.
- A directed functional relationship is not automatically the physical hose itself. Reusing one for both physical topology and directed coolant transfer would conflate distinct semantics unless their contracts explicitly distinguished those roles.

**Electrical resources and firmware assignments**

- `ControllerResource` and `ControllerResourceAssignment` are separate records, each with properties and provenance. Existing assignment tests establish resource-mapping fields; they do not infer physical wiring from a resource assignment.
- The inspected DYZE sources do not establish a printer-board resource assignment for the Cooling Unit pump, fans, or blockage detection. The pause behavior's signal path must remain unknown.

**Evidence and uncertainty**

- `Provenance` and per-record provenance fields exist. The current model can retain source evidence on the relevant component, port, connection, or relationship.
- This does not automatically make every property claim source-qualified or establish an unknown cable/sensor connection. Manufacturer documentation, inference from interface names, and actual as-built observations must remain distinguishable.

#### Minimal representation/query acceptance case

For an installed Cooling Unit and Typhoon LCX, a future acceptance test should be able to answer, without using connection endpoint ordering as direction:

- Which physical hose connection joins the Cooling Unit cold output to the LCX inlet?
- Which physical hose connection joins the LCX outlet to the Cooling Unit warm-return input?
- Which directed coolant path is supported by those two connected interface roles?
- Can the query return that liquid path without treating the separate 12 V supply, fan wiring, or firmware assignments as coolant connections?

The relevant existing test files are `test_semantic_connection.py`, `test_semantic_relationship.py`, `test_semantic_relationship_queries.py`, `test_controller_resource_assignment.py`, and persistence/provenance tests. The inspected tests cover basic endpoint, registered relationship, assignment, and provenance behavior, but not this fluid-medium/directed-flow acceptance case.

**Assessment:** Existing V0.2 records can represent much of the installed topology and retain directional hints, but a validated, queryable directed-fluid-transfer contract is not demonstrated. This is a concrete semantic-contract/query gap relative to the existing V0.2 statement that fluid direction must be representable. It is **not proof that a new ontology entity is necessary**.

Alternatives to evaluate, without implementing any now:

1. Define and test a bounded convention for port direction plus physical connection medium, with a query that traverses that convention.
2. If this cannot remain unambiguous, evaluate a typed directed-transfer relation while retaining the hose as a separate undirected physical connection.
3. Consider a new ontology construct only if a concrete acceptance test shows the existing canonical boundary cannot express the necessary distinction.

#### Directed-fluid-transfer contract comparison and recommendation (2026-10-11)

**Inspection basis:** Read-only inspection of the canonical model, port/connection/relationship definitions, query helpers, and existing connection, relationship, and persistence tests at the published checkpoint. This comparison does not change source code or tests.

**What the current contracts establish**

- `CanonicalMachineModel._has_canonical_object()` includes canonical port IDs. `add_relationship()` checks endpoints with that general lookup, so a `SemanticRelationship` can refer to ports as its ordered source and target. This endpoint support alone does not establish fluid-transfer semantics.
- `SemanticPort.direction` is a string with a default of `unknown`; the inspected contract does not provide a validated fluid-direction vocabulary.
- `SemanticConnection` represents a physical connection between two ports. Its endpoint order is intentionally nonsemantic. `connection_type`, properties, and provenance can hold descriptive data, but the inspected contract does not validate a shared fluid-medium vocabulary or relate that data to directed flow.
- `SemanticRelationship` has ordered `source_id` and `target_id`, but its registered types do not currently include fluid transfer. The query helpers filter existing relationships by source, target, type, or ordered endpoint pair; they do not traverse a fluid loop or validate a physical hose reference.
- Persistence tests demonstrate round-trip preservation of generic connections and relationships, not a directed coolant-path query.

**Option A -- convention over port roles and physical connection metadata**

A convention could label a hose connection as fluid/coolant and use validated inlet/outlet roles to infer direction across that hose without depending on endpoint order. This is less invasive conceptually, but the current direction field is not validated and no query implements the convention. More importantly, hose-end roles alone do not state how fluid transfers between a component's own inlet and outlet. This option is insufficient by itself for a verified end-to-end loop query.

**Option B -- typed directed-transfer relationship over existing ports (preferred for Planning to evaluate)**

Keep each hose as an undirected `SemanticConnection`; represent directed transfer separately with an explicitly registered, typed relationship whose ordered endpoints are ports. The eventual contract would need to define the transfer type and its validated medium/path metadata. A transfer across a hose should reference the associated physical connection and validate that it joins the same two ports in either endpoint order. An internal transfer through a component should be distinguishable from transfer across a physical connection. Preserve provenance and unknown values; do not infer a direction from `endpoint_a_id` or `endpoint_b_id`.

Existing `SemanticRelationship` and its query helpers provide a possible starting point, but the allow-list, type validation, connection-reference consistency, and path-query behavior would need to be deliberately specified and tested. Do not simply overload `supports`, `participates_in`, or another existing type to mean coolant flow. This option does not, by itself, prove that a new ontology entity is needed.

**Minimal acceptance case for a future bounded implementation**

Represent an installed Cooling Unit and Typhoon LCX with these boundaries and path segments:

1. Cooling Unit cold output -> LCX inlet, across physical hose A.
2. LCX inlet -> LCX outlet, through the LCX component.
3. LCX outlet -> Cooling Unit warm-return input, across physical hose B.
4. Cooling Unit warm-return input -> cold output, through the Cooling Unit.

A query should identify hose A and hose B by their physical connection records, return the directed sequence above, and retain evidence/provenance for each asserted transfer. Reversing either hose connection's stored endpoint order must not alter the result. Round-trip persistence must preserve the same queried path. The query must not include the Cooling Unit's separate electrical supply, fan wiring, or controller-resource/firmware assignments as coolant flow. Missing or unverified transfer direction must remain unknown rather than being inferred from connection storage order.

**Conclusion:** Planning accepted the bounded Option B contract on 2026-10-12 as an appropriate proposed conceptual/documentation design. This acceptance does not authorize implementation, test changes, production-validation claims, or ontology expansion. The existing port-role validation gap remains explicit.

No source, tests, catalog definitions, or ontology were changed for this research. Keep broader flow-rate semantics, flow sensors, leaks, pressure, coolant chemistry, and a universal fluid-safety ontology deferred as stated in the existing V0.2 checkpoint.

#### Bounded directed-fluid-transfer contract specification (2026-10-11)

**Status and scope:** Proposed semantic/query contract for Planning review only. It is limited to an installed liquid-coolant loop such as a Cooling Unit and Typhoon LCX. It does not define universal fluid safety, coolant chemistry, pressure/flow-rate semantics, leak detection, or a new ontology entity.

##### 1. Physical connectivity versus directional transfer

- `SemanticConnection` records physical adjacency between two ports. Stored endpoint order has no directional meaning. Physical connectivity alone does not establish which way a medium flows.
- A directed transfer is a separate assertion with ordered source and target ports. Its direction comes from that assertion and its supporting evidence, never from `endpoint_a_id` versus `endpoint_b_id`.
- An across-hose transfer must reference an explicitly classified fluid-hose connection. The current `connection_type` is a free string, so this contract proposes a validated classification such as `fluid_hose`; arbitrary text, port labels, and proximity are insufficient.
- A hose may be known to connect two ports while its flow direction remains unknown. Preserve the physical fact without inventing a directed transfer.

##### 2. Proposed relationship contract

Evaluate a dedicated registered relationship type named `fluid_transfer` using `SemanticRelationship`. This name is proposed and is not currently registered.

- `source_id` and `target_id` must resolve to distinct canonical `SemanticPort` records. The source is upstream for this transfer step and the target downstream. A component ID, controller ID, wire, or `SemanticConnection` ID is not a valid transfer endpoint.
- Require a validated relationship-level `medium` value. For this bounded contract the only recognized value is `liquid_coolant`; missing or unrecognized values are invalid for the coolant query. The relationship medium must be present as a key in both endpoint ports' medium-scoped role maps.
- Require a validated `segment_kind`, with initial values `across_connection` and `within_component`, distinguishing transfer across a hose from transfer through a component.
- **Canonical role location:** Each `SemanticPort` owns its role assignments, scoped by medium. Propose using the existing `SemanticPort.properties` container with a reserved `fluid_roles` map, for example `{"liquid_coolant": "inlet"}` or `{"liquid_coolant": "outlet"}`. Do not duplicate a `fluid_role` value on each transfer relationship. This is a proposed contract shape, not a currently validated model field.
- **Role-pair validation:** The relationship's `medium` must be a recognized controlled key present in both endpoint ports' `fluid_roles` maps. For this bounded contract, `liquid_coolant` is the only allowed key and `inlet`/`outlet` are the only allowed role values. For `across_connection`, source role must be `outlet` and target role `inlet`; for `within_component`, source role must be `inlet` and target role `outlet`.
- **Contradictory or missing roles:** Reject malformed maps, invalid values, contradictory role/segment combinations, and medium mismatches. Missing role keys, unknown values, or unsupported media leave the role unresolved; transfers with unresolved endpoint roles must not be treated as valid traversable edges. Do not infer roles from free text or interpret generic `SemanticPort.direction` as coolant-flow direction.
- **Existing-contract limitation:** `SemanticPort.properties` can structurally store this map, but the current contract does not validate its schema, medium keys, or role values. A future validation boundary must interpret and validate the medium-scoped map consistently before it is authoritative. If the current port contract cannot represent and validate roles reliably, record that specific limitation for Planning rather than silently duplicating roles on relationships or adding an ontology entity now.
- For `across_connection`, require `physical_connection_id` referencing an existing, non-self fluid-hose `SemanticConnection`. Its two endpoint IDs must equal the transfer's source/target IDs as an unordered pair. Either stored endpoint order is valid. Electrical, fan, signal, and other non-fluid connections must be rejected.
- For `within_component`, require `through_component_id`. Both ports must belong to that same installed component and must be distinct. Do not invent a hose reference for internal transfer.
- Reject unknown relationship types, non-port endpoints, dangling references, endpoint mismatch, missing required metadata, contradictory segment fields, unsupported media, and inconsistent roles. Do not overload `supports`, `participates_in`, or unrelated relationship types.
- `SemanticRelationship.properties` can store arbitrary data, but storage is not validation. The contract must specify a deliberate validation boundary for the controlled values and references. Prefer using the current ports, physical connections, relationships, and provenance. Consider a new entity only if a concrete constraint cannot be represented and validated with those concepts; that requires a separate Planning decision.

##### 3. Directed path and loop query

A future query should accept a start port, a target port or non-empty-loop request, and the required medium. Example API names are illustrative, not an implementation commitment.

- Traverse only validated `fluid_transfer` relationships matching the requested medium, following source to target. Never traverse physical connections or generic relationships as though they were flow assertions.
- Return the ordered transfer-relationship IDs. For every across-connection step also return the referenced physical connection ID; for each within-component step return the component ID.
- Adjacent steps must share the same canonical port ID. A loop must be a non-empty directed cycle; a zero-step query from a port to itself is not a loop.
- If more than one valid route exists, return the alternatives or an explicit ambiguity. Never silently select a path because of storage or insertion order.
- Electrical supply, fan wiring, controller-resource assignments, firmware mappings, and unrelated physical connections must not become coolant-flow edges, even if they share components with the fluid loop.

##### 4. Provenance, unknowns, and incomplete installations

- Every directed step needs provenance that supports its direction and segment kind, such as a manufacturer reference, engineering record, or physical observation. Evidence of connectivity alone does not prove direction.
- An unverified direction remains unknown and is not traversable as an established directed edge. Preserve known physical connections and their evidence, and record the unresolved direction rather than inventing a transfer, medium, internal path, or loop closure.
- An incomplete physical configuration must produce an incomplete result, not a completed loop inferred from intended behavior or undocumented assumptions.
- If competing or unresolved transfer hypotheses need first-class representation, specify their status and query behavior separately. Do not present an uncertain assertion as a verified edge.

##### 5. Minimal positive acceptance case

**Evidence classification:** The cited manufacturer sources document products and published guides, but do not establish the graph below as verified installed topology. The precise port labels and role assignments, hose A/B placements, transfer directions, internal port arrangement and transfer through either component, and loop closure below are explicitly synthetic acceptance-fixture assertions. None of these graph edges is claimed as manufacturer-documented or inferred from those sources. This fixture is not evidence for the user's installed machine or a catalog topology.

The following graph is constructed synthetic test data:

1. **Synthetic fixture assertion:** Cooling Unit cold output (`outlet`) -> LCX inlet (`inlet`), across synthetic physical hose A.
2. **Synthetic fixture assertion:** LCX inlet (`inlet`) -> LCX outlet (`outlet`), through the LCX component.
3. **Synthetic fixture assertion:** LCX outlet (`outlet`) -> Cooling Unit warm-return input (`inlet`), across synthetic physical hose B.
4. **Synthetic fixture assertion:** Cooling Unit warm-return input (`inlet`) -> Cooling Unit cold output (`outlet`), through the Cooling Unit component.

A query starting at the Cooling Unit cold output must return all four directed steps in that order, identify hose A and hose B for steps 1 and 3, and explicitly include the closing transfer inside the Cooling Unit.

##### 6. Negative and persistence acceptance cases

- Reverse hose A's stored endpoint order, then hose B's independently. The directed result must remain unchanged.
- Reverse a transfer relationship's source and target. Directional traversal must change, demonstrating that transfer direction is independent of physical endpoint storage order.
- Remove a referenced hose; mismatch its endpoints; classify it as electrical; omit the reference; or use a non-port endpoint. The step must be rejected or excluded with a clear validation result.
- Remove the medium, segment kind, component/connection reference, or validated port role. The incomplete step must not qualify for the path.
- Save and reload. Transfer IDs, ordered endpoints, metadata, provenance, component and connection references, and the queried ordered path must survive round-trip.
- Include electrical supply and fan connections in the same fixture and verify they are absent from the coolant route.
- Mark a transfer direction unknown. The result must become incomplete/unresolved rather than inferring direction from physical endpoint order or claiming a closed loop.
- Create two distinct valid routes between the same endpoints and verify that ambiguity is reported rather than silently resolving to one route.

**Decision trigger:** If a required rule cannot be validated using existing canonical ports, connections, relationships, properties, and provenance, record the smallest failing case and the exact unexpressible constraint for Planning. No application, schema, ontology, source-code, or test changes are authorized under this specification.

##### Planning acceptance checkpoint (2026-10-12)

**Planning disposition:** ACCEPTED as a bounded proposed research contract. Acceptance is conceptual/documentation-level only, not implementation authorization and not a claim that production validation exists.

**Boundaries retained:** The medium-scoped `fluid_roles` map remains a proposed contract; the existing `SemanticPort.properties` container does not currently validate its schema, medium keys, or role values. Physical connection endpoint order remains non-directional. The Cooling Unit/LCX four-step graph remains synthetic acceptance-fixture data, not manufacturer-verified or installed topology. No new canonical entity, application change, test change, or broad ontology expansion is authorized.

**Next Research action:** Continue source-evidence work on the documented kink/blockage print-pause detector and signal path; the conflicting published 50 mm bend-radius guidance; and the exact installed cooling kit, hose/fitting arrangement, wiring, and firmware integration. Preserve source evidence and uncertainties in this existing record. Do not make this work a prerequisite for Promega wiring. Return to Planning if a concrete test or implementation case shows a constraint the current model cannot express or validate coherently.

## Shared Documentation, Encoding, and Display Standard -- Research Proposal (2026-10-11)

**Status:** Planning adopted the core recommendations on 2026-10-11, subject to the bounded enforcement and workflow decisions recorded below. Broader configuration changes, repository-wide cleanup, and historical-file rewrites remain outside this authorization.

### Purpose and scope

Define a small, cross-workstream method for keeping repository documents accurate, portable, readable, and safe to copy into tools. Separate four different things that can look alike during an incident: file bytes, decoded characters, Git normalization, and presentation by a terminal/editor/Markdown renderer.

This is a documentation and workflow proposal. It does not change Machine Builder architecture or authorize broad normalization of existing files.

### Verified repository baseline

Checked against local HEAD, fetched `origin/main`, and live remote `main` at `274a1cd5432fb3803dc351c4b3074c86d6689ccf` on 2026-10-11:

- `.gitattributes` contains `* text=auto`. Git reports the `text` attribute as `auto` and no explicit `eol` attribute for the inspected Markdown files.
- Effective `core.autocrlf=true` is configured in `C:/Program Files/Git/etc/gitconfig`; this is system-level Git configuration, not a repository-local declaration.
- There is no root `.editorconfig`.
- The standards index and Research handoff both decode as valid UTF-8 without a BOM, use consistent CRLF working-tree line endings, and end with a newline.
- The unrelated, pre-existing worktree modification is `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`. It is outside this research scope and must be preserved.
- The 2026-10-05 repository audit recorded LF-normalized index content with CRLF commonly produced in Windows working trees, plus six then-observed mixed-line-ending files and two historical UTF-8-with-BOM files. That was a dated inventory, not a present-day scan of every file; do not treat it as authorization for broad cleanup.

The prior audit transcript rendered some examples as `â€”` and `Ã—`. That display alone does not prove whether the source contained those code points or a display/decoding path altered them. Any repair must first inspect the actual file characters and Git diff. Do not rewrite the historical passage based only on a console excerpt.

### Recommended shared defaults

#### 1. Encoding and Unicode

- Use UTF-8 without BOM for new Markdown research notes, handoffs, and ordinary documentation unless a specific consuming tool requires otherwise.
- ASCII is a valid subset of UTF-8, not a separate repository encoding policy. Readable Unicode punctuation and symbols are acceptable in prose where intentional. Prefer plain ASCII punctuation in executable commands, identifiers, and copy/paste instructions to reduce ambiguity.
- A file that decodes as valid UTF-8 is not necessarily semantically correct. Mojibake can itself consist of valid Unicode characters encoded as valid UTF-8. Compare suspicious text against the intended character or trusted source, and report code points when display is uncertain.
- Preserve a historical file's existing BOM or encoding until an intentional, reviewable edit has a reason to change it. Do not use a new-file default as a reason to rewrite unrelated files.
- PowerShell encoding rules are version-dependent. Windows PowerShell 5.1 and PowerShell 7 do not share all file-reading, file-writing, redirection, and native-pipeline defaults. In Windows PowerShell 5.1, do not rely on the implicit encoding of `Out-File`, `>`, `>>`, or `Set-Content` to create a UTF-8 repository file. Specify encoding deliberately or use an exact-byte method when preservation is required.
- For PowerShell source containing non-ASCII characters that must be parsed by Windows PowerShell 5.1, follow Microsoft's 5.1 encoding guidance; a UTF-8 BOM may be required for reliable decoding. Do not apply the Markdown no-BOM rule indiscriminately to executable scripts.
- `$OutputEncoding` concerns text sent from PowerShell to native programs; it does not set the encoding used by file redirection or every file-writing cmdlet.

#### 2. Line endings, whitespace, and end-of-file

- Treat Git-normalized text in the index as the version-controlled baseline. The existing `* text=auto` attribute supports text line-ending normalization; the current system `core.autocrlf=true` explains why CRLF Windows working trees can coexist with normalized index content.
- Preserve a target file's existing working-tree line-ending style during a surgical edit. A file should not be left with mixed CRLF, LF-only, or CR-only sequences. Do not normalize an entire file merely to make a small content change.
- New or deliberately rewritten Markdown should have a final newline. Do not silently remove a final newline from an existing file.
- Avoid tabs for Markdown indentation and visual alignment; use spaces. Do not add trailing spaces. For Markdown hard breaks, do not rely on two trailing spaces; prefer normal paragraphs, lists, or a clearly intentional alternative.
- `git diff --check` is required after edits. It detects introduced whitespace errors and conflict markers under Git's applicable rules; it is not an encoding validator, Unicode correctness check, or proof that no characters were lost.

#### 3. Markdown structure and durable research records

- Use Markdown heading markers rather than bold text as simulated headings. Keep one clear document title followed by a logical `##` / `###` hierarchy.
- Separate paragraphs and block structures with blank lines. Use proper list syntax and actual Markdown tables only for genuinely tabular comparisons.
- Fence code with matching delimiters and an appropriate language label. If an example contains the same fence marker, use a longer outer fence. Executable PowerShell presented to the user must follow `CHAT_WORKFLOW.md` Section 16 and `Copy/Paste Command Formatting Safety`: one continuous `powershell` block with no fence metadata, no nested Markdown fences, no interleaved prose, and no invisible steps the user must remove.
- Prefer complete, locally meaningful research checkpoints over fragments. Dates should use `YYYY-MM-DD`; if a checkpoint needs a time, include the timezone. Record source title/organization, identifier or version, URL, access/retrieval date, relevant section/page, and what the source does and does not establish where available. Keep facts, observations, inferences, and unresolved questions distinct.
- Do not hard-wrap prose to mimic a particular chat or terminal width. Markdown renderers can visually wrap paragraphs differently from the stored source. A visual wrap is not evidence that a newline exists in the file.

#### 4. Display, copy/paste, and rendering

- Diagnose suspicious output in this order: inspect bytes and decoding; inspect actual code points; compare the worktree content and Git diff; then inspect terminal/renderer/font behavior. Do not start by replacing visible odd characters.
- Windows console input/output code pages, PowerShell's native-pipeline encoding, and terminal font availability are separate settings. A missing glyph or font fallback changes how text looks, not the file's stored bytes. Markdown itself is not a portable way to prescribe a viewer's font.
- When unusual punctuation appears corrupted, display the suspect characters as ASCII code-point labels such as `U+2014` instead of retransmitting the character through a potentially lossy console. Compare against the expected text and source before editing.
- When output seems to have missing spaces or truncated text, compare `git diff`, explicit line counts, and the actual decoded file. Terminal wrapping, clipped console output, and chat presentation are not evidence that spaces or lines are missing in the repository. Do not paste visually wrapped excerpts back into a tracked file as though they were the original source.
- Copy/paste instructions must be complete and literal. Use straight quotes and ordinary hyphens in commands; keep explanation outside the executable block; never require the user to repair formatting after copying.

### Short read-only diagnostic procedure

For a file whose encoding, newline, or display is in question:

1. Capture `git status --short --branch` and confirm the expected commit and worktree changes before touching anything.
2. Inspect `git ls-files --eol -- path/to/file`, `git check-attr text eol -- path/to/file`, and `git config --show-origin --get core.autocrlf`. These establish the applicable Git attributes and checkout configuration; they do not prove character encoding.
3. Read the file as bytes with `[System.IO.File]::ReadAllBytes()`. Check the UTF-8 BOM bytes (`EF BB BF`), then decode with a strict UTF-8 decoder such as `New-Object System.Text.UTF8Encoding($false, $true)`. A decoding exception means the content is not valid UTF-8 under that check.
4. Count CRLF, LF-only, and CR-only sequences and check the final newline. Compare the working-tree content against the intended source. For a rigorous character/display check, print the numeric Unicode code points of the suspect line rather than displaying its characters.
5. Inspect `git diff -- path/to/file` and run `git diff --check`. If the question is whether normalized content differs from the current commit, `git hash-object --path=path/to/file path/to/file` can be compared with `git rev-parse HEAD:path/to/file`; matching hashes indicate the cleaned content matches that committed blob. A differing hash means content differs, not necessarily that corruption occurred.
6. Only after the stored characters are shown to be correct should terminal code pages, `$OutputEncoding`, font glyph support, Markdown preview, visual wrapping, or chat rendering be treated as the likely source of the appearance.

All checks should be read-only until the cause and proposed correction are established. Avoid temporary files and broad rewrites when direct inspection suffices.

### Evaluation of repository enforcement options

**Existing `.gitattributes`:** Keep `* text=auto` unchanged for this proposal. It concerns Git text detection and line-ending normalization, not UTF-8 validation. Do not run `git add --renormalize .` or introduce a repository-wide line-ending conversion as part of this work.

**Adopted `.editorconfig`:** Planning authorized this minimal root file with the following exact content:

```ini
root = true

[*.md]
indent_style = space
insert_final_newline = true
```

No other properties are authorized in this first change. In particular, omit `end_of_line`, `trim_trailing_whitespace`, and `charset`. This scoped change does not alter Git line-ending behavior.

**`.gitattributes` and line endings -- deferred:** Planning explicitly excluded a Git-attribute or line-ending change from this adoption. Preserve the existing `* text=auto` rule and current system-level `core.autocrlf=true` behavior. Evaluate explicit Markdown LF enforcement only in a separate decision if a demonstrated cross-platform need arises.

**Workflow safety gap and Planning ownership:** Planning owns any edit to `CHAT_WORKFLOW.md`; Research must not edit it as part of this adoption. The concise insertion proposed for the existing `Paste-Ready PowerShell Safety Refinement` guidance is:

> Before correcting suspected corrupted text, inspect the actual file bytes/decoding or character code points and compare the file/Git diff with the intended source. Never repair text solely because a terminal, chat rendering, font, or wrapped console excerpt makes it look wrong. Distinguish verified stored-content defects from presentation artifacts.

This wording is a proposal for Planning to apply in the existing guidance, not an additional workflow section.

### Official references checked on 2026-10-11

- Microsoft, [about_Character_Encoding -- Windows PowerShell 5.1](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding?view=powershell-5.1): version-dependent file and command encoding behavior.
- Microsoft, [Out-File -- PowerShell 7.5](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/out-file?view=powershell-7.5): explicit encoding choices and the UTF-8-no-BOM default in modern PowerShell.
- Microsoft, [Windows Console Code Pages](https://learn.microsoft.com/en-us/windows/console/console-code-pages): input and output code pages are separate; Unicode is recommended for new command-line applications.
- Microsoft, [Windows Terminal profile appearance](https://learn.microsoft.com/en-us/windows/terminal/customize-settings/profile-appearance): terminal font configuration and fallback.
- Git, [gitattributes](https://git-scm.com/docs/gitattributes): `text=auto`, normalization, and explicit `eol` behavior.
- Git, [git-config](https://git-scm.com/docs/git-config): `core.autocrlf` and `core.eol` behavior.
- Git, [git-diff](https://git-scm.com/docs/git-diff): the scope of `--check` whitespace/conflict-marker checking.
- EditorConfig, [Specification](https://spec.editorconfig.org/): `charset`, `insert_final_newline`, `indent_style`, `end_of_line`, and `trim_trailing_whitespace`.
- CommonMark, [Version 0.31.2 specification](https://spec.commonmark.org/0.31.2/): Markdown line endings, headings, lists, and fenced code.
- GitHub Docs, [Basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax): Markdown rendering, including the distinction between a source newline and a rendered line break.

### Planning decision and bounded adoption (2026-10-11)

Planning adopted the core recommendations of this research on 2026-10-11, within these explicit boundaries:

- Add only the root `.editorconfig` shown above, with `root = true`, Markdown `indent_style = space`, and `insert_final_newline = true`.
- Defer `end_of_line`, `trim_trailing_whitespace`, and `charset` properties. Preserve existing file encodings unless an intentional, reviewable edit justifies a change.
- Leave `.gitattributes`, `core.autocrlf`, Git line-ending behavior, and historical files unchanged. Do not perform repository-wide normalization.
- Planning owns the actual `CHAT_WORKFLOW.md` edit. The concise proposed insertion is recorded above; Research must not edit that workflow as part of this adoption.

The authorized change is limited to the root `.editorconfig`, confirmed local text corrections in this section, and the Research handoff update. No source, tests, ontology, or unrelated documentation changes are authorized by this decision.

The next Research mission remains the queued directed-fluid-transfer query-contract evaluation versus undirected physical connections. Promega wiring remains the active implementation priority.
