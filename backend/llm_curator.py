"""Claude Haiku 4.5 curator: picks final 6-8 and writes a one-line 'why now' blurb."""
import os
import json
import uuid
import re
from typing import Optional

from emergentintegrations.llm.chat import LlmChat, UserMessage


SYSTEM = """You are MoodReel's cinema tastemaker. You curate a short list of movies for the user's exact vibe *right now* and write one crackling sentence per pick explaining why THIS movie fits THIS moment.

Rules:
- Output STRICT JSON only. No preamble, no markdown fences.
- Pick 6 to 8 movies from the candidates provided. Do not invent movies.
- If the user provided FREE_TEXT (a specific request like "vampire movie", "space heist", "underwater horror"), the FREE_TEXT is the STRONGEST signal — filter aggressively so every pick clearly matches those keywords/theme. Drop candidates that don't fit even if they match the mood.
- If NO candidate matches the FREE_TEXT well, return {"picks": [], "reason": "no matches"} so the app can tell the user honestly.
- Each blurb: 1 sentence, 12-24 words, second-person ("you"), specific and evocative. No cliches like "must watch" or "masterpiece".
- Slightly favor hidden gems when the user's obscure dial is high.
- Never mention the dial, the weather, or the mood by name inside the blurb.

Schema:
{"picks": [{"id": <int>, "blurb": "<string>"}], "reason": "<optional string when picks is empty>"}"""


def _fallback_blurb(m: dict, mood: Optional[str]) -> str:
    hooks = {
        "nostalgic": "A warm, grainy time capsule that still lands square in the chest.",
        "cozy": "A soft, small-hours watch that treats you kindly without going saccharine.",
        "chaotic": "Twitchy, propulsive, and unwilling to sit still — the perfect nerve-jangler.",
        "melancholy": "A quiet ache of a film that lets loneliness be beautiful for a while.",
        "euphoric": "A shot of pure movie-serotonin that leaves you buzzing on the walk home.",
        "weird": "A slippery, dreamlike oddity that rewires how you look at ordinary rooms.",
        "romantic": "A love story with real bruises and real breath — no gauze, no lies.",
        "angry": "A clenched-fist watch that channels rage into something sharp and cinematic.",
    }
    base = hooks.get(mood or "cozy", "A well-shot, well-earned watch that fits the hour perfectly.")
    return f"{m.get('title')} ({m.get('year')}): {base}"


def _extract_json(text: str) -> dict:
    if not text:
        return {}
    text = text.strip()
    text = re.sub(r"^```(?:json)?", "", text).strip()
    text = re.sub(r"```$", "", text).strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            return {}
    return {}


async def curate(candidates: list[dict], mood: Optional[str], free_text: Optional[str],
                 dial: int, nostalgia: bool, weather: Optional[str], event: Optional[str],
                 tod: str, want_n: int = 8) -> list[dict]:
    key = os.environ.get("EMERGENT_LLM_KEY")
    slim = [
        {
            "id": c["id"],
            "title": c["title"],
            "year": c["year"],
            "genres": c.get("genres", [])[:3],
            "rating": c.get("rating"),
            "gem": c.get("gem", False),
            "keywords": c.get("keywords", []),
            "overview": (c.get("overview") or "")[:220],
        }
        for c in candidates[:24]
    ]

    if not key or not candidates:
        picks = candidates[:want_n]
        for p in picks:
            p["blurb"] = _fallback_blurb(p, mood)
        return picks

    user_prompt = (
        f"MOOD: {mood or 'unspecified'}\n"
        f"FREE_TEXT: {free_text or 'none'}\n"
        f"DIAL (1=mainstream, 10=obscure): {dial}\n"
        f"NOSTALGIA_MODE: {nostalgia}\n"
        f"WEATHER: {weather or 'unknown'}\n"
        f"CULTURAL_EVENT: {event or 'none'}\n"
        f"TIME_OF_DAY: {tod}\n"
        f"WANT_N: {want_n}\n\n"
        f"CANDIDATES:\n{json.dumps(slim, ensure_ascii=False)}\n\n"
        "Return the JSON now."
    )

    try:
        chat = LlmChat(
            api_key=key,
            session_id=f"moodreel-{uuid.uuid4().hex[:8]}",
            system_message=SYSTEM,
        ).with_model("anthropic", "claude-haiku-4-5-20251001")
        reply = await chat.send_message(UserMessage(text=user_prompt))
        data = _extract_json(reply)
        picks_meta = data.get("picks") or []
        by_id = {c["id"]: c for c in candidates}
        out = []
        for p in picks_meta:
            m = by_id.get(p.get("id"))
            if m:
                mm = {**m, "blurb": (p.get("blurb") or _fallback_blurb(m, mood)).strip()}
                out.append(mm)
        if not out:
            out = [{**c, "blurb": _fallback_blurb(c, mood)} for c in candidates[:want_n]]
        return out[:want_n]
    except Exception:
        picks = candidates[:want_n]
        for p in picks:
            p["blurb"] = _fallback_blurb(p, mood)
        return picks
