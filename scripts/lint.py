#!/usr/bin/env python3
"""
Course-wiki lint — health-check for an LLM-maintained Obsidian course wiki.

Usage:
    python3 lint.py [VAULT_DIR] [--concepts concepts] [--chapters chapters]
                    [--terms a,b,c] [--report OUT.md]

Checks (Karpathy "LLM Wiki" Lint operation):
  1. broken wikilinks / image embeds
  2. orphan pages (no inbound link; landing 'Welcome' exempt)
  3. back-link asymmetry  (concept -> chapter exists, chapter -> concept missing)
  4. frontmatter missing  (type / updated / tags)
  5. heavily-mentioned terms without their own page (heuristic, informational)
  6. open questions / conflicts (data gaps)

Files under `.obsidian/` and any `_templates/` folder are ignored.
Stdlib only. Exit non-zero if hard problems (broken links/embeds, frontmatter
gaps, back-link gaps) are found.
"""
import os, re, sys, glob, argparse

_BUF = []
def emit(*a):
    s = " ".join(str(x) for x in a)
    print(s); _BUF.append(s)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vault", nargs="?", default=".", help="vault directory")
    ap.add_argument("--concepts", default="concepts", help="concepts folder name")
    ap.add_argument("--chapters", default="chapters", help="per-source folder name")
    ap.add_argument("--terms", default="", help="comma-list of key terms to check")
    ap.add_argument("--report", default="", help="write markdown report to this path")
    args = ap.parse_args()
    root = args.vault.rstrip("/")

    def keep(p):
        return ".obsidian" not in p and "_templates" not in p
    md = [p for p in glob.glob(f"{root}/**/*.md", recursive=True) if keep(p)]
    if not md:
        emit(f"no markdown found under {root!r}"); sys.exit(2)
    images = {os.path.basename(p) for p in glob.glob(f"{root}/attachments/*")}
    base = lambda p: os.path.splitext(os.path.basename(p))[0]
    rel  = lambda p: os.path.relpath(p, root)

    names, alias2file, fm = set(), {}, {}
    ar = re.compile(r"aliases:\s*\[(.*?)\]")
    field = lambda txt, k: (re.search(rf"^{k}:\s*(.+)$", txt, re.M) or [None, None])[1]
    for p in md:
        b = base(p); names.add(b); txt = open(p, encoding="utf-8").read()
        fm[b] = {"type": field(txt, "type"), "updated": field(txt, "updated"),
                 "tags": "tags:" in txt}
        m = ar.search(txt)
        if m:
            for a in (x.strip().strip("\"'") for x in m.group(1).split(",")):
                if a: names.add(a); alias2file[a] = b
    canon = lambda t: alias2file.get(t, t)

    wl = re.compile(r"(!?)\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
    SKIP = {"링크", "페이지명", "create a link", "name", "<page>", "<Unit> - <Title>",
            "<Concept>", "<Topic>"}
    links, broken, broken_img, inbound = {}, set(), set(), {}
    for p in md:
        b = base(p); outs = set()
        raw = open(p, encoding="utf-8").read()
        raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)   # drop HTML comments
        txt = re.sub(r"`[^`]*`", "", raw)                  # drop code spans
        for bang, t in wl.findall(txt):
            t = t.strip()
            if bang == "!":
                if t.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg")) and t not in images:
                    broken_img.add(f"{rel(p)} → ![[{t}]]")
                continue
            if t in SKIP: continue
            if t not in names:
                broken.add(f"{rel(p)} → [[{t}]]"); continue
            c = canon(t); outs.add(c); inbound[c] = inbound.get(c, 0) + 1
        links[b] = outs

    sec = lambda t: emit(f"\n=== {t} ===")
    hard = 0

    sec("1) broken wikilink / image embed")
    if broken or broken_img:
        for x in sorted(broken): emit("  broken link:", x)
        for x in sorted(broken_img): emit("  broken embed:", x)
        hard += len(broken) + len(broken_img)
    else: emit("  0 ✅")

    sec("2) orphan (inbound 0)")
    orphans = sorted(b for b in {base(p) for p in md} if b not in inbound and b != "Welcome")
    emit("  ", orphans or "none ✅")

    sec("3) back-link asymmetry (concept↔chapter)")
    concepts = [base(p) for p in md if f"/{args.concepts}/" in p or p.startswith(f"{root}/{args.concepts}/")]
    chapters = [base(p) for p in md if f"/{args.chapters}/" in p or p.startswith(f"{root}/{args.chapters}/")]
    gaps = [(ch, c) for c in concepts for ch in links.get(c, ()) if ch in chapters and c not in links.get(ch, set())]
    if gaps:
        for ch, c in sorted(gaps): emit(f"  {ch}  ⟶ missing ⟵  [[{c}]]")
        hard += len(gaps)
    else: emit("  0 ✅")

    sec("4) frontmatter missing (type/updated/tags)")
    fmgaps = [b for b in (base(p) for p in md) if b != "Welcome"
              and (not fm[b]["type"] or not fm[b]["updated"] or not fm[b]["tags"])]
    if fmgaps:
        for b in fmgaps: emit("  ", b, [k for k in ("type", "updated", "tags") if not fm[b][k]])
        hard += len(fmgaps)
    else: emit("  0 ✅")

    sec("5) key terms without own page (informational)")
    terms = [t.strip() for t in args.terms.split(",") if t.strip()]
    if terms:
        alltxt = " ".join(open(p, encoding="utf-8").read() for p in md)
        for t in terms:
            if not any(t.lower() in n.lower() for n in names):
                n = len(re.findall(re.escape(t), alltxt))
                if n: emit(f"  '{t}': {n} mentions, no page")
    else: emit("  (pass --terms a,b,c to check)")

    sec("6) open questions / conflicts (data gaps)")
    found = False
    for p in md:
        for ln in open(p, encoding="utf-8"):
            low = ln.lower()
            if ("open question" in low or "conflict" in low or "❓" in ln or "⚠️" in ln) \
               and "형식:" not in ln and "format" not in low:
                emit(f"  {base(p)}: {ln.strip()[:90]}"); found = True
    if not found: emit("  none")

    emit(f"\nsummary: {len(md)} md, {len(images)} images, "
         f"{len(concepts)} concepts, {len(chapters)} chapters | hard issues: {hard}")

    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(f"# Lint report — `{root}`\n\n```\n" + "\n".join(_BUF).strip() + "\n```\n")
        print(f"\n[report written: {args.report}]")
    sys.exit(1 if hard else 0)

if __name__ == "__main__":
    main()
