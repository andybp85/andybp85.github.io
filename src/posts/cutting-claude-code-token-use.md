date:          2026-07-02
categories:    claude-code|tokens

_July 2, 2026_

## How I cut Claude Code's token use: build right, stay lean, compress the rest

I got into coding with Claude in earnest the week Fable came out. Something about that model clicked — I went from poking at
it between tasks to building alongside it every day, and the bill for that enthusiasm showed up fast. I was blowing through
tokens at a rate that made me stop and look at where they were all going. My natural inclination, with something nagging at me
like that, is to go searching high and low for anything I can do about it — every lever I can find, however small. It turned
out there were a lot of them.

They sort into a few buckets. The biggest sits upstream of all the others: not building the wrong thing in the first place,
because the most expensive tokens are the ones you burn unwinding a bad guess. Then there's cutting what comes *into* the
context — the command output, file reads, and web pages the agent slurps up — and trimming what the model writes back out.
There's keeping the config itself lean, since every line of `CLAUDE.md` gets paid for on *every* turn. There's managing the
context that piles up over a long session — compacting it, clearing it, stashing the parts worth keeping somewhere durable.
And there's a bit of tooling to make the whole effort visible and repeatable: skills, and a statusline that shows me the meter.

The first one starts well before the first log line is ever written.

### The cheapest token is the one you never spend

Before any compression trick, the biggest lever is upstream of all of them: don't build the wrong thing. A model that writes
the wrong module, gets corrected, half-fixes it, gets corrected again, and finally lands the right design has burned all of
it — the false starts, the corrections, the re-reads — and every one of those turns then sits in the context bloating every
turn after. My most expensive tokens aren't log spam. They're the ones I spend unwinding a bad first attempt.

