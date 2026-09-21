import { useEffect, useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { fetchMovieDetail } from "@/lib/api";
import { X, ExternalLink, PlayCircle } from "lucide-react";

export default function MovieModal({ movie, onClose }) {
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!movie) return;
    let alive = true;
    setLoading(true);
    setDetail(null);
    fetchMovieDetail(movie.id)
      .then((d) => { if (alive) { setDetail(d); setLoading(false); } })
      .catch(() => { if (alive) { setDetail(null); setLoading(false); } });
    return () => { alive = false; };
  }, [movie]);

  if (!movie) return null;
  const m = { ...movie, ...(detail || {}) };
  const backdrop = m.backdrop && m.backdrop.startsWith("http") ? m.backdrop
    : m.backdrop ? `https://image.tmdb.org/t/p/w1280${m.backdrop}` : null;
  const poster = m.poster && m.poster.startsWith("http") ? m.poster
    : m.poster ? `https://image.tmdb.org/t/p/w500${m.poster}` : null;

  return (
    <Dialog open={!!movie} onOpenChange={(open) => { if (!open) onClose(); }}>
      <DialogContent
        className="max-w-3xl w-[95vw] p-0 border border-white/10 bg-[#0B0B10]/95 backdrop-blur-2xl overflow-hidden rounded-2xl"
        data-testid="movie-modal"
      >
        <DialogHeader className="sr-only">
          <DialogTitle>{m.title}</DialogTitle>
        </DialogHeader>
        <div className="relative">
          {backdrop && (
            <div className="absolute inset-0 -z-0">
              <img src={backdrop} alt="" className="h-56 md:h-72 w-full object-cover opacity-40" />
              <div className="absolute inset-0 bg-gradient-to-t from-[#0B0B10] via-[#0B0B10]/60 to-transparent" />
            </div>
          )}
          <button onClick={onClose}
                  className="absolute top-3 right-3 z-10 rounded-full glass w-9 h-9 flex items-center justify-center text-white hover:bg-white/10"
                  data-testid="modal-close-button" aria-label="Close">
            <X size={16} />
          </button>

          <div className="relative pt-6 md:pt-10 px-5 md:px-8 pb-6 flex gap-5">
            {poster && (
              <img src={poster} alt={m.title}
                   className="hidden md:block w-40 lg:w-48 aspect-[2/3] object-cover rounded-xl shadow-2xl border border-white/10" />
            )}
            <div className="flex-1 min-w-0">
              <div className="flex flex-wrap items-center gap-2 mb-2">
                <span className="rounded-md bg-black/50 px-1.5 py-0.5 text-[11px] font-mono-alt text-amber-300">
                  ★ {m.rating?.toFixed?.(1) ?? m.rating}
                </span>
                <span className="text-[11px] font-mono-alt text-white/70">{m.year}</span>
                {m.runtime && <span className="text-[11px] font-mono-alt text-white/70">{m.runtime} min</span>}
                {m.gem && <span className="text-[11px] font-mono-alt uppercase tracking-wider text-purple-300">Hidden Gem</span>}
              </div>
              <h2 className="font-serif-editorial text-2xl md:text-4xl font-semibold tracking-tight text-white leading-tight">
                {m.title}
              </h2>
              {m.director && (
                <p className="text-sm text-slate-400 mt-1">Directed by <span className="text-slate-200">{m.director}</span></p>
              )}
              {m.blurb && (
                <p className="font-instrument italic text-purple-200/90 mt-4 text-lg leading-snug">
                  &ldquo;{m.blurb}&rdquo;
                </p>
              )}
              {m.overview && (
                <p className="text-slate-300/90 mt-3 text-[15px] leading-relaxed">{m.overview}</p>
              )}

              {m.genres?.length > 0 && (
                <div className="flex flex-wrap gap-1.5 mt-4">
                  {m.genres.filter(Boolean).slice(0, 5).map((g) => (
                    <span key={g} className="text-[11px] font-mono-alt uppercase tracking-widest text-slate-400 border border-white/10 rounded-full px-2 py-0.5">
                      {g}
                    </span>
                  ))}
                </div>
              )}

              <div className="mt-5 flex flex-wrap items-center gap-3">
                {m.trailer && (
                  <a href={m.trailer} target="_blank" rel="noreferrer"
                     className="inline-flex items-center gap-2 rounded-full bg-white text-black px-4 py-2 text-sm font-medium hover:bg-purple-200 transition-colors"
                     data-testid="modal-trailer-link">
                    <PlayCircle size={16} /> Watch Trailer
                  </a>
                )}
                <a href={`https://www.themoviedb.org/movie/${m.id}`} target="_blank" rel="noreferrer"
                   className="inline-flex items-center gap-2 rounded-full border border-white/15 px-4 py-2 text-sm text-slate-200 hover:bg-white/[0.05]"
                   data-testid="modal-tmdb-link">
                  <ExternalLink size={14} /> TMDB
                </a>
              </div>

              {m.providers?.length > 0 && (
                <div className="mt-5">
                  <div className="text-[11px] font-mono-alt uppercase tracking-widest text-purple-300 mb-2">Where to watch (US)</div>
                  <div className="flex flex-wrap gap-2">
                    {m.providers.map((p) => (
                      <span key={p} className="text-xs rounded-md glass px-2 py-1 text-slate-200">{p}</span>
                    ))}
                  </div>
                </div>
              )}

              {m.cast?.length > 0 && (
                <div className="mt-5">
                  <div className="text-[11px] font-mono-alt uppercase tracking-widest text-purple-300 mb-2">Cast</div>
                  <div className="flex flex-wrap gap-x-3 gap-y-1 text-sm text-slate-300">
                    {m.cast.slice(0, 6).map((c) => (
                      <span key={c.name}><span className="text-slate-100">{c.name}</span><span className="text-slate-500"> as {c.character}</span></span>
                    ))}
                  </div>
                </div>
              )}

              {loading && !detail && <div className="mt-4 text-xs text-slate-500 font-mono-alt">loading detail…</div>}
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
