# README rework and a docs/ folder

Source: claude.ai chat (Squarish Projects), 2026-11-19 to 2026-11-20, Dave with Claude (staged as readme-and-docs.md): "I think the whole thing needs it's own /docs folder so the readme can also be more brief and point to docs, your workflow example is a good one."

## Intent
The owner, 2026-11-19: "Let's take out the comparison entirely, I'd rather this be a humble ode
to jig than a marketing stunt." "And agree the setup and walkthrough is CRUCIAL and missing."
"I've noticed the run-on sentences, too."

Restated: the README becomes a short front page (pitch, install, a first job walked through,
links), the detail moves into a new `docs/` folder, the comparison is gone, and every sentence
reads cleanly.

## Done when
Run from the job's worktree root. Each check prints nothing unless it says otherwise.

- [ ] **Order.** `grep -n '^## ' README.md` shows, in order: the install section (requirements
  included), the first-job walkthrough, the links into `docs/`, then the short feedback and
  development section. Above the first `##` sits the title and a pitch of two short paragraphs.
- [ ] **No comparison.** `grep -n 'Compared to other toolkits\|Superpowers\|mattpocock\|Kiro\|ECC' README.md docs/*.md`
- [ ] **Install line.** `grep -c 'claude plugin marketplace add davemadethis/jig\|claude plugin install jig@davemadethis' README.md` prints `2`.
- [ ] **No `## Up next`.** `grep -rn 'Up next' README.md docs/`. Parked work is a `## No phase` item in `.jig/roadmap.md` now.
- [ ] **One flow line.** `grep -rn 'plan → do' README.md docs/`. The Job line in `docs/workflows.md` matches the Job line `python3 .jig/jig.py flows` prints, and the roles and workflows tables match `python3 .jig/jig.py roles` and `python3 .jig/jig.py flows`.
- [ ] **Full command form.** `grep -nE '`jig [a-z]' README.md docs/*.md` (every quoted command is `python3 .jig/jig.py …`).
- [ ] **Commands exist.**
  `grep -ohE 'python3 \.jig/jig\.py [a-z-]+' README.md docs/*.md | sort -u | while read -r _ _ c; do python3 .jig/jig.py "$c" --help >/dev/null 2>&1 || echo "no command: $c"; done`
  and
  `grep -ohE '/jig:[a-z-]+' README.md docs/*.md | sort -u | while read -r s; do [ -d "plugin/skills/${s#/jig:}" ] || echo "no skill: $s"; done`.
  Each flag quoted after a command shows in that command's `--help`.
- [ ] **Owner-only marked.** `docs/commands.md` marks as owner-only exactly the skills
  `grep -l 'disable-model-invocation: true' plugin/skills/*/SKILL.md` lists (today: adopt, feedback,
  init, redocument, relay, release, repos, rigger, send, update), and no others.
- [ ] **Links resolve.** This prints nothing:
  ```
  python3 - README.md docs/*.md <<'PY'
  import os, re, sys
  slug = lambda h: re.sub(r'[^\w\- ]', '', re.sub(r'[`*]', '', h).strip().lower()).replace(' ', '-')
  for f in sys.argv[1:]:
      for t in re.findall(r'\]\(([^)\s]+)\)|(?:src|srcset)="([^"]+)"', open(f).read()):
          t = t[0] or t[1]
          if re.match(r'[a-z]+:', t): continue
          p, _, a = t.partition('#')
          q = os.path.normpath(os.path.join(os.path.dirname(f), p)) if p else f
          if not os.path.exists(q): print(f, 'missing', t)
          elif a and q.endswith('.md') and a not in {slug(h) for h in re.findall(r'^#+ (.+)$', open(q).read(), re.M)}: print(f, 'no anchor', t)
  PY
  ```
- [ ] **Terms.** Each of job, board, gate, handoff, hubnode, subnode, trunk, scope, page
  contract, metarepo, pararepo, rigger, tier and effort has a `## <term>` heading in
  `docs/glossary.md`. So does every other jig term the README or a page uses (role, workflow,
  spec, owns and shares, phase, staging, the decision log), each saying what it is and what it is not.
  For each term, `grep -n -m1 -i '<term>' README.md` and the same on each page shows the first use
  defining it in that sentence or linking it to `docs/glossary.md#<term>` (a page links `glossary.md#<term>`).
