# teams-agent

Manage team agents, skills, and hooks from the shared registry.

## Commands

| User types                  | Action                                                  |
|-----------------------------|---------------------------------------------------------|
| `/teams-agent install`      | Install / update everything from registry main branch   |
| `/teams-agent v2`           | Install exactly version v2 from the registry (git tag)  |
| `/teams-agent push v3`      | Push local agents/skills/hooks to registry, tag as v3   |
| `/teams-agent push`         | Same but ask the user for a version tag first           |

---

## Steps

### 1. Parse the argument

Look at what the user typed after `/teams-agent`:

- **Nothing** or **`install`** → install latest
- **Starts with `v` and is a version tag** (e.g. `v1`, `v2`) → install that version
- **`push v3`** → push with tag v3
- **`push`** (no tag) → ask the user: "What version tag do you want to publish? (e.g. v3)"

### 2. Run the right command via Bash from the project root

| Case                   | Command to run                                      |
|------------------------|-----------------------------------------------------|
| install latest         | `python3 .claude/installer.py install`              |
| install version        | `python3 .claude/installer.py install --ref v2`     |
| push with tag          | `python3 .claude/installer.py push v3`              |

### 3. Show output

Print the installer output exactly as returned.

### 4. After install — tell the user

- What was installed or updated (list the items)
- That `.claude/installer.lock.json` was updated
- To commit `installer.lock.json` to pin this version for the whole team

### 5. After push — tell the user

- That the registry was updated and tagged
- The exact command teammates should run to get this version: `/teams-agent v3`

### 6. On failure

- Show the error message from the installer
- If HTTP 404 on manifest: the version tag does not exist in the registry
- If git clone fails: check that the registry URL in `.claude/installer.config.json` is correct and accessible
- If git push fails: the user needs push access to the registry repo (SSH key or GitHub token)
- If `.claude/installer.py` is missing: tell the user to copy it from the `claude-agent-md` repo
- If `.claude/installer.config.json` is missing: tell the user to create it with the registry URL
