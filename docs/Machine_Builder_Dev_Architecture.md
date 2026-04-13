# Machine Builder – Dev Architecture

## Folder Structure

builder_versions/
  V7.9/
    js/
      app.js
      canvas.js
      device_renderer.js
      wiring_renderer.js
      device_controller.js
      port_interaction.js
      connection_engine.js
      hardware_loader.js
      ui_console.js
    style.css

hardware_database/
  boards/
  motors/
  sensors/
  heaters/
  index.json per folder

assets/
  images/
  icons/

---

## Data Flow

hardware_loader → loads JSON  
↓
DeviceRenderer → draws devices  
↓
PortInteraction → detects clicks  
↓
ConnectionEngine → stores connections  
↓
WiringRenderer → draws connections  

---

## Current Problem Area

WiringRenderer:
- Mixing routing + entry/exit logic
- No clear path model
- No obstacle awareness

---

## Target Architecture (V7.10)

### Step 1: Anchor Points
Each connection:
- startPort
- endPort

### Step 2: Exit Points
- move OUT of device cleanly

### Step 3: Routing Space
- only route in “safe space”
- never inside device bounds

### Step 4: Path Generation
- orthogonal path
- deterministic

### Step 5: Render
- draw full path as segments

---

## Future Upgrade Path

V7.10 → stable routing  
V7.11 → wire selection + editing  
V7.12 → collision avoidance  
V8.0 → full layout engine