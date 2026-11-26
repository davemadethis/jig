# Inbox and designer rules

## Inbox

`.jig/inbox/` holds messages to this repo's hubnode, one Markdown file each, written by the
session that sends it (`<YYYY-MM-DD>-<slug>.md`), with a header naming it `inbox: true`, `to` (a
repo name or alias from `jig repos`), `from` and `sent`. Like staging, it is never committed.
A message is not a staged file: it is read and done with, never landed or resolved, and
nothing else (a commit, a gate, a release) looks at the inbox. It is one-way, to the hubnode;
the hubnode answers only through the owner.

`jig inbox`, in the trunk checkout only, prints each unread message in full, oldest first, and
moves it to `.jig/inbox/read/`, where it can be read again. A message whose `to` isn't this repo
is moved to `.jig/inbox/misaddressed/` and named: it is no ruling here, and the owner places it. A tool may announce unread messages with each
of the owner's prompts, but only `jig inbox` marks one read, and it refuses outside the trunk
checkout: a subnode marking a message read would hide a ruling from the hubnode. In a message, the owner's own words appear as
`The owner, <date>: "<words>"`; those are the owner's ruling, as if given in the hubnode's own
conversation, and the rest is context from the sender. They settle everything but a fixed rule's
word (`rules-staging.md`, Staging), which only the owner's reply in the hubnode's conversation gives. Before acting on one, the hubnode checks
the state it answers, as for any reply that may have gone stale. What it rules lands where any
ruling does: a decision entry, a spec, the board.

A typed repo name, wherever jig takes one (a staged file's `target`, a message's `to`), is a
name or alias in `jig repos`, or the name a listed checkout gives itself, with case ignored. A
name more than one entry answers to finds none, and is refused naming them. One that matches only once punctuation is
dropped (`a_p` for `ap`) is refused, naming the near one: two near-identical names have sent
work to the wrong repo. `jig repos alias <repo> <alias>` adds an alias, and refuses one any
other entry already answers to, its checkout's own name included, as `add` and `rename` refuse
such a name, and `add` refuses a checkout whose own name another entry answers to; `jig repos which
<name>` prints the repo a typed name finds, or the refusal. `jig inbox check <file>…` checks a
message's header from outside any repo, as `staging check` does: a missing key, a `to` no entry
answers to, or, for a file already in a listed repo's inbox, a `to` naming another repo.

## Designers

A **designer** is a design session for one product repo, kept outside it: it holds the owner's
running record of the product and drafts what the repo will get. Its folder lives outside every
repo, so no repo session can open it, and the owner's repos list points to it from the repo's
entry (`jig designer <repo>`, run by the designer when it starts). A designer reaches its repo only
by staging and by the inbox; it never edits a repo. A metarepo has no designer: its pararepos'
designers stage to it.
