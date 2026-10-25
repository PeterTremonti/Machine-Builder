# Machine Builder - Research / Architecture (#2) Replacement Prompt

<!-- BEGIN VERIFIED RESEARCH STARTUP STATE: MB-20261024-2356-01 -->
## Current Research startup state - 2026-10-25

- **Published baseline at latest preflight:** local HEAD, fetched `origin/main`, and live `origin/main` matched `b5e2d079120206758124ce8431fe57556fb6b4d5` (`docs: refresh stable-code audit continuity`, 2026-10-24 23:48:12 EDT). No commits were found between Planning's reported checkpoint and HEAD. Recheck refs before any future repository work.
- **Current local document state at task start:** shared index was empty. The Research handoff had the local 62-line continuity addition; the replacement prompt was clean. Other workstreams have modified and untracked paths. Preserve every unrelated file and do not assume old status snapshots still apply.
- **Published Promega composer:** commit `a4c5ad9347ae56990f9de4049b78cc3cc591e22f` (`add shared Promega specimen composer`, 2026-10-24 18:49:27 EDT) adds `src/machine_builder/promega_specimen.py` and updates `tests/test_promega_reference_specimen.py` with the combined specimen composition/round-trip path. Accepted contract: `build_promega_reference_specimen() -> EditorState`, returning a detached complete state built through existing authoring paths. This is a published builder/test milestone, not a dedicated application-menu entry point.
- **Promega physical harness crosswalk:** bounded research is accepted, but reference documentation and guide-position-to-PCB-pad identity do not prove the installed cable identity or continuity. P9/P11 fan mapping and H2/H4 heater plus S8/S6 sensor mappings remain unresolved pending the user's physical inspection of the printer. Preserve P4/P2 and other machine-specific unknowns; do not repeat completed research without a new evidence target.
- **Routing/cone findings:** separate visible stubs, endpoint fanout/escape geometry, and missing direct stub-selection coverage are actionable diagnostics, not a confirmed root cause. #4 retains implementation ownership.
- **Application entry point and integration:** the ordinary app workflow has no confirmed dedicated Promega-specimen entry point. Planning accepted future atomic installation of a complete state as a populated, unsaved document: Cancel prevents composition and installation; composition/preparation failure preserves the active document, path, modified state, and history; successful installation replaces visual and semantic state together, clears history/path, marks the populated document modified, and notifies listeners after commitment. Normal Save As/Open behavior must remain. #3 owns the composer; #4 owns future UI integration after its GUI acceptance work stabilizes. Coordinate the whole-state API with concurrent store/scene changes.
- **Dragging lag:** handoff `MB-20261024-1834-01` was sent to #4. Read-only inspection found full connection updates on node-position events and multiple potential refreshes during scene synchronization. These are optimization leads, not measured results or a confirmed root cause. #4 owns instrumentation and implementation after current GUI acceptance work stabilizes. #2 did not modify source or run performance tests.
- **Other accepted research:** DYZE historical bend-radius wording and the prototype-era pause-feature question are ANSWERED under `MB-20261018-2038-01`; do not repeat archive searches without a materially different question or new primary evidence. Octopus V1.1 / TMC5160T Pro contact 6 (`SLEEP` versus `CLK`) remains unresolved and belongs to #3.
- **Publication authorization:** Planning authorized only these two Research continuity documents under `MB-20261024-2356-01`, with commit subject `docs: refresh Research continuity after Promega milestones`. Keep the edits separate from source/test changes. Confirm publication and grant consumption through Git history and matching refs; this prompt does not prove its own publication.

## Operating and validation boundaries
- Research provides source-grounded evidence and bounded comparisons; Planning controls durable architecture and implementation authorization.
- Read `CHAT_WORKFLOW.md`, `DOCUMENTATION_AUTHORITY.md`, `MASTER_PLAN.md`, `PROJECT_CURRENT_STATE.md`, and `machine-builder-research/START_HERE.md` as appropriate to the actual assignment.
- This continuity refresh is documentation-only. Do not report application tests as run.
- Preserve UTF-8 and existing line endings. Read back each edited file, inspect its focused diff, and run `git diff --check`.
- Preserve every unrelated staged, modified, and untracked path. For the authorized publication, stage only the two Research handoff/prompt files, verify the exact staged set and complete staged diff, run `git diff --cached --check`, commit, push normally, fetch, and verify local HEAD, fetched `origin/main`, and live remote `main` all match. Do not force-push.
<!-- END VERIFIED RESEARCH STARTUP STATE: MB-20261024-2356-01 -->

