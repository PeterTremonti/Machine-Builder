// V7.14.6 — Localized routing (fixes frozen vertical line + stub glitches)

function getLocalBounds(A, B) {
  const minX = Math.min(A.x, B.x);
  const maxX = Math.max(A.x, B.x);
  const minY = Math.min(A.y, B.y);
  const maxY = Math.max(A.y, B.y);

  return { minX, maxX, minY, maxY };
}

function routeFromLeft(start, end, bounds) {
  const safeX = bounds.minX - 40;

  return [
    start,
    { x: safeX, y: start.y },
    { x: safeX, y: end.y },
    end
  ];
}

function routeFromRight(start, end, bounds) {
  const safeX = bounds.maxX + 40;

  return [
    start,
    { x: safeX, y: start.y },
    { x: safeX, y: end.y },
    end
  ];
}

function routeFromTop(start, end, bounds) {
  const safeY = bounds.minY - 40;

  return [
    start,
    { x: start.x, y: safeY },
    { x: end.x, y: safeY },
    end
  ];
}

function routeFromBottom(start, end, bounds) {
  const safeY = bounds.maxY + 40;

  return [
    start,
    { x: start.x, y: safeY },
    { x: end.x, y: safeY },
    end
  ];
}

export function buildWirePath(A, A1, B1, B, devices) {
  if (!A || !A1 || !B || !B1) return [];

  const start = { x: A1.x, y: A1.y };
  const end = { x: B1.x, y: B1.y };

  // 🔥 ONLY use the two ports for bounds
  const bounds = getLocalBounds(start, end);

  // 🔒 LOCK to start port direction (no flipping)
  switch (A.edge) {
    case "left":
      return routeFromLeft(start, end, bounds);

    case "right":
      return routeFromRight(start, end, bounds);

    case "top":
      return routeFromTop(start, end, bounds);

    case "bottom":
      return routeFromBottom(start, end, bounds);

    default:
      return routeFromLeft(start, end, bounds);
  }
}