# Machine Builder Deferred Research

## 1. Purpose

This document records research topics that are recognized as useful or likely to become necessary, but are intentionally not part of the current research priority.

Deferred does not mean rejected.

A topic may be deferred because:

- the core ontology is not mature enough;
- implementation does not currently require it;
- the research would be premature;
- another concept must be resolved first;
- the engineering domain is too specialized for the current milestone;
- additional real-machine evidence is needed.

The purpose is to prevent useful ideas from being forgotten while also preventing them from distracting the current architecture work.

---

# 2. Deferral Principle

The project should distinguish:

```text
Needed Now
    ↓
Active Research

Useful Later
    ↓
Deferred Research

Interesting but Unnecessary
    ↓
Reference / Archive

Known Wrong Direction
    ↓
Rejected

A deferred concept should remain visible without becoming an implementation requirement.

3. Current Core Priority

The current research priority remains:

Canonical Machine Model
        ↓
Ontology Refinement
        ↓
Relationship Constraints
        ↓
Provenance
        ↓
Stress Testing
        ↓
Implementation Handoffs

Research outside these areas should normally be deferred unless it exposes a problem in the current architecture.

4. Deferred Research Categories

Current deferred categories include:

Advanced Electrical Engineering
Advanced Safety Engineering
Formal Kinematics
Advanced Process Modeling
Advanced Tooling
Runtime / Telemetry
Temporal Modeling
Advanced Firmware Translation
Knowledge Graphs
3D Machine Representation
CAD Integration
CAM Integration
Electrical CAD Integration
Industrial Interoperability
Advanced Diagnostics
Formal Calibration
Advanced Catalog Engineering

The order is not necessarily the order in which these will eventually be researched.

5. Advanced Electrical Engineering
Status

Deferred.

Reason

The canonical architecture can already represent:

components;
ports;
connections;
controller resources;
electrical properties.

Detailed electrical engineering analysis should not block ontology development.

Future Topics

Potential future research includes:

circuit topology;
conductor sizing;
ampacity;
voltage drop;
short-circuit current;
overcurrent protection;
protective bonding;
grounding;
shielding;
connector ratings;
insulation;
temperature derating;
current-carrying conductor count;
wire routing;
termination limits.
Important Principle

Voltage and current alone are not sufficient to determine wire suitability.

Future evaluation must consider the complete relevant engineering context.

Relevant Standards

Likely future references include:

IEC 60204-1
Relevant electrical installation standards
Connector-specific standards
Conductor / cable standards

The exact standards set should be researched when this domain becomes active.

6. Advanced Safety Engineering
Status

Deferred beyond foundational ontology.

Current Support

The architecture already recognizes:

Hazard
Risk
Risk Reduction Requirement
Safety Function
Safety-Related Control Implementation
Validation
Safe State
Future Research

Potential topics include:

Performance Level;
Safety Integrity Level;
category architecture;
diagnostic coverage;
mean time to dangerous failure;
PFHd;
common-cause failures;
fault exclusion;
redundancy;
safety validation;
safety-related software;
proof testing.
Important Boundary

Certification-grade safety analysis is not a current v0.x implementation requirement.

The ontology should preserve the concepts needed to support such analysis later without pretending that the current software performs certification.

7. Formal Kinematics
Status

Deferred beyond current conceptual modeling.

Current Support

The architecture already distinguishes:

Axis
Joint
Link
Actuator
Motor
Drive
Coordinate Frame
Transform
Kinematic Relationship
Future Research

Potential topics include:

homogeneous transforms;
forward kinematics;
inverse kinematics;
Jacobians;
coupled motion;
workspace;
singularities;
transmission ratios;
backlash;
compliance;
calibration;
dynamic modeling.
Stress Cases

Future kinematic research should include:

CoreXY
IR3
Robotic arms
Rotary CNC
Delta mechanisms
SCARA
Parallel kinematics

The ontology should not become dependent on a particular mathematical implementation prematurely.

8. Advanced Coordinate Modeling
Status

Deferred.

Current Support

CoordinateFrame and Transform are established architectural concepts.

Future Topics
frame trees;
dynamic frames;
tool offsets;
work offsets;
probing frames;
camera calibration;
object frames;
moving reference frames;
synchronized multi-frame systems.
Potential External References

Future research may include:

ISO 9787;
ISO 17295;
robotics coordinate standards;
machine-tool coordinate conventions.
9. Advanced Measurement and Metrology
Status

Deferred.

Current Support

The ontology distinguishes:

Sensor
Measurand
Measurement
Measurement Result
Uncertainty
Feedback
Future Topics
uncertainty propagation;
calibration certificates;
traceability;
measurement systems;
repeatability;
reproducibility;
sensor models;
measurement error;
environmental compensation;
calibration history;
reference standards;
test equipment.
Potential Foundation

JCGM VIM remains the primary terminology reference.

10. Formal Calibration Model
Status

Deferred.

Reason

Calibration crosses multiple domains:

Measurement
    ↓
Analysis
    ↓
Derived Value
    ↓
Configuration
    ↓
Validation

A complete calibration model should not be created until the measurement, provenance, and property models are sufficiently mature.

Future Topics
calibration procedure;
calibration result;
reference artifact;
test conditions;
uncertainty;
derived correction;
configuration update;
calibration validity;
calibration history.
11. Advanced Process Modeling
Status

Deferred.

Current Support

The ontology currently distinguishes:

Capability
Function
Task
Process
Operation
Action
Procedure
Future Research

Potentially relevant concepts include:

workplan;
workingstep;
process parameter;
process requirement;
process result;
operation dependency;
sequencing;
setup;
setup change;
inspection step;
rework;
process verification.
Relevant References

Potentially:

ISO 14649 / STEP-NC
ISO/ASTM 52900 family
Manufacturing process standards
CAM information models
Boundary

Machine Builder should not become a full CAM application merely because process concepts exist in the ontology.

12. Advanced Tooling Model
Status

Deferred.

Current Support

The ontology distinguishes:

Tool
Toolhead
Carriage
Workholding
Future Topics
tool library;
tool identity;
tool life;
tool wear;
tool offsets;
automatic tool changing;
tool holders;
tool stations;
tool qualification;
tool-material compatibility;
process-specific tool capabilities.
Stress Cases
CNC;
IDEX;
tool changers;
multi-material systems;
industrial robots.
13. Runtime and Telemetry
Status

Deferred.

Current Support

Runtime State is distinct from Configuration.

Future Topics
live telemetry;
event streams;
runtime snapshots;
fault history;
machine state history;
operator actions;
time-series measurements;
remote monitoring;
alerts;
dashboards;
runtime-to-model synchronization.
Important Boundary

Runtime data should not redefine the canonical architecture merely because it is observed more frequently.

14. Temporal Modeling
Status

Deferred.

Reason

Machine information changes over time.

Examples:

Component installed
Component removed
Firmware changed
Configuration changed
Tool mounted
Tool removed
Calibration updated
Machine modified
Future Research

Potential topics:

validity intervals;
temporal versions;
machine revisions;
configuration revisions;
installation history;
maintenance history;
historical states;
event sourcing;
snapshot models.
Important Requirement

Historical facts should not disappear merely because the machine has changed.

15. Advanced Firmware Translation
Status

Deferred beyond the current mapping architecture.

Current Support

The project already recognizes:

Canonical Model
    ↕
Firmware Mapping

including:

direct;
calculated;
composite;
conditional;
version-specific mappings.
Future Topics
formal capability models;
parser frameworks;
code generation;
version compatibility;
feature detection;
semantic equivalence;
translation loss;
round-trip testing;
firmware plugin architecture;
unsupported-feature diagnostics.
16. Firmware Macro / Program Semantics
Status

Deferred.

Reason

Macros and firmware programs can combine:

commands;
conditions;
actions;
state;
procedures;
calculations;
control logic.

Treating them as simple configuration fields would lose meaning.

Future Research

Potential topics:

macro semantics;
command intent;
conditional execution;
procedural interpretation;
state transitions;
embedded control logic.
17. Knowledge Graph Research
Status

Deferred.

Current Decision

A knowledge graph may complement the canonical model but is not currently the canonical storage architecture.

Future Questions
What queries actually require graph traversal?
Which relationships benefit from graph representation?
How should external standards be linked?
How should provenance be traversed?
Should external product knowledge be graph-backed?
Can a graph representation coexist with a structured persistence model?
Important Rule

Do not adopt graph technology merely because the ontology contains relationships.

The architectural problem should justify the technology.

18. Advanced Provenance
Status

Partially active; advanced work deferred.

Current Support

The project already requires provenance conceptually.

Future Topics
evidence graphs;
provenance chains;
source weighting;
confidence propagation;
conflict resolution;
provenance snapshots;
audit history;
source version tracking;
evidence validity.
Desired Future Capability

The system should eventually answer:

Why does Machine Builder believe this?

and:

What would change this conclusion?

19. Advanced Conflict Resolution
Status

Deferred.

Current Support

Conflicting evidence must not silently overwrite previous information.

Future Topics
source authority;
source freshness;
confidence scoring;
evidence comparison;
user resolution;
automated conflict detection;
conflict history.

Potential result:

Fact A
Fact B
Conflict
Resolution
Resolution Evidence
20. Advanced Component Catalog Engineering
Status

Deferred.

Current Support

The architecture distinguishes:

Catalog Product
Product Version
Machine Component
Future Topics
product families;
variants;
substitutions;
compatible products;
supplier information;
lifecycle state;
obsolete products;
manufacturer revisions;
datasheet extraction;
connector/pin metadata;
dimensional models;
performance curves;
torque/speed characteristics.
Important Boundary

Catalog engineering should support machine creation without allowing catalog data to silently override physical evidence.

21. Advanced Motor and Actuator Modeling
Status

Deferred.

Current Support

Motor and Actuator are distinct concepts.

Future Topics
torque/speed curves;
winding resistance;
inductance;
thermal limits;
inertia;
acceleration limits;
load estimation;
transmission efficiency;
stall conditions;
missed steps;
servo feedback;
actuator duty cycles.
Engineering Use

These concepts are especially useful when evaluating whether available parts can realistically build a new machine.

22. Advanced Mechanical Engineering
Status

Deferred.

Future Topics
structural stiffness;
deflection;
vibration;
resonance;
bearing loads;
belt tension;
screw efficiency;
backlash;
thermal expansion;
mass/inertia;
fastener properties;
frame analysis.
Boundary

Machine Builder may eventually support useful engineering evaluations without becoming a general-purpose finite-element analysis package.

23. Thermal Modeling
Status

Deferred.

Potential Topics
heater sizing;
thermal mass;
chamber heating;
cooling;
heat transfer;
thermal gradients;
thermal limits;
insulation;
heater duty cycle;
environmental conditions.
Stress Cases

Particularly relevant to:

Stratasys SST1200es;
heated chambers;
hotends;
heated beds;
industrial machines.
24. Fluid and Pneumatic Systems
Status

Deferred.

Reason

The ontology should eventually support machines involving:

coolant;
compressed air;
vacuum;
hydraulics;
pneumatics.

However, the current machine corpus does not require a complete fluid ontology.

Future Topics
fluid ports;
fittings;
valves;
pumps;
reservoirs;
pressure;
flow;
tubing;
hydraulic/pneumatic functions;
leak detection.
Potential References
ISO 1219 series
Additional fluid-power standards as required
25. Electrical Signal Modeling
Status

Deferred.

Reason

The project has established Ports and Connections but has not finalized a universal Signal concept.

Future Topics
analog signals;
digital signals;
differential signals;
PWM;
frequency;
electrical characteristics;
signal integrity;
logic levels;
impedance;
shielding;
termination.

A universal Signal concept should only be adopted if it improves rather than confuses the ontology.

26. Communication Networks
Status

Deferred.

Future Topics
CAN;
RS485;
Ethernet;
USB;
serial;
SPI;
I2C;
fieldbus systems;
network topology;
addressing;
protocols;
device discovery;
communication capabilities.
Current Evidence

The CFS provides a useful RS485 stress case.

Distributed controllers provide additional evidence.

27. Industrial Interoperability
Status

Deferred.

Future Topics

Potential integrations include:

OPC UA;
industrial fieldbus systems;
PLC systems;
machine-tool information models;
MES;
manufacturing databases;
digital-thread systems.
Boundary

Interoperability should be driven by an actual integration requirement rather than broad standards accumulation.

28. CAD Integration
Status

Deferred.

Potential Future Functions

Machine Builder may eventually exchange:

geometry;
component locations;
mounting structures;
dimensions;
coordinate frames;
transforms;
assemblies;
metadata.
Boundary

Machine Builder is not intended to become a general CAD system.

29. 3D Machine Representation
Status

Deferred.

Future Topics
3D machine visualization;
spatial hierarchy;
connector locations;
cable routing;
harness visualization;
tubing;
physical clearances;
animated motion;
exploded views;
maintenance views.
Existing Architectural Preparation

The current separation between:

Physical Coordinates
Coordinate Frames
Visual Model

is intended to make future 3D support possible without redefining the ontology.

30. Parametric Routing
Status

Deferred.

Future Topics
cable routes;
harness paths;
tubing;
slack;
service loops;
bend radius;
cable bundles;
physical connector geometry;
automated path generation.

Potential future integration with Blender or other geometry systems may become useful.

31. Advanced Wiring Engineering
Status

Deferred.

Future Topics
individual conductors;
wire gauge;
insulation;
current;
voltage;
voltage drop;
fuse/protection;
connector ratings;
routing;
shielding;
harness grouping;
service loops;
termination;
labeling.

The architectural distinction between:

Physical Connection
Logical Mapping
Visual Connection

provides the necessary foundation.

32. Diagnostics
Status

Deferred.

Future Topics
diagnostic relationships;
fault isolation;
symptom → cause reasoning;
test procedures;
expected measurements;
troubleshooting paths;
live signal visualization;
wiring fault detection;
component health;
maintenance recommendations.
Existing Architectural Preparation

Provenance, relationships, measurement results, and runtime state all provide foundations for future diagnostics.

33. Maintenance and Lifecycle
Status

Deferred.

Future Topics
maintenance procedures;
inspection schedules;
wear tracking;
component replacement;
service history;
spare parts;
lifecycle state;
obsolescence;
maintenance records.

This domain may eventually intersect strongly with Machine Component and Product Version modeling.

34. Digital-Twin-Like Runtime Integration
Status

Deferred.

Future Possibility

The canonical machine model could eventually act as a persistent engineering representation that is synchronized with:

physical machine;
firmware;
runtime state;
telemetry;
maintenance;
configuration.
Important Boundary

The project should not claim to be a full digital twin simply because it contains machine state.

The requirements of a digital-twin system should be researched separately if that direction becomes important.

35. Formal Requirement Engineering
Status

Deferred.

Potential Topics
stakeholder needs;
system requirements;
derived requirements;
allocation;
traceability;
verification;
validation;
change management.
Relevant Reference

ISO/IEC/IEEE 15288 provides useful systems-engineering context.

A full requirements-management system is not currently required.

36. Advanced System Architecture Views
Status

Deferred.

Future Possibility

Machine Builder may support multiple formal views:

Physical View
Electrical View
Logical View
Functional View
Control View
Safety View
Process View
Maintenance View
Visual View
Existing Foundation

The Aspect concept and ISO/IEC/IEEE 42010 architecture-view ideas provide a useful foundation.

The project should determine later how much formal viewpoint machinery is actually useful.

37. Advanced Documentation Generation
Status

Deferred.

Potential Outputs
machine architecture report;
wiring diagrams;
BOM;
firmware configuration;
service manual;
maintenance instructions;
calibration records;
safety documentation;
component schedules.

The canonical model should eventually support generating multiple documents from the same underlying information.

38. Advanced Import / Export
Status

Deferred.

Potential Formats
firmware configuration;
BOM;
CSV;
JSON;
YAML;
XML;
STEP;
electrical CAD formats;
machine descriptions;
manufacturer data.

The canonical model should remain the semantic center regardless of file format.

39. Simulation
Status

Deferred.

Potential Topics
motion simulation;
collision detection;
kinematic simulation;
thermal simulation;
process simulation;
electrical simulation;
controller simulation.
Boundary

Simulation should be treated as a future consumer of the canonical model unless an actual simulation feature becomes a core project requirement.

40. AI-Assisted Engineering
Status

Deferred.

Potential Future Uses
semantic extraction from manuals;
component identification;
wiring interpretation;
firmware parsing assistance;
anomaly detection;
documentation extraction;
research assistance;
candidate relationship generation.
Important Principle

AI-generated interpretations should retain provenance and uncertainty.

AI output should not automatically become authoritative machine fact.

41. Advanced Reverse Engineering
Status

Deferred.

Potential Future Topics
automatic wiring discovery;
pin identification;
firmware inference;
behavior inference;
component identification;
protocol reverse engineering;
machine-structure reconstruction.

The current research process already supports manual reverse engineering.

Automation should come after the semantic model is sufficiently mature.

42. Full Hardware Capability Reasoning
Status

Deferred.

Future Goal

Given a set of available components, Machine Builder might eventually determine:

Can these parts build this machine?

Potential reasoning could include:

mechanical compatibility;
motor torque;
electrical compatibility;
controller resources;
firmware support;
tool requirements;
thermal limits;
safety;
wiring.

This is an important long-term goal but should not drive the first ontology implementation.

43. Part-Reuse and Salvage Engineering
Status

Deferred.

Motivation

Machine Builder may eventually help build machines from available parts.

Potential questions:

Can this motor drive this mechanism?
Can this controller support these actuators?
Will this power supply support the machine?
Can this rail support the load?
Can this connector carry the required current?

This directly connects the catalog, Machine Component, engineering evaluation, and machine architecture layers.

44. Engineering Recommendation Engine
Status

Deferred.

Future Possibility

The system could eventually generate recommendations such as:

Use a larger conductor.
Change the controller.
Add a driver.
Reduce acceleration.
Add an interlock.
Use a different tool.
Increase structural support.
Verify the motor specification.

Recommendations must distinguish:

Required
Recommended
Optional
Unknown

and retain the engineering basis.

45. Advanced Compatibility
Status

Deferred.

Current Support

Basic semantic compatibility is already part of the visual-builder direction.

Future Topics
electrical compatibility;
mechanical compatibility;
protocol compatibility;
firmware compatibility;
thermal compatibility;
material compatibility;
dimensional compatibility;
controller-resource compatibility;
process compatibility.

Compatibility may eventually require multi-stage evaluation rather than a single boolean.

46. Future Research Priority Rule

A deferred topic should become active when one of the following occurs:

A current implementation task cannot proceed correctly without it.
A stress case exposes a missing architectural concept.
Multiple existing concepts become inconsistent without it.
A meaningful user workflow requires it.
A standards-driven requirement makes it necessary.
A planned machine research target depends on it.

A topic should not become active merely because it is interesting.

47. What Should Remain Deferred

For the current ontology milestone, the following should remain explicitly outside the critical path:

Full database selection
Knowledge graph implementation
Full CAD integration
Full CAM system
Certification-grade safety engine
Complete digital twin
Advanced thermal simulation
Full finite-element analysis
Complete electrical CAD replacement
Full industrial MES integration
Universal Flow ontology
Universal Signal ontology
Universal Channel ontology
Full runtime telemetry platform

These may eventually become valuable.

They should not distort the core ontology prematurely.

48. Deferred Research Dependencies

Many deferred domains depend on current ontology work.

Examples:

Advanced Kinematics
    depends on
Axis + Joint + Coordinate Frame

Electrical Engineering
    depends on
Port + Connection + Property

Diagnostics
    depends on
Relationship + Measurement + Runtime State + Provenance

Calibration
    depends on
Measurement + Result + Property + Provenance

Firmware Translation
    depends on
Canonical Model + Relationships + Controller Resources

Safety Engineering
    depends on
Function + Control + Components + Provenance

3D Routing
    depends on
Physical Connection + Path + Coordinate Frames

This dependency structure explains why the current ontology should be developed before many advanced features.

49. Deferred Research Review Rule

At each major research milestone, review the deferred list and ask:

Does this topic now affect current architecture?

Does a new machine require it?

Has implementation exposed a missing concept?

Has a standard made it necessary?

Can it remain deferred?

Most deferred topics should remain deferred until a concrete need appears.

50. Summary

Deferred research exists to protect the project from two opposite failures:

Failure A:
    Ignore important future concepts

and:

Failure B:
    Research everything before building anything

The intended balance is:

Core semantic problem
        ↓
Research
        ↓
Decision
        ↓
Implementation

while future domains remain visible:

Deferred
    ↓
Revisit when justified

The long-term project is intentionally broad, but the current architecture should mature from the strongest evidence and highest-value machine stress cases rather than attempting to solve every engineering domain simultaneously.