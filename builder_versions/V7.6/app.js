let machineDevices=[]
let connections=[]
let mode="basic"

const deviceDB=[
"Controller Board",
"Stepper Motor",
"Hotend",
"Cooling Fan",
"Thermistor",
"Endstop",
"Extruder",
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
x:100,
y:100
}

machineDevices.push(device)

drawDevice(device)

updateList()

log("Added device: "+name,"info")

updateGraph()
}

function drawDevice(device){

let div=document.createElement("div")

div.className="deviceNode"
div.innerText=device.name

div.style.left=device.x+"px"
div.style.top=device.y+"px"

div.id=device.id

makeDraggable(div,device)

document.getElementById("canvas").appendChild(div)

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

}

document.onmouseup=function(){
document.onmousemove=null
}

}

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

function toggleMode(){

mode = mode==="basic" ? "advanced":"basic"

log("Mode switched to "+mode,"info")

}

function runDiagnostics(){

let hasHotend=false
let hasThermistor=false
let hasFan=false

machineDevices.forEach(d=>{

if(d.name==="Hotend") hasHotend=true
if(d.name==="Thermistor") hasThermistor=true
if(d.name==="Cooling Fan") hasFan=true

})

if(hasHotend && !hasThermistor)
log("ERROR: Hotend missing thermistor","error")

if(hasHotend && !hasFan)
log("WARNING: Hotend cooling fan missing","warn")

if(hasHotend && hasThermistor && hasFan)
log("Hotend system OK","info")

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

function log(msg,type){

let div=document.createElement("div")

div.className=type
div.innerText=msg

document.getElementById("console").appendChild(div)

}