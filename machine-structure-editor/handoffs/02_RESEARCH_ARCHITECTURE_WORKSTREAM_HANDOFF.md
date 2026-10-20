# Chat 02 — Research / Architecture Workstream Handoff

<!-- BEGIN VERIFIED POST-PUBLICATION STATUS: MB-20261020-1622-02 -->
## Current verified Research checkpoint — 2026-10-20

- **Latest shared baseline:** `ae5a9a1672d151c37e392e9bff4f2421f0a465f2` — `Fix Octopus receiving-interface persistence`. Fresh preflight confirmed local HEAD, fetched `origin/main`, and live remote `main` match.
- **Latest earlier Research publication:** `29c2e54412c6621b112ccfee710e79e6fba46c91` — `Record integer-key persistence investigation findings`.
- **Board persistence follow-up:** #3 published the Octopus receiving-interface persistence fix in `ae5a9a1672d151c37e392e9bff4f2421f0a465f2`. Planning reports the 65-test focused suite passed; Research did not independently rerun it. The generic serializer and separate TMC5160T module map were not changed.
- **Separate unresolved hardware question:** Octopus V1.1 contact 6 versus TMC5160T Pro V1.0 J1-6 remains **UNRESOLVED**. Do not conflate it with the receiving-interface persistence fix or duplicate #3 investigation.
- **Research source finding:** `_encode()` rejects non-string dictionary keys; the earlier Octopus specification used integer contact-position keys. The Board fix is scoped to the Octopus receiving interface. Do not silently stringify keys or change the generic serializer.
- **Previous closeout:** `MB-20261020-1149-01` (`PUBLISHED — SLOT RELEASED`) was sent to Planning, as confirmed by the user.
- **Current publication grant:** `MB-20261020-1900-01` authorizes exactly these two paths at baseline `ae5a9a1672d151c37e392e9bff4f2421f0a465f2`:
  - `machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md`
  - `machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_REPLACEMENT_PROMPT.md`
- **Validation:** strict UTF-8 readback, `git diff --check`, exact staged path set, full staged diff review, staged/worktree blob equality, normal push, and post-push ref verification are required.
- **Local-state boundary:** the Standards Index is clean. Preserve all other workstream changes and untracked paths. Only the two grant-authorized files may enter this commit.
- **Next action:** finish staged review, commit with `Refresh Research recovery handoff and replacement prompt`, push normally, verify local/fetched/live remote refs, then send Planning a separate `PUBLISHED — SLOT RELEASED` closeout.

Older status text below this checkpoint is historical wherever it conflicts with these verified facts.
<!-- END VERIFIED POST-PUBLICATION STATUS: MB-20261020-1622-02 -->


## Purpose

This is the living continuity document for Chat 02 — Research / Architecture.

Its purpose is to preserve research questions, evidence, standards, source material, conclusions, uncertainties, and research already completed so that a replacement Research chat does not unnecessarily repeat previous work.

The goal is evidence-driven guidance for Planning and Implementation.

---

# Recovery Instructions

Follow the universal replacement-chat recovery procedure in `CHAT_WORKFLOW.md` §17. It defines the shared startup sequence; do not duplicate or redefine that sequence here.

Research-specific recovery requirements:

1. Read `machine-builder-research/START_HERE.md` on every Research / Architecture replacement. It is the authoritative Research navigation and recovery entry point.
2. Resume from the current Next Action and active Research question in this handoff. Use `START_HERE.md` to locate the subject-matter authorities relevant to that action.
3. When a research question depends on implementation behavior, verify the actual current checkout and relevant tests as required by §17; do not assume a remembered commit, file state, line number, or test result.
4. Preserve source provenance for important findings, including the source version, date, URL, relevant section/page, and what the source does and does not establish where available.
5. Distinguish documented facts, direct observations/measurements, inference, and interpretation. State limitations and preserve unresolved uncertainty rather than filling gaps with assumptions.
6. Re-check primary sources when information may have changed or the source revision matters.
7. Classify findings before recommending architectural implications. Report project-level implications to Planning rather than independently changing durable architecture.

---

# Current Role of Chat 02

Chat 02 investigates questions that arise from Planning and Implementation.

Primary responsibilities:

* standards research
* terminology research
* manufacturer documentation
* CAD/system conventions
* established engineering practices
* software architecture precedent
* implementation-pattern research
* comparison of existing approaches
* reporting evidence and limitations back to Chat 01

Chat 02 should not independently redefine durable project architecture.

Where research suggests a project-level architectural change, report the evidence and proposed implication to Planning rather than silently promoting the change.

---

# Research Reporting Classifications

Use:

```text
IMPLEMENTATION ONLY
```

for useful implementation knowledge that does not alter architecture.

```text
WATCH
```

for an important distinction or possibility not yet established as required.

```text
REINFORCE
```

for external evidence supporting an architecture already being used.

```text
NEW PRINCIPLE — candidate
```

for a potentially durable architectural principle that requires Planning review.

```text
RECONSIDER
```

when evidence indicates an existing architecture may be insufficient or contradictory.

---

# Source Preservation Rule

Important research must preserve enough information for a replacement Research chat to identify the original evidence.

For each important source, record as much of the following as available:

```text
Source title:

Organization / author:

Document or standard identifier:

Publication/version:

URL or repository location:

Date accessed:

Relevant section/page:

What it establishes:

What it does NOT establish:

How it affects Machine Builder:
```

Do not keep only a conclusion without the source that supports it.

Do not keep only a URL without recording why the source mattered.

Standards should include the standard number and relevant terminology/section where practical.

For manufacturer hardware research, distinguish among:

```text
documented schematic/connectivity
documented mechanical/interface information
documented firmware behavior
direct observation
measurement
inference
```

Do not promote an inference to a documented hardware fact.

---

# Connector / Interface Research

Research into connector terminology has established important conceptual distinctions around:

```text
Physical Connector

    ≠

Reusable Connector Definition

    ≠

Mating Interface

    ≠

Intermateability / compatibility

    ≠

Actual Mated Connector Pair
```

Manufacturer and engineering-system evidence also supports distinctions involving:

* housing/body
* contact/terminal
* mating interface
* termination interface
* keying/polarization
* retention
* mating parts
* reusable definitions versus installed instances

Current architectural conclusion:

These concepts should not automatically become individual canonical Machine Builder entities.

The current model should introduce additional entities only when an actual machine case demonstrates the need.

Broad connector/mating terminology research is therefore considered substantially complete for the current V0.2 architecture.

Repeat this research only when a materially different hardware case demonstrates a new requirement.

---

# Routing Research

Research has identified established precedent for separating routing concerns such as:

```text
route/topology generation

        ↓

route geometry

        ↓

spacing/nudging/adjustment

        ↓

final visual route
```

Research has also identified precedent for:

* preserving existing topology during incremental editing
* minimizing unnecessary rerouting
* edge/segment separation preferences
* orthogonal nudging
* movable and protected route segments
* bend penalties
* incremental topology preservation

Important examples investigated include:

* yFiles orthogonal routing and minimum-edge-distance concepts
* libavoid routing/nudging concepts
* Microsoft Automatic Graph Layout / MSAGL routing and nudging
* academic work on orthogonal graph drawing and segment separation

The architectural interpretation remains cautious:

```text
preferred spacing

    ≠

hard geometric legality

topology preservation

    ≠

a particular router implementation
```

Routing research should inform implementation without automatically dictating architecture.

Current Routing architectural boundary remains:

```text
canonical connection semantics
        ↓
routing relevance / endpoint information
        ↓
pathfinding / geometric legality
        ↓
visual route geometry
        ↓
stability / preservation / repair
```

