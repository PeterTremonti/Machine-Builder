# Machine Builder

Machine Builder is a visual hardware configuration tool for designing machines such as:

- 3D printers
- CNC routers
- Laser engravers
- motion systems
- robotics platforms

The tool allows users to assemble machines from hardware components and visualize how they connect.

Future goals include:

- wiring diagram generation
- hardware compatibility checks
- automatic firmware configuration generation

Supported firmware targets (planned):

- Klipper
- Marlin
- RepRapFirmware
- GRBL

---

## Project Structure

Machine-Builder/

builder_versions/
  versioned releases of the builder

firmware_sources/
  raw firmware configuration data used to build the hardware database

hardware_database/
  structured hardware definitions used by the builder

docs/
  design documentation and project notes

---

## Current Status

Active development.

Current version: 7.5

Next planned version: 7.6 (visual machine canvas).