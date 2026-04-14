"""
Command line runner for the Music Recommender Simulation.

Run: python -m src.main
"""

from src.recommender import load_songs, recommend_songs


def _print_recommendations(title: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)
    print(f"Profile: {user_prefs}")
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print(f"\nTop {k} recommendations:\n")
    for i, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"{i}. {song['title']} — {song['artist']} ({song['genre']}, {song['mood']})")
        print(f"   Score: {score:.3f}")
        print(f"   Reasons: {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = [
        (
            "Profile A — High-Energy Pop",
            {"genre": "pop", "mood": "happy", "energy": 0.85, "likes_acoustic": False},
        ),
        (
            "Profile B — Chill Lofi",
            {"genre": "lofi", "mood": "chill", "energy": 0.38, "likes_acoustic": True},
        ),
        (
            "Profile C — Deep Intense Rock",
            {"genre": "rock", "mood": "intense", "energy": 0.92, "likes_acoustic": False},
        ),
        (
            "Profile D — Adversarial (high energy + sad mood)",
            {"genre": "pop", "mood": "sad", "energy": 0.95, "likes_acoustic": False},
        ),
        (
            "Profile E — Adversarial (conflicting: chill genre hint + metal taste)",
            {"genre": "metal", "mood": "relaxed", "energy": 0.5, "likes_acoustic": True},
        ),
    ]

    for title, prefs in profiles:
        _print_recommendations(title, prefs, songs, k=5)


if __name__ == "__main__":
    main()
