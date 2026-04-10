let machineDevices=[]
let connections=[]
let mode="basic"

let connectMode=false
let startPort=null

const deviceDB=[

"Host Computer",
"Controller Board",
"Stepper Motor",
"Extruder",
"Hotend",
"Thermistor",
"Cooling Fan",
"Endstop",
"Probe"

]

const deviceSelect=document.getElementById("deviceSelect")

deviceDB.forEach(d=>{

let opt=document.createElement("option")
opt.value=d
opt.text=d
deviceSelect.appendChild(opt)

})

function addDevice(){

let name=deviceSelect.value

let device={

id:"dev"+Date.now(),
name:name,
x:120,
y:120,
ports:["A","B"]

}

machineDevices.push(device)

drawDevice(device)

updateList()

updateGraph()

log("Added "+name,"info")

}

function drawDevice(device){

let node=document.createElement("div")

node.className="deviceNode"

node.style.left=device.x+"px"
node.style.top=device.y+"px"

node.id=device.id

let title=document.createElement("div")
title.innerText=device.name

node.appendChild(title)

device.ports.forEach(p=>{

let port=document.createElement("div")

port.className="port"

port.onclick=function(e){

e.stopPropagation()

handlePortClick(device,p)

}

node.appendChild(port)

})

makeDraggable(node,device)

document.getElementById("canvas").appendChild(node)

}

function makeDraggable(element,device){

element.onmousedown=function(e){

let offsetX=e.clientX-device.x
let offsetY=e.clientY-device.y

document.onmousemove=function(e){

device.x=e.clientX-offsetX
device.y=e.clientY-offsetY

element.style.left=device.x+"px"
element.style.top=device.y+"px"

drawConnections()

}

document.onmouseup=function(){

document.onmousemove=null

}

}

}

function handlePortClick(device,port){

if(!startPort){

startPort={device,port}

log("Select destination port","info")

}else{

connections.push({

from:startPort,
to:{device,port}

})

startPort=null

drawConnections()

}

}

function drawConnections(){

document.querySelectorAll(".connection").forEach(c=>c.remove())

connections.forEach(c=>{

let from=document.getElementById(c.from.device.id)
let to=document.getElementById(c.to.device.id)

let x1=c.from.device.x+80
let y1=c.from.device.y+20

let x2=c.to.device.x
let y2=c.to.device.y+20

let line=document.createElement("div")

line.className="connection"

line.style.left=x1+"px"
line.style.top=y1+"px"

line.style.width=Math.hypot(x2-x1,y2-y1)+"px"

line.style.transform=`rotate(${Math.atan2(y2-y1,x2-x1)}rad)`

document.getElementById("canvas").appendChild(line)

})

}

function toggleMode(){

mode = mode==="basic" ? "advanced":"basic"

document.getElementById("modeLabel").innerText = mode

log("Mode switched to "+mode,"info")

}

function updateList(){

let list=document.getElementById("deviceList")

list.innerHTML=""

machineDevices.forEach(d=>{

let li=document.createElement("li")

li.innerText=d.name

list.appendChild(li)

})

}

function updateGraph(){

let graph=document.getElementById("graph")

graph.innerHTML=""

machineDevices.forEach(d=>{

let line=document.createElement("div")

line.innerText=d.name

graph.appendChild(line)

})

}

function runDiagnostics(){

let hotend=false
let therm=false

machineDevices.forEach(d=>{

if(d.name==="Hotend") hotend=true
if(d.name==="Thermistor") therm=true

})

if(hotend && !therm)

log("Hotend missing thermistor","error")

}

function log(msg,type){

let div=document.createElement("div")

div.className=type
div.innerText=msg

document.getElementById("console").appendChild(div)

}