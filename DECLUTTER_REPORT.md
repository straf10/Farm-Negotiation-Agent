# Declutter report

Branch `declutter`, worktree `C:\Python\Kaggriculture-declutter`, based on `main` @ `920ef63`.
Scope: the tracked files only (`git ls-files`). Gitignored material (`data/`, `gates/` replays,
`baselines/`, `runs/`, `notebooks/`, `.venv/`) is absent from the worktree, as the prompt states.

## 1. Baseline

### 1.1 Metrics (tracked files, `scratchpad/metrics.py`, newline count)

| | files | lines |
|---|---:|---:|
| **total** | **243** | **159,554** |
| gates | 15 | 59,554 |
| docs | 50 | 36,901 |
| data | 12 | 28,021 |
| analysis | 38 | 14,116 |
| tests | 42 | 8,930 |
| harness | 15 | 4,718 |
| agent | 15 | 3,758 |
| engine_reference | 4 | 1,883 |
| (root) | 7 | 1,310 |
| checkpoints | 42 | 210 |
| scripts | 2 | 133 |
| .github | 1 | 20 |

Python only: `analysis` 38 files / 14,116 lines, `tests` 42 / 8,930, `harness` 15 / 4,718,
`agent` 15 / 3,758, `engine_reference` 1 / 1,086, root 1 / 10. Total 112 files / 32,618 lines.

### 1.2 Tests

Run with the CI pins (`requirements-dev.txt`, `PYTHONPATH=.`) in a scratch venv
(`scratchpad/testenv`). The main checkout's `.venv` was not modified.

| environment | passed | failed | skipped |
|---|---:|---:|---:|
| main `.venv` as found (`kaggle-environments` **1.32.6**) | 436 | 12 | 49 |
| scratch venv, pins from `requirements-dev.txt` (**1.32.7**) | **447** | **1** | 49 |

The 11 extra failures in the main `.venv` are one cause: `requirements-dev.txt` pins
`kaggle-environments==1.32.7`, which is the version `engine_reference/` mirrors and the one the
v1t hinge tests and the vendored-constant guard assume. Under 1.32.7 they pass.

The one remaining failure is **not fixed here** and is **not** in my scope:

- `tests/test_archive_sync.py::test_cmd_top_selects_by_team_and_reports_shortfall` expects the
  output directory `top2_2026-08-29`, but `analysis/archive_sync.py:338` names it with
  `dt.date.today()`. It passes only on 2026-08-29. The prompt says not to edit
  `tests/test_archive_sync.py` or `analysis/archive_sync.py`, because the parallel agent owns them.
  Fix: the test should monkeypatch the date (or pass `--date`) rather than hard-code it.

So the test check cannot read "zero failures" until that test is fixed on `main`. Every change in
this branch was verified against the same 447 passing tests, with no new failures.

### 1.3 Lint and dead-code scans (before)

- `ruff check --select F401,F841,ERA001`: **35** findings. F401 26 (all autofixable), F841 6,
  ERA001 3. The repo is not ruff-clean at baseline, so "clean on the touched files" means every
  finding in each file I touch is resolved, or is listed here as deliberately kept.
- `vulture --min-confidence 80`: 3 findings (`s6_step2e.py:96` unsatisfiable ternary,
  `test_s16_recovery_bit_equivalence.py:84` unused import, `test_v1s_herd.py:20` unused parameter).

### 1.4 Submission sha256 (must survive)

What exists locally:

- `submission.tar.gz` (repo root, gitignored): sha256
  `b81007323a6b6a203b94d996ddc8064b9b477e0a7673e049ecb2dfb8321b2cf7`, 15 members (`main.py` plus
  14 `agent/*.py` files). Its `agent/` snapshot is older than HEAD. Of the 14 `agent/*.py` files,
  11 differ from HEAD (`git show HEAD:<path> | cmp`). So it is not the current build of either final
  submission. Its `main.py` is byte-identical to HEAD.
- `baselines/2026-08-07|09|10/submission_*.tar.gz`: earlier versions (v1g, v1h, v1h_2d), not the
  two final submissions.

