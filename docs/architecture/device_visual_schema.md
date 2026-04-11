# Device Visual Schema

The Device Visual Schema defines how hardware devices are displayed on the Machine Builder canvas.

This schema allows devices to be rendered automatically using data from the hardware database.

Without this schema, devices would require hardcoded graphics.

With the schema, the visual builder can render any device defined in the database.

---

# Purpose

The visual schema defines:

• device shape
• device size
• connector positions
• port locations
• visual icons
• labels

This allows Machine Builder to draw devices consistently.

---

# Visual Rendering Pipeline

Device rendering follows this process:

```
Hardware Database
       ↓
Device Definition
       ↓
Visual Schema
       ↓
Canvas Renderer
```

The renderer uses the visual schema to place ports and connectors.

---

# Visual Schema Structure

Example structure:

```
{
  "visual": {
    "shape": "rectangle",
    "size": { "width": 200, "height": 120 },
    "ports": [],
    "connectors": [],
    "labels": []
  }
}
```

---

# Device Shape

The basic device outline.

Supported shapes:

```
rectangle
rounded_rectangle
circle
custom
```

Example:

```
"shape": "rectangle"
```

---

# Device Size

Defines the default display size.

Example:

```
"size": {
  "width": 220,
  "height": 140
}
```

Units are canvas pixels.

The canvas can scale these values when zooming.

---

# Port Visualization

Ports represent logical device interfaces.

Each port has a visual location.

Example:

```
"ports": [
  {
    "id": "stepper_x",
    "x": 10,
    "y": 40,
    "side": "left",
    "label": "X"
  }
]
```

Fields:

| Field | Description                                  |
| ----- | -------------------------------------------- |
| id    | port identifier (must match hardware schema) |
| x     | x position                                   |
| y     | y position                                   |
| side  | board edge location                          |
| label | visible text                                 |

---

# Port Side

Ports may be anchored to device edges.

Valid sides:

```
left
right
top
bottom
```

Example:

```
"side": "left"
```

This helps the routing engine draw cleaner wires.

---

# Connector Visualization

Physical connectors can be drawn on the device.

Example:

```
"connectors": [
  {
    "id": "fan0",
    "type": "JST-XH-2",
    "x": 180,
    "y": 30,
    "rotation": 90
  }
]
```

Fields:

| Field    | Description          |
| -------- | -------------------- |
| id       | connector identifier |
| type     | connector model      |
| x        | x position           |
| y        | y position           |
| rotation | visual orientation   |

---

# Connector Rotation

Rotation angles:

```
0
90
180
270
```

This allows connectors to face the correct direction.

---

# Label System

Devices can include visual labels.

Example:

```
"labels": [
  {
    "text": "BTT Octopus",
    "x": 100,
    "y": 10,
    "align": "center"
  }
]
```

Fields:

| Field | Description    |
| ----- | -------------- |
| text  | label text     |
| x     | x position     |
| y     | y position     |
| align | text alignment |

---

# Port Icons

Ports can display icons.

Examples:

```
stepper
fan
heater
thermistor
gpio
power
ground
```

Example definition:

```
{
  "id": "fan0",
  "x": 10,
  "y": 80,
  "icon": "fan"
}
```

Icons help identify port types visually.

---

# Example Board Visual Schema

Example visual definition for a controller board.

```
"visual": {

  "shape": "rectangle",

  "size": {
    "width": 240,
    "height": 160
  },

  "ports": [

    {
      "id": "stepper_x",
      "side": "left",
      "x": 10,
      "y": 40,
      "icon": "stepper",
      "label": "X"
    },

    {
      "id": "stepper_y",
      "side": "left",
      "x": 10,
      "y": 70,
      "icon": "stepper",
      "label": "Y"
    },

    {
      "id": "heater_0",
      "side": "right",
      "x": 230,
      "y": 60,
      "icon": "heater",
      "label": "HE0"
    },

    {
      "id": "thermistor_0",
      "side": "right",
      "x": 230,
      "y": 100,
      "icon": "thermistor",
      "label": "TH0"
    }

  ],

  "labels": [
    {
      "text": "Controller Board",
      "x": 120,
      "y": 10,
      "align": "center"
    }
  ]
}
```

---

# Motor Visual Schema

Motors are simpler devices.

Example:

```
"visual": {

  "shape": "circle",

  "size": {
    "width": 80,
    "height": 80
  },

  "ports": [
    {
      "id": "coil",
      "side": "bottom",
      "x": 40,
      "y": 80,
      "icon": "stepper"
    }
  ],

  "labels": [
    {
      "text": "Stepper Motor",
      "x": 40,
      "y": 10,
      "align": "center"
    }
  ]
}
```

---

# Canvas Rendering Rules

The renderer must:

• draw device shape
• place connectors
• place ports
• render labels
• attach wire anchors to ports

---

# Port Anchors

Ports create wire attachment points.

Example:

```
Board Port → Wire → Device Port
```

Wire routing originates from the port anchor position.

---

# Zoom-Level Behavior

Device visuals change depending on zoom level.

Zoomed Out:

Device icons only.

Medium Zoom:

Ports visible.

Close Zoom:

Connector details visible.

---

# Future Visual Features

Future improvements may include:

• board images
• component outlines
• animated signal flow
• connector pin visualization
• harness grouping

---

# Benefits

The visual schema allows Machine Builder to:

• render devices automatically
• support thousands of hardware devices
• avoid hardcoded UI layouts
• keep visuals synchronized with the hardware database
