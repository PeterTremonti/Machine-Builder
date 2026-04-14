function groupPorts(ports) {
  const groups = {
    power: [],
    signal: [],
    other: []
  };

  for (const p of ports) {
    if (p.function === "power") groups.power.push(p);
    else if (p.function === "signal") groups.signal.push(p);
    else groups.other.push(p);
  }

  return groups;
}

function assignSides(groups) {
  return [
    { side: "bottom", ports: groups.power },
    { side: "left", ports: groups.signal },
    { side: "right", ports: groups.other }
  ].filter(g => g.ports.length > 0);
}

function layoutPortsOnSide(group, device, spacing = 25) {
  const count = group.ports.length;
  const total = (count - 1) * spacing;

  return group.ports.map((port, i) => {
    const offset = i * spacing - total / 2;

    let x = device.x;
    let y = device.y;

    if (group.side === "bottom") {
      x = device.x + device.width / 2 + offset;
      y = device.y + device.height;
    }

    if (group.side === "top") {
      x = device.x + device.width / 2 + offset;
      y = device.y;
    }

    if (group.side === "left") {
      x = device.x;
      y = device.y + device.height / 2 + offset;
    }

    if (group.side === "right") {
      x = device.x + device.width;
      y = device.y + device.height / 2 + offset;
    }

    return {
      id: port.id,
      function: port.function,
      edge: group.side,
      x,
      y
    };
  });
}

export function generatePorts(device, rawPorts) {
  const groups = groupPorts(rawPorts);
  const assigned = assignSides(groups);

  let result = [];

  for (const group of assigned) {
    result = result.concat(layoutPortsOnSide(group, device));
  }

  return result;
}