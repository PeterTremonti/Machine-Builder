import { onPortClick } from "./systems/wiring.js";
import { makeDraggable } from "./systems/dragging.js";
import { render } from "./core/renderer.js";
import { state } from "./core/state.js";

const devices = document.getElementById("devices");

function createDevice(x, y, label, portType) {
  const el = document.createElement("div"); // ✅ FIRST
  el.className = "device";
  el.style.left = x + "px";
  el.style.top = y + "px";
  el.innerText = label;

  const port = document.createElement("div");
  port.className = "port";
  port.style.left = "-5px";
  port.style.top = "20px";

  const portObj = {
    el: port,
    type: portType
  };

  port.onclick = () => onPortClick(portObj);

  el.appendChild(port);
  devices.appendChild(el);

  // ✅ NOW el exists, safe to store
  const deviceObj = { el };
  state.devices.push(deviceObj);

  makeDraggable(el);
}

createDevice(200, 200, "Controller", "output");
createDevice(500, 300, "Stepper", "input");

render();