Historical preparation record: 2026-10-20 (pre-commit final review under grant `MB-20261020-1900-01`; baseline `ae5a9a1672d151c37e392e9bff4f2421f0a465f2`)

## Historical publication record through 2026-10-20

- **Latest verified shared baseline (2026-10-20):** `dfefa9df337bc431a0056554d5c72843075132cf` — `Refresh Research recovery handoff and replacement prompt`. Local HEAD, fetched `origin/main`, and live remote `main` matched after publication.
- **Parent:** `ae5a9a1672d151c37e392e9bff4f2421f0a465f2` — `Fix Octopus receiving-interface persistence`.
- **Latest Research publication:** the two-file recovery refresh was published in `dfefa9df337bc431a0056554d5c72843075132cf`.
- **Exact committed paths:**
  - `machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md`
  - `machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_REPLACEMENT_PROMPT.md`
- **Push verification:** normal push succeeded; subsequent fetch confirmed local HEAD, fetched `origin/main`, and live remote `main` all match the published commit.
- **Validation:** strict UTF-8 readback, pre-staging and staged whitespace checks, exact staged-path check, staged/worktree blob equality, and exact committed-path verification passed.
- **Tests:** no application tests were run; this was a documentation-only publication.
- **Historical authorization (2026-10-20):** grant `MB-20261020-1900-01` was consumed and the slot released. No active Research publication grant remained at that checkpoint.
- **Research status:** `_encode()` rejection of non-string dictionary keys was source-confirmed. #3 has published the Octopus receiving-interface persistence fix; Planning reports 65 focused tests passing, which Research did not independently rerun. Contact 6 remains a separate unresolved hardware-path question.
- **Historical local-state snapshot (2026-10-20):** at that checkpoint, the handoff and prompt post-publication refreshes were unstaged local-only edits and the Standards Index was clean. This describes only that historical state, not the current working tree. Preserve all other workstream changes.
- **Historical next action (2026-10-20):** send or confirm Planning closeout `MB-20261020-1934-01`, then await Planning direction. This described the next step at that historical checkpoint; later Planning instructions and the current grant supersede it.

Older publication history follows below; do not interpret its historical authorization or staging statements as current.

## Accepted Research disposition
Planning accepted the historic wording conflict and current prototype-feature status as **ANSWERED** under `MB-20261018-2038-01`. No further archive probing is required solely for those questions. No ontology expansion or implementation is authorized.

### Integer-key persistence checkpoint (accepted by Planning 2026-10-19)

Planning accepted the read-only Research finding under `MB-20261019-1547-01`, following `MB-20261019-1450-01`.

- **Source-confirmed mechanism:** `machine-structure-editor/src/machine_builder/persistence.py` `_encode()` rejects non-string dictionary keys before JSON encoding. `serialize_editor_state()` invokes `_encode(state)`, and `save_editor_state()` serializes before temporary-file creation.
- **Source-confirmed data shape:** `BTT_OCTOPUS_MOTOR_DRIVER_RECEIVING_INTERFACE_SPEC["contacts"]` uses integer contact-position keys, and the specification is embedded in `machine-structure-editor/src/machine_builder/controller_board_fixtures.py` by `add_octopus_tmc5160t_mating_experiment()`.
- **Not demonstrated:** no runtime test was run; the exact first nested map encountered was not confirmed; a complete Octopus save/reopen failure has not been demonstrated. Do not report the runtime hypothesis as reproduced.
- **Preferred representation:** contact records carrying numeric `position` fields. Do not change the generic serializer or silently stringify keys.
- **Disposition:** #3 subsequently published the Octopus receiving-interface persistence fix at `ae5a9a1672d151c37e392e9bff4f2421f0a465f2`. Planning reports 65 focused tests passed; Research did not rerun them. Contact 6 remains a separate unresolved hardware-path question.

### Historical page evidence
- Capture: https://web.archive.org/web/20250914220257/https://docs.dyzedesign.com/liquid-cooling.html
- Wayback capture timestamp: `2025-09-14 22:02:57`.
- The capture footer says `Last Updated: 9/4/2025, 1:31:37 PM`.
- The captured First setup section says the tubing bend radius must never be smaller than 2 inches (50 mm).
- The captured Mounting section says kink/blockage faults will be detected and printing paused, and also says the radius should not exceed 2 inches (50 mm). This directly verifies that the contradictory inequalities and automatic-pause claim coexisted in the captured version.

