const OFFSET = 20;

export function getPortAnchor(port) {
  const rect = port.el.getBoundingClientRect();

  return {
    x: rect.left + rect.width / 2,
    y: rect.top + rect.height / 2
  };
}

/**
 * FIXED direction stub:
 * NO target awareness
 */
export function getStubPoint(anchor, side) {
  switch (side) {
    case "left":   return { x: anchor.x - OFFSET, y: anchor.y };
    case "right":  return { x: anchor.x + OFFSET, y: anchor.y };
    case "top":    return { x: anchor.x, y: anchor.y - OFFSET };
    case "bottom": return { x: anchor.x, y: anchor.y + OFFSET };
  }
}