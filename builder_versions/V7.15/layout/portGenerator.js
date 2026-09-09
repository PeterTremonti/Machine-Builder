export function generatePorts(device, rawPorts) {
  const ports = [];

  const width = device.width;
  const height = device.height;

  // simple grouping
  const powerPorts = rawPorts.filter(p => p.function === "power");
  const signalPorts = rawPorts.filter(p => p.function === "signal");

  // POWER → bottom edge
  powerPorts.forEach((p, i) => {
  const spacing = width / (powerPorts.length + 1);

  ports.push({
    id: p.id,
    function: p.function,
    edge: "bottom",
    x: device.x + spacing * (i + 1),
    y: device.y + height
  });
});

  // SIGNAL → left edge
  signalPorts.forEach((p, i) => {
    ports.push({
      id: p.id,
      function: p.function,
      edge: "left",
      x: device.x,
      y: device.y + height / 2 + (i === 0 ? -10 : 10)
    });
  });

  return ports;
}