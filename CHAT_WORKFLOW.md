# Machine Builder — Chat Workflow

## 1. Purpose

This document defines how the ChatGPT workstreams used for Machine Builder operate, recover from chat-length limits, interact with the shared repository, and communicate discoveries.

The purpose is to make the project durable across replacement chats.

Conversation history is not the project's permanent memory.

The durable project memory is:

```text
MASTER_PLAN.md
PROJECT_CURRENT_STATE.md
CHAT_WORKFLOW.md
workstream handoffs
source/documentation files
the repository itself
```

---

# 2. Current Workstreams

The project currently uses these workstream roles:

```text
01 — Planning / Architecture
02 — Research / Architecture
03 — Controller / Board
04 — Routing / Diagnostics
05 — Efficiency / Modularization
```

Chat-instance suffixes such as `3.1`, `3.2`, `3.3`, `4.1`, etc. are organizational labels for the user's ChatGPT conversation list.

They identify replacement instances of the same workstream.

They do not represent repository branches, software versions, architecture identifiers, or separate projects.

---

# 3. Document Ownership

Each document has a primary owner.

```text
MASTER_PLAN.md
    → Planning / Architecture (#1)

PROJECT_CURRENT_STATE.md
    → Planning / Architecture (#1)

CHAT_WORKFLOW.md
    → Project-wide workflow rules

01 Planning handoff
    → Planning / Architecture (#1)

02 Research handoff
    → Research / Architecture (#2)

03 Board handoff
    → Controller / Board (#3)

04 Routing handoff
    → Routing / Diagnostics (#4)

05 Efficiency handoff
    → Efficiency / Modularization (#5)
```

A workstream should not silently rewrite another workstream's handoff.

---

# 4. Repository Authority

The current shared repository uses one active branch:

```text
main
```

There should be one normal shared working checkout.

The project does not use parallel WIP branches/worktrees as the normal chat workflow.

For current implementation facts, use this authority order:

```text
Current repository / current main
        >
current tests
        >
workstream handoff
        >
PROJECT_CURRENT_STATE.md
        >
MASTER_PLAN.md
        >
conversation memory
```

This ordering is intentional.

A handoff can explain why something exists.

The repository and tests determine what actually exists.

---

# 5. Repository State Must Be Verified

A chat must not assume that a remembered commit, line number, test count, or file contents are current.

Before making an implementation decision, inspect the current repository when practical.

At minimum, implementation work should be reconciled against:

```text
current main
current file contents
current tests
current relevant handoff
```

A raw GitHub URL may help locate a file, but it is not sufficient evidence that the chat has the current contents.

GitHub/connected-repository retrieval may expose stale or previously retrieved content.

When current contents matter, use the actual current checkout or have the user provide the current file contents.

---

# 6. No Chat-Owned Repository Editing Through Artifacts

For these workstreams, the user maintains the local repository.

Chats should not:

* create file artifacts for repository files
* attach generated repository replacements as files
* upload repository files into chat storage
* silently modify repository files through file-management systems
* use Python merely to manufacture repository files

Instead, provide the user with exact paste-ready text or commands.

The user will make the local repository change.

---

# 7. Python / Tool Use

The user prefers to perform repository changes through VS Code / PowerShell rather than through Python-generated artifacts.

Do not use Python when a normal command, source inspection, or paste-ready replacement is sufficient.

Use the simplest practical inspection method.

Do not introduce tool complexity merely for convenience.

---

# 8. Full-File Replacement Preference

When modifying a reasonably sized file, prefer:

```text
FULL FILE REPLACEMENT
```

over surgical editing.

The goal is to minimize user error and avoid requiring the user to reconstruct a file from scattered fragments.

Surgical edits are acceptable when a full replacement is impractical or unnecessarily large.

Repeated surgical editing of the same large file is a signal that its modularity should be reconsidered.

---

# 9. Required Surgical Edit Format

Whenever a surgical edit is required, provide:

```text
REPOSITORY CHANGE REQUIRED

File:
exact repository path

Action:
EDIT EXISTING FILE

Repository state inspected:
branch
commit

Location:
exact line range

Anchor:
exact nearby class / function / text

Plain-language description:
what this code is doing and what the user should look for

Change:
complete paste-ready replacement or insertion
```

