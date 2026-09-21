"""OpenWeather wrapper + IP geolocation fallback."""
import os
import time
import httpx
from typing import Optional

_cache: dict = {}
_TTL = 60 * 20


def has_key() -> bool:
    return bool(os.environ.get("OPENWEATHER_API_KEY"))


async def _ip_geo(ip: Optional[str]) -> Optional[dict]:
    try:
        async with httpx.AsyncClient(timeout=6.0) as c:
            url = f"http://ip-api.com/json/{ip}" if ip else "http://ip-api.com/json/"
            r = await c.get(url)
            if r.status_code == 200:
                d = r.json()
                if d.get("status") == "success":
                    return {"lat": d["lat"], "lon": d["lon"], "city": d.get("city"), "country": d.get("country")}
    except Exception:
        pass
    return None


def _classify(desc: str, temp: Optional[float]) -> str:
    d = (desc or "").lower()
    if "rain" in d or "drizzle" in d or "shower" in d:
        return "rainy"
    if "storm" in d or "thunder" in d:
        return "stormy"
    if "snow" in d:
        return "snowy"
    if "clear" in d:
        if temp is not None and temp < 5:
            return "cold_clear"
        return "sunny"
    if "cloud" in d or "overcast" in d:
        return "cloudy"
    if "mist" in d or "fog" in d or "haze" in d:
        return "foggy"
    return "mild"


async def get_weather(lat: Optional[float] = None, lon: Optional[float] = None, ip: Optional[str] = None) -> dict:
    key = os.environ.get("OPENWEATHER_API_KEY")
    ck = f"{lat},{lon},{ip}"
    now = time.time()
    if ck in _cache and now - _cache[ck][0] < _TTL:
        return _cache[ck][1]

    city = None
    country = None
    if lat is None or lon is None:
        geo = await _ip_geo(ip)
        if geo:
            lat, lon, city, country = geo["lat"], geo["lon"], geo["city"], geo["country"]

    if not key or lat is None or lon is None:
        result = {"available": False, "condition": "mild", "description": "unknown", "temp": None, "city": city, "country": country}
        _cache[ck] = (now, result)
        return result

    try:
        async with httpx.AsyncClient(timeout=8.0) as c:
            r = await c.get("https://api.openweathermap.org/data/2.5/weather",
                            params={"lat": lat, "lon": lon, "appid": key, "units": "metric"})
            r.raise_for_status()
            d = r.json()
        desc = (d.get("weather") or [{}])[0].get("description", "")
        temp = (d.get("main") or {}).get("temp")
        result = {
            "available": True,
            "condition": _classify(desc, temp),
            "description": desc,
            "temp": temp,
            "city": city or d.get("name"),
            "country": country,
        }
    except Exception:
        result = {"available": False, "condition": "mild", "description": "unknown", "temp": None, "city": city, "country": country}

    _cache[ck] = (now, result)
    return result
