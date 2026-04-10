# Wiring System

Machine Builder supports multiple levels of wiring detail.

---

# Connection Hierarchy

```
Device
 ↓
Port
 ↓
Connector
 ↓
Wire
 ↓
Cable
 ↓
Harness
```

---

# Wire

A wire represents a single conductor.

Attributes:

• color
• gauge
• signal type

---

# Cable

A cable contains one or more wires.

Example:

Stepper motor cable:

```
4 wires
```

---

# Harness

Harnesses bundle cables together.

Example:

Toolhead harness.

Harnesses improve diagram readability.

---

# Cable Length

Two values exist:

Estimated length
Measured length

Measured values override estimates.
