# Hardware Database Schema

The hardware database defines all hardware components that Machine Builder can use.

It contains structured descriptions of:

• controller boards
• motors
• sensors
• actuators
• connectors
• cables

The database allows Machine Builder to:

• display devices visually
• validate wiring
• generate firmware configurations
• generate bill of materials

---

# Database Directory Structure

```
hardware_database/

 boards/
 devices/
 motors/
 sensors/
 connectors/
 cables/
 assemblies/
```

Each entry is a JSON file describing one hardware item.

Example:

```
boards/btt_octopus_v1_1.json
motors/nema17_42mm.json
connectors/jst_xh_4pin.json
```

---

# Core Hardware Object Structure

All hardware entries share a common base structure.

```
{
  "id": "unique_identifier",
  "name": "Human readable name",
  "manufacturer": "Company name",
  "category": "device category",
  "description": "Short description",
  "ports": [],
  "specs": {},
  "connectors": []
}
```

---

# Hardware Categories

```
board
motor
sensor
heater
fan
power_supply
display
probe
endstop
connector
cable
assembly
```

---

# Ports

Ports represent electrical interfaces on a device.

Example:

```
"ports": [
  {
    "id": "step_x",
    "name": "X Stepper",
    "type": "stepper",
    "direction": "output",
    "signals": ["step", "dir", "enable"]
  }
]
```

Port fields:

| Field     | Description                |
| --------- | -------------------------- |
| id        | unique port identifier     |
| name      | display name               |
| type      | functional type            |
| direction | input or output            |
| signals   | list of electrical signals |

---

# Signal Types

Signals describe communication or power types.

Examples:

```
step
dir
enable
pwm
analog
digital
uart
spi
i2c
heater
thermistor
fan
power
ground
```

These allow the diagnostics engine to validate connections.

---

# Connector Definition

Devices may expose physical connectors.

Example:

```
"connectors": [
  {
    "id": "fan0",
    "type": "JST-XH-2",
    "pins": [
      { "pin": 1, "signal": "power" },
      { "pin": 2, "signal": "ground" }
    ]
  }
]
```

Connector fields:

| Field | Description          |
| ----- | -------------------- |
| id    | connector identifier |
| type  | connector model      |
| pins  | pin definitions      |

---

# Specifications Field

Technical specifications are stored under `"specs"`.

Example:

```
"specs": {
  "voltage": "24V",
  "current_max": "10A",
  "power_max": "240W"
}
```

Specs vary depending on device type.

Examples:

Motors

```
"specs": {
  "step_angle": 1.8,
  "rated_current": 1.5,
  "voltage": 3.2
}
```

Heaters

```
"specs": {
  "voltage": 24,
  "power": 40
}
```

---

# Controller Board Schema

Example controller board definition.

```
{
  "id": "btt_octopus_v1_1",
  "name": "BTT Octopus v1.1",
  "manufacturer": "BigTreeTech",
  "category": "board",

  "ports": [

    {
      "id": "stepper_x",
      "name": "X Stepper Driver",
      "type": "stepper",
      "direction": "output",
      "signals": ["step", "dir", "enable"]
    },

    {
      "id": "heater_0",
      "name": "Hotend Heater",
      "type": "heater",
      "direction": "output",
      "signals": ["pwm", "power"]
    },

    {
      "id": "thermistor_0",
      "name": "Hotend Thermistor",
      "type": "thermistor",
      "direction": "input",
      "signals": ["analog"]
    },

    {
      "id": "fan_0",
      "name": "Fan 0",
      "type": "fan",
      "direction": "output",
      "signals": ["pwm", "power"]
    }

  ],

  "specs": {
    "voltage": "12-24V",
    "max_heater_current": "10A"
  }
}
```

---

# Motor Example

```
{
  "id": "nema17_42mm",
  "name": "NEMA17 Stepper Motor",
  "manufacturer": "Generic",
  "category": "motor",

  "ports": [
    {
      "id": "coil",
      "name": "Stepper Input",
      "type": "stepper",
      "direction": "input",
      "signals": ["coil_a", "coil_b"]
    }
  ],

  "specs": {
    "step_angle": 1.8,
    "rated_current": 1.5,
    "holding_torque": "40Ncm"
  }
}
```

---

# Sensor Example

```
{
  "id": "100k_thermistor",
  "name": "100K NTC Thermistor",
  "manufacturer": "Generic",
  "category": "sensor",

  "ports": [
    {
      "id": "signal",
      "type": "thermistor",
      "direction": "output",
      "signals": ["analog"]
    }
  ],

  "specs": {
    "resistance": "100K",
    "beta": 3950
  }
}
```

---

# Connector Definition Example

```
{
  "id": "jst_xh_2",
  "name": "JST-XH 2 Pin",
  "category": "connector",

  "specs": {
    "pin_count": 2,
    "pitch": "2.54mm",
    "max_current": "3A"
  }
}
```

---

# Cable Definition Example

```
{
  "id": "stepper_cable_4",
  "name": "Stepper Cable",
  "category": "cable",

  "specs": {
    "wire_count": 4,
    "gauge": "24AWG",
    "shielded": false
  }
}
```

---

# Assembly Example

Assemblies represent reusable machine modules.

Example:

```
{
  "id": "eva_toolhead",
  "name": "EVA Toolhead",
  "category": "assembly",

  "devices": [
    "extruder_bmg",
    "hotend_v6",
    "fan_4010",
    "fan_5015",
    "probe_bltouch"
  ]
}
```

Assemblies allow users to drop entire machine subsystems into a design.

---

# Future Extensions

The hardware schema is designed to support future systems:

• automatic firmware mapping
• connector pin mapping
• electrical load analysis
• machine BOM generation
• harness engineering
