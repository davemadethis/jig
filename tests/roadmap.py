"""Smoke's roadmap fixtures. A fixture says its phases in the old roadmap.md form, and jig's own
conversion writes them as roadmap.json: the one place the old parser runs.

    python3 tests/roadmap.py json   .jig/roadmap.md becomes .jig/roadmap.json by jig's conversion,
                                    products placed as Family places them (a metarepo's glossary,
                                    none elsewhere), the .md removed; it fails on anything the
                                    conversion would name and wait on
    python3 tests/roadmap.py open   .jig/roadmap.json drawn as .jig/roadmap.md, for an edit in that form
    python3 tests/roadmap.py md [FILE]  FILE (or stdin), a roadmap.json, drawn in that form on stdout
    python3 tests/roadmap.py edit FILE CODE  FILE, a roadmap JSON draft, edited in that form: CODE
                                    runs on its text as `s`, and the result is converted back
    python3 tests/roadmap.py loads ARGS…  runs `jig ARGS…` in-process and prints the most times
                                    any one roadmap file was parsed: 1 when every reader shared it
    python3 tests/roadmap.py values  adds to .jig/roadmap.json a Widget phase per VALUES entry, its
                                    note, exit text and scope text that value, and two No phase
                                    items per value, Widget's and the repo's own, interleaved
    python3 tests/roadmap.py checkvalues  reads `jig roadmap --json --product Widget` on stdin: each
                                    value comes back as written, with nothing read from it
    python3 tests/roadmap.py lossy  the conversion's check fires on its output: a conversion that
                                    loses a note line is named, with that line
    python3 tests/roadmap.py sweep  the class is closed, conversion side: each line of LINES inserted
                                    at every position of RICH is named by the conversion, or is
                                    held in a record of the section it was inserted in
"""
import json
import re
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
# What the old form read as syntax, each to be a JSON text, note and exit text as it is.
VALUES = ["x (after y)", "x (touches docs/a.md)", "x (labels ui)", "a\nb", "  lead",
          "x; stops at y; parked 2026-01-01", "## h", "Exit when:", "- `z`: w", "\u0002"]
# The richest old roadmap: two products, notes, boxes, scopes, both lists, an Up next.
RICH = """# Roadmap

## alpha
The alpha note.

Exit when:
- [ ] boots
- [x] ships

Scopes:
- `s`: screen (labels ui) (touches docs/a.md)
- `t`: radio (after alpha/s)

## Widget alpha
Widget's note.
(after alpha)

Scopes:
- `w`: widget work

## Gadget alpha
Scopes:
- `g`: gadget work

## No phase
- `q`: payments; stops at cache; parked 2026-11-13
  - nested detail

## Widget No phase
- `wq`: widget item

## Up next
- `u`: offline"""
INSERTS = ["prose", "  indented prose", "- bullet", "  - nested", "```\n(after x)\n```", "(after x)",
           "(labels ui)", "# H1", "<!-- c -->", "- [ ] box", "- `z`: scope"]


def owners() -> dict:
    """Family's owners: the glossary's in a metarepo, none elsewhere."""
    return jig.term_owners(GLOSSARY.read_text()) if Path(jig.META).is_file() and GLOSSARY.is_file() else {}


def convert(md: str, before: str = "") -> str:
    """MD converted as jig's conversion does. A fixture editing a roadmap.json (BEFORE) keeps its
    products: their headings are placed under them, and its `products` list stays."""
    kept = (jig.roadmap_load(before) or {}).get("products") or [] if before else []
    placed = {**owners(), **{p: "" for p in kept}}
    named = jig.uncarried(md, placed)
    if named:
        sys.exit("the conversion names: " + "; ".join(named))
    data = jig.roadmap_data(md, placed)
    # A kept product no record names and the glossary no longer holds is a rename's old name.
    used = {r.get("product") for r in data["phases"] + data["no_phase"]}
    data["products"] = [p for p in dict.fromkeys(kept + data["products"]) if p in used or p in owners()]
    return jig.roadmap_dumps(data)


what = sys.argv[1] if len(sys.argv) > 1 else ""
if what == "json":
    JSON.write_text(convert(MD.read_text(), JSON.read_text() if JSON.is_file() else ""))
    MD.unlink()
