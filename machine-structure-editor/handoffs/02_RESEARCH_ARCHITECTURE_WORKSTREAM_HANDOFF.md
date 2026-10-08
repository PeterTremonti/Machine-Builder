**# Chat 02 — Research / Architecture Workstream Handoff**

**## Purpose**

This is the living continuity document for Chat 02 — Research / Architecture.

Its purpose is to preserve research questions, evidence, standards, source material, conclusions, uncertainties, and research already completed so that a replacement Research chat does not unnecessarily repeat previous work.

The goal is evidence-driven guidance for Planning and Implementation.

**---**

**# Recovery Instructions**

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

**---**

**# Current Role of Chat 02**

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

**---**

**# Research Reporting Classifications**

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

**---**

**# Source Preservation Rule**

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

**---**

**# Connector / Interface Research**

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

**---**

**# Routing Research**

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

Routing research should inform the implementation without automatically dictating architecture.

**---**

**# Board / Connector Research**

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

Current implementation evidence from Maestro and Octopus does not yet require a canonical Connector or MatingInterface entity.

**---**

**# Current Research Findings of Interest**

**### Controller Resource vs Physical Interface**

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

**### Mating**

A physical mating relationship can be conceptually distinct from resource exposure and resource assignment.

Current implementation experiments use:

```text
SemanticPort

    --mated_with-->

SemanticPort
```

without requiring a dedicated mating entity.

The research question remains whether future hardware cases eventually require additional reusable interface/compatibility concepts.

**---**

**# Research That Should Not Be Repeated Without a New Question**

Do not repeat broad connector/mating terminology research merely because a new Board chat starts.

The following questions have already received substantial investigation:

* connector versus mating interface terminology

* reusable connector definition versus physical connector

* intermateability concept

* housing/contact distinctions

* general orthogonal-routing topology versus geometry distinctions

* established routing nudging/separation concepts

Repeat research only when a new implementation case asks a materially different question or the relevant standard/documentation has changed.

**---**

**# Research Queue**

Current useful questions include:

**### Board**

* Does the Octopus receiving driver socket and TMC5160T J1/J2 documentation introduce a requirement for richer contact-level reusable definitions?

* What do other replaceable-driver or pluggable-module systems require?

* When does connector compatibility become an actual canonical machine requirement?

**### Routing**

* What is the appropriate boundary between topology selection, geometric repair, and preferred spacing?

* Which routing behaviors deserve durable architecture versus implementation heuristics?

**### General Machine Model**

* How should Function, Capability, Process, Operation, Task, and sequencing relate in broader manufacturing systems?

* What does a modular hybrid manufacturing machine require that conventional printer cases do not?

**---**

**# Research-to-Planning Protocol**

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

**---**

**# Current State**

Updated:

2026-10-05

Research role:

evidence and external precedent for Planning and Implementation.

Current major research themes:

* connector/interface semantics

* board hardware representation

* mating relationships

* orthogonal routing architecture

* modular machine/process architecture

* real-data validation of the canonical hardware/visual boundary

Current documentation priority:

Preserve source provenance and research conclusions so that replacement chats do not have to reconstruct the research history from conversation memory.

**---**

**# Documentation Reconciliation Checkpoint**

Updated: 2026-10-04

Planning has established the project documentation authority model:

> **One primary question → one authoritative document.**

Research-side documentation reconciliation was completed against that model without modifying root Planning-owned documents.

Research authority state:

* machine-builder-research/START_HERE.md — authoritative Research navigation/recovery entry point.

* machine-builder-research/architecture/ARCHITECTURE_OVERVIEW.md — authoritative settled architecture baseline.

* machine-builder-research/ontology/ONTOLOGY_CURRENT.md — authoritative current canonical ontology.

* machine-builder-research/ontology/TERMINOLOGY_BASELINE.md — authoritative terminology baseline.

* machine-builder-research/decisions/DECISION_LOG.md — authoritative accepted-decision history.

