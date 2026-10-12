# Kaggriculture — the record

The competition ended 2026-09-30 (submissions closed). This file is the post-mortem: what the
competition is, what we built, what we measured, what did not work, and what is still open. It
replaces the earlier planning docs, the pass journal and the audit notes. Their full text is in git
history at commit `920ef63`.

Engine ground truth is `kaggle-environments==1.32.7`, mirrored byte-for-byte in `engine_reference/`.
Where a doc and the engine disagree, the engine wins.

---

## 1. Result

| | Submission | Public score (2026-09-01) | Ladder record | Status |
|---|---|---:|---:|---|
| Slot A | `55726984`: reconstruction + H2 tail-liquidation | 1,494.8 | 110-134 (WR 0.451) over 244 eps | uploaded 2026-08-23 23:07, evicted `55586926` |
| Slot B | `55675634`: reconstruction + market pull-forward + tile recovery | 1,501.3 | 169-157 (WR 0.518) over 326 eps | frozen 2026-08-21 19:06; higher score since 08-28 |

- Team standing on 2026-09-01: rank 1,574 of 7,210 (score 1,501.3). Donor (ReCurSiON, `55586926`
  route): rank 839, score 1,844.5, frozen since 2026-08-14. Gap 343 points, 735 places.
- Final Bradley-Terry ranking: not in this repo. It is produced after the deadline from the episodes
  played until about 2026-10-15. Record it here from the final leaderboard.
- Prize structure: ten equal prizes of $5,000 for places 1-10. The target was a stable top 10, not
  rank 1.
- **Update 2026-10-12 (board snapshot 15:19 UTC, 10,148 teams).** STRAF rank 4,479, score 909.6.
  Public scores have deflated since 1 September: `55726984` is 903.5 and `55675634` is 865.5 (not
  re-collected). Scores are not comparable across dates, so use ranks. The top 10 is led by
  M & M & P & Q at 3,298.0. Submissions closed on 2026-09-30. The final Bradley-Terry ranking is still
  to be recorded here once the board settles, around 2026-10-14.

**The honest headline.** Both final submissions replay a decoded action tape of another team's
policy, with a thin closed-loop overlay. They are not an original strategy. Our own heuristic agent
(`agent/`, planner → scheduler → executor) is the readable reference. It is not what sits on the
ladder. Measurement showed the copy is faithful (fidelity 0.12% median bank error). The copy still
lost about 1,036 points to its donor, and no desk instrument we built could say why (section 9).

---

## 2. The competition (from the organisers' page and forum)

- Dates: start 2026-07-29; team merger and entry deadline 2026-09-23; final submission deadline
  2026-09-30 23:59 UTC. Games continue about two weeks after the deadline (to about 2026-10-15), then a
  single Bradley-Terry tournament over the episodes between active agents produces the final ranking.
  Episodes against submissions deactivated since then are excluded.
- Format: two players, separate farms, one 720-turn season (30 days × 24 turns). Winner = most coins
  at the end. A match result changes the skill rating; the coin difference does not.
- Submissions: up to 5 per day. Only the latest 2 submissions are tracked; a third retires the oldest.
  Eviction is by date, not score. An inactive submission plays zero episodes.
- Each submission runs a validation episode against itself before it joins the pool.
- Organisers' answers: fertilizer is sellable; animals need no CARE to make fertilizer; fertilizer does
  not accumulate; the 24-day window in the price function is deliberate (setup-heavy early game).
- Organisers' statement on coupling: the shared market is the only interaction between the two
  players. "If you both sell the same product, you both suffer; the first seller gets the better price."
- Daily top-episodes dataset: episodes ranked by mean rating, up to 20 GB of replays per day.
  Replays are diagnostic and target curves, never a source of moves (behavioural cloning and
  trajectory copying are out of scope for this repo).

---

## 3. Engine ground truth

Verified deviations from the documentation. Each one below is either a tested fact in
`tests/test_engine_facts.py` (the engine-bump detector) or an official answer.

**Mechanics and yields**
- Care bonus increments by **+1** per day, not +2 as documented.
- Fertilizer is sellable (organisers confirmed).
- DIG is a no-op on an occupied coop or pasture; it works only on an empty one.
- A seed planted on day d counts day d as its first unwatered day. An unwatered tile becomes a weed the
  same night, because the end-of-day increment runs before the weed check.
