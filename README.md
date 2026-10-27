# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

A content-based recommender: it matches each song's own features to the user's stated taste.

```
UserProfile ─┐
             ├─► score each song ─► sort high→low ─► top k + reasons
songs.csv ───┘
```

- **Song features used:** genre, mood, energy, valence, acousticness. Tempo and danceability are skipped because they move almost exactly with energy in this data.
- **UserProfile stores:** favorite genre, favorite mood, target energy (0–1), target valence (0–1, default 0.5), likes acoustic (yes/no).
- **Scoring (max 5 points):** exact matches and closeness checks are worth 2.5 each, so no single feature dominates.
  - Genre match: +1.5
  - Mood match: +1.0
  - Energy: up to +1.5, using `1 − |song − target|`, so the *closest* song wins, not the highest
  - Valence: up to +0.5, same closeness rule
  - Acousticness: up to +0.5, same closeness rule (target 0.8 if the user likes acoustic, 0.2 if not)
- **Choosing songs:** sort all songs by score, return the top k (default 5), each with a short reason like "genre match (+1.5)".

**Expected biases:**

- Most genres have only one song, so many users get at most one genre match. Lofi (3 songs) and chill (3 songs) fans get the most full matches.
- Matching is exact text: "indie pop" ≠ "pop" and "relaxed" ≠ "chill", so close fits lose points over a label.
- Mid-range songs are never far from any target, so they score decently for everyone, while extreme songs (classical, metal) only rank for users who want that extreme.
- The yes/no acoustic setting and the 0.5 valence default push results toward songs near those values.



---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
==================================================
 Top Recommendations
==================================================

1. Midnight Coding by LoRoom
   Score: 4.89 / 5.00
     - genre match: lofi (+1.5)
     - mood match: chill (+1.0)
     - energy 0.42 vs target 0.40 (+1.47)
     - valence 0.56 vs target 0.50 (+0.47)
     - acousticness 0.71 vs target 0.80 (+0.45)

2. Library Rain by Paper Lanterns
   Score: 4.84 / 5.00
     - genre match: lofi (+1.5)
     - mood match: chill (+1.0)
     - energy 0.35 vs target 0.40 (+1.42)
     - valence 0.60 vs target 0.50 (+0.45)
     - acousticness 0.86 vs target 0.80 (+0.47)

3. Focus Flow by LoRoom
   Score: 3.95 / 5.00
     - genre match: lofi (+1.5)
     - energy 0.40 vs target 0.40 (+1.50)
     - valence 0.59 vs target 0.50 (+0.46)
     - acousticness 0.78 vs target 0.80 (+0.49)

4. Spacewalk Thoughts by Orbit Bloom
   Score: 3.19 / 5.00
     - mood match: chill (+1.0)
     - energy 0.28 vs target 0.40 (+1.32)
     - valence 0.65 vs target 0.50 (+0.42)
     - acousticness 0.92 vs target 0.80 (+0.44)

5. Coffee Shop Stories by Slow Stereo
   Score: 2.31 / 5.00
     - energy 0.37 vs target 0.40 (+1.46)
     - valence 0.71 vs target 0.50 (+0.40)
     - acousticness 0.89 vs target 0.80 (+0.46)

==================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



