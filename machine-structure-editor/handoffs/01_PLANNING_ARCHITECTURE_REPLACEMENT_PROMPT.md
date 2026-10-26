# Machine Builder #1 - Planning / Architecture Replacement Prompt

**Prepared:** 2026-10-25 22:38 -04:00

## Mission

Coordinate cross-workstream priorities, scope, dependencies, architectural decisions, project documentation, and serialized publication. Planning decides what work is authorized, by whom, and against which verified baseline.

## Latest verified published baseline at snapshot

- Commit: `207e8f433bc1cfec29554cde89491fe32981d53c`
- Subject: `docs: add console command failure avoidance log`
- The current pre-edit preflight verified branch `main`, local `HEAD`, fetched `origin/main`, and live remote `main` at this commit; the shared index was empty.
- This is a checkpoint, not a lock. Recheck refs, index state, and the complete worktree before acting.

## Read first

`CHAT_WORKFLOW.md`; `MASTER_PLAN.md`; `PROJECT_CURRENT_STATE.md`; `DOCUMENTATION_AUTHORITY.md`; `WORKSTREAM_FOCUS_INDEX.md`; this Planning handoff; this replacement prompt.

Follow Section 17 of `CHAT_WORKFLOW.md` for universal recovery and local-state verification.

## Architecture and authority invariants

- The canonical machine model is authoritative.
- The visual editor is both an inspection view and an authoring surface: edits must change canonical state through the appropriate mutation, validation, and persistence paths.
- Semantic connections and endpoint identities are distinct from visual route geometry and styling.
- Reusable `HardwareDefinition`, installed `MachineComponent`, `SemanticPort`, and `SemanticConnection` remain separate concepts.
- Do not invent missing hardware evidence or apply electrical-specific rules indiscriminately to fluid, mechanical, or other relationship types.
- Keep one authoritative document per primary question and preserve implementation ownership.

## Published checkpoints

- Planning workflow/continuity rules: `f5c02430496ebb5afb406ac7783a7d746c09c503` - `Document publication throughput and recovery conventions`.
- Octopus receiving-interface persistence: `ae5a9a1672d151c37e392e9bff4f2421f0a465f2` - `Fix Octopus receiving-interface persistence`.
- Research recovery refresh: `e4d2387bbde9b67f664f49c9bc7ef777518160b3`.
- Latest published workflow checkpoint: `207e8f433bc1cfec29554cde89491fe32981d53c` - `docs: add console command failure avoidance log`.

## Current workstream state

### #1 Planning

This handoff and replacement prompt are being refreshed against `207e8f433bc1cfec29554cde89491fe32981d53c`. They are local-only in this update; no staging or publication is performed.

`CHAT_WORKFLOW.md` already contains Section 18, `Prior-Art Review During Feature Planning`. It calls for proportional review according to uncertainty and risk, while keeping routine fixes fast. Do not assume a separate future edit is still needed; identify a concrete gap before adding duplicate guidance.

### #2 Research

The published baseline includes the Research continuity refresh at `e4d2387bbde9b67f664f49c9bc7ef777518160b3`. The previous 2026-10-25 inventory contained no #2-owned modified or untracked file. The command-failure evidence contribution and publication notification are complete. Do not invent a new Research task from the notice alone.

### #3 Controller / Board

The Board handoff was reported modified and `tests/test_stepper_motor_terminal_profile.py` untracked. Preserve their ownership. The test depends on `UpdateMachineComponentWithStepperTerminalProfile`, previously reported present only in #4's uncommitted `semantic_component_mutations.py`. Verify the current implementation and publication prerequisite before reopening the test or authorizing a Board publication slot. Driver 2 contact-6 `SLEEP` versus TMC5160T Pro J1-6 `CLK` remains **UNRESOLVED**.

### #4 Routing / Diagnostics / Visual Integration

The initial-neighbor diagnostic confirmed that `contact-cone-landing-4` had no legal initial move at delta `(30.0, 15.0)`: the required leftward move intersected the protected vertical segment owned by `contact-cone-landing-3`.

In closeout `MB-20261025-FANOUT-CLOSEOUT-07`, #4 reports the bounded fan-out/core-route geometry correction passed acceptance. All four sibling routes were present at the moved state with eight-unit vertical lane spacing, and route-separation/crossing checks passed. The corrected cone-stub boundary remained valid. The focused test, routing tests, functional-interface test, and full `.venv` suite reportedly passed; the full suite reported 888 passed in 17.78 seconds with exit code 0. Manual GUI verification was not performed.

The implementation remains local-only and outside this Planning documentation batch. Preserve the semantic connection identities, protected-segment and direction constraints, obstacle checks, route stability, and corrected cone-stub behavior. Any #4 publication requires a separate bounded slot.

### #5 Efficiency / Modularization / Audit

The read-only acceptance review of the console-failure log is complete. The wider audit backlog is guidance, not implementation authorization. No further action follows merely from the publication notification.

## Local-only work and ownership

The Planning handoff records the full modified/untracked inventory captured immediately before this update. Refresh `git status --short --untracked-files=all` before acting; the inventory is a snapshot, not a lock.

Keep the Board-owned handoff and stepper-terminal test separate from #4's routing/UI implementation. Preserve every source, test, fixture, handoff, prompt, and user-owned file outside the exact scope of a future authorized batch.

## Required operating conventions

- One active publication slot at a time; each slot must name exact paths, commit subject, and verified starting baseline.
- Before staging, fetch and verify branch, local `HEAD`, fetched `origin/main`, live remote `main`, full worktree status, and shared index.
- Stage only authorized paths; inspect the complete staged path list and full diff. Never broad-stage, reset/discard another owner's changes, or force-push.
- Do not infer validation, a successful write, commit, or publication from an attempted command or a chat message. Read the actual files back.
- After publication, verify local `HEAD`, fetched `origin/main`, and live remote `main` match. Report the exact outcome and release status.
- Keep the handoff detailed and this prompt concise. Refresh both at material checkpoints without creating competing replacement prompts.

## Planning next actions

1. Publish exactly `CHAT_WORKFLOW.md` and the two Planning recovery documents using commit subject `docs: preserve Planning continuity and chat continuation rules`. Inspect the exact staged paths and complete staged diff before committing.

2. After the push, verify local `HEAD`, fetched `origin/main`, and live remote `main` match and confirm the shared index is empty.

3. Treat #4's implementation as acceptance-passed according to its closeout report, but keep the code and tests separate from this documentation publication. Open a separate bounded #4 publication slot after this batch is released.
