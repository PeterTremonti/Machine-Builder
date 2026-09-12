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