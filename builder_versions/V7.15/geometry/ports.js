const OFFSET = 20;

/**
 * Stub is PURELY based on edge
 */
export function getStubPoint(port) {
  switch (port.edge) {
    case "bottom":
      return { x: port.x, y: port.y + OFFSET };

    case "top":
      return { x: port.x, y: port.y - OFFSET };

    case "left":
      return { x: port.x - OFFSET, y: port.y };

    case "right":
      return { x: port.x + OFFSET, y: port.y };
  }
}