What is missing, so the byte-identical rebuild **cannot run in this checkout**:

- `data/derived/s6_step1_reconstruction_ReCurSiON.json`, `s6_step1_fidelity_*`, `s6_step1_shed_*`,
  `s6_step1b_cluster_*` are absent everywhere locally (only 12 tracked derived files exist).
  `analysis/build_reconstruction_submission.py` and `build_tape_overlay_submission.py` both read them.
- `analysis/s6_step1b_cluster.py`, which produces `s6_step1b_cluster_*.json`, is **not tracked** in
  the repo and not on disk in the main checkout (searched by name, excluding `.venv`). It is cited by name in `build_reconstruction_submission.py:126,175`. So even with the
  data present, the cluster artefact cannot be regenerated from tracked source. This is a
  reproducibility gap for the post-mortem and should be recorded in the final report.
- The stream sha256 values the docs cite (`1d9e0efd…`, `89ce9e86…`, `09250ef5…`) match no artefact
  present locally.

Consequence for the checks: **the sha256 rebuild check is not run.** The mitigation is structural.
I do not touch any file in the build path, namely `main.py`, `agent/`, `engine_reference/`,
`analysis/build_*_submission.py` and `analysis/s6_step1_reconstruct.py` (the producer of the
reconstruction artefact). I check that by listing every changed path against that set.

### 1.5 Line endings (worktree setup)

The global git config sets `core.autocrlf = true`. A fresh worktree therefore checked out all
241 text files with CRLF, while the index holds LF and the main checkout is LF. That matters
because `agent_fingerprint` hashes source bytes, and `test_engine_reference_matches_installed`
compares bytes. I rewrote the worktree's text files to LF (this touched no content: `git diff HEAD`
is empty). One binary-classified file
(`docs/source/notebooks/v13-r3-top-meta-order-safe-premium-control.md`) was converted by mistake and
restored byte-for-byte from HEAD. After the rewrite, `git status` still lists the 241 files as
modified because of stale index stat data, although `git diff HEAD --stat` is empty. I am checking
content, not `git status`, until the index is rebuilt.

### 1.6 Relative links (`*.md`)

265 relative links are checked. 178 are broken in the worktree:

- 117 point at gitignored paths (`baselines/`, `data/`, `gates/`, `analysis/` files that are
  untracked). They resolve in the main checkout, so they are not broken in practice.
- 61 point at files that do not exist in either checkout, so they are broken at HEAD. Examples:
  `docs/MASTERPLAN.md` (3 links), `baselines/2026-08-28/s16_phase2_three_arm.md`,
  `analysis/b1_top5_profile.py` (the real file is `b1_top_profile.py`),
  `analysis/s9_h2_bound.py`, `analysis/s9_h1_bound.py`, `analysis/s9_commit_audit.py`.
  Stale links are a documentation defect and belong to the docs pass.

## 2. Must-survive entry points

| Entry | Role | Status here |
|---|---|---|
| `main.py` | Kaggle entrypoint; `agent` is imported last on purpose | untouched (its F401 is deliberate) |
| `agent/` (`policy`, `tape_overlay`, ...) | submitted policy | untouched |
| `analysis/build_reconstruction_submission.py` | packages the majority-vote reconstruction, the base of both final submissions | untouched |
| `analysis/build_tape_overlay_submission.py` | `augment` mode = 55675634 (reconstruction + market overlay + tile recovery); `liquidate` mode = H2 tail-liquidation (the 55726984 overlay) | untouched |
| `analysis/build_tape_submission.py` | open-loop donor tape (ancestor) | untouched |
| `analysis/s6_step1_reconstruct.py` | produces the reconstruction artefact the builder reads | not reachable from the survive entries, so it is in the must-survive set |
| `engine_reference/` | read-only engine mirror (byte-compared to the installed engine) | untouched |
| `harness/` + `analysis/s8_replay_io.py`, `s9_market_ledger.py`, `v1v_shop_demand.py` | local harness and shared readers (`harness/ladder.py` imports `v1v_shop_demand.units_per_tick`) | kept |
| `analysis/tape_agent.py`, `donor_streams.py`, `s1_extract_donors.py`, `s6_step0_leg1.py`, `s6_step1_phase0.py` | the reconstruction chain the producer and builder use | kept |
| `analysis/archive_sync.py`, `b1_top_profile.py`, `s7_ladder_census.py`, `s10_replay_bench.py` (Instrument A) | post-mortem tooling | kept |

