import { render } from "../core/renderer.js";

let active = null;
let offsetX = 0;
let offsetY = 0;

export function makeDraggable(el) {
  el.addEventListener("mousedown", (e) => {
    active = el;

    const rect = el.getBoundingClientRect();
    offsetX = e.clientX - rect.left;
    offsetY = e.clientY - rect.top;

    document.addEventListener("mousemove", onMove);
    document.addEventListener("mouseup", onUp);
  });
}

function onMove(e) {
  if (!active) return;

  active.style.left = (e.clientX - offsetX) + "px";
  active.style.top = (e.clientY - offsetY) + "px";

  render(); // 🔥 THIS IS THE KEY FIX
}

function onUp() {
  active = null;

  document.removeEventListener("mousemove", onMove);
  document.removeEventListener("mouseup", onUp);
}