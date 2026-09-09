import { onPortClick } from "./systems/wiring.js";
import { makeDraggable } from "./systems/dragging.js";
import { render } from "./core/renderer.js";
import { state } from "./core/state.js";
import { generatePorts } from "./layout/portGenerator.js";

const devicesContainer = document.getElementById("devices");

function createDevice(x, y, label) {
  const el = document.createElement("div");
  el.className = "device";
  el.style.left = x + "px";
  el.style.top = y + "px";
  el.innerText = label;

  const deviceObj = {
    el,
    x,
    y,
    width: 120,
    height: 60,
    ports: []
  };

  const rawPorts = [
    { id: "vin", function: "power" },
    { id: "step", function: "signal" }
  ];

  const layoutPorts = generatePorts(deviceObj, rawPorts);
  deviceObj.ports = layoutPorts;

  layoutPorts.forEach(portData => {
    const port = document.createElement("div");
    port.className = "port";

const PORT_SIZE = 10; // match your CSS

port.style.left = (portData.x - x - PORT_SIZE / 2) + "px";
port.style.top = (portData.y - y - PORT_SIZE / 2) + "px";

    const portObj = {
      el: port,
      type: portData.function,
      device: deviceObj,
      data: {
  id: portData.id,
  function: portData.function,
  edge: portData.edge,
  el: port
}
    };

    port.onclick = () => onPortClick(portObj);

    el.appendChild(port);
  });

  devicesContainer.appendChild(el);
  state.devices.push(deviceObj);

  makeDraggable(el);
}

createDevice(200, 200, "Controller");
createDevice(500, 300, "Stepper");

render();