Do not give instructions such as:

> "Add this to the port loop."

unless the loop is also identified precisely.

The user is not expected to know programming terminology.

Explain enough of the surrounding code to make the location unambiguous.

---

# 10. Multiple Surgical Edits

When several surgical edits are required in the same file:

Prefer applying edits from the highest line number to the lowest line number.

Example:

```text
Edit 2
Lines 700–720

Edit 1
Lines 300–330
```

This prevents an earlier edit from shifting the line numbers needed by a later edit.

If edits must be performed in another order, explicitly state that the later line numbers have changed and provide the updated locations.

Every edit must also have an exact textual anchor.

If the cited line range or anchor does not exist in the user's checkout:

```text
STOP
```

Do not guess.

The file should be re-inspected because the chat may be working from an older version.

---

# 11. File Size and Modularity

Approximately 1,000 lines is a useful review trigger, not a hard maximum.

A file around or above that size should prompt the question:

> Does this file still represent one cohesive responsibility?

Consider:

* responsibility boundaries
* dependency direction
* coupling
* testability
* readability
* reuse
* ownership
* whether several independent responsibilities are accumulating

Do not split files solely to satisfy a line-count number.

Chat 05 is responsible for periodically identifying possible modularity/code-health concerns.

The workstream that owns the code decides how a refactor should actually be performed.

---

# 12. Code Documentation

Important source modules, classes, and public functions should have useful documentation describing their purpose and important non-obvious behavior.

Documentation should be added incrementally when code is created or meaningfully modified.

Do not stop current development solely to document every historical file.

A future code-health review may identify documentation gaps.

Useful module documentation should explain the module's responsibility.

Useful function/class documentation should explain purpose and important invariants when those are not obvious from the code.

---

# 13. README Maintenance

`README.md` is the project's orientation document.

Update it when a change would cause a new developer or replacement chat to start in the wrong place.

Typical triggers include:

* project purpose changes
* new workstream structure
* new authoritative starting documents
* renamed or replaced handoffs
* major repository-layout changes
* changes to startup/recovery instructions
* major milestones that change what "where to start" means

Do not update README for every commit or test-count change.

---

# 14. Generated Repository Tree

`recursive_git_tree.txt` is a generated path index.

It should be regenerated when the repository structure changes materially, including:

* new files
* deleted files
* moved files
* renamed files
* major directory changes

It does not need regeneration for ordinary edits inside existing files.

It is a navigation aid, not a source of truth for file contents.

---

# 15. Testing and Checkpoints

Meaningful implementation checkpoints should report the actual verification result.

For example:

```text
Checkpoint 32
Workstream: Controller / Board
Chat instance: 3.1
Date/time: 2026-10-03 00:10 EDT
Commit: abc1234
Tests: 756 passed
```

The timestamp should use the project/user local timezone.

A checkpoint should describe:

```text
What changed
Why it matters
What was verified
Architectural interpretation
Decisions / classifications
Unresolved questions
Next action
```

Test counts from different dates should not be compared as though they were simultaneous.

Checkpoint timestamps are part of the project's timeline integrity.

A meaningful checkpoint should record the local project/user date and time, including timezone, at the time the checkpoint is established or verified.

When a checkpoint records a repository commit, the checkpoint timestamp describes when that repository state was verified for the checkpoint. It is not merely the date on which the handoff text was later copied or edited.

Use the timestamp to interpret repository chronology:

- a commit that predates the checkpoint timestamp may legitimately lack changes described by that checkpoint;
- a later commit may include the checkpoint changes or supersede them;
- an apparently older commit should not be treated as evidence against a newer timestamped checkpoint without checking repository history;
- when chronology is ambiguous, inspect Git history and the actual current checkout rather than guessing.

Git commit dates and handoff checkpoint timestamps should therefore be treated as related evidence, not interchangeable fields.


The later checkpoint supersedes the earlier test count as the newer state, unless the repository history shows otherwise.

---

# 16. Handoff Structure

Living workstream handoffs should maintain:

```text
Recovery Instructions
Current State
Next Action
What We've Done So Far
Decisions / Classifications
Important Files
Research Context
Unresolved Issues
Latest Test State
```

