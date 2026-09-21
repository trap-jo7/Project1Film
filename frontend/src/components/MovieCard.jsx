import { motion } from "framer-motion";

export default function MovieCard({ movie, index, onOpen, nostalgia }) {
  const poster = movie.poster && movie.poster.startsWith("http") ? movie.poster
    : movie.poster ? `https://image.tmdb.org/t/p/w500${movie.poster}` : null;
  return (
    <motion.article
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-40px" }}
      transition={{ duration: 0.5, ease: "easeOut", delay: (index % 8) * 0.05 }}
      className="group flex flex-col gap-3"
      data-testid={`movie-card-${movie.id}`}
    >
      <button
        onClick={() => onOpen(movie)}
        className={`poster relative overflow-hidden rounded-xl bg-[#14121C] aspect-[2/3] w-full text-left focus:outline-none focus:ring-2 focus:ring-purple-500/60 ${nostalgia ? "nostalgia-tint" : ""}`}
        data-testid={`movie-card-open-${movie.id}`}
      >
        <div className="absolute inset-0 -z-0"
             style={{
               background: `linear-gradient(140deg, hsl(${(movie.id * 37) % 360} 50% 22%) 0%, hsl(${(movie.id * 71 + 60) % 360} 40% 12%) 100%)`,
             }}>
          <div className="absolute inset-0 dot-grid opacity-40" />
          <div className="absolute inset-0 flex flex-col items-center justify-center px-5 text-center">
            <span className="font-serif-editorial italic text-white/95 text-xl md:text-2xl leading-tight">{movie.title}</span>
            <span className="mt-2 font-mono-alt text-[10px] uppercase tracking-widest text-white/60">{movie.year}</span>
          </div>
        </div>
        {poster && (
          <img src={poster} alt={movie.title} loading="lazy"
               className="relative z-[1] h-full w-full object-cover"
               onError={(e) => { e.currentTarget.style.display = "none"; }} />
        )}
        <div className="pointer-events-none absolute inset-0 z-[2] bg-gradient-to-t from-black/85 via-black/30 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 z-[3] p-3 md:p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="rounded-md bg-black/50 backdrop-blur-sm px-1.5 py-0.5 text-[10px] font-mono-alt text-amber-300">
              ★ {movie.rating?.toFixed?.(1) ?? movie.rating}
            </span>
            <span className="text-[10px] font-mono-alt text-white/60">{movie.year}</span>
            {movie.gem && (
              <span className="relative rounded-md bg-purple-500/25 border border-purple-400/40 px-1.5 py-0.5 text-[10px] font-mono-alt text-purple-200 uppercase tracking-wider"
                    data-testid={`gem-badge-${movie.id}`}>
                Hidden Gem
                <span className="sparkle" style={{ top: -3, right: -3 }} />
              </span>
            )}
          </div>
          <h3 className="font-serif-editorial text-lg md:text-xl font-semibold text-white leading-tight tracking-tight line-clamp-2">
            {movie.title}
          </h3>
        </div>
      </button>

      {movie.blurb && (
        <p className="font-instrument italic text-slate-300/90 text-[15px] leading-snug px-1"
           data-testid={`movie-blurb-${movie.id}`}>
          &ldquo;{movie.blurb}&rdquo;
        </p>
      )}
    </motion.article>
  );
}
