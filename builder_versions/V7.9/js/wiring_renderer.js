import {ctx} from "./canvas.js"

export class WiringRenderer
{

constructor(connectionEngine, deviceRenderer)
{
this.engine = connectionEngine
this.renderer = deviceRenderer
}

draw()
{

const connections = this.engine.getConnections()

const margin = 40 // distance to stay away from devices

function pushOut(point, dir)
{
    if(dir === "left")  return {x: point.x - margin, y: point.y}
    if(dir === "right") return {x: point.x + margin, y: point.y}
    if(dir === "top")   return {x: point.x, y: point.y - margin}
    if(dir === "bottom")return {x: point.x, y: point.y + margin}
}

connections.forEach(conn => {

const a = this.renderer.getPortPosition(conn.from.deviceId, conn.from.portId)
const b = this.renderer.getPortPosition(conn.to.deviceId, conn.to.portId)

if(!a || !b) return

const dirA = this.getPortSide(conn.from)
const dirB = this.getPortSide(conn.to)

const offset = 30

// ✅ true directional exits
const exitA = this.getExitPoint(a, dirA, offset)
const exitB = this.getExitPoint(b, dirB, offset)
const safeA = pushOut(exitA, dirA)
const safeB = pushOut(exitB, dirB)

ctx.strokeStyle = "#00ffff"
ctx.lineWidth = 2
ctx.beginPath()

// start routing from safe zone, not port
ctx.moveTo(safeA.x, safeA.y)


// 🚨 CRITICAL CHANGE: NO midpoint averaging anymore

// horizontal-first path
if(dirA === "left" || dirA === "right")
{
    ctx.lineTo(safeB.x, safeA.y)
}
// vertical-first path
else
{
    ctx.lineTo(safeA.x, safeB.y)
}

// go to safeB
ctx.lineTo(safeB.x, safeB.y)

// final clean entry into port B
ctx.lineTo(exitB.x, exitB.y)
ctx.lineTo(b.x, b.y)

ctx.stroke()

})

}

// ===============================
// HELPERS
// ===============================

getExitPoint(p, side, offset)
{
switch(side)
{
case "left": return {x:p.x-offset,y:p.y}
case "right": return {x:p.x+offset,y:p.y}
case "top": return {x:p.x,y:p.y-offset}
case "bottom": return {x:p.x,y:p.y+offset}
default: return {...p}
}
}

getPortSide(port)
{
    return port.side || "right"
}

}