No additional Research-side routing principle is currently required unless a concrete implementation question arises.

---

# Board / Connector Research

Current Board research has examined real hardware interface representation and connector terminology.

Important evidence includes:

* IEC connector terminology and intermateability concepts
* Molex connector/interface documentation
* TE Connectivity connector and mating terminology
* Autodesk Inventor connector/mating/interface concepts
* manufacturer documentation for actual controller boards and driver modules

Current Board research supports the following working model:

```text
Hardware Definition

        ↓

installed hardware instance

        ↓

physical interface SemanticPort(s)

        ↓

relationships / physical connections
```

Current implementation evidence from the Duet 2 Maestro and BTT Octopus/TMC5160T cases does not yet require a canonical:

```text
Connector
MatingInterface
Contact
DriverSocket
DriverModule
```

entity.

These remain candidates only if a concrete hardware case demonstrates that the existing model cannot express the required semantics accurately.

---

# Current Research Findings of Interest

## Controller Resource vs Physical Interface

A Controller Resource is not automatically a physical connector or pin.

It may be exposed through one or more physical access points.

Research should continue to distinguish:

```text
resource identity

physical interface identity

contact/pin identity

electrical connection

assignment
```

A physical connector can expose one or more controller resources.

A resource may also be exposed through multiple physical interfaces.

Therefore:

```text
connector = port = pin = resource
```

must not be assumed.

---

## Mating

A physical mating relationship can be conceptually distinct from resource exposure and resource assignment.

Current implementation experiments use:

```text
SemanticPort
    --mated_with-->
SemanticPort
```

without requiring a dedicated mating entity.

The research question remains whether future hardware cases eventually require richer reusable interface/compatibility concepts.

At present, no such requirement has been established.

---

## Hardware Definition vs Installed Controller

The current Board architecture uses the distinction:

```text
reusable HardwareDefinition
        ↓
installed Controller
```

The installed `Controller` may reference its reusable `HardwareDefinition`.

This represents an instance/association relationship, not inheritance.

No separate ontology entity is currently required solely to express that relationship.

---

# Real-Data Integration Validation Checkpoint

Updated: 2026-10-05

Chat 03 — Controller / Board and Chat 04 — Routing / Diagnostics independently reviewed the first real-data integration case using the Duet 2 Maestro.

This checkpoint validates the existing architectural boundary against a real controller rather than synthetic-only data.

## Board findings

The current `Duet 2 Maestro v1.0` `HardwareDefinition` is a legitimate reusable canonical hardware definition with manufacturer provenance.

Existing evidence includes sources such as:

* Duet3D hardware-design repository
* `Headers.sch`
* Duet wiring documentation
* product documentation
* Duet motor/heater technical documentation

The current hardware definition contains 17 physical connector/interface specifications, covering:

* 6 motor interfaces: X, Y, Z-A, Z-B, E0, E1
* 5 endstop interfaces: X, Y, Z, E0, E1
* 6 heater interfaces: three Molex and three screw-terminal interfaces

The existing representation already demonstrates:

```text
physical interface
        ↓
SemanticPort
        ↓
Controller Resource
```

rather than treating a connector as a controller resource.

The physical Maestro inspection also established a broader interface inventory, including:

```text
USB
Ethernet
PanelDue
PanelDue_SD
12864 EXP1
12864 EXP2
Probe
E2
E3
C_GND
J21
TEMP_OB
ERASE
Always On Fan
Fan1
A VIN
E 5V EN
5V PS
```

These do not automatically become installed `SemanticPort`s.

Each interface should be classified according to whether it represents:

* a meaningful semantic connection endpoint
* an expansion interface
* a communication/display connection
* a service/configuration interface
* a test/ATE point

The Maestro provides a strong real-world example of:

```text
controller resource
        ↓
exposed_through
        ↓
multiple physical SemanticPorts
```

This reinforces the rule that:

```text
connector = port = pin = resource
```

must not be assumed.

## E2/E3 expansion evidence

The Maestro's external driver interfaces and corresponding expansion module provide an additional useful test case:

```text
physical header
    ≠
driver module
    ≠
controller resource
    ≠
machine axis
```

The external module's drives can be exposed by firmware as additional drives and can be remapped to machine functions.

This reinforces the architectural rule that machine configuration must not be baked into the reusable Maestro hardware definition.

## Board ownership and implementation boundary

The Board implementation constructs canonical objects directly, including:

* `HardwareDefinition`
* `Controller`
* `MachineComponent`
* `ControllerResource`
* `SemanticPort`
* `SemanticRelationship`
* `Provenance`
* `CanonicalMachineModel`

No parallel Board-specific semantic model was identified.

No Board → Routing implementation dependency or adapter was identified.

No new canonical `Connector`, `MatingInterface`, `Contact`, `DriverSocket`, or Board-specific semantic entity is currently justified.

One concrete ownership/governance issue remains:

`hardware_catalog.py` currently contains both generic reusable catalog definitions and Board-specific definitions such as Maestro and TMC5160T data.

This is a shared-file ownership question for Planning; it is not currently a reason to refactor the model.

---

# Maestro Completion Checkpoint

Updated: 2026-10-08

Chat 03 — Controller / Board reports that the Duet 2 Maestro V1.0 Board coverage is complete.

The Maestro was intentionally completed as a real reusable hardware specimen because the physical M3D Promega uses this controller and therefore provides the strongest first end-to-end validation case.

The completed Maestro work establishes a sufficiently complete reusable Board specimen without requiring a new semantic layer.

Important retained evidence boundaries include the distinction between:

```text
verified board/interface facts
        ≠
firmware-specific configuration
        ≠
actual installed Promega machine usage
```

The completed Maestro specimen should therefore be treated as the Board-side hardware foundation for later machine instantiation and firmware mapping.

The next architectural question is no longer:

```text
What additional Maestro catalog entities are missing?
```

It is:

```text
What is the smallest set of non-Board
MachineComponent, SemanticPort, Assignment,
Connection, and validation support required
to instantiate the actual Promega accurately?
```

That question belongs primarily to Planning/Implementation, with Research support only for concrete evidence gaps.

---

# First Real Visual Integration Seam

The canonical model already provides the identity relationships needed for real integration:

```text
HardwareDefinition

        ↓

Controller / MachineComponent

        ↓

SemanticPort

        ↓

SemanticConnection
```

`SemanticPort` already supports both component-owned and controller-owned ports and carries information such as:

* `component_id`
* `controller_id`
* `connector_id`
* `pin_id`
* `purpose`
* `direction`
* properties
* provenance

The existing visual architecture already projects component-owned ports through the existing mechanism:

```text
MachineComponent
        ↓
project_component_ports()
        ↓
VisualPort.semantic_reference
```

The corresponding controller-owned projection is the clearest current visual integration seam:

```text
Controller

    ↓

controller.port_ids

    ↓

canonical SemanticPort

    ↓

VisualPort.semantic_reference

    ↓

PortGraphicsItem

    ↓

connection editing

    ↓

canonical SemanticConnection

    ↓

existing Routing
```

This is a generic visual/editor integration need, not a Maestro-specific Routing requirement.

---

# Physical Geometry Versus Visual State

The real-data review clarified an important three-way distinction.

```text
Hardware Definition

    physical board dimensions
    documented board outline
    documented connector locations
    documented connector orientation

        ↓

Visual / document state

    node placement
    visual rotation
    zoom/detail level
    filters/layers
    selection/highlighting

        ↓

Routing

    wire paths
    endpoint escape geometry
    obstacle/pathfinding state
    route stability/continuity
```

