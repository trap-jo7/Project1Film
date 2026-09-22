"""Rules-based candidate filter. Maps mood + weather + time + dial to TMDB parameters
and scores/filters our mock catalog when TMDB is unavailable."""
import re
from typing import Optional

MOOD_GENRE_TMDB = {
    "nostalgic": [12, 18, 10751, 10402],           # Adventure, Drama, Family, Music
    "cozy":      [16, 35, 10751, 10749],           # Animation, Comedy, Family, Romance
    "chaotic":   [28, 53, 80, 878],                # Action, Thriller, Crime, Sci-Fi
    "melancholy":[18, 10749, 36],                  # Drama, Romance, History
    "euphoric":  [35, 10402, 12, 16],              # Comedy, Music, Adventure, Animation
    "weird":     [14, 27, 878, 9648],              # Fantasy, Horror, Sci-Fi, Mystery
    "romantic":  [10749, 18, 35],                  # Romance, Drama, Comedy
    "angry":     [28, 80, 53, 27],                 # Action, Crime, Thriller, Horror
}

MOOD_YEAR_WINDOW = {
    "nostalgic": (1970, 1999),
    "cozy":      (1985, 2024),
    "chaotic":   (1990, 2024),
    "melancholy":(1960, 2024),
    "euphoric":  (1980, 2024),
    "weird":     (1960, 2024),
    "romantic":  (1970, 2024),
    "angry":     (1990, 2024),
}

WEATHER_BOOSTS = {
    "rainy":     ["cozy", "melancholy", "romantic"],
    "stormy":    ["chaotic", "angry", "weird"],
    "snowy":     ["cozy", "nostalgic", "romantic"],
    "sunny":     ["euphoric", "chaotic"],
    "cloudy":    ["melancholy", "weird"],
    "foggy":     ["weird", "melancholy"],
    "cold_clear":["melancholy", "cozy"],
    "mild":      ["cozy", "euphoric"],
}

EVENT_BOOSTS = {
    "spooky_season":     ["weird", "angry"],
    "holiday_season":    ["cozy", "nostalgic", "romantic"],
    "cozy_winter":       ["cozy", "melancholy"],
    "valentines":        ["romantic", "melancholy"],
    "awards_season":     ["melancholy", "weird"],
    "summer_blockbuster":["chaotic", "euphoric"],
    "spring_indie":      ["weird", "melancholy"],
}


def dial_to_votes(dial: int) -> tuple[int, Optional[int]]:
    """dial: 1 (mainstream) .. 10 (deep cut). Returns (min_votes, max_votes)."""
    d = max(1, min(10, int(dial)))
    if d <= 2:
        return 5000, None
    if d <= 4:
        return 2000, None
    if d <= 6:
        return 500, 5000
    if d <= 8:
        return 150, 2000
    return 30, 800


def tmdb_params(mood: Optional[str], nostalgia: bool, dial: int) -> dict:
    m = mood or "cozy"
    genres = MOOD_GENRE_TMDB.get(m, [18])
    year_from, year_to = MOOD_YEAR_WINDOW.get(m, (1970, 2024))
    if nostalgia:
        year_from, year_to = 1970, 1999
    min_votes, max_votes = dial_to_votes(dial)
    d = max(1, min(10, dial))
    if d <= 3:
        sort_by = "popularity.desc"
    elif d <= 6:
        sort_by = "vote_average.desc"
    else:
        sort_by = "vote_average.desc"
    return {
        "genre_ids": genres,
        "year_from": year_from,
        "year_to": year_to,
        "min_votes": min_votes,
        "max_votes": max_votes,
        "sort_by": sort_by,
    }


