# Machine Builder — Project Context

## Project

Machine Builder is intended to become a **Machine Development Environment (MDE)** for describing, designing, understanding, validating, and eventually generating control representations for real machines.

It is not intended to be merely a firmware configurator.

The long-term conceptual flow is:

Physical Machine
    ↓
Canonical Machine Model
    ↓
Firmware / Control Representation

and:

Firmware / Configuration
    ↓
Semantic Parsing / Interpretation
    ↓
Canonical Machine Model

The canonical machine model is the primary semantic representation.

---

## Repository Structure

The current repository contains separate implementation and research areas.

```text
Machine-Builder/
├── machine-structure-editor/
│   └── Visual Builder implementation
│
├── machine-builder-research/
│   └── Research / architecture / ontology / standards
│
├── docs/
│   └── Existing and historical project documentation
│
├── hardware_database/
├── firmware_sources/
├── builder_versions/
└── README.md

The machine-structure-editor/ directory is the active implementation project.

The machine-builder-research/ directory is the durable research and architecture knowledge base.

Existing root-level documentation may contain useful historical material, but it is not automatically authoritative over the current research documents.

Chat Responsibilities
Research / Architecture

This workstream is responsible for:

terminology
nomenclature
ontology
semantic relationships
architecture
subsystem boundaries
standards research
machine-model concepts
research findings
architectural tradeoffs
unresolved conceptual questions
decisions affecting future implementation
Implementation / Coder

This workstream is responsible for:

application code
UI
visual builder implementation
tests
implementation architecture
implementation debugging
serialization
software versioning

The two workstreams exchange decisions and implementation feedback through explicit handoffs.

Current Implementation Status

The Machine Structure Editor has reached:

v0.1.0

This is an implementation milestone, independent of the research and ontology version streams.

The current implementation has established a working foundation around:

visual nodes
explicit ports
port-to-port connections
connection compatibility feedback
connection selection/deletion
undo/redo
multi-selection
component palette
automated testing

The next implementation work is continuing from the visual-builder architecture and requirements documents.

Research / Architecture Status

The research side is consolidating the first formal semantic ontology.

The current work has already established high-confidence distinctions among:

Object
Classification
Role
Aspect
Property
Relationship
Provenance

and among many machine concepts, including:

Axis
Joint
Link
Actuator
Motor
Drive
Controller

Sensor
Measurement Result
Feedback
Control Function
Control Loop

Function
Capability
Task
Operation
Action
Procedure
Safety Function

Port
Connection
Path

Coordinate Frame
Transform

The first formal ontology checkpoint is being prepared as:

O0.1

The broader research/architecture stream is tracked independently as:

R0.1
R0.2
...

Implementation remains independently versioned as:

v0.1.0
v0.2.0
...
Canonical Machine Model Principles

The canonical model must describe the machine independently of a particular firmware.

Firmware terms are implementation representations, not canonical identities.

The model must not assume:

one motor = one axis
one axis = one motor
one sensor = one function
one function = one component
one tool = one carriage
one subsystem = one controller
one connection = one wire

Real machines already demonstrate violations of these assumptions.

Object / Classification / Role / Aspect

The current foundational model distinguishes:

Object

An identifiable entity represented by the machine model.

Classification

What kind/type/category an object belongs to.

Role

What an object is being used as in a particular machine or context.

Aspect

A structured way of viewing or organizing the same underlying objects and relationships according to an engineering concern.

Property

A characteristic or value associated with an object.

Relationship

A typed semantic association between objects or other model entities.

Provenance

Evidence about where a fact, value, relationship, classification, inference, or derivation came from.

These distinctions are intended to prevent the model from becoming a rigid inheritance tree.

Examples

A physical motor can simultaneously have:

Object:
    Motor-017

Classification:
    Stepper Motor

Role:
    Z-axis actuator

Properties:
    current
    steps/revolution
    dimensions

Relationships:
    driven_by → Driver
    participates_in → Z motion
    part_of → Z assembly

The same type of motor could have a different role in another machine.

A catalog definition describes what a part/product is.

A machine component represents the actual occurrence installed in a machine.

Motion Architecture

The canonical model distinguishes:

Axis
Joint
Link
Actuator
Motor
Drive
Controller

A logical axis is not necessarily a motor.

A motor is not necessarily an axis.

A joint is a mechanical relationship and may be active or passive.

Kinematic relationships may be many-to-many.

Examples include:

CoreXY:
    multiple motors participate in multiple logical axes

Multi-Z:
    multiple motors participate in one logical axis

Coordinate systems are modeled separately from axes.

Coordinate Model

Coordinate frames are treated as first-class semantic candidates.

Conceptually:

CoordinateFrame
    ├─ parent
    ├─ transform
    ├─ semantic role
    └─ reference object

Examples may eventually include:

machine frame
work frame
tool frame
object frame
camera frame
task frame

Visual canvas coordinates are not machine coordinates.

Measurement Model

The current measurement architecture distinguishes:

Measurand
    ↓
Measurement System / Procedure
    ↓
Measurement Result
    ↓
Consumer

A measurement result may be consumed by:

control
calibration
diagnostics
display
logging
safety

Feedback is a use of measurement/information by a control process rather than a physical sensor subtype.

Function / Capability / Execution Model

Current working definitions are:

Capability:
    an ability possessed by a system

Function:
    a defined machine/subsystem behavior or service

Task:
    intended body of work

Operation:
    bounded executable work unit

Action:
    discrete executable behavior

Procedure:
    specified way of carrying out an activity/process

Control Function:
    function used to regulate or determine machine behavior

Safety Function:
    function required to achieve or maintain a safe state or reduce risk

Control Loop:
    a control implementation using setpoints and measured/estimated response

These concepts are related but are not interchangeable.

Port / Connection Model

Connections are centered on ports.

Preferred structure:

Component
    ↓
Port
    ↓
Connection
    ↓
Port
    ↓
Component

Port is not synonymous with:

connector
pin
signal
wire

Connection is not synonymous with a visual line.

Potential connection domains include:

electrical
signal
communication
mechanical
material
fluid
logical

The exact final subtype hierarchy remains under development.

Compatibility should be determined by semantic port information rather than visual appearance.

Subsystems

A subsystem is a bounded portion of a machine that may possess its own:

structure
functions
capabilities
resources
state
control behavior
communication interfaces

while still participating in the larger machine.

The Creality CFS is an important example.

A CFS can contain:

multiple material sources
rewind motors
filament-presence sensors
feeder motors
lower transport components
buffer
controller
communication interfaces
material paths

A higher-level machine function may span multiple subsystems.

Process Model

The current conceptual process structure is:

Product / Workpiece
        ↓
Process
        ↓
Task
        ↓
Operation / Working Step
        ↓
Action

A procedure describes how an activity or process is performed.

Machine functions may be realized during operations and actions.

This process model is intended to remain independent of firmware syntax.

Safety Architecture

Safety is modeled as a distinct semantic layer.

The current conceptual structure is:

Hazard
    ↓
Risk
    ↓
Risk Reduction Requirement
    ↓
Safety Function
    ↓
Safety-Related Control Implementation
    ↓
Verification / Validation

Important standards research includes:

ISO 12100
ISO 13849-1
ISO 13849-2
IEC 62061
ISO 13850
ISO 14118
ISO 14119
ISO 14120

Safety standards are treated as vocabulary and architecture evidence, not as a direct schema to copy.

Engineering Evaluation

The long-term builder is expected to perform engineering checks and recommendations in addition to representing machines.

A future electrical example is conductor/circuit evaluation involving:

voltage
current
wire gauge
conductor material
length
ampacity
voltage drop
temperature
installation conditions
protection
terminations
load

Such results should be modeled as engineering evaluations with explicit inputs, assumptions, methods, applicable standards, results, and provenance.

This is a future capability, not part of the current ontology checkpoint unless it exposes a foundational concept.

Catalog vs Machine Component

The project distinguishes:

Catalog / Product Definition
        ↓
Product Version / Type
        ↓
Actual Machine Component / Occurrence

Catalog information may describe:

specifications
dimensions
electrical characteristics
connectors
pins
manufacturer information
supplier information

A machine component adds context such as:

machine role
physical placement
wiring
relationships
current configuration
provenance

A catalog part should not directly become a machine component without an explicit creation/assignment step.

Firmware Model

Firmware is treated as an implementation representation.

The intended architecture is:

Firmware / Configuration
        ↓
Parser / Semantic Interpretation
        ↓
Canonical Machine Model

and:

Canonical Machine Model
        ↓
Target Validation
        ↓
Firmware Adapter / Generator
        ↓
Firmware Configuration

Supported or researched firmware/control systems include:

Klipper
RepRapFirmware
Marlin
FluidNC
GRBL
grblHAL
LinuxCNC
Repetier
Smoothieware
TinyG / g2core
others as research requires

Firmware terminology must be mapped to canonical concepts rather than becoming the canonical vocabulary.

Research Machines

Important machines and systems used as ontology stress tests include:

M3D Promega
Sovol SV08
LowRider 3
IdeaFormer IR3
Creality Hi / CFS
Stratasys 1200es
Carvera
K40
3018 CNC
IDEX systems
industrial servo/robotic systems

These examples are used to identify assumptions that fail across different architectures.

Standards Research

The research currently draws from multiple standards families, including:

ISO 841
ISO 8373
ISO 9787
IEC 81346
IEC 81346-14
ISO 10303 / STEP
ISO/ASTM 52900
ISO 14649
IEC 61131
IEC 61800
CiA 402
JCGM 200 / VIM
ISO 12100
ISO 13849
IEC 62061
ISO 13850
ISO 14118
ISO 14119
ISO 14120
ISO/IEC/IEEE 15288
ISO/IEC/IEEE 42010
ISO 15926
OPC UA information-model work

The current version/status of standards must be verified when they become authoritative to a decision because standards can be revised or replaced.

Evidence and Provenance

Important facts should retain, where practical:

source
source type
organization / author
title
version / edition
URL
date accessed
method
confidence
explicit / derived / inferred
validation status
notes

A standard reference should retain its designation and edition/version.

Historical versions must remain distinguishable from current editions.

The project should never silently overwrite an old standard reference merely because a newer edition exists.

Current Research Goal

The immediate research goal is to complete:

Machine Builder Ontology O0.1

The current consolidation sequence is:

Core concepts
    ↓
Definitions and boundaries
    ↓
Object / Classification / Role / Aspect
    ↓
Relationships
    ↓
Constraints / cardinality
    ↓
Provenance
    ↓
Real-machine stress testing
    ↓
Ontology O0.1

The goal is a semantic foundation, not a database schema.

Future Research Handoff

When a new research conversation needs to recover this project:

Read START_HERE.md.
Read PROJECT_CONTEXT.md.
Read RESEARCH_ROADMAP.md.
Read the current architecture and ontology documents.
Check DECISION_LOG.md.
Check OPEN_QUESTIONS.md.
Use standards, machine, and firmware indexes for detailed evidence.

Do not treat historical notes as current decisions without checking the current authoritative documents.