- Melon caps at 6 units from age 10 (ages 11-12 add nothing); with fertilizer it caps at age 8.
- Strawberry yields exactly 4 times (ages 10, 12, 14, 16), then decays to a weed.
- Decay is −1 every 2 **steps** (not turns).
- Fertilizer needs no CARE. Each surviving animal makes one unit available per day, fed or not, and it
  does not accumulate.
- `PLANT` is atomic per turn: two units asking for one seed means neither plants.
- Planting uses the seed; one seed, two planters, zero plants.
- Invalid actions are silent no-ops. The server never reports an error. Anything untested locally is
  unknown on the server.

**Map and labour**
- The shed is not a tile. It is reachable only from the four centre tiles (4,4), (5,4), (4,5), (5,5).
- Hands spawn on the four centre tiles and ignore LOCKED. Locked tiles are passable from engine 1.32.3
  (fixed 2026-08-03); tile actions on them are no-ops.
- Shed drops and pickups are resolved before the LOCKED guard from 1.32.5. Routing from (4,4) is only
  sub-optimal, not broken.
- One HIRE is one market order, and `maxMarketOrdersPerTurn` = 10. Hands are wiped nightly. So a crew
  hired entirely in hour 0 cannot exceed 10, however high `hands_target` is set. This is why hands
  plateau at 12 in the top profile.
- The n-th hire of the day costs fib(n): 1, 1, 2, 3, 5, 8, 13, 21 (reset every morning).
- Step 718 is the last executable turn. A SELL on step 718 executes.

**Balance changes (the two bumps that changed the game)**
- **1.32.6 (live from about 2026-08-08):** the town-centre demand schedule is removed (flat −1 per
  product per tick). `townCenterSellInterval` goes 12 → 24, so the centre absorbs 30 units per product
  per season instead of 140 (−79%). Shops are drawn **with replacement**, `MAX_SHOP_INSTANCES = 8`.
  Expected distinct shop types 5.25; a given type absent with probability 34.4%; all eight present with
  probability 0.24%. MELON, with no shop buyer, depends wholly on the town centre. Consequence: a
  `town_pin="schedule"` harness setting samples a distribution that appears in 0.24% of episodes.
- **1.32.7 (installed; not yet live in the replays we measured on 2026-08-15):** market-only, scarcity
  side only, CARROT/TOMATO/EGG only, through a new `hinge` shape f(x) = u + 8·max(0, u−1)², with u = x/T.
  TOMATO and EGG are a strict no-op below their knee; CARROT changes from depletion 1 upward. The glut
  side is byte-identical for all nine products.

Engine-bump detector (no install needed): `pip index versions`, `pip download --no-deps --no-binary :all:`,
then diff the `.py` and the `.json`. The json carries `townCenterSellInterval`, `turnsPerDay`,
`maxMarketOrdersPerTurn` and `shedCapacity`. A `MARKET_PARAMS` change does not show in the configuration,
so it is detectable only behaviourally, from replay market pairs.

**The live discussion cannot be checked programmatically** (client-rendered forum). Only the version pin
and the byte diff are automatable tripwires.

---

## 4. Economics and market (for reading any ladder number)

Written against engine 1.32.4 (town numbers superseded by 1.32.6); base prices are a ceiling, not a
forecast.

**Profit per tile-day** (daily watering, no fertilizer, base prices): MELON 142.0 (10 tile-days, 6 units
at $250); CARROT 28.3; STRAWBERRY 23.8; WHEAT 22.5; TOMATO 17.3. Melon's apparent lead is fragile: it
depends entirely on the town centre. Selling 100 melons in one go realised $21,721 of the $25,000 the
first unit's price promised (87%); selling 200 realised $26,527 of $50,000 (53%).

**Animals (season totals, base prices, feed at $25):** goose $300 (coop, egg $50), cow $400 (pasture,
milk $160), sheep $500 (pasture, wool $200). Cared and fed: goose +$1,675, cow +$4,635, sheep +$5,575,
against +$275 to +$375 when only fed. The CARE bonus is a counter that adds `1 + interval` units per
production cycle (goose ×2, cow ×3, sheep ×4). The slower the animal, the bigger the multiplier.

