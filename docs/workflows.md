# Workflows

Every session in a jig repo is a node, and every step it takes belongs to a
[workflow](glossary.md#workflow) and a [role](glossary.md#role). The workflows are data inside
`jig.py`, so jig knows each [job](glossary.md#job)'s next step and who takes it. It refuses a
step taken out of order.

## Nodes

There are two kinds of node. The [hubnode](glossary.md#hubnode) is yours. It owns
[trunk](glossary.md#trunk), writes a [spec](glossary.md#spec) only when one comes straight
from your conversation, and runs every [gate](glossary.md#gate) and merge. A
[subnode](glossary.md#subnode) is every other session. Each node runs at a model
[tier](glossary.md#tier) and an [effort](glossary.md#effort), two numbers explained below.

| Node | Settings | What it does | Roles it may load |
|---|---|---|---|
| hubnode | the owner's session; tier 2, effort 1 or better | talks, decides, assigns, gates, merges, releases, pushes, publishes | spec (only for specs drafted from the conversation) |
| subnode | the role's | takes one role on one job, works only in its worktree, reports back, never touches trunk | any of the five |

## Roles

A subnode takes one of five roles. Each runs at its own tier and effort. The work role builds and makes each
[handoff](glossary.md#handoff). The check role runs the complete suite, once per gate or per
[batch](glossary.md#batch).

| Role | Tier, effort | Steps it owns |
|---|---|---|
| spec | 2, 2 | spec, consolidate |
| bug | 2, 1 | bug, then the spec for what it found |
| work | 2, 3 | work, handoff, fixes, hand-resolved syncs |
| review | 2, 2 | review-work (the job's whole diff), review-change (only what changed since the last review); always a fresh session |
| check | 3, 4 | check (the complete suite, before a release too), trace a failed batch, survey |

The hubnode's own steps belong to no role: assign, gate, merge, release, push and publish. jig
itself, with no model, refuses a step out of order. It also removes a merged job's clean
worktree and branch.

## Tiers and efforts

Tiers and efforts are numbers, and `plugin/tiers.json` maps them to models and effort levels. A
lower number is stronger. So when a new model ships, one file changes and the rules don't.

`python3 .jig/jig.py roles` prints each role's settings in effect. A repo can set its own in
`roles` in `.jig/config.json`, each with its reason.

## The workflow table

`→` continues a session that already exists. `⇢` starts a new one.

| Workflow | Steps | Starts on | Controls |
|---|---|---|---|
| Job | spec ⇢ work ⇢ review-work → handoff → gate ⇢ check → merge | `python3 .jig/jig.py open` | merge only on the owner's word |
| Fix | work ⇢ review-change → handoff | a review with blocking findings | three strikes: a job's third blocking review starts Bug |
| Sync | work ⇢ review-change → handoff | a sync with a hand-resolved conflict | a clean sync needs nothing |
| Bug | bug → spec ⇢ Job | a job's third blocking review, a feedback group, or the owner's `/jig:bug` | never on a session's own reading that something is broken |
| Feedback | consolidate ⇢ bug + spec → consolidate ⇢ Job | staged feedback, in the jig repo | one bug + spec per group; overlaps answered before any job opens |
| Batch | gate → merge ⇢ check → trace | two or more gated jobs | one check on trunk; a failure is traced to its merge, then Fix on that job |
| Release | check → release → push → publish | the owner's word | refused while a batch check is owed; push and publish only on the owner's word |
| Survey | survey ⇢ spec ⇢ Jobs | `/jig:survey`, `/jig:adopt`, `/jig:update` | |
| Redocument | spec ⇢ Jobs ⇢ Batch ⇢ Job | `/jig:redocument` | the spec is the remap; the last job is the cleanup |

Some things are fixed, whatever the config says. Merge, push and publish wait for the owner's
word. Every review runs in a fresh session. A release always gets a complete check first.

`python3 .jig/jig.py flows` prints the same table from the data.

## Next step

`python3 .jig/jig.py next` names each job's next step and who takes it. It also says whether
that step continues a session or starts a new one. The hubnode reads it before assigning
anything.

## The rig

`/jig:rig` is the hubnode's front door. It shows one picture: what can start now, what waits on
what, what waits on you, and the roadmap's next step. Then it asks you one batch of decisions
and acts on your answers. `/jig:rig auto` writes the specs and starts the jobs it can without
asking, and leaves your questions open for later.

## The drawing

The same nodes, roles and workflows, drawn from the data in `jig.py` by `scripts/roles_svg.py`.
A check fails when the drawing and the data disagree.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/roles-and-flows-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="../assets/roles-and-flows-light.svg">
  <img src="../assets/roles-and-flows-light.svg" alt="Roles: the hubnode (the owner's session) assigns, gates, merges, releases, pushes and publishes; a subnode takes one role, outside the trunk checkout; spec (tier 2, effort 2) writes and consolidates specs; bug (2,1) investigates and writes the spec for what it found; work (2,3, one session per job) builds, hands off, fixes and syncs; review (2,2, always a fresh session) runs review-work and review-change; check (3,4) runs the complete suite, before a release too, traces a failed batch and surveys; jig itself refuses steps out of order and cleans up after a merge. Workflows: Job is spec, work, review-work, handoff, gate, check, merge; Fix and Sync are work, review-change, handoff; Bug is bug, spec, then a Job; Feedback, Batch, Release, Survey and Redocument follow, each with its starting point and controls. The tables below say the same in text.">
</picture>