The distinction is:

* documented physical characteristics of manufactured hardware belong with the reusable Hardware Definition when trustworthy evidence exists;
* where the user places or rotates the board in the editor belongs to visual/document state;
* connection-path geometry and routing behavior belong to Routing.

The Maestro data inspected during the real-data review did not establish a structured set of physical connector x/y positions and orientations sufficient to require a richer geometry model.

Therefore the first generic board visualizer may legitimately use:

```text
board rectangle + sorted/labeled ports
```

without inventing exact physical connector placement.

Later, documented geometry can enrich the same visual mechanism without creating a second semantic model.

---

# Detail Levels, Filters, and Layers

The real-data review reinforces the recovered editor design constraint:

> The editor uses one underlying machine/semantic + visual dataset. Basic/intermediate/extreme detail are presentation/detail modes over that same data. Exact information thresholds remain intentionally undecided. Filters and layers provide additional independent view-state controls. Changing zoom/detail must never create or mutate a second semantic model.

A reasonable eventual progression is:

## Basic

* board outline
* grouped/sorted interface labels

## Intermediate

* connector groups
* interface/resource/type information
* richer labels

## Extreme

* documented physical connector locations
* connector orientation
* individual contacts/pins where useful
* actual board image/asset
* precise target-port highlighting for troubleshooting

These are presentation modes over the same underlying canonical and visual data, not separate data models.

---

# Future Semantic Contracts

No new Protocol, adapter, or Board → Routing contract is currently justified.

Potential future read-only semantic queries may include:

* resolving a visual endpoint to its canonical `SemanticPort` and owner;
* semantic compatibility evaluation between two canonical interfaces;
* exposing canonical connection invariants required during connection authoring.

These should be introduced only when a concrete consumer need demonstrates that direct canonical-model access is no longer an appropriate boundary.

---

# Historical Research Assignment — Octopus Pin-6 Discrepancy

## BTT Octopus V1.1 ↔ TMC5160T Pro V1.0 Pin-6 Discrepancy

This was a prior narrowly targeted Board task. Planning accepted its related evidence checkpoint on 2026-10-09. The SLEEP-versus-CLK electrical explanation remains unresolved; reopen only under a new Planning assignment.

Question:

> Resolve or further narrow the BTT Octopus V1.1 ↔ TMC5160T Pro V1.0 pin-6 discrepancy.

Known facts:

* Octopus generic `MOTOR_DRIVER` receiving interface contact 6 is labelled `SLEEP`.
* TMC5160T Pro V1.0 J1-6 is labelled `CLK` / external clock input.
* TMC5160T is documented as usable with the Octopus family.
* The Octopus schematic shows the driver sleep/control net entering a driver jumper/configuration network.

The research task is to determine whether authoritative primary evidence can establish why the physically mating interfaces are usable despite the differing labels.

Primary evidence to investigate:

1. Exact Octopus V1.1 schematic connectivity around driver socket contact 6 and its jumper/configuration network.
2. Exact net naming and jumper positions for SPI versus UART/standalone or other intended driver configurations.
3. BTT Octopus manual/jumper documentation specifying what contact 6 becomes electrically in the intended TMC5160 configuration.
4. TMC5160/TMC5160T primary documentation explaining the required state or permissible use of `CLK` when an external clock is not used.
5. BTT TMC5160T Pro schematic/BOM/revision evidence confirming that J1-6 is genuinely `CLK` and identifying any relevant onboard circuitry.
6. Official BTT example/configuration evidence showing TMC5160T installed on Octopus V1.1.

Critical research rules:

```text
Do not infer CLK = SLEEP.

Do not treat "known to work" as physical/electrical proof.

Do not substitute a generic internet pinout for BTT primary evidence.

Distinguish:

physical contact identity
    ≠
electrical net identity
    ≠
configured electrical state
```

Required result format:

```text
RESEARCH FINDING

Question:

...

Primary sources consulted:

...

Verified Octopus contact-6 path:

...

Verified TMC5160T J1-6 path:

...

Documented explanation:

...

or:

Primary-source explanation remains unresolved.

Remaining uncertainty:

...

Semantic conclusion / Machine Builder impact:

...
```

No repository changes are authorized merely to perform this research.

If primary evidence cannot establish the electrical explanation, retain the discrepancy as unresolved rather than manufacturing a compatibility explanation.

---

# Research That Should Not Be Repeated Without a New Question

Do not repeat broad connector/mating terminology research merely because a new Board chat starts.

The following questions have already received substantial investigation:

* connector versus mating interface terminology
* reusable connector definition versus physical connector
* intermateability concept
* housing/contact distinctions
* general orthogonal-routing topology versus geometry distinctions
* established routing nudging/separation concepts
* general canonical-vs-visual boundary
* general controller-resource-vs-physical-port distinction

Repeat research only when a new implementation case asks a materially different question or the relevant standard/documentation has changed.

---

# Research Queue — Future Questions Only

The entries below are possible future questions, not active authorization. As of 2026-10-09, await a new Planning assignment before resuming any queue item.


## Board

1. Octopus V1.1 ↔ TMC5160T Pro V1.0 contact-6 discrepancy: retained as unresolved after Planning accepted the evidence checkpoint; reopen only if Planning assigns renewed research.
2. Determine whether any concrete replaceable-driver/module case requires richer contact-level or reusable compatibility semantics.
3. Determine when connector compatibility becomes an actual canonical machine requirement.
4. Promega: the six bounded integration-research deliverables are accepted and complete; supply further evidence only for concrete gaps identified during Planning-coordinated implementation.

## Routing

1. Research only concrete questions that emerge around the boundary between topology selection, geometric repair, and preferred spacing.
2. Determine whether any routing behavior currently treated as a heuristic deserves durable architectural status.

## General Machine Model

1. How should Function, Capability, Process, Operation, Task, and sequencing relate in broader manufacturing systems?
2. What does a modular hybrid manufacturing machine require that conventional printer cases do not?
3. Stress-test the existing canonical model against broader hybrid-manufacturing architectures only when that work becomes useful to Planning.

These broader machine-model questions remain intentionally secondary to the immediate real-data implementation path.

---

## CAD / Geometry

### Accepted future CAD candidate: SolidCraft (2026-10-17)

Planning accepted SolidCraft via `MB-20261017-1121-01` as an optional future CAD geometry-authoring/import candidate, not a V0.2 requirement or project dependency. SolidCraft owns the CAD document and parametric geometry; Machine Builder's canonical model remains authoritative for installed component identity/role, HardwareDefinition, SemanticPort/SemanticConnection, provenance, and firmware requirements/mapping. CAD geometry or a successful STEP import must not be treated as evidence of electrical connectivity, physical wiring, or firmware correctness. Future evaluation gates: (1) repeatable bracket/enclosure STEP round-trip and component placement; (2) verify units, coordinate frame, orientation, geometry fidelity, component association, and traceable source/revision metadata; (3) evaluate CLI/JSON/MCP only after the manual boundary proves useful and repeatable. Planning owns later roadmap placement and evaluation authorization; no immediate action is assigned.

# Research-to-Planning Protocol

When reporting a research result to Chat 01, use:

```text
RESEARCH FINDING

Question:

...

Sources:

...

Documented evidence:

...

Interpretation:

...

What the evidence does NOT establish:

...

Classification:

IMPLEMENTATION ONLY / WATCH / REINFORCE /
NEW PRINCIPLE — candidate / RECONSIDER

Implication for Machine Builder:

...

Recommended next research or implementation question:

...
```

This keeps evidence separate from conclusion.