### Manufacturer support clarification
- DYZE Technical Support email was displayed as Tuesday, October 13, 2026, at 11:30 AM, in response to questions submitted on October 12. Timezone is not stated in the supplied email copy.
- For supplied soft, high-temperature rubber tubing, 1/4-inch ID x 3/8-inch OD, support confirms a 50 mm minimum bend radius, measured to the tube OD as the email states. The minimum applies while stationary and while moving.
- Support explicitly states the automatic kink/blockage detection and print-pause feature is unavailable in the current version. The statement was carried over from an earlier prototype, which was removed because too many false positives and insufficient consistency made it an unreliable safeguard. Support apologized and said the documentation would be updated.
- Current guide: https://docs.dyzedesign.com/liquid-cooling.html . Its displayed footer is `10/13/2026, 5:11:12 PM`; the current guide agrees with the 50 mm minimum and no longer includes the old automatic-pause claim.
- The email's explicit promise, same-day guide timestamp and matching content strongly support attributing the documentation correction to the support questions. The internal edit history is unavailable, so the exact edit event is not directly proven.

## Remaining unknowns and evidence limits
- Installed Cooling Unit revision, actual tubing/fittings, routing, wiring, and firmware configuration remain unknown. Do not infer them from documentation.
- Wayback all-time exact-URL CDX returned 21 rows after digest collapsing, spanning 2019-07-02 through 2025-09-14. A query limited to 2026-09-01 through 2026-10-20 returned HTTP 200 with zero rows; a wildcard request returned HTTP 503.
- Exact-URL Common Crawl requests for five recent 2026 collections returned HTTP 504. Those failures do not prove there are no captures.
- Further archive probing is not needed for the questions Planning marked ANSWERED. Continue only if a distinct unresolved question or new primary evidence appears.

## Publication record and next-session instructions
- **Publication status:** COMPLETE for Planning slot `MB-20261018-2347-01`.
- **Commit:** `e210c92af2edac5b8a5e92df122225622ff4f007`
- **Subject:** `Reconcile DYZE cooling source evidence`
- **Push verification:** normal push succeeded; a subsequent fetch and live `git ls-remote` confirmed local `HEAD`, fetched `origin/main`, and live remote `main` all match the published commit.
- **Scope verification:** the commit parent was `458b287565f11b6fa89c9c2bcdc27da90a2a9cfb`, and the commit changed exactly the three authorized paths listed in the current repository status section.
- **Checks completed:** the shared index was empty before staging; only the three authorized paths were staged; strict UTF-8 validation, target-only working-tree whitespace check, exact staged-path check, staged blob hash comparison, and staged whitespace check passed.
- **Historical recovery refresh record (2026-10-20):** publication completed at `dfefa9df337bc431a0056554d5c72843075132cf`. This follow-up edit records the verified post-push state locally and remains unpublished unless separately authorized.
- **Historical authorization boundary (2026-10-20):** grant `MB-20261020-1900-01` is consumed. These post-publication recovery edits are local-only and are not authorized for another publication.
- **Next-session repository guard:** the shared `main` branch may advance with other workstreams. Fetch and verify the actual current local/fetched/live references before further repository operations; do not assume the repository remains at this commit, and never move it backward to this baseline.
- **Preservation rule:** inspect the shared index before any Git write. Preserve all unrelated staged, unstaged, and untracked work belonging to other workstreams.
- **Research scope:** the historical DYZE wording conflict and current prototype-feature status are ANSWERED under `MB-20261018-2038-01`. Do not conduct more archive probing solely for those questions, expand the ontology, or infer implementation authorization. Continue only for a distinct unresolved question or new primary evidence.

## Essential project boundaries
- Read current workflow and authority docs as needed: `CHAT_WORKFLOW.md`, `DOCUMENTATION_AUTHORITY.md`, `WORKSTREAM_FOCUS_INDEX.md`, `MASTER_PLAN.md`, and `PROJECT_CURRENT_STATE.md`.
- Keep physical coolant topology distinct from electrical wiring and firmware assignments.
- Do not claim the current Cooling Unit provides automatic kink/blockage detection or print pausing.
- Do not make this investigation a prerequisite for #4 visual work or Promega wiring.
- #2 owns the Standards Index, Research handoff, and this canonical prompt. Planning owns publication-slot authorization.
