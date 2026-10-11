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

After preserving this catalog report, investigate a real manufacturer's liquid-cooled hotend/coolant-loop example. Keep separate:

- physical coolant path, ports, hoses, fittings, flow direction, pump, reservoir, radiator, and cold plate where applicable;
- electrical power and signal wiring for pumps, fans, sensors, and control devices;
- firmware-facing sensors, outputs, settings, and control semantics;
- manufacturer facts, source-derived inference, and unresolved as-built details.

Initial standards leads are ISO 1219-1 and ISO 1219-2 for fluid-power symbols/diagrams, and ISO 14617-1 and ISO 14617-2 for graphical symbols. Confirm the exact scope and applicability before relying on them. First test whether the existing canonical model and the `SemanticRelationship`/`SemanticConnection` distinction adequately represent the actual case. Do not add coolant/flow ontology entities merely because the example is new.