For project-level state changes, use:

```text
PROJECT CURRENT STATE UPDATE REQUEST

Why:

...

Proposed location:

...

Proposed content:

...

Source:

...
```

Planning / Architecture decides whether to incorporate it.

---

# Current State

Updated: 2026-10-18

Research role:

Evidence and external precedent for Planning and Implementation.

Current major research themes:

* real hardware / Board representation
* connector and interface semantics
* mating relationships
* replaceable driver/module compatibility
* orthogonal routing architecture
* modular machine/process architecture
* real-data validation of the canonical hardware/visual boundary

Current Board state:

```text
Duet 2 Maestro V1.0

COMPLETE
```

Most recent Board checkpoint (accepted; electrical discrepancy retained as unresolved history):

```text
Octopus V1.1 ↔ TMC5160T Pro V1.0
Planning accepted the evidence checkpoint on 2026-10-09.
The contact-6 SLEEP-versus-CLK electrical explanation remains unresolved.
```

Current Promega integration status:

Planning accepted all six bounded Promega integration research deliverables: Installed-Hardware Inventory; Component-Side Endpoint Evidence Matrix; Compound Extruder Harness Mapping Matrix; Extruder-Harness Physical-Inspection Checklist; Functional-Relationship Evidence Matrix; and Firmware Resource-Binding Matrix.

Keep documented physical components, functional relationships, versioned firmware configuration, and verified physical connections distinct. Evidence in one category does not by itself establish facts in another.

The official Promega v1.0.1 Compound configuration is version-qualified reference evidence only. The user's active firmware configuration and physical machine variant remain unverified.

Unresolved mappings and discrepancies:
* P4/P2 to physical E0/E1 drive mapping.
* Compound heater H2/H4 and PT1000 S8/S6 harness mapping.
* Printer-specific P9/P11 fan mapping.
* Cold-section fan logical-output assignment versus the documented Always On connection.
* Legacy M307 settings versus current Promega documentation's M301 settings.

Current architecture disposition:

```text
No new canonical hardware entity is currently justified.

Research should be evidence-driven and case-driven.

Maestro is complete enough to serve as the first real
hardware specimen for canonical-model and visual integration.

The next major implementation question is accurate
instantiation of the actual Promega machine.
```

Current documentation priority:

Preserve source provenance and research conclusions so that replacement chats do not have to reconstruct the research history from conversation memory.

Next Action:

**Bounded SKR Mini E3 V3.0 EXP1 review — ACCEPTABLE (2026-10-17).** Research reviewed #4's implementation and validation evidence under proposal `MB-20261015-1154-01`. Acceptance was sent to Planning (`MB-20261017-0009-01`) and Routing (`MB-20261017-0009-02`). This closes only the bounded fixture/test evidence gap, not general connector/contact validation or physical wiring.

**Validation evidence and attribution.** #4 reported 6 dedicated SKR tests passing in 0.14 s, 96 focused regression tests passing in 4.17 s, 853 full-suite tests passing in 36.85 s, and `git diff --check` passing at its earlier checkpoint. Research reviewed the supplied results and did not independently rerun those tests. This documentation pass runs no pytest, firmware-source/hash, external-source, or hardware tests.

**Publication preflight (2026-10-18).** Before staging, branch `main`, local `HEAD`, fetched `origin/main`, and live remote `main` matched at `0700c3f61bb47d186756b704f89b80ed280c8915`. This is the pre-publication baseline; use Git to establish the current repository state.

**Intended publication paths (only).**
- `machine-builder-research/standards/STANDARDS_INDEX.md`
- `machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md`

**Publication result (2026-10-18).** The authorized two-file source-recheck checkpoint was published as `bd5afc14d818264216796bee7d98640422211851` (`Record cooling-loop source recheck findings`). Post-push verification showed local `HEAD`, fetched `origin/main`, and live remote `main` matched at that commit. The archive follow-up is separate local research and has no publication slot.

**Unresolved evidence and limits.** EXP1 position 8 -> `PD6` is source-supported, but physical orientation, PCB pad/net identity, mating-face/cavity mapping, continuity, and as-built wiring remain unverified. The local Marlin snapshot's upstream origin remains unknown. Conditional peripheral-macro interpretation is not a universal mapping. The Octopus Driver 2 contact-6 `SLEEP` / `DRIVER2_SLP` versus TMC5160T Pro J1 contact-6 `CLK` discrepancy remains unresolved. Integer-key persistence is source-confirmed at the mechanism level but remains an untested runtime hypothesis: `persistence.py` rejects non-string dictionary keys, while the Octopus receiving-interface specification uses integer contact-position keys; no runtime test was run, the exact first nested map was not confirmed, and a complete save/reopen failure was not demonstrated. This remains separate from group-level `mated_with` limitations. Do not normalize uncertain facts or alter catalog data merely to force a passing test.

**Evidence record and coordination trail.** The ten-position source inventory, source locators, mapping-layer reconciliation, and bounded test outcome are retained in the single Standards Index entry above, not duplicated in a second appendix here. Message trail: proposal `MB-20261015-1154-01`; Planning disposition and authorization `MB-20261015-2142-01` / `MB-20261015-2142-02`; implementation request `MB-20261016-0024-01`; source-inventory/recovery direction `MB-20261016-0025-01`; source-locator note `MB-20261016-1753-01`; Research source inventory `MB-20261016-1755-01`; mapping-layer direction `MB-20261016-1806-01`; documentation-refresh direction `MB-20261016-1808-01`; #4 source/test report `MB-20261016-1833-01`; #4 implementation evidence `MB-20261016-2125-01`; Research acceptance messages `MB-20261017-0009-01` and `MB-20261017-0009-02`. The stated follow-up relationship between the 17:53 and 17:55 IDs conflicts with their timestamp order. Planning has not reconciled that discrepancy; do not infer chronology from those timestamps alone.

**General Research priority.** Promega source-supported wiring remains the general project priority. The separate cooling investigation remains open and is not a prerequisite for Promega wiring.

**Accepted future CAD candidate.** Planning accepted SolidCraft via `MB-20261017-1121-01` as an optional future CAD candidate, not a V0.2 requirement or dependency. SolidCraft owns CAD documents and parametric geometry; Machine Builder remains authoritative for canonical component identity/role, HardwareDefinition, SemanticPort/SemanticConnection, provenance, and firmware requirements/mapping. Geometry or STEP import does not prove electrical connectivity or firmware correctness. Evaluation gates and deferred status are recorded in the existing **CAD / Geometry** section above. No evaluation is authorized now.

**Validation performed in this correction.** The saved files and staged blobs were checked directly as UTF-8. The suspected display-corruption marker was absent before editing, so encoding conversion was not needed. The established baseline and cooling evidence remain in their existing sections. Target-only working-tree and staged `git diff --check` are run after this correction.

**Historical result (updated 2026-10-19).** Planning accepted the DYZE historical wording conflict and current prototype-feature status as ANSWERED under `MB-20261018-2038-01`. The earlier Research publication completed as `e210c92af2edac5b8a5e92df122225622ff4f007` (`Reconcile DYZE cooling source evidence`). The branch subsequently advanced through the screenshot update and #3 Board evidence work; the current verified shared baseline is `9b3013d1cbecebbc32e6e17909a8ea09885a4833` (`Document revision-pinned TMC5160T routing evidence`). The prior publication grant is consumed; the active Research publication grant and next action are recorded in the Live-State Summary below.

# Documentation Reconciliation Checkpoint

Updated: 2026-10-04

Planning established the project documentation authority model:

> **One primary question → one authoritative document.**

