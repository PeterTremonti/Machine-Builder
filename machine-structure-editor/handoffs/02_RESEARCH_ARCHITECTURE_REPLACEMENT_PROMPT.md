# Machine Builder - Research / Architecture (#2) Replacement Prompt
Prepared: 2026-10-19 (refreshed for active publication slot `MB-20261019-1819-01`; pre-publication state)

## Current repository and publication status
- **Latest verified shared baseline (2026-10-19):** `9b3013d1cbecebbc32e6e17909a8ea09885a4833` - `Document revision-pinned TMC5160T routing evidence`. Fresh preflight verified local HEAD, fetched `origin/main`, and live remote `main` match at this commit; recheck before any future Git write.
- **Most recent published Research batch:** `e210c92af2edac5b8a5e92df122225622ff4f007` - `Reconcile DYZE cooling source evidence` (2026-10-19). Newer local Research changes are not included in that publication.
- **Historical parent baseline for the published `e210c92` commit:** `458b287565f11b6fa89c9c2bcdc27da90a2a9cfb` (`Create Screenshot 2026-10-19 002012.png`).
- **Historical Planning publication grant (consumed):** `MB-20261018-2347-01` authorized the three paths below for the completed `e210c92af2edac5b8a5e92df122225622ff4f007` publication. It does not authorize publishing newer local updates.
- **Historical post-push verification:** for that publication, local `HEAD`, fetched `origin/main`, and live remote `main` were verified equal to `e210c92af2edac5b8a5e92df122225622ff4f007`. The newer shared baseline is recorded above.
- **Published paths:**
  - `machine-builder-research/standards/STANDARDS_INDEX.md`
  - `machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md`
  - `machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_REPLACEMENT_PROMPT.md`
- **Validation:** strict UTF-8 checks, target-only `git diff --check`, exact staged-path verification, staged-blob/working-file equality, and `git diff --cached --check` all passed before commit. The commit parent and exact three committed paths were verified.
- **Current local Research changes:** `machine-builder-research/standards/STANDARDS_INDEX.md`, `machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md`, and this replacement prompt have unstaged, unpublished updates. They are not included in the current shared baseline.
- **Current authorization:** old grant `MB-20261018-2347-01` is consumed. Grant `MB-20261019-1815-02` was superseded by active grant `MB-20261019-1819-01`, which authorizes only the three Research paths listed above. Approved subject: `Record integer-key persistence investigation findings`. No runtime regression test is authorized.
- **Shared index at the fresh preflight:** empty. Preserve all other workstream changes in the worktree and stage only the three paths authorized by `MB-20261019-1819-01`.
- Preserve all other workstream changes. Do not stage broadly, reset, discard, or unstage another workstream's work.

## Standing publication and recovery rules (Planning directives, 2026-10-19)

- **Publish and yield (`MB-20261019-1749-01`):** publish a complete, validated, coherent batch as soon as an explicit slot authorizes its exact paths. Do not wait for unrelated work. If blocked or no safe authorized batch is ready, do not stage or publish; report the blocker and yield. This standing convention does not itself grant publication authority.
- **Recovery freshness (`MB-20261019-1752-01`):** update the canonical handoff and this prompt in place after material findings, validation results, recovery-relevant failures, blocker/owner/next-action changes, publication changes, and yield decisions. Keep this prompt concise and self-contained; retain detailed evidence and history in the handoff.
- **Current verified state:** branch `main`; local HEAD, `origin/main`, and live remote `main` matched at the baseline recorded above. The Standards Index, Research handoff, and replacement prompt have local unpublished updates.
- **Exact next action:** complete publication under `MB-20261019-1819-01`. Immediately before staging, recheck branch, local HEAD, fetched `origin/main`, live remote `main`, empty shared index, and prior Research ancestry. Validate UTF-8 and target-only whitespace; inspect the complete three-file diff; stage only the authorized paths; verify the exact staged list and complete staged diff; run `git diff --cached --check`; commit with subject `Record integer-key persistence investigation findings`; push normally; and verify local, fetched, and live remote checkpoints. No runtime test is authorized. Immediately afterward send Planning a separate `PUBLISHED — SLOT RELEASED` or `BLOCKED — SLOT RELEASED` closeout.
- **When a new grant is issued:** recheck branch, local HEAD, `origin/main`, live remote `main`, shared index, and all worktree changes. Stage only authorized paths; inspect the full staged diff; run `git diff --cached --check`; commit and push normally; verify local/fetched/live remote checkpoints; then refresh this prompt with the actual result.