Handoff Formatting Integrity

Living handoffs must remain valid, readable Markdown.

Use normal Markdown structure for durable documents:

- headings use Markdown heading markers such as `#`, `##`, or `###`;
- do not simulate headings by wrapping the heading itself in bold text;
- horizontal rules use a standalone `---` line;
- fenced code blocks must have matching opening and closing fences;
- do not leave a code fence open across unrelated prose or the rest of the document;
- executable PowerShell must not be mixed into surrounding explanatory prose;
- runnable commands intended for the user must follow the Copy/Paste Command Formatting Safety rules in `CHAT_WORKFLOW.md`;
- checkpoint sections should use a clear heading, local date/time with timezone, and structured checkpoint content;
- preserve the established handoff section order and do not move historical checkpoints into the current `Next Action` section.

When creating or editing a handoff, inspect the rendered structure or the raw Markdown as appropriate and verify that headings, separators, lists, quotations, and code blocks remain syntactically complete.

A formatting problem in one part of a handoff must not be allowed to turn the remainder of the document into accidental code, ordinary chat text, or other unintended Markdown structure.

Chronological checkpoints belong in the history section.

Do not insert new checkpoints around a separate `Next Action` section.

The current `Next Action` is a current-state field.

Historical checkpoints should be appended chronologically.

Full-file replacement is preferred when updating a reasonably sized handoff.

---

# 17. Workstream Recovery

When a chat reaches its conversation-length limit:

```text
Replacement chat
        ↓
Read CHAT_WORKFLOW.md
        ↓
Read MASTER_PLAN.md
        ↓
Read PROJECT_CURRENT_STATE.md
        ↓
Read the workstream handoff
        ↓
Inspect current repository state
        ↓
Continue from current Next Action
```

Do not reconstruct the workstream from memory if the handoff contains the needed information.

Do not assume the latest remembered test result is current.

Do not assume an old line number is still valid.

---

# 18. Planning / Architecture (#1)

Chat 01 owns:

* long-term architecture
* Master Plan
* project-wide current state
* cross-workstream coordination
* durable architectural decisions
* future ideas
* deferred problems
* deciding whether implementation findings change project architecture

Chat 01 should not independently rewrite implementation-owned handoffs.

---

# 19. Research / Architecture (#2)

Chat 02 owns:

* research continuity
* standards
* terminology
* manufacturer documentation
* CAD/system precedent
* engineering practices
* external technical evidence
* source provenance
* research conclusions
* unresolved research questions

Important sources should preserve:

```text
source
document/version
URL or location
date accessed
relevant section/page
what it establishes
what it does not establish
Machine Builder implication
```

Do not invent missing citations.

---

# 20. Controller / Board (#3)

Chat 03 owns:

* board implementation
* hardware definitions
* controller physical interfaces
* controller resources
* board-related fixtures/tests
* physical interface experiments
* Board workstream handoff

Board implementation should preserve the established semantic distinctions and should not introduce new canonical entities without concrete evidence.

---

# 21. Routing / Diagnostics (#4)

Chat 04 owns:

* routing implementation
* route diagnostics
* topology/geometry investigation
* routing tests
* routing-specific implementation experiments
* Routing workstream handoff

Routing behavior should not silently redefine canonical machine semantics.

---

# 22. Efficiency / Modularization (#5)

Chat 05 is primarily an inspection and recommendation workstream.

It may inspect:

* file size
* module responsibility
* dependencies
* duplication
* coupling
* documentation gaps
* test organization
* architectural/code-health smells

By default, Chat 05 should not independently rewrite code owned by another workstream.

Its normal output is:

```text
problem identified
        ↓
evidence
        ↓
dependency / impact analysis
        ↓
recommendation
        ↓
owning workstream performs implementation
```

Chat 05 should not become a second implementation branch.

---

# 23. Project Current State Requests

Workstreams should not independently rewrite `PROJECT_CURRENT_STATE.md`.

When a project-level discovery is important, report:

```text
PROJECT CURRENT STATE UPDATE REQUEST

Why:
...

Proposed location:
...

Proposed content:
...

Source:
...
```

Planning / Architecture decides whether and how the update is incorporated.

---

# 24. Architecture Classification

