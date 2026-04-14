import { state } from "./state.js";
import { getStubPoint } from "../geometry/ports.js";
import { buildWirePath } from "../geometry/routing.js";
import { drawDebug } from "../debug/debug.js";

const svg = document.getElementById("wires");

function safePoint(p) {
  if (!p) return { x: 0, y: 0 };

  return {
    x: typeof p.x === "number" ? p.x : 0,
    y: typeof p.y === "number" ? p.y : 0,
    edge: p.edge
  };
}

/**
 * 🔥 FIX: use the ACTUAL clicked port DOM element
 */
function resolvePort(portObj) {
  const portEl = portObj?.data?.el;

  if (!portEl) {
    const r = portObj?.device?.el?.getBoundingClientRect?.();
    if (!r) return { x: 0, y: 0 };
    return { x: r.left, y: r.top };
  }

  const rect = portEl.getBoundingClientRect();

  return safePoint({
    x: rect.left + rect.width / 2,
    y: rect.top + rect.height / 2,
    edge: portObj.data.edge
  });
}

export function render() {
  svg.innerHTML = "";

  state.wires.forEach(wire => {
    const A = resolvePort(wire.from);
    const B = resolvePort(wire.to);

    if (!A || !B) return;

    const A1 = getStubPoint(A);
    const B1 = getStubPoint(B);

    if (!A1 || !B1) return;

    const path = buildWirePath(A, A1, B1, B, state.devices);

    const d = path.map((p, i) =>
      (i === 0 ? "M" : "L") + `${p.x},${p.y}`
    ).join(" ");

    const el = document.createElementNS("http://www.w3.org/2000/svg", "path");
    el.setAttribute("d", d);
    el.setAttribute("stroke", "cyan");
    el.setAttribute("fill", "none");
    el.setAttribute("stroke-width", "2");

    svg.appendChild(el);

    drawDebug(path);
  });
}