**Land:** fixed order NE $1,000 → SW $2,000 → SE $4,000, 25 tiles per quadrant. Each quadrant pays back in
days at $25 per tile-day (NE 1.6 days, SW 3.2, SE 6.4). The real cost of land is the labour to work it.

**Labour:** 5 hands cost $12 cumulative and give 115 worker-turns a day. This is the best return in the
game, as long as there is work for them to do.

**Market price function.** `price(inv) = base + sign · amp · f(|inv − I0|)`, sign +1 below I0 (scarcity
raises price), −1 above it. `amp = target · base / f(T)`. Floor $1. I0 = 10,000 for every product.
`T` is one 5×5 quadrant's capacity over a 24-day calibration window.

| Product | Base | T | Below f / target | Above f / target | Price at I0−T | I0+T | I0+2T |
|---|---:|---:|---|---|---:|---:|---:|
| Wheat | 25 | 400 | sqrt .80 | log .20 | 45 | 20 | 19 |
| Carrot | 35 | 450 | log .20 | sqrt .70 | 42 | 10 | 1 |
| Tomato | 60 | 200 | linear .40 | sqrt .60 | 84 | 24 | 9 |
| Strawberry | 120 | 100 | sqrt .70 | linear 1.60 | 204 | **1** | 1 |
| Melon | 250 | 300 | log .20 | **sq 3.60** | 300 | **1** | 1 |
| Egg | 50 | 332 | linear .40 | log .20 | 70 | 40 | 39 |
| Milk | 160 | 122 | sqrt .60 | linear 1.60 | 256 | **1** | 1 |
| Wool | 200 | 105 | log .20 | **sq 3.20** | 240 | **1** | 1 |
| Fertilizer | 100 | 200 | linear .40 | linear .40 | 140 | 60 | 20 |

Premium products (strawberry, melon, milk, wool) fall to the $1 floor after modest surplus. Staples
absorb hundreds of units. Sell cliffs (units above I0 until the $1 floor, 1.32.4): wool 59, strawberry 62,
milk 76, melon 158, fertilizer 493, carrot 842, wheat and egg above 2,000.

Practical rules that followed: trickle, do not dump; floor sales add no inventory; the first seller gets
the better price; scarcity pushes prices up as well as down.

---

## 5. How to measure (the rules we settled on)

These came out of passes that were wrong in the way the rule now prevents.

**Reading the ladder**
1. A new submission starts at 600 points and plays a burst (about 14.6 episodes an hour for about five
   hours, 73 episodes), then 0.7-2.0 an hour. Judge nothing inside the first ~70 episodes. The burst is
   where the win rate lies: ours read 66.1% / 50.8% / 46.7% across thirds while the opponent median
   rose 1,212 → ~1,950. Nothing about the agent changed; matchmaking caught up.
2. Absolute score deflates across the pool. The invariant is **rank**. A score delta without a rank
   measures nothing.
3. Frozen decay is monotone in the rating band (median points a day, frozen teams): 2800+ −69.6;
   2400-2800 −66.9; 2000-2400 −73.5; 1600-2000 −56.4; 1200-1600 −35.9; 800-1200 −11.0; 0-800 −2.8. A
   decay figure is comparable only within a band.
4. A re-submission costs about 1,000 points and hundreds of places while it re-places. Never re-submit
   an unchanged agent.
5. Two readings taken at different times compare nothing. The field turns over under you (a
   byte-identical agent lost 182 points over 135 episodes). To compare two of our agents, field both and
   read them in the same window.
6. The live score is a diagnostic. The product is the two submissions in the slots at the deadline.
7. Readability: sample (episodes, score) per submission id, drop probes with no new episode. The rating
   is readable when |drift| ≤ 1 point per episode and its sign has flipped at least once.

**Acceptance (for any candidate change)**, in this order:
1. Per-opponent win/loss, per seat, never pooled.
2. Bradley-Terry over the bench (`--round-robin`).
3. Median bank (diagnostic only).
4. Mean difference in mirror (regression detector only).

