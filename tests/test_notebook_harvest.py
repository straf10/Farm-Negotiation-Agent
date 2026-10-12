"""analysis/notebook_harvest.py: verify on a synthetic fixture, plus the parsing helpers.

The fixture (tests/fixtures/notebook_harvest) is three invented notebooks, not competition data:
  fx/good     a card whose quotes appear in its cell (passes)
  fx/fake     a card whose quote is not in the cited cell (fails cards-grounded)
  fx/missing  a relevant notebook with no card (fails relevant-covered)
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from analysis import notebook_harvest as nh

FIXTURE = ROOT / "tests" / "fixtures" / "notebook_harvest"


def test_verify_flags_fake_quote_and_missing_card(capsys):
    rc = nh.main(["verify", "--root", str(FIXTURE), "--offline"])
    out = capsys.readouterr().out.splitlines()

    assert rc == 1
    assert "FAIL cards-grounded: fx__fake.md: quote not found in cell 1" in " ".join(out)
    assert "FAIL relevant-covered: fx/missing is relevant but fx/missing has no card" in out
    assert "PASS universe-complete" in out
    assert "PASS every-ref-accounted" in out
    # The good card contributes no failure line of its own.
    assert not [line for line in out if line.startswith("FAIL") and "fx__good" in line]
    # One line per failure: every FAIL line is its own line, and the summary counts them.
    fail_lines = [line for line in out if line.startswith("FAIL")]
    assert out[-1].endswith(f"{len(fail_lines)} failure lines")


def test_card_parse_reads_schema_and_evidence():
    text = (FIXTURE / "notebooks" / "cards" / "fx__good.md").read_text(encoding="utf-8")
    card = nh.parse_card(text)

    assert card["fields"]["ref"] == "fx/good"
    assert card["fields"]["family"] == "wheat-first"
    assert [i for i, _ in card["evidence"]] == [1, 1]
    assert card["evidence"][1][1] == 'return {"plant": "WHEAT"}'


def test_render_card_round_trips_through_parse():
    hdr = {k: "x" for k in nh.CARD_HEADER}
    hdr["ref"] = "own/slug"
    body = {k: "n/a" for k in nh.CARD_BODY}
    card = nh.parse_card(nh.render_card(hdr, body, [(3, "print(1)")]))

    assert card["fields"]["ref"] == "own/slug"
    assert all(k in card["fields"] for k in nh.CARD_KEYS)
    assert card["evidence"] == [(3, "print(1)")]


def test_code_tokens_ignore_comments_and_layout():
    a = "x = 1  # the first note\n\ny=2\n"
    b = "x=1\ny   =   2\n"
    assert nh.code_tokens(a) == nh.code_tokens(b)
    assert nh.code_tokens("def act(obs):\n    return 1\n") != nh.code_tokens("def act(obs):\n    return 2\n")


def test_cluster_groups_exact_and_near_copies():
    base = nh.shingles(nh.code_tokens(" ".join(f"t{i}" for i in range(200))))
    near = set(base) | {10**12}  # one extra shingle: Jaccard 197/198, above the 0.9 threshold
    far = nh.shingles(nh.code_tokens(" ".join(f"u{i}" for i in range(200))))
    other = nh.shingles(nh.code_tokens(" ".join(f"v{i}" for i in range(200))))
    members = {
        "a/rep": {"code_hash": "h1", "shingles": base, "votes": 5, "last_run": "2026-09-01"},
        "b/copy": {"code_hash": "h2", "shingles": near, "votes": 1, "last_run": "2026-09-02"},
        "c/exact": {"code_hash": "h1", "shingles": far, "votes": 0, "last_run": "2026-08-01"},
        "d/other": {"code_hash": "h9", "shingles": other, "votes": 0, "last_run": "2026-08-01"},
    }
    rep_of = nh.cluster(members)

    # b joins by Jaccard, c joins by equal code_hash, d shares nothing and stays a singleton.
    assert rep_of == {"b/copy": "a/rep", "c/exact": "a/rep"}


def test_fenced_block_limit_is_five_lines():
    ok = "```\n" + "x\n" * 5 + "```\n"
    too_long = "```\n" + "x\n" * 6 + "```\n"
    assert nh.check_fenced_blocks(ok) == []
    assert nh.check_fenced_blocks(too_long) == ["fenced block at line 1 is 6 lines (limit 5)"]


def test_audit_sample_is_reproducible_from_seed():
    population = [f"o/s{i}" for i in range(50)]
    first = nh.sample_from(20261012, population, 20)
    assert first == nh.sample_from(20261012, list(reversed(population)), 20)
    assert len(set(first)) == 20
