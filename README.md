# Kaggriculture

Our entry to the Kaggle simulation competition [Kaggriculture](https://www.kaggle.com/competitions/kaggriculture)
(2026-07-29 to 2026-09-30). Two players run farms on a shared market for a 720-turn season. The final
ranking is a Bradley-Terry tournament over the games played after the deadline.

**Start with [docs/RECORD.md](docs/RECORD.md)**: the outcome, the engine facts, the measurements, what
did not work, and the open questions.

## What reached the ladder

Our two final submissions replay a decoded action tape of another team's policy. The tape is a
majority vote over that team's own traces, and it was validated for fidelity against the donor's own
opponents (0.12% median bank error) before use. On top of it sit closed-loop overlays of our own: tile
recovery for one slot, and H2 tail-liquidation for the other.

The copy is faithful, and it still lost about 1,000 rating points to its donor. We never found the
reason. The heuristic agent in `agent/` is our readable reference and our research platform. It is not
what was submitted.

## Repository layout

| Path | Contents |
|---|---|
| `main.py`, `agent/` | The heuristic agent (planner, scheduler, executor, receipts) and its guard tests. `main.py` is the Kaggle loader entry point, and `agent` must stay the last callable it imports. |
| `analysis/build_tape_overlay_submission.py` | Builds the self-contained submission for the two final slots: `--mode augment` (tile recovery) and `--mode liquidate` (H2). |
| `analysis/build_reconstruction_submission.py`, `build_tape_submission.py` | The majority-vote route and the open-loop tape it descends from. |
| `analysis/s6_step1_reconstruct.py` | Produces the reconstruction artefact the builders read. |
| `analysis/s10_replay_bench.py` | Instrument A: replays recorded ladder episodes with our action stream substituted. |
| `analysis/archive_sync.py`, `analysis/b1_top_profile.py` | The kaggle CLI collector, and the top-K profile of the current leaderboard. |
| `harness/` | Local play, paired comparisons, Bradley-Terry ladder, metrics, checkpoint fingerprints. |
| `engine_reference/` | Read-only byte mirror of `kaggle-environments==1.32.7`. Never imported. |
| `checkpoints/*/manifest.json`, `gates/*/results.json` | Fingerprints of accepted baselines and the aggregate gate results. Agent packages and replays are not tracked. |
| `tests/` | Engine-fact tripwires, agent guards, harness and instrument tests. |
| `docs/RECORD.md` | The record. |

## Setup and checks

```bash
pip install -r requirements-dev.txt
PYTHONPATH=. pytest tests/        # what CI runs on every push
```

Some tests read gitignored replays. They skip in a fresh clone, which is expected.

Play the agent against a built-in opponent (`pass`, `random`, `starter`) or another agent file:

```bash
python -m harness.cli play main.py starter --steps 720
python -m harness.cli compare main.py starter --seed-set dev
```

Build the two final submissions. The builders need the local replays and derived artefacts, which
are not in the repo (see section 11 of the record):

```bash
python analysis/build_tape_overlay_submission.py --team ReCurSiON --mode augment --package
python analysis/build_tape_overlay_submission.py --team ReCurSiON --mode liquidate --package
```

## Engine

Pinned to `kaggle-environments==1.32.7`. Where the documentation and the engine disagree, the engine
wins. The verified deviations are in section 3 of the record. Each one is either a tripwire test or an
official answer from the organisers. To check for an engine change without installing it, diff the
package's `.py` and `.json` against `engine_reference/`.

## Data

Replays, derived data, gate replays and packaged submissions are gitignored. They are game data and are
not redistributed. Competitor notebook source was never executed or extracted.

## Licence

[MIT](LICENSE)