## Accepted Research disposition
Planning accepted the historic wording conflict and current prototype-feature status as **ANSWERED** under `MB-20261018-2038-01`. No further archive probing is required solely for those questions. No ontology expansion or implementation is authorized.

### Integer-key persistence checkpoint (accepted by Planning 2026-10-19)

Planning accepted the read-only Research finding under `MB-20261019-1547-01`, following `MB-20261019-1450-01`.

- **Source-confirmed mechanism:** `machine-structure-editor/src/machine_builder/persistence.py` `_encode()` rejects non-string dictionary keys before JSON encoding. `serialize_editor_state()` invokes `_encode(state)`, and `save_editor_state()` serializes before temporary-file creation.
- **Source-confirmed data shape:** `BTT_OCTOPUS_MOTOR_DRIVER_RECEIVING_INTERFACE_SPEC["contacts"]` uses integer contact-position keys, and the specification is embedded in `machine-structure-editor/src/machine_builder/controller_board_fixtures.py` by `add_octopus_tmc5160t_mating_experiment()`.
- **Not demonstrated:** no runtime test was run; the exact first nested map encountered was not confirmed; a complete Octopus save/reopen failure has not been demonstrated. Do not report the runtime hypothesis as reproduced.
- **Preferred representation:** contact records carrying numeric `position` fields. Do not change the generic serializer or silently stringify keys.
- **Disposition:** Planning will route the bounded runtime regression to the implementation owner. #2 needs no further investigation unless contradictory evidence appears. This prompt is included in active documentation-only grant `MB-20261019-1819-01`; do not run the runtime regression under this grant.

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
- **Recovery refresh record:** this prompt is included in active publication grant `MB-20261019-1819-01`. After publication, refresh this prompt in place with the actual verified commit and remote state; any later refresh will remain a separate local change unless separately authorized.
- **Authorization boundary:** prior grant `MB-20261018-2347-01` is consumed, and `MB-20261019-1815-02` was superseded. Active grant `MB-20261019-1819-01` covers only the three Research paths listed above. Do not include other workstream paths; stop if any preflight or scope guard fails.
- **Next-session repository guard:** the shared `main` branch may advance with other workstreams. Fetch and verify the actual current local/fetched/live references before further repository operations; do not assume the repository remains at this commit, and never move it backward to this baseline.
- **Preservation rule:** inspect the shared index before any Git write. Preserve all unrelated staged, unstaged, and untracked work belonging to other workstreams.
- **Research scope:** the historical DYZE wording conflict and current prototype-feature status are ANSWERED under `MB-20261018-2038-01`. Do not conduct more archive probing solely for those questions, expand the ontology, or infer implementation authorization. Continue only for a distinct unresolved question or new primary evidence.

## Essential project boundaries
- Read current workflow and authority docs as needed: `CHAT_WORKFLOW.md`, `DOCUMENTATION_AUTHORITY.md`, `WORKSTREAM_FOCUS_INDEX.md`, `MASTER_PLAN.md`, and `PROJECT_CURRENT_STATE.md`.
- Keep physical coolant topology distinct from electrical wiring and firmware assignments.
- Do not claim the current Cooling Unit provides automatic kink/blockage detection or print pausing.
- Do not make this investigation a prerequisite for #4 visual work or Promega wiring.
- #2 owns the Standards Index, Research handoff, and this canonical prompt. Planning owns publication-slot authorization.
