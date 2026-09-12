# Machine Builder Research & Architecture

## Purpose

This directory is the durable research, architecture, terminology, ontology, standards, and machine-knowledge record for the Machine Builder / Machine Development Environment (MDE) project.

The implementation repository is:

```text
Machine-Builder/
└── machine-structure-editor/

The Machine Structure Editor contains application implementation and has its own implementation version history.

This directory contains the research and architecture knowledge that guides that implementation.

Start Here

Read these files in this order when recovering project context:

PROJECT_CONTEXT.md
RESEARCH_ROADMAP.md
architecture/ARCHITECTURE_OVERVIEW.md
ontology/TERMINOLOGY_BASELINE.md
ontology/ONTOLOGY_CURRENT.md
decisions/DECISION_LOG.md
questions/OPEN_QUESTIONS.md

Use the indexes in standards/, machines/, and firmware/ to locate deeper research when required.

Responsibility Boundary
This directory

Contains:

research
standards analysis
terminology
ontology
semantic relationships
architectural decisions
machine research
firmware research
unresolved questions
research-to-implementation handoffs
machine-structure-editor/

Contains:

application code
UI implementation
tests
implementation configuration
implementation documentation
software version history

Research decisions may affect implementation, but implementation files should not become the authoritative source for the canonical machine ontology.

Versioning

The project uses independent version streams.

Implementation
v0.1.0
v0.2.0
v0.3.0
Research / Architecture
R0.1
R0.2
R0.3
Ontology
O0.1
O0.2
O0.3

These versions may reference one another but do not need to advance together.

Current Status
Implementation

Machine Structure Editor:

v0.1.0

The visual builder has working foundations for nodes, ports, connections, compatibility feedback, selection, editing, and related interaction behavior.

The implementation is currently moving into its next development stage.

Research / Architecture

The research side is consolidating the foundational semantic model and preparing the first formal ontology checkpoint.

The current major research focus is:

Object
Classification
Role
Aspect
Relationship
Property
Provenance

followed by finalizing the first canonical concept and relationship model.

Core Principle

Machine Builder is intended to represent machines independently of any single firmware.

The long-term flow is:

Physical Machine
        ↓
Canonical Machine Model
        ↓
Firmware / Control Representation

and:

Firmware / Configuration
        ↓
Semantic Interpretation
        ↓
Canonical Machine Model

The canonical model describes the machine.

Firmware is one possible implementation of that machine.

Current Architectural Direction

The project is moving toward a structured semantic model based on:

Objects
Classifications
Roles
Aspects
Properties
Typed Relationships
Evidence / Provenance

rather than a rigid inheritance-only hierarchy.

Important distinctions currently include:

Axis ≠ Motor
Axis ≠ Joint
Joint ≠ Actuator
Motor ≠ Drive
Drive ≠ Controller

Sensor ≠ Measurement Result
Measurement Result ≠ Feedback

Function ≠ Capability
Function ≠ Action
Function ≠ Operation
Operation ≠ Procedure
Task ≠ Function

Port ≠ Connector
Port ≠ Pin
Connection ≠ Visual Line
Physical Connection ≠ Logical Mapping

Visual Position ≠ Physical Position
Runtime State ≠ Configuration
Firmware Term ≠ Canonical Concept
Current High-Confidence Concept Areas

The current ontology research includes concepts such as:

Machine
Subsystem
Component
Axis
Joint
Link
Actuator
Motor
Drive
Controller

Sensor
Measurand
Measurement System
Measurement Result

Coordinate Frame
Transform

Function
Capability
Control Function
Safety Function
Control Loop
Command
Signal
State
Fault

Process
Task
Operation
Working Step
Action
Procedure

Tool
Mechanical Interface

Port
Connection
Path

Property
Quantity
Unit
Uncertainty
Provenance

Some concepts remain intentionally unresolved and should not be treated as finalized:

Resource
Channel
Flow
Route
Evidence Principle

Research conclusions must remain distinguishable from their sources.

Important information should preserve, where practical:

source
source type
organization / author
title
version / edition
URL
date accessed
relevant concept
what the source establishes
what the source does not establish
confidence
notes

Direct evidence, inference, derived values, and assumptions should not be silently mixed.

Authority Principle

Every important concept should have one current authoritative location.

Current documents should describe the present architecture and terminology.

Historical research should remain available as evidence but should not silently override current decisions.

When a decision changes:

current document
    ↓
new definition

decision log
    ↓
why the change happened

Historical material should remain identifiable as historical.

Research ↔ Implementation Loop

The intended workflow is:

Research
    ↓
Architectural Decision
    ↓
Implementation Handoff
    ↓
Implementation
    ↓
Testing / Observation
    ↓
Research Feedback
    ↓
Refined Architecture

Implementation discoveries are evidence and may cause research decisions to change.

Research decisions are not considered implemented until the implementation work actually incorporates them.

Future Chat Recovery

A new research/architecture conversation should be able to recover the project without relying on the historical conversation that produced these files.

Start with:

START_HERE.md

then read:

PROJECT_CONTEXT.md
RESEARCH_ROADMAP.md

and only then open the current architecture, ontology, decisions, questions, standards, machine, or firmware material required for the task.

The purpose of this structure is to preserve the project's knowledge independently of any single ChatGPT conversation.