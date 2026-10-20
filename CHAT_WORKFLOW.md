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

## 5.1 Local Checkout Execution Boundary

The Machine Builder workstream chats do not operate inside the user's local Windows repository checkout.

The local checkout is maintained and controlled by the user.

Chats must not assume they can execute PowerShell, Git, tests, or file-editing commands against the user's local checkout.

Any command intended to inspect, modify, or test the local repository must be provided to the user as a paste-ready command.

The user runs the command in the local checkout and returns the resulting output to the chat.

Chat tool access, GitHub retrieval, connected-repository content, pasted source, or Library copies must not be treated as equivalent to execution against the user's actual local checkout.

When current repository state matters, the chat must clearly distinguish between information it can inspect remotely or from supplied material and information that must be verified by the user in the local checkout.

This is a standing project workflow boundary, not a temporary tool limitation, and chats should not repeatedly describe it as such.

The intended interaction is:

```text
Chat determines what must be inspected / changed / tested
        ↓
Chat provides exact paste-ready command(s)
        ↓
User runs the command in the local Windows checkout
        ↓
User returns output
        ↓
Chat interprets the actual result and continues
```

The user's local repository and locally executed tests remain the authoritative implementation state.

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

# 7. Python / Tool Use and Hard Repository Tool-Routing Rule

The user prefers to perform repository changes through VS Code / PowerShell rather than through Python-generated artifacts.

For **Machine Builder repository work**, the following tooling/workflows are prohibited:

* Python
* Jupyter
* pandas
* dataframes
* data-analysis workflows
* generated notebooks
* plotting/charting workflows
* spreadsheet-style data-analysis workflows
* temporary analysis scripts
* temporary analysis files
* temporary analysis artifacts
* equivalent analysis-tool workflows used in place of direct repository inspection or project tooling

This is a **hard tool-routing/workflow rule**, not merely a preference.

Do not invoke a prohibited tool or workflow even when the intended use is only to:

* inspect repository files
* count lines, occurrences, or values
* compare text
* parse or transform source
* calculate a value
* validate an edit
* generate a temporary artifact
* test whether the tool is available
* report that the tool is unavailable
* generate a no-op
* demonstrate that no artifact is being generated

Do not invoke the prohibited tool first and then explain that it was unavailable or produced nothing.

The prohibited tool must not be invoked at all.

The prohibition applies to repository inspection, source inspection, planning, architecture work, documentation review, implementation review, testing, visual-editor work, routing work, and audit work.

The prohibition is about the **tool/workflow**, not about reasoning.

A workstream may reason about code, architecture, hardware, research, routing, tests, or repository structure normally.

The intended repository tooling path is:

```text
PowerShell / terminal
        ↓
Git
        ↓
direct repository/source/documentation inspection
        ↓
existing project tooling
        ↓
project tests
```

Use the simplest practical inspection method.

Do not introduce tool complexity merely for convenience.

### Tool-Selection Preflight

Before invoking any tool for a Machine Builder task, determine whether the requested action concerns the repository.

If it does:

1. Do not select Python, Jupyter, pandas, dataframe/data-analysis, notebook, plotting, spreadsheet-analysis, or equivalent analysis tooling.

2. Use the approved PowerShell / terminal / Git / direct-source / project-test workflow.

3. If the task can be completed by giving the user a paste-ready repository command, give the command instead of invoking another tool.

4. If the task requires current local repository state, have the user run the required command in the authoritative local checkout.

The absence of a legitimate data-analysis need must never be treated as a reason to invoke a data-analysis workflow.

### Accidental Tool-Routing/Workflow Violation

If a prohibited Python/data-analysis/Jupyter-style tool is accidentally invoked:

1. Stop that tool workflow immediately.

2. Do not retry the prohibited tool.

3. Do not generate a no-op artifact or temporary analysis artifact.

4. Do not continue using the prohibited tool merely to explain or inspect the failure.

5. Briefly identify that a repository tool-routing/workflow violation occurred.

6. Return immediately to the approved PowerShell / terminal / Git / direct-source / project-test workflow.

7. Continue the repository task from the actual available evidence.

An accidental prohibited-tool invocation does not make the repository task impossible and does not replace the required local verification workflow.

---

# 8. Full-File Replacement and Artifact Scope

When modifying a reasonably sized file, prefer:

```text
FULL FILE REPLACEMENT
```

over surgical editing.

The goal is to minimize user error and avoid requiring the user to reconstruct a file from scattered fragments.

Surgical edits are acceptable when a full replacement is impractical or unnecessarily large.

Repeated surgical editing of the same large file is a signal that its modularity should be reconsidered.

