#!/usr/bin/env bash
# Two levels. With no argument this is the quick check: it runs on every stop (the hook's
# limit is 300s), and while working, beside the smoke sections a change touched. With --full
# it adds the complete suite: the check role runs that once per gate, or once per batch on
# trunk. Exit 2 blocks the agent from finishing; stderr is shown to it.
set -u

fail() { echo "check: $1" >&2; exit 2; }
# No bytecode beside the source: roles_svg.py imports jig.py, and smoke copies whatever lands in
# plugin/templates/jig/ into every .jig/ it makes.
export PYTHONDONTWRITEBYTECODE=1

# --- quick -----------------------------------------------------------------
claude plugin validate ./plugin >/dev/null 2>&1 || fail "plugin invalid (claude plugin validate ./plugin)"
# compile() rather than py_compile, which writes __pycache__ beside the source whatever
# PYTHONDONTWRITEBYTECODE says, and smoke copies that folder into every .jig/ it makes.
python3 -W error -c 'import pathlib, sys
for f in sys.argv[1:]: compile(pathlib.Path(f).read_text(encoding="utf-8"), f, "exec")' plugin/templates/jig/jig.py scripts/roles_svg.py || fail "jig.py does not compile"
# README's "Who does what" pictures are drawn from jig.py's ROLES and FLOWS; a change to either
# without a redraw would leave the README stating old tables.
python3 scripts/roles_svg.py --check || fail "README's drawing is stale: python3 scripts/roles_svg.py, then commit assets/"

# --- complete --------------------------------------------------------------
if [ "${1:-}" = "--full" ]; then
  bash tests/smoke.sh || fail "smoke failed (bash tests/smoke.sh)"
fi

exit 0
