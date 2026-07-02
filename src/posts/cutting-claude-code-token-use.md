date:          2026-07-02
categories:    claude-code|tokens

_July 2, 2026_

## Compress the output, rewrite the commands: cutting Claude Code's token use

Every time an agent reads a file, greps a repo, or runs a test, the whole output lands in the context window — and you
pay for it on *every* turn after that, right up until it gets summarized away. Most of it is noise the model glanced at
once and never needed again: the 200-line `ls -la`, the stack trace it read the top of, the `ps aux` dump it wanted one
process out of. It all just sits there, costing tokens, forever.

So I put two little Rust tools in the pipe between me and the model. `rtk` rewrites verbose commands into compact ones
before their output ever reaches the context; `sqz` compresses and de-duplicates whatever's left. Both hang off Claude
Code's [PreToolUse hooks](https://docs.claude.com/en/docs/claude-code/hooks) so it's completely transparent — I don't
type anything different, the output just shows up smaller. As of this writing rtk has rewritten **5,708 commands and
saved 2.6M tokens** — about 27% of everything it touched — and sqz has compressed **1,335 payloads for another 125K**.
That's real money and, more to the point, real context I get to spend on the actual problem instead of on log spam.

Why bother? Because the raw output is wildly over-detailed for whatever the model is actually doing, and the
per-command receipts are almost comical:

- `ps aux` — **98.8%** smaller. The model wanted one process, not every daemon on the box.
- A `vitest` run — **93.5%**. Green checkmarks compress to nothing; only the failures carry information.
- `git commit` — **60.7%**, across 300-odd commits. That's a lot of boilerplate nobody reads.

By sheer volume the workhorse is `rtk read` — 408 file reads, nearly a million tokens saved on its own. Every
unfiltered read is output you rent for the rest of the session.

Here's how to set it up, top to bottom.

### Install and wire the hooks

Both are single binaries — [rtk](https://github.com/rtk-ai/rtk) and [sqz](https://github.com/ojuschugh1/sqz); grab them
from their repos (mine came off Homebrew). The wiring is one command each, because both ship an `init` that writes the
Claude Code hooks for you:

```shell
rtk init --global
sqz init --global
```

`--global` writes to `~/.claude/settings.json` so the hooks fire in every project, not just the current directory — the
foot-gun is running `init` bare inside one repo and wondering why nothing happens anywhere else. What lands is a pair of
`PreToolUse` hooks on the `Bash` tool, so every shell command Claude Code runs gets routed through the tools first:

```json
"PreToolUse": [
  { "matcher": "Bash", "hooks": [{ "type": "command", "command": "sqz hook claude" }] },
  { "matcher": "Bash", "hooks": [{ "type": "command", "command": "rtk hook claude" }] }
]
```

That's the whole transparent layer. If you'd rather see it before you trust it, that block is exactly what `init` writes
— you can paste it by hand instead.

### Register the MCP tools — then actually tell the model to use them

`sqz init` also registers its MCP server (the `sqz`-managed entry in your MCP config), which hands the model a set of
compressing file-read, grep, and list tools. Here's the step everyone skips: installing them changes nothing on its own,
because left alone the model reaches for the built-in `Read` and `Grep` every single time. You have to say otherwise, in
`CLAUDE.md`:

```markdown
- Prefer `sqz_read_file` over `Read` and `sqz_grep` over `Grep` for anything non-trivial.
- Output may include a `§ref:HASH§` token — a pointer to content already in context.
  Resolve it with `sqz expand` when you need the full text.
```

The hooks fire on their own; the MCP tools need that rule. Half of getting this working is plumbing — the other half is
convincing the model to use the plumbing.

### Compaction, and one env tweak

`sqz init` wires two more hooks for long sessions — one on `PreCompact`, one on session resume — so when Claude Code
compacts a long conversation it's handled deliberately instead of by the blunt default. Nothing to configure there; init
sets it up. The only knob I turn by hand is the auto-compact window, so it fires less often:

```json
"env": { "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "400000" }
```

Fewer compaction cycles, and the ones that do fire are working on a context that's already been tidied.

### Trim the output side too

Everything so far works on what comes *into* the context — command output, file reads. But the model's own responses
cost tokens as well, both when it writes them and on every turn after, and that's just as tunable with a few lines of
`CLAUDE.md`:

```markdown
## Output Style
Fragment-first. Drop filler (just/really/basically/actually/simply), pleasantries, hedging.
Short synonyms over verbose. Technical terms exact. Code blocks unchanged.
Clarity > brevity when they conflict (e.g., articles in docstrings and error messages).
```

Fragments over full sentences, no "Great question!", no hedging throat-clearing. The one guard rail is that last line:
clarity wins when it fights brevity, so it doesn't start dropping the articles that make an error message or a docstring
readable. It's the cheapest measure here — no install, no binary, just telling the model to talk like it's paying by the
word. Which it is.

### Doing the same in another agent

Neither tool is really Claude-only. Both `init` commands can target agents besides Claude — run `rtk init --help` and
`sqz init --help` and you'll see the flags — so for the tools themselves, porting can be as small as a different one. For
anything without a turnkey installer, here are the four hooks-into-the-workflow to go looking for, roughly in order of
how universally they exist:

- **A shell you can shim.** Free and universal, because it needs no cooperation from the agent — it just hits your shell.
  Alias `ls`→`rtk ls`, `grep`→`rtk grep`, or drop a wrapper on the `PATH`, and every command gets leaner. Blunter than a
  real hook that can inspect the command first, but it works no matter what you're running.
- **MCP support.** Most agentic coders speak [MCP](https://modelcontextprotocol.io) now. Register the same sqz server and
  the compressing reads come along unchanged — same code, same job, new front-end. Highest-leverage piece to copy first.
- **A steering file.** Whatever the local equivalent of `CLAUDE.md` is — a rules file, an `AGENTS.md`, a "custom
  instructions" doc — that's where the *prefer the compressing tools* nudge goes. Skip it and your MCP server sits idle.
- **Hooks, skills, or a plugin system.** The one that varies most. The transparent command-rewrite needs a genuine
  pre-execution hook, and not every agent exposes one. So check for it by name: lifecycle hooks? a skills or plugin
  mechanism you can hang behavior off? If yes, that's where the rewrite lives. If no, fall back to the shell aliases —
  or wait for sqz's forthcoming HTTP proxy, which sits between the app and the API and needs no per-agent wiring at all.

That's the whole setup: install two binaries, run `init` twice, add a steering block, turn one knob. It's living
plumbing, so it'll keep shifting — the numbers climb every session, and the day that HTTP proxy lands I'll rip half of
this out and be glad to.
