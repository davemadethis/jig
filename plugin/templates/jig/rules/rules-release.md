# Versioning and release rules

## Versioning

jig repos use `MILESTONE.FEATURE.PATCH`. A version says how much the product changed: what it is, or what it offers the people who use it. "The product" is what the repo makes: the software in a regular repo or a pararepo, and the product definition in a metarepo.

- **X — Milestone (`+1.0.0`).** The product's identity, architecture or core experience changes shape. *Code:* a rewrite of the core engine, a new platform, an overhaul of the interface. *Metarepo:* a product added, merged or retired; a principle reversed; a core model replaced.
- **Y — Feature (`+0.1.0`).** A new capability, or a change in what the product offers or how it is used. *Code:* a new feature set, a redesigned workflow, a new integration. *Metarepo:* a decision accepted or superseded that changes what a product offers; a new product, feature or concept page; a glossary term for a new thing. Rule of thumb: it earns a highlight in the release notes.
- **Z — Polish (`+0.0.1`).** Nothing the product offers changes. *Code:* fixes, small tweaks, copy, dependency bumps, performance, refactors. *Metarepo:* wording, pointers, file moves and renames with no change in meaning, a claim moved down to its pararepo with no change in meaning, a name's status, Open questions, struck project-scope entries, research marked Proposed. *Pararepo:* a pin bump on its own.

**What others must do doesn't count.** A change a reader has to act on still gets a `**Breaking:**` line saying what to change, but it doesn't raise the level. A metarepo release sends each pararepo whose citations the release broke a pin-bump request with its rewrite list, whatever the level.

**Choosing the level.** A release takes the highest level of any change in it. The hubnode proposes the level with a one-line reason, and the owner's word releases it.

A repo published to a package registry, whose users expect SemVer, needs a rule of its own; jig has none yet.

### Before 1.0.0

*Only for a repo whose latest release is `0.y.z`. A repo at `1.0.0` or later skips this section.*

Y and Z work as above, and X stays 0. Releasing `1.0.0` is the owner's call that the core is complete and the product is ready for general use. Before that, a change that would be a Milestone is a Y.

## Release

`jig release` runs the repo's own protocol. On trunk, with a clean tree and nothing staged, it
runs `.jig/scripts/check.sh`, then `.jig/scripts/release.sh <version>`: the build and the version
bump, which only the repo knows how to do. It commits the tracked files the script changed,
checks that each glob in `release.artifacts` matched a file, turns `## Unreleased` in
`.jig/decisions.md` into `## vX.Y.Z - YYYY-MM-DD` with an empty one above it, and tags
`vX.Y.Z`. A failure puts the tracked files back and tags nothing. The version is the last tag
bumped by `--patch` (the default), `--feature` or `--milestone` (Versioning); the first is `--version X.Y.Z`, or `--feature` (0.1.0). Before 1.0.0, `--milestone` refuses: `--version 1.0.0` is the owner's call. `--minor` and `--major` still work, as `--feature` and `--milestone`.

In a plain repo, until `release.sh` has steps and `config.json` names its artifacts, the release
refuses and points to `/jig:release`, which asks what the repo builds and ships. A metarepo and
a pararepo release with defaults: steps and artifacts are optional (any that are given still run
and must match), and jig's own checks run before the tag. A metarepo's are its history checks
(`rules-metarepo.md`). A pararepo's refuse when the metarepo can't be reached (`jig repos add meta`), when the
pin isn't one of its releases (`main`, a hand-made tag), when the `AGENTS.md` header isn't the
generated one (P1), when `.jig/meta-cache/` is tracked (P3), or when a `buffer.md` row is neither
Open nor Closed or shares its id (P2); a newer metarepo release, a cited path outside
`contract_paths`, or a metarepo pointer to a file or heading this repo doesn't have, is reported as `jig sync` reports it and refuses nothing. So is a staged pin-bump request:
the release names it, and isn't held by it. Then the release
settles the sync buffer (`rules-pararepo.md`, The sync buffer).

After the tag, the release runs `.jig/scripts/publish.sh <version> <artifact>…`: what the repo
sends out (a push, a hosted release, a store upload), with the files this run built as paths
from the repo root. While the script still holds its `# TODO: publish steps.` line, the
publish isn't decided yet: jig skips it and prints the push command. A repo that publishes
nothing deletes the line. A publish that fails leaves the tag, which may already be pushed:
jig prints the command to run it again and exits 1.