Why: a third of our bank variance is the town's random shop draw, which lifts both seats and cancels in
win/loss. Premium-drain correlation with bank was +0.605, while the win rate was flat to inverted against
the same variable. The metric we led with was invisible to the one we were judged by.

**Experimental protocol.** Both seats always. Classify each knob before any A/B: does it change how many
tiles are occupied on any night? If yes it is an occupancy change, and both arms need `--town-pin basket`.
Dev seeds 0-47 to screen, holdout 100-147 to confirm, smoke 0-11 for controls, and 200-247 burned. Game
spread is about 19% of median bank, so 24-48 seeds is the floor. Pre-register every kill condition, and
write the final configuration comment before creating a screen checkpoint, because a comment edited later
changes the package fingerprint.

**Fill criteria** name their numerator and denominator. Sell fill (committed/ordered) was 0.863 and floor
fill 0.725; the two are different quantities. The market simulator reproduced recorded money in 4,314 of
4,314 transitions (worst difference $0.00), so committed counters are facts.

**The fidelity gate.** Any route reconstruction must replay against the donor's own recorded opponents in
their own towns before it can be shipped. Calibration: ReCurSiON's reconstruction replays at 0.12% median
bank error; the tetsuya reconstruction at 59%. Trace count and cross-trace agreement are not sufficient.
Advisory floor: market agreement below 0.90 is a kill.

**The impact ceiling.** Before any market-side arm is built, bound it on paper. The engine has one
market: `market_price` is a pure function of inventory, and quotes are symmetric, so a same-turn round trip
nets zero. Profit exists only for units held across turns, and your own trading walks the price against
you (WHEAT: inventory 10,000 → $25; 9,900 → $35; 9,500 → $47). Compute the maximum over splits with no
cash, shed or order limit. Convert at $253 per episode. Under about one rating point, do not build. Never
bound a market arm with a flow heuristic: `maxMarketOrdersPerTurn` caps orders, not units.

**Standing rules.** Price a lever in rating points, and price a programme as a whole. A pass ends in an
upload or it is not run. Retain earlier generations of opponents, because a change that only beats the
latest top-30 can lose to older agents still on the ladder. A STOP is final only after its own root cause's
implied control has been run.

---

## 6. What the top of the ladder does

**Current engine (B2, 60 newest episodes of the official dataset, all 120 seats on 1.32.6+, median bank
$82,747).** Median profile: money $516 at d5, $4,863 at d10, $16,720 at d15, $48,560 at d20, $82,747 at
the end. Planted tiles 56 / 62 / 60 / 61 at d10 / d15 / d20 / d24. Hands 3 / 14 / 9 / 14 / 10 at d5 / d10 /
d15 / d20 / d29. Animals peak at 9 cows and 4 sheep. Three quadrants (SE never). Crop tile-days:
STRAWBERRY 577, WHEAT 559, MELON 180, about 1,316 in total.

- **Production is copied.** Nine teams with six or more seats show almost identical tile-days and units.
  Winners and losers (57 of 57 seats) are identical in tiles, hands, animals, quadrants, tile-days, units,
  first sell day and batch.
- **The edge is realised price on three shallow-curve products.** The same units produce a 1.49× spread
  in final bank ($63,866 to $94,850). Realised price spreads: STRAWBERRY 2.75×, WOOL 3.70×, MILK 3.49×.
  WHEAT (1.12×) and MELON (1.17×) are flat. The top plays a sell-timing contest on three products. Teams
  differ in which premium they win.
- Our own realised prices on the same replays: MILK $210.62, WOOL $196.81, with 1.7× the opponent's wool
  volume. Our sell side was not the problem. Our production was: 415 crop tile-days against 1,316.

**Earlier snapshot (1 August, before 1.32.6).** Winners and losers sold and planted in near-identical
volumes (plant 74 vs 81, sell 331 vs 322, hire 291 vs 295), and winners planted and bought less land. The
difference was when, what, and at what price. Strawberry was the primary crop for 515 of 580 seats, which is
the de facto meta. Its linear collapse made it the largest arbitrage for anyone who sold first.

