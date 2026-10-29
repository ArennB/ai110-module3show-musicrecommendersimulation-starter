"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import MAX_SCORE, load_songs, recommend_songs


USER_PROFILES = {
    # Upbeat, danceable, positive mainstream music
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "target_valence": 0.85,
        "likes_acoustic": False,
    },
    # A late-night study listener who wants calm, acoustic background music
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "target_valence": 0.60,
        "likes_acoustic": True,
    },
    # Loud, driving, darker-sounding guitar music
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "target_valence": 0.40,
        "likes_acoustic": False,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for profile_name, user_prefs in USER_PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\n" + "=" * 50)
        print(f" Top Recommendations: {profile_name}")
        print("=" * 50)
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n{rank}. {song['title']} by {song['artist']}")
            print(f"   Score: {score:.2f} / {MAX_SCORE:.2f}")
            for reason in explanation.split("; "):
                print(f"     - {reason}")
        print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
