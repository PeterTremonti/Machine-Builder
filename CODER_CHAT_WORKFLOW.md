# Machine Builder Coding Chat Workflow

This document defines the preferred workflow for Machine Builder implementation/coder chats.

## Authoritative current state

The local Windows repository and user-reported local test results are authoritative for current implementation state.

GitHub branches and commits are authoritative for committed remote state only.

Do not assume that GitHub contains uncommitted local changes.

The assistant does not have direct access to the developer's Windows working tree unless a tool explicitly provides such access.

## Normal implementation workflow

The preferred implementation loop is:

1. Inspect the current local/reported repository state.
2. Make one focused change.
3. Run the focused tests.
4. Run the full test suite at meaningful checkpoints.
5. Validate the GUI when the change affects visual behavior.
6. Update the relevant README/handoff/state documentation.
7. Commit and push at a meaningful checkpoint.

The developer applies code changes locally through PowerShell and reports the actual result.

Do not claim that local files were edited, local tests were run, commits were made, or changes were pushed unless the developer provides the actual result or an available tool demonstrably performs that operation.

## Tool-use guidance

For ordinary implementation work, prefer:

- normal reasoning
- repository inspection based on user-provided local results
- complete PowerShell patches
- developer-run pytest

Avoid unnecessary use of:

- Python/data-analysis workflows
- python_user_visible
- container/sandbox execution
- File Library/file-analysis workflows
- unnecessary tool orchestration

These tools are not inherently bad or unavailable. Avoid them because ordinary Machine Builder implementation work does not normally require them, and long coding sessions have previously encountered separate usage limits for chats involving data analysis.

Use web/GitHub access when current committed remote state or genuinely current external information is required. Do not use it as a substitute for the user's local working tree.

## Change/checkpoint cadence

Keep changes focused.

Aim for a GitHub checkpoint after approximately 5–10 meaningful file modifications, or sooner at a natural milestone.

Do not make a tiny commit for every experiment.

Do not wait until a large investigation or conversation is nearly exhausted before checkpointing important progress.

At a checkpoint, make the repository itself contain enough documentation for the next coding chat to resume without reconstructing everything from conversation history.

## Testing authority

The user's locally reported pytest result is authoritative for the current local working tree.

The assistant must not claim tests passed unless the developer has actually run them and supplied the result.

A post-test pytest cleanup warning on Windows is not itself a test failure when the test suite has already reported all tests passing.

## Routing investigation

Routing Debug Mode intentionally bypasses normal route-stability history. It is useful for examining raw deterministic routing, but it is not equivalent to normal mode when evaluating hysteresis or route stability.

Do not change routing constants merely to suppress a route transition until the reason for that transition is understood.

## Recovery when a chat approaches a usage/context limit

If a coding chat approaches a usage or context limit:

1. Stop expanding the investigation unnecessarily.
2. Update the current implementation handoff/state document.
3. Ensure meaningful local work is tested.
4. Commit and push an appropriate checkpoint.
5. Start the next coder chat from the repository state.

The next chat should establish its state from the repository before relying on historical conversation details.

## Machine Builder documentation boundaries

Do not reopen settled V0.2 ontology/architecture decisions merely because an implementation detail raises an interesting idea.

Genuine semantic or architectural issues should be reported back to the appropriate Research chat rather than silently changing the implementation architecture.

## Current implementation handoff

The primary implementation handoff is:

`machine-structure-editor/handoffs/V0.2_VISUAL_EDITOR_IMPLEMENTATION_HANDOFF.md`

The current routing investigation has a more specific handoff:

`machine-structure-editor/handoffs/ROUTING_STABILITY_INVESTIGATION_HANDOFF_4.3.md`

## Research / implementation / visual-editor coordination

Keep the implementation chat focused on implementation.

Routing diagnostics, hysteresis, route selection, endpoint escape behavior,
and similar routing mechanisms are visual/presentation/runtime concerns.
They must not be promoted into the canonical semantic machine model merely
because implementation work exposes an interesting idea.

Genuine semantic or architectural questions should be reported to the
appropriate Research chat.

The implementation roadmap's modularity rules remain in force:

- small cohesive modules
- low coupling
- smallest reasonable changes
- clear subsystem boundaries
- normal refactoring when justified
- focused tests
- focused commits
- repeated implementation friction may be architectural evidence

The current visual-editor canvas architecture is already split into focused
modules. Do not move behavior back into a monolithic canvas implementation.