**Fingerprints (31 July).** The record holder (bank $157,449) hired 10.8 a day, peaked at 13 hands, bought
land on day 0 and planted 105 tiles, primarily strawberry. A mid-ladder farm with $38,514 hired 6.8 a day,
peaked at 7 hands and never bought land. Winners disagreed about which crop mattered. What repeated was the
economics around the plant: crew size and land timing.

**Other sources, and what each was used for.**
- Rayk Kretzschmar's reference ladder (MIT): graded tiers 0-5, $3,000 to $46,211, with a byte-identical
  scheduler and a different POLICY dict per tier. Used as regression opponents. Tiers 6-9 separate only
  through the market layer ($164 to $2,617 per episode); cited, not used (their trace encoding is outside
  the MIT grant).
- HarvestForge-X's majority-vote reconstruction (`3000-socre`): the method that built the donor route. It
  priced its own premium-lead market layer at +$1,912 per episode when you own the route.
- Kaito Fukami's multi-generation write-up: (1) tuning against the current top-30 alone loses to old
  generations returning with a small overlay; (2) keep three disjoint evaluation surfaces; (3) the
  selection key we adopted; (4) **state aliasing**: a public-state kNN router won selection 70/78 against
  67/78 and lost after the freeze 31/38 against 33/38. More classifier confidence cannot recover future
  information. Every "recover the donor's conditioning from replays" arm we tried had this shape.
  (5) Their architecture was one open-loop backbone with four closed-loop components, of which we measured
  three and never examined the fourth (a WHEAT market maker). (6) An artifact contract: route hash, size,
  latency, parity call count, and the archive SHA reproduced under two filenames.

---

## 7. What we built

**The submitted policy is a tape, not a planner.** The two final submissions are self-contained `main.py`
files built by `analysis/build_tape_overlay_submission.py` (augment mode for `55675634`, liquidate mode for
the H2 variant on `55726984`) and `analysis/build_reconstruction_submission.py`. The output inlines the
overlay code and embeds a stream. It has no runtime import from `agent/`.

- **Reconstruction.** Per decision point, the modal action across the donor's own 50 traces (a
  majority vote). A policy measurement, not a copy of one performance. Fidelity 0.12% median bank error;
  the cross-trace agreement was 0.993 production and 0.980 market.
- **Tile recovery overlay** (`55675634`). Six rules that repair weed and decay losses on the donor's own
  farm. SMOKE 336-0-0; the overlay's own occupancy bias runs in its favour and is not separated.
- **H2 tail-liquidation** (`55726984`). Rule: for STRAWBERRY, from day 22 on, skip a sale while the price is
  below $25. Force a sale if a unit has been held more than 4 days, if holdings would exceed 12 units, if
  step ≥ 686, or if fewer than 4 days remain. A sale is issued only on a round whose queue has at most nine
  orders. Parameters were frozen before the confirmation. The 12-unit cap is a shed-headroom bound: 20 units
  overflowed the 100-unit shed in 8 of 253 episodes; 12 or 16 units in none.

**The heuristic agent (`agent/`).** Planner, scheduler and executor, with guard tests and engine-fact
tripwires. Its per-turn cost is about 0.02 ms. It was our research platform and our reference, not what
reached the ladder. The tape overlay (`agent/tape_overlay.py`) is the code path the H2 builder copies.

**Harness and instruments.**
- `harness/`: play, compare (paired seeds), ladder (Bradley-Terry over a bench), metrics (market walk
  checked against recorded money), checkpoint fingerprinting, town pinning.
- Instrument A (`analysis/s10_replay_bench.py`): replays every recorded ladder episode with our seat's
  action stream substituted and the opponent seat as a tape. The α-control reproduced 509 of 509 episodes
  bit-exactly. The H2 calibration reproduced the frozen result on 412 confirmation episodes.
- The shared replay reader (`analysis/s8_replay_io.py`) and market ledger (`analysis/s9_market_ledger.py`).
- The collector (`analysis/archive_sync.py`) for the kaggle CLI; the top-K profile (`analysis/b1_top_profile.py`).

**What did not ship, and why.** Each of these was measured and stopped. Section 9 holds the numbers.

---

## 8. The final submissions and their evidence

