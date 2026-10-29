import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

# Scoring weights. Experiment: energy doubled (1.5 -> 3.0), genre halved (1.5 -> 0.75)
GENRE_WEIGHT = 0.75
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 3.0
VALENCE_WEIGHT = 0.5
ACOUSTIC_WEIGHT = 0.5
MAX_SCORE = GENRE_WEIGHT + MOOD_WEIGHT + ENERGY_WEIGHT + VALENCE_WEIGHT + ACOUSTIC_WEIGHT

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into dicts, converting numeric fields to int/float."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song out of MAX_SCORE against user preferences and return (score, reasons)."""
    score = 0.0
    reasons = []

    # Exact matches: full weight or nothing
    if song["genre"] == user_prefs["favorite_genre"]:
        score += GENRE_WEIGHT
        reasons.append(f"genre match: {song['genre']} (+{GENRE_WEIGHT})")
    if song["mood"] == user_prefs["favorite_mood"]:
        score += MOOD_WEIGHT
        reasons.append(f"mood match: {song['mood']} (+{MOOD_WEIGHT})")

    # Closeness checks: closer to target = more points, up to the full weight
    acoustic_target = 0.8 if user_prefs["likes_acoustic"] else 0.2
    closeness_checks = [
        ("energy", user_prefs["target_energy"], ENERGY_WEIGHT),
        ("valence", user_prefs.get("target_valence", 0.5), VALENCE_WEIGHT),
        ("acousticness", acoustic_target, ACOUSTIC_WEIGHT),
    ]
    for feature, target, weight in closeness_checks:
        points = weight * (1 - abs(song[feature] - target))
        score += points
        reasons.append(f"{feature} {song[feature]:.2f} vs target {target:.2f} (+{points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs as (song, score, explanation), highest score first."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    top_k = sorted(scored, key=lambda item: item[1], reverse=True)[:k]
    return [(song, score, "; ".join(reasons)) for song, score, reasons in top_k]
