# Machine Model Architecture

The machine model represents the entire machine internally.

It is firmware-independent.

---

# Machine Structure

```
Machine
 ├ Devices
 ├ Ports
 ├ Connections
 ├ Connectors
 └ Harnesses
```

---

# Devices

Devices represent physical hardware.

Examples:

Controller boards
Steppers
Hotends
Fans
Endstops

Devices contain ports.

---

# Ports

Ports represent electrical interfaces.

Examples:

STEP output
PWM output
thermistor input
GPIO

Ports define:

• type
• direction
• voltage
• signal protocol

---

# Connections

Connections link two ports.

Example:

```
Board STEP0 → X Motor STEP
```

Connections may reference cables.

---

# Connectors

Connectors represent physical plugs.

Examples:

JST-XH
Dupont
MicroFit

Connector definitions include:

• pin count
• pin numbering
• compatible wire gauges

---

# Harnesses

Harnesses group multiple cables.

Example:

```
Toolhead Harness
 ├ Heater cable
 ├ Thermistor cable
 ├ Fan cable
```

Harnesses simplify visualization.
