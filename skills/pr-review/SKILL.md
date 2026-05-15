# pr-review

Review the current git diff or a specified pull request for correctness, security, and team standards.

## Steps

1. If the user passed a PR number (e.g. `/pr-review 42`), run:
   `gh pr diff 42`
   Otherwise run: `git diff main...HEAD`

2. Read the diff and evaluate:
   - Correctness: logic errors, missing edge cases, off-by-one errors
   - Security: SQL injection, XSS, hardcoded secrets, missing auth checks
   - Team standards: matches patterns in CLAUDE.md, no `any` types, no `SELECT *`
   - Test coverage: are new functions covered by tests?

3. Output a structured review:
   - **Summary** — one sentence on what this change does
   - **Issues** — list of problems, each tagged [BLOCKER], [SUGGESTION], or [NITPICK]
   - **Verdict** — Approve / Request Changes

4. Be specific: include file name and line number for every issue raised.
