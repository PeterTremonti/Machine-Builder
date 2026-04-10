# Builder Modes

Machine Builder supports multiple wiring detail levels.

---

# Fast Mode

Simplest connection system.

```
device → device
```

Used for quick machine planning.

---

# Basic Mode

Adds cable information.

```
device → cable → device
```

---

# Advanced Mode

Includes connectors.

```
device → connector → cable → connector → device
```

---

# Engineering Mode

Full harness design.

Includes:

• wire color
• wire gauge
• connector pin mapping
• cable length
• harness grouping
