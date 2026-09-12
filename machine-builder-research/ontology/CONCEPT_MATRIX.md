# Machine Builder Concept Matrix

## 1. Purpose

This document provides a working matrix of the major concepts currently identified for the Machine Builder ontology.

Its purpose is to make the relationships between concepts visible while preserving distinctions that are important to the architecture.

This is not yet a database schema.

It is a semantic planning artifact used to answer questions such as:

- What kind of concept is this?
- What does it describe?
- What does it relate to?
- What should it not be confused with?
- How mature is the concept?
- What real machine cases require it?

---

## 2. Concept Categories

The current ontology uses several broad semantic categories.

```text
Core Modeling
    Object
    Classification
    Role
    Aspect
    Property
    Relationship
    Provenance

Machine Structure
    Machine
    Machine Component
    Subsystem
    Catalog Product
    Product Version

Motion / Geometry
    Axis
    Joint
    Link
    Actuator
    Motor
    Drive
    Kinematic Relationship
    Coordinate Frame
    Transform

Interfaces / Connectivity
    Port
    Connector
    Pin
    Connection
    Physical Connection
    Logical Mapping
    Path
    Harness

Measurement / Information
    Sensor
    Measurand
    Measurement
    Measurement Result
    Feedback

Functions / Process
    Capability
    Function
    Task
    Process
    Operation
    Action
    Procedure
    Control Function
    Safety Function
    Control Loop

Control / Computing
    Controller
    Controller Resource
    Firmware
    Firmware Mapping
    Firmware Term
    Configuration
    Runtime State
    Mode
    Fault

Safety
    Hazard
    Risk
    Risk Reduction Requirement
    Safety-Related Control Implementation
    Safe State
    Guard
    Interlock

Engineering Evaluation
    Constraint
    Compatibility
    Verification
    Validation
    Evaluation Result

Visual Representation
    Visual Model
    Node
    Visual Connection
    Canvas
3. Core Modeling Concepts
Concept	Category	Primary Purpose	Common Confusion	Current Status
Object	Core	Identifiable modeled entity	Class, component	Accepted
Classification	Core	Describes what kind/type an Object is	Role	Accepted
Role	Core	Describes contextual participation	Classification, Function	Accepted
Aspect	Core	Engineering view/structuring dimension	Classification	Accepted
Property	Core	Characteristic/value	Classification	Accepted
Relationship	Core	Typed semantic association	Visual edge	Accepted
Provenance	Core	Evidence and origin information	Comment/note	Accepted
Architectural observation

These concepts are intended to work together.

An Object may:

have one or more Classifications;
perform one or more Roles;
be viewed through multiple Aspects;
have Properties;
participate in Relationships;
have Provenance attached to any of the above.

This avoids forcing all semantic meaning into a rigid inheritance tree.

4. Machine Structure Matrix
Concept	What It Represents	Distinct From	Example
Machine	Whole system of interest	Subsystem	3D printer
Machine Component	Actual machine-specific hardware occurrence	Catalog Product	Installed Z motor
Catalog Product	Product definition	Machine Component	Motor model
Product Version	Specific revision/variant	Product	Motor revision B
Subsystem	Bounded machine portion with internal structure	Simple group	CFS
Occurrence	Context-specific occurrence of a product/entity	Product definition	Installed controller
Key distinction
Catalog Product
      ↓
Product Version
      ↓
Machine Component

The catalog describes what exists.

The Machine Component describes what exists in the particular machine.

5. Motion Matrix
Concept	Describes	Is Not	Example
Axis	Logical machine motion/coordinate semantics	Motor	X axis
Joint	Constrained relative mechanical motion	Axis	Rotary joint
Link	Rigid/structural mechanical element	Joint	Gantry member
Actuator	Element producing controlled physical effect	Motor alone	Z actuator assembly
Motor	Electromechanical energy conversion	Axis	Stepper motor
Drive	Control system for actuator/motor	Motor	Servo drive
Kinematic Relationship	Motion transformation/coupling	Simple connection	CoreXY
Coordinate Frame	Reference coordinate system	Canvas position	Tool frame
Transform	Relationship between coordinate frames	Coordinate Frame	Tool-to-machine transform
Important architectural rule

The model must support:

many motors → one axis
one motor → multiple coordinated motions
many actuators → one mechanism
one actuator → multiple machine functions

This is why Axis, Motor, Joint, Actuator, and Drive cannot be collapsed.

6. Coordinate Matrix
Concept	Meaning	Example	Important Distinction
Coordinate Frame	Engineering reference system	Machine frame	Not visual coordinates
Transform	Mapping between frames	Tool→machine transform	Not a frame itself
Canvas Coordinate	UI location	Node x/y	Not physical location
Physical Position	Location in a physical frame	Tool position	Not canvas location
Stress cases

Coordinate modeling should eventually handle:

belt printers;
rotary axes;
robot-like machines;
tool offsets;
camera systems;
multi-axis machines.
7. Interface and Connectivity Matrix
Concept	Purpose	Distinct From	Example
Port	Semantic interface endpoint	Connector, Pin	Motor power port
Connector	Physical interface structure	Port	JST connector
Pin	Individual contact/terminal	Port	Pin 1
Connection	Semantic connection	Visual line	Port A↔Port B
Physical Connection	Physical linkage/path	Logical mapping	Wire
Logical Mapping	Logical correspondence	Physical connection	Heater enable
Path	Physical/topological route	Flow	Filament path
Harness	Grouped routed physical elements	Single wire	Toolhead harness
Domain examples

Ports may participate in:

Electrical
Signal
Communication
Mechanical
Material
Fluid
Logical

The exact domain structure remains subject to further ontology refinement.

8. Measurement Matrix
Concept	Meaning	Distinct From	Example
Sensor	Element involved in obtaining measurement information	Measurement Result	Thermistor
Measurand	Quantity being measured	Sensor	Temperature
Measurement	Activity/process of measuring	Result	Temperature measurement
Measurement Result	Information produced by measurement	Sensor	205 °C
Feedback	Use of measurement information in control	Sensor	Temperature feedback
Key architecture
Sensor
   ↓
Measurement
   ↓
Measurement Result
   ↓
Possible consumers
    ├── Control
    ├── Diagnostics
    ├── Calibration
    ├── Display
    ├── Logging
    └── Safety

The same measurement may have multiple consumers.

9. Functional Matrix
Concept	Core Question	Example	Distinct From
Capability	What can it do?	Can heat	
Function	What behavior/service does it provide?	Maintain temperature	
Task	What intended work is to be performed?	Print part	
Process	What organized activity achieves a result?	Additive manufacturing	
Operation	What bounded work unit is executed?	Heat build volume	
Action	What discrete behavior occurs?	Enable heater	
Procedure	How is an activity carried out?	Heating procedure	
Control Function	How is behavior regulated?	Temperature control	
Safety Function	What function provides/reduces safety risk?	Prevent restart	
Control Loop	How do setpoint, control and feedback interact?	Heater PID loop	
Important rule

These concepts form a vocabulary of related meanings, not one universal inheritance hierarchy.

For example:

Task
    may contain Operations

Operation
    may invoke Actions

Function
    may be implemented by Operations/Actions

Procedure
    may specify how a Task/Operation is performed

Control Function
    is a specialized Function

Safety Function
    is a specialized Function in the safety context

The exact formal relationships remain under development.

10. Control and Computing Matrix
Concept	Purpose	Example	Distinct From
Controller	Coordinates machine control/resources	Duet board	Firmware
Controller Resource	Finite control capability	Driver 2	Whole controller
Firmware	Software executing control behavior	RRF	Canonical model
Firmware Mapping	Correspondence between canonical and firmware semantics	Z axis→M584 mapping	Raw parameter
Firmware Term	Firmware-specific semantic term	M584	Canonical concept
Configuration	Intended setup	80 steps/mm	Runtime state
Runtime State	Current condition	Z homed	Configuration
Mode	Current operational behavior context	Homing	Generic state
Fault	Abnormal/required intervention condition	Driver fault	Configuration
11. Safety Matrix
Concept	Meaning	Example
Hazard	Source of potential harm	Moving gantry
Risk	Likelihood/severity associated with harm	Pinch risk
Risk Reduction Requirement	Required risk reduction	Prevent access while moving
Safety Function	Function used for risk reduction	Guard interlock stop
Safety-Related Control Implementation	Implementation realizing safety function	Safety relay/controller
Safe State	Defined safe condition	Motion disabled
Guard	Physical protective barrier	Door
Interlock	Relationship/device monitoring guard state	Door switch
Conceptual chain
Hazard
  ↓
Risk
  ↓
Risk Reduction Requirement
  ↓
Safety Function
  ↓
Safety-Related Implementation
  ↓
Validation
  ↓
Safe State

Safety concepts should retain standards references and evidence.

12. Engineering Evaluation Matrix
Concept	Purpose	Example
Constraint	Condition that must be satisfied	Driver current limit
Compatibility	Determines whether entities work together	Port voltage compatibility
Verification	Conformance to specified requirement	Check generated setting
Validation	Confirmation of suitability/intended behavior	Validate safety function
Evaluation Result	Derived assessment	WARNING
Provenance	Explains evidence/method	Datasheet + calculation

Potential evaluation statuses:

PASS
WARNING
RECOMMENDATION
INVALID
UNKNOWN

These statuses are not themselves machine facts.

13. Visual Matrix
Concept	Purpose	Canonical?	Example
Visual Model	UI representation	No	Builder state
Node	Visual object	No	Motor node
Visual Connection	Rendered relationship	No	Connection line
Canvas	Visual workspace	No	Builder canvas
Canvas Coordinate	Visual location	No	x=350, y=200
Rule

The canonical model may be projected into multiple visual models.

One visual model must not be assumed to be the only valid representation of the machine.

14. Relationship Matrix

The following relationships are currently important enough to treat as explicit candidates.

Relationship	Source	Target	Meaning
contains	Machine/Subsystem	Object/Subsystem	Structural containment
part_of	Object	Object	Structural membership
classified_as	Object	Classification	Type/category
has_role	Object	Role	Contextual participation
has_property	Object/Relationship	Property	Characteristic
mounted_on	Object	Object	Physical attachment
connected_to	Port/Object	Port/Object	Connectivity
measures	Sensor/System	Measurand	Measurement relationship
participates_in	Object	Axis/Function/Process	Contribution
drives	Drive/Actuator	Motion/Mechanism	Active control/drive relationship
implements	Entity	Function/Requirement	Realization
maps_to	Entity	Entity	Correspondence
derived_from	Fact/Result	Source Fact(s)	Derivation
supported_by	Claim/Fact	Evidence	Supporting evidence
has_parent_frame	Coordinate Frame	Coordinate Frame	Frame hierarchy
transformed_by	Frame/Object	Transform	Coordinate transformation
has_resource	Controller	Controller Resource	Resource ownership
generated_by	Result	Method/Process	Derivation context

This matrix is expected to grow.

15. One-to-Many and Many-to-Many Expectations

The ontology must not assume that relationships are universally one-to-one.

Examples:

Multiple Motors → One Axis
Motor A ─┐
Motor B ─┼──→ Z Axis
Motor C ─┘
One Sensor → Multiple Consumers
                 ┌──→ Control
Sensor → Result ─┼──→ Diagnostics
                 └──→ Logging
One Controller → Many Resources
Controller
 ├── Driver 0
 ├── Driver 1
 ├── GPIO 4
 ├── ADC 2
 └── CAN
One Logical Signal → Multiple Physical Elements
Logical Signal
      ↓
Mapping
   ├── Pin
   ├── Wire
   └── Connector

Multiplicity should therefore be explicit rather than assumed.

16. Classification Versus Role Matrix

This distinction is central.

Statement	Classification or Role?	Why
"This is a stepper motor."	Classification	Describes what it is
"This motor drives the Z axis."	Role	Describes contextual use
"This board is a controller."	Classification	Describes type
"This board controls the printer."	Role/context	Describes participation
"This sensor is a thermistor."	Classification	Device type
"This sensor measures bed temperature."	Role/relationship	Context of use
"This motor is an extruder actuator."	Role	Machine-specific use

One object may retain its classification while changing roles.

17. Function Versus Capability Matrix
Statement	Capability	Function
"Can heat the bed."	Yes	No
"Maintain bed temperature."	No	Yes
"Can move the tool."	Yes	No
"Move tool along X."	No	Yes
"Supports tool changing."	Yes	Potentially
"Perform tool change."	No	Yes

Capability concerns ability.

Function concerns defined behavior/service.

18. Physical Versus Logical Matrix
Example	Physical	Logical
Wire connecting two pins	Yes	Possibly
Temperature signal	No	Yes
Connector	Yes	No
Heater enable mapping	No	Yes
Motor mechanically coupled to belt	Yes	Possibly
Axis mapping in firmware	No	Yes
Visual line between nodes	No	No

Some real-world elements participate in both domains, but the concepts remain distinct.

19. Configuration Versus State Matrix
Example	Configuration	Runtime State
Maximum temperature = 250 °C	Yes	No
Current temperature = 205 °C	No	Yes
X steps/mm = 80	Yes	No
X position = 120 mm	No	Yes
Driver current = 1.2 A	Yes	No
Driver faulted	No	Yes
Tool assigned to Toolhead 1	Yes	Potentially
Tool currently mounted	No	Yes

Some values may have both configured and runtime forms.

20. Provenance Matrix
Information Type	Typical Source	Example
Documented Fact	Manufacturer document	Motor current
Observation	Physical inspection	Wire connects to pin 3
Measurement	Instrument/test	Resistance
Derived	Calculation	Steps/mm
Inference	Reasoning from evidence	Motor likely Z
User Assertion	User-provided information	"This is stock"
Standard Requirement	Standard	Safety requirement
Firmware Fact	Firmware source/config	Driver assignment

These should not be treated as equally strong evidence.

21. Concept Maturity

The current maturity of major concept groups is approximately:

Concept Group	Maturity
Object / Classification / Role / Aspect	High
Provenance / Evidence	High
Relationships	High-level established, details incomplete
Machine Component / Catalog	High
Motion / Axis / Joint / Actuator	High-level established
Coordinate Frames	High-level established
Ports / Connections	High-level established
Measurement	High-level established
Function Vocabulary	High-level established
Control	Medium
Safety	Medium
Process / Manufacturing	Medium
Controller Resources	Medium
Engineering Evaluation	Medium
Firmware Mapping	Medium
Runtime State	Medium
Visual Semantics	High enough for current implementation
Full ontology constraints/cardinality	Early
Storage/schema	Deferred

"Maturity" describes semantic confidence, not implementation completeness.

22. Stress-Test Matrix

The ontology should be tested against at least the following machine patterns.

Stress Case	Primary Concepts Tested
Promega	Axis, controller resources, firmware mapping, probing
SV08	Multiple Z actuators, distributed control, coordinate structure
LowRider	Multiple actuators, squaring, CNC process
IR3	Coordinate transforms, belt kinematics
CFS	Subsystem, material paths, local control, interfaces
CoreXY	Kinematic relationships
IDEX	Multiple tools, coordinated motion, process/tool semantics
Tool Changer	Tool, toolhead, carriage, process
Closed Loop	Measurement, feedback, control loop
CNC	Operation, tool, workholding, coordinate frames
Industrial Machine	Safety, controller resources, subsystems, aspects

A concept that fails a stress case should trigger ontology review rather than immediate special-case implementation.

23. Current Deliberate Gaps

The following concepts are intentionally not considered fully resolved.

Flow

May be useful for:

material;
fluid;
energy;
communication.

However, it risks becoming an overly broad abstraction.

Signal

Has multiple meanings across electrical, logical, control, and communication domains.

Channel

May refer to:

physical;
logical;
communication;
controller resources;
measurement.
Event

Likely useful but not yet sufficiently defined for universal use.

Resource

Useful at the controller level but potentially too broad as a universal concept.

Interface

Useful term, but its relationship to Port, Connector, Pin, API, and protocol requires continued refinement.

State

Clearly important, but the exact relationship among State, Mode, Fault, Operating State, and Configuration State remains under development.

These are active ontology questions rather than omissions to be filled automatically.

24. Current Ontology Direction

The current model is moving toward:

Object
├── Classification
├── Role
├── Aspect
├── Property
├── Relationship
└── Provenance

with specialized domains connected through typed concepts:

Machine Structure
Motion
Coordinates
Connectivity
Measurement
Functions
Control
Process
Safety
Controllers
Firmware
Engineering Evaluation
Visual Representation

This is preferable to a single deep inheritance hierarchy.

25. Guiding Rule for New Concepts

Before adding a concept, determine:

What semantic problem does this concept solve?

What existing concept is insufficient?

What does the new concept mean?

What does it explicitly not mean?

Which real machine requires the distinction?

Which standard or engineering practice supports it?

What relationships does it participate in?

What evidence would establish it?

A new concept should exist because it preserves an important engineering distinction.

26. Summary

The Concept Matrix is a map of the current ontology rather than a finalized schema.

Its most important conclusions are:

Objects need classification, role, aspect, properties, relationships, and provenance.
Physical machine structure must remain distinguishable from logical, functional, and visual structures.
Motion concepts must not collapse into motor-centric assumptions.
Interfaces and connections need domain-aware semantics.
Measurement must be separated from sensors and feedback.
Function vocabulary must preserve its distinct meanings.
Catalog products and machine components are different concepts.
Configuration and runtime state are different.
Firmware terminology is not canonical terminology.
Unknown and uncertain information must remain representable.
Relationship multiplicity must be flexible.
Stress cases are required to validate the ontology.

The matrix will evolve as relationship constraints, provenance, controller resources, process semantics, firmware mappings, and machine stress tests are refined.