### Whole-File Replacement Rule

When the user explicitly requests a **whole file**, **complete file**, **entire file**, **full-file replacement**, **rewrite the file**, or equivalent wording, treat that as an exact artifact-scope instruction.

For such a request:

* The requested artifact is the **complete resulting file**, not an addition to the current file.

* Do not append a new section to the existing file merely because the requested content is longer than expected.

* Do not produce an incremental patch when the user explicitly requested the complete file.

* Do not create a second competing "full" version unless the user explicitly asks for alternatives.

* Preserve existing content that is still valid, but incorporate the requested changes into the complete replacement.

* Do not invent additional content merely to make the replacement "more complete."

* Do not silently change the requested scope from "whole file" to "add this to the current version."

* If the complete file is needed from the repository, inspect/retrieve the authoritative current file first, then construct the complete replacement from that source.

* For a reasonably sized file, prefer a complete-file replacement over repeated surgical insertions when the user explicitly requests a whole-file result.

* Before applying the replacement, verify that the resulting artifact is actually the complete file and not merely the previous file plus an appended/generated section.

### Artifact-Scope Preflight

Before modifying or generating a repository artifact, determine the requested scope:

```text
whole file / complete replacement
        →
produce the complete resulting artifact

targeted edit / patch
        →
modify only the requested area

new file
        →
create only the requested new artifact
```

Do not switch between these scopes without the user's instruction.

The requested artifact scope takes precedence over a convenience-based editing method.

### Revision Integrity

When revising a whole-file result after feedback:

* Start from the complete current intended file.

* Produce the complete revised file again.

* Do not append the revision to the previous response or file.

* Do not preserve a rejected intermediate version as competing current content unless explicitly requested.

* When the user asks for another whole-file revision, the response must again contain the complete resulting file.

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

This section is the single authoritative project-wide procedure for replacing a chat after a conversation reaches its length limit. `README.md` and workstream handoffs must refer to it instead of maintaining competing universal recovery checklists.

### Documentation-first recovery and local-state verification

**Purpose:** Recover project context efficiently without requiring the user to relay repository documents that are already accessible to the chat.

**1. Read the committed documentation baseline first.**

Before asking the user to paste project documents, retrieve the latest accessible committed versions from the repository's canonical remote, normally `main`. Identify the commit used and the retrieval time.

Read the universal recovery documents together:

* `CHAT_WORKFLOW.md`, including this section.
* `MASTER_PLAN.md`.
* `PROJECT_CURRENT_STATE.md`.
* The receiving workstream's current living handoff.
* The matching WORKSTREAM_FOCUS_INDEX.md entry (navigation only; the handoff remains authoritative for detailed technical state).

Also read `DOCUMENTATION_AUTHORITY.md` for Planning, plus any workstream-specific or task-specific authorities required by the handoff.

Do not ask the user to paste documents that are accessible from the committed repository. Do not substitute memory, old chat summaries, or historical reports for the required documents.

**2. Verify the local checkout separately.**

The committed remote baseline provides project context; it does not establish the user's working-tree state.

Use one compact, batched, read-only Git check to establish the actual local branch, `HEAD`, remote reference, and working-tree status before implementation or file changes. Inspect relevant local diffs when they matter.

The local checkout remains authoritative for source and test contents, uncommitted changes, user-owned files, actual branch state, and locally executed test results. A dirty local document may contain newer information than the remote version; preserve and reconcile that difference rather than overwriting it.

**3. Use a bounded fallback.**

If the remote is private, inaccessible, or a required document cannot be retrieved confidently, ask for only the missing information. Batch missing documents or relevant sections into one request wherever practical. Prefer a targeted local command over a broad dump that overwhelms the console.

**Console-output and paste limit:**

- Observed paste ceiling: approximately 884 numbered content lines (the visible range was 369-1252). This is an observed ceiling, not a guaranteed capacity.
- Maximum routine target per command: at most 700 total printed lines, including headings and status messages. Prefer 350 lines or fewer for long documents; long lines and command echo can still cause clipping.
- Read large documents in separate bounded batches. Check file length and headings first, then print only needed sections. Do not combine multiple long documents into one console dump.
- Print a clear completion marker. If output is clipped or the completion marker is missing, treat unread sections as unavailable and continue with smaller ranges; never claim the full document was read.

**4. Do not create substitute artifacts.**

Do not generate downloadable update scripts, replacement document artifacts, patches, or repository copies as a workaround for the unavailable local checkout. If local changes cannot be applied through an available established workflow, provide the exact proposed text and concise direct-edit instructions for the user to apply in the authoritative checkout. Never imply that a proposed change has been applied.

