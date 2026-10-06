# Machine Builder – Chat Bootstrap

This document is used to restore project context when starting a new ChatGPT session.

The Machine Builder project is a visual machine configuration tool used to design machines such as:

• 3D printers
• CNC machines
• robotics systems

The system allows users to:

• add hardware devices
• connect them visually
• generate firmware configurations
• validate machine designs

Core architecture is described in:

MachineBuilder_Master_Brain.md

Additional system specifications exist in:

docs/architecture
docs/ui

When starting a new conversation, load these documents to restore project knowledge and continue development without losing design decisions.


04/12/26 11:11pm - 
# Machine Builder – Chat Bootstrap (V7.9.3+)

## Current State
We are building a modular machine design tool focused on:
- Wiring diagrams
- Hardware layout
- Future firmware/config generation

The system currently supports:
- Device spawning
- Port detection
- Click-to-connect wiring
- Dragging devices
- Orthogonal (90°) wire routing

## Current Problems
Wiring renderer is unstable:
- Floating wire legs
- Incorrect entry/exit behavior
- Wires passing through devices
- Geometry breaks depending on click order

Root issue:
Routing logic is layered incorrectly instead of being designed as a path system.

## Immediate Goal
Rebuild wiring renderer using a clean routing model:
1. Ports define anchor points
2. Wires route ONLY through safe space
3. Entry/exit handled as separate step
4. No conditional hacks

## Rules Going Forward
- Always provide FULL FILE replacements (no snippets unless trivial)
- Prioritize stability over cleverness
- Build systems, not patches
- Every feature must be debuggable visually

## Next Target Version
V7.10 – Clean Routing Engine