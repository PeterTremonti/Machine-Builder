# Machine Builder – Version 7.8 Specification

Version 7.8 introduces the **first true visual machine builder**.

This version focuses on:

• machine canvas
• device placement
• cable connections
• routing visualization

---

# Primary Features

## Visual Machine Canvas

Users can place devices on a workspace.

Devices include:

• controller boards
• motors
• hotends
• sensors
• fans
• power supplies

Ports are visible on each device.

Connections are drawn between ports.

---

## Device Placement

Devices can be:

• dragged from device library
• placed on canvas
• moved freely

Device positions are stored.

---

## Port Connections

Ports can be connected by dragging.

Example:

```
Board STEP0 → X Motor
Board HE0 → Heater
Board TH0 → Thermistor
```

Connections appear as wires.

---

## Cable Routing Engine

Automatic routing creates clean wiring paths.

Routing rules:

• orthogonal lines
• minimal overlap
• collision avoidance

Users may adjust routes manually.

---

## Connection Highlighting

Hovering over a device highlights all connected wires.

Hovering over a port highlights its connection path.

---

## Cable Bundling

Multiple wires between areas can be grouped.

Example:

```
Toolhead Harness
 ├ Heater
 ├ Thermistor
 ├ Fan
 └ Probe
```

Bundles improve diagram readability.

---

## Zoom Level Detail

Canvas detail changes with zoom level.

Zoomed Out:

Harness level.

Medium Zoom:

Cable level.

Close Zoom:

Wire level.

---

## Diagnostics Integration

Diagnostics run automatically.

Warnings appear for issues such as:

• missing thermistor
• duplicate pins
• incompatible connections

---

## Cable Length Estimation

Cable lengths are estimated from device positions.

Users can override with measured values.

---

# Development Goals

Version 7.8 establishes the foundation for:

• assembly modules
• firmware generation
• BOM generation

Future versions will expand the system.
