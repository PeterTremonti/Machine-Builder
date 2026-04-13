export function routeManhattan(a, b) {
  /**
   * FIXED ROUTING STRATEGY:
   * always horizontal first, then vertical
   */

  const midX = (a.x + b.x) / 2;

  return [
    a,
    { x: midX, y: a.y },
    { x: midX, y: b.y },
    b
  ];
}

export function buildWirePath(A, A1, B1, B) {
  return [
    A,
    A1,
    ...routeManhattan(A1, B1).slice(1, -1),
    B1,
    B
  ];
}