# Chat 02 — Research / Architecture Workstream Handoff

## Purpose

This is the living continuity document for Chat 02 — Research / Architecture.

Its purpose is to preserve research questions, evidence, standards, source material, conclusions, uncertainties, and research already completed so that a replacement Research chat does not unnecessarily repeat previous work.

The goal is evidence-driven guidance for Planning and Implementation.

---

# Recovery Instructions

A replacement Research chat should:

1. Read this handoff completely.
2. Read `MASTER_PLAN.md` and `PROJECT_CURRENT_STATE.md`.
3. Review the current repository when a research question concerns implementation behavior.
4. Treat authoritative external sources as evidence.
5. Preserve source provenance for important findings.
6. Distinguish documented facts from interpretation.
7. Report uncertainty rather than filling gaps with assumptions.
8. Re-check current sources when time-sensitive information may have changed.
9. Classify findings appropriately before recommending architectural changes.
10. Treat the local repository, current tests, and current handoffs as authoritative for implementation state.
11. Do not assume an unverified repository commit, file state, or test result from conversation history.

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

# Current Active Research Question

## BTT Octopus V1.1 ↔ TMC5160T Pro V1.0 Pin-6 Discrepancy

This is the current narrowly targeted Board research task.

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

# Current Research Queue

## Board

1. Resolve or further narrow the Octopus V1.1 ↔ TMC5160T Pro V1.0 contact-6 discrepancy using primary evidence.
2. Determine whether any concrete replaceable-driver/module case requires richer contact-level or reusable compatibility semantics.
3. Determine when connector compatibility becomes an actual canonical machine requirement.
4. Support Planning/Implementation with concrete evidence needed to instantiate the actual Promega accurately.

## Routing

1. Research only concrete questions that emerge around the boundary between topology selection, geometric repair, and preferred spacing.
2. Determine whether any routing behavior currently treated as a heuristic deserves durable architectural status.

## General Machine Model

1. How should Function, Capability, Process, Operation, Task, and sequencing relate in broader manufacturing systems?
2. What does a modular hybrid manufacturing machine require that conventional printer cases do not?
3. Stress-test the existing canonical model against broader hybrid-manufacturing architectures only when that work becomes useful to Planning.

These broader machine-model questions remain intentionally secondary to the immediate real-data implementation path.

---

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

Updated: 2026-10-08

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

Current immediate Board research:

```text
Octopus V1.1 ↔ TMC5160T Pro V1.0
contact-6 SLEEP vs CLK discrepancy
```

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

---

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

# Recovery Rule

When a future Chat 02 reaches the conversation limit:

```text
Read this handoff
    ↓
Read MASTER_PLAN.md
    ↓
Read PROJECT_CURRENT_STATE.md
    ↓
Review the Research source register / authoritative Research documents
    ↓
Verify the current repository state when implementation behavior matters
    ↓
Continue the current research queue
```

Do not redo completed research unless a new question requires it or the source has materially changed.

---

# Live-State Summary

As of 2026-10-08:

```text
Research / Architecture role
        =
evidence, standards, terminology,
manufacturer documentation, precedent,
and architecture validation

Broad connector terminology research
        =
substantially complete

Duet 2 Maestro V1.0 Board research
        =
COMPLETE

Real-data canonical/visual boundary validation
        =
REINFORCED

Routing architecture research
        =
stable; investigate only concrete new questions

PowerShell/parser research
        =
CLOSED

Current active research question
        =
Octopus V1.1 ↔ TMC5160T Pro V1.0
pin-6 SLEEP vs CLK discrepancy
```

The current Research objective is therefore **not broad ontology expansion**.

The objective is to resolve concrete evidence gaps that affect accurate representation of real machine hardware and to provide Planning with evidence-backed conclusions without inventing semantics.
