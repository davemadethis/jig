# Handoff: readme-and-docs

Commit: 0f7702dac287846621735d79b59332081a7d9e29
Date: 2026-11-23
Spec: .jig/specs/readme-and-docs.md
Review: tier 2, effort 3
Ran: claude-opus-5-5 at medium
Review-change: tier 2, effort 3
Review-change ran: claude-opus-5-5 at medium

## Built
<!-- what this delivers, in a few lines -->
README.md is now a short front page: a two-paragraph pitch, then Install (requirements, the
install line, --plugin-dir), A first job (nine steps from /jig:init to merge, with the real R3
refusal), Read more (links into docs/), a two-line On trust, and Feedback and working on jig.
The comparison section is gone. Seven new pages: docs/glossary.md, jobs.md, workflows.md,
records.md, metarepos.md, commands.md and hooks.md. scripts/roles_svg.py's docstring and
.jig/scripts/check.sh's comment and failure message now name docs/workflows.md.
.claude-plugin/marketplace.json says "parallel jobs" instead of "parallel lanes". Nothing under plugin/ changed.

## Done-when evidence
<!-- one line per spec item: the command run and what it printed -->
- Order: `grep -n '^## ' README.md` → 📦 Install, 🧭 A first job, 📚 Read more, 💬 Feedback and working on jig; two pitch paragraphs above.
- No comparison: the grep printed nothing.
- Install line: `grep -c …` → 2.
- No Up next: `grep -rn 'Up next' README.md docs/` printed nothing.
- One flow line: the `plan → do` grep printed nothing. The Job row in docs/workflows.md is `spec ⇢ work ⇢ review-work → handoff → gate ⇢ check → merge`, and the roles and workflows tables match `jig roles` and `jig flows`.
- Full command form: the `` `jig [a-z] `` grep printed nothing.
- Commands exist: both loops printed nothing. Each quoted flag (open --spec/--owns/--reserve, reviewed --tier/--effort/--blocking, checked --tier/--effort/--seconds, propose --withdraw, init --meta/--para, update --apply, roadmap --write) is in its command's --help.
- Owner-only: docs/commands.md marks exactly adopt, feedback, init, redocument, relay, release, repos, rigger, send and update, the set the disable-model-invocation grep lists.
- Links resolve: the script printed nothing.
- Terms: every required term, plus node, roadmap, batch, workaround and inbox, has a `## ` heading in docs/glossary.md. A first-use script finds each term's first line in every file linked to the glossary. The exceptions are the page titles `# Jobs`, `# Workflows` and `# Metarepos`, where the next sentence links the term.
- The refusal is real: run in a scratch repo with JIG_CONFIG and XDG_CONFIG_HOME set, it printed `jig: R3 src/other.py is not job greeting's: ask the hubnode to add it to shares`, exit 1. That line is verbatim in the README. ~/.config/jig was untouched (mtime 08:37).
- Sentences: the script printed nothing (rerun after the davewriter pass and after every reword).
- Pages pass jig's rules: `python3 .jig/jig.py rules` → ok on 0f7702d. The Overview/Notes/Misc/Changes grep printed nothing, and every page but the glossary opens with a lead paragraph.
- Trust: docs/hooks.md names all four plugin hooks (after an edit, when the agent stops, with each prompt, at session start). README keeps a two-line On trust that links docs/hooks.md.
- The picture's home: `python3 scripts/roles_svg.py --check` → ok, and the README grep on roles_svg.py and check.sh printed nothing.
- Marketplace: the `lanes` grep printed nothing.
- Plugin untouched: `git diff --stat main -- plugin/` is empty, and the docs-path grep in plugin/ counts 27 lines, the same as main.
- `python3 .jig/jig.py queue -- .jig/scripts/check.sh` → exit 0.

