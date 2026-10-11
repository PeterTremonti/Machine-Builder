# Machine Builder — Master Plan

## 1. Purpose

Machine Builder is intended to become a machine-model-first engineering environment for describing, inspecting, documenting, validating, configuring, and eventually designing real machines.

The initial practical focus is 3D printers and related motion-control machines.

The underlying architecture is intentionally broader so that the system can eventually support CNC, laser machines, hybrid manufacturing systems, and other machines without replacing the canonical machine model.

The central principle is:

> The physical machine is the machine. Firmware is a versioned implementation of that machine, not the machine's identity.

---

# 2. Original idea

The project originally began as a way to configure and ultimately convert a real printer to working firmware.

The original problem exposed a larger need:

* hardware identification
* board and resource mapping
* wiring documentation
* compatibility checking
* diagnostics
* firmware translation
* machine documentation
* eventually physical machine representation

The project therefore evolved from a firmware configurator into a machine-building/modeling system.

---

# 3. Working idea

The current working concept is a machine-model-first system built around a canonical semantic representation.

The broad pipeline is:

```text
Physical Machine
        ↓
Canonical Machine Model
        ↓
Firmware Requirements / Mapping
        ↓
Target Firmware + Version
        ↓
Generated Configuration
```

The reverse direction is also important:

```text
Firmware / Configuration
        ↓
Semantic Interpretation
        ↓
Canonical Machine Model
```

The canonical machine model is authoritative.

Visual/editor state is an authoring and presentation layer over that model rather than a second semantic model.

---

# 4. Core architecture

The current working semantic chain is approximately:

```text
Physical Machine
        ↓
Machine Component
        ↓
Hardware Definition
        ↓
Controller
        ↓
Controller Resource
        ↓
Port / Connector / Pin
        ↓
Connection
        ↓
Function / Capability
```

Important distinctions must remain explicit.

```text
Hardware Definition
    ≠
installed hardware instance

Controller
    ≠
Controller Resource

Controller Resource
    ≠
physical Port / Connector / Pin

physical Connection
    ≠
Controller Resource Assignment

Function
    ≠
Capability

canonical semantic state
    ≠
visual/editor state
```

New entities should not be introduced merely because an implementation concept has a useful name. Concrete evidence should demonstrate that the existing model cannot represent the required meaning.

---

# 5. V0.2

V0.2 is the current implementation milestone.

The goal is to establish a dependable canonical machine model and a usable visual/editor foundation rather than prematurely implementing the entire long-term vision.

The current implementation includes substantial semantic-authoring and visual-editor infrastructure.

The repository and automated tests are authoritative for actual implementation status.

---

# 6. Current hardware direction

The initial hardware catalog should prioritize real, documented hardware for which reliable specifications and provenance can be established.

Important current examples include:

* Duet 2 Maestro
* BTT Octopus V1.1
* BIGTREETECH TMC5160T V1.0
* real motors, heaters, sensors, fans, probes, and other documented machine hardware

Reusable Hardware Definitions describe known hardware.

Installed Machine Components and Controllers represent the machine-specific instances.

---

# 7. Current Board architecture direction

Board work is currently using:

```text
HardwareDefinition
        ↓
installed Controller / MachineComponent
        ↓
controller-owned or component-owned SemanticPort
        ↓
connector grouping / interface metadata
        ↓
semantic relationships and physical/electrical connections
```

Recent Maestro and Octopus implementation experiments have provided evidence that the current model can represent:

* multiple connector groups
* different connector sizes and interface types
* one Controller Resource exposed through multiple physical access points
* replaceable driver-module interfaces
* controller-owned and component-owned physical mating endpoints
* `mated_with` relationships without requiring a new canonical Connector, DriverSocket, MatingInterface, or DriverModule entity for the cases tested so far

These conclusions remain subject to concrete evidence from additional hardware cases.

---

# 8. Current routing direction

Routing is an implementation subsystem over canonical connection semantics.

An important working distinction is:

```text
Route topology
    = corridor/side choices, bend sequence, structural organization

Route geometry
    = exact coordinates, segment positions, lengths, and spacing
```

