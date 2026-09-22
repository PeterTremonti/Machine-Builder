# Machine Builder Coding Chat Workflow

This file records the preferred workflow for Machine Builder implementation chats.

## Authoritative repository state

The authoritative working repository is the developer's local Windows checkout:

`machine-structure-editor`

The assistant does not have direct access to that Windows working tree unless a tool explicitly provides such access.

Do not assume that GitHub contains uncommitted local changes.

Use:

- local PowerShell output for current working-tree state
- GitHub for committed/pushed remote state
- the repository's tests as the implementation authority

## Tool-use rules

For implementation work, prefer:

1. Complete PowerShell patches supplied by the assistant.
2. The developer runs those patches locally.
3. The developer runs `python -m pytest`.
4. The developer reports the actual result.
5. The assistant analyzes that result and supplies the next focused change.

Do not treat these as substitutes for the developer's local repository:

- Python execution environments
- `python_user_visible`
- container/sandbox shells
- File Library/search results
- web access to GitHub

Do not claim that local files were edited, local tests were run, or commits were created unless the developer provides the actual result or a tool explicitly demonstrates that operation.

## Chat/tool-limit caution

This project should avoid unnecessary use of Advanced Data Analysis and other limited tools during long coding sessions.

In particular, avoid using:

- Python for repository analysis or editing
- `python_user_visible`
- spreadsheet/data-analysis workflows
- unnecessary file-analysis/upload workflows
- unnecessary tool orchestration

Use web access only when current external information or verification is actually required.

The local implementation workflow should remain primarily text + PowerShell + developer-run pytest.

## Change cadence

Keep implementation changes focused.

After roughly 5–10 meaningful file modifications, or at a meaningful implementation milestone:

1. run the relevant focused tests
2. run the full test suite
3. update documentation/handoff state when appropriate
4. commit and push the checkpoint

Do not create a tiny commit for every experimental test.

Do not wait until a very large investigation has accumulated before creating a checkpoint.

## Routing investigation rule

Routing experiments should preserve the distinction between:

- normal route-stability behavior
- raw/debug routing behavior

Routing Debug Mode intentionally bypasses the normal stability history and therefore should not be treated as equivalent to normal-mode behavior when evaluating hysteresis or route stability.

## Recovery rule

If a coding chat approaches its usage or context limit, stop expanding the investigation and create a clean repository checkpoint and handoff.

The next coding chat should begin by checking:

- current branch
- git status
- current tests
- current handoff/state documentation
- latest pushed commit

Do not reconstruct repository state from conversation history when the repository itself can provide it.