**5. Resume from verified state.**

After the required reading and local-state check, continue from the workstream handoff's recorded `Next Action`. Record the baseline and timestamp associated with each inspection or update. Missing timestamps or unverified baselines must remain explicitly missing or unverified; never reconstruct them from another report's timestamp.

This process reduces user effort without weakening ownership boundaries, test requirements, or implementation and commit authorization gates.

### Canonical replacement prompts and checkpoint freshness

Each workstream maintains one canonical, in-repository recovery prompt, owned by that workstream and updated in place. The standard path is `machine-structure-editor/handoffs/NN_WORKSTREAM_REPLACEMENT_PROMPT.md`; Planning uses `machine-structure-editor/handoffs/01_PLANNING_ARCHITECTURE_REPLACEMENT_PROMPT.md`.

The **living handoff** is the detailed history of evidence, decisions, validation, and remaining gaps. The **replacement prompt** is the concise, self-contained recovery snapshot: mission, latest verified published commit, unpublished local work, actual validation state, unresolved criteria, current queue/slot state, ownership boundaries, and the exact next action.

Refresh both documents at material checkpoints, especially after a research or implementation result, changed next action, failed operation affecting recovery, publication or slot release, or before ending a substantial work session. Do not wait for an expected length-limit warning. Keep one canonical prompt; do not create a new file for every revision.

A prompt pasted into chat is not proof the repository file was saved. When the chat cannot directly write to the local checkout, provide one guarded command to update only the workstream-owned file, then verify its read-back and whitespace/encoding results from actual output. Report clearly if the file is missing, stale, local-only, or unverified. Do not repeatedly dump the same prompt as a substitute for confirming the file state.

The recovery prompt may remain local and unpublished while still being usable. It must distinguish the published baseline from all local-only changes and must not claim a write, validation, commit, or push that was only attempted. Refreshing a prompt does not itself require replacing the active chat, staging the file, or expanding a publication grant.

## Required on every replacement chat

1. Read `CHAT_WORKFLOW.md`, including its current operating constraints and this recovery section.
2. Read `MASTER_PLAN.md`.
3. Read `PROJECT_CURRENT_STATE.md`.
4. Read the current living handoff for the workstream being resumed.
5. Inspect the user's actual current local checkout. Confirm the branch, `HEAD`, working-tree status, and relevant current source/test state before relying on implementation or verification claims.
6. Resume from the current handoff's Next Action. Do not assume a remembered task, commit, test result, line number, or file state is still current.

## Additional workstream-specific required reading

A workstream may require a small number of additional documents on every replacement. Those requirements must be explicitly identified as required on every replacement in the workstream's current handoff or designated entry point. They supplement the universal list above and must not repeat it.

A `START_HERE.md` or navigation document is not automatically mandatory merely because it exists or links to other documents. The workstream must explicitly designate it as required on every replacement.

## Consult when relevant to the active Next Action

Consult additional architecture, ontology, research, implementation, source, test, standards, machine, or other workstream documents when the current task needs them. Use `DOCUMENTATION_AUTHORITY.md` when document authority or ownership is unclear, when the task changes documentation authority, or when locating the primary document for a question. Inspect current source and tests whenever claims about current implementation or verification depend on them. Consult adjacent handoffs when work crosses ownership boundaries.

## Historical and reference documents

Do not routinely reread historical, superseded, archived, or old handoff documents. Consult them only when the active task needs historical evidence, the context of a past decision, or an explanation of a document's disposition or replacement. Use `HISTORICAL_DOCUMENT_ARCHIVE.md` when appropriate. Historical text and old test output do not override the current checkout and current verification.

Do not reconstruct the workstream from conversation memory when durable documents contain the needed information.

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

# 25.1 Handoff Lifecycle / Rollover

Each workstream should have one clearly identifiable live/current handoff.

**Live handoff = recover current state and continue work.**

The live handoff should stay focused on the information a new chat needs to recover the workstream's present state, including:

* purpose and ownership;
* established architecture and terminology still relevant to current work;
* current verified implementation or representation;
* active decisions and constraints;
* unresolved questions or blockers;
* important current files;
* verified repository and test state;
* current next action;
* other concise current-state context needed for safe continuation.

Completed work should normally appear in the live handoff as concise current-state facts and checkpoint references rather than as a detailed chronological narrative.

Detailed completed history, superseded actions, investigative chronology, intermediate evidence, and prior-state material should be preserved in historical/versioned records when it is no longer needed for current-state recovery.

**Historical handoff = preserve prior state, history, and provenance.**

A handoff rollover should be considered when completed history begins to dominate current-state readability, when a major phase or milestone closes, or when a fresh chat would have to spend substantial effort distinguishing historical material from active work.