**H2 gate chain (`55726984`).** Found on the dev set: W/L 232-180 to 255-157, c = 23, b = 0, McNemar
p = 2.4e-7 across the full 412-episode confirmation set. The dev pass (c = 11, b = 0, p = 0.0010) and the
pre-declared holdout (c − b = +4, p = 0.125, against a pre-declared bar of c − b ≥ +10 and p < 0.05) were
both reported; the holdout failed and is burned. A 159-episode fresh confirmation gave c = 8, b = 0,
p = 0.0078. Margin +$458 per episode, gained on the opponent's bank (−$357) more than on ours (+$110).
That is why median bank alone cannot see it.

**Instrument A head-to-head (S16, 539-episode confirmation set).** H2 clears p < 0.01 on both seats against
the shared base (seat 0 p = 2.4e-4, seat 1 p = 1.2e-4). The `55675634` overlay (market pull-forward plus tile
recovery) clears neither seat (seat 0 p = 0.035, seat 1 p = 0.55), before its own occupancy bias is
subtracted. Only 68.1% of episodes it fires on reproduce bit-exactly. The live ladder could not separate them
(CMH p = 0.961; the minimum detectable effect at 80% power was 20 points on a 90/105 read).

**Slot policy used.** `55586926` (the reconstruction alone) was evicted by `55726984` on 2026-08-23, with the
route surviving inside it. The next upload was planned to drop `55675634`, the decision the S16 evidence
supported.

**Archive identity.** The augment-path archive reproduced as sha256 prefix `f6f46c25` in the S9 gate. No
full archive hash of either final submission is recorded in the repo. The donor stream hashes cited in
earlier docs (`1d9e0efd`, `89ce9e86`, `09250ef5`) match no artefact still on disk.

---

## 9. The measured STOP register

Each row is one increment, its verdict, and the mechanism that binds. The numbers are from the pass that
measured them.

