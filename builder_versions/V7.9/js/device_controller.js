import {canvas} from "./canvas.js"

export class DeviceController
{

constructor(renderer)
{
this.renderer=renderer
this.dragging=null

canvas.addEventListener("mousedown",e=>this.mouseDown(e))
canvas.addEventListener("mousemove",e=>this.mouseMove(e))
canvas.addEventListener("mouseup",()=>this.mouseUp())
}

mouseDown(e)
{

const x = e.offsetX
const y = e.offsetY

for(const device of this.renderer.devices)
{

const hw=this.renderer.hardware[device.type]

if(
x>device.x &&
x<device.x+hw.visual.size.width &&
y>device.y &&
y<device.y+hw.visual.size.height
)
{
this.dragging=device
this.offsetX = x-device.x
this.offsetY = y-device.y
return
}

}

}

mouseMove(e)
{

if(!this.dragging) return

const x = e.offsetX
const y = e.offsetY

this.dragging.x = x - this.offsetX
this.dragging.y = y - this.offsetY

}

mouseUp()
{
this.dragging=null
}

}