* machine-builder-research/questions/OPEN_QUESTIONS.md — authoritative unresolved-question register.

* machine-builder-research/checkpoints/V0.2_RESEARCH_CHECKPOINT.md — current Research / Architecture checkpoint.

* machine-builder-research/PROJECT_CONTEXT.md — current supporting/background context, not authority for project state, architecture, ontology, or terminology.

* machine-builder-research/RESEARCH_ROADMAP.md — current supporting Research roadmap.

* machine-builder-research/architecture/DATA_FLOW.md and SYSTEM_BOUNDARIES.md — supporting architecture references.

* machine-builder-research/ontology/CONCEPT_MATRIX.md and RELATIONSHIP_MATRIX.md — supporting ontology reference views.

* machine-builder-research/future/DEFERRED_RESEARCH.md — deferred-research record subordinate to the active Research queue.

Reconciliation performed:

* START_HERE.md now reflects the current V0.2 editor role and points Research recovery to the live Research handoff.

* PROJECT_CONTEXT.md now reflects the current five-workstream organization, established O0.1 state, and its supporting/background role.

* RESEARCH_ROADMAP.md now reflects the active V0.2 implementation and the bidirectional canonical-model/editor boundary.

* Supporting architecture and ontology reference documents now identify their authoritative parent documents.

* DEFERRED_RESEARCH.md was reviewed during the audit but was not modified in this reconciliation checkpoint.

No new canonical entity, ontology rule, or durable architecture principle was promoted by this documentation reconciliation.

No historical Research material was intentionally deleted.

Planning-sensitive future topics remain unchanged: Board interface compatibility, Routing topology/geometry boundaries, Function / Capability / Process / Operation / Task relationships, and broader hybrid-manufacturing stress cases.

**---**

# Real-Data Integration Validation Checkpoint

Updated: 2026-10-05

Chat 03 — Controller / Board and Chat 04 — Routing / Diagnostics have now independently reviewed the first real-data integration case using the Duet 2 Maestro.

This checkpoint validates the existing architectural boundary against a real controller rather than synthetic-only data.

## Board findings

The current `Duet 2 Maestro v1.0` `HardwareDefinition` is a legitimate reusable canonical hardware definition with manufacturer provenance.

Existing evidence includes sources such as:

* Duet3D hardware-design repository

* `Headers.sch`

* Duet wiring documentation

* product documentation

* Duet motor/heater technical documentation

The current hardware definition contains **17 physical connector/interface specifications**, covering:

* 6 motor interfaces: X, Y, Z-A, Z-B, E0, E1

* 5 endstop interfaces: X, Y, Z, E0, E1

* 6 heater interfaces: three Molex and three screw-terminal interfaces

The existing representation already demonstrates an important relationship:

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

These do not automatically become installed `SemanticPort`s. Each interface should be classified according to whether it represents a meaningful semantic connection endpoint, an expansion interface, communication/display connection, or service/configuration interface.

The Maestro also provides a strong real-world example of:

```text
controller resource
        ↓
exposed_through
        ↓
multiple physical SemanticPorts
```

Therefore:

```text
connector = port = pin = resource
```

must not be assumed.

### E2/E3 expansion evidence

The Maestro's external driver interfaces and the corresponding expansion module provide an additional useful test case:

```text
physical header
    ≠
driver module
    ≠
controller resource
    ≠
machine axis
```

The external module's drives can be exposed by the firmware as additional drives and can be remapped to machine functions.

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

## Routing findings

Chat 04 confirmed that the existing Routing implementation boundary remains healthy.

The production routing path remains conceptually:

```text
Visual/presentation geometry
        ↓
ConnectionGraphicsItem
        ↓
ConnectionRoutingEngine
        ↓
endpoint / relevance / pathfinder
```

Routing does not depend on Board/controller implementation internals, and Board/controller code does not depend directly on Routing internals.

The current synthetic/example Routing work is therefore not considered defective and does not need to be reworked solely because real Board data is being introduced.

## First real visual integration seam

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