Entry-point reachability was computed with an `ast` import graph (`scratchpad/impgraph.py`). It
follows function-level imports too. String loading was grepped separately (`importlib`, `runpy`,
`subprocess`), with these results:

- `harness/bench_agents/*.py` are loaded **by path string**, not by import. `analysis/s6_step0_leg1.py:44`
  sets `META_ROUTE = Path("harness/bench_agents/meta_route.py")`, and that module is on the
  reconstruction producer's path. `tests/test_meta_bench.py` resolves `meta_route.py` and
  `meta_route_sheep.py` by path as well. The import graph alone would have wrongly marked them dead.
- `analysis/archive_sync.py` shells out to `kaggle`. That is live and kept.

## 3. Hidden dependencies found (must be honoured before any deletion)

1. **Frozen agent code cites analysis scripts in comments.** `agent/config.py` cites
   `e0_s3_blockers.py`, `v1o1_product_split.py`, `v1o3_visit_efficiency.py` and `meta_route.py`;
   `agent/tape_overlay.py` cites `s9_h2_k10.py`; `agent/sell_ahead.py` cites `v1i_h0_sell_diagnostic.py`;
   `agent/scheduler.py` cites `v1o1_product_split.py`; `tests/test_agent_guards.py:1447` cites
   `v1o1_product_split.py` in a docstring. Deleting those scripts makes the agent's provenance
   comments dangle, and the agent is the submitted artefact. So those scripts are REVIEW, not SAFE.
2. **The H2 builder copies agent logic from a dead-looking script.**
   `analysis/build_tape_overlay_submission.py:410` says its inline `make_h2_agent` tail is a
   byte-copy of `analysis/s9_h2_k10.py`, and `analysis/s10_replay_bench.py:178` cites
   `s9_h2_k10.py::_streams`. `s9_h2_k10.py` is provenance for the H2 tail-liquidation submission and
   should stay.
3. **The harness cites `replay_profile.py` as the source of the end-of-day definition.**
   `harness/metrics.py:561` says it must "match analysis.replay_profile's end-of-day definition
   exactly". That is a live dependency in comments, not imports.
4. **`harness/cli.py:258` and `harness/compare.py:303`** explain the design by pointing at
   `analysis/v1o3_visit_efficiency.py`.
5. **Chain dependency.** `analysis/s6_step1_reconstruct.py` imports `s6_step0_leg1` (for `_dist`,
   `_parse_seeds`, `run_pairing` inside `cmd_bank`) and `s1_extract_donors`/`donor_streams`. Those
   stay alive through the producer.
6. **Tracked allowlist entries** in `.gitignore` name `data/derived/v1u_travel_ratio-2026-08-15.json`,
   `v1u_oracle-2026-08-15.json`, `s6_step0_leg3.json`, `v1v_shop_demand.json` and others. Deleting the
   v1u or s6_step0 scripts leaves those artefacts without a producer.
7. **`test_agent_guards.py` imports `analysis.s6_step2e`** (for a guard). Removing `s6_step2e` needs
   that guard test to change, so it is REVIEW.