Research-side documentation reconciliation was completed against that model without modifying root Planning-owned documents.

Research authority state:

* `machine-builder-research/START_HERE.md` — authoritative Research navigation/recovery entry point.
* `machine-builder-research/architecture/ARCHITECTURE_OVERVIEW.md` — authoritative settled architecture baseline.
* `machine-builder-research/ontology/ONTOLOGY_CURRENT.md` — authoritative current canonical ontology.
* `machine-builder-research/ontology/TERMINOLOGY_BASELINE.md` — authoritative terminology baseline.
* `machine-builder-research/decisions/DECISION_LOG.md` — authoritative accepted-decision history.
* `machine-builder-research/questions/OPEN_QUESTIONS.md` — authoritative unresolved-question register.
* `machine-builder-research/checkpoints/V0.2_RESEARCH_CHECKPOINT.md` — current Research / Architecture checkpoint.
* `machine-builder-research/PROJECT_CONTEXT.md` — current supporting/background context, not authority for project state, architecture, ontology, or terminology.
* `machine-builder-research/RESEARCH_ROADMAP.md` — current supporting Research roadmap.
* `machine-builder-research/architecture/DATA_FLOW.md` and `SYSTEM_BOUNDARIES.md` — supporting architecture references.
* `machine-builder-research/ontology/CONCEPT_MATRIX.md` and `RELATIONSHIP_MATRIX.md` — supporting ontology reference views.
* `machine-builder-research/future/DEFERRED_RESEARCH.md` — deferred-research record subordinate to the active Research queue.

Reconciliation performed:

* `START_HERE.md` reflects the current V0.2 editor role and points Research recovery to the live Research handoff.
* `PROJECT_CONTEXT.md` reflects the current five-workstream organization, established O0.1 state, and its supporting/background role.
* `RESEARCH_ROADMAP.md` reflects the active V0.2 implementation and the bidirectional canonical-model/editor boundary.
* Supporting architecture and ontology reference documents identify their authoritative parent documents.
* `DEFERRED_RESEARCH.md` was reviewed during the audit but was not modified in this reconciliation checkpoint.

No new canonical entity, ontology rule, or durable architecture principle was promoted by this documentation reconciliation.

No historical Research material was intentionally deleted.

Planning-sensitive future topics remain:

* Board interface compatibility
* Routing topology/geometry boundaries
* Function / Capability / Process / Operation / Task relationships
* broader hybrid-manufacturing stress cases

---

# Repository Encoding / Line-Ending Audit Checkpoint

Updated: 2026-10-05 18:17:02 -04:00

Chat 05 — Efficiency / Modularization / Audit completed a read-only repository encoding and line-ending audit following a real Unicode corruption incident during a PowerShell edit of `hardware_catalog.py`.

## Findings

The repository's stored/index representation is consistent.

The repository contains `.gitattributes` with `* text=auto`, and the applicable Git configuration has `core.autocrlf=true`.

The observed convention is:

```text
Git repository/index
    LF-normalized text

Windows working tree
    CRLF normally produced by Git
```

The widespread CRLF working-tree representation is therefore expected Windows Git checkout behavior, not evidence of repository-wide line-ending corruption.

The audit reported:

```text
870  index LF / worktree CRLF
3    index LF / worktree LF
6    index LF / worktree MIXED
13   binary/-text handling
5    no line endings
```

The six files with genuinely mixed working-tree line endings were:

```text
CHAT_WORKFLOW.md
machine-structure-editor/handoffs/01_PLANNING_ARCHITECTURE_WORKSTREAM_HANDOFF.md
machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md
machine-structure-editor/handoffs/05_EFFICIENCY_MODULARIZATION_WORKSTREAM_HANDOFF.md
machine-structure-editor/src/machine_builder/hardware_catalog.py
machine-structure-editor/tests/test_connection_authoring.py
```

The audit also found two UTF-8-with-BOM files:

```text
CODER_CHAT_WORKFLOW.md
docs/historical/routing/ROUTING_STABILITY_INVESTIGATION_HANDOFF_4.3.md
```

No invalid UTF-8 files were found among the audited text-like files.

## `hardware_catalog.py` incident

The current file contains valid UTF-8 and correct Unicode, including:

```text
40 × 40 × 10 mm
6200 ±10% RPM
20.4 × 15.3 × 23.2 mm
```

No current mojibake was found.

The earlier Unicode corruption was a real transient editing incident, but the current repository no longer contains that corrupted state.

## Repository editing standard

For new or deliberately rewritten text files, use UTF-8 without BOM unless an existing historical file has a documented reason to retain another encoding.

For small tracked-file edits:

1. Prefer a small `git apply` patch when practical.
2. When PowerShell string editing is appropriate, explicitly decode and encode UTF-8.
3. Do not rely on PowerShell's implicit/default text encoding for repository files.
4. Guard replacements so they fail when the expected source block is missing.
5. Also fail when a supposedly unique source block occurs more than once.
6. Preserve existing line endings rather than normalizing the entire file unnecessarily.
7. Run `git diff --check` after editing.
8. Inspect the relevant git diff.
9. Run focused tests before broader testing at the appropriate checkpoint.

Byte-based UTF-8 read/write remains appropriate when exact byte-level or BOM preservation is specifically required, but it is not the default mechanism for every ordinary replacement.

The important distinction is:

> **CRLF in the Windows working tree is acceptable. Accidental transcoding of UTF-8 source text is not.**

Uncontrolled PowerShell text round-trips that rely on implicit encoding should not be used for tracked repository edits.

## Cleanup assessment

A separate controlled cleanup checkpoint may eventually be warranted for:

* the six mixed working-tree files
* deliberate review of the two historical BOM files
* any future confirmed mojibake

No repository-wide mass conversion is warranted from this audit.

No cleanup or normalization was performed by Chat 05 during the audit.

## Research classification

Primary classification:

```text
REINFORCE
```

Secondary classification:

```text
IMPLEMENTATION ONLY
```

`WATCH` remains appropriate for the localized mixed-line-ending files and historical BOM cases until a deliberate cleanup decision is made.

## Workflow implication

This finding does not change the canonical machine architecture.

It reinforces the project-wide requirement that ordinary Machine Builder repository inspection, source mining, implementation, testing, and audit work use the normal repository tooling rather than Python/Jupyter/data-analysis workflows.

The authoritative project-wide tooling, timeline-integrity, and copy/paste command-formatting rules live in `CHAT_WORKFLOW.md`.

---

# PowerShell / Parser Safety Research Checkpoint

Updated: 2026-10-07

## Research conclusion

The Machine Builder PowerShell incident was a parse-time failure in an over-complex composed repository command.

The surviving cascade diagnostics do not establish the exact first malformed token, so no stronger certainty should be claimed.

The following technical conclusions are established:

* Multiline parenthesized PowerShell expressions are valid and must not be prohibited.
* Avoid unnecessary backtick line continuation.
* Use here-strings for substantial literal multiline text where appropriate, with exact delimiters.
* `System.Management.Automation.Language.Parser.ParseInput()` is an optional parse-only preflight for unusually complex PowerShell.
* The repository-safe workflow remains:

```text
bounded inspection
    ↓
validation
    ↓
smallest practical edit
    ↓
git diff --check
    ↓
diff inspection
    ↓
focused tests
    ↓
broader tests as appropriate
```

* Do not modify repository source merely to obtain diagnostic output when a non-mutating inspection, test, or other diagnostic path can provide the same evidence.

## Separate tooling incident

The `Analysis errored` / Python incident is a separate Machine Builder tooling violation.