def keyword_score(m: dict, tokens: list[str]) -> float:
    """Return keyword match score for a movie. 0 = no match."""
    if not tokens:
        return 0.0
    haystacks = [
        (m.get("title") or "").lower(),
        (m.get("overview") or "").lower(),
        " ".join((m.get("genres") or [])).lower(),
        " ".join((m.get("moods") or [])).lower(),
        " ".join((m.get("keywords") or [])).lower(),
    ]
    hay = " || ".join(haystacks)
    score = 0.0
    for tok in tokens:
        if not tok:
            continue
        t = tok.lower().strip()
        if len(t) < 3:
            continue
        if t in haystacks[0]:
            score += 5.0
        if t in haystacks[4]:  # keywords field is the highest signal
            score += 4.0
        if t in haystacks[2] or t in haystacks[3]:
            score += 2.0
        if t in haystacks[1]:
            score += 1.5
        # crude plural / stem: "vampires" -> "vampire"
        if t.endswith("s") and t[:-1] in hay and t not in hay:
            score += 2.0
    return score


_STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "for", "with", "to", "of", "in", "on", "at",
    "movie", "movies", "film", "films", "give", "me", "want", "watch", "something",
    "please", "im", "i'm", "feeling", "feel", "kind", "type", "some", "any",
}


def tokenize_query(q: str) -> list[str]:
    if not q:
        return []
    q = q.lower()
    parts = re.findall(r"[a-z][a-z'-]+", q)
    return [p for p in parts if p not in _STOPWORDS and len(p) >= 3]


def filter_by_keywords(catalog: list[dict], query: str, limit: int = 24) -> list[dict]:
    tokens = tokenize_query(query)
    if not tokens:
        return []
    scored = [(keyword_score(m, tokens), m) for m in catalog]
    scored = [(s, m) for s, m in scored if s > 0]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [m for _, m in scored[:limit]]


def score_movie(m: dict, mood: Optional[str], weather: Optional[str], event: Optional[str],
                nostalgia: bool, dial: int, preferred_moods: Optional[list[str]] = None,
                preferred_genres: Optional[list[str]] = None) -> float:
    score = 0.0
    if mood and mood in (m.get("moods") or []):
        score += 3.0
    if weather:
        for boost_mood in WEATHER_BOOSTS.get(weather, []):
            if boost_mood in (m.get("moods") or []):
                score += 0.8
    if event:
        for boost_mood in EVENT_BOOSTS.get(event, []):
            if boost_mood in (m.get("moods") or []):
                score += 0.6
    if nostalgia and 1970 <= (m.get("year") or 2000) <= 1999:
        score += 1.5
    # Personalization: reward preferred moods & genres from user history
    if preferred_moods:
        for pm in preferred_moods:
            if pm in (m.get("moods") or []):
                score += 1.1
    if preferred_genres:
        movie_genres = set(g.lower() for g in (m.get("genres") or []) if g)
        for pg in preferred_genres:
            if pg.lower() in movie_genres:
                score += 0.9
    # Dial: high dial rewards low popularity, low dial rewards popularity
    pop = m.get("popularity") or 0
    if dial >= 7:
        score += max(0, (60 - pop)) / 60.0
        if m.get("gem"):
            score += 1.2
    elif dial <= 3:
        score += min(pop, 100) / 100.0
    score += (m.get("rating") or 0) / 20.0
    return score


def filter_and_rank_mock(catalog: list[dict], mood: Optional[str], weather: Optional[str],
                         event: Optional[str], nostalgia: bool, dial: int, limit: int = 8,
                         exclude_ids: Optional[list[int]] = None,
                         preferred_moods: Optional[list[str]] = None,
                         preferred_genres: Optional[list[str]] = None) -> list[dict]:
    excl = set(exclude_ids or [])
    filtered = [m for m in catalog if m["id"] not in excl]
    scored = [(score_movie(m, mood, weather, event, nostalgia, dial, preferred_moods, preferred_genres), m)
              for m in filtered]
    scored.sort(key=lambda x: x[0], reverse=True)
    picks = [m for _, m in scored[: limit * 2]]
    if not picks:
        return filtered[:limit] or catalog[:limit]
    seen = set()
    out = []
    for m in picks:
        if m["id"] in seen:
            continue
        seen.add(m["id"])
        out.append(m)
        if len(out) >= limit:
            break
    return out


def mark_gems(movies: list[dict]) -> list[dict]:
    for m in movies:
        if "gem" not in m:
            vc = m.get("vote_count") or 0
            pop = m.get("popularity") or 0
            m["gem"] = vc < 3000 and pop < 30
    return movies
