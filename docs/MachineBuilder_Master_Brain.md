# Machine Builder – Master Brain File

Project Name:
Machine Builder

Purpose:
A visual hardware configuration tool for building machines such as:

- 3D Printers
- CNC Routers
- Laser Engravers
- Motion Systems
- Robotics Platforms

The system allows users to:

• Add hardware devices
• Connect them to controller boards
• Generate wiring diagrams
• Validate hardware compatibility
• Generate firmware configurations

Future goal:
Become a CAD-like system for machine architecture.

---

CORE FEATURES

Device Builder
Users add hardware components such as:

- Controller boards
- Stepper drivers
- Steppers
- Hotends
- Fans
- Thermistors
- Endstops
- Probes
- Displays
- Power supplies

Each device has ports.

Ports connect to other device ports.

Connections form the machine graph.

---

Machine Graph

The machine is internally represented as:

Nodes = devices
Edges = connections

Example:

Octopus Board
 ├ STEP0 → X Motor
 ├ STEP1 → Y Motor
 ├ HE0 → Hotend
 ├ TH0 → Thermistor
 └ FAN0 → Cooling Fan

---

Connection Modes

Fast Mode

Drag device → connect cable between ports.

No wiring detail.

Used for quick planning.

---

Basic Mode

Connections include:

• cable type
• wire count
• direction

---

Advanced Mode

Connections include:

• pin mapping
• wire colors
• voltage
• current limits
• UART/SPI/I2C details

---

Firmware Targets

Machine Builder will generate configuration for:

Klipper  
Marlin  
RepRapFirmware  
GRBL

---

Hardware Database

The system will include a hardware database.

Database sources include:

Marlin pins files
Klipper configs
GRBL cpu maps
Manufacturer documentation

Database structure:

hardware_database/

 boards/
 devices/
 motion/

Example board file:

btt_octopus_v1_1.json

Example device file:

hotend_generic.json

---

Firmware Source Archive

Raw firmware data stored separately.

firmware_sources/

 marlin/
 klipper/
 grbl/

These are parsed later.

---

Project Architecture

MachineBuilder/

 index.html

 js/
   app.js
   deviceDB.js
   wiring.js
   diagnostics.js

 css/
   style.css

 hardware_database/

 firmware_sources/

 docs/

---

Future Major Systems

Visual Machine Canvas

Drag devices onto workspace.

Ports appear visually.

Connections drawn between ports.

---

Connection Graph Engine

Internal representation:

devices[]
connections[]

Used for:

• diagnostics
• firmware generation
• wiring diagrams

---

Diagnostics Engine

Detects problems like:

missing thermistor
missing cooling fan
invalid pin usage
power overload
duplicate pin assignment

---

Firmware Generator

Exports machine configuration files for:

Klipper
Marlin
RepRapFirmware
GRBL

---

Long Term Vision

Machine Builder becomes:

Machine Design Environment

similar to:

• electronic CAD
• mechanical CAD

but focused on machine architecture.