The routing system should preserve stable route structure when practical while allowing geometry to change.

Preferred visual spacing and hard legality constraints should remain conceptually distinct.

Routing behavior should not redefine canonical machine connectivity.

---

# 9. Visual editor direction

The visual editor is an authoring and inspection environment over the canonical model.

Visual state may include:

* canvas position
* size
* selection
* zoom
* pan
* routing geometry
* grouping
* layers and filters
* semantic zoom
* presentation details

These are not substitutes for canonical machine meaning.

The editor should allow different levels of detail without creating multiple semantic representations of the same machine.

---

# 10. Firmware direction

Firmware is an implementation target rather than the definition of the machine.

The long-term system should support semantic translation between the machine model and multiple firmware ecosystems, including examples such as:

* Klipper
* RepRapFirmware
* Marlin
* GRBL and related machine-control systems where appropriate

Translation should operate on machine concepts rather than textual substitution between configuration files.

---

# 11. Documentation and provenance

Hardware facts should be traceable to appropriate sources.

Useful source categories include:

* manufacturer manuals
* pinout documentation
* electrical specifications
* CAD models
* photographs
* wiring diagrams
* firmware documentation
* configuration examples
* standards
* other authoritative technical sources

Known information should not be fabricated merely to make a model complete.

Unknown information should remain unknown or explicitly flagged.

---

# 12. Future machine scope

The architecture is intended to expand beyond the initial printer use cases.

Future stress-test machines and systems include:

* resin printers
* laser-equipped printers
* laser cutters
* LowRider machines
* CNC machines
* hybrid machines
* modular manufacturing systems
* unusual motion systems
* machines with multiple tools or processes

The architecture should be tested against these increasingly difficult cases rather than being optimized only for conventional Cartesian printers.

---

# 13. Future problems / deferred ideas

This section is a durable holding area for good ideas that are not yet part of the active implementation.

Ideas should not be lost merely because they are intentionally deferred.

Each future item should record:

```text
Idea
Why it may matter
Current status
Evidence currently available
What would justify revisiting it
```

Examples currently worth preserving include:

* richer reusable connector definitions
* deeper connector compatibility/intermateability modeling
* more detailed board and connector visualization
* wire/harness-level engineering
* richer machine geometry and mechanical representation
* machine/process/task modeling for hybrid manufacturing
* reusable assemblies and tool modules
* increasingly detailed diagnostics
* broader firmware import and reverse reconstruction
* additional manufacturing processes
* machine-level sequencing and shared-resource modeling

These remain future/candidate areas unless promoted by evidence and architecture review.

---

### Future-feature intake entries - 2026-10-11

- **Visual port-layout readability - user testing issue.** The user recalls that ports were clustered along one side of the application view, making labels and connections difficult to read while inspecting the Promega specimen. A previous #4 investigation may have considered spacing, ordering, filtering, or layers, but the cause and current implementation status remain unverified. Revisit during an appropriate GUI inspection milestone after the Promega wiring slice is testable. Success means the user can distinguish relevant ports, labels, and connections well enough to inspect the build. Reproduce the symptom before selecting a solution. Do not displace active Promega work without a priority decision.

- **Data-driven hardware catalog architecture - research proposal.** On 2026-10-11, #2 recommended a staged, declarative, revision-qualified hardware catalog with validation, explicit source evidence, uncertainty, and adapters into the existing canonical model. Candidate authoring formats include restricted YAML validated with JSON Schema Draft 2020-12, with JSON as a lower-dependency alternative. Prefer string-keyed objects and contact arrays with explicit numeric positions. This remains a research proposal, not a format decision or implementation authorization. Defer a schema/loader pilot and broad catalog migration until after the Promega milestone and a separate Planning decision. No ontology expansion is implied.

# 14. Modularity and code health

The project should favor cohesive modules with clear responsibilities.

A file approaching roughly 1,000 lines is a useful prompt to reevaluate its responsibilities.

This is not a hard maximum.

A larger file may remain appropriate when it represents one cohesive responsibility.

