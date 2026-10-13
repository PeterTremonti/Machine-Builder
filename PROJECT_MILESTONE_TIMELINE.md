# Project Milestone Timeline

**Status:** Initial Planning draft, prepared October 13, 2026. Review before adding this document to the documentation authority map.

## Purpose and boundaries

This document records significant project milestones, when they occurred, what changed, and the evidence supporting each record. It is a chronology, not a replacement for the project's planning, current-state, architecture, or workstream documents.

- `MASTER_PLAN.md` remains the planning and decision authority.
- `PROJECT_CURRENT_STATE.md` remains the current-state snapshot.
- `DOCUMENTATION_AUTHORITY.md` remains the map of documentation responsibilities.
- Workstream handoffs remain the detailed records for their respective work.
- Legacy retrospective material remains historical evidence, not current authority.

Dates must retain their evidence type. A Git commit timestamp establishes when that commit was recorded; it does not automatically establish when a decision was first discussed or accepted. Document headings and handoff observations are not interchangeable with Git timestamps.

### Evidence labels

- **Git-pinned:** Full commit identity, timestamp, and parent were recovered from Git.
- **Document-recorded:** The event or decision date is recorded in a project document, but may not be the introducing commit date.
- **Reported:** A workstream or saved checkpoint reports the evidence, but the original transcript or primary record is incomplete.
- **Limited / undated:** The milestone is supported only partially, or its date or identity remains unknown.

## Chronology

### Early project history