elif what == "open":
    if not MD.exists():
        MD.write_text(jig.roadmap_md(jig.roadmap_load(JSON.read_text()) if JSON.is_file() else jig.ROADMAP_SEED_DATA))
elif what == "md":
    raw = Path(sys.argv[2]).read_text() if len(sys.argv) > 2 else sys.stdin.read()
    sys.stdout.write(jig.roadmap_md(jig.roadmap_load(raw) or jig.ROADMAP_SEED_DATA))
elif what == "edit":
    path = Path(sys.argv[2])
    before = path.read_text()
    s = jig.roadmap_md(jig.roadmap_load(before) or jig.ROADMAP_SEED_DATA)
    exec(sys.argv[3])
    path.write_text(convert(s, before))
elif what == "loads":
    counts: dict[str, int] = {}
    parse = jig.roadmap_parse

    def counted(raw: str):
        counts[raw] = counts.get(raw, 0) + 1
        return parse(raw)
    jig.roadmap_parse = counted
    try:
        jig.main(sys.argv[2:])
    except SystemExit:
        pass
    sys.stdout.flush()
    print(f"most parses of one roadmap: {max(counts.values(), default=0)}", file=sys.stderr)
elif what == "values":
    d = json.loads(JSON.read_text())
    d["phases"] += [{"product": "Widget", "name": f"v{n}", "note": v, "exit": [{"text": v, "done": False}],
                     "scopes": [{"id": "s", "text": v}]} for n, v in enumerate(VALUES)]
    d["no_phase"] += [r for n, v in enumerate(VALUES)
                     for r in ({"id": f"i{n}", "text": v, "product": "Widget"}, {"id": f"j{n}", "text": v})]
    JSON.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
elif what == "checkvalues":
    d = json.load(sys.stdin)
    got = {p["key"]: p for p in d["phases"]}
    items = {i["id"]: i["record"] for i in d["no_phase"]}
    for n, v in enumerate(VALUES):
        p = got[f"Widget v{n}"]
        rec = p["scopes"][0]["record"]
        assert p["record"]["note"] == v and p["record"]["exit"][0]["text"] == v and rec["text"] == v, (n, p)
        assert not {"after", "labels", "needed_by", "touches"} & set(rec) and not p["scopes"][0]["state"] == "blocked", p
        assert items[f"Widget No phase/i{n}"]["text"] == v, items
elif what == "lossy":
    real = jig.roadmap_data

    def lossy(md, owners):
        d = real(md, owners)
        d["phases"][0]["note"] = "kept line"
        return d
    jig.roadmap_data = lossy
    named = jig.uncarried("# Roadmap\n\n## a\nkept line\nlost line\n\nScopes:\n- `s`: x\n", {})
    assert named == ["under ## a: lost line"], named
elif what == "sweep":
    owners = {"Widget": "this repo", "Gadget": "this repo"}
    lines = RICH.split("\n")
    assert not jig.uncarried(RICH, owners), jig.uncarried(RICH, owners)
    bad = []
    for k in range(len(lines) + 1):
        heads = [l for l in lines[:k] if l.startswith("## ")]
        under = (heads[-1][3:].strip() if heads else "")
        under = jig.NO_PHASE if under == "Up next" else under
        for ins in INSERTS:
            md = "\n".join(lines[:k] + ins.split("\n") + lines[k:])
            if jig.uncarried(md, owners):
                continue
            data = jig.roadmap_data(md, owners)
            if problems := jig.roadmap_file_problems(jig.roadmap_dumps(data), owners):
                bad.append((k, ins, "converts, then refused", problems))
                continue
            # The section it was inserted in, by the test's own split: a phase whole, or a list.
            held = [p for p in data["phases"] if jig.phase_key(p) == under] + \
                [i for i in data["no_phase"] if jig.list_key(i.get("product", "")) == under]
            words = [w for w in re.findall(r"[A-Za-z0-9][A-Za-z0-9_./-]*", ins) if w not in ("after", "labels", "needed", "by")]
            dump = json.dumps(held, ensure_ascii=False)
            if not under or not all(w in dump for w in words):
                bad.append((k, ins, "converts, and isn't held under", under or "the top"))
    assert not bad, "\n".join(map(str, bad))
else:
    sys.exit(__doc__)