When rolling over:

* preserve the old handoff rather than deleting its information;
* create a fresh live handoff;
* rewrite the new live handoff from the current verified state rather than mechanically copying and trimming the old handoff;
* carry forward all information still necessary for correct current work, including active constraints, unresolved blockers, important architecture, current verified state, and next action;
* make clear which prior handoff was superseded and when, providing enough provenance without turning the new handoff into a transcript.

Historical handoffs must not remain competing current documents. There should be one obvious live handoff for each workstream.

Historical records may be corrected when an archival factual error is discovered, but they are no longer the normal working document for the active workstream.

This rule does not impose a rigid line-count or arbitrary size threshold. Rollover is based on current-state readability and meaningful phase or milestone boundaries.

Do not invent a new historical directory or naming convention when an established documentation-authority or historical-archive convention already exists. Follow the project's existing documentation organization.

# 26. Commit and Push Workflow

Authorized workstreams may use PowerShell and command-line Git to stage, commit, push, and verify their assigned, validated changes when existing workstream authority permits publication. GitHub Desktop remains an available alternative when the user performs publication manually; it is not mandatory for workstreams with standing publication authority.

The normal sequence is:

1. Validate the work and inspect the complete change scope.
2. Preserve concurrent work and ensure the index is in the expected state.
3. Stage only explicitly authorized paths.
4. Review staged paths and the complete staged diff; run `git diff --check`.
5. Commit and push using the workstream's existing publication authority.
6. Verify local HEAD, fetched `origin/main`, and live remote main.
7. Report actual test results, publication state, commit details, and remaining worktree changes.

A routine authorized commit and push does not require a second Planning approval. This section does not authorize changes outside the existing assignment or workstream scope.

## Standard checkpoint sequence

1. **Preflight:** Resolve and verify the repository root, branch, HEAD, fetched `origin/main`, and live remote main. Inspect the complete worktree, index, staged and unstaged diffs, and all untracked paths. Fetch before deciding whether the baseline is current. If state is unexpected or ambiguous, stop and reconcile without discarding work.

2. **Validate:** Use the project's verified virtual environment. Run focused tests first, then the full test suite when appropriate for the change. For documentation-only work, inspect the content and structure and run whitespace checks; do not present code tests as necessary or claim they passed when they were not run.

3. **Review scope:** Inspect the entire working-tree diff for every authorized path and run `git diff --check`. Ensure the index is empty before staging unless existing staged content has been explicitly identified and safely handled. Preserve concurrent edits and untracked files.

4. **Stage deliberately:** Stage only the exact approved paths using explicit `git add -- <path>` arguments. Never use `git add .` or `git add -A` in this workflow. Compare the staged path list to the exact expected list, inspect the complete staged diff, and run `git diff --cached --check`. Stop before committing if paths are missing, extra, unexpected, ambiguous, or mixed with other work.

5. **Commit and inspect:** Commit only after required validation and scope checks pass, using existing commit authority. A routine authorized commit does not require a second Planning approval merely because it is a commit. Afterward, record the commit hash and subject, inspect its exact changed-file list and diff, and check the remaining worktree status.

6. **Publish normally:** Push to the intended branch without force-pushing. Then fetch `origin` again, compare local HEAD with fetched `origin/main`, and query live remote main. When no concurrent commit intervenes, the hashes should match. If remote main advanced, check whether the intended commit is contained in the fetched remote history and reconcile safely. Do not blindly reset, revert, amend, rebase, overwrite, or force-push to conceal a failure.

7. **Close out with evidence:** Report actual test commands and results, whitespace-check results, commit hash and subject, exact committed paths, publication verification, and every modified or untracked path remaining afterward. Attribute test results to the workstream that ran them and distinguish this task's files from unrelated shared-checkout work.

## Native Git exit handling

Capture `$LASTEXITCODE` immediately after each native Git command whose result controls execution. For `git diff --quiet`, exit `0` means no differences, exit `1` means differences exist, and other nonzero values indicate an error. Interpret the exit code directly; do not compare empty output with `$true` to infer success.

On failure, stop, inspect state, and report the observed evidence and safe next action. Keep PowerShell guarded, with clear status messages and safe returns. Do not use `exit 1`, blanket resets/reverts, blind amend, or force-push as routine recovery.

## Commit Metadata Output Format

Every meaningful commit request must provide both Summary and Description using the following canonical format. This is the project's standard presentation format, not merely an example. For command-line Git, use Summary as the commit subject and Description as the commit body; GitHub Desktop is not mandatory when the workstream is authorized to publish.

**Summary**

