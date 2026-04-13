const svg = document.getElementById("wires");

export function drawDebug(points) {
  points.forEach((p, i) => {
    const c = document.createElementNS("http://www.w3.org/2000/svg", "circle");

    c.setAttribute("cx", p.x);
    c.setAttribute("cy", p.y);
    c.setAttribute("r", 3);

    if (i === 0 || i === points.length - 1)
      c.setAttribute("fill", "red");
    else
      c.setAttribute("fill", "lime");

    svg.appendChild(c);
  });
}