- [ ] **The refusal is real.** The walkthrough's refused commit and its message come from this run,
  with the walkthrough's own job and file names. Its output's `jig: R3 …` line appears verbatim in `README.md`:
  ```
  S=$(mktemp -d); export JIG_CONFIG=$S/repos.json XDG_CONFIG_HOME=$S/cfg
  cd $S && git init -q -b main && git config user.email t@t && git config user.name t
  cp -r <worktree>/plugin/templates/jig .jig && cp <worktree>/plugin/templates/{AGENTS,CLAUDE}.md .
  # the walkthrough's files, committed; then python3 .jig/jig.py init, commit the board,
  # write and commit the spec, python3 .jig/jig.py open <job> --spec … --owns <file>,
  # commit .jig/jobs.json on trunk (the hook reads trunk's board), then in the job's
  # worktree edit the owned file and one it doesn't own, and git commit.
  ```
  On 2026-11-23 the spec role ran this with job `greeting` owning `src/app.py` and a stray edit to
  `src/other.py`. The hook printed `jig: R3 src/other.py is not job greeting's: ask the hubnode to add it to shares`, exit 1.
- [ ] **Sentences.** This prints nothing, or only lines the reviewer confirms are list items the
  script ran together:
  ```
  python3 - README.md docs/*.md <<'PY'
  import re, sys
  for f in sys.argv[1:]:
      t = re.sub(r'```.*?```', '', open(f).read(), flags=re.S)
      t = ' '.join(l for l in t.splitlines() if not l.lstrip().startswith(('|', '#', '<')))
      for s in re.split(r'(?<=[.!?])\s+', re.sub(r'\s+', ' ', t)):
          if len(s.split()) > 30: print(f, len(s.split()), s[:80])
  PY
  ```
- [ ] **Pages pass jig's own rules.** `python3 .jig/jig.py rules` passes on the job's last commit
  (the hook refuses a page naming a root document, `.jig/specs/`, `.jig/handoffs/` or
  `.jig/roadmap.md`, and a doubled heading). Each page but the glossary opens with a lead
  paragraph and no heading named Overview, Notes, Misc or Changes:
  `grep -n '^## \(Overview\|Notes\|Misc\|Changes\)' docs/*.md`.
- [ ] **Trust.** `docs/hooks.md` names each plugin hook in `plugin/hooks/hooks.json` (four today: the format step after
  an edit, the check on stop, the inbox count on a prompt, the node line at session start).
  `README.md` keeps a two-line summary that links to it.
- [ ] **The picture's home.** `python3 scripts/roles_svg.py --check` passes. Its docstring and
  `.jig/scripts/check.sh`'s comment and failure message name `docs/workflows.md`, not the README:
  `grep -n README scripts/roles_svg.py .jig/scripts/check.sh`.
- [ ] **Marketplace.** `grep -n lanes .claude-plugin/marketplace.json`.
- [ ] **Plugin untouched.** `git diff --stat main -- plugin/`, and `grep -rn 'docs/\(glossary\|jobs\|workflows\|records\|metarepos\|commands\|hooks\)\.md' plugin/` shows no new line.
- [ ] `python3 .jig/jig.py queue -- .jig/scripts/check.sh` passes.

## Out of scope
- Any change under `plugin/`, including `plugin/.claude-plugin/plugin.json`'s description.
- A `jig` shim on the PATH (the owner chose the full form).
- `docmap` entries mapping the new pages to `plugin/**` (see Decisions).
- `AGENTS.md`'s lines naming `marketing/FEATURES.md` and `marketing/DIFFERENCES.md`, which don't exist on trunk. That's a follow-up for the hubnode.
- A decision-log line: the README and docs aren't in the plugin a release ships.

## Touches
- README.md
- docs/glossary.md
- docs/jobs.md
- docs/workflows.md
- docs/records.md
- docs/metarepos.md
- docs/commands.md
- docs/hooks.md
- scripts/roles_svg.py (docstring only)
- .jig/scripts/check.sh (comment and failure message only)
- .claude-plugin/marketplace.json

## The layout

