import {init_canvas} from "./canvas.js"
import {DeviceRenderer} from "./device_renderer_v79.js"
import {DeviceController} from "./device_controller.js"
import {PortInteraction, connectionEngine} from "./port_interaction.js"
import {WiringRenderer} from "./wiring_renderer.js"

let renderer
let wiringRenderer

async function start()
{

init_canvas()

const response = await fetch("../hardware_database/boards/btt_octopus_v1_1.json")
const octopus = await response.json()

const hardware = {
btt_octopus_v1_1: octopus
}

renderer = new DeviceRenderer(hardware)

new DeviceController(renderer)
new PortInteraction(renderer)

wiringRenderer = new WiringRenderer(connectionEngine, renderer)

renderer.spawnDevice("btt_octopus_v1_1",200,200)

loop()

}

function loop()
{
renderer.draw()
wiringRenderer.draw()
requestAnimationFrame(loop)
}

start()