```text
<summary value only>
```

**Description**

```text
<description value only>
```

The Summary and Description headings are explanatory labels and must remain outside their respective copy/paste blocks. Each block must contain only the value for that GitHub Desktop field.

Do not put Summary: or Description: inside either copy/paste block. Do not present the metadata only as ordinary prose without a dedicated copy/paste block. Do not place explanatory prose, instructions, Markdown labels, or other metadata inside either block.

The user should be able to copy each block verbatim into the corresponding GitHub Desktop field.

This rule applies whenever a chat asks the user to enter or use Git commit Summary and/or Description text, including commit/push checkpoints.

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

## Durable documentation authority and handoff maintenance

When a change creates, renames, moves, retires, or materially changes the authority or status of a durable project document, review `DOCUMENTATION_AUTHORITY.md` and update it as part of the coordinated documentation change whenever the map would otherwise become inaccurate.

Do not add every source file, test, or supporting artifact to the authority map. Update the relevant living workstream handoff when a change materially affects that workstream's ownership, continuity, decisions, or Next Action. For material repository-structure changes, also follow the generated repository-tree rule in Section 14.

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

## User-facing execution instructions

Assume the user understands that repository commands are run against their authoritative local checkout. Do not repeatedly explain this established workflow.

Do not preface repository instructions with disclaimers that a chat cannot directly write to the user's local files, or remind the user that they must run the provided commands. Mention execution limitations only when the user asks about them or a concrete limitation materially changes the requested action.

For repository work, provide the exact, action-ready command or edit, its scope and necessary prerequisites, and the verification output to return. Never imply that local files were changed, tests run, or Git actions completed unless the user reports that result or an authorized tool verifies it.

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

---
# 34. Cross-Workstream Messaging and Copy-Ready Handoffs

This section defines the required format for messages that move between Machine Builder workstream chats.

## Required sender-to-recipient label

Every cross-workstream message must be fully enclosed in one clearly identified copy-ready block. The first line inside the block must use this format:

From #N -> To #M - Topic

Replace #N with the sending chat and #M with the receiving chat. For example:

From #2 -> To #1 - Promega endpoint evidence matrix

From #1 -> To #4 - Component endpoint authoring

The sender, recipient, and topic must be inside the copy-ready block. The user must not have to type a prefix, prepend a label, or supply missing context when pasting the message.

## Self-contained copy blocks

- Put every instruction, report, handoff, acceptance review, decision, and required context inside the copy-ready block.
- Do not put required portions before or after the block where the user must remember to copy them separately.
- Use one complete block per destination chat. If multiple chats need messages, provide separate blocks in numerical chat order: #1, #2, #3, #4, #5.
- Within each chat's file list, sort file paths alphabetically.
- Text outside a copy-ready block may explain the message to the user, but it must not be necessary to make the copied message understandable or actionable.
- Replies intended to be forwarded to another chat must follow the same rule, including reports returned to Planning. A report from #2 to #1 must carry the label "From #2 -> To #1" inside its own block.
- Do not force ordinary responses intended only for the user into cross-workstream blocks.

## Publication queue and shared Git index

All workstreams share one local checkout and one Git index. Editing and publication are separate activities.