| File | Holds |
|---|---|
| `README.md` | Title, a two-paragraph pitch, Install (requirements, the install line, `claude --plugin-dir` to try it), A first job (the walkthrough), Read more (one line per page below, plus `.jig/RULES.md` after init), a two-line On trust summary, Feedback and working on jig (today's section, shortened). |
| `docs/glossary.md` | Every term, `## <term>` each, per `.jig/RULES.md`'s glossary form: what it is and what it is not. |
| `docs/jobs.md` | Jobs: the board, owns and shares, worktrees, rules run from trunk's copy, handoff and its one fresh review, gate, merge, bug before fix, workarounds and their ledger. |
| `docs/workflows.md` | Nodes, roles and workflows: the picture from `assets/`, the three tables, tiers and efforts, `python3 .jig/jig.py next`, `/jig:rig`. |
| `docs/records.md` | What jig keeps in a repo: the one always-loaded file, pages and the page contract, the decision log, the roadmap, staging, releases. |
| `docs/metarepos.md` | Metarepos and pararepos: citations, sync, proposals, the buffer, moving a repo in. |
| `docs/commands.md` | Every command, grouped: setting a repo up (init, survey, adopt, update, redocument), day to day, the hubnode's, across chats (stage, repos, relay, send, rigger), release and feedback. Owner-only ones marked inline. |
| `docs/hooks.md` | The git hooks (what they refuse, the opt-in marker) and the plugin hooks: the whole On trust text. |

The walkthrough, in the README: `/jig:init`; `/jig:spec` on a small task; the hubnode opens the
job (`python3 .jig/jig.py open …`, then the board committed on trunk); the work session commits a
file the job doesn't own, and the hook refuses it, with the real message shown; `/jig:review`,
`python3 .jig/jig.py reviewed`, `python3 .jig/jig.py handoff`; `python3 .jig/jig.py gate`; the
merge on the owner's word. Each step says who runs it (you, the hubnode, a subnode).

## Alternatives considered
- The staged table's layout (getting-started, concepts, workflows, commands, features, trust) —
  rejected because this repo runs jig, so `docs/` is under its page contract: a page is named for
  a system and holds sections named for what that system has, never a genre such as getting
  started or features [seen: `.jig/docs-page.md`, `.jig/RULES.md` (Documentation)]. The glossary's
  home is `docs/glossary.md`, not `concepts.md` [seen]. Install and the walkthrough stay in the
  README, where the owner put them. The "What it does" items go to the pages whose system they
  describe, not to a features page.
- A `jig` shim — rejected by the owner (Decisions).

## Decisions
- The owner, 2026-11-23: "the docs/ table is a suggestion; the spec picks the layout". The layout is the one above.
- The owner, 2026-11-23: "use that order and walkthrough". README order: pitch (two short
  paragraphs), install with requirements, the first-job walkthrough, links into `docs/`. The
  walkthrough runs `/jig:init`, `/jig:spec` on a small task, opening the job, a commit outside the
  job's files refused by the hook (the real message), review, gate, merge.
- The owner, 2026-11-23: "write the full python3 .jig/jig.py form, no shim". Every command in the README and docs is `python3 .jig/jig.py …`.
- The hubnode, 2026-11-23: keep the flow line that matches `python3 .jig/jig.py flows`'s Job workflow
  (`spec ⇢ work ⇢ review-work → handoff → gate ⇢ check → merge`) and drop
  `spec → plan → do → commit … → merge`.
- The hubnode, 2026-11-23: each term is defined, or linked to its definition, before first use: job, board, gate, handoff, hubnode, subnode, trunk, scope, page contract, metarepo, pararepo, rigger, tier and effort.
- Voice: the README and pages are for people outside the repo, in the owner's voice. The work role
  writes them, then runs `/davewriter:davewriter` on each, then reruns the Sentences check. Aim
  under 25 words a sentence and split anything over 30.
- Interpreted: the "Compared to other toolkits" section goes whole (table and both paragraphs).
  Its last paragraph's point, that the prose is short and what must not be skipped lives in hooks,
  survives as a sentence in the pitch or in `docs/hooks.md`.
- Interpreted: README.md:44's `## Up next` sentence goes to `docs/records.md` as "parked work is an
  item under `## No phase` in `.jig/roadmap.md`", matching `.jig/RULES.md` (Roadmap).
- Interpreted: the README keeps a short feedback and development section after the links. It is
  for outsiders, and how this repo is worked has no home in `docs/`.
- Interpreted: the README keeps the "What it does" core as the pitch's substance (parallel jobs
  fenced by hooks, rules run from trunk's copy, bug before fix, one fresh review per handoff); the
  rest of that list moves to the pages.
- Interpreted: the `/jig:redocument` paragraph becomes one line in `docs/commands.md`.
- Interpreted: today's On trust text names three plugin hooks while `plugin/hooks/hooks.json` has
  four (SessionStart was added since). `docs/hooks.md` states all four.
- Interpreted: the drawing moves with the tables to `docs/workflows.md`, so `scripts/roles_svg.py`'s
  docstring and `.jig/scripts/check.sh`'s comment and failure message are updated to name it.
  `check.sh` is this repo's own script, not a file `/jig:update` writes, so AGENTS.md's ".jig/
  changes only by /jig:update" doesn't cover it. The hubnode can strike this if it reads that line otherwise.
- Interpreted: no `docmap` entries. Mapping the pages to `plugin/**` would put every page into
  every later jig change's fold-in. Whether jig's own docs move with its code that way is the
  owner's call, and the hubnode raises it after the merge.
- Interpreted: `.claude-plugin/marketplace.json`'s "parallel lanes" becomes "parallel jobs". It is
  the repo's marketplace file, not `plugin/`.
- Interpreted: pages name `.jig/` paths freely. jig is the product here, and `.jig/RULES.md` allows
  "a tool whose product is jig". `python3 .jig/jig.py survey` may list those lines, and that's expected.

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
