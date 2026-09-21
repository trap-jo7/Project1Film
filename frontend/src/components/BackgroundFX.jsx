export default function BackgroundFX() {
  return (
    <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden" aria-hidden>
      <div className="absolute inset-0 hero-gradient" />
      <div className="absolute inset-0 dot-grid opacity-60" />
      <div className="orb purple" style={{ width: 520, height: 520, top: -160, left: -120 }} />
      <div className="orb oxblood" style={{ width: 480, height: 480, top: 60, right: -140, animationDelay: "3s" }} />
      <div className="orb rose" style={{ width: 360, height: 360, top: "48%", left: "45%", animationDelay: "6s", opacity: 0.35 }} />
      <div className="absolute inset-x-0 bottom-0 h-64 bg-gradient-to-t from-[#0B0B10] to-transparent" />
    </div>
  );
}
