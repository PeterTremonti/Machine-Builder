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

## Preferred file-edit workflow

For Machine Builder implementation changes, prefer complete-file replacements when practical.

When providing a file replacement:

* give the exact repository-relative path
* give the complete intended file contents
* provide a PowerShell command that replaces the file
* avoid requiring manual surgery through a large source file

Small focused PowerShell patches remain acceptable when a complete replacement would create unnecessary risk or excessive output.

The developer's local file and test result remain authoritative after the replacement.

## Tool-use guidance

For ordinary implementation work, prefer:

* normal reasoning
* repository inspection based on user-provided local results
* GitHub/web inspection when genuinely useful
* complete-file PowerShell replacements when practical
* focused PowerShell commands for source inspection
* developer-run pytest
* developer-run GUI validation

### Python / Jupyter / Data Analysis

Do not use Python, Jupyter, ChatGPT Data Analysis, or similar data-analysis execution for ordinary Machine Builder implementation or routing work unless:

* the user explicitly requests it, or
* the task genuinely cannot be completed without it.

For the Machine Builder 4.4 routing investigation, Python/Jupyter/Data Analysis is intentionally prohibited so that the effect of those tools on cross-chat usage-limit behavior can be observed separately.

Use the developer's local PowerShell, pytest, and GUI output instead.

### GitHub / web access

GitHub and web access remain explicitly allowed.

Do not avoid GitHub searches or committed-remote repository inspection merely because the project is avoiding Python/Jupyter.

GitHub/web access may be used when:

* current committed repository state is useful
* a source file must be inspected remotely
* external documentation or research is genuinely relevant
* a current external fact needs verification

GitHub/web access is not a substitute for the developer's local working tree when current uncommitted state matters.

### Other tools

Avoid unnecessary use of:

* python_user_visible
* container/sandbox execution
* File Library/file-analysis workflows
* unnecessary tool orchestration

These tools are not inherently unavailable. They are simply not the normal path for Machine Builder implementation work.

## Change/checkpoint cadence

Keep changes focused.

Aim for a GitHub checkpoint after approximately 5–10 meaningful file modifications, or sooner at a natural milestone.

Do not make a tiny commit for every experiment.

Do not wait until a large investigation or conversation is nearly exhausted before checkpointing important progress.

At a checkpoint, make the repository itself contain enough documentation for the next coding chat to resume without reconstructing everything from conversation history.

Smaller checkpoints are preferred when a long investigation is becoming difficult to carry safely across chats.

## Testing authority

The user's locally reported pytest result is authoritative for the current local working tree.

The assistant must not claim tests passed unless the developer has actually run them and supplied the result.

A post-test pytest cleanup warning on Windows is not itself a test failure when the test suite has already reported all tests passing.

## Routing investigation

Routing Debug Mode intentionally bypasses normal route-stability history. It is useful for examining raw deterministic routing, but it is not equivalent to normal mode when evaluating hysteresis or route stability.

Do not change routing constants merely to suppress a route transition until the reason for that transition is understood.

Do not increase ROUTE_STABILITY_COST_TOLERANCE merely to hide a transition whose underlying cause is still unexplained.

During incremental-routing experiments, distinguish:

* route geometry changes: the same basic topology/corridor remains while coordinates move
* route topology changes: the sequence of corridor directions/elbows/sides changes

A small geometric movement should not automatically be treated as evidence that a topology change is desirable.

## Recovery when a chat approaches a usage/context limit

If a coding chat approaches a usage or context limit:

1. Stop expanding the investigation unnecessarily.
2. Update the current implementation handoff/state document.
3. Ensure meaningful local work is tested.
4. Commit and push an appropriate checkpoint.
5. Start the next coder chat from the repository state.

The next chat should establish its state from the repository before relying on historical conversation details.

If a tool-specific usage limit appears to affect one conversation while another conversation remains usable, do not assume the limit is conversation-local. Record the observed behavior and continue the implementation using text-only/local workflows where practical.

## Machine Builder documentation boundaries

Do not reopen settled V0.2 ontology/architecture decisions merely because an implementation detail raises an interesting idea.

Genuine semantic or architectural issues should be reported back to the appropriate Research chat rather than silently changing the implementation architecture.

## Current implementation handoff

The primary implementation handoff is:

`machine-structure-editor/handoffs/V0.2_VISUAL_EDITOR_IMPLEMENTATION_HANDOFF.md`

The active routing investigation handoff is:

`machine-structure-editor/handoffs/ROUTING_STABILITY_INVESTIGATION_HANDOFF_4.4.md`

The previous 4.3 routing handoff remains historical context.

## Research / implementation / visual-editor coordination

Keep the implementation chat focused on implementation.

Routing diagnostics, hysteresis, route selection, endpoint escape behavior, incremental route continuity, and similar routing mechanisms are visual/presentation/runtime concerns.

They must not be promoted into the canonical semantic machine model merely because implementation work exposes an interesting idea.

Genuine semantic or architectural questions should be reported to the appropriate Research chat.

The implementation roadmap's modularity rules remain in force:

* small cohesive modules
* low coupling
* smallest reasonable changes
* clear subsystem boundaries
* normal refactoring when justified
* focused tests
* focused commits

Repeated implementation friction may be architectural evidence, but should not automatically trigger a broad refactor.

The current visual-editor canvas architecture is already split into focused modules. Do not move behavior back into a monolithic canvas implementation.