The current visual architecture already projects component-owned ports through the existing mechanism:

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

## Physical geometry versus visual state

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

* **documented physical characteristics of the manufactured hardware** belong with the reusable Hardware Definition when trustworthy evidence exists;

* **where the user places or rotates the board in the editor** belongs to visual/document state;

* **connection-path geometry and routing behavior** belong to Routing.

The current Maestro data inspected does not yet establish structured physical connector x/y positions or orientations.

Therefore the first generic board visualizer may legitimately use a simple:

```text
board rectangle + sorted/labeled ports
```

representation without inventing exact physical connector placement.

Later, documented geometry can enrich the same visual mechanism without creating a second semantic model.

## Detail levels, filters, and layers

The real-data review also reinforces the recovered editor design constraint:

> The editor uses one underlying machine/semantic + visual dataset. Basic/intermediate/extreme detail are presentation/detail modes over that same data. Exact information thresholds remain intentionally undecided. Filters and layers provide additional independent view-state controls. Changing zoom/detail must never create or mutate a second semantic model.

A reasonable eventual progression is:

**Basic**

* board outline;

* grouped/sorted interface labels.

**Intermediate**

* connector groups;

* interface/resource/type information;

* richer labels.

**Extreme**

* documented physical connector locations;

* connector orientation;

* individual contacts/pins where useful;

* actual board image/asset;

* precise target-port highlighting for troubleshooting.

These are presentation modes over the same underlying canonical and visual data, not separate data models.

## Future semantic contracts

No new Protocol, adapter, or Board → Routing contract is currently justified.

Potential future read-only semantic queries may include:

* resolving a visual endpoint to its canonical `SemanticPort` and owner;

* semantic compatibility evaluation between two canonical interfaces;

* exposing canonical connection invariants required during connection authoring.

These should be introduced only when a concrete consumer need demonstrates that direct canonical-model access is no longer an appropriate boundary.

## Research classification

Primary classification:

```text
REINFORCE
```

The real Maestro data validates the existing canonical-model-centered architecture rather than exposing a missing semantic layer.

Secondary classification:

```text
IMPLEMENTATION ONLY
```

The immediate gaps are primarily completeness and projection:

* expand the real Maestro hardware specimen using the existing representation;

* project controller-owned `SemanticPort`s into the existing visual-port mechanism;

* exercise real semantic connection creation and candidate filtering;

* later add the RRF 3.5.4 / Promega implementation specimen.

A limited:

```text
WATCH
```

remains appropriate for:

* whether documented physical connector geometry eventually warrants richer Hardware Definition structures;

* whether a future hardware case demonstrates a genuine need for reusable connector/mating/contact entities;

* whether semantic compatibility or connection-invariant queries become sufficiently complex to justify explicit read-only contracts.

## Recommended real-data implementation sequence

The combined Board and Routing review supports the following sequence:

```text
1. Complete the real Duet 2 Maestro hardware specimen
        ↓
2. Project controller-owned SemanticPorts into the generic visual editor
        ↓
3. Add a real reusable external component
        ↓
4. Evaluate semantic connection candidates
        ↓
5. Create canonical SemanticConnection
        ↓
6. Route the connection using existing Routing
        ↓
7. Build the RRF 3.5.4 / Promega implementation mapping specimen
```

The Maestro does not need to be fully modeled down to every obscure service/debug interface before the visual/editor integration can begin.

The first useful generic visualization can use the real canonical controller and its known interfaces without inventing undocumented physical geometry.

## Overall conclusion

The first real controller has now exercised the intended semantic chain:

```text
real hardware evidence
        ↓
Hardware Definition
        ↓
installed Controller
        ↓
physical interfaces / SemanticPorts
        ↓
Controller Resources
        ↓
machine semantics
        ↓
future firmware-specific implementation mapping
```

The corresponding visual/editor path is:

```text
canonical SemanticPort
        ↓
VisualPort
        ↓
connection editing
        ↓
canonical SemanticConnection
        ↓
Routing geometry
```

