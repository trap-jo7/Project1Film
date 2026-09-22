"""TMDB v3 API wrapper with in-memory cache and Mongo persistence."""
import os
import time
import httpx
from typing import Optional

TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"
TMDB_BACKDROP = "https://image.tmdb.org/t/p/w1280"

_cache: dict = {}
_TTL = 60 * 30  # 30 min


def _get_key() -> Optional[str]:
    return os.environ.get("TMDB_API_KEY") or None


def has_key() -> bool:
    return bool(_get_key())


async def _get(path: str, params: dict) -> dict:
    key = _get_key()
    if not key:
        raise RuntimeError("TMDB_API_KEY missing")
    params = {**params, "api_key": key}
    ck = path + "?" + "&".join(f"{k}={v}" for k, v in sorted(params.items()) if k != "api_key")
    now = time.time()
    if ck in _cache and now - _cache[ck][0] < _TTL:
        return _cache[ck][1]
    async with httpx.AsyncClient(timeout=15.0) as client:
        r = await client.get(f"{TMDB_BASE}{path}", params=params)
        r.raise_for_status()
        data = r.json()
    _cache[ck] = (now, data)
    return data


GENRE_MAP = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy", 80: "Crime",
    99: "Documentary", 18: "Drama", 10751: "Family", 14: "Fantasy", 36: "History",
    27: "Horror", 10402: "Music", 9648: "Mystery", 10749: "Romance", 878: "Sci-Fi",
    10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western",
}


def _shape(m: dict) -> dict:
    year = None
    if m.get("release_date"):
        try:
            year = int(m["release_date"][:4])
        except Exception:
            year = None
    return {
        "id": m.get("id"),
        "title": m.get("title") or m.get("name"),
        "year": year,
        "runtime": m.get("runtime"),
        "rating": round(m.get("vote_average") or 0, 1),
        "vote_count": m.get("vote_count") or 0,
        "genres": [GENRE_MAP.get(g, "") for g in (m.get("genre_ids") or [])] or [g["name"] for g in (m.get("genres") or [])],
        "moods": [],
        "poster": f"{TMDB_IMG}{m['poster_path']}" if m.get("poster_path") else None,
        "backdrop": f"{TMDB_BACKDROP}{m['backdrop_path']}" if m.get("backdrop_path") else None,
        "overview": m.get("overview") or "",
        "popularity": m.get("popularity") or 0,
    }


async def discover(genre_ids: list[int], year_from: int, year_to: int,
                   min_votes: int, max_votes: Optional[int], sort_by: str, page: int = 1) -> list[dict]:
    params = {
        "with_genres": ",".join(str(g) for g in genre_ids) if genre_ids else "",
        "primary_release_date.gte": f"{year_from}-01-01",
        "primary_release_date.lte": f"{year_to}-12-31",
        "vote_count.gte": min_votes,
        "sort_by": sort_by,
        "language": "en-US",
        "include_adult": "false",
        "page": page,
    }
    if max_votes is not None:
        params["vote_count.lte"] = max_votes
    data = await _get("/discover/movie", {k: v for k, v in params.items() if v not in (None, "")})
    return [_shape(m) for m in data.get("results", [])]


async def trending_week() -> list[dict]:
    data = await _get("/trending/movie/week", {"language": "en-US"})
    return [_shape(m) for m in data.get("results", [])]


async def search(query: str, page: int = 1) -> list[dict]:
    data = await _get("/search/movie", {"query": query, "language": "en-US",
                                        "include_adult": "false", "page": page})
    return [_shape(m) for m in data.get("results", []) if m.get("poster_path")]


async def details(movie_id: int) -> dict:
    data = await _get(f"/movie/{movie_id}", {"append_to_response": "videos,credits,watch/providers", "language": "en-US"})
    shaped = _shape(data)
    trailer = None
    for v in (data.get("videos") or {}).get("results", []):
        if v.get("site") == "YouTube" and v.get("type") == "Trailer":
            trailer = f"https://www.youtube.com/watch?v={v['key']}"
            break
    shaped["trailer"] = trailer
    cast = [{"name": c["name"], "character": c.get("character", "")} for c in (data.get("credits") or {}).get("cast", [])[:6]]
    shaped["cast"] = cast
    director = next((c["name"] for c in (data.get("credits") or {}).get("crew", []) if c.get("job") == "Director"), None)
    shaped["director"] = director
    providers = ((data.get("watch/providers") or {}).get("results") or {}).get("US") or {}
    flatrate = [p["provider_name"] for p in providers.get("flatrate", [])]
    shaped["providers"] = flatrate
    return shaped
