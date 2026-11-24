# <task name>

Source: <who asked or reported, when; for a bug, the symptom in their words>
<!-- A line of its own here, `Scope: <phase>/<scope>, …`, naming the roadmap ids this task
     takes (`No phase/<id>` for an item). No id taken: no line. -->
<!-- A line of its own here, `Later: <id>, …`, naming the roadmap ids this task leaves for
     later work, each already on trunk's roadmap (a roadmap change on the owner's yes puts a
     new one there). Nothing left for later: no line. -->

## Intent
One or two sentences. What should be true when this is done that isn't true now.

## Done when
- [ ] observable check 1 (a test, a command output, a thing on screen)
- [ ] observable check 2

## Out of scope
<!-- Work nothing will do, or work another named spec, job or repo does, each with why. Work
     left for later is a `Later:` id, never a line here: this section closes with the spec. -->
- what this task deliberately does not touch

## Touches
- files / modules expected to change

## Alternatives considered
<!-- Required for any fix. Proof you looked one layer up. -->
- <sibling path or correction> — rejected because <reason> — reason is [seen|assumed]

## Decisions
- anything chosen during the work that someone would ask "why?" about later

## Roles
<!-- `python3 .jig/jig.py roles`'s output when this spec was written, as printed. The
     repo's settings, not this task's: never edit a role here. -->