## Review
<!-- findings from the adversarial review, and what you did about each -->
Round 1, review-work of 74f86a8: 4 blocking, all fixed in d91b455.
- B1: the walkthrough left out filling in and committing the handoff note. Added.
- B2: there were no check, `checked` or `mark gated` steps between gate and merge. Added to the README and docs/jobs.md.
- B3: "plugin hooks run only in an opted-in repo" was false for session-start. Fixed.
- B4: merge prints "Sync the clean jobs" and syncs nothing itself. Fixed.
- I also took S1–S6 (who starts each session; only append files resolve themselves; alt text "above"; drop "except it's enforced"; Node and Roadmap glossary terms; drop the roles_svg and check sentences) and O1–O3 (tone down "every cut lands"; `--withdraw <branch>`; owner-only wording).
- O4 ("Starts on" vs flows' "trigger:") and O5 (the hooks slogan the spec asked to keep) are left as they are, on the hubnode's word.
Round 2, review-change of d91b455: 1 blocking, fixed in 82ef7b5. The opt-in sentence said "three hooks run your repo's scripts", but only two do. Also fixed: `reviewed` needed --tier/--effort so the gate doesn't warn. 0f7702d split the sentence that made too long.
Round 3, review-change of 0f7702d: 0 blocking.

## Fold-in
<!-- Every documentation page that covers code this changed: does it still describe the
     code? Replace each ___ and tick the box: the stale sentences are edited (deleting
     counts), or none went stale and this says why. Each roadmap item naming one of those
     pages (an Up next item, or a taken scope) has its own line: keep one answer, built,
     untouched or departed: <why>. An Up next item answered built leaves the roadmap when
     the job merges. The gate refuses an unanswered line. An UNOWNED file has no page
     covering it: add it to docmap in the board, or say why it needs none. A pair line
     (`<id> vs <log> § <ids> (<page>): ___`) is answered after its colon, once for every id
     on it: agrees, narrows: <how>, or conflicts: <resolution>; on a line of several ids,
     narrows and conflicts name at least one of them. jig reads the rest of the line, so it
     stays as jig wrote it. -->

- [x] UNOWNED scripts/roles_svg.py — add to docmap (a new page starts from .jig/docs-page.md), or no page needed because it is this repo's own dev script, which draws docs/workflows.md's picture (the repository's own tooling, its build, CI, release and dev scripts, needs none)

## Shared files changed
<!-- each shared/common file, and why this job had to touch it -->
- scripts/roles_svg.py: docstring only, to name docs/workflows.md now that the drawing lives there.
- .jig/scripts/check.sh: comment and failure message only, for the same reason.
- .claude-plugin/marketplace.json: "parallel lanes" → "parallel jobs", to match the README's term.
Departures from the spec, all judged sound in review-work:
1. Pages never name `.jig/roadmap.md`, `.jig/specs/` or `.jig/handoffs/`, because the hook refuses a docs/ line that does. docs/records.md says "the roadmap's `## No phase` section".
2. The pages describe plugin/templates/jig/RULES.md (the product), which is newer than the installed .jig/RULES.md.
3. The workflows table's "Trigger" column is "Starts on", and the drawing sits at the end of docs/workflows.md. This keeps the first-use term check clean: "trigger" contains "rigger".
4. In docs/commands.md, /jig:hardware writes "a circuit's page", so "board" keeps its jig meaning.
Found by running the walkthrough end to end: after `mark greeting gated`, the hubnode has to commit .jig/jobs.json on trunk, or `merge` refuses with "commit or stash first". README step 8 and docs/jobs.md say so.

## Test by hand
<!-- what a person should click or watch -->
Read the README on GitHub: the picture on docs/workflows.md renders in light and dark, and the glossary links land on their headings. Follow the nine walkthrough steps in a throwaway repo. The reviewer did, and it ran through to a successful merge.

## Left
<!-- what remains on this job -->
Nothing on this job. Follow-ups for the hubnode, from the spec: whether to map the new pages in docmap (the owner's call), and AGENTS.md's marketing/ lines (ignored on the brief's word).
