# Machine Builder Firmware Research Index

## 1. Purpose

This document indexes firmware and machine-control software researched for Machine Builder.

The purpose of firmware research is not to make Machine Builder a firmware encyclopedia.

Firmware research exists to determine:

- how different systems represent machine semantics;
- where firmware terminology differs from canonical machine terminology;
- what machine capabilities can or cannot be represented;
- how controller resources are exposed;
- how configuration maps to physical architecture;
- how existing configurations can be interpreted back into canonical machine information;
- where firmware differences expose weaknesses in the ontology.

The core principle is:

> Firmware is an implementation representation of a machine, not the canonical definition of the machine.

---

# 2. Firmware Research Strategy

Firmware research follows:

```text
Firmware
   ↓
Identify concepts and terminology
   ↓
Determine what machine meaning is represented
   ↓
Map to canonical concepts
   ↓
Identify unsupported or ambiguous semantics
   ↓
Stress-test ontology

The project does not need to support every firmware system before the canonical ontology is useful.

A smaller set of substantially different firmware systems provides more architectural value than a long list of similar implementations.

3. Current Firmware Research Corpus

The current important firmware/control systems include:

RepRapFirmware
Klipper
Marlin
FluidNC
grblHAL
Smoothieware
GRBL
TinyG / g2core
LinuxCNC
Repetier

Other systems may be added as specific machine research requires them.

4. Firmware Research Status

Firmware research may be classified as:

Primary Comparison
Secondary Comparison
Supporting Evidence
Future Research
Primary Comparison

Firmware currently used to test canonical modeling and translation architecture.

Secondary Comparison

Firmware providing useful contrasting semantics or machine capabilities.

Supporting Evidence

Firmware researched mainly to answer a specific question.

Future Research

Potentially useful but not currently required.

5. RepRapFirmware

Status: Primary Comparison

Primary Machine: M3D Promega

Importance

RepRapFirmware is one of the principal firmware systems used to test the forward and reverse translation architecture.

It is particularly useful because configuration exposes explicit machine concepts such as:

motion mapping;
drive assignment;
microstepping;
motion scale;
endstops;
probes;
machine geometry;
kinematic modes;
tools.
Known Promega Evidence

Existing research includes parameters such as:

M584
M350
M92
M208
M669
M569
G31

Examples include:

M584 X0 Y1 Z2
M350 X16 Y16 Z16 I1
M92 X80 Y80 Z282.7
M208 X0:380 Y0:380 Z0:380
M669 K1
M569 S1
G31 ...

These statements are firmware representations of underlying machine semantics.

They should not become canonical concepts merely because they are expressed in RRF syntax.

Concepts Tested
id="74t6w2"
Axis
Controller Resource
Drive Assignment
Motion Scale
Microstepping
Kinematics
Probe
Endstop
Limits
Firmware Version
6. Klipper

Status: Primary Comparison

Primary Machines / Examples:

SV08
planned SST1200es retrofit
planned LowRider controller architecture
Ender-class experiments
Importance

Klipper is particularly valuable because it has a substantially different architecture from firmware systems in which most machine behavior is implemented on one microcontroller.

It provides important evidence for:

host/MCU separation;
distributed control;
multiple MCUs;
toolhead controllers;
configuration-driven machine definition;
macros;
hardware pins;
motion systems;
kinematics.
Concepts Tested
Controller
Distributed Controller
Controller Resource
Firmware
Host Software
Communication Interface
Kinematics
Macro / Procedure-like behavior
Configuration
Runtime State
Important Architectural Lesson

The canonical machine model cannot assume:

Machine
    ↓
One Controller
    ↓
One Firmware Image

Klipper provides strong evidence for a more general architecture:

Machine
 ├── Host Controller
 ├── MCU A
 ├── MCU B
 └── Local / Toolhead Controllers
7. Marlin

Status: Primary Comparison

Importance

Marlin provides a widely used configuration-oriented firmware model and is especially useful for comparing:

board/pin assignments;
axis definitions;
motion configuration;
heaters;
sensors;
tools;
kinematics;
feature flags;
compile-time versus runtime configuration.
Relevant Machines

Marlin research includes:

IR3
Ender-class machines
LowRider-related configurations
Other conventional printers
Concepts Tested
Axis
Pin
Controller Resource
Kinematics
Heater
Sensor
Tool
Configuration
Firmware Feature
Important Lesson

Marlin configuration often expresses several layers simultaneously:

Hardware
Machine Semantics
Firmware Capabilities
Build-Time Options
Runtime Parameters

The canonical model should keep those layers distinguishable.

8. FluidNC

Status: Secondary / Primary for CNC Comparison

Domain

CNC motion control.

Importance

FluidNC is useful because it provides a modern configuration-oriented CNC firmware architecture.

It helps test:

CNC axes;
steppers;
motors;
homing;
spindle control;
I/O;
kinematics;
machine settings;
controller resources.
Relevant Machine

LowRider research.

Concepts Tested
Axis
Actuator
Controller Resource
Spindle
Tool
Homing
CNC Process
Firmware Mapping
Architectural Importance

FluidNC helps prevent the firmware abstraction from being limited to 3D-printing concepts.

9. grblHAL

Status: Secondary Comparison

Domain

CNC motion control.

Importance

grblHAL extends the GRBL-style architecture to more capable hardware and provides useful evidence about:

motion control;
axes;
drivers;
I/O;
plugins;
controller capabilities.
Relevant Machine

LowRider research.

Concepts Tested
Controller
Driver
Axis
I/O
Spindle
Homing
Firmware Capability
10. GRBL

Status: Supporting Comparison

Domain

CNC motion control.

Importance

GRBL is useful as a comparatively simple CNC control architecture.

It provides a useful baseline for:

axis configuration;
steps/mm;
acceleration;
limits;
homing;
spindle control;
motion commands.
Importance to Ontology

GRBL demonstrates that firmware may expose relatively simple machine semantics while still controlling a machine containing substantially richer physical relationships.

The canonical model therefore cannot be defined only by what a particular firmware exposes.

11. Smoothieware

Status: Secondary Comparison

Relevant Machine

Carvera-related research.

Importance

Smoothieware provides another controller/firmware architecture with:

configuration files;
modules;
axes;
tools;
motors;
temperature control;
I/O.
Concepts Tested
Module
Controller
Axis
Motor
Tool
Temperature
Configuration
Firmware Mapping
12. TinyG / g2core

Status: Supporting / Future Comparison

Domain

CNC and motion control.

Importance

Useful as an example of an embedded motion-control architecture with relatively explicit motion and machine-control semantics.

Potential Concepts Tested
Axis
Motion Control
Planner
Controller
Motor
Spindle
Runtime State
Configuration

This firmware family may become more useful when CNC and motion-control interoperability are investigated in greater depth.

13. LinuxCNC

Status: Future / High-Value Comparison

Domain

CNC and general machine control.

Architectural Importance

LinuxCNC is particularly valuable because it is much broader than a conventional embedded 3D-printer firmware.

It may expose concepts around:

hardware abstraction;
real-time control;
kinematics;
HAL;
joints;
axes;
signals;
components;
machine state;
control loops.
Potential Ontology Value

LinuxCNC is a strong candidate for deeper future research into:

Axis
Joint
Kinematics
Signal
Channel
Control Function
Hardware Abstraction
Runtime State
Important Note

Its terminology must not be adopted wholesale.

It is primarily valuable as a stress case for the Machine Builder abstraction.

14. Repetier

Status: Supporting / Future Comparison

Domain

3D-printer firmware.

Potential Research Value

Useful for comparing:

axis configuration;
motion settings;
extruder/tool concepts;
temperature control;
endstops;
firmware configuration.
Current Priority

Lower than RepRapFirmware, Klipper, and Marlin because the current ontology already has sufficient evidence from the primary comparison systems.

15. Firmware Comparison Matrix
Firmware	Primary Domain	Architectural Value
RepRapFirmware	3D printing / general motion	Canonical-to-firmware mapping, explicit configuration
Klipper	3D printing / distributed control	Host/MCU split, distributed resources
Marlin	3D printing	Hardware/configuration/pin semantics
FluidNC	CNC	CNC + modern configuration architecture
grblHAL	CNC	Controller/driver/plugin abstraction
GRBL	CNC	Simple embedded CNC baseline
Smoothieware	Motion / CNC / additive	Module-based control architecture
TinyG / g2core	CNC	Embedded motion control
LinuxCNC	CNC / industrial	Axes, joints, HAL, kinematics, control
Repetier	3D printing	Additional printer comparison
16. Firmware Concepts That Should Remain Outside the Canonical Ontology

The following may be valid firmware concepts without becoming universal Machine Builder concepts:

G-code command
Macro
Configuration Directive
Compile-Time Option
Firmware Module
Firmware Section
Pin Alias
Config Key
Firmware Object
Firmware State Variable

A firmware-specific concept becomes relevant to the canonical ontology only when it represents a meaningful machine semantic.

17. Firmware Term Versus Canonical Concept

Example:

Firmware:
    M584 X0 Y1 Z2

Canonical interpretation:

Axis X
Axis Y
Axis Z
Controller Resources
Motion Assignment Relationships

Another example:

Klipper:
    step_pin
    dir_pin

Canonical interpretation may include:

Controller Resource
Electrical Port
Logical Motion Mapping

The firmware terms remain useful as evidence and source representation.

18. Firmware Capability Model

A future firmware model should distinguish:

Firmware supports concept
Firmware can implement concept
Firmware configuration expresses concept
Firmware configuration currently enables concept

These are not necessarily the same.

For example:

Firmware Capability:
    multiple independent Z steppers

Machine Configuration:
    four Z steppers enabled

Actual Hardware:
    four Z motors installed

These represent different claims.

19. Firmware Version Context

Firmware mappings must be version-aware.

A mapping may apply to:

Firmware:
    RepRapFirmware

Version:
    3.5.x

and differ for:

Firmware:
    RepRapFirmware

Version:
    3.6.x

Likewise, a Klipper configuration may depend on the capabilities of a particular implementation or MCU architecture.

The mapping layer should therefore eventually support:

Firmware
Version
Capability
Mapping
Applicability
20. Firmware-to-Canonical Data Flow

The preferred reverse direction is:

Firmware Source
      ↓
Parser
      ↓
Firmware Semantic Representation
      ↓
Canonical Mapping
      ↓
Canonical Machine Model

The parser should not directly populate arbitrary canonical fields without semantic interpretation.

Example:

M92 Z282.7

should become an interpreted machine property such as:

Z motion scale = 282.7 steps/unit

with provenance pointing back to the firmware source.

21. Canonical-to-Firmware Data Flow

The preferred generation direction is:

Canonical Machine Model
      ↓
Firmware Capability Evaluation
      ↓
Firmware Mapping
      ↓
Constraint Validation
      ↓
Generated Configuration

Generation should not begin until unsupported or ambiguous requirements are identified.

22. Firmware Translation Categories

Mappings may be:

Direct
Canonical value
    ↓
Firmware parameter
Calculated
Canonical geometry
    ↓
Firmware-specific steps/unit
Composite
One canonical concept
    ↓
Multiple firmware settings
Conditional
Canonical requirement
    ↓
Different settings depending on firmware capability
Version-specific
Canonical concept
    ↓
Firmware vX mapping
    ↓
Different mapping for firmware vY
23. Firmware Information Loss

A firmware representation can contain less information than the canonical model.

Example:

Canonical Model:
    Motor identity
    Motor specification
    Mechanical coupling
    Axis role
    Controller resource
    Wiring
    Calibration
    Provenance

Firmware:
    Driver assignment
    Current
    Steps/unit

The reverse interpretation cannot necessarily recover every original fact.

This is expected.

The architecture should explicitly represent information that cannot be recovered.

Possible statuses include:

Unsupported
Not Represented
Unknown
Ambiguous
Requires External Evidence
24. Firmware Round-Trip Testing

A future translator should support tests such as:

Canonical Model
      ↓
Firmware Generator
      ↓
Generated Configuration
      ↓
Firmware Parser
      ↓
Canonical Interpretation

Important semantics should survive the round trip.

The resulting models do not need to be identical in serialization.

They should preserve equivalence of the relevant machine semantics.

25. Firmware Stress-Test Questions

Firmware research should ask:

What does this firmware call an axis?

What does it call a motor?

Can multiple motors contribute to one axis?

Can one motor contribute to multiple axes?

How are controller resources represented?

How are pins represented?

How are tools represented?

How are sensors represented?

How are measurements represented?

How are runtime states represented?

How are control loops represented?

How are safety functions represented?

How are subsystems or distributed controllers represented?

What information is impossible to represent?

What information is hidden behind macros or configuration conventions?

These questions are more important than simply cataloging syntax.

26. Firmware Research and Machine Research

Firmware and machine research must remain linked.

For example:

Machine:
    SV08

Firmware:
    Klipper

may establish:

Physical evidence:
    four Z motors

Firmware evidence:
    four independent stepper definitions

Canonical conclusion:
    one Z Axis
    four participating actuators

Multiple evidence streams therefore reinforce the same machine semantic model.

27. Firmware Research and Controller Research

Firmware should also be separated from the physical controller.

For example:

Controller:
    BTT board

Firmware:
    Klipper

Host:
    Raspberry Pi-class computer

These are different modeled entities.

The architecture should not imply:

Firmware = Controller

or:

Controller = Machine
28. Firmware and Runtime State

Firmware may expose runtime concepts such as:

homing state;
temperatures;
fault state;
motion state;
heater state;
communication state.

These should be interpreted as evidence about canonical Runtime State.

They should not overwrite configuration.

Example:

Configuration:
    Z maximum travel = 380 mm

Runtime:
    Z position = 120 mm
29. Firmware and Macros

Macros deserve special caution.

A macro may combine:

commands;
conditions;
state checks;
motion;
control;
safety-related actions;
procedures.

Therefore:

Macro ≠ Function
Macro ≠ Operation
Macro ≠ Procedure

A macro may implement or invoke several canonical concepts.

Future firmware interpretation should treat macros as executable evidence rather than assuming a one-to-one semantic mapping.

30. Firmware and Safety

Firmware may participate in a safety architecture without being the complete safety system.

Examples include:

emergency stop handling;
endstop behavior;
heater shutdown;
motion limits;
fault responses.

These behaviors must be evaluated in context.

The existence of a firmware safety feature does not automatically establish a compliant Safety Function.

31. Firmware Research Folder Structure

The intended repository structure is:

machine-builder-research/
└── firmware/
    ├── FIRMWARE_RESEARCH_INDEX.md
    ├── klipper/
    ├── reprapfirmware/
    ├── marlin/
    └── other/

Potential per-firmware files may include:

README.md
ARCHITECTURE.md
CONFIGURATION.md
SEMANTICS.md
CAPABILITIES.md
PARSER_NOTES.md
MAPPING.md
SOURCES.md

The structure may evolve.

32. Firmware Research Record

A useful firmware research record should eventually contain:

Firmware Identity
Version
Architecture
Supported Controllers
Configuration Model
Motion Model
Axis Model
Driver Model
I/O Model
Sensor Model
Tool Model
Control Model
State Model
Safety Model
Communication
Distributed Control
Capabilities
Version Differences
Canonical Mappings
Known Information Loss
Sources
Open Questions

Not every firmware needs every category immediately.

33. Current Primary Firmware Stress Set

The current most important firmware systems are:

RepRapFirmware
Klipper
Marlin
FluidNC

These provide a useful contrast among:

Traditional 3D printer firmware
Distributed host/MCU architecture
Configuration-heavy embedded firmware
CNC-oriented configuration/control
34. Secondary Firmware Stress Set

The current secondary systems are:

grblHAL
GRBL
Smoothieware
LinuxCNC
TinyG / g2core
Repetier

These should be expanded when specific ontology questions require them.

35. What Firmware Research Should Not Become

Firmware research should not become:

a replacement for firmware documentation;
a list of every configuration key;
an assumption that firmware terminology equals machine terminology;
a requirement that every firmware support every canonical concept;
a firmware-centric machine ontology.

The important question is always:

What machine meaning does this firmware representation tell us?

36. Firmware Capability Stress Cases

The firmware corpus should eventually test at least:

Single-axis/single-motor mapping
Multiple motors per axis
Multiple axes per motor
CoreXY
Independent Z motors
CNC spindle
Laser control
Tool changing
Distributed MCUs
CAN-connected peripherals
Local toolhead controllers
Closed-loop control
Probing
Temperature control
Safety-related shutdown
Machine limits
37. Current Firmware Architecture Principle

The current firmware architecture is:

                    CANONICAL MACHINE MODEL
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
             Firmware Mapping     Capability Check
                    │                   │
                    └─────────┬─────────┘
                              ▼
                     Firmware Representation
                              │
                              ▼
                       Controller / Host
                              │
                              ▼
                         Physical Machine

The reverse path is equally important:

Physical Machine
      ↓
Controller / Firmware
      ↓
Configuration / Runtime Information
      ↓
Firmware Parser
      ↓
Canonical Interpretation
38. Firmware Ontology Boundary

The canonical ontology should represent machine meaning.

Firmware research should preserve firmware-specific structure separately.

For example:

Canonical:
    Controller Resource

Firmware:
    Klipper MCU pin definition

or:

Canonical:
    Axis participates in kinematic system

Firmware:
    `[kinematics] corexy`

The firmware representation is evidence of the underlying machine architecture.

39. Firmware Research Principle

The most important firmware research rule is:

Never let the configuration language of one firmware define what a machine is.

The Machine Builder ontology must be able to represent a machine before choosing:

firmware;
controller;
host;
UI;
storage format.

Firmware research exists to discover how canonical machine semantics are implemented, exposed, constrained, or obscured by different control systems.

40. Summary

The current firmware research corpus provides architectural contrast across:

RepRapFirmware
Klipper
Marlin
FluidNC
grblHAL
GRBL
Smoothieware
LinuxCNC
TinyG / g2core
Repetier

The primary comparison set is:

RepRapFirmware
Klipper
Marlin
FluidNC

These systems are sufficient to continue testing the current ontology without broadening the firmware list unnecessarily.

The key research goals remain:

Translate firmware representations into canonical machine semantics.
Generate firmware representations from canonical machine semantics.
Preserve provenance and version applicability.
Detect unsupported or lossy translations.
Test the ontology against substantially different machine-control architectures.
Keep firmware terminology separate from canonical terminology.
Use differences between firmware systems as evidence for general machine concepts rather than as reasons to create firmware-specific ontology exceptions.