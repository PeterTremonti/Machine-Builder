# Machine Builder Open Questions

## 1. Purpose

This document records unresolved questions that materially affect Machine Builder research, ontology, architecture, or implementation.

An open question is not necessarily a problem.

Some questions are intentionally left unresolved because:

- more evidence is needed;
- a real machine stress case has not yet been encountered;
- multiple valid approaches remain;
- the implementation does not yet require the answer;
- the concept is better deferred than prematurely formalized.

The purpose of this document is to preserve those questions so they can be resolved deliberately rather than rediscovered later.

---

# 2. Question Status

Open questions may have the following states:

```text
Open
Investigating
Blocked
Deferred
Resolved
Superseded
Open

Recognized but not actively being investigated.

Investigating

Currently being researched or tested.

Blocked

Cannot be resolved until another dependency is available.

Deferred

Intentionally postponed because it is not currently needed.

Resolved

A decision has been made and recorded elsewhere.

Superseded

The question has been replaced by a different question or architectural direction.

3. Priority

Questions may be classified as:

Critical
High
Medium
Low
Deferred

Priority reflects architectural impact, not urgency in the current implementation sprint.

4. Ontology Foundation Questions
Q-001 — What Is the Exact Formal Nature of an Object?

Status: Open

Priority: High

Question

Is Object primarily:

an identity-bearing entity;
a generic semantic node;
a superclass-like abstraction;
an occurrence;
or a combination of these?
Current Direction

Object is an identifiable modeled entity.

The project currently prefers identity plus Classification rather than a universal class hierarchy.

What Would Resolve It?

Further ontology modeling and stress testing against:

physical components;
functions;
abstractions;
measurements;
resources;
relationships.
Q-002 — How Much Identity Belongs in Object Versus Occurrence?

Status: Open

Priority: High

Question

How should the ontology formally distinguish:

Product
Product Version
Physical Occurrence
Machine Component
Current Direction

Machine Component is the preferred terminology for actual machine-specific hardware occurrences.

Open Issue

A formal occurrence model may be useful beyond hardware.

Q-003 — Can Every Relevant Entity Be Modeled as an Object?

Status: Open

Priority: Medium

Question

Should things such as:

Function;
Role;
Property;
Measurement Result;
Constraint;
Requirement;

all be modeled as Objects in the implementation, or should some exist outside the Object abstraction?

Current Direction

The semantic ontology distinguishes them conceptually even if an implementation later represents some of them using common infrastructure.

Q-004 — What Exactly Is an Aspect?

Status: Open

Priority: High

Question

How closely should Machine Builder's Aspect model follow IEC 81346 terminology and structuring?

Current Direction

Aspect is an engineering structuring/view dimension.

Open Issues

Need to determine:

which aspects are inherent;
which are project-defined;
whether aspects may overlap;
how aspect membership affects identification;
whether an object can have unlimited aspects.
5. Property Questions
Q-005 — What Is the Formal Property Model?

Status: Open

Priority: High

Question

How should Properties represent:

scalar values;
enumerations;
ranges;
units;
dimensions;
complex structures;
arrays;
relationships;
calculated values;
uncertainty;
validity.
Current Direction

Properties need provenance and units where appropriate.

Open Issue

Exact property representation should not be frozen until enough engineering domains have been tested.

Q-006 — How Should Units Be Represented?

Status: Open

Priority: High

Question

Should units be:

strings;
normalized identifiers;
a controlled vocabulary;
a unit ontology;
a library reference?
Important Requirements

The model eventually needs to support:

mm
mm/min
A
V
°C
N
N·m
steps/mm

while distinguishing physical dimensions from arbitrary firmware units.

Q-007 — How Should Dimensionless and Domain-Specific Units Work?

Status: Open

Priority: Medium

Question

How should the model treat quantities such as:

steps/mm;
steps/revolution;
ratios;
percentages;
firmware-specific units.
Open Issue

These are meaningful engineering quantities but are not always SI units.

Q-008 — How Should Ranges and Limits Be Modeled?

Status: Open

Priority: Medium

Question

Should a component property support:

nominal value
minimum
maximum
recommended range
absolute limit
operating range

as separate semantic properties?

6. Relationship Questions
Q-009 — Which Relationships Need First-Class Identity?

Status: Open

Priority: High

Question

When should a Relationship be represented as a first-class object rather than a simple typed edge?

Examples

Potentially complex relationships include:

Connection;
Mapping;
Mechanical coupling;
Role;
Calibration;
Safety implementation;
Controller assignment.
Current Direction

If a relationship has substantial properties, provenance, lifecycle, or context, it may need first-class identity.

Q-010 — Should implements and realizes Be Separate?

Status: Open

Priority: Medium

Question

Do these words represent materially different relationships?

implements
realizes
Current Direction

Keep both provisionally until standards and stress cases demonstrate whether one is sufficient.

Q-011 — Should connects_to Be Universal?

Status: Open

Priority: High

Question

Should one generic relationship represent:

electrical connection;
mechanical connection;
material connection;
fluid connection;
communication connection;

with a domain property?

Or should these be separate relationship types?

Current Direction

A common Connection concept is attractive, but domain-specific semantics must remain explicit.

Q-012 — Is Path a First-Class Concept?

Status: Open

Priority: Medium

Question

Should physical routes such as:

filament paths;
tubing;
cable routing;
fluid paths;
mechanical transmission paths

be modeled as identifiable Path objects?

Current Direction

Path appears useful for the CFS and wiring architecture, but its full scope is unresolved.

Q-013 — Should Physical Connection and Path Be Separate?

Status: Open

Priority: Medium

Question

For example:

Wire physically_connects A → B
Wire follows Path X

Should Path describe topology while Connection describes endpoint attachment?

Current Direction

This distinction appears useful but requires testing.

Q-014 — How Should Relationship Inverses Work?

Status: Open

Priority: Medium

Question

Should inverse relationships be:

stored;
derived;
query-only;
selected based on implementation requirements?

Example:

contains
part_of
Current Direction

Avoid unnecessary duplication unless there is a strong reason to store both.

Q-015 — How Should Relationship Cardinality Be Enforced?

Status: Open

Priority: High

Question

Should cardinality be enforced:

statically by schema;
dynamically by validation;
contextually;
through specialized rules?
Important Stress Cases
CoreXY;
multiple Z actuators;
multiple sensors;
multiple tools;
distributed controllers.
7. Provenance Questions
Q-016 — What Is the Exact Provenance Model?

Status: Open

Priority: High

Question

How should provenance represent:

source;
method;
date;
author;
version;
confidence;
evidence location;
assumptions;
calculations;
inference chain?
Current Direction

Provenance is first-class, but the exact structure remains unresolved.

Q-017 — How Should Conflicting Evidence Be Stored?

Status: Open

Priority: High

Question

When two sources disagree, should the model store:

Fact A
Fact B
Conflict
Resolution

as separate entities?

Current Direction

Conflicting evidence must not silently overwrite existing information.

Q-018 — How Should Confidence Be Represented?

Status: Open

Priority: Medium

Question

Should confidence be:

qualitative;
numeric;
probabilistic;
a controlled vocabulary;
domain-specific?
Current Direction

Qualitative confidence is sufficient initially.

A more formal model can be added later if justified.

Q-019 — How Should Inference Chains Work?

Status: Open

Priority: Medium

Question

If:

A → inference → B
B → inference → C

how should C retain lineage back to A?

Requirement

The final conclusion should remain explainable.

8. Motion and Kinematics Questions
Q-020 — What Exactly Is the Formal Axis Model?

Status: Open

Priority: High

Question

Should Axis represent:

a coordinate axis;
a machine motion;
a controllable degree of freedom;
a firmware motion channel;
one of several overlapping concepts?
Current Direction

Axis represents machine motion/coordinate semantics.

Q-021 — How Should Joint and Axis Relate?

Status: Open

Priority: High

Question

What formal relationship connects:

Joint
Link
Actuator
Axis
Coordinate Frame
Stress Cases
CoreXY;
articulated robots;
belt printers;
CNC rotary axes.
Q-022 — How Should Kinematics Be Represented?

Status: Open

Priority: High

Question

Should kinematics be:

a relationship;
a transformation object;
a function;
a subsystem;
a graph;
some combination?
Current Direction

Kinematic relationships should be explicit and support transformations.

Q-023 — How Should Mechanical Transmission Be Modeled?

Status: Open

Priority: Medium

Question

How should the ontology represent:

gears;
pulleys;
belts;
screws;
chains;
linkages;
differentials;
couplings?
Requirement

Mechanical transmission must support derivation of motion relationships and ratios.

9. Coordinate Questions
Q-024 — How Formal Should Transform Representation Be?

Status: Open

Priority: High

Question

Should Transforms use:

homogeneous matrices;
translation + rotation;
quaternions;
Euler representations;
implementation-specific structures?
Current Direction

Keep the semantic Transform distinct from its storage representation.

Q-025 — How Should Non-Euclidean or Machine-Specific Coordinates Be Handled?

Status: Open

Priority: Medium

Question

How should the system represent unusual coordinate systems such as:

belt-printer coordinates;
wrapped/rotary coordinates;
machine-specific kinematic coordinates?
Stress Case

IR3 is an important test.

10. Measurement Questions
Q-026 — Should Measurement and Measurement Result Be Separate Objects?

Status: Open

Priority: Medium

Question

Is this distinction necessary:

Measurement
    ↓
Measurement Result

or can a Measurement Result directly represent the event/result of measurement?

Current Direction

The semantic distinction is useful, but implementation may simplify the representation.

Q-027 — How Should Uncertainty Be Represented?

Status: Open

Priority: Medium

Question

Should uncertainty be:

a property;
an object;
an interval;
a probability distribution;
a domain-specific structure?
Evidence

VIM/JCGM terminology provides a useful foundation.

Q-028 — How Should Calibration Be Modeled?

Status: Open

Priority: High

Question

Should Calibration be:

a Function;
a Process;
a Procedure;
a Result;
a relationship between measurement and configuration?
Current Direction

Calibration is likely a process involving measurement, derivation, and resulting configuration changes.

11. Function and Process Questions
Q-029 — Is Activity Needed as a First-Class Concept?

Status: Open

Priority: Medium

Question

Do Task, Process, Operation, Action, and Procedure adequately cover activity semantics?

Current Direction

Do not add Activity merely because standards or common language use the term.

Add it only if stress cases require a meaningful distinction.

Q-030 — How Should Function Relate to Capability?

Status: Open

Priority: High

Question

Can:

Capability

be expressed as an attribute of a Function, or does it need independent identity?

Current Direction

Capability and Function are conceptually distinct.

Q-031 — How Should Functions Be Organized?

Status: Open

Priority: High

Question

Should Functions have:

hierarchies;
decomposition;
composition;
inputs/outputs;
preconditions;
postconditions;
resources;
implementations?
Current Direction

Function must support meaningful relationships without becoming a universal parent of all executable concepts.

Q-032 — How Should Operations Relate to Functions?

Status: Open

Priority: High

Question

Can an Operation:

invoke a Function;
realize a Function;
be an instance of a Function;
contain Actions that implement a Function?
Importance

This affects process planning and firmware generation.

Q-033 — How Should Procedures Relate to Operations?

Status: Open

Priority: Medium

Question

Should Procedure describe:

how an Operation is performed

while Operation describes:

what bounded work is performed
Current Direction

Yes conceptually, but the formal relationship remains open.

12. Control Questions
Q-034 — Is Control Function a Specialized Function?

Status: Open

Priority: Medium

Current Direction

Yes.

Open Issue

Need to define the formal relationship without making Control Function synonymous with firmware control code.

Q-035 — How Should Control Loops Be Represented?

Status: Open

Priority: High

Question

Should Control Loop be:

a structural object;
a relationship pattern;
a Function;
a subsystem;
a graph of control relationships?
Current Direction

Control Loop is a meaningful structural concept.

Q-036 — How Should Open-Loop Control Be Represented?

Status: Open

Priority: Medium

Question

Can the control model naturally represent systems without feedback?

Requirement

The ontology must not require feedback for all control.

Q-037 — How Should Multiple Feedback Sources Work?

Status: Open

Priority: Medium

Question

How should the model represent:

multiple sensors;
redundant sensors;
cascaded loops;
observers/estimated measurements?
13. Controller and Resource Questions
Q-038 — What Exactly Is a Controller Resource?

Status: Open

Priority: High

Question

Should Controller Resource include only physical resources, or also:

software resources;
communication capabilities;
processing capacity;
memory;
timers;
firmware channels?
Current Direction

Controller Resource is a finite capability provided by a Controller.

Q-039 — How Should Shared Resources Be Modeled?

Status: Open

Priority: High

Stress Cases
shared timers;
multiplexed pins;
shared ADC channels;
shared communication buses;
alternate pin functions.
Q-040 — How Should Distributed Controllers Be Modeled?

Status: Open

Priority: High

Stress Cases
SV08;
toolhead controllers;
CFS;
CAN nodes;
remote I/O.
Current Direction

Controllers should participate in a larger machine rather than being assumed to be one central board.

14. Connectivity Questions
Q-041 — What Exactly Is a Port?

Status: Open

Priority: High

Question

How broad should Port be?

Possible interpretations include:

semantic interface;
connection endpoint;
physical interface;
logical interface.
Current Direction

Port is a semantic interface endpoint.

Q-042 — How Should Ports Map to Connectors and Pins?

Status: Open

Priority: High

Question

Can:

Port
    maps_to
Connector
    contains
Pin

represent all important cases?

Or are additional concepts required?

Q-043 — Can a Port Be Multi-Domain?

Status: Open

Priority: Medium

Question

Can one Port simultaneously provide:

power;
data;
signal;
mechanical attachment?
Example

A toolhead interface may carry both power and communication.

Q-044 — How Should Direction Be Modeled?

Status: Open

Priority: High

Question

Should direction belong to:

Port;
Connection;
Signal;
Flow;
logical mapping?
Requirement

Physical connectivity may be nondirectional while a logical signal is directional.

Q-045 — How Should Bundles and Harnesses Map to Individual Connections?

Status: Open

Priority: Medium

Question

How should the system represent:

Harness
    contains
Cable
    contains
Conductors

while also representing individual logical signals?

15. Flow and Signal Questions
Q-046 — Should Flow Exist as a Universal Concept?

Status: Deferred

Priority: Deferred

Question

Is a general Flow concept useful for:

filament;
coolant;
compressed air;
electricity;
data;
mechanical power?
Current Direction

Do not formalize until domain-specific requirements justify it.

Q-047 — Should Signal Exist as a Universal Concept?

Status: Deferred

Priority: Deferred

Question

Would a universal Signal concept clarify or confuse:

electrical signals;
communication data;
logical information;
commands;
feedback?
Current Direction

Keep domain-specific meanings distinct until evidence supports consolidation.

Q-048 — Is Command a Canonical Concept?

Status: Open

Priority: Medium

Question

Should Command be distinct from:

Action;
Signal;
Request;
Operation;
Control Output?
Current Direction

Command may represent intent sent to a machine or subsystem, but formal semantics are not yet finalized.

16. Process and Tool Questions
Q-049 — How Formal Should Process Modeling Become?

Status: Open

Priority: Medium

Question

How much of:

process;
task;
operation;
workingstep;
action;
procedure

should become canonical machine architecture?

Current Direction

Support enough to connect machine capabilities to manufacturing tasks without prematurely becoming a full CAM system.

Q-050 — How Should Tool and Toolhead Relate?

Status: Open

Priority: Medium

Question

Can a Toolhead:

contain multiple Tools;
select one Tool;
change Tools;
itself be a Tool?
Stress Cases
tool changers;
IDEX;
multi-tool systems;
CNC.
Q-051 — How Should Workholding Be Modeled?

Status: Open

Priority: Low

Question

Is Workholding simply a Machine Component Role, or is it a distinct concept?

Examples
build plate;
vice;
chuck;
clamp;
fixture.
17. Safety Questions
Q-052 — How Formal Should Safety Modeling Become in the First Releases?

Status: Open

Priority: Medium

Question

How much of the safety architecture should become executable or machine-checkable?

Current Direction

Safety concepts should be represented early enough to preserve architecture, but certification-grade analysis is not a v0.x requirement.

Q-053 — How Should Safety Functions Map to Components?

Status: Open

Priority: High

Question

Should a Safety Function explicitly reference:

sensors;
logic;
outputs;
actuators;
stopping behavior;
safe state?
Current Direction

Yes, but exact structure remains open.

Q-054 — How Should Safety Validation Be Represented?

Status: Open

Priority: Medium

Question

Should validation evidence be represented as:

Evaluation Results;
Test Procedures;
Test Results;
Evidence objects;
a dedicated Validation model?
18. Engineering Evaluation Questions
Q-055 — What Belongs in the Evaluation Engine?

Status: Open

Priority: High

Candidate Areas
electrical compatibility;
current limits;
voltage drop;
wire sizing;
thermal limits;
motion limits;
controller resources;
safety requirements;
component compatibility.
Current Direction

Evaluation should consume canonical model information rather than define the machine ontology itself.

Q-056 — How Should Engineering Rules Be Versioned?

Status: Open

Priority: Medium

Question

Should each evaluation rule retain:

standard edition;
rule version;
assumptions;
source;
date;
calculation method?
Current Direction

Yes.

Q-057 — How Should Stale Evaluation Results Be Detected?

Status: Open

Priority: High

Question

If an input changes, how does the system know which evaluation results are no longer valid?

Candidate Mechanisms
dependency graph;
provenance lineage;
content hashes;
explicit invalidation;
recalculation markers.
19. Firmware Questions
Q-058 — How Should Firmware Capabilities Be Modeled?

Status: Open

Priority: High

Question

How should the system represent:

Firmware supports feature X
Firmware partially supports feature Y
Firmware requires workaround Z
Requirement

Generation must distinguish unsupported from unconfigured.

Q-059 — How Should Firmware Version Differences Be Modeled?

Status: Open

Priority: High

Question

Should mappings be tied to:

exact firmware version;
version range;
capability declaration;
semantic feature set?
Current Direction

Version applicability must be retained.

Q-060 — How Should Lossy Translation Be Represented?

Status: Open

Priority: High

Question

How should Machine Builder indicate when firmware cannot represent part of the canonical model?

Desired Behavior

Avoid silent information loss.

Potential statuses:

Unsupported
Approximation
Ignored
Requires Manual Configuration
Not Representable
20. Runtime Questions
Q-061 — How Should Runtime State Connect to the Canonical Model?

Status: Open

Priority: Medium

Question

Should runtime state:

attach directly to canonical Objects;
exist as separate state snapshots;
be time-series data;
be a hybrid?
Q-062 — How Should Historical Runtime State Be Stored?

Status: Open

Priority: Low

Question

Will the system eventually need:

event history;
telemetry;
snapshots;
fault history;
calibration history?
21. Temporal Questions
Q-063 — How Should Machine History Be Modeled?

Status: Open

Priority: Medium

Question

How should the model represent:

Component installed
Component removed
Firmware changed
Configuration changed
Machine modified

without destroying historical truth?

Q-064 — How Should Configuration Versions Relate to Machine Revisions?

Status: Open

Priority: Medium

Question

Should:

Machine Revision
Configuration Revision
Firmware Revision
Hardware Revision

be independent versions linked through context?

Current Direction

Likely yes, but formal version context is not yet defined.

22. Visual Builder Questions
Q-065 — How Much Visual State Should Be Persisted?

Status: Open

Priority: Medium

Candidate Data
node positions;
node size;
grouping;
collapsed state;
routing;
visibility;
viewport;
selection.
Current Direction

Persist presentation state separately from canonical semantics.

Q-066 — Can One Object Have Multiple Visual Representations?

Status: Open

Priority: High

Question

Can one canonical Object appear:

in a machine overview;
electrical view;
functional view;
wiring view;
3D view

simultaneously or independently?

Current Direction

Yes.

This is one of the major reasons the visual model is separate.

Q-067 — How Should Grouping Work?

Status: Open

Priority: Medium

Question

Is a visual group:

purely presentation;
a semantic subsystem;
either depending on explicit context?
Current Direction

Visual grouping must not automatically create a semantic Subsystem.

23. Storage and Implementation Questions
Q-068 — What Storage Model Should Be Used?

Status: Deferred

Priority: Deferred

Question

Should the eventual system use:

relational database;
document database;
graph database;
embedded store;
hybrid model?
Current Direction

Do not decide until ontology and relationship requirements are mature.

Q-069 — What Should the Canonical Serialization Format Be?

Status: Open

Priority: Medium

Question

What format should support:

human readability;
provenance;
versioning;
relationships;
extensibility;
round-tripping?

Candidates may include:

JSON;
YAML;
XML;
specialized graph serialization;
custom structured format.

No final choice has been made.

Q-070 — How Much Should Schema and Ontology Be Coupled?

Status: Open

Priority: High

Question

Should implementation schema directly mirror ontology classes, or should implementation use a more flexible internal representation?

Current Direction

Semantic ontology should constrain meaning without forcing one implementation architecture.

24. Knowledge Graph Questions
Q-071 — What Problems Actually Require a Knowledge Graph?

Status: Deferred

Priority: Deferred

Question

Which future features genuinely benefit from graph technology beyond a well-structured canonical model?

Potential candidates:

cross-machine knowledge;
standards relationships;
parts compatibility;
provenance traversal;
external knowledge.
Q-072 — How Should External Knowledge Be Linked?

Status: Open

Priority: Low

Question

How should Machine Builder reference:

standards;
manufacturer documents;
firmware source;
external identifiers;
product catalogs?
25. Standards Questions
Q-073 — When Should Additional Standards Be Researched?

Status: Resolved

Priority: High

Decision

Do not conduct an unrestricted standards hunt.

When a genuinely new semantic domain appears:

identify the domain;
conduct a targeted standards scan;
record relevant standards;
incorporate useful distinctions where justified.
Related

decisions/DECISION_LOG.md

Q-074 — How Should Standard Versions Be Tracked?

Status: Open

Priority: Medium

Question

Should each standard reference retain:

organization
standard number
edition
publication date
status
applicability
source
Current Direction

Yes.

26. Research Process Questions
Q-075 — When Is a Concept Mature Enough for the Ontology?

Status: Open

Priority: High

Question

What evidence threshold is sufficient?

Current Direction

A concept should generally have:

a clear definition;
non-equivalence distinctions;
real-machine evidence;
relevant relationships;
sufficient research support;
no known unresolved contradiction that undermines its use.
Q-076 — How Should Ontology History Be Maintained?

Status: Open

Priority: Medium

Question

When a major ontology concept changes, should the project preserve:

snapshots;
diffs;
decision records;
all three?
Current Direction

Major changes should be traceable.

Q-077 — How Should Research Findings Be Promoted?

Status: Open

Priority: Medium

Question

What threshold moves information from:

Research Evidence
    ↓
Candidate Concept
    ↓
Accepted Ontology
    ↓
Implementation Requirement

into the next stage?

27. Current Highest-Priority Questions

The questions most likely to affect the next ontology phase are:

Q-005  Formal Property Model
Q-009  First-Class Relationships
Q-011  Universal / Domain-Specific Connections
Q-015  Relationship Cardinality
Q-016  Provenance Model
Q-020  Formal Axis Model
Q-022  Kinematic Representation
Q-028  Calibration Modeling
Q-031  Function Organization
Q-032  Operation ↔ Function
Q-038  Controller Resource
Q-039  Shared Resources
Q-041  Port Definition
Q-042  Port ↔ Connector ↔ Pin
Q-044  Direction
Q-055  Evaluation Engine Scope
Q-058  Firmware Capabilities
Q-059  Firmware Version Differences
Q-060  Lossy Translation
Q-075  Ontology Maturity Threshold

These should receive attention before lower-impact implementation schema questions.

28. Questions Intentionally Deferred

The following are recognized but should not currently block progress:

Universal Flow
Universal Signal
Universal Channel
Knowledge Graph Storage
Database Technology
Universal State Model
Detailed Runtime History
Advanced 3D Geometry Storage
Full CAM Process Ontology
Certification-Grade Safety Automation

These should be revisited when a concrete requirement makes them relevant.

29. Resolution Rule

When an open question is resolved:

Record the decision.
Update the relevant architecture document.
Update the ontology document if necessary.
Update this question to Resolved.
Record the decision identifier.
Update implementation handoffs where applicable.

Example:

Q-041 Port Definition
    ↓
Resolved by D-XXX
    ↓
Update:
    ONTOLOGY_CURRENT.md
    RELATIONSHIP_MATRIX.md
    implementation handoff

The question should remain in history rather than disappearing.

30. Final Research Principle

Open questions are not failures.

They are a deliberate mechanism for preventing the project from making unsupported assumptions.

The preferred sequence is:

Question
    ↓
Evidence
    ↓
Stress Test
    ↓
Decision
    ↓
Ontology / Architecture
    ↓
Implementation

When evidence is insufficient, the correct answer is often:

Not yet known.

rather than an invented certainty.