from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import uuid
import random
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

from mock_data import MOCK_MOVIES, all_moods
from rules_engine import tmdb_params, filter_and_rank_mock, mark_gems, dial_to_votes, filter_by_keywords, tokenize_query
from llm_curator import curate
from context import cultural_event, time_of_day
import tmdb_client
import weather_client

mongo_url = os.environ["MONGO_URL"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

app = FastAPI(title="MoodReel API")
api = APIRouter(prefix="/api")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("moodreel")


# ------------------ MODELS ------------------
class RecommendRequest(BaseModel):
    mood: Optional[str] = None
    vibe_text: Optional[str] = None
    dial: int = 5
    nostalgia: bool = False
    limit: int = 8
    lat: Optional[float] = None
    lon: Optional[float] = None
    exclude_ids: List[int] = Field(default_factory=list)
    preferred_moods: List[str] = Field(default_factory=list)
    preferred_genres: List[str] = Field(default_factory=list)


class VibeCreate(BaseModel):
    mood: Optional[str] = None
    vibe_text: Optional[str] = None
    dial: int = 5
    nostalgia: bool = False


# ------------------ HELPERS ------------------
def _client_ip(request: Request) -> Optional[str]:
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else None


async def _get_candidates(mood: Optional[str], nostalgia: bool, dial: int, weather: Optional[str],
                          event: Optional[str], limit: int, exclude_ids: list[int] | None = None,
                          preferred_moods: list[str] | None = None,
                          preferred_genres: list[str] | None = None,
                          page_offset: int = 0,
                          vibe_text: Optional[str] = None) -> tuple[list[dict], str, bool]:
    """Returns (candidates, source, keyword_matched). Uses keyword search when vibe_text is present."""
    excl = set(exclude_ids or [])
    tokens = tokenize_query(vibe_text or "")

    if tmdb_client.has_key():
        try:
            movies: list[dict] = []
            if tokens:
                # Prefer TMDB search when we have a free-text query
                try:
                    search_hits = await tmdb_client.search(" ".join(tokens))
                    movies.extend(search_hits)
                except Exception as e:
                    logger.warning(f"TMDB search failed: {e}")
            if not movies:
                p = tmdb_params(mood, nostalgia, dial)
                base_pages = [1, 2] if dial >= 5 else [1]
                pages = [pg + page_offset for pg in base_pages]
                for pg in pages:
                    movies.extend(await tmdb_client.discover(
                        genre_ids=p["genre_ids"], year_from=p["year_from"], year_to=p["year_to"],
                        min_votes=p["min_votes"], max_votes=p["max_votes"], sort_by=p["sort_by"], page=pg,
                    ))
            for m in movies:
                m["moods"] = [mood] if mood else []
            mark_gems(movies)
            movies = [m for m in movies if m["id"] not in excl]
            if not tokens:
                random.shuffle(movies)
            return movies[: max(limit * 2, 16)], "tmdb", bool(tokens)
        except Exception as e:
            logger.warning(f"TMDB failed, falling back: {e}")

    # Mock catalog path
    if tokens:
        kw_hits = filter_by_keywords(MOCK_MOVIES, vibe_text, limit=limit * 3)
        kw_hits = [m for m in kw_hits if m["id"] not in excl]
        if kw_hits:
            mark_gems(kw_hits)
            return kw_hits[: limit * 2], "mock", True

    ranked = filter_and_rank_mock(
        MOCK_MOVIES, mood, weather, event, nostalgia, dial, limit=limit * 2,
        exclude_ids=list(excl), preferred_moods=preferred_moods, preferred_genres=preferred_genres,
    )
    mark_gems(ranked)
    return ranked, "mock", False


# ------------------ ROUTES ------------------
@api.get("/")
async def root():
    return {"service": "MoodReel", "status": "ok"}


@api.get("/health")
async def health():
    return {
        "tmdb": tmdb_client.has_key(),
        "weather": weather_client.has_key(),
        "llm": bool(os.environ.get("EMERGENT_LLM_KEY")),
    }


@api.get("/moods")
async def moods():
    return {"moods": all_moods()}


@api.get("/context")
async def context(request: Request, lat: Optional[float] = None, lon: Optional[float] = None):
    now = datetime.now(timezone.utc)
    ip = _client_ip(request)
    weather = await weather_client.get_weather(lat=lat, lon=lon, ip=ip)
    tod = time_of_day(now)
    event = cultural_event(now)
    trending_titles: list[str] = []
    if tmdb_client.has_key():
        try:
            tr = await tmdb_client.trending_week()
            trending_titles = [t["title"] for t in tr[:5] if t.get("title")]
        except Exception:
            pass
    return {
        "weather": weather,
        "time_of_day": tod,
        "event": event,
        "trending_titles": trending_titles,
        "now": now.isoformat(),
    }


@api.post("/recommend")
async def recommend(req: RecommendRequest, request: Request):
    now = datetime.now(timezone.utc)
    tod = time_of_day(now)
    event = cultural_event(now)
    ip = _client_ip(request)
    weather = await weather_client.get_weather(lat=req.lat, lon=req.lon, ip=ip)
    limit = max(4, min(12, req.limit))
    page_offset = min(3, max(0, len(req.exclude_ids) // 8))
    candidates, source, kw_matched = await _get_candidates(
        req.mood, req.nostalgia, req.dial, weather.get("condition"), event, limit,
        exclude_ids=req.exclude_ids, preferred_moods=req.preferred_moods,
        preferred_genres=req.preferred_genres, page_offset=page_offset,
        vibe_text=req.vibe_text,
    )
    picks = await curate(
        candidates=candidates, mood=req.mood, free_text=req.vibe_text, dial=req.dial,
        nostalgia=req.nostalgia, weather=weather.get("condition"), event=event, tod=tod, want_n=limit,
    )
    return {
        "picks": picks,
        "source": source,
        "keyword_matched": kw_matched,
        "no_matches": bool(req.vibe_text) and len(picks) == 0,
        "context": {"weather": weather, "time_of_day": tod, "event": event},
    }


@api.get("/movie/{tmdb_id}")
async def movie_detail(tmdb_id: int):
    if tmdb_client.has_key():
        try:
            return await tmdb_client.details(tmdb_id)
        except Exception as e:
            logger.warning(f"TMDB detail failed: {e}")
    m = next((x for x in MOCK_MOVIES if x["id"] == tmdb_id), None)
    if not m:
        raise HTTPException(404, "movie not found")
    return {
        **m, "trailer": None, "cast": [], "director": None, "providers": [],
    }


@api.post("/vibe")
async def create_vibe(v: VibeCreate):
    vid = uuid.uuid4().hex[:10]
    doc = {
        "id": vid,
        "mood": v.mood,
        "vibe_text": v.vibe_text,
        "dial": v.dial,
        "nostalgia": v.nostalgia,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.vibes.insert_one(doc)
    return {"id": vid, "url_suffix": f"?v={vid}"}


@api.get("/vibe/{vid}")
async def get_vibe(vid: str):
    doc = await db.vibes.find_one({"id": vid}, {"_id": 0})
    if not doc:
        raise HTTPException(404, "vibe not found")
    return doc


app.include_router(api)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
async def _shutdown():
    client.close()
