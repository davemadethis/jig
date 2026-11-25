"""Smoke's roadmap fixtures, written and read in the form jig's checks read: the roadmap file is
JSON, and a fixture says its phases as headings and lists, which jig.py's own functions convert.

    python3 tests/roadmap.py json   .jig/roadmap.md becomes .jig/roadmap.json, products placed by
                                    docs/glossary.md, the .md removed (a fixture's write)
    python3 tests/roadmap.py open   .jig/roadmap.json as .jig/roadmap.md, for an edit in that form
    python3 tests/roadmap.py md [FILE]  FILE (or stdin) as that form, on stdout (a fixture's read)
    python3 tests/roadmap.py edit FILE CODE  FILE, a roadmap JSON draft, edited in that form: CODE
                                    runs on its text as `s`, and the result is written back as JSON
"""
import importlib.util
import sys
from pathlib import Path

# A __pycache__ beside plugin/templates/jig/jig.py would be copied into every .jig/ smoke makes.
sys.dont_write_bytecode = True

spec = importlib.util.spec_from_file_location(
    "jig", Path(__file__).resolve().parent.parent / "plugin" / "templates" / "jig" / "jig.py")
jig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(jig)

MD, JSON, GLOSSARY = Path(".jig/roadmap.md"), Path(".jig/roadmap.json"), Path("docs/glossary.md")
what = sys.argv[1] if len(sys.argv) > 1 else ""
if what == "json":
    owners = jig.term_owners(GLOSSARY.read_text()) if GLOSSARY.is_file() else {}
    before = JSON.read_text() if JSON.is_file() else ""
    JSON.write_text(jig.roadmap_json_of(MD.read_text(), before, owners))
    MD.unlink()
elif what == "open":
    if not MD.exists():
        MD.write_text(jig.roadmap_md_of(JSON.read_text() if JSON.is_file() else ""))
elif what == "md":
    raw = Path(sys.argv[2]).read_text() if len(sys.argv) > 2 else sys.stdin.read()
    sys.stdout.write(jig.roadmap_md_of(raw))
elif what == "edit":
    path = Path(sys.argv[2])
    raw = path.read_text()
    s = jig.roadmap_md_of(raw)
    exec(sys.argv[3])
    path.write_text(jig.roadmap_json_of(s, raw, {}))
else:
    sys.exit(__doc__)