8. **`harness/cli.py:5` documents `--bench pass,starter,meta_route`.** `meta_route` is not a
   built-in (only `kaggle_environments`' `agents` dict resolves bare names), so this example does not
   work. The path form would be needed. This is a stale doc, not a deletion, and is listed for the
   docs pass.
9. **Stale engine version string.** The `compare()` warning in `harness/compare.py:720` says
   "under engine 1.32.6". The pinned engine is 1.32.7.
10. **`v1v_shop_demand.py` is live**, although it looks like a one-shot. `harness/ladder.py:189`
    imports `units_per_tick` from it, and the agent guard tests import its `SHOPS` table.

## 4. Candidates and tiers

Tier definitions from the prompt. **SAFE** = unreachable, no doc references, no behaviour change.
**REVIEW** = reachable but probably obsolete, or a doc rewrite that drops information.

### 4.1 Observation: no file meets the SAFE definition

Every dead analysis script has at least one doc reference (`docs/journal/memory.md`, `review.md`,
`ROADMAP.md`, `docs/plans/*.md`), and most have an `agent/` or `harness/` citation as well. So the literal SAFE tier
is empty for whole files. The SAFE work in this branch is therefore limited to changes that delete
no file and need no doc edit: unused imports, unused locals and parameters, a dead ternary branch,
and emoji markers in non-agent code. Every dead script, its tests and its artefacts are REVIEW (4.3).

### 4.2 SAFE tier, executed in this branch

Executed as five commits, C1 to C5 (section 7). Each went through pytest (pinned env), ruff on the
touched files, vulture, the build-path check and the link check (section 6).

- **C1 `Remove unused imports in analysis and tests`** (ruff F401). Files: `analysis/s6_step0_leg2.py`,
  `s6_step0_leg3.py`, `s6_step2b_phase0.py`, `s6_step2b_phase05.py`, `s6_step2c.py`, `s6_step2d.py`,
  `s7_ladder_census.py`, `s8_replay_io.py`, `v1u_oracle.py`, `v1u_travel_ratio.py`,
  `tests/test_meta_bench.py`, `test_s10_bench_alpha_synthetic.py`, `test_s16_recovery_bit_equivalence.py`
  (also clears its vulture finding), `test_s9_live_read_reader.py`, `test_s9_market_ledger.py`,
  `test_tile_recovery.py`. Kept on purpose: `main.py:10` (the loader needs `agent` imported last), and
  `analysis/s6_step1_reconstruct.py:224` (producer, left untouched).
- **C2 `Drop unused locals, a dead parameter and a dead ternary`** (ruff F841, vulture):
  `analysis/v1r_feed_reserve.py:238`, `tests/test_agent_guards.py:288` (the `make_day_plan` call stays
  for its effect), `tests/test_harness.py:223` (the `compare` call stays, it writes replays),
  `tests/test_metrics.py:179` (plus its stale comment), `tests/test_s13_seat_asymmetry.py:91`
  (`pytest.importorskip` stays, it is the skip), `tests/test_v1s_herd.py:20` (`enabled` is never
  passed, I checked), `analysis/s6_step2e.py:96` (`"WEED" if False else`). Kept:
  `engine_reference/kaggriculture.py:249` (read-only mirror, byte-compared to the installed engine).
- **C3 `Strip emoji warning markers from non-agent code`**: 13 lines in nine files. Docstrings
  lose the glyph and keep the bold text. Printed output keeps the signal as `WARNING:` or `STOP:`:
  `analysis/s6_step2c.py`, `v1i_h0_sell_diagnostic.py`, `v1r_feed_reserve.py`, `v1u_oracle.py`,
  `harness/ladder.py`, `harness/town_pin.py`, `tests/test_agent_guards.py`, `tests/test_metrics.py`
  (3 docstrings), `tests/test_s6_step2e.py`. Kept: every marker under `agent/` (frozen), and
  `analysis/build_tape_overlay_submission.py:672` (builder).

ERA001 flagged the section banners `# ---- play()` and `# ---- compare()` in `tests/test_harness.py` as
commented-out code. They are banners, so I dropped the parentheses (C2). That clears the finding
without touching any code. The `agent/config.py:175` ERA001 is frozen and stays.

- **C4 `Unwrap markdown links to files that exist in neither checkout`** (section 4.3 D, which had
  deferred it). 60 links become their link text, one link to an existing file loses its `:300` line
  suffix, and one malformed dataset link becomes a proper URL. The ROADMAP §1 table and the end of
  `docs/journal/memory.md` are not touched: the highest changed line in memory.md is 4722 of 5,276, and
  the first changed ROADMAP line is 448. The 117 links to gitignored artefacts are left as they are.
- **C5 `Remove dead helpers and an unused constant (vulture 60%, pass 2)`**: `invalidate_cache()` in
  `board_join.py`, `all_donor_tapes()` in `donor_streams.py`, `BASELINE` in `test_meta_bench.py`, and two
  unread tuple-unpack names in `test_agent_guards.py`. Kept after review: `opponent_clean()` (4.3 E),
  `SCREEN_SUBS` (Instrument A config), and the `compare()` dataclass fields that vulture reports (the
  result schema, not dead code).

### 4.3 REVIEW tier, not executed (for decision)

Lines are the file's own line count. "Cited by" means a reference outside the candidate's own tests.

**A. Dead one-shot analysis scripts (pass-specific).** No importers from the survive set.

| Path | Lines | Tests that exist only for it | Cited by | Recommendation |
|---|---:|---|---|---|
| `analysis/s10_opponent_inventory.py` | 1,177 | `tests/test_s11_b25_leakage.py` (123), `test_s11_b2_reporting.py` (150) | docs/plans | **delete** script and both tests |
| `analysis/s16_slot_comparison.py` | 527 | `tests/test_s16_slot_comparison.py` (96) | ROADMAP, `tests/test_s16_*` (text) | **delete** with its test |
| `analysis/s13_seat_asymmetry.py` | 500 | `tests/test_s13_seat_asymmetry.py` (131) | imported by s16_slot_comparison | **delete** with s16 chain |
| `analysis/s6_step2e.py` | 624 | `tests/test_s6_step2e.py` (89) | **`tests/test_agent_guards.py` imports it** | delete only after the guard test is reworked |
| `analysis/s6_step2d.py` | 460 | `tests/test_s6_step2d.py` (94) | docs | **delete** with s6_step2 chain |
| `analysis/s6_step2c.py` | 417 | `tests/test_s6_step2c.py` (93) | docs | **delete** with chain |
| `analysis/s6_step2b_phase05.py` | 338 | `tests/test_s6_step2b_phase05.py` (75) | imported by 2c, 2d, 2e | **delete** with chain |
| `analysis/s6_step2b_phase0.py` | 286 | none | no importers | **delete** (dead) |
| `analysis/s6_step0_leg2.py` | 248 | `tests/test_s6_step0.py` (151, shared) | review.md | **delete** with leg3 and the test |
| `analysis/s6_step0_leg3.py` | 166 | (same) | `.gitignore` allowlist | delete, and the `s6_step0_leg3.json` allowlist entry |
| `analysis/v1u_oracle.py` | 627 | `tests/test_v1u_oracle.py` (186) | imported by v1u_travel_ratio | **delete** chain |
| `analysis/v1u_travel_ratio.py` | 552 | `tests/test_v1u_travel_ratio.py` (153) | `.gitignore` allowlist | **delete** chain and its 2 data allowlist entries |
| `analysis/v1r_feed_reserve.py` | 308 | none (agent tests cover the feature) | agent test names | **delete** script, keep agent tests |
| `analysis/e0_s3_blockers.py` | 257 | none | `agent/config.py` comment | keep until agent comment is re-worded |
| `analysis/v1i_h0_sell_diagnostic.py` | 350 | none | `agent/sell_ahead.py` comment | keep until agent comment is re-worded |
| `analysis/v1o1_product_split.py` | 93 | none | `agent/config.py`, `agent/scheduler.py`, test docstring | keep as provenance |
| `analysis/v1o3_visit_efficiency.py` | 150 | none | `agent/config.py`, `harness/cli.py:258`, `harness/compare.py:303` | keep as provenance |
| `analysis/s10_dropped_sells.py` | 175 | none | ROADMAP, docs/plans | **delete**, fix docs |
| `analysis/replay_profile.py` | 343 | `tests/test_replay_profile.py` (87) | **`harness/metrics.py:561` names it as the definition** | keep, or move the definition into `harness/metrics.py` |
| `analysis/s9_h2_k10.py` | 183 | none | **H2 builder copies from it**, `s10_replay_bench.py:178` | **keep** (provenance of the shipped H2 variant) |
| `analysis/s9_live_read_55726984.py` | 1,254 | `tests/test_s14_melon_rephasing.py` (91), `test_s15_gate2_hand_routing.py` (128), `test_s9_live_read_reader.py` (96) | `analysis/s8_replay_io.py:131` (comment) | **keep**: post-mortem of the chosen final submission 55726984 |

Subtotal for the "delete" rows (script + own tests): 25 files, about 7,700 lines, once the agent
and harness citations are reworded. `reference_ladder.py` (64 lines) is not counted.

**B. Harness bench agents (loaded by path).**

| Path | Lines | Used by | Recommendation |
|---|---:|---|---|
| `harness/bench_agents/meta_route.py` | 457 | `analysis/s6_step0_leg1.py:44` (`META_ROUTE`, live producer path), `tests/test_meta_bench.py`, `analysis/tape_agent.py` docstring | **keep** |
| `harness/bench_agents/meta_route_sheep.py` | 34 | `tests/test_meta_bench.py`, `meta_route.py` | **keep** |
| `harness/bench_agents/reference_ladder.py` | 64 | `tests/test_s6_step0.py` only | keep for now: it loads the R25 reference agents fetched into the gitignored `reference/` folder. Decide with that folder |
| `harness/bench_agents/__init__.py` | 1 | package marker | keep with the above |

**C. Tracked artefacts** (the prompt's item 6).

- `gates/**/results.json`: 15 files, 59,539 lines, **37% of the repo**. Ten of them (41,793 lines) are
  not cited by any tracked file, checked by directory name:
  `s9p2_holdout` (7,453), `s9p2_dev` (7,453), `s6_step1b_gate_dev` (7,452), `s9p2_base_dev` (7,452),
  `t1_valmorlee_holdout` (3,414), `overlay_smoke` (2,067), `rev_metrics` (1,949), `s9p2_smoke` (1,946),
  `s9p2_swap_smoke` (1,946), `v1r_inert_check` (661). **Recommend delete**; history keeps them.
  Keep the five that docs cite: `s9_phase2` (3 cites, 199 lines), `gate_v1h2d_feed_slack` (3),
  `gate_v1h2_dev` (2), `gate_v1h2d_eod_surplus` (2), `s6_step1b_gate_holdout` (1).
- `checkpoints/*/manifest.json`: 42 files, 210 lines in total. Keep (the R14 fingerprint record).
- `data/derived/` allowlist: 12 tracked files. Keep the ones docs cite; the v1u and s6_step0 entries
  go with their scripts.
- `.gitignore`: simplify once the artefact decisions above are made.

**D. Documents** (the prompt's item 4). All REVIEW because each is a rewrite that drops narrative.

- `ROADMAP.md` (874 lines): compress to a record of what was built, learned and did not work. Keep
  every measured number that backs a conclusion. **Do not edit the §1 table** (parallel agent).
- `docs/plans/` (19 files, 4,875 lines): delete after their outcomes are in the record.
- `docs/journal/memory.md` (5,276 lines, partly Greek): fold findings into the record. **Do not edit
  the end of the file** (parallel agent).
- `docs/source/notebooks/` (22 files, 24,932 lines): markdown extracts of Kaggle notebooks. The
  `.gitignore` comment says the docs cite them, and some discuss other teams' code. Check them
  against the §2.4b exposure rule before deciding. Not my call.
- `review.md` (232 lines), `docs/INDEX.md` (118), `docs/meta/` (2 files, 1,190), `docs/reference/` (4
  files, 484): fix links and claims. Not done in this branch.
- `README.md` (101 lines): front door. Needs the final result numbers from ROADMAP, so it comes after
  the ROADMAP record.
- Broken links: the 61 missing-everywhere links were fixed in C4 (section 1.6). The other 117 point at
  gitignored artefacts that resolve in the main checkout. A rewrite of these docs is still REVIEW.

**E. Code-level, not SAFE** (each needs an evidence-backed change).

- Duplicated helpers. `_sha256` and `_assert_gitignored` are defined in each of the three
  `analysis/build_*_submission.py` files, and `donor_streams.py:37` has a third `_sha256`. A shared
  module would have to be created, and the builders are must-survive, so REVIEW.
- `analysis/s8_replay_io.py:114` `opponent_clean()`: no callers. It records a rule for live reads,
  that a seat which crashed mid-episode is not a real opponent. Kept, because the rule is not
  written anywhere else in the repo.
- Dead internals in REVIEW-tier scripts, decided with their script: `analysis/s6_step2d.py:76`
  `FREE_GATE`, `:79` `_prod`, `analysis/s6_step2e.py:59` `DOLLAR_PER_RATING_PT`, `:279` `slope_weeds`.
- `analysis/s10_replay_bench.py:134` `SCREEN_SUBS` is unused. It sits in Instrument A, which must
  survive, so it is kept as configuration.
- Left untouched on purpose: `analysis/s6_step1_reconstruct.py:224` (an unused import, in the
  producer). Removing it provably keeps output byte-identical, but I could not run the producer to
  confirm it, so it waits for a run with the data.
- Deliberate duplication: `_shape` is inlined in `build_tape_overlay_submission.py` (lines 101 and
  455) to keep the shipped `main.py` self-contained. Do not consolidate.
- Time/space inefficiency: no candidate has a benchmark yet. Not measured in this pass.

## 5. Surprises

1. The reconstruction submission cannot be rebuilt from tracked source: `s6_step1b_cluster.py` is not
   in git or on disk, and its artefact is absent (section 1.4).
2. The local `.venv` runs the wrong engine (1.32.6), so 11 tests fail there that pass under the pinned
   1.32.7.
3. A date-dependent test in the parallel agent's file (`test_cmd_top_...`) fails on any day other than
   2026-08-29.
4. `harness/cli.py:5` shows an example that does not run (`meta_route` is not a bare name).
5. The top-level `submission.tar.gz` is an older snapshot of `agent/`, not the current build.
6. `ruff` ERA001 flags section banners as commented-out code (false positives).

## 6. Iteration log

Checks after every commit: (a) pytest with the pinned env, no new failures, pass count unchanged
unless tests are deleted; (b) ruff F401/F841/ERA001 on the touched files; (c) the sha256 check:
not runnable (section 1.4), so the substitute is the build-path check (no changed path may be in
the build-path set of section 2); (d) grep for every deleted path or symbol: none deleted;
(e) relative-link check: no new broken links.

**Pass 1.** Candidates: ruff F401 (26), F841 (6), ERA001 (3), vulture-80 (3), emoji markers (13 lines),
broken links (61 missing-everywhere).
Removed or fixed: C1 (24 imports), C2 (7 locals, parameter and dead ternary, 2 banner headers), C3 (13
emoji lines), C4 (61 links).
Failures met along the way, all resolved without touching the test or the logic:
- 11 tests failed in the main `.venv` (engine 1.32.6). Fixed by running under the pinned 1.32.7 env.
- `engine_reference` compared as byte-different. That was a worktree line-ending artefact (section 1.5).
- A binary-classified notebook was converted to LF by my first attempt. Restored from HEAD before any commit.
- `test_cmd_top_selects_by_team_and_reports_shortfall` fails (date-dependent, parallel agent's file). Not fixed; reported.

**Pass 2.** Candidates: vulture 60% (45). Removed: C5 (2 helpers, 1 constant, 2 unread names). Kept after
review: `opponent_clean`, `SCREEN_SUBS`, `compare()` dataclass fields, `pytestmark` (pytest reads it).
Unreachable set and test-only set unchanged. No failures.

**Pass 3.** Candidates: vulture 60% (40), ruff repo-wide (4). Every remaining finding is one of: agent
or engine (frozen), `main.py`'s deliberate import, the producer's unused import (left, section 4.3 E),
REVIEW-tier internals, or a deliberate keep. **No new SAFE candidate: loop stops** (cap of 5 not reached).

## 7. Result

### 7.1 Commits (on `declutter`, after `main` @ `920ef63`)

| commit | subject |
|---|---|
| `c5f4435` | Add declutter inventory report (baseline, candidates, tiers) |
| `1737c45` | Remove unused imports in analysis and tests (ruff F401) |
| `221161e` | Drop unused locals, a dead parameter and a dead ternary (ruff F841, vulture) |
| `55b5e45` | Strip emoji warning markers from non-agent code |
| `b958d17` | Unwrap markdown links to files that exist in neither checkout |
| `409ad63` | Remove dead helpers and an unused constant (vulture 60%, pass 2) |
| (this commit) | Update the report with the executed result |

### 7.2 Before and after

| | before | after |
|---|---:|---:|
| tracked files | 243 | 243 (+1 report) → **244 with the report** |
| lines, code and docs, excluding the report | 159,554 | 159,524 (**−30**) |
| Python lines | 32,618 | 32,588 (**−30**: +34 / −64 in the diff) |
| files deleted | — | **0** |
| ruff F401/F841/ERA001 | 35 | 4 (all kept: `main.py` F401, `agent/config.py` ERA001, `engine_reference` F841, producer F401) |
| vulture 80% | 3 | 0 |
| relative links missing in both checkouts | 61 | 0 |
| relative links to gitignored artefacts | 117 | 117 (resolve in the main checkout) |

The line reduction is small, and that is the honest result of this pass. The prompt's large wins sit
in the REVIEW tier: the 25 dead-script files (about 7,700 lines), the 10 uncited gates results
(41,793 lines), and the docs rewrite. They need decisions from you, so they were not executed.

### 7.3 Tests

| | before (pinned 1.32.7) | after (pinned 1.32.7) |
|---|---:|---:|
| passed | 447 | 447 |
| failed | 1 | 1 |
| skipped | 49 | 49 |
| tests removed | — | 0 |

The one failure is `test_cmd_top_selects_by_team_and_reports_shortfall`, owned by the parallel agent
(section 1.2). The "zero failures" check is **not met** in this branch because of it, and I did not
work around it. The fix is one line in a file this task was told to leave alone.

### 7.4 sha256 verification

**Not run.** The rebuild needs `data/derived/s6_step1_reconstruction_ReCurSiON.json`, its fidelity,
shed and cluster artefacts, and the untracked `analysis/s6_step1b_cluster.py`. None of these are
available (section 1.4). So neither final submission can be rebuilt here, and the byte-identical check
is not met.

Substitute, which I did run for every commit: no protected path changed. Protected means `main.py`,
`agent/`, `engine_reference/`, `analysis/build_*_submission.py` and `analysis/s6_step1_reconstruct.py`.
Checked against the base with `git diff --name-only 920ef63 HEAD`, which returned no protected path.
The archive that exists locally, `submission.tar.gz`, is untouched and still has sha256
`b81007323a6b6a203b94d996ddc8064b9b477e0a7673e049ecb2dfb8321b2cf7`.

### 7.5 What is still open

1. **Fix the date-dependent archive-sync test** on `main` (parallel agent). Until then the test check is red.
2. **Rebuild the reconstruction on a machine with the data.** The builder reads an artefact from
   `analysis/s6_step1b_cluster.py`, which is in neither git nor the local tree. Recover or re-create that
   script, track it, and then run the byte-identical check.
3. **Decide the REVIEW tier** (section 4.3): the 25-file dead-script set, the 10 uncited gate results,
   `opponent_clean`, the bench agents, and the docs rewrite (ROADMAP record, plans, memory fold, README).
4. **Fix the stale `--bench meta_route` example** in `harness/cli.py:5` and the "engine 1.32.6" string in
   `harness/compare.py:720`.
