import { render } from "../core/renderer.js";

export function makeDraggable(el) {
  let offsetX, offsetY, dragging = false;

  el.addEventListener("mousedown", e => {
    dragging = true;
    offsetX = e.offsetX;
    offsetY = e.offsetY;
  });

  window.addEventListener("mousemove", e => {
    if (!dragging) return;

    el.style.left = (e.clientX - offsetX) + "px";
    el.style.top = (e.clientY - offsetY) + "px";

    render(); // recompute wires
  });

  window.addEventListener("mouseup", () => dragging = false);
}