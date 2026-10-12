"""Harvest the kaggriculture competition notebooks for the post-deadline meta read.

Run as ``python -I analysis/notebook_harvest.py <command>``. Commands:

  list       enumerate the competition notebooks by dateCreated and by voteCount, plus a keyword search
  pull       download every ref in the universe with ``kaggle kernels pull`` (resumable, 1 call/s)
  inventory  parse each download with json (never executed), cluster near-copies, write inventory.csv
  verify     check the inventory, the cards and the synthesis; exits 1 on any failure

Everything written goes under ``notebooks/``, which is gitignored. Notebook text is data: this module
reads cells and tokenises code, and never imports, executes or installs anything a notebook names.

Conventions used throughout:
  * ``cell <i>`` is the 0-based index into a notebook's ``cells`` array (markdown cells included). A
    plain ``.py`` kernel is one cell, index 0.
  * ``code_hash`` is sha256 over the code cells after tokenising with the stdlib ``tokenize`` module
    (comments, whitespace and layout dropped). Cells are joined with a separator, so cell boundaries count.
  * Near-copy (``dup_of``): equal ``code_hash``, or Jaccard >= 0.9 on the sets of token 4-grams. Notebooks
    with fewer than 3 code lines are never clustered (they would all collide on trivial code).
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import os
import random
import re
import shutil
import subprocess
import sys
import time
import tokenize
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMP = "kaggriculture"
PAGE = 100  # the CLI caps --page-size at 100 in practice (its help says 200)
MAX_PAGES = 100
GAP = 1.0  # seconds between Kaggle calls
MAX_TRIES = 4
TRANSIENT = re.compile(r"429|Too Many Requests|\b5\d\d\b|timed out|timeout|Connection", re.IGNORECASE)
SOURCE_SUFFIXES = {".ipynb", ".py", ".r", ".rmd", ".jl", ".sql"}
KINDS = (
    "agent",
    "strategy-analysis",
    "replay-analysis",
    "engine-study",
    "leaderboard-tool",
    "starter-fork",
    "eda-only",
    "empty",
    "off-topic",
)
DUP_JACCARD = 0.9
TRIVIAL_CODE_LINES = 3
UNIVERSE_COLS = ["ref", "title", "author", "lastRunTime", "totalVotes", "source"]
PULL_COLS = ["ref", "status", "error", "attempts", "seconds"]
INVENTORY_COLS = [
    "ref",
    "title",
    "author",
    "created",
    "last_run",
    "votes",
    "version",
    "status",
    "path",
    "bytes",
    "sha256",
    "n_code_cells",
    "n_md_cells",
    "code_lines",
    "md_words",
    "code_hash",
    "dup_of",
    "author_rank",
    "kind",
    "relevant",
    "reason",
]
class Layout:
    """Where the harvest lives. ``verify`` takes another root so the tests can run on a fixture."""

    def __init__(self, root: Path = ROOT) -> None:
        self.root = root
        self.nb = root / "notebooks"
        self.index = self.nb / "_index"
        self.raw = self.nb / "raw"
        self.cards = self.nb / "cards"
        self.meta_md = root / "docs" / "NOTEBOOK_META.md"

    def dest(self, ref: str) -> Path:
        owner, slug = ref.split("/", 1)
        return self.raw / f"{owner}__{slug}"


# ---------------------------------------------------------------- Kaggle CLI

_last_call = [0.0]


def kaggle_cmd() -> str:
    for cand in (ROOT / ".venv" / "Scripts" / "kaggle.exe", ROOT / ".venv" / "bin" / "kaggle"):
        if cand.exists():
            return str(cand)
    found = shutil.which("kaggle")
    if found is None:
        raise SystemExit("kaggle CLI not found (expected .venv\\Scripts\\kaggle.exe)")
    return found


def kaggle_env() -> dict[str, str]:
    """The process environment plus ``.env`` (KAGGLE_API_TOKEN). The token is never printed."""
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    envfile = ROOT / ".env"
    if envfile.exists():
        for line in envfile.read_text(encoding="utf-8").splitlines():
            key, sep, val = line.partition("=")
            if sep and key.strip() and not key.lstrip().startswith("#"):
                env[key.strip()] = val.strip().strip('"').strip("'")
    return env


def run_kaggle(args: list[str]) -> tuple[str, str]:
    """Run the CLI with 1 s pacing and up to MAX_TRIES tries on transient errors.

    The CLI exits 255 even on success, so the exit code is ignored. Callers judge the result
    from the output they parse.
    """
    out = err = ""
    for attempt in range(1, MAX_TRIES + 1):
        wait = GAP - (time.monotonic() - _last_call[0])
        if wait > 0:
            time.sleep(wait)
        _last_call[0] = time.monotonic()
        try:
            proc = subprocess.run(
                [kaggle_cmd(), *args], capture_output=True, env=kaggle_env(), timeout=300, check=False
            )
            out = proc.stdout.decode("utf-8", "replace")
            err = proc.stderr.decode("utf-8", "replace")
        except subprocess.TimeoutExpired:
            out, err = "", "timed out"
        if not TRANSIENT.search(err) or attempt == MAX_TRIES:
            return out, err
        time.sleep(2**attempt)
    return out, err


def parse_listing(out: str) -> list[dict] | None:
    lines = out.splitlines()
    start = next((i for i, line in enumerate(lines) if line.startswith("ref,")), None)
    if start is None:
        return None
    return list(csv.DictReader(io.StringIO("\n".join(lines[start:]))))


def fetch_listing(scope: list[str], sort: str) -> tuple[list[dict], int, int]:
    """Paginate a kernel listing to the end. Returns (unique rows, pages, raw row count)."""
    seen: dict[str, dict] = {}
    raw = 0
    for page in range(1, MAX_PAGES + 1):
        out, err = run_kaggle(
            ["kernels", "list", *scope, "--page-size", str(PAGE), "-p", str(page), "--sort-by", sort, "--csv"]
        )
        rows = parse_listing(out)
        if rows is None:
            if page > 1 and not out.strip():
                return list(seen.values()), page - 1, raw
            detail = (err or out).strip()[-300:]
            raise RuntimeError(f"listing {scope} sort={sort} page {page} returned no CSV header: {detail}")
        raw += len(rows)
        for row in rows:
            seen.setdefault(row["ref"], row)
        if len(rows) < PAGE:
            return list(seen.values()), page, raw
    raise RuntimeError(f"listing {scope} sort={sort} did not finish in {MAX_PAGES} pages")


def has_source(dest: Path) -> bool:
    return dest.is_dir() and any(
        p.suffix.lower() in SOURCE_SUFFIXES for p in dest.iterdir() if p.is_file()
    )


def write_csv(path: Path, cols: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_universe(lay: Layout, path: Path | None) -> list[dict]:
    if path is None:
        candidates = sorted(lay.index.glob("universe_*.csv"))
        if not candidates:
            raise SystemExit("no universe_*.csv yet; run `list` first")
        path = candidates[-1]
    return read_csv(path)


# ---------------------------------------------------------------- commands

def cmd_list(lay: Layout, stamp: str) -> None:
    by_date, pages_d, raw_d = fetch_listing(["--competition", COMP], "dateCreated")
    by_votes, pages_v, raw_v = fetch_listing(["--competition", COMP], "voteCount")
    by_search, pages_s, raw_s = fetch_listing(["-s", COMP], "dateCreated")
    # Private notebooks come back as a placeholder with no ref. There is nothing to pull, so they are
    # counted here and left out of the universe.
    anonymous = sum(1 for r in by_search if not r["ref"])
    by_search = [r for r in by_search if r["ref"]]

    refs_date = {r["ref"] for r in by_date}
    refs_votes = {r["ref"] for r in by_votes}
    competition: dict[str, dict] = {}
    for row in by_date + by_votes:
        competition.setdefault(row["ref"], row)
    universe = [{**row, "source": "competition"} for row in competition.values()]
    extra: dict[str, dict] = {}
    for row in by_search:
        if row["ref"] not in competition:
            extra.setdefault(row["ref"], {**row, "source": "search"})
    universe += list(extra.values())
    universe.sort(key=lambda r: r["ref"])

    out_path = lay.index / f"universe_{stamp}.csv"
    write_csv(out_path, UNIVERSE_COLS, universe)
    summary = {
        "stamp": stamp,
        "competition_dateCreated": {"pages": pages_d, "raw_rows": raw_d, "unique": len(refs_date)},
        "competition_voteCount": {"pages": pages_v, "raw_rows": raw_v, "unique": len(refs_votes)},
        "search_kaggriculture": {"pages": pages_s, "raw_rows": raw_s, "unique": len(by_search)},
        "sort_disagreement": sorted(refs_date ^ refs_votes),
        "search_only_refs": sorted(extra),
        "search_placeholder_rows_without_ref": anonymous,
        "universe": len(universe),
    }
    (lay.index / f"list_summary_{stamp}.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"universe {len(universe)} refs -> {out_path.relative_to(lay.root)}")
    print(json.dumps({k: v for k, v in summary.items() if k != "search_only_refs"}, indent=2))


def first_error_line(err: str, out: str) -> str:
    lines = [ln.strip() for ln in (err or out).splitlines() if ln.strip()]
    return (lines[-1] if lines else "no output from kaggle kernels pull")[:200]


def cmd_pull(lay: Layout, universe_path: Path | None) -> None:
    universe = load_universe(lay, universe_path)
    lay.raw.mkdir(parents=True, exist_ok=True)
    log_path = lay.index / "pull_log.csv"
    prior = {r["ref"]: r for r in read_csv(log_path)} if log_path.exists() else {}
    rows: list[dict] = []
    for n, row in enumerate(universe, 1):
        ref = row["ref"]
        dest = lay.dest(ref)
        if has_source(dest) and (dest / "kernel-metadata.json").exists():
            rows.append({"ref": ref, "status": "downloaded", "error": "", "attempts": 0, "seconds": 0})
            continue
        dest.mkdir(parents=True, exist_ok=True)
        t0 = time.monotonic()
        out, err = run_kaggle(["kernels", "pull", ref, "-p", str(dest), "-m"])
        ok = has_source(dest)
        rows.append(
            {
                "ref": ref,
                "status": "downloaded" if ok else "unavailable",
                "error": "" if ok else first_error_line(err, out),
                "attempts": 1,
                "seconds": round(time.monotonic() - t0, 2),
            }
        )
        if n % 25 == 0:
            print(f"  pulled {n}/{len(universe)}", flush=True)
            write_csv(log_path, PULL_COLS, rows)
    write_csv(log_path, PULL_COLS, rows)
    done = sum(r["status"] == "downloaded" for r in rows)
    print(f"pull: {done} downloaded, {len(rows) - done} unavailable of {len(rows)}")
    if prior:
        print(f"  (prior log had {len(prior)} rows)")


def read_notebook(path: Path) -> list[tuple[str, str]]:
    """Return (cell_type, source) per cell. JSON is parsed, never executed."""
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".ipynb":
        nb = json.loads(text)
        cells = []
        for cell in nb.get("cells", []):
            src = cell.get("source", "")
            if isinstance(src, list):
                src = "".join(src)
            cells.append((cell.get("cell_type", "code"), src))
        return cells
    return [("code", text)]


_SKIP_TOKENS = {
    tokenize.COMMENT,
    tokenize.NL,
    tokenize.NEWLINE,
    tokenize.INDENT,
    tokenize.DEDENT,
    tokenize.ENDMARKER,
}


def code_tokens(src: str) -> list[str]:
    """Tokenise a code cell without running it. Non-Python cells fall back to a regex split."""
    try:
        return [t.string for t in tokenize.generate_tokens(io.StringIO(src).readline) if t.type not in _SKIP_TOKENS]
    except (tokenize.TokenError, SyntaxError):
        return re.findall(r"[A-Za-z_]\w*|\d+(?:\.\d+)?|\S", re.sub(r"#[^\n]*", "", src))


def shingles(tokens: list[str], k: int = 4) -> set[int]:
    return {zlib.crc32("\x1f".join(tokens[i : i + k]).encode("utf-8")) for i in range(len(tokens) - k + 1)}


def code_fingerprint(cells: list[tuple[str, str]]) -> tuple[str, list[str], int]:
    per_cell = [code_tokens(src) for typ, src in cells if typ == "code"]
    digest = hashlib.sha256("\x1e".join(" ".join(t) for t in per_cell).encode("utf-8")).hexdigest()
    flat: list[str] = []
    for toks in per_cell:
        flat.extend(toks)
        flat.append("\x1d")
    return digest, flat, len(per_cell)


def parse_rank_map(lb_path: Path) -> dict[str, int]:
    """Map lower-cased Kaggle username -> best team rank on the leaderboard snapshot."""
    ranks: dict[str, int] = {}
    with lb_path.open(newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            rank = int(row["Rank"])
            for user in (row.get("TeamMemberUserNames") or "").split(","):
                user = user.strip().lower()
                if user and (user not in ranks or rank < ranks[user]):
                    ranks[user] = rank
    return ranks


LB_GLOB = "data/archive/raw/live_leaderboard_*/kaggriculture-publicleaderboard-*.csv"


def latest_leaderboard() -> Path:
    found = sorted(ROOT.glob(LB_GLOB))
    if not found:
        raise SystemExit(f"no leaderboard snapshot matching {LB_GLOB}")
    return found[-1]


def find_source(dest: Path, meta: dict) -> Path | None:
    code_file = meta.get("code_file") if meta else None
    if code_file and (dest / code_file).exists():
        return dest / code_file
    cands = sorted(p for p in dest.iterdir() if p.is_file() and p.suffix.lower() in SOURCE_SUFFIXES)
    return cands[0] if cands else None


def cluster(members: dict[str, dict]) -> dict[str, str]:
    """Union-find over exact code_hash and token-4-gram Jaccard >= DUP_JACCARD. Returns ref -> representative."""
    parent = {ref: ref for ref in members}

    def find(ref: str) -> str:
        while parent[ref] != ref:
            parent[ref] = parent[parent[ref]]
            ref = parent[ref]
        return ref

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    by_hash: dict[str, list[str]] = {}
    for ref, m in members.items():
        by_hash.setdefault(m["code_hash"], []).append(ref)
    for refs in by_hash.values():
        for other in refs[1:]:
            union(refs[0], other)

    order = sorted(members, key=lambda r: len(members[r]["shingles"]))
    for i, a in enumerate(order):
        sa = members[a]["shingles"]
        for b in order[i + 1 :]:
            sb = members[b]["shingles"]
            if len(sb) > len(sa) / DUP_JACCARD:
                break
            if find(a) == find(b) or not sa or not sb:
                continue
            inter = len(sa & sb)
            if inter / (len(sa) + len(sb) - inter) >= DUP_JACCARD:
                union(a, b)

    groups: dict[str, list[str]] = {}
    for ref in members:
        groups.setdefault(find(ref), []).append(ref)
    rep_of: dict[str, str] = {}
    for refs in groups.values():
        if len(refs) == 1:
            continue
        rep = max(refs, key=lambda r: (members[r]["votes"], members[r]["last_run"]))
        for ref in refs:
            if ref != rep:
                rep_of[ref] = rep
    return rep_of


SIGNAL_PATTERNS = {
    "agent_defs": re.compile(
        r"def\s+(act|policy|play|decide|get_action|agent|choose|step|observe|respond|submission|my_agent|\w*agent\w*|\w*policy\w*)\b"
    ),
    "sim": re.compile(r"kaggle_environments|kaggriculture", re.IGNORECASE),
    "kag": re.compile(r"kaggriculture", re.IGNORECASE),
    "farm": re.compile(
        r"wheat|strawberry|carrot|tomato|melon|\bshop|herd|\bhire\b|buy_|\btiles?\b|\bfarm|kaggriculture", re.IGNORECASE
    ),
    "eda": re.compile(r"read_csv|plt\.|sns\.|matplotlib|seaborn|\.describe\(|\.corr\(|\.hist\("),
    "strategy_md": re.compile(
        r"strateg|meta\b|tile|crop|sell|hire|hiring|plant|animal|herd|land|price|bank|opponent|replay|engine|rule|top\b|leaderboard",
        re.IGNORECASE,
    ),
    "lb": re.compile(r"leaderboard", re.IGNORECASE),
}


def signals(cells: list[tuple[str, str]]) -> dict[str, str]:
    code = "\n".join(src for typ, src in cells if typ == "code")
    md = "\n".join(src for typ, src in cells if typ == "markdown")
    heading = ""
    for typ, src in cells:
        if typ == "markdown":
            # First markdown line that is text rather than an HTML tag or a blank line.
            for line in src.splitlines():
                stripped = line.strip()
                if stripped and not stripped.startswith("<"):
                    heading = stripped.lstrip("#").strip()[:90]
                    break
            if heading:
                break
    defs = sorted(set(SIGNAL_PATTERNS["agent_defs"].findall(code)))
    return {
        "heading": heading,
        "agent_defs": ";".join(defs[:6]),
        "sim_refs": str(len(SIGNAL_PATTERNS["sim"].findall(code))),
        "kag_mentions": str(len(SIGNAL_PATTERNS["kag"].findall(code + "\n" + md))),
        "farm_terms": str(len(SIGNAL_PATTERNS["farm"].findall(code + "\n" + md))),
        "eda_hits": str(len(SIGNAL_PATTERNS["eda"].findall(code))),
        "strategy_md_hits": str(len(SIGNAL_PATTERNS["strategy_md"].findall(md))),
        "leaderboard_hits": str(len(SIGNAL_PATTERNS["lb"].findall(md + code))),
    }


def cmd_inventory(lay: Layout, universe_path: Path | None) -> None:
    universe = load_universe(lay, universe_path)
    pull_path = lay.index / "pull_log.csv"
    pull_log = {r["ref"]: r for r in read_csv(pull_path)} if pull_path.exists() else {}
    lb_ranks = parse_rank_map(latest_leaderboard())
    triage_path = lay.index / "triage.csv"
    triage = {r["ref"]: r for r in read_csv(triage_path)} if triage_path.exists() else {}

    members: dict[str, dict] = {}
    rows: dict[str, dict] = {}
    sig_rows: list[dict] = []
    for u in universe:
        ref = u["ref"]
        row = {c: "" for c in INVENTORY_COLS}
        row.update(
            ref=ref,
            title=u["title"],
            author=u["author"],
            created="n/a",
            last_run=u["lastRunTime"],
            votes=u["totalVotes"],
        )
        dest = lay.dest(ref)
        owner = ref.split("/", 1)[0].lower()
        row["author_rank"] = str(lb_ranks.get(owner, ""))
        pl = pull_log.get(ref, {})
        if not has_source(dest):
            row["status"] = f"unavailable:{pl.get('error', 'not pulled')}"
            rows[ref] = row
            continue
        meta_path = dest / "kernel-metadata.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
        src = find_source(dest, meta)
        try:
            cells = read_notebook(src)
        except (ValueError, OSError) as exc:
            row["status"] = f"unavailable:unparseable ({type(exc).__name__})"
            rows[ref] = row
            continue
        data = src.read_bytes()
        # The CLI exposes no version number, so `version` is the first 12 hex of the source's sha256:
        # it pins the exact text that was read.
        row["version"] = hashlib.sha256(data).hexdigest()[:12]
        digest, tokens, n_code = code_fingerprint(cells)
        code_lines = sum(
            1 for typ, s in cells if typ == "code" for ln in s.splitlines() if ln.strip()
        )
        md_words = sum(len(s.split()) for typ, s in cells if typ == "markdown")
        row.update(
            status="downloaded",
            path=src.relative_to(lay.root).as_posix(),
            bytes=str(len(data)),
            sha256=hashlib.sha256(data).hexdigest(),
            n_code_cells=str(n_code),
            n_md_cells=str(sum(1 for typ, _ in cells if typ == "markdown")),
            code_lines=str(code_lines),
            md_words=str(md_words),
            code_hash=digest,
        )
        rows[ref] = row
        sig = signals(cells)
        t = triage.get(ref, {})
        row["kind"] = t.get("kind", "")
        row["relevant"] = t.get("relevant", "")
        # A reason written by hand in triage.csv wins. Otherwise cite the signals that were read.
        row["reason"] = t.get("reason") or (
            f"{len(sig['agent_defs'].split(';')) if sig['agent_defs'] else 0} agent-style defs "
            f"({sig['agent_defs'] or 'none'}); {code_lines} code lines; {md_words} md words; "
            f"strategy terms in md: {sig['strategy_md_hits']}; heading: {sig['heading'] or 'none'}"
        )
        if code_lines >= TRIVIAL_CODE_LINES:
            members[ref] = {
                "code_hash": digest,
                "shingles": shingles(tokens),
                "votes": int(u["totalVotes"] or 0),
                "last_run": u["lastRunTime"] or "",
            }
        sig_rows.append({"ref": ref, "votes": u["totalVotes"], "last_run": u["lastRunTime"], **sig})

    reps = cluster(members)
    for ref, rep in reps.items():
        rows[ref]["dup_of"] = rep
    write_csv(lay.index / "inventory.csv", INVENTORY_COLS, [rows[u["ref"]] for u in universe])
    write_csv(
        lay.index / "triage_signals.csv",
        [
            "ref",
            "votes",
            "last_run",
            "heading",
            "agent_defs",
            "sim_refs",
            "kag_mentions",
            "farm_terms",
            "eda_hits",
            "strategy_md_hits",
            "leaderboard_hits",
        ],
        sig_rows,
    )
    clusters = {rep for rep in reps.values()}
    print(
        f"inventory: {len(rows)} rows, {sum(r['status'] == 'downloaded' for r in rows.values())} downloaded, "
        f"{len(reps)} duplicates in {len(clusters)} clusters"
    )


CARD_KEYS = [
    "ref",
    "version",
    "last_run",
    "author_rank",
    "votes",
    "kind",
    "family",
    "architecture",
    "production",
    "market",
    "claimed result",
    "novel vs RECORD §6",
    "evidence",
]
CARD_HEADER = CARD_KEYS[:7]
CARD_BODY = CARD_KEYS[7:12]
CARD_LINE = re.compile(r"^(" + "|".join(re.escape(k) for k in CARD_KEYS) + r"):(.*)$")
EVIDENCE_LINE = re.compile(r'^\s*(?:[-*]\s*)?cell (\d+):\s*"(.+)"\s*$')
AUDIT_SAMPLE = 20
EXTRACTION_SAMPLE = 10
MAX_EXTRACTION_DISAGREEMENTS = 1
MIN_TAGGED_CLAIMS = 10


def card_path(lay: Layout, ref: str) -> Path:
    return lay.cards / f"{ref.replace('/', '__')}.md"


def parse_card(text: str) -> dict:
    """Read a card written in the fixed schema. Evidence lines are `cell <i>: "<phrase>"`."""
    fields: dict[str, str] = {}
    evidence: list[tuple[int, str]] = []
    current = None
    for line in text.splitlines():
        m = CARD_LINE.match(line)
        if m:
            current = m.group(1)
            fields[current] = m.group(2).strip()
            continue
        e = EVIDENCE_LINE.match(line)
        if e and current == "evidence":
            evidence.append((int(e.group(1)), e.group(2)))
            continue
        if line.strip() and current is not None:
            fields[current] = (fields[current] + " " + line.strip()).strip()
    return {"fields": fields, "evidence": evidence}


def render_card(hdr: dict, body: dict, evidence: list[tuple[int, str]]) -> str:
    lines = [f"{k}: {hdr[k]}" for k in CARD_HEADER]
    lines += [f"{k}: {body[k]}" for k in CARD_BODY]
    if evidence:
        lines.append("evidence:")
        lines += [f'- cell {i}: "{q}"' for i, q in evidence]
    else:
        lines.append("evidence: n/a")
    return "\n".join(lines) + "\n"


def norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def read_inventory(lay: Layout) -> list[dict]:
    path = lay.index / "inventory.csv"
    return read_csv(path) if path.exists() else []


def cmd_dupcards(lay: Layout) -> None:
    """Write a card for each relevant near-copy that has none yet.

    A near-copy's card says it is a near-copy and that the code shows no strategic change. It cites no
    evidence, because nothing in the copy differs from the representative's cited cells.
    """
    inv = read_inventory(lay)
    by_ref = {r["ref"]: r for r in inv}
    lay.cards.mkdir(parents=True, exist_ok=True)
    written = 0
    for r in inv:
        if not (r.get("dup_of") and r["relevant"] == "Y"):
            continue
        path = card_path(lay, r["ref"])
        if path.exists():
            continue
        rep = by_ref[r["dup_of"]]
        rep_card = card_path(lay, rep["ref"])
        if not rep_card.exists():
            raise SystemExit(f"representative card missing for {rep['ref']}; write it before its copies")
        family = parse_card(rep_card.read_text(encoding="utf-8"))["fields"].get("family", "n/a")
        hdr = {
            "ref": r["ref"],
            "version": r["version"],
            "last_run": r["last_run"],
            "author_rank": r["author_rank"] or "n/a",
            "votes": r["votes"],
            "kind": r["kind"],
            "family": family,
        }
        body = {
            "architecture": f"n/a (near-copy of {rep['ref']})",
            "production": "n/a (near-copy)",
            "market": "n/a (near-copy)",
            "claimed result": "n/a (near-copy)",
            "novel vs RECORD §6": f"no strategic change in code vs {rep['ref']} (near-copy, same code_hash or Jaccard >= {DUP_JACCARD})",
        }
        path.write_text(render_card(hdr, body, []), encoding="utf-8")
        written += 1
    print(f"dupcards: wrote {written} near-copy cards")


def fresh_listing_refs() -> tuple[set[str], set[str], set[str]]:
    by_date, _, _ = fetch_listing(["--competition", COMP], "dateCreated")
    by_votes, _, _ = fetch_listing(["--competition", COMP], "voteCount")
    by_search, _, _ = fetch_listing(["-s", COMP], "dateCreated")
    return (
        {r["ref"] for r in by_date if r["ref"]},
        {r["ref"] for r in by_votes if r["ref"]},
        {r["ref"] for r in by_search if r["ref"]},
    )


def sample_from(seed: int, population: list[str], k: int) -> list[str]:
    return random.Random(seed).sample(sorted(population), k)


def check_fenced_blocks(text: str) -> list[str]:
    problems, inside, start, count = [], False, 0, 0
    for n, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            if not inside:
                inside, start = True, n
                count = 0
            else:
                inside = False
                if count > 5:
                    problems.append(f"fenced block at line {start} is {count} lines (limit 5)")
        elif inside:
            count += 1
    return problems


def cmd_verify(lay: Layout, offline: bool) -> int:
    failures: list[str] = []
    passed: list[str] = []

    def check(name: str, problems: list[str]) -> None:
        if problems:
            failures.extend(f"FAIL {name}: {p}" for p in problems)
        else:
            passed.append(name)

    inv = read_inventory(lay)
    by_ref = {r["ref"]: r for r in inv}
    downloaded = [r for r in inv if r["status"] == "downloaded"]
    universe_files = sorted(lay.index.glob("universe_*.csv"))
    universe = read_csv(universe_files[-1]) if universe_files else []
    cards = {}
    for path in sorted(lay.cards.glob("*.md")) if lay.cards.exists() else []:
        cards[path.name] = parse_card(path.read_text(encoding="utf-8"))
    card_refs = {c["fields"].get("ref", "") for c in cards.values()}

    # 1. universe-complete
    p: list[str] = []
    if not universe:
        p.append("no universe_*.csv; run `list`")
    uni_refs = {r["ref"] for r in universe}
    p += [f"{ref} is in the universe but not in inventory.csv" for ref in sorted(uni_refs - set(by_ref))]
    if not offline:
        date_refs, vote_refs, search_refs = fresh_listing_refs()
        fresh = date_refs | vote_refs | search_refs
        p += [f"{ref} is on the fresh listing but not in inventory.csv" for ref in sorted(fresh - set(by_ref))]
        if len(date_refs) < 602:
            p.append(f"fresh competition listing has {len(date_refs)} refs, below 602 (drop unexplained)")
        if date_refs != vote_refs:
            p.append(f"sort orders disagree on {len(date_refs ^ vote_refs)} refs")
    check("universe-complete", p)

    # 2. every-ref-accounted
    p = []
    for r in inv:
        if r["status"] == "downloaded":
            path = lay.root / r["path"]
            if not path.exists():
                p.append(f"{r['ref']}: file {r['path']} missing on disk")
                continue
            data = path.read_bytes()
            if hashlib.sha256(data).hexdigest() != r["sha256"]:
                p.append(f"{r['ref']}: sha256 differs from inventory")
            if path.suffix.lower() == ".ipynb":
                try:
                    json.loads(data.decode("utf-8"))
                except ValueError as exc:
                    p.append(f"{r['ref']}: does not parse as JSON ({exc})")
        elif not (r["status"].startswith("unavailable:") and r["status"][12:].strip()):
            p.append(f"{r['ref']}: status '{r['status']}' is neither downloaded nor unavailable:<error>")
    check("every-ref-accounted", p)

    # 3. relevance-complete
    p = []
    for r in downloaded:
        if r["kind"] not in KINDS:
            p.append(f"{r['ref']}: kind '{r['kind']}' is not in the allowed set")
        if r["relevant"] not in ("Y", "N"):
            p.append(f"{r['ref']}: relevant '{r['relevant']}' is not Y or N")
        if not r["reason"].strip():
            p.append(f"{r['ref']}: empty reason")
        if r["dup_of"]:
            rep = by_ref.get(r["dup_of"])
            if rep is None or rep["status"] != "downloaded":
                p.append(f"{r['ref']}: dup_of {r['dup_of']} is not a downloaded row")
            elif rep["dup_of"]:
                p.append(f"{r['ref']}: dup_of {r['dup_of']} is itself a duplicate")
            elif rep["relevant"] != r["relevant"]:
                p.append(f"{r['ref']}: relevance differs from its representative {rep['ref']}")
    check("relevance-complete", p)

    # 4. relevant-covered
    p = []
    for r in downloaded:
        if r["relevant"] == "Y":
            target = r["dup_of"] or r["ref"]
            if not card_path(lay, target).exists():
                p.append(f"{r['ref']} is relevant but {target} has no card")
    check("relevant-covered", p)

    # 5. cards-grounded
    p = []
    for name, card in cards.items():
        ref = card["fields"].get("ref", "")
        if ref not in by_ref:
            p.append(f"{name}: ref '{ref}' is not in inventory.csv")
            continue
        if name != card_path(lay, ref).name:
            p.append(f"{name}: file name does not match ref {ref}")
        missing = [k for k in CARD_KEYS if k not in card["fields"]]
        if missing:
            p.append(f"{name}: schema fields missing: {', '.join(missing)}")
        row = by_ref[ref]
        if row["status"] != "downloaded":
            if card["evidence"]:
                p.append(f"{name}: cites evidence but {ref} was not downloaded")
            continue
        cells: list[tuple[str, str]] = []
        try:
            cells = read_notebook(lay.root / row["path"])
        except ValueError:
            p.append(f"{name}: source for {ref} does not parse")
        for idx, phrase in card["evidence"]:
            if idx >= len(cells):
                p.append(f"{name}: cell {idx} does not exist ({len(cells)} cells)")
            elif norm_ws(phrase) not in norm_ws(cells[idx][1]):
                p.append(f"{name}: quote not found in cell {idx}: \"{phrase[:60]}\"")
            if len(phrase.split()) > 15:
                p.append(f"{name}: cell {idx} quote is over 15 words")
    check("cards-grounded", p)

    # 6. synthesis-complete
    p = []
    text = lay.meta_md.read_text(encoding="utf-8") if lay.meta_md.exists() else ""
    if not text:
        p.append("docs/NOTEBOOK_META.md is missing")
    else:
        p += [f"section {n} heading missing" for n in range(1, 8) if not re.search(rf"^## {n}\. ", text, re.MULTILINE)]
        p += [f"card {ref} is not cited in NOTEBOOK_META.md" for ref in sorted(card_refs) if ref and ref not in text]
        cited = set(re.findall(r"`([\w.\-]+/[\w.\-]+)`", text)) & set(by_ref)
        p += [f"NOTEBOOK_META.md cites {ref}, which has no card" for ref in sorted(cited) if not card_path(lay, ref).exists()]
        table_families = set()
        in_s2 = False
        for line in text.splitlines():
            if re.match(r"^## 2\. ", line):
                in_s2 = True
            elif re.match(r"^## 3\. ", line):
                in_s2 = False
            elif in_s2 and line.startswith("|") and "---" not in line:
                first = line.strip().strip("|").split("|")[0].replace("*", "").strip()
                if first and first.lower() != "family":
                    table_families.add(first)
        card_families = {c["fields"].get("family", "") for c in cards.values()}
        p += [f"family '{f}' has no member card" for f in sorted(table_families) if f not in card_families]
        p += [f"family '{f}' on cards is not in the section 2 table" for f in sorted(card_families - table_families) if f]
        in_s5, tags = False, 0
        for line in text.splitlines():
            if re.match(r"^## 5\. ", line):
                in_s5 = True
            elif re.match(r"^## 6\. ", line):
                in_s5 = False
            elif in_s5 and re.search(r"\b(corroborated|contradicted|unverifiable)\b", line):
                tags += 1
        if tags < MIN_TAGGED_CLAIMS:
            p.append(f"section 5 has {tags} tagged claims, needs {MIN_TAGGED_CLAIMS}")
    check("synthesis-complete", p)

    # 7. relevance-audit (recorded sample, reproducible from its seed)
    p = []
    audit_path = lay.index / "audit_relevance.json"
    if not audit_path.exists():
        p.append("audit_relevance.json missing")
    else:
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        population = [r["ref"] for r in downloaded if r["relevant"] == "N"]
        if audit["sample"] != sample_from(audit["seed"], population, AUDIT_SAMPLE):
            p.append("recorded sample does not match its seed and the current N population")
        for ref in audit["sample"]:
            res = audit["results"].get(ref)
            if res is None:
                p.append(f"{ref}: no re-read result recorded")
            elif res["relevant_on_reread"] == "Y":
                p.append(f"{ref}: re-read cold as relevant (rule must be fixed and a new sample drawn)")
    check("relevance-audit", p)

    # 8. extraction-audit
    p = []
    audit_path = lay.index / "audit_extraction.json"
    if not audit_path.exists():
        p.append("audit_extraction.json missing")
    else:
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        population = sorted(card_refs - {""})
        if audit["sample"] != sample_from(audit["seed"], population, EXTRACTION_SAMPLE):
            p.append("recorded sample does not match its seed and the current card population")
        total = sum(int(audit["results"].get(ref, {}).get("material_disagreements", 1)) for ref in audit["sample"])
        if total > MAX_EXTRACTION_DISAGREEMENTS:
            p.append(f"{total} material disagreements in the sample (limit {MAX_EXTRACTION_DISAGREEMENTS})")
    check("extraction-audit", p)

    # 9. policy-respected
    p = []
    if lay.meta_md.exists():
        p += check_fenced_blocks(lay.meta_md.read_text(encoding="utf-8"))
    if not offline:
        status = subprocess.run(
            ["git", "status", "--porcelain", "--", "notebooks"],
            cwd=lay.root,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()
        if status:
            p.append(f"git status shows files under notebooks/: {status[:200]}")
        ignored = subprocess.run(
            ["git", "check-ignore", "-q", "notebooks/raw"], cwd=lay.root, capture_output=True, check=False
        )
        if ignored.returncode != 0:
            p.append("notebooks/raw is not gitignored")
    check("policy-respected", p)

    failed = {f.split()[1].rstrip(":") for f in failures}
    for line in passed:
        print(f"PASS {line}")
    for line in failures:
        print(line)
    print(f"verify: {len(passed) + len(failed)} checks, {len(passed)} passed, {len(failures)} failure lines")
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["list", "pull", "inventory", "dupcards", "verify"])
    parser.add_argument("--root", type=Path, default=ROOT, help="repo root (tests pass a fixture)")
    parser.add_argument("--stamp", default=dt.date.today().isoformat(), help="date stamp for universe_<date>.csv")
    parser.add_argument("--universe", type=Path, default=None, help="universe CSV (default: latest)")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="verify: skip the fresh Kaggle listing and the git checks (used by the fixture tests)",
    )
    args = parser.parse_args(argv)
    lay = Layout(args.root)
    if args.command == "list":
        lay.index.mkdir(parents=True, exist_ok=True)
        cmd_list(lay, args.stamp)
    elif args.command == "pull":
        cmd_pull(lay, args.universe)
    elif args.command == "inventory":
        cmd_inventory(lay, args.universe)
    elif args.command == "dupcards":
        cmd_dupcards(lay)
    else:
        return cmd_verify(lay, args.offline)
    return 0


if __name__ == "__main__":
    sys.exit(main())
