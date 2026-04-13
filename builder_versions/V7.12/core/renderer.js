import { state } from "./state.js";
import { getPortAnchor, getStubPoint } from "../geometry/ports.js";
import { buildWirePath } from "../geometry/routing.js";
import { drawDebug } from "../debug/debug.js";

const svg = document.getElementById("wires");

export function render() {
  svg.innerHTML = "";

  state.wires.forEach(wire => {
    const A = getPortAnchor(wire.from);
    const B = getPortAnchor(wire.to);

    // FIXED STUBS (NO TARGET LOGIC)
    const A1 = getStubPoint(A, "right");
    const B1 = getStubPoint(B, "left");

    const path = buildWirePath(A, A1, B1, B, state.devices);

    const d = path.map((p, i) =>
      (i === 0 ? "M" : "L") + `${p.x},${p.y}`
    ).join(" ");

    const el = document.createElementNS("http://www.w3.org/2000/svg", "path");
    el.setAttribute("d", d);
    el.setAttribute("stroke", "cyan");
    el.setAttribute("fill", "none");
    el.setAttribute("stroke-width", "2");

    // IMPORTANT: wires stay visible above parts
    el.style.zIndex = 999;

    svg.appendChild(el);

    drawDebug(path);
    console.log("routing:", A, B);
  });
}