import {log} from "./ui_console.js"
import {canvas} from "./canvas.js"

export class PortInteraction
{

constructor(connectionEngine, deviceRenderer)
{

canvas.addEventListener("click",(event)=>{

const rect = canvas.getBoundingClientRect()

const x = (event.clientX - rect.left) * (canvas.width / rect.width)
const y = (event.clientY - rect.top) * (canvas.height / rect.height)

log(`click at ${Math.round(x)}, ${Math.round(y)}`)

const port = deviceRenderer.findPortAt(x,y)

if(!port)
{
log("no port detected")
return
}

log(`clicked port: ${port.portId}`)

if(!connectionEngine.pendingPort)
{
log("starting connection")
connectionEngine.begin(port)
}
else
{
log("completing connection")
connectionEngine.tryComplete(port)
}

})

}

}