A smaller file may still deserve decomposition when it contains unrelated concerns.

Refactoring decisions should consider:

* responsibility boundaries
* dependency direction
* testability
* reuse
* readability
* coupling
* ownership by the relevant workstream

---

# 15. Development workflow

The repository uses one active `main` branch and one shared working checkout.

Specialized chats are workstreams, not competing branches.

Current workstream roles are:

```text
01 Planning / Architecture
02 Research / Architecture
03 Controller / Board
04 Routing / Diagnostics
05 Efficiency / Modularization
```

Chat-instance suffixes such as `3.1`, `3.2`, or `4.3` identify replacement chat instances for human organization. They are not architectural identifiers.

The repository, tests, and current `main` state are authoritative.

---

# 16. Long-term goal

The long-term goal is a general machine-engineering environment in which a real machine can be:

```text
described
→ inspected
→ documented
→ validated
→ wired
→ diagnosed
→ mapped to firmware
→ converted between firmware systems
→ modified
→ expanded
→ eventually designed
```

while maintaining one canonical semantic representation of the machine underneath the different views and outputs.

---

# 17. Planning rule

The Master Plan describes long-term direction and durable future ideas.

It should evolve deliberately.

It should not become a transcript.

It should not be rewritten merely because an implementation experiment produces a temporary idea.

The durable decision flow is:

```text
Idea
    ↓
Research / experiment
    ↓
Evidence
    ↓
Architecture review
    ↓
Current-state decision
    ↓
Implementation
```

Deferred ideas remain recorded rather than forgotten.

---

# 18. Relationship to other project documentation

```text
MASTER_PLAN.md
    = long-term direction and durable future ideas

PROJECT_CURRENT_STATE.md
    = current project-wide status, active direction, and open questions

01_PLANNING_ARCHITECTURE_WORKSTREAM_HANDOFF.md
    = Planning / Architecture continuity

02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md
    = Research continuity and source/evidence history

03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md
    = Controller / Board implementation continuity

04_ROUTING_STABILITY_WORKSTREAM_HANDOFF.md
    = Routing / Diagnostics implementation continuity

05_EFFICIENCY_MODULARIZATION_WORKSTREAM_HANDOFF.md
    = Code-health and modularity review continuity
```

No document should silently become a replacement for another document's role.

## Planning Decision — Promega Vertical-Slice Focus (2026-10-10)

**Decision:** Shift the immediate implementation emphasis toward proving the existing Machine Builder architecture against the standard M3D Promega, rather than expanding the ontology or beginning broad catalog work.

The objective is a credible machine specimen that can represent documented installed hardware, controller interfaces, component-owned and controller-owned physical endpoints, physical connections, functional relationships, version-qualified firmware assignments, and persistent visual associations without inventing unknown facts.

### Completed foundation

* The generic palette canonical-component checkpoint is committed as `8d496aa50a09f2319a665233354ede49c00160f6`.
* Physical connection metadata authoring is committed and published as `c445bef287d736afd20807f29d2506aab2434eaa`. The implementation captures wire color, harness ID, and notes on canonical `SemanticConnection.properties`, preserves visual-route separation, and passed the recorded acceptance review.
* Research has completed the bounded Promega inventory, component-side endpoint, harness, physical-inspection, functional-relationship, and firmware-resource investigations.
* The existing ontology remains adequate for the examined cases. No new ontology entity has been justified.

### Next integration direction

Planning will coordinate the next bounded implementation steps to establish a real Promega specimen. The order should follow demonstrated dependencies: establish reviewed hardware instantiation and board-interface coverage, author available physical connections without fabricating missing mappings, express documented functional relationships separately from wiring, and verify save/reopen persistence.

The Maestro J4 bed-heater interface correction was committed and published as e85a1e38af74622de3a1b62cf1641af4b707fd26 (Correct Maestro bed heater interface mapping). The correction maps the bed-heater interface through J4 contacts 3/4. Duet3D's published figure of up to 18 A subject to thermal testing is not a verified safe maximum for J4's contacts or the complete bed-output circuit.

