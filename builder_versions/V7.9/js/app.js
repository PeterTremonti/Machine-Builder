import {init_canvas} from "./canvas.js"
import {DeviceRenderer} from "./device_renderer_v79.js"
import {ConnectionEngine} from "./connection_engine.js"
import {WiringRenderer} from "./wiring_renderer.js"
import {PortInteraction} from "./port_interaction.js"
import {loadHardwareDatabase} from "./hardware_loader.js"
import {DeviceController} from "./device_controller.js"


let deviceRenderer
let wiringRenderer
let connectionEngine

async function start()
{

init_canvas()

const hardware = await loadHardwareDatabase()

deviceRenderer = new DeviceRenderer(hardware)

new DeviceController(deviceRenderer)

connectionEngine = new ConnectionEngine()

wiringRenderer = new WiringRenderer(connectionEngine,deviceRenderer)

new PortInteraction(connectionEngine, deviceRenderer)

deviceRenderer.spawnDevice("btt_octopus_v1_1",200,200)
deviceRenderer.spawnDevice("nema17", 50, 100)
deviceRenderer.spawnDevice("nema17", 50, 200)
deviceRenderer.spawnDevice("nema17", 50, 300)
deviceRenderer.spawnDevice("nema17", 50, 400)
deviceRenderer.spawnDevice("hotend", 500, 200)
deviceRenderer.spawnDevice("thermistor", 500, 300)

renderLoop()

}

function renderLoop()
{

deviceRenderer.draw()

wiringRenderer.draw()

requestAnimationFrame(renderLoop)

}

start()