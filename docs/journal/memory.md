# Journal: core findings

The session log of 5 August to 12 October 2026, reduced to what still holds. The original log had
71 dated sessions over 5,276 lines, in Greek. It is kept in git history at `920ef63:docs/journal/memory.md`.

Engine facts and the STOP register live in [RECORD.md](../RECORD.md). This file keeps what RECORD
does not: our own corrections, the dated decisions, the submission history, and the open items.

---

## Latest state (2026-10-15)

Submissions closed on 2026-09-30. **Leaderboard:** post-deadline snapshot
`data/archive/raw/live_leaderboard_2026-10-15/kaggriculture-publicleaderboard-2026-10-15T08_12_48.csv`
(08:12 UTC, 10,148 teams; STRAF rank 4,432, score 924.4) is recorded in [RECORD.md](../RECORD.md) §1.
**`55675634` replays:** 760 files in `data/archive/raw/live_55675634/` (154 September + 606
post-cutoff). **Top-50 profile:** `data/derived/b1_top_profile_post0930_2026-10-14.json` (see prompt
04 close loop). **Manifest:** `data/archive/manifest.csv` is the provenance index (2,384 episodes,
4,768 seat-rows); `manifest_daily_index.csv` keeps the old daily-dataset header.

**Prompt 04 iteration log (close data / final board).**
1. Pulled `live_leaderboard_2026-10-14` then `2026-10-15`; used the latter for §1.
2. Downloaded 606 missing `55675634` post-cutoff replays (0 API failures).
3. `b1_top_profile` hung on `episode-122734506` — root cause: `step_ledger` simulated 1e6-unit SELL
   orders literally; fixed with `MAX_UNITS_PER_MARKET_PASS` in `s9_market_ledger.py` and UTF-8 manifest
   read in `b1_top_profile.py`.
4. Copied `manifest.csv` → `manifest_daily_index.csv`, then `archive_sync.py manifest --force`.

Prior review: [REVIEW_2026-10-14.md](../post_mortem/REVIEW_2026-10-14.md).

## State on 2026-10-12

Submissions closed on 2026-09-30. The board was in its convergence window. The final ranking had not
been recorded yet.

**Session 2026-10-12, post-deadline data refresh** (run by the parallel agent under `prompts/01`):

- **Leaderboard:** 10,148 teams, snapshot 15:19 UTC. STRAF rank 4,479, score 909.6.
- **Active pair:** `55726984` at public 903.5 (1,000 episodes listed, the listing cap). `55675634` at
  public 865.5, not collected in this pass.
- **Post-deadline corpus:** 7,737 replays (616 ours, 394 top-50, 6,727 October shard) with 15,474
  feature rows and no parse errors. The working set was swapped in. The old copies were moved, not
  deleted, to `data/archive/superseded_2026-10-12/` (619 MB). **Deletion awaits your decision.**
- **Not done:** the top-50 profile (`b1_top_profile.py`) was not produced, and the provenance manifest
  needs a `--force` rebuild because the old one has the wrong schema.
- **Tests:** 452 passed, 49 skipped, 0 failed. The skips need gitignored replay folders.

**Session 2026-10-13, notebook meta harvest** (`prompts/03`):

- **Coverage:** 689 public notebooks (602 listed, 87 found by keyword search), all downloaded. 664 relevant,
  25 not. 544 representatives and 120 near-copies in 60 clusters. Nothing from `notebooks/` is committed.
- **Output:** `docs/NOTEBOOK_META.md`, with 23 families and a claim check. Of 15 notebook claims tested against the
  768 top-50 seat traces, 5 match the field, 2 do not, and 8 cannot be tested with this set.
- **RECORD:** no edits to §6, §10 or §11. Proposed wording for §10 and §11 is in the meta document. One notebook
  names tomato, carrot and egg as the §11.5 hinge products; the top-50 set has no pre-change baseline to test it.
- **Policy:** §12 now allows reading notebook code as data, with no execution and no commits of downloads.

---

## 1. Corrections to our own readings

These overturned something we had written down as fact. Read them before trusting an older number.

- **The 65% ladder win rate was the placement burst.** Overall 54.5%, by thirds 66.1% / 50.8% / 46.7%.
  Controlled and converged (n=53): 43.4%, falling with opponent strength (54% / 41% / 38% for
  under 1,800 / 1,800-2,100 / above 2,100). *(2026-08-20)*
- **Absolute score deflates across the whole ladder; compare by rank.** At a fixed rank the score falls
  26 to 49 points a day between #25 and #900. Below about #1,200 it rises, as new entrants arrive.
  Over the same period we lost 32.9 points and gained 15 places. *(2026-08-20)*
