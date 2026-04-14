# 🎵 Music Recommender Simulation

## Project Summary

This repository is a **CLI-first** teaching simulation: a small content-based recommender reads `data/songs.csv`, scores each row against a Python dictionary of listener preferences, and prints an ordered list with numeric scores and plain-language “reason” strings. It mirrors the *shape* of real streaming suggestions—turn tastes plus item features into a ranking—without using real user logs or machine learning training.

---

## How The System Works

### Real platforms vs this simulator

Large services like Spotify or YouTube blend many signals. **Collaborative filtering** learns from *other users’* behavior: co-likes, skips, playlist co-occurrence, and sequence patterns (“people who kept this track also finished that album”). **Content-based filtering** uses *each item’s own attributes*: genre tags, mood labels, tempo, loudness/energy, acoustic instrumentation, or text embeddings from lyrics/metadata. Production systems mix both, plus exploration, freshness rules, and business constraints.

Main **data types** you see in industry: implicit feedback (skips, completes, replays), explicit feedback (likes, saves), social/graph signals (follows, shares), editorial metadata (genre, language), audio features (tempo, key, danceability), and contextual signals (time of day, workout vs focus).

### What this build prioritizes

This version is intentionally **content-only**: it never compares you to neighbors. It prioritizes **exact genre and mood string matches**, then **numeric closeness** on `energy`, then a light **acousticness fit** based on `likes_acoustic`. That is enough to separate “bright pop” from “lofi chill” when the CSV contains both.

**Song object / row features used in code:** `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness` (loaded as typed numbers from CSV).

**User profile / prefs dictionary keys:** `genre`, `mood`, `energy` (target 0–1), and `likes_acoustic` (boolean). The `Song` and `UserProfile` dataclasses in `src/recommender.py` mirror the same idea for tests: `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`.

**Scoring rule vs ranking rule:** the **scoring rule** maps *one* `(user, song)` pair to a number plus reasons. The **ranking rule** applies that judge to *every* song, then orders the list (here: `sorted(..., reverse=True)` and slice the first `k`). You need both because the score is local, but the product question is global (“what are my top picks right now?”).

**Why `sorted()` here:** `list.sort()` mutates the same list in place and returns `None`. `sorted()` builds a **new** ordered list and leaves the original untouched—handy when you still need the unsorted catalog for other prints or tests.

### Algorithm recipe (final)

Discrete matches (weights tunable via `RECOMMENDER_EXPERIMENT`—see Experiments):

- **Genre exact match:** `+2.0` points (halved to `+1.0` in experiment mode).
- **Mood exact match:** `+1.0` point.
- **Energy similarity:** `+ (1 - |song.energy - user.energy|) * w_e`, where `w_e` is `1.0` normally and `2.0` in experiment mode. Closer energies score higher; the user is not “rewarded” for always picking bigger numbers.
- **Acoustic fit:** `+ (1 - |song.acousticness - target|) * 0.5`, where `target` is `0.85` if `likes_acoustic` else `0.20`.

**Bias note:** genre outweighs mood on purpose, so the system can **over-prioritize genre** and keep intense pop (`Gym Hero`) high for listeners who share energy with party tracks even when their textual mood does not match—especially if the dataset lacks rows for a requested mood.

### Data flow (Mermaid)

```mermaid
flowchart LR
  CSV["data/songs.csv"] --> LOAD["load_songs"]
  PREFS["User prefs"] --> SCORE["score_song each row"]
  LOAD --> SCORE
  SCORE --> LIST["Each row: score plus reasons"]
  LIST --> SORT["Sort by score high to low"]
  SORT --> TOP["Take top k"]
  TOP --> CLI["Terminal output"]
```

If the diagram does not render in your Markdown preview, use [Mermaid Live Editor](https://mermaid.live) to validate, or view this file on GitHub (README Mermaid is supported there).

---

## Example taste profile (Phase 2)

```python
DEFAULT_TASTE = {
    "genre": "pop",
    "mood": "happy",
    "energy": 0.85,
    "likes_acoustic": False,
}
```

This profile is wide enough to separate **intense rock** from **chill lofi** (different genre/mood gates), but narrow enough that energy ties still reorder near matches.

---

## Getting Started

### Setup

1. Create a virtual environment (recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # macOS / Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app from the repository root:

   ```bash
   python -m src.main
   ```

   You should see `Loaded songs: 18` followed by several labeled profile blocks.

### Running Tests

```bash
pytest
```

If `pytest` cannot import `src`, run from the repo root (a small `conftest.py` adds the project root to `sys.path`).

---

## Terminal output (for screenshots)

Terminal captures live in `screenshots/` and are embedded below (titles, scores, and reasons visible in each).

| Profile | File |
| --- | --- |
| High-Energy Pop | `screenshots/a.png` |
| Chill Lofi | `screenshots/b.png` |
| Deep Intense Rock | `screenshots/c.png` |
| Adversarial high energy + sad mood | `screenshots/d.png` |
| Adversarial metal + relaxed | `screenshots/e.png` |

![Profile A — High-Energy Pop](screenshots/a.png)

![Profile B — Chill Lofi](screenshots/b.png)

![Profile C — Deep Intense Rock](screenshots/c.png)

![Profile D — Adversarial high energy + sad mood](screenshots/d.png)

![Profile E — Adversarial metal + relaxed](screenshots/e.png)

### Captured CLI excerpt (Profile A)

```
Loading songs from data/songs.csv...
Loaded songs: 18
...
1. Sunrise City — Neon Echo (pop, happy)
   Score: 4.460
   Reasons: genre match (+2.0); mood match (+1.0); energy closeness (+0.97; gap=0.03); acoustic fit (+0.49; target=0.20)
```

---

## Experiments You Tried

**Weight shift (assigned experiment):** export `RECOMMENDER_EXPERIMENT=1` before running Python. Genre match drops from `+2.0` to `+1.0`, and the energy similarity multiplier doubles (`1.0 → 2.0`). On the high-energy pop profile, *Sunrise City* stayed first, but runners-up tightened around energy—showing the knob changes *ordering* among partial matches more than it invents new understanding.

**What was not automated here:** temporarily commenting out the mood check (a second valid experiment). Doing so would lift mood-agnostic ties; if you try it locally, diff the printed top 5 against baseline.

---

## Limitations and Risks

See the full write-up in [**model_card.md**](model_card.md), especially the **Limitations and Bias** and **Evaluation** sections. Short version: tiny catalog, no collaborative signal, and exact string moods mean **missing moods behave like silent bias**.

---

## Reflection pointers

- Detailed pairwise profile commentary: [`reflection.md`](reflection.md)
- Structured model documentation: [`model_card.md`](model_card.md)