| # | Increment | Verdict and binding mechanism |
|---:|---|---|
| 1 | Land expansion ×3 (v1c) | STOP. Capacity and routing bind, not land. |
| 2 | Wheat 12→24 tiles, crew 10→12 (v1j) | STOP, −$759. One HIRE = one order, cap 10 a turn, hands wiped nightly. Not a cost problem. |
| 3 | Hands target 12 (v1o.2) | STOP on the priced gate: +$4,145 but $478 priced loss against a $415 budget. 12 hands emit more priority-0 WATER than FEED survives. |
| 4 | Animal-upkeep protection, 7 variants (v1o.3) | STOP twice on acceptance. Escapes 13 → 0, but crop tile-days 612 → 574. 13 escapes ≈ $135/ep against ≈ $1,180/ep of production. Mirror read +$4,878 (p = 3e-6): the clearest case of mirror as a ceiling. |
| 5 | Feed round (standing) | At least one animal unfed for 100% of hours of a median day from day 9. Any reordering inside tier 0 is zero-sum. |
| 6 | Strawberry last-plant day 16/20 (v1o.1) | STOP, structural. Breaks production counters, loses $4.1k / $7.9k. |
| 7 | Late-season replant (v1k) | STOP, −$167 (CI spans 0). Filled tiles with a cheap crop. On the shelf: re-test with a crop above $50 per tile-day. |
| 8 | Wheat → carrot by $/tile-day (v1l) | STOP, −$7,161 per episode. |
| 9 | Melon race (v1m, v1m.2) | STOP at smoke (28 unexplained escapes); E1 re-scored under the delta rule and passed; shipped as v1m_d2. |
| 10 | Fertilizer capture (v1n) | Closed: 62.7% of the loss is structural; the fixable 28 units are ≤ $720 per ep. |
| 11 | 12-14 animals in one step | Hard-gate failure, 660-885 escapes. Feed logistics, not market saturation. |
| 12 | Herd 13 on the reserve (3 arms) | STOP at smoke, −$15k to −$21k per ep. The ramp is not the lever: three animals past ten sit 7-8 tiles from the shed (herd distance +59%). Cash was fixed; logistics was not. |
| 13 | Shop-adaptive sell floor | −$1.1k to −$24.8k per ep. Production-constrained, not glut-constrained. (Revised by row 31.) |
| 14 | Herd re-composition toward cow | Damage larger in towns with a yarn store: MILK saturation in mirror. |
| 15 | Shed-access routing fix (D26) | Net-negative; reverted. Routing distance must be decoupled from urgency first. |
| 16 | Herd compaction (v1p.1) | STOP at smoke, −$875. Escapes exactly 2 in all 24 orientations. |
| 17 | Zone assignment (v1p.2) | STOP at smoke, −$6,966. The partition has no cross-turn memory. |
| 18 | Two controls on v1p.1 | STOP. Refutes v1p.1's root cause and finds a second, independent mechanism. The ten pasture slots are already the ten nearest of 13 available. |
| 19 | Sticky zones (v1p.2b) | STOP at smoke, −$2,689. The constraint is not which tasks a unit is offered. |
| 20 | Min-cost matching oracle (item ④) | Refuted as the herd-13 unblock. Whole-pool optimum +$4,709 per ep, reached only by underfeeding. Buildable arm +$812. Leg 2 moves the wrong way. Any matcher must keep urgency in its cost. |
| 21 | Market overlay on the donor tape (T2) | STOP at smoke. Shed capacity pins realised strawberry price. Re-measured on 253 live replays: our route peaks at 84/100 (median 72), and the binding figure is the minimum free capacity at day boundary, 16 units. Bounded to ≤ 12 held units; the H2 rule uses exactly that. |
| 22 | In-place SELL reordering ("the Cleo rule") | Refuted analytically and empirically: lockstep across players means reordering cannot move realised price. |
| 23 | Own-farm repair (S6 step 2a) | STOP at phase 0. Loss is 100% WHEAT on five tiles; ceiling $599/ep; full recovery +2.4 points, 0.09% of the gap. |
| 24 | Restore the erased sell timing (S6 step 2b) | Refuted. The donor's strawberry rule is a fixed global calendar, invariant across 50 towns; the vote already reproduces it. |
| 25 | Market channel, channel-wide (S6 step 2c) | Every market channel is town-invariant. Family closed. |
| 26 | Production channel (S6 step 2d) | Town-reactive, but bounded at $597/ep = +2.4 points. Its bank-gap decomposition was circular (Kaggle pairs by rating). |
| 27 | Loss tail (S6 step 2e) | Shop composition explains bank (R² 0.37); desync explains nothing. 11 of 178 episodes flippable, +6.2 points upper bound. The 2.14× bank spread is the town. Programme closed. |
| 28 | S7 leg 0 census | A re-reading: retired three of this document's own claims. |
| 29 | Re-donor to a top-4 route (S7 Leg A) | KILL by measurement. Every top-4 candidate is state-adaptive (cross-trace agreement 0.25-0.37 against ReCurSiON's 0.993). Tetsuya's reconstruction lost 59% median bank against its own opponents. The "ship anyway" rule would have shipped a chimera. |
| 30 | WHEAT market maker (S7 Ship B) | KILL by paper bound. Ceiling $2.0k per ep = 7.9 points with no cash, shed or order limit. The roof is our own price impact. |
| 31 | Re-test of the glut constraint | Reopened. Across all nine products the route is glut-constrained: WOOL sits at the $1 floor a median of 30 turns per episode, MILK 7, STRAWBERRY 2. Premium products are deep in collapse. Status: open and untested. |
| 32 | Leakage-safe dump predictor (S11 B2.5) | KILL, final. Precision MELON 0.10 against 0.076 base; STRAWBERRY 0.48 against 0.191. Target was ≥ 0.70 on both. |
| 33 | Seat gap of 18 points (S13) | Not established at this size; a ~5-point seat effect is not ruled out and not actionable. CMH p = 0.204; dropping each submission's first 70 episodes shrinks the pooled gap from +0.052 to +0.020 (placement burst). |
| 34 | WOOL as second flip lever (S14) | KILL. WOOL shed stock is zero on every trough day. Production-gated like MELON. |
| 35 | MELON wave 2 worth its tile-days (S14) | Answered: yes. $57.5 per tile-day net of seed. Deleting it costs $9,044 per ep. Do not shrink it. |
| 36 | Which live overlay is stronger (S16) | Live ladder: not separable. Instrument A: H2 clears both seats; the shipped overlay clears neither. Live ladder cannot arbitrate a 5-point edge before the deadline (about 1,251 episodes an arm, 48-57 days, against about 26 left). |
| 37 | MELON re-phasing (S15 Phase 1) | STOP at gate 2. Gate 1 passed (+$4,558 on 539 confirmation episodes). Gate 2 failed: idle hand-turn capacity 25 against a floor of 42 turns, and free land 6 tiles against 14 needed. |

**Blocked before build** (no row number): the MELON pull-forward. Our own melon stock is zero on every
day through 18; the day-10 and day-20 blocks are harvest events sold within the day, so no overlay
degree of freedom exists. Genuinely held inventory was about 12 units (about $650 per episode). Also, the
`liquidate` and `augment` modes of the tape overlay are mutually exclusive, so any new arm must compose
with H2, not replace it.

---

## 10. What did not work, in one place

- More hands, more land, more animals, as such. Volume was identical between winners and losers. Our own
  herd and crew could not be scheduled to reach the top's animal count: the feed round never closes and
  one HIRE is one order.
- Tuning against a local bench. Our round-robin ranked v1i above v1h, and the ladder ranked them the other
  way. A local bench that disagrees with the live ordering is not an instrument.
- Re-donoring to a top-4 route, and any "recover the donor's conditioning from replays" arm. Both are state
  aliasing in the sense of Kaito's write-up.
- A market maker sized by flow heuristics. Price impact sets the roof, not the order cap.
- Reordering SELLs inside a tier, and any change to the sell calendar of a fixed-calendar donor.

---

## 11. Still open, for the post-mortem

1. **The 1,036-point gap to the donor is unexplained.** Every desk instrument compares traces to each other
   and reports fidelity. None has ever scored our route against a real ladder opponent. That remains the
   open question. The only instrument able to answer it is Instrument A on the final pair, with the
   opponents as tapes, and it is priced to first order only.
2. **Row 31 (glut-constrained route) is the one lever never tested.** The premium-product collapse is
   measured. Whether a sell-floor can be taken without the shed wall (row 21) and the common-mode result (§5.2
   of the old plan) has not been tested.
3. **The reconstruction chain cannot be rebuilt from this repo.** The builder reads artefacts from
   `data/derived/` that are absent, and it cites a cluster script that is in neither git nor on disk
   (`s6_step1b_cluster`). The byte-identical check of either final submission was never run here.
4. **The final Bradley-Terry ranking** is not in this repo. Fill it from the final leaderboard.
5. **Live evidence on 1.32.7.** The hinge curve for CARROT, TOMATO and EGG was not visible in the live
   replays we measured (2026-08-15 dataset: all 1.32.6). Whether it reached live play is unknown here.
6. **Seat effect.** Not established at 18 points; not refuted. Power at a 5-point effect was about 24%.

---

## 12. Data policy and provenance

- The repo is public. Routes, submission packages, replays, derived data and gate replays are
  gitignored. `gates/` tracks only the aggregate `results.json`. Do not commit competition data.
- Competitor notebook source was never executed or extracted. Only markdown, tables and printed statistics
  were read as evidence.
- Replays are game data and may be used as route sources, with provenance recorded
  (episode id, seat, team, sha256). Licensing exposure at the prize stage (the "own original work"
  warranty) is recorded here and was not re-opened.
- The earlier planning, journal and audit documents were consolidated into this file. Their full text is in
  git history at commit `920ef63`.
- The engine mirror `engine_reference/` is read-only. The test suite compares it byte-for-byte with the
  installed package, and every engine-fact test reads the installed package, never the mirror.

**Code references to the removed documents.** Comments in the code cite the old documents by name and
section (for example "old roadmap §6 row 21"). Those citations resolve to the pre-consolidation files
at commit `920ef63`: `git show 920ef63:ROADMAP.md`, and the same for the journal, the audit and the
plans. The submission builders are the one exception. Some of their citations are written into the
submitted `main.py` text, and changing them would change the archive bytes, so they keep the old wording.
The removed analysis scripts can be recovered the same way, with `git show 920ef63:analysis/<name>.py`.