It must not be conflated with the PowerShell parser failure.

The existing Machine Builder tooling rule already prohibits Python, Jupyter, pandas, notebooks, generated analysis workflows, temporary analysis scripts/artifacts, and data-analysis workflows for ordinary repository work.

## Workflow disposition

No additional `CHAT_WORKFLOW.md` change is justified by this research result.

Workstream #4's recorded PowerShell/parser research dependency is resolved.

No special Routing workflow change is required.

## External provenance

Microsoft Learn — `about_Parsing`:

```text
https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_parsing
```

Accessed: 2026-10-07

Establishes:

PowerShell parsing behavior, valid natural multiline syntax, and the fragility of backtick continuation.

Microsoft Learn — `about_Quoting_Rules`:

```text
https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules
```

Accessed: 2026-10-07

Establishes:

single-quoted strings and here-string syntax/behavior.

Microsoft Learn — `Parser.ParseInput`:

```text
https://learn.microsoft.com/en-us/dotnet/api/system.management.automation.language.parser.parseinput
```

Accessed: 2026-10-07

Establishes:

parse-only processing of PowerShell input and returned parser errors without executing the script.

Microsoft Learn — Windows PowerShell 5.1 `about_Character_Encoding`:

```text
https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding?view=powershell-5.1
```

Accessed: 2026-10-07

Establishes:

important encoding/default-behavior considerations for Windows PowerShell 5.1.

Machine Builder implication:

Use explicit encoding/preserve existing file encoding and line endings when modifying repository text files.

## Disposition

Closed.

No material change to the Research workstream's current architecture or research queue.

---

# Repository Change Rule

Chat 02 should not independently rewrite `PROJECT_CURRENT_STATE.md`.

When research reveals a project-level implication, report:

```text
PROJECT CURRENT STATE UPDATE REQUEST

Why:

...

Proposed location:

...

Proposed content:

...

Source:

...
```

Planning / Architecture decides whether to incorporate it.

If Chat 02 needs a repository file changed for research documentation:

```text
REPOSITORY CHANGE REQUIRED

File:

exact repository path

Action:

...

Location:

exact section / line range / anchor

Change:

complete paste-ready text
```

A research result does not itself authorize a repository edit.

---

# Surgical Edit Rules

When a surgical edit is necessary:

* identify the repository commit inspected;
* give exact line numbers;
* give an exact text/class/function anchor;
* describe the location in plain language;
* for multiple edits, give edits from highest line number to lowest when possible;
* explicitly warn when an earlier edit changes the location of a later edit;
* never rely on programmer shorthand that is not meaningful to a non-programmer user.

If the expected line or anchor cannot be found, stop and re-inspect the current file.

---

# Continuation Rule

Continue from the current Next Action in this handoff. Treat dated chronological checkpoints as historical evidence, not as replacements for current work state; consult them when the active question needs their original evidence, rationale, or chronology.
Do not redo completed research unless a new question requires it or the source has materially changed.

---

# Hardware Catalog Research Knowledge Checkpoint — 2026-10-11

## Durable research record

The detailed catalog/interchange proposal is recorded in `machine-builder-research/standards/STANDARDS_INDEX.md` under **Hardware Catalog and Interchange Formats — Research Proposal (2026-10-11)**. That section contains the format comparison, standards/reference leads, proposed record fields and directory layout, firmware adapter boundaries, candidate examples, gaps, staged adoption, and deferred decisions. This handoff records the decision-relevant summary rather than duplicating the full report.

## Recommendation and boundaries

Evaluate a declarative, versioned catalog with stable product/revision identity, claim-level evidence and uncertainty, structural validation, and separate version-aware adapters for firmware-native data. Keep reusable `HardwareDefinition` distinct from installed `MachineComponent`; keep physical ports/connections distinct from controller resources and firmware mappings. Represent contacts as records with numeric positions instead of integer dictionary keys, and prove persistence behavior through a bounded pilot.

Manufacturer specifications, drawings, firmware examples, and observations of the user's actual machine are different evidence classes. Ambiguous sources and absent facts must not become asserted as-built connections. This research does not authorize ontology expansion or implementation.

## Timing and authority

- The Promega wiring vertical slice remains the active priority. Catalog implementation is deferred until that milestone and a separate Planning decision.
- `MASTER_PLAN.md` Section 13 is the canonical register for future problems and deferred ideas.
- Catalog layout, schema fields, and format choices remain research recommendations, not approved requirements.
- Next research focus: a real liquid-cooled hotend/coolant-loop example, separating physical fluid topology from electrical wiring and firmware interpretation. ISO 1219-1/-2 and ISO 14617-1/-2 are initial leads whose scope must be confirmed.

## Historical repository checkpoint for the catalog documentation update

The original catalog documentation edit recorded pre-edit HEAD `7316c22ae09fed95aba3bbf568c1e6d3bdc25493`, checked at `2026-10-11 10:39:16 -04:00`. This is a historical checkpoint, not the current live repository state. The catalog research record and corresponding Research handoff checkpoint were subsequently published in commit `25d8268600c0979ecfccfccb8a1b0b04bcf89014` (`Record hardware catalog research and handoff checkpoint`). The live checkout was separately re-verified before this liquid-cooling documentation update.

# Live-State Summary

## Established research baseline

- **Broad connector terminology research:** substantially complete.
- **Duet 2 Maestro V1.0 board research:** complete as a Research workstream milestone; retain the existing source-specific evidence and Board workstream handoff as authorities for their respective details.
- **Real-data canonical/visual boundary validation:** reinforced.
- **Routing architecture research:** stable; investigate concrete new questions rather than reopening settled decisions without evidence.
- **PowerShell/parser research:** closed unless a new, concrete blocker appears.

## Current checkpoint

- The catalog/interchange proposal remains documented in `machine-builder-research/standards/STANDARDS_INDEX.md` as research, not implementation authorization. `MASTER_PLAN.md` Section 13 remains the canonical register for future problems and deferred ideas. The existing catalog research record was published in commit `25d8268600c0979ecfccfccb8a1b0b04bcf89014`; catalog implementation remains deferred unless Planning separately authorizes it.
- The bounded SKR Mini E3 V3.0 EXP1 review is ACCEPTABLE within the limited scope as of 2026-10-17. #4 reported 6 dedicated, 96 focused-regression, and 853 full-suite tests passing at its earlier checkpoint; Research reviewed the supplied evidence but did not rerun those tests.
- **Latest verified shared baseline (2026-10-20):** `ae5a9a1672d151c37e392e9bff4f2421f0a465f2` — `Fix Octopus receiving-interface persistence`.
- **Current local checkpoint (2026-10-20):** publication baseline `ae5a9a1672d151c37e392e9bff4f2421f0a465f2`; this two-file Research batch is authorized under `MB-20261020-1900-01` and awaits final staged review.
- **Local Research work:** the Standards Index is clean. This handoff and replacement prompt are the exact two files authorized for publication under `MB-20261020-1900-01`.
- **Authorization:** grant `MB-20261019-1819-01` is consumed. Current grant `MB-20261020-1900-01` authorizes only the two Research handoff files at baseline `ae5a9a1672d151c37e392e9bff4f2421f0a465f2`.
- **Shared-index preservation:** the slot preflight confirmed an empty index before staging. The index now contains only the two paths authorized by `MB-20261020-1900-01`; preserve all unrelated worktree changes.
- SolidCraft is an optional future geometry-authoring/import candidate (`MB-20261017-1121-01`), not a V0.2 requirement or dependency. Planning owns future roadmap placement and evaluation authorization.
- **Next action:** publish the two authorized Research files under `MB-20261020-1900-01` after final staged-diff review. Then verify refs and send a separate `PUBLISHED — SLOT RELEASED` closeout.