The important result is that the current architecture survives contact with real hardware data without requiring a new semantic layer.

The primary remaining work is **real-data coverage, generic visual projection, and later firmware mapping**, not architectural reinvention.

**---**

**# Repository Encoding / Line-Ending Audit Checkpoint**

Updated: 2026-10-05 18:17:02 -04:00

Chat 05 — Efficiency / Modularization / Audit completed a read-only repository encoding and line-ending audit following a real Unicode corruption incident during a PowerShell edit of hardware_catalog.py.

**## Findings**

The repository's stored/index representation is consistent.

The repository contains .gitattributes with * text=auto, and the applicable Git configuration has core.autocrlf=true.

The observed convention is:

\\\	ext

Git repository/index
    LF-normalized text

Windows working tree
    CRLF normally produced by Git
\\\

The widespread CRLF working-tree representation is therefore expected Windows Git checkout behavior, not evidence of repository-wide line-ending corruption.

The audit reported:

\\\	ext

870  index LF / worktree CRLF
3    index LF / worktree LF
6    index LF / worktree MIXED
13   binary/-text handling
5    no line endings
\\\

The six files with genuinely mixed working-tree line endings were:

\\\	ext

CHAT_WORKFLOW.md
machine-structure-editor/handoffs/01_PLANNING_ARCHITECTURE_WORKSTREAM_HANDOFF.md
machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md
machine-structure-editor/handoffs/05_EFFICIENCY_MODULARIZATION_WORKSTREAM_HANDOFF.md
machine-structure-editor/src/machine_builder/hardware_catalog.py
machine-structure-editor/tests/test_connection_authoring.py
\\\

The audit also found two UTF-8-with-BOM files:

\\\	ext

CODER_CHAT_WORKFLOW.md
docs/historical/routing/ROUTING_STABILITY_INVESTIGATION_HANDOFF_4.3.md
\\\

No invalid UTF-8 files were found among the audited text-like files.

**## hardware_catalog.py incident**

The current file contains valid UTF-8 and correct Unicode, including:

\\\	ext

40 × 40 × 10 mm
6200 ±10% RPM
20.4 × 15.3 × 23.2 mm
\\\

No current mojibake was found.

The earlier Unicode corruption was a real transient editing incident, but the current repository no longer contains that corrupted state.

**## Repository editing standard**

For new or deliberately rewritten text files, use UTF-8 without BOM unless an existing historical file has a documented reason to retain another encoding.

For small tracked-file edits:

1. Prefer a small git apply patch when practical.
2. When PowerShell string editing is appropriate, explicitly decode and encode UTF-8.
3. Do not rely on PowerShell's implicit/default text encoding for repository files.
4. Guard replacements so they fail when the expected source block is missing.
5. Also fail when a supposedly unique source block occurs more than once.
6. Preserve existing line endings rather than normalizing the entire file unnecessarily.
7. Run git diff --check after editing.
8. Inspect the relevant git diff.
9. Run the focused tests before broader testing at the appropriate checkpoint.

Byte-based UTF-8 read/write remains appropriate when exact byte-level or BOM preservation is specifically required, but it is not the default mechanism for every ordinary replacement.

The important distinction is:

> **CRLF in the Windows working tree is acceptable. Accidental transcoding of UTF-8 source text is not.**

Uncontrolled PowerShell text round-trips that rely on implicit encoding should not be used for tracked repository edits.

**## Cleanup assessment**

A separate controlled cleanup checkpoint may eventually be warranted for the six mixed working-tree files, deliberate review of the two historical BOM files, and any future confirmed mojibake.

No repository-wide mass conversion is warranted from this audit.

No cleanup or normalization was performed by Chat 05 during the audit.

**## Research classification**

Primary classification:

\\\	ext

REINFORCE
\\\

Secondary classification:

\\\	ext

IMPLEMENTATION ONLY
\\\

WATCH remains appropriate for the localized mixed-line-ending files and historical BOM cases until a deliberate cleanup decision is made.