When useful, discoveries should be classified as:

```text
IMPLEMENTATION ONLY
WATCH
REINFORCE
NEW PRINCIPLE — candidate
RECONSIDER
```

A candidate principle is not automatically durable architecture.

Implementation success alone does not prove that a new canonical entity is necessary.

---

# 25. Repository Ownership

Each workstream may investigate broadly, but repository changes should respect ownership.

For a change belonging to another workstream:

```text
identify the issue
        ↓
explain the evidence
        ↓
report to the owning workstream
```

Do not silently modify another workstream's code because a change appears convenient.

---

# 26. Commit and Push Workflow

The user prefers **GitHub Desktop** for commits and pushes because it provides separate Summary and Description fields and is easier for the user's workflow.

The normal process is:

```text
workstream makes/test changes
        ↓
report actual test result
        ↓
prepare commit Summary
        ↓
prepare commit Description
        ↓
user commits in GitHub Desktop
        ↓
user pushes in GitHub Desktop
```

Chats should **not normally commit or push through console commands**.

Console-based `git commit` / `git push` should only be used when the user explicitly requests that workflow.

Every meaningful commit request should provide both:

```text
Summary:
short commit title

Description:
clear explanation of what changed,
why it changed,
what was verified,
and any important architectural constraint preserved
```

A chat must not omit the Description when a meaningful commit is being requested.

The user should not have to invent or reconstruct the commit description.

GitHub Desktop remains the preferred commit/push mechanism even when the workstream used PowerShell for inspection or testing.

---

# 27. Source and Documentation Checkpoint

A meaningful documentation change should normally be grouped into a coherent documentation checkpoint rather than committed one tiny edit at a time.

When repository structure changes:

```text
documentation/files finalized
        ↓
references checked
        ↓
recursive_git_tree.txt regenerated
        ↓
diff inspected
        ↓
cohesive commit
        ↓
push
```

The generated tree should describe the committed repository structure.

Historical documents should be retained until their contents and references have been reviewed.

---

# 28. README / Master Plan / Current State Boundaries

Use these documents for different purposes:

```text
MASTER_PLAN.md
    = long-term direction, major plan, future ideas

PROJECT_CURRENT_STATE.md
    = current project-wide status, active direction, open questions

README.md
    = project orientation and where to start

CHAT_WORKFLOW.md
    = how the chats operate

workstream handoffs
    = detailed continuity for each workstream
```

No document should silently become a replacement for another document's role.

---

# 29. Recovery From Stale Repository Information

If a chat discovers that its remembered or retrieved repository state is older than the current shared `main` state:

1. Stop relying on the stale information.
2. Identify the current commit.
3. Inspect the current file(s).
4. Reconcile the handoff against the current repository.
5. Continue only from the current state.

A raw GitHub link or cached repository result must not override the actual current checkout.


When comparing a handoff or checkpoint with the current repository, consider the recorded checkpoint date/time and recorded commit together.

If the current or referenced commit predates the checkpoint timestamp, do not assume that commit contains the checkpoint's changes. Verify the relevant Git history or inspect the current checkout.

If a handoff contains a newer checkpoint timestamp but an older recorded HEAD, treat the timestamped checkpoint as the temporal record and re-resolve the actual repository state before making a decision.

When chronology is uncertain, report the uncertainty rather than silently choosing the older or newer value.

---

# 30. User Workflow Preference

The standard PowerShell working directory for all Machine Builder chats is:

`C:\Users\Peter\Documents\GitHub\Machine-Builder`

Chats should assume the terminal starts at the repository root and should not unnecessarily change the current directory. When a command temporarily requires a subdirectory, it should leave the terminal at the repository root when the command sequence is complete.

The user prefers:

* exact PowerShell commands
* clear sequential steps
* full-file replacements where practical
* exact file paths
* exact line numbers for surgical edits
* exact anchors for surgical edits
* plain-language descriptions of technical locations
* minimal Git complexity
* no unnecessary file artifacts
* concise but complete explanations

The user is not expected to know programming terminology.

The workflow should make repository work understandable and mechanically actionable without requiring programming expertise.

---

# 31. Recovery Principle

The objective of this workflow is simple:

> A chat can end without the work ending.