## Current Research focus
### Accepted integer-key persistence checkpoint (Planning acceptance: 2026-10-19)

Planning accepted the read-only Research finding under `MB-20261019-1547-01`, following `MB-20261019-1450-01`.

**Source-confirmed mechanism:** `machine-structure-editor/src/machine_builder/persistence.py` `_encode()` rejects non-string dictionary keys before JSON encoding. `serialize_editor_state()` invokes `_encode(state)`, and `save_editor_state()` serializes before creating or writing its temporary file.

**Source-confirmed data shape:** `BTT_OCTOPUS_MOTOR_DRIVER_RECEIVING_INTERFACE_SPEC["contacts"]` uses integer contact-position keys. The specification is embedded in `machine-structure-editor/src/machine_builder/controller_board_fixtures.py` by `add_octopus_tmc5160t_mating_experiment()`.

**Evidence boundary:** no runtime test was run; the exact first nested map encountered was not confirmed, and a complete Octopus save/reopen failure has not been demonstrated. Do not report the runtime hypothesis as reproduced.

**Preferred representation:** contact records carrying numeric `position` fields. Do not change the generic serializer or silently stringify keys.

**Disposition and owner:** #3 subsequently published the Octopus receiving-interface persistence fix in `ae5a9a1672d151c37e392e9bff4f2421f0a465f2`. Planning reports the focused 65-test suite passed; Research did not rerun it. The separate contact-6 discrepancy remains unresolved; do not duplicate #3 investigation.

**Current-source update (2026-10-18; reconciled with DYZE support email and historical capture).** DYZE Technical Support's full email supplied by the user confirms that the supplied 1/4-inch ID x 3/8-inch OD soft, high-temperature rubber tube must have a bend radius no smaller than 50 mm, measured to the tube OD as support specifies, in stationary and moving conditions. Support states the automatic kink/blockage detection and print-pause feature is unavailable in the current version; it was carried over from a prototype and removed because of false positives and inadequate consistency for a reliable safeguard. Support replied at 11:30 AM on October 13 and promised a documentation update; the current Liquid Cooling guide displays an October 13, 2026, 5:11:12 PM update timestamp. The inspected September 14, 2025 Wayback capture, whose own footer says it was last updated September 4, 2025, directly shows the old conflicting minimum/maximum bend-radius instructions and the earlier automatic-pause claim. The same-day sequence and matching content strongly support attributing the correction to the questions submitted on October 12, although the internal edit history is unavailable. The all-time Wayback query returned 21 rows after digest collapsing; a 2026 exact-date-window query returned no rows, one wildcard query returned HTTP 503, and five Common Crawl exact-URL attempts returned HTTP 504. Those service failures are not evidence of empty collections. Installed Cooling Unit revision, actual tubing/fittings, routing, wiring, and firmware configuration remain unverified.

### Standing publication and recovery rules (Planning directives, 2026-10-19)

- **Publish and yield (`MB-20261019-1749-01`):** when an explicit publication slot is active, publish a complete, validated, coherent batch within its exact authorized paths as soon as ready. Do not hold a slot for unrelated work. If no safe authorized batch is ready, do not stage or publish; report the blocker and yield. This standing convention does not create or extend a grant.
- **Recovery freshness (`MB-20261019-1752-01`):** refresh this detailed handoff and the canonical replacement prompt in place after material findings, test or audit results, blockers, ownership/dependency/readiness changes, recovery-relevant failures, publication changes, and yield decisions. The handoff retains detailed evidence and history; the prompt provides a concise, self-contained verified snapshot.
- **Preflight and preservation:** immediately before any Git write, verify branch, local HEAD, `origin/main`, live remote `main`, shared index, and worktree. Stage only paths in the active grant; inspect the full staged diff and run `git diff --cached --check`; commit and push normally; verify the resulting remote checkpoint. Never stage another workstream, disturb unrelated index entries, use broad staging/reset/discard/unstage operations, or force-push.
- **Current disposition:** the two-file recovery refresh is authorized under `MB-20261020-1900-01`; the earlier three-file grant is consumed. No Research implementation or additional investigation is authorized by this slot.
- **Publication action:** stage only the Research handoff and replacement prompt, inspect the complete staged diff, commit with the approved subject, push normally, verify refs, and send a separate closeout.

**Concrete next action (2026-10-20; grant `MB-20261020-1900-01`):** finish final staged review and publish only the two authorized files. After successful push verification, send a separate `PUBLISHED — SLOT RELEASED` closeout and refresh local recovery state as needed.


- **Completed liquid-cooling checkpoint (initial source check: 2026-10-11; current-source recheck: 2026-10-18):** DYZE DESIGN Typhoon LCX and Liquid Cooling source findings, ISO applicability and model-fit assessment remain recorded in `machine-builder-research/standards/STANDARDS_INDEX.md`. The earlier bend-radius conflict is a historical source observation; the current public guide explicitly states a 50 mm minimum. The V0.2 architecture assessment is cross-referenced in Section 14 of `machine-builder-research/checkpoints/V0.2_RESEARCH_CHECKPOINT.md`.
- **Model fit:** Existing records can represent much of the installed coolant-loop topology, but the inspected contracts/tests do not demonstrate a validated query contract for connection medium and directed fluid flow. Treat this as a contract/query limitation, not automatic authorization to add ontology entities.
- **Disposition (Planning acceptance `MB-20261018-2038-01`): ANSWERED.** The September 14, 2025 archived page verifies the historical bend-radius contradiction and prototype-era automatic-pause claim. DYZE support email dated October 13 confirms the 50 mm minimum for the supplied tubing and confirms the feature is absent from the current version. The same-day documentation correction is strongly attributable to the support questions, while the exact internal edit time remains unverified. Installed Cooling Unit revision, actual tubing/fittings, routing, wiring, and firmware are still machine-specific unknowns.
- **Planning decision received (2026-10-11):** Adopt the bounded shared documentation/encoding/display standard. The root `.editorconfig` scope and explicit deferrals are recorded in the checkpoint below; Planning retains ownership of the eventual `CHAT_WORKFLOW.md` edit.
- **Queued next Research evidence work:** No further archive probing is required for the answered questions. Continue only for a distinct unresolved question or new primary evidence. Preserve installed-machine unknowns and keep Research separate from Promega wiring and #4 visual work.
- **Queued Research follow-up:** Planning accepts the bounded Option B contract as proposed design/documentation only. Implementation, tests, production-validation claims, and ontology expansion remain deferred unless separately authorized.

# Shared Documentation, Encoding, and Display Standard Checkpoint -- 2026-10-11

## Planning decision and authorized scope

Planning adopted the core recommendations on 2026-10-11 with limited first-step enforcement.

- The authorized root `.editorconfig` contains `root = true` and `[*.md]` with only `indent_style = space` and `insert_final_newline = true`.
- Explicitly deferred: `end_of_line`, `trim_trailing_whitespace`, and `charset`; changes to `.gitattributes` or `core.autocrlf`; repository-wide line-ending normalization; and historical-file encoding conversions.
- Planning owns changes to `CHAT_WORKFLOW.md`. The concise proposed insertion is recorded in the standards index under this research proposal; Research has not edited the workflow.
- The joined-word examples were checked against the stored proposal section. Literal defects are corrected locally; appearances caused only by console wrapping or rendering are not treated as file defects.

## Validation and boundaries

