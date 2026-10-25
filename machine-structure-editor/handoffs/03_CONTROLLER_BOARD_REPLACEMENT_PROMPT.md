# Machine Builder - #3 Controller/Board Replacement Prompt

Prepared: 2026-10-24 20:03:57 -04:00 | Verified published baseline: `a4c5ad9347ae56990f9de4049b78cc3cc591e22f` - `add shared Promega specimen composer`.

## Startup and repository authority

Use the existing checkout: `C:\Users\Peter\Documents\GitHub\Machine-Builder`.

Read `CHAT_WORKFLOW.md`, `MASTER_PLAN.md`, `PROJECT_CURRENT_STATE.md`, and `machine-structure-editor/handoffs/03_CONTROLLER_BOARD_WORKSTREAM_HANDOFF.md`. Then verify branch, `HEAD`, `origin/main`, live remote `main`, `git status --short --untracked-files=all`, and `git diff --cached --name-only`. This prompt records a checkpoint; do not assume the baseline is still current.

The checkout and Git index are shared by workstreams #1-#5. Preserve other workstreams' staged, unstaged, and untracked changes. Never blanket-stage, reset, discard, stash, or unstage another workstream's work. Never force-push. Keep Board tasks within #3 ownership.

## Latest published Board implementation: Promega reference specimen composer

Published commit: `a4c5ad9347ae56990f9de4049b78cc3cc591e22f`
Subject: `add shared Promega specimen composer`
Parent: `93d94e1a7dbf0a75cd7e1a7acc814d50fb61142e`

Published paths only:
- `machine-structure-editor/src/machine_builder/promega_specimen.py`
- `machine-structure-editor/tests/test_promega_reference_specimen.py`

Planning authorization: `MB-20261024-1746-01`; API clarification: `MB-20261024-1805-02`.

The public contract is `build_promega_reference_specimen() -> EditorState`. It creates a fresh detached state via a private `MachineCanvas`, standard template/canonical mutation paths, and existing Promega fixture helpers. It does not mutate the active canvas/document.

The specimen includes 14 uniquely role-labelled components, separate X/Y cable-reference endpoints, eight XY positional-reference connections, three IR Z-probe reference connections, FAN0/FAN2 assignments, reported firmware-command evidence, and the logical Z motor resource assignment supported by `M584`. Installed SD-card verification remains `not_independently_verified`.

Do not treat this reference specimen as proof of the physical machine. Component identity, physical presence/wiring, cable/contact correspondence, motor winding, endstop behavior, and the P9/P11/H2/H4/S8/S6 crosswalk remain unresolved where not independently evidenced.

### Published validation

- Composer and test `py_compile`: exit code 0.
- `tests/test_promega_reference_specimen.py`: 5 passed in 2.08s.
- Focused eight-file Promega/Maestro regression suite: 58 passed in 2.73s.
- `git diff --check` and post-push local/remote reference convergence checks passed at implementation publication.

The living handoff Section 37 records the eight regression-test filenames.

## Prior Board milestone: Octopus persistence

Commit `ae5a9a1672d151c37e392e9bff4f2421f0a465f2`, `Fix Octopus receiving-interface persistence`, changed the Octopus receiving-interface contact map to a list of 18 position-labelled records and added save/reopen coverage. Its published focused suite reported 65 passed in 0.33s. This is separate from the later Promega composer commit.

## Electrical discrepancy - UNRESOLVED

Octopus V1.1 Driver 2 contact 6 is documented as `SLEEP` / `DRIVER2_SLP`. TMC5160T Pro V1.0 module J1-6 is documented as `CLK` (external clock input); J1-3 `SCK/CFG2` is the SPI serial clock.

Do not infer continuity, contact mating, electrical equivalence, a confirmed short, incompatibility, or the as-built jumper state from matching numbers, third-party manuals, product pairing, or issue reports. Section 35 of the living handoff contains the evidence. Keep this question **UNRESOLVED** unless revision-qualified evidence closes the circuit path.

## Current local-worktree boundary

At the initial inspection on 2026-10-24:
- Branch was `main`; `HEAD`, `origin/main`, and live remote `main` matched the composer commit.
- The shared Git index was empty.
- The #3 handoff already contained a local Section 35 manual/issue #25 research-note addition. Preserve it; this continuity refresh does not resolve the electrical question.
- The replacement prompt was clean before this refresh. Both #3 documents are expected to be locally modified afterwards.
- Routing/GUI (#4) has existing modified files across its handoff, canvas/editing/scene/UI/state modules, graphics/routing modules, `semantic_component_mutations.py`, `store.py`, and canvas/routing/functional-interface tests.
- Existing untracked #4 files include `machine-structure-editor/handoffs/04_ROUTING_STABILITY_REPLACEMENT_PROMPT.md`, `machine-structure-editor/tests/test_connection_wire_color.py`, and `machine-structure-editor/tests/test_stepper_motor_terminal_profile.py`.
- The shared fixture `machine-structure-editor/wiring test machines/Maestro and 4 port motor 4 wires J9 contact view.machine.json` is locally modified.

Recheck exact live status on every resume. Do not assume this snapshot is unchanged.

## Stepper-terminal-profile test - HOLD

`machine-structure-editor/tests/test_stepper_motor_terminal_profile.py` remains local-only. Its previously reported combined result of 34 passed in 0.20s depended on `UpdateMachineComponentWithStepperTerminalProfile` in the modified local #4-owned `machine-structure-editor/src/machine_builder/semantic_component_mutations.py`; that result did not establish a published-baseline pass.

Do not stage or publish this test or the #4 implementation. After #4 verifies publication of its dependency, recheck the shared state and follow Planning's explicit reassessment and separate Board-slot decision before resuming this test.

## Next action on resumption

1. Read the latest Planning coordination and verify the actual shared repository state.
2. Do not repeat or amend the completed Promega composer implementation.
3. Keep File-menu/UI integration with #4.
4. Keep the stepper-terminal-profile test on hold until its dependency is published and Planning reassesses.
5. Preserve the unresolved TMC5160T contact-6 disposition.
6. Planning authorized publication under `MB-20261024-2010-01` for the two continuity documents only. Keep the pre-existing Section 35 research-note/status hunk unstaged, honoring Section 36. Verify the exact staged diff, commit as `docs: refresh Promega composer continuity`, push normally, confirm ref convergence, then report `PUBLISHED — SLOT RELEASED` to Planning.
