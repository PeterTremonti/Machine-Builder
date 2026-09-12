# Machine Research Index

## 1. Purpose

This document is the index of machines used as research subjects and architectural stress cases for Machine Builder.

The machine corpus serves several purposes:

- provide real engineering evidence;
- test ontology concepts;
- expose hidden assumptions;
- compare different machine architectures;
- test firmware-independent modeling;
- identify relationships that a conventional printer model cannot express;
- provide implementation validation cases.

A machine is not included merely because it is interesting.

The most valuable research machines are those that expose a meaningful modeling problem.

---

# 2. Research Principle

Machine research follows:

```text
Machine
   ↓
Observe architecture
   ↓
Identify semantic concepts
   ↓
Identify unusual relationships
   ↓
Stress-test ontology
   ↓
Record evidence

The goal is not to create a perfect technical manual for every machine.

The goal is to learn what the Machine Builder ontology must be capable of representing.

3. Machine Research Status

Current machine research categories are:

Primary Stress Case
Secondary Stress Case
Supporting Example
Future Research
Primary Stress Case

A machine that currently tests important architectural assumptions.

Secondary Stress Case

A machine that tests one or more useful concepts but is not currently driving architecture.

Supporting Example

A machine used as evidence or comparison.

Future Research

A machine or architecture identified as potentially useful but not yet investigated sufficiently.

4. Current Research Corpus

The current important machine corpus includes:

Promega
SV08
LowRider
IR3
Creality CFS
Stratasys SST1200es
Ender 3 / SKR Mini E3
Creality Hi / CFS
Carvera
K40
3018 CNC
IDEX-class machines
Tool-changing machines
Closed-loop machines

Not every machine requires a dedicated permanent research document immediately.

5. Primary Stress Cases
5.1 M3D Promega

Status: Primary Stress Case

Domain: Additive manufacturing / 3D printing

Architectural Importance

The Promega is one of the principal baseline machines for Machine Builder development.

It provides a comparatively conventional machine while still exposing important real-world details.

Known Relevant Characteristics
Machine:
    M3D Promega

Controller:
    Duet 2 Maestro

Firmware:
    RepRapFirmware

Known firmware version:
    RRF 3.5.4

Machine geometry:
    approximately 388 mm class XYZ

Motion:
    CoreXY-style XY motion
    Z motion
Important Research Areas
firmware mapping;
controller resources;
axis/motor relationships;
probing;
coordinate frames;
configuration interpretation;
calibration;
wiring;
visual representation.
Stress Cases

The Promega tests:

Firmware-independent axis semantics
Controller resource mapping
Multiple Z actuator planning
Probe representation
Physical vs logical connectivity
Machine-specific roles
Configuration provenance
Important Firmware Evidence

Existing research includes parameters such as:

M584
M350
M92
M208
M669
M569
G31

These are evidence about machine semantics rather than canonical ontology concepts.

Related Research

Recommended future location:

machines/promega/
6. SV08

Status: Primary Stress Case

Domain: Additive manufacturing / 3D printing

Architectural Importance

The SV08 is especially important because it combines CoreXY motion with multiple independently controlled Z actuators and distributed control elements.

Relevant Characteristics
Motion:
    CoreXY
    four independent Z motors

Architecture:
    flying gantry

Firmware:
    Klipper
Concepts Tested
Axis ≠ Motor
One logical Z axis → multiple actuators
Distributed control
Controller resources
Kinematic relationships
Firmware mapping
Toolhead/local electronics
Why It Matters

A naive model may attempt:

Z Axis → Z Motor

The SV08 disproves that assumption.

The canonical model must instead permit:

Z Motor 1 ─┐
Z Motor 2 ─┼──→ Z Axis
Z Motor 3 ─┤
Z Motor 4 ─┘

while retaining the identity and controller assignment of each motor.

7. LowRider / MPCNC-Class Router

Status: Primary Stress Case

Domain: CNC / routing

Architectural Importance

LowRider is an important cross-domain and cross-firmware test because it introduces CNC-specific process and motion requirements while supporting multiple controller/firmware ecosystems.

Research Targets
multiple Y/Z actuators;
squaring;
coordinated motion;
CNC tooling;
workholding;
process/operation semantics;
controller resources.
Firmware Evidence

Research has included:

FluidNC
RepRapFirmware
Marlin
grblHAL
Concepts Tested
Axis
Actuator
Kinematics
Coordinate Frames
Tool
Workholding
Operation
Process
Firmware Mapping
Importance

LowRider prevents the ontology from becoming an additive-manufacturing-only model.

8. IdeaFormer IR3

Status: Primary Stress Case

Domain: Belt-based additive manufacturing

Architectural Importance

The IR3 is important because it violates conventional Cartesian machine assumptions.

Relevant Characteristics
Belt-oriented motion
Non-standard machine geometry
Marlin-based firmware evidence
Machine-specific coordinate transformation
Concepts Tested
Coordinate Frame
Transform
Axis
Kinematic Relationship
Tool Position
Firmware Motion Mapping
Importance

The IR3 demonstrates that:

Machine Builder must model machine motion semantics independently from simplistic XYZ hardware assumptions.

9. Creality CFS

Status: Primary Stress Case

Domain: Material handling / additive manufacturing subsystem

Architectural Importance

The CFS is one of the most important subsystem stress cases.

It demonstrates that a machine component or subsystem may contain substantial internal structure and behavior.

Known Physical Architecture

A simplified representation is:

CFS
├── Spool Mechanisms
│   ├── Rewind / Roller Motor
│   ├── Filament-Present Sensor
│   └── Feeder Motor
├── Lower Feed Section
│   ├── Filament Sensor
│   └── Feeder Motor
├── Material Paths
├── Buffer
├── Buffer Switch
├── Local Controller
└── Communication Interface
Additional Research

Known communication research includes:

RS485
Half duplex
230400 baud
8N1
24 V
GND
RS485 A/B
Buffer control signals
Important Concepts Tested
Subsystem
Material Path
Sensor
Actuator
Local Controller
Communication
Buffer
Capability
Function
State
Port
Connection
Important Architectural Lesson

The CFS should not be represented simply as:

Filament Feeder

It is a bounded subsystem containing multiple components, functions, resources, interfaces, and internal relationships.

10. Stratasys SST1200es

Status: Primary Stress Case

Domain: Industrial additive manufacturing

Architectural Importance

The SST1200es provides a substantially different machine architecture from modern hobbyist printers.

It is particularly useful for testing:

proprietary hardware;
industrial machine structure;
chamber heating;
legacy electronics;
safety;
subsystem modeling;
retrofit architectures.
Known Relevant Characteristics
Machine:
    Stratasys SST1200es

Chamber:
    heated

Chamber heaters:
    two approximately 400 W,
    120 VAC heaters

Build platform:
    no conventional heated bed
    approximately 3/8" ABS plate

Mechanical structure:
    approximately 15.75 mm rods
Planned Conversion

The research/engineering plan has included:

BTT Octopus family controller
TMC5160T drivers
BTT Pi
Klipper
Important Research Questions

The conversion makes this machine especially valuable because the same physical architecture will be represented first as proprietary legacy equipment and later as a modern open controller/firmware implementation.

This creates a strong test for:

Physical machine
      ↓
Canonical model
      ↓
New controller
      ↓
New firmware representation

without changing the underlying machine identity.

Additional Research

Mechanical documentation has been collected for:

structural dimensions;
chamber system;
heaters;
material path;
cartridge/filament mechanisms;
toolhead mechanisms.

Network/software-specific sections are lower priority for the conversion project.

11. Ender 3 / SKR Mini E3 V3

Status: Secondary Stress Case

Domain: Additive manufacturing

Architectural Importance

The Ender 3 is useful as a simple and widely understood baseline machine.

The SKR Mini E3 V3 provides a modern controller replacement example.

Research Uses
Marlin
Klipper
Controller replacement
Basic axis mapping
Basic wiring
Firmware comparison
Configuration generation
Importance

It provides a relatively simple machine against which more complex stress cases can be compared.

12. Creality Hi / CFS

Status: Secondary Stress Case

Architectural Importance

The Creality Hi with working CFS provides another real example of:

printer-to-subsystem integration;
communication;
material handling;
distributed electronics;
tool/material coordination.
Research Use

This machine can complement direct CFS reverse engineering and provides evidence about how a commercial machine integrates the subsystem.

13. Carvera

Status: Secondary Stress Case

Domain: CNC machining

Architectural Importance

Carvera is useful for testing:

CNC semantics;
multiple axes;
tooling;
automatic tool changing;
machine process concepts;
controller abstraction.
Firmware Research

Research has included a Makera/Smoothieware-derived firmware environment.

Concepts Tested
Tool
Tool Changer
Operation
Process
Axis
Controller
Firmware Mapping
14. K40

Status: Secondary / Supporting Stress Case

Domain: Laser cutting / engraving

Architectural Importance

The K40 adds a machine domain substantially different from filament extrusion and CNC cutting.

Research Areas
laser source;
motion system;
safety;
enclosure;
interlock;
controller;
job/process semantics.
Known Uncertainty

The exact controller architecture should not be assumed until directly verified for the specific machine under study.

15. 3018 CNC

Status: Supporting Stress Case

Domain: CNC machining

Research Use

Useful for testing:

CNC axes;
spindle;
tool;
workholding;
simple machining operations;
controller/firmware mappings.
Importance

Provides a small CNC architecture against which LowRider and larger machines can be compared.

16. IDEX-Class Machines

Status: Secondary Stress Case / Architecture Class

Architectural Importance

Independent Dual Extrusion machines challenge assumptions about:

multiple tools;
multiple toolheads;
multiple carriages;
independent motion;
coordinated process planning.
Concepts Tested
Tool
Toolhead
Carriage
Axis
Process
Operation
Capability

The IDEX concept is more important than any one particular printer model.

17. Tool-Changing Machines

Status: Secondary Stress Case / Architecture Class

Architectural Importance

Tool changers test whether the ontology can distinguish:

Tool
Toolhead
Carriage
Mount
Machine Function
Process Requirement
Important Questions

A machine may contain:

multiple tools;
one carriage;
multiple holders;
a tool-changing mechanism;
tool identity/state;
different process capabilities.

The ontology should not require every tool to have a permanent one-to-one relationship with a carriage.

18. Closed-Loop Machines

Status: Secondary Stress Case / Architecture Class

Architectural Importance

Closed-loop systems are important for testing:

Sensor
Measurement
Measurement Result
Feedback
Control Function
Control Loop
State
Example Sensors

Potential research examples include:

encoders;
load cells;
pressure sensors;
force sensors;
position sensors.
Importance

The ontology must support a sensor feeding multiple functions rather than assuming every sensor exists solely for one control loop.

19. CoreXY Machines

Status: Primary Architecture Pattern

Importance

CoreXY is a fundamental kinematic stress case.

The machine has:

Motor A
Motor B

but both motors participate in both:

X motion
Y motion
Required Modeling
Motor A ──→ Kinematic Relationship ──→ X
Motor A ──→ Kinematic Relationship ──→ Y

Motor B ──→ Kinematic Relationship ──→ X
Motor B ──→ Kinematic Relationship ──→ Y

A one-motor/one-axis ontology fails this case.

20. Multiple-Actuator-Axis Machines

Status: Primary Architecture Pattern

Example

A single logical Z axis may have:

Z Actuator 1
Z Actuator 2
Z Actuator 3
Z Actuator 4
Concepts Tested
Axis;
Actuator;
Motor;
Drive;
Controller Resource;
synchronization;
squaring;
calibration.

This pattern is represented by the SV08 and other machines.

21. Distributed-Control Machines

Status: Primary Architecture Pattern

Examples
SV08
CFS systems
CAN-connected toolheads
Remote I/O
Industrial distributed controllers
Concepts Tested
Controller
Controller Resource
Subsystem
Communication Interface
Port
Mapping
Firmware
Runtime State

The ontology must not assume one controller owns the entire machine.

22. Machine Classes Versus Individual Machines

Some research subjects are machine classes rather than one physical machine.

Examples:

CoreXY
IDEX
Tool Changer
Closed Loop
Multiple-Z
Distributed Control

These are useful because they represent architectural patterns that occur across many machines.

A machine-class stress case should not automatically become a Machine object in the user's project database.

It is research evidence about possible machine architectures.

23. Machine Research Folder Structure

The intended repository organization is:

machine-builder-research/
└── machines/
    ├── MACHINE_RESEARCH_INDEX.md
    ├── promega/
    ├── stratasys-1200es/
    ├── sv08/
    ├── creality-cfs/
    └── other/

As research matures, individual machine folders may contain:

README.md
ARCHITECTURE.md
MECHANICAL.md
ELECTRICAL.md
CONTROLLER.md
FIRMWARE.md
MOTION.md
SENSORS.md
TOOLS.md
RESEARCH_NOTES.md
SOURCES.md

Not every machine needs every file.

24. Machine Research Evidence Levels

Machine information should be categorized approximately as:

Verified
Documented
Measured
Observed
Strongly Inferred
Weakly Inferred
Unknown

Examples:

Verified

Direct measurement or confirmed documentation.

Documented

Manufacturer or authoritative documentation.

Measured

Observed through an actual measurement.

Observed

Direct physical inspection.

Strongly Inferred

Multiple independent evidence sources support the conclusion.

Weakly Inferred

Plausible but insufficiently supported.

Unknown

No adequate evidence currently exists.

25. Machine Research Record

A useful machine research record should eventually include:

Machine Identity
Manufacturer
Model
Revision / Variant
Domain
Research Status
Primary Stress Cases
Mechanical Architecture
Electrical Architecture
Controller Architecture
Firmware
Motion Architecture
Coordinate Systems
Sensors
Actuators
Tools
Subsystems
Interfaces
Safety
Process
Known Modifications
Unknowns
Sources
Provenance
Research Questions

This does not imply every machine document must immediately contain every field.

26. Research Versus Machine Modeling

Machine research and machine modeling are separate activities.

Research may establish:

"This machine appears to have four independent Z motors."

The canonical model may later represent:

Four Machine Components
    classified_as
Stepper Motor

Each:
    has_role
    Z-axis actuator

All:
    participate_in
    Z Axis

Research is evidence-gathering.

The canonical model is semantic representation.

27. Modifications and Retrofit Research

A machine may have multiple hardware states over its life.

Example:

SST1200es
    ↓
Original controller
    ↓
Retrofit controller
    ↓
New firmware

The research record must distinguish:

Modified Architecture
Planned Architecture

A planned retrofit must not be treated as the current physical machine state.

28. Machine Research Questions

Each machine may have questions such as:

What is physically present?
What is documented?
What is inferred?
What controller resources exist?
How are motion relationships implemented?
What sensors exist?
What functions exist?
What subsystems exist?
What firmware semantics are exposed?
What safety structures exist?
Which assumptions does this machine break?

The final question is particularly important.

29. Machine Stress-Test Matrix
Machine / Pattern	Primary Concepts Tested
Promega	Firmware mapping, controller resources, CoreXY, probing
SV08	Multiple actuators per axis, distributed control
LowRider	CNC, multiple axes/actuators, process/tooling
IR3	Coordinate transforms, non-Cartesian motion
CFS	Subsystem, material paths, local control
SST1200es	Industrial machine, retrofit, safety, proprietary architecture
Ender 3	Simple baseline, firmware comparison
Carvera	CNC, tooling, tool changing
K40	Laser, safety, enclosure, process
3018	Simple CNC
IDEX	Independent tools/carriages
Tool Changer	Tool identity and mounting
Closed Loop	Measurement and feedback
CoreXY	Kinematics
Distributed Controllers	Controller/resource topology
Multiple-Z	Axis/actuator multiplicity
30. Research Priority

Current approximate priority is:

Highest
    Promega
    SV08
    LowRider
    IR3
    CFS
    SST1200es

Medium
    Ender 3
    Carvera
    Distributed-control examples
    Tool-changing examples
    IDEX

Supporting
    K40
    3018
    Additional conventional printers

Future
    Industrial robots
    More complex CNC
    Closed-loop industrial machinery
    Hybrid machines

Priority may change as ontology stress testing reveals new needs.

31. What Machine Research Should Not Become

Machine research should not become:

a collection of unstructured build logs;
a replacement for the canonical ontology;
a collection of firmware configuration files with no semantic interpretation;
an exhaustive encyclopedia of every machine detail;
a duplicate of manufacturer manuals;
a substitute for engineering validation.

Research should focus on evidence that changes or validates the machine architecture model.

32. Research Promotion Path

Machine research should feed the ontology through:

Machine Observation
       ↓
Evidence
       ↓
Research Finding
       ↓
Concept / Relationship Candidate
       ↓
Stress Test
       ↓
Ontology Decision
       ↓
Canonical Model
       ↓
Implementation Requirement

A single machine observation should not automatically become a universal rule.

It becomes a rule only when supported by broader reasoning or multiple evidence sources.

33. Primary Machine Research Principle

The most important rule for the machine corpus is:

Study machines that break assumptions, not merely machines that look different.

A hundred conventional Cartesian printers provide less architectural information than a small number of machines that expose fundamentally different relationships.

The current corpus is intentionally diverse because each major stress case answers a different ontology question.

34. Summary

The current machine research corpus provides evidence for the architecture across:

Conventional 3D Printing
CoreXY
Multiple-Z
Belt Printing
CNC
Laser
Material Handling
Industrial Additive Manufacturing
Distributed Control
Independent Tools
Tool Changers
Closed-Loop Control

The most important current machines are:

Promega
SV08
LowRider
IR3
Creality CFS
Stratasys SST1200es

These machines should remain the primary architectural test set until the ontology is sufficiently mature to handle their important differences without special-case modeling.