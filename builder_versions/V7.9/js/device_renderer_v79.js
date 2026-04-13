import {ctx} from "./canvas.js"

export class DeviceRenderer
{

constructor(hardware)
{
this.hardware = hardware
this.devices = []
}

spawnDevice(type,x,y)
{
this.devices.push({
id:crypto.randomUUID(),
type,
x,
y
})
}

draw()
{
ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height)

this.devices.forEach(device=>{

const hw = this.hardware[device.type]
if(!hw) return

ctx.fillStyle="#333"
ctx.fillRect(device.x,device.y,hw.visual.size.width,hw.visual.size.height)

ctx.strokeStyle="#999"
ctx.strokeRect(device.x,device.y,hw.visual.size.width,hw.visual.size.height)

// board label
ctx.fillStyle = "#ffffff"
ctx.font = "12px Arial"
ctx.textAlign = "left"
ctx.fillText(hw.name, device.x + 10, device.y + 15)

// ports
hw.visual.ports.forEach(port=>{

const px=device.x+port.x
const py=device.y+port.y

ctx.beginPath()
ctx.arc(px,py,6,0,Math.PI*2)
ctx.fillStyle="#00aaff"
ctx.fill()

ctx.fillStyle="#ffffff"
ctx.font="10px Arial"

if(port.side==="right")
{
ctx.textAlign="right"
ctx.fillText(port.label,px-8,py+4)
}
else
{
ctx.textAlign="left"
ctx.fillText(port.label,px+8,py+4)
}

})

})
}

// 🔴 CRITICAL FUNCTION (this is what was "missing")
findPortAt(x,y)
{

for(const device of this.devices)
{

const hw=this.hardware[device.type]

for(const port of hw.visual.ports)
{

const px=device.x+port.x
const py=device.y+port.y

const dx=x-px
const dy=y-py

const dist=Math.sqrt(dx*dx+dy*dy)

if(dist<8)
{
    console.log("CLICKED PORT:", port.id, "SIDE:", port.side)

    return {
        deviceId: device.id,
        portId: port.id,
        portType: this.getPortType(hw,port.id),

        // ADD THIS LINE
        side: port.side
    }
}

}

}

return null

}

getPortType(hw,portId)
{
const port=hw.ports.find(p=>p.id===portId)
return port ? port.type : "unknown"
}

getPortPosition(deviceId,portId)
{

for(const device of this.devices)
{

if(device.id!==deviceId) continue

const hw=this.hardware[device.type]

const port=hw.visual.ports.find(p=>p.id===portId)

if(!port) return null

return {
x:device.x+port.x,
y:device.y+port.y
}

}

return null

}

}