- Preserve the existing line-ending and encoding of the two Research documents; the new root `.editorconfig` is UTF-8 without BOM and uses the current Windows working-tree newline style.
- Validate the exact three authorized paths with `git diff --check` and inspect the complete staged diff before publication.
- This is a documentation/configuration-only change. It does not authorize source, test, ontology, historical-file, or other-workstream edits.

## Next Research mission

**Planning decision received (2026-10-12):** Planning accepts the bounded Option B contract as a proposed conceptual/documentation design. The medium-scoped `fluid_roles` map remains a proposal, not a currently validated port contract. Physical connection endpoint ordering remains non-directional; the Cooling Unit/LCX loop is synthetic acceptance-fixture data. No implementation, test, production-validation, or ontology expansion authorization was granted.

**Cooling-loop official-source follow-up (2026-10-12):** At the source check on that date, the then-rendered DYZE DESIGN Liquid Cooling guide appeared to give opposing bend-radius instructions and did not identify how the reported kink/blockage print pause was detected or signaled to printer firmware. This is a historical observation, not a description of the live page rechecked on 2026-10-18; see the current-source update in the Standards Index. Public changelog PCN-00006 records the Typhoon-to-LCX/Air product transition, but the installed revision remains unknown. Current kit specifications are reference evidence only, not proof of the hardware installed on the Promega. The official DYZE contact form remains a route for clarification of the detector, electrical interface and firmware questions.

**Official drawing and support-path follow-up (2026-10-12):** DYZE's official CAD index links a Cooling Unit STEP asset dated 2022-05-16 and a one-sheet PDF assembly drawing dated 2025-09-09. The drawing shows input/output/fill G1/4 fittings, a two-position connector explicitly labelled power, and a low-water indication beside the level slot. It does not document a kink detector or a printer-facing pause signal. The revision relationship between those assets and the installed unit remains unverified. DYZE's official contact form is the identified route for requesting the missing radius, detector, electrical-interface, and firmware details.

**Tubing product listing cross-check (2026-10-12):** DYZE's tubing listing provides two size options, including the 1/4 inch ID x 3/8 inch OD size identified as included in the kit guide. The listing provides no bend-radius specification. Ask DYZE to confirm the actual supplied tubing part/size and the correct bend-radius requirement; the product page does not resolve the conflicting guide statements.

**Localized-guide and filament-monitor distinction (2026-10-12):** DYZE's French-language generic guide does not resolve the English kit guide's opposing 50 mm minimum and maximum; the English build-your-own section also says "Low bend radius to prevent kinking." Written clarification is still needed. DYZE's Orthus guide documents filament-motion monitoring and filament-fault pauses, not coolant-tube monitoring. It does not explain the Cooling Unit's stated kink/blockage pause.

**Generic mixed-brand loop feasibility (2026-10-12):** A loop assembled from different-brand computer-cooling parts may be feasible, but cannot be approved from brand or appearance alone. The new vendor-neutral checklist in the Standards Index covers heat load/radiator duty, pump curve versus system resistance, wetted-metal and coolant compatibility, tubing/fitting/seal ratings, electrical ratings and control, priming/leak testing, and moving-hose clearance. It distinguishes a serviceable custom loop from a sealed AIO and explicitly keeps DYZE product-specific numbers, its unresolved 50 mm radius instructions, and its undocumented coolant kink/pause path from becoming universal requirements. The unidentified spare parts remain unqualified until their materials, labels/specifications, and intended thermal duty can be checked.

**Historical next-action note (superseded after the full 2026-10-13 support email and Wayback inspection).** The September 14, 2025 capture verified the prior conflicting radius instructions and prototype-era automatic-pause claim. DYZE support confirmed the correct 50 mm minimum and that the feature was removed from the current version after false positives. The explicit documentation promise, same-day update timestamp, and matching corrected content strongly support attribution to the support questions; internal edit history is unavailable. Planning accepted the historical contradiction and current feature-status question as ANSWERED under `MB-20261018-2038-01`. No further archive probing is required for these findings.

## DYZE Liquid-Cooling Evidence Reconciliation — 2026-10-12

**Durable evidence record:** `machine-builder-research/standards/STANDARDS_INDEX.md`, section “DYZE Liquid-Cooling Evidence Reconciliation — 2026-10-12,” contains the direct source links and detailed evidence classifications.

### Findings to carry forward

- The current English DYZE cooling guide has contradictory bend-radius directions: one passage says 50 mm minimum; another says 50 mm maximum. A separate passage recommends a low bend radius to prevent kinking. The conflict remains unresolved.
- The currently identified tubing listing gives two sizes but does not establish the exact material or complete operating ratings of the tubing supplied with the relevant kit.
- Independent manufacturers use different bend-radius datums. Guidance for fixed/static bends does not establish suitability for repeated dynamic flexing or service life. Independent product ratings are not transferable to DYZE's tube.
- DYZE publicly states that kink/blockage detection pauses printing, but the reviewed public documentation does not verify the sensor/method, threshold, electrical output, controller connection, firmware/configuration, or fault/reset behavior.

### Interpretation and evidence boundaries

The **50 mm minimum remains an unconfirmed working hypothesis**, not an approved DYZE specification. Do not assume centerline or inside-surface measurement. Do not infer that missing interface documentation proves the sensor/protection mechanism does not exist. Likewise, do not equate the drawing's low-water-level indication with an electrical output or kink detector without evidence.

### User action and external dependency

**User action:** None currently required. The DYZE support request has already been submitted; no duplicate request is needed.

**External dependency:** DYZE's written response is needed to resolve the bend-radius contradiction and datum, identify the applicable tube construction and operating/motion limits, and explain the sensing and printer-pause implementation.

### Research next step

Continue only where there is a specific evidence target with material value, such as a newly located authoritative specification, an archived revision that directly resolves the wording, or DYZE's response. Avoid repeating broad searches that have not produced new evidence. This external dependency does not block independent Promega work or other already-authorized workstreams.

## Promega J28 Coordinate Identity Correction - 2026-10-12

The expected-connection inventory correction is recorded in `machine-builder-research/standards/STANDARDS_INDEX.md` under "Promega J28 Guide-View Position to PCB Pad Crosswalk - 2026-10-12".

The correct reference crosswalk is:

| Promega guide-view / legacy fixture position | Duet 2 Maestro V1.0 PCB pad | Function |
|---:|---:|---|
| 1 | 5 | `Z_PROBE_IN` - IR-01 / S10 |
| 2 | 4 | GND - IR-02 / P5 |
| 3 | 3 | `Z_PROBE_MOD` - crosswalk reference only |
| 4 | 2 | +3.3 V - IR-03 / S9 |
| 5 | 1 | +5 V - crosswalk reference only |

**Correction:** The earlier inventory's phrase "PCB contact identity 1/2/4" was incorrect terminology for guide-view/fixture positions 1/2/4. The corresponding PCB pads are 5/4/2.

**Evidence:** Board workstream checkpoint `12fc3dc0b4522a5efee03f68baf931f47a3c6d8f`; pinned Duet 2 Maestro V1.0 PCB source commit `56958640c73c7febf3bce6e1eefbbdffd5a2db1b`; Promega Duet Maestro Wiring guide https://promega.printm3d.com/documentation/electronics/duet-maestro-wiring; Routing reference slice `ec5c7381fe5624e94bb22c81740153ce260ab298`.

Guide-view position, PCB pad, and physical cable cavity/mating orientation are distinct identities. The correction does not establish installed cable wiring or continuity. The three reference IR-probe relationships remain unchanged, and the P4/P2, H2/H4, S8/S6, and P9/P11 mapping uncertainties remain open.
