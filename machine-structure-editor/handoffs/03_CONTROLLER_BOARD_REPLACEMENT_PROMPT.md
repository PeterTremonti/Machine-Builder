# Machine Builder — #3 Controller/Board Replacement Prompt

Prepared: 2026-10-21 16:30 EDT | Published baseline observed before this continuity refresh: `7d4fc6c0378ffd4de455c8db05dcd636034711c1` — `Add proportional prior-art review to planning workflow`.

## Startup and repository authority

Use the existing checkout: `C:\Users\Peter\Documents\GitHub\Machine-Builder`.

The checkout and Git index are shared by workstreams #1–#5. Local status is authoritative. Before resuming, fetch `origin`, verify branch, `HEAD`, `origin/main`, and live remote `main`; inspect `git status --short --untracked-files=all` and `git diff --cached --name-only`. Preserve all other staged, unstaged, and untracked changes. Never blanket-stage, reset, discard, stash, or unstage another workstream's work. Never force-push.

Required reading: `CHAT_WORKFLOW.md`, `MASTER_PLAN.md`, `PROJECT_CURRENT_STATE.md`, and `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`. Use their latest committed/local state rather than assuming this snapshot is current.

## Published Board state

### Octopus receiving-interface persistence

The Octopus receiving-interface contact-list correction and save/reopen regression are published in commit `ae5a9a1672d151c37e392e9bff4f2421f0a465f2`, subject `Fix Octopus receiving-interface persistence`.

Published paths:
- `machine-structure-editor/src/machine_builder/hardware_catalog.py`
- `machine-structure-editor/tests/test_octopus_driver_mating.py`
- `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`

The contact map is a list of 18 records containing numeric `position`, original `label`, and original `classification`: positions 1–16 are active, position 17 is NC/not-connected, and position 18 is DIAG/diagnostic. Publication validation passed `65 passed in 0.33s`. The staged whitespace check passed, and post-push `HEAD`, `origin/main`, and live remote `main` matched the published commit. The generic persistence encoder and separate TMC5160T module-interface contact map were not changed.

The Board investigation checkpoint `9b3013d1cbecebbc32e6e17909a8ea09885a4833` (`Document revision-pinned TMC5160T routing evidence`) is historical context; the Octopus persistence fix above is a later published commit.

### Electrical discrepancy — UNRESOLVED

Octopus V1.1 Driver 2 contact 6 is documented as `SLEEP` / `DRIVER2_SLP`. TMC5160T Pro V1.0 module J1-6 is documented as `CLK` (external clock input); J1-3 `SCK/CFG2` is the SPI serial clock. Existing public artifacts, product pairing, third-party manual copies, and issue reports do not establish revision-qualified contact-to-contact continuity, exact module routing, the as-built jumper state, or electrical equivalence.

Do not infer a confirmed short, incompatibility, or installed electrical path without suitable evidence. Preserve the explicit **UNRESOLVED** disposition. The living handoff section 35 contains the detailed source investigation; verify whether its currently noted local-only source addition is actually present in the worktree or published revision before relying on it.

## Stepper-terminal-profile test — blocked on #4

The local-only file `machine-structure-editor/tests/test_stepper_motor_terminal_profile.py` exercises `UpdateMachineComponentWithStepperTerminalProfile` and terminal projection behavior.

Last reported combined-working-tree command on 2026-10-20:

`python -m pytest -q tests/test_stepper_motor_terminal_profile.py tests/test_controller_board_fixtures.py`

Result: `34 passed in 0.20s`. This result depends on the symbol being present in the modified local #4-owned `machine-structure-editor/src/machine_builder/semantic_component_mutations.py`. The symbol was absent from the published baseline `7d4fc6c0378ffd4de455c8db05dcd636034711c1`, so this was not a validation run against published code alone.

Planning message `MB-20261020-2045-03` accepted the blocker: #4 owns publication of the implementation dependency and received the next validation/publication slot. Keep the Board test local and unpublished; do not stage it alongside #4's code. After #4 reports verified publication, Planning will reassess the actual shared baseline and authorize a separate Board slot. Re-run the tests against that verified state rather than assuming the previous result is sufficient.

## Documentation publication boundary

Planning message `MB-20261021-1618-01` grants a documentation-only slot for these two paths:

- `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`
- `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_REPLACEMENT_PROMPT.md`

It does not authorize the stepper-terminal-profile test, `semantic_component_mutations.py`, or any other product-code/test/workstream paths. Once this continuity refresh has been published and verified, that documentation slot is released; do not reuse it for further changes.

At this prompt's preparation, the published baseline was `7d4fc6c0378ffd4de455c8db05dcd636034711c1`. That is the pre-refresh baseline, not a substitute for rechecking the live state on startup.

## Local worktree preservation

At preflight, the shared index was empty. The Board handoff already had an unstaged section 35 source-note addition about the V1.0 manual and issue #25, separate from the continuity changes in section 36. That addition is intentionally not part of this refresh's staged handoff content; preserve it unstaged unless Planning grants a separate scope.

Other worktree changes were present, including Research handoff/prompt edits, Routing/canvas and graphics edits, `semantic_component_mutations.py`, `store.py`, routing and functional-interface tests, the untracked stepper-terminal-profile test, other workstream replacement prompts, a connection-wire-color test, and a machine fixture. Recheck exact status on each resume and preserve all paths not explicitly authorized.

## Next action on resumption

Check the latest Planning coordination message and actual published baseline. Do not stage or publish the stepper-terminal-profile test while its required implementation symbol is unpublished. Wait for #4's verified publication, then follow Planning's separate Board-slot decision. Keep contact-6 **UNRESOLVED** unless new revision-qualified electrical evidence resolves it.
