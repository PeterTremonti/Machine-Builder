# Machine Builder - Research / Architecture (#2) Replacement Prompt
Prepared: 2026-10-19 (publication review refresh; time not captured)

## Current repository and publication slot
- Verified baseline before staging: `458b287565f11b6fa89c9c2bcdc27da90a2a9cfb` — `Create Screenshot 2026-10-19 002012.png` (unrelated screenshot-only commit; no Research target paths changed in it).
- Planning publication grant: `MB-20261018-2347-01`.
- The pre-publication guard confirmed branch `main`, local `HEAD`, fetched `origin/main`, and live remote `main` matched the baseline; the shared staging index was empty.
- Authorized publication scope is limited to these three paths:
  - `machine-builder-research/standards/STANDARDS_INDEX.md`
  - `machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_WORKSTREAM_HANDOFF.md`
  - `machine-structure-editor/handoffs/02_RESEARCH_ARCHITECTURE_REPLACEMENT_PROMPT.md`
- Review must finish before staging. Preserve all other workstream edits and never stage broadly.

## Accepted Research disposition
Planning accepted the historic wording conflict and current prototype-feature status as **ANSWERED** under `MB-20261018-2038-01`. No further archive probing is required solely for those questions. No ontology expansion or implementation is authorized.

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

## Publication procedure
1. Re-run a fresh guarded preflight immediately before staging. Confirm branch `main`, local `HEAD`, fetched `origin/main`, live remote `main`, the empty shared staging index, and the exact three target states.
2. Strictly validate UTF-8 and run target-only `git diff --check`. Inspect the complete diffs of the two tracked documents and the complete untracked prompt.
3. Stage only the three paths listed above. Verify the exact staged path list; inspect the complete staged diff; run `git diff --cached --check`.
4. Commit and push normally. Do not reset, discard, unstage, or stage other workstreams' paths.
5. Verify local `HEAD`, fetched `origin/main`, and live remote `main` all match. Report the full commit hash, subject, exact paths, checks and remote verification to Planning (#1).
6. After publication, refresh this prompt in place with the verified commit result. Explicitly record that this post-publication prompt refresh is a local, unpublished change not included in the publication commit. Do not stage it again without a new Planning slot.

## Essential project boundaries
- Read current workflow and authority docs as needed: `CHAT_WORKFLOW.md`, `DOCUMENTATION_AUTHORITY.md`, `WORKSTREAM_FOCUS_INDEX.md`, `MASTER_PLAN.md`, and `PROJECT_CURRENT_STATE.md`.
- Keep physical coolant topology distinct from electrical wiring and firmware assignments.
- Do not claim the current Cooling Unit provides automatic kink/blockage detection or print pausing.
- Do not make this investigation a prerequisite for #4 visual work or Promega wiring.
- #2 owns the Standards Index, Research handoff, and this canonical prompt. Planning owns publication-slot authorization.
