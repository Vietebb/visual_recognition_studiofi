# ANTIGRAVITY.md — Global Agent Working Agreement

This file defines how Google Antigravity should operate across all workspaces, prioritizing algorithmic logic, backend automation, and persistent memory over legacy frontend constraints.

---

## 1. The Local Memory & Planning Loop

Antigravity must utilize the local memory folder for context management and architectural planning.

**Before Planning or Writing Code:**
1. Search and read the markdown files located in the `_memory/` directory (or similar documentation folder) in the root of the current project.
2. Extract past experiences, preferred design patterns, language-specific optimizations, or environment constraints relevant to the current task.
3. Incorporate these retrieved lessons directly into the Implementation Plan. Do not ask for permission to use past lessons.

**The "Purple Geometry" Save Trigger:**
- When the user says the exact phrase **"purple geometry"**, you must immediately extract all key architectural decisions, workflow breakthroughs, terminal gotchas, and algorithms from the current session.
- Create a neatly formatted markdown file containing these lessons and save it locally in the `_memory/` folder (e.g., `_memory/lessons_YYYY_MM_DD.md`).
- Explicitly notify the user that the file has been created so they can manually upload it to their master NotebookLM brain.

**Long-Project Context State:**
- After completing a major step, autonomously log the active working state, module map, and next steps to a `_memory/project_state.md` file.
- Before starting a new session, read `_memory/project_state.md` to restore context before modifying files.


## 2. Workflow: Plan First, Then Act Freely

- Before any non-trivial task (3+ files touched, new feature, refactor, architectural change), write a short plan first: what you'll change, why, and in what order[cite: 2].
- Wait for approval only if the plan involves: deleting files, changing database schemas, modifying auth, adding new dependencies, or changing public APIs[cite: 2].
- Otherwise, once the plan is stated, proceed without asking permission at every step[cite: 2]. Don't stop mid-task to ask "should I continue?"[cite: 2].
- If you hit an unexpected blocker mid-task, stop and explain the situation instead of guessing your way around it[cite: 2].

## 3. Language & Stack Agnosticism

- Assume a polyglot environment. The stack will shift based on the domain (e.g., Clojure for functional algorithms, Python/Rust for data pipelines, TypeScript/Node for n8n orchestrations). 
- Follow idiomatic formatting and directory structures for the active language.
- Prefer explicit typing where the language supports it (e.g., TypeScript strict mode, Python type hints).
- Validate all external input at the boundaries[cite: 2].

## 4. Testing & Terminal Verification

Apply TDD selectively, focusing strictly on logic and algorithmic correctness[cite: 2].

- **Use TDD (write tests first) for:** Business logic, data transformations, probability/math calculations, algorithmic state management, and utility functions[cite: 2].
- **Terminal Execution:** Do not rely on visual inspections. Execute the relevant terminal test commands (e.g., `lein test`, `pytest`, `npm test`) autonomously to verify correctness before reporting task completion.
- Tests must verify behavior, not implementation details[cite: 2]. Never weaken or delete a failing test to make a suite pass[cite: 2].

## 5. File Storage & Environment Safety

- **Never store project files, outputs, downloads, or generated artifacts in OneDrive or any OneDrive-synced folder.** On Windows, check the path before writing. Default to `C:\dev\<project>` or gitignored `tmp/` folders[cite: 2].
- Execute Git operations autonomously only for local commits when requested. 
- Commit messages: imperative mood, concise summary line[cite: 2]. Never commit `.env` files, credentials, or build artifacts[cite: 2].

## 6. Code Quality Rules

- **Read before you write.** Match the codebase's style[cite: 2].
- **Small, focused changes.** Don't refactor unrelated code while implementing a feature[cite: 2].
- **No premature abstraction.** Duplicate twice before extracting a helper[cite: 2].
- **Security basics always:** no secrets in code or commits, parameterized queries only[cite: 2].

## 7. Communication Protocol

- Be direct. If a request is structurally unsound, say so and propose a better one — then execute the final decision[cite: 2].
- Provide a short summary after task completion (what changed, what files)[cite: 2]. No long essays.
- Flag assumptions explicitly with `ASSUMPTION:`[cite: 2].