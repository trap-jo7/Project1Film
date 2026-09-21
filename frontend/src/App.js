import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Toaster, toast } from "sonner";
import { Sparkles, RefreshCw, Share2, Dice5, Film } from "lucide-react";

import BackgroundFX from "@/components/BackgroundFX";
import CursorGlow from "@/components/CursorGlow";
import MoodChips from "@/components/MoodChips";
import ContextBadge from "@/components/ContextBadge";
import VibeControls from "@/components/VibeControls";
import MovieCard from "@/components/MovieCard";
import MovieModal from "@/components/MovieModal";
import { fetchContext, fetchRecommendations, createVibe, fetchVibe } from "@/lib/api";

function readVibeFromUrl() {
  const p = new URLSearchParams(window.location.search);
  return {
    v: p.get("v"),
    mood: p.get("mood"),
    dial: p.get("dial") ? parseInt(p.get("dial"), 10) : null,
    text: p.get("text") || "",
    nost: p.get("nost") === "1",
  };
}

export default function App() {
  const initialUrl = useMemo(readVibeFromUrl, []);
  const [context, setContext] = useState(null);
  const [mood, setMood] = useState(initialUrl.mood || null);
  const [dial, setDial] = useState(Number.isFinite(initialUrl.dial) && initialUrl.dial ? initialUrl.dial : 5);
  const [nostalgia, setNostalgia] = useState(initialUrl.nost);
  const [vibeText, setVibeText] = useState(initialUrl.text);
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [source, setSource] = useState(null);
  const [surprise, setSurprise] = useState(null);
  const [openMovie, setOpenMovie] = useState(null);
  const geoRef = useRef({ lat: null, lon: null });

  // Auto-detect geo (silent, best-effort)
  useEffect(() => {
    if (!navigator.geolocation) return;
    navigator.geolocation.getCurrentPosition(
      (pos) => { geoRef.current = { lat: pos.coords.latitude, lon: pos.coords.longitude }; },
      () => {}, { timeout: 4000, maximumAge: 5 * 60 * 1000 }
    );
  }, []);

  // Initial context + load from saved vibe id (if any)
  useEffect(() => {
    fetchContext().then(setContext).catch(() => {});
    if (initialUrl.v) {
      fetchVibe(initialUrl.v).then((v) => {
        if (v.mood) setMood(v.mood);
        if (typeof v.dial === "number") setDial(v.dial);
        if (v.vibe_text) setVibeText(v.vibe_text);
        setNostalgia(!!v.nostalgia);
      }).catch(() => {});
    }
  }, []);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const { picks, source: src, context: ctx } = await fetchRecommendations({
        mood, vibe_text: vibeText, dial, nostalgia,
        lat: geoRef.current.lat, lon: geoRef.current.lon,
      });
      setMovies(picks || []);
      setSource(src);
      if (ctx) setContext((old) => old || ctx);
    } catch (e) {
      toast.error("Couldn't fetch picks. Please try again.");
    } finally {
      setLoading(false);
    }
  }, [mood, dial, nostalgia, vibeText]);

  // First load + reload when key inputs change (debounced)
  useEffect(() => {
    const t = setTimeout(load, 350);
    return () => clearTimeout(t);
  }, [mood, dial, nostalgia, load]);

  const handleShare = async () => {
    try {
      const { id } = await createVibe({ mood, vibe_text: vibeText, dial, nostalgia });
      const params = new URLSearchParams();
      if (id) params.set("v", id);
      if (mood) params.set("mood", mood);
      params.set("dial", String(dial));
      if (nostalgia) params.set("nost", "1");
      if (vibeText) params.set("text", vibeText);
      const url = `${window.location.origin}${window.location.pathname}?${params.toString()}`;
      await navigator.clipboard.writeText(url);
      toast.success("Vibe link copied", { description: "Anyone with the link opens your exact vibe." });
    } catch (e) {
      toast.error("Couldn't copy link");
    }
  };

  const handleSurprise = () => {
    if (movies.length === 0) return;
    const pick = movies[Math.floor(Math.random() * movies.length)];
    setSurprise(pick);
  };

  const heroTitle = nostalgia ? "Rewind to warmer light." : "What are you in the mood for?";
  const heroSub = nostalgia
    ? "Late-night VHS static, coming-of-age fire escapes, cult classics you swore you'd remembered."
    : "Tell MoodReel your vibe. We'll pull films — famous, forgotten, and a few you've never heard of.";

  return (
    <div className="relative min-h-screen text-slate-100">
      <BackgroundFX />
      <CursorGlow />
      <Toaster theme="dark" position="bottom-center" richColors closeButton />

      {/* HEADER */}
      <header className="relative z-10 px-5 md:px-10 pt-6 md:pt-8 flex items-center justify-between">
        <div className="flex items-center gap-2" data-testid="brand-logo">
          <Film size={20} className="text-purple-300" />
          <span className="font-serif-editorial text-2xl tracking-tight">MoodReel</span>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={handleSurprise}
                  disabled={movies.length === 0}
                  className="hidden md:inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.03] px-3.5 py-1.5 text-sm text-slate-200 hover:bg-white/[0.06] transition-colors disabled:opacity-40"
                  data-testid="surprise-button">
            <Dice5 size={14} /> Surprise Me
          </button>
          <button onClick={handleShare}
                  className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.03] px-3.5 py-1.5 text-sm text-slate-200 hover:bg-white/[0.06] transition-colors"
                  data-testid="share-button">
            <Share2 size={14} /> Share
          </button>
        </div>
      </header>

      {/* HERO */}
      <section className="relative z-10 px-5 md:px-10 pt-10 md:pt-16 pb-8 md:pb-12 max-w-6xl mx-auto">
        <div className="mb-5">
          <ContextBadge context={context} />
        </div>
        <motion.h1
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: "easeOut" }}
          className="font-serif-editorial text-4xl sm:text-5xl lg:text-6xl xl:text-7xl tracking-tight leading-[0.98] text-white max-w-4xl"
        >
          {heroTitle.split(" ").map((w, i) => (
            <span key={i} className="inline-block mr-2">
              {w === "vibe?" || w === "light." ? (
                <span className="italic text-transparent bg-clip-text bg-gradient-to-r from-purple-300 via-rose-300 to-amber-200">{w}</span>
              ) : w}
            </span>
          ))}
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15, duration: 0.6 }}
          className="mt-4 md:mt-6 text-slate-300/90 text-base md:text-lg max-w-2xl leading-relaxed"
        >
          {heroSub}
        </motion.p>

        <div className="mt-8 md:mt-10">
          <MoodChips selected={mood} onSelect={setMood} />
        </div>

        <div className="mt-6 md:mt-8">
          <VibeControls
            dial={dial} onDial={setDial}
            nostalgia={nostalgia} onNostalgia={setNostalgia}
            vibeText={vibeText} onVibeText={setVibeText}
            onGo={load}
          />
        </div>
      </section>

      {/* RESULTS */}
      <section className="relative z-10 px-5 md:px-10 pb-24 max-w-7xl mx-auto">
        <div className="flex items-end justify-between mb-6 md:mb-8">
          <div>
            <div className="text-[11px] font-mono-alt uppercase tracking-widest text-purple-300 mb-1">
              {source === "mock" ? "Curated Sample" : "The Reel"}
            </div>
            <h2 className="font-serif-editorial text-2xl md:text-3xl tracking-tight text-white">
              {mood ? <>Cinema for a <span className="italic text-purple-200">{mood}</span> hour</> : "Tonight's picks"}
              {nostalgia && <span className="italic text-amber-200/80"> · rewound</span>}
            </h2>
          </div>
          <button onClick={load}
                  className="inline-flex items-center gap-2 rounded-full glass px-4 py-2 text-sm text-slate-200 hover:bg-white/[0.08] transition-colors"
                  data-testid="refresh-button">
            <RefreshCw size={14} className={loading ? "animate-spin" : ""} />
            Refresh
          </button>
        </div>

        {loading && movies.length === 0 ? (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5 md:gap-7">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="aspect-[2/3] rounded-xl glass animate-pulse" />
            ))}
          </div>
        ) : movies.length === 0 ? (
          <div className="glass rounded-2xl p-10 text-center">
            <Sparkles className="mx-auto text-purple-300" size={22} />
            <p className="mt-3 font-serif-editorial text-xl">No films match that vibe.</p>
            <p className="text-slate-400 mt-1 text-sm">Try loosening the dial or picking a different mood.</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5 md:gap-7" data-testid="movie-grid">
            {movies.map((m, i) => (
              <MovieCard key={`${m.id}-${i}`} movie={m} index={i} onOpen={setOpenMovie} nostalgia={nostalgia} />
            ))}
          </div>
        )}

        <div className="md:hidden mt-8 flex justify-center">
          <button onClick={handleSurprise}
                  disabled={movies.length === 0}
                  className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.03] px-4 py-2 text-sm text-slate-200 hover:bg-white/[0.06] disabled:opacity-40"
                  data-testid="surprise-button-mobile">
            <Dice5 size={14} /> Surprise Me
          </button>
        </div>

        <footer className="mt-16 text-center text-xs text-slate-500 font-mono-alt uppercase tracking-widest">
          MoodReel · TMDB{source ? ` · ${source}` : ""}{context?.event ? ` · ${context.event.replace("_", " ")}` : ""}
        </footer>
      </section>

      {/* Modal for regular open */}
      <MovieModal movie={openMovie} onClose={() => setOpenMovie(null)} />

      {/* Surprise reveal */}
      <AnimatePresence>
        {surprise && (
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-40 bg-black/70 backdrop-blur-md flex items-center justify-center p-6"
            onClick={() => setSurprise(null)}
            data-testid="surprise-overlay"
          >
            <motion.div
              initial={{ scale: 0.85, rotate: -4, opacity: 0 }}
              animate={{ scale: 1, rotate: 0, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              transition={{ type: "spring", stiffness: 220, damping: 20 }}
              className="glass-strong rounded-3xl p-6 max-w-md w-full text-center"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="text-[11px] font-mono-alt uppercase tracking-widest text-purple-300 mb-3">Tonight, watch</div>
              {surprise.poster && (
                <img src={surprise.poster.startsWith("http") ? surprise.poster : `https://image.tmdb.org/t/p/w500${surprise.poster}`}
                     alt={surprise.title}
                     className="mx-auto w-44 aspect-[2/3] object-cover rounded-xl shadow-2xl border border-white/10 mb-4" />
              )}
              <h3 className="font-serif-editorial text-3xl leading-tight text-white">{surprise.title}</h3>
              <p className="text-slate-400 text-sm mt-1">{surprise.year} · ★ {surprise.rating}</p>
              {surprise.blurb && (
                <p className="font-instrument italic text-purple-200 mt-4 text-lg">&ldquo;{surprise.blurb}&rdquo;</p>
              )}
              <div className="mt-5 flex justify-center gap-2">
                <button onClick={() => { setOpenMovie(surprise); setSurprise(null); }}
                        className="rounded-full bg-white text-black px-4 py-2 text-sm font-medium hover:bg-purple-200"
                        data-testid="surprise-open-detail">
                  Tell me more
                </button>
                <button onClick={handleSurprise}
                        className="rounded-full border border-white/15 px-4 py-2 text-sm text-slate-200 hover:bg-white/10"
                        data-testid="surprise-again">
                  Reroll
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
