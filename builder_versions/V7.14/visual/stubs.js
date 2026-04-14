import { state } from "../core/state.js";
import { render } from "../core/renderer.js";

export function onPortClick(port) {
  console.log("Clicked port:", port);

  if (!state.pendingConnection) {
    state.pendingConnection = port;
    return;
  }

  const a = state.pendingConnection;
  const b = port;

  state.pendingConnection = null;

  // Direction resolution (basic)
  let from = a;
  let to = b;

  if (a.type === "input" && b.type === "output") {
    from = b;
    to = a;
  }

  state.wires.push({ from, to });

  render();
}