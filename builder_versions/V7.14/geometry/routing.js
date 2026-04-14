// V7.12 - Obstacle-aware Manhattan Router

function isInsideRect(p, rect) {
  return (
    p.x >= rect.left &&
    p.x <= rect.right &&
    p.y >= rect.top &&
    p.y <= rect.bottom
  );
}

/**
 * Find a safe "channel Y" line that avoids device overlap
 */
function findSafeY(a, b, devices) {
  const baseY = (a.y + b.y) / 2;

  let y = baseY;

  for (const d of devices) {
    const rect = d.el.getBoundingClientRect();

    // if our horizontal segment would cross a box
    const crosses =
      (a.x < rect.right && b.x > rect.left) ||
      (b.x < rect.right && a.x > rect.left);

    const insideY = y >= rect.top && y <= rect.bottom;

    if (crosses && insideY) {
      // push route down
      y = rect.bottom + 30;
    }
  }

  return y;
}

/**
 * Stable orthogonal routing with obstacle avoidance
 */
export function routeManhattan(a, b, devices) {
  const midY = findSafeY(a, b, devices);

  return [
    a,
    { x: a.x, y: midY },
    { x: b.x, y: midY },
    b
  ];
}

/**
 * Full wire path assembly
 */
export function buildWirePath(A, A1, B1, B, devices) {
  const core = routeManhattan(A1, B1, devices);

  return [
    A,
    A1,
    ...core.slice(1, -1),
    B1,
    B
  ];
}