- **`median_bank` is about a third city, and the rating cannot see it.** Drain correlates with bank
  (r = +0.605), but drain against win rate is flat or inverted. Elo and Bradley-Terry fit only W/L.
  *(2026-08-20)*
- **The 2.75-3.70x price spread was the town, not the agent.** Between towns, 99-100% of the price
  variance sits in the town; within one town, 0-1%. Shops are drawn with replacement (8 instances).
  *(2026-08-17)*
- **Engine 1.32.7 went live between 14 and 16 August.** 61 of 61 episodes on the 16 August dataset ran
  1.32.7; 28 of 28 on 14 August ran 1.32.6. Dollar figures under `checkpoints/v1u_base` predate the
  change. *(2026-08-16)*
- **The B1 donor tape was contaminated by the engine version.** 56 of its 66 replays had
  `townCenterSellInterval: 12`, which is pre-1.32.6. The re-measurement uses the newer 60. *(2026-08-11)*
- **Replay alignment.** The observation at step *t* is recorded after action *t*. Any read of
  pre-trade state must take step *t-1*. *(2026-08-21)*
- **Round trips in one turn earn nothing.** Quotes are symmetric around the same inventory, so a buy
  and sell in one turn cancel. Profit exists only for units held across turns. *(2026-08-21)*
- **The forum claim that byte-identical copies land 300-1,400 points apart by early-draw luck does not
  hold here.** An unlucky copy would win, not lose. *(2026-08-20)*
- **A reconstruction must be replayed against its own opponents before upload.** The tetsuya
  reconstruction showed a 59% median bank error on that replay, against 0.12% for ours. A trace count
  alone would have passed it. *(2026-08-21)*

## 2. Ladder mechanics, as measured

- **Only the latest two submissions are active.** A submission outside the latest two plays no
  episodes. Its score freezes. The final Bradley-Terry runs on post-deadline episodes, which a dead
  bot does not play.
- **Eviction is by date, not by score.** The T1 tape pushed out v1i on 10 August, not the higher-scoring
  v1o.2. The next upload evicts whichever active slot is oldest.
- **A converged rating decays without a code change.** 632.2, then 618.4, then 600.2.
- **The burst is the first 5 hours.** About 14.6 episodes per hour, then 0.7-2.0 per hour. Win rates
  measured inside the burst mean little.
- **Leaderboard entries reset on a new upload.** A new upload starts near 600 and needs about a day to
  converge.

## 3. Standing rules that came out of the journal

- **Price the programme before each pass.** If the ceiling is under 1% of the gap, do not run another
  pass. *(2026-08-20)*
- **A pass ends in an upload, or it does not run.** *(2026-08-20)*
- **Priced gate, not a hard zero, for non-structural counters.** Structural counters stay hard zeros:
  `clipped_production_ticks`, `plant_decay_units_lost`, no-ops, market abort, and low-price sales above
  2%. Every other non-zero counter costs a fixed price, with a $500/episode ceiling. Any counter that
  is non-zero needs a written mechanism; an unexplained one counts as a bug and stops the pass.
  *(2026-08-10)*
- **Objective order:** median bank first, then W/L against the meta bench, with mean difference only as
  a tie-breaker and regression detector. *(2026-08-10)*
- **Fidelity replay before any reconstruction upload.** Advisory KILL floor: market agreement under
  0.90. *(2026-08-21)*
- **Reports go to `baselines/`, narrative to the journal, and the roadmap changes only when the plan,
  a gate or a standing rule changes.** *(2026-08-20)*
- **Ship twice, then measure.** Both planned ships (A and B, section 6) end in uploads, and the
  measurement bench is calibrated against those uploads. Decided by the user on 2026-08-20.

## 4. Decisions by the user

- **2026-08-17:** the bench is tiers 0-5 of the reference agents plus our three donor tapes as a fixed
  mirror. Tiers 6-9 are skipped, because their `_TRACE` is not covered by our guards.
- **2026-08-10:** the priced-gate decision above, replacing the hard-zero metric gate.
- **2026-08-11:** the rule against seeding routes from public replays is lifted. The rule that governs
  what we may copy then becomes: copy the *profile*, not the *tape*. The profile is about 20 numbers
  (13 animals at 9C+4S on a 6/12/13 ramp, quadrant timing, tile-days, sell calendar), which carry no
  licence obligation. The tape carries provenance, redistribution and CC-BY terms. The public repo makes
  those terms active, not theoretical.
- **2026-08-11:** one `ROADMAP.md` replaces `MASTERPLAN.md` and `current_phase.md`.
- **2026-08-20:** the roadmap is cut from 2,906 lines to 544. Standing narrative stays in the journal.
- **2026-08-20:** the Kaito notebook was moved out of the repo root into the gitignored `/notebooks/`,
  because it was untracked in a public repo. The standing rule is to delete it after extraction; that
  deletion was left to the user.

## 5. Submission history

The ids are as cited in the journal. Dates are UTC upload times.

| Date | Id | Build | Outcome |
|---|---|---|---|
| 2026-08-06 | (not recorded) | First package from the frozen v1e checkpoint | Working tree was about 600 points behind v1e on dev seeds; packaged from the checkpoint, not the tree |
| 2026-08-07 | 55324447 | v1g, second upload | Replaces the first |
| 2026-08-09 | 55383610 | v1h | Best publicScore 652.5 (2026-08-11) |
| 2026-08-09 18:58 | 55387820 | Unexplained, not in the repo | Pushed v1g out of the active pair. Never explained |
| 2026-08-09 | 55390611 | v1h.2d | Completed at 613.6 |
| 2026-08-10 14:58 | 55409945 | v1m_d2 | Pending; 626.1, later 651.5 |
| 2026-08-10 | 55414570 | v1i | 632.2, then 618.4 without code change |
| 2026-08-11 17:06 | 55438252 | v1o.2 | 643.9, then 647.5; inactive by 16 August |
| 2026-08-16 | 55548339 | T1, Valmorlee tape | 1,091 to 1,617.6 over a day. Evicted by date on 17 August |
| 2026-08-17 09:24 | 55575305 | Ueddy tape | Started at 600.1; 1,027.8 after 7 episodes |
| 2026-08-17 22:29 | 55586926 | S6 step 1b, reconstruction | Evicted Valmorlee by date |
| 2026-08-21 19:06 | 55675634 | Reconstruction, market overlay and tile recovery | Frozen. Public 865.5 on 2026-10-12. Higher-scoring slot from 28 August |
| 2026-08-23 23:07 | 55726984 | Reconstruction plus H2 tail liquidation | Evicted 55586926 by date. Public 903.5 on 2026-10-12 |

As of 18 August the active pair was Ueddy (55575305) and the reconstruction (55586926). The pair in
the last two rows is the final pair.

## 6. Sessions that ended in a kill or a stop

Short form. The engine-level reasons and the full rows are in [RECORD.md](../RECORD.md) §9.

- **Ship A, re-donor on the top-4 route (2026-08-21):** KILL. All four top-4 policies are state-adaptive.
  The fidelity replay failed, so the route could not be copied.
- **Ship B, WHEAT market maker (2026-08-21):** KILL. The impact ceiling is $2.009 per episode, which is
  7.94 rating points at best, against a 50-point threshold. The glut ride-along was measured on WHEAT
  alone, and WOOL sits at the $1 floor for a median of 30 turns. Row 31 (glut) is still untested.
- **S6 step 2d, closed-loop tile control (2026-08-18):** the production residual is town-reactive, but
  its recoverable value is $597 per episode, about 2.4 points, or 0.09% of the gap. STOP.
- **S6 step 2a, repair layer (2026-08-16 and 08-18):** refuted by measurement; not built.
- **S3 herd-13, step 2 (2026-08-15):** STOP.
- **MELON race v1m (2026-08-10):** STOP at smoke, then at the E1 dev gate.
- **v1n (2026-08-10):** KILL. The structural component is 62.7%, explicitly out of scope.
- **v1c NE land expansion (2026-08-05):** three capacity and routing variants failed the smoke gate.
  Reverted exactly; the animals step did not proceed while v1c was regressive.

## 7. Open items (as of 2026-10-15)

- **Submissions are closed.** The deadline was 2026-09-30 23:59 UTC. Ship B component (i) and the glut
  test (row 31) were never built or uploaded, and can no longer be submitted. They stay here as the
  record of what was not done.
- **Superseded copies:** `data/archive/superseded_2026-10-12/` measures 648.2 MB (12 files). The
  review recommends keeping it. Deletion is still your decision.
- **Notebook proposals:** wording for RECORD §10 and §11 is still only proposed in
  [NOTEBOOK_META.md](../NOTEBOOK_META.md) §6. It was not merged.
- **Still unexplained:** the gap of about 1,036 points to the donor at #9, and the ghost upload
  55387820. See [RECORD.md](../RECORD.md) §11.

---

*Coverage note.* Every session heading was read, along with each verdict, correction, status and
"next session" line. No session was read end to end. The bodies were read in part, mostly the parts
that state findings: the 21 August, 20 August, 17 August, 16 August, 11 August (planning, parts A and
E), 10 August (α) and 5 August (v0 to v1b) entries. The rest is summarised from its headings and
markers, so some detail in the middle of the log is not covered here.