Every important idea, decision, research result, implementation checkpoint, and future problem should have a durable home outside conversation memory.

The repository and project documentation are the project's long-term memory.

---

# 32. Cross-Workstream File Ownership

Workstream-specific implementation files have one owning workstream.

Shared implementation, infrastructure, and canonical-model files also have one explicit owner, even when multiple workstreams depend on them.

Ownership is determined by responsibility, not by the number of workstreams that consume a file.

Workstreams should interact through agreed canonical model types, interfaces, identifiers, and other stable contracts rather than sharing implementation ownership.

When a workstream needs a change to a file outside its ownership:

1. Report the requirement to Planning / Architecture;
2. Planning determines whether the change is warranted;
3. Planning delegates the implementation to the owning workstream;
4. the owning workstream performs and tests the change;
5. dependent workstreams consume the resulting shared contract or implementation.

Changes affecting a shared canonical contract or semantic boundary require Planning / Architecture review before implementation.

The preferred default pattern is:

    Board-owned implementation
            |
    shared canonical contract
            |
    Routing-owned implementation

This is the project's default shared contract, separate implementation ownership model.

---

# 33. Machine Builder Tooling and Repository Editing Safety

The following are hard operating constraints for all Machine Builder workstreams, including Planning itself.

## Repository inspection and implementation tooling

For ordinary repository inspection, source mining, implementation, testing, visual-editor work, routing work, and architecture/audit work, do not use:

- Python
- Jupyter
- pandas
- dataframes
- data-analysis workflows
- generated notebooks
- temporary analysis scripts
- temporary analysis files or artifacts
- spreadsheet-style data-analysis workflows

Use instead:

- PowerShell / terminal
- git
- direct repository/source inspection
- existing project tooling
- project tests

The presence of JSON, configuration files, firmware sources, hardware inventories, or large source trees does not by itself make a task a data-analysis task.

Do not create analysis artifacts merely to inspect or transform repository content.

If an exceptional task genuinely requires another tool, identify the concrete reason first and keep that work isolated from the implementation repository.

## Safe tracked-file editing

For small edits to tracked repository text files:

1. Prefer a small git apply patch when practical.
2. When PowerShell string editing is appropriate, explicitly decode and encode UTF-8.
3. Do not rely on PowerShell's implicit/default text encoding for repository files.
4. Guard replacements so they fail when the expected source block is missing.
5. Also fail when a supposedly unique source block occurs more than once.
6. Preserve existing line endings rather than normalizing the entire file unnecessarily.
7. After editing, run git diff --check.
8. Inspect the relevant git diff.
9. Run focused tests before broader testing at the appropriate checkpoint.

The repository currently uses Git text normalization with * text=auto and Windows core.autocrlf=true. CRLF in the Windows working tree is acceptable; accidental transcoding of UTF-8 source text is not.

New or deliberately rewritten text files should use UTF-8 without BOM unless an existing historical file has a documented reason to retain another encoding.

## Copy/Paste Command Formatting Safety

Runnable PowerShell commands intended for the user must be delivered as one continuous copy/paste block.

Do not place Markdown fences inside a PowerShell copy/paste block.

Do not place explanatory prose such as Then, Next, or Run this inside the executable command block.

Do not place a language marker such as powershell inside the executable command block.
The opening Markdown fence for an executable PowerShell block must use the plain powershell language-marker fence with no id= attribute, HTML attribute, title, or other metadata. Do not add metadata to executable command fences.

When a command must contain multi-line Markdown or other literal text, use a PowerShell here-string or another representation that does not introduce nested Markdown fences into the outer response formatting.

The entire executable sequence should begin with the first command and end with the final reporting command. Any explanation belongs outside that block.

Before giving a path-sensitive command, either state the required starting directory or resolve the repository root inside the command itself.

After a command block is supplied, the user should be able to copy the block verbatim without having to remove Markdown, prose, or formatting markers.

This requirement applies to all workstreams and all repository operations, including read-only inspection commands.

## Paste-Ready PowerShell Safety Refinement

For repository commands intended to be copied directly from chat into PowerShell:

