# Notebook meta read: kaggriculture competition notebooks

Post-mortem of the public notebooks for the kaggriculture competition, run after the deadline. Notebook code was read as data and never executed, and no notebook code is copied into this file. Per-notebook cards are in `notebooks/cards/` (gitignored). The harvest tool is `analysis/notebook_harvest.py`.

## 1. Coverage

Universe 689 refs: 602 from the competition listing (both sort orders agree) and 87 found only by keyword search. Downloaded 689; unavailable 0. Relevant 664; not relevant 25. Representatives 544; near-copies 120, in 60 clusters. Cards 664. Snapshot: competition listing and leaderboard of 2026-10-12 (15:19 UTC), replays through 2026-10-11.

Three limits apply throughout. Kaggle does not expose creation dates in this listing, so `created` is n/a. The CLI exposes no version, so `version` is the first 12 hex characters of each source's sha256. Some near-copy cards were written by hand rather than generated, so their architecture text is not uniform.

## 2. Strategy families

Twenty-three families (raw card labels are in `notebooks/_index/family_map.csv`). Cards count near-copies. The most-voted member's card gives its architecture and claimed result as the notebook states them; these are the author's descriptions, not verified results. Runs are the first and last `last_run` of the family's cards.

| Family | Cards | Most-voted member (rank, votes) | Its card: architecture | Its card: claimed result | Runs |
|---|---|---|---|---|---|
| heuristic-and-rule-agents | 123 | `guruprasaathas111/kaggriculture-master-engine-v3` (1824, 123) | master engine (V6 in its title): integrates 13 pre-computed public route tapes, a sales reservation window with debt accounting, a financed SE-quad... | proven 95.1% win rate and +17.5M net margin (cell header) | 2026-06-19 to 2026-09-30 |
| replay-analysis | 72 | `raykkretzschmar/kaggriculture-findings-from-zero-to-top-meta` (2400, 207) | notes and working diary, not a single policy: a local agent built from repeatable moves of the current leaders, tested from both seats | n/a (working notes; results in the diary sections) | 2026-07-31 to 2026-10-11 |
| engine-and-market-analysis | 67 | `jaxa623/2802-two-identical-agents-90-points-apart` (1049, 71) | not an agent: presentation of two identical agents rated 90 points apart; the notebook is largely CSS for readability | two identical agents 90 points apart (title) | 2026-07-31 to 2026-09-24 |
| tape-and-route-replay | 50 | `yhay81/shop-router-0909` (193, 137) | rule-based router in a 234-line main.py (writefile): plan chosen at step 144 from the first two revealed shops; DIG inserted when weeds block plant... | n/a | 2026-08-02 to 2026-09-13 |
| evaluation-and-measurement | 49 | `raykkretzschmar/kaggriculture-rank-your-agent` (2400, 148) | ranking tool, not a policy: a seat-swapped round robin against a fixed ladder of tiers, ranked by Bradley-Terry; writes a submittable submission.ta... | tier 5 banks ~46k, while the meta band banks ~149k-165k | 2026-08-02 to 2026-10-01 |
| ahmed-V-series | 45 | `ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins` (550, 298) | rule-based agent in a 2,626-line main.py built on V37; feed rule compares production value with wheat cost | reacting development (704): V38 646/58/0 (91.8%) against V37 609/67/28 (86.5%) | 2026-09-03 to 2026-09-30 |
| kaito-lineage | 28 | `kaitofukami/25-27-strict-future-v27-midgame-meta-reset` (868, 219) | dominant low-entropy HIRE4 opening kept; the stale continuation replaced; a higher-scoring seat router rejected after failing 2 of 3 real losses | captured after policy freeze: v27 25/27 against previous v26 14/27 (seat 0 16/17, seat 1 9/10) | 2026-08-03 to 2026-09-30 |
| no-strategy-text | 28 | `flexonafft/kaggriculture-multi-route-farming-agent` (3214, 125) | n/a (five cells; no defs or prose visible to the structure skim; the strategy was not read) | n/a | 2026-08-03 to 2026-09-30 |
| tschinkel-2945-lineage | 25 | `thomastschinkel/the-2945-farm-96-vs-the-top-10-public-bots` (2775, 162) | route replayer (v9/4), standard library only: the public lineage's recorded 720-turn schedules, re-selected as shops unlock; about 3 ms per turn | 2944.7 on the live ladder for this exact file (submission 56269928), 128-73 over its first 201 ladder games... | 2026-08-09 to 2026-09-28 |
| rl-and-learned | 19 | `andrewsokolovsky/kaggriculture-breaking-the-tie` (4504, 75) | learned router: behaviour cloning from a teacher plus counterfactual oracle labels and DAgger rounds; a RouterNet MLP chooses between teacher and e... | promotion gate: a learned candidate is submitted only if it passes the held-out evaluation against the teacher | 2026-07-07 to 2026-09-23 |
| tutorial-starter-baseline | 19 | `bovard/kaggriculture-getting-started` (9343, 1242) | official-style tutorial with a short example agent (melon_maxxer, 98 lines): step toward target tiles, sell above a threshold | n/a | 2026-07-30 to 2026-09-23 |
| aurax-reactive-router | 18 | `aurax7/kaggriculture-shop-router-reactive-v5` (34, 99) | rule-based reactive shop router in a 3,316-line main.py (111 helper defs) with a parent liquidation layer | n/a | 2026-08-12 to 2026-09-19 |
| packaging-and-embedded-payload | 18 | `jek1wantaufik/building-a-kaggriculture-ai-agent` (2732, 81) | n/a (one code cell with a source-splitting helper, split_source; the strategy was not read) | n/a | 2026-08-04 to 2026-09-27 |
| clone-and-preemption-sales | 17 | `boatlee/84-84-base-public-holdout-v14-clone-preemption` (1195, 183) | complete rule-based agent (V14, payload in base85 parts, not decoded); production schedule reconstructed from public Gold-tier replays; premium-sal... | V14 vs Ueddy replay proxies 48-0 and vs CemBas replay proxies 48-0 | 2026-08-08 to 2026-09-22 |
| blacklions-public | 15 | `blacklions/kaggriculture-v20-adaptive-queue-public-experiment` (1158, 7) | unchanged single-file artifact from Tetsu's public adaptive strategy, reproduced and hash-checked; one official smoke game | historical-opponent league: 2,010 wins, 0 draws, 0 losses, 0 errors | 2026-08-02 to 2026-08-09 |
| boatlee-clean-room | 15 | `boatlee/v16-rc5-high-score-8c-4s-premium-market-lead` (1195, 324) | rule-based agent (247-line main.py): compact 8 COW and 4 SHEEP production route with a one-turn market lead | schedule matched at 99.91% of decision steps | 2026-08-03 to 2026-09-02 |
| moon-frontier-lineage | 15 | `romantamrazov/kaggriculture-hamburger` (1338, 131) | n/a (the Hamburger lineage notebook; the cells were not read beyond the title) | n/a | 2026-08-01 to 2026-09-22 |
| pipe-lineage | 11 | `nathanjacob/kaggriculture-pipe-7-wheat-microstructure` (1155, 66) | one parameter change on the V45 base: buying seventy wheat is no longer the best first-turn action (microstructure of the wheat round trip) | one parameter change: 179 wins, 1 loss, 0 ties across a 10-agent tournament over 1,800 games | 2026-09-14 to 2026-09-21 |
| compiled-cpp-policy | 9 | `yhay81/three-day-shop-router` (193, 126) | hybrid: C++ policy (136 lines) with a six-day budget guard, tape and plugin ABI behind a Python bridge (209 lines); base tape with turn-360 switches | n/a | 2026-09-03 to 2026-10-02 |
| x-and-other-named-agents | 7 | `yamakawanin/kaggriculture-adaptive-public-state-multi-route` (548, 26) | adaptive public-state multi-route version of the programme agent (cells not read beyond the title) | n/a | 2026-08-14 to 2026-09-19 |
| educational-decision-aid | 6 | `prvsiyan/kaggriculture-visible-price-switch-lab` (769, 7) | small standalone lab: a state-conditioned crop decision that uses only the market prices visible in the observation (choose_fast_crop, route_late_w... | n/a | 2026-09-12 to 2026-09-20 |
| herd-safety | 6 | `arsgorynich/herd-safe-v3-experimental-risk-aware-feed` (127, 74) | rule-based agent: a sale predictor for opponent sales gates herd feeding; packaged source (zlib payload, not decoded); derivative of Dmitrii Gluzdo... | Herd-Safe v2 6/2/0 against 0/4/4 and 0/0/8 in the table | 2026-09-23 to 2026-09-29 |
| harvestforge-x | 2 | `salemali7/kaggriculture-2900` (1866, 80) | HarvestForge-X 2900 variant: reconstructed from reference runs 92165990, 92185587 and 92223213; payload loader and valid_action; archive builder | 60/60 wins | 2026-08-22 to 2026-09-17 |

## 3. Meta timeline

Representatives only, by the notebook's last run. Counts are representatives per period, with the three most common families and the most-voted representative.

- **launch to 2026-08-10** (134 representatives). Most common: heuristic-and-rule-agents 34, replay-analysis 17, tape-and-route-replay 15. Most-voted: `bovard/kaggriculture-getting-started` (1242 votes, rank 9343).
- **2026-08-11 to 2026-08-31** (161 representatives). Most common: heuristic-and-rule-agents 38, evaluation-and-measurement 23, engine-and-market-analysis 23. Most-voted: `boatlee/v16-rc5-high-score-8c-4s-premium-market-lead` (324 votes, rank 1195).
- **2026-09-01 to 2026-09-30** (243 representatives). Most common: heuristic-and-rule-agents 31, ahmed-V-series 29, engine-and-market-analysis 27. Most-voted: `ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins` (298 votes, rank 550).
- **from 2026-10-01 (post-deadline)** (6 representatives). Most common: replay-analysis 4, evaluation-and-measurement 1, compiled-cpp-policy 1. Most-voted: `leoprovorov/a-song-of-ice-and-fire-fixed-flexible` (139 votes, rank 735).

Counts show when notebooks were run, not how often a strategy was used.

## 4. Latest meta read

- Representatives run on or after 2026-09-01: 249. Of these, 23 have authors ranked 300 or better on the 2026-10-12 leaderboard and 5 are ranked 100 or better.
- By kind: agent 160, strategy-analysis 84, replay-analysis 5.
- Most common families: heuristic-and-rule-agents 31, ahmed-V-series 29, replay-analysis 29, engine-and-market-analysis 27, evaluation-and-measurement 22.
- Most-voted: `ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins` (298 votes), `leoprovorov/kaggricult-man-reverse-engineering` (184 votes), `thomastschinkel/the-2945-farm-96-vs-the-top-10-public-bots` (162 votes).
- Post-deadline representatives (6): `destbreso/x-ray-your-agent` (strategy-analysis), `farukece/kaggriculture-episodes-guided-tour-of-the-dataset` (agent), `georgymamarin/kaggriculture-what-2600-farms-do-differently` (strategy-analysis), `jwj1342/kaggriculture-final-strategy-and-lessons` (agent), `leoprovorov/a-song-of-ice-and-fire-fixed-flexible` (strategy-analysis), `mqingcs/kaggriculture-observed-production-and-last-dance` (strategy-analysis).
- Replay facts from the same set (section 5): 96.7% of seats make their first sale on day 0, and 67.6% finish in four quadrants.

## 5. Claim check against replays

Each claim is a concrete, checkable statement from a notebook. The test runs on the field: the 768 seat traces of the top-50 post-deadline replays (394 episodes, `data/archive/raw/top50_post0930_2026-10-12/`). None of the claimants' own games are in that set, so the field stands in for them and the table says where it cannot.

| # | Notebook | Cell | Claim (quoted, 15 words or fewer) | Field test | Verdict |
|---|---|---|---|---|---|
| 1 | `raykkretzschmar/kaggriculture-rank-your-agent` | cell 5 | "tier 5 banks ~46k, while the meta band banks" (card figure: 149k to 165k) | Median final money 103,756 over 768 seats (quartiles 93,902 and 115,612); 1.4% of seats fall in 149k to 165k. | contradicted |
| 2 | `fierus/xray-kaggle` | cell 11 | "contrata de media 280,0 veces por partida" (hires per game, average 280) | Field median total hires 300 per game (mean 295.1); 280 is 6.7% from the median. | corroborated |
| 3 | `fierus/xray-kaggle` | cell 11 | "Primera venta ejecutada: día 0" (first sale on day 0) | First sale on day 0 for 742 of 767 seats (96.7%). | corroborated |
| 4 | `fierus/xray-kaggle` | card claimed result (cell not located) | "mean final money 100,749" | Field mean final money 105,330; the claim is 4.3% from it. | corroborated |
| 5 | `aasim2003/notebookb3a3ef21c3` | cell 0 | "I hire about ten" (workers each morning) | Field median total hires 300 over the 30-day season, about 10.0 per day. | corroborated |
| 6 | `revanthtambisetty/kaggriculture-economy-mechanics` | cell 3 | "Slow-decay products (WHEAT, EGG, FERTILIZER) hold most of their price" | Wheat and egg reach $1.50 or less in 0.0% and 0.0% of seats. The unit count (past 200 units) is not in the scan. | corroborated |
| 7 | `revanthtambisetty/kaggriculture-economy-mechanics` | cell 3 | "Fast-decay products (STRAWBERRY, MELON, MILK, WOOL) reach the $1 floor" | Seats reaching $1.50 or less: wool 65.4%, milk 27.9%, strawberry 22.3%, melon 0.7%. | contradicted |
| 8 | `busyaprime/the-best-thing-to-farm-has-a-market-of-59-units` | cell 0 | "Sheep return 266.7 coins per tile per day" | The scan has no per-tile income; not testable here. | unverifiable |
| 9 | `busyaprime/the-best-thing-to-farm-has-a-market-of-59-units` | cell 0 | "market absorbs 59 units before the price hits its floor" | The scan has no unit-level market data; not testable here. | unverifiable |
| 10 | `yhay81/six-day-public-state-fieldbook` | cell 0 | "recorded 22,795 wins, 58 draws, and 1,211 losses in 24,064 games" | The claimant is not in the top-50 set. The 0.9485 point rate recomputes from these counts (0.9485). | unverifiable |
| 11 | `fleongg/kaggriculture-public-2830-4-v21-1-no-preemption` | cell 0 | "Kaggle showed a verified public score of 2830.4 at publication time" | A publication-time score for a submission outside the top-50 set; not testable here. | unverifiable |
| 12 | `jeffmarcecadet/reverse-engineering-rank-5-thunder-thunder` | cell 1 | "Land on exactly days 6 and 10, three quadrants, never the fourth." | The claimant is not in the top-50 set. 67.6% of seats finish in four quadrants, so the claim is not a field pattern. | unverifiable |
| 13 | `kaitofukami/25-27-strict-future-v27-midgame-meta-reset` | cell 0 | "captured after policy freeze" (25/27) | The claimant is not in the top-50 set; a frozen-policy count, not testable here. | unverifiable |
| 14 | `destbreso/what-1-32-7-changed-and-what-it-did-not` | cell 0 | "Three price curves changed on 2026-08-15." | The top-50 set is post-deadline and has no pre-change replays to compare; not testable here. | unverifiable |
| 15 | `kaitofukami/177-180-fresh-top-30-v21-1-conditional-memory` | cell 0 | "On a newer Top-30 snapshot, its Dennis route fell to 19/46" | The snapshot is not in this set; not testable here. | unverifiable |

Tally: 5 of 15 match the field, 2 do not, and 8 cannot be tested with this set.

## 6. Against our record

Proposed wording only. This file does not edit RECORD §6, §10 or §11; each line names the notebook and cell it rests on.

- **§10, first bullet (more hands, more land, more animals).** Proposed addition: "A public replay analysis finds winners mostly do not take more actions" (`busyaprime/what-actually-wins-on-the-kaggriculture-ladder`, cell 7, heading "Do winners just do more? Mostly not").
- **§10, second bullet (local bench).** Proposed addition: "A local holdout of 177/180 did not carry over: on a newer Top-30 snapshot, the old public v21 route fell to 19/46" (`kaitofukami/177-180-fresh-top-30-v21-1-conditional-memory`; cell 0 reads "On a newer Top-30 snapshot, its Dennis route fell to 19/46"; the card's claimed result names the old public v21 route).
- **§11.1 (1,036-point gap).** No card in the set reports a live-ladder score for a route of this kind that I found. The nearest, `andrewsokolovsky/kaggriculture-breaking-the-tie`, gates its learned candidate only against its own teacher (card, claimed result). Proposed: "Still open: no public notebook reports a live-ladder score for a route like ours; the closest gates only against its teacher."
- **§11.2 (row 31, glut-constrained route).** `xreina8/kaggriculture-300-melons-return-36-of-face-value`, cell 0: "selling 300 melons returns 36% of face value". It measures what a large sale returns, not a sell-floor. Proposed: "Public notebooks measure what a large sale returns (300 melons: 36% of face value); none tests a sell-floor, so row 31 stays untested."
- **§11.4 (final Bradley-Terry ranking).** `raykkretzschmar/kaggriculture-rank-your-agent`, cell 0: "ranks everyone with Bradley-Terry". Proposed: "A public tool implements seat-swapped round-robin Bradley-Terry ranking; it is a candidate for reproducing the final ranking from the final leaderboard (not run)."
- **§11.5 (1.32.7 hinge curve).** `destbreso/what-1-32-7-changed-and-what-it-did-not`, cell 0: "Three price curves changed on 2026-08-15." Its card names tomato, carrot and egg, and cell 0 reports that recorded episodes "replay identically on either build, 40 of 40 banks". Proposed: "A public notebook names tomato, carrot and egg as the three products changed on 2026-08-15, and reports that recorded episodes replay identically on either build. Unverified here."
- **§11.6 (seat effect).** `yhay81/your-seed-does-not-fix-the-town`, cell 0: "draws each town shop from the same random" stream as weed spawns (card architecture line), and a crop farm's season swings 28% from worst draw to best. A paired-seat design assumes both seats face the same world. Proposed question: "Before reading the 18-point gap, check whether the power estimate allows for world variance from shared shop draws."

## 7. Appendix: every relevant notebook

One line per relevant notebook: family, then the card's architecture line (cut to about 110 characters). Near-copies point to their representative.

| Ref | Family | Summary |
|---|---|---|
| `aanaakaliil/notebook858a103738` | tutorial-starter-baseline | rule-based: one 30-line agent() function, submitted with the kaggle CLI |
| `aasim2003/notebookb3a3ef21c3` | heuristic-and-rule-agents | rule-based bot: a play() function written to main.py (913 lines); hires and sells by fixed rules |
| `abhinav0370/cha22-agent` | heuristic-and-rule-agents | n/a (near-copy of guruprasaathas111/kaggriculture-master-engine-v3) (near-copy of `guruprasaathas111/kaggriculture-master-engine-v3`) |
| `abhirajhiwale/crack-kaggriculture-e783-meta-breaker` | evaluation-and-measurement | n/a (community baseline archive from the notebook output; the notebook's own code is a packaging stub) |
| `ahmed1harfoush/kaggriculture-notebook` | heuristic-and-rule-agents | rule-based agent with run_episode and evaluate_agent harness; role-based task assignment (farmer and workers) |
| `ahmedberatozer/kaggriculture-v23-adaptive-routes-smart-sales` | ahmed-V-series | template agent: an embedded base64 template (not decoded) written to main.py; donor handle points to anothe... |
| `ahmedberatozer/kaggriculture-v25-new-production-routes-with-rea` | aurax-reactive-router | n/a (near-copy of aurax7/kaggriculture-reactive-router) (near-copy of `aurax7/kaggriculture-reactive-router`) |
| `ahmedberatozer/kaggriculture-v31-production-and-sale-priority` | ahmed-V-series | rule-based agent in a 1,490-line main.py written by %%writefile; production and sale priority over the route |
| `ahmedberatozer/kaggriculture-v34-observed-market-timing` | ahmed-V-series | rule-based agent in a 1,865-line main.py; router and shed/tile helpers; sale-block ordering |
| `ahmedberatozer/kaggriculture-v35-reactive-sales-sheep-expansi` | aurax-reactive-router | n/a (near-copy of flexonafft/kaggriculture-most-powerfull-route) (near-copy of `flexonafft/kaggriculture-most-powerfull-route`) |
| `ahmedberatozer/kaggriculture-v36-guarded-four-turn-sales` | aurax-reactive-router | n/a (near-copy of flexonafft/kaggriculture-most-powerfull-route) (near-copy of `flexonafft/kaggriculture-most-powerfull-route`) |
| `ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins` | ahmed-V-series | rule-based agent in a 2,626-line main.py built on V37; feed rule compares production value with wheat cost |
| `ahmedberatozer/kaggriculture-v39-ready-before-the-rush` | ahmed-V-series | n/a (near-copy of ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins) (near-copy of `ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins`) |
| `ahmedberatozer/kaggriculture-v40-plans-that-fit-the-shops` | ahmed-V-series | n/a (near-copy of ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins) (near-copy of `ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins`) |
| `ahmedberatozer/kaggriculture-v41-review-candidate` | aurax-reactive-router | n/a (near-copy of aurax7/kaggriculture-shop-router-reactive-v5) (near-copy of `aurax7/kaggriculture-shop-router-reactive-v5`) |
| `ahmedberatozer/kaggriculture-v42-production-that-fits-the-marke` | aurax-reactive-router | n/a (near-copy of aurax7/kaggriculture-shop-router-reactive-v5) (near-copy of `aurax7/kaggriculture-shop-router-reactive-v5`) |
| `ahmedberatozer/kaggriculture-v43-recovering-lost-harvests` | ahmed-V-series | rule-based agent, self-contained main.py; warehouse protection layer added to the V42 route policy |
| `ahmedberatozer/kaggriculture-v44-winning-the-same-turn-sale-race` | ahmed-V-series | rule-based agent; keeps the complete V43 policy and adds one narrow market rule |
| `ahmedberatozer/kaggriculture-v45-first-turn-wheat-round-trip` | ahmed-V-series | rule-based agent; keeps the complete V44 policy and changes exactly one market turn |
| `ahmedberatozer/kaggriculture-v46-first-turn-microstructure-and-s` | ahmed-V-series | rule-based agent; keeps the V43 farming, service and warehouse layers and the V44 clone-gated pre-emption |
| `ahmedberatozer/kaggriculture-v47-reactive-market-coordination` | ahmed-V-series | self-contained submission agent combining the V46 route and safety system with pre-overflow sales, clone-aw... |
| `ahmedberatozer/kaggriculture-v48-clear-the-queue` | ahmed-V-series | rule-based agent; a small update to V47 that removes market sale slots which cannot sell |
| `ahmedberatozer/kaggriculture-v49-funded-sale-timing-and-worker` | ahmed-V-series | rule-based agent; V48 route, market and race layers unchanged, with economic layers appended from Tschinkel... |
| `ahmedberatozer/kaggriculture-v50-early-yarn-commit` | ahmed-V-series | rule-based agent built on V49; two added layers: v233x early six-sheep commit and weedlag recovery |
| `ahmedberatozer/kaggriculture-v51-lean-flock` | ahmed-V-series | rule-based agent built on V50; adds a single-hand sheep service credited to Tschinkel's 2945 Farm |
| `ahmedberatozer/kaggriculture-v52-lean-flock-yarn-route` | ahmed-V-series | rule-based agent (SOURCE_BLOB zlib payload, not decoded) built on V50; adds a single-hand sheep service fro... |
| `ahmedberatozer/kaggriculture-v53-opening-signature` | ahmed-V-series | rule-based agent (SOURCE_BLOB zlib payload, not decoded) keeping the V52 farm, route and market policy exactly |
| `ahmedberatozer/kaggriculture-v54-productive-wheat-and-patient` | ahmed-V-series | n/a (near-copy of ahmedberatozer/kaggriculture-v55-one-turn-market-race-edge) (near-copy of `ahmedberatozer/kaggriculture-v55-one-turn-market-race-edge`) |
| `ahmedberatozer/kaggriculture-v55-one-turn-market-race-edge` | ahmed-V-series | rule-based agent; keeps V54 production, purchases, route tables and field actions; one market parameter cha... |
| `ahmedberatozer/kaggriculture-v56-smarter-seeds-and-fertilizer` | ahmed-V-series | rule-based agent (SOURCE_BLOB, zlib-compressed payload, not decoded); keeps the late seed budget and adds o... |
| `ahmedberatozer/kaggriculture-v57-funding-order-invariant` | ahmed-V-series | n/a (near-copy of ahmedberatozer/kaggriculture-v56-smarter-seeds-and-fertilizer) (near-copy of `ahmedberatozer/kaggriculture-v56-smarter-seeds-and-fertilizer`) |
| `ahmedberatozer/more-yield-smarter-labor` | ahmed-V-series | rule-based agent in a 2,356-line main.py built on V36; fertilization projects, guarded warehouse sales, sha... |
| `akashbabu17/kaggriculture-autonomous-multi-agent-farming` | heuristic-and-rule-agents | rule-based agent with three decoupled operational layers; tiered BFS movement and a capex evaluator in a 17... |
| `akhileshgodugu/strong-statr-barnyard-economist` | tape-and-route-replay | tape replay: a hardcoded list of 719 actions recorded from one game, replayed (agent in base85 parts, not d... |
| `alejandrofonda/kaggriculture-ppo-training` | rl-and-learned | learned policy: behaviour cloning (20 episodes) then PPO fine-tuning (300 episodes) of a policy downloaded... |
| `alejandrofonda/kaggriculture-ppo-training-v18` | rl-and-learned | learned policy: behaviour cloning then PPO continued training from a preloaded checkpoint; evaluation every... |
| `alejandrofonda/kaggriculture-self-play-az-lite-gpu-search-12h` | rl-and-learned | hybrid: candidate-config search (AlphaZero-lite style) over a loaded policy, with replay calibration and az... |
| `alejandrofonda/kaggriculture-state-p1-2-2` | tutorial-starter-baseline | loader only: finds a dataset directory under /kaggle/input and writes to /kaggle/working; no policy in the... |
| `alejandrofonda/kaggriculture-test-minimal` | rl-and-learned | same learned-policy pipeline as the PPO training v20 notebook (downloads a model, then trains) |
| `alexandergremyakov/harvest-pulse-goose-dividend-v2` | heuristic-and-rule-agents | rule-based planner in a 2,922-line main.py written by %%writefile: candidate tasks, global assignment of ha... |
| `alexkulll/kaggriculture` | heuristic-and-rule-agents | rule-based scaling MVP: fixed targets (20 plants, 4 hands), crop table, quadrant ranges and market actions |
| `alperen5252525/kaggriculture-first-in-line-stock-into-income` | clone-and-preemption-sales | rule-based agent; the agent payload (SOURCE_SHA256 check, not decoded) plus a sale-timing rule |
| `alperen5252525/kaggriculture-market-rhythm-sale-policy` | clone-and-preemption-sales | rule-based farm core kept; a measured sale policy decides when and how ready products reach the queue |
| `alperen5252525/kaggriculture-metacounter-r1-scored-agent` | ahmed-V-series | n/a (near-copy of ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins) (near-copy of `ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins`) |
| `alperen5252525/kaggriculture-ready-stock-earlier-sales` | clone-and-preemption-sales | runnable public-source agent (SOURCE_B85 payload, not decoded) built on Ahmed Berat Ozer's V46 with one exp... |
| `alperen5252525/turn-one-market-advantage-kaggriculture` | replay-analysis | n/a (near-copy of nathanjacob/beyond-v43-what-the-top-clusters-do-on-turn-1) (near-copy of `nathanjacob/beyond-v43-what-the-top-clusters-do-on-turn-1`) |
| `amaterasuuuuu/shabby-farm` | tape-and-route-replay | rule-based planner: plans the season as dated commitments, replays them through one ledger, compiles surviv... |
| `ameythakur20/kaggriculture-deterministic-farm-planning-agent` | heuristic-and-rule-agents | deterministic rule-based planner (fixed seed 42); 247-line main.py with trace actor, weed repair, future qu... |
| `ameythakur20/kaggriculture-premium-first-market-agent` | heuristic-and-rule-agents | rule-based agent (819-line main.py) packaging a v43 policy with seat, farm and weed guards |
| `anandkumar369o/kagg-team-decisions` | replay-analysis | analysis script, not a policy: loads replay episodes and tabulates named teams' decisions per day bucket |
| `anasriaz/kaggriculture` | compiled-cpp-policy | hybrid: C++ policy with a six-day budget guard and a bundled tape, compiled against a simulator header; Pyt... |
| `andrewsokolovsky/kaggriculture` | clone-and-preemption-sales | rule-based overlay on a parent V14 policy (473 lines): moves a premium sale already scheduled this turn to... |
| `andrewsokolovsky/kaggriculture-breaking-the-tie` | rl-and-learned | learned router: behaviour cloning from a teacher plus counterfactual oracle labels and DAgger rounds; a Rou... |
| `anhadmahajan06/kaggriculture-autonomous-ai-farming-agent` | ahmed-V-series | rule-based agent: V56 base with early-cycle opening, seed capping, fertiliser conservation and a layer-D or... |
| `anshu042006/kaggriculture` | heuristic-and-rule-agents | rule-based agent: crop table, tile search, movement, plant choice, market actions and a 194-line farmer_action |
| `antimocarlino/o-p-a-antimode-v1` | heuristic-and-rule-agents | rule-based agent with market regimes: strikes when price is high against its recent average and retreats to... |
| `arashmdoust/kaggriculture-strategic-farm-agent` | heuristic-and-rule-agents | rule-based agent (150-line submission.py) with price, ripeness and market helpers; evaluation harness in th... |
| `arsgorynich/herd-safe-v3-experimental-risk-aware-feed` | herd-safety | rule-based agent: a sale predictor for opponent sales gates herd feeding; packaged source (zlib payload, no... |
| `arsgorynich/kaggriculture-v40-challenger` | ahmed-V-series | rule-based derivative of Dmitrii Gluzdov's More Wheat, Smarter Sales v9 with a weed build-repair fix (zlib... |
| `arsgorynich/kaggriculture-v43-local-confirmed` | ahmed-V-series | exact public V43 by Ahmed Berat Ozer, with the source and attributions kept (zlib payload, not decoded) |
| `arsgorynich/order-book-v3-response-improvement` | kaito-lineage | rule-based derivative of shiiin9's Your Market List Is an Order Book, with a v3 response improvement (packe... |
| `artemzapara/type-safety-with-pydantic-models` | evaluation-and-measurement | no strategy: typed wrappers (Pydantic v2 models) for observations, tiles and commands; a random-walk baseli... |
| `ashok205/top10-replay-dataset-archive` | replay-analysis | data pipeline, not a policy: scans replay headers for team names and archives episodes of the top-10 teams... |
| `aurax7/kaggriculture-reactive-router` | aurax-reactive-router | rule-based reactive router in a 657-line main.py: shed-adjacent placement, tile lookup, no-op detection, li... |
| `aurax7/kaggriculture-shop-router-reactive-v2` | aurax-reactive-router | rule-based shop router in a 225-line main.py: projected shed, advanced-sale accounting, room guard, weed re... |
| `aurax7/kaggriculture-shop-router-reactive-v4` | aurax-reactive-router | rule-based reactive shop router in a 2,767-line main.py with a parent liquidation layer |
| `aurax7/kaggriculture-shop-router-reactive-v5` | aurax-reactive-router | rule-based reactive shop router in a 3,316-line main.py (111 helper defs) with a parent liquidation layer |
| `aurax7/kaggriculture-shop-router-reactive-v6` | aurax-reactive-router | n/a (near-copy of aurax7/kaggriculture-shop-router-reactive-v5) (near-copy of `aurax7/kaggriculture-shop-router-reactive-v5`) |
| `aurax7/kaggriculture-shop-router-reactive-v7` | aurax-reactive-router | n/a (near-copy of aurax7/kaggriculture-shop-router-reactive-v5) (near-copy of `aurax7/kaggriculture-shop-router-reactive-v5`) |
| `avikdas567/kaggriculture-microeconomic-dynamic-policy-engine` | engine-and-market-analysis | analytical model and decision engine: price functions by product (sqrt and log shapes) and a fibonacci cost... |
| `avioon/apex-v4-2687-elo-bow-before-the-herd-rank-75` | compiled-cpp-policy | hybrid: C++ policy (137 lines) with a six-day budget guard and a tape behind a plugin ABI; Python bridge (3... |
| `avioon/kaggriculture-apex-v5-emperor` | compiled-cpp-policy | n/a (near-copy of avioon/apex-v4-2687-elo-bow-before-the-herd-rank-75) (near-copy of `avioon/apex-v4-2687-elo-bow-before-the-herd-rank-75`) |
| `avioon/kaggriculture-apex-v7-god-emperor` | compiled-cpp-policy | hybrid: the same C++ plugin framework as apex-v4, with a 527-line Python bridge; base tape with state-condi... |
| `avndope/measure-first` | evaluation-and-measurement | measurement study, not a farm policy: a local evaluator checked against real ladder episodes; bootstrap com... |
| `ayeshasummaiyya/fields-of-fortune-strategic-farming-agent` | heuristic-and-rule-agents | rule-based planner in a 423-line main.py: plan objects, job building, crop choice, logistics and market |
| `ayodejiibrahimlateef/kaggriculture-cloning-v45-open-78-experiment` | heuristic-and-rule-agents | one-parameter derivative of degnonguidi's public V45 cloning agent (zlib payload patched in place, not deco... |
| `ayomideabdulrahmon/kaggle-agriculture` | tutorial-starter-baseline | baseline_agent (41 lines) and an environment install; a template baseline |
| `az05192000gmailcom/kaggriculture-from-orders-to-actual-trades` | engine-and-market-analysis | replay analysis: replays market settlement one unit at a time and accounts cash by category (revenue, seeds... |
| `bardiabahadori/kaggriculture-agent-selection-engine-traps` | engine-and-market-analysis | measurement harness, not an agent: starter-versus-pass checks, head-to-head runs and candidate ranking; sho... |
| `beamhonor0911/kaggriculture-episodes-exploratory-data-analysis` | replay-analysis | exploratory data analysis of an episodes dataset (replays and results); no policy |
| `beicicc/kaggriculture-c01-scenario-v7-reproduction` | heuristic-and-rule-agents | n/a (near-copy of beicicc/kaggriculture-c05-mid-herd-10) (near-copy of `beicicc/kaggriculture-c05-mid-herd-10`) |
| `beicicc/kaggriculture-c02-core-3-cow-1-sheep` | heuristic-and-rule-agents | n/a (near-copy of beicicc/kaggriculture-c05-mid-herd-10) (near-copy of `beicicc/kaggriculture-c05-mid-herd-10`) |
| `beicicc/kaggriculture-c03-target-herd-14` | heuristic-and-rule-agents | n/a (near-copy of beicicc/kaggriculture-c05-mid-herd-10) (near-copy of `beicicc/kaggriculture-c05-mid-herd-10`) |
| `beicicc/kaggriculture-c04-target-herd-15` | heuristic-and-rule-agents | n/a (near-copy of beicicc/kaggriculture-c05-mid-herd-10) (near-copy of `beicicc/kaggriculture-c05-mid-herd-10`) |
| `beicicc/kaggriculture-c05-mid-herd-10` | heuristic-and-rule-agents | rule-based planner in one cell: 30-day market model, shed pathing, quadrant crop mix and staged herd |
| `beicicc/kaggriculture-c06-scenario-fertilizer` | heuristic-and-rule-agents | n/a (near-copy of beicicc/kaggriculture-c05-mid-herd-10) (near-copy of `beicicc/kaggriculture-c05-mid-herd-10`) |
| `beicicc/kaggriculture-c07-public-v12-tape` | tape-and-route-replay | tape replay: a literal recorded action list (TRACE_ACTIONS) replayed turn by turn by a 3-line agent() |
| `beicicc/kaggriculture-c08-schema-safe-89308208` | tape-and-route-replay | tape replay: literal TRACE_ACTIONS list with an 11-line agent() that guards the schema |
| `beicicc/kaggriculture-c09-dynamic-shed` | tape-and-route-replay | tape replay: literal TRACE_ACTIONS list with a 28-line agent() that adds a dynamic shed rule |
| `beicicc/kaggriculture-c10-conservative-probe-router` | tape-and-route-replay | tape router: five literal recorded traces (base, crop, berry, current, nishchal) selected by a route flag,... |
| `beicicc/kaggriculture-c11-moon-sales-schema-safe` | tape-and-route-replay | tape replay: literal TRACE_ACTIONS list with a 10-line agent(); buys one cow where c07 buys three |
| `beicicc/kaggriculture-c12-rayk-public-delta-schema-safe` | tape-and-route-replay | tape replay: compressed trace (zlib and base85, not decoded) with public episode patches and a 63-line term... (near-copy of `beicicc/kaggriculture-c13-licensed-hand-ablation`) |
| `beicicc/kaggriculture-c13-licensed-hand-ablation` | tape-and-route-replay | tape replay: compressed trace (zlib and base85, not decoded) with public episode patches and a 63-line term... |
| `beicicc/kaggriculture-c14-late-crop-weed-recovery` | tape-and-route-replay | tape replay with a 115-line hand-lag recovery layer on a compressed trace (zlib and base85, not decoded) |
| `beicicc/kaggriculture-c22-exact-reproducibility-control` | tape-and-route-replay | n/a (near-copy of beicicc/kaggriculture-c25-exact-final-quota-control) (near-copy of `beicicc/kaggriculture-c25-exact-final-quota-control`) |
| `beicicc/kaggriculture-c23-exact-reproducibility-control` | tape-and-route-replay | n/a (near-copy of beicicc/kaggriculture-c25-exact-final-quota-control) (near-copy of `beicicc/kaggriculture-c25-exact-final-quota-control`) |
| `beicicc/kaggriculture-c24-exact-dynamic-rating-control` | tape-and-route-replay | n/a (near-copy of beicicc/kaggriculture-c25-exact-final-quota-control) (near-copy of `beicicc/kaggriculture-c25-exact-final-quota-control`) |
| `beicicc/kaggriculture-c25-exact-final-quota-control` | tape-and-route-replay | tape router: a literal TRACE_ACTIONS list plus named market branches (top, Carlos router, somewhere router,... |
| `beicicc/kaggriculture-c26-kaito-v23-dual-regime` | tape-and-route-replay | n/a (near-copy of beicicc/kaggriculture-c28-exact-byte-replica-b) (near-copy of `beicicc/kaggriculture-c28-exact-byte-replica-b`) |
| `beicicc/kaggriculture-c27-exact-byte-control` | tape-and-route-replay | n/a (near-copy of beicicc/kaggriculture-c28-exact-byte-replica-b) (near-copy of `beicicc/kaggriculture-c28-exact-byte-replica-b`) |
| `beicicc/kaggriculture-c28-exact-byte-replica-b` | tape-and-route-replay | tape replay: two zlib/base85 action traces (legacy and rebalance) with weed-repair replay, a price floor an... |
| `beicicc/kaggriculture-c29-exact-byte-replica-c` | tape-and-route-replay | n/a (near-copy of beicicc/kaggriculture-c28-exact-byte-replica-b) (near-copy of `beicicc/kaggriculture-c28-exact-byte-replica-b`) |
| `beicicc/kaggriculture-c30-pr1394-activation-control` | tape-and-route-replay | n/a (near-copy of beicicc/kaggriculture-c28-exact-byte-replica-b) (near-copy of `beicicc/kaggriculture-c28-exact-byte-replica-b`) |
| `beicicc/kaggriculture-c31-kaito-v22-official-1-32-6` | tape-and-route-replay | tape replay of a compressed action list (_ACTIONS, zlib base85) with weed-repair replay and market price he... |
| `bekamaregasanegewo/notebook2eb78cabb1` | heuristic-and-rule-agents | rule-based production agent written as a string inside the cell and saved to a file; returns farmer, hands... |
| `beraterolelk/kaggriculture-meta-field-guide-top-30-playbook` | replay-analysis | field guide: an audit of the public Top-30 record and a short route agent (ROUTE list, PREMIUM set) |
| `bernubritz/kaggriculture-h4-best` | tape-and-route-replay | action tape packaged as a base64 gzip tar (actions.json, not decoded) with a verification note |
| `bielabs/base-data-structures-for-kaggriculture` | engine-and-market-analysis | base data structures for simulating the market: price shapes (linear, sq, sqrt, log), Market and Item class... |
| `binasalama/kaggriculture-v28-gate-fixed` | tape-and-route-replay | tape replay: compressed action list (_ACTIONS, zlib base85) with weed-repair replay and a fresh-market laye... |
| `binasalama/kaggriculture-v29-reactive` | tape-and-route-replay | tape replay with the same fresh-market and weed-replay layers as v28, plus a reactive town-demand term |
| `binasalama/kaggriculture-v30-time-switch` | tape-and-route-replay | tape replay: compressed action list (_ACTIONS, zlib base85) with a day-18 switch and the fresh-market and w... |
| `binasalama/kaggriculture-v31-early-livestock` | tape-and-route-replay | tape replay with early livestock: pasture and second-cow actions tracked by done flags on top of the v28 la... |
| `biohack44/kaggriculture` | heuristic-and-rule-agents | n/a (near-copy of beicicc/kaggriculture-c05-mid-herd-10) (near-copy of `beicicc/kaggriculture-c05-mid-herd-10`) |
| `blacklions/kaggriculture` | clone-and-preemption-sales | n/a (near-copy of koushikrudra/kaggriculture-preempt-h6) (near-copy of `koushikrudra/kaggriculture-preempt-h6`) |
| `blacklions/kaggriculture-v1` | blacklions-public | self-contained submission combining four strategy families from the supplied public notebooks, with a visib... |
| `blacklions/kaggriculture-v11-public-experiment` | blacklions-public | n/a (near-copy of blacklions/kaggriculture-v12-public-experiment) (near-copy of `blacklions/kaggriculture-v12-public-experiment`) |
| `blacklions/kaggriculture-v12-public-experiment` | blacklions-public | embedded bundle (base64 tar.gz, not decoded) with a run_episode harness; submission/v12 with parity and lea... |
| `blacklions/kaggriculture-v14-public-experiment` | blacklions-public | n/a (near-copy of blacklions/kaggriculture-v12-public-experiment) (near-copy of `blacklions/kaggriculture-v12-public-experiment`) |
| `blacklions/kaggriculture-v15-public-experiment` | blacklions-public | n/a (near-copy of blacklions/kaggriculture-v12-public-experiment) (near-copy of `blacklions/kaggriculture-v12-public-experiment`) |
| `blacklions/kaggriculture-v16-public-experiment` | blacklions-public | n/a (near-copy of blacklions/kaggriculture-v12-public-experiment) (near-copy of `blacklions/kaggriculture-v12-public-experiment`) |
| `blacklions/kaggriculture-v17-public-experiment` | blacklions-public | n/a (near-copy of blacklions/kaggriculture-v12-public-experiment) (near-copy of `blacklions/kaggriculture-v12-public-experiment`) |
| `blacklions/kaggriculture-v18-public-experiment` | blacklions-public | n/a (near-copy of blacklions/kaggriculture-v12-public-experiment) (near-copy of `blacklions/kaggriculture-v12-public-experiment`) |
| `blacklions/kaggriculture-v19-frontier-public-experiment` | blacklions-public | n/a (near-copy of blacklions/kaggriculture-v12-public-experiment) (near-copy of `blacklions/kaggriculture-v12-public-experiment`) |
| `blacklions/kaggriculture-v20-adaptive-queue-public-experiment` | blacklions-public | unchanged single-file artifact from Tetsu's public adaptive strategy, reproduced and hash-checked; one offi... |
| `blacklions/kaggriculture-v3-public-experiment` | blacklions-public | n/a (near-copy of blacklions/kaggriculture-v6-public-experiment) (near-copy of `blacklions/kaggriculture-v6-public-experiment`) |
| `blacklions/kaggriculture-v4-public-experiment` | blacklions-public | n/a (near-copy of blacklions/kaggriculture-v6-public-experiment) (near-copy of `blacklions/kaggriculture-v6-public-experiment`) |
| `blacklions/kaggriculture-v6-public-experiment` | blacklions-public | embedded-bundle wrapper with a run_episode harness; submission/v6 with parity and league checks |
| `blacklions/kaggriculture-v7-public-experiment` | blacklions-public | n/a (near-copy of blacklions/kaggriculture-v12-public-experiment) (near-copy of `blacklions/kaggriculture-v12-public-experiment`) |
| `blacklions/kaggriculture-v9-public-experiment` | blacklions-public | n/a (near-copy of blacklions/kaggriculture-v12-public-experiment) (near-copy of `blacklions/kaggriculture-v12-public-experiment`) |
| `bnzn261029/visible-state-all-router-over-seven-public-syouya` | heuristic-and-rule-agents | rule-based router appended to submission.py (136 lines): features, pick and agent, routing over seven publi... |
| `boatlee/84-84-base-public-holdout-v14-clone-preemption` | clone-and-preemption-sales | complete rule-based agent (V14, payload in base85 parts, not decoded); production schedule reconstructed fr... |
| `boatlee/four-quadrant-route-breakdown-and-feasibility` | boatlee-clean-room | replay study of a four-quadrant macro-route, with a 719-action open-loop agent (r0_main.py, 50 lines) packa... |
| `boatlee/kaggriculture-near-mirror-episode-diagnosis` | boatlee-clean-room | replay analysis of two completed episodes: per-component action agreement (farmer, hands, market); no polic... |
| `boatlee/kaggriculture-v7-replay-diagnosis-v8-selection` | boatlee-clean-room | replay diagnosis over a 71-episode baseline corpus, then selection of a V8 candidate; market-only patches j... |
| `boatlee/v13-r3-top-meta-order-safe-premium-control` | boatlee-clean-room | complete rule-based agent (payload in base85 parts, not decoded): 719-turn production schedule, actor-local... |
| `boatlee/v16-rc2-high-score-near-mirror-market-relay` | boatlee-clean-room | high-output production program that is selective on yarn store, plus one narrow market controller; 678-line... |
| `boatlee/v16-rc5-high-score-8c-4s-premium-market-lead` | boatlee-clean-room | rule-based agent (247-line main.py): compact 8 COW and 4 SHEEP production route with a one-turn market lead |
| `boatlee/v16-rc5-r5a-high-score-8c-4s-recovery` | boatlee-clean-room | same 8 COW and 4 SHEEP route and one-turn market lead as RC5, with a recovery layer (412-line main.py) |
| `boatlee/v17-r1-rc2-high-score-10c-4s-market-storage` | boatlee-clean-room | three-quadrant production route (10 cows, 4 sheep) reconstructed from one public episode, with two bounded... |
| `boatlee/v20-adaptive-r1-multi-route-agent` | boatlee-clean-room | multi-route agent: several complete production schedules kept available and chosen from the public state (p... |
| `boatlee/v21-r1-public-state-route-portfolio` | boatlee-clean-room | multi-route agent: several complete production schedules available, selected only from public observation (... |
| `boatlee/v29-r1-adaptive-market-hysteresis` | boatlee-clean-room | coherent high-output three-quadrant production program plus a stateful market controller (hysteresis); payl... |
| `bovard/kaggriculture-getting-started` | tutorial-starter-baseline | official-style tutorial with a short example agent (melon_maxxer, 98 lines): step toward target tiles, sell... |
| `bruceqdu/my-2026-08-04-high-score-pipeline` | tape-and-route-replay | fixed-route agent (route 1) held as a source string and written to main.py with a bundle; route hash recorded |
| `bruceqdu/reinforcement-learning-and-mcts-a-tutorial` | rl-and-learned | learned search: policy-value network with root PUCT search (MCTS) over the Kaito V27 agent as a fixed route... |
| `bruceqdu/two-reinforcement-learning-examples-from-kaito-v27` | rl-and-learned | tabular epsilon-greedy Q-learning overlays on Kaito V27 at two decision points (step 695 and step 336); the... |
| `busyaprime/the-best-thing-to-farm-has-a-market-of-59-units` | engine-and-market-analysis | economics analysis from a reference season log and crop and price curves; no submitted policy |
| `busyaprime/what-actually-wins-on-the-kaggriculture-ladder` | replay-analysis | replay analysis: parses 720-turn replays into per-side features (plant, sell, hire, harvest, fertilise, buy... |
| `chaimaamatrag/kaggriculture-competition` | heuristic-and-rule-agents | rule-based agent (207-line agent function) plus a trial runner (run_trials) that compares variants |
| `chaitanyajamble/kaggriculture` | heuristic-and-rule-agents | rule-based planner in a 378-line submission.py (%%writefile): build_plan, plan_tile_action, assign_unit_act... |
| `chandanverma/kagriculture-top1-v16rc5` | tape-and-route-replay | n/a (near-copy of binasalama/kaggriculture-v28-gate-fixed) (near-copy of `binasalama/kaggriculture-v28-gate-fixed`) |
| `cjlcjlcjl/kaggriculture-what-the-top-farms-do-a-live-meta` | replay-analysis | analysis notebook: a guide and a live tracker re-run daily on the official replay dataset; episodes selecte... |
| `cracker1war/kaggriculture-strategy-analysis-v2` | heuristic-and-rule-agents | rule-based agent on a crop and animal economics table (costs, prices, first yield, growth days), 144-turn b... |
| `crystalbaby/god-s-mode-hacked-stores` | engine-and-market-analysis | research notebook on the hidden shop-selection seed: seed oracle and one-cell interventions on the shared r... |
| `crystalbaby/kaggriculture-dynamic-route-agent` | packaging-and-embedded-payload | packed agent: a Base85 source of about 182 KB reconstructed to a file, then validated and archived; route a... |
| `crystalbaby/kaggriculture-v38-public-submission` | ahmed-V-series | n/a (near-copy of ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins) (near-copy of `ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins`) |
| `crystalbaby/market-smart-farming-kaggriculture` | tape-and-route-replay | rule-based portfolio of thirteen complete route programmes stored as tapes, with selective capacity relief... |
| `daisy023/kaggriculture-smart-farming-agent` | heuristic-and-rule-agents | rule-based agent: one 217-line my_agent function |
| `daniilkrasnovvv/farm-top-solution-in-lb` | heuristic-and-rule-agents | deterministic planner: standard-library-only agent source with a validator for legal units and market order... |
| `daniilkrasnovvv/kaggriculture-easy-bronse-in-lb-2628-2` | boatlee-clean-room | n/a (near-copy of boatlee/v16-rc2-high-score-near-mirror-market-relay) (near-copy of `boatlee/v16-rc2-high-score-near-mirror-market-relay`) |
| `dariushafshar/18-144-episodes-local-win-rate-ranks-backwards` | evaluation-and-measurement | evaluation study, no submitted policy: two own agents (v8, v9) on a 15-opponent pool, 2,880 paired episodes... |
| `dariushafshar/agent-tuned-for-a-dead-game` | engine-and-market-analysis | measurement note: tuning against 1.32.5 demand; centre-interval and shop-sell-interval parameters; no submi... |
| `dariushafshar/banked-3000-every-game-the-last-callable-trap` | engine-and-market-analysis | harness finding, not a policy: an entrypoint naming bug in which Kaggle calls the first callable, so the ba... |
| `dariushafshar/beating-your-own-best-agent-is-the-wrong-test` | evaluation-and-measurement | measurement note: a candidate beat the tracked submission 93-100% on its own seed sets, but scored 40.0% ag... |
| `dariushafshar/care-is-a-4-2x-multiplier-animal-economics` | engine-and-market-analysis | analysis of animal care economics using the engine's refresh function; sweep of care multipliers; a 152-lin... |
| `dariushafshar/eviction-gate-harness-measure-before-you-submit` | evaluation-and-measurement | evaluation harness, not a policy: scans agent source for denied imports, runs a 240-episode panel with fixe... |
| `dariushafshar/kaggriculture-s-mean-vote-beats-biohub-s-by-52` | engine-and-market-analysis | not an agent: median and trimmed vote analysis across Kaggle competitions, Kaggriculture included as one venue |
| `dariushafshar/neither-theory-explains-why-venues-pay-more` | engine-and-market-analysis | not an agent: a table of five Kaggle competitions (rewards, teams, median votes, kernels-only) |
| `dariushafshar/rating-decay-near-the-medal-line-80-pts-day` | engine-and-market-analysis | not an agent: sixteen full-board snapshots of ratings, decay per hour by rating band |
| `dariushafshar/same-file-9-days-apart-1839-vs-1238` | engine-and-market-analysis | not an agent: displayed ratings of 22 submissions polled every ~12 minutes for 17.5 days (15,813 readings) |
| `dariushafshar/the-engine-changed-under-us` | engine-and-market-analysis | not an agent: economics study of kaggle-environments 1.32.6 (town centre sale interval from 12 to 24 turns)... |
| `dariushafshar/the-real-median-kaggle-notebook-gets-2-votes` | engine-and-market-analysis | not an agent: median votes per venue from the Kernels and Competitions tables |
| `dariushafshar/who-actually-buys-your-crops` | engine-and-market-analysis | not an agent: town demand model (each unlocked shop consumes the products it demands every 4 turns) and a s... |
| `dariushafshar/your-rating-fell-your-standing-rose` | engine-and-market-analysis | not an agent: a frozen evicted rating (2,157.6) and its standing on archived boards |
| `dariushafshar/your-top-10-is-a-coinflip-past-2000-teams` | engine-and-market-analysis | not an agent: public-to-private survival of top-10 finishes across Kaggle competitions, bucketed by team count |
| `datascikhan/agrisim-deep-dive` | replay-analysis | replay analysis: loads episode JSON replays from the 2026-09-15 dataset and parses agent actions; no submit... |
| `datascikhan/cropsense-the-adaptive-farm-ai` | heuristic-and-rule-agents | four-pass rule-based adaptive agent: scan tiles, assign workers by urgency, plan sales within limits, pick... |
| `datascikhan/farmcraft-kaggriculture-grandmaster` | packaging-and-embedded-payload | packaging and receipt harness around a FarmCraft Prime agent: submission.py written from a source string, S... |
| `datascikhan/farmpilot-ai` | heuristic-and-rule-agents | layered rule-based agent (AgriMind Lite): crop and animal return tables, tile scan, worker assignment by pr... |
| `datascikhan/harvestlens-an-independent-kaggriculture-bench` | packaging-and-embedded-payload | packaging and benchmark harness around a Kaggriculture Grandmaster agent: submission.py written from a sour... |
| `datascikhan/kaggriculture-trajectory-engine` | replay-analysis | replay analysis: loads episode replays from the 2026-09-15 dataset, extracts observation keys and per-episo... |
| `debmalya84/kaggriculture-episode-data-a-gentle-eda` | replay-analysis | exploratory analysis of the daily public episode dataset: opening one replay, final score distribution, pri... |
| `dedquoc/kaggriculture-zero-drought-crop-protection` | heuristic-and-rule-agents | deterministic priority state machine (v1 and v2 agents in a 109-line main.py): water before harvest to avoi... |
| `degnonguidi/best-agent-ranking` | kaito-lineage | rule-based derivative of the strongest agents published on 20-21 September: an exact order book for the mar... |
| `degnonguidi/kaggriculture-agent-builder` | compiled-cpp-policy | n/a (near-copy of yhay81/three-day-shop-router) (near-copy of `yhay81/three-day-shop-router`) |
| `degnonguidi/kaggriculture-cloning-agent` | ahmed-V-series | n/a (near-copy of ahmedberatozer/kaggriculture-v45-first-turn-wheat-round-trip) (near-copy of `ahmedberatozer/kaggriculture-v45-first-turn-wheat-round-trip`) |
| `degnonguidi/kaggriculture-utils-v1` | replay-analysis | n/a (near-copy of leoprovorov/kaggricult-man-reverse-engineering) (near-copy of `leoprovorov/kaggricult-man-reverse-engineering`) |
| `delayedkarma/whatwheatwrought-a-kaggriculture-tale` | heuristic-and-rule-agents | rule-based wheat agent (agent, 136 lines; submission.py 138 lines by writefile): plant wheat, water daily,... |
| `denizeryilmaz/v111-8c4s-economic-core-premium-lead` | boatlee-clean-room | n/a (near-copy of boatlee/v16-rc5-high-score-8c-4s-premium-market-lead) (near-copy of `boatlee/v16-rc5-high-score-8c-4s-premium-market-lead`) |
| `destbreso/97-predictable-extracting-decision-trees` | evaluation-and-measurement | not an agent: classifies agents into script, brancher, scheduler or mixed by extracting decision trees from... |
| `destbreso/a-dna-test-for-agents` | evaluation-and-measurement | not an agent: a genome-style test for agent lineage from replays: a thirty-band signature of the conserved... |
| `destbreso/a-field-guide-to-replay-agents` | replay-analysis | not an agent: field guide; most strong agents are a recorded season with a thin layer of code; eight kinds... |
| `destbreso/a-macroeconomic-x-ray-of-the-kaggriculture-meta` | engine-and-market-analysis | not an agent: price capture of one tracked team's real episodes on four dates (Aug 15, 23, 27, 30); per-day... |
| `destbreso/a-week-four-x-ray-of-the-top-twelve` | replay-analysis | not an agent: x-ray of the top twelve: live singletons, clone clades and public-family pairs; routes switch... |
| `destbreso/agent-telemetry-catch-what-you-lose` | engine-and-market-analysis | not an agent: a silent-loss ledger that counts actions the engine accepts but ignores (feed with no wheat,... |
| `destbreso/an-instrument-for-agent-selection` | evaluation-and-measurement | not an agent: fourth-generation selection instrument: rival panels, paired sign and McNemar tests, power an... |
| `destbreso/can-i-clone-you-from-your-dna` | evaluation-and-measurement | not an agent: argues that a published agent can be rebuilt from its replays when it has one measurable prop... |
| `destbreso/dissecting-the-top-two` | replay-analysis | not an agent: full-turn analysis of the two top agents on engine 1.32.7; identity by the turn-24 opening si... |
| `destbreso/every-community-agent-one-arena` | evaluation-and-measurement | not an agent: a public dataset of 95 community agents with licences and provenance; 93 carry base64 payload... |
| `destbreso/everyone-is-playing-the-same-opening` | replay-analysis | not an agent: census of exact action matching over 9,092 seats in 4,546 ladder games across thirteen days,... |
| `destbreso/from-1-to-24k-episodes-a-second` | engine-and-market-analysis | not an agent: engine throughput study: the environment plays about one episode a second, against a C++ port... |
| `destbreso/how-many-opponents-is-a-pool-of-forty` | evaluation-and-measurement | not an agent: method for choosing the opponent set; a pool of forty needs nineteen opponents; the eight-opp... |
| `destbreso/island-ga-an-owned-schedule-is-a-moat` | engine-and-market-analysis | not an agent: a search over owned schedules; the winning shape on this ladder is a base schedule plus a thi... |
| `destbreso/kaggriculture-compare-two-agents` | evaluation-and-measurement | not an agent: game-by-game comparison of two agents over 112 identical games; medoid episode and mutable su... |
| `destbreso/kaggriculture-how-much-money-is-in-this-game` | engine-and-market-analysis | not an agent: the money available in the game: market inventory starts at 10,000 per good and the price fal... |
| `destbreso/kaggriculture-know-your-noise` | evaluation-and-measurement | not an agent: how much a score difference is noise: variance of paired differences, correlation between sea... |
| `destbreso/kaggriculture-measure-your-agent` | evaluation-and-measurement | not an agent: an offline harness with six checks (population, seats, intervals, reproducibility) and a THIN... |
| `destbreso/kaggriculture-the-free-experiment-you-already-ran` | rl-and-learned | not an agent: uses the unrated self-play game that runs before submission to test whether an agent is fixed... |
| `destbreso/kaggriculture-what-kind-of-game-is-this` | engine-and-market-analysis | not an agent: game-theory analysis on 32,570 real episodes: no dominant strategy; the two banks in one epis... |
| `destbreso/kaggriculture-what-kind-of-optimisation-is-this` | replay-analysis | not an agent: companion analysis: routes have conserved and variable regions that can be located; candidate... |
| `destbreso/kagsim-the-engine-at-2000-episodes-per-second` | engine-and-market-analysis | not an agent: a C++ port of the engine (kagsim) run against the live environment: trace replay exact on eng... |
| `destbreso/measure-twice-submit-once-know-your-error` | evaluation-and-measurement | not an agent: an offline protocol for deciding a submission: paired replays, exact sign tests, power calcul... |
| `destbreso/mutants-at-the-top-genetic-potential-of-a-replay` | replay-analysis | not an agent: analysis of the top ten: each top agent's route varies from its own past runs in one channel... |
| `destbreso/rating-convergence-episodes-not-hours` | engine-and-market-analysis | not an agent: rating convergence per episode, not per hour: three probes (warming, byte-identical, settled)... |
| `destbreso/six-checks-before-you-waste-a-submission` | evaluation-and-measurement | not an agent: six checks before spending a submission: same game (engine version), paired seats, population... |
| `destbreso/the-farm-day-as-a-routing-problem` | replay-analysis | not an agent: routing analysis of the farm day: a public hand-written script and the rank-1 team's private... |
| `destbreso/the-leaderboard-has-a-fossil-record` | replay-analysis | not an agent: every episode ever played is in the record; lineages appear and take a quarter to a half of t... |
| `destbreso/the-leaderboard-is-a-habitat-gradient` | replay-analysis | not an agent: the leaderboard as a habitat gradient with rating as the axis; the population abstraction tes... |
| `destbreso/the-trades-were-paying-for-the-farm` | tape-and-route-replay | not an agent: knockout experiment on a leaderboard: the seller channel of a top agent's child is deleted; t... |
| `destbreso/v7-38-finance7-a-full-agent-layer-by-layer` | compiled-cpp-policy | chassis plus two published layers (a mirror counter and a financing repair) in a compiled agent; the predec... |
| `destbreso/what-1-32-7-changed-and-what-it-did-not` | engine-and-market-analysis | not an agent: what engine 1.32.7 changed: three price curves changed on 2026-08-15 (tomato, carrot, egg); r... |
| `destbreso/what-is-fixed-what-emerged-and-how-you-can-tell` | engine-and-market-analysis | not an agent: a classification of claims about the game as fixed (follows from the engine) or emergent (a f... |
| `destbreso/which-language-does-your-agent-speak` | evaluation-and-measurement | not an agent: classifies an agent's behaviour as a texture: colours each turn by whether it matches what th... |
| `destbreso/who-is-beating-you-and-is-it-you` | replay-analysis | not an agent: reads a submission's defeats and separates the rivals that beat it into lineages; the current... |
| `destbreso/wins-not-money` | evaluation-and-measurement | not an agent: two agents share a market for 720 turns; the episode is won by the bank, and the leaderboard... |
| `destbreso/x-ray-your-agent` | replay-analysis | not an agent: a one-run x-ray of a submission from its replays: whether it is a copyable script, which oppo... |
| `desyatio/93-wr-vs-kaito-s-v21-1-local-tuning-experiment` | kaito-lineage | local tuning fork of Kaito Fukami's v21.1 conditional-memory agent (AGENT_CODE string): market weights for... |
| `devraai/kaggriculture-data-analysis-and-modeling` | replay-analysis | data analysis and modelling notebook on Kaggriculture data (contents: data loading, cleaning and EDA); no s... |
| `devraai/kaggriculture-ladder-telemetry-eda-modeling` | replay-analysis | EDA of ladder telemetry data files (setup, loading, cleaning, EDA sections); no submitted policy in the cel... |
| `devraai/kaggriculture-match-replay-analysis-modeling` | replay-analysis | logistic regression predicting whether player 0 wins a match from replay features; no submitted policy |
| `dheerajkannaujiya/start-with-basic` | heuristic-and-rule-agents | grid-scanning rule-based agent with Manhattan pathfinding (get_direction, agent): classifies all 25 tiles e... |
| `dianatofficial/kaggriculture-reactive-agent-strategy-eda` | heuristic-and-rule-agents | rule-based apex agent (80-line apex_agent): dynamic arbitrage, Fibonacci labour scaling, zero-weed irrigati... |
| `dimitrisx94/submission-for-the-kaggriculture-competition` | heuristic-and-rule-agents | rule-based day simulator: agent, shed quantity and move logic, per-hand day schedules (simulate_day_agent);... |
| `dimong4/kaggriculture` | heuristic-and-rule-agents | rule-based agent with base agents for transactions, terminal item choice, soil and plant repair, cashflow,... |
| `djamilabenchikh/graph-reinforcement-learning` | rl-and-learned | graph reinforcement learning overlay on the V16-RC5 policy: a learned model decides only the planned quanti... |
| `dmitriigluzdov/kaggriculture-7-turn-rescue-historical-lb-2800` | clone-and-preemption-sales | rule-based controller: a 7-turn opening rescue for liquidity, built on shiiin9's order book and V55/V56 inp... |
| `dmitriigluzdov/kaggriculture-a-smaller-market-shock` | tschinkel-2945-lineage | rule-based agent on The 2945 Farm base; an otherwise idle opening worker grows one extra wheat crop before... |
| `dmitriigluzdov/kaggriculture-herd-safe-sale-window-lb-2700` | herd-safety | full-season controller: finances planting, livestock care, collection and sales; two complete production pl... |
| `dmitriigluzdov/kaggriculture-more-wheat-smarter-sales` | ahmed-V-series | scheduled crop and livestock controller with reactive market decisions; built on shiiin9's Order Book, Ahme... |
| `dmitriigluzdov/kaggriculture-one-more-wheat` | tschinkel-2945-lineage | rule-based agent: Tschinkel's Metav4 farm plus Nathan Jacob's Pipe16 idle-worker layer; the temporary openi... |
| `dmitriigluzdov/kaggriculture-two-coins-one-sheep-lb-2600` | moon-frontier-lineage | rule-based farming routes (The Moon Counts Melons, public v37 parent) with a two-action sale window from da... |
| `drashtisingh14/novabyte-kaggriculture` | tutorial-starter-baseline | Kaggriculture tutorial with a melon-maxxer example agent (56 lines): step toward target tile, sell melons b... |
| `dreldirdirifadol/dirdiri-3` | heuristic-and-rule-agents | rule-based agent in one 221-line agent() function (code cell only) |
| `dynamo14324/kaggriculture-advanced-ml-decision-framework` | no-strategy-text | n/a (one code cell; no top-level defs or prose visible to the structure skim; the strategy was not read) |
| `dynamo14324/kaggriculture-breaking-the-3500-barrier` | replay-analysis | not an agent: analysis of the current meta shifts and a performance comparison of published agents; V22 (Ka... |
| `dynamo14324/kaggriculture-reproducible-multi-worker-policy` | heuristic-and-rule-agents | single-file observation-only agent: staged crop liquidity, animal production and worker allocation (plans,... |
| `dynamo14324/kaggriculture-starter-guide` | tutorial-starter-baseline | heuristic agent (agent, 44 lines) with profitability analysis of crops and animals |
| `ektarr/diversified-scheduler-baseline-kaggriculture` | heuristic-and-rule-agents | dependency-free main.py agent (diversified scheduler) with a run_match harness; default 25-tile plan spread... |
| `emanuellcs/kaggriculture-agent` | tape-and-route-replay | trace replay: a full season of actions for the farmer and the hands plus market orders at every step; the t... |
| `evelyn3976/kaggriculture-adaptive-market-scheduler-v1` | heuristic-and-rule-agents | rule-based adaptive market scheduler (one code cell): episode-state reset, farm and hand normalisation help... |
| `evelyn3976/kaggriculture-frontier-v156-coherent-liquidity-v6` | moon-frontier-lineage | rule-based frontier-lineage agent with coherent liquidity: weed repair, fresh-market state, trace actor (ba... |
| `evelyn3976/kaggriculture-kaito-v27-public-safety-v7` | kaito-lineage | guard layer around an embedded Kaito v27 rebalance action list (base85 payload, not decoded): action normal... |
| `evelyn3976/kaggriculture-v21-public-market-v5` | kaito-lineage | payload-loaded v21 public-market agent: market delta application, sell totals and selection (agent, 111 lin... |
| `evelyn3976/kaggriculture-v6-limited-dynamic-v8` | moon-frontier-lineage | frontier-style agent with the same helper set as the frontier v156 notebook: limited dynamic market control... |
| `evgendvorkin/kaggriculture` | kaito-lineage | copy of anhadmahajan06's autonomous farming agent (chassis, router, parent liquidation) in a code cell, wit... |
| `farhanabidtech786/kaggriculture-beginner-friendly` | heuristic-and-rule-agents | n/a (near-copy of indarkarhana/rank-top10-read-the-market-choose-the-farm) (near-copy of `indarkarhana/rank-top10-read-the-market-choose-the-farm`) |
| `farukece/kaggriculture-episodes-guided-tour-of-the-dataset` | replay-analysis | not an agent: guide to the Kaggriculture Episodes dataset: what each table holds, how tables join, quality... |
| `fatihmiilliolu/kaggriculture-episodes-comprehensive-eda-agent` | replay-analysis | EDA of the Kaggriculture Episodes dataset with a time series of average score; key takeaways; an agent cell... |
| `fierus/xray-kaggle` | replay-analysis | not an agent: public-data analysis of one submission (56087555) across 75 public episodes; a scripted openi... |
| `fleongg/kaggriculture-public-2830-4-v21-1-no-preemption` | kaito-lineage | exact submitted agent bytes (payload parts, not decoded): Kaito Fukami's v21 tactical-memory agent with one... |
| `flexonafft/kaggriculture-adaptive-farm-intelligence` | compiled-cpp-policy | n/a (near-copy of avioon/kaggriculture-apex-v7-god-emperor) (near-copy of `avioon/kaggriculture-apex-v7-god-emperor`) |
| `flexonafft/kaggriculture-most-powerfull-route` | aurax-reactive-router | reactive router in a writefile cell with the same helper set as aurax7's reactive router (shed adjacency, p... |
| `flexonafft/kaggriculture-multi-route-farming-agent` | no-strategy-text | n/a (five cells; no defs or prose visible to the structure skim; the strategy was not read) |
| `flexonafft/kaggriculture-smart-farm-strategy-lab` | no-strategy-text | n/a (two cells; no defs or prose visible to the structure skim; the strategy was not read) |
| `foysalemonshanto/last-day-lb-2727-2` | ahmed-V-series | n/a (near-copy of ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins) (near-copy of `ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins`) |
| `foysalemonshanto/read-the-market-choose-the-farm` | x-and-other-named-agents | E283 variant B1: the 3025.0 B0 agent plus one controlled behavioural change (a Feed5-first opening adapted... |
| `georgymamarin/kaggriculture-visualized-what-every-crop-pays` | replay-analysis | not an agent: visual beginner's guide to every mechanic and to what each crop pays; a small step-toward age... |
| `georgymamarin/kaggriculture-what-2600-farms-do-differently` | replay-analysis | not an agent: analysis page on episode features: the top of the board against the middle of the same window... |
| `goodpjw2008/kaggriculture-melon-threshold-squeeze-2749` | aurax-reactive-router | n/a (near-copy of aurax7/kaggriculture-shop-router-reactive-v5) (near-copy of `aurax7/kaggriculture-shop-router-reactive-v5`) |
| `guruprasaathas111/game-theoretic-master-discrete-optimization` | heuristic-and-rule-agents | pure uncompressed master agent with a game-theoretic framing: symmetric competing agents, a 720-turn horizo... |
| `guruprasaathas111/kaggriculture-fully-dynamic-autonomous-agent` | aurax-reactive-router | n/a (near-copy of aurax7/kaggriculture-shop-router-reactive-v5) (near-copy of `aurax7/kaggriculture-shop-router-reactive-v5`) |
| `guruprasaathas111/kaggriculture-master-engine-v3` | heuristic-and-rule-agents | master engine (V6 in its title): integrates 13 pre-computed public route tapes, a sales reservation window... |
| `guruprasaathas111/kaggriculture-master-engine-v53e01d74d8f` | ahmed-V-series | n/a (near-copy of ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins) (near-copy of `ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins`) |
| `guruprasaathas111/kaggriculture-top-2-master-engine-v4` | heuristic-and-rule-agents | 41-route multi-expert system: microstructure immunity, dynamic shop adaptation, deterministic submission; l... |
| `haidangnguyen1802/ppotrain` | no-strategy-text | n/a (two cells; no defs or prose visible to the structure skim; the title suggests PPO training but the str... |
| `haideptry/countering-the-big-3-meta` | replay-analysis | n/a (near-copy of haideptry/demystifying-2900-meta-reflex-engine-and-bot) (near-copy of `haideptry/demystifying-2900-meta-reflex-engine-and-bot`) |
| `haideptry/demystifying-2900-meta-reflex-engine-and-bot` | replay-analysis | not an agent: forensic breakdown of the late-season breakthroughs past 2850-2945 Elo: from brittle static r... |
| `haideptry/the-2950-peak-farm` | kaito-lineage | n/a (near-copy of evgendvorkin/kaggriculture) (near-copy of `evgendvorkin/kaggriculture`) |
| `haideptry/the-2965-master-hybrid-engine` | heuristic-and-rule-agents | hybrid engine (V79 Harvest Ledger) with an evidence-led rollback of V78; writefile chassis agent |
| `haideptry/the-shepherds-ledger-herd-safe-sovereign` | herd-safety | herd-safe sovereign agent (MarketShock-M1-WR1K): protects guaranteed feed buffers of wheat and water throug... |
| `hakdevelopment/kaggriculture-2887-score-fieldcraft-agent` | packaging-and-embedded-payload | compact release of a previously submitted agent with an offline build, a match demo and diagnostics; the ag... |
| `hanialsh/notebook868efb1104` | no-strategy-text | n/a (three cells; no defs or prose visible to the structure skim; the strategy was not read) |
| `hanifnoerrofiq/a-wonderful-life` | packaging-and-embedded-payload | payload packaging: a gzip and tar payload in the cell (not decoded); checkpoint agent by title |
| `hanifnoerrofiq/pioneers-of-kaggle-town` | packaging-and-embedded-payload | checkpoint 1 packaging: an lzma and base64 payload in the cell (not decoded) |
| `hanifnoerrofiq/pioneers-of-kaggle-town-candidate-2` | packaging-and-embedded-payload | checkpoint-base candidate: lzma and base64 agent payload in the cell (not decoded) |
| `hank0123/kaggriculture-is-your-agent-really-better` | evaluation-and-measurement | not an agent: reusable paired-seed evaluation: seat splits, paired outcomes, bootstrap intervals, a results... |
| `haodou092/kaggriculture-harvest-ledger` | kaito-lineage | rule-based final agent V94: restores the V81 spatial mirror gate; complete stable production policy; market... |
| `hboyang/kitex-v0` | kaito-lineage | derivative of Kaito v48 fast routes with a short list of changes (KiteX v0) |
| `hesoponyo/pure-rl-agent-bc-ppo-self-play` | rl-and-learned | learned: a per-unit entity-token Transformer policy, behaviour-cloned on about 4,600 episodes, then PPO sel... |
| `hgh1024/kaggriculture-herd-safe-v2-sale-horizon-2` | moon-frontier-lineage | n/a (near-copy of dmitriigluzdov/kaggriculture-two-coins-one-sheep-lb-2600) (near-copy of `dmitriigluzdov/kaggriculture-two-coins-one-sheep-lb-2600`) |
| `holeneckles/grandmaster` | heuristic-and-rule-agents | rule-based agent with six helpers (step direction, Manhattan distance, shed adjacency, nearest shed tile, q... |
| `holeneckles/notebooke394244546` | heuristic-and-rule-agents | single rule-based agent() function in one code cell |
| `hosen42/kaggriculture-m4a-metav4-sr18-2690-1` | ahmed-V-series | Hack2Publish agent derived from Ahmed Berat Ozer's public V47 (Apache-2.0 notices kept in main.py); complet... |
| `hosen42/kaggriculture-v11-hc1-full-panel-validation` | evaluation-and-measurement | not a policy: full opponent-panel validation of agent V11-HC1 on fresh seeds, both seats, after a focused test |
| `hosen42/kaggriculture-v11-hc1-vs-h5-validation` | evaluation-and-measurement | not a policy: focused validation of HC1 against H5 (primary) and V11 (regression) on fresh seeds with exact... |
| `hosseinbadrnezhad/kaggriculture-episodes-index-etl-eda-visualize-mod` | replay-analysis | ETL, EDA and visualisation over the episodes index: safe CSV reads, missingness audit, column typing, plots... |
| `hosseinbadrnezhad/kaggriculture-reference-agents-etl-eda-visualize-m` | replay-analysis | ETL, EDA and visualisation over reference agents: the same pipeline as the episodes-index notebook; not a p... |
| `hussainbakhsh5/notebook372c7e8667` | heuristic-and-rule-agents | series of rule-based crop agents: wheat agents v1 to v5, a melon agent and a carrot agent, with a hire test... |
| `iamsdt/kaggriculture-from-the-source-price-clock-trap` | engine-and-market-analysis | not an agent: the price machine, the clock and the traps, derived from the environment source and checked a... |
| `iamsdt/kaggriculture-what-a-farmer-turn-is-worth` | engine-and-market-analysis | not an agent: value of a farmer-turn: what a hand earns rather than what it costs; walking share; best harv... |
| `indarkarhana/kaggriculture-verified-route-replay-2948-9` | tape-and-route-replay | packages a recorded route trajectory from a public ladder replay (THUNDER THUNDER, episode 90565430, the wi... |
| `indarkarhana/rank-top10-read-the-market-choose-the-farm` | heuristic-and-rule-agents | deterministic agent: treats the public shop sequence as an early demand signal and commits to one farm plan... |
| `indarkarhana/shape-the-shop-work-the-pasture-top-10` | tape-and-route-replay | layered visible-state rule network over a complete farm; conserved cow and sheep pasture bundles relabelled... |
| `indarkarhana/what-your-kaggriculture-benchmark-isn-t-measuring` | evaluation-and-measurement | not an agent: two ways a local benchmark reports the wrong number: replay-derived opponents desynchronised... |
| `ishivapatil/adaptive-replay-agent-kaggriculture` | clone-and-preemption-sales | adaptive replay agent: public-signature clone profile, front-running, terminal liquidation, shed access and... |
| `ishivapatil/kaggriculture-cow-empire-v3` | heuristic-and-rule-agents | cow-focused rule-based agent: one agent() function in a code cell |
| `ishivapatil/kaggriculture-cow-empire-v4` | heuristic-and-rule-agents | n/a (near-copy of ishivapatil/kaggriculture-cow-empire-v3) (near-copy of `ishivapatil/kaggriculture-cow-empire-v3`) |
| `ishivapatil/kaggriculture-limit-breaker-agent` | moon-frontier-lineage | frontier-lineage agent (limit breaker): regime, copy action, hand alignment, trace actor and weed repair he... |
| `ishivapatil/kaggriculture-mathematical-exploit-agent` | heuristic-and-rule-agents | rule-based agent with Manhattan distance, move and agent functions; the markdown frames it mathematically |
| `ishivapatil/kaggriculture-v27-midgame-meta-reset-thunder` | kaito-lineage | Kaito v27 midgame meta reset packaged in the frontier-style helper set (thunder variant) |
| `ishivapatil/strict-future-meta-reset-v25-hardcoded-replay` | moon-frontier-lineage | n/a (near-copy of ishivapatil/kaggriculture-limit-breaker-agent) (near-copy of `ishivapatil/kaggriculture-limit-breaker-agent`) |
| `jamesgambrah/kaggriculture-tournament-agent` | heuristic-and-rule-agents | tournament agent: FarmState, a 255-line MultiTilePlanner, next-step routing and Manhattan distance |
| `jamesgambrah/kaggriculture-tournament-agent-dr-james-gambrah` | heuristic-and-rule-agents | tournament agent with a MarketEngine (63 lines), shed-adjacency helpers and next-step routing |
| `jaxa623/2780-beyond-48-0-128-128-worlds-with-95-cis` | engine-and-market-analysis | n/a (near-copy of jaxa623/2802-two-identical-agents-90-points-apart) (near-copy of `jaxa623/2802-two-identical-agents-90-points-apart`) |
| `jaxa623/2802-two-identical-agents-90-points-apart` | engine-and-market-analysis | not an agent: presentation of two identical agents rated 90 points apart; the notebook is largely CSS for r... |
| `jeffmarcecadet/reverse-engineering-rank-5-thunder-thunder` | aurax-reactive-router | rule-based price-adaptive portfolio farm (THUNDER THUNDER, rank 5): not a tape; builds change from game to... |
| `jek1wantaufik/building-a-kaggriculture-ai-agent` | packaging-and-embedded-payload | n/a (one code cell with a source-splitting helper, split_source; the strategy was not read) |
| `jerisadeumai/kaggriculture-capstone-mixture-of-experts-moe` | rl-and-learned | mixture-of-experts agent: crop expected-value model with a switch on price against base price, BFS farmer z... |
| `jocelyndumlao/kaggriculture-ai-agent` | packaging-and-embedded-payload | n/a (77 cells; a git helper run_git and no visible strategy text; the strategy was not read) |
| `joelpjoseph/kaggriculture-v4-1` | aurax-reactive-router | rule-based chassis agent: a 501-line Chassis class with make_agent, shed adjacency and no-op helpers |
| `jominurk21cs1077/opponent-economy-forecast-300-to-719-top40` | replay-analysis | XGBoost forecast of opponent final bank from turn 0-299 features, trained on top-40 team replays |
| `jominurk21cs1077/opponent-economy-forecast-300-to-719-top5` | replay-analysis | XGBoost forecast of opponent final bank trained on the top-5 live leaderboard teams' replays (named in the... |
| `jominurk21cs1077/opponent-economy-forecast-top40-v5` | replay-analysis | GPU XGBoost forecast of opponent final bank from turn 0-299 features; trained on top-40 replays only |
| `joymietalicuad/economics-driven-rule-agent-ecobot-v2` | heuristic-and-rule-agents | economics-driven rule agent (EcoBot v2): workload-adaptive crew sizing, adaptive herd scaling, grain feed,... |
| `junaid512/02-adaptive-replay-agent` | clone-and-preemption-sales | agent combining a replay-derived 719-step production schedule with price-impact SELL ranking, near-clone ga... |
| `junaid512/kaggriculture-v01-drip` | heuristic-and-rule-agents | agent built from an audit of the environment source (drip strategy): depth table, probes, Wilson intervals,... |
| `justinmnic/kaggriculture` | rl-and-learned | learned: MPECS self-play and relational-critic training (initial self-play stage); no submitted policy read |
| `juvenalpedrobaptista/kaggriculture` | heuristic-and-rule-agents | single rule-based agent() function (69 lines) in one code cell |
| `juyhg65/65-notebookks` | heuristic-and-rule-agents | single rule-based agent() function (61 lines) in one code cell |
| `jwj1342/kaggriculture-final-strategy-and-lessons` | evaluation-and-measurement | not an agent: postmortem of experiments, failures and corrections for two final submissions (a team named R... |
| `kaitofukami/103-128-fresh-public-v43-sparse-shop-hybrid` | kaito-lineage | public-state hybrid: one coherent 719-step opening with exactly two observable shop branches and no opponen... |
| `kaitofukami/159-160-vs-frontier-v20-weed-slip-recovery` | kaito-lineage | closed-loop route mirror of the Frontier public agent with a bounded recovery from visible weed slips; iden... |
| `kaitofukami/177-180-fresh-top-30-v21-1-conditional-memory` | kaito-lineage | public-state nearest-route memory that changes order, not inventory; identity-free conditional order contro... |
| `kaitofukami/238-238-known-streams-v58-minimax-closed-loop` | kaito-lineage | public-state best-response engine (minimax, closed loop): keeps an option-preserving route; four observable... |
| `kaitofukami/25-27-strict-future-v27-midgame-meta-reset` | kaito-lineage | dominant low-entropy HIRE4 opening kept; the stale continuation replaced; a higher-scoring seat router reje... |
| `kaitofukami/40-40-early-floor-39-46-top-10-v48-fast-routes` | kaito-lineage | fast-routes public backbone (v43 idea) with a few empirically justified continuations; v48 repairs an execu... |
| `kaitofukami/v15-top5-robust-market-gate` | kaito-lineage | validated modal route (senkin13 episode) kept unchanged; consensus-gated collision market controller: v13 e... |
| `kaiwalyaatulraut/kaggriculture-solution` | heuristic-and-rule-agents | n/a (near-copy of romanrozen/strong-barnyard-economist) (near-copy of `romanrozen/strong-barnyard-economist`) |
| `kaptaan45/kaggriculture-championship-agent-simulation` | heuristic-and-rule-agents | championship agent (GrandmasterAgent): town-demand adaptive portfolio over unlocked shops, and multi-agent... |
| `kathimunishwar/kaggriculture-replay-agent` | heuristic-and-rule-agents | n/a (near-copy of romanrozen/strong-barnyard-economist) (near-copy of `romanrozen/strong-barnyard-economist`) |
| `kenanzhang9/kaggriculture-a1-t31-guard` | heuristic-and-rule-agents | controlled candidate built on the strongest historical A1 policy; keeps A1's final-day behaviour and adds o... |
| `kenanzhang9/notebook6cc8bf1c92` | ahmed-V-series | n/a (near-copy of ahmedberatozer/more-yield-smarter-labor) (near-copy of `ahmedberatozer/more-yield-smarter-labor`) |
| `keremelik/kaggriculture-cash-path-1327` | engine-and-market-analysis | not an agent: a short engine lab on cash flow (engine 1.32.7): cash comes only from selling; shops unlock e... |
| `keremelik/kaggriculture-paired-not-paper` | evaluation-and-measurement | not an agent: paired bank delta versus paper Elo; a 20-0 result inverted against a dump live rating (about... |
| `keremelik/kaggriculture-two-fail-cells` | evaluation-and-measurement | not an agent: identification of two late failing cells (missing milk and missing wool) in one open-loop fil... |
| `kevin250304/kaggriculture-healthstone-route-20260810` | boatlee-clean-room | n/a (one code cell packaging a HealthStone route; the route was not read) |
| `kirderf/live-seed-test-v3` | engine-and-market-analysis | seed-recovery study: rebuilds pre-spawn empty and weed masks from public observations to recover the hidden... |
| `kirderf/seed-recover-live-test-thom95` | engine-and-market-analysis | n/a (near-copy of kirderf/seed-recover-live-test-thom95-v2) (near-copy of `kirderf/seed-recover-live-test-thom95-v2`) |
| `kirderf/seed-recover-live-test-thom95-v2` | engine-and-market-analysis | live seed-recovery test: a 65-line Recover class run against an observed live episode |
| `kirderf/seed-recover-weed-live` | engine-and-market-analysis | live seed recovery with weed masks: is_weed, empty tiles and tile masks feeding a 78-line Recover |
| `kirderf/seedbf-c-build-v2` | engine-and-market-analysis | seed brute-force build: draws candidate seeds and checks them against the observed state (py_draw) |
| `kirderf/seedbf-weed-build` | engine-and-market-analysis | seed brute-force on weed builds: build_mask and py_check against observed weeds |
| `kiykhoi/kaggriculture-agents` | no-strategy-text | n/a (one code cell; the strategy was not read) |
| `koushikkumardinda/kaggriculture-starter` | heuristic-and-rule-agents | meta-strategy agent: precomputed Fibonacci hire cost curve, town shop arbitrage, labour and liquidity manag... |
| `koushikrudra/kaggriculture-preempt-h6` | clone-and-preemption-sales | trace-replay farm layer (public Hamburger lineage) with a market layer rewritten for the 2026-08-06 balance... |
| `krishnayadav456wrsty/kaggriculture` | tschinkel-2945-lineage | n/a (near-copy of thomastschinkel/kaggriculture-public-state-router-74-5-win-rate) (near-copy of `thomastschinkel/kaggriculture-public-state-router-74-5-win-rate`) |
| `kunaldesale2408/kaggriculture-2026-v1` | replay-analysis | analysis notebook with an article-mode switch (SHOW_ANALYSIS); the claims were not read beyond the switch |
| `kunaldesale2408/kaggriculture-ttv1` | packaging-and-embedded-payload | packages the audited public Top-2 Master Engine V4 branch against five frozen opponent families; production... |
| `l4r3nn/kaggriculture-agent-v1` | no-strategy-text | n/a (one code cell; the strategy was not read) |
| `lamhuy8904/kaggriculture-master-tactical-agent` | replay-analysis | notes from replay hunting and a tactical agent: four hidden failure modes found by auditing replays from th... |
| `laveshjadon/kagriculture-winning-notebook` | tschinkel-2945-lineage | n/a (near-copy of thomastschinkel/the-2945-farm-96-vs-the-top-10-public-bots) (near-copy of `thomastschinkel/the-2945-farm-96-vs-the-top-10-public-bots`) |
| `leneen/kaggriculture` | heuristic-and-rule-agents | baseline balanced farmer: wheat for early cash, melons for revenue; step toward nearest target; plant and e... |
| `leoprovorov/a-song-of-ice-and-fire-final-update` | replay-analysis | n/a (near-copy of leoprovorov/a-song-of-ice-and-fire-fixed-flexible) (near-copy of `leoprovorov/a-song-of-ice-and-fire-fixed-flexible`) |
| `leoprovorov/a-song-of-ice-and-fire-fixed-flexible` | replay-analysis | not an agent: command-by-command analysis of the top agent Majkel1337: a command is a class plus a good; av... |
| `leoprovorov/kaggricult-man-reverse-engineering` | replay-analysis | replay laboratory and an exact agent map of the top agents, with one bounded market-timing intervention (T4... |
| `lime0001/score2710-t23-kaggriculture-smart-harvest` | ahmed-V-series | n/a (near-copy of ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins) (near-copy of `ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins`) |
| `lixiuqixiaoke/v24-robustmarketlead` | tape-and-route-replay | n/a (near-copy of binasalama/kaggriculture-v28-gate-fixed) (near-copy of `binasalama/kaggriculture-v28-gate-fixed`) |
| `llccqq624/did-my-farm-make-the-highlight-reel` | replay-analysis | replay lookup tool: types a team name and counts its wins, losses, seats and familiar opponents from the re... |
| `llccqq624/kaggriculture-adaptive-barnyard-portfolio` | heuristic-and-rule-agents | two-part portfolio: melons play the long game, wheat keeps the barn moving, and a mixed herd turns spare ac... |
| `llccqq624/kaggriculture-adaptive-counterbook` | no-strategy-text | n/a (near-copy of reyhanksatria/kaggriculture-adaptive-shop-guard) (near-copy of `reyhanksatria/kaggriculture-adaptive-shop-guard`) |
| `llccqq624/kaggriculture-adaptive-shop-guard` | no-strategy-text | n/a (near-copy of reyhanksatria/kaggriculture-adaptive-shop-guard) (near-copy of `reyhanksatria/kaggriculture-adaptive-shop-guard`) |
| `llccqq624/kaggriculture-counter-cycle-ranch` | heuristic-and-rule-agents | n/a (near-copy of llccqq624/kaggriculture-adaptive-barnyard-portfolio) (near-copy of `llccqq624/kaggriculture-adaptive-barnyard-portfolio`) |
| `llccqq624/kaggriculture-dual-market-relay` | no-strategy-text | n/a (near-copy of reyhanksatria/kaggriculture-adaptive-shop-guard) (near-copy of `reyhanksatria/kaggriculture-adaptive-shop-guard`) |
| `llccqq624/kaggriculture-market-aware-crop-mix` | heuristic-and-rule-agents | diversified crop mix: plots of melon, carrot and wheat; reduces melon exposure when its price falls or the... |
| `llccqq624/kaggriculture-market-weather-report` | replay-analysis | replay analysis of market price paths: which products are calm and which chaotic, and the days each market... |
| `llccqq624/kaggriculture-melon-rush-baseline` | heuristic-and-rule-agents | n/a (near-copy of llccqq624/kaggriculture-market-aware-crop-mix) (near-copy of `llccqq624/kaggriculture-market-aware-crop-mix`) |
| `llccqq624/kaggriculture-opening-book-first-48-turns` | replay-analysis | replay analysis: compresses strong openings (first 48 turns) into readable sequences and a small set of ope... |
| `llccqq624/kaggriculture-premium-queue-split` | no-strategy-text | n/a (near-copy of reyhanksatria/kaggriculture-adaptive-shop-guard) (near-copy of `reyhanksatria/kaggriculture-adaptive-shop-guard`) |
| `llccqq624/kaggriculture-replay-data-miner` | replay-analysis | data miner: turns the strongest replays into tidy episode, player and action tables |
| `llccqq624/kaggriculture-the-shops-remember-the-route` | no-strategy-text | n/a (near-copy of reyhanksatria/kaggriculture-adaptive-shop-guard) (near-copy of `reyhanksatria/kaggriculture-adaptive-shop-guard`) |
| `llccqq624/kaggriculture-top-5-meta-ensemble` | no-strategy-text | n/a (one code cell; the strategy was not read) |
| `llccqq624/kaggriculture-weedproof-clone-market` | no-strategy-text | n/a (near-copy of reyhanksatria/kaggriculture-adaptive-shop-guard) (near-copy of `reyhanksatria/kaggriculture-adaptive-shop-guard`) |
| `lokesh0252/kaggriculture-v1` | ahmed-V-series | n/a (near-copy of ahmedberatozer/more-yield-smarter-labor) (near-copy of `ahmedberatozer/more-yield-smarter-labor`) |
| `lucashmateo/kaggriculture-replays-no-oom-3-dataframes` | replay-analysis | replay tooling: loads one game from the multi-GB replays parquet into three DataFrames (actions, banks, mar... |
| `lucifer19/harvest-nocturne-v2-a-lighter-start` | tape-and-route-replay | Harvest Nocturne V2: a lighter start on the same rhythm; packages a deterministic archive; credits the Two... |
| `lucifer19/kaggriculture-night-harvest` | tape-and-route-replay | order-safe challenger: exact marginal impact on the proven production basin; freezes the 719-step route; V2... |
| `lynnsakurai/farmer-john-and-the-idle-seller` | ahmed-V-series | mathematical framing of a reorder operator: within one invocation the established reorder operator is appli... |
| `lynnsakurai/farmer-john-and-the-wheat-seller` | ahmed-V-series | wheat-seller variant: sale rule over the parent's executable sale, demand from revealed shops, and the mark... |
| `lynnsakurai/farming-score-a-mathematical-approach` | ahmed-V-series | four-route programme as the policy backbone; three public checkpoints select prefix-compatible continuation... |
| `lynnsakurai/farming-score-v2-a-better-approach` | ahmed-V-series | V2: removes a remaining defect in the final sale queue, where the projected pre-market stock of each cash p... |
| `lynnsakurai/farming-score-v3-replay-revised` | ahmed-V-series | the supplied two-route policy converted from C++ to one standalone Python agent; at turn 360 route 1 is sel... |
| `lynnsakurai/farming-score-v4-a-better-shop` | ahmed-V-series | V4: same-day weed recovery and shop-conditioned livestock substitution; a Chassis and make_agent router (wr... |
| `lynnsakurai/farming-score-v5-timing-optimized` | ahmed-V-series | n/a (near-copy of lynnsakurai/farming-score-v4-a-better-shop) (near-copy of `lynnsakurai/farming-score-v4-a-better-shop`) |
| `makimakiai/kaggriculture-carrot-fleet-simple-python-baseline` | heuristic-and-rule-agents | small deterministic baseline agent: move toward target, jobs, unit actions, market actions (agent) |
| `manderson240/cohezion-kaggriculture-multi-agent-policy-baseline` | tutorial-starter-baseline | single code cell: optimize_agricultural_policy, an optimisation-based multi-agent policy baseline; the stra... |
| `manjunadhpadarthi/new-benchmark-task-0f570` | evaluation-and-measurement | not an agent: FarmBench, a benchmark asking a language model to make fifteen economic decisions from Kaggri... |
| `mansiaggarwal88/kaggriculture-build-your-first-farming-agent` | tutorial-starter-baseline | tutorial agent: handle market, planting and plant care, and my_wheat_farmer; prints a text summary and asks... |
| `mansiaggarwal88/kaggriculture-can-specialists-beat-one-agent` | heuristic-and-rule-agents | not a submission: a portfolio of four specialist modules (Cournot, linear programming, real options) compar... |
| `mansiaggarwal88/kaggriculture-local-agent-evaluation-harness` | evaluation-and-measurement | not a strategy notebook: harness that runs baseline and challenger agents, summarises win rates, mean score... |
| `mansiaggarwal88/kaggriculture-reactive-agent-550-lb` | heuristic-and-rule-agents | reactive agent: strategic decisions every 2-3 days separated from turn-level execution; the best observed p... |
| `mansiaggarwal88/when-smart-math-fails-in-adversarial-games` | engine-and-market-analysis | not an agent: why real-options and volatility reasoning misfires in an adversarial market, where demand res... |
| `mansiaggarwal88/why-our-kaggriculture-ai-failed-math-vs-reality` | evaluation-and-measurement | not an agent: score history of a failed farming AI and its redesign into adaptive agents (version 3) |
| `maverickss26/kaggriculture-v1` | heuristic-and-rule-agents | agent built after reading the environment source: the README numbers disagree with the code; a BFS agent wi... |
| `maximolorenzoylosada/kaggriculture-what-a-turn-is-worth` | engine-and-market-analysis | not an agent: the scarce resource is actions (720 per game); profit per action for crops and animals; melon... |
| `merkiraz/counter-cyclical-orchard` | heuristic-and-rule-agents | independently written, observation-driven agent (Adaptive Biome Scheduler V3): distributed endgame and cash... |
| `mhmda81/kaggriculture-data-quality-check` | replay-analysis | data quality check on 639 episodes: missing values, duplicates and score anomalies (IQR outliers); not a po... |
| `mhmda81/kaggriculture-unlocked-a-beginner-s-guide` | replay-analysis | beginner's guide to the match replay dataset: what it contains and a visualisation of episode scores; not a... |
| `mobeenfatimah/kaggriculture-agribot-heuristic-state-machine` | heuristic-and-rule-agents | heuristic state-machine agent (KaggricultureSimulator, 47 lines): environment rules extracted from the mark... |
| `mohitsongra/kaggriculture-getting-started` | tutorial-starter-baseline | tutorial with an agent (213 lines): task planning (_tasks), step toward and Manhattan helpers |
| `mohui666/kaggriculture-v66-public-agent` | heuristic-and-rule-agents | Kaggriculture v66: public-observation rule agent; the complete source is in a repository (candidate_v66_met... |
| `moncefelm/kaggriculture-getting-started` | heuristic-and-rule-agents | agent with a forecast class and shop daily-draw helpers (_Forecast, avg_sale_price, _shop_daily_draw, _cent... |
| `motemen/kaggriculture-meta-census-lineage-occupancy` | replay-analysis | not an agent: who is farming what at the top of the ladder, and how fast the meta rotates; lineage occupancy |
| `moushunchen/twelve-seeds-three-melons` | x-and-other-named-agents | field notes from a 600-Elo farm: successive versions (v0 to v8) with ideas per version; v7 and v8 are on th... |
| `mpwolke/doomed-kaggleculture-harvest` | heuristic-and-rule-agents | rule-based VirtualFarmAgent (25 lines) and agent (31 lines) in code cells; course-style notebook |
| `mqingcs/kaggriculture-observed-production-and-last-dance` | compiled-cpp-policy | two independent policies sharing a licensed production and market layer: observed production (56713902) and... |
| `msama01/kaggriculture-evaluation-agent-performance-analys` | evaluation-and-measurement | evaluation harness: fixture agent, engine-behaviour checks, quick duels, archive loader, challenger evaluat... |
| `mtoshidesu/testkaggriculture-getting-started` | tutorial-starter-baseline | n/a (near-copy of bovard/kaggriculture-getting-started) (near-copy of `bovard/kaggriculture-getting-started`) |
| `mtoshidesu/testkaggriculture-hamburger` | moon-frontier-lineage | Frontier Fusion: starts from the uploaded Frontier Lab high-score baseline and adds only changes with a cle... |
| `muelsyse111/kaggriculture-crop-timing-and-labor-budget` | tutorial-starter-baseline | not an agent: rules-derived planning for crop timing, shed pressure and farm-hand cost curves; not an agent... |
| `muelsyse111/kaggriculture-exp006-independent-baseline-audit` | tutorial-starter-baseline | independently written baseline crop controller: budgets existing cash, models future supply and demand, res... |
| `muelsyse111/kaggriculture-exp20260908-01-funding-audit` | evaluation-and-measurement | rejected funding-trigger experiment: one off-boundary budget check added to the policy; NO-GO, not submitted |
| `mugundhjb/v21-multi-route-agent-sell-divergence-guarder` | kaito-lineage | v21 multi-route agent with a sell-divergence guard (kawa route labels, legacy layout switch, action copy) |
| `muneeb2405/kaggriculture-cow-ranch-with-fertilizer-probe` | clone-and-preemption-sales | from C68 to a calibrated SmartMarketController: a cow ranch with a fertiliser probe; replay opponent shifts... |
| `municef1/lb-2448-single-file-kaggriculture-agent` | tape-and-route-replay | single-file agent: a fixed 719-step tape for farm and market, evolved from yhay81's shop-router route 0 by... |
| `mzcao7/kaggriculture-2476-8-peak-lightgbm-xgboost` | rl-and-learned | learned ensemble agent (EnsembleAgent) with LightGBM and XGBoost tree models on state features; route asset... |
| `nagatakengo/costs` | engine-and-market-analysis | not an agent: hiring costs and timing; cost functions per crop (wheat one-time seed 10, price 25, first yie... |
| `nagatakengo/kaggriculture` | heuristic-and-rule-agents | V6.2 notebook: StrategyConfig with market price, score, sell rules for melon and milk, harvest age and tile... |
| `nagatakengo/predict-future-melon-prices` | heuristic-and-rule-agents | not an agent: predicts future melon prices from replay movements of two skill cohorts (lowest 10% and 20%,... |
| `nagatakengo/range-of-action` | replay-analysis | not an agent: where farmers and workers spend their time: stagnation areas, actions per tile, route animati... |
| `nagatakengo/study-kaggriculture` | replay-analysis | not an agent: extracts two datasets by final money: the position of the top xx% and the whole-field xx%; th... |
| `nathanjacob/beyond-v43-what-the-top-clusters-do-on-turn-1` | replay-analysis | not an agent: strategy-clustering pipeline that fingerprints the top 50 leaderboard teams and groups them b... |
| `nathanjacob/colosseum-876-2600-agent-testing-framework` | evaluation-and-measurement | n/a (21 cells: an agent testing framework named Colosseum; the framework was not read beyond its title) |
| `nathanjacob/how-many-twins-strategy-clustering-kaggriculture` | replay-analysis | n/a (strategy clustering on twin agents; the cells were not read beyond the title) |
| `nathanjacob/kaggriculture-pipe-2-agent` | pipe-lineage | n/a (two cells; the agent was not read beyond its structure) |
| `nathanjacob/kaggriculture-pipe-5-terminal-boost` | pipe-lineage | n/a (near-copy of nathanjacob/kaggriculture-pipe-7-wheat-microstructure) (near-copy of `nathanjacob/kaggriculture-pipe-7-wheat-microstructure`) |
| `nathanjacob/kaggriculture-pipe-7-wheat-microstructure` | pipe-lineage | one parameter change on the V45 base: buying seventy wheat is no longer the best first-turn action (microst... |
| `nathanjacob/kaggriculture-pipe-8-clean-opening` | pipe-lineage | two synergistic opening changes on the Pipe-7 line, found by a six-step pipeline |
| `nathanjacob/kaggriculture-pipe15-two-layers` | pipe-lineage | n/a (the Pipe15 agent with two layers; the cells were not read beyond the title) |
| `nathanjacob/kaggriculture-pipe16-idle-workers` | pipe-lineage | Pipe-16 on the Metav4 farm: idle workers turn wasted PASS actions into free wheat; a fork of the Metav4 base |
| `nathanjacob/kaggriculture-pipe18-six-layers` | pipe-lineage | n/a (near-copy of nathanjacob/kaggriculture-pipe16-idle-workers) (near-copy of `nathanjacob/kaggriculture-pipe16-idle-workers`) |
| `nathanjacob/no-cow-left-behind-v40-autopsy-fix` | replay-analysis | post-mortem and fix of Ahmed Berat Ozer's v40 (dead cows bug), found by replay analysis |
| `navazshfathi/notebook198200c757` | no-strategy-text | n/a (four cells; no defs or prose visible to the structure skim; the strategy was not read) |
| `navazshfathi/notebook76f6a59396` | no-strategy-text | n/a (near-copy of navazshfathi/notebook198200c757) (near-copy of `navazshfathi/notebook198200c757`) |
| `navazshfathi/shop-router-0908` | tape-and-route-replay | n/a (near-copy of yhay81/shop-router-0908) (near-copy of `yhay81/shop-router-0908`) |
| `nekkon/strawberry-pays-24x-what-the-price-table-says` | engine-and-market-analysis | not an agent: strawberry pays 24 times what the README price table says; simulation of drain by day, sell r... |
| `nekkon/the-strawberry-field-is-worth-3-847` | engine-and-market-analysis | not an agent: value of a full strawberry field: about 100 units sold for 3,847, not the 12,000 the base pri... |
| `nihilisticneuralnet/kaggriculture-population-robust-economy` | no-strategy-text | n/a (four cells; no defs or prose visible to the structure skim; the strategy was not read) |
| `nikital7/4000x-environment-speedup-kaggriculture` | engine-and-market-analysis | not an agent: a bit-exact C++ port of the environment: an episode in 0.18-0.30 ms instead of 815 ms; identi... |
| `nishchaljainds/kaggriculture-full-engine-teardown-my-agent` | engine-and-market-analysis | full engine teardown plus the complete agent submitted: market price helpers, sell blocks, shed drop, lifet... |
| `nursrijan/kaggriculture-market-economics-game-theory` | engine-and-market-analysis | analytical and algorithmic study of the market game: melon sale revenue simulation and a grandmaster v4 age... |
| `nursrijan/kaggriculture-starter-agent-strategy` | tutorial-starter-baseline | starter agent and strategy guide: planting, watering, fertilising, harvesting and weed clearing; livestock... |
| `nusrati/2650-score` | aurax-reactive-router | n/a (near-copy of flexonafft/kaggriculture-most-powerfull-route) (near-copy of `flexonafft/kaggriculture-most-powerfull-route`) |
| `nusrati/2715-6` | tape-and-route-replay | n/a (near-copy of yhay81/shop-router-0908) (near-copy of `yhay81/shop-router-0908`) |
| `ocean240812/kaggress-meta-rl-vs-deterministic` | replay-analysis | not an agent: a comparison of paradigms after ten days and fourteen of the author's own submissions: fronti... |
| `ocean240812/kaggriculture-complete-eda-baseline-agent` | tutorial-starter-baseline | EDA and a baseline wheat-loop agent (68 lines): yield per tile per day, ROI, net profit and a shape and pri... |
| `ocean240812/kaggriculture-strategy-guide` | tutorial-starter-baseline | teaching notebook with a minimal agent and a local game runner (make_minimal_agent, run_local_game) and a f... |
| `olegmelnik/kaggriculture-c68-thunder-adaptive` | tschinkel-2945-lineage | compact packaging of the public C68 solution: a refreshed THUNDER field route with price-impact SELL orderi... |
| `olegmelnik/kaggriculture-v26-seat-portfolio` | kaito-lineage | v26 Break the Copy Cycle: two complete routes, one per engine seat (post-v25 HIRE4 route for seat 0) |
| `paiky1995/inside-the-kaggriculture-market-machine` | engine-and-market-analysis | not an agent: an explanation of the market machine (price shapes and inventory response) across 44 cells |
| `pavloivanin/kaggriculture-baseline` | heuristic-and-rule-agents | enhanced deterministic agent (adaptive town-market): dynamic price floor guard, 25-plot core with a Northea... |
| `pengwang91/wide-sigma-cma-tuned-scenario-aware-submitted` | moon-frontier-lineage | a copy of pilkwang's scenario-aware economic policy plus a machine-tuned knob layer (CMA-ES with a wide sig... |
| `pilkwang/kaggriculture-precomputed-schedule-policy` | tape-and-route-replay | precomputed schedule policy: a 720-turn action program fixed before the first observation (sigma); both sea... |
| `pilkwang/kaggriculture-structured-economic-policy` | evaluation-and-measurement | research candidate B: the same V36 parent program and no-op slot adapter as candidate A; an admission model... |
| `premaananda108/rule-agent-ecobot-v7-arena-analytics` | heuristic-and-rule-agents | fully reactive economics-driven rule agent (EcoBot v7): sell orders re-priced every turn against the live m... |
| `priyankavuruti/kaggiculture-ai-farmingagent` | heuristic-and-rule-agents | multi-agent orchestrator: BaseAgent, SecurityGuard, CropAdvisor, WeatherRisk and MarketPrice agents under K... |
| `prvsiyan/kaggle-frontier-lab-strategy-improvement` | evaluation-and-measurement | promotion funnel: seventeen routers faced five strong controls on four unseen seeds; three finalists frozen... |
| `prvsiyan/kaggriculture-baseline` | moon-frontier-lineage | baseline controller with a one-worker-less opening: four farm hands instead of five; engine 1.32.6 with sel... |
| `prvsiyan/kaggriculture-dawn-ledger-pareto-action-cards` | educational-decision-aid | standalone educational lab: Pareto action cards comparing visible farm actions on reward, turns, energy, fo... |
| `prvsiyan/kaggriculture-field-clock-action-budget` | educational-decision-aid | compact inspectable policy for choosing the next farm action under a limited visible budget: tasks ranked b... |
| `prvsiyan/kaggriculture-floor-aware-market-ledger-20260923` | engine-and-market-analysis | floor-aware visible-state attribution: a market ledger that infers a rival's sales as a certified lower bou... |
| `prvsiyan/kaggriculture-frontier-lab-high-score-visuals` | moon-frontier-lineage | exact standalone main.py and submission archive; the action sequence distilled from public episode 89256171... |
| `prvsiyan/kaggriculture-frontier-the-moon-counts-melons` | moon-frontier-lineage | executable strategy lab: reconstructs the exact controller built on haideptry's public source; final market... |
| `prvsiyan/kaggriculture-frontier-the-soil-remembers-rain` | moon-frontier-lineage | executable strategy lab on the same controller family: archived carrot study (V228 and V229) describing ear... |
| `prvsiyan/kaggriculture-hybrid-state-ledger-20260922` | heuristic-and-rule-agents | original reproducible policy pattern: a visible-state regime switch for routes, price guards and action bud... |
| `prvsiyan/kaggriculture-market-ledger-seasonal-counterplay` | educational-decision-aid | educational framework: legal visible observations are translated into an explicit strategy phase; action ad... |
| `prvsiyan/kaggriculture-reserve-garden-counterfactuals` | educational-decision-aid | visible-state strategy notebook for ranking a small action set while protecting cash and food reserves, wit... |
| `prvsiyan/kaggriculture-route-ab-timing-lab-20260921` | engine-and-market-analysis | reproducible study of a visible-state route change: keep the established production and market controller a... |
| `prvsiyan/kaggriculture-the-win-rate-illusion` | evaluation-and-measurement | write-up on why win rate misleads: a win rate over one panel is not a measure of strength (notebook text) |
| `prvsiyan/kaggriculture-visible-price-shock-lab-2026-09-22` | engine-and-market-analysis | lab on visible price shocks: how a visible price move on one product changes the policy's sales (notebook t... |
| `prvsiyan/kaggriculture-visible-price-switch-lab` | educational-decision-aid | small standalone lab: a state-conditioned crop decision that uses only the market prices visible in the obs... |
| `prvsiyan/kaggriculture-weatherboard-route-regime-switches` | educational-decision-aid | visible-state route board: decides when a market-dependent plan is available, affordable and worth using (R... |
| `prvsiyan/where-the-wheat-remembers-tomorrow-kaggriculture` | evaluation-and-measurement | version 2 public evidence update: the agent artifact is byte-identical; a publicly observable action trajec... |
| `rafifariqrabbani/kaggriculture-greedy-optimizer-staged-frozen-rl` | rl-and-learned | hybrid: greedy candidate generation and optimisation (every possible action proposed, Hungarian worker assi... |
| `rahuljiwane/kaggriculture-rahul-jiwane` | kaito-lineage | n/a (near-copy of kaitofukami/177-180-fresh-top-30-v21-1-conditional-memory) (near-copy of `kaitofukami/177-180-fresh-top-30-v21-1-conditional-memory`) |
| `rajan1673/kagriculture` | heuristic-and-rule-agents | rule-based agent (59 lines) with target finding, step toward, crop tile classification and animal targets |
| `rakhansyah/an-unintelligent-attempt-teaching-greedy-workers` | clone-and-preemption-sales | greedy workers that read the market: a mix formula re-weights every crop every day by its projected value;... |
| `rauffauzanrambe/kaggriculture-finding-conditional-fresh-vegetable` | replay-analysis | replay analysis log: engine mechanics first, then earlier public strategy families; section 4 with an agent... |
| `ravi123a321at/177-180-fresh-top-30-v21-1-conditional-memory` | kaito-lineage | n/a (near-copy of kaitofukami/177-180-fresh-top-30-v21-1-conditional-memory) (near-copy of `kaitofukami/177-180-fresh-top-30-v21-1-conditional-memory`) |
| `raykkretzschmar/kaggriculture-findings-from-zero-to-top-meta` | replay-analysis | notes and working diary, not a single policy: a local agent built from repeatable moves of the current lead... |
| `raykkretzschmar/kaggriculture-rank-your-agent` | evaluation-and-measurement | ranking tool, not a policy: a seat-swapped round robin against a fixed ladder of tiers, ranked by Bradley-T... |
| `rehanliaqat17/kaggriculture-getting-started` | tutorial-starter-baseline | tutorial with a simulation engine, a farm-state analysis, an advanced macro agent (132 lines), a smart agen... |
| `renjistarfall/kaggriculture-best-agent` | ahmed-V-series | n/a (near-copy of ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins) (near-copy of `ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins`) |
| `revanthtambisetty/kaggriculture-economy-mechanics` | engine-and-market-analysis | n/a (reference tables from the engine source; no strategy) |
| `revanthtambisetty/two-private-bots-beating-kaggriculture-meta` | replay-analysis | not an agent: structured extraction from 15 recent replays (3 per top-5 team) grouping the top five by open... |
| `reyhanksatria/adaptive-route-agent-v1` | packaging-and-embedded-payload | packed route agent: a base64 and zlib payload in the cell (not decoded); adaptive route agent by title |
| `reyhanksatria/adaptive-route-agent-v2` | packaging-and-embedded-payload | packed route agent: an agent payload in the cell (not decoded); adaptive route agent by title |
| `reyhanksatria/best-market-agent-high-strategy` | heuristic-and-rule-agents | n/a (near-copy of indarkarhana/rank-top10-read-the-market-choose-the-farm) (near-copy of `indarkarhana/rank-top10-read-the-market-choose-the-farm`) |
| `reyhanksatria/kaggriculture-adaptive-shop-guard` | no-strategy-text | n/a (one code cell; the strategy was not read; the title names an adaptive shop guard) |
| `reyhanksatria/kaggriculture-dynamic-route-agent` | no-strategy-text | n/a (two cells; the strategy was not read; the title names a dynamic route agent) |
| `ritzraha/cow-money-melon-mayhem-and-the-scoreboard` | heuristic-and-rule-agents | rule-based agent that reads the price curves backwards and then reads the opponent (agent, 265 lines): quad... |
| `rivakajangu/your-rating-is-noisier-than-your-improvement` | engine-and-market-analysis | not an agent: a note on measuring: the same bit-identical agent resubmitted scored about 270 points apart;... |
| `rogerrogerroger3r/kaggriculture-a-ruler-for-agent-changes` | engine-and-market-analysis | not an agent: a paired head-to-head harness plus a C++ agent route without root; noise measured by resubmit... |
| `rogerrogerroger3r/test-a-public-agent-before-you-spend-a-slot` | evaluation-and-measurement | not an agent: a test of a public agent before a live slot is spent: games needed and a z-score; the agent's... |
| `rogerrogerroger3r/the-best-player-s-tape-is-not-the-best-tape` | tape-and-route-replay | tape study: sixteen tapes extracted from public episodes of agents rated 2970 to 3074 (3074 was rank 1 on t... |
| `rohitt94/kaggriculture-route-replay-agent` | packaging-and-embedded-payload | route replay agent packaging: verify agent, normalise, build the archive and sanity check; the route was no... |
| `romanrozen/strong-barnyard-economist` | heuristic-and-rule-agents | barnyard economist write-up and agent (31 cells); the cells were not read beyond the layout styling |
| `romantamrazov/kaggriculture-hamburger` | moon-frontier-lineage | n/a (the Hamburger lineage notebook; the cells were not read beyond the title) |
| `ronaldkwilson/measuring-is-the-hard-part` | evaluation-and-measurement | not an agent: notes on the evaluation harness; a no-op audit found 45% of harvest actions were silently doi... |
| `rubenmaya/pruebas` | heuristic-and-rule-agents | planner with simulate_sell, price_at, a fibonacci hire cost, a market manager, a strategic planner and a Hu... |
| `ryanmyers03/kaggriculture-agent-v1` | heuristic-and-rule-agents | dependency-free agent(obs) implementation, the same as the one submitted; local run and submission notes |
| `ryuorlandotamin/kaggriculture-is-your-new-agent-actually-better` | evaluation-and-measurement | not an agent: Bayesian evaluation of noisy agent comparisons: Dirichlet posteriors on outcomes, paired tabl... |
| `safwanahmadsaffi/kaggriculture-findings-from-zero-to-top-meta` | replay-analysis | n/a (near-copy of raykkretzschmar/kaggriculture-findings-from-zero-to-top-meta) (near-copy of `raykkretzschmar/kaggriculture-findings-from-zero-to-top-meta`) |
| `saitejabandaruin/kaggriculture-pure-architecture-2600-elo-v3` | heuristic-and-rule-agents | grandmaster architecture: progressive disclosure, fail-fast and quick recovery, designed for a 0% timeout r... |
| `saitejabandaruin/kaggriculture-pytorch-dqn-baseline` | rl-and-learned | learned baseline: a PyTorch DQN agent (DQNAgent) with a starter EDA of crop yields, weather patterns and ma... |
| `saitejabandaruin/kaggriculture-ultimate-mega-ensemble-3000` | heuristic-and-rule-agents | mega-ensemble of routers under the same grandmaster design: frontier trace router (The Moon Counts Melons)... |
| `saitejabandaruin/kaggriculture-winning-strategies` | replay-analysis | not an agent: replay parser and parallel loader, feature engineering across replays, winning-strategy minin... |
| `saitejabandaruin/starter-complete-pytorch-dqn-agent` | rl-and-learned | n/a (near-copy of saitejabandaruin/kaggriculture-pytorch-dqn-baseline) (near-copy of `saitejabandaruin/kaggriculture-pytorch-dqn-baseline`) |
| `sakhawathossen/hybrid-kaggriculture` | clone-and-preemption-sales | n/a (near-copy of sakhawathossen/kaggriculture-final-hybrid-champion) (near-copy of `sakhawathossen/kaggriculture-final-hybrid-champion`) |
| `sakhawathossen/kaggriculture-final-hybrid-champion` | clone-and-preemption-sales | adaptive C166 anti-meta agent: a second active-slot experiment against the plateauing V27 agent; promotes a... |
| `salaheldinelnabarawy/kaggriculture-engine-mechanics-field-guide` | engine-and-market-analysis | n/a (rules read from the public engine source; no strategy) |
| `salemali7/harvest-kaggriculture` | harvestforge-x | HarvestForge-X: production-focused strategy built around rapid livestock expansion and efficient field use;... |
| `salemali7/kaggriculture-2900` | harvestforge-x | HarvestForge-X 2900 variant: reconstructed from reference runs 92165990, 92185587 and 92223213; payload loa... |
| `sangitabannore/kaggriculture-sangita-jiwane-2` | boatlee-clean-room | n/a (near-copy of boatlee/v16-rc2-high-score-near-mirror-market-relay) (near-copy of `boatlee/v16-rc2-high-score-near-mirror-market-relay`) |
| `sanketmahale2701/kaggriculture-episodes-eda` | replay-analysis | EDA of the Kaggriculture episodes dataset (13 cells; no definitions or prose visible to the structure skim;... |
| `secretiveplotter1863/kaggleculture` | heuristic-and-rule-agents | single rule-based agent() function (44 lines) in one code cell |
| `semalytics/kaggriculture-melon-first-strategy-v6b` | heuristic-and-rule-agents | reactive melon-first agent (V6b): tile zones, BFS first move, task and worker actions, and a market builder... |
| `serariagomes/kaggriculture-rule-based-agent` | heuristic-and-rule-agents | baseline rule-based agent with a local evaluation loop, config sweep, tile census, a Foreman helper and a p... |
| `seyamalam/kaggriculture-open-source-agent` | no-strategy-text | n/a (one code cell; the strategy was not read) |
| `seyitkaangunes/kaggriculture-2820-score` | kaito-lineage | V44 plus four market layers: layers 1, 2 and 4 in the first live submission; all four in the second; replay... |
| `shashvatsingham/kaggriculture-a-robust-heuristic-farmer` | no-strategy-text | n/a (the robust heuristic farmer was not read beyond the title) |
| `shashwat12a/kaggriculture-rl-model` | no-strategy-text | n/a (an RL model notebook; the cells were not read beyond the title) |
| `shiiin9/your-market-list-is-an-order-book` | kaito-lineage | n/a (near-copy of degnonguidi/best-agent-ranking) (near-copy of `degnonguidi/best-agent-ranking`) |
| `shivam2212/high-speed-compressed-replay-retrival` | replay-analysis | tool for high-speed retrieval of compressed replays (the cells were not read beyond the title) |
| `shivam2212/shiv17-5-turn-counter-relay` | clone-and-preemption-sales | rule-based counter-relay (should_counter_relay): sells fertiliser stock five turns before its own scheduled... |
| `shorooghahmadi/kaggriculture-agent-v2` | heuristic-and-rule-agents | n/a (near-copy of shorooghahmadi/kaggriculture-economics-farm-manager) (near-copy of `shorooghahmadi/kaggriculture-economics-farm-manager`) |
| `shorooghahmadi/kaggriculture-economics-farm-manager` | heuristic-and-rule-agents | rule-based farm manager with the environment's exact price and yield formulas reimplemented; capital policy... |
| `shorooghahmadi/kaggriculture-v2-agent` | heuristic-and-rule-agents | from-scratch rule-based agent v2, tested locally against the built-in starter; changes from v1 kept where t... |
| `shorooghahmadi/kaggriculture-v3-agent` | kaito-lineage | v3 agent with a contribution card: upstream Kaito v21.1 conditional-memory agent; public route provenance f... |
| `shorooghahmadi/kaggriculture-v3-agent4` | heuristic-and-rule-agents | v2 agent diagnosis and fixes with verified local results: price-aware crop choice, targeted fertiliser, ong... |
| `shrutikondabathula/submission-ipynb` | heuristic-and-rule-agents | submission agent: analyze_state, farm_scanner, generate_farmer_actions, intelligent_score and a best-action... |
| `shrutikondabathula/submission-v1-ipynb` | heuristic-and-rule-agents | submission v1: crop_score, scan_farm, build_task_queue and score_task (a task queue with best-action choice) |
| `sidhaarthshree/a-reactive-agent-with-optimal-task` | heuristic-and-rule-agents | reactive agent of about 660 lines: optimal task assignment, census and preflight checks; every decision com... |
| `sidhaarthshree/kaggriculture-the-scarcity-rancher` | heuristic-and-rule-agents | the same reactive agent under another title: about 660 lines; price history, duel and census helpers; prefl... |
| `sidhaarthshree/the-complete-getting-started-guide` | tutorial-starter-baseline | getting-started guide: replay display, board reading, shed inference, price and sell revenue, buy cost and... |
| `skomuro/2000-baseline-silver-medal-route` | tutorial-starter-baseline | 2,000+ baseline: a complete farming route, market timing and tape-signature helpers (_tape_at, _signature_d... |
| `songoku2005/kaggriculture` | heuristic-and-rule-agents | rule-based agent in a 458-line submission.py (writefile): distance, step-toward and shed-tile helpers, agen... |
| `souvikdbiswas/kaggriculture-v5-hybrid-agent` | rl-and-learned | V5 hybrid: safe multi-route portfolio with reactive integrity: prefix-compatibility checks, feature extract... |
| `starkhushi/kaggriculture-6-engine-traps-each-one-measured` | engine-and-market-analysis | not an agent: six engine traps measured by reading kaggriculture.py: the wheat loop in the official guide h... |
| `statma/kaggriculture-herd-safe-sale-window-race-ca20` | herd-safety | herd-safe sale window race (ca20): writes the verified competition archive with a sha256 check; cells not r... |
| `statma/kaggriculture-herd-safe-sale-window-race-ca25` | herd-safety | herd-safe sale window race (ca25): archive build; cells not read beyond the header |
| `statma/kaggriculture-herd-safe-sale-window-submit` | herd-safety | herd-safe sale window submission notebook; cells not read beyond the header |
| `statma/kaggriculture-tetsutani-demand-preserving` | tschinkel-2945-lineage | packaging of tetsutani's demand-preserving turn sale timing (cells not read beyond the title) |
| `statma/kaggriculture-thomas-2944-candidate` | tschinkel-2945-lineage | candidate packaging of the 2944 agent in the 2945 Farm lineage (cells not read beyond the title) |
| `stevenleehans/kaggriculture-rank-580-lord-momo-returns` | packaging-and-embedded-payload | packaging of a rank-580 agent (Lord Momo returns); cells not read beyond the title |
| `stevenleehans/kaggriculture-strongest-farmer-of-today` | packaging-and-embedded-payload | n/a (near-copy of stevenleehans/kaggriculture-rank-580-lord-momo-returns) (near-copy of `stevenleehans/kaggriculture-rank-580-lord-momo-returns`) |
| `stevenleehans/kaggriculture-x544-nah-i-d-win` | tschinkel-2945-lineage | standalone X567 main.py: the verified X562 route plus one frozen market-only overlay (move SELL MILK 6 from... |
| `stevenleehans/kaggriculture-x578-i-m-the-strongest` | tschinkel-2945-lineage | standalone X594 main.py: a Ryo-live adaptive closed-loop planner, based on the complete Ryo Hasegawa replay... |
| `stpeteishii/kaggriculture-head-to-head-match-runner` | replay-analysis | tooling, not a policy: runs a head-to-head match between two submissions (main.py files) and renders the re... |
| `stpeteishii/kaggriculture-match-replay-reproducer` | replay-analysis | tooling: reproduces a played match from its saved episode JSON without agent files |
| `sumitchavhan7/kaggriculture-episodes-2026-08-07` | replay-analysis | replay analytics on the 2026-08-07 episodes: parallel file loading, configurable sampling caps, per-step an... |
| `sunil123kumar/kaggriculture-idle-workers` | pipe-lineage | n/a (near-copy of nathanjacob/kaggriculture-pipe16-idle-workers) (near-copy of `nathanjacob/kaggriculture-pipe16-idle-workers`) |
| `sunil123kumar/kaggriculture-sale-window` | moon-frontier-lineage | n/a (near-copy of dmitriigluzdov/kaggriculture-two-coins-one-sheep-lb-2600) (near-copy of `dmitriigluzdov/kaggriculture-two-coins-one-sheep-lb-2600`) |
| `sunil123kumar/kaggriculture-top-10-public-bots` | tschinkel-2945-lineage | n/a (near-copy of thomastschinkel/the-2945-farm-96-vs-the-top-10-public-bots) (near-copy of `thomastschinkel/the-2945-farm-96-vs-the-top-10-public-bots`) |
| `sunil123kumar/kaggriculture-v6` | aurax-reactive-router | n/a (near-copy of aurax7/kaggriculture-shop-router-reactive-v5) (near-copy of `aurax7/kaggriculture-shop-router-reactive-v5`) |
| `sunil123kumar/kaggriculture-v8` | ahmed-V-series | n/a (near-copy of ahmedberatozer/kaggriculture-v48-clear-the-queue) (near-copy of `ahmedberatozer/kaggriculture-v48-clear-the-queue`) |
| `sunil123kumar/kaggriculture-wheat-microstructure` | pipe-lineage | n/a (near-copy of nathanjacob/kaggriculture-pipe-7-wheat-microstructure) (near-copy of `nathanjacob/kaggriculture-pipe-7-wheat-microstructure`) |
| `sunyuxiang136/kaggriculture-opening-stock-v8-frozen-baseline` | tschinkel-2945-lineage | frozen baseline of an older agent for studying inventory, execution and market timing; builds on the attrib... |
| `sushanthtiruvaipati/kaggriculture-barnyard-frontrun-v1` | heuristic-and-rule-agents | rule-based barnyard front-running agent: shed access, projected shed, public signature helpers in one code... |
| `syedtahahassan/kaggriculture-hack` | ahmed-V-series | n/a (near-copy of ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins) (near-copy of `ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins`) |
| `takamichitoda/flyfarmer-connectome-plays-kaggriculture` | x-and-other-named-agents | a joke entry: a fly connectome (728 neurons, 35,704 synapses) wired as a farm controller; no learning; the... |
| `taylorclark637/kaggriculture` | heuristic-and-rule-agents | Omega-State sovereign agent: Joseph-stabilised EKF oracle for prices and an A* lattice router for swarm dis... |
| `taylorclark637/kaggriculture-the-biosphere-construct-v22` | heuristic-and-rule-agents | Biosphere Construct V22: an autonomous economic arbitrage and swarm-routing agent; a Joseph-stabilised EKF... |
| `taylorclark637/sovereign-swarm-kinematics-the` | heuristic-and-rule-agents | autonomous self-optimising sovereign agent (QEL engine): an environment class, an introspective log-parsing... |
| `techabinesh/competition-launch-kaggriculture` | heuristic-and-rule-agents | single agent() function (102 lines) in one code cell |
| `tetsutani/adaptive-farming-strategy-for-kaggriculture` | tschinkel-2945-lineage | adaptive farming strategy: a public policy whose farm motion and forest-axis figures show the strategy (sho... |
| `tetsutani/demand-preserving-turn-sale-timing` | tschinkel-2945-lineage | demand-preserving turn sale timing: a public policy with KPI cards, forest axes and plant and pasture count... |
| `tetsutani/fork-of-adaptive-farming-strategy-for-kaggricult` | tschinkel-2945-lineage | fork of tetsutani's adaptive farming strategy with the same figures and an embedded magic policy (regime, c... |
| `tetsutani/market-smart-farming-kaggriculture` | tschinkel-2945-lineage | market smart farming: figures and KPI cards for a tetsutani-style route; plant and pasture counts per season |
| `tetsutani/shape-the-shop-work-the-pasture-kaggriculture` | tschinkel-2945-lineage | shape the shop, work the pasture: tetsutani figures with KPI cards and plant and pasture counts; the route... |
| `theepanss/notebooke6e24888ed` | heuristic-and-rule-agents | KaggricultureProAgent with an agent_function in one code cell (structure only) |
| `themeend/177-180-fresh-top-30-v21-1-conditional-memory` | kaito-lineage | n/a (near-copy of kaitofukami/177-180-fresh-top-30-v21-1-conditional-memory) (near-copy of `kaitofukami/177-180-fresh-top-30-v21-1-conditional-memory`) |
| `thomastschinkel/kaggriculture-93-8-win-rate-public-state-router` | tschinkel-2945-lineage | public-state router: six-day blocks (144 turns), five stored public tapes from top-ladder runs, public stat... |
| `thomastschinkel/kaggriculture-95-5-win-rate-via-replay-routing` | tschinkel-2945-lineage | router over public replays: one opening for six days, then one of several public schedules chosen from mark... |
| `thomastschinkel/kaggriculture-public-state-router-74-5-win-rate` | tschinkel-2945-lineage | public-state router v3.1: prefix-guarded tail switching between routes sharing the same opening turns; thre... |
| `thomastschinkel/the-2945-farm-96-vs-the-top-10-public-bots` | tschinkel-2945-lineage | route replayer (v9/4), standard library only: the public lineage's recorded 720-turn schedules, re-selected... |
| `thomastschinkel/the-metav4-farm-submission-v13` | tschinkel-2945-lineage | route replayer (Metav4 tape) with two corrections: labour hires priced on the Fibonacci scale and a loosene... |
| `timmass2/the-kaggriculture-market-end-to-end` | engine-and-market-analysis | n/a (analysis notebook: price and demand model with charts; no submitted policy in the cells read) |
| `titakongolo/notebook-kaggriculture-replay-lab-en` | replay-analysis | replay lab: turns every replay into a competitive advantage (English); analysis of replays with 18 cells, n... |
| `titakongolo/notebook-kaggriculture-replay-lab-fr` | replay-analysis | Replay Lab (French): explains why a final score does not suffice to improve an agent; demo replay creation... |
| `tokenjunkielabs/titan-arlene-v14-source` | moon-frontier-lineage | unchanged Arlene v14 baseline packaged under Apache-2.0, attributed to Arlene and lynnsakurai (the farming... |
| `tokenjunkielabs/titan-kaggriculture-frontier-source` | kaito-lineage | TITAN: an Apache-2.0 derivative of Kaito Fukami's public v43 SparseShopHybrid agent, with attributed inventors |
| `tokenjunkielabs/tokenjunkielabs-farm-manager` | packaging-and-embedded-payload | offline TITAN agent: retrieves one fixed, merged release and preserves its exact source with its licences (... |
| `trnhquangminh140/kaggriculture-strategic-decision-making` | heuristic-and-rule-agents | strategic decision agent with a digital-twin state (DigitalTwinState): automatic land expansion, dynamic ma... |
| `tuannm3812/hierarchical-task-coordinator-htdc-v12` | heuristic-and-rule-agents | Hierarchical Task-Driven Coordinator (HTDC v12): greedy joint-optimal search with exhaustive fallback for u... |
| `umutdorukztrk/kagricultre-baseline` | heuristic-and-rule-agents | baseline rule-based agent with bfs, move_towards and agent (code cells) |
| `uninhibitedscholar/kaggriculture-beyond-48-order-sequencing` | engine-and-market-analysis | n/a (near-copy of jaxa623/2802-two-identical-agents-90-points-apart) (near-copy of `jaxa623/2802-two-identical-agents-90-points-apart`) |
| `uninhibitedscholar/kaggriculture-pipe-7-market-microstructure` | pipe-lineage | n/a (near-copy of nathanjacob/kaggriculture-pipe-7-wheat-microstructure) (near-copy of `nathanjacob/kaggriculture-pipe-7-wheat-microstructure`) |
| `vaibhavchavanpatil/kaggriculture-capstone-project-final` | heuristic-and-rule-agents | capstone rule-based agent: scans the NW quadrant, harvests mature crops first, then waters |
| `varshakattimani/building-a-kaggriculture-ai-agent` | packaging-and-embedded-payload | n/a (near-copy of jek1wantaufik/building-a-kaggriculture-ai-agent) (near-copy of `jek1wantaufik/building-a-kaggriculture-ai-agent`) |
| `vedant7312/222222` | tape-and-route-replay | n/a (near-copy of indarkarhana/shape-the-shop-work-the-pasture-top-10) (near-copy of `indarkarhana/shape-the-shop-work-the-pasture-top-10`) |
| `vijaikm/kaggriculture-bc-policy-inference-starter` | rl-and-learned | learned: pure-NumPy behaviour-cloning policy inference on the spatial BC policy weights, trained on the 500... |
| `vijaikm/kaggriculture-gpu-trap-cpu-run` | no-strategy-text | n/a (one code cell; the strategy was not read) |
| `vijaikm/kaggriculture-match-replay-eda-starter` | replay-analysis | EDA and action forensics on 500+ match replays: spawn symmetry and win-rate disparity between seats; town s... |
| `vijaikm/kaggriculture-modular-agent-framework` | heuristic-and-rule-agents | modular agent architecture: TileInfo and ObservationWrapper, SpatialNavigator, CropManager, MarketBroker an... |
| `vijaikm/kaggriculture-score-convergence-2026` | engine-and-market-analysis | not an agent: how many days until a submission's score is real: 15 submissions (v30-v44) and 231 episodes p... |
| `vijaikm/kaggriculture-simulation-eda` | engine-and-market-analysis | simulation EDA and market microstructure analytics: shape functions and market price; a SimulationReplayAna... |
| `vijaikm/new-benchmark-task-209d2` | evaluation-and-measurement | benchmark task: a decision-transformer return-to-go construction (kaggriculture_dt_rtg); not an agent |
| `vijaikm/new-benchmark-task-2d7c5` | evaluation-and-measurement | benchmark task: spatial topography (spatial_topography); not an agent |
| `vijaikm/new-benchmark-task-3c74f` | evaluation-and-measurement | benchmark task: market elasticity price (market_elasticity_price); not an agent |
| `vijaikm/new-benchmark-task-6549a` | evaluation-and-measurement | benchmark task: preemption game theory (preemption_game_theory); not an agent |
| `vinceybb/kaggriculture-validate-before-you-submit` | evaluation-and-measurement | validation-first harness for a public agent: exact artifact identity, deterministic packaging, self-play an... |
| `vishal567/why-tomatoes-lost-a-60-game-kaggriculture-agent` | replay-analysis | analysis of why a tomato-based agent lost 60 games (title); the cells were not read beyond the title |
| `web3cainiao/kaggriculture-v21-tactical-memory` | kaito-lineage | attributed reproduction of the public Kaito v21 tactical-memory route; the 144/150 in the title is a local... |
| `wei111111/v46d-skill-rebuild-review-guide` | replay-analysis | not an agent: review guide for v46d: Bradley-Terry and Elo competition models, the agent engineering frame,... |
| `weijunguo/kaggriculture-reproducible-local-benchmark` | evaluation-and-measurement | balanced 20-match local comparison of V13 and V14.4 with a reproducible benchmark; a complexity argument fo... |
| `wzhengbiao/kaggriculture-hybu-submit` | no-strategy-text | n/a (one code cell; the strategy was not read) |
| `wzhengbiao/kaggriculture-v15stack-nb` | no-strategy-text | n/a (near-copy of wzhengbiao/kaggriculture-v15stack-submit) (near-copy of `wzhengbiao/kaggriculture-v15stack-submit`) |
| `wzhengbiao/kaggriculture-v15stack-submit` | no-strategy-text | n/a (one code cell; the strategy was not read) |
| `xishengfeng/kaggriculture-replay-database` | no-strategy-text | n/a (one code cell; the strategy was not read) |
| `xishengfeng/rl-v9-market-off-tape-rulemirror-league` | rl-and-learned | market-off-tape RL v9: a RuleMirror of the tape, a MarketGym for the market, and a causal league; tape sell... |
| `xreina8/does-a-farming-game-get-supply-and-demand-right` | engine-and-market-analysis | not an agent: estimates the market price elasticity from the public episodes (ordinary least squares with f... |
| `xreina8/kaggriculture-300-melons-return-36-of-face-value` | engine-and-market-analysis | not an agent: what selling does to one's own price, absorption per day, the centre multiplier, from the eng... |
| `xreina8/kaggriculture-a-b-two-agents-with-error-bars` | evaluation-and-measurement | not an agent: an A/B harness for two agents with Wilson 95% intervals; a run of twenty games (12-8) is show... |
| `xreina8/what-decides-rating-once-money-stops-mattering` | engine-and-market-analysis | not an agent: what decides rating once money stops mattering: 44,000 ladder games with per-agent features a... |
| `xuantianfengwu/kaggriculture-adaptive-land-allocator` | heuristic-and-rule-agents | n/a (near-copy of xuantianfengwu/kaggriculture-capacity-release) (near-copy of `xuantianfengwu/kaggriculture-capacity-release`) |
| `xuantianfengwu/kaggriculture-adaptive-land-allocator-r10` | heuristic-and-rule-agents | n/a (near-copy of xuantianfengwu/kaggriculture-capacity-release) (near-copy of `xuantianfengwu/kaggriculture-capacity-release`) |
| `xuantianfengwu/kaggriculture-capacity-release` | heuristic-and-rule-agents | rule-based capacity-release agent: financing base from day 3; from hour 20 releases crop stock by warehouse... |
| `xuantianfengwu/kaggriculture-day-3-cow-challenger` | heuristic-and-rule-agents | n/a (near-copy of xuantianfengwu/kaggriculture-capacity-release) (near-copy of `xuantianfengwu/kaggriculture-capacity-release`) |
| `xuantianfengwu/kaggriculture-hour-4-financing-allocator` | heuristic-and-rule-agents | n/a (near-copy of xuantianfengwu/kaggriculture-capacity-release) (near-copy of `xuantianfengwu/kaggriculture-capacity-release`) |
| `xuantianfengwu/kaggriculture-melon-baseline-v4` | heuristic-and-rule-agents | melon baseline v4: a rule-based agent with crop plan, task list, move and unit actions; submission.py is fi... |
| `xuantianfengwu/kaggriculture-preempt-selector` | clone-and-preemption-sales | preempt selector: the animal mix is chosen at the opening, and sales are pre-empted ahead of the harvest wa... |
| `xuantianfengwu/kaggriculture-terminal-logistics` | heuristic-and-rule-agents | n/a (near-copy of xuantianfengwu/kaggriculture-capacity-release) (near-copy of `xuantianfengwu/kaggriculture-capacity-release`) |
| `xuantianfengwu/kaggriculture-timed-six-cow` | clone-and-preemption-sales | six-cow capital allocator: pre-empts a neighbour's next-day milk sale with a single-batch sale |
| `xuanzhang001/kaggriculture-auto-top1` | tschinkel-2945-lineage | n/a (near-copy of dmitriigluzdov/kaggriculture-one-more-wheat) (near-copy of `dmitriigluzdov/kaggriculture-one-more-wheat`) |
| `xuanzhang001/kaggriculture-pipe7-public-top1` | pipe-lineage | n/a (near-copy of nathanjacob/kaggriculture-pipe-7-wheat-microstructure) (near-copy of `nathanjacob/kaggriculture-pipe-7-wheat-microstructure`) |
| `y3uanm/kaggriculture-conservative-market-router-v5` | tschinkel-2945-lineage | n/a (near-copy of y3uanm/kaggriculture-safe-baseline-rollback-v20) (near-copy of `y3uanm/kaggriculture-safe-baseline-rollback-v20`) |
| `y3uanm/kaggriculture-market-impact-router-v4` | tschinkel-2945-lineage | n/a (near-copy of y3uanm/kaggriculture-safe-baseline-rollback-v20) (near-copy of `y3uanm/kaggriculture-safe-baseline-rollback-v20`) |
| `y3uanm/kaggriculture-safe-baseline-rollback-v20` | tschinkel-2945-lineage | safe rollback of v20 as a public-state router: prefix-guarded tail switching and three online repairs, with... |
| `yamakawanin/kaggriculture-2312-9-q30-v2a` | x-and-other-named-agents | replay-distilled programme-network agent (q30_v2a): shop-conditioned 72-turn physical choreography; not a p... |
| `yamakawanin/kaggriculture-adaptive-public-state-multi-route` | x-and-other-named-agents | adaptive public-state multi-route version of the programme agent (cells not read beyond the title) |
| `yamakawanin/kaggriculture-public-state-adaptive-champion-v2` | x-and-other-named-agents | public-state adaptive champion v2 of the programme agent (cells not read beyond the title) |
| `yamakawanin/king-v4e-rc4` | x-and-other-named-agents | King-v4e RC4: a replay-derived programme-network agent (not primitive-action RL, not a neural policy); matu... |
| `yangkuangou/9-goods-one-market-kaggriculture-price-lab` | engine-and-market-analysis | not an agent: a copyable price and sale lab: each unit gets a quote from the shared inventory; supply moves... |
| `yangkuangou/kaggriculture-agent-lab-copy-replay-compare` | tutorial-starter-baseline | agent lab: copy a dependency-light wheat agent (copyable_wheat_agent), a paired cash check, and a replay da... |
| `yangkuangou/kaggriculture-crop-calendar-30-day-planner` | engine-and-market-analysis | not an agent: a 30-day crop calendar from the public crop rules: first yield date, watered days in the bonu... |
| `yasutakababa/kaggriculture-late-purchase-v16-submit` | no-strategy-text | n/a (one code cell; the late-purchase strategy was not read) |
| `yhay81/fieldbook-commit-for-three-days` | tape-and-route-replay | tape router: cuts public episodes at shop boundaries, joins candidate plans with similar shops and economic... |
| `yhay81/public-match-history-router-rating-2929-aug-30` | tape-and-route-replay | conditional action-history router: two-shop route selection (checkpoints at step 72 and 144) over fixed 719... |
| `yhay81/replay-public-episode-actions-across-seeds-in-c` | tape-and-route-replay | not a policy: a C++ environment that replays one public player's 719-action tape across seeds (the tape is... |
| `yhay81/shop-router-0908` | tape-and-route-replay | tape router: several complete action tapes, switched at two visible checkpoints |
| `yhay81/shop-router-0909` | tape-and-route-replay | rule-based router in a 234-line main.py (writefile): plan chosen at step 144 from the first two revealed sh... |
| `yhay81/shop-router-0911-simple` | tape-and-route-replay | simplified runtime (23-line writefile): replays a fixed action tape and, after the first two shops are publ... |
| `yhay81/shop-router-0913` | tape-and-route-replay | n/a (near-copy of yhay81/shop-router-0911-simple) (near-copy of `yhay81/shop-router-0911-simple`) |
| `yhay81/six-day-public-state-fieldbook` | tape-and-route-replay | small public-state router around reviewed six-day plans: five 144-turn blocks; chooses the next six-day pla... |
| `yhay81/three-day-shop-router` | compiled-cpp-policy | hybrid: C++ policy (136 lines) with a six-day budget guard, tape and plugin ABI behind a Python bridge (209... |
| `yhay81/when-do-daily-top-episodes-see-your-agent` | evaluation-and-measurement | not an agent: measures when a rising submission enters the daily top-episode sample (28,201 episodes from 5... |
| `yhay81/your-seed-does-not-fix-the-town` | engine-and-market-analysis | engine study, not a policy: town shop unlocks are drawn from the same random stream as weed spawns (one dra... |
| `zaedradwan/notebookbbeb477a58` | heuristic-and-rule-agents | iterated rule-based farm_agent versions (about 12 cells) with my_agent, debug_agent and test_agent helpers |
| `zakariajoudar/rule-based-agent-with-dynamic-ma` | heuristic-and-rule-agents | rule-based winning-strategy agent: phased by game day (early days wheat for fast return, mid game land expa... |
| `zalejohn/submission-py` | heuristic-and-rule-agents | submission agent with worker assignment to the nearest unclaimed tiles, a grid scan, a desired hand count a... |
| `zhincez/a-gate-you-already-beat-cannot-measure-anything` | evaluation-and-measurement | not an agent: an offline gate with two opponents (28/30 and 30/30) cannot measure a change once it has no g... |
| `zhincez/replaying-someone-elses-tape-gets-you-88-percent` | tape-and-route-replay | not an agent: measures how much of a fixed tape's owner's score a replay reproduces, on 26 real replays of... |
| `zhincez/your-score-peaked-because-you-met-weak-opponents` | engine-and-market-analysis | not an agent: a write-up on rating dynamics: four agents, each peaking above 2000 in two hours and then sli... |
| `zihengedie/best-version` | packaging-and-embedded-payload | attributed derivative of the supplied 2802, V43, V46, V47 and V48 agents; no GPU, internet, dataset or trai... |

## Notes on the harvest

- Verdicts: corroborated when the field figure is within 10% of the claim, or the condition holds for at least 90% of seats (for a "never" claim, 1% or fewer); contradicted when it falls outside those bounds; unverifiable when the scan does not measure the quantity or the claimant is not in the 50 teams.
- The harvest log (`notebooks/_index/harvest_log.md`) records each verify pass, and the relevance and extraction audits are in `notebooks/_index/audit_relevance.json` and `notebooks/_index/audit_extraction.json`.
- No notebook was executed. Cells were read as data with `json`. Embedded payloads were not decoded.