### Preserve uncertainty and defer scope expansion

Keep the user's actual machine variant, firmware configuration, harness arrangement, and undocumented pin or connector assignments unverified until evidence establishes them. Keep the unresolved P4/P2, H2/H4, S8/S6, and P9/P11 mappings explicit.

Defer broad catalog importing, supplier integrations, a personal custom catalog, and further ontology expansion unless the real-machine workflow demonstrates a concrete need. Return to architecture only when a specific case shows that the existing semantics cannot represent the required relationship coherently.

## Planning Checkpoint — Promega Vertical Slice and Connector/Contact Validation (2026-10-10)

The vertical slice has progressed from general authoring infrastructure to a source-qualified Promega reference specimen and a small number of reference connection edges. It is not yet a complete or verified as-built machine model.

### Current sequencing decision

1. Review and run the bounded connector/contact validation only after #4 checks #2's reissued proposal against the actual code and current baseline.
2. Keep the SKR Mini E3 V3.0 EXP1 round-trip acceptance separate from the Octopus in-memory structural assessment and its legacy integer-key persistence limitation.
3. Preserve the Octopus `SLEEP` / `DRIVER2_SLP` versus TMC5160T Pro V1.0 `CLK` discrepancy. Do not infer contact-to-contact electrical compatibility from a group-level `mated_with` relationship.
4. Complete the Promega endpoint/connection graph from source-supported evidence, then address documented functional relationships and version-qualified firmware mappings as separate modeling tasks.
5. Reconcile the reference model against the user's actual machine only when physical variant, harness, active configuration, and wiring evidence are available.

The SKR position-8 firmware mapping is consistently reported as `PD6`; direct rendered-manufacturer-PDF verification is still open. Connector/contact representation remains conditionally accepted, and no ontology expansion is authorized by the current evidence.

## Planning Operating Decision - Workstream Autonomy and Durable Knowledge (2026-10-11)

Workstreams are expected to continue their standing missions, preserve findings in durable documentation, and report at meaningful milestones. `CHAT_WORKFLOW.md` Sections 36-37 define autonomous continuation and feature intake. `MASTER_PLAN.md` Section 13 is the single future-feature register.

The Promega reference-wiring vertical slice remains the immediate implementation priority. The port-layout issue is a deferred usability item. The data-driven catalog proposal is deferred until after the Promega milestone and a separate bounded Planning decision. Neither authorizes current scope expansion or ontology changes.

## Planning Checkpoint - Promega IR-Probe Fixture Publication (2026-10-11)

**Published checkpoint:** `9f3626b5b3117c2aef691eec4b04ae9b863485d0` - `Add reusable Promega IR-probe reference wiring fixture`.

The supplied publication output reports a full-suite result of **838 passed in 8.07 seconds**, followed by successful publication verification: local HEAD, fetched `origin/main`, and live remote `main` matched. The commit contains exactly `machine-structure-editor/src/machine_builder/promega_fixtures.py` and `machine-structure-editor/tests/test_promega_ir_probe_connections.py`.

This advances the Promega reference-wiring vertical slice. It does not, by itself, establish a complete machine connection graph, the wiring of the user's individual printer, or successful visual inspection of the application.

### Superseding sequencing decision

The October 10 connector/contact-spike sequencing is superseded as the immediate priority. Continue the Promega wiring path first:

1. Preserve the newly published fixture and test; use the actual committed implementation and assertions to establish exactly what is now covered.
2. Continue the smallest useful source-supported Promega wiring milestone within #4's authorization. Do not invent machine-side cable assignments where evidence remains incomplete.
3. Use #3's ongoing Promega harness and Maestro evidence research as supporting input, without requiring every research question to be resolved before independent implementation can proceed.
4. Keep the port-layout readability issue in Section 13 for a later GUI inspection milestone.
5. Defer the SKR hardware spike and broad catalog schema/loader implementation unless Planning explicitly reprioritizes them.

Reference documentation and firmware examples must remain distinct from verified as-built wiring and the active configuration on the user's printer.