- Prefer simple statements and natural PowerShell line breaks over unnecessarily complex expression construction.
- Multiline parenthesized expressions are valid PowerShell and are not prohibited, but do not use them when a simpler expression is clearer.
- Do not use backtick line continuation unless there is no clearer alternative. A trailing space after a backtick breaks continuation and can be difficult to see.
- Use single-quoted here-strings for substantial literal source text or multiline replacement text. Keep the here-string delimiters syntactically exact.
- Keep discovery, validation, modification, and testing as distinct steps rather than embedding many operations inside one large expression.
- Validate all anchors and expected counts before writing any repository file.
- For unusually complex PowerShell, prefer a parse-only validation step before allowing the command to perform repository changes. PowerShell's parser APIs can report syntax errors without executing the script.
- Do not infer the cause of a parser error solely from a later token named in a cascade of syntax diagnostics. Inspect earlier structural syntax first.
- Embedded punctuation inside quoted literal text, such as parentheses in a Python string, should not be treated as PowerShell syntax. A diagnostic pointing at such text may be a cascade symptom.
- Do not rely on implicit text encoding when modifying repository files. Preserve the existing file encoding/line endings or explicitly use the required encoding. Windows PowerShell 5.1 and PowerShell 7 have different default encoding behavior.

Do not modify a repository source file merely to obtain diagnostic output when an existing test, direct inspection, or a non-mutating diagnostic path can provide the same evidence. Prefer the least invasive method that answers the question.

## Workstream Tooling Boundaries

Machine Builder workstreams must use the simplest appropriate text and repository tooling for their assigned responsibility.

Planning / Architecture, Research / Architecture, Controller / Board, Routing / Diagnostics, and Efficiency / Modularization / Audit workstreams must not invoke Data Analysis, Python, Jupyter, pandas, notebooks, generated analysis workflows, or temporary analysis artifacts for ordinary Machine Builder repository inspection, source inspection, planning, architecture work, documentation review, implementation review, testing, or audit.

Repository inspection and project reasoning for these workstreams should use PowerShell / terminal commands, Git, direct source and documentation inspection, and the project's existing tests and tooling.

Do not introduce Python, Jupyter, pandas, notebooks, generated analysis scripts, or analysis artifacts merely because they appear convenient for a repository task.

The absence of an appropriate data-analysis need must not be treated as a reason to invoke a data-analysis workflow.

A workstream may use another tool only when the task itself explicitly requires that tool's supported capability and the use is consistent with the workstream's ownership and project rules.

## Repository Edit Safety

When a command is intended to modify a tracked file, the operation must fail closed.

If the expected file, anchor text, occurrence count, or other stated precondition is not exactly what was expected, make no change and report the mismatch.

Prefer `git apply` for small tracked-file edits.

For other surgical text edits, use explicit UTF-8 handling and preserve the existing file's line-ending behavior where practical.

Do not perform uncontrolled `Get-Content` / `Set-Content` or equivalent read/write round-trips on tracked text files.

After every tracked-file edit, run `git diff --check`, inspect the resulting diff, and verify `git status` before proceeding.

Do not combine unrelated workstream changes in the same edit or commit.

Path-sensitive commands must resolve the repository root or explicitly establish their required starting directory.

Executable commands should avoid unnecessary non-ASCII or invisible characters unless those characters are deliberately required by the task.

# Action-Ready Work Rule

When the next action is clear and ready to execute, provide the actual command or other paste-ready instruction in the same user-visible response as the explanation.

Do not spend a response merely describing what is planned when the user is ready to run the work.

Executable PowerShell commands intended for the user must appear in the final user-visible response itself. Do not provide the only copy/pasteable version of a command through internal reasoning, tool output, commentary, hidden content, or any other channel the user may not see or may have to expand to retrieve.

When a command is required, use the project's required command-formatting rules directly in that response:
- one continuous copy/paste block;
- use a plain Markdown powershell code fence;
- do not add id=, HTML attributes, titles, or other metadata to the opening fence;
- do not put explanatory prose inside the executable block;
- do not put nested Markdown fences inside the executable block.

The expected pattern is:

What matters / why
        |
actual command or paste-ready action
        |
expected result / next checkpoint

This applies to repository inspection, testing, implementation, documentation changes, and other work where a concrete next action is already known.

The user should not have to compose commands from a plan that the chat has already determined.
