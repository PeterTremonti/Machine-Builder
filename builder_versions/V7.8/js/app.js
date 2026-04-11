let devices = []

let active_device = null

let drag_offset_x = 0
let drag_offset_y = 0

window.onload = function()
{

init_canvas()

let button = document.getElementById("load_board")

button.onclick = async function()
{

let board = await load_hardware("../../hardware_database/boards/btt_octopus_v1_1.json")

devices.push({
data: board,
x:100,
y:100
})

render_scene()

}

canvas.addEventListener("mousedown",mouse_down)
canvas.addEventListener("mousemove",mouse_move)
canvas.addEventListener("mouseup",mouse_up)

}

function render_scene()
{

ctx.clearRect(0,0,canvas.width,canvas.height)

devices.forEach(device => {

draw_board(device.data,device.x,device.y)

})

}

function mouse_down(event)
{

let rect = canvas.getBoundingClientRect()

let mx = event.clientX - rect.left
let my = event.clientY - rect.top

devices.forEach(device => {

let w = device.data.visual.size.width
let h = device.data.visual.size.height

if(mx > device.x && mx < device.x+w && my > device.y && my < device.y+h)
{

active_device = device

drag_offset_x = mx - device.x
drag_offset_y = my - device.y

}

})

}

function mouse_move(event)
{

if(active_device == null) return

let rect = canvas.getBoundingClientRect()

let mx = event.clientX - rect.left
let my = event.clientY - rect.top

active_device.x = mx - drag_offset_x
active_device.y = my - drag_offset_y

render_scene()

}

function mouse_up()
{

active_device = null

}