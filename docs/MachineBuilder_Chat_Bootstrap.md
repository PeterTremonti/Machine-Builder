Project: Machine Builder

Purpose:
Visual hardware configuration tool for building machines such as 3D printers, CNC routers, laser engravers, and robotics platforms.

Current Version:
7.5

Next Version:
7.6

Major features already implemented:

• device database
• device selection
• device list
• console logging
• diagnostics
• basic/advanced modes
• initial board rendering

Next development goals:

Version 7.6

Add visual machine builder.

Features:

• device icons
• drag devices onto canvas
• visible ports
• drag connections between ports
• wiring visualization
• machine graph panel

Connection Modes:

Fast Mode
simple cable between ports

Basic Mode
adds wiring details

Advanced Mode
adds pin and electrical data

Future plans include:

hardware database
firmware generators
machine diagnostics engine
automatic configuration generation for

Klipper
Marlin
RepRapFirmware
GRBL

Hardware database sources:

Marlin pins folder
Klipper config folder
GRBL cpu_map

These will be downloaded and stored in:

firmware_sources/

for parsing later.

Goal:
Build a reusable machine planning tool usable for all future builds.