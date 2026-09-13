# Machine Builder Current Ontology
## O0.1 Minimum 3D-Printer Model

## 1. Purpose

This document records the current O0.1 canonical semantic model for Machine Builder.

It is a working ontology checkpoint, not a final ontology for all machine domains.

## 2. Scope

O0.1 is intentionally optimized for describing and translating 3D printers.

Supported domains are centered on:

- mechanical machine structure
- moving axes and kinematics
- motors / actuators / drives
- extruders / tools
- heaters / fans
- sensors / probes / endstops
- controllers / controller resources
- electrical connections
- machine Functions / Capabilities
- Properties / calibration / provenance
- firmware context and mappings

Future fluid, hydraulic, fuel, liquid-cooling, and general plumbing semantics are deferred.

## 3. Semantic foundation

### Object
An identifiable modeled entity.

Examples: Machine, Machine Component, Motor, Sensor, Controller, Axis, Port, Tool.

### Classification
What kind or category of thing an Object is.

### Role
How an Object participates in a specific machine context.

### Aspect
An engineering viewpoint such as Physical, Electrical, Functional, or Control.

### Property
A characteristic/value associated with an Object or justified Relationship.

Properties may carry unit, source, uncertainty, validity, confidence, method, and version context.

### Relationship
A typed semantic association between modeled entities. Relationship definitions may specify direction, multiplicity, scope, and constraints.

### Provenance
Information describing where and how a fact, relationship, classification, derived value, or result was established.

Minimum provenance information:

- source
- evidence type
- method
- date/version/context
- confidence when meaningful
- derivation/supporting evidence

## 4. Machine structure

### Machine
The primary system of interest.

### Machine Component
An actual machine-specific hardware occurrence. It is distinct from a Catalog Product.

### Catalog Product
An external product definition. Catalog information does not automatically instantiate a machine component.

### Product Version
A specific product revision/variant when specifications or behavior differ.

### Subsystem
A bounded portion of a Machine that may contain components, functions, resources, interfaces, and local control.

## 5. Motion

### Axis
Machine-level motion/coordinate semantics. Axis is not Motor, Drive, Joint, or firmware channel.

### Joint
A constrained mechanical relationship permitting relative motion. Included where needed by the machine model; not required for every simple printer.

### Link
A relatively rigid physical element in a mechanical structure.

### Actuator
An element capable of producing a controlled physical effect.

### Motor
An electromechanical energy-conversion device producing mechanical motion.

### Drive
A control system/component responsible for controlling a motor or actuator.

### Kinematic Relationship
A relationship expressing how motions are coupled/transformed.

O0.1 must support at least:

- ordinary Cartesian motion
- multi-actuator axes
- CoreXY
- IDEX-style multiple carriages
- belt-printer arrangements

## 6. Coordinates

### Coordinate Frame
A reference coordinate system with defined machine meaning.

### Transform
The mathematical relationship between coordinate frames.

### Canvas Coordinate
A visual-model coordinate. It is not physical machine position.

## 7. Electrical connectivity

### Port
A semantic interface endpoint.

O0.1 focuses Port on electrical printer interfaces, while leaving later domains open.

### Connector
A physical electrical connector structure that may contain multiple pins/terminals.

### Pin / Terminal
A discrete electrical contact/terminal used to identify electrical endpoints within the supported connection model.

### Connection
A semantic relationship between compatible electrical endpoints.

Physical electrical connections are normally nondirectional. Semantic signals may have direction.

A Connection is not a visual line.

## 8. Sensors / thermal devices

### Sensor
A physical sensing component.

### Measurement Result
A result produced from sensing, distinct from the Sensor itself.

### Probe
A sensor/interface arrangement used for machine probing or related reference detection.

### Endstop
A machine reference/limit sensing arrangement. It may be physical, electrical, or otherwise implemented by the controller/drive as appropriate to the machine.

### Heater
A physical heating component controlled through a machine/controller resource.

### Fan
A cooling/air-moving component controlled through a machine/controller resource.

## 9. Controller

### Controller
A computing/control entity responsible for coordinating machine resources or behaviors.

### Controller Resource
A finite resource or capability supplied by a Controller.

Examples:

- stepper driver channel
- GPIO
- ADC input
- PWM output
- timer
- UART
- CAN
- Ethernet
- other resources actually needed by supported printer configurations

Controller Resources remain associated with their Controller.

Shared use is represented through allocation/usage relationships and constraints.

## 10. Function and capability

### Capability
An outcome/ability the machine or subsystem can provide.

### Function
A meaningful machine behavior/service.

A Function is not a universal parent of Task, Operation, Action, or Procedure.

Function applicability depends on the machine's structure, purpose, configuration, and context.

The user interface may group/filter applicable Functions by purpose, subsystem, firmware relevance, setup state, diagnostics, or another view without duplicating the Function itself.

### Control Function
A Function used to regulate machine behavior through information, commands, measurements, or feedback.

## 11. Tools and printer-specific machine behavior

### Tool / Extruder
A machine element or subsystem associated with applying/removing/processing material in the printer context.

O0.1 supports ordinary and multiple extruders/tools but does not attempt a universal manufacturing-tool ontology.

## 12. Properties and calibration

Property values may be:

- known
- unknown
- absent
- not applicable
- observed/measured
- derived
- inferred
- configured
- calibrated

Derived nominal values and calibrated working values may coexist.

## 13. Firmware

### Firmware Context
The optional current or target firmware context associated with a machine.

### Firmware Family
The firmware ecosystem, such as Klipper, Marlin, or RepRapFirmware.

### Firmware Version
The target/current firmware version or version range relevant to representation and compatibility.

### Firmware Capability
A capability supported by a particular firmware target/version/hardware context.

### Firmware Term
A firmware-specific command, configuration key, object-model term, macro concept, or other representation term.

### Firmware Mapping
A mapping from canonical machine semantics to firmware-specific representation or the reverse.

Mappings may be one-to-one, one-to-many, many-to-one, conditional, calculated, transformed, or version-specific.

### Translation Result
The outcome of transforming one representation into another.

Useful statuses include:

- semantic-preserving
- transformed
- approximated
- partial
- unsupported
- manual intervention required

Firmware-specific customizations such as macros are separate from physical machine identity.

## 14. Evaluation

Evaluation results are derived information, not permanent canonical facts.

O0.1 evaluation is limited to the minimum structure necessary to support future structural, compatibility, requirement, and calculation checks.

Full engineering simulation and certification-grade analysis are later concerns.

## 15. Deferred concepts

The following remain intentionally outside the minimum O0.1 model:

- universal Flow ontology
- universal fluid/mechanical/material interface ontology
- hydraulic/fuel/fluid systems
- water-cooling/plumbing semantics
- full process/task/operation/action/procedure execution ontology
- advanced robotics configuration-space semantics
- complete safety ontology
- full simulation ontology
