# Machine Builder - Research / Architecture (#2) Replacement Prompt

<!-- BEGIN VERIFIED POST-PUBLICATION STARTUP STATE: MB-20261020-1622-02 -->
## Verified Research startup state — 2026-10-20

- **Latest shared baseline:** `ae5a9a1672d151c37e392e9bff4f2421f0a465f2` — `Fix Octopus receiving-interface persistence`. The latest preflight confirmed branch `main`, local HEAD, fetched `origin/main`, and live remote `main` match.
- **Earlier Research publication:** `29c2e54412c6621b112ccfee710e79e6fba46c91` — `Record integer-key persistence investigation findings`.
- **Board fix:** #3 published the Octopus receiving-interface persistence fix at `ae5a9a1672d151c37e392e9bff4f2421f0a465f2`; Planning reports the focused 65-test suite passed. Research did not independently rerun those tests. The generic serializer and TMC5160T map were not changed.
- **Contact 6:** the separate Octopus/TMC5160T hardware-path discrepancy remains **UNRESOLVED**. Do not duplicate #3 investigation.
- **Current authorization:** grant `MB-20261020-1900-01` covers exactly the Research handoff and replacement prompt at baseline `ae5a9a1672d151c37e392e9bff4f2421f0a465f2`.
- **Closeout history:** `MB-20261020-1149-01` (`PUBLISHED — SLOT RELEASED`) was sent to Planning, confirmed by the user.
- **Scope and preservation:** the Standards Index is clean. Preserve every other workstream change; stage and publish only the two paths in the current grant.
- **Research finding:** `_encode()` rejects non-string dictionary keys. The earlier Octopus specification stored contact positions under integer keys; the later Board fix is specific to the receiving-interface persistence case. Do not change the generic serializer or silently stringify keys.
- **Next action:** validate, stage and inspect only the two authorized files; commit with `Refresh Research recovery handoff and replacement prompt`, push normally, verify all refs, and send a separate `PUBLISHED — SLOT RELEASED` closeout.

Older text below this startup checkpoint is historical where it conflicts with the facts above. No additional Research investigation or runtime testing is authorized by this slot.
<!-- END VERIFIED POST-PUBLICATION STARTUP STATE: MB-20261020-1622-02 -->

Prepared: 2026-10-20 (pre-commit final review under grant `MB-20261020-1900-01`; baseline `ae5a9a1672d151c37e392e9bff4f2421f0a465f2`)

## Current repository and publication status

- **Latest verified shared baseline (2026-10-20):** `ae5a9a1672d151c37e392e9bff4f2421f0a465f2` — `Fix Octopus receiving-interface persistence`. Local HEAD, fetched `origin/main`, and live remote `main` matched during preflight.
- **Latest earlier Research publication:** `29c2e54412c6621b112ccfee710e79e6fba46c91` — `Record integer-key persistence investigation findings`.
- **Latest Board publication:** `ae5a9a1672d151c37e392e9bff4f2421f0a465f2` — `Fix Octopus receiving-interface persistence`. Planning reports 65 focused tests passed; Research did not independently rerun them.
- **Distinct unresolved issue:** Octopus V1.1 contact 6 versus TMC5160T Pro V1.0 J1-6 remains **UNRESOLVED**. The Board persistence fix does not settle that hardware-path question.
- **Active Planning grant:** `MB-20261020-1900-01` authorizes exactly these paths at baseline `ae5a9a1672d151c37e392e9bff4f2421f0a465f2`:
  - `machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md`
  - `machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_REPLACEMENT_PROMPT.md`
- **Current staged state:** the shared index contains exactly those two paths for final review. The Standards Index is clean. No other workstream path is part of this batch.
- **Validation:** strict UTF-8 readback and pre-staging `git diff --check` passed. Staged-path scope, staged whitespace, and staged/worktree blob equality were checked before this final review. Commit and push remain pending.
- **Research disposition:** `_encode()` rejection of non-string dictionary keys was source-confirmed, but Research did not reproduce the complete runtime failure. The subsequent Board fix is specific to the Octopus receiving interface; do not silently stringify keys or change the generic serializer.
- **Prior closeout:** `MB-20261020-1149-01` (`PUBLISHED — SLOT RELEASED`) was sent to Planning, as confirmed by the user.
- **Next action:** finish reviewing the complete staged diff, commit with `Refresh Research recovery handoff and replacement prompt`, push normally, verify refs, and send a separate `PUBLISHED — SLOT RELEASED` closeout.

Older publication details and the historical research record follow below.

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
- **Recovery refresh record:** the earlier post-publication refresh was local-only until grant `MB-20261020-1900-01`. This authorized two-file batch is now staged for review; any post-push refresh must record the actual commit and verified refs and remain local-only unless separately authorized.
- **Authorization boundary:** prior Research grants are consumed. Grant `MB-20261020-1900-01` authorizes only the two Research handoff files at baseline `ae5a9a1672d151c37e392e9bff4f2421f0a465f2`. No runtime test or product-code change is authorized.
- **Next-session repository guard:** the shared `main` branch may advance with other workstreams. Fetch and verify the actual current local/fetched/live references before further repository operations; do not assume the repository remains at this commit, and never move it backward to this baseline.
- **Preservation rule:** inspect the shared index before any Git write. Preserve all unrelated staged, unstaged, and untracked work belonging to other workstreams.
- **Research scope:** the historical DYZE wording conflict and current prototype-feature status are ANSWERED under `MB-20261018-2038-01`. Do not conduct more archive probing solely for those questions, expand the ontology, or infer implementation authorization. Continue only for a distinct unresolved question or new primary evidence.

## Essential project boundaries
- Read current workflow and authority docs as needed: `CHAT_WORKFLOW.md`, `DOCUMENTATION_AUTHORITY.md`, `WORKSTREAM_FOCUS_INDEX.md`, `MASTER_PLAN.md`, and `PROJECT_CURRENT_STATE.md`.
- Keep physical coolant topology distinct from electrical wiring and firmware assignments.
- Do not claim the current Cooling Unit provides automatic kink/blockage detection or print pausing.
- Do not make this investigation a prerequisite for #4 visual work or Promega wiring.
- #2 owns the Standards Index, Research handoff, and this canonical prompt. Planning owns publication-slot authorization.
