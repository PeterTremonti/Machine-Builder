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

04/12/26 11:13pm - 
# Machine Builder

A modular machine design and wiring tool.

## 🚀 What It Does
- Visually place hardware components
- Connect ports with wires
- Build machine layouts interactively

## 🧠 Goal
To evolve into a full machine development platform:
- Wiring diagrams
- Hardware planning
- Firmware generation
- Simulation

---

## 🧩 Current Features
- Device rendering
- Drag & drop movement
- Port-based connections
- Orthogonal wire routing (in progress)

---

## ⚠️ Current Status
Version: **V7.9.3**

The wiring system is functional but under active redevelopment.

Known issues:
- Wire routing inconsistencies
- Geometry edge cases

---

## 🛠️ Next Version (V7.10)
- Complete rewrite of wiring engine
- Clean routing system
- Stable connection paths

---

## 📂 Project Structure
See:
Machine_Builder_Dev_Architecture.md

---

## 💡 Philosophy
This project is built around:
- Modularity
- Visual clarity
- Expandability

---

## 🔮 Future Plans
- Smart wiring suggestions
- Component libraries
- Firmware export (Klipper, Marlin, etc.)
- Simulation engine

---

## 🧪 Development Approach
- Build → Test → Break → Rebuild better
- Avoid patching broken systems
- Prefer clean architecture over quick fixes

---

## 🤝 Contributing
Currently a solo experimental project, but structured for future expansion.

---

## 📌 Note
This is not just a wiring tool.

It is the foundation of a **machine design ecosystem**.