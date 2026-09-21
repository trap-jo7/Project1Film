import { useEffect, useRef } from "react";

export default function CursorGlow() {
  const glowRef = useRef(null);
  const dotRef = useRef(null);

  useEffect(() => {
    if (window.matchMedia("(hover: none)").matches) return;
    let raf = 0;
    let mx = -100, my = -100, gx = -100, gy = -100;
    const onMove = (e) => { mx = e.clientX; my = e.clientY; };
    const loop = () => {
      gx += (mx - gx) * 0.16;
      gy += (my - gy) * 0.16;
      if (glowRef.current) glowRef.current.style.transform = `translate(${gx}px, ${gy}px) translate(-50%, -50%)`;
      if (dotRef.current) dotRef.current.style.transform = `translate(${mx}px, ${my}px) translate(-50%, -50%)`;
      raf = requestAnimationFrame(loop);
    };
    window.addEventListener("mousemove", onMove);
    raf = requestAnimationFrame(loop);
    return () => { window.removeEventListener("mousemove", onMove); cancelAnimationFrame(raf); };
  }, []);

  return (
    <>
      <div ref={glowRef} className="cursor-glow" />
      <div ref={dotRef} className="cursor-dot" />
    </>
  );
}