So the first thing I reach for is [Superpowers](https://claude.com/plugins/superpowers) — obra's framework of process skills
that make the model work like a disciplined engineer instead of an eager one. Its `/brainstorming` skill runs a Socratic
back-and-forth to pin down what I actually want *before* a line of code exists; there's a test-driven-development skill where
the test has to fail first, a systematic-debugging one that demands a root cause before a fix, and a subagent-driven flow with
code review baked in. It sounds like ceremony right up until you price out the alternative. Twenty minutes of brainstorming is
a rounding error next to a wrong build you throw away and re-read fifty times on the way to the right one.

Holding the work together is [beans](https://github.com/hmans/beans) — "a CLI-based, flat-file issue tracker for humans and
robots," which is exactly what it says on the tin. Tasks live as plain Markdown in a `.beans/` directory right next to the
code, version-controlled, and the agent reads and writes them through a GraphQL query engine that pulls only the fields it
needs — so it gets a full picture of the project while keeping token use to a minimum. The plan lives on disk, not in the
context, so the model isn't re-deriving "what were we doing again" from scratch every session. I wired it in with a little
`SessionStart` hook — `beans-gate.sh` — that fires when I open a project: no git repo, it offers to `git init`; no `.beans/`
dir, it offers to `beans init`; already set up, it just runs `beans prime` to load the board. Deterministic detection, the
yes/no in chat, and a `.beans-declined` sentinel so it shuts up if I say no once.

### The runtime leak, and two little tools

That's the build side. The rest is runtime, and here the leak is mechanical: every file the agent reads, every repo it greps,
every test it runs dumps its whole output into the context window — and you pay for that on *every* turn after, right up until
it gets summarized away. Most of it is noise the model glanced at once and never needed again: the 200-line `ls -la`, the stack
trace it read the top of, the `ps aux` dump it wanted one process out of. It all just sits there, costing tokens, forever. I
went at that from a few directions:

- **Rewrite noisy command output** into something compact before it ever reaches the context.
- **Compress and de-duplicate** whatever text is left over.
- **Handle compaction deliberately**, instead of turning the default summarizer loose on a long session.
- **Trim the model's own output**, since everything it writes costs tokens too — and lingers in the context after.

Two little Rust tools do most of the work — [`rtk`](https://github.com/rtk-ai/rtk) and
[`sqz`](https://github.com/ojuschugh1/sqz) — hanging off Claude Code's
[hooks](https://docs.claude.com/en/docs/claude-code/hooks) so it's transparent; I don't type anything different, the output
just shows up smaller. A bit of `CLAUDE.md` steering ties them together. First, the numbers.

As of this writing rtk has rewritten **5,708 commands and saved 2.6M tokens** — about 27% of everything it touched — and sqz
has compressed **1,335 payloads for another 125K**. That's real money, and more to the point real context I get to spend on
the actual problem instead of on log spam. The per-command receipts are almost comical:

- `ps aux` — **98.8%** smaller. The model wanted one process, not every daemon on the box.
- A `vitest` run — **93.5%**. Green checkmarks compress to nothing; only the failures carry information.
- `git commit` — **60.7%**, across 300-odd commits. That's a lot of boilerplate nobody reads.

By sheer volume the workhorse is `rtk read` — 408 file reads, nearly a million tokens saved on its own. Every unfiltered read
is output you rent for the rest of the session.

Now here's how I set it up, top to bottom.

### Install and wire the hooks

Both are single binaries — [rtk](https://github.com/rtk-ai/rtk) and [sqz](https://github.com/ojuschugh1/sqz); grab them from
their repos (mine came off Homebrew). The wiring is one command each, because both ship an `init` that writes the Claude Code
hooks for you:

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

That's the whole transparent layer. If you'd rather see it before you trust it, that block is exactly what `init` writes —
you can paste it by hand instead.

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

The same idea works on the web, not just the disk. When Claude needs something off a page, the naive path is to fetch raw
HTML — nav bars, script tags, tracking pixels, the whole DOM — and let the model dig the actual content out of the soup,
paying for every byte of markup on the way. I run [Firecrawl](https://www.firecrawl.dev/) instead, which returns clean
Markdown: same page, [roughly 94% fewer input tokens](https://www.firecrawl.dev/blog/claude-code-token-efficiency). It's the
disk-read lesson pointed at the network — hand the model the content, not the container.

### Keep the config itself lean

Here's the trap I walked into early: I plugged all this leaking tool output, then quietly re-created the problem in my own
config. `CLAUDE.md` is loaded into the context on *every* turn, forever — it's part of the system prompt. So is every rule
file that applies. A bloated config is a tax you pay on every message of every session, and it's the easiest one to stop
noticing, because you wrote it yourself.

Anthropic's own [guidance on `CLAUDE.md`](https://claude.com/blog/using-claude-md-files) is blunt about it: "It's tempting to
create a comprehensive `CLAUDE.md` right away. Resist that urge." Start simple, expand deliberately, and only add a rule that
solves a real problem you actually hit — not a theoretical one. When it gets long, the fix isn't to cram harder; it's to
"break up information into separate markdown files and reference them." Which is what I did, but with a twist that makes it
nearly free.

The twist is path scoping. My language rules don't live in `CLAUDE.md` — they live in `~/.claude/rules/`, one file per
language, each with a `paths:` glob in its frontmatter:

```markdown
---
paths:
  - "**/*.py"
  - "**/*.pyi"
---
* always use uv
* ruff for format + lint
* annotate every function signature — all params + return (incl. `-> None`)
* avoid `Any` — prefer precise types, protocols, or generics
```

Claude Code only loads a rule file when I actually touch a file that matches. Edit a stylesheet and `css.md` comes in; the
Python, TypeScript, and Swift rules stay on disk, where they cost nothing. A shared `general.md` (globbed to every source
extension) carries the cross-language principles, and each language file stacks its specifics on top only when relevant. So
the context holds exactly the rules for the code I'm looking at and not a byte more — the Firecrawl folks measured this pattern
at [a 41% cut](https://www.firecrawl.dev/blog/claude-code-token-efficiency) in rules overhead, and it tracks.

Then there's the stuff I never want the agent to read at all, and two lists handle it — one advisory, one enforced.
`.claudeignore` keeps generated junk out of context by convention — `node_modules/`, `dist/`, `build/`, `*.min.js`, `*.lock`,
everything that's compiled output or a dependency I'll never hand-edit. And the `permissions.deny` block in `settings.json` is
the version with teeth, doing double duty:

```json
"deny": [
  "Read(~/.ssh)", "Write(~/.ssh)",
  "Read(./.env)", "Read(./.env.*)", "Read(./secrets/**)", "Read(./config/credentials.json)",
  "Read(node_modules/**)", "Read(dist/**)", "Read(build/**)", "Read(*.lock)", "Read(./.idea/**)"
]
```

Half of that is security — there's no version of "the agent reads my `.ssh` keys or my `.env`" that ends well, so it simply
can't. The other half is the same token hygiene as the ignore file, but enforced: a `.lock` file is 10,000 lines of pinned
hashes no human reads and no model needs, and denying the read means it can never accidentally slurp one into the context to
answer some unrelated question.

### Keep the context clean

No matter how lean the input, a long session accumulates. The single best thing you can do about it is boring: clean the
context, aggressively. That's almost verbatim the advice from [this token-saving
writeup](https://mydataschool.com/blog/how-to-save-tokens/) — its fourth trick is literally titled "Clean the context.
Aggressively." — and the reasoning is worth internalizing. Every turn you keep, the model re-reads the entire conversation, so
token counts grow almost quadratically. The instinct is to hoard context in case the model forgets something. Resist it. A
focused short session beats a sprawling long one every time.

In practice that's two habits: `/compact` right after an exploration phase, once the useful conclusion has crystallized and
the forty file reads that got me there are just ballast; and a brand-new session whenever I switch tasks, rather than dragging
the old one along. Thariq's notes push this into a real discipline — his sharpest single test for any pile of tool output is
also the whole argument for handing work to a subagent:

> Will I need this tool output again, or just the conclusion?
>
> *— from [Thariq's notes on session management and 1M context](https://github.com/shanraisshan/claude-code-best-practice/blob/main/tips/claude-thariq-tips-16-apr-26.md)*

The mechanics of compaction I mostly automate. `sqz init` wired two hooks for it — one on `PreCompact`, one on session
resume — so when Claude Code does compact a long conversation, it's handled deliberately instead of by the blunt default.
Nothing to configure there; init sets it up. The only knob I turn by hand is the auto-compact window, so it fires less often:

```json
"env": { "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "400000" }
```

Fewer compaction cycles, and the ones that do fire are working on a context that's already been tidied.

The last piece is remembering across the clears. Wiping a session to save tokens is a great idea right up until you throw away
the one fact you needed. So I lean on Claude Code's own [memory](https://docs.claude.com/en/docs/claude-code/memory) — a small
index file plus one fact per file, written deliberately — and on [memsearch](https://github.com/zilliztech/memsearch) for
semantic recall over past sessions, so the durable stuff (a decision I made, a gotcha I hit, who the project is even for)
survives a `/clear` and gets pulled back in on demand instead of living rent-free in every context window. Clearing hard only
works if the things worth keeping have somewhere to land.

### Trim the output side too

Everything so far works on what comes *into* the context — command output, file reads. But the model's own responses cost
tokens as well, both when it writes them and on every turn after, and that's just as tunable with a few lines of `CLAUDE.md`:

```markdown
## Output Style
Fragment-first. Drop filler (just/really/basically/actually/simply), pleasantries, hedging.
Short synonyms over verbose. Technical terms exact. Code blocks unchanged.
Clarity > brevity when they conflict (e.g., articles in docstrings and error messages).
```

Fragments over full sentences, no "Great question!", no hedging throat-clearing. The one guard rail is that last line:
clarity wins when it fights brevity, so it doesn't start dropping the articles that make an error message or a docstring
readable. It's the cheapest measure here — no install, no binary, just telling the model to talk like it's paying by the word.
Which it is.

### Doing the same in another agent

Neither tool is really Claude-only. Both `init` commands can target agents besides Claude — run `rtk init --help` and
`sqz init --help` and you'll see the flags — so for the tools themselves, porting can be as small as a different one. For
anything without a turnkey installer, here are the four hooks-into-the-workflow to go looking for, roughly in order of how
universally they exist:

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

### Just starting to make my own skills

All of this — Superpowers, the rules files, even the little site-voice skill I wrote to keep this blog from sounding like a
press release — has me sold on skills as the real unlock, and I'm only just starting to build my own. The token argument for
them is almost unfair. At session start Claude reads only each skill's name and one-line description, something like 30 to 100
tokens each; the full body loads only when the model decides it's relevant. As the Firecrawl writeup puts it: "Everything
added to `CLAUDE.md` is paid every session forever. Skills with correct descriptions are paid only when needed." That's
progressive disclosure applied to capability — I can have dozens installed and pay for exactly the ones a given task touches.
The catch is that the description has to be precise enough for the model to pattern-match against, or the skill never fires.

The first real one I built wraps the [4+1 architecture](https://en.wikipedia.org/wiki/4%2B1_architectural_view_model)
model — Kruchten's old idea of describing a system as five separate views (logical, process, development, physical, and
scenarios to tie them together) instead of one overloaded diagram trying to show classes, deployment, and runtime all at once.
It's the kind of thing I know how to do but do inconsistently, which is exactly what a skill is for: encode the discipline
once, trigger it when I'm actually writing an architecture doc. The next one I'll probably make wraps
[repomix](https://github.com/yamadashy/repomix) — it "packs your entire repository into a single, AI-friendly file," with
token counting and a Tree-sitter `--compress` mode, which is the right tool for pointing Claude at an existing codebase and
asking real questions about it.

Which, honestly, I haven't needed much yet — because so far it's been almost all greenfield. I've spent this whole stretch
building out ideas I've had kicking around for years and finally have the leverage to knock out in an afternoon. Scanning and
understanding big existing repos is the next frontier; for now I've been happily catching up on my own backlog.

### The dashboard that keeps me honest

You can't manage what you can't see, and the token windows that actually bite — the 5-hour session limit and the weekly one —
are invisible until you slam into them. So I built the numbers into my statusline. Claude Code hands your statusline command a
JSON blob on every tick — model, context percentage, git state, and crucially `rate_limits.five_hour` and `.seven_day` — and
whatever your script prints becomes the line. Mine is a bash script styled after my old
[Prezto Sorin](https://github.com/sorin-ionescu/prezto) shell prompt so it feels like home: blue folder, git branch with the
Sorin status glyphs (ahead, behind, staged, modified, untracked, stashed), and then the Claude-specific stuff — the model, a
ten-cell context bar with a percentage, session age, and both rate-limit windows with a countdown to reset.

That last part is the one that changed my behavior. Seeing `5h:62%(↺1h20m)` parked in the corner turns an abstract limit into
a gauge I glance at, the way you watch a fuel needle. I cribbed the approach from two writeups worth reading if you want to
roll your own — [Daniel Mackay's walkthrough](https://www.dandoescode.com/blog/claude-code-custom-statusline) of the
JSON-to-shell contract, and [Gordon Beeming's multi-line version](https://github.com/GordonBeeming/claude-statusline) for the
fancier layout ideas — and then bent it to look like the prompt I've stared at for a decade.

### Where it landed me

The funny part is where all this ended up. I run Opus 4.8 almost exclusively now — the biggest, most capable model on
offer — which a year ago would have been a reckless way to torch a plan. But between building the right thing the first time,
keeping the config lean, cleaning the context hard, and compressing everything that's left, I have a genuinely hard time
hitting the 5-hour session limit anymore, never mind the weekly one. That's the whole game: spend the savings on a smarter
model doing the actual work, not on log spam nobody reads.

It's living plumbing, so it'll keep shifting — the numbers climb every session and I keep finding new places to trim. But the
shape holds: don't build the wrong thing, don't load what you don't need, don't keep what you're done with, and compress the
rest.

### Sources

- [12 Ways to Cut Token Consumption in Claude Code](https://www.firecrawl.dev/blog/claude-code-token-efficiency) — Firecrawl
- [Using CLAUDE.md files](https://claude.com/blog/using-claude-md-files) — Anthropic
- [claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice/tree/main/best-practice) — a
  continuously-updated reference collection
