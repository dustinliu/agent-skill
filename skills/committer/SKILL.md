---
name: committer
description: Create git commits with concise markdown-formatted commit messages. Use when the user wants to commit changes.
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash
---

# Commit Changes

You are assisting the user in creating git commits based on their specific needs.

## Steps

1. **Check current status**: Run these commands in parallel:
   - `git status` to see all changes (never use the `-uall` flag)
   - `git diff` to see staged and unstaged changes
   - `git log -5 --oneline` to understand the commit message style

2. **Analyze changes**: Review all changes and decide which files should be committed.

3. **Create commit message**:
   - Must use markdown format (use `##` as the title)
   - Must be as concise as possible (max 1-2 sentences)
   - Focus on WHAT changed and WHY, not HOW
   - Follow the existing commit style in the git log

4. **Stage files**: Use `git add <specific-files>` to include relevant files.
   - Prefer using file names to add specific files.
   - Do not commit files containing secrets (.env, credentials.json, etc.).

5. **Create commit**: Use HEREDOC format and include the Co-Authored-By line:
   ```bash
   git commit -m "$(cat <<'EOF'
   ## Your commit title

   - Brief description of the changes.
   - ...

   Co-Authored-By: [LLM Model Name]
   EOF
   )"
   ```

6. **Verification**: After committing, run `git status` to confirm success.

## Important Rules

- Always write commit messages in English.
- Always ask for confirmation before staging new files.
- Always create a new commit (do not use `--amend` unless explicitly requested).
- If a pre-commit hook fails, fix the issue and create a new commit (do not amend).
- Never skip hooks (`--no-verify`) unless explicitly requested.
- Never push unless explicitly requested by the user.
- Do not create empty commits if there are no changes.
- Before committing, show the commit message and staged files to the user and ask for confirmation.

## Commit Message Format Example

```
## Add user authentication
- Implemented JWT-based authentication with refresh tokens.
- Implemented cookie-based authentication.

Co-Authored-By: [LLM Model Name]
```
