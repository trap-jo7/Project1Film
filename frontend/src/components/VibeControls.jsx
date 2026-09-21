import { Switch } from "@/components/ui/switch";

export default function VibeControls({ dial, onDial, nostalgia, onNostalgia, vibeText, onVibeText, onGo }) {
  const dialLabel = dial <= 3 ? "Mainstream" : dial <= 6 ? "Balanced" : dial <= 8 ? "Deep Cut" : "Buried Treasure";
  return (
    <div className="grid grid-cols-1 lg:grid-cols-[1fr_auto] gap-4 lg:gap-6 items-stretch">
      <div className="glass rounded-2xl p-4 md:p-5">
        <label className="block text-[11px] font-mono-alt uppercase tracking-widest text-purple-300 mb-2">
          Describe the vibe
        </label>
        <div className="flex gap-2">
          <input
            type="text"
            value={vibeText}
            onChange={(e) => onVibeText(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && onGo?.()}
            placeholder="a rainy Sunday, a heart still bruised, something in a foreign language…"
            className="flex-1 bg-transparent outline-none text-slate-100 placeholder:text-slate-500 text-[15px] md:text-base font-serif-editorial italic"
            data-testid="vibe-input"
          />
          <button
            onClick={() => onGo?.()}
            className="rounded-full bg-white text-black px-4 py-1.5 text-sm font-medium hover:bg-purple-200 transition-colors"
            data-testid="vibe-submit-button"
          >
            Reel it
          </button>
        </div>
      </div>

      <div className="glass rounded-2xl p-4 md:p-5 flex flex-col gap-3 min-w-[280px]">
        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-[11px] font-mono-alt uppercase tracking-widest text-purple-300">
              Mainstream ↔ Obscure
            </label>
            <span className="text-[11px] font-mono-alt text-slate-300">{dialLabel} · {dial}</span>
          </div>
          <input
            type="range" min={1} max={10} step={1} value={dial}
            onChange={(e) => onDial(parseInt(e.target.value, 10))}
            className="vibe-dial"
            data-testid="obscure-dial"
          />
        </div>
        <div className="flex items-center justify-between pt-1">
          <div>
            <div className="text-sm text-slate-100 flex items-center gap-1.5">
              <span>🕯️</span>Nostalgia Mode
            </div>
            <div className="text-[11px] text-slate-500 font-mono-alt uppercase tracking-widest">70s–90s bias · sepia grain</div>
          </div>
          <Switch checked={nostalgia} onCheckedChange={onNostalgia} data-testid="nostalgia-toggle" />
        </div>
      </div>
    </div>
  );
}