**## Workflow implication**

This finding does not change the canonical machine architecture.

It reinforces the project-wide requirement that ordinary Machine Builder repository inspection, source mining, implementation, testing, and audit work use the normal repository tooling rather than Python/Jupyter/data-analysis workflows.

The authoritative project-wide tooling, timeline-integrity, and copy/paste command-formatting rules now live in CHAT_WORKFLOW.md.

# PowerShell / Parser Safety Research Checkpoint

Updated:
2026-10-07

## Research conclusion

The Machine Builder PowerShell incident was a parse-time failure in an over-complex composed repository command. The surviving cascade diagnostics do not establish the exact first malformed token, so no stronger certainty should be claimed.

The following technical conclusions are established:

- Multiline parenthesized PowerShell expressions are valid and must not be prohibited.
- Avoid unnecessary backtick line continuation.
- Use here-strings for substantial literal multiline text where appropriate, with exact delimiters.
- `System.Management.Automation.Language.Parser.ParseInput()` is an optional parse-only preflight for unusually complex PowerShell.
- The repository-safe workflow remains:
  bounded inspection
  → validation
  → smallest practical edit
  → `git diff --check`
  → diff inspection
  → focused tests
  → broader tests as appropriate.
- Do not modify repository source merely to obtain diagnostic output when a non-mutating inspection, test, or other diagnostic path can provide the same evidence.

## Separate tooling incident

The `Analysis errored` / Python incident is a separate Machine Builder tooling violation. It must not be conflated with the PowerShell parser failure.

The existing Machine Builder tooling rule already prohibits Python, Jupyter, pandas, notebooks, generated analysis workflows, temporary analysis scripts/artifacts, and data-analysis workflows for ordinary repository work.

## Workflow disposition

No additional `CHAT_WORKFLOW.md` change is justified by this research result.

Workstream #4's recorded PowerShell/parser research dependency is resolved. No special Routing workflow change is required.

## External provenance

Microsoft Learn — `about_Parsing`:
https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_parsing

Accessed:
2026-10-07

Establishes:
PowerShell parsing behavior, valid natural multiline syntax, and the fragility of backtick continuation.

Microsoft Learn — `about_Quoting_Rules`:
https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules

Accessed:
2026-10-07

Establishes:
single-quoted strings and here-string syntax/behavior.

Microsoft Learn — `Parser.ParseInput`:
https://learn.microsoft.com/en-us/dotnet/api/system.management.automation.language.parser.parseinput

Accessed:
2026-10-07

Establishes:
parse-only processing of PowerShell input and returned parser errors without executing the script.

Microsoft Learn — Windows PowerShell 5.1 `about_Character_Encoding`:
https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding?view=powershell-5.1

Accessed:
2026-10-07

Establishes:
important encoding/default-behavior considerations for Windows PowerShell 5.1.

Machine Builder implication:
Use explicit encoding/preserve existing file encoding and line endings when modifying repository text files.

## Next action

No material change to the Research workstream's next action results from this checkpoint. The PowerShell/parser item is closed and Workstream #4's dependency is resolved.

**---
**# Repository Change Rule**

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

**---**

**# Surgical Edit Rules**

When a surgical edit is necessary:

* identify the repository commit inspected;

* give exact line numbers;

* give an exact text/class/function anchor;

* describe the location in plain language;

* for multiple edits, give edits from highest line number to lowest when possible;

* explicitly warn when an earlier edit changes the location of a later edit;

* never rely on programmer shorthand that is not meaningful to a non-programmer user.

If the expected line or anchor cannot be found, stop and re-inspect the current file.

**---**

**# Recovery Rule**

When a future Chat 02 reaches the conversation limit:

```text
Read this handoff

    ↓

Read MASTER_PLAN.md

    ↓

Read PROJECT_CURRENT_STATE.md

    ↓

Review the source register

    ↓

Continue the current research queue
```

Do not redo completed research unless a new question requires it or the source has materially changed.
