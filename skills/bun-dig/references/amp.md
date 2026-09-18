# Amp CLI (`~/.amp/bin/amp`)

Verified on 0.0.1789516872-g161c83 and 0.0.1789549843-gf041d8 (2026-09-16). Amp auto-updates daily; re-run the scripts before trusting anything below.

## Layout

- Bun executable, arm64 Mach-O. `__BUN` segment holds two modules: the CLI bundle (UTF-16LE, ~6.5 MB decoded) and a `keyring.*.node` native addon.
- `scripts/unpack.py`, `scripts/extract_tools.py`, `scripts/amp_modes.py` all work unchanged across the two builds above.
- Verification: `amp tools list --mode <mode> --json` lists the local tools active in a mode, using the same gating function the extractor reads.

## Architecture

- The CLI is an executor. It registers every local tool spec with the server through `executor_tools_register`; the server runs the agent loop, owns the system prompt, and filters tools per mode with its own copy of the mode table.
- The system prompt is not in the binary. Mode entries carry only a `systemPrompt` key (`low`, `medium`, `high`, `ultra`, `smart`, `large`, `rush`, `review`, `puck`, `nostromo`).
- Server-side tools (Task, oracle, finder, librarian, read_thread, painter, the thread/schedule/Slack/Gmail management tools, about 77 names) appear only in name lists and UI label maps.

## Local tools (23)

Grep, Read, apply_patch, async_shell_command, create_file, download_thread_changes, download_thread_file, edit_file, find_thread, get_diagnostics, glob, load_plugin, read_mcp_resource, read_web_page, reload_mcp, reload_plugins, reload_skills, shell_command, shell_command_kill, shell_command_status, skill, upload_thread_file, web_search.

Thin wrappers over the server API: `web_search` (`webSearch2`), `read_web_page` (`extractWebPageContent`), `find_thread` (`/api/threads/find`). Everything else does its work on the machine.

## Mode table

- Two copies exist in the bundle. The one the gating function `XXe(toolName, modeKey)` reads is the larger (11 modes: deep, smart, rush, review, puck, large, low, medium, high, ultra, nostromo). The smaller copy lacks low, puck, nostromo and uses different list constants.
- Gating: with `includeTools` set, a tool is enabled when it is in `includeTools` or `deferredTools`; deferred tools are enabled but not sent up front. MCP and plugin tools bypass the whitelist. No `includeTools` means everything is enabled (custom agents).
- GPT-backed modes (low, medium, high, deep, rush) use `shell_command` + `apply_patch` and get no Read, Grep, glob, edit_file, or create_file. Claude-backed modes (smart, large, ultra) swap `apply_patch` for `edit_file`, `create_file`, `read_mcp_resource`. No mode whitelists Read, Grep, glob, or get_diagnostics.
- medium and high share identical tool lists; they differ in model and prompt key.

## Quirks worth knowing

- `shell_command` (sync, xterm-rendered progress, timeout kills) and `async_shell_command` (background, returns `pid`) are separate implementations. `shell_command_status` and `shell_command_kill` only know processes created by the async one, yet the mode whitelists include only the sync one.
- Model-issued shell commands run under `/bin/bash` with `set -o pipefail; shopt -u extglob` prepended; user-issued ones use the login shell.
- `git commit` in a shell command is rewritten to add `Amp-Thread-ID` and `Co-authored-by: Amp` trailers unless disabled by settings or `AMP_DISABLE_AMP_THREAD_TRAILER=1` / `AMP_DISABLE_AMP_COAUTHOR_TRAILER=1`.
- File tools refuse paths that traverse a symlink into a guarded location (`.ssh`, `.gnupg`, `.env`, `.git` internals, IDE configs, system directories); writing the real path directly is allowed.
- Read, edit_file, create_file, apply_patch, and read-like shell commands attach discovered AGENTS.md / AGENT.md / CLAUDE.md content to their result for the server to inject.
- The `@ampcode/plugin` `.d.ts` (about 2000 lines) is embedded as a template literal; search for `export function defineTool` to cut it out.
