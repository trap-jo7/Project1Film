import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

export const api = axios.create({ baseURL: API, timeout: 45000 });

export async function fetchContext(lat, lon) {
  const params = {};
  if (lat) params.lat = lat;
  if (lon) params.lon = lon;
  const { data } = await api.get("/context", { params });
  return data;
}

export async function fetchRecommendations({ mood, vibe_text, dial, nostalgia, lat, lon, limit = 8 }) {
  const { data } = await api.post("/recommend", { mood, vibe_text, dial, nostalgia, lat, lon, limit });
  return data;
}

export async function fetchMovieDetail(id) {
  const { data } = await api.get(`/movie/${id}`);
  return data;
}

export async function createVibe(payload) {
  const { data } = await api.post("/vibe", payload);
  return data;
}

export async function fetchVibe(id) {
  const { data } = await api.get(`/vibe/${id}`);
  return data;
}
