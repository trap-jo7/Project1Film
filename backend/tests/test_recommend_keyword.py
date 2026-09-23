"""Backend tests focused on keyword-search bug fix for /api/recommend."""
import os
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://reel-vibe-1.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"


@pytest.fixture(scope="module")
def s():
    sess = requests.Session()
    sess.headers.update({"Content-Type": "application/json"})
    return sess


def _post(s, payload):
    r = s.post(f"{API}/recommend", json=payload, timeout=60)
    assert r.status_code == 200, f"status {r.status_code} body {r.text}"
    return r.json()


def test_health(s):
    r = s.get(f"{API}/health", timeout=15)
    assert r.status_code == 200
    d = r.json()
    assert d["llm"] is True
    assert d["tmdb"] is False


def test_vampire_keyword(s):
    d = _post(s, {"vibe_text": "vampire movie", "dial": 5, "limit": 8})
    assert d["keyword_matched"] is True
    picks = d["picks"]
    assert len(picks) > 0
    text = " ".join((p.get("title", "") + " " + (p.get("overview") or "")) for p in picks).lower()
    assert "vampire" in text
    titles = [p["title"] for p in picks]
    assert any("vampire" in t.lower() for t in titles), f"Interview with the Vampire missing: {titles}"


def test_space_opera_keyword(s):
    d = _post(s, {"vibe_text": "space opera", "dial": 5, "limit": 8})
    assert d["keyword_matched"] is True
    titles = [p["title"].lower() for p in d["picks"]]
    assert any(t in titles for t in ["star wars", "dune", "2001: a space odyssey", "blade runner", "blade runner 2049"]), titles


def test_superhero_keyword(s):
    d = _post(s, {"vibe_text": "superhero", "dial": 5, "limit": 8})
    assert d["keyword_matched"] is True
    titles = [p["title"].lower() for p in d["picks"]]
    expected = {"batman begins", "deadpool", "logan", "big hero 6", "the dark knight rises", "the dark knight"}
    assert any(t in expected for t in titles), titles


def test_horror_scary_keyword(s):
    d = _post(s, {"vibe_text": "horror scary", "dial": 5, "limit": 8})
    assert d["keyword_matched"] is True
    titles = [p["title"].lower() for p in d["picks"]]
    expected = {"the shining", "the thing", "the black phone", "the neon demon", "interview with the vampire"}
    assert any(t in expected for t in titles), titles


def test_nonsense_query(s):
    d = _post(s, {"vibe_text": "unicorn ninja underwater tap dance", "dial": 5, "limit": 8})
    # Either no_matches=true with empty picks, OR very small non-generic set
    picks = d["picks"]
    titles = [p["title"].lower() for p in picks]
    unrelated = {"amélie", "the godfather", "forrest gump", "pulp fiction"}
    assert not any(t in unrelated for t in titles), f"Unrelated top picks returned: {titles}"
    if len(picks) == 0:
        assert d["no_matches"] is True
    else:
        assert len(picks) <= 4, f"Too many picks for nonsense: {titles}"


def test_mood_only_still_works(s):
    d = _post(s, {"vibe_text": "", "mood": "cozy", "dial": 5, "limit": 8})
    assert d["keyword_matched"] is False
    assert 6 <= len(d["picks"]) <= 8


def test_default_landing(s):
    d = _post(s, {"vibe_text": "", "mood": None, "dial": 5, "limit": 8})
    assert d["keyword_matched"] is False
    assert len(d["picks"]) == 8


def test_see_more_exclude_ids(s):
    d1 = _post(s, {"vibe_text": "", "mood": "cozy", "dial": 5, "limit": 8})
    first_ids = [p["id"] for p in d1["picks"]]
    d2 = _post(s, {"vibe_text": "", "mood": "cozy", "dial": 5, "limit": 8, "exclude_ids": first_ids})
    second_ids = [p["id"] for p in d2["picks"]]
    overlap = set(first_ids) & set(second_ids)
    assert not overlap, f"Overlap: {overlap}"


def test_posters_are_tmdb_cdn(s):
    d = _post(s, {"vibe_text": "", "mood": None, "dial": 5, "limit": 8})
    for p in d["picks"]:
        assert p.get("poster", "").startswith("https://image.tmdb.org"), p
