# Machine Builder Concept Matrix
## O0.1 Minimum Scope

| Concept | O0.1 | Purpose in O0.1 | Notes / Deferral |
|---|---|---|---|
| Machine | Yes | Primary machine identity | Physical machine is the machine |
| Machine Component | Yes | Installed physical occurrence | Preferred over part instance |
| Catalog Product | Yes | External product definition | Separate from installed component |
| Product Version | Yes | Variant/revision identity | Important for hardware/firmware compatibility |
| Subsystem | Yes | Bounded machine grouping | CFS/toolhead/controller groups can use it |
| Axis | Yes | Machine motion semantics | Not a motor or firmware channel |
| Joint | Conditional | Mechanical relation when needed | Do not require for simple Cartesian printers |
| Link | Conditional | Rigid structural element | Use when mechanical model needs it |
| Actuator | Yes | Controlled physical effect | May include motor/drive/transmission |
| Motor | Yes | Motion-producing component | Stepper/servo/etc. |
| Drive | Yes | Motor/actuator control layer | Distinct from Controller |
| Kinematic Relationship | Yes | Coupled/transformed motion | CoreXY, multi-actuator, belt printer |
| Coordinate Frame | Yes | Machine coordinate semantics | Needed for robust transforms/offsets |
| Transform | Yes | Frame relationship | Separate from visual coordinates |
| Port | Yes | Semantic electrical endpoint | Broader future domains deferred |
| Connector | Yes | Physical electrical connector structure | O0.1 electrical scope |
| Pin / Terminal | Yes | Discrete electrical contact | Electrical-only first version |
| Connection | Yes | Semantic electrical connectivity | Physical connection distinct from visual line |
| Sensor | Yes | Physical sensing component | Distinct from measurement result |
| Measurement Result | Yes | Result of sensing | Provenance/context important |
| Probe | Yes | Printer probing function/input | Includes common Z-probe use cases |
| Endstop | Yes | Reference/limit sensing | Sensorless variants must remain representable |
| Heater | Yes | Thermal actuator | Electrical/control mapping needed |
| Fan | Yes | Cooling/air-moving actuator | Electrical/control mapping needed |
| Tool / Extruder | Yes | Material application hardware | Printer-focused scope |
| Controller | Yes | Machine control entity | May be multiple per machine |
| Controller Resource | Yes | Finite resource/capability | Driver/GPIO/ADC/PWM/etc. |
| Function | Yes | Machine behavior/service | Applicable by machine context/purpose |
| Capability | Yes | Outcome/ability | Distinct from Function |
| Control Function | Yes | Regulation/control behavior | Use where needed |
| Property | Yes | Machine values/characteristics | Supports units/context/provenance |
| Calibration | Yes | Empirical working values | May differ from derived nominal values |
| Provenance | Yes | Evidence and derivation | Cross-cutting |
| Firmware Context | Yes | Current/target implementation context | Optional for machine identity |
| Firmware Family | Yes | Target ecosystem | Klipper/Marlin/RRF |
| Firmware Version | Yes | Version-specific translation | Important for compatibility |
| Firmware Capability | Yes | Target-supported behavior | Supported vs configured vs unsupported |
| Firmware Term | Yes | Target-specific representation | Never canonical by itself |
| Firmware Mapping | Yes | Canonical ↔ firmware translation | Many mapping forms |
| Translation Result | Yes | Preserve/report conversion outcome | Loss must never be silent |
| Evaluation Result | Limited | Derived checks | Full evaluator later |
| Function/Operation hierarchy | No | Not required for firmware generation | Defer richer execution ontology |
| Process | Deferred | Workflow/process modeling | Future |
| Task | Deferred | Work-unit modeling | Future |
| Operation | Deferred | Executable work unit | Future |
| Action | Deferred | Discrete executable behavior | Future |
| Procedure | Deferred | How work is performed | Future |
| Universal Flow | Deferred | Cross-domain transfer abstraction | Revisit with actual need |
| Fluid Interface | Deferred | Fluid systems | O0.2+ |
| Water Cooling Model | Deferred | Liquid-cooled hotends | O0.2 target |
| Filament Plumbing/Path Detail | Deferred | Tubing/couplers/material path | O0.2 target |