- **April 10–14, 2026 — Early repository and version-era history.** The public GitHub history listing surfaced `e70a8dd` (“Initial commit”), `aee4c60` (“Initial Machine Builder Commit,” shown April 10), `b564fc2` (“7.8,” shown April 11), `037e7b7` (“New chat. 7.9 abandoned for 7.10,” shown April 13), and `e0f3933` (“7.14 done.,” shown April 14). **Limited:** Only abbreviated identities and dates from the public history listing were recovered for this inventory. These subjects do not establish that each number was a formal release. [Public commit history](https://github.com/PeterTremonti/Machine-Builder/commits/main)

- **Unknown date — Transition to a machine-model-first engineering environment.** Current planning and legacy retrospective material document the project's evolution away from a firmware-configurator framing toward representing the physical machine, a canonical machine model, and firmware-specific mappings as distinct layers. The precise origin date and introducing commit have not been pinned. Do not assign a date from a later retrospective.

### September 2026

- **September 15, 2026 — V0.2 research and implementation checkpoint.** Git-pinned commit [`c77b5e35c8f5e1df1d44ec48f0197352aadd6e1c`](https://github.com/PeterTremonti/Machine-Builder/commit/c77b5e35c8f5e1df1d44ec48f0197352aadd6e1c), parent `55fe4edf097195341951ed78727303a13d44d4b3`, timestamp `2026-09-15T11:24:39-04:00`. The checkpoint establishes a bounded V0.2 research/implementation stopping point using the O0.1 canonical vocabulary rather than creating a new universal ontology. Its principle is to implement the bounded model and revisit ontology only when a concrete case shows that the existing semantics are insufficient. This is the earliest pinned evidence in the reviewed material for the V0.2 research boundary; whether earlier discussions occurred is unknown.

### October 2026 — Documentation, continuity, and authoring infrastructure

- **October 3, 2026 — Documentation framework established.** Git-pinned commit [`5c4cdc9dc2e3f282378b2150641a0050b6fd4573`](https://github.com/PeterTremonti/Machine-Builder/commit/5c4cdc9dc2e3f282378b2150641a0050b6fd4573), parent `23e29b1322c44f0b8b1f686c585d93e8253e0703`, timestamp `2026-10-03T16:44:39-04:00`, subject “Establish Machine Builder documentation framework.” This is a documented project-governance milestone. Specific later changes to the authority map should be read from their own commits.

- **October 5, 2026 — Historical Visual Builder references reconciled.** Git-pinned commit [`e2f12fd65a88a53f245717da3737d64c39a5f076`](https://github.com/PeterTremonti/Machine-Builder/commit/e2f12fd65a88a53f245717da3737d64c39a5f076), parent `3ad13703e8c6f3df59fa0a2b6e90f2e8be299959`, timestamp `2026-10-05T22:18:30-04:00`. Research documentation was clarified to identify old Visual Builder materials as historical/reference material, preserving them rather than treating them as current architecture authority or deleting the historical record.

- **October 7, 2026 — Workstream handoff lifecycle formalized.** Git-pinned commit [`437e67414827f279fee92d1f38f6c82409e14046`](https://github.com/PeterTremonti/Machine-Builder/commit/437e67414827f279fee92d1f38f6c82409e14046), parent `65ea442d2f8318c2c37b95409c5a40f3112236ec`, timestamp `2026-10-07T16:22:32-04:00`, subject “Formalize handoff lifecycle and rollover.” This formalized a repeatable record for workstream continuity and transition between chats.

- **October 8, 2026 — Octopus interface investigation recorded as complete.** Git-pinned commit [`611a22d941345cfe922b96bbf7a9bc027fe6239b`](https://github.com/PeterTremonti/Machine-Builder/commit/611a22d941345cfe922b96bbf7a9bc027fe6239b), parent `6921759924bfd31047ae702a1253a23690e55f22`, timestamp `2026-10-08T22:48:03-04:00`. The commit records completion of the investigation. This is a research closeout, not evidence that every investigated interface is electrically compatible.

- **October 9, 2026 — Canonical-component palette regression coverage.** Git-pinned commit [`8d496aa50a09f2319a665233354ede49c00160f6`](https://github.com/PeterTremonti/Machine-Builder/commit/8d496aa50a09f2319a665233354ede49c00160f6), parent `9c18e4a513ba2befdc2dee9129f26907f75180e0`, timestamp `2026-10-09T17:07:46-04:00`. The committed change added regression coverage for canonical component creation, component-owned port authoring, undo/redo, and save/reopen identity and linkage. The associated handoff records 70 focused and 805 full-suite tests passing; exact original command output was not recovered in the evidence-pinning pass, so see the validation record below.

### October 10–11, 2026 — Promega vertical-slice priority

- **October 10, 2026, 00:22:38 EDT — Physical connection metadata authoring.** Git-pinned commit [`c445bef287d736afd20807f29d2506aab2434eaa`](https://github.com/PeterTremonti/Machine-Builder/commit/c445bef287d736afd20807f29d2506aab2434eaa), parent `8d496aa50a09f2319a665233354ede49c00160f6`. Canonical `SemanticConnection.properties` gained creation-time capture for wire color, harness ID, and notes, keeping physical connection metadata separate from visual route geometry. The checkpoint reports 46 focused and 827 full-suite tests, but the exact tested-tree SHA and original transcript were not pinned.

- **October 10, 2026, 01:01:59 EDT — Planning decision: prioritize a real Promega vertical slice.** Git-pinned commit [`8ce8102539f10a46d4d057934dfff7570cc92164`](https://github.com/PeterTremonti/Machine-Builder/commit/8ce8102539f10a46d4d057934dfff7570cc92164), parent `c445bef287d736afd20807f29d2506aab2434eaa`. `MASTER_PLAN.md` records the decision to prove the existing architecture against the standard M3D Promega before expanding the ontology or beginning broad hardware-catalog work. The sequence is to instantiate reviewed hardware and board interfaces, author only source-supported physical connections, model functional relationships separately from wiring, and verify visual persistence. The decision states that the examined ontology was sufficient; no new ontology entity had been justified.

- **October 10, 2026, 19:22:31 EDT — Promega vertical-slice checkpoint refreshed.** Git-pinned commit [`52d96d662359eb2299d523dcec8771f010ee7232`](https://github.com/PeterTremonti/Machine-Builder/commit/52d96d662359eb2299d523dcec8771f010ee7232), parent `783c3b56b9f549fbb443c3f7a9a905c413f6a36a`. The checkpoint describes progress from general authoring infrastructure to a source-qualified reference specimen and a small number of reference connections. It explicitly says the specimen is not a complete or verified as-built machine model.

- **October 11, 2026, 00:46:21 EDT — Reusable Promega IR-probe reference wiring fixture.** Git-pinned commit [`9f3626b5b3117c2aef691eec4b04ae9b863485d0`](https://github.com/PeterTremonti/Machine-Builder/commit/9f3626b5b3117c2aef691eec4b04ae9b863485d0), parent `52d96d662359eb2299d523dcec8771f010ee7232`. The fixture adds a bounded source-backed reference-wiring slice. The project snapshot reports 838 tests passed in 8.07 seconds; the original console transcript and exact tested-tree identity were not pinned in this review.

- **October 11, 2026, 00:54:21 EDT — Autonomous workstream continuity documented.** Git-pinned commit [`88fb470b7b60c53d2db4059d271df0a2c2f693b1`](https://github.com/PeterTremonti/Machine-Builder/commit/88fb470b7b60c53d2db4059d271df0a2c2f693b1), parent `9f3626b5b3117c2aef691eec4b04ae9b863485d0`. This documents workstream continuity following the preceding implementation milestones.

- **October 11, 2026, 12:35:02 EDT — Liquid-cooled hotend research checkpoint recorded.** Git-pinned commit [`274a1cd5432fb3803dc351c4b3074c86d6689ccf`](https://github.com/PeterTremonti/Machine-Builder/commit/274a1cd5432fb3803dc351c4b3074c86d6689ccf), parent `25d8268600c0979ecfccfccb8a1b0b04bcf89014a`. Research records a bounded investigation into the DYZE liquid-cooled hotend and coolant loop. Later direct supplier clarification changed the evidence available for hose bend radius and cooling-unit protection claims; see October 13 below.

### October 12, 2026 — Source qualification and hardware crosswalks

- **October 12, 2026, 15:29:06 EDT — Flexible-hose bend-radius interpretation recorded.** Git-pinned commit [`11a25a0e65178179c3025d6683119ce8c52056ff`](https://github.com/PeterTremonti/Machine-Builder/commit/11a25a0e65178179c3025d6683119ce8c52056ff), parent `8c7e94efa3f0d691bbd678ad836ea81a283335f8`. This was an interpretation of public guidance, not a confirmed supplier statement. The working hypothesis in this historical record must not override the later direct supplier response.

- **October 12, 2026, 16:00:37 EDT — DYZE public-evidence reconciliation.** Git-pinned commit [`ff74c318ea15ca4b891ee3d5b523d932d14d8610`](https://github.com/PeterTremonti/Machine-Builder/commit/ff74c318ea15ca4b891ee3d5b523d932d14d8610), parent `11a25a0e65178179c3025d6683119ce8c52056ff`. At this checkpoint, public bend-radius guidance was still considered conflicting and supplier confirmation was pending. It documented 50 mm as an unconfirmed working hypothesis and did not establish blockage detection or automatic print pausing.

- **October 12, 2026, 16:01:51 EDT — Promega J28 identity qualified by source and guide-view position.** Git-pinned commit [`ec5c7381fe5624e94bb22c81740153ce260ab298`](https://github.com/PeterTremonti/Machine-Builder/commit/ec5c7381fe5624e94bb22c81740153ce260ab298), parent `ff74c318ea15ca4b891ee3d5b523d932d14d8610`. Routing distinguished guide-view position from fixture position, PCB pad, and cable cavity while adding three source-supported J28 reference links. This is a bounded reference-wiring milestone, not proof of the complete as-built machine graph. The historical test evidence has unresolved provenance; see the validation notes below.

- **October 12, 2026, 18:00:46 EDT — J34/E0 STOP reference-PCB crosswalk published.** Git-pinned commit [`287a1489a53dc695d5dc5a55defd795151de3719`](https://github.com/PeterTremonti/Machine-Builder/commit/287a1489a53dc695d5dc5a55defd795151de3719), parent `e4c8d6edb8fdc773e80b527b17c3ef162618182c`. The Board workstream added the J34 E0 STOP PCB identity crosswalk while preserving the existing stable semantic endpoint IDs. Reported validation: 30 focused Board fixture tests passed, 843 full-suite tests passed, `git diff --check` passed, and the publication was verified against `origin/main`. This does not close unrelated unresolved Promega extruder, fan, heater, or thermistor mappings.

### October 13, 2026 — Supplier clarification and live checkpoint

- **October 13, 2026 — DYZE supplier clarification received, as reported by Research.** A direct written response from DYZE technical support confirms a 50 mm minimum bend radius for the supplied 1/4-inch ID × 3/8-inch OD tubing, measured with reference to the tubing's outside diameter. The supplier also clarified that the current Cooling Unit does **not** have blockage detection or automatic print pausing; those claims were inherited from a prototype and are to be corrected in the documentation. This supersedes the earlier public-source hypothesis about bend radius and resolves the uncertainty in the public research note about those protection capabilities. **Reported / primary reference not yet archived:** Research reports receiving the response on October 13, 2026, but the original support message has not yet been retained as a durable primary-source artifact in the reviewed repository evidence. Do not infer dynamic-flex cycle life or additional temperature/pressure ratings; these were not provided.

- **October 13, 2026 — Live Git checkpoint independently refreshed.** The local `HEAD`, local `origin/main`, and live remote `refs/heads/main` all resolved to `287a1489a53dc695d5dc5a55defd795151de3719`, commit date October 12, 2026. This confirms the J34 publication was still the branch tip at the time of the check. The working tree was **not clean**: Planning/workflow/Routing files and Visual Editor source/tests had concurrent uncommitted changes, including an untracked functional-interface connection test. Those changes were preserved. This is a dated checkout observation, not a claim that the worktree is clean or that the same branch tip remains current indefinitely.

## Historical test evidence and limits

Test figures below are historical evidence records. They are not a current test baseline, and the timeline author did not rerun these suites.

| Checkpoint | Reported result | Evidence grade and limitation |
| --- | --- | --- |
| `8d496aa50a09f2319a665233354ede49c00160f6` | 70 focused; 805 full-suite passed | Recorded in the committed handoff. Original full console transcript and exact command were not recovered. |
| `c445bef287d736afd20807f29d2506aab2434eaa` | 46 focused; 827 full-suite passed | Reported in the project snapshot; exact invocation, transcript, and tested-tree SHA were not pinned. |
| `9f3626b5b3117c2aef691eec4b04ae9b863485d0` | 838 passed in 8.07 seconds | Reported in `MASTER_PLAN.md`; the tested-tree SHA, exact command, and raw transcript were not recovered here. |
| J28 Routing checkpoint, around `11a25a0e65178179c3025d6683119ce8c52056ff` | 33 focused and 842 full-suite passed | Conflicting reported timings: the published handoff says 5.73/8.44 seconds; a supplement says 5.46/8.45 seconds. The handoff's validation SHA and the supplement's stated test checkpoint also differ. The exact run-to-tree pairing remains unresolved. Do not label these as tests proven to have run on `ec5c738...`. |
| `287a1489a53dc695d5dc5a55defd795151de3719` | 30 focused Board fixture tests; 843 full-suite passed | Workstream-reported validation at the J34 publication checkpoint, with whitespace validation and ancestry checks also reported as passing. This is the strongest of the listed recent checkpoint records, but remains a reported run rather than a new execution for this timeline. |

Older test-count figures such as 756, 765, 772, or 52 focused tests appear in historical workstream notes but were not all tied to full commit identities, exact invocations, and tested trees in the evidence reviewed. Preserve them as historical reports only; do not plot them as a continuous trend.

## Open evidence gaps

1. **Early history and project origin:** Resolve full commit identities and parents for the initial April entries; identify when the firmware-configurator-to-machine-model-first transition was actually made.
2. **V0.2 stopping rule:** The September 15 checkpoint is the earliest pinned evidence found. Earlier discussion or approval, if any, remains unverified.
3. **Historical test provenance:** Recover raw transcripts and exact tested-tree SHAs for older reports if they are needed for an audit. The J28 run-to-tree and timing ambiguity remains unresolved.
4. **DYZE primary communication:** Retain a durable, appropriately redacted copy or reference to the supplier response if audit-grade primary-source traceability is required.
5. **Future repository state:** Refresh live Git and worktree status whenever using this document for a current branch or publication claim. The October 13 Git observation is only a historical snapshot.

## Interpretation rule

A milestone with a missing date, parent, raw test transcript, physical assembly identity, or primary-source reference must keep that limitation visible. Do not upgrade an unknown to a confirmed fact because a later document repeats it. The purpose of this timeline is to make project history easier to navigate without making the historical record look more certain than the evidence supports.
