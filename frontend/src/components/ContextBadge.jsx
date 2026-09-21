import { WEATHER_ICON, EVENT_LABEL } from "@/lib/moods";

const TOD_LABEL = { morning: "Morning", afternoon: "Afternoon", evening: "Evening", late_night: "Late Night" };

export default function ContextBadge({ context }) {
  if (!context) return null;
  const w = context.weather || {};
  const cond = w.condition || "mild";
  const icon = WEATHER_ICON[cond] || "✨";
  const parts = [];
  if (w.city) parts.push(w.city);
  if (typeof w.temp === "number") parts.push(`${Math.round(w.temp)}°C`);
  const location = parts.join(" · ");
  return (
    <div className="inline-flex items-center gap-3 rounded-full glass px-4 py-1.5 text-xs md:text-sm text-slate-200"
         data-testid="context-badge">
      <span className="text-base leading-none">{icon}</span>
      <span className="capitalize">{cond.replace("_", " ")}</span>
      {location && <><span className="text-white/20">·</span><span>{location}</span></>}
      <span className="text-white/20">·</span>
      <span>{TOD_LABEL[context.time_of_day] || "Now"}</span>
      {context.event && (
        <>
          <span className="text-white/20">·</span>
          <span className="font-mono-alt uppercase tracking-widest text-[10px] md:text-[11px] text-purple-300">
            {EVENT_LABEL[context.event] || context.event}
          </span>
        </>
      )}
    </div>
  );
}
