// Track user activity in localStorage to personalize recommendations without login
const KEY = "moodreel_history_v1";
const MAX_TRACK = 40;

function readRaw() {
  try {
    return JSON.parse(localStorage.getItem(KEY) || "{}");
  } catch {
    return {};
  }
}

function writeRaw(data) {
  try {
    localStorage.setItem(KEY, JSON.stringify(data));
  } catch {}
}

export function trackMoodPick(mood) {
  if (!mood) return;
  const h = readRaw();
  h.moods = h.moods || {};
  h.moods[mood] = (h.moods[mood] || 0) + 1;
  writeRaw(h);
}

export function trackMovieOpen(movie) {
  if (!movie) return;
  const h = readRaw();
  h.opened = h.opened || [];
  const entry = { id: movie.id, title: movie.title, genres: movie.genres || [], at: Date.now() };
  h.opened = [entry, ...h.opened.filter((x) => x.id !== movie.id)].slice(0, MAX_TRACK);
  h.genres = h.genres || {};
  (movie.genres || []).forEach((g) => {
    if (!g) return;
    h.genres[g] = (h.genres[g] || 0) + 1;
  });
  writeRaw(h);
}

export function preferences() {
  const h = readRaw();
  const topN = (obj, n) => Object.entries(obj || {}).sort((a, b) => b[1] - a[1]).slice(0, n).map(([k]) => k);
  return {
    preferred_moods: topN(h.moods, 3),
    preferred_genres: topN(h.genres, 4),
    opened_ids: (h.opened || []).map((x) => x.id),
    opened: h.opened || [],
  };
}

export function clearHistory() {
  try { localStorage.removeItem(KEY); } catch {}
}
