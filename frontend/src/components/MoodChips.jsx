import { motion } from "framer-motion";
import { MOODS } from "@/lib/moods";

export default function MoodChips({ selected, onSelect }) {
  return (
    <div className="flex flex-wrap gap-2 md:gap-3" data-testid="mood-chip-row">
      {MOODS.map((m, i) => {
        const isSelected = selected === m.id;
        return (
          <motion.button
            key={m.id}
            onClick={() => onSelect(isSelected ? null : m.id)}
            data-testid={`mood-chip-${m.id}`}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.04 * i, duration: 0.4, ease: "easeOut" }}
            whileHover={{ y: -2 }}
            whileTap={{ scale: 0.97 }}
            className={`relative px-4 py-2 rounded-full border text-sm md:text-[15px] flex items-center gap-2 transition-colors backdrop-blur-md
              ${isSelected
                ? "border-purple-400/60 bg-gradient-to-br from-purple-500/25 to-rose-500/25 text-white shadow-[0_0_30px_-6px_rgba(168,85,247,0.55)]"
                : "border-white/10 bg-white/[0.03] text-slate-200 hover:bg-white/[0.06] hover:text-white"}`}
          >
            <span className="text-base leading-none">{m.emoji}</span>
            <span className="font-medium tracking-tight">{m.label}</span>
            {m.sparkle && (
              <>
                <span className="sparkle" style={{ top: -3, right: -3 }} />
                <span className="sparkle" style={{ bottom: 2, left: 6, animationDelay: "0.7s" }} />
              </>
            )}
          </motion.button>
        );
      })}
    </div>
  );
}