- Workstreams may inspect and edit their own files, run tests, and update their own handoffs while another workstream holds the publication slot. They must preserve ownership boundaries and leave other owners' staged content untouched.
- A report that work has started is not a publication request. To enter the queue as READY, an owner reports the exact intended paths, an updated handoff, actual validation results, a proposed commit subject, and any unresolved ownership questions.
- Planning (#1) assigns explicit queue positions and grants exactly one active publication slot. Prioritize blockers and dependencies first; among equally ready requests, use the oldest complete READY report. State each owner's status and whether the user needs to act.
- Only the active slot holder may stage, commit, and push. Other workstreams may continue editing, testing, investigating, and updating their handoffs, but must not stage, commit, or push until their slot is granted.
- Immediately before staging, the slot holder must fetch and verify the branch, local HEAD, origin/main, and live remote main; inspect git status --short and git diff --cached --name-only. If any paths are already staged, stop and report them to Planning. Never unstage, reset, discard, stash, or commit another workstream's staged content.
- If the index is empty, stage only the explicitly approved owner-scoped paths. Verify the exact staged list, inspect the complete staged diff, run staged whitespace checks, commit with the reported subject, push normally, and verify HEAD equals origin/main and live main. Recheck immediately before git add; if the state changed, stop.
- Other workstreams should not infer a slot from old output or from being listed first in a document. A publication slot is granted explicitly in Planning's latest coordination message and remains exclusive until remote verification or an explicit release.
- If a workstream completes its assigned task, it should continue with the next already-authorized in-scope action. If none is clear, it should ask Planning for the next focus with its completed work and possible in-scope candidates, rather than silently waiting or beginning unauthorized work.

### Publish-and-yield throughput and mandatory slot closeout

Treat a publication slot as permission to publish a specified coherent batch, not as a reason to hold the queue while unrelated work remains unfinished.

When the slot arrives, publish the smallest **complete, coherent, validated unit** within the exact grant as soon as practical. Include dependent implementation, tests, and documentation needed to make that unit sound. Leave unfinished or unrelated changes local. Do not split mutually dependent changes merely to reduce a batch, and do not publish an incomplete unit to increase throughput.

If no safe, complete batch fits the grant or a guard fails, stop before staging and release the slot with a concrete `NOT READY — SLOT RELEASED` or `BLOCKED — SLOT RELEASED` report. Continue permitted research, editing, and validation while queued; queued workstreams are not expected to sit idle.

Every slot holder must send Planning a separate, explicit closeout immediately after publishing or yielding. A successful closeout must say `PUBLISHED — SLOT RELEASED` and include the full commit hash, subject, exact committed paths, actual validation, post-push verification of local `HEAD`, fetched `origin/main`, and live remote `main`, plus remaining local work. A non-publication closeout must say `NOT READY — SLOT RELEASED` or `BLOCKED — SLOT RELEASED` and state the failed guard, exact staged/index state, remaining local changes, and next action. Do not bury slot release in a research update and expect Planning to infer it.

A grant is scoped to its named paths and baseline. If branch or remote main advances after the grant, stop before staging. Verify ancestry and request explicit renewal against the actual baseline; never assume the old grant automatically covers a new baseline. Never revert an intentional intervening commit merely to restore an earlier baseline.

If yielding with staged work, first inspect the full index. Unstage only the slot holder's own paths when they are the only staged paths and doing so is necessary to release the slot. If any other owner's paths are staged, do not touch the index; stop and report the conflict.

Refresh your handoff and canonical recovery prompt at material checkpoints, including after a publication or yield. Do not delay an otherwise valid publication just to bundle a recovery prompt that is outside the grant. Such a prompt update may remain local-only and must be reported as such. After explicit closeout, do not publish again until Planning grants a new slot.

## Copy completeness

Before sending a cross-workstream message, verify that its block is complete, correctly addressed, and contains the entire handoff. Do not require the user to reconstruct, shorten, relabel, or combine content from different parts of a response.

The purpose is to eliminate manual sender prefixes and prevent the user from copying too little or too much.

## Standardized Cross-Workstream Reporting Format

Use the structured reporting style established by the Controller/Board workstream's milestone reports as the default across all Machine Builder workstreams. This section standardizes reporting presentation; it does not change workstream ownership, publication authority, acceptance criteria, or task scope.

### Required copy-ready message form

- Every cross-workstream assignment, decision request, acknowledgement, status report, milestone report, and acceptance review must be fully enclosed in one clearly identified, copy-ready message block.
- The first line inside that block must identify sender, recipient, and topic, using the required form: `From #N -> To #M - Specific Topic`.
- The message must be self-contained. Do not send the substantive cross-chat message as plain prose outside the copy-ready block and expect the recipient to infer that it is a handoff.
- Use the structured metadata and sections below as the default. Adapt them to the task when a field or section is genuinely irrelevant; do not fabricate activity or fill sections with boilerplate.

### Rendered copy-block presentation

- For cross-workstream prose messages intended to be pasted into another chat, use a dedicated styled writing/draft block with a copy control whenever the response interface supports one. Do not substitute a generic code block intended for source code or commands.
- Keep the required `From #N -> To #M - Specific Topic` first line and every actionable part of the message inside that single writing/draft block. Explanations for the user stay outside it and must not be necessary to use the copied message.
- Standardize the semantic block type and copy boundary, not exact colors or font sizes. The interface controls the visual rendering, which may vary.
- Keep executable PowerShell separate in the plain `powershell`-labeled code block required below. Never put executable commands in a prose writing/draft block.

### Metadata block

Use these bold labels where applicable:

- **Classification:** Identify the task as research, documentation-only, implementation, validation, audit, acceptance review, or another accurate category.
- **Verified repository baseline:** Give the actual commit SHA and subject when verified and relevant. If the repository was not inspected or the baseline was not verified, say so explicitly. Never present a prior chat's baseline as the current one without checking.
- **Durable destination:** Name the existing repository path and section where the result was recorded. If no durable update occurred, state that clearly.
- **Validation:** Name the checks actually performed and their results. Distinguish the reporting workstream's own execution from results supplied by another workstream.
- **Publication:** State whether the work is uncommitted, staged, committed, pushed, and remotely verified as applicable. Do not imply that committing a change proves that a push succeeded.
- **Disposition:** For formal audit or acceptance reviews, state `ACCEPTABLE` or `BLOCKED` and tie the disposition to explicit criteria and available evidence.

### Standard report sections

For substantive milestone and handoff reports, use these sections in this order:

1. `## Durable update completed` — state what was actually changed and where it was recorded. If no durable update occurred, say so instead of implying one.
2. `## Findings preserved` — list the material conclusions and their evidence. Clearly distinguish verified facts, reported-but-not-independently-verified results, inferences, recommendations, conflicts, and unresolved questions.
3. `## Recommended next steps` — give the next bounded action, responsible workstream, and any dependency or Planning decision required.

Keep reports concise, concrete, and scannable. Report exact paths and test results where relevant. A proposed fix is not a verified fix; a claimed test pass is not an independently verified test pass; and missing evidence must remain visible.

Simple acknowledgements may use a shorter form, but must still use the required sender/recipient/topic label and one complete copy-ready block. Formal acceptance reviews must retain the existing read-only boundary and explicit disposition requirements.

### Executable command formatting remains separate

This reporting standard does not override the PowerShell and copy/paste safety requirements elsewhere in `CHAT_WORKFLOW.md`.

- User-facing executable PowerShell must use the existing plain `powershell` code-fence format, with no fence metadata, title, or language-marker additions beyond the required language label.
- A command must be continuous, complete, and directly copyable. Do not place explanatory prose inside it, and do not put nested Markdown fences inside an executable PowerShell block.
- When a cross-workstream instruction also needs executable commands, ensure the message and command remain complete and the rendered copy boundaries cannot truncate either one. Do not make the user repair fences or reconstruct missing instructions.
- Before sending a long or complex command, inspect the complete block for premature fence endings, missing sections, malformed here-string terminators, or formatting that would turn part of the command into ordinary text.

### Scope and authority

These conventions apply consistently to workstreams #1 through #5. They do not grant permission to edit another workstream's files, modify application code, change the ontology, stage or publish changes, or exceed existing task authority. All existing repository safeguards, workstream responsibilities, test restrictions, cross-chat requirements, and shared-checkout protections remain in force.

# 35. Workstream Handoff and Planning Documentation Cadence

## Individual workstream handoff cadence

Each workstream must update its live handoff after every five commits attributable to that workstream have been successfully published since its last substantive handoff update.

Count each attributable commit individually even if multiple commits are pushed in one batch. Only published commits count toward the threshold. A handoff-only commit does not count toward the next five-commit interval.

This is a maximum routine interval, not a reason to delay an important update. Update the relevant handoff immediately after a significant milestone, material implementation or architecture decision, verified checkpoint, newly identified blocker, or ownership transition.

## Planning's additional cross-workstream cadence

Planning integrates the project-wide picture and must not wait for an individual workstream's five-commit threshold when a material cross-workstream change is already known.

- Refresh `PROJECT_CURRENT_STATE.md` when a material actual-state change, validation result, blocker, or next action is established. Describe the evidentiary status accurately.
- Update `MASTER_PLAN.md` when project scope, priorities, sequencing, or architectural decisions change.
- Update the Planning handoff at material cross-workstream changes, milestones, ownership transitions, and before context handoffs.
- Update `DOCUMENTATION_AUTHORITY.md` when document authority or ownership changes.
- Preserve meaningful superseded decisions and milestones in `HISTORICAL_DOCUMENT_ARCHIVE` when they warrant retention. Do not turn the archive into a duplicate commit log.
- Update `CHAT_WORKFLOW.md` when a common process rule has been adopted.

Batch related documentation edits sensibly, but do not knowingly leave the project-state record stale simply because no individual workstream has yet reached five commits. Update only documents appropriate to their established ownership and authority, and preserve unrelated concurrent changes.

## Evidence status language

Project reports and documentation must distinguish these different states:

- **Reported:** a workstream or person stated a result; this alone does not establish independent verification.
- **Locally inspected:** the relevant source, diff, or repository state was directly examined.
- **Tested:** the specified test or check was actually run and its observed outcome recorded.
- **Published:** the relevant commit was verified on the remote repository.

A reported result may trigger Planning review or a suitably qualified current-state update without being presented as locally inspected, tested, or published. Do not promote one evidence state to another without performing and recording the corresponding verification.

This section supplements the handoff lifecycle and rollover rules in Section 25.1. Section 34, Cross-Workstream Messaging and Copy-Ready Handoffs, remains intact and mandatory.

# 36. Autonomous Workstream Continuation and Durable Knowledge

## Continuing missions

Each workstream has a continuing mission defined by the Master Plan, current project state, and its own live handoff. Completing an immediate assignment is a milestone, not the end of that mission.

At the start of work and after a context replacement, read the applicable workflow, current project state, and workstream handoff. Recover the goal, completed work, evidence, unresolved questions, scope boundaries, and next actions.

When the next useful action is clear and within authorization, take it without waiting for routine instructions from Planning. A discovery or completed search is not itself a stopping condition. Record the result, identify what follows, and continue. Do not wait for another workstream when useful work can proceed independently.

Escalate genuine blockers, cross-workstream conflicts, decisions outside the workstream's authority, and changes that would exceed approved scope. Explain the concrete issue and recommended resolution. Continue other independent work where practical.

## Durable findings and workstream-owned history

Repository documentation is the durable project record. Chat responses are not a substitute for preserving useful findings.

Unless an assignment explicitly prohibits repository writes, research-only work may update workstream-owned research notes and its handoff while remaining prohibited from changing production code, catalog data, or tests. An explicit no-repository-write boundary must be honored; in that case provide a complete, actionable handoff to the authorized owner.

At meaningful milestones, each workstream must update its own handoff and appropriate research or implementation records. Preserve useful source links and revisions, decisions and rationale, evidence status, uncertainty, remaining questions, completed work, checkpoint, and next actions. Do not leave important findings only in chat history or downloadable files.

A material cross-workstream message is also a continuity checkpoint when it records a new design preference, decision, scope or ownership change, evidence result, validation result, blocker, dependency, or publication state. The sending workstream updates its own handoff in the same work session, before or immediately after sending the message. Routine acknowledgments that add no state do not require a documentation rewrite.

At those checkpoints, include the exact paths, purpose of the changes, checks actually run, publication state, unresolved questions, and one concrete next action with its owner. Planning maintains WORKSTREAM_FOCUS_INDEX.md from the updated handoffs and verified checkpoint reports; individual workstreams provide the information for their entries but do not rewrite another workstream's handoff.

An exact warning threshold for conversation length cannot be relied upon. Keep the handoff current throughout the work rather than waiting for a length-limit warning. When replacing a chat, provide a dated, copy-ready startup prompt based on the latest handoff and focus-index entry. The prompt is a generated convenience, not a second history archive.

When work must be performed in the user's local checkout, provide complete, guarded, copy-ready PowerShell commands. Do not claim local execution unless the returned results establish it. Do not use a downloadable artifact as a substitute for durable repository documentation.

Update workstream documentation at significant milestones, decisions, blockers, and before context replacement. The five-published-commit cadence in Section 35 is a maximum routine interval, not permission to delay important updates.

## Reporting and coordination

Report meaningful milestones, verified outcomes, material blockers, and decisions—not every intermediate discovery. Distinguish reported, locally inspected, tested, and published outcomes under Section 35.

Planning owns project-level priority, cross-workstream conflicts, architecture decisions, and project-wide synthesis. Planning does not need to prescribe every routine next step or personally reconstruct each workstream's technical findings.

These rules do not override workstream ownership, publication authority, test/tool restrictions, or shared-checkout safeguards. Section 34's complete, copy-ready sender-to-recipient handoff convention remains mandatory.

# 37. Future Feature Intake and Canonical Register

## Canonical location

`MASTER_PLAN.md` Section 13, "Future problems / deferred ideas," is the canonical register for future features, usability problems, and out-of-scope opportunities. Do not create a competing backlog unless Planning explicitly changes this decision.

## Required intake and duplicate avoidance

When any workstream discovers a genuinely new, unrecorded out-of-scope feature, usability issue, or research opportunity, it must provide Planning one complete copy-ready message beginning:

`From #N -> To #1 - Future Feature Intake: <topic>`

Include the problem or opportunity, impact, supporting context or sources, constraints, possible acceptance outcome, and suitable revisit point. Mark unverified recollection or speculation clearly.

Do not repeatedly submit the same intake after Planning has acknowledged or recorded it. If the item already exists, preserve relevant technical evidence in the workstream's own durable notes and handoff, and continue the current mission. Send Planning an update only when new evidence materially changes the item, its urgency, scope, or acceptance criteria.

Planning records accepted candidates in Section 13 and controls their priority. An intake message alone does not mean the item is recorded, prioritized, or authorized for implementation. Future-feature intake must not interrupt active work.

Immediately blocking safety or data-integrity concerns must still be escalated promptly; do not defer an active blocker merely because a future-feature register exists.
