export function getStubDirection(port) {
  switch (port.edge) {
    case "left":
      return { x: -20, y: 0 };

    case "right":
      return { x: 20, y: 0 };

    case "top":
      return { x: 0, y: -20 };

    case "bottom":
      return { x: 0, y: 20 };

    default:
      return { x: 0, y: 20 };
  }
}

export function applyStub(point, port) {
  if (!port || !port.edge) {
    return { x: point.x, y: point.y };
  }

  const d = getStubDirection(port);

  return {
    x: point.x + d.x,
    